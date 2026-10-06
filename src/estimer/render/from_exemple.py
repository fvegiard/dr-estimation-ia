"""Build a renderer input directory from a gold EXEMPLE relevé (HR26-14) - used to prove the renderer.

python -m src.estimer.render.from_exemple EXEMPLE.pdf bordereau-materiel.csv feuilles.csv OUT_DIR [--reserves reserves.md]

EXEMPLE.pdf is the target relevé: original vector plan pages + a PyMuPDF overlay drawn in optional-content
layers named "RELEVE ...". For every sheet of feuilles.csv (materiel, agrege, travaux) this tool writes:
  OUT_DIR/plans.pdf        the plan pages with the RELEVE overlay removed (= the original drawing, still vector)
  OUT_DIR/estimate.json    one element per gold marker: centre, bbox, shape, colour, label detail lines, flags
  OUT_DIR/bordereau.csv    materiel rows (gold CSV), corrected
  OUT_DIR/familles.csv     agrege / travaux rows read cell by cell from the EXEMPLE bordereau, corrected
  OUT_DIR/feuilles.json    sheet -> bordereau format
  OUT_DIR/reserves.md      reserves / notes of every sheet, corrected
  OUT_DIR/corrections.json every correction applied to the EXEMPLE text (rule, before, after)
  OUT_DIR/provenance.json  input sha256 + per-sheet marker/row reconciliation
Nothing is invented: every position comes from the EXEMPLE overlay, every text from the gold CSV.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import pymupdf

from . import corrections_exemple as C
from . import tableau as T

OC_RE = re.compile(rb"/OC\s*/(\w+)\s*BDC")
NUM = r"-?\d+(?:\.\d+)?|-?\.\d+"
TJ_RE = re.compile(rb"\[<([0-9a-fA-F]+)>\]TJ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def releve_mc_names(doc: pymupdf.Document, page: pymupdf.Page) -> set[str]:
    """Property names (MC0, MC1, ...) of `page` that point to an OCG whose name starts with RELEVE."""
    kind, val = doc.xref_get_key(page.xref, "Resources/Properties")
    if kind == "xref":
        props = doc.xref_object(int(val.split()[0]))
    elif kind == "dict":
        props = val
    else:
        return set()
    out = set()
    for name, xref in re.findall(r"/(\w+)\s+(\d+)\s+0\s+R", props):
        m = re.search(r"/Name\s*\((.*?)\)", doc.xref_object(int(xref)))
        if m and m.group(1).startswith("RELEVE"):
            out.add(name)
    return out


def overlay_split(doc: pymupdf.Document, page: pymupdf.Page) -> tuple[list[int], list[bytes]]:
    """(content xrefs of the original drawing, overlay stream bodies in drawing order)."""
    mcs = releve_mc_names(doc, page)
    base, overlay = [], []
    for x in page.get_contents():
        s = doc.xref_stream(x)
        m = OC_RE.search(s)
        if m and m.group(1).decode() in mcs:
            overlay.append(s)
        else:
            base.append(x)
    return base, overlay


def _shape_bbox(s: str, page_h: float):
    """Marker geometry from one overlay path stream -> (shape, bbox top-left origin)."""
    body = s.split("BDC", 1)[1]
    m = re.search(rf"({NUM})\s+({NUM})\s+({NUM})\s+({NUM})\s+re", body)
    if m:
        x, y, w, h = map(float, m.groups())
        return "rect", (x, page_h - (y + h), x + w, page_h - y)
    pts, ops, nums = [], [], []
    for tok in body.split():
        if re.fullmatch(NUM, tok):
            nums.append(float(tok))
            continue
        if tok in ("m", "l", "c"):
            ops.append(tok)
            pts.extend(zip(nums[0::2], nums[1::2]))
        nums = []
    if not pts:
        return None, None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    # EXEMPLE : triangle pointe en haut (3 sommets) sur E01/E06/E09/E12/EU01-04, losange (4 sommets) sur
    # E03/E04/E05/E08/E11/E14 et EU02-04 (docs/FORMAT-EXEMPLE.md, pastilles par format)
    sommets = {(round(px, 2), round(py, 2)) for px, py in pts}
    kind = "circle" if "c" in ops else ("triangle" if len(sommets) == 3 else "diamond")
    return kind, (min(xs), page_h - max(ys), max(xs), page_h - min(ys))


LABEL_SIZES = (b"/helv 4.8 Tf", b"/helv 5.2 Tf")   # 5.2: étiquettes PL des feuilles E03/E04/E05/E08/E11/E14
RG_RE = re.compile(rb"(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+RG")


def read_markers(doc: pymupdf.Document, pno: int) -> list[dict]:
    """Gold markers of plan page `pno` (0-based): each = shape stream, leader, white box, label text.

    The label may have detail lines under the repère (power, circuit: "CH-01" / "1250 W S25,27"); they are
    returned in `extra`. `color` is the marker stroke colour."""
    page = doc[pno]
    H = page.rect.height
    _, ov = overlay_split(doc, page)
    out = []
    for i, s in enumerate(ov):
        if i < 3 or not any(k in s for k in LABEL_SIZES) or b"BT" not in s:
            continue
        texts = [bytes.fromhex(t.decode()).decode("latin-1") for t in TJ_RE.findall(s)]
        shape, bbox = _shape_bbox(ov[i - 3].decode("latin-1"), H)
        if bbox is None or not texts:
            continue
        cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
        m = RG_RE.search(ov[i - 3])
        color = [round(float(v), 6) for v in m.groups()] if m else None
        mk = {"repere": texts[0], "extra": texts[1:], "shape": shape, "color": color,
              "x": round(cx, 3), "y": round(cy, 3), "bbox": [round(v, 3) for v in bbox]}
        if b"/helv 5.2 Tf" in s:
            mk["label_size"] = 5.2                       # étiquettes PL des feuilles en palette B
        box = re.search(rf"({NUM})\s+({NUM})\s+({NUM})\s+({NUM})\s+re", ov[i - 1].decode("latin-1"))
        if box:
            x, y, w, h = map(float, box.groups())
            mk["label_bbox"] = [round(x, 3), round(H - (y + h), 3), round(x + w, 3), round(H - y, 3)]
        lead = re.findall(rf"({NUM})\s+({NUM})\s+[ml]\b", ov[i - 2].decode("latin-1"))
        if len(lead) >= 2:
            mk["leader_end"] = [round(float(lead[-1][0]), 3), round(H - float(lead[-1][1]), 3)]
        out.append(mk)
    return out


BOX_BORDER_RGB = (0.25, 0.3, 0.35)


def read_box_rect(page: pymupdf.Page) -> list[float] | None:
    """Rectangle de l'encadré RELEVE de l'EXEMPLE (bordure gris-bleu 0,7 pt, fond blanc)."""
    best = None
    for d in page.get_drawings():
        c = d.get("color")
        if c and all(abs(a - b) < 0.02 for a, b in zip(c, BOX_BORDER_RGB)) and d.get("fill") == (1.0, 1.0, 1.0):
            r = d["rect"]
            if best is None or r.width * r.height > best.width * best.height:
                best = r
    return [round(v, 3) for v in best] if best else None


def strip_overlay(doc: pymupdf.Document, pno: int) -> None:
    """Remove the RELEVE overlay streams (and their layer properties) from page `pno`, in place."""
    page = doc[pno]
    mcs = releve_mc_names(doc, page)
    base, _ = overlay_split(doc, page)
    doc.xref_set_key(page.xref, "Contents", "[" + " ".join(f"{x} 0 R" for x in base) + "]")
    for name in mcs:
        doc.xref_set_key(page.xref, f"Resources/Properties/{name}", "null")


def _props_refs(doc: pymupdf.Document, xref: int) -> set[int]:
    kind, val = doc.xref_get_key(xref, "Resources/Properties")
    if kind == "xref":
        val = doc.xref_object(int(val.split()[0]))
    elif kind != "dict":
        return set()
    return {int(x) for x in re.findall(r"(\d+)\s+0\s+R", val)}


def prune_ocgs(doc: pymupdf.Document) -> int:
    """Drop from the catalog's /OCProperties every OCG no page (or page-level form XObject) refers to."""
    cat = doc.pdf_catalog()
    kind, ocp = doc.xref_get_key(cat, "OCProperties")
    if kind != "dict":
        return 0
    used: set[int] = set()
    for page in doc:
        used |= _props_refs(doc, page.xref)
        for xo in page.get_xobjects():
            used |= _props_refs(doc, xo[0])
    listed = {int(x) for x in re.findall(r"(\d+)\s+0\s+R", ocp)}
    drop = {x for x in listed - used if "/OCG" in doc.xref_get_key(x, "Type")[1]}
    new = re.sub(r"(\d+)\s+0\s+R", lambda m: "" if int(m.group(1)) in drop else m.group(0), ocp)
    doc.xref_set_key(cat, "OCProperties", new)
    return len(drop)




# ---------------------------------------------------------------- toutes les feuilles (26 sur HR26-14)
HEADER_RE = re.compile(r"(\d+) reperes / (\d+) familles(?: / RES (\d+))?")
DIVERGENCES_RE = re.compile(r"(\d+) divergences plan/cedule A RESOUDRE")
CALIBRES_RE = re.compile(r"(\d+) calibres distincts dans les sources")
CODE_RE = re.compile(r"[A-Z]+\d*")
QTY_RE = re.compile(r"^(\d+(?:\.\d+)?)(?: / R(\d+))?$")
MAT_TEXT = ("materiel", "designation", "portee", "modele", "prescription")
FAM_TEXT = ("famille", "portee", "modele", "prescription", "source")


def read_header(page: pymupdf.Page) -> dict:
    """Compteurs de l'encadré RELEVE de l'EXEMPLE : reperes, familles, RES (absent dans l'encadré v6)."""
    return read_header_text(page.get_text())


def read_header_text(text: str) -> dict:
    m = HEADER_RE.search(text)
    if not m:
        return {}
    return {"reperes": int(m.group(1)), "familles": int(m.group(2)),
            "res": int(m.group(3)) if m.group(3) else None}


def read_legend(page: pymupdf.Page) -> dict[str, list]:
    """Légende de l'encadré : code famille -> [qte, R] (R = None quand l'encadré n'affiche pas les réserves).

    Encadré standard : code gras 8,2 pt + quantité 7,1 pt ; encadré v6 (E03/E04/E05/E08) : 10 pt / 10 pt."""
    spans = [sp for b in page.get_text("dict")["blocks"] for line in b.get("lines", []) for sp in line["spans"]
             if sp["font"].startswith("Helvetica")]
    out = {}
    for sp in spans:
        if "Bold" not in sp["font"] or not CODE_RE.fullmatch(sp["text"]):
            continue
        size = sp["size"]
        qsize = 7.1 if abs(size - 8.2) < 0.05 else (10.0 if abs(size - 10.0) < 0.05 else None)
        if qsize is None:
            continue
        o = sp["origin"]
        near = sorted((q["origin"][0] - o[0], q["text"]) for q in spans
                      if "Bold" not in q["font"] and abs(q["size"] - qsize) < 0.05
                      and abs(q["origin"][1] - o[1]) < 0.6 and q["origin"][0] > o[0] and QTY_RE.match(q["text"]))
        if near:
            m = QTY_RE.match(near[0][1])
            out[sp["text"]] = [float(m.group(1)), int(m.group(2)) if m.group(2) else (0 if qsize == 7.1 else None)]
    return out


def _glyph_shape(d: dict) -> str:
    ops = [i[0] for i in d["items"]]
    if "re" in ops:
        return "rect"
    if "c" in ops:
        return "circle"
    return "triangle" if len(ops) == 3 else "diamond"


def read_legend_glyphs(page: pymupdf.Page, box: list[float] | None):
    """Glyphes de légende de l'EXEMPLE : {code: forme} et (décalage de la 1re ligne, pas) dans l'encadré."""
    if not box:
        return {}, None
    br = pymupdf.Rect(box)
    glyphs = [d for d in page.get_drawings() if d.get("fill") and d["rect"] in br and 6 < d["rect"].width < 14
              and abs(d["rect"].width - d["rect"].height) < 1.5]
    spans = [sp for b in page.get_text("dict")["blocks"] for line in b.get("lines", []) for sp in line["spans"]
             if "Bold" in sp["font"] and CODE_RE.fullmatch(sp["text"]) and pymupdf.Point(sp["origin"]) in br]
    shapes, cys, gxs = {}, [], []
    for sp in spans:
        ox, oy = sp["origin"]
        near = [d for d in glyphs if 0 < ox - d["rect"].x1 < 20 and abs((d["rect"].y0 + d["rect"].y1) / 2 - (oy - 3)) < 4]
        if near:
            g = min(near, key=lambda d: ox - d["rect"].x1)
            shapes[sp["text"]] = _glyph_shape(g)
            cys.append(round((g["rect"].y0 + g["rect"].y1) / 2, 2))
            gxs.append(round(g["rect"].x0))
    ys = sorted(set(cys))
    steps = [b - a for a, b in zip(ys, ys[1:]) if b - a > 3]
    ncols = len({x // 5 for x in gxs})
    rows = (round(ys[0] - br.y0, 3), round(min(steps), 3) if steps else 0.0, ncols) if ys else None
    return shapes, rows


def corriger_table(name: str, fmt: str, table: dict, journal: list) -> tuple[list[dict], list[str]]:
    """Lignes de famille et notes d'une feuille agrégée / travaux de l'EXEMPLE, corrigées et journalisées."""
    rows = []
    for r in table["rows"]:
        n = r.get("qte") or r.get("lieux") or "0"
        ctx = {"code": r["id"], "n": int(float(n)) if re.fullmatch(r"\d+(\.\d+)?", n) else 0}
        rows.append(C.corriger_ligne(name, r, FAM_TEXT, ctx, journal))
    notes = [C.corriger_cellule(name, "notes", "notes", line, {}, journal) for line in table["notes"]]
    return rows, notes


def corriger_materiel(name: str, rows: list[dict], reserves: list[str], journal: list):
    rows = [C.corriger_ligne(name, r, MAT_TEXT, {}, journal) for r in rows]
    res = [C.corriger_cellule(name, "reserves", "reserves", line, {}, journal) for line in reserves]
    return rows, res


def build(exemple: Path, bordereau_csv: Path | None, feuilles_csv: Path, out_dir: Path,
          reserves_md: Path | None = None, log=print) -> dict:
    """Entrée du moteur de rendu pour TOUTES les feuilles de feuilles.csv (materiel, agrege, travaux)."""
    from .data import read_reserves_md

    out_dir.mkdir(parents=True, exist_ok=True)
    feuilles = sorted(csv.DictReader(open(feuilles_csv, newline="", encoding="utf-8")), key=lambda r: int(r["page"]))
    mat_rows = list(csv.DictReader(open(bordereau_csv, newline="", encoding="utf-8"))) if bordereau_csv else []
    fields = list(mat_rows[0].keys()) if mat_rows else ["feuille", "repere", "source", "materiel", "designation",
                                                        "qte", "portee", "modele", "prescription", "parent"]
    res_md = read_reserves_md(reserves_md) if reserves_md else {}

    src = pymupdf.open(exemple)
    bords = T.sheet_bordereaux(src)
    journal: list = []
    sheets, counters, recon, meta = [], defaultdict(list), [], []
    out_mat, out_fam, reserves_out = [], [], {}
    for i, f in enumerate(feuilles):
        name, pno = f["feuille"], int(f["page"]) - 1
        page = src[pno]
        W, H = page.rect.width, page.rect.height
        fmt = bords.get(name, {}).get("format", "materiel")
        marks = read_markers(src, pno)
        legend = read_legend(page)
        head = read_header(page)
        famname, gold, modele_legende = {}, {}, {}
        if fmt == "materiel":
            rows, res = corriger_materiel(name, [r for r in mat_rows if r["feuille"] == name],
                                          res_md.get(name, []), journal)
            gold = {r["repere"]: r for r in rows}
            out_mat += [dict(r, format="materiel") for r in rows]
            n_rows = len(rows)
        else:
            table = T.read_table([src[p] for p in bords[name]["pages"]], fmt)
            rows, res = corriger_table(name, fmt, table, journal)
            for r in rows:
                famname.setdefault(r["id"], r["famille"])
                mod = r.get("modele", "").split("\n")[-1].strip()
                if mod and mod != C.MODELE_NON_INDIQUE:
                    modele_legende.setdefault(r["id"], mod)
                out_fam.append(dict(r, feuille=name, format=fmt))
            n_rows = len(rows)
        reserves_out[name] = res
        by_code = defaultdict(list)
        for m in marks:
            by_code[m["repere"].rstrip("*").rsplit("-", 1)[0]].append(m)
        seen = defaultdict(int)
        for code, ms in by_code.items():
            ms.sort(key=lambda m: int(re.sub(r"\D", "", m["repere"].rsplit("-", 1)[1]) or 0))
            q_r = legend.get(code)
            for k, m in enumerate(ms):
                rep = m["repere"].rstrip("*")
                seen[rep] += 1
                row = gold.get(rep)
                mat = row["materiel"] if row else famname.get(code, code)
                reserve = None if not q_r or q_r[1] is None else k < q_r[1]
                el = {"sheet": name, "page": i + 1, "x": m["x"], "y": m["y"], "bbox": m["bbox"],
                      "shape": m["shape"], "repere": rep, "source": row["source"] if row else "", "code": code,
                      "flags": ["revalider"] if m["repere"].endswith("*") else [], "color": m["color"],
                      "label_lines": m["extra"]}
                for key in ("label_bbox", "leader_end", "label_size"):
                    if key in m:
                        el[key] = m[key]
                if head and head.get("res") is None and code in modele_legende:
                    el["modele_legende"] = modele_legende[code]      # encadré v6 : ligne modèle sous le nom
                if reserve is not None:
                    el["reserve"] = reserve
                counters[(code, mat)].append(el)
        missing = sorted(set(gold) - set(seen)) if gold else []
        extra = sorted(set(seen) - set(gold)) if gold else sorted(c for c in by_code if c not in famname)
        recon.append({"sheet": name, "format": fmt, "exemple_page": pno + 1,
                      "exemple_bordereau_pages": [p + 1 for p in bords.get(name, {}).get("pages", [])],
                      "markers": len(marks), "rows": n_rows, "missing_markers": missing,
                      "markers_without_row": extra, "header": head, "legend": legend,
                      "header_reperes": f.get("reperes", ""), "header_res": f.get("res", "")})
        log(f"{name} ({fmt}): page {pno + 1}, {len(marks)} marqueurs, {n_rows} lignes"
            + (f", sans ligne {extra}" if extra else "") + (f", manquants {missing}" if missing else ""))
        sheets.append({"page": i + 1, "sheet": name, "width_px": W, "height_px": H, "raster_source": "vector",
                       "exemple_page": pno + 1, "box_hint": read_box_rect(page)})
        shp, rows_geo = read_legend_glyphs(page, sheets[-1]["box_hint"])
        sheets[-1]["legend_shapes"] = shp
        sheets[-1]["legend_rows"] = rows_geo
        text = page.get_text()
        for key, rx in (("divergences", DIVERGENCES_RE), ("calibres", CALIBRES_RE)):   # lignes rouges v6
            m = rx.search(text)
            if m:
                sheets[-1][key] = int(m.group(1))
        meta.append({"sheet": name, "format": fmt, "exemple_page": pno + 1,
                     "note": "LOGEMENTS TYPES" if "feuille de logements types" in text else ""})
        strip_overlay(src, pno)

    src.select([int(f["page"]) - 1 for f in feuilles])
    dropped = prune_ocgs(src)
    src.set_toc([])
    src.save(out_dir / "plans.pdf", garbage=3, deflate=True)
    log(f"plans.pdf: {src.page_count} pages, {dropped} calques RELEVE/inutilises retires")

    est = {
        "format": "dupuis-family-counts/1", "source_pdf": "plans.pdf",
        "note": "Gold HR26-14 positions read from the EXEMPLE.pdf RELEVE overlay (x, y = marker centre in PDF "
                "points, top-left origin; width_px/height_px = page size in points).",
        "sheets": sheets,
        "counters": [{"group_id": k + 1, "name": mat, "family": code, "quantity": len(els), "elements": els}
                     for k, ((code, mat), els) in enumerate(counters.items())],
    }
    (out_dir / "estimate.json").write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(out_dir / "bordereau.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields + (["format"] if "format" not in fields else []))
        w.writeheader()
        w.writerows(out_mat)
    if out_fam:
        with open(out_dir / "familles.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FAM_FIELDS, extrasaction="ignore")
            w.writeheader()
            w.writerows(out_fam)
    (out_dir / "feuilles.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(out_dir / "reserves.md", "w", encoding="utf-8") as fh:
        fh.write("# Reserves (EXEMPLE HR26-14, corrigees)\n")
        for name, lines in reserves_out.items():
            if lines:
                fh.write(f"\n## {name}\n" + "".join(f"{line}\n" for line in lines))
    (out_dir / "corrections.json").write_text(json.dumps({"resume": C.resume(journal), "corrections": journal},
                                                         ensure_ascii=False, indent=1), encoding="utf-8")
    prov = {"inputs": {str(p.name): sha256(p) for p in [exemple, feuilles_csv]
                       + ([bordereau_csv] if bordereau_csv else []) + ([reserves_md] if reserves_md else [])},
            "corrections": C.resume(journal), "sheets": recon}
    (out_dir / "provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1), encoding="utf-8")
    return prov


FAM_FIELDS = ["feuille", "format", "id", "qte", "famille", "portee", "lieux", "afournir", "modele",
              "prescription", "source"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render.from_exemple")
    ap.add_argument("exemple", type=Path)
    ap.add_argument("bordereau_csv", type=Path)
    ap.add_argument("feuilles_csv", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--reserves", type=Path, default=None)
    a = ap.parse_args(argv)
    prov = build(a.exemple, a.bordereau_csv, a.feuilles_csv, a.out_dir, a.reserves)
    print("corrections:", prov["corrections"])
    bad = [s for s in prov["sheets"] if s["missing_markers"] or s["markers_without_row"]]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
