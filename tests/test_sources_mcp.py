"""Une référence renommée doit être arrêtée avant toute extraction de symboles."""
from pathlib import Path

import pymupdf
import pytest

from serveur_mcp import serveur
from serveur_mcp.sources import motif_reference


def creer_pdf(chemin: Path, textes: list[str]) -> Path:
    with pymupdf.open() as doc:
        for texte in textes:
            page = doc.new_page()
            page.insert_text((30, 40), texte)
        doc.save(chemin)
    return chemin


def test_releve_renomme_detecte_meme_apres_trois_pages(tmp_path):
    pdf = creer_pdf(tmp_path / "E05-Electricite.pdf", [
        "PLAN ELECTRIQUE E01", "PLAN E02", "PLAN E03",
        "RELEVE E05 - MATERIEL\n115 reperes / 21 familles / calques activables",
    ])
    assert "page 4" in (motif_reference(pdf) or "")


@pytest.mark.parametrize("texte", [
    "E05 PLAN ELECTRIQUE\nRELEVE DES CONDITIONS EXISTANTES",
    "E05 MATERIEL ELECTRIQUE\nPRISE DE COURANT",
    "",
])
def test_source_sans_releve_acceptee(tmp_path, texte):
    assert motif_reference(creer_pdf(tmp_path / "E05.pdf", [texte])) is None


def test_reference_nommee_explicitement(tmp_path):
    pdf = creer_pdf(tmp_path / "E05-relevé.pdf", ["PLAN E05"])
    assert "nom de fichier" in (motif_reference(pdf) or "")


def test_preparation_refuse_avant_copie_et_pipeline(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path / "dossiers"))
    pdf = creer_pdf(tmp_path / "E05-Electricite.pdf", [
        "RELEVE E05 - MATERIEL\n115 reperes / 21 familles",
    ])
    with pytest.raises(serveur.ToolError, match="Source refusée"):
        serveur.preparer_dossier("ESSAI", str(pdf))
    assert not list((tmp_path / "dossiers/ESSAI/entree").iterdir())
    assert not (tmp_path / "dossiers/ESSAI/travail/feuilles.csv").exists()


def test_reprise_refuse_reference_deja_deposee(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    dossier = serveur.dossier_de("ESSAI", creer=True)
    creer_pdf(dossier / "entree/E05.pdf", [
        "RELEVE E05 - MATERIEL\n115 reperes / 21 familles",
    ])
    (dossier / "travail/blocs-index.csv").write_text("sig_id\n", encoding="utf-8")
    with pytest.raises(serveur.ToolError, match="Source refusée"):
        serveur.relever_automatique("ESSAI", reprendre=True)
