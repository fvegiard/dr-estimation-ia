# EEWin — le catalogue de produits et son lien avec les QPL de Plan Expert

Source : base `EE` reconstruite à partir des 52 scripts officiels de Dupuis (`eewin/scripts/`, chargeur `eewin/run.sh`,
0 erreur : 60 tables, 160 procédures, 18 fonctions), SQL Server 2022 dans le conteneur `eewin`. Tout ce qui suit a été lu
dans `INFORMATION_SCHEMA`, `sys.indexes`, `sys.sql_modules` (`OBJECT_DEFINITION`) et dans les scripts eux-mêmes, puis
rejoué par `eewin/examples/catalogue_checks.sql` (sortie réelle : `eewin/examples/catalogue_checks.log`, 0 `Msg`).
Côté Plan Expert : `ensembles-ee.csv` (132 lignes, recensement du 2026-09-25) et les QPL de Dupuis présents ici
(`dossiers/S-1714/reference/S-1714-Dupuis-PlanExpert.qpl`, `dossiers/S-1844/reference/S-1844-Dupuis-PlanExpert.qpl`).

Convention de citation : `fichier l. N` = ligne N du script tel que livré ; la version **vivante** d'une procédure est
toujours celle du dernier script qui la (re)crée, indiqué à chaque fois. Complète `CALCUL-SOUMISSION.md` (qui explique
comment `SOUPRO`/`SOUENS` sont calculés une fois copiés dans une soumission) : ici, on explique **d'où viennent** les
produits, les prix, les temps et les ensembles avant la soumission.

---

## 1. Ce que la base contient réellement (et ne contient pas)

`catalogue_checks.log` §1 : `PRODUITS` 0 ligne, `ENSEMBLE` 0, `ENSCOMPO` 0, `PROCAT` 0, `PROGLOSS` 0, `BDEE` 0,
`PriceUpdate_Products` 0, **`PROCORRESP` 84 721**. Les 52 scripts sont un **schéma + un jeu de correspondances de
clés**, pas le catalogue de DR : aucun prix, aucun temps, aucun ensemble. Le catalogue vivant est dans la base
EEWin du serveur DR, jamais dans le paquet `V14_UpdateDatabase.zip`.

Conséquence : tout ce qui est écrit ici sur les **mécanismes** est prouvé par le code ; ce qui est écrit sur les
**valeurs** (prix, temps, ENS_ID) ne peut être vérifié qu'avec un export de la base vivante.

---

## 2. La table `PRODUITS` — 39 colonnes, 3 clés, 2 prix, 1 temps

Définition : `CreateTables.sql` l. 527-571, puis colonnes ajoutées par `V7` (`DATECOUNET`, `RESCOUNET`), `V8`
(`PREFERED`), `V9` (`PRO_ID_NEW`, `PRO_ID_OLD`), `V15` (`CODEUPCDIS`), `V19` (`SHOWONWEB`), `V44` (`PRO_ID_Parent`).
`CLEMANU` passe de 20 à 30 caractères dans `V13_UpdateDatabase.sql` l. 278-292 (« Passage de 20 a 30 char pour les
CLEMANU de toutes les tables » : `COMMITEM`, `FACPRO`, `PriceUpdate_Products`, `PRODUITS`, `SOUPRO`).

| Colonne (`CreateTables.sql` l.) | Type | Rôle prouvé |
|---|---|---|
| `PRO_ID` (l. 529) | `varchar(20)` | identifiant du produit. Les 3 premiers caractères = **division** du distributeur (`LEFT(PRO_ID, 3)` partout dans `up_PriceUpdate_UpdateProducts`, `V22` l. 909-911 et 946-948). Format observé dans les QPL : `LQE008445` (3 lettres + 6 chiffres, 9 car.). `V18` l. 18 exclut de la mise au rebut les `PRO_ID` de **20** caractères (`LEN(PRO_ID) <> 20`) : ce sont les produits qui ne viennent pas d'une liste de prix (le script ne dit pas comment ils sont numérotés) |
| `CLEMANU` (l. 530) | `varchar(30)` | **clé manufacturier** — pièce d'identité du produit d'un catalogue à l'autre. C'est la clé de `PROCORRESP` (§4). Index `IDX_CLEMANU` (`V3` l. 2085) |
| `CLEDIST` (l. 532) | `varchar(20)` | clé du distributeur (son numéro d'article). Index `IDX_CLEDIST` (`V3` l. 2081) |
| `CLEPERS` (l. 531) | `varchar(20)` | **clé personnelle** de l'entrepreneur. Jamais alimentée par la mise à jour de prix (absente de `PriceUpdate_Products`, §3) ; écrite seulement par `up_PRODUITS_Update` (paramètre `@CLEPERS`, `V45` l. 41 sqq.). Index `IDX_CLEPERS` (`V3` l. 2089). `upbi_ProductsPrefered_BatchAssign` (`V8` l. 199) traite `CLEPERS <> ''` comme « produit que l'usager a fait sien » |
| `CODEUPC` / `CODEUPCDIS` | `varchar(12)` | UPC personnel / UPC du distributeur (`V15`), même règle « on écrase si jamais personnalisé » que `DESC` (`V22` l. 885) |
| `CODECAT` (l. 534) | `varchar(3)` | catégorie → `PROCAT.CODECAT` (`CreateTables.sql` l. 518-525 : `CODECAT`, `DESC` 40 car., plus `ACC_NO/ACH_NO/ACT_NO` comptables ajoutés `V11`). Une catégorie **système** commence par `+` ou `#` et peut être écrasée par la liste de prix ; une catégorie personnelle est conservée (`V22` l. 887) |
| `DESCDIST` / `DESC` | `varchar(60)` | description du distributeur / description personnelle ; `DESC` n'est remplacée que si vide ou égale à `DESCDIST` (`V22` l. 884) |
| `COUBRUTUNI` (l. 537) + `COUUM` (l. 538) | `float` + `varchar(2)` | **coût brut unitaire** et son unité (§7) |
| `COUESC` | `float` | escompte % sur le brut |
| `PROMCOUNET` | `float` | **prix net** (promo/net négocié) — prioritaire sur brut−escompte dans le calcul (`CALCUL-SOUMISSION.md` §3) |
| `DATECOUT` / `DATECOUNET` / `RESCOUNET` | `datetime`/`datetime`/`int` | date de la liste de prix / date du prix net / réserve « prix net Rexel » (`V7` l. 1-34, EE-222) |
| `QPP` / `MULCOM` | `float` | quantité par paquet / multiple de commande |
| `TEMPUNI` (l. 544) + `TEMPUM` (l. 545) | `float` + `varchar(2)` | **temps d'installation unitaire** et son unité (§7) |
| `CODEFOUR` (l. 546) | `varchar(2)` | code fournisseur dérivé de la division : `NE`, `LE`, `GE`, `SE`, sinon `WE` (`V22` l. 930-934) |
| `NOUVEAU`, `DNR` (l. 547-548) | `varchar(1)` | nouveau dans la liste / **D**iscontinued-**N**ot-**R**eplaced (`up_PriceUpdate_DiscontinueProducts`) |
| `PREFERED` | `varchar(1)` | produit préféré (`V8`, EE-263 « Prix net Rexel Phase 2 ») ; `upbi_ProductsPrefered_BatchAssign` le pose à `'1'` pour tout produit ayant une `CLEPERS`, présent dans un `ENSCOMPO`, une commande, une soumission ou une facture depuis `@LimitDate`, en excluant les `PRO_ID` préfixés `NLS` (`V8` l. 264, 284, 304) |
| `PRO_ID_NEW`, `PRO_ID_OLD`, `PRO_ID_Parent` | `varchar(20)` | chaînage remplacement / parent (`V9` l. 1-34, `V44` l. 20) — stockés seulement, aucune procédure ne les lit |

---

## 3. Comment DR reçoit les prix : la chaîne `PriceUpdate_*`

### 3.1 Table de transit `PriceUpdate_Products`

`CreateTables.sql` l. 950 sqq. ; colonnes vivantes (`catalogue_checks.log` §6) :
`PRO_ID, DESC, CODECAT, COUUM, TEMPUM, CLEMANU, CLEDIST, DESCDIST, QPP, MULCOM, COUBRUTUNI, COUESC, PROMCOUNET, NOUVEAU,
DATECOUT` (origine) + `CODEUPC, CODEUPCDIS` (`V15` l. 44-83) + `SHOWONWEB` (`V19` l. 25-41). Index `IDX_PRO_ID` (`V3` l. 2077).

**Ce qu'un fichier de distributeur peut livrer se limite à ces 18 colonnes.** Il n'y a **ni `TEMPUNI`, ni `CLEPERS`**
dans la table de transit : le distributeur livre l'*unité* du temps (`TEMPUM`) mais **jamais le temps lui-même**.

### 3.2 Les 6 procédures, dans l'ordre où l'application les appelle

| Étape | Procédure (version vivante) | Effet |
|---|---|---|
| 1 | `up_PriceUpdate_ClearProducts` (`CreateScripts.sql` l. 4090) | `TRUNCATE TABLE PriceUpdate_Products` |
| 2 | `up_PriceUpdate_SaveProduct` (`V19` l. 46-110), une fois **par ligne** du fichier | `INSERT INTO PriceUpdate_Products` des 18 colonnes |
| 3 | `up_PriceUpdate_UpdateProducts` (`V22` l. 844-949) | fusion transit → `PRODUITS` (§3.3) |
| 4 | `up_PriceUpdate_DiscontinueProducts(@Division, @UpdateDate)` (`V18` l. 5-19) | `DNR='Y', NOUVEAU='N'` pour tout `PRO_ID LIKE @Division+'%'` dont `DATECOUT <> @UpdateDate` et `LEN(PRO_ID) <> 20` — ce qui n'était pas dans la liste du jour est discontinué |
| 5 | `up_PriceUpdate_ClearGlossary(@Division)` / `up_PriceUpdate_InsertGlossary` (`CreateScripts.sql` l. 4215-4240) | rechargent `PROGLOSS` (`TYPEGLOSS, CATEGORIE, SOUSCAT, CODE, DESCRIPTIO, CODEBANK`) pour `CODEBANK = @Division` : le glossaire de recherche du distributeur |

Rien dans les scripts ne lit le fichier : le parsing (CSV/URL) est dans l'application Delphi. La table de licence `BDEE`
porte les paramètres de connexion : `NODIST` (numéro de client chez le distributeur), `DIVISION varchar(3)`,
`DIVISIONPX varchar(2)`, `ISINT` (`V5` l. 1-30, « Nouvelle licence »), puis `PRICEURL`, `ORDERURLFR/EN`, `AUTHURL`,
`AUTHGLOKEY`, `AUTHCLIKEY`, `URLMODE` (`V11` l. 2038-2141) et `SRCHWEBURL` (`V18` l. 21). `BDEE_MULTI`
(`V43` l. 1-30 : `DistributorCode varchar(3)` PK, `DistributorName`, `ORDRE`) permet plusieurs distributeurs depuis V43.

### 3.3 `up_PriceUpdate_UpdateProducts` — la logique de fusion (V22 l. 844-949)

1. **Insertion des inconnus** (l. 856-870) : `INSERT INTO PRODUITS (PRO_ID, TEMPUM, DATECREE)` pour tout `PRO_ID` du
   transit absent de `PRODUITS`. Seul le **`TEMPUM`** est repris — `TEMPUNI` naît à `NULL`.
2. **Passe « Wolseley / clients réguliers »** (l. 881-911), `WHERE LEFT(PRO_ID,3) NOT IN ('NWE','NOE','NQE','NME','WAE',
   'WME','WOE','WQE','LQE','GSE','SOE') AND LEFT(PRO_ID,3) IN ('WOP','WQP','WEP','WWP') AND EE_Calgary() = 0` :
   copie **brut + escompte + net** (`COUBRUTUNI, COUESC, PROMCOUNET`, l. 898-900), `CODEFOUR = 'WE'` (l. 897),
   `DATECOUNET = DATECOUT` (l. 904 : « Date prix net = date coût brut pour Wolseley »).
3. **Passe « Rexel (Nedco/Westburne) + Sonepar (Lumen/Sesco/Gescan) + Wolseley interne »** (l. 913-948),
   `WHERE LEFT(PRO_ID,3) IN (les 11 divisions) OR (WOP/WQP/WEP/WWP AND EE_Calgary() = 1)` :
   - copie descriptif, clés, `COUUM`, `QPP`, `MULCOM`, `NOUVEAU`, `DATECOUT` (l. 921-929, 939-940) ;
   - **ne touche pas aux prix** : `COUBRUTUNI = CASE WHEN DATECOUNET IS NULL THEN COALESCE(COUBRUTUNI,0) ELSE COUBRUTUNI END`
     (l. 935-937, « Initialise a 0 a l'ajout, sinon, ne touche pas a ce prix. MaJ de prix decouplee ») ;
   - `DATECOUNET` **n'est plus écrit** (l. 941 commentée) : chez ces distributeurs la **liste d'articles** et le
     **prix net** arrivent par deux canaux distincts ; le prix net entre par `up_PRODUITS_Update(@COUBRUTUNI, @COUESC,
     @PROMCOUNET, @DATECOUNET, @RESCOUNET)` (`V45` l. 41 sqq.), c'est-à-dire par l'application, article par article.
   - `CODEFOUR` : `N→NE`, `L→LE`, `G→GE`, `S→SE`, sinon `WE` (l. 930-934).

Historique de cette procédure (utile pour dater une base) : `CreateScripts.sql` l. 4148 (une seule passe, `CODEFOUR N→NE
sinon WE`) → `V7` l. 519 (EE-222, 2014-11-25 : « Prix net pas dans le catalogue pour Rexel », `COUESC/PROMCOUNET`
préservés pour les 8 divisions N*/W*) → `V10` l. 6 (EE-1044, 2016-11-21 : split en deux passes) → `V13` l. 11 (ajout
`LQE`, `CODEFOUR 'LU'`) → `V14` l. 80118 (ajout `GSE`, `SOE`, `LU→LE`) → `V15` l. 159 (`CODEUPC`) → `V16` l. 24
(EE-1723, 2018-06-12 : `COALESCE(…,0)` pour ne plus remettre à 0 les prix des anciens clients Rexel) → `V19` l. 112
(`SHOWONWEB`) → `V22` l. 844 (divisions Wolseley `WOP/WQP/WEP/WWP` + `EE_Calgary()`).

### 3.4 Divisions et distributeurs — ce que le code dit, mot pour mot

| Préfixe `PRO_ID` | Groupe (commentaires du code) | `CODEFOUR` | Preuve |
|---|---|---|---|
| `NWE, NOE, NQE, NME` | Nedco (Rexel) | `NE` | `V22` l. 913 « Nedco / Westburne / Rexel » (l. 878), l. 930 |
| `WAE, WME, WOE, WQE` | Westburne (Rexel) | `WE` | idem, l. 934 |
| `LQE` | Lumen (Sonepar) | `LE` (`LU` en V13) | `V22` l. 913 « clients Sonepar (Lumen, Sesco, Gescan) », l. 931 |
| `GSE` | Gescan (Sonepar) | `GE` | l. 932 |
| `SOE` | Sesco (Sonepar) | `SE` | l. 933 |
| `WOP, WQP, WEP, WWP` | Wolseley | `WE` | `V22` l. 880 « logique de prix Wolseley », l. 913 « employés de Wolseley (Interne / EE_Calgary) », l. 911/948 |
| `NLS` | exclu des produits « préférés » | — | `V8` l. 264/284/304 (le code ne dit pas ce que c'est) |

La 2ᵉ lettre (`W/O/Q/M/A`) n'est jamais interprétée par le SQL ; seule la chaîne de 3 caractères l'est. `EE_Calgary()`
(`V22` l. 813-835) retourne 1 si la colonne `PRODUITS.LC` existe — la base « interne Wolseley/Calgary » est identifiée
par la présence de cette colonne, pas par une donnée.

---

## 4. `PROCORRESP` — la table de correspondance entre catalogues (84 721 lignes vivantes)

Créée dans `V13_UpdateDatabase.sql` l. 264-274 : `OLDDIV varchar(3), OLDCLEMANU varchar(30), NEWDIV varchar(3),
NEWCLEMANU varchar(30)` ; `ISUSER varchar(120)` ajouté `V16` l. 1-16 ; procédure `up_PROCORRESP_Update` `V16` l. 134-181
(insert/update champ à champ, `@ISUSER varchar(1)` alors que la colonne fait 120).

**Chargement** (compté dans les scripts et dans la base, `catalogue_checks.log` §2) :

| Script | Action | Lignes |
|---|---|---|
| `V14` l. 2-4 | `DELETE … WHERE OLDDIV IN ('WQE','NQE')` | — |
| `V14` l. 6-80113 | 79 315 `INSERT` : `WQE→LQE` 26 606, `NQE→LQE` 20 251, `NOE→SOE` 26 606, `WOE→SOE` 5 852 | |
| `V16` l. 187-189 | `DELETE … WHERE OLDDIV IN ('NWE','WOE','WAE')` (efface les 5 852 `WOE` de V14) | |
| `V16` l. 191-11570 | 11 258 `INSERT` : `WAE→GSE` 5 535, `WOE→SOE` 3 471, `NWE→GSE` 2 252 | |
| **Base vivante** | 90 573 − 5 852 = **84 721** ✓ | `ISUSER` = NULL partout (§3 du log) |

**Sens** : la clé manufacturier (`CLEMANU`) d'un produit du catalogue **Rexel** (Westburne `W*E` / Nedco `N*E`) → la clé
manufacturier du **même produit** dans le catalogue **Sonepar** (Lumen `LQE`, Sesco `SOE`, Gescan `GSE`). La direction
est toujours Rexel → Sonepar (`OLDDIV = NEWDIV` : 0 ligne). 33 341 lignes gardent la même `CLEMANU` (changement de
division seulement) ; 51 380 la changent, parce que les deux distributeurs n'encodent pas le fabricant de la même façon
(`V14` l. 7 : `WQE PHI376WHX → LQE LIG376WHX` ; log §4 : `NQE EPOD8X8X4 → LQE HOFASE884`, `NQE THSBC52171K → LQE
IBE52171K`). `OLDCLEMANU` ne dépasse jamais 20 caractères (ancienne longueur), `NEWCLEMANU` monte à 28 — c'est la
raison du passage à 30 dans `V13`.

**Aucune procédure ne lit `PROCORRESP`** (`catalogue_checks.log` §5 : seule `up_PROCORRESP_Update` la mentionne).
La table est livrée à l'application, qui doit — c'est la seule jointure possible avec les colonnes disponibles —
retrouver le nouveau produit par `PRODUITS.CLEMANU = NEWCLEMANU AND LEFT(PRO_ID,3) = NEWDIV` (index `IDX_CLEMANU`) et
réécrire les `PRO_ID` des `ENSCOMPO`, `SOUPRO`, `SOUENSCO`… d'un client qui passe de Rexel à Sonepar. `PRO_ID_NEW/OLD`
(`V9`) sont les colonnes prévues pour mémoriser ce chaînage ; le script ne montre pas le code qui les remplit.

Pour DR, 84 721 lignes livrées dans le paquet **et** le fait que les 16 produits des QPL soient en division `LQE` (§6)
disent la même chose : la base EEWin de DR est un catalogue **Lumen**, et Dupuis a des ensembles construits à l'époque
Rexel qui ont été convertis.

---

## 5. `ENSEMBLE` / `ENSCOMPO` — les assemblages

`CreateTables.sql` l. 154-175 et 139-153 ; `DESC` élargi 40→60 (`up_ENSEMBLE_Update`, commentaire « V3 → Passage de 40
à 60 chars »). Index : `IDX_ENS_ID`, `IDX_CLEPERS` sur `ENSEMBLE` (`V3` l. 16-20) ; `IDX_ENS_ID (ENS_ID, ORDRE)` et
`IDX_PRO_ID` sur `ENSCOMPO` (`V3` l. 2021 sqq.).

| Table.colonne | Type | Rôle |
|---|---|---|
| `ENSEMBLE.ENS_ID` (l. 156) | `varchar(20)` | identifiant de l'ensemble — c'est ce que le QPL exporte (§6) |
| `ENSEMBLE.CLEPERS` (l. 157) | `varchar(20)` | **la seule clé « lisible »** d'un ensemble ; pas de `CLEMANU`/`CLEDIST` : un ensemble n'appartient à aucun distributeur |
| `ENSEMBLE.DESC` | `varchar(60)` | description |
| `ENSEMBLE.COUUM` (l. 159) | `varchar(2)` | unité de l'ensemble (`U` pour une prise, `F`/`M` pour un conduit au pied/mètre) — pilote le ratio des composants linéaires (`CALCUL-SOUMISSION.md` §4) |
| `ENSEMBLE.TEMPSEC`, `TEMPUNI`, `TEMPUM` (l. 161-163) | `float, float, varchar(2)` | temps par section, temps unitaire, unité de temps de l'ensemble lui-même (s'ajoutent aux temps des composants) |
| `ENSEMBLE.PROFIT`, `SYSTEM`, `USES_DISC`, `OLDESTPROD` | | profit % (jamais lu par le calcul SQL), ensemble système, utilise l'escompte, plus vieux prix de composant |
| `ENSCOMPO.ENS_ID, ORDRE, PRO_ID` (l. 141-143) | | composant = un produit `PRODUITS.PRO_ID` (pas d'ensemble imbriqué : `ENSCOMPO` n'a pas de colonne `TYPEITEM`) |
| `ENSCOMPO.QTE, QTEUM, TYPRATIO, DIV, DIVUM` (l. 144-148) | | `TYPRATIO='L'` : `QTE` unités de composant par `DIV` `DIVUM` d'ensemble (ex. 1 raccord par 10 pieds) ; sinon : `QTE` par section |

Les procédures qui écrivent ces tables sont `up_ENSEMBLE_Update` (`CreateScripts.sql` l. 650, `V3` l. 26) et
`up_ENSCOMPO_Update` (`CreateScripts.sql` l. 582) — champ à champ, `ENS_ID` fourni par l'application. Aucun script
ne génère `ENS_ID` ; aucune fonction `NEWID()`/hash dans les 178 modules (grep sur `sys.sql_modules` : 0).

---

## 6. Le lien avec les QPL : `EEExchangeData`

### 6.1 La structure dans le .qpl

Dans `S-1714-Dupuis-PlanExpert.qpl` l. 29-31 :

```xml
<Group GroupID="129">
  <EEExchangeData ItemType="A" ItemID="ENSCFFFDBD5146159B90" Name="conduit 3/4 03c12"
                  Key="19PE0.75 #12" PersonalKey="19PE0.75 #12" Description="conduit 3/4 03c12"/>
</Group>
```

puis, dans la feuille, `<Line Name="conduit 3/4 03c12" GroupID="129" …>` : chaque tracé (ou compteur) du plan porte le
`GroupID` du groupe, et le groupe porte l'article EEWin. `S-1844-Dupuis-PlanExpert.qpl` l. 29-34 : deux groupes
(`ENSAFF5D05713B179C81` « conduit 3/4 07c12 » clé `19PE0.75 #12` ; `ENS9E93142F911561EE1` « conduit 2 33c12 » clé
`19PE2 #12`). Les 26 autres QPL du dépôt (relevés IA, S-1272, S-1689…) n'ont **aucun** `EEExchangeData`.

### 6.2 Correspondance attribut QPL ↔ colonne EE (par domaine, par longueur, par contenu)

| Attribut QPL | Colonne EEWin | Preuve |
|---|---|---|
| `ItemType="A"` / `"P"` | `SOUREL.TYPEITEM` `'A'` (ensemble) / `'P'` (produit) | mêmes lettres que le domaine lu par `sp_SOU_CalculTotaux` (`CALCUL-SOUMISSION.md` §2) |
| `ItemID` (type A) | `ENSEMBLE.ENS_ID varchar(20)` | 116/116 valeurs = `ENS` + 17 hexadécimaux = **20 caractères** exactement (longueur max de la colonne) |
| `ItemID` (type P) | `PRODUITS.PRO_ID varchar(20)` | 16/16 valeurs = `LQE` + 6 chiffres ; `LQE` est une division reconnue par `up_PriceUpdate_UpdateProducts` (`V22` l. 947) |
| `Key` (type P) | `PRODUITS.CLEMANU varchar(30)` | **14 des 16** clés (`IBE52171K`, `HOFASE884`, `HUBHBL2810`, `SCEPVC2`, `CONEMT11/2`, …) existent dans `PROCORRESP.NEWCLEMANU` avec `NEWDIV='LQE'` (`catalogue_checks.log` §4). Les 2 absentes (`CAB1/0RW90GRE`, `CAB3/0BARECU`) ont exactement la même grammaire (`CAB` + calibre + isolant) que `CAB3/0RW90GRE` qui y est |
| `Key` (type A) | `ENSEMBLE.CLEPERS varchar(20)` | seule colonne-clé d'`ENSEMBLE` ; 48 valeurs distinctes, longueur max **20** ; `Key = PersonalKey` dans les 3 occurrences disponibles |
| `PersonalKey` (type P) | `PRODUITS.CLEPERS varchar(20)` | par le nom et le type ; **non vérifiable ici** (aucun QPL du dépôt n'a d'article type P ; le recensement n'a pas conservé `PersonalKey`) |
| `Name` = `Description` | `ENSEMBLE.DESC` / `PRODUITS.DESC varchar(60)` | égaux dans 131/132 lignes ; longueur max 42 ≤ 60 |

Ce qui est **certain** : le QPL n'exporte **ni prix, ni temps, ni composition** (`CostEach = 0` partout, recensement §2).
Il exporte trois choses par article : l'identifiant (`ENS_ID`/`PRO_ID`), la clé lisible (`CLEPERS` pour un ensemble,
`CLEMANU` pour un produit) et la description. **Le prix et la main-d'œuvre ne se trouvent qu'en rejoignant `ENSEMBLE` →
`ENSCOMPO` → `PRODUITS` (COUBRUTUNI, COUESC, PROMCOUNET, TEMPUNI) dans la base vivante de DR**, puis en appliquant les
formules de `CALCUL-SOUMISSION.md` §3-4.

### 6.3 Les 132 articles recensés (`ensembles-ee.csv`)

| Famille de clé | Nb `ItemID` | Nb clés distinctes | Nature | Preuve |
|---|---|---|---|---|
| `19PE…` (`19PE0.5 #12`, `19PE0.75 PVC #12`, `19PE2 # 0000`, `19PE vide 1`, …) | 106 | 40 | ensembles **conduit + fils** : diamètre en pouces, `#` calibre AWG/kcmil, `PVC`, `vide` | dans S-1714 et S-1844 ces groupes portent des `<Line>` (tracés linéaires) |
| `4PE …` (`4PE prise 15A 120v`, `4PE int. 3W 15A 347V`, `4PE prise CR20 120V`) | 9 | 8 | ensembles **prise / interrupteur** | portés par des `<Counter>` (marques comptées : 1 572, 556, 261…) |
| `TMEC11/423` | 1 | 1 | ensemble conduit EMT | — |
| clés `CLEMANU` (`HOFASE884`, `IBE52171K`, `CAB…`, `SCEPVC…`) | 16 | 16 | **produits** Lumen : boîtes Hoffman/Iberville, câbles, conduits PVC | `PROCORRESP` §4 |

La **même clé personnelle** désigne des ensembles **différents** d'un projet à l'autre : `19PE2 #12` ↔ 13 `ENS_ID`
distincts, `19PE0.75 #12` ↔ 7 (`ENSCFFFDBD5146159B90` « conduit 3/4 03c12 » dans S-1714, `ENSAFF5D05713B179C81`
« conduit 3/4 07c12 » dans S-1844). Interprétation soutenue par les descriptions : la clé code le **conduit** (3/4 po,
#12), la description code le **nombre de conducteurs** (03c12 vs 07c12) ; Dupuis crée donc un ensemble par combinaison
conduit × nombre de fils, en réutilisant la clé du conduit. `IDX_CLEPERS` n'est pas unique (`is_unique = 0`), la base
le permet. **Pour retrouver un prix, seule `ENS_ID` est fiable ; `Key` seule est ambiguë.**

`19PE`/`4PE` ne correspondent à aucun code des scripts (`CODECAT` fait 3 caractères ; `PROCAT`/`PROGLOSS` sont vides) :
c'est la nomenclature personnelle de l'estimateur, à décoder avec lui ou avec la base vivante.

### 6.4 Lacune du recensement à corriger

`ensembles-ee.csv` affiche `marks_total = 0` et `n_projects = 0` pour **114 des 132** articles. Cause lue dans
`outils/census_qpl.py` l. 116-131 : seuls les `<Counter>` sont rattachés aux articles EE ; les `<Line>` (l. 132-141)
ne le sont pas. Or les 106 ensembles `19PE…` sont des tracés linéaires. Les 8 955 tracés du corpus (recensement §2) sont
donc déjà **pré-attribués à un ensemble EEWin dans 30 projets**, et cette information n'a pas été comptée. C'est la
donnée la plus précieuse du corpus pour la longueur de conduit : à recompter en rattachant `Line.GroupID` →
`EEExchangeData.ItemID`, longueur en pixels × échelle de la feuille.

---

## 7. Unités : `COUUM`, `TEMPUM`, `QTEUM`, `DIVUM`

Toutes en `varchar(2)` et toutes tirées de `Sys_Units` (19 lignes, `CreateData.sql` l. 1-24 ; `catalogue_checks.log`
§7). Le code stocké est `CodeEN` (`fn_UM_GetUniteDeBase(@CodeEN)` ; `fn_UM_GetNatureUnite` accepte `CodeEN` ou `CodeFR`
selon `@Lang`).

| `CodeEN` (`CodeFR`) | Type | Base × ratio | Produits / Ensembles |
|---|---|---|---|
| `U`, `C`, `K` | unité | `U` × 1, 100, 1000 | P+A / P / P |
| `M`, `HM`, `KM` | longueur | `M` × 1, 100, 1000 | P+A |
| `F` (`P`), `CF` (`CP`), `KF` (`KP`) | longueur | `F` × 1, 100, 1000 | P+A |
| `L`, `CL` | longueur-unité | `L` × 1, 100 | P |
| `RL`, `PR` | rouleau, paire | — | P |
| `BO`, `PG` (`PQ`) | **paquet** (`Package = 1`) | conversion par `QPP` (`fn_UM_GetRatioDeConversion`, 1/QPP) | P |
| `LB`, `CB`, `KG`, `CK` | poids | `LB` × 1, 100 ; `KG` × 1, 100 | P |

Un `TEMPUNI = 0.25` avec `TEMPUM = 'C'` veut dire 0,25 h **par centaine** ; le calcul divise par le ratio (`CALCUL-SOUMISSION.md`
§3, §6). Les distributeurs livrent `COUUM` et `TEMPUM` (§3.1), donc **l'unité du temps est dictée par la liste de prix,
la valeur du temps par l'entrepreneur**.

---

## 8. Réponses courtes

- **D'où viennent les prix ?** D'un fichier/URL de distributeur chargé ligne par ligne dans `PriceUpdate_Products` puis
  fusionné par `up_PriceUpdate_UpdateProducts`. Pour Wolseley, brut+escompte+net arrivent ensemble. Pour Rexel et
  Sonepar (donc Lumen = DR), la liste n'apporte que l'article et son brut à la création ; le **prix net** est mis à jour
  séparément via `up_PRODUITS_Update` (`PROMCOUNET`, `DATECOUNET`).
- **D'où viennent les temps de main-d'œuvre ?** **Jamais du distributeur.** `TEMPUNI` n'existe pas dans
  `PriceUpdate_Products` ; il n'est écrit que par `up_PRODUITS_Update`, `up_ENSEMBLE_Update` et les copies vers
  `SOUPRO`/`SOUENS` (`catalogue_checks.log` §5). Les temps de DR sont la propriété de DR, dans `PRODUITS.TEMPUNI` et
  `ENSEMBLE.TEMPUNI/TEMPSEC` de la base vivante.
- **Que sont les `ENS…` du QPL ?** `ENSEMBLE.ENS_ID` (20 car.). **`19PE0.75 #12` ?** `ENSEMBLE.CLEPERS`, la clé
  personnelle de Dupuis, non unique. **`LQE008445` / `HOFASE884` ?** `PRODUITS.PRO_ID` / `PRODUITS.CLEMANU` d'un produit
  Lumen (prouvé par `PROCORRESP`, 14/16).
- **Que faut-il pour chiffrer un QPL ?** Un export de la base vivante de DR limité à `ENSEMBLE`, `ENSCOMPO`, `PRODUITS`
  (et `Sys_Units*` déjà ici). Avec `ENS_ID` en clé, chaque tracé et chaque marque des 30 projets liés reçoit coût brut,
  net, temps — sans rien deviner.

---

## 9. Fichiers

- `eewin/examples/catalogue_checks.sql` — les 8 requêtes citées, rejouables.
- `eewin/examples/catalogue_checks.log` — leur sortie sur la base vivante (2026-09-27).
- `eewin/docs/CALCUL-SOUMISSION.md` — les formules appliquées aux copies `SOUPRO`/`SOUENS`.
