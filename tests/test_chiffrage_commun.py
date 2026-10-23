"""Moteur de chiffrage commun (entrainement/chiffrage_commun.py) : test doré sur la référence gelée S-1902,
contrefactuels par décision, erreurs d'entrée, conversion des runs de l'ancien protocole et comparateur v2.

Données réelles du dépôt (référence gelée, kit, runs commités) : ce sont des fichiers versionnés, pas des fixtures.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENTRAINEMENT = ROOT / 'entrainement'
KIT = ENTRAINEMENT / 'S-1902' / 'kit'
SOUMISSION = ROOT / 'dossiers' / 'S-1902' / 'soumission'
RUNS = ENTRAINEMENT / 'S-1902' / 'runs'


def charger(nom: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nom, ENTRAINEMENT / f'{nom}.py')
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module          # les dataclasses exigent un module enregistré
    spec.loader.exec_module(module)
    return module


moteur = charger('chiffrage_commun')
convertir_run = charger('convertir_run')
comparer = charger('comparer')


@pytest.fixture(scope='module')
def contexte() -> dict[str, Any]:
    return {
        'quantites': moteur.lire_json(SOUMISSION / 'quantites.json'),
        'decisions': moteur.lire_json(SOUMISSION / 'decisions.json'),
        'params': moteur.Parametres.depuis(moteur.lire_json(KIT / 'parametres.json')),
        'catalogue': moteur.charger_catalogue(KIT / 'catalogue-prix-temps-dupuis.csv'),
        'reference': json.loads((SOUMISSION / 'chiffrage_dupuis.json').read_text(encoding='utf-8')),
    }


def test_moteur_reproduit_la_reference_gelee(contexte: dict[str, Any]) -> None:
    """Test doré : quantites + decisions + paramètres → exactement le chiffrage_dupuis.json gelé (194 000 $)."""
    c = moteur.chiffrer(contexte['quantites'], contexte['decisions'], contexte['params'], contexte['catalogue'])
    ref = contexte['reference']
    for cle in ('taux', 'materiel', 'heures_relevees', 'heures_chargees', 'main_doeuvre', 'total_acceo'):
        assert c[cle] == ref[cle], cle
    assert c['prix_vente'] == 194000
    assert c['facteur'] == 1.244
    assert [lg['code'] for lg in c['lignes']] == [lg['code'] for lg in ref['lignes']]
    for a, b in zip(c['lignes'], ref['lignes'], strict=True):
        for cle in ('q', 'p', 'h', 'art', 'u', 'desc'):
            assert a[cle] == b[cle], (a['code'], cle)
    assert c['par_article'] == ref['par_article']
    assert c['lots'] == {'F-LOT': 13034.8, 'B-LOT': 6200.0, 'G-01b': 600.0, 'G-07': 7400.0}


def test_quantites_tracables_au_catalogue(contexte: dict[str, Any]) -> None:
    """Les lignes « catalogue » redonnent le prix de la référence depuis les colonnes « À UTILISER » (dernier Dupuis)."""
    lignes = contexte['quantites']['lignes']
    au_catalogue = [lg for lg in lignes if lg.get('prix', {}).get('type') == 'catalogue']
    assert len(au_catalogue) >= 40
    ref = {lg['code']: lg for lg in contexte['reference']['lignes']}
    for lg in au_catalogue:
        p, h = moteur.resoudre_prix(lg['prix'], contexte['catalogue'], lg['code'])
        assert abs(p - ref[lg['code']]['p']) < 1e-9 and abs(h - ref[lg['code']]['h']) < 1e-9, lg['code']


@pytest.mark.parametrize('cle, valeur, delta_acceo, delta_heures', [
    ('monuments', 'dupuis', -2 * (1461.22 - 250.0), 0.0),                       # E-02 ×2 au prix Dupuis
    ('lot_eclairage', 'readme_11893', -(13034.80 - 11893.0), 0.0),              # lot éclairage du README
    ('eae_hors_plan', 'sautes', -5100.0, -64.9),                                # A-01…A-06 : 64,9 h → arrondi 1 050 → 990 h
])
def test_contrefactuels_par_decision(contexte: dict[str, Any], cle: str, valeur: str, delta_acceo: float, delta_heures: float) -> None:
    base = moteur.chiffrer(contexte['quantites'], contexte['decisions'], contexte['params'], contexte['catalogue'])
    autre = dict(contexte['decisions'])
    autre[cle] = valeur
    c = moteur.chiffrer(contexte['quantites'], autre, contexte['params'], contexte['catalogue'])
    assert abs((c['total_acceo'] - base['total_acceo']) - delta_acceo) < 0.01
    assert abs((c['heures_relevees'] - base['heures_relevees']) - delta_heures) < 0.01


def test_postes_composites_couverts_retire_les_lignes_du_detail(contexte: dict[str, Any]) -> None:
    autre = dict(contexte['decisions'])
    autre['postes_composites'] = 'couverts'
    c = moteur.chiffrer(contexte['quantites'], autre, contexte['params'], contexte['catalogue'])
    codes = {lg['code'] for lg in c['lignes']}
    assert not codes & {'D-01', 'D-02', 'D-03', 'D-04', 'D-05', 'D-06', 'E-01', 'E-04', 'E-05'}
    assert c['total_acceo'] < contexte['reference']['total_acceo']


def test_deterministe(contexte: dict[str, Any]) -> None:
    a = moteur.chiffrer(contexte['quantites'], contexte['decisions'], contexte['params'], contexte['catalogue'])
    b = moteur.chiffrer(contexte['quantites'], contexte['decisions'], contexte['params'], contexte['catalogue'])
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


@pytest.mark.parametrize('lignes, decisions, message', [
    ([{'code': 'X', 'q': 1, 'art': '3.22', 'prix': {'type': 'catalogue', 'entrees': [{'desc': 'ENTREE INEXISTANTE'}]}}], {}, 'absent du catalogue'),
    ([{'code': 'X', 'q': 1, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1}},
      {'code': 'X', 'q': 1, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1}}], {}, 'code en double'),
    ([{'code': 'X', 'q': 1, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1},
      'decision': {'cle': 'monuments', 'actif_si': ['lumen']}}], {}, "n'est pas dans decisions.json"),
    ([{'code': 'X', 'q': 1, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1}}], {'monuments': 'or'}, 'valeurs connues'),
    ([{'code': 'X', 'q': -1, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1}}], {}, '≥ 0'),
    ([{'code': 'X', 'q': 1, 'prix': {'type': 'fixe', 'p': 1, 'h': 1}}], {}, 'article du bordereau manquant'),
])
def test_entrees_invalides_refusees(contexte: dict[str, Any], lignes: list[dict[str, Any]], decisions: dict[str, Any], message: str) -> None:
    with pytest.raises(moteur.ErreurChiffrage, match=message):
        moteur.chiffrer({'dossier': 'T', 'lignes': lignes}, decisions, contexte['params'], contexte['catalogue'])


def test_arrondis_dupuis() -> None:
    """Heures chargées arrondies vers le haut au multiple de 10 ; prix de vente arrondi au millier."""
    params = moteur.Parametres(taux=85.0, facteur=1.244)
    catalogue: dict[str, Any] = {}
    q = {'dossier': 'T', 'lignes': [{'code': 'A', 'q': 3, 'art': '3.22', 'prix': {'type': 'fixe', 'p': 100.0, 'h': 3.7}}]}
    c = moteur.chiffrer(q, {}, params, catalogue)
    assert c['heures_relevees'] == 11.1 and c['heures_chargees'] == 20
    assert c['main_doeuvre'] == 1700.0 and c['materiel'] == 300.0 and c['total_acceo'] == 2000.0
    assert c['prix_vente'] == round(2000.0 * 1.244 / 1000) * 1000


@pytest.mark.parametrize('run', sorted(p.name for p in RUNS.iterdir() if (p / 'chiffrage.json').exists()))
def test_moteur_reproduit_les_runs_de_l_ancien_protocole(run: str) -> None:
    """Les 10 runs commités, convertis en quantites.json à prix fixes, redonnent leurs propres totaux par le moteur."""
    rechiffre, ecarts = convertir_run.convertir(RUNS / run, KIT, {}, ecrire=False)
    assert ecarts == [], ecarts
    assert rechiffre['prix_vente'] == json.loads((RUNS / run / 'chiffrage.json').read_text(encoding='utf-8'))['prix_vente']


def test_comparateur_sur_la_reference_elle_meme(tmp_path: Path) -> None:
    """Nouveau protocole : la référence comparée à elle-même est OK, écart nul, attribution exacte vide."""
    run = tmp_path / 'ref-copie'
    run.mkdir()
    shutil.copy(SOUMISSION / 'quantites.json', run / 'quantites.json')
    shutil.copy(SOUMISSION / 'decisions.json', run / 'decisions.json')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    assert rapport['verdict'] == 'OK' and rapport['protocole'] == 'nouveau'
    assert rapport['totaux']['prix_vente']['delta'] == 0.0
    assert rapport['criteres']['dans_1_pct'] and rapport['criteres']['rappel_codes'] == 1.0
    assert rapport['attribution']['decisions'] == []
    assert (run / 'chiffrage.json').exists()


def test_comparateur_attribue_une_decision_par_contrefactuel(tmp_path: Path) -> None:
    """Même quantités, monuments au prix Dupuis : l'écart est attribué en entier à la décision « monuments »."""
    run = tmp_path / 'monuments-dupuis'
    run.mkdir()
    shutil.copy(SOUMISSION / 'quantites.json', run / 'quantites.json')
    decisions = moteur.lire_json(SOUMISSION / 'decisions.json')
    decisions['monuments'] = 'dupuis'
    moteur.ecrire_json(decisions, run / 'decisions.json')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    att = rapport['attribution']
    assert [d['decision'] for d in att['decisions']] == ['monuments']
    assert abs(att['decisions'][0]['delta_acceo'] - 2 * (1461.22 - 250.0)) < 0.01
    assert att['run_avec_decisions_ref']['prix_vente'] == 194000
    assert rapport['par_article']['3.34']['dans_seuil'] is False       # −2 422 $ sur 3 764 $ : hors ±10 %
    assert rapport['verdict'] == 'ÉCART'                               # un total à −1,5 % mais un article faux


def test_comparateur_ancien_protocole_sur_un_run_commite() -> None:
    """Un run de l'ancien protocole garde le schéma historique de rapport.json et reçoit l'attribution par articles."""
    rapport = comparer.comparer('S-1902', RUNS / 'sonnet-2', KIT, ROOT)
    assert rapport['protocole'] == 'ancien' and rapport['verdict'] == 'ÉCART'
    assert rapport['totaux']['prix_vente']['run'] == 175000 and rapport['totaux']['prix_vente']['ref'] == 194000
    assert set(rapport['lignes']) >= {'ref', 'run', 'codes_communs', 'manquantes', 'en_plus', 'ecarts'}
    assert rapport['attribution']['mode'].startswith('approximation')
    assert {d['decision'] for d in rapport['attribution']['decisions']} == set(moteur.DECISIONS_CONNUES)
