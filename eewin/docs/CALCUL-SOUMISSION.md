# EEWin — comment une soumission est calculée (mathématique des procédures SQL)

Source : base `EE` reconstruite à partir des 52 scripts officiels de Dupuis (`eewin/scripts/`, chargeur `eewin/run.sh`,
0 erreur : 60 tables, 160 procédures, 18 fonctions). Tout ce qui suit a été lu dans `sys.sql_modules`
(`OBJECT_DEFINITION`) et dans `INFORMATION_SCHEMA` sur la base vivante (SQL Server 2022, conteneur `eewin`), puis
prouvé par une soumission synthétique passée dans les procédures officielles (section 9, script
`eewin/examples/worked_example.sql`, sortie `eewin/examples/worked_example.log`).

Vérification adversariale du 2026-09-27 : chaque numéro de ligne, colonne, formule et valeur ci-dessous a été recontrôlé
sur la base vivante (`OBJECT_DEFINITION` des 178 modules, `INFORMATION_SCHEMA`, rejeu intégral de `worked_example.sql` →
sortie identique octet pour octet au `.log`) ; les mentions « exécuté » renvoient à des tests supplémentaires rejoués
puis nettoyés par `cleanup_example.sql` (14 compteurs à 0).

Convention de citation : `nom_de_procédure l. N` = ligne N du texte retourné par `OBJECT_DEFINITION` (fichier
`sys.sql_modules`, ligne 1 vide, `CREATE PROCEDURE` en ligne 2). Pour `sp_SOU_CalculTotaux`, la version vivante est celle
de `V36_UpdateDatabase.sql` (ligne 100 = `CREATE PROCEDURE`) : ligne script = ligne module + 98.

---

## 1. Inventaire : ce qui calcule et ce qui ne calcule pas

178 modules lus (`SELECT o.type, o.name FROM sys.sql_modules m JOIN sys.objects o …` : 160 `P`, 17 `FN`, 1 `TF`).
Recensement par `grep` sur les 178 définitions :

- l'arithmétique **coût / vendant / taxe** (`COUESC / 100`, `PROFIT / 100`, lecture de `TAXDEF.TAUXPRV*`, appel de
  `fn_CastAE`) n'existe que dans **2** modules : `sp_SOU_CalculTotaux` et `sp_FAC_CalculTotaux` ;
- l'arithmétique de **quantités** (appel de `fn_UM_GetRatioDeConversion`) existe dans **16** modules : les 2 précédents,
  les 6 `sp_{SOU,FAC}_UpdateQteTotal{Oth,Ens,Lots}_v2`, les 6 de l'ancienne chaîne V1 (`sp_SOUPRO_Quantity`,
  `sp_SOU_CalculQteTotalItem`, leurs jumeaux FAC et les doublons nommés littéralement `dbo.sp_SOUPRO_Quantity`,
  `dbo.sp_SOU_CalculQteTotalItem`), plus `fn_GetQuantyProductIn` et `fn_GetProductCompositionConcat` qui recalculent la
  quantité d'un composant pour l'afficher (même formule `QTE / DIV × ratio` qu'au §4, `fn_GetQuantyProductIn` l. 18-25) ;
- les autres sont des `up_<TABLE>_Update` / `up_<TABLE>_Delete` (INSERT/UPDATE/DELETE champ à champ), des copies
  (`up_CopySoumis_Full`, `up_CopySouBlocDiv`, `up_CloneRecords`), des descriptions (`fn_CompositionConcat`,
  `sp_CalculUsage_*`), la mise à jour de liste de prix (`up_PriceUpdate_*`) et la gestion de session/licence.

| Rôle | Module (côté soumission) | Jumeau facture | Défini dans |
|---|---|---|---|
| **Totaux d'une soumission** (coûtant, vendant, TVP, heures, montants taxables) | `sp_SOU_CalculTotaux` | `sp_FAC_CalculTotaux` | `V36_UpdateDatabase.sql` l. 100 / l. 721 |
| Cumul des quantités de produits (relevé → `SOUPRO.QTEOTH/QTEENS/QTELOT`) | `sp_SOUPRO_Quantity_V2` → `sp_SOU_UpdateQteTotalOth_v2`, `sp_SOU_UpdateQteTotalEns_v2`, `sp_SOU_UpdateQteTotalLots_v2` | `sp_FACPRO_Quantity_V2` + `_v2` FAC | `V30_UpdateDatabase.sql` l. 483, 90, 351 ; `V39_UpdateDatabase.sql` l. 83 (Ens_v2) |
| Ancienne version (curseurs, V1) du cumul — **cassée sur cette base** | `sp_SOUPRO_Quantity` → `sp_SOU_CalculQteTotalItem` → `EXEC dbo.sp_SOU_UpdateQteTotal{Oth,Ens,Lots}` (l. 42-46) ; ces trois procédures n'existent que sous le nom littéral `dbo.sp_SOU_UpdateQteTotal…` (schéma `dbo`, nom contenant le point), donc l'appel échoue : `Msg 2812 Could not find stored procedure 'dbo.sp_SOU_UpdateQteTotalOth'` (exécuté) | idem FAC (noms sans point, non testés) | renommées par `sp_rename` dans `V24_UpdateDatabase.SQL` l. 6-41 |
| Arrondi | `fn_CastAE(@Input DECIMAL(18,6), @Precision INT)` = `ROUND(@Input, @Precision)` | — | `V30_UpdateDatabase.sql` l. 10 |
| Multiplicateur de bloc | `fn_MultBlock(@SOU_ID, @BLO_ID_REL INT)` → `SOUBLO.MULT` (1 si absent) | — | `V30_UpdateDatabase.sql` l. 27 |
| Unités | `fn_UM_GetRatioDeConversion` (`V21` l. 5), `fn_UM_GetUniteDeBase` (`V21` l. 87), `fn_UM_GetNatureUnite` (`V38` l. 6) | — | `V21_UpdateDatabase.sql`, `V38_UpdateDatabase.sql` |
| Variante « Calgary » (coût rendu `LC`) | `EE_Calgary()` = 1 si la colonne `PRODUITS.LC` existe | — | `V22_UpdateDatabase.sql` l. 813 |

**Ce qui n'est PAS calculé en SQL** (vérifié par `grep` sur les 178 définitions) :

- Le sommaire de la soumission stocké dans `SOUMIS` — `MATCOUTREL, MATCOUTLOT, MATVENDCAL, MATPORTTVP, SERCOUTCAL,
  SERVENDCAL, SERHRESCAL, AUTCOUTCAL, MATCOUTMO, MATADMPC/MO, MATPROFPC/MO, GLOBAJUPC/MO, GLOBAJU2PC/MO, TOTTAXFED,
  TOTTAXPRV, TAUXMD, MATTOTALMD, MATPROFDEF, TYPEPROF` — n'apparaît que dans `up_SOUMIS_Update` (paramètres l. 50-127)
  et `up_FACTURES_Update`. Aucune procédure ne les dérive : administration %, profit % du sommaire, ajustements globaux,
  taxes fédérale/provinciale finales et coût de main-d'œuvre (`heures × TAUXMD`) sont calculés par l'application
  (Delphi — cf. commentaire « TO_CopyPaste en Delphi », `up_CopySoumis_Full` l. 32) et **écrits** dans `SOUMIS`.
- `MULCOM` (multiple de commande), `FRAIS.*`, `TAUX.*`, `CLITAUX.*`, `PROFGRID.*`, `SOUREL.PROFITPLUS/PROFITMOIN`,
  `PRODUITS.PROFIT`, `SOUENS.PROFIT`, `SOULOTS.PROFIT` : stockés/copiés seulement, jamais lus par un calcul SQL.
  Le seul profit qui compte en SQL est **`SOUREL.PROFIT`** (par ligne de relevé).

---

## 2. Modèle de données utilisé par le calcul

Toutes les tables `SOU*` sont clés par `SOU_ID` (`varchar(20)`) ; **aucune clé étrangère** (`sys.foreign_keys` = 0 ligne).
Tables (définitions dans `CreateTables.sql`) :

| Table | Rôle | Colonnes lues par le calcul |
|---|---|---|
| `SOUMIS` (l. 692) | entête de soumission | `TAX_ID` (colonne l. 799 ; lue par `sp_SOU_CalculTotaux` l. 144) ; reçoit `MATTAXAB1..5`, `SERTAXAB1..5`, `AUTTAXAB1..5`, `CALCTIMSTP` |
| `SOUREL` (l. 851) | **lignes du relevé** : la quantité comptée sur les plans | `TYPERELEVE` (`P` matériel → `MATTAXAB*`, `S` service → `SERTAXAB*`, `O` autre → `AUTTAXAB*`, d'après `sp_SOU_CalculTotaux` l. 526-555), `TYPEITEM` (`P` produit lu dans `SOUPRO` par `PRO_ID = ITEM_ID`, l. 200-202 ; `N` traité exactement comme `P`, l. 189 — sens « produit non catalogué » [non vérifié] ; `A` ensemble = `SOUENS.ENS_ID`, l. 266 ; `L` lot = `SOULOTS.LOTS_ID`, l. 317 ; `T` ligne ignorée par le calcul, l. 343 — sens « titre » [non vérifié] ; `S` service et `O` autre : coût = `COUTANBRUT`, l. 353-356), `ITEM_ID`, `BLO_ID`, `DIV_ID`, `ORDRE`, `QTE`, `QTEUM`, `SECTION`, `PROFIT`, `TYPETAXE`, `COUTANBRUT` |
| `SOUPRO` (l. 820) | copie « dans la soumission » des produits | `COUBRUTUNI` (coût brut unitaire), `COUUM` (unité du coût), `COUESC` (escompte %), `PROMCOUNET` (coût net spécial/promo), `QPP` (qté par paquet), `TEMPUNI`, `TEMPUM` (temps d'installation unitaire + unité) ; reçoit `QTEOTH/QTEENS/QTELOT`, `UnitSelling`, `CODEIMPR`, `CALCTIMSTP`. La colonne `LC` (coût rendu, variante Calgary) **n'existe dans aucune table de cette base** (`INFORMATION_SCHEMA.COLUMNS`, 0 ligne) : la procédure travaille sur une copie `#SOUPRO_TEMP` (l. 115) à laquelle elle ajoute une colonne `LC` vide quand `@EE_CALGARY = 0` (l. 118-121) |
| `SOUENS` (l. 617) / `SOUENSCO` (l. 638) | ensembles (assemblies) et leurs composants | `SOUENS.COUUM, TEMPUNI, TEMPSEC, TEMPUM` ; `SOUENSCO.PRO_ID, QTE, QTEUM, TYPRATIO, DIV, DIVUM` |
| `SOULOTS` (l. 654) / `SOULOTSCO` (l. 679) | lots et composants | `SOULOTS.COUUM, TEMPUNI, TEMPUM, COUTANTSEL, COUTANT1..4` ; `SOULOTSCO.PRO_ID, QTE, QTEUM` |
| `SOUBLO` (l. 596) | blocs | `MULT` (`int`) — multiplicateur appliqué aux lignes `P` |
| `SOUDIV` (l. 607) | divisions | aucune colonne lue par le calcul (regroupement) |
| `SOUAMD` (l. 585) | facteur main-d'œuvre par bloc × division | `FACTMD` (`float`) |
| `TAXDEF` (l. 904) | définitions de taxes | `CODETAX1..5`, `TAUXPRV1..5`, `TVPSURCPER` (`TAUXFED*` n'est pas lu en SQL) |
| `Sys_Units` (l. 969, 19 lignes) / `Sys_UnitsConversion` (l. 987, 65 lignes) | unités et ratios | voir §6 |

Le catalogue (`PRODUITS`, `ENSEMBLE`, `ENSCOMPO`) n'est **pas** lu par le calcul : c'est la copie `SOUPRO`/`SOUENS`/
`SOUENSCO` figée dans la soumission qui sert (prix au moment de la soumission). Aucune procédure SQL ne fait la copie
catalogue → soumission ; c'est l'application.

Pont avec Plan Expert : dans un `.qpl` de Dupuis, un élément `<EEExchangeData ItemType="A" ItemID="ENS…" Key="…"
PersonalKey="…" …/>` porte les mêmes noms de domaine que `SOUREL.TYPEITEM='A'` / `SOUREL.ITEM_ID` = `SOUENS.ENS_ID`
(`varchar(20)` ; les `ENS…` font 20 caractères). Le QPL de référence `S-1714-Dupuis-PlanExpert.qpl` n'en contient qu'**un
seul** (`ItemType="A" ItemID="ENSCFFFDBD5146159B90" Key="19PE0.75 #12"`). Le recensement `ensembles-ee.csv` compte
**132 lignes = 116 `ItemType="A"` (`ENS…`, ensembles) + 16 `ItemType="P"` (`LQE…`, 9 caractères, produits)**. Le chemin
d'import QPL → SOUREL n'est pas dans les scripts SQL (application), seule la correspondance de noms est constatée.

---

## 3. Étape 1 — coût net unitaire d'un produit (`CoutantNetReel`)

`sp_SOU_CalculTotaux` l. 192-207 (ligne `P`/`N`) :

```sql
SELECT @CoutantNetSpecial = SP.PROMCOUNET,
       @COUBRUTUNI        = ISNULL(SP.COUBRUTUNI, 0.0),
       @COUESC            = ISNULL(SP.COUESC, 0.0),
       ...
IF @CoutantNetSpecial > 0
  SET @CoutantNetReel = @CoutantNetSpecial
ELSE
  SET @CoutantNetReel = @COUBRUTUNI - (@COUBRUTUNI * (@COUESC / 100.0));
```

> **CoutantNet = PROMCOUNET si > 0, sinon COUBRUTUNI × (1 − COUESC/100)**, exprimé par unité `COUUM`.

`SP` est `#SOUPRO_TEMP`, copie des lignes `SOUPRO` de la soumission (l. 115, 200). La même expression est répétée pour
les composants d'ensemble (l. 230-233, 239-242) et de lot (l. 295-298).
En mode Calgary (`@EE_CALGARY = 1`) le coût unitaire utilise `SP.LC` (landed cost) à la place (l. 360-366) ; sur cette
base `dbo.EE_Calgary()` retourne 0 (pas de colonne `PRODUITS.LC`, `EE_Calgary` l. 8-15) et appeler `sp_SOU_CalculTotaux`
avec `@EE_CALGARY = 1` échoue : `Msg 207 Invalid column name 'LC'` (exécuté ; la colonne n'est ajoutée à `#SOUPRO_TEMP`
que si `@EE_CALGARY = 0`, l. 118-121).

---

## 4. Étape 2 — coût d'un ensemble (`TYPEITEM = 'A'`)

`sp_SOU_CalculTotaux` l. 218-272. Chaque composant `SOUENSCO` est classé par `TYPRATIO` :

- **`TYPRATIO = 'L'`** (composant « linéaire », proportionnel à la quantité d'ensemble) → entre dans `CoutantNetReel`.
  Sa quantité par ensemble (l. 220-227) :
  ```sql
  CASE WHEN (SEC.TYPRATIO = 'L') AND (SE.COUUM != '') AND (fn_UM_GetNatureUnite(SE.COUUM) = 'L')
       THEN CASE WHEN ISNULL(SEC.DIV,0.0) != 0
                 THEN (ISNULL(SEC.QTE,0.0) / SEC.DIV) * fn_UM_GetRatioDeConversion(SE.COUUM, SEC.DIVUM, 0)
                 ELSE 0 END
       ELSE SEC.QTE END AS QTE_cmp
  ```
  > Si l'ensemble se mesure en longueur (`SOUENS.COUUM` de nature `L`, ex. `F`), la quantité du composant est
  > **QTE / DIV × ratio(COUUM_ensemble → DIVUM)** — « QTE unités de composant par DIV unités d'ensemble » ; sinon
  > (ensemble à l'unité) c'est simplement `SEC.QTE`.
- **`TYPRATIO ≠ 'L'`** (composant « par section ») → entre dans `CoutantNetSection`, quantité `SEC.QTE`, et incrémente
  `DivisibleEnSections` (l. 255-258).

Agrégation (l. 268-271) :

```sql
@CoutantNetReel    = SUM(fn_CastAE(QTE_cmp * CoutantNetReel_cmp    * fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp, QPP_cmp), 2))
@CoutantNetSection = SUM(          QTE_cmp * CoutantNetSection_cmp * fn_UM_GetRatioDeConversion(QTEUM_cmp, COUUM_cmp, QPP_cmp))
@DivisibleEnSections = SUM(DivisibleSection_cmp)
```

> **CoûtNet(ensemble) = Σ_L arrondi₂(QTE_cmp × CoûtNet(produit) × ratio(QTEUM_cmp → COUUM_produit))**
> **CoûtSection(ensemble) = Σ_{non L} QTE_cmp × CoûtNet(produit) × ratio(…)** (non arrondi par composant).

Le temps d'installation de l'ensemble (l. 276-285) ne vient **que** de `SOUENS` — le `TEMPUNI` des produits composants
n'est pas lu pour un ensemble :

```sql
@TempsInstallationSection = SE.TEMPSEC,
@TempsInstallationTotal   = @QTE * SE.TEMPUNI * fn_UM_GetRatioDeConversion(@QTEUM, SE.TEMPUM, @QPP)   -- @QPP remis à 0 l. 274
...
IF (@DivisibleEnSections > 0)
  SET @TempsInstallationTotal = @TempsInstallationTotal + (@TempsInstallationSection * @SECTION);
```

> **Heures(ligne A) = QTE × SOUENS.TEMPUNI × ratio(QTEUM → TEMPUM) + SECTION × SOUENS.TEMPSEC** (le second terme
> seulement si l'ensemble a au moins un composant « par section »).

---

## 5. Étape 2 bis — coût d'un lot (`TYPEITEM = 'L'`)

`sp_SOU_CalculTotaux` l. 292-338 : même somme que l'ensemble mais sans notion de section
(`@CoutantNetReel = SUM(fn_CastAE(QTE_cmp × CoûtNet × ratio, 2))`, l. 319), puis **un coût forcé peut remplacer la somme** :

```sql
@CoutantNetReel = CASE WHEN SL.COUTANTSEL = 1 THEN SL.COUTANT1
                       WHEN SL.COUTANTSEL = 2 THEN SL.COUTANT2
                       WHEN SL.COUTANTSEL = 3 THEN SL.COUTANT3
                       WHEN SL.COUTANTSEL = 4 THEN SL.COUTANT4
                       ELSE @CoutantNetReel END
```

Heures du lot (l. 326) : `@QTE × SL.TEMPUNI × ratio(@QTEUM → SL.TEMPUM)` — là encore, pas le `TEMPUNI` des composants.

Anomalie relevée dans le jumeau facture `sp_FAC_CalculTotaux` (diff des deux définitions) : `WHEN SL.COUTANTSEL = 4 THEN
SL.COUTANT3` et le `ELSE @CoutantNetReel` est commenté → côté facture, un lot avec `COUTANTSEL` hors 1-4 a un coût `NULL`.

---

## 6. Unités : `fn_UM_GetRatioDeConversion(@UMDE_ID, @UMA_ID, @QPP)`

Définition (`V21_UpdateDatabase.sql` l. 5 ; module l. 6-30) :

```sql
IF ((@UMDE_ID = 'PG') OR (@UMDE_ID = 'BO')) AND (@UMA_ID = 'U') RETURN 0;
SELECT @UNITTOUNIT = P.UNITTOUNIT, @UNITTOPACKAGE = P.UNITTOPACKAGE, @PACKAGETOUNIT = P.PACKAGETOUNIT, @RATIO = P.RATIO
FROM SYS_UNITSCONVERSION P WHERE P.UNITFROM = @UMDE_ID AND P.UNITTO = @UMA_ID;
SET @R = CASE WHEN @PACKAGETOUNIT = 1 THEN CASE WHEN @QPP = 0 THEN 0 ELSE 1.0 / @QPP END
              WHEN @UNITTOUNIT = 1 THEN @RATIO
              ELSE 0 END;
```

> ratio(de → à) = `Sys_UnitsConversion.RATIO` si les deux unités sont dans le même groupe de compatibilité ;
> **1/QPP** pour unité → paquet (`U → PG`, `U → BO`) ; **0 dans tous les autres cas** (paquet → unité, ou aucune ligne).

Conséquences vérifiées sur la base (`worked_example.log` §9) : `F → CF = 0.01`, `F → F = 1`, `U → U = 1`,
**`F → C = 0`** (`C` = centaine d'unités, `Sys_Units.CompatibilityGroup` A ; `F` = pied, groupe B : aucune ligne
`Sys_UnitsConversion` entre les deux). Un produit dont `COUUM` n'est pas du même groupe que la `QTEUM` du relevé ou du
composant a donc un **coût de 0 sans aucune erreur**. Conséquence : un fil compté en `F` doit avoir un `COUUM` du groupe B
(`F`, `CF`, `KF`, `M`, `HM`, `KM`) ; avec `C`/`K` (groupe A) le ratio est 0.

`Sys_Units` (19 lignes) : `Type` = `U` (comptage) ou `L` (longueur) — c'est ce que retourne `fn_UM_GetNatureUnite` ;
`BaseUnitCodeEN` = unité de base du groupe (`U` pour `C`,`K` ; `F` pour `CF`,`KF` ; `M` pour `HM`,`KM` ; `LB` pour `CB` ;
`KG` pour `CK` ; `L` pour `CL`) — c'est ce que retourne `fn_UM_GetUniteDeBase`. Unités : `U C K F CF KF M HM KM L CL
RL PR BO PG LB CB KG CK`.

Le paramètre `@QPP` de `fn_UM_GetRatioDeConversion` est lui-même déclaré `INT` (l. 2), comme `@QPP` dans
`sp_SOU_CalculTotaux` (l. 46) et `@QPP_SOUPRO` dans `sp_SOU_CalculQteTotalItem` (l. 5), alors que `SOUPRO.QPP` est `float`
(`INFORMATION_SCHEMA.COLUMNS`) : une quantité par paquet fractionnaire est tronquée à l'entier partout où la fonction est
appelée (`SELECT @i = 1.5` avec `@i INT` → 1, exécuté).

---

## 7. Étape 3 — coûtant, vendant, TVP d'une ligne de relevé

Boucle sur `SOUREL` (l. 150-157) : `WHERE SOU_ID = @SOU_ID AND TYPERELEVE = @TypeReleve ORDER BY SOU_ID, TYPERELEVE,
BLO_ID, DIV_ID, ORDRE`. Les lignes `TYPEITEM = 'T'` (titres) sont ignorées (l. 343).

Paramètres d'appel (l. 2-8) : `@TypeReleve` (`P`/`S`/`O`), `@EE_CALGARY`, `@ModeCalcul` (`C` = majoration sur coût,
`G` = marge brute), `@VendantUAvantVendantT` (1 = arrondir le vendant unitaire puis multiplier, 0 = arrondir le vendant
total puis diviser), `@VPM` (précision d'arrondi du vendant unitaire), `@DoLog`.

### 7.1 Coûtant

```sql
IF ((@TypeReleve = 'S') AND (@TypeItem = 'S')) OR ((@TypeReleve = 'O') AND (@TypeItem = 'O'))
  SET @CoutantUnitaire = @COUTANBRUT;                                          -- l. 353-356
ELSE
  SET @CoutantUnitaire = @CoutantNetReel * fn_UM_GetRatioDeConversion(@QTEUM, @COUUM, @QPP);   -- l. 365
SET @CoutantTotal = fn_CastAE(@QTE * @CoutantUnitaire, 2);                   -- l. 369
IF (A) AND (@DivisibleEnSections > 0)
  SET @CoutantTotal = fn_CastAE(@CoutantTotal + (@SECTION * @CoutantNetSection), 2);           -- l. 371-372
```

> **CoûtantUnitaire = CoûtNet × ratio(QTEUM_relevé → COUUM_item)** (pour `S`/`O` : `SOUREL.COUTANBRUT` tel quel)
> **CoûtantTotal = arrondi₂(QTE × CoûtantUnitaire) [+ arrondi₂(SECTION × CoûtSection)]**

### 7.2 Vendant (profit de la ligne = `SOUREL.PROFIT`, en %)

```sql
IF (@DivisibleEnSections = 0) AND ((@VendantUAvantVendantT = 1) OR (@QTE = 0))
  @VendantUnitaire = CASE WHEN @ModeCalcul = 'C' THEN fn_CastAE(@CoutantUnitaire * (1.0 + (@PROFIT / 100.0)), @VPM)
                          WHEN @ModeCalcul = 'G' AND @PROFIT < 100 THEN fn_CastAE(@CoutantUnitaire / (1.0 - (@PROFIT / 100.0)), @VPM)
                          ELSE 0 END
  @VendantTotal = fn_CastAE(@QTE * @VendantUnitaire, 2)                                       -- l. 382-394
ELSE
  @VendantTotal = CASE WHEN 'C' THEN fn_CastAE(@CoutantTotal * (1.0 + (@PROFIT / 100.0)), 2)
                       WHEN 'G' AND @PROFIT < 100 THEN fn_CastAE(@CoutantTotal / (1.0 - (@PROFIT / 100.0)), 2) ELSE 0 END
  @VendantUnitaire = fn_CastAE(@VendantTotal / @QTE, 2)                                       -- l. 399-407
```

> Mode `C` : **Vendant = Coûtant × (1 + PROFIT/100)** ; mode `G` : **Vendant = Coûtant / (1 − PROFIT/100)** (0 si
> PROFIT ≥ 100). Un ensemble « avec sections » passe toujours par la branche total-puis-unitaire.

### 7.3 TVP sur coût (taxe provinciale non récupérable incluse dans le prix)

Taux (l. 414-425) : `SOUREL.TYPETAXE` est cherché dans `TAXDEF.CODETAX1..5` du `SOUMIS.TAX_ID` ; le taux est le
`TAUXPRV{i}` correspondant, l'index `i` sert au cumul taxable. Si `TAXDEF.TVPSURCPER = 1` (l. 436) :

```sql
-- ensemble avec sections : unitaire = 0, total = fn_CastAE(@VendantTotal + (@CoutantTotal * (@TaxeProv / 100.0)), 2)     -- l. 438-441
-- sinon, unitaire d'abord :  @VendantUnitaireIncluantTVP = fn_CastAE(@VendantUnitaire + (@CoutantUnitaire * (@TaxeProv / 100.0)), @VPM)
--                            @VendantTotalIncluantTVP    = fn_CastAE(@QTE * @VendantUnitaireIncluantTVP, 2)                 -- l. 444-447
-- sinon, total d'abord :     @VendantTotalIncluantTVP    = fn_CastAE(@VendantTotal + (@CoutantTotal * (@TaxeProv / 100.0)), 2)
--                            @VendantUnitaireIncluantTVP = fn_CastAE(@VendantTotalIncluantTVP / @QTE, @VPM)                 -- l. 449-451
```

> **VendantTVP = Vendant + Coûtant × TAUXPRV/100** — la TVP est calculée sur le **coûtant**, pas sur le vendant.

Deux effets de bord prouvés par exécution (mêmes données qu'au §9) :

- **`TAXDEF.TVPSURCPER = 0`** : les deux `…IncluantTVP` restent à 0 (l. 433-434), donc `fCoutPortionTVP = (0 −
  VendantTotal) × MULT` (l. 462) : la « portion TVP » retournée vaut **moins le vendant** (log : `fCoutPortionTVP =
  -448.80` pour PRISE, −506,40, −117,00, −127,66). `UnitSelling` reçoit alors le vendant unitaire hors TVP (l. 589-592).
- **`TYPETAXE` absent de `CODETAX1..5`** : `@TaxeProv` et `@INDEXTAX` ne sont pas remis à zéro à chaque ligne (déclarés
  l. 58-59, assignés seulement quand la CTE l. 414-423 trouve une ligne ; le `IF … IS NULL` l. 425 ne couvre que la
  première ligne du curseur). Une ligne avec un code inconnu **hérite du taux et de l'index de la ligne précédente** :
  `ZZP-RECEP` passé à `TYPETAXE='Z'` a été taxé à 9,975 % et cumulé dans `MATTAXAB1` (log : `TaxeProv 9.975`,
  `MATTAXAB1 = 1199.86` inchangé).

### 7.4 Cumul par ligne, blocs et main-d'œuvre (l. 459-481)

```sql
IF (@TypeReleve = 'P') AND (@TypeItem IN ('P','N','A','L'))
  @fCout           =  @CoutantTotal * @MULT_BLOC;
  @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal) * @MULT_BLOC;
  @fVendant        =  @VendantTotal * @MULT_BLOC;
  @fLaborTotal     =  @fLaborTotal + (@TempsInstallationTotal * @LaborFactor * @MULT_BLOC);
ELSE IF (S,S)  @fCout = @CoutantTotal; @fVendant = @VendantTotal; @fLaborTotal = @fLaborTotal + @QTE;
ELSE IF (O,O)  @fCout = @CoutantTotal; @fVendant = @VendantTotal; @fCoutPortionTVP = (@VendantTotalIncluantTVP - @VendantTotal);
@fCoutantTotal += @fCout;  @fCoutantTotalPortionTVP += @fCoutPortionTVP;  @fVendantTotal += @fVendant;
```

> `MULT_BLOC` = `SOUBLO.MULT` du bloc de la ligne (1 si absent, l. 173-177) — **appliqué aux lignes matériel seulement**,
> pas aux services ni aux autres. `LaborFactor` = `SOUAMD.FACTMD` du couple bloc × division (1 si absent, l. 180-185).
> Pour un relevé `S`, `fLaborTotal` cumule directement la `QTE` (heures) de la ligne.

Deux troncatures dues aux déclarations (l. 38-39) : `@MULT_BLOC INT` (cohérent, `SOUBLO.MULT` est `int`) mais
**`@LaborFactor INT` alors que `SOUAMD.FACTMD` est `float`** : un facteur 1,5 devient 1 (prouvé : `SELECT @i = 1.5` →
1, et dans l'exemple la ligne à 1 h × 1,5 × 2 donne `fLaborTotal = 2`). Un facteur de main-d'œuvre fractionnaire est
donc sans effet en SQL.

### 7.5 Montants taxables et prix de vente unitaire

- Cumul par index de taxe (l. 488-492) : `@MontantTax{i} += @fVendant` (vendant **hors** portion TVP, après `MULT_BLOC`),
  puis écrit dans `SOUMIS.MATTAXAB1..5` / `SERTAXAB1..5` / `AUTTAXAB1..5` selon `@TypeReleve` (l. 526-555).
- `SOUPRO.UnitSelling` (l. 565-602) : `MAX(VendantUnitaire[IncluantTVP])` par `ITEM_ID` de la table `@Log` ; or `@Log`
  n'est alimentée que si `@DoLog = 1` (l. 496-510). **Avec `@DoLog = 0`, `UnitSelling` n'est jamais mis à jour** (prouvé :
  après un appel `@DoLog = 0`, `UnitSelling` reste `NULL` pour les 5 produits ; après un appel `@DoLog = 1` en mode `G`,
  `ZZP-RECEP` passe à 13,76). La condition est écrite `IF NOT EXISTS (SOUPRO …) UPDATE SOUPRO SET UnitSelling = -1 …
  ELSE UPDATE … SET UnitSelling = …` : la branche `-1` ne met donc jamais rien à jour, et seuls les produits
  **directement en ligne de relevé** reçoivent une valeur (les composants d'ensemble restent `NULL` — vérifié §9).
- Retour (l. 608-611) : `fCoutantTotal, fCoutantTotalPortionTVP, fVendantTotal, fLaborTotal` — c'est ce que
  l'application range ensuite dans `MATCOUTREL / MATPORTTVP / MATVENDCAL / MATTOTALMD` (ou `SER*`, `AUT*`) de `SOUMIS`.

---

## 8. Quantités de produits à commander (`sp_SOUPRO_Quantity_V2`)

`sp_SOUPRO_Quantity_V2` (l. 34-36) enchaîne `sp_SOU_UpdateQteTotalOth_v2`, `…Ens_v2`, `…Lots_v2` qui recalculent
`SOUPRO.QTEOTH`, `QTEENS`, `QTELOT` (quantité venant des lignes produit, des ensembles, des lots) **dans l'unité de base
de `COUUM`** :

- Produits en ligne directe (`Oth_v2` l. 19-30) :
  `New_QTE = Σ [SR.QTE × fn_MultBlock(SOU_ID, BLO_ID)] × ratio(SR.QTEUM → fn_UM_GetUniteDeBase(SP.COUUM), SP.QPP)`
- Ensembles (`Ens_v2` l. 18-29) :
  ```sql
  SUM((CASE WHEN CMP1.TYPRATIO = 'L'
            THEN CAST(CMP1.QTE_ENSCO * fn_UM_GetRatioDeConversion(SR.QTEUM, CMP1.COUUM, 0) AS NUMERIC(18,3)) * SR.QTE
            ELSE CMP1.QTE_ENSCO * SR.SECTION END) * dbo.fn_MultBlock(SR.SOU_ID, SR.BLO_ID))
  ```
  puis `× ratio(QTEUM_cmp → base(COUUM_produit), QPP)` (l. 18). `QTE_ENSCO` = même règle QTE/DIV×ratio qu'au §4
  (l. 33-41) ; `CMP1.COUUM` est le `COUUM` de l'**ensemble** (`E.COUUM`, l. 33).
  > composant `L` : **arrondi₃(QTE_composant × ratio(QTEUM_relevé → COUUM_ensemble)) × QTE_relevé × MULT** ; composant
  > « section » : **QTE_composant × SECTION × MULT**. (Dans l'exemple §9 le ratio vaut 1 : `U → U`, `F → F`.)
- Lots (`Lots_v2` l. 24) : `CMP1.QTE × SR.QTE × ratio(SR.QTEUM → L.COUUM) × fn_MultBlock(…)`.

Contraintes révélées par l'exécution :

- `fn_MultBlock(@SOU_ID VARCHAR(20), @BLO_ID_REL INT)` : **`BLO_ID` doit être une chaîne numérique** (`'1'`, `'001'`)
  bien que `SOUREL.BLO_ID`/`SOUBLO.BLO_ID` soient `varchar(3)` — un bloc `'B1'` fait échouer le cumul
  (`Msg 245 … converting the varchar value 'B1' to data type int`, `sp_SOU_UpdateQteTotalOth_v2` l. 55) et **le lot
  entier est abandonné** (erreur de conversion = fin du batch : le nettoyage qui suivait n'a pas tourné, exécuté).
  `sp_SOU_CalculTotaux`, lui, compare `BLO_ID` en `varchar` (l. 173-175) et accepte `'B1'` (exécuté : bloc `B1`,
  `MULT=3` → `MULT_BLOC 3`, `fCout 7.50` pour 1 boîte à 2,50 $).
- Les trois `_v2` font `CLOSE CUR_2 ; DEALLOCATE CUR_2` hors du `IF @REPLACE_FILTER > 0` qui l'a ouvert
  (`Oth_v2` l. 110-111, `Ens_v2` l. 136-137, `Lots_v2` l. 123-124) : appelées avec `@REPLACE_FILTER = 0` elles lèvent
  6 × `Msg 16916 A cursor with the name 'CUR_2' does not exist` (exécuté ; les quantités sont quand même écrites,
  identiques à celles du §9.2). Appeler avec 1 ou 2 — **mais** avec `@REPLACE_FILTER > 0` la branche des codes
  d'impression (`Oth_v2` l. 83-108) fait `EXEC dbo.sp_SOU_CalculCodeImpr` (l. 101) pour chaque `SOUREL.CODEIMPR <> ''`
  (l. 87-91) ; cette procédure n'existe que sous le nom littéral `[dbo].[dbo.sp_SOU_CalculCodeImpr]` (voir §1) →
  `Msg 2812 Could not find stored procedure 'dbo.sp_SOU_CalculCodeImpr'` (exécuté : une ligne `SOUREL` `TYPEITEM='P'`,
  `CODEIMPR='A'`, `@REPLACE_FILTER = 1`, puis supprimée). Les quantités du curseur `CUR_1` (l. 55-78) sont écrites
  avant l'erreur. Donc : `@REPLACE_FILTER = 1 ou 2` **et** `SOUREL.CODEIMPR = ''` sur toutes les lignes, sinon
  `Msg 2812` ; le jumeau facture `sp_FAC_CalculCodeImpr` existe correctement.
- Une ligne dont le total, arrondi à 2 décimales, ne change pas n'est pas réécrite (`CAST(… AS NUMERIC(18,2)) !=`,
  `Oth_v2` l. 42-43) — sauf si `@DoLog = 1` (l. 41), où toutes les lignes sont écrites dans la table `@SOUPROLOG`
  (l. 46-52) au lieu de `SOUPRO`.

---

## 9. Exemple numérique exécuté sur la base vivante

Script : `eewin/examples/worked_example.sql` (tout passe par `up_TAXDEF_Update`, `up_PRODUITS_Update`, `up_ENSEMBLE_Update`,
`up_ENSCOMPO_Update`, `up_SOUMIS_Update`, `up_SOUBLO_Update`, `up_SOUDIV_Update`, `up_SOUAMD_Update`, `up_SOUPRO_Update`,
`up_SOUENS_Update`, `up_SOUENSCO_Update`, `up_SOULOTS_Update`, `up_SOULOTSCO_Update`, `up_SOUREL_Update`, puis
`sp_SOUPRO_Quantity_V2`, `sp_SOU_CalculTotaux` ×5, et nettoyage par `up_DeleteSoumis_Full @DeleteHeader=1`,
`up_TAXDEF_Delete`, `up_PRODUITS_Delete`, `up_ENSEMBLE_Delete`, `up_ENSCOMPO_Delete`). Sortie complète :
`eewin/examples/worked_example.log` (0 `Msg`, tous les compteurs finaux à 0).

### 9.1 Données

Taxe `ZZTX` : `CODETAX1='M'`, `TAUXPRV1=9.975` ; `CODETAX2='S'`, `TAUXPRV2=0` ; `TVPSURCPER=1`.
Soumission `ZZTEST-CALC`, bloc `1` (`MULT=2`), division `1`, `SOUAMD.FACTMD=1.5`.

| Produit (`SOUPRO`) | `COUBRUTUNI` | `COUUM` | `COUESC` | `PROMCOUNET` | coût net (§3) | `TEMPUNI`/`TEMPUM` |
|---|---|---|---|---|---|---|
| ZZP-WIRE (fil #12) | 40,00 | CF | 10 | 0 | 40 × 0,90 = **36,00 $/CF** | 1,5 h / CF |
| ZZP-BOX (boîte) | 3,00 | U | 0 | 2,50 | **2,50 $/U** (promo gagne) | 0,25 h / U |
| ZZP-RECEP (prise) | 12,00 | U | 25 | 0 | 12 × 0,75 = **9,00 $/U** | 0,30 h / U |
| ZZP-EMT (EMT ¾) | 95,00 | CF | 0 | 0 | **95,00 $/CF** | 2,0 h / CF |
| ZZP-STRAP (bride) | 0,80 | U | 0 | 0 | **0,80 $/U** | 0,05 h / U |

Ensembles (`SOUENS`/`SOUENSCO`) :

- `ZZENS-PRISE` (`COUUM='U'`, `TEMPUNI=0.10`, `TEMPSEC=0`) : 1 U BOX (`L`), 1 U RECEP (`L`), 20 F WIRE (`L`).
- `ZZENS-CONDUIT` (`COUUM='F'`, `TEMPUNI=0.05`, `TEMPSEC=0.10`) : 1 F EMT (`L`, DIV 1 F), 3 F WIRE (`L`, DIV 1 F),
  1 U STRAP (`TYPRATIO='S'` → par section).

Lot `ZZLOT-RACK` (`COUUM='U'`, `TEMPUNI=4`, `COUTANTSEL=0`) : 10 U STRAP, 50 F EMT.

Lignes de relevé (`SOUREL`) :

| `TYPERELEVE`/`TYPEITEM` | `ITEM_ID` | `QTE` `QTEUM` | `SECTION` | `PROFIT` | `TYPETAXE` | `COUTANBRUT` |
|---|---|---|---|---|---|---|
| P/A | ZZENS-PRISE | 10 U | 0 | 20 | M | — |
| P/A | ZZENS-CONDUIT | 100 F | 10 | 20 | M | — |
| P/P | ZZP-RECEP | 5 U | 0 | 30 | M | — |
| P/L | ZZLOT-RACK | 1 U | 0 | 15 | M | — |
| S/S | LABOR | 8 U | 0 | 25 | S | 65,00 |
| O/O | PERMIT | 1 U | 0 | 10 | M | 300,00 |

### 9.2 Quantités (`sp_SOUPRO_Quantity_V2`, log §10)

| `PRO_ID` | `QTEENS` | `QTEOTH` | `QTELOT` | calcul (§8) |
|---|---|---|---|---|
| ZZP-BOX | 20 | 0 | 0 | 1 × 10 × 2 |
| ZZP-RECEP | 20 | 10 | 0 | 1 × 10 × 2 ; 5 × 2 |
| ZZP-WIRE | 1000 (F) | 0 | 0 | 20 × 10 × 2 = 400 ; 3 × 100 × 2 = 600 → en unité de base `F` (base de `CF`) |
| ZZP-EMT | 200 (F) | 0 | 100 (F) | 1 × 100 × 2 ; lot 50 × 1 × 2 |
| ZZP-STRAP | 20 | 0 | 20 | section : 1 × 10 × 2 ; lot 10 × 1 × 2 |

### 9.3 Totaux matériel (`sp_SOU_CalculTotaux 'P'`, `ModeCalcul='C'`, `VendantUAvantVendantT=1`, `VPM=2`, log §11a)

**ZZENS-PRISE** : CoûtNet = 2,50 + 9,00 + arrondi₂(20 × 36 × 0,01) = 2,50 + 9,00 + 7,20 = **18,70** ; sections 0.
CoûtantUnitaire 18,70 ; CoûtantTotal 187,00. VendantUnitaire = arrondi₂(18,70 × 1,20) = 22,44 ; VendantTotal 224,40.
TVP : 22,44 + 18,70 × 0,09975 = 24,3053 → 24,31 ; total 243,10. Heures = 10 × 0,10 = 1,0.
Cumul ×MULT 2 : `fCout` 374,00 ; `fCoutPortionTVP` (243,10 − 224,40) × 2 = 37,40 ; `fVendant` 448,80 ;
`fLaborTotal` 1,0 × **1** (1,5 tronqué) × 2 = 2,0. — log : `374.000000|37.400000|448.800000|…|2.000000` ✔

**ZZENS-CONDUIT** : composants `L` par pied : EMT 1 × 95 × 0,01 = 0,95 ; fil 3 × 36 × 0,01 = 1,08 → CoûtNet **2,03 $/F** ;
section : STRAP 1 × 0,80 = **0,80 $/section**, `DivisibleEnSections=1`.
CoûtantTotal = arrondi₂(100 × 2,03) + 10 × 0,80 = 203,00 + 8,00 = **211,00**.
Branche total-d'abord : VendantTotal = 211 × 1,20 = 253,20 ; VendantUnitaire 2,53. TVP (cas sections) : unitaire 0,
total 253,20 + 211 × 0,09975 = 274,247 → 274,25. Heures = 100 × 0,05 + 10 × 0,10 = 6,0.
Cumul ×2 : 422,00 ; 42,10 ; 506,40 ; heures 12 → `fLaborTotal` 14. — log ✔

**ZZP-RECEP ×5** : 9,00 → 45,00 ; vendant 11,70 / 58,50 ; TVP 12,60 / 63,00 ; heures 5 × 0,30 = 1,5.
Cumul ×2 : 90,00 ; 9,00 ; 117,00 ; heures 3 → 17. — log ✔

**ZZLOT-RACK** : 10 × 0,80 + arrondi₂(50 × 95 × 0,01) = 8,00 + 47,50 = **55,50** (`COUTANTSEL=0` → somme conservée) ;
vendant 55,50 × 1,15 = 63,825 → 63,83 ; TVP 63,83 + 55,50 × 0,09975 = 69,366 → 69,37 ; heures 1 × 4 = 4.
Cumul ×2 : 111,00 ; 11,08 ; 127,66 ; heures 8 → 25. — log ✔

**Retour `P`** : `fCoutantTotal 997.00 | fCoutantTotalPortionTVP 99.58 | fVendantTotal 1199.86 | fLaborTotal 25.00` ✔
`SOUMIS.MATTAXAB1 = 1199.86` (index 1 = code `M`).

### 9.4 Service et autre (log §11b, §11c)

- **LABOR** (`S`) : CoûtantUnitaire = `COUTANBRUT` 65 ; total 520 ; vendant 81,25 / 650,00 ; taux `S` → `TAUXPRV2 = 0`
  → portion TVP 0 ; **pas de ×MULT** ; `fLaborTotal = QTE = 8`. Retour `520 | 0 | 650 | 8` ; `SOUMIS.SERTAXAB2 = 650` ✔
- **PERMIT** (`O`) : 300 → 330,00 ; TVP 330 + 300 × 0,09975 = 359,925 → 359,93 ; portion 29,93 ; pas de ×MULT.
  Retour `300 | 29.93 | 330 | 0` ; `SOUMIS.AUTTAXAB1 = 330` ✔

`SOUPRO.UnitSelling` : seul `ZZP-RECEP` = 12,60 (vendant unitaire TVP incluse, car `TVPSURCPER=1`) ; les composants
d'ensemble restent `NULL` (§7.5) ✔

### 9.5 Variantes (log §13, §14)

- `ModeCalcul='G'` : vendant = coûtant / (1 − p). PRISE 18,70/0,8 = 23,375 → 23,38 × 10 × 2 = 467,60 ; CONDUIT 211/0,8
  = 263,75 × 2 = 527,50 ; RECEP 9/0,7 = 12,857 → 12,86 × 5 × 2 = 128,60 ; LOT 55,5/0,85 = 65,294 → 65,29 × 2 = 130,58.
  Total **1254,28** = log ✔ (coûtant et heures inchangés).
- `VendantUAvantVendantT=0` : mêmes vendants, mais TVP calculée sur les totaux : PRISE 224,40 + 18,653 = 243,05 (au lieu
  de 243,10) → portion 37,30 ; RECEP 58,50 + 4,489 = 62,99 → 8,98. `fCoutantTotalPortionTVP` **99,46** (au lieu de 99,58)
  = log ✔. L'ordre d'arrondi change les cents.

---

## 10. Résumé des formules (pour ré-implémentation)

```
CoûtNet(prod)        = PROMCOUNET > 0 ? PROMCOUNET : COUBRUTUNI × (1 − COUESC/100)              [par COUUM]
ratio(a→b, QPP)      = Sys_UnitsConversion.RATIO | 1/QPP (U→paquet) | 0 (sinon)
QTE_cmp(A, 'L')      = nature(COUUM_ens)='L' ? QTE/DIV × ratio(COUUM_ens→DIVUM) : QTE
CoûtNet(A)           = Σ_L arrondi₂(QTE_cmp × CoûtNet(prod) × ratio(QTEUM_cmp→COUUM_prod, QPP))
CoûtSection(A)       = Σ_{¬L} QTE_cmp × CoûtNet(prod) × ratio(…)
CoûtNet(L)           = COUTANTSEL∈1..4 ? COUTANT{sel} : Σ arrondi₂(QTE_cmp × CoûtNet(prod) × ratio(…))
CoûtantUnitaire      = (S,O) ? COUTANBRUT : CoûtNet(item) × ratio(QTEUM_relevé→COUUM_item, QPP)
CoûtantTotal         = arrondi₂(QTE × CoûtantUnitaire) [+ arrondi₂(SECTION × CoûtSection) si A avec sections]
Vendant              = mode C : Coûtant × (1 + PROFIT/100) | mode G : Coûtant / (1 − PROFIT/100)
                       (arrondi VPM sur l'unitaire si VendantUAvantVendantT=1 et pas de sections, sinon arrondi₂ sur le total)
VendantTVP           = Vendant + Coûtant × TAUXPRV{i}/100        (i : TYPETAXE ∈ TAXDEF.CODETAX1..5 ; si TVPSURCPER=1,
                       sinon VendantTVP = 0 et fPortionTVP = −Vendant ; TYPETAXE inconnu → taux/index de la ligne précédente)
Heures(P,N)          = QTE × TEMPUNI_prod × ratio(QTEUM→TEMPUM_prod, QPP)
Heures(A)            = QTE × TEMPUNI_ens × ratio(QTEUM→TEMPUM_ens) + SECTION × TEMPSEC_ens (si sections)
Heures(L)            = QTE × TEMPUNI_lot × ratio(QTEUM→TEMPUM_lot)
Par ligne P          : fCout = CoûtantTotal × MULT ; fVendant = Vendant × MULT ; fPortionTVP = (VendantTVP − Vendant) × MULT ;
                       fLabor += Heures × int(FACTMD) × MULT
Par ligne S          : fCout, fVendant sans MULT ; fLabor += QTE
Par ligne O          : fCout, fVendant, fPortionTVP sans MULT
Taxable{i}           = Σ fVendant des lignes dont TYPETAXE → i   → SOUMIS.{MAT|SER|AUT}TAXAB{i}
Retour               = Σ fCout, Σ fPortionTVP, Σ fVendant, fLabor    (le sommaire de SOUMIS — admin %, profit %, ajustements,
                       TPS/TVQ finales, heures × TAUXMD — est calculé par l'application, pas en SQL)
UnitSelling(prod)    = MAX(VendantUnitaire[TVP]) des lignes P/N du produit — écrit seulement si @DoLog = 1
Qté à commander      : QTEOTH = Σ QTE × MULT × ratio(QTEUM→base(COUUM), QPP)
                       QTEENS = Σ [L : arrondi₃(QTE_cmp × ratio(QTEUM_relevé→COUUM_ens)) × QTE | ¬L : QTE_cmp × SECTION] × MULT × ratio(QTEUM_cmp→base(COUUM), QPP)
                       QTELOT = Σ QTE_cmp × QTE × ratio(QTEUM_relevé→COUUM_lot) × MULT × ratio(QTEUM_cmp→base(COUUM), QPP)
```

## 11. Pièges confirmés par exécution

1. Unité du coût hors du groupe de compatibilité de la quantité (`F` vs `C`) → ratio 0 → coût 0 sans erreur (§6).
2. `BLO_ID` non numérique → `fn_MultBlock` plante le cumul des quantités (§8).
3. `SOUAMD.FACTMD` fractionnaire tronqué à l'entier (`@LaborFactor INT`, §7.4) ; `QPP` fractionnaire tronqué (`@QPP INT`, §6).
4. `sp_SOUPRO_Quantity_V2 @REPLACE_FILTER=0` → `Msg 16916` sur `CUR_2` (§8) ; utiliser 1 ou 2, avec `SOUREL.CODEIMPR = ''` partout (sinon `Msg 2812` sur `dbo.sp_SOU_CalculCodeImpr`, §8).
5. Le temps des produits composants n'entre pas dans les heures d'un ensemble ou d'un lot : seules `SOUENS.TEMPUNI/TEMPSEC`
   et `SOULOTS.TEMPUNI` comptent (§4, §5).
6. `MULT_BLOC` ne s'applique qu'au relevé `P` (§7.4).
7. `UnitSelling` n'est renseigné que pour les produits en ligne directe (§7.5).
8. `sp_FAC_CalculTotaux` : `COUTANTSEL = 4` lit `COUTANT3` et n'a pas de `ELSE` (§5).
9. 7 objets nommés littéralement `dbo.sp_SOU_…` / `dbo.sp_SOUPRO_Quantity` (procédures V1) : effet de `sp_rename 'dbo.x',
   'dbo.y'` dans `V24_UpdateDatabase.SQL` ; la chaîne V1 `sp_SOUPRO_Quantity → sp_SOU_CalculQteTotalItem` plante en
   `Msg 2812` (§1) ; les versions `_v2`/`_V2` sont les seules utilisables.
10. `UnitSelling` n'est écrit que si `sp_SOU_CalculTotaux` est appelée avec `@DoLog = 1` (§7.5).
11. `TVPSURCPER = 0` → `fCoutantTotalPortionTVP` retourné = −Σ vendant ; `TYPETAXE` inconnu → hérite du taux de la
    ligne précédente (§7.3).
12. `@EE_CALGARY = 1` sur une base sans colonne `LC` → `Msg 207 Invalid column name 'LC'` (§3).
