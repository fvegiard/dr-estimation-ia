"""Lecture anonyme d'un dossier Google Drive public (« toute personne disposant du lien »), sans clé ni G:.

La page https://drive.google.com/embeddedfolderview?id=<dossier> liste les fichiers et sous-dossiers d'un dossier
public : on n'a besoin que des noms et des identifiants pour relier les documents reçus aux projets Plan Expert.
Marche sur ce PC comme dans Copilot cloud.
"""
from __future__ import annotations

import html
import re

import requests

ORIGINAL = "13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7"   # dossier « original » : documents reçus par projet
_ENTREE = re.compile(r'<div class="flip-entry" id="entry-([^"]+)".*?<a href="([^"]+)".*?'
                     r'<div class="flip-entry-title">(.*?)</div>', re.S)


class DossierDrive:
    def __init__(self, session: requests.Session | None = None):
        self.s = session or requests.Session()

    def lister(self, dossier_id: str) -> list[dict]:
        r = self.s.get("https://drive.google.com/embeddedfolderview", params={"id": dossier_id}, timeout=60)
        r.raise_for_status()
        return [{"id": i, "nom": html.unescape(t).strip(), "dossier": "/folders/" in href,
                 "url": html.unescape(href)} for i, href, t in _ENTREE.findall(r.text)]

    def fichiers(self, dossier_id: str, prefixe: str = "") -> list[dict]:
        """Tous les fichiers sous le dossier, avec « chemin » relatif (récursif)."""
        out = []
        for e in self.lister(dossier_id):
            chemin = f"{prefixe}{e['nom']}"
            if e["dossier"]:
                out += self.fichiers(e["id"], chemin + "/")
            else:
                out.append({**e, "chemin": chemin})
        return out
