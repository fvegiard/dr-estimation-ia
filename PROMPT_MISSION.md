# MISSION DE FINALISATION COMPLÈTE : DR-ESTIMATION-IA MCP SERVER

## Contexte & Client
- **Entreprise** : DR Électrique inc. (Varennes QC, RBQ 5587-4812-01)
- **Chargé de projet** : Francis Végiard
- **Taux horaire MO de référence** : 124 $/h
- **Objectif** : Finalisation clé en main du pipeline d'extraction, comptage et métré des plans électriques.

## Spécifications Techniques & Logique Métier
1. **Environnement virtuel permanent** :
   - Le serveur MCP doit impérativement utiliser .venv compilé en local (.venv/Scripts/python.exe -m serveur_mcp), démarrant en moins de 0.2 seconde sans compilation dynamique.
2. **Gestion des plans bruts vs références estimateurs** :
   - Les fichiers contenant eleve sont des références humaines de comparaison.
   - Les plans bruts à métrer s'appellent E05-Electricite.pdf ou similaire.
3. **Moteur d'extraction et de vision** :
   - Rendu raster haute résolution 5694px découpé en 12 tuiles (tiles).
   - Extraction des 106 signatures de blocs CAD (prises, interrupteurs, luminaires, thermostats, panneaux).
4. **Livrables de sortie obligatoires** :
   - PDF final annoté avec points de couleur sur chaque symbole extrait.
   - Rapport de décompte des quantités et estimation des coûts MO à 124 $/h.
   - Exportation de la nomenclature (BOM) et du fichier Plan Expert .qpl.

## Protocole de Test & Commits
- Chaque module doit être validé par un test unitaire et d'intégration avec Exit Code 0.
- Commiter chaque étape avec des messages de commit conventionnels explicites.
