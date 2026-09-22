"""Métré des artères et injection de tracés <Line> dans un .qpl.

Porté depuis planexpert-s1857-saint-michel/arteres/ (voir
docs/consolidation.md) :
- `compute_arteres.py` : géométrie du métré (Manhattan orthogonal, montées,
  raccords locaux, réserves) — les données de la soumission (niveaux,
  équipements, départs) sont chargées depuis un JSON `--config`, jamais
  codées en dur.
- `inject_lines.py` : injection des segments dans le .qpl, chemins en
  arguments, assertion d'unicité des GroupID **corrigée**.
"""
