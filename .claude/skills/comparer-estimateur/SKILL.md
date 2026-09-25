---
name: comparer-estimateur
description: Rejoue le jeu de référence (relevé IA vs projets Plan Expert de l'estimateur) et explique ce qui a changé. À utiliser après toute modification de releve/ ou de la compétence releve-planexpert, ou quand une nouvelle copie corrigée de l'estimateur arrive.
allowed-tools: Bash(python -m src.validation.jeu_reference*) Bash(python -m src.validation.compare_qpl*) Read Glob Grep
---

# Comparer au relevé de l'estimateur

1. `python -m src.validation.jeu_reference` depuis la racine du dépôt.
2. Lis `dossiers/_jeu-reference/resultats.md` : rappel/précision par dossier et écart à la ligne de base.
3. Pour chaque dossier qui a bougé de plus d'un point, ouvre `dossiers/<S>/comparaison-dupuis-qpl/ecart-dupuis.md`
   (tableau par libellé, marques manquantes/en trop avec coordonnées) et dis quels libellés expliquent le changement.
4. Ne mets à jour la ligne de base (`--nouvelle-base`) que si aucun dossier n'a régressé et que Francis l'a demandé.

Nouvelle copie de l'estimateur pour un dossier `<S>` : dépose son `.qpl` dans `dossiers/<S>/reference/<S>-Dupuis-PlanExpert.qpl`,
les dimensions de ses PNG (lues dans l'en-tête, 24 octets, jamais les images elles-mêmes) dans
`dossiers/<S>/reference/dupuis-png-dimensions.txt` (`dossier|nom.png|largeur|hauteur`) et le `feuilles.csv` du relevé IA dans
`dossiers/<S>/reference/feuilles-ia.csv` ; le dossier entre alors dans le jeu.
