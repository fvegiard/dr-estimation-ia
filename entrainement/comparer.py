#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Compare un run d'entraînement à la référence gelée du dossier et attribue l'écart aux décisions de portée.

Usage : comparer.py <S> <run_dir> [--kit <kit>]  → écrit <run_dir>/rapport.json et rapport.md.
Codes de sortie : 0 si le verdict est OK, 1 sinon, 2 si un fichier manque ou est invalide.

Convention de signe, partout : Δ = run − référence (négatif = le run est en dessous). Elle vaut pour les totaux,
les articles et l'écart attribué à chaque décision, dans les deux modes.

Deux protocoles de run sont acceptés :
- ancien : `chiffrage.json` écrit par le `chiffrage.py` du run (lignes à prix fixes, pas d'étiquette de décision) ;
  un run converti par `convertir_run.py` (`quantites.json` avec `protocole: converti`) reste dans ce mode ;
- nouveau : `quantites.json` + `decisions.json` ; `chiffrage.json` est recalculé ici par le moteur commun à chaque
  comparaison, et l'écart est attribué décision par décision par contrefactuel : Δ(décision) = run − run rechiffré
  avec la décision de la référence. Sans ligne étiquetée, l'effet des décisions n'est pas mesurable et le rapport le dit.

Verdict (seuils dans `<kit>/parametres.json`, clé `seuils`) : prix de vente dans ±total_pct ET heures chargées dans
±heures_pct (au moins un pas d'arrondi des heures) ET chaque article du bordereau dans ±article_pct (ou ±article_min_abs $).
Le ±1 % historique est rapporté (`dans_1_pct`) mais ne fait plus le verdict : un total juste peut cacher des erreurs qui
se compensent. Le prix de vente du run est recalculé depuis son total ACCEO avec le facteur et l'arrondi du kit, pour que
référence et run soient jugés avec le même facteur ; le prix déclaré par le run est rapporté à part s'il diffère.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chiffrage_commun import (  # noqa: E402
    DECISIONS_CONNUES, ErreurChiffrage, Parametres, charger_catalogue, chiffrer, ecrire_json, lire_json,
)

SEUILS_DEFAUT: dict[str, float] = {'total_pct': 3.0, 'article_pct': 10.0, 'heures_pct': 5.0, 'historique_pct': 1.0, 'article_min_abs': 1000.0}

# Ancien protocole : à défaut d'étiquettes sur les lignes, chaque décision est approchée par les articles qu'elle touche
# (SYNTHESE.md 2026-10-21). C'est une approximation ; le nouveau protocole calcule l'effet exact par contrefactuel.
ARTICLES_PAR_DECISION: dict[str, tuple[str, ...]] = {
    'postes_composites': ('3.27', '3.28'),
    'monuments': ('3.34',),
    'lot_eclairage': ('3.35',),
    'eae_hors_plan': ('3.22', '5.19'),
    'conduits': ('3.23', '3.31', '3.33'),
}


def ecart(a: float, b: float) -> dict[str, Any]:
    return {'ref': a, 'run': b, 'delta': round(b - a, 2), 'pct': round((b - a) / a * 100, 2) if a else None}


def total_article(v: dict[str, Any], taux: float) -> float:
    if 'total' in v:
        return float(v['total'])
    return float(v.get('materiel', 0.0)) + float(v.get('heures', 0.0)) * taux


def charger_seuils(kit: Path) -> dict[str, float]:
    seuils = dict(SEUILS_DEFAUT)
    chemin = kit / 'parametres.json'
    if chemin.exists():
        params = lire_json(chemin)
        for k, v in cast(dict[str, Any], params.get('seuils', {})).items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                seuils[str(k)] = float(v)
    return seuils


def parametres_kit(kit: Path, ref: dict[str, Any]) -> Parametres:
    """Paramètres du kit ; à défaut, ceux que la référence déclare, sinon les valeurs historiques (85 $/h, 1,244)."""
    chemin = kit / 'parametres.json'
    if chemin.exists():
        return Parametres.depuis(lire_json(chemin))
    return Parametres(taux=float(ref.get('taux', 85.0)), facteur=float(ref.get('facteur', 1.244)))


def arrondir_prix(total_acceo: float, params: Parametres) -> float:
    ap = params.arrondi_prix
    return float(round(total_acceo * params.facteur / ap) * ap) if ap > 0 else round(total_acceo * params.facteur, 2)


def lignes_etiquetees(quantites: dict[str, Any]) -> bool:
    """Vrai si au moins une ligne porte une étiquette de décision (`decision` ou `variantes`)."""
    return any(('decision' in lg or 'variantes' in lg) for lg in cast(list[dict[str, Any]], quantites.get('lignes', [])))


def protocole_du_run(run: Path, kit: Path) -> str:
    """'nouveau' si quantites.json + decisions.json existent et que quantites.json n'est pas une conversion, sinon 'ancien'."""
    if (run / 'quantites.json').exists() and (run / 'decisions.json').exists() and (kit / 'parametres.json').exists():
        if lire_json(run / 'quantites.json').get('protocole') != 'converti':
            return 'nouveau'
    return 'ancien'


def chiffrage_du_run(run: Path, kit: Path, protocole: str) -> dict[str, Any]:
    """chiffrage.json du run : recalculé par le moteur et réécrit sur disque en protocole nouveau, lu tel quel sinon."""
    if protocole == 'nouveau':
        params = Parametres.depuis(lire_json(kit / 'parametres.json'))
        catalogue = charger_catalogue(kit / 'catalogue-prix-temps-dupuis.csv')
        c = chiffrer(lire_json(run / 'quantites.json'), lire_json(run / 'decisions.json'), params, catalogue)
        ecrire_json(c, run / 'chiffrage.json')
        return c
    return lire_json(run / 'chiffrage.json')


def attribution_exacte(run: Path, kit: Path, ref: dict[str, Any], ref_decisions: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """Nouveau protocole. Δ(décision) = run − run rechiffré avec la décision de la référence (négatif = la décision du run
    fait baisser le prix). `hors_decisions` = run rechiffré avec TOUTES les décisions de la référence − référence : ce qui
    reste quand les décisions sont alignées, c'est l'écart de relevé. `interaction` = ce que les Δ un à un ne capturent
    pas (arrondi des heures chargées au multiple de 10, surtout)."""
    params = Parametres.depuis(lire_json(kit / 'parametres.json'))
    catalogue = charger_catalogue(kit / 'catalogue-prix-temps-dupuis.csv')
    quantites = lire_json(run / 'quantites.json')
    decisions = lire_json(run / 'decisions.json')
    if not lignes_etiquetees(quantites):
        return {'mode': "exact impossible : aucune ligne étiquetée (decision / variantes) dans quantites.json, l'effet des décisions n'est pas mesurable",
                'decisions': [], 'etiquetage': False}
    details: list[dict[str, Any]] = []
    somme_acceo = 0.0
    somme_prix = 0
    for cle in DECISIONS_CONNUES:
        if cle not in decisions or cle not in ref_decisions or decisions[cle] == ref_decisions[cle]:
            continue
        contre = dict(decisions)
        contre[cle] = ref_decisions[cle]
        try:
            c = chiffrer(quantites, contre, params, catalogue)
        except ErreurChiffrage as e:
            details.append({'decision': cle, 'run': decisions[cle], 'ref': ref_decisions[cle], 'erreur': str(e)})
            continue
        d_acceo = round(float(base['total_acceo']) - float(c['total_acceo']), 2)
        d_prix = int(base['prix_vente']) - int(c['prix_vente'])
        somme_acceo += d_acceo
        somme_prix += d_prix
        details.append({'decision': cle, 'run': decisions[cle], 'ref': ref_decisions[cle], 'delta_acceo': d_acceo, 'delta_prix': d_prix})
    toutes = dict(decisions)
    for cle in DECISIONS_CONNUES:
        if cle in ref_decisions:
            toutes[cle] = ref_decisions[cle]
    resultat: dict[str, Any] = {'mode': 'exact (contrefactuel par décision)', 'decisions': details, 'etiquetage': True,
                                'somme_deltas_acceo': round(somme_acceo, 2), 'somme_deltas_prix': somme_prix}
    try:
        c_ref = chiffrer(quantites, toutes, params, catalogue)
        ref_pv = arrondir_prix(float(ref['total_acceo']), params)
        resultat['run_avec_decisions_ref'] = {'total_acceo': c_ref['total_acceo'], 'prix_vente': c_ref['prix_vente']}
        resultat['interaction_acceo'] = round(float(base['total_acceo']) - float(c_ref['total_acceo']) - somme_acceo, 2)
        resultat['hors_decisions_acceo'] = round(float(c_ref['total_acceo']) - float(ref['total_acceo']), 2)
        resultat['hors_decisions_prix'] = int(c_ref['prix_vente']) - int(ref_pv)
    except ErreurChiffrage as e:
        resultat['run_avec_decisions_ref'] = {'erreur': str(e)}
    return resultat


def attribution_par_articles(arts: dict[str, dict[str, Any]], run_decisions: dict[str, Any] | None,
                             ref_decisions: dict[str, Any] | None) -> dict[str, Any]:
    """Ancien protocole : écart par groupe d'articles, étiqueté par décision quand decisions.json existe. Une décision
    identique entre run et référence ne reçoit rien (`identique: true`) : l'écart de ses articles va dans « autres »."""
    details: list[dict[str, Any]] = []
    couverts: set[str] = set()
    non_imputes = 0.0
    for cle, articles in ARTICLES_PAR_DECISION.items():
        delta = round(sum(float(arts[a]['delta_total']) for a in articles if a in arts), 2)
        couverts.update(articles)
        d: dict[str, Any] = {'decision': cle, 'articles': list(articles)}
        if run_decisions is not None:
            d['run'] = run_decisions.get(cle)
        if ref_decisions is not None:
            d['ref'] = ref_decisions.get(cle)
        identique = run_decisions is not None and ref_decisions is not None \
            and run_decisions.get(cle) is not None and run_decisions.get(cle) == ref_decisions.get(cle)
        d['identique'] = identique
        if identique:
            d['delta_acceo'] = 0.0
            d['delta_articles_non_impute'] = delta
            non_imputes += delta
        else:
            d['delta_acceo'] = delta
        details.append(d)
    reste = round(sum(float(v['delta_total']) for a, v in arts.items() if a not in couverts) + non_imputes, 2)
    return {'mode': 'approximation par articles (ancien protocole)', 'decisions': details, 'autres_articles_delta_acceo': reste}


def comparer(S: str, run: Path, kit: Path, racine: Path) -> dict[str, Any]:
    ref_dir = racine / 'dossiers' / S / 'soumission'
    ref = lire_json(ref_dir / 'chiffrage_dupuis.json')
    protocole = protocole_du_run(run, kit)
    out = chiffrage_du_run(run, kit, protocole)
    seuils = charger_seuils(kit)
    params = parametres_kit(kit, ref)
    ref_pv = arrondir_prix(float(ref['total_acceo']), params)
    run_pv = arrondir_prix(float(out.get('total_acceo', 0.0)), params)
    run_pv_declare = float(out.get('prix_vente', run_pv))
    taux_ref = float(ref['taux'])
    taux_run = float(out.get('taux', taux_ref))

    tot = {
        'materiel': ecart(float(ref['materiel']), float(out.get('materiel', 0.0))),
        'heures_relevees': ecart(float(ref['heures_relevees']), float(out.get('heures_relevees', 0.0))),
        'heures_chargees': ecart(float(ref['heures_chargees']), float(out.get('heures_chargees', 0.0))),
        'total_acceo': ecart(float(ref['total_acceo']), float(out.get('total_acceo', 0.0))),
        'prix_vente': ecart(ref_pv, run_pv),
    }
    ref_arts = cast(dict[str, dict[str, Any]], ref['par_article'])
    run_arts = cast(dict[str, dict[str, Any]], out.get('par_article', {}))
    arts: dict[str, dict[str, Any]] = {}
    for a in sorted(set(ref_arts) | set(run_arts)):
        r = ref_arts.get(a, {})
        o = run_arts.get(a, {})
        rt = total_article(r, taux_ref) if r else 0.0
        ot = total_article(o, taux_run) if o else 0.0
        delta = round(ot - rt, 2)
        tol = max(abs(rt) * seuils['article_pct'] / 100.0, seuils['article_min_abs'])
        arts[a] = {'ref_h': r.get('heures'), 'run_h': o.get('heures'), 'ref_mat': r.get('materiel'), 'run_mat': o.get('materiel'),
                   'ref_total': round(rt, 2), 'run_total': round(ot, 2), 'delta_total': delta, 'dans_seuil': abs(delta) <= tol}

    ref_lignes = cast(list[dict[str, Any]], ref['lignes'])
    run_lignes = cast(list[dict[str, Any]], out.get('lignes', []))
    ref_codes = {str(lg['code']): lg for lg in ref_lignes}
    run_codes = {str(lg.get('code')): lg for lg in run_lignes}
    communs = sorted(set(ref_codes) & set(run_codes))
    ecarts_lignes: list[dict[str, Any]] = []
    for c in communs:
        a, b = ref_codes[c], run_codes[c]
        if abs(float(a['q']) - float(b.get('q', 0))) > 1e-6 or abs(float(a['p']) - float(b.get('p', 0))) > 0.005 \
                or abs(float(a['h']) - float(b.get('h', 0))) > 1e-3:
            ecarts_lignes.append({'code': c, 'ref': {k: a[k] for k in ('q', 'p', 'h')}, 'run': {k: b.get(k) for k in ('q', 'p', 'h')},
                                  'src_run': b.get('src')})
    manquantes = sorted(set(ref_codes) - set(run_codes))
    en_plus = sorted(set(run_codes) - set(ref_codes))

    pct_prix = tot['prix_vente']['pct']
    pct_h = tot['heures_chargees']['pct']
    tol_h = max(float(ref['heures_chargees']) * seuils['heures_pct'] / 100.0, float(params.arrondi_heures))
    articles_hors = [a for a, v in arts.items() if not v['dans_seuil']]
    criteres: dict[str, Any] = {
        'total': {'pct': pct_prix, 'seuil_pct': seuils['total_pct'], 'ok': pct_prix is not None and abs(float(pct_prix)) <= seuils['total_pct']},
        'heures': {'pct': pct_h, 'seuil_pct': seuils['heures_pct'], 'tolerance_h': round(tol_h, 2),
                   'ok': abs(float(tot['heures_chargees']['delta'])) <= tol_h},
        'articles': {'hors_seuil': articles_hors, 'seuil_pct': seuils['article_pct'], 'seuil_min_abs': seuils['article_min_abs'],
                     'ok': not articles_hors},
        'dans_1_pct': pct_prix is not None and abs(float(pct_prix)) <= seuils['historique_pct'],
        'rappel_codes': round(len(communs) / len(ref_codes), 4) if ref_codes else None,
        'precision_codes': round(len(communs) / len(run_codes), 4) if run_codes else None,
    }
    verdict = 'OK' if criteres['total']['ok'] and criteres['heures']['ok'] and criteres['articles']['ok'] else 'ÉCART'

    ref_dec = lire_json(ref_dir / 'decisions.json') if (ref_dir / 'decisions.json').exists() else None
    run_dec = lire_json(run / 'decisions.json') if (run / 'decisions.json').exists() else None
    if protocole == 'nouveau' and ref_dec is not None:
        attribution = attribution_exacte(run, kit, ref, ref_dec, out)
    else:
        attribution = attribution_par_articles(arts, run_dec, ref_dec)

    rapport: dict[str, Any] = {
        'dossier': S, 'run': run.name, 'protocole': protocole, 'facteur': params.facteur, 'seuils': seuils,
        'totaux': tot, 'par_article': arts,
        'lignes': {'ref': len(ref_lignes), 'run': len(run_lignes), 'codes_communs': len(communs),
                   'manquantes': manquantes, 'en_plus': en_plus, 'ecarts': ecarts_lignes},
        'criteres': criteres, 'attribution': attribution, 'verdict': verdict,
    }
    if abs(run_pv_declare - run_pv) > 0.5:
        rapport['prix_vente_declare_run'] = run_pv_declare
        rapport['facteur_run'] = out.get('facteur')
    return rapport


def fmt_pct(v: Any) -> str:
    return f"{float(v):+.2f} %" if isinstance(v, (int, float)) else '—'


def rapport_markdown(rapport: dict[str, Any]) -> str:
    tot = cast(dict[str, dict[str, Any]], rapport['totaux'])
    arts = cast(dict[str, dict[str, Any]], rapport['par_article'])
    cr = cast(dict[str, Any], rapport['criteres'])
    lg = cast(dict[str, Any], rapport['lignes'])
    md = [f"# Rapport {rapport['dossier']} — {rapport['run']} : **{rapport['verdict']}** (protocole {rapport['protocole']})", "",
          "Δ = run − référence (négatif : le run est en dessous).", "",
          "| Total | Référence | Run | Δ | % |", "|---|---|---|---|---|"]
    for k, v in tot.items():
        md.append(f"| {k} | {v['ref']:,.2f} | {v['run']:,.2f} | {v['delta']:+,.2f} | {fmt_pct(v['pct'])} |".replace(',', ' '))
    if 'prix_vente_declare_run' in rapport:
        md.append(f"\nPrix déclaré par le run : {rapport['prix_vente_declare_run']:,.0f} $ (facteur du run {rapport.get('facteur_run')}) ; "
                  f"le tableau utilise le facteur du kit ({rapport['facteur']}).".replace(',', ' '))
    md += ["", "| Critère | Mesure | Seuil | OK |", "|---|---|---|---|",
           f"| prix de vente | {fmt_pct(cr['total']['pct'])} | ±{cr['total']['seuil_pct']} % | {'oui' if cr['total']['ok'] else 'non'} |",
           f"| heures chargées | {fmt_pct(cr['heures']['pct'])} | ±{cr['heures']['seuil_pct']} % (≥ {cr['heures']['tolerance_h']} h) | {'oui' if cr['heures']['ok'] else 'non'} |",
           f"| articles hors seuil | {', '.join(cr['articles']['hors_seuil']) or 'aucun'} | ±{cr['articles']['seuil_pct']} % ou "
           f"{cr['articles']['seuil_min_abs']:.0f} $ | {'oui' if cr['articles']['ok'] else 'non'} |",
           f"| dans ±1 % (historique) | {'oui' if cr['dans_1_pct'] else 'non'} | — | — |",
           f"| codes : rappel / précision | {cr['rappel_codes']} / {cr['precision_codes']} | — | — |", "",
           f"Lignes : réf {lg['ref']}, run {lg['run']}, communes {lg['codes_communs']}, écarts {len(lg['ecarts'])}, "
           f"manquantes {len(lg['manquantes'])}, en plus {len(lg['en_plus'])}", "",
           "| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |", "|---|---|---|---|---|---|---|"]
    for a, v in arts.items():
        md.append(f"| {a} | {v['ref_h']} | {v['run_h']} | {v['ref_mat']} | {v['run_mat']} | {v['delta_total']:+.2f} | {'oui' if v['dans_seuil'] else 'non'} |")
    att = cast(dict[str, Any], rapport['attribution'])
    md += ["", f"## Écart attribué aux décisions — {att['mode']}", "",
           "| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |", "|---|---|---|---|---|"]
    for d in cast(list[dict[str, Any]], att['decisions']):
        if d.get('identique'):
            colonne = f"identique, non imputé ({d.get('delta_articles_non_impute', 0.0):+.2f} $ sur {', '.join(cast(list[str], d.get('articles', [])))})"
        else:
            colonne = str(d.get('delta_prix', ', '.join(cast(list[str], d.get('articles', [])))))
        md.append(f"| {d['decision']} | {d.get('run', '—')} | {d.get('ref', '—')} | {d.get('delta_acceo', d.get('erreur', '—'))} | {colonne} |")
    if 'somme_deltas_acceo' in att:
        md.append(f"\nSomme des Δ par décision : {att['somme_deltas_acceo']:+.2f} $ ACCEO ({att['somme_deltas_prix']:+d} $ de prix) ; "
                  f"interaction (arrondis) : {att.get('interaction_acceo', 0.0):+.2f} $ ; "
                  f"hors décisions (relevé, prix, temps) : {att.get('hors_decisions_acceo', 0.0):+.2f} $ ACCEO "
                  f"({att.get('hors_decisions_prix', 0):+d} $ de prix) ; run avec toutes les décisions de la référence : {att.get('run_avec_decisions_ref')}")
    if 'autres_articles_delta_acceo' in att:
        md.append(f"\nAutres articles et décisions identiques (non attribués) : Δ ACCEO {att['autres_articles_delta_acceo']:+.2f} $")
    ecarts = cast(list[dict[str, Any]], lg['ecarts'])
    if ecarts:
        md += ["", "## Écarts par ligne (code commun)", "| code | réf q/p/h | run q/p/h | source run |", "|---|---|---|---|"]
        for e in ecarts[:60]:
            md.append(f"| {e['code']} | {e['ref']['q']}/{e['ref']['p']}/{e['ref']['h']} | {e['run']['q']}/{e['run']['p']}/{e['run']['h']} | "
                      f"{str(e['src_run'])[:60]} |")
    return '\n'.join(md)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Compare un run à la référence gelée et attribue l'écart aux décisions")
    ap.add_argument('S')
    ap.add_argument('run_dir', type=Path)
    ap.add_argument('--kit', type=Path, default=None, help='kit du dossier (défaut : entrainement/<S>/kit)')
    args = ap.parse_args(argv)
    racine = Path(__file__).resolve().parent.parent
    kit: Path = args.kit if args.kit is not None else racine / 'entrainement' / str(args.S) / 'kit'
    run: Path = args.run_dir
    try:
        rapport = comparer(str(args.S), run, kit, racine)
    except ErreurChiffrage as e:
        print(f"manquant ou invalide : {e}")
        return 2
    with (run / 'rapport.json').open('w', encoding='utf-8') as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1)
    md = rapport_markdown(rapport)
    (run / 'rapport.md').write_text(md, encoding='utf-8')
    print('\n'.join(md.split('\n')[:18]))
    return 0 if rapport['verdict'] == 'OK' else 1


if __name__ == '__main__':
    sys.exit(main())
