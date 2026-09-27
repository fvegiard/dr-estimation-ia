# Plan Expert → EEWin : ce qu'un relevé `.qpl` alimente dans la base EE

Sources : base `EE` reconstruite à partir des 52 scripts officiels de Dupuis (`eewin/scripts/`, 0 erreur : 60 tables,
160 procédures, 18 fonctions — 177 modules lus dans `sys.sql_modules`) ; QPL de référence
`/home/claude/data/dossiers/S-1714/reference/S-1714-Dupuis-PlanExpert.qpl` (775 524 octets, XML UTF-8 BOM, CRLF) et
`S-1844-Dupuis-PlanExpert.qpl` ; recensement `ensembles-ee.csv` (132 `ItemID` trouvés dans les 510 QPL analysables du corpus
Dupuis 2021-2026). Preuve exécutée : `eewin/examples/qpl_to_eewin_sql.py` → `planexpert_import_S-1714.sql` /
`.log` et `planexpert_import_S-1844.sql` / `.log` (section 6).

Convention de citation : `proc l. N` = ligne N du texte `OBJECT_DEFINITION` (obtenu par
`STRING_SPLIT(OBJECT_DEFINITION(OBJECT_ID('proc')), CHAR(10), 1)`, `ordinal` = N) ; `script:N` = ligne N du fichier
`eewin/scripts/<script>` ; `qpl:N` = ligne N du fichier `.qpl`. Les compléments de calcul (formules de coût, de vente, de
main-d'œuvre) sont dans [[CALCUL-SOUMISSION]] ; le dictionnaire des colonnes dans [[SCHEMA]].

---

## 0. Résumé

- **Aucun objet SQL de EE ne lit un `.qpl`.** Les 52 scripts et les 177 modules ne contiennent ni `EEExchange`, ni `Quoter`,
  ni `Plan`, ni `import`/`export`, ni XML (seule exception : `fn_STR_Alphaorder` l. 27 utilise `CAST(... AS XML)` pour
  découper une chaîne). L'échange est fait par l'application EEWin (Delphi) qui écrit dans les tables `SOU*` par les
  procédures `up_<TABLE>_Update`.
- Ce que le QPL apporte à EE tient dans **un seul nœud par groupe** : `<Group GroupID="129"><EEExchangeData ItemType="A"
  ItemID="ENSCFFFDBD5146159B90" Key="19PE0.75 #12" PersonalKey="19PE0.75 #12" Name=… Description=…/>` (qpl:29-30) ; les
  compteurs et tracés qui portent ce `GroupID` donnent la **quantité** ; tout le reste (prix, temps, composition) vient du
  catalogue EE (`ENSEMBLE`/`ENSCOMPO`/`PRODUITS`), jamais du QPL (129 `<Price>` à `CostEach="0"` dans S-1714, 0 prix non nul
  dans les 27 QPL locaux ni dans les 510 du corpus).
- Chaîne de données prouvée sur la base vivante : `Counter/Line GroupID` → `SOUREL` (`EXT_ID` = GroupID, `TYPEITEM` =
  `ItemType`, `ITEM_ID` = `ItemID`, `QTE` = compte ou longueur) → `SOUENS.ENS_ID` = `ITEM_ID` (copie de `ENSEMBLE`) →
  `SOUENSCO` (copie de `ENSCOMPO`) → `SOUPRO.QTEENS` (`sp_SOU_UpdateQteTotalEns_v2` l. 13-66) → `sp_SOU_CalculTotaux`
  (l. 215-287 pour un `A`).
- Les colonnes qui portent la trace d'un logiciel externe existent depuis la version V6 du schéma (2014-08-12) :
  `SOUMIS.EXTAPP char(1)`, `SOUMIS.EXTFILE varchar(200)`, `SOUMIS.ORIGIN char(1)`, `SOUMIS.ORIGINREF varchar(200)`,
  `SOUREL.EXT_ID varchar(20)`, `SOUENS.ENS_ORG_ID varchar(20)` (V6_UpdateDatabase.sql:794-800, 1350-1353, 690-693). Elles
  sont **écrites** par `up_SOUMIS_Update`, `up_SOUREL_Update`, `up_SOUENS_Update` et **jamais lues** par un calcul ; la
  seule valeur posée en SQL est `ORIGIN='C'` (copier-coller, `up_CopySoumis_Full` l. 32). La valeur de `EXTAPP` que EEWin
  écrit pour Plan Expert n'est dans aucun script : **non prouvée**.
- Ce que le QPL **ne peut pas** alimenter : les groupes sans `EEExchangeData` (128 des 129 groupes de S-1714, 64 des 66 de
  S-1844 : « exit », « PRISE DEPLACER », « PVC 1po »…) n'ont pas d'`ITEM_ID`, donc rien en EE ne peut les chiffrer ; les
  longueurs sont en pixels (`Scale Value="0,09375" Type="1"`, qpl:7244 — sémantique non documentée dans le fichier) ;
  `SECTION`, `PROFIT`, `TYPETAXE`, `BLO_ID`/`DIV_ID` et la main-d'œuvre ne viennent pas du QPL.

---

## 1. Ce qui a été cherché et ce qui a été trouvé

| Recherche (insensible à la casse) | Dans les 52 scripts | Dans les 177 `OBJECT_DEFINITION` | Conclusion |
|---|---|---|---|
| `EEExchange`, `Quoter`, `PlanExpert`, `Plan Expert`, `Takeoff`, `Counter`, `GroupID` | 0 ligne | 0 ligne | le vocabulaire du QPL n'existe pas côté SQL |
| `\bplan` | 0 ligne (hors `UMPLAN`) | `UMPLAN` seulement (`up_SOUMIS_Update`, `up_FACTURES_Update`) | `SOUMIS.UMPLAN varchar(2)` (CreateTables.sql:805) = unité de mesure « du plan » ; jamais lue par un calcul |
| `import`, `export`, `xml` | 0 | `fn_STR_Alphaorder` l. 27 (`CAST(... AS XML)` pour découper une liste) | pas d'import/export SQL |
| `relev` | — | `TYPERELEVE`/`@TypeReleve` : `fn_GetProductComposition*`, `sp_SOUPRO_Quantity*`, `sp_SOU_CalculTotaux`, `sp_*_Del_UnusedProd`, `up_*REL_Update`, `up_CopySou*` | « relevé » = les lignes `SOUREL` (`TYPERELEVE` `P` matériel, `S` service, `O` autre, `U` prix unitaires) |
| `web`, `transfer`, `exchange` | `SOUWEBLOG`/`FACWEBLOG` (CreateTables.sql:878, 466), `_TransferCompleted` (999), `BDEE.SRCHWEBURL` (V18:21) | `up_SOUWEBLOG_Update` (CreateScripts.sql:3778) | `SOUWEBLOG (SOU_ID, WEB_ID varchar(15), TRF_DATE varchar(25), RESULT varchar(10), MESSAGE varchar(60))` = journal d'un transfert **web** (`--WEXPORTED = 0, -- EM : Pour la version Interne`, V25:33), sans rapport avec Plan Expert |
| `EXT_ID`, `EXTAPP`, `EXTFILE`, `ORIGIN`, `ENS_ORG_ID` | ajoutés V6 (2014-08-12), reportés V11, V20, V23, V24 | `up_SOUMIS_Update` l. 6-9, `up_SOUREL_Update` l. 8, `up_SOUENS_Update` l. 7, `up_FACTURES_Update`, `up_FACREL_Update`, `up_FACENS_Update`, `up_CopySoumis_Full` l. 32-33, `up_CopyFactures_Full` | **les seules colonnes « externes »** du schéma (section 3) |
| Copie catalogue → soumission (`FROM ENSEMBLE`, `FROM ENSCOMPO`, `FROM PRODUITS` vers `SOU*`) | — | aucune : `ENSEMBLE`/`ENSCOMPO` n'apparaissent que dans `up_ENSEMBLE_*`, `up_ENSCOMPO_*` ; `PRODUITS` dans `upbi_ProductsPrefered_*` et `up_PriceUpdate_*` | la copie `ENSEMBLE→SOUENS`, `ENSCOMPO→SOUENSCO`, `PRODUITS→SOUPRO` est faite par l'application (les seules `INSERT INTO SOUENS/SOUPRO` sont `up_SOUENS_Update`, `up_SOUPRO_Update` et `up_CopySouBlocDiv` l. 89-118 qui copie **de `SOUENS` à `SOUENS`** entre deux soumissions) |

Preuve d'origine du schéma V6 : en-tête « Script created by SQL Compare version 6.2.1 … Run this script on
D00106\EEWIN.EEWin_3_126 to make it the same as D00106\EEWIN.EEWin_3_128 » (V6_UpdateDatabase.sql:1-4), commentaires
`-- 2014-07-31 EMadore V6 - Ajout` sur `@ORIGIN`, `@ORIGINREF`, `@EXTAPP`, `@EXTFILE` (`up_SOUMIS_Update` l. 6-9) et
`-- 2014-08-12 EMadore V6 : New` sur `@ENS_ORG_ID` (`up_SOUENS_Update` l. 7).

---

## 2. Anatomie d'un QPL (S-1714, 8 503 marques)

Racine `QuoterPlanSession` (qpl:2). Comptes obtenus par `xml.etree` sur le fichier :

| Chemin | Nb | Attributs | Rôle pour EE |
|---|---|---|---|
| `Project` | 1 | `Name="S-1714 PARTAGE DE RIVIERA"` ; enfants `Description, ContactName, ContactInfo, JobNumber, Comment, CreationDate=2026/3/20, LastModified=2026/3/27, DisplayResultsForAllPlans` | → `SOUMIS.DESCDOC varchar(200)` (convention) |
| `Workspace/ActivePlan`, `RecentPlans/Plan` | 1 + 10 | `Name` | aucun |
| `Plans/Group` | **1** | `GroupID="129"` (qpl:29) | le seul pont vers EE |
| `Plans/Group/EEExchangeData` | **1** | `ItemType="A" ItemID="ENSCFFFDBD5146159B90" Name="conduit 3/4 03c12" Key="19PE0.75 #12" PersonalKey="19PE0.75 #12" Description="conduit 3/4 03c12"` (qpl:30) | section 3 |
| `Plans/Plan` | 52 | `Name`, `FileName` (PNG) ; enfants `Thumbnail`, `Scale`, `Bookmarks/Bookmark`, `Comment`, `Layers` | feuille → `SOUBLO.BLO_ID` (convention, section 3) |
| `Plan/Scale` | 52 | `Value` (`0` sur 51 feuilles, `0,09375` sur « 01-PLANS - 23 2 », qpl:7244), `Type="1"`, `Precision="2"`, `SetManually`, `Engineering` | conversion pixel → unité : **non documentée** dans le fichier |
| `Plan/Layers/Layer` | 208 (4 par feuille) | `Index 0-3`, `Name`, `Opacity`, `Visible`, `Active` | calque → `SOUDIV.DIV_ID` (convention) |
| `Layer/Legend` | 52 | position, `ShowMeasure="True"` | aucun |
| `Layer/Counter` | **462** | `Name`, `GroupID`, `Shape`, `DefaultSize`, `Text`, couleurs, `ShowMeasure`, `Visible` ; enfants `Element X Y Width Height` × **8 503** | 1 `Element` = 1 marque → `SOUREL.QTE` (compte) |
| `Layer/Line` | **54** | `Name`, `GroupID`, `Color`, `PenWidth`, `PenType`, `ShowMeasure`, `Visible` ; enfants `Element X1 Y1 X2 Y2` × **1 825** | Σ longueurs de segments (pixels) → `SOUREL.QTE` |
| `Layer/Area` | 4 | `Name`, `GroupID`, `Pattern`… ; `Element/Point X Y` × 84 | surface (pixels²) |
| `Layer/Rectangle` | 6 | géométrie seulement, **pas de `GroupID`** | aucun |
| `Prices/Price` | **129** | `Key="<GroupID>;;<Counter|Line|Area>;"`, `CostEach="0"`, `MarkupEach="0"`, `SystemType="2"` (qpl:12491-12621) | 129 = 93 `Counter` + 32 `Line` + 4 `Area` = exactement l'ensemble des `GroupID` dessinés ; **0 prix** |
| `Reports/Report/Property` | 16 | `ShowProjectInfo`, `Estimating*`, `Quote*`, `OrderBy*Filter`, `ReportSortBy`, `QuoteReportSortBy` | Plan Expert a des rapports « Estimating » et « Quote », mais leurs montants ne sont pas dans le fichier |

Constantes vérifiées sur les 27 QPL locaux (5 de Dupuis en `reference/`, 22 produits par la chaîne IA dans `planexpert/` et `export-natif/`) : `SystemType="2"`
partout, `CostEach` et `MarkupEach` = `0` partout, `GroupID` ↔ `Name` en bijection (aucun `GroupID` avec deux noms), et la
clé `Prices/Price/@Key` commence toujours par le `GroupID`. Seuls **2 QPL** portent un `EEExchangeData` : S-1714 (1 groupe),
S-1844 (2 groupes, qpl 64 et 65 : `ENSAFF5D05713B179C81 "conduit 3/4 07c12" Key="19PE0.75 #12"` et `ENS9E93142F911561EE1
"conduit 2 33c12" Key="19PE2 #12"`) — et tous les objets liés sont des `Line` (conduits). Les 22 QPL produits par notre
chaîne n'ont **aucun** `Group`.

Le groupe 129 de S-1714 est un `Line Name="conduit 3/4 03c12" GroupID="129"` (qpl:7445) sur la feuille n° 24 « 01-PLANS -
23 2 » (`FileName="01-PLANS - 23 (2).png"`, qpl:7242), calque `Index="0"` (qpl:7250) : **83 segments, 39 083 px** de
longueur cumulée (Σ √((X2-X1)²+(Y2-Y1)²)).

---

## 3. Correspondance QPL → EE (niveau de preuve indiqué)

Niveaux : **code** = une procédure lit/écrit la valeur avec ce sens ; **schéma** = type, longueur, nom et historique de
migration concordent, aucune procédure ne le prouve ; **convention** = choix d'implémentation de notre chaîne, à valider
avec l'export de la base vivante de DR ou avec Dupuis.

| QPL | Colonne EE | Preuve | Détail |
|---|---|---|---|
| `EEExchangeData/@ItemType` = `A` | `SOUREL.TYPEITEM varchar(1)` = `'A'` | **code** | `sp_SOU_CalculTotaux` l. 215 `IF (@TypeReleve = 'P') AND (@TypeItem = 'A')` ; `sp_SOU_UpdateQteTotalEns_v2` l. 52 `AND SR.TYPEITEM = 'A'` ; `up_CopySouBlocDiv` l. 80 |
| `EEExchangeData/@ItemType` = `P` | `SOUREL.TYPEITEM` = `'P'` | **code** | `sp_SOU_CalculTotaux` l. 189 `(@TypeItem = 'P') OR (@TypeItem = 'N')` ; `sp_SOU_UpdateQteTotalOth_v2` l. 29 |
| `EEExchangeData/@ItemID` = `ENS…` (20 car.) | `SOUREL.ITEM_ID varchar(20)` = `SOUENS.ENS_ID varchar(20)` (copie de `ENSEMBLE.ENS_ID`, CreateTables.sql:154) | **code** (jointure) + **schéma** (longueur) | `sp_SOU_UpdateQteTotalEns_v2` l. 53 `AND SR.ITEM_ID = CMP1.ENS_ID`, l. 114 `AND SR.ITEM_ID = SE.ENS_ID` ; `sp_SOU_CalculTotaux` l. 266 `and SE.ENS_ID = @ITEM_ID` ; `up_CopySouBlocDiv` l. 74 `ITEM_ID AS ENS_ID` ; 116/116 `A` du recensement font 20 caractères et commencent par `ENS` |
| `EEExchangeData/@ItemID` = `LQE008445` (9 car.) | `SOUREL.ITEM_ID` = `SOUPRO.PRO_ID varchar(20)` (copie de `PRODUITS.PRO_ID`) | **code** (jointure) + **schéma** (préfixe) | `sp_SOU_UpdateQteTotalOth_v2` l. 34 `WHERE SP.PRO_ID = SR2.ITEM_ID_cmp` ; préfixe de division `LQE` reconnu par `up_PriceUpdate_UpdateProducts` l. 69 `LEFT(PRODUITS.PRO_ID, 3) NOT IN (… 'LQE' …)` et présent dans `PROCORRESP.NEWDIV` (46 857 lignes `NEWDIV='LQE'` sur 90 573) ; 16/16 `P` du recensement font 9 caractères `LQE` |
| `@Key` / `@PersonalKey` (`19PE0.75 #12`, ≤ 20 car. sur les 132) | `ENSEMBLE.CLEPERS varchar(20)` → copié dans `SOUENS.CLEPERS varchar(40)` ; pour un `P` : `PRODUITS.CLEMANU varchar(30)` (`IBE52171K`) | **schéma** | index `IDX_CLEPERS` sur `ENSEMBLE` ; aucune procédure ne lit `CLEPERS` pour chercher un ensemble (les seules lectures sont la copie `up_CopySouBlocDiv` l. 93-98 et `PRODUITS.CLEPERS` dans `upbi_ProductsPrefered_*`) |
| `@Name` / `@Description` (≤ 42 car. sur les 132) | `ENSEMBLE.[DESC] varchar(60)` → `SOUENS.[DESC]` ; `Counter/@Name` → `SOUREL.DESCR varchar(60)` | **schéma** | `up_SOUREL_Update` l. 12 `@DESCR varchar(60)` |
| `Group/@GroupID` (`129`) | `SOUREL.EXT_ID varchar(20)` | **schéma** (V6, même livraison que `EXTAPP`/`EXTFILE`) | ajouté V6_UpdateDatabase.sql:1350-1353, paramètre `up_SOUREL_Update` l. 8 ; **jamais lu** par une procédure ; que EEWin y écrive le `GroupID` ou la clé `129;;Line;` n'est pas prouvé |
| `count(Counter/Element)` | `SOUREL.QTE float`, `SOUREL.QTEUM = 'U'` | **code** (usage de QTE) | `sp_SOU_UpdateQteTotalOth_v2` l. 26 `SUM(SR.QTE * dbo.fn_MultBlock(...))` ; `sp_SOU_UpdateQteTotalEns_v2` l. 27 `… * SR.QTE` ; `sp_SOU_CalculTotaux` l. 152 `ISNULL(SR.QTE,0.0)` |
| `Σ longueur(Line/Element)` × facteur d'échelle | `SOUREL.QTE`, `SOUREL.QTEUM = SOUMIS.UMPLAN` (`F`, `M`… — `Sys_Units.CodeEN`, 19 unités, `Type='L'` pour `M, HM, KM, F, CF, KF`) | **schéma** (unité) ; **facteur non prouvé** | `fn_UM_GetRatioDeConversion(SR.QTEUM, CMP1.COUUM, 0)` (Ens_v2 l. 27) exige une unité de longueur compatible avec `ENSEMBLE.COUUM` ; sinon ratio 0 → quantité 0 sans erreur ([[CALCUL-SOUMISSION]] §6) |
| `Plan` (feuille) | `SOUBLO.BLO_ID varchar(3)` (+ `SOUREL.BLO_ID`) | **convention** | `fn_MultBlock(@SOU_ID, @BLO_ID_REL INT)` l. 2 caste `BLO_ID` en entier → **numérique obligatoire** (`'24'`, pas `'01-PLANS - 23 2'`) |
| `Layer/@Index` (calque) | `SOUDIV.DIV_ID varchar(3)` (+ `SOUREL.DIV_ID`) | **convention** | `up_SOUDIV_Update` l. 6 |
| nom du fichier `.qpl` | `SOUMIS.EXTFILE varchar(200)` | **schéma** (nom) | V6:797-800 ; écrit par `up_SOUMIS_Update` l. 9 ; jamais lu |
| « vient de Plan Expert » | `SOUMIS.EXTAPP char(1)` | **schéma** ; **valeur inconnue** | seule valeur d'origine posée en SQL : `ORIGIN='C'` (`up_CopySoumis_Full` l. 32, « TO_CopyPaste en Delphi ») ; aucun `EXTAPP=` dans les 52 scripts |
| `Prices/Price/@CostEach`, `@MarkupEach` | — | **code** (absence) | toujours `0` ; les prix d'EE vivent dans `PRODUITS.COUBRUTUNI/COUESC/PROMCOUNET` → `SOUPRO` (`sp_SOU_CalculTotaux` l. 239-241) |
| `Scale`, `Area`, `Rectangle`, `Legend`, `Bookmarks`, `Reports` | — | — | rien en EE ne les reçoit |

---

## 4. La chaîne complète : d'une marque comptée à la quantité de produit

Ordre d'écriture que l'application doit respecter (les procédures de cumul ne créent aucune ligne : elles ne font que
`UPDATE` ce qui existe déjà).

### 4.1 En-tête `SOUMIS`

`up_SOUMIS_Update` (V11_UpdateDatabase.sql:913-916 pour la version avec `@ORIGIN`, `@ORIGINREF`, `@EXTAPP`, `@EXTFILE`) :
`SOU_ID varchar(20)` (clé de toutes les tables `SOU*`, aucune clé étrangère : `sys.foreign_keys` = 0 ligne), `NODOC varchar(12)`,
`DESCDOC varchar(200)`, `UMPLAN varchar(2)`, `EXTFILE`, `EXTAPP`, `CALCTIMSTP varchar(14)` (posé par
`sp_SOUPRO_Quantity_V2` l. 27-28 au moment du cumul).

### 4.2 Grille `SOUBLO` × `SOUDIV`

`up_SOUBLO_Update` (`@BLO_ID varchar(3)`, `@MULT int`, l. 6, 10) et `up_SOUDIV_Update` (`@DIV_ID varchar(3)`, l. 6). `SOUBLO.MULT`
multiplie toutes les quantités du bloc (`fn_MultBlock` l. 7-12 : `SOUBLO.MULT`, 1 si le bloc n'existe pas).

### 4.3 Copie du catalogue dans la soumission — obligatoire, faite par l'application

- `ENSEMBLE` → `SOUENS` par `up_SOUENS_Update` (l. 3-19 : `@ENS_ID`, `@ENS_ORG_ID`, `@DESC`, `@QTETOT`, `@QTETOTSECT`,
  `@CALCTIMSTP`, `@COUUM`, `@TEMPUNI`, `@TEMPSEC`, `@TEMPUM`, `@DATECREE`, `@OLDESTPROD`, `@CLEPERS`, `@PROFIT`).
  `ENS_ORG_ID` = identifiant d'origine au catalogue (nom de colonne, V6) : la soumission garde `ENS_ID` (ce que `SOUREL`
  référence) et l'origine.
- `ENSCOMPO` → `SOUENSCO` par `up_SOUENSCO_Update` (l. 2-13 : `@ENS_ID`, `@PRO_ID`, `@ORDRE`, `@QTE`, `@QTEUM`, `@TYPRATIO`,
  `@DIV`, `@DIVUM`).
- `PRODUITS` → `SOUPRO` par `up_SOUPRO_Update` (l. 3-33) pour **chaque composant** et chaque produit relevé directement.

Pourquoi c'est obligatoire : `sp_SOU_UpdateQteTotalEns_v2` part de `FROM SOUPRO SPP LEFT JOIN (...)` (l. 16) et met à jour
`SOUPRO` par `UPDATE ... WHERE SOU_ID = ... AND PRO_ID = ...` (l. 87) — un produit absent de `SOUPRO` n'a **jamais** de
quantité ; la composition est lue dans `SOUENS E, SOUENSCO C WHERE E.SOU_ID = C.SOU_ID AND E.ENS_ID = C.ENS_ID AND E.SOU_ID =
@SOU_ID` (l. 45-48), jamais dans `ENSEMBLE`/`ENSCOMPO`. Même logique dans `sp_SOU_CalculTotaux` : `select sp.* into
#SOUPRO_TEMP from SOUPRO sp` (l. 115) puis `FROM SOUENS SE, SOUENSCO SEC, #SOUPRO_TEMP sp` (l. 260-266).

### 4.4 Lignes de relevé `SOUREL`

`up_SOUREL_Update` l. 3-27 : `@SOU_ID, @BLO_ID, @DIV_ID, @TYPERELEVE, @EXT_ID, @ORDRE varchar(6), @TYPEITEM, @ITEM_ID, @DESCR,
@QTE, @SECTION, @QTEUM, @PROFIT, @TYPETAXE, @CODEIMPR, @COUTANBRUT, @TEMPSUNIT, @TEMPSSEC, @TEMPSUM, @PROFITPLUS, @PROFITMOIN,
@ACC_NO, @ACH_NO, @ACT_NO`. Une ligne par (feuille, calque, groupe lié) : `TYPERELEVE='P'`, `TYPEITEM`/`ITEM_ID` du
`EEExchangeData`, `QTE` = compte ou longueur, `EXT_ID` = `GroupID`. `ORDRE` est une chaîne numérique sur 6 (`up_CopySouBlocDiv`
l. 44 : `RIGHT('000000' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)`), tri `ORDER BY SOU_ID, TYPERELEVE,
BLO_ID, DIV_ID, ORDRE` (`sp_SOU_CalculTotaux` l. 157).

### 4.5 Cumul des quantités : `sp_SOUPRO_Quantity_V2`

`sp_SOUPRO_Quantity_V2 @SOU_ID, @REPLACE_FILTER, @DoLog, @SOUPROLOG` (l. 3) — « Normalement cette procedure est appelée
uniquement pour : (TYPERELEVE = 'P') » (l. 7) — pose `SOUMIS.CALCTIMSTP = @UID` (l. 27-28) puis appelle (l. 34-36) :

- `sp_SOU_UpdateQteTotalOth_v2` : lignes `TYPEITEM IN ('P','N')` (l. 29), `QTE_cmp = SUM(SR.QTE × fn_MultBlock)` par
  `BLO_ID, ITEM_ID, QTEUM` (l. 26-30), converti vers l'unité de base du produit (l. 19) → `SOUPRO.QTEOTH` (l. 64).
- `sp_SOU_UpdateQteTotalEns_v2` : lignes `TYPEITEM = 'A'` (l. 52) ; pour chaque composant `C` de l'ensemble `E` :
  `QTE_ENSCO = (C.QTE / C.DIV) × ratio(E.COUUM → C.DIVUM)` si `C.TYPRATIO='L'` et `E.COUUM` est une longueur, sinon `C.QTE`
  (l. 33-41) ; `QTE_cmp = Σ [ (TYPRATIO='L' ? round₃(QTE_ENSCO × ratio(SR.QTEUM → C.COUUM)) × SR.QTE : QTE_ENSCO × SR.SECTION)
  × fn_MultBlock(SR.SOU_ID, SR.BLO_ID) ]` (l. 24-30) → `SOUPRO.QTEENS` (l. 87). Puis, si `@REPLACE_FILTER > 0`, propagation de
  `SOUREL.CODEIMPR` aux produits des ensembles (`sp_SOU_CalculCodeImpr`, l. 105-134).
- `sp_SOU_UpdateQteTotalLots_v2` : lignes `TYPEITEM = 'L'` → `SOUPRO.QTELOT`.

`@REPLACE_FILTER` doit être > 0 : à 0, `CLOSE CUR_2` (l. 136) ferme un curseur jamais ouvert (Msg 16916, prouvé dans
`eewin/examples/worked_example.log`).

`SOUENS.QTETOT` et `SOUENS.QTETOTSECT` ne sont calculés par **aucune** procédure : ils n'apparaissent que comme paramètres de
`up_SOUENS_Update`, dans les copies (`up_CopySouBlocDiv` l. 91) et dans l'ancienne version V1 des cumuls. Le total par
ensemble est donc, lui aussi, une valeur écrite par l'application.

### 4.6 Nettoyage : `sp_SOUPRO_Del_UnusedProd`

Supprime de `SOUPRO` (l. 12-40) tout produit qui n'est ni composant d'un `SOUENS`/`SOUENSCO` de la soumission, ni composant
d'un `SOULOTS`/`SOULOTSCO`, ni `ITEM_ID` d'une ligne `SOUREL` `TYPERELEVE IN ('P','U')` — donc l'inverse exact de 4.3.

### 4.7 Totaux : `sp_SOU_CalculTotaux`

Boucle sur `SOUREL WHERE SOU_ID = @SOU_ID AND TYPERELEVE = @TypeReleve` (l. 150-157) ; branche ensemble l. 215-287 :
coût net des composants depuis `#SOUPRO_TEMP` (`PROMCOUNET` sinon `COUBRUTUNI × (1 − COUESC/100)`, l. 239-241), sommes
l. 268-271, temps `@QTE × SE.TEMPUNI × ratio(@QTEUM → SE.TEMPUM)` + `SE.TEMPSEC × @SECTION` depuis `SOUENS` (l. 276-285). Les
lignes `TYPEITEM = 'T'` (titres) sont ignorées (l. 343). Formules complètes : [[CALCUL-SOUMISSION]] §4, §7.

---

## 5. Les 132 ensembles du recensement face au schéma

`ensembles-ee.csv` (colonnes `item_id, item_type, key, name, description, marks_total, n_projects, labels`) :

| Constat (calculé sur le CSV) | Colonne EE | Compatible ? |
|---|---|---|
| 116 `item_type='A'`, `item_id` = 20 caractères, préfixe `ENS` (100 %) | `ENSEMBLE.ENS_ID varchar(20)` | oui, longueur exacte |
| 16 `item_type='P'`, `item_id` = 9 caractères, préfixe `LQE` (100 %) ; `key` = `IBE52171K`, `HOFASE884`, `HUBHBL2810`, `CAB3/0BARECU`… | `PRODUITS.PRO_ID varchar(20)` ; `key` → `PRODUITS.CLEMANU varchar(30)` | oui ; le préfixe de division `LQE` est celui que `up_PriceUpdate_UpdateProducts` l. 69 exclut de la mise à jour de prix et que `PROCORRESP.NEWDIV` porte (46 857 lignes) |
| `key` max 20 caractères ; 106/132 commencent par `19PE` (conduits), 9 par `4PE` (prises) | `ENSEMBLE.CLEPERS varchar(20)` | oui, à la limite exacte |
| `name`/`description` max 42 caractères, identiques sur 131/132 | `ENSEMBLE.[DESC] varchar(60)` | oui |
| 3 767 marques liées dans 30 projets (sur 386 005 marques du corpus) | `SOUREL.QTE` | < 1 % du relevé de Dupuis passe par le pont EE ; le reste est compté hors EE |

Sans la base vivante de DR (0 ligne dans `ENSEMBLE`, `ENSCOMPO`, `PRODUITS` de la base rebâtie), un `ENS_ID` ne donne ni prix,
ni temps, ni composition : le QPL n'en contient aucun.

---

## 6. Preuve exécutée sur la base vivante

`eewin/examples/qpl_to_eewin_sql.py FILE.qpl --sou-id … --px-to-unit k [--seed-synthetic-catalogue] [--cleanup]` lit le QPL
et n'émet que des appels aux procédures officielles (`up_*_Update`, `sp_SOUPRO_Quantity_V2`, `sp_SOU_CalculTotaux`,
`up_DeleteSoumis_Full`, `up_*_Delete`). Comme la base rebâtie n'a aucun catalogue, l'option `--seed-synthetic-catalogue`
crée un `ENSEMBLE` **synthétique** dont seuls `ENS_ID`, `CLEPERS` et `DESC` viennent du QPL (composition inventée et
étiquetée `SYNTHETIC` : 1 pi de conduit `ZZPE-CONDUIT` à 100 $/CF et *n* conducteurs `ZZPE-WIRE` à 40 $/CF par pied, *n* lu
dans le nom `03c12`). `--px-to-unit 1` laisse les longueurs en **pixels** (le facteur réel dépend de `Scale`, non documenté).

Résultats (`planexpert_import_S-1714.log`, 0 `Msg`) :

| Table | Ligne écrite | Vient de |
|---|---|---|
| `SOUMIS` | `SOU_ID=ZZTEST-PE1714, EXTAPP='', EXTFILE='S-1714-Dupuis-PlanExpert.qpl', UMPLAN='F', CALCTIMSTP=20269271693343` | nom du fichier ; `CALCTIMSTP` posé par `sp_SOUPRO_Quantity_V2` l. 27-28 |
| `SOUBLO` / `SOUDIV` | `BLO_ID='24'` (feuille 24 « 01-PLANS - 23 2 »), `DIV_ID='0'` (« Calque par défaut ») | position de la feuille, `Layer/@Index` |
| `SOUENS` | `ENS_ID=ENS_ORG_ID=ENSCFFFDBD5146159B90, CLEPERS='19PE0.75 #12', DESC='SYNTHETIC conduit 3/4 03c12', COUUM='F'` | copie de `ENSEMBLE` (synthétique) |
| `SOUENSCO` | `ZZPE-CONDUIT QTE=1 F L DIV=1 F` ; `ZZPE-WIRE QTE=3 F L DIV=1 F` | copie de `ENSCOMPO` |
| `SOUREL` | `BLO_ID=24, DIV_ID=0, EXT_ID='129', TYPEITEM='A', ITEM_ID=ENSCFFFDBD5146159B90, DESCR='conduit 3/4 03c12', QTE=39083.0, QTEUM='F'` | `Line GroupID=129` : 83 segments, 39 083 px × 1 |
| `SOUPRO` après `sp_SOUPRO_Quantity_V2` | `ZZPE-CONDUIT QTEENS=39083.0` ; `ZZPE-WIRE QTEENS=117249.0` (= 3 × 39 083) ; `QTEOTH=QTELOT=0` | `sp_SOU_UpdateQteTotalEns_v2` l. 24-30, 87 |
| `sp_SOU_CalculTotaux 'P'` | `CoutantNetReel=2.20/F` (1,00 + 3 × 0,40), `CoutantTotal=85 982,60`, `TempsInstallationTotal=0` (ensemble synthétique `TEMPUNI=0`) | l. 268-285 |

S-1844 (`planexpert_import_S-1844.log`, 0 `Msg`) : 2 lignes `SOUREL` (`EXT_ID='64'` → `ENSAFF5D05713B179C81`, 9 162 px ;
`EXT_ID='65'` → `ENS9E93142F911561EE1`, 7 513 px), 2 `SOUENS`, 4 `SOUENSCO`, `SOUPRO.QTEENS` = 16 675 (conduit) et
312 063 (= 7 × 9 162 + 33 × 7 513 fils). Les 66 objets restants (64 groupes sans `EEExchangeData`, ex. `Counter 'FIXTURE
ENLEVER'` 204 marques) sont listés en commentaire dans le `.sql` : non importables.

Nettoyage (`planexpert_cleanup_*.log`) : tous les comptes à 0 (`soumis, sourel, soupro, souens, souensco, soublo, soudiv,
ensemble, produits`).

---

## 7. Ce qu'il faut encore obtenir (et à qui le demander)

1. **La valeur de `SOUMIS.EXTAPP`** écrite par EEWin pour un projet venu de Plan Expert, et **ce que EEWin met dans
   `SOUREL.EXT_ID`** (`GroupID`, clé `129;;Line;`, autre) — aucun script ne le dit ; seule une soumission réelle importée dans
   la base vivante de DR (lecture de `SOUMIS.EXTAPP, EXTFILE, ORIGIN` et `SOUREL.EXT_ID`) tranchera.
2. **La sémantique de `Plan/Scale`** (`Value="0,09375" Type="1"` ; 86 % des feuilles du corpus à `0`) pour convertir les
   longueurs de `Line` en `SOUMIS.UMPLAN` ; sans elle `SOUREL.QTE` d'un conduit reste en pixels.
3. **L'export du catalogue vivant** (`ENSEMBLE`, `ENSCOMPO`, `PRODUITS`, `TAUX`) : c'est lui qui transforme
   `ENSCFFFDBD5146159B90` en coût et en heures ; le QPL ne contient que la clé.
4. Le lien humain pour les 128/129 groupes non liés de S-1714 : Dupuis chiffre ces marques hors du pont EE (étiquettes
   `PRISE`, `INT`… du recensement, 386 005 marques dont 3 767 liées) — le mapping étiquette → `ENS_ID` est une table à
   construire avec lui, pas à déduire des fichiers.

---

## Annexe — commandes exécutées

```bash
# Recherche du vocabulaire QPL dans les scripts
grep -rniE "EEExchange|Quoter|PlanExpert|Plan Expert|Takeoff|Counter|GroupID" eewin/scripts/     # 0 ligne
grep -niE "\bplan|web|transfer|exchange|echange" eewin/scripts/*.sql eewin/scripts/*.SQL          # UMPLAN, SOUWEBLOG, _TransferCompleted

# Extraction des 177 définitions avec numéros de ligne exacts (ordinal = ligne OBJECT_DEFINITION)
sqlcmd -d EE -Q "SELECT RTRIM(o.type) COLLATE DATABASE_DEFAULT + ' ' + o.name COLLATE DATABASE_DEFAULT
                 FROM sys.sql_modules m JOIN sys.objects o ON o.object_id=m.object_id ORDER BY o.name"
sqlcmd -d EE -h -1 -y 8000 -Q "SELECT ordinal, value FROM STRING_SPLIT(OBJECT_DEFINITION(OBJECT_ID('[dbo].[<nom>]')), CHAR(10), 1) ORDER BY ordinal"
grep -liE "exchange|quoter|xml|import|export|takeoff|relev" <defs>/*.sql                          # TYPERELEVE + fn_STR_Alphaorder
grep -ln "ENSEMBLE\b|ENSCOMPO\b|INTO SOUPRO|INSERT INTO SOUENS" <defs>/*.sql                      # aucune copie catalogue→soumission

# Colonnes
SELECT TABLE_NAME, ORDINAL_POSITION, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_NAME IN ('SOUMIS','SOUREL','SOUENS','SOUENSCO','SOUPRO','SOUBLO','SOUDIV','ENSEMBLE','ENSCOMPO','PRODUITS','PROCORRESP','SOUWEBLOG');
SELECT COUNT(*) FROM PROCORRESP WHERE NEWDIV='LQE';                                                -- 46857
SELECT * FROM Sys_Units;                                                                           -- 19 unités

# QPL : structure, Prices, groupes (xml.etree) ; preuve
python3 eewin/examples/qpl_to_eewin_sql.py S-1714-Dupuis-PlanExpert.qpl --sou-id ZZTEST-PE1714 --px-to-unit 1 --seed-synthetic-catalogue > planexpert_import_S-1714.sql
docker cp planexpert_import_S-1714.sql eewin:/tmp/ && docker exec eewin /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '…' -C -d EE -W -s '|' -i /tmp/planexpert_import_S-1714.sql
python3 eewin/examples/qpl_to_eewin_sql.py … --cleanup > planexpert_cleanup_S-1714.sql            # puis même exécution
```
