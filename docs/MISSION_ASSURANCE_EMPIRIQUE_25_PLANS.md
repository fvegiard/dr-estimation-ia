# MISSION : ASSURANCE EMPIRIQUE — BANC D'ESSAI 25 PLANS SUR LE SERVEUR MCP ISOLÉ

## Contexte et Objectif
Francis Végiard exige une preuve empirique solide et automatisée de la robustesse visuelle et fonctionnelle du serveur MCP d'estimation (`dr-estimation-ia`).
Tu dois tester de manière autonome un échantillon rigoureux de 25 plans/planches électriques issus des dossiers réels de soumission et/ou du banc de test de DR Électrique inc.

## Exigences de la Mission
1. **Isolation du banc d'essai** :
   - Travailler dans un répertoire isolé `travail-mcp/campagne-25-plans/`.
   - Ne pas altérer les dossiers de référence existants.

2. **Échantillon de 25 planches/plans** :
   - Sélectionner 25 feuilles/plans réels (ex. planches issues de `G:\Mon disque\D-claude-non-public-20260923\dr-electrique-soumissions-2026\S-1645 ANNEXE-BOURASSA\25084_Plans_Electrique.pdf`, Campus MIL `S-1842`, Sun Life `S-1644`, et les cas de tests représentatifs du répertoire).
   - Couvrir différentes disciplines : éclairage, puissance, moyenne tension 25kV, contrôle d'accès.

3. **Traitement MCP complet de bout en bout** :
   - Exécuter la chaîne complète : vectorisation, classification de symboles, comptage, pastilles de repérage centrées, bordereau incrusté dans l'espace libre, génération de projet Plan Expert (.qpl), tableur BOM Excel avec onglet Main-d'œuvre au taux officiel de 124 $/h, et planches de contrôle PNG.

4. **Validation du Rendu Visuel (Assurance Empirique)** :
   - Vérifier le score visuel (pastilles centrées sur les symboles, zéro chevauchement destructif, encadré bordereau dans l'espace libre).
   - Générer pour chaque plan la planche de contrôle (`controle/*.png`).
   - Journaliser le taux de succès (Exit code 0, score visuel /25).

5. **Livrable Final** :
   - Produire un rapport d'assurance empirique consolidé `docs/RAPPORT_ASSURANCE_EMPIRIQUE_25_PLANS.md` avec tableau de synthèse (Nom du plan, Feuille, Nombre de repères, Score visuel, BOM générée, Statut).
   - Valider la suite de tests avec pytest (exit code 0).