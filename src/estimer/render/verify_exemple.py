"""Compare a rendered relevé with the gold EXEMPLE.pdf, sheet by sheet.

python -m src.estimer.render.verify_exemple RENDU.pdf RENDU.report.json EXEMPLE.pdf GOLD_INPUT_DIR [--json out.json]

Checks (exit 1 if any fails):
  markers    every gold marker centre (read from the EXEMPLE overlay) has a drawn marker within 0.05 pt
  header     "N reperes / F familles / RES n" equals the EXEMPLE box header of the same sheet
  legend     family code -> "qty / Rn" identical to the EXEMPLE legend
  bordereau  every text span (text + origin rounded to 0.1 pt) of the bordereau pages identical
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


def verify(rendu: Path, report: Path, exemple: Path, gold_dir: Path) -> dict:
    out = pymupdf.open(rendu)
    ex = pymupdf.open(exemple)
    rep = json.loads(report.read_text(encoding="utf-8"))
    prov = json.loads((gold_dir / "provenance.json").read_text(encoding="utf-8"))
    ex_page = {s["sheet"]: s["exemple_page"] - 1 for s in prov["sheets"]}
    rows = []
    for s in rep["sheets"]:
        name, pno = s["sheet"], s["plan_page"] - 1
        gold = read_markers(ex, ex_page[name])
        g = np.array([(m["x"], m["y"]) for m in gold]).reshape(-1, 2)
        d = drawn_markers(out[pno], pymupdf.Rect(s["box"]))
        dist = cKDTree(d).query(g)[0] if len(d) and len(g) else np.array([np.inf])
        mine_b = [p - 1 for p in s["bordereau_pages"]]
        ex_b = bordereau_pages_of(ex, name, ex_page[name] + 1)
        a = Counter((sp["text"], round(sp["origin"][0], 1), round(sp["origin"][1], 1))
                    for p in mine_b for sp in _spans(out[p]))
        b = Counter((sp["text"], round(sp["origin"][0], 1), round(sp["origin"][1], 1))
                    for p in ex_b for sp in _spans(ex[p]))
        la, lb = legend(out[pno]), legend(ex[ex_page[name]])
        row = {
            "sheet": name,
            "markers_gold": len(g), "markers_drawn": len(d), "marker_max_dist_pt": round(float(dist.max()), 4),
            "markers_ok": len(g) == len(d) and float(dist.max()) <= MARKER_TOL_PT,
            "header": header(out[pno]), "header_exemple": header(ex[ex_page[name]]),
            "legend_diff": {k: [la.get(k), lb.get(k)] for k in set(la) | set(lb) if la.get(k) != lb.get(k)},
            "bordereau_pages": [len(mine_b), len(ex_b)],
            "bordereau_spans_same": sum((a & b).values()),
            "bordereau_spans_diff": sum((a - b).values()) + sum((b - a).values()),
        }
        row["header_ok"] = row["header"] == row["header_exemple"] and row["header"] is not None
        row["legend_ok"] = not row["legend_diff"]
        row["bordereau_ok"] = row["bordereau_spans_diff"] == 0 and len(mine_b) == len(ex_b)
        row["ok"] = row["markers_ok"] and row["header_ok"] and row["legend_ok"] and row["bordereau_ok"]
        rows.append(row)
    return {"sheets": rows, "ok": all(r["ok"] for r in rows),
            "markers": sum(r["markers_gold"] for r in rows),
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
        print(f"{r['sheet']:6} markers {r['markers_drawn']}/{r['markers_gold']} (max {r['marker_max_dist_pt']} pt)  "
              f"header {'OK' if r['header_ok'] else 'DIFF'} [{r['header']}]  legend {'OK' if r['legend_ok'] else r['legend_diff']}  "
              f"bordereau {r['bordereau_pages'][0]}/{r['bordereau_pages'][1]} p, spans diff {r['bordereau_spans_diff']}")
    print(f"TOTAL markers {res['markers']}, bordereau spans identical {res['bordereau_spans_same']}, "
          f"different {res['bordereau_spans_diff']} -> {'OK' if res['ok'] else 'FAIL'}")
    if a.json:
        a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
