"""Import de compteurs dans un .qpl Plan Expert existant + charte graphique.

- `import_counters.py` : CSV d'occurrences -> compteurs insérés dans le
  .qpl (porté depuis planexpert-s1857-saint-michel/tools/import/, CLI
  typer remplacée par argparse — voir docs/consolidation.md).
- `charte.py` : règles forme/couleur/taille par famille d'objets (porté
  depuis planexpert-s1857-saint-michel/verification/rules_dupuis.py) et
  classification des libellés en postes.
"""
