#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Extrait de la référence gelée (dossiers/<S>/soumission/chiffrage_dupuis.py) les fichiers du nouveau protocole :
`quantites.json` et `decisions.json` à côté de la référence, `parametres.json` dans le kit.

Chaque ligne garde les valeurs exactes de la référence. Quand la source cite une entrée du catalogue Dupuis dont les
colonnes « À UTILISER » redonnent exactement le prix et le temps de la ligne, la ligne est écrite en `prix.type =
catalogue` (traçable) ; sinon elle reste en `fixe` avec sa source (jugement, Lumen, entrée absente du catalogue).
Les cinq décisions de portée du banc sont étiquetées sur les lignes concernées (voir METHODE.md §Décisions).

Usage : extraire_reference.py [S]   (défaut S-1902) — réexécutable, sortie identique à chaque fois.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chiffrage_commun import PI_PAR_M, charger_catalogue, cle_catalogue, ecrire_json  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent

# code → entrées du catalogue Dupuis (desc, mult) + suppléments, telles que la source de la référence les cite.
CATALOGUE_PAR_CODE: dict[str, dict[str, Any]] = {
    'A-03': {'entrees': [('ENLEVER PRISE', 1)]},
    'A-04': {'entrees': [('ENLEVER PRISE', 1)]},
    'A-05': {'entrees': [('RELO PRISE', 1)]},
    'A-06': {'entrees': [('RELO ENCASTRE', 1)]},
    'B-02': {'entrees': [('DISJ15A1P', 1)]},
    'B-04': {'entrees': [('DISJ 15A2P', 1)]},
    'C-01': {'entrees': [('MOTEUR UAF-1', 1)]},
    'C-01b': {'entrees': [('CONDUIT 1 13C12', 1)]},
    'C-02': {'entrees': [('MOTEUR', 1)]},
    'C-03': {'entrees': [('CHAUDIERE', 1)]},
    'C-04': {'entrees': [('HUMIDIFICATEUR', 1)]},
    'C-04b': {'entrees': [('INTERR 30A 3P 600V CEMA', 1)]},
    'C-07': {'entrees': [('CONDUIT 3/4 03C12', 1)]},
    'D-01': {'entrees': [('PRISE DUPLEX 15A 120V', 1), ('PRISE DUPLEX 15/20A 120V', 1), ('TEL/DATA', 1)],
             'supplement_p': 17.43, 'supplement_h': 0.5, 'note': 'boîte 12x12 17,43 $ / 0,5 h absente du catalogue → supplément'},
    'D-02': {'entrees': [('PRISE DUPLEX 15A 120V', 2), ('PRISE USB 125V 15 AMP', 4)]},
    'D-03': {'entrees': [('PRISE DUPLEX 15A 120V', 1)]},
    'D-04': {'entrees': [('PRISE DUPLEX 15A 120V', 1), ('TEL/DATA', 1)]},
    'D-05': {'entrees': [('PRISE DUPLEX 15A 120V', 1), ('TEL/DATA', 1)]},
    'D-06': {'entrees': [('PRISE DUPLEX 15A 120V', 1)]},
    'D-17': {'entrees': [('PRISE DUPLEX 15A 120V', 1)], 'supplement_p': 12.0, 'note': 'supplément dispositif IG ≈ 12 $ (Lumen LEV5262IG non lu)'},
    'D-07': {'entrees': [('PRISE DUPLEX 20A 125V GFI', 1)]},
    'D-08': {'entrees': [('TEL/DATA 3/4', 1)]},
    'D-11': {'entrees': [('LECTEUR DE CARTE', 1)]},
    'D-20': {'entrees': [('LECTEUR DE CARTE', 1), ('GACHE', 1)]},
    'D-21': {'entrees': [('THERMOSTAT', 1)]},
    'D-22': {'entrees': [('SORTIE TV', 1)]},
    'D-12': {'entrees': [('PERCEMENT PLANCHER', 1)]},
    'D-12b': {'entrees': [('COUPE FEU TUBE 10.1 FL O', 1)]},
    'D-13': {'entrees': [('CONDUIT 3/4 07C12', 1)]},
    'D-14': {'entrees': [('CONDUIT VIDE 3/4', 1)]},
    'D-19': {'entrees': [('SCAN DALLE BETON', 1)]},
    'E-03': {'entrees': [('MONUMENT PLANCHER', 1)]},
    'E-04': {'entrees': [('PRISE DUPLEX 15A 120V', 1)]},
    'E-01': {'entrees': [('PRISE DUPLEX 15A 120V', 2), ('TEL/DATA', 1)]},
    'E-05': {'entrees': [('PRISE DUPLEX 15A 120V', 1), ('TEL/DATA', 1)]},
    'F-01': {'entrees': [('FIXTURE TYPE A', 1)]},
    'F-07': {'entrees': [('ENSEIGNE SORTIE', 1)]},
    'F-11': {'entrees': [('INTERRUPTEUR 15A 120V', 1)]},
    'F-08': {'entrees': [('CONDUIT 3/4 03C12', 1)]},
    'G-01': {'entrees': [('DETECTEUR A FUMEE', 1)]},
    'G-02': {'entrees': [('CONDUIT VIDE 3/4', 1)], 'supplement_p': 0.41, 'supplement_h': 0.028, 'note': 'fil alarme 16 AWG 0,41 $/pi, 0,028 h/pi absent du catalogue → supplément'},
    'G-04': {'entrees': [('RELO PANN ANNOCIATEUR', 1)]},
    'H-01': {'entrees': [('NACELLE', 1)]},
}

# Les cinq décisions de portée (SYNTHESE.md) : quelles lignes elles touchent, dans la référence.
POSTES_COMPOSITES = ('D-01', 'D-02', 'D-03', 'D-04', 'D-05', 'D-06', 'E-01', 'E-04', 'E-05')   # lignes « poste de travail » de la feuille Détail
EAE_HORS_PLAN = ('A-01', 'A-02', 'A-03', 'A-04', 'A-05', 'A-06')                              # démantèlement/relocalisation depuis le Détail
LOTS = ('F-LOT', 'B-LOT', 'G-01b', 'G-07')
LOT_ECLAIRAGE_DETAIL = 11 * 185 + 12 * 290 + 15 * 230 + 6 * 110 + 1500 + 3 * 475 + 3 * 161.60   # 13 034,80 $
LOT_ECLAIRAGE_README = 11893.0

DECISIONS_REFERENCE: dict[str, Any] = {
    'postes_composites': 'en_plus',
    'monuments': 'lumen',
    'lot_eclairage': 'detail_13034_80',
    'eae_hors_plan': 'comptes',
    'conduits': 'temps_pi',
    'justifications': {
        'postes_composites': "Référence gelée 2026-10-20 : les postes de travail de la feuille Détail (D-01 ×18, D-02 ×5, D-03…D-06, E-01, E-04, E-05) sont comptés EN PLUS du relevé.",
        'monuments': "E-02 ×2 au prix Lumen 1 461,22 $ (poke-through Hubbell) ; E-03 ×2 au prix Dupuis 250 $.",
        'lot_eclairage': "chiffrage_dupuis.py F-LOT = somme du détail (A1 ×11, Axis ×33, trousses, E ×3, Z6 ×3) = 13 034,80 $ ; le 11 893 $ du README est l'allocation du midi.",
        'eae_hors_plan': "A-01…A-06 comptés depuis la feuille Détail (E.A.E/E.A.R hors plan), en 5.19 et 3.22.",
        'conduits': "Pas de colonne TEMPSEC au catalogue : temps/pi seulement ; 1\" 05c12 → « CONDUIT 3/4 07C12 », 1\" #8 → « CONDUIT 1 13C12 », longueurs du Détail en m × 3,28084.",
    },
}

PARAMETRES_REFERENCE: dict[str, Any] = {
    'taux': 85.0,
    'facteur': 1.244,
    'arrondi_heures': 10,
    'arrondi_prix': 1000,
    'pi_par_m': PI_PAR_M,
    'seuils': {'total_pct': 3.0, 'article_pct': 10.0, 'heures_pct': 5.0, 'historique_pct': 1.0},
    'source': "METHODE.md §5-7 : taux 85 $/h (Dupuis août-oct. 2026), facteur 1,244 (S-1844 : 191 909,19 → 238 744 $), arrondis Dupuis ; seuils = comparateur v2",
}


def charger_lignes_reference(script: Path) -> list[dict[str, Any]]:
    """Exécute le script de la référence dans un espace isolé et récupère sa liste L (il réécrit son propre JSON, à l'identique)."""
    espace: dict[str, Any] = {'__file__': str(script), '__name__': '__extraction__'}
    exec(compile(script.read_text(encoding='utf-8'), str(script), 'exec'), espace)  # noqa: S102 — script du dépôt, lu tel quel
    lignes = espace.get('L')
    if not isinstance(lignes, list):
        raise SystemExit(f"{script} : liste L introuvable")
    return [dict(cast(dict[str, Any], x)) for x in cast(list[Any], lignes)]


def spec_prix(code: str, p: float, h: float, catalogue: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Spécification de prix exacte pour la ligne : `catalogue` si les entrées citées redonnent (p, h), sinon `fixe`."""
    m = CATALOGUE_PAR_CODE.get(code)
    if m is not None:
        pc = float(m.get('supplement_p', 0.0))
        hc = float(m.get('supplement_h', 0.0))
        for desc, mult in m['entrees']:
            e = catalogue[cle_catalogue(desc)]
            pc += mult * e.prix
            hc += mult * e.temps
        if abs(pc - p) < 1e-9 and abs(hc - h) < 1e-9:
            spec: dict[str, Any] = {'type': 'catalogue', 'entrees': [{'desc': d, 'mult': mu} for d, mu in m['entrees']]}
            if m.get('supplement_p'):
                spec['supplement_p'] = m['supplement_p']
            if m.get('supplement_h'):
                spec['supplement_h'] = m['supplement_h']
            return spec, str(m.get('note', ''))
        return {'type': 'fixe', 'p': p, 'h': h}, f"catalogue cité mais valeurs différentes ({pc:.4f} $ / {hc:.4f} h) → valeur de la référence conservée"
    return {'type': 'fixe', 'p': p, 'h': h}, ''


def construire_quantites(lignes_ref: list[dict[str, Any]], catalogue: dict[str, Any], dossier: str) -> tuple[dict[str, Any], list[str]]:
    journal: list[str] = []
    lignes: list[dict[str, Any]] = []
    for x in lignes_ref:
        code = str(x['code'])
        spec, note = spec_prix(code, float(x['p']), float(x['h']), catalogue)
        ligne: dict[str, Any] = {'code': code, 'desc': x['desc'], 'q': x['q'], 'u': x['u'], 'art': x['art'], 'src': x['src']}
        if code == 'E-02':
            ligne['variantes'] = {'cle': 'monuments', 'options': {
                'lumen': {'prix': {'type': 'fixe', 'p': float(x['p']), 'h': float(x['h'])}},
                'dupuis': {'prix': {'type': 'catalogue', 'entrees': [{'desc': 'MONUMENT PLANCHER', 'mult': 1}]}}}}
        elif code == 'F-LOT':
            ligne['variantes'] = {'cle': 'lot_eclairage', 'options': {
                'detail_13034_80': {'prix': {'type': 'fixe', 'p': LOT_ECLAIRAGE_DETAIL, 'h': 0.0}},
                'readme_11893': {'prix': {'type': 'fixe', 'p': LOT_ECLAIRAGE_README, 'h': 0.0}}}}
        else:
            ligne['prix'] = spec
        if code in POSTES_COMPOSITES:
            ligne['decision'] = {'cle': 'postes_composites', 'actif_si': ['en_plus']}
        if code in EAE_HORS_PLAN:
            ligne['decision'] = {'cle': 'eae_hors_plan', 'actif_si': ['comptes']}
        if code in LOTS:
            ligne['lot'] = True
        if note:
            journal.append(f"{code}: {note}")
        lignes.append(ligne)
    quantites = {
        'dossier': dossier,
        'source': f"extrait de dossiers/{dossier}/soumission/chiffrage_dupuis.py (référence gelée 2026-10-20) par entrainement/extraire_reference.py",
        'unites': {'pi': 'longueurs du Détail en m × 3,28084', 'u': 'unité', 'lot': 'forfait', 'poste': 'poste de travail', 'cct': 'circuit', 'rangée': 'rangée de luminaires'},
        'lignes': lignes,
    }
    return quantites, journal


def main(argv: list[str]) -> int:
    dossier = argv[1] if len(argv) > 1 else 'S-1902'
    soumission = RACINE / 'dossiers' / dossier / 'soumission'
    kit = RACINE / 'entrainement' / dossier / 'kit'
    catalogue = charger_catalogue(kit / 'catalogue-prix-temps-dupuis.csv')
    lignes_ref = charger_lignes_reference(soumission / 'chiffrage_dupuis.py')
    quantites, journal = construire_quantites(lignes_ref, catalogue, dossier)
    ecrire_json(quantites, soumission / 'quantites.json')
    ecrire_json(DECISIONS_REFERENCE, soumission / 'decisions.json')
    ecrire_json(PARAMETRES_REFERENCE, kit / 'parametres.json')
    lignes_q = cast(list[dict[str, Any]], quantites['lignes'])
    n_cat = sum(1 for lg in lignes_q if cast(dict[str, Any], lg.get('prix', {})).get('type') == 'catalogue')
    print(f"{len(lignes_q)} lignes → {soumission / 'quantites.json'} ({n_cat} au catalogue, {len(lignes_q) - n_cat} fixes/variantes)")
    for j in journal:
        print('  ', j)
    print(f"decisions.json : { {k: v for k, v in DECISIONS_REFERENCE.items() if k != 'justifications'} }")
    print(f"parametres.json → {kit / 'parametres.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
