"""Compare an estimator output (estimate.json) with the HR26-14 gold bordereau.

  python -m src.estimer.compare_bordereau ESTIMATE.json GOLD_DIR [--out OUT.json]

GOLD_DIR is the `apprentissage/hr26-14-exemplaire/` folder (branch
hr26-14-entrainement), extracted from EXEMPLE.pdf:
- bordereau-materiel.csv          one row per mark (DSI01-08, E02/E07/E10/E13), `materiel`, `qte`;
- bordereau-electrique-agrege.csv per sheet x code (E01/E03-06/E08/E09/E11/E12/E14), `famille`, `qte`;
- bordereau-travaux-eu.csv        emergency lighting (EU01-04), `famille`, `lieux` (marks on plan).
The three files cover disjoint sheets. Each gold line is mapped to an estimator
family with the same keyword categoriser the estimator uses
(`src.qpl.categorie.categoriser`); the description text is used, never the code.
Comparison is at dossier level (per family): the plan PDF is image-only and has
no sheet number the pipeline can read, so pages are not matched to sheets.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from src.qpl.categorie import categoriser

from .families import FAMILIES


def _rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def gold_family_counts(gold_dir: Path) -> tuple[Counter, dict]:
    fam: Counter = Counter()
    per_sheet: dict[str, Counter] = defaultdict(Counter)
    for r in _rows(gold_dir / "bordereau-materiel.csv"):
        f = categoriser(r["materiel"]).categorie
        q = int(float(r["qte"] or 0))
        fam[f] += q
        per_sheet[r["feuille"]][f] += q
    for r in _rows(gold_dir / "bordereau-electrique-agrege.csv"):
        f = categoriser(r["famille"]).categorie
        q = int(float(r["qte"] or 0))
        fam[f] += q
        per_sheet[r["feuille"]][f] += q
    for r in _rows(gold_dir / "bordereau-travaux-eu.csv"):
        f = categoriser(r["famille"]).categorie
        q = int(float(r["lieux"] or 0))
        fam[f] += q
        per_sheet[r["feuille"]][f] += q
    return fam, {k: dict(v) for k, v in sorted(per_sheet.items())}


def compare(estimate: dict, gold: Counter) -> dict:
    pred = Counter(estimate.get("totals", {}))
    rows = []
    for f in FAMILIES:
        p, g = pred.get(f, 0), gold.get(f, 0)
        if not p and not g:
            continue
        rows.append({"family": f, "predicted": p, "gold": g,
                     "count_error": (p - g) / g if g else None})
    tp, tg = sum(pred.values()), sum(gold.values())
    abs_err = sum(abs(pred.get(f, 0) - gold.get(f, 0)) for f in FAMILIES)
    return {"families": rows,
            "total": {"predicted": tp, "gold": tg, "count_error": (tp - tg) / tg if tg else None},
            "sum_abs_family_error_over_gold": abs_err / tg if tg else None}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.compare_bordereau")
    ap.add_argument("estimate", type=Path)
    ap.add_argument("gold_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    est = json.loads(a.estimate.read_text(encoding="utf-8"))
    gold, per_sheet = gold_family_counts(a.gold_dir)
    res = compare(est, gold)
    res["gold_per_sheet"] = per_sheet
    res["estimate_source_sha256"] = est.get("source_sha256")
    res["model"] = est.get("model")
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        a.out.write_text(txt, encoding="utf-8")
    print(txt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
