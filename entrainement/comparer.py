#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare un run d'entraînement (chiffrage.json) à la référence gelée (chiffrage_dupuis.json) du dossier.
Usage : comparer.py <S> <run_dir>  → écrit <run_dir>/rapport.json et rapport.md ; code 0 si écart prix de vente ≤ 1 %, 1 sinon, 2 si fichier manquant."""
import json, sys, math
from pathlib import Path

S, run = sys.argv[1], Path(sys.argv[2])
root = Path(__file__).resolve().parent.parent
ref_p = root / 'dossiers' / S / 'soumission' / 'chiffrage_dupuis.json'
out_p = run / 'chiffrage.json'
if not ref_p.exists() or not out_p.exists():
    print(f"manquant: {ref_p if not ref_p.exists() else out_p}"); sys.exit(2)
ref = json.load(open(ref_p, encoding='utf-8'))
out = json.load(open(out_p, encoding='utf-8'))
FACT = 1.244
ref_pv = round(ref['total_acceo'] * FACT / 1000) * 1000

def d(a, b):
    return {'ref': a, 'run': b, 'delta': round(b - a, 2), 'pct': round((b - a) / a * 100, 2) if a else None}

tot = {
    'materiel': d(ref['materiel'], out.get('materiel', 0)),
    'heures_relevees': d(ref['heures_relevees'], out.get('heures_relevees', 0)),
    'heures_chargees': d(ref['heures_chargees'], out.get('heures_chargees', 0)),
    'total_acceo': d(ref['total_acceo'], out.get('total_acceo', 0)),
    'prix_vente': d(ref_pv, out.get('prix_vente', 0)),
}
arts = {}
for a in sorted(set(ref['par_article']) | set(out.get('par_article', {}))):
    r = ref['par_article'].get(a, {}); o = out.get('par_article', {}).get(a, {})
    rt = r.get('total', (r.get('materiel', 0) + r.get('heures', 0) * ref['taux'])) if r else 0
    ot = o.get('total', (o.get('materiel', 0) + o.get('heures', 0) * out.get('taux', 85))) if o else 0
    arts[a] = {'ref_h': r.get('heures'), 'run_h': o.get('heures'), 'ref_mat': r.get('materiel'), 'run_mat': o.get('materiel'), 'delta_total': round(ot - rt, 2)}
# lignes : rapprochement par code puis par article
ref_codes = {l['code']: l for l in ref['lignes']}
run_codes = {l.get('code'): l for l in out.get('lignes', [])}
communs = sorted(set(ref_codes) & set(run_codes))
ecarts_lignes = []
for c in communs:
    a, b = ref_codes[c], run_codes[c]
    if abs(a['q'] - b.get('q', 0)) > 1e-6 or abs(a['p'] - b.get('p', 0)) > 0.005 or abs(a['h'] - b.get('h', 0)) > 1e-3:
        ecarts_lignes.append({'code': c, 'ref': {k: a[k] for k in ('q', 'p', 'h')}, 'run': {k: b.get(k) for k in ('q', 'p', 'h')}, 'src_run': b.get('src')})
rapport = {
    'dossier': S, 'run': run.name, 'totaux': tot, 'par_article': arts,
    'lignes': {'ref': len(ref['lignes']), 'run': len(out.get('lignes', [])), 'codes_communs': len(communs),
               'manquantes': sorted(set(ref_codes) - set(run_codes)), 'en_plus': sorted(set(run_codes) - set(ref_codes)),
               'ecarts': ecarts_lignes},
    'verdict': 'OK' if tot['prix_vente']['pct'] is not None and abs(tot['prix_vente']['pct']) <= 1.0 else 'ÉCART',
}
json.dump(rapport, open(run / 'rapport.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
md = [f"# Rapport {S} — {run.name} : **{rapport['verdict']}**", "", "| Total | Référence | Run | Δ | % |", "|---|---|---|---|---|"]
for k, v in tot.items():
    md.append(f"| {k} | {v['ref']:,.2f} | {v['run']:,.2f} | {v['delta']:+,.2f} | {v['pct']:+.2f} % |".replace(',', ' '))
md += ["", f"Lignes : réf {len(ref['lignes'])}, run {len(out.get('lignes', []))}, communes {len(communs)}, écarts {len(ecarts_lignes)}, manquantes {len(rapport['lignes']['manquantes'])}, en plus {len(rapport['lignes']['en_plus'])}", "", "| Article | h réf | h run | mat réf | mat run | Δ total |", "|---|---|---|---|---|---|"]
for a, v in arts.items():
    md.append(f"| {a} | {v['ref_h']} | {v['run_h']} | {v['ref_mat']} | {v['run_mat']} | {v['delta_total']:+.2f} |")
if ecarts_lignes:
    md += ["", "## Écarts par ligne (code commun)", "| code | réf q/p/h | run q/p/h | source run |", "|---|---|---|---|"]
    for e in ecarts_lignes[:60]:
        md.append(f"| {e['code']} | {e['ref']['q']}/{e['ref']['p']}/{e['ref']['h']} | {e['run']['q']}/{e['run']['p']}/{e['run']['h']} | {str(e['src_run'])[:60]} |")
(run / 'rapport.md').write_text('\n'.join(md), encoding='utf-8')
print('\n'.join(md[:9]))
sys.exit(0 if rapport['verdict'] == 'OK' else 1)
