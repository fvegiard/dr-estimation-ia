"""Pipeline de préparation d'un dossier de soumission.

Porté depuis planexpert-core/releve/ (voir docs/consolidation.md) :
imports convertis en imports relatifs de package. Les étapes :

1. `prepare.py`              dossier déposé -> feuilles, rasters, tuiles, mots
2. `extract_occurrences.py`  étiquettes texte -> occurrences (déterministe)
3. `zoom.py`                 lecture visuelle d'une zone avec règles graduées
4. `build_qpl.py`            occurrences + nomenclature -> projet .qpl + rasters
5. `render_pdf.py`           plans annotés + rapport de métré + dossier PDF

NON portés (dépendent de l'agent local de Francis) : agent_sdk.py, run.py.
"""
