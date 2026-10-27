#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Calibre le facteur de passage « sommaire ACCEO → prix remis » de Daniel Dupuis sur les couples connus,
et mesure la position de ses prix par rapport au plus bas soumissionnaire quand le résultat d'ouverture est connu.

Entrée : prix/dupuis/couples-sommaire-prix-remis.csv (séparateur ;) — une ligne par dossier remis :
    dossier;date;sommaire_acceo;prix_remis;plus_bas_soumissionnaire;gagnant;source;a_verifier
    Les colonnes vides sont permises (un couple sans sommaire ne sert qu'à la colonne « plus bas »).
Sortie : prix/dupuis/calibration-facteur.md (rapport) ; code 0. Le facteur n'est JAMAIS écrit dans parametres.json
par ce script : c'est une décision de Jo, le rapport la prépare.

Usage : calibrer_facteur.py [--csv <fichier>] [--sortie <rapport.md>]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CSV_DEFAUT = RACINE / 'prix' / 'dupuis' / 'couples-sommaire-prix-remis.csv'
RAPPORT_DEFAUT = RACINE / 'prix' / 'dupuis' / 'calibration-facteur.md'


@dataclass(frozen=True)
class Couple:
    dossier: str
    date: str
    sommaire_acceo: float | None
    prix_remis: float | None
    plus_bas: float | None
    gagnant: str
    source: str
    a_verifier: bool

    @property
    def ratio(self) -> float | None:
        if self.sommaire_acceo and self.prix_remis:
            return self.prix_remis / self.sommaire_acceo
        return None

    @property
    def pct_vs_plus_bas(self) -> float | None:
        if self.plus_bas and self.prix_remis:
            return (self.prix_remis / self.plus_bas - 1.0) * 100.0
        return None


def _nombre(v: str) -> float | None:
    v = v.strip().replace(' ', '').replace(' ', '').replace(',', '.')
    if not v:
        return None
    try:
        return float(v)
    except ValueError as e:
        raise SystemExit(f"valeur numérique illisible : {v!r} ({e})") from e


def lire_couples(chemin: Path) -> list[Couple]:
    with chemin.open(encoding='utf-8-sig', newline='') as f:
        lignes = list(csv.DictReader(f, delimiter=';'))
    couples: list[Couple] = []
    for lg in lignes:
        couples.append(Couple(
            dossier=(lg.get('dossier') or '').strip(), date=(lg.get('date') or '').strip(),
            sommaire_acceo=_nombre(lg.get('sommaire_acceo') or ''), prix_remis=_nombre(lg.get('prix_remis') or ''),
            plus_bas=_nombre(lg.get('plus_bas_soumissionnaire') or ''), gagnant=(lg.get('gagnant') or '').strip(),
            source=(lg.get('source') or '').strip(), a_verifier=(lg.get('a_verifier') or '').strip().lower() in ('oui', 'x', '1', 'vrai', 'true'),
        ))
    return couples


def statistiques(valeurs: list[float]) -> dict[str, float | None]:
    if not valeurs:
        return {'n': 0, 'moyenne': None, 'ecart_type': None, 'min': None, 'max': None}
    return {
        'n': len(valeurs), 'moyenne': statistics.fmean(valeurs),
        'ecart_type': statistics.stdev(valeurs) if len(valeurs) >= 2 else None,
        'min': min(valeurs), 'max': max(valeurs),
    }


def rapport(couples: list[Couple], facteur_actuel: float, acceo_exemple: float) -> str:
    ratios = [r for r in (c.ratio for c in couples) if r is not None]
    ratios_confirmes = [r for r in (c.ratio for c in couples if not c.a_verifier) if r is not None]
    st = statistiques(ratios_confirmes)
    st_tous = statistiques(ratios)
    pcts = [p for p in (c.pct_vs_plus_bas for c in couples) if p is not None]
    sp = statistiques(pcts)
    md = ["# Calibration du facteur « sommaire ACCEO → prix remis » (Daniel Dupuis)", "",
          "Généré par `entrainement/calibrer_facteur.py` depuis `prix/dupuis/couples-sommaire-prix-remis.csv`. Le facteur en vigueur reste",
          f"celui du kit (`parametres.json` : {facteur_actuel}) tant que Jo n'en décide pas autrement.", "",
          "| Dossier | Date | Sommaire ACCEO ($) | Prix remis ($) | Ratio | Plus bas ($) | Dupuis vs plus bas | Gagnant | Source | À vérifier |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c in couples:
        md.append("| {d} | {dt} | {s} | {p} | {r} | {pb} | {pv} | {g} | {src} | {av} |".format(
            d=c.dossier, dt=c.date or '—',
            s=f"{c.sommaire_acceo:,.2f}".replace(',', ' ') if c.sommaire_acceo else '—',
            p=f"{c.prix_remis:,.0f}".replace(',', ' ') if c.prix_remis else '—',
            r=f"{c.ratio:.3f}" if c.ratio is not None else '—',
            pb=f"{c.plus_bas:,.0f}".replace(',', ' ') if c.plus_bas else '—',
            pv=f"{c.pct_vs_plus_bas:+.1f} %" if c.pct_vs_plus_bas is not None else '—',
            g=c.gagnant or '—', src=c.source or '—', av='oui' if c.a_verifier else ''))
    md += ["", "## Facteur", ""]
    n = int(st['n'] or 0)
    if n == 0:
        md.append("Aucun couple confirmé : le facteur ne peut pas être calibré.")
    elif n == 1:
        md.append(f"Un seul couple confirmé (ratio {st['moyenne']:.3f}) : écart-type indéfini, le facteur n'est pas calibré, "
                  "il est posé. Il faut au moins 5 dossiers remis par Daniel avec leur sommaire ACCEO pour parler de calibration.")
    else:
        moy = float(st['moyenne'] or 0.0)
        et = st['ecart_type']
        md.append(f"{n} couples confirmés : ratio moyen {moy:.3f}, écart-type {et:.3f}, min {st['min']:.3f}, max {st['max']:.3f}."
                  if et is not None else f"{n} couples confirmés : ratio moyen {moy:.3f}.")
        if et is not None:
            md.append(f"Sur un sommaire de {acceo_exemple:,.0f} $, ±1 écart-type = ±{acceo_exemple * et:,.0f} $ sur le prix de vente "
                      f"({et / moy * 100:.1f} %).".replace(',', ' '))
    n_tous = int(st_tous['n'] or 0)
    if n_tous > n:
        moy_t = float(st_tous['moyenne'] or 0.0)
        et_t = st_tous['ecart_type']
        md.append("")
        mn_t = float(st_tous['min'] or 0.0)
        mx_t = float(st_tous['max'] or 0.0)
        etendue = f"écart-type {et_t:.3f}, min {mn_t:.3f}, max {mx_t:.3f}" if et_t is not None else ""
        variation = f" de {et_t / moy_t * 100:.0f} % (±{acceo_exemple * et_t:,.0f} $ sur {acceo_exemple:,.0f} $)".replace(',', ' ') if et_t is not None else ''
        md.append(f"En comptant les {n_tous - n} couples « à vérifier » ({n_tous} au total) : ratio moyen {moy_t:.3f}, {etendue}. "
                  f"Lecture : le facteur n'est pas une constante de Dupuis ; il varie d'un dossier à l'autre{variation}. "
                  "Ces couples doivent être confirmés (même portée, auteur du prix) avant de changer parametres.json.")
    md += ["", f"Sensibilité sur un sommaire de {acceo_exemple:,.0f} $ :".replace(',', ' '), "", "| Facteur | Prix de vente ($) | vs facteur actuel |", "|---|---|---|"]
    facteurs: set[float] = {1.20, facteur_actuel, 1.30, 1.35}
    if n:
        facteurs.add(round(float(st['moyenne'] or 0.0), 3))
    if n_tous:
        facteurs.add(round(float(st_tous['moyenne'] or 0.0), 3))
    for k in sorted(facteurs):
        pv = acceo_exemple * k
        md.append(f"| {k:.3f} | {round(pv / 1000) * 1000:,.0f} | {(k / facteur_actuel - 1) * 100:+.1f} % |".replace(',', ' '))
    a_faire = [c for c in couples if c.sommaire_acceo and not c.prix_remis]
    if a_faire:
        md += ["", "## Prix remis à retrouver (un sommaire ACCEO existe, le prix remis manque)", ""]
        for c in a_faire:
            montant = f"{c.sommaire_acceo:,.2f}".replace(',', ' ')
            md.append(f"- {c.dossier} (sommaire {montant} $) : {c.source or 'source à préciser'}")
        md.append("")
        md.append(f"Avec ces {len(a_faire)} prix, le facteur reposerait sur {len(a_faire) + n} couples au lieu de {n}.")
    md += ["", "## Position par rapport au plus bas soumissionnaire", ""]
    if not pcts:
        md.append("Aucun résultat d'ouverture avec le prix du plus bas soumissionnaire dans le fichier.")
    else:
        md.append(f"{int(sp['n'] or 0)} dossiers avec résultat d'ouverture : Dupuis en moyenne {float(sp['moyenne'] or 0.0):+.1f} % par rapport au plus bas "
                  f"(min {float(sp['min'] or 0.0):+.1f} %, max {float(sp['max'] or 0.0):+.1f} %). Viser le prix de Dupuis, c'est viser cette position ; "
                  "le banc doit aussi mesurer l'écart au plus bas.")
    return '\n'.join(md) + '\n'


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Calibration du facteur ACCEO → prix remis et position vs plus bas soumissionnaire")
    ap.add_argument('--csv', type=Path, default=CSV_DEFAUT)
    ap.add_argument('--sortie', type=Path, default=RAPPORT_DEFAUT)
    ap.add_argument('--dossier', default='S-1902', help='dossier dont le kit donne le facteur en vigueur et la référence le sommaire d’exemple')
    ap.add_argument('--facteur-actuel', type=float, default=None, help='défaut : facteur de entrainement/<dossier>/kit/parametres.json')
    ap.add_argument('--acceo-exemple', type=float, default=None, help='défaut : total ACCEO de dossiers/<dossier>/soumission/chiffrage_dupuis.json')
    args = ap.parse_args(argv)
    chemin: Path = args.csv
    if not chemin.exists():
        print(f"fichier manquant : {chemin}", file=sys.stderr)
        return 2
    facteur_actuel = args.facteur_actuel
    if facteur_actuel is None:
        params = RACINE / 'entrainement' / str(args.dossier) / 'kit' / 'parametres.json'
        if not params.exists():
            print(f"facteur en vigueur introuvable ({params}) : passer --facteur-actuel", file=sys.stderr)
            return 2
        facteur_actuel = float(json.loads(params.read_text(encoding='utf-8'))['facteur'])
    acceo_exemple = args.acceo_exemple
    if acceo_exemple is None:
        ref = RACINE / 'dossiers' / str(args.dossier) / 'soumission' / 'chiffrage_dupuis.json'
        if not ref.exists():
            print(f"sommaire d'exemple introuvable ({ref}) : passer --acceo-exemple", file=sys.stderr)
            return 2
        acceo_exemple = float(json.loads(ref.read_text(encoding='utf-8'))['total_acceo'])
    couples = lire_couples(chemin)
    texte = rapport(couples, float(facteur_actuel), float(acceo_exemple))
    sortie: Path = args.sortie
    sortie.write_text(texte, encoding='utf-8')
    print(texte)
    print(f"→ {sortie}")
    return 0 if all(not math.isnan(c.ratio or 0.0) for c in couples) else 1


if __name__ == '__main__':
    sys.exit(main())
