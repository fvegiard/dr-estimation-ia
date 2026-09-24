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

from collections import Counter

from src.qpl.categorie import categoriser
from src.qpl.normalisation import canonique
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
    res = {"humaines": h, "ia": ia, "appariees": a, "manquantes": tot["manquantes"], "en_trop": tot["en_trop"],
           "rappel": round(100 * a / h, 1) if h else 0.0, "precision": round(100 * a / ia, 1) if ia else 0.0}
    res["normalise"] = evaluer_normalise(s, comp)
    cat = accord_categories(comp)
    res["categorie"] = {"couples": cat["couples"], "accord": cat["accord"], "pourcentage": cat["pourcentage"],
                         "confusions": [{"humain": h, "ia": i, "n": n}
                                        for (h, i), n in cat["confusions"].most_common(5)]}
    return res, cat["confusions"]


def accord_categories(comp: "cq.Comparaison", seuil: float = cq.SEUIL_MARQUE) -> dict:
    """Among matched couples (position-based, unchanged), how many agree on
    CATEGORY (src.qpl.categorie.categoriser) rather than on the exact label —
    label agreement is ~0 % because the AI writes descriptive labels and the
    estimator writes short prefixed codes for the same device. Informative
    only : never used for the pass/fail regression check."""
    total = accord = 0
    confusions: Counter = Counter()
    for res in comp.resultats[seuil].values():
        for couple in res.couples:
            ch = categoriser(couple.humain.marque.libelle).categorie
            cia = categoriser(couple.ia.libelle).categorie
            total += 1
            if ch == cia:
                accord += 1
            else:
                confusions[(ch, cia)] += 1
    return {"couples": total, "accord": accord, "pourcentage": _pc(accord, total),
            "confusions": confusions}


def _pc(a: int, b: int) -> float:
    return round(100 * a / b, 1) if b else 0.0


def evaluer_normalise(s: str, comp_brut: "cq.Comparaison") -> dict:
    """Secondary metrics with the learnt label dictionary (reported, never used for regressions):
    label agreement of matched couples (raw vs canonical), and recall/precision after dropping
    noise labels ('rebut') on both sides."""
    brut = cq.accord_libelles(comp_brut)
    norm = cq.accord_libelles(comp_brut, canonique)
    d = DOSSIERS / s
    ref = d / "reference"
    dims = cq.lire_dimensions(ref / "dupuis-png-dimensions.txt", s)
    humains = cq.lire_qpl(ref / f"{s}-Dupuis-PlanExpert.qpl", "humain")
    ias = cq.lire_qpl(d / "planexpert" / f"{s}.qpl", "ia")
    rebut_h = cq.filtrer_rebut(humains, canonique)
    rebut_ia = cq.filtrer_rebut(ias, canonique)
    cq.preparer_humain(humains, dims)
    anomalies = cq.preparer_ia(ias, cq.lire_feuilles(ref / "feuilles-ia.csv"), d / "planexpert")
    comp = cq.comparer(humains, ias, anomalies)
    tot = cq.totaux(comp)
    acc = cq.accord_libelles(comp, canonique)
    return {"accord_libelle_brut": _pc(brut["accord"], brut["couples"]),
            "accord_libelle_canonique": _pc(norm["accord"], norm["couples"]),
            "rebut_humain": rebut_h, "rebut_ia": rebut_ia,
            "humaines": tot["humaines"], "ia": tot["ia"], "appariees": tot["appariees"],
            "rappel": _pc(tot["appariees"], tot["humaines"]), "precision": _pc(tot["appariees"], tot["ia"]),
            "accord_libelle_canonique_sans_rebut": _pc(acc["accord"], acc["couples"])}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--nouvelle-base", action="store_true", help="enregistrer les résultats comme ligne de base")
    args = p.parse_args(argv)
    jeu = dossiers_du_jeu()
    if not jeu:
        print("aucun dossier dans le jeu de référence", file=sys.stderr)
        return 2
    par_dossier = {s: evaluer(s) for s in jeu}
    res = {s: r for s, (r, _) in par_dossier.items()}
    confusions_globales: Counter = Counter()
    for _, confusions in par_dossier.values():
        confusions_globales.update(confusions)
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
    lignes += ["", f"Régressions (> {TOLERANCE} point) : {', '.join(regressions) if regressions else 'aucune'}", "",
               "## Normalised labels (apprentissage/qpl-2021-2026/normalisation.json) — informative only", "",
               "| S- | Label agreement raw | Label agreement canonical | Noise dropped H/IA | Recall (no noise) | Precision (no noise) |",
               "|---|--:|--:|--:|--:|--:|"]
    for s, r in res.items():
        n = r["normalise"]
        lignes.append(f"| {s} | {n['accord_libelle_brut']:.1f} % | {n['accord_libelle_canonique']:.1f} % | "
                      f"{n['rebut_humain']}/{n['rebut_ia']} | {n['rappel']:.1f} % | {n['precision']:.1f} % |")
    lignes += ["", "## Category agreement (src.qpl.categorie — rule-based, informative only)", "",
               "Among matched couples (position-based, unchanged), share whose category "
               "(dispositif / luminaire / securite_incendie / telecom_donnees / chauffage / "
               "distribution / mecanique_moteur / autre / indetermine) agrees — regardless of exact label wording.",
               "",
               "| S- | Matched couples | Category agreement |", "|---|--:|--:|"]
    for s, r in res.items():
        c = r["categorie"]
        lignes.append(f"| {s} | {c['couples']} | {c['pourcentage']:.1f} % |")
    lignes += ["", "### Top 5 disagreeing category pairs (all projects combined)", "",
               "| Human category | AI category | Occurrences |", "|---|---|--:|"]
    if confusions_globales:
        for (ch, cia), n in confusions_globales.most_common(5):
            lignes.append(f"| {ch} | {cia} | {n} |")
    else:
        lignes.append("| — | — | 0 |")
    lignes.append("")
    (SORTIE / "resultats.md").write_text("\n".join(lignes), encoding="utf-8")
    print("\n".join(lignes))
    if args.nouvelle_base:
        base_path.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ligne de base enregistrée : {base_path}")
        return 0
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
