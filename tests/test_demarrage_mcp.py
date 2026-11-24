"""Contrôle du vrai transport stdio et des dépendances utilisées par le pipeline."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

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


def _ligne_initialize(version: str = "2025-06-18") -> bytes:
    return b'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"' + \
        version.encode() + b'","capabilities":{},"clientInfo":{"name":"mesure","version":"1"}}}'


def test_reponse_initialize_pareille_au_serveur_officiel():
    """La réponse immédiate est identique, champ par champ, à celle que le noyau du SDK produit."""
    import anyio

    import mcp_types
    from mcp.server.connection import Connection
    from mcp.server.runner import serve_one

    from serveur_mcp import demarrage
    from serveur_mcp.serveur import mcp

    rapide = demarrage.reponse_initialize(_ligne_initialize())
    assert rapide is not None, "la version 2025-06-18 doit être traitée en chemin rapide"
    ligne, poise = rapide
    assert json.loads(ligne)["result"]["protocolVersion"] == "2025-06-18"
    assert poise["version"] == "2025-06-18" and poise["client_info"]["name"] == "mesure"

    officiel: dict = {}

    async def noyau():
        resultat = await serve_one(mcp._lowlevel_server, demarrage.CtxEchange(1), "initialize",
                                   {"protocolVersion": "2025-06-18", "capabilities": {},
                                    "clientInfo": {"name": "mesure", "version": "1"}},
                                   connection=Connection.for_loop(None), lifespan_state={})
        officiel.update(resultat)

    anyio.run(noyau)
    assert officiel == json.loads(ligne)["result"], (
        "l'écart serait servi au client par deux serveurs différents")


def test_reponse_initialize_replis():
    """Version inconnue, notification, trame illisible : la main revient au serveur officiel."""
    from serveur_mcp import demarrage

    assert demarrage.reponse_initialize(b"not json") is None
    assert demarrage.reponse_initialize(
        b'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"1999-01-01"}}') is None
    assert demarrage.reponse_initialize(
        b'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}') is None
    assert demarrage.reponse_initialize(
        b'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}') is None


def test_versions_poise_suivent_le_sdk():
    """Les versions figées de la réponse immédiate restent celles du SDK installé (contrôle d'écart)."""
    import mcp_types

    from serveur_mcp import demarrage

    assert set(demarrage.VERSIONS_POISE) == set(mcp_types.version.HANDSHAKE_PROTOCOL_VERSIONS)


def test_chemin_lance_est_leger():
    """`serveur_mcp.lance` et `serveur_mcp.demarrage` ne tirent ni le SDK, ni pymupdf, ni skimage."""
    import subprocess
    import sys

    code = (
        "import sys; import serveur_mcp.lance, serveur_mcp.demarrage;"
        "interdits = ('mcp', 'pymupdf', 'PIL', 'openpyxl', 'sklearn', 'uvicorn');"
        "charges = sorted(m.split('.')[0] for m in sys.modules if m.split('.')[0] in interdits);"
        "print(charges); sys.exit(bool(charges))"
    )
    subprocess.run([sys.executable, "-c", code], check=True,
                   cwd=str(Path(__file__).resolve().parents[1]))

