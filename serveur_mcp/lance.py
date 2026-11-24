"""Point d'entrée du serveur MCP « Expert estimateur » — argparse léger, import complet différé.

`python -m serveur_mcp` répond « initialize » avant d'avoir chargé le SDK (0,2 s exigé,
`demarrage.py`) ; ce module ne doit importer QUE la bibliothèque standard. Le transport
HTTP n'a pas de limite d'amorçage : l'import complet n'y est fait qu'à ce moment précis.
"""
from __future__ import annotations

import argparse
import sys


def lance(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m serveur_mcp", description="Serveur MCP Expert estimateur")
    ap.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    ap.add_argument("--hote", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--hote-permis", action="append", default=[], help="nom d'hôte public accepté (ex. estim.exemple.ca)")
    a = ap.parse_args(argv)
    if a.transport == "stdio":
        from . import demarrage
        return demarrage.stdio()
    from .serveur import application_http
    import uvicorn

    uvicorn.run(application_http(a.hote, a.hote_permis), host=a.hote, port=a.port)
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return lance(argv)
    except KeyboardInterrupt:
        return 0
    except BrokenPipeError:
        return 0
    finally:
        # Le transport du SDK peut fermer sys.stdout en sortant (stdio) : le vidage
        # final ne doit pas faire quitter le serveur en erreur pour un canal déjà fermé.
        try:
            sys.stdout.flush()
        except (ValueError, OSError, AttributeError):
            pass
