"""Tests de src/estimer/compare_bordereau.py : lecture des deux formes d'estimation
et comparaison à périmètre égal.

Ces deux défauts ont été trouvés en comparant pour de vrai le relevé kimi-k3 à
l'exemplaire HR26-14 : le comparateur ne savait pas lire la sortie du pont
`render/from_releve.py` et la notait 0 sans rien signaler, puis il comparait une
feuille relevée aux 26 feuilles de l'exemplaire.
"""
import csv
import json

import pytest

from src.estimer.compare_bordereau import (compare, feuilles_estimees, gold_family_counts,
                                           totaux_predits)


def _ecrire(path, entetes, lignes):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=entetes)
        w.writeheader()
        w.writerows(lignes)


@pytest.fixture
def exemplaire(tmp_path):
    """Trois bordereaux couvrant des feuilles disjointes, comme l'exemplaire réel."""
    _ecrire(tmp_path / "bordereau-materiel.csv",
            ["feuille", "materiel", "qte"],
            [{"feuille": "DSI01", "materiel": "DETECTEUR DE FUMEE", "qte": "10"},
             {"feuille": "DSI02", "materiel": "DETECTEUR DE FUMEE", "qte": "7"}])
    _ecrire(tmp_path / "bordereau-electrique-agrege.csv",
            ["feuille", "famille", "qte"],
            [{"feuille": "E01", "famille": "APPAREIL DE CHAUFFAGE ELECTRIQUE", "qte": "5"}])
    _ecrire(tmp_path / "bordereau-travaux-eu.csv",
            ["feuille", "famille", "lieux"],
            [{"feuille": "EU01", "famille": "BLOC ALIMENTATION EXISTANT A ENLEVER", "lieux": "3"}])
    return tmp_path


def test_lit_la_forme_totals():
    assert totaux_predits({"totals": {"securite_incendie": 4}})["securite_incendie"] == 4


def test_lit_la_forme_counters():
    """Sortie du pont relevé : une entrée par famille avec ses éléments.

    Sans cette lecture, un relevé valide était noté « predicted: 0 » : on aurait conclu
    que l'IA n'avait rien trouvé alors que c'est le comparateur qui ne savait pas lire."""
    est = {"counters": [{"family": "DETECTEUR FUMEE",
                         "elements": [{"sheet": "DSI01"}, {"sheet": "DSI01"}]},
                        {"family": "KLAXON", "elements": [{"sheet": "DSI01"}]}]}
    assert totaux_predits(est)["securite_incendie"] == 3


def test_refuse_une_estimation_illisible():
    """Une forme inconnue doit lever, jamais être notée 0 en silence."""
    with pytest.raises(ValueError, match="illisible"):
        totaux_predits({"quelque_chose": 1})


def test_feuilles_estimees_depuis_les_elements():
    est = {"sheets": [{"sheet": "DSI01"}],
           "counters": [{"family": "KLAXON", "elements": [{"sheet": "dsi02"}]}]}
    assert feuilles_estimees(est) == {"DSI01", "DSI02"}


def test_total_restreint_aux_feuilles_relevees(exemplaire):
    """À périmètre égal, l'écart mesure la justesse ; sinon il mesure le non-relevé."""
    tout, _ = gold_family_counts(exemplaire)
    une, _ = gold_family_counts(exemplaire, {"DSI01"})
    assert sum(tout.values()) == 25          # 10 + 7 + 5 + 3, les trois bordereaux
    assert sum(une.values()) == 10           # la seule feuille relevée


def test_detail_par_feuille_reste_complet(exemplaire):
    """La restriction ne doit pas masquer les feuilles non relevées : elles restent listées."""
    _, par_feuille = gold_family_counts(exemplaire, {"DSI01"})
    assert set(par_feuille) == {"DSI01", "DSI02", "E01", "EU01"}


def test_ecart_honnete_contre_ecart_trompeur(exemplaire):
    """Le même relevé donne -0 % à périmètre égal et -60 % contre tout l'exemplaire."""
    est = {"counters": [{"family": "DETECTEUR FUMEE",
                         "elements": [{"sheet": "DSI01"}] * 10}]}
    tout, _ = gold_family_counts(exemplaire)
    une, _ = gold_family_counts(exemplaire, {"DSI01"})
    assert compare(est, une)["total"]["count_error"] == 0.0
    assert compare(est, tout)["total"]["count_error"] == pytest.approx(-0.6)
