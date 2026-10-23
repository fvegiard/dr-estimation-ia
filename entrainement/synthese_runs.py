#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Synthèse automatique d'un banc : lit `runs/*/rapport.json` (comparateur v2) et écrit `SYNTHESE-auto.md`.

Une ligne par run (prix, écart, heures, articles hors seuil, verdict), puis l'écart attribué à chaque décision de portée
(moyenne et étendue sur les runs) et le reste non attribué. Rien n'est saisi à la main : relancer ce script après chaque
run ou après tout changement de la référence ou des seuils.

Usage : synthese_runs.py <S>
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import Any, cast

RACINE = Path(__file__).resolve().parent.parent


def lire_rapports(dossier_runs: Path) -> list[dict[str, Any]]:
    rapports: list[dict[str, Any]] = []
    for run in sorted(p for p in dossier_runs.iterdir() if (p / 'rapport.json').exists()):
        rapports.append(cast(dict[str, Any], json.loads((run / 'rapport.json').read_text(encoding='utf-8'))))
    return rapports


def fmt(v: float | None, dec: int = 0, signe: bool = False) -> str:
    if v is None:
        return '—'
    s = f"{v:+,.{dec}f}" if signe else f"{v:,.{dec}f}"
    return s.replace(',', ' ')


def synthese(S: str, rapports: list[dict[str, Any]]) -> str:
    if not rapports:
        return f"# Synthèse {S}\n\nAucun rapport.json dans runs/.\n"
    ref_prix = float(cast(dict[str, Any], rapports[0]['totaux'])['prix_vente']['ref'])
    md = [f"# Synthèse automatique — {S} ({len(rapports)} runs)", "",
          f"Référence : {fmt(ref_prix)} $. Généré par `entrainement/synthese_runs.py` depuis `runs/*/rapport.json` (comparateur v2 : "
          "prix ±total_pct, heures ±heures_pct, chaque article ±article_pct). Un run est OK seulement si les trois critères passent.", "",
          "| Run | Protocole | Prix ($) | Δ prix | Δ heures | Articles hors seuil | Codes rappel / précision | ±1 % | Verdict |",
          "|---|---|---|---|---|---|---|---|---|"]
    pcts: list[float] = []
    for r in rapports:
        tot = cast(dict[str, dict[str, Any]], r['totaux'])
        cr = cast(dict[str, Any], r['criteres'])
        pct = tot['prix_vente']['pct']
        if isinstance(pct, (int, float)):
            pcts.append(float(pct))
        hors = cast(list[str], cr['articles']['hors_seuil'])
        md.append(f"| {r['run']} | {r['protocole']} | {fmt(float(tot['prix_vente']['run']))} | {fmt(pct, 1, True) if isinstance(pct, (int, float)) else '—'} % "
                  f"| {fmt(tot['heures_chargees']['pct'], 1, True) if isinstance(tot['heures_chargees']['pct'], (int, float)) else '—'} % "
                  f"| {len(hors)} ({', '.join(hors[:6])}{'…' if len(hors) > 6 else ''}) | {cr['rappel_codes']} / {cr['precision_codes']} "
                  f"| {'oui' if cr['dans_1_pct'] else 'non'} | {r['verdict']} |")
    if pcts:
        md += ["", f"Écart moyen sur le prix : {statistics.fmean(pcts):+.1f} % ; écart-type {statistics.stdev(pcts):.2f} points"
               if len(pcts) >= 2 else f"Écart sur le prix : {pcts[0]:+.1f} %",
               f" ; {sum(1 for r in rapports if r['verdict'] == 'OK')}/{len(rapports)} OK."]
    # attribution par décision
    par_dec: dict[str, list[float]] = {}
    identiques: dict[str, int] = {}
    modes: set[str] = set()
    autres: list[float] = []
    hors_decisions: list[float] = []
    for r in rapports:
        att = cast(dict[str, Any], r['attribution'])
        modes.add(str(att['mode']))
        for d in cast(list[dict[str, Any]], att['decisions']):
            if d.get('identique'):
                identiques[str(d['decision'])] = identiques.get(str(d['decision']), 0) + 1
                continue
            v = d.get('delta_acceo')
            if isinstance(v, (int, float)):
                par_dec.setdefault(str(d['decision']), []).append(float(v))
        a = att.get('autres_articles_delta_acceo')
        if isinstance(a, (int, float)):
            autres.append(float(a))
        h = att.get('hors_decisions_acceo')
        if isinstance(h, (int, float)):
            hors_decisions.append(float(h))
    md += ["", "## Écart attribué aux décisions de portée (Δ ACCEO, $ ; Δ = run − référence)", "", f"Mode(s) : {' ; '.join(sorted(modes))}.", "",
           "| Décision | Runs où elle diffère | Moyenne | Min | Max | Stable ? |", "|---|---|---|---|---|---|"]
    for cle, vals in par_dec.items():
        et = statistics.stdev(vals) if len(vals) >= 2 else 0.0
        stable = 'oui' if abs(statistics.fmean(vals)) > 0 and et <= 0.15 * abs(statistics.fmean(vals)) else 'non'
        md.append(f"| {cle} | {len(vals)} | {fmt(statistics.fmean(vals), 0, True)} | {fmt(min(vals), 0, True)} | {fmt(max(vals), 0, True)} | {stable} |")
    for cle, n_id in identiques.items():
        if cle not in par_dec:
            md.append(f"| {cle} | 0 (identique à la référence dans {n_id} runs) | — | — | — | — |")
    if hors_decisions:
        md.append(f"| hors décisions (relevé, prix, temps) | {len(hors_decisions)} | {fmt(statistics.fmean(hors_decisions), 0, True)} | {fmt(min(hors_decisions), 0, True)} | {fmt(max(hors_decisions), 0, True)} | — |")
    if autres:
        md.append(f"| autres articles et décisions identiques (non attribués) | {len(autres)} | {fmt(statistics.fmean(autres), 0, True)} | {fmt(min(autres), 0, True)} | {fmt(max(autres), 0, True)} | — |")
    md += ["", "Lecture : en mode « approximation par articles » (ancien protocole), l'effet d'une décision est l'écart des articles qu'elle touche, "
           "pas son effet exact ; en mode « exact » (nouveau protocole), c'est le run rechiffré avec la décision de la référence."]
    return '\n'.join(md) + '\n'


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage : synthese_runs.py <S>", file=sys.stderr)
        return 2
    S = args[0]
    dossier = RACINE / 'entrainement' / S
    rapports = lire_rapports(dossier / 'runs')
    texte = synthese(S, rapports)
    (dossier / 'SYNTHESE-auto.md').write_text(texte, encoding='utf-8')
    print(texte)
    return 0


if __name__ == '__main__':
    sys.exit(main())
