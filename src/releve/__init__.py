"""Outil de relevé de quantités (Plan Expert) — socle réutilisable.

Porté depuis `dr-releves-2026/_socle/releve/` (voir docs/consolidation.md).

Sous-commandes, une par étape du pipeline documenté dans
`docs/pipeline-qpl.md` : inventaire, index, raster, qpl, verifier, xlsx.
Voir `__main__.py` pour le point d'entrée en ligne de commande
(`python -m src.releve <sous-commande> ...`), et `xlsx_export.py` pour
l'export `releve.xlsx` au gabarit DR (`python -m src.releve.xlsx_export`).
"""

__version__ = "0.2.0"
