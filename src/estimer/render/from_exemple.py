"""Build a renderer input directory from a gold EXEMPLE relevé (HR26-14) - used to prove the renderer.

python -m src.estimer.render.from_exemple EXEMPLE.pdf bordereau-materiel.csv feuilles.csv OUT_DIR [--reserves reserves.md]

EXEMPLE.pdf is the target relevé: original vector plan pages + a PyMuPDF overlay drawn in optional-content
layers named "RELEVE ...". From it this tool writes:
  OUT_DIR/plans.pdf       the plan pages of the sheets in bordereau-materiel.csv, with the RELEVE overlay
                          content streams removed (= the original drawing, still vector)
  OUT_DIR/estimate.json   estimer-format sheets/counters; one element per gold marker with its exact
                          anchor (centre, bbox, shape) read from the overlay, repère and source id
  OUT_DIR/bordereau.csv   the gold rows of those sheets (descriptive bordereau fields)
  OUT_DIR/reserves.md     copied when --reserves is given
  OUT_DIR/provenance.json input sha256 + per-sheet marker/row reconciliation
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
    kind = "circle" if "c" in ops else "diamond"
    return kind, (min(xs), page_h - max(ys), max(xs), page_h - min(ys))


def read_markers(doc: pymupdf.Document, pno: int) -> list[dict]:
    """Gold markers of plan page `pno` (0-based): each = shape stream, leader, white box, label text (helv 4.8)."""
    page = doc[pno]
    H = page.rect.height
    _, ov = overlay_split(doc, page)
    out = []
    for i, s in enumerate(ov):
        if b"/helv 4.8 Tf" not in s or i < 3:
            continue
        texts = [bytes.fromhex(t.decode()).decode("latin-1") for t in TJ_RE.findall(s)]
        shape, bbox = _shape_bbox(ov[i - 3].decode("latin-1"), H)
        if bbox is None:
            continue
        cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
        out.append({"repere": texts[0], "extra": texts[1:], "shape": shape,
                    "x": round(cx, 3), "y": round(cy, 3), "bbox": [round(v, 3) for v in bbox]})
    return out


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


def build(exemple: Path, bordereau_csv: Path, feuilles_csv: Path, out_dir: Path,
          reserves_md: Path | None = None, log=print) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(bordereau_csv, newline="", encoding="utf-8")))
    fields = list(rows[0].keys())
    pages = {r["feuille"]: int(r["page"]) for r in csv.DictReader(open(feuilles_csv, newline="", encoding="utf-8"))}
    header = {r["feuille"]: r for r in csv.DictReader(open(feuilles_csv, newline="", encoding="utf-8"))}
    order = []
    for r in rows:
        if r["feuille"] not in order:
            order.append(r["feuille"])
    order.sort(key=lambda f: pages[f])

    src = pymupdf.open(exemple)
    sheets, counters, recon = [], defaultdict(list), []
    by_sheet = defaultdict(dict)
    for r in rows:
        by_sheet[r["feuille"]][r["repere"]] = r
    for i, name in enumerate(order):
        pno = pages[name] - 1
        page = src[pno]
        W, H = page.rect.width, page.rect.height
        marks = read_markers(src, pno)
        gold = by_sheet[name]
        seen = defaultdict(int)
        for m in marks:
            seen[m["repere"]] += 1
            row = gold.get(m["repere"])
            code = m["repere"].rsplit("-", 1)[0]
            counters[(code, row["materiel"] if row else code)].append({
                "sheet": name, "page": i + 1, "x": m["x"], "y": m["y"], "bbox": m["bbox"], "shape": m["shape"],
                "repere": m["repere"], "source": row["source"] if row else "", "code": code, "flags": []})
        missing = sorted(set(gold) - set(seen))
        extra = sorted(set(seen) - set(gold))
        dup = sorted(k for k, n in seen.items() if n > 1)
        recon.append({"sheet": name, "exemple_page": pno + 1, "markers": len(marks), "gold_rows": len(gold),
                      "missing_markers": missing, "markers_without_row": extra, "duplicate_markers": dup,
                      "header_reperes": header[name]["reperes"], "header_res": header[name]["res"]})
        log(f"{name}: page {pno + 1}, {len(marks)} markers / {len(gold)} gold rows"
            + (f", missing {missing}" if missing else "") + (f", extra {extra}" if extra else ""))
        sheets.append({"page": i + 1, "sheet": name, "width_px": W, "height_px": H, "raster_source": "vector",
                       "exemple_page": pno + 1})
        strip_overlay(src, pno)

    # keep the original page objects (seal widgets, layers) rather than re-inserting them
    src.select([pages[name] - 1 for name in order])
    dropped = prune_ocgs(src)
    src.set_toc([])
    src.save(out_dir / "plans.pdf", garbage=3, deflate=True)
    log(f"plans.pdf: {src.page_count} pages, {dropped} RELEVE/unused layers removed")

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
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(r for r in rows if r["feuille"] in order)
    if reserves_md:
        shutil.copyfile(reserves_md, out_dir / "reserves.md")
    prov = {"inputs": {str(p.name): sha256(p) for p in [exemple, bordereau_csv, feuilles_csv]
                       + ([reserves_md] if reserves_md else [])},
            "sheets": recon}
    (out_dir / "provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1), encoding="utf-8")
    return prov


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render.from_exemple")
    ap.add_argument("exemple", type=Path)
    ap.add_argument("bordereau_csv", type=Path)
    ap.add_argument("feuilles_csv", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--reserves", type=Path, default=None)
    a = ap.parse_args(argv)
    prov = build(a.exemple, a.bordereau_csv, a.feuilles_csv, a.out_dir, a.reserves)
    bad = [s for s in prov["sheets"] if s["missing_markers"] or s["markers_without_row"]]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
