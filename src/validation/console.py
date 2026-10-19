"""Sortie console des CLI de validation : toujours en UTF-8.

Sous Windows, Python écrit dans un tube ou un fichier avec l'encodage local (cp1252) : le verdict
`GEL VIOLÉ` devient illisible pour le lanceur qui décode en UTF-8, et une flèche « → » fait planter le CLI
(UnicodeEncodeError) — le verdict de la boucle d'acceptation est alors perdu pour `releve/run.py`. Chaque
CLI de `src.validation` appelle `forcer_utf8()` avant `main()` : la sortie est en UTF-8 sur tous les postes
(console Windows comprise, déjà en UTF-8 depuis Python 3.6) ; le lanceur décode en UTF-8.
"""
from __future__ import annotations

import sys


def forcer_utf8() -> None:
    """stdout et stderr du processus en UTF-8 (sans effet sur un flux qui n'est pas un TextIOWrapper)."""
    for flux in (sys.stdout, sys.stderr):
        reconfigurer = getattr(flux, "reconfigure", None)
        if reconfigurer is not None:
            reconfigurer(encoding="utf-8")
