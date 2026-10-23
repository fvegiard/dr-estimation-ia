#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Écrit `<kit>/NOMENCLATURE.md` : les codes de ligne imposés aux runs (code, libellé court, unité, article du bordereau),
tirés de `dossiers/<S>/soumission/quantites.json` sans rien révéler du résultat — ni quantité, ni prix, ni temps, ni le
raisonnement des décisions de portée. Les parenthèses qui contiennent un nombre sont retirées ; quelques libellés sont
remplacés explicitement (LIBELLES_NEUTRES) parce que leur formulation trahirait une décision.

Usage : nomenclature.py [S]   (défaut S-1902) — réexécutable, sortie identique.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, cast

RACINE = Path(__file__).resolve().parent.parent

LIBELLES_NEUTRES: dict[str, str] = {
    'D-01': 'Poste de travail intégré au mobilier (feuille Détail) : JB + prises + boîte data',
    'D-02': "Tables avec boîte d'électrification (feuille Détail) : prises doubles + prises USB",
    'D-08': 'Sorties data murales/colonne : boîte + conduit 3/4" + corde',
    'D-13': 'Conduit EMT 1" sous dalle, conducteurs #12',
    'D-14': 'Conduit EMT 3/4" data sous dalle, vide + corde',
    'D-17': 'Prises MALT isolées (IG orange)',
    'E-02': 'Monuments de plancher poke-through (prise + RJ45)',
    'F-02': 'Luminaires C1 / C1_1 / C1_3 Axis — pose',
    'F-05': 'Rangées linéaires suspendues : suspension à la dalle, alimentation',
    'F-08': 'Conduit EMT 3/4" + flexible — raccordement des luminaires',
    'F-LOT': 'PRIX DE LOT ÉCLAIRAGE (luminaires, trousses, enseignes)',
    'B-LOT': 'PRIX DE LOT DISTRIBUTION (panneau NF + disjoncteurs)',
    'G-07': 'Services JCI/Simplex (bypass, programmation, annonciateur, vérification, certificat)',
    'B-01b': 'Transfert des circuits existants dans PP-3',
    'B-09': 'Mise à jour des fiches + identification des panneaux',
}

ARTICLE_FRAIS = ('H-01', 'H-02', 'H-03', 'H-04')


def libelle_court(code: str, desc: str) -> str:
    if code in LIBELLES_NEUTRES:
        return LIBELLES_NEUTRES[code]
    court = re.sub(r'\s*\([^)]*\d[^)]*\)', '', desc)       # parenthèses contenant un nombre
    court = re.sub(r'\s*—\s*\d[^—]*$', '', court)           # « — 22 dispositifs »
    return re.sub(r'\s{2,}', ' ', court).strip()


def nomenclature(S: str) -> str:
    q = cast(dict[str, Any], json.loads((RACINE / 'dossiers' / S / 'soumission' / 'quantites.json').read_text(encoding='utf-8')))
    lignes = cast(list[dict[str, Any]], q['lignes'])
    md = [f"# Nomenclature des codes de ligne — {S}", "",
          "Codes imposés aux runs (libellé court, unité, article du bordereau). Un code = une ligne de `quantites.json` ; les quantités,",
          "prix et temps viennent de toi et des entrées du kit. Une quantité sans code reçoit un code `X-nn` avec un libellé clair.",
          "Les lignes de lot (`lot`) portent `\"lot\": true` ; les frais de chantier et heures de jugement (H-xx) vont dans l'article indiqué.", "",
          "| Code | Libellé | Unité | Article |", "|---|---|---|---|"]
    for lg in lignes:
        code = str(lg['code'])
        md.append(f"| {code} | {libelle_court(code, str(lg.get('desc', '')))} | {lg.get('u', 'u')} | {lg['art']} |")
    md += ["", f"Articles du bordereau utilisés : {', '.join(sorted({str(lg['art']) for lg in lignes}))}.",
           f"Frais de chantier et jugement ({', '.join(ARTICLE_FRAIS)}) : article {lignes[-1]['art']}."]
    return '\n'.join(md) + '\n'


def main(argv: list[str]) -> int:
    S = argv[1] if len(argv) > 1 else 'S-1902'
    texte = nomenclature(S)
    sortie = RACINE / 'entrainement' / S / 'kit' / 'NOMENCLATURE.md'
    sortie.write_text(texte, encoding='utf-8')
    print(texte)
    print(f"→ {sortie}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
