"""Contrôle des sources : un relevé renommé ne devient pas un plan brut."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path


def motif_reference(pdf: Path) -> str | None:
    """Repère les références explicites sans inférer le rôle d'un simple scan.

    Les exports du moteur portent un encadré et un résumé caractéristiques.
    Le contrôle porte sur toutes les pages, y compris celles après les plans.
    """
    import pymupdf

    def normaliser(texte: str) -> str:
        return unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode().upper()

    nom = normaliser(pdf.stem)
    if re.search(r"RELEVE|TAKE[ _-]*OFF|ESTIMATEUR|DUPUIS", nom):
        return "nom de fichier désignant un relevé de référence"
    with pymupdf.open(pdf) as doc:
        for index in range(len(doc)):
            numero = index + 1
            page = doc[index]
            texte = " ".join(normaliser(page.get_textpage().extractText()).split())
            encadre = re.search(r"\bRELEVE\b.{0,100}\bMATERIEL\b", texte)
            compte = re.search(r"\d+\s+REPERES\s*/\s*\d+\s+FAMILLES\b", texte)
            if encadre and compte:
                return f"page {numero} : encadré de relevé et décompte de repères déjà présents"
    return None
