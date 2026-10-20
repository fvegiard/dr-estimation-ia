"""Contrôle du vrai transport stdio et des dépendances utilisées par le pipeline."""
from __future__ import annotations

import importlib
import sys

import pytest

from outils.mesurer_demarrage_mcp import mesurer


def test_demarrage_stdio_et_catalogues():
    # La performance dépend du poste : le benchmark CLI impose séparément < 0,2 s.
    preuve = mesurer(sys.executable)
    assert preuve["exit_code"] == 0
    assert preuve["initialize_s"] > 0
    assert preuve["catalogues_s"] >= preuve["initialize_s"]
    assert preuve["outils"] > 0


@pytest.mark.parametrize("module", [
    "pymupdf", "PIL.Image", "openpyxl", "pydantic", "numpy", "scipy",
    "sklearn", "joblib", "markdown", "mcp.server", "uvicorn", "requests",
])
def test_dependance_pipeline_importable(module):
    # Aucun importorskip : une dépendance déclarée absente bloque la livraison.
    importlib.import_module(module)
