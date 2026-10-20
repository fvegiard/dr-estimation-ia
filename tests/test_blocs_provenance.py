"""Les sorties des blocs citent leur inventaire, jamais un dossier de démonstration."""
from __future__ import annotations

import csv
import sys

import pymupdf
import pytest

from releve import blocs_vers_releve


def _csv(chemin, lignes):
    with chemin.open("w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)


@pytest.mark.parametrize("luminaire", [False, True])
@pytest.mark.parametrize(("titre", "attendu"), [
    ("Plan nouveau", "plan"),
    ("TABLEAU DES APPAREILS", "tableau"),
    ("SCHÉMA UNIFILAIRE", "schema"),
    ("DÉTAIL D'INSTALLATION", "detail"),
    ("LÉGENDE ÉLECTRIQUE", "legende"),
])
def test_provenance_source_reelle_sans_dossier_ou_tableau_invente(
        tmp_path, monkeypatch, luminaire, titre, attendu):
    """Cinq blocs déjà extraits suffisent; aucun rendu ou pipeline d'extraction à rejouer."""
    base = tmp_path
    tmp_path = base / "DOSSIER" / "travail"
    tmp_path.mkdir(parents=True)
    (tmp_path / "feuilles").mkdir()
    (tmp_path / "blocs").mkdir()
    document = pymupdf.open()
    page = document.new_page(width=600, height=200)
    page.insert_text((20, 20), "NOUVEAU")
    for decalage in range(0, 500, 100):
        page.draw_rect(pymupdf.Rect(80 + decalage, 80, 100 + decalage, 86), width=0.5)
        if luminaire:
            page.insert_text((84 + decalage, 77), "A1", fontsize=6)
    document.save(tmp_path / "feuilles" / "BAT-A.pdf")
    document.close()
    _csv(tmp_path / "feuilles.csv", [{"feuille": "BAT-A", "fichier": "batiment-electrique.pdf",
                                    "page": "1", "role": "plan", "titre": titre}])
    _csv(tmp_path / "blocs-index.csv", [{"sig_id": "S001", "signature": "rectangle"}])
    _csv(tmp_path / "blocs-familles.csv", [{
        "sig_id": "S001", "label": "ENCASTRE" if luminaire else "BOITE JONCTION",
        "famille": "eclairage" if luminaire else "distribution", "forme": "carre",
        "code": "LU" if luminaire else "BJ", "materiel": "Luminaire" if luminaire else "Boîte",
        "legende_no": "", "diam_min": "0", "diam_max": "99", "feuilles": "", "note": "",
    }])
    _csv(tmp_path / "blocs" / "BAT-A.csv", [{
        "signature": "rectangle", "x_pt": str(90 + decalage), "y_pt": "83", "w_pt": "20", "h_pt": "6",
        "diametre_pt": "20",
    } for decalage in range(0, 500, 100)])
    monkeypatch.setattr(sys, "argv", ["blocs_vers_releve.py", str(tmp_path), "--modele", "test"])
    blocs_vers_releve.main()
    with (tmp_path / "occurrences-visuel.csv").open(encoding="utf-8") as fichier:
        occurrences = list(csv.DictReader(fichier))
    with (tmp_path / "feuilles-classement.csv").open(encoding="utf-8") as fichier:
        classement = list(csv.DictReader(fichier))
    assert classement[0]["type"] == attendu
    from serveur_mcp import serveur
    monkeypatch.setenv("ESTIMATEUR_BASE", str(base))
    quantites = serveur.quantites("DOSSIER")
    with (tmp_path / "nomenclature.csv").open(encoding="utf-8") as fichier:
        nomenclature = list(csv.DictReader(fichier))
    if attendu != "plan":
        assert occurrences == []
        assert nomenclature == []
        assert quantites["represente"] == quantites["total"] == 0
        assert f"Feuilles exclues des plans : BAT-A ({attendu})" in (
            tmp_path / "reserves.md").read_text(encoding="utf-8")
        return
    assert len(occurrences) == 5
    assert [(o["x_pt"], o["y_pt"]) for o in occurrences] == [
        (f"{90 + decalage:.1f}", "83.0") for decalage in range(0, 500, 100)]
    assert quantites["represente"] == quantites["total"] == 5
    assert "batiment-electrique.pdf, page 1, feuille BAT-A" in nomenclature[0]["source"]
    assert "bloc S001" in nomenclature[0]["source"]
    textes = "\n".join((tmp_path / nom).read_text(encoding="utf-8") for nom in (
        "nomenclature.csv", "rapport-releve.md", "reserves.md", "feuilles-classement.csv",
    ))
    for fictif in ("E-001", "E-008", "E008", "E-201", "E-203", "S-1902", "Georgette", "21 feuilles",
                   "116/121", "20 USB", "cartouche="):
        assert fictif not in textes
    assert "Inventaire : 1 feuille(s)" in textes
    assert "hypothèses du moteur à confirmer" in textes
    if luminaire:
        assert nomenclature[0]["label"] == "LUMINAIRE A1"
        assert nomenclature[0]["description"] == "Luminaire type A1"
        assert "A1 : 5" in textes


def test_provenance_incomplete_est_signalee():
    assert blocs_vers_releve.source_feuille("PLAN-A", {}) == (
        "fichier non renseigné, page non renseignée, feuille PLAN-A")


@pytest.mark.parametrize(("feuille", "attendu"), [
    ({"feuille": "plans-p01", "role": "plan", "titre": "PLAN ELECTRIQUE"}, "plan"),
    ({"feuille": "BAT-A", "role": "plan", "titre": "PLAN NOUVEAU"}, "plan"),
    ({"feuille": "BAT-A", "role": "plan", "titre": "PLAN D'ÉCLAIRAGE ET DÉTAILS"}, "plan"),
    ({"feuille": "BAT-A", "role": "plan", "titre": "PLAN DES PANNEAUX ÉLECTRIQUES"}, "plan"),
    ({"feuille": "BAT-A", "role": "plan", "titre": "PLAN ET SCHÉMA D'ALIMENTATION"}, "plan"),
    ({"feuille": "E201", "role": "legende", "titre": "PLAN"}, "legende"),
    ({"feuille": "E201", "role": "plan", "titre": "LÉGENDE ÉLECTRIQUE"}, "legende"),
    ({"feuille": "plans-p01", "role": "devis", "titre": "DEVIS"}, "devis"),
    ({"feuille": "E201", "role": "plan", "titre": "TABLEAU DES APPAREILS"}, "tableau"),
    ({"feuille": "E201", "role": "plan", "titre": "PANNEAUX ÉLECTRIQUES"}, "tableau"),
    ({"feuille": "E201", "role": "plan", "titre": "SCHÉMA UNIFILAIRE"}, "schema"),
    ({"feuille": "E201", "role": "plan", "titre": "DÉTAIL D'INSTALLATION"}, "detail"),
    ({"feuille": "plans-p01", "role": "detail", "titre": "INSTALLATION"}, "detail"),
])
def test_classement_role_et_titre_sans_restriction_de_nom(feuille, attendu):
    assert blocs_vers_releve.classer_feuille(feuille) == attendu
