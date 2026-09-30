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


def gold_family_counts(gold_dir: Path, feuilles: set[str] | None = None) -> tuple[Counter, dict]:
    """Totaux de l'exemplaire par famille, et le détail par feuille.

    `feuilles` restreint le total aux feuilles demandées. Sans restriction, comparer un
    relevé d'une seule feuille aux 26 de l'exemplaire donne un écart de -95 % qui ne dit
    rien de la justesse : il mesure ce qui n'a pas été relevé, pas ce qui a été mal relevé.
    Les trois bordereaux (matériel, agrégé, travaux EU) couvrent des feuilles disjointes,
    donc restreindre les feuilles sélectionne de fait le ou les formats concernés.
    """
    fam: Counter = Counter()
    per_sheet: dict[str, Counter] = defaultdict(Counter)

    def retenu(feuille: str) -> bool:
        return feuilles is None or feuille.strip().upper() in feuilles

    for r in _rows(gold_dir / "bordereau-materiel.csv"):
        f = categoriser(r["materiel"]).categorie
        q = int(float(r["qte"] or 0))
        if retenu(r["feuille"]):
            fam[f] += q
        per_sheet[r["feuille"]][f] += q
    for r in _rows(gold_dir / "bordereau-electrique-agrege.csv"):
        f = categoriser(r["famille"]).categorie
        q = int(float(r["qte"] or 0))
        if retenu(r["feuille"]):
            fam[f] += q
        per_sheet[r["feuille"]][f] += q
    for r in _rows(gold_dir / "bordereau-travaux-eu.csv"):
        f = categoriser(r["famille"]).categorie
        q = int(float(r["lieux"] or 0))
        if retenu(r["feuille"]):
            fam[f] += q
        per_sheet[r["feuille"]][f] += q
    return fam, {k: dict(v) for k, v in sorted(per_sheet.items())}


def feuilles_estimees(estimate: dict) -> set[str]:
    """Feuilles réellement couvertes par l'estimation (pour comparer à périmètre égal)."""
    noms = {str(s.get("sheet") or s.get("feuille") or "").strip().upper()
            for s in estimate.get("sheets") or []}
    for c in estimate.get("counters") or []:
        for el in c.get("elements") or []:
            n = str(el.get("sheet") or el.get("feuille") or "").strip().upper()
            if n:
                noms.add(n)
    return {n for n in noms if n}


def totaux_predits(estimate: dict) -> Counter:
    """Totaux par famille, quelle que soit la forme du fichier d'estimation.

    Deux chaînes produisent un `estimate.json` : le pipeline `estimer` écrit `totals`,
    le pont `render/from_releve.py` écrit `counters` (une entrée par famille avec ses
    éléments). Sans cette conversion, un relevé parfaitement valide était noté
    « predicted: 0 » — on aurait conclu que l'IA n'avait rien trouvé alors que c'est le
    comparateur qui ne savait pas lire.
    """
    if estimate.get("totals"):
        return Counter(estimate["totals"])
    if estimate.get("counters"):
        pred = Counter()
        for c in estimate["counters"]:
            nom = c.get("family") or c.get("name") or ""
            n = c.get("quantity")
            if n is None:
                n = len(c.get("elements") or [])
            pred[categoriser(nom).categorie] += n
        return pred
    raise ValueError("estimation illisible : ni « totals » ni « counters ». Un fichier "
                     "d'une autre forme serait note 0 sans que rien ne le signale.")


def compare(estimate: dict, gold: Counter) -> dict:
    pred = totaux_predits(estimate)
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
    ap.add_argument("--feuilles", default=None,
                    help="feuilles de l'exemplaire à retenir (séparées par des virgules). "
                         "« auto » se limite aux feuilles couvertes par l'estimation.")
    a = ap.parse_args(argv)
    est = json.loads(a.estimate.read_text(encoding="utf-8"))
    if a.feuilles == "auto":
        retenues = feuilles_estimees(est)
        if not retenues:
            raise SystemExit("--feuilles auto : l'estimation ne nomme aucune feuille")
    elif a.feuilles:
        retenues = {f.strip().upper() for f in a.feuilles.split(",") if f.strip()}
    else:
        retenues = None
    gold, per_sheet = gold_family_counts(a.gold_dir, retenues)
    res = compare(est, gold)
    res["feuilles_comparees"] = sorted(retenues) if retenues else "toutes"
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
