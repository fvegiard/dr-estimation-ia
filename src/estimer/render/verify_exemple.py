"""Compare a rendered relevé with the gold EXEMPLE.pdf, sheet by sheet, on ALL sheets (materiel, agrege, travaux).

python -m src.estimer.render.verify_exemple RENDU.pdf RENDU.report.json EXEMPLE.pdf GOLD_INPUT_DIR [--json out.json]

Checks (exit 1 if any fails):
  markers    every gold marker centre (read from the EXEMPLE overlay) has a drawn marker within 0.05 pt
  header     reperes / familles identical to the EXEMPLE box; RES identical where the EXEMPLE box shows it
             (encadre v6 E03/E04/E05/E08 without RES: RES = reperes, convention of the other sheets)
  legend     family code -> quantity identical; "/ Rn" identical where the EXEMPLE legend shows it
  bordereau  same pages count per sheet; same rows; every cell equal to the EXEMPLE cell AFTER the logged
             corrections (corrections_exemple), same notes, same subtitles, no truncation ("...") left
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


def verify(rendu: Path, report: Path, exemple: Path, gold_dir: Path) -> dict:
    out = pymupdf.open(rendu)
    ex = pymupdf.open(exemple)
    rep = json.loads(report.read_text(encoding="utf-8"))
    prov = json.loads((gold_dir / "provenance.json").read_text(encoding="utf-8"))
    expected_sheets = [s["sheet"] for s in prov["sheets"]]
    actual_sheets = [s["sheet"] for s in rep["sheets"]]
    sheets_ok = bool(expected_sheets) and actual_sheets == expected_sheets
    ex_page = {s["sheet"]: s["exemple_page"] - 1 for s in prov["sheets"]}
    unexpected_sheets = [name for name in actual_sheets if name not in ex_page]
    ex_bords = T.sheet_bordereaux(ex)
    rows = []
    for s in rep["sheets"]:
        if s["sheet"] not in ex_page:
            # Coverage fails for this entry; continue inspecting all known sheets.
            continue
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
        header_ok = bool(h_out) and bool(h_ex) and h_out["reperes"] == h_ex["reperes"] \
            and h_out["familles"] == h_ex["familles"] \
            and h_out["res"] == (h_ex["res"] if h_ex["res"] is not None else h_ex["reperes"])
        l_out, l_ex = FX.read_legend(out[pno]), FX.read_legend(ex[ex_page[name]])
        legend_diff = {}
        for k in set(l_out) | set(l_ex):
            o, e = l_out.get(k), l_ex.get(k)
            if o is None or e is None or o[0] != e[0] or (e[1] is not None and o[1] != e[1]) \
                    or (e[1] is None and o[1] != o[0]):
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
        row["ok"] = row["markers_ok"] and row["header_ok"] and row["legend_ok"] and row["bordereau_ok"]
        rows.append(row)
    pages_ok = out.page_count == ex.page_count
    return {"sheets": rows, "ok": sheets_ok and all(r["ok"] for r in rows) and pages_ok,
            "sheets_ok": sheets_ok, "expected_sheets": expected_sheets, "actual_sheets": actual_sheets,
            "unexpected_sheets": unexpected_sheets,
            "pages": [out.page_count, ex.page_count], "pages_ok": pages_ok,
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
    if res["unexpected_sheets"]:
        print("UNEXPECTED sheets:", ", ".join(res["unexpected_sheets"]))
    for r in res["sheets"]:
        h = r["header"] or {}
        print(f"{r['sheet']:5} {r['format']:8} reperes {r['markers_drawn']}/{r['markers_gold']} "
              f"(max {r['marker_max_dist_pt']} pt)  encadre {'OK' if r['header_ok'] else 'DIFF'} "
              f"[{h.get('reperes')}/{h.get('familles')}/RES {h.get('res')}]  legende "
              f"{'OK' if r['legend_ok'] else r['legend_diff']}  bordereau {r['bordereau_pages'][0]}/"
              f"{r['bordereau_pages'][1]} p, lignes {r['rows'][0]}/{r['rows'][1]}, cellules {r['cells_same']}/"
              f"{r['cells']} (brutes {r['cells_raw_same']}), notes {'OK' if r['notes_ok'] else 'DIFF'}, "
              f"sous-titres {'OK' if r['subtitles_ok'] else 'DIFF'}, troncatures {r['truncations']}")
        for c in r["cell_diff"][:3]:
            print("      ecart", c)
    print(f"TOTAL pages {res['pages'][0]}/{res['pages'][1]}, reperes {res['markers']}, cellules {res['cells_same']}/"
          f"{res['cells']} (identiques brutes {res['cells_raw_same']}), troncatures {res['truncations']}, "
          f"spans exacts {res['bordereau_spans_same']} (diff {res['bordereau_spans_diff']}, info) -> "
          f"{'OK' if res['ok'] else 'FAIL'}")
    if a.json:
        a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
