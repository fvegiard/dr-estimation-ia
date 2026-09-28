# Vérification de `eewin/EE_DR.sql` — un seul fichier qui recrée la base `EE` à l'identique

Date d'exécution : 2026-09-27, 14:13 → 14:40 (heure de l'Est). Serveur : SQL Server 2022 (RTM-CU27, 16.0.4295.3),
conteneur Docker `eewin`, base source `EE` (rebâtie le 2026-09-27 à 16:17 UTC à partir des 52 scripts officiels de
`eewin/scripts/`, journal `eewin/run.log` : 0 erreur ; puis alimentée par `eewin/soumissions-dr/load_dr_submissions.sql`,
voir [[SOUMISSIONS-DR]]). Toutes les sorties citées ci-dessous sont des sorties réelles, conservées intégralement dans
`eewin/verification/`.

## 0. Résultat en une ligne

`eewin/EE_DR.sql` (8 080 854 octets, 98 655 lignes, 441 lots `GO`, SHA-256
`d8aacb160d88e75aa2db7f2d805f0e59223ff7661a6fb83e58ad25939d0a46e2`), exécuté seul dans une base vide `EE_TEST`, redonne
une base que la comparaison objet par objet et **ligne par ligne** (84 837 lignes, 60 tables, 1 061 colonnes, 106 index,
61 défauts, 178 modules hachés SHA-256, 17 compteurs d'identité) déclare **`IDENTICAL`, 0 différence**
(`eewin/verification/02-compare-EE-vs-EE_TEST.log`, dernière ligne). Le moteur officiel `sp_SOU_CalculTotaux` rejoué dans
`EE_TEST` redonne 238 744,00 et 96 298,36 (`03-engine-EE_TEST.log`).

## 1. Choix de l'outil (ordre imposé par la tâche : mssql-scripter → sqlpackage/bcp → générateur Python)

| Outil | Essayé | Résultat réel | Preuve |
|---|---|---|---|
| **mssql-scripter** (Microsoft, PyPI) | oui | pip-installable (`mssql_scripter-1.0.0a23`, dernière publication PyPI **2018-06-28**, `docs/sources/pypi-mssql-scripter.json`). Trois obstacles successifs : ICU absent (`DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1` règle), `libssl.so.1.0.0` absente d'Ubuntu 24.04 (fournie localement depuis le paquet bionic `libssl1.0.0_1.0.2n-1ubuntu5.13`), puis **échec définitif au login TDS** : `System.InvalidOperationException: Internal connection fatal error` dans `System.Data.SqlClient.TdsParser.TryRun` → `CompleteLogin`. Le client SQL de 2018 embarqué ne lit pas la réponse de login de SQL Server 2022. Aucun fichier produit. | `verification/00-mssql-scripter-attempt.log`, `00-mssql-scripter-sqltoolsservice.log` (journal .NET complet) |
| **sqlpackage** `/Action:Script` | non (écarté sur documentation) | « creates a Transact-SQL incremental update script that updates the **schema** of a target database » — pas de données dans le script ; un `.bacpac` contient les données en BCP binaire, pas en T-SQL. Ne répond pas à « un seul .sql schéma + données ». | `docs/sources/sqlpackage-script.txt` l.38 |
| **bcp** | non (écarté) | un fichier par table, format natif ou texte, pas de T-SQL, pas de schéma. | `/opt/mssql-tools18/bin/bcp` présent dans le conteneur, non pertinent |
| **Générateur Python** `eewin/tools/generate_ee_dr_sql.py` | **retenu** | 728 lignes, code et commentaires en anglais, une seule dépendance (`pymssql 2.4.2`, FreeTDS). Lit uniquement les vues catalogue de la base vivante et fait `SELECT *` sur chaque table. Rien n'est écrit à la main. | `01-load-EE_TEST.log`, `02-compare-EE-vs-EE_TEST.log`, `07-determinism.log` |

Ce que le générateur lit, et où (aucune valeur inventée) :

| Section de `EE_DR.sql` | Vues catalogue lues | Lignes du fichier |
|---|---|---|
| Garde de cible (base système, collation `French_CI_AS`, base non vide → `RAISERROR` 16) | `sys.databases.collation_name` de la source | 17-24 |
| 160 procédures (avant les tables, voir §3.2) | `sys.sql_modules.definition` (= `OBJECT_DEFINITION`), `uses_ansi_nulls`, `uses_quoted_identifier`, `sys.objects` | 26-11165 |
| 60 tables : colonnes, types, longueurs, `COLLATE`, `IDENTITY(seed,inc)`, `NULL/NOT NULL`, défauts, PK | `sys.tables`, `sys.columns`, `sys.types`, `sys.identity_columns`, `sys.default_constraints`, `sys.key_constraints`, `sys.index_columns` | 11166-12573 |
| 61 index non-clés (`UNIQUE`, `INCLUDE`, filtre, options non par défaut) | `sys.indexes`, `sys.index_columns` | 12574-12637 |
| Clés étrangères (0 dans `EE`) et contraintes CHECK (0) — code présent pour une base qui en aurait | `sys.foreign_keys`, `sys.foreign_key_columns`, `sys.check_constraints` | 12638-12640 |
| 18 fonctions, triées topologiquement | `sys.sql_expression_dependencies` | 12641-13620 |
| Données : 84 837 lignes dans 12 tables, `INSERT … VALUES` par paquets de 1 000, `SET IDENTITY_INSERT` | `SELECT *` ordonné par la clé primaire | 13621-98611 |
| 17 compteurs d'identité remis à la valeur de la source | `sys.identity_columns.last_value` | 98612-98652 |

## 2. Preuve : `EE_TEST` créée à partir du seul `EE_DR.sql`

Commandes exécutées (`verification/01-load-EE_TEST.log`, sortie intégrale) :

```
$ sha256sum eewin/EE_DR.sql
d8aacb160d88e75aa2db7f2d805f0e59223ff7661a6fb83e58ad25939d0a46e2  eewin/EE_DR.sql
$ sqlcmd -Q "IF DB_ID('EE_TEST') IS NOT NULL BEGIN ALTER DATABASE EE_TEST SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE EE_TEST; END; CREATE DATABASE EE_TEST COLLATE French_CI_AS;"
$ docker cp eewin/EE_DR.sql eewin:/tmp/EE_DR.sql
$ sqlcmd -d EE_TEST -f 65001 -x -b -I -i /tmp/EE_DR.sql
…
EE_DR.sql applied to EE_TEST
exit=0 elapsed=25s
```

Le journal contient 0 ligne `Msg ` (erreur), 51 messages informatifs « The module 'X' depends on the missing object 'Y'.
The module will still be created » et 7 « Caution: Changing any part of an object name… ». Les 51 messages viennent de
l'ordre alphabétique de création des procédures (l'appelée n'existe pas encore au moment où l'appelante est créée) ou
d'objets qui **n'existent pas non plus dans `EE`** (`dbo.sp_CalculCodeImpr`, `dbo.sp_SOU_UpdateQteTotalOth`… : ils
n'existent que sous un nom avec point, [[SCHEMA]] §6.1). Les 7 « Caution » sont émis par les 7 `sp_rename` du §3.1.

Options `sqlcmd` et pourquoi (`docs/sources/sqlcmd-utility.txt`, `sqlcmd-commands.txt`) :
`-f 65001` = fichier UTF-8 (« Specifies the input and output code pages », l.738) ; `-x` = « Causes sqlcmd to ignore
scripting variables … useful when a script contains many INSERT statements that might contain strings that have the same
format as regular variables, such as $(<variable_name>) » (l.929) ; `-b` = « sqlcmd exits and returns a DOS ERRORLEVEL
value when an error occurs … 1 when the SQL Server error message has a severity level greater than 10 » (l.1005) ;
`:on error exit` en tête de fichier (« Sets the action to perform when an error occurs … the exit option, sqlcmd exits »,
`sqlcmd-commands.txt` l.189-193) — le fichier s'arrête donc à la première erreur même sans `-b`. `-I` = `QUOTED_IDENTIFIER ON`,
comme pour les 52 scripts d'origine (`eewin/run.sh`).

## 3. Comparaison `EE` ↔ `EE_TEST` (`eewin/tools/compare_ee_databases.sql`, sortie `02-compare-EE-vs-EE_TEST.log`)

Le script compare, dans les deux sens (`EXCEPT` A→B puis B→A), et ne fait aucune hypothèse sur les noms de tables :

| # | Ce qui est comparé | Source de la comparaison | Résultat |
|---|---|---|---|
| 1 | collation, niveau de compatibilité, options ANSI de la base | `sys.databases` | `French_CI_AS`, 160, FULL, 0, 0 des deux côtés |
| 2 | comptes d'objets par type | `sys.objects` | DEFAULT_CONSTRAINT 61/61, PRIMARY_KEY_CONSTRAINT 45/45, SQL_SCALAR_FUNCTION 17/17, SQL_STORED_PROCEDURE 160/160, SQL_TABLE_VALUED_FUNCTION 1/1, USER_TABLE 60/60 |
| 3 | liste des tables | `sys.tables` ⊖ | 0 table d'un seul côté |
| 4 | `COUNT(*)` de chaque table | curseur sur les 60 tables | 60/60 `same`, 84 837 = 84 837 |
| 5 | 1 061 colonnes : position, type, longueur, précision, nullabilité, défaut, collation, identité, seed, incrément | `INFORMATION_SCHEMA.COLUMNS` + `sys.columns` + `sys.identity_columns` ⊖ | 0 différence |
| 6 | 106 index et clés : nom, type, unique, PK, colonnes clés dans l'ordre + ASC/DESC, colonnes incluses, options de verrou, fill factor | `sys.indexes` + `sys.index_columns` (`STRING_AGG … WITHIN GROUP`) ⊖ | 0 différence, 106/106 |
| 7 | 61 défauts (table, colonne, définition ; le nom n'est comparé que s'il est donné par l'utilisateur), FK 0/0, CHECK 0/0 | `sys.default_constraints`, `sys.foreign_keys`, `sys.check_constraints` ⊖ | 0 différence |
| 8 | 178 modules : schéma, nom, type, **SHA-256 de `definition`**, `uses_ansi_nulls`, `uses_quoted_identifier` | `sys.sql_modules` + `HASHBYTES('SHA2_256', …)` ⊖ | 0 différence ; FN 17/17 (25 067 caractères), P 160/160 (271 270), TF 1/1 (872) |
| 9 | valeur courante de chaque identité | `sys.identity_columns.last_value` ⊖ | 0 différence ; 17 tables listées côte à côte (ex. PROCORRESP 90 573/90 573, SOUAMD 10/10) |
| 10 | **données** : pour chaque table, `SELECT toutes-les-colonnes FROM EE.t EXCEPT SELECT … FROM EE_TEST.t` et l'inverse (colonnes `text` converties en `nvarchar(max)`, seules non comparables telles quelles) | SQL dynamique bâti depuis `sys.columns` | 60 tables comparées (10b = 0 table sautée), 84 837/84 837, 0 ligne d'un seul côté |
| Σ | | | `overall_verdict = IDENTICAL, total_differences = 0` |

### 3.1 Contrôle négatif : la comparaison voit-elle vraiment les écarts ? (`04-negative-control.log`)

Trois altérations volontaires dans `EE_TEST` : `UPDATE dbo.CATSTATUS SET LIBELEEN = 'TAMPERED' WHERE UniqueId = 1`,
`DROP INDEX IDX_CLI_ID ON dbo.CLIENTS`, `ALTER FUNCTION [dbo].GetCurrentUserSession() … RETURN 'TAMPERED'`. Résultat :
section 6 → `only in EE|CLIENTS|IDX_CLI_ID` (106 vs 105), section 8 → deux lignes `GetCurrentUserSession` avec deux
SHA-256 différents (et `uses_quoted_identifier` 1 vs 0), section 10 → `CATSTATUS|20|20|1|1|DIFFERENT`,
`overall_verdict = DIFFERENCES FOUND, total_differences = 4`. Puis `EE_TEST` rechargée depuis le fichier → de nouveau
identique (`05-reload-and-recompare.log`, `06-final-generate-load-compare.log`).

Un premier passage du script de comparaison (14:29) avait planté sur 3 sections et 8 tables (`Msg 8155 No column name
was specified`) tout en affichant `IDENTICAL` : le verdict n'était pas fiable. Corrigé (alias sur toutes les colonnes
dérivées) et **un compteur `10b` a été ajouté** : nombre de tables non comparées, qui doit être 0. Les journaux 02, 04,
05, 06 sont postérieurs à la correction et contiennent 0 `Msg `.

### 3.2 Ce qu'il a fallu reproduire fidèlement (et comment)

1. **Sept procédures dont le nom contient un point** (`dbo.sp_SOU_CalculCodeImpr`, `dbo.sp_SOU_CalculProductUsageInAssemblies`,
   `dbo.sp_SOU_CalculQteTotalItem`, `dbo.sp_SOU_UpdateQteTotalEns`, `dbo.sp_SOU_UpdateQteTotalLots`,
   `dbo.sp_SOU_UpdateQteTotalOth`, `dbo.sp_SOUPRO_Quantity`), produites par `V24_UpdateDatabase.SQL` l.6-41
   (`EXEC sp_rename 'dbo.sp_X', 'dbo.sp_SOU_X'`) — déjà relevé dans [[SCHEMA]] §6.1. Leur texte `sys.sql_modules.definition`
   porte toujours l'**ancien** nom (`CREATE PROCEDURE … sp_CalculCodeImpr`), comportement documenté : « Renaming a stored
   procedure, function, view, or trigger won't change the name of the corresponding object either in the definition column
   of the sys.sql_modules catalog view or obtained using the OBJECT_DEFINITION built-in function »
   (`docs/sources/sp-rename-transact-sql.txt` l.149). Le générateur détecte l'écart entre le nom dans l'en-tête `CREATE` et
   `sys.objects.name`, crée le module sous l'ancien nom puis exécute `EXEC sys.sp_rename @objname = N'[dbo].[sp_CalculCodeImpr]',
   @newname = N'dbo.sp_SOU_CalculCodeImpr', @objtype = 'OBJECT'` (`EE_DR.sql` l.252, 271, 325, 381, 407, 433, 459). Résultat :
   même nom, même texte, même SHA-256 (section 8 = 0 différence).
2. **Une procédure référence une colonne supprimée.** `dbo.sp_SOU_CalculProductUsageInAssemblies` (texte
   `sp_CalculProductUsageInAssemblies`, créée par `V21_UpdateDatabase.sql` l.272) fait `UPDATE SOUPRO SET INASSEMBLIE = …`
   (V21 l.306) ; la colonne `SOUPRO.INASSEMBLIE` ajoutée en V21 l.225-238 est supprimée par `V36_UpdateDatabase.sql`
   l.27-40 (`DROP COLUMN INASSEMBLIE`) — [[SCHEMA]] §6.2. Premier essai de chargement (procédures après les tables) :
   `Msg 207, Level 16 … Procedure sp_CalculProductUsageInAssemblies, Line 36 — Invalid column name 'INASSEMBLIE'`, arrêt.
   Cause documentée : « Deferred name resolution can only be used when you reference nonexistent table objects. All other
   objects must exist at the time the stored procedure is created. For example, when you reference an existing table in a
   stored procedure you cannot list nonexistent columns for that table » (`docs/sources/deferred-name-resolution-and-compilation.txt`
   l.42). Solution retenue : **les 160 procédures sont créées avant les 60 tables** (`EE_DR.sql` l.26 puis l.11166) ; aucune
   table n'existant encore, la résolution différée s'applique à toutes et l'état final est celui de `EE` (procédure présente,
   texte identique, inexécutable dans les deux bases). Les 18 fonctions restent après les tables (pas de résolution différée
   pour les fonctions).
3. **Compteurs d'identité.** `sys.identity_columns.last_value` vaut 90 573 pour `PROCORRESP` (84 721 lignes : V16 a supprimé
   des lignes après insertion, [[SCHEMA]] §6.4) et 10, 7, 14, 72, 72, 58, 10 pour sept tables **vides** (`SOUAMD`,
   `SOULOTS`, `SOULOTSCO`, `SOUENSCO`, `ENSCOMPO`, `PRODUITS`, `TAXDEF` : lignes insérées puis effacées par les tests
   antérieurs — `eewin/examples/cleanup_example.sql` l.8-15 efface `TAXDEF`, `PRODUITS`, `ENSCOMPO` via `up_*_Delete`,
   `planexpert_cleanup_S-1714.sql` l.5-10 idem, `soumissions-dr/unload_dr_submissions.sql` l.2-3 passe par
   `up_DeleteSoumis_Full` qui cascade sur `SOUAMD`, `SOUENSCO`, `SOULOTS`, `SOULOTSCO`). Pour une table pleine,
   `DBCC CHECKIDENT (t, RESEED, n)` suffit. Pour une
   table vide qui n'a jamais reçu de ligne, la documentation prévient : « If no rows are inserted into the table since the
   table was created … the first row inserted after you run DBCC CHECKIDENT uses new_reseed_value as the identity. If rows
   are present in the table, or if all rows are removed by using the DELETE statement, the next row inserted uses
   new_reseed_value + the current increment value » (`docs/sources/dbcc-checkident-transact-sql.txt` l.111). Le générateur
   insère donc une ligne jetable portant la valeur `last_value` (`SET IDENTITY_INSERT ON`) puis la supprime par `DELETE`
   (`EE_DR.sql` l.98594-98651). Preuve (`08-identity-next-value-EE_TEST.log`) : dans `EE_TEST`, `INSERT INTO dbo.SOUAMD
   DEFAULT VALUES` → `SCOPE_IDENTITY() = 11` ; `INSERT INTO dbo.PROCORRESP …` → `90574`. Exactement ce que donnerait `EE`.
4. **Littéraux et `sqlcmd`.** `sqlcmd` « recognizes commands only if they appear at the start of a line »
   (`sqlcmd-commands.txt` l.99) et `GO` seul sur une ligne termine un lot (l.253), même à l'intérieur d'une chaîne : le
   générateur vérifie chaque module (0 cas) et coupe toute chaîne de données dont une ligne commencerait par `:` ou serait
   `GO` (0 cas dans `EE`, mais le code le gère). Toutes les chaînes sont émises en `N'…'` ; les `float` avec `repr()` Python
   (chaîne la plus courte qui redonne exactement le même double IEEE-754) ; les `datetime` en `'AAAA-MM-JJThh:mm:ss.mmm'`.
   La section 10 (EXCEPT exact sur toutes les colonnes, dont 237 `float` et 93 `datetime`) prouve qu'aucune valeur n'a bougé.

### 3.3 Incident pendant la vérification, et ce qu'il révèle

Le test moteur (`03-engine-EE_TEST.log`, 14:30) a été rejoué **dans `EE` aussi** pour comparer les chiffres. Or
`sp_SOU_CalculTotaux` écrit `SOUMIS.AUTTAXAB1..5` (S-1844) et `MATTAXAB1..5` (1400-INDUSTRIEL) : ces 10 colonnes sont
passées de `NULL` à `0.0` dans `EE` après la génération de 14:24. La re-comparaison de 14:32 (`05-reload-and-recompare.log`)
a donc trouvé `SOUMIS|2|2|2|2|DIFFERENT` : le générateur n'était pas en cause, la source avait changé. `EE_DR.sql` a été
régénéré depuis l'état courant d'`EE` à 14:33 (`06-final-generate-load-compare.log` montre le `diff` entre les deux
versions : exactement les 2 lignes `INSERT` de `SOUMIS`), `EE_TEST` rechargée, comparaison → `IDENTICAL`. Le constat
« le SQL n'écrit pas les totaux SOUMIS, seulement *TAXAB1..5 » de [[SOUMISSIONS-DR]] §4 est ainsi reconfirmé par un
effet de bord observé.

## 4. Déterminisme (`07-determinism.log`)

Re-scripter `EE` puis re-scripter `EE_TEST` avec le même générateur :

```
$ diff eewin/EE_DR.sql EE_again.sql        → seule la ligne 2 (-- Generated <horodatage>) diffère
$ diff eewin/EE_DR.sql EE_TEST_again.sql   → seules les lignes 2 et 3 (-- Generated, -- Source database: EE_TEST) diffèrent
SHA-256 des trois fichiers sans ces 2 lignes d'en-tête : 9b538eb1108b15d120c4f820b660548055a10d7b3f3483407856dfd24773695f (×3)
```

Le fichier produit depuis la copie est donc octet pour octet le fichier produit depuis l'original : la boucle
`EE → EE_DR.sql → EE_TEST → EE_DR.sql` est fermée.

## 5. Moteur officiel dans la copie (`03-engine-EE_TEST.log`)

Mêmes appels que `eewin/soumissions-dr/load_dr_submissions.sql` §1.5 et §2.4
(`EXEC dbo.sp_SOU_CalculTotaux @SOU_ID = 'S-1844', @TypeReleve = 'O', @EE_CALGARY = 0, @ModeCalcul = 'C',
@VendantUAvantVendantT = 1, @VPM = 2, @DoLog = 0` et `@SOU_ID = '1400-INDUSTRIEL', @TypeReleve = 'P'`), dans `EE` puis
dans `EE_TEST` :

| Base | S-1844 `fCoutantTotal` / `fVendantTotal` | 1400-INDUSTRIEL `fCoutantTotal` / `fVendantTotal` | `SOUPRO.UnitSelling` |
|---|---|---|---|
| EE | 238744.000000 / 238744.000000 | 96298.360000 / 96298.360000 | 96298.360000000001 |
| EE_TEST | 238744.000000 / 238744.000000 | 96298.360000 / 96298.360000 | 96298.360000000001 |

(`fCoutantTotalPortionTVP = −238744` / `−96298.36` des deux côtés : c'est l'anomalie « sans TAXDEF, portion TVP = −vendant »
déjà décrite dans [[SOUMISSIONS-DR]] §4, reproduite à l'identique.)

## 6. Limites honnêtes

- La copie est fidèle **au niveau des vues catalogue et des données** ; ne sont pas reproduits (absents ou sans objet dans `EE`) :
  permissions, utilisateurs de base, propriétés étendues (0), séquences (0), types utilisateur (0), déclencheurs (0), vues (0),
  synonymes (0), fichiers/groupes de fichiers (un seul `PRIMARY`), options de base autres que la collation (les valeurs
  `is_ansi_nulls_on = 0`, `is_quoted_identifier_on = 0`, `compatibility_level = 160`, `FULL` sont celles d'une base créée
  par `CREATE DATABASE` par défaut sur cette instance, section 1 de la comparaison).
- Les 59 défauts nommés par le système (`DF__TABLE__COL__xxxx`) reçoivent un nouveau nom aléatoire dans la copie ; la
  comparaison (section 7) porte sur table + colonne + définition, et sur le nom seulement pour les 2 défauts nommés par
  l'utilisateur (`DF_BDEE_LVERSION`, `DF_BDEE_KVERSION`).
- `sys.sql_expression_dependencies` n'est pas comparé : l'ordre de création (procédures avant tables) fait que davantage de
  références y sont enregistrées comme non résolues au départ ; SQL Server les résout à la première exécution.
- Le test d'identité (§3.2.3) a incrémenté les compteurs de `SOUAMD` et `PROCORRESP` dans `EE_TEST` (une transaction
  annulée ne rembobine pas une identité) : `EE_TEST` n'est plus strictement identique à `EE` après ce dernier test.
  `EE_TEST` est une base jetable ; la recréer prend 25 s (§2).
- `EE_DR.sql` photographie `EE` **au 2026-09-27 14:33 EDT**. Toute écriture ultérieure dans `EE` (y compris un simple
  `EXEC sp_SOU_CalculTotaux`, §3.3) impose de régénérer : `python eewin/tools/generate_ee_dr_sql.py --password '…' --database EE
  --output eewin/EE_DR.sql`, puis §2 et §3.

## 7. Fichiers

| Fichier | Rôle |
|---|---|
| `eewin/EE_DR.sql` | le livrable : schéma + 178 modules + 84 837 lignes + compteurs d'identité |
| `eewin/tools/generate_ee_dr_sql.py` | générateur (Python 3.11, `pymssql`) |
| `eewin/tools/compare_ee_databases.sql` | comparaison de deux bases d'une même instance (`-v SRC=… DST=…`) |
| `eewin/verification/00-mssql-scripter-attempt.log`, `00-mssql-scripter-sqltoolsservice.log` | échec de mssql-scripter, commandes et journal .NET |
| `eewin/verification/01-load-EE_TEST.log` | création d'`EE_TEST` + chargement (sortie intégrale, exit 0) |
| `eewin/verification/02-compare-EE-vs-EE_TEST.log` | comparaison complète → `IDENTICAL` |
| `eewin/verification/03-engine-EE_TEST.log` | `sp_SOU_CalculTotaux` dans `EE` et `EE_TEST` |
| `eewin/verification/04-negative-control.log` (+ `.full.log`) | 3 altérations volontaires détectées |
| `eewin/verification/05-reload-and-recompare.log`, `06-final-generate-load-compare.log` | incident §3.3 et régénération finale |
| `eewin/verification/07-determinism.log` | même fichier depuis `EE` et depuis `EE_TEST` |
| `eewin/verification/08-identity-next-value-EE_TEST.log` | prochaine identité 11 / 90 574 |
| `eewin/docs/sources/` | texte intégral des pages officielles citées (Microsoft Learn, PyPI) + `SOURCES.txt` (URL, date, SHA-256) |
