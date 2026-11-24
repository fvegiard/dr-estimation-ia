"""Multiplicateurs, portées et poste chiffrable : aucun zéro d'absence."""
from __future__ import annotations

import json

import pytest

from src.releve import chiffrage, quantites


def travail(tmp_path, note="Plan du RDC"):
    w = tmp_path / "travail"
    w.mkdir()
    for nom, texte in {
        "feuilles.csv": "feuille,fichier,page,titre\nE200,plans.pdf,2,Plan\n",
        "feuilles-classement.csv": f"feuille,type,note\nE200,plan,{note}\n",
        "nomenclature.csv": "label,portee\nPRISE,INSTALLER\nPROJECTEUR,INSTALLER\n",
        "occurrences-visuel.csv": "feuille,label,x_pt,y_pt,portee,qte,source_qte\n"
                                  "E200,PRISE,10,10,INSTALLER,2,note 3 (deux prises)\n"
                                  "E200,PRISE,20,20,CONSERVER,,\n"
                                  "E200,PROJECTEUR,90,80,INSTALLER,,\n",
        "occurrences-texte.csv": "feuille,label,x_pt,y_pt,portee,qte,source_qte\n"
                                 "E200,PRISE,10,10,INSTALLER,2,note 3 (deux prises)\n",
    }.items():
        (w / nom).write_text(texte, encoding="utf-8")
    return w


def test_zones_source_postes_et_reperes(tmp_path):
    w = travail(tmp_path, "CHAMBRE TYPE")
    (w / "multiplicateurs.csv").write_text("feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source\n"
        "E200,6,,,,,cédules E200\nE200,3,1,1,30,30,étages sur E200\n", encoding="utf-8")
    rs = quantites.calculer(w)
    assert not rs["reserves"]
    valeurs = {(r["label"], r["portee"]): (r["represente"], r["quantite"]) for r in rs["lignes"]}
    assert valeurs == {("PRISE", "INSTALLER"): (1, 6), ("PRISE", "CONSERVER"): (1, 3), ("PROJECTEUR", "INSTALLER"): (1, 6)}
    pose = next(r for r in rs["lignes"] if r["label"] == "PRISE" and r["portee"] == "INSTALLER")
    assert "note 3" in pose["source"][0] and "×3" in pose["source"][0]


def test_pas_de_facteur_par_defaut_si_unite_type(tmp_path):
    rs = quantites.calculer(travail(tmp_path, "CHAMBRES TYPES"))
    assert rs["reserves"] and all(r["quantite"] is None for r in rs["lignes"])


@pytest.mark.parametrize("ligne", ["2,1,,,,note", "nan,,,,,note", "0,,,,,note", "2,,,,,", "1.2,,,,,note"])
def test_facteurs_invalides_refuses(tmp_path, ligne):
    w = travail(tmp_path)
    (w / "multiplicateurs.csv").write_text("feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source\nE200," + ligne, encoding="utf-8")
    with pytest.raises(ValueError, match=r"multiplicateurs\.csv:2"):
        quantites.calculer(w)


def test_prix_et_heures_uniquement_pour_poste_sourcable(tmp_path):
    w = travail(tmp_path)
    catalogue = tmp_path / "catalogue.csv"
    catalogue.write_text("description;um;prix_a_utiliser;temps_a_utiliser;date_dernier;projet_dernier\n"
        "PRISE;U;30.01;1.25;2026-11-02;historique\nPROJECTEUR;U;220;0;2026-11-03;historique\n"
        "EMT;P;4;0.2;2026-11-01;historique\n", encoding="utf-8")
    correspondances = tmp_path / "articles.csv"
    correspondances.write_text("label,portee,unite,description,um,source_equivalence\n"
        "PRISE,INSTALLER,u,PRISE,U,preuve 1\nPROJECTEUR,INSTALLER,u,PROJECTEUR,U,preuve 2\n"
        "EMT,INSTALLER,m,EMT,P,preuve 3\n", encoding="utf-8")
    longueur = {"feuille": "E200", "famille": "EMT", "portee": "INSTALLER", "longueur_m": "3.048", "source": "p.2"}
    p = w / "metre-longueurs.json"
    p.write_text(json.dumps({"complet": False, "lignes": [longueur]}), encoding="utf-8")
    q = quantites.calculer(w)
    r = chiffrage.calculer(w, q, catalogue, correspondances)
    assert r["prix_forfaitaire"] is None and not r["complet"] and not r["rendu_client_autorise"]
    assert r["couverture_postes"]["Non chiffrable"] == 2
    l = next(p for p in r["postes"] if p["portee"] == "INSTALLER" and p["label"] == "PRISE")
    assert (l["materiel_cad"], l["heures"]) == ("60.02", "2.5000")
    assert "catalogue.csv:2" in l["source_catalogue"]
    non_chiffres = [p for p in r["postes"] if p["statut"] == "Non chiffrable"]
    assert all(p["heures"] is None and p["materiel_cad"] is None for p in non_chiffres)
    p.write_text(json.dumps({"complet": True, "lignes": [longueur]}), encoding="utf-8")
    r = chiffrage.calculer(w, q, catalogue, correspondances)
    emt = next(p for p in r["postes"] if p["label"] == "EMT")
    assert (emt["qte_catalogue"], emt["materiel_cad"], emt["heures"]) == ("10.000000", "40.00", "2.0000")