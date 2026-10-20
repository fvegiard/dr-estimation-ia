"""Régressions des livrables : deux sources, multiplicateurs et MO sourcée."""
from __future__ import annotations

import csv
import json
import zipfile

import pytest
from openpyxl import load_workbook

from serveur_mcp import livrables, serveur


def _travail(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    travail = tmp_path / "ESSAI" / "travail"
    travail.mkdir(parents=True)
    sortie = travail.parent / "sortie"
    sortie.mkdir()
    (sortie / "vecteur").mkdir()
    (sortie / "vecteur" / "bordereau.csv").write_text(
        "repere,code\nP01-01,PRISE\nL01-01,LUMINAIRE\n", encoding="utf-8")
    fichiers = {
        "feuilles.csv": "feuille,page\nE01,1\n",
        "feuilles-classement.csv": "feuille,type\nE01,plan\n",
        "nomenclature.csv": "label,description,famille,heures_unitaires,source_heures\n"
                            "PRISE,Prise double,prise,0.5,Barème approuvé ligne 7\n"
                            "LUMINAIRE,Luminaire,luminaire,,\n",
        "occurrences-texte.csv": "feuille,label,x_pt,y_pt,exclure\n"
                                 "E01,PRISE,10,10,\nE01,PRISE,80,80,1\nE01,PRISE,81,81,oui\n"
                                 "E01,PRISE,82,82,x\nE01,PRISE,83,83,true\n",
        "occurrences-visuel.csv": "feuille,label,x_pt,y_pt,exclure\n"
                                  "E01,PRISE,10,10,\nE01,LUMINAIRE,20,20,\n",
        "multiplicateurs.csv": "feuille,facteur,source\nE01,3,Cartouche : 3 unités\n",
    }
    for nom, contenu in fichiers.items():
        (travail / nom).write_text(contenu, encoding="utf-8")
    return travail, sortie


def test_bom_union_multiplicateurs_et_mo_sans_heures_inventees(tmp_path, monkeypatch):
    travail, sortie = _travail(tmp_path, monkeypatch)
    resultat = serveur._empaqueter_zip_png(travail, sortie, "ESSAI", {})
    assert resultat["quantites"]["represente"] == 2
    assert resultat["quantites"]["total"] == 6
    with (sortie / "png" / "ESSAI-BOM-QUANTITES.csv").open(encoding="utf-8") as fichier:
        comptes = {r["label"]: r for r in csv.DictReader(fichier)}
    assert {k: r["total"] for k, r in comptes.items()} == {"PRISE": "3", "LUMINAIRE": "3"}
    assert ((sortie / "png" / "ESSAI-BOM.csv").read_bytes()
            == (sortie / "vecteur" / "bordereau.csv").read_bytes())
    classeur = load_workbook(sortie / "png" / "ESSAI-BOM.xlsx", data_only=True)
    releve = list(classeur["Relevé"].values)
    assert {r[1]: r[2] for r in releve[1:]} == {"PRISE": 3, "LUMINAIRE": 3}
    mo = {r[0]: r for r in list(classeur["Main-d'œuvre"].values)[1:] if r[0]}
    assert mo["PRISE"][3:6] == (1.5, 124, 186)
    assert mo["LUMINAIRE"][2:4] == (None, None)
    assert mo["LUMINAIRE"][5] is None
    classeur.close()
    estimation = json.loads((sortie / "png" / "ESSAI-ESTIMATION-MO.json").read_text(encoding="utf-8"))
    assert estimation["complet"] is False
    assert "CONSERVER" in estimation["reserve_portee"]
    reserve_portee = mo["Réserve de portée"][1]
    assert isinstance(reserve_portee, str)
    assert "CONSERVER" in reserve_portee
    assert estimation["cout_mo_total"] is None
    assert estimation["sous_total_postes_chiffres"] == 186
    with zipfile.ZipFile(sortie / "ESSAI-LIVRABLES-PNG.zip") as archive:
        assert {"ESSAI-BOM.csv", "ESSAI-BOM-QUANTITES.csv", "ESSAI-BOM.xlsx", "ESSAI-ESTIMATION-MO.md",
                "quantites.csv", "releve/multiplicateurs.csv"} <= set(archive.namelist())


def test_erreur_export_xlsx_ne_peut_pas_etre_masquee(tmp_path, monkeypatch):
    travail, sortie = _travail(tmp_path, monkeypatch)

    def erreur(*args):
        raise OSError("Export XLSX impossible")

    monkeypatch.setattr(livrables, "ecrire_xlsx", erreur)
    with pytest.raises(OSError, match="Export XLSX impossible"):
        serveur._empaqueter_zip_png(travail, sortie, "ESSAI", {})
    assert not (sortie / "ESSAI-LIVRABLES-PNG.zip").exists()


@pytest.mark.parametrize("valeur", ["abc", "-1", "nan", "inf"])
def test_heures_invalides_refusees(tmp_path, monkeypatch, valeur):
    travail, sortie = _travail(tmp_path, monkeypatch)
    nomenclature = travail / "nomenclature.csv"
    nomenclature.write_text(
        nomenclature.read_text(encoding="utf-8").replace("0.5", valeur), encoding="utf-8")
    with pytest.raises(ValueError, match="heures_unitaires"):
        serveur._empaqueter_zip_png(travail, sortie, "ESSAI", {})


def test_heures_sans_source_restent_non_chiffrables(tmp_path, monkeypatch):
    travail, sortie = _travail(tmp_path, monkeypatch)
    nomenclature = travail / "nomenclature.csv"
    nomenclature.write_text(
        nomenclature.read_text(encoding="utf-8").replace("Barème approuvé ligne 7", ""), encoding="utf-8")
    resultat = serveur._empaqueter_zip_png(travail, sortie, "ESSAI", {})
    assert resultat["estimation_mo"]["cout_mo_total"] is None
    assert all(p["heures"] is None for p in resultat["estimation_mo"]["postes"])


@pytest.mark.parametrize("exclusion", ["1", "oui", "x", "true"])
def test_controle_ignore_les_occurrences_exclues_invalides(tmp_path, monkeypatch, exclusion):
    travail, _ = _travail(tmp_path, monkeypatch)
    (travail / "feuilles.csv").write_text(
        "feuille,page,largeur_pt,hauteur_pt\nE01,1,100,100\n", encoding="utf-8")
    (travail / "reserves.md").write_text("# R-001 : essai synthétique\n", encoding="utf-8")
    (travail / "occurrences-visuel.csv").write_text(
        "feuille,label,x_pt,y_pt,exclure\n"
        f"E01,INCONNU,999,999,{exclusion}\n", encoding="utf-8")
    resultat = serveur.verifier_releve("ESSAI")
    assert resultat["pret"], resultat["erreurs"]
    assert resultat["occurrences"] == 1
