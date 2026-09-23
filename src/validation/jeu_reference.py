"""Jeu de référence : rejoue compare_qpl sur tous les dossiers qui ont un projet Plan Expert humain.

    python -m src.validation.jeu_reference                 # compare à la ligne de base, code 1 si régression
    python -m src.validation.jeu_reference --nouvelle-base # enregistre les résultats comme ligne de base

Un dossier entre dans le jeu dès que `dossiers/<S>/reference/` contient :
  - `<S>-Dupuis-PlanExpert.qpl`  (projet de l'estimateur),
  - `dupuis-png-dimensions.txt`  (dossier|nom.png|largeur|hauteur, lu dans l'en-tête des PNG de l'estimateur),
  - `feuilles-ia.csv`            (feuilles.csv de prepare.py pour le relevé IA),
et que `dossiers/<S>/planexpert/<S>.qpl` (relevé IA) existe.

Sorties : `dossiers/_jeu-reference/resultats.json` et `resultats.md`. Aucun chiffre saisi à la main.
Régression = rappel ou précision d'un dossier qui baisse de plus de TOLERANCE points par rapport à `ligne-de-base.json`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.validation import compare_qpl as cq

RACINE = Path(__file__).resolve().parents[2]
DOSSIERS = RACINE / "dossiers"
SORTIE = DOSSIERS / "_jeu-reference"
TOLERANCE = 1.0  # points de pourcentage


def dossiers_du_jeu() -> list[str]:
    out = []
    for d in sorted(DOSSIERS.glob("S-*")):
        s = d.name
        ref = d / "reference"
        if all(p.exists() for p in (ref / f"{s}-Dupuis-PlanExpert.qpl", ref / "dupuis-png-dimensions.txt",
                                     ref / "feuilles-ia.csv", d / "planexpert" / f"{s}.qpl")):
            out.append(s)
    return out


def evaluer(s: str) -> dict:
    d = DOSSIERS / s
    ref = d / "reference"
    dims = cq.lire_dimensions(ref / "dupuis-png-dimensions.txt", s)
    feuilles = cq.lire_feuilles(ref / "feuilles-ia.csv")
    humains = cq.lire_qpl(ref / f"{s}-Dupuis-PlanExpert.qpl", "humain")
    ias = cq.lire_qpl(d / "planexpert" / f"{s}.qpl", "ia")
    cq.preparer_humain(humains, dims)
    anomalies = cq.preparer_ia(ias, feuilles, d / "planexpert")
    comp = cq.comparer(humains, ias, anomalies)
    rel = lambda q: q.relative_to(RACINE).as_posix()  # chemins relatifs au dépôt : sortie identique partout (CI, cloud, PC)
    tot = cq.ecrire_sorties(comp, d / "comparaison-dupuis-qpl", {
        "dossier": s, "humain": rel(ref / f"{s}-Dupuis-PlanExpert.qpl"), "ia": rel(d / "planexpert" / f"{s}.qpl"),
        "dims": rel(ref / "dupuis-png-dimensions.txt"), "feuilles": rel(ref / "feuilles-ia.csv")})
    h, ia, a = tot["humaines"], tot["ia"], tot["appariees"]
    return {"humaines": h, "ia": ia, "appariees": a, "manquantes": tot["manquantes"], "en_trop": tot["en_trop"],
            "rappel": round(100 * a / h, 1) if h else 0.0, "precision": round(100 * a / ia, 1) if ia else 0.0}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--nouvelle-base", action="store_true", help="enregistrer les résultats comme ligne de base")
    args = p.parse_args(argv)
    jeu = dossiers_du_jeu()
    if not jeu:
        print("aucun dossier dans le jeu de référence", file=sys.stderr)
        return 2
    res = {s: evaluer(s) for s in jeu}
    SORTIE.mkdir(parents=True, exist_ok=True)
    (SORTIE / "resultats.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    base_path = SORTIE / "ligne-de-base.json"
    base = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else {}
    lignes = ["# Jeu de référence — relevé IA vs projets Plan Expert de l'estimateur", "",
              "_Généré par `python -m src.validation.jeu_reference` ; seuil d'appariement 1,2 % de la diagonale._", "",
              "| S- | Marques humaines | Marques IA | Appariées | Manquantes IA | En trop IA | Rappel | Précision | Δ rappel | Δ précision |",
              "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    regressions = []
    for s, r in res.items():
        b = base.get(s)
        dr = f"{r['rappel'] - b['rappel']:+.1f}" if b else "—"
        dp = f"{r['precision'] - b['precision']:+.1f}" if b else "—"
        if b and (r["rappel"] < b["rappel"] - TOLERANCE or r["precision"] < b["precision"] - TOLERANCE):
            regressions.append(s)
        lignes.append(f"| {s} | {r['humaines']} | {r['ia']} | {r['appariees']} | {r['manquantes']} | {r['en_trop']} | "
                      f"{r['rappel']:.1f} % | {r['precision']:.1f} % | {dr} | {dp} |")
    lignes += ["", f"Régressions (> {TOLERANCE} point) : {', '.join(regressions) if regressions else 'aucune'}", ""]
    (SORTIE / "resultats.md").write_text("\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    if args.nouvelle_base:
        base_path.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ligne de base enregistrée : {base_path}")
        return 0
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
