"""Compare a rendered relevé with the gold EXEMPLE.pdf, sheet by sheet, on ALL sheets (materiel, agrege, travaux).

python -m src.estimer.render.verify_exemple RENDU.pdf RENDU.report.json EXEMPLE.pdf GOLD_INPUT_DIR [--json out.json]

Checks (exit 1 if any fails):
  markers    every gold marker centre (read from the EXEMPLE overlay) has a drawn marker within 0.05 pt
  header     reperes / familles identical to the EXEMPLE box; RES identical, and absent where the EXEMPLE box
             has none (encadre v6 E03/E04/E05/E08)
  legend     family code -> quantity identical; "/ Rn" identical (absent in the v6 legend)
  bordereau  same pages count per sheet; same rows; every cell equal to the EXEMPLE cell AFTER the logged
             corrections (corrections_exemple), same notes, same subtitles, no truncation ("...") left
  calques    RELEVE layers (OCG) of each sheet identical to the EXEMPLE: names on the plan page and on each
             bordereau page, order in the layer panel (/D/Order), layers of the sheet only (one OCG per family
             AND per sheet + one legend layer per sheet); document-wide: same (name, on/off) multiset (370)
  renvoi     every page reference of the RELEVE box ("... page 2") identical to the EXEMPLE text
  encadre    every non-legend line of the RELEVE box (title, counter, hint, RES line, footer): same text, size,
             colour, and position within ENCADRE_TOL_PT of the box corner
  lignes de legende  same for every legend row span (family code, wrapped label, model line, quantity)
  signets    bookmarks identical to the EXEMPLE: (level, title, page) of every entry, in order
  pages      total pages identical to the EXEMPLE
The raw (uncorrected) cell identity and the old exact-span metric are reported for information.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pymupdf
from scipy.spatial import cKDTree

from . import style as S
from . import corrections_exemple as C
from . import from_exemple as FX
from . import tableau as T
from .from_exemple import read_markers

MARKER_TOL_PT = 0.05
ENCADRE_TOL_PT = 0.15
RENVOI_RE = re.compile(r"\bpage \d+")
LEGENDE_TAILLES = (S.ROW_LABEL_SIZE, S.ROW_QTY_SIZE, S.V6_LABEL_SIZE, S.V6_QTY_SIZE)   # lignes de famille


def _spans(page: pymupdf.Page):
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for sp in line["spans"]:
                yield sp


def legend(page: pymupdf.Page) -> dict[str, str]:
    """Legend rows: bold 8.2 pt family code -> nearest 7.1 pt quantity text on the same baseline."""
    spans = list(_spans(page))
    qtys = [sp for sp in spans if abs(sp["size"] - S.ROW_QTY_SIZE) < 0.05]
    out = {}
    for sp in spans:
        if "Bold" in sp["font"] and abs(sp["size"] - S.ROW_CODE_SIZE) < 0.05 and re.fullmatch(r"[A-Z]+\d*", sp["text"]):
            o = sp["origin"]
            near = sorted((q["origin"][0] - o[0], q["text"]) for q in qtys
                          if abs(q["origin"][1] - o[1]) < 0.6 and q["origin"][0] > o[0])
            out[sp["text"]] = near[0][1] if near else None
    return out


def header(page: pymupdf.Page) -> str | None:
    m = re.search(r"\d+ reperes / \d+ familles / RES \d+", page.get_text())
    return m.group(0) if m else None


def drawn_markers(page: pymupdf.Page, box: pymupdf.Rect) -> np.ndarray:
    c = [((d["rect"].x0 + d["rect"].x1) / 2, (d["rect"].y0 + d["rect"].y1) / 2) for d in page.get_drawings()
         if d.get("fill_opacity") and abs(d["fill_opacity"] - S.FILL_OPACITY) < 0.01 and not box.intersects(d["rect"])]
    return np.array(c).reshape(-1, 2)


def bordereau_pages_of(ex: pymupdf.Document, sheet: str, start: int) -> list[int]:
    """0-based EXEMPLE pages titled 'BORDEREAU MATERIEL - <sheet>' following the plan page."""
    out, p = [], start
    while p < ex.page_count and f"BORDEREAU MATERIEL - {sheet}" in ex[p].get_text()[:200]:
        out.append(p)
        p += 1
    return out


PV_RE = re.compile(r";(?=\S)")


def corriger_sous_titre(text: str) -> str:
    """Sous-titre travaux de l'EXEMPLE : 'travaux;9 appareils' -> 'travaux; 9 appareils'."""
    return PV_RE.sub("; ", text)


def expected_table(name: str, fmt: str, table: dict) -> tuple[list[dict], list[str]]:
    journal: list = []
    if fmt == "materiel":
        rows = [C.corriger_ligne(name, r, FX.MAT_TEXT, {}, journal) for r in table["rows"]]
        notes = [C.corriger_cellule(name, "reserves", "reserves", n, {}, journal) for n in table["notes"]]
        return rows, notes
    return FX.corriger_table(name, fmt, table, journal)


def _res_of(head: str | None) -> dict:
    return FX.read_header_text(head or "")


# ---------------------------------------------------------------- calques, signets, texte de l'encadré
def releve_ocgs(doc: pymupdf.Document) -> dict[int, dict]:
    """OCG RELEVE du document : xref -> {name, on, ...} (get_ocgs)."""
    return {x: v for x, v in doc.get_ocgs().items() if v["name"].startswith("RELEVE")}


def page_ocgs(doc: pymupdf.Document, pno: int, rel: dict[int, dict]) -> list[int]:
    """xref des OCG RELEVE déclarés par la page `pno` (ressources /Properties)."""
    kind, val = doc.xref_get_key(doc[pno].xref, "Resources/Properties")
    props = doc.xref_object(int(val.split()[0])) if kind == "xref" else (val if kind == "dict" else "")
    return [int(x) for x in re.findall(r"/\w+\s+(\d+)\s+0\s+R", props) if int(x) in rel]


def order_ocgs(doc: pymupdf.Document) -> list[int]:
    """xref des OCG dans l'ordre du panneau des calques (/OCProperties/D/Order aplati)."""
    kind, val = doc.xref_get_key(doc.pdf_catalog(), "OCProperties/D/Order")
    return [int(x) for x in re.findall(r"(\d+)\s+0\s+R", val)] if kind == "array" else []


def calques_feuille(doc: pymupdf.Document, plan: int, bords: list[int], rel: dict[int, dict],
                    order: list[int]) -> dict:
    """Calques RELEVE d'une feuille : noms sur la page plan, sur chaque page de bordereau, ordre du panneau."""
    own = page_ocgs(doc, plan, rel)
    return {"xrefs": set(own),
            "plan": sorted(rel[x]["name"] for x in own),
            "bordereau": [sorted(rel[x]["name"] for x in page_ocgs(doc, p, rel)) for p in bords],
            "bordereau_xrefs": {x for p in bords for x in page_ocgs(doc, p, rel)},
            "ordre": [rel[x]["name"] for x in order if x in own]}


def signets(doc: pymupdf.Document) -> list[tuple[int, str, int]]:
    return [(t[0], t[1], t[2]) for t in doc.get_toc(simple=False)]


def _box_spans(page: pymupdf.Page, box: pymupdf.Rect) -> list[dict]:
    return [sp for b in page.get_text("dict", clip=box)["blocks"] for line in b.get("lines", [])
            for sp in line["spans"] if sp["text"].strip() and pymupdf.Point(sp["origin"]) in box]


def renvois(page: pymupdf.Page, box: pymupdf.Rect) -> list[str]:
    """Lignes de l'encadré qui renvoient à une page (« ... page 2 »), de haut en bas."""
    return [sp["text"] for sp in sorted(_box_spans(page, box), key=lambda s: (round(s["origin"][1], 1), s["origin"][0]))
            if RENVOI_RE.search(sp["text"])]


def _ligne_de_legende(sp: dict) -> bool:
    """Span d'une ligne de famille de la légende : code (gras 8,2 / 10), libellé, modèle, quantité."""
    size = sp["size"]
    return any(abs(size - z) < 0.05 for z in LEGENDE_TAILLES) or ("Bold" in sp["font"]
                                                                  and abs(size - S.ROW_CODE_SIZE) < 0.05)


def _lignes(page: pymupdf.Page, box: pymupdf.Rect, legende: bool) -> list[tuple]:
    return sorted((round(sp["origin"][1] - box.y0, 3), round(sp["origin"][0] - box.x0, 3), sp["text"],
                   round(sp["size"], 2), f"{sp['color']:06x}")
                  for sp in _box_spans(page, box) if _ligne_de_legende(sp) == legende)


def encadre_lignes(page: pymupdf.Page, box: pymupdf.Rect) -> list[tuple]:
    """Lignes de l'encadré hors lignes de famille : (dy, dx, texte, corps, couleur) depuis le coin du cadre."""
    return _lignes(page, box, legende=False)


def legende_lignes(page: pymupdf.Page, box: pymupdf.Rect) -> list[tuple]:
    """Lignes de famille de la légende (code, libellé coupé, modèle, quantité) : (dy, dx, texte, corps, couleur)."""
    return _lignes(page, box, legende=True)


def encadre_ecarts(mine: list[tuple], gold: list[tuple]) -> list:
    """Chaque ligne du gold appariée à une ligne du rendu de même texte, corps et couleur, à ENCADRE_TOL_PT près ;
    rapporte les lignes du gold sans partenaire et celles du rendu en trop."""
    reste = list(mine)
    out = []
    for g in gold:
        m = next((m for m in reste if m[2:] == g[2:] and abs(m[0] - g[0]) <= ENCADRE_TOL_PT
                  and abs(m[1] - g[1]) <= ENCADRE_TOL_PT), None)
        if m is None:
            out.append({"attendu": g, "rendu": next((m for m in reste if m[2] == g[2]), None)})
        else:
            reste.remove(m)
    cites = [o["rendu"] for o in out if o["rendu"] is not None]
    return out + [{"attendu": None, "rendu": m} for m in reste if m not in cites]


def verify(rendu: Path, report: Path, exemple: Path, gold_dir: Path) -> dict:
    out = pymupdf.open(rendu)
    ex = pymupdf.open(exemple)
    rep = json.loads(report.read_text(encoding="utf-8"))
    prov = json.loads((gold_dir / "provenance.json").read_text(encoding="utf-8"))
    ex_page = {s["sheet"]: s["exemple_page"] - 1 for s in prov["sheets"]}
    ex_bords = T.sheet_bordereaux(ex)
    rel_out, rel_ex = releve_ocgs(out), releve_ocgs(ex)
    ord_out, ord_ex = order_ocgs(out), order_ocgs(ex)
    rows = []
    for s in rep["sheets"]:
        name, pno, fmt = s["sheet"], s["plan_page"] - 1, s.get("format", "materiel")
        gold = read_markers(ex, ex_page[name])
        g = np.array([(m["x"], m["y"]) for m in gold]).reshape(-1, 2)
        d = drawn_markers(out[pno], pymupdf.Rect(s["box"]))
        dist = cKDTree(d).query(g)[0] if len(d) and len(g) else np.array([np.inf])
        mine_b = [p - 1 for p in s["bordereau_pages"]]
        ex_b = ex_bords.get(name, {}).get("pages", [])
        a = Counter((sp["text"], round(sp["origin"][0], 1), round(sp["origin"][1], 1))
                    for p in mine_b for sp in _spans(out[p]))
        b = Counter((sp["text"], round(sp["origin"][0], 1), round(sp["origin"][1], 1))
                    for p in ex_b for sp in _spans(ex[p]))
        # encadre
        h_out, h_ex = FX.read_header(out[pno]), FX.read_header(ex[ex_page[name]])
        # encadré v6 du gold (E03/E04/E05/E08) : pas de RES, le rendu ne doit pas en afficher non plus
        header_ok = bool(h_out) and bool(h_ex) and h_out["reperes"] == h_ex["reperes"] \
            and h_out["familles"] == h_ex["familles"] and h_out["res"] == h_ex["res"]
        l_out, l_ex = FX.read_legend(out[pno]), FX.read_legend(ex[ex_page[name]])
        legend_diff = {}
        for k in set(l_out) | set(l_ex):
            o, e = l_out.get(k), l_ex.get(k)
            if o is None or e is None or o[0] != e[0] or o[1] != e[1]:
                legend_diff[k] = [o, e]
        # bordereau cellule par cellule
        t_ex = T.read_table([ex[p] for p in ex_b], fmt)
        t_out = T.read_table([out[p] for p in mine_b], fmt)
        exp_rows, exp_notes = expected_table(name, fmt, t_ex)
        cells = same = raw_same = 0
        cell_diff = []
        for i, (eo, er, ro) in enumerate(zip(exp_rows, t_ex["rows"], t_out["rows"])):
            for k in eo:
                cells += 1
                if T.norm(ro.get(k, "")) == T.norm(eo[k]):
                    same += 1
                else:
                    cell_diff.append({"ligne": i + 1, "colonne": k, "rendu": ro.get(k, ""), "attendu": eo[k]})
                raw_same += T.norm(ro.get(k, "")) == T.norm(er[k])
        notes_ok = T.norm(" ".join(t_out["notes"])) == T.norm(" ".join(exp_notes))
        exp_subs = [corriger_sous_titre(x) for x in t_ex["subtitles"]]
        subs_ok = [T.norm(x) for x in t_out["subtitles"]] == [T.norm(x) for x in exp_subs]
        trunc = sum(1 for r in t_out["rows"] for v in r.values() if "..." in v) \
            + sum(1 for n in t_out["notes"] if "..." in n)
        row = {
            "sheet": name, "format": fmt,
            "markers_gold": len(g), "markers_drawn": len(d), "marker_max_dist_pt": round(float(dist.max()), 4),
            "markers_ok": len(g) == len(d) and float(dist.max()) <= MARKER_TOL_PT,
            "header": h_out, "header_exemple": h_ex, "header_ok": header_ok,
            "legend_diff": legend_diff, "legend_ok": not legend_diff,
            "bordereau_pages": [len(mine_b), len(ex_b)],
            "rows": [len(t_out["rows"]), len(t_ex["rows"])],
            "cells": cells, "cells_same": same, "cells_raw_same": raw_same, "cell_diff": cell_diff,
            "notes": [len(t_out["notes"]), len(t_ex["notes"])], "notes_ok": notes_ok,
            "subtitles_ok": subs_ok, "subtitles": [t_out["subtitles"], exp_subs], "truncations": trunc,
            "bordereau_spans_same": sum((a & b).values()),
            "bordereau_spans_diff": sum((a - b).values()) + sum((b - a).values()),
        }
        row["bordereau_ok"] = (len(mine_b) == len(ex_b) and row["rows"][0] == row["rows"][1] and same == cells
                               and notes_ok and subs_ok and trunc == 0)
        # calques RELEVE de la feuille (page plan + pages de bordereau), ordre du panneau
        c_out = calques_feuille(out, pno, mine_b, rel_out, ord_out)
        c_ex = calques_feuille(ex, ex_page[name], ex_b, rel_ex, ord_ex)
        row["calques"] = [len(c_out["plan"]), len(c_ex["plan"])]
        row["calques_diff"] = {k: [c_out[k], c_ex[k]] for k in ("plan", "bordereau", "ordre") if c_out[k] != c_ex[k]}
        row["calques_hors_feuille"] = len(c_out["bordereau_xrefs"] - c_out["xrefs"])
        row["_xrefs"] = c_out["xrefs"]
        # encadré : renvois de page et lignes hors légende (titre, compteur, renvoi, RES, pied)
        box_out, box_ex = pymupdf.Rect(s["box"]), pymupdf.Rect(FX.read_box_rect(ex[ex_page[name]]))
        row["renvoi"] = [renvois(out[pno], box_out), renvois(ex[ex_page[name]], box_ex)]
        row["renvoi_ok"] = row["renvoi"][0] == row["renvoi"][1] and bool(row["renvoi"][1])
        row["encadre_diff"] = encadre_ecarts(encadre_lignes(out[pno], box_out),
                                             encadre_lignes(ex[ex_page[name]], box_ex))
        row["encadre_ok"] = not row["encadre_diff"]
        l_mine, l_gold = legende_lignes(out[pno], box_out), legende_lignes(ex[ex_page[name]], box_ex)
        row["legende_lignes"] = [len(l_mine), len(l_gold)]
        row["legende_lignes_diff"] = encadre_ecarts(l_mine, l_gold)
        row["legende_lignes_ok"] = not row["legende_lignes_diff"]
        rows.append(row)
    # un calque par famille ET par feuille : aucun OCG RELEVE partagé entre deux feuilles
    xrefs = [r.pop("_xrefs") for r in rows]
    for k, r in enumerate(rows):
        r["calques_partages"] = len(xrefs[k] & set().union(*(x for j, x in enumerate(xrefs) if j != k)))
        r["calques_ok"] = not r["calques_diff"] and not r["calques_hors_feuille"] and not r["calques_partages"]
        r["ok"] = (r["markers_ok"] and r["header_ok"] and r["legend_ok"] and r["bordereau_ok"] and r["calques_ok"]
                   and r["renvoi_ok"] and r["encadre_ok"] and r["legende_lignes_ok"])
    etats = [sorted((v["name"], v["on"]) for v in rel_out.values()), sorted((v["name"], v["on"]) for v in rel_ex.values())]
    calques_ok = etats[0] == etats[1]
    toc = [signets(out), signets(ex)]
    signets_ok = toc[0] == toc[1]
    pages_ok = out.page_count == ex.page_count
    return {"sheets": rows, "ok": all(r["ok"] for r in rows) and pages_ok and calques_ok and signets_ok,
            "pages": [out.page_count, ex.page_count], "pages_ok": pages_ok,
            "calques": [len(rel_out), len(rel_ex)], "calques_ok": calques_ok,
            "calques_on": [sum(v["on"] for v in rel_out.values()), sum(v["on"] for v in rel_ex.values())],
            "signets": [len(toc[0]), len(toc[1])], "signets_ok": signets_ok,
            "signets_diff": [[a, b] for a, b in zip(*toc) if a != b][:10],
            "renvois_ok": sum(r["renvoi_ok"] for r in rows), "encadres_ok": sum(r["encadre_ok"] for r in rows),
            "legendes_lignes_ok": sum(r["legende_lignes_ok"] for r in rows),
            "markers": sum(r["markers_gold"] for r in rows),
            "cells": sum(r["cells"] for r in rows), "cells_same": sum(r["cells_same"] for r in rows),
            "cells_raw_same": sum(r["cells_raw_same"] for r in rows),
            "truncations": sum(r["truncations"] for r in rows),
            "bordereau_spans_same": sum(r["bordereau_spans_same"] for r in rows),
            "bordereau_spans_diff": sum(r["bordereau_spans_diff"] for r in rows)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render.verify_exemple")
    ap.add_argument("rendu", type=Path)
    ap.add_argument("report", type=Path)
    ap.add_argument("exemple", type=Path)
    ap.add_argument("gold_dir", type=Path)
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args(argv)
    res = verify(a.rendu, a.report, a.exemple, a.gold_dir)
    for r in res["sheets"]:
        h = r["header"] or {}
        print(f"{r['sheet']:5} {r['format']:8} reperes {r['markers_drawn']}/{r['markers_gold']} "
              f"(max {r['marker_max_dist_pt']} pt)  encadre {'OK' if r['header_ok'] else 'DIFF'} "
              f"[{h.get('reperes')}/{h.get('familles')}/RES {h.get('res')}]  legende "
              f"{'OK' if r['legend_ok'] else r['legend_diff']}  bordereau {r['bordereau_pages'][0]}/"
              f"{r['bordereau_pages'][1]} p, lignes {r['rows'][0]}/{r['rows'][1]}, cellules {r['cells_same']}/"
              f"{r['cells']} (brutes {r['cells_raw_same']}), notes {'OK' if r['notes_ok'] else 'DIFF'}, "
              f"sous-titres {'OK' if r['subtitles_ok'] else 'DIFF'}, troncatures {r['truncations']}, "
              f"calques {r['calques'][0]}/{r['calques'][1]} {'OK' if r['calques_ok'] else 'DIFF'}, "
              f"renvoi {'OK' if r['renvoi_ok'] else 'DIFF'}, encadre {'OK' if r['encadre_ok'] else 'DIFF'}, "
              f"lignes de legende {r['legende_lignes'][0]}/{r['legende_lignes'][1]} "
              f"{'OK' if r['legende_lignes_ok'] else 'DIFF'}")
        for c in r["cell_diff"][:3]:
            print("      ecart", c)
        if r["calques_diff"] or r["calques_hors_feuille"] or r["calques_partages"]:
            print("      calques", {k: v for k, v in r["calques_diff"].items() if k != "bordereau"},
                  f"hors feuille {r['calques_hors_feuille']}, partages {r['calques_partages']}")
        if not r["renvoi_ok"]:
            print("      renvoi", r["renvoi"])
        for c in r["encadre_diff"][:3]:
            print("      encadre", c)
        for c in r["legende_lignes_diff"][:3]:
            print("      legende", c)
    for a, b in res["signets_diff"][:3]:
        print("      signet", a, "attendu", b)
    print(f"CALQUES RELEVE {res['calques'][0]}/{res['calques'][1]} (actifs {res['calques_on'][0]}/"
          f"{res['calques_on'][1]}) {'OK' if res['calques_ok'] else 'DIFF'}, signets {res['signets'][0]}/"
          f"{res['signets'][1]} {'OK' if res['signets_ok'] else 'DIFF'}, renvois {res['renvois_ok']}/"
          f"{len(res['sheets'])}, encadres {res['encadres_ok']}/{len(res['sheets'])}, lignes de legende "
          f"{res['legendes_lignes_ok']}/{len(res['sheets'])}")
    print(f"TOTAL pages {res['pages'][0]}/{res['pages'][1]}, reperes {res['markers']}, cellules {res['cells_same']}/"
          f"{res['cells']} (identiques brutes {res['cells_raw_same']}), troncatures {res['truncations']}, "
          f"spans exacts {res['bordereau_spans_same']} (diff {res['bordereau_spans_diff']}, info) -> "
          f"{'OK' if res['ok'] else 'FAIL'}")
    if a.json:
        a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
