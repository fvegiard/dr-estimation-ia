#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Convertit un run de l'ancien protocole (chiffrage.py → chiffrage.json) vers le nouveau (quantites.json + decisions.json),
puis vérifie que le moteur commun redonne les mêmes totaux à partir des lignes du run.

Les lignes gardent leurs prix et temps tels quels (`prix.type = fixe`) : la conversion ne rechiffre rien, elle rend
le run lisible par `chiffrage_commun.py` et `comparer.py` (attribution de l'écart par décision). Les codes en double
reçoivent un suffixe « #n » ; les lots absents des lignes deviennent des lignes `lot`.

Usage : convertir_run.py <run_dir> [--decisions <fichier.json>] [--kit <kit>] [--ecrire]
    sans --ecrire : contrôle seulement (code 0 si les totaux sont reproduits, 1 sinon) ;
    --decisions   : decisions.json à recopier dans le run (sinon un fichier vide, à remplir).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chiffrage_commun import (  # noqa: E402
    ErreurChiffrage, Parametres, charger_catalogue, chiffrer, ecrire_json, lire_json,
)


def quantites_depuis_chiffrage(chiffrage: dict[str, Any], dossier: str, run: str) -> dict[str, Any]:
    """Lignes du chiffrage.json d'un run → quantites.json (prix fixes, codes dédoublonnés, lots en lignes)."""
    lignes_brutes = cast(list[dict[str, Any]], chiffrage.get('lignes', []))
    vus: dict[str, int] = {}
    lignes: list[dict[str, Any]] = []
    for lg in lignes_brutes:
        code = str(lg['code'])
        n = vus.get(code, 0) + 1
        vus[code] = n
        if n > 1:
            code = f"{code}#{n}"
        lignes.append({'code': code, 'desc': str(lg.get('desc', '')), 'q': float(lg['q']), 'u': str(lg.get('u', 'u')),
                       'art': str(lg['art']), 'src': str(lg.get('src', '')),
                       'prix': {'type': 'fixe', 'p': float(lg['p']), 'h': float(lg['h'])}})
    materiel_lignes = sum(float(lg['q']) * float(lg['p']) for lg in lignes_brutes)
    lots = cast(dict[str, Any], chiffrage.get('lots') or {})
    lots_deja_en_lignes = abs(materiel_lignes - float(chiffrage.get('materiel', 0.0))) < 0.01
    if not lots_deja_en_lignes:
        for nom, montant in lots.items():
            lignes.append({'code': f"LOT:{nom}"[:40], 'desc': str(nom), 'q': 1.0, 'u': 'lot', 'art': 'lot', 'src': 'lots du chiffrage.json',
                           'prix': {'type': 'fixe', 'p': float(montant), 'h': 0.0}, 'lot': True})
    return {
        'dossier': dossier,
        'protocole': 'converti',
        'source': f"converti depuis runs/{run}/chiffrage.json (ancien protocole : prix et temps recopiés tels quels, sans étiquette de décision)",
        'codes_dedoublonnes': sum(1 for v in vus.values() if v > 1),
        'lots_convertis_en_lignes': not lots_deja_en_lignes,
        'lignes': lignes,
    }


def controler(chiffrage: dict[str, Any], rechiffre: dict[str, Any]) -> list[str]:
    """Écarts entre les totaux du run et ceux que le moteur redonne (vides si tout est reproduit)."""
    ecarts: list[str] = []
    for cle, tol in (('materiel', 0.01), ('total_acceo', 0.01), ('heures_relevees', 0.01)):
        a = float(chiffrage.get(cle, 0.0))
        b = float(rechiffre[cle])
        if abs(a - b) > tol:
            ecarts.append(f"{cle} : run {a:.3f} ≠ moteur {b:.3f}")
    if int(chiffrage.get('heures_chargees', 0)) != int(rechiffre['heures_chargees']):
        ecarts.append(f"heures_chargees : run {chiffrage.get('heures_chargees')} ≠ moteur {rechiffre['heures_chargees']}")
    if int(chiffrage.get('prix_vente', 0)) != int(rechiffre['prix_vente']):
        ecarts.append(f"prix_vente : run {chiffrage.get('prix_vente')} ≠ moteur {rechiffre['prix_vente']}")
    return ecarts


def convertir(run_dir: Path, kit: Path, decisions: dict[str, Any], ecrire: bool) -> tuple[dict[str, Any], list[str]]:
    chiffrage = lire_json(run_dir / 'chiffrage.json')
    quantites = quantites_depuis_chiffrage(chiffrage, str(chiffrage.get('dossier') or kit.parent.name), run_dir.name)
    params = Parametres(taux=float(chiffrage.get('taux', 85.0)), facteur=float(chiffrage.get('facteur', 1.244)))
    catalogue = charger_catalogue(kit / 'catalogue-prix-temps-dupuis.csv')
    rechiffre = chiffrer(quantites, decisions, params, catalogue)
    ecarts = controler(chiffrage, rechiffre)
    if ecrire:
        ecrire_json(quantites, run_dir / 'quantites.json')
        ecrire_json(decisions, run_dir / 'decisions.json')
        ecrire_json(rechiffre, run_dir / 'chiffrage-moteur.json')
    return rechiffre, ecarts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ancien run (chiffrage.json) → quantites.json + decisions.json, contrôlés par le moteur commun")
    ap.add_argument('run_dir', type=Path)
    ap.add_argument('--kit', type=Path, default=None)
    ap.add_argument('--decisions', type=Path, default=None, help='decisions.json à recopier dans le run')
    ap.add_argument('--ecrire', action='store_true', help='écrit quantites.json, decisions.json et chiffrage-moteur.json dans le run')
    args = ap.parse_args(argv)
    run_dir: Path = args.run_dir
    kit: Path = args.kit if args.kit is not None else run_dir.resolve().parent.parent / 'kit'
    try:
        decisions = lire_json(args.decisions) if args.decisions is not None else {'justifications': {'_conversion': 'ancien protocole : décisions non étiquetées'}}
        rechiffre, ecarts = convertir(run_dir, kit, decisions, bool(args.ecrire))
    except ErreurChiffrage as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 2
    print(f"{run_dir.name} : moteur → matériel {rechiffre['materiel']:,.2f} $, {rechiffre['heures_chargees']} h, ACCEO {rechiffre['total_acceo']:,.2f} $, "
          f"prix {rechiffre['prix_vente']:,} $".replace(',', ' '))
    for e in ecarts:
        print('  ÉCART', e)
    return 1 if ecarts else 0


if __name__ == '__main__':
    sys.exit(main())
