#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Prépare un dossier de run isolé (hors dépôt) pour un chiffrage à l'aveugle selon le nouveau protocole.

Le dossier reçoit : le kit (relevé, Détail, bordereau, catalogue, METHODE.md, CONSIGNES.md, parametres.json), une copie du
moteur commun `chiffrage_commun.py` (l'agent peut se contrôler lui-même), `run.json` (modèle et effort DEMANDÉS — jamais
une preuve du modèle réellement exécuté) et `PROMPT.md` construit depuis `prompt-run.md` : la partie commune à tous
les runs d'abord (cachable par le fournisseur), la partie propre au run à la fin.

Usage : preparer_run.py <S> <nom_run> --dest <dossier hors dépôt> [--modele sonnet|opus] [--effort low|medium|high|xhigh|max]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHIERS_KIT = ('releve.xlsx', 'catalogue-prix-temps-dupuis.csv', 'METHODE.md', 'CONSIGNES.md', 'NOMENCLATURE.md', 'parametres.json',
                'rapport-releve.md', 'reserves.md')


def preparer(S: str, nom: str, dest: Path, modele: str, effort: str) -> Path:
    kit = RACINE / 'entrainement' / S / 'kit'
    if not kit.is_dir():
        raise SystemExit(f"kit introuvable : {kit}")
    if dest.resolve().is_relative_to(RACINE.resolve()):
        raise SystemExit(f"le dossier de run doit être hors du dépôt (reçu {dest})")
    run = dest / nom
    if run.exists():
        raise SystemExit(f"existe déjà : {run}")
    run.mkdir(parents=True)
    manquants: list[str] = []
    for f in FICHIERS_KIT:
        src = kit / f
        if src.exists():
            shutil.copy(src, run / f)
        else:
            manquants.append(f)
    if (kit / 'entree').is_dir():
        shutil.copytree(kit / 'entree', run / 'entree')
    shutil.copy(RACINE / 'entrainement' / 'chiffrage_commun.py', run / 'chiffrage_commun.py')
    gabarit = (RACINE / 'entrainement' / 'prompt-run.md').read_text(encoding='utf-8')
    prompt = gabarit.replace('{{S}}', S).replace('{{RUN}}', nom).replace('{{MODELE}}', modele).replace('{{EFFORT}}', effort)
    (run / 'PROMPT.md').write_text(prompt, encoding='utf-8')
    (run / 'run.json').write_text(json.dumps({
        'dossier': S, 'run': nom, 'modele_demande': modele, 'effort_demande': effort,
        'note': "modèle et effort DEMANDÉS au lancement ; le modèle réellement exécuté se lit dans la transcription de l'agent, pas ici",
        'kit_manquants': manquants, 'protocole': 'quantites.json + decisions.json → chiffrage_commun.py',
    }, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return run


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dossier de run isolé pour le chiffrage à l'aveugle (nouveau protocole)")
    ap.add_argument('S')
    ap.add_argument('nom_run')
    ap.add_argument('--dest', type=Path, required=True, help='dossier parent, hors du dépôt')
    ap.add_argument('--modele', default='sonnet', choices=('sonnet', 'opus', 'haiku', 'fable'))
    ap.add_argument('--effort', default='high', choices=('low', 'medium', 'high', 'xhigh', 'max'))
    args = ap.parse_args(argv)
    run = preparer(str(args.S), str(args.nom_run), Path(args.dest), str(args.modele), str(args.effort))
    print(f"run prêt : {run}\n  prompt : {run / 'PROMPT.md'}\n  attendu : quantites.json + decisions.json, puis python3 chiffrage_commun.py . --kit .")
    return 0


if __name__ == '__main__':
    sys.exit(main())
