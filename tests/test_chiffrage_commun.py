"""Moteur de chiffrage commun (entrainement/chiffrage_commun.py) : test doré sur la référence gelée S-1902,
contrefactuels par décision, validation des entrées, conversion des runs de l'ancien protocole et comparateur v2.

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
    if sys.path and sys.path[0] == str(ENTRAINEMENT):   # comparer.py s'ajoute en tête de sys.path : ne pas le laisser à la session pytest
        sys.path.pop(0)
    return module


moteur = charger('chiffrage_commun')
convertir_run = charger('convertir_run')
comparer = charger('comparer')

PARAMS_SIMPLES = moteur.Parametres(taux=85.0, facteur=1.244)
CATALOGUE_VIDE: dict[str, Any] = {}


def ligne(code: str, q: float = 1, p: float = 100.0, h: float = 1.0, **extra: Any) -> dict[str, Any]:
    d: dict[str, Any] = {'code': code, 'q': q, 'art': '3.22', 'prix': {'type': 'fixe', 'p': p, 'h': h}}
    d.update(extra)
    return d


@pytest.fixture(scope='module')
def contexte() -> dict[str, Any]:
    return {
        'quantites': moteur.lire_json(SOUMISSION / 'quantites.json'),
        'decisions': moteur.lire_json(SOUMISSION / 'decisions.json'),
        'params': moteur.Parametres.depuis(moteur.lire_json(KIT / 'parametres.json')),
        'catalogue': moteur.charger_catalogue(KIT / 'catalogue-prix-temps-dupuis.csv'),
        'reference': json.loads((SOUMISSION / 'chiffrage_dupuis.json').read_text(encoding='utf-8')),
    }


# ---------------------------------------------------------------- test doré

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
    assert c['decisions'] == {k: v for k, v in contexte['decisions'].items() if k != 'justifications'}
    assert c['dossier'] == 'S-1902'
    assert set(c) >= set(moteur.CLES_CHIFFRAGE)


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


# ---------------------------------------------------------------- mécanique du moteur (catalogue vide, lignes synthétiques)

def test_arrondis_dupuis() -> None:
    """Heures chargées arrondies vers le haut au multiple de 10 ; prix de vente arrondi au millier."""
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [ligne('A', q=3, p=100.0, h=3.7)]}, {}, PARAMS_SIMPLES, CATALOGUE_VIDE)
    assert c['heures_relevees'] == 11.1 and c['heures_chargees'] == 20
    assert c['main_doeuvre'] == 1700.0 and c['materiel'] == 300.0 and c['total_acceo'] == 2000.0
    assert c['prix_vente'] == round(2000.0 * 1.244 / 1000) * 1000


def test_heures_chargees_ne_bascule_pas_sur_le_bruit_flottant() -> None:
    """200 × 0,55 h = 110,000…01 en flottant : 110 h chargées, jamais 120."""
    assert moteur.heures_chargees(200 * 0.55, 10) == 110
    assert moteur.heures_chargees(23 * 0.1 + 39 * 0.1 + 38 * 0.1, 10) == 10
    assert moteur.heures_chargees(110.0004, 10) == 110       # sous la 3e décimale : encore 110
    assert moteur.heures_chargees(110.001, 10) == 120
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [ligne('A', q=200, p=0.0, h=0.55)]}, {}, PARAMS_SIMPLES, CATALOGUE_VIDE)
    assert c['heures_chargees'] == 110 and c['main_doeuvre'] == 9350.0


def test_arrondis_a_zero_desactivent_les_arrondis() -> None:
    params = moteur.Parametres(taux=85.0, facteur=1.0, arrondi_heures=0, arrondi_prix=0)
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [ligne('A', q=3, p=100.0, h=3.7)]}, {}, params, CATALOGUE_VIDE)
    assert c['heures_chargees'] == 11.1 and c['main_doeuvre'] == 943.5 and c['prix_vente'] == 1243.5


def test_variante_q_surcharge_la_quantite_et_garde_le_prix() -> None:
    lg = ligne('A', q=10, p=100.0, h=1.0, variantes={'cle': 'postes_composites', 'options': {'en_plus': {'q': 3}, 'couverts': {}}})
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [lg]}, {'postes_composites': 'en_plus'}, PARAMS_SIMPLES, CATALOGUE_VIDE)
    assert c['lignes'][0]['q'] == 3 and c['lignes'][0]['p'] == 100.0
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [lg]}, {'postes_composites': 'couverts'}, PARAMS_SIMPLES, CATALOGUE_VIDE)
    assert c['lignes'][0]['q'] == 10


def test_variante_prix_gagne_sur_le_prix_de_la_ligne() -> None:
    lg = ligne('A', q=1, p=100.0, h=1.0, variantes={'cle': 'monuments', 'options': {
        'lumen': {'prix': {'type': 'fixe', 'p': 1461.22, 'h': 1.0}}, 'dupuis': {}}})
    assert moteur.chiffrer({'dossier': 'T', 'lignes': [lg]}, {'monuments': 'lumen'}, PARAMS_SIMPLES, CATALOGUE_VIDE)['lignes'][0]['p'] == 1461.22
    assert moteur.chiffrer({'dossier': 'T', 'lignes': [lg]}, {'monuments': 'dupuis'}, PARAMS_SIMPLES, CATALOGUE_VIDE)['lignes'][0]['p'] == 100.0


def test_variante_absente_retombe_sur_le_prix_de_la_ligne() -> None:
    """Option retenue hors de `variantes.options` : la ligne garde son prix et son q ; sans prix, erreur."""
    lg = ligne('A', q=2, p=100.0, h=1.0, variantes={'cle': 'monuments', 'options': {'dupuis': {'prix': {'type': 'fixe', 'p': 250.0, 'h': 1.0}}}})
    c = moteur.chiffrer({'dossier': 'T', 'lignes': [lg]}, {'monuments': 'lumen'}, PARAMS_SIMPLES, CATALOGUE_VIDE)
    assert c['lignes'][0]['p'] == 100.0 and c['lignes'][0]['q'] == 2
    sans_prix = {k: v for k, v in lg.items() if k != 'prix'}
    with pytest.raises(moteur.ErreurChiffrage, match='pas de prix de repli'):
        moteur.chiffrer({'dossier': 'T', 'lignes': [sans_prix]}, {'monuments': 'lumen'}, PARAMS_SIMPLES, CATALOGUE_VIDE)


def test_acceo_tempsec_refuse_sans_colonne_tempsec() -> None:
    with pytest.raises(moteur.ErreurChiffrage, match='TEMPSEC'):
        moteur.chiffrer({'dossier': 'T', 'lignes': [ligne('A')]}, {'conduits': 'acceo_tempsec'}, PARAMS_SIMPLES, CATALOGUE_VIDE)


def test_decision_et_variantes_se_combinent() -> None:
    lg = ligne('A', q=1, p=100.0, h=1.0, decision={'cle': 'eae_hors_plan', 'actif_si': ['comptes', 'releve']},
               variantes={'cle': 'eae_hors_plan', 'options': {'comptes': {'q': 5}, 'releve': {'q': 2}, 'sautes': {}}})
    q = {'dossier': 'T', 'lignes': [lg]}
    assert moteur.chiffrer(q, {'eae_hors_plan': 'comptes'}, PARAMS_SIMPLES, CATALOGUE_VIDE)['lignes'][0]['q'] == 5
    assert moteur.chiffrer(q, {'eae_hors_plan': 'releve'}, PARAMS_SIMPLES, CATALOGUE_VIDE)['lignes'][0]['q'] == 2
    assert moteur.chiffrer(q, {'eae_hors_plan': 'sautes'}, PARAMS_SIMPLES, CATALOGUE_VIDE)['lignes'] == []


def test_catalogue_doublons_derniere_valeur_et_unites(tmp_path: Path) -> None:
    """Même description deux fois : même unité → la plus récente gagne ; unités différentes → « um » obligatoire."""
    csv = tmp_path / 'cat.csv'
    csv.write_text('description;um;prix_a_utiliser;temps_a_utiliser;date_dernier\n'
                   'FIL X;P;0.90;0.007;2026-08-19\nFIL X ;P;1.06;0.007;2026-09-10\n'
                   'FLEX Y;P;4.23;0.05;2026-01-01\nFLEX Y;M;13.88;0.16;2026-01-01\n', encoding='utf-8')
    journal: list[str] = []
    cat = moteur.charger_catalogue(csv, journal)
    assert journal and 'FIL X' in journal[0]
    assert moteur.resoudre_prix({'type': 'catalogue', 'entrees': [{'desc': 'fil x'}]}, cat, 'T') == (1.06, 0.007)
    with pytest.raises(moteur.ErreurChiffrage, match='plusieurs unités'):
        moteur.resoudre_prix({'type': 'catalogue', 'entrees': [{'desc': 'FLEX Y'}]}, cat, 'T')
    assert moteur.resoudre_prix({'type': 'catalogue', 'entrees': [{'desc': 'FLEX Y', 'um': 'M'}]}, cat, 'T') == (13.88, 0.16)


@pytest.mark.parametrize('lignes, decisions, message', [
    ([ligne('X', prix={'type': 'catalogue', 'entrees': [{'desc': 'ENTREE INEXISTANTE'}]})], {}, 'absent du catalogue'),
    ([ligne('X'), ligne('X')], {}, 'code en double'),
    ([ligne('X', decision={'cle': 'monuments', 'actif_si': ['lumen']})], {}, "n'est pas dans decisions.json"),
    ([ligne('X')], {'monuments': 'or'}, 'valeurs connues'),
    ([ligne('X')], {'monument': 'lumen'}, 'clé inconnue'),
    ([ligne('X', decision={'cle': 'monument', 'actif_si': ['lumen']})], {'monuments': 'lumen'}, 'décision inconnue'),
    ([ligne('X', decision={'cle': 'lot_eclairage', 'actif_si': ['detail']})], {'lot_eclairage': 'detail_13034_80'}, 'valeurs inconnues'),
    ([ligne('X', variantes={'cle': 'monuments', 'options': {'lumen': {}, 'dupuy': {}}})], {'monuments': 'lumen'}, 'valeurs inconnues'),
    ([ligne('X', decision={'cle': 'monuments', 'actif_si': ['dupuis']}, variantes={'cle': 'conduits', 'options': {'bidon': {}}})],
     {'monuments': 'lumen', 'conduits': 'temps_pi'}, 'valeurs inconnues'),      # ligne inactive, étiquette quand même validée
    ([ligne('X', q=-1)], {}, '≥ 0'),
    ([{'code': 'X', 'q': 1, 'prix': {'type': 'fixe', 'p': 1, 'h': 1}}], {}, 'article du bordereau manquant'),
    ([{'code': 'X', 'art': '3.22', 'prix': {'type': 'fixe', 'p': 1, 'h': 1}, 'variantes': {'cle': 'monuments', 'options': {'lumen': {'q': 3}}}}],
     {'monuments': 'lumen'}, 'q : nombre attendu'),                                # q de la ligne obligatoire même surchargé
    ([ligne('X', lot='non')], {}, 'lot doit être un booléen'),
    ([ligne('X', desc=12)], {}, 'chaîne attendue'),
])
def test_entrees_invalides_refusees(lignes: list[dict[str, Any]], decisions: dict[str, Any], message: str) -> None:
    with pytest.raises(moteur.ErreurChiffrage, match=message):
        moteur.chiffrer({'dossier': 'T', 'lignes': lignes}, decisions, PARAMS_SIMPLES, CATALOGUE_VIDE)


def test_nan_et_infinity_refuses(tmp_path: Path) -> None:
    (tmp_path / 'q.json').write_text('{"dossier": "T", "lignes": [{"code": "X", "q": NaN, "art": "3.22", "prix": {"type": "fixe", "p": 1, "h": 1}}]}', encoding='utf-8')
    with pytest.raises(moteur.ErreurChiffrage, match='NaN'):
        moteur.lire_json(tmp_path / 'q.json')
    with pytest.raises(moteur.ErreurChiffrage, match='fini'):
        moteur._nombre(float('inf'), 'T')


@pytest.mark.parametrize('params, message', [
    ({'taux': '85', 'facteur': 1.244}, 'nombre attendu'),
    ({'taux': 85, 'facteur': True}, 'nombre attendu'),
    ({'taux': 85, 'facteur': 1.244, 'arrondi_heures': 10.9}, 'entier'),
    ({'taux': 85, 'facteur': 1.244, 'arrondi_prix': -1000}, 'entier'),
    ({'taux': 0, 'facteur': 1.244}, '> 0'),
    ({'facteur': 1.244}, 'obligatoires'),
])
def test_parametres_stricts(params: dict[str, Any], message: str) -> None:
    with pytest.raises(moteur.ErreurChiffrage, match=message):
        moteur.Parametres.depuis(params)


# ---------------------------------------------------------------- runs de l'ancien protocole

@pytest.mark.parametrize('run', sorted(p.name for p in RUNS.iterdir() if (p / 'chiffrage.json').exists()))
def test_moteur_reproduit_les_runs_de_l_ancien_protocole(run: str) -> None:
    """Les 10 runs commités, convertis en quantites.json à prix fixes, redonnent leurs propres totaux par le moteur."""
    rechiffre, ecarts = convertir_run.convertir(RUNS / run, KIT, {}, ecrire=False)
    assert ecarts == [], ecarts
    assert rechiffre['prix_vente'] == json.loads((RUNS / run / 'chiffrage.json').read_text(encoding='utf-8'))['prix_vente']


# ---------------------------------------------------------------- comparateur v2

def copie_reference(dossier: Path) -> Path:
    dossier.mkdir()
    shutil.copy(SOUMISSION / 'quantites.json', dossier / 'quantites.json')
    shutil.copy(SOUMISSION / 'decisions.json', dossier / 'decisions.json')
    return dossier


def test_comparateur_sur_la_reference_elle_meme(tmp_path: Path) -> None:
    """Nouveau protocole : la référence comparée à elle-même est OK, écart nul, attribution exacte vide."""
    run = copie_reference(tmp_path / 'ref-copie')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    assert rapport['verdict'] == 'OK' and rapport['protocole'] == 'nouveau'
    assert rapport['totaux']['prix_vente']['delta'] == 0.0
    assert rapport['criteres']['dans_1_pct'] and rapport['criteres']['rappel_codes'] == 1.0
    att = rapport['attribution']
    assert att['decisions'] == [] and att['etiquetage'] is True and att['hors_decisions_acceo'] == 0.0
    assert (run / 'chiffrage.json').exists()


def test_comparateur_attribue_une_decision_par_contrefactuel(tmp_path: Path) -> None:
    """Même quantités, monuments au prix Dupuis : Δ = run − référence, attribué en entier à « monuments », résidu nul."""
    run = copie_reference(tmp_path / 'monuments-dupuis')
    decisions = moteur.lire_json(run / 'decisions.json')
    decisions['monuments'] = 'dupuis'
    moteur.ecrire_json(decisions, run / 'decisions.json')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    att = rapport['attribution']
    assert [d['decision'] for d in att['decisions']] == ['monuments']
    assert abs(att['decisions'][0]['delta_acceo'] + 2 * (1461.22 - 250.0)) < 0.01      # négatif : le run est en dessous
    assert att['decisions'][0]['delta_prix'] == -3000
    assert att['somme_deltas_acceo'] == att['decisions'][0]['delta_acceo']
    assert att['interaction_acceo'] == 0.0 and att['hors_decisions_acceo'] == 0.0 and att['hors_decisions_prix'] == 0
    assert att['run_avec_decisions_ref']['prix_vente'] == 194000
    assert rapport['totaux']['total_acceo']['delta'] == att['decisions'][0]['delta_acceo']   # même signe que les totaux
    assert rapport['par_article']['3.34']['dans_seuil'] is False       # −2 422 $ sur 3 764 $ : hors ±10 %
    assert rapport['verdict'] == 'ÉCART'                               # un total à −1,5 % mais un article faux


def test_comparateur_reecrit_chiffrage_json_a_chaque_comparaison(tmp_path: Path) -> None:
    run = copie_reference(tmp_path / 'rafraichi')
    decisions = moteur.lire_json(run / 'decisions.json')
    decisions['monuments'] = 'dupuis'
    moteur.ecrire_json(decisions, run / 'decisions.json')
    comparer.comparer('S-1902', run, KIT, ROOT)
    assert json.loads((run / 'chiffrage.json').read_text(encoding='utf-8'))['prix_vente'] == 191000
    decisions['monuments'] = 'lumen'
    moteur.ecrire_json(decisions, run / 'decisions.json')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    assert rapport['verdict'] == 'OK'
    assert json.loads((run / 'chiffrage.json').read_text(encoding='utf-8'))['prix_vente'] == 194000


def test_comparateur_v2_sans_etiquette_est_chiffre_mais_non_attribuable(tmp_path: Path) -> None:
    run = copie_reference(tmp_path / 'sans-etiquette')
    q = moteur.lire_json(run / 'quantites.json')
    for lg in q['lignes']:
        if 'variantes' in lg:                       # on fige la variante retenue comme prix fixe
            lg['prix'] = {'type': 'fixe', 'p': {'E-02': 1461.22, 'F-LOT': 13034.80}[lg['code']], 'h': 1.0 if lg['code'] == 'E-02' else 0.0}
        lg.pop('decision', None)
        lg.pop('variantes', None)
    moteur.ecrire_json(q, run / 'quantites.json')
    rapport = comparer.comparer('S-1902', run, KIT, ROOT)
    assert rapport['protocole'] == 'nouveau' and rapport['verdict'] == 'OK'
    assert rapport['attribution']['etiquetage'] is False and rapport['attribution']['decisions'] == []


def test_comparateur_ancien_protocole_sur_un_run_commite() -> None:
    """Un run v1 (converti) garde le schéma historique de rapport.json et reçoit l'attribution par articles ;
    une décision identique à la référence (conduits) n'est pas imputée."""
    rapport = comparer.comparer('S-1902', RUNS / 'sonnet-2', KIT, ROOT)
    assert rapport['protocole'] == 'ancien' and rapport['verdict'] == 'ÉCART'
    assert rapport['totaux']['prix_vente']['run'] == 175000 and rapport['totaux']['prix_vente']['ref'] == 194000
    assert set(rapport['lignes']) >= {'ref', 'run', 'codes_communs', 'manquantes', 'en_plus', 'ecarts'}
    att = rapport['attribution']
    assert att['mode'].startswith('approximation')
    par_cle = {d['decision']: d for d in att['decisions']}
    assert set(par_cle) == set(moteur.DECISIONS_CONNUES)
    assert par_cle['conduits']['identique'] is True and par_cle['conduits']['delta_acceo'] == 0.0
    assert par_cle['monuments']['identique'] is False and par_cle['monuments']['delta_acceo'] < 0


def test_critere_heures_tolere_un_pas_d_arrondi(tmp_path: Path) -> None:
    """Petit dossier : +0,5 h relevée fait +10 h chargées ; le critère heures ne doit pas échouer pour un pas d'arrondi."""
    racine = tmp_path / 'racine'
    soum = racine / 'dossiers' / 'T' / 'soumission'
    soum.mkdir(parents=True)
    kit = racine / 'kit'
    kit.mkdir()
    shutil.copy(KIT / 'parametres.json', kit / 'parametres.json')
    shutil.copy(KIT / 'catalogue-prix-temps-dupuis.csv', kit / 'catalogue-prix-temps-dupuis.csv')
    params = moteur.Parametres.depuis(moteur.lire_json(kit / 'parametres.json'))
    ref = moteur.chiffrer({'dossier': 'T', 'lignes': [ligne('A', q=100, p=10.0, h=1.0)]}, {}, params, CATALOGUE_VIDE)
    moteur.ecrire_json(ref, soum / 'chiffrage_dupuis.json')
    run = tmp_path / 'run'
    run.mkdir()
    moteur.ecrire_json({'dossier': 'T', 'lignes': [ligne('A', q=100, p=10.0, h=1.005)]}, run / 'quantites.json')
    moteur.ecrire_json({}, run / 'decisions.json')
    rapport = comparer.comparer('T', run, kit, racine)
    assert rapport['totaux']['heures_chargees']['delta'] == 10.0
    assert rapport['criteres']['heures']['ok'] is True and rapport['criteres']['heures']['tolerance_h'] == 10.0
    assert rapport['criteres']['total']['ok'] is False      # sur 9 500 $, le pas de 10 h vaut +8,9 % : c'est le prix qui tranche, pas les heures
