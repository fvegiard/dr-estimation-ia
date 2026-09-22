"""Fixtures synthétiques partagées — AUCUNE donnée client.

Le PDF de test est généré à la volée par pymupdf : 2 pages avec cartouche
E100/E200 et texte, comme l'exige le SPEC. Les fichiers CSV/JSON de
`tests/fixtures/` sont synthétiques (quantités, positions, noms fictifs).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Lance une commande CLI du package et échoue proprement si != 0."""
    result = subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"commande en erreur ({result.returncode}) : {args}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    return result


@pytest.fixture(scope="session")
def pdf_synthetique(tmp_path_factory) -> Path:
    """PDF synthétique : 2 pages, cartouche E100/E200 en bas à droite,
    texte de plan au corps. Généré par pymupdf, aucune donnée client."""
    import pymupdf

    dossier = tmp_path_factory.mktemp("pdf")
    doc = pymupdf.open()
    for numero in ("E100", "E200"):
        page = doc.new_page(width=612, height=792)  # lettre portrait
        page.insert_text((72, 72), f"Plan synthetique {numero} - fixture de test", fontsize=12)
        page.insert_text(
            (72, 120),
            "Luminaire DS1  Prise duplex 20A 125V  Panneau P-1",
            fontsize=10,
        )
        page.insert_text((72, 200), "Aucune donnee client - page generee pour les tests", fontsize=9)
        # cartouche en bas à droite, numéro de feuille en plus gros
        page.draw_rect(pymupdf.Rect(430, 690, 590, 770))
        page.insert_text((440, 712), "PROJET SYNTHETIQUE", fontsize=8)
        page.insert_text((440, 730), "Fixture dr-estimation-ia", fontsize=8)
        page.insert_text((500, 762), numero, fontsize=16)
    chemin = dossier / "E-plans-synthetiques.pdf"
    doc.save(chemin)
    doc.close()
    return chemin


@pytest.fixture(scope="session")
def dossier_inbox(pdf_synthetique) -> Path:
    """Dossier d'entrée contenant le PDF synthétique (pour `inventaire`)."""
    return pdf_synthetique.parent
