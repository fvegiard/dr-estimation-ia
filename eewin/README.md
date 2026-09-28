# `eewin/` — la base SQL Server d'EEWin (Dupuis), rebâtie, documentée, rechargeable en un fichier

EEWin est le logiciel d'estimation (Delphi + SQL Server) dont Dupuis fournit les scripts de base de données. Ce dossier
contient les 52 scripts officiels, la base `EE` rebâtie à partir d'eux dans un conteneur SQL Server 2022, six documents qui
expliquent ce que la base contient et comment elle calcule, les deux soumissions chiffrées de DR chargées dedans, et
**un seul fichier `EE_DR.sql` qui recrée le tout à l'identique** (preuve dans [docs/VERIFICATION.md](docs/VERIFICATION.md)).

Règle du dossier : rien n'est inventé. Chaque affirmation des documents cite une table/colonne, une procédure (avec le
numéro de ligne de son `OBJECT_DEFINITION`) ou une ligne de script ; chaque chiffre a été rejoué sur la base vivante et
la sortie réelle est conservée à côté (`examples/*.log`, `soumissions-dr/preuves/`, `verification/`).

## Le livrable : `EE_DR.sql`

| | |
|---|---|
| Contenu | 60 tables (1 061 colonnes, 45 clés primaires, 61 index, 61 défauts), 160 procédures, 18 fonctions, 84 837 lignes de données (catalogue de correspondance `PROCORRESP` 84 721, unités, statuts, et les soumissions DR S-1844 et 1400-INDUSTRIEL), 17 compteurs d'identité alignés |
| Taille | 8 080 854 octets, 98 655 lignes, UTF-8, 441 lots `GO` |
| SHA-256 | `d8aacb160d88e75aa2db7f2d805f0e59223ff7661a6fb83e58ad25939d0a46e2` (état d'`EE` au 2026-09-27 14:33 EDT) |
| Généré par | `tools/generate_ee_dr_sql.py` (Python 3.11 + `pymssql`), depuis les vues catalogue de la base vivante — jamais à la main |
| Vérifié par | `tools/compare_ee_databases.sql` : base source et base rechargée comparées objet par objet et **ligne par ligne** → `IDENTICAL`, 0 différence |

### Recharger la base (25 secondes)

Dans une instance SQL Server (testé uniquement sur 2022 RTM-CU27, 16.0.4295.3), la base cible doit exister, être **vide**
et avoir la collation `French_CI_AS` — le fichier refuse sinon (garde en tête de fichier, `RAISERROR` 16).

```bash
# 1. base cible vide, bonne collation
sqlcmd -S <serveur> -U sa -P '<mdp>' -C -Q "CREATE DATABASE EE_DR COLLATE French_CI_AS"
# 2. chargement : -f 65001 (UTF-8), -x (pas de substitution $(var)), -b (arrêt à la première erreur), -I (QUOTED_IDENTIFIER ON)
sqlcmd -S <serveur> -U sa -P '<mdp>' -C -d EE_DR -f 65001 -x -b -I -i eewin/EE_DR.sql
# attendu : 0 ligne "Msg", messages informatifs "depends on the missing object" (ordre de création) et 7 "Caution" (sp_rename), puis
# EE_DR.sql applied to EE_DR
```

Avec le conteneur de ce projet (`eewin`, image `mcr.microsoft.com/mssql/server:2022-latest`, port 1433) :

```bash
docker cp eewin/EE_DR.sql eewin:/tmp/EE_DR.sql
docker exec eewin /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<mdp>' -C -Q "CREATE DATABASE EE_DR COLLATE French_CI_AS"
docker exec eewin /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<mdp>' -C -d EE_DR -f 65001 -x -b -I -i /tmp/EE_DR.sql
```

Vérifier qu'une base rechargée est identique à une base de référence présente sur la même instance :

```bash
sqlcmd -S <serveur> -U sa -P '<mdp>' -C -W -s '|' -v SRC=EE DST=EE_DR -i eewin/tools/compare_ee_databases.sql
# dernière ligne attendue : IDENTICAL|0
```

Régénérer `EE_DR.sql` après toute écriture dans la base source (même un simple `EXEC sp_SOU_CalculTotaux` écrit dans
`SOUMIS`, voir VERIFICATION §3.3) :

```bash
python3 -m venv .venv && .venv/bin/pip install pymssql
.venv/bin/python eewin/tools/generate_ee_dr_sql.py --server localhost --port 1433 --user sa --password '<mdp>' --database EE --output eewin/EE_DR.sql
```

Le fichier est déterministe : deux générations depuis la même base ne diffèrent que par la ligne d'horodatage
(`verification/07-determinism.log`).

### Alternative : les 52 scripts d'origine

`scripts/` contient les scripts officiels (SHA-256 dans `SHA256SUMS`) et `run.sh` les rejoue dans l'ordre
`CreateTables → CreateScripts → CreateData → Central_* → V0 → UpdateDatabase → V3…V45` (`run.log` : 0 erreur). C'est ainsi
qu'`EE` a été bâtie ; `EE_DR.sql` en est la photographie après chargement des soumissions DR. Différence pratique : les
scripts d'origine sont en Windows-1252 (`sqlcmd -f 1252`) et créent une base **sans aucune soumission** ; `EE_DR.sql` est
en UTF-8 et contient les lignes DR.

## Les documents (`docs/`)

| Document | Question à laquelle il répond | À retenir |
|---|---|---|
| [SCHEMA.md](docs/SCHEMA.md) (2 423 lignes) | Qu'y a-t-il dans la base ? | 60 tables décrites colonne par colonne par domaine (catalogue, ensembles, soumissions, factures, commandes, clients/taux/taxes, système). **0 clé étrangère, 0 CHECK, 0 déclencheur, 0 vue** : toute l'intégrité est dans le code. ERD déduit des jointures des procédures. §5 inventaire et graphe d'appel des 178 routines. §6 anomalies prouvées : 7 procédures nommées littéralement `dbo.sp_SOU_…` (effet de `sp_rename` dans V24), 2 procédures qui référencent la colonne supprimée `INASSEMBLIE`, tranche de taxe 6 jamais alimentée, écart 90 573 → 84 721 lignes `PROCORRESP` expliqué. Annexe B : historique des colonnes ajoutées script par script. |
| [CALCUL-SOUMISSION.md](docs/CALCUL-SOUMISSION.md) (510 lignes) | Comment une soumission est-elle calculée ? | Seuls 2 modules font l'arithmétique coût/vendant/taxe : `sp_SOU_CalculTotaux` et `sp_FAC_CalculTotaux`. Étapes : coût net unitaire d'un produit → coût d'un ensemble (`TYPEITEM='A'`) → coût d'un lot (`'L'`) → conversion d'unités (`fn_UM_GetRatioDeConversion`) → coûtant/vendant/TVP d'une ligne de relevé → quantités à commander (`sp_SOUPRO_Quantity_V2`). §9 exemple numérique exécuté (`examples/worked_example.sql/.log`), §10 formules résumées pour ré-implémentation, §11 pièges confirmés par exécution (`@REPLACE_FILTER=0` → Msg 16916, `CODEIMPR <> ''` → Msg 2812, etc.). |
| [CATALOGUE-ET-LIEN-QPL.md](docs/CATALOGUE-ET-LIEN-QPL.md) (325 lignes) | D'où viennent les prix et les temps, et comment les `ENS…` des QPL se rattachent-ils à la base ? | `PRODUITS` (39 colonnes, 3 clés, 2 prix, 1 temps) ; chaîne `PriceUpdate_*` : pour Rexel/Sonepar (donc Lumen = DR) la liste distributeur **n'apporte aucun prix** ; les temps de main-d'œuvre ne viennent jamais du distributeur (`PRODUITS.TEMPUNI`, `ENSEMBLE.TEMPUNI/TEMPSEC` = propriété de DR). `PROCORRESP` (84 721 lignes) = table de correspondance entre catalogues. Les `ENS…` du QPL sont des `ENSEMBLE.ENS_ID`, `19PE0.75 #12` une `CLEPERS`. Pour chiffrer un QPL il faut un export `ENSEMBLE`/`ENSCOMPO`/`PRODUITS` de la base vivante de DR. |
| [PLAN-EXPERT-VERS-EEWIN.md](docs/PLAN-EXPERT-VERS-EEWIN.md) (296 lignes) | Qu'est-ce qu'un relevé `.qpl` alimente dans la base ? | **Aucun objet SQL ne lit un `.qpl`** : c'est l'application Delphi qui écrit dans `SOU*` via `up_<TABLE>_Update`. Le QPL n'apporte qu'un `ItemID`/`ItemType` par groupe et des quantités (compteurs, tracés) ; prix, temps, composition viennent du catalogue. Chaîne prouvée sur la base vivante : `GroupID` → `SOUREL` → `SOUENS` → `SOUENSCO` → `SOUPRO.QTEENS` → `sp_SOU_CalculTotaux` (`examples/planexpert_import_S-1714.sql/.log`, `S-1844`). 128 des 129 groupes de S-1714 n'ont pas d'`EEExchangeData` : rien en EE ne peut les chiffrer. |
| [SOUMISSIONS-DR.md](docs/SOUMISSIONS-DR.md) (119 lignes) | Quels chiffres réels de DR sont dans la base, et d'où viennent-ils ? | 4 courriels de Daniel Dupuis lus ; 2 chiffres exploitables : S-1844 forfait **238 744,00 $** (PDF LC 2000 / SAQ) et cotation Siemens **96 298,36 $** pour un switchboard SB2 (1400 Industriel, Laprairie). Chargés uniquement par les procédures officielles (`soumissions-dr/load_dr_submissions.sql`), moteur rejoué (mêmes totaux), cycle unload→load rejoué. S-1857 (17,5 Mo) non extractible par le connecteur ; LABOMAR = formulaire vierge. Constats moteur : 2 jeux de résultats avec `@DoLog=1`, le SQL n'écrit que `*TAXAB1..5` dans `SOUMIS`, `TAXDEF` vide → portion TVP négative. |
| [VERIFICATION.md](docs/VERIFICATION.md) | `EE_DR.sql` recrée-t-il vraiment la base ? | Choix de l'outil (mssql-scripter essayé et prouvé inutilisable contre SQL Server 2022 ; sqlpackage écarté sur documentation ; générateur Python retenu), création d'`EE_TEST` depuis le seul fichier, comparaison en 10 sections → `IDENTICAL`, contrôle négatif (3 altérations détectées), moteur rejoué dans la copie, déterminisme, prochaine valeur d'identité. Sources officielles citées ligne par ligne, texte intégral dans `docs/sources/`. |

## Arborescence

```
eewin/
├── EE_DR.sql                    le livrable (schéma + modules + données)
├── README.md                    ce fichier
├── SHA256SUMS                   empreintes des 52 scripts officiels
├── run.sh, run.log              rejeu des 52 scripts (0 erreur)
├── scripts/                     les 52 scripts officiels de Dupuis (Windows-1252)
├── docs/                        les 6 documents + sources/ (textes officiels cités, URL + SHA-256 + date)
├── examples/                    requêtes rejouables et leurs sorties (.sql + .log) citées par les documents
├── soumissions-dr/              textes des courriels/PDF, lignes.csv, load/unload/verify .sql, preuves/
├── tools/                       generate_ee_dr_sql.py, compare_ee_databases.sql
└── verification/                journaux bruts 00 → 08 de la vérification d'EE_DR.sql
```

## Conventions

- Documents, journaux et commentaires destinés à Francis en français ; code, noms de fichiers/variables et messages de
  commit en anglais (décision du 2026-09-24).
- Une base « vivante » = la base `EE` du conteneur `eewin` ; « prouvé » = exécuté sur cette base avec la sortie conservée ;
  `[non vérifié]` marque explicitement ce qui n'a pas pu être prouvé.
- Dates et heures en heure de l'Est (America/Toronto).
