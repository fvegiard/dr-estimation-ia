# Base de données Plan Expert (EE) — script consolidé V0 → V45

Script SQL unique consolidé à partir du package `V14_UpdateDatabase.zip` fourni par
M. Daniel Dupuis (estimateur sénior DR Électrique), 22 septembre 2026.

- **Fichier :** `EE_BaseDeDonnees_Complet_V0_V45.sql` (12 929 214 octets)
- **SHA256 :** `0aa1ec89ca16abc0a1e88f696bbf491c785e497410d9747f1723cc54650148f7`
- **Encodage :** Windows-1252 (CP1252) — ouvrir avec ce codage dans SSMS, pas UTF-8.
- **Séparateur de lots :** `GO` (2 029 lots) — requis pour l'exécution SSMS/sqlcmd.
- **Aucun `USE` :** le script ne sélectionne pas de base ; choisir la base cible avant l'exécution.

## Ordre d'exécution des sections

Le script est déjà dans l'ordre exact ; chaque section porte sa bannière `/* SECTION : … */` :

1. `DeleteScripts.sql` — suppression des stored procedures
2. `DeleteTables.sql` — suppression des tables
3. `CreateTables.sql` — création des tables
4. `CreateScripts.sql` — création des stored procedures
5. `CreateData.sql` — données de référence
6. `Central_CreateTables.sql` — tables centrales
7. `Central_CreateScripts.sql` — procédures centrales
8. `UpdateDatabase.sql (V0/V1/V2)` — migrations de base
9. `V3_UpdateDatabase.sql` → `V45_UpdateDatabase.sql` — migrations successives

## Cas d'usage

- **Base de données neuve :** sauter les sections 1–2 (DeleteScripts / DeleteTables) — il n'y a
  rien à supprimer. Commencer à `CreateTables.sql`.
- **Base de données existante (rebuild complet) :** le script est destructif
  (DROP PROCEDURE / DROP TABLE). **Faire une sauvegarde complète avant l'exécution.**

## Notes

- `V28_UpdateDatabase.sql` et `V35_UpdateDatabase.sql` sont des sections vides
  (placeholders dans le package d'origine — aucune migration à ces versions).
- La section 5 (`CreateData.sql`) correspond à la base « EE » standard ; les scripts
  `_Calgary` exclusifs à la version interne ne font pas partie de ce package.

## Vérification d'intégrité

```bash
sha256sum EE_BaseDeDonnees_Complet_V0_V45.sql
# doit donner : 0aa1ec89ca16abc0a1e88f696bbf491c785e497410d9747f1723cc54650148f7
```
