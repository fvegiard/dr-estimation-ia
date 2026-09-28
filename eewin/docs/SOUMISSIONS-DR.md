# Soumissions chiffrées de DR Électrique chargées dans la base `EE`

Date d'exécution : 2026-09-27 (heure de l'Est). Base : SQL Server 2022, conteneur `eewin`, base `EE` rebâtie à partir
des 52 scripts `eewin/scripts/`. Dossier de travail : `eewin/soumissions-dr/`.

Règle suivie : **aucun chiffre inventé**. Chaque valeur écrite en base est copiée d'un document reçu par courriel
(texte conservé dans `eewin/soumissions-dr/<dossier>/`), ou est la sortie du moteur officiel `sp_SOU_CalculTotaux`.
Ce qui n'est pas dans le document est `NULL`.

## 1. Ce que le connecteur Microsoft 365 a réellement livré

Boîte lue : `fvegiard@dreelectrique.com`. Expéditeur filtré : `ddupuis@dreelectrique.com` (Daniel Dupuis, Estimateur Sénior).

| Courriel (objet, date HE) | Pièce jointe | Ce que `read_resource` retourne | Prix trouvés |
|---|---|---|---|
| « S-1844 », 2026-08-26 10:48 | `Soumission_S-1844_LC2000_SAQ_.pdf` (212 641 o) | texte des 3 pages | **1** : forfait 238 744,00 $ avant TPS/TVQ (p. 1) |
| « Fwd: Soumission 1400 Industriel Laprairie », 2026-02-13 08:50 | `1400 Industriel Laprairie.pdf` (65 001 o) + 6 images inline | texte des 11 pages (proposal Siemens `gemmox000_12222500_00_00_M00`) ; le PDF ne porte **aucun prix** | **1**, dans le corps du courriel de Johnny Gemme (Siemens) du 2025-12-22 : « 96 298.36$ (22-24 semaines de livraison après approbation des dessins) » |
| « 1857 », 2026-09-09 09:09 | `S-1857 (27-Août-2026).pdf` (17 478 872 o) ; `Dupuis corriger.zip` (28 611 971 o) | `PDF text extraction failed (likely a scanned, encrypted, or malformed PDF)` ; zip non lisible | **0** |
| « Fwd: LABOMAR PROBIOTIC PROJECT Invitation à soumissionner », 2026-01-16 et 2026-01-19 | `Exhibit_D_-_Rev1-1_Cost_Estimate.xlsx` (25 436 o) | feuille « Bid 1 » : formulaire de soumission du gérant de construction, 47 postes, toutes les cellules « Final Pricing » à 0 | **0** (formulaire vierge ; la fourchette 6–8 M$ du courriel est celle de l'appel d'offres, tous corps de métier) |

Limites précises du connecteur, constatées :

- `read_resource` sur une pièce jointe retourne le **texte extrait**, jamais le binaire. Les `SHA256` des PDF/xlsx
  originaux sont donc **indisponibles** ; `eewin/soumissions-dr/SHA256SUMS` couvre les fichiers texte conservés.
- Le PDF S-1857 (17,5 Mo, probablement des plans scannés) n'est pas extractible ; le zip non plus. **Aucune ligne
  S-1857** n'a pu être chiffrée. Les dossiers locaux `data/dossiers/S-1857` et `S-1857-v3` sont des relevés de
  quantités (QPL, xlsx), sans prix.
- La cotation Siemens n'est **pas une soumission DR** : c'est un prix d'achat fournisseur (via FRANKLIN EMPIRE INC,
  Longueuil) pour une entrée électrique au 1400 Industriel, La Prairie (bâtisse de GE). Aucun numéro S- n'existe.

Total : **2 lignes chiffrées** (`lignes.csv`, colonnes `total_$` renseignées) + 15 composants du SB2 sans prix
unitaire (listés dans `lignes.csv` avec prix vides, non chargés).

## 2. Modélisation dans `EE` (chemin officiel uniquement)

Toutes les écritures passent par les procédures `up_*_Update` (`eewin/scripts/CreateScripts.sql`, dernières versions
V3/V6/V11/V15/V22/V41) et par les moteurs `sp_SOUPRO_Quantity_V2` / `sp_SOU_CalculTotaux` (V36:100). Script :
`eewin/soumissions-dr/load_dr_submissions.sql` ; contre-script : `unload_dr_submissions.sql` (`up_DeleteSoumis_Full`
V3:1660, `up_ENSEMBLE_Delete`, `up_CLIENTS_Delete`) ; contrôle : `verify_dr_submissions.sql`.

### 2.1 S-1844 — forfait sans détail

| Table (procédure) | Clé | Valeurs copiées du document | Source |
|---|---|---|---|
| `CLIENTS` (`up_CLIENTS_Update`, CreateScripts.sql:66) | `CLI_ID='LC2000'` | `NOMCIE='LC 2000'`, `CONTACT='Tibor Demeter, Chef estimateur'`, `RUE1='4045, rue Lavoisier'`, `VILLE='Boisbriand'`, `CODEPOSTAL='J7H 1N1'`, `PROVINCE='Québec'`, `EMAIL='tdemeter@LC2000.com'` | PDF p. 1, bloc CLIENT |
| `SOUMIS` (`up_SOUMIS_Update`, V22:241 — 139 paramètres) | `SOU_ID='S-1844'` | `NODOC='S-1844'`, `DESCDOC='SAQ — Travaux d'électricité (rez-de-chaussée)'`, `DATEDOC=2026-08-25`, `CLIENTNO='LC2000'` + colonnes `CLIENT*` figées, `SITECIE='SAQ'`, `NOTEPRINC` = liste TRAVAUX/EXCLUS, `NOTEBAS` = conditions 1-10, `EST_NAME='Daniel Dupuis'` (expéditeur, « Estimateur Sénior » ; le PDF est signé Jonathan Parent, Chargé de projets), `EXTFILE` = chemin du texte conservé, `AUTCOUTCAL=AUTVENDCAL=238744.00` (sortie moteur, §3), `TOTCALCULE=1` | PDF p. 1-3 ; courriel |
| `SOUBLO` (`up_SOUBLO_Update`, V41:9) / `SOUDIV` (`up_SOUDIV_Update`, V41:74) | `BLO_ID='1'` « Rez-de-chaussée », `DIV_ID='1'` « Travaux d'électricité », `MULT=1` | grille minimale ; `BLO_ID` numérique car `fn_MultBlock(@BLO_ID_REL INT)` (SCHEMA.md, note `SOUBLO.MULT`) | — |
| `ENSEMBLE` (`up_ENSEMBLE_Update`, V3:26) | `ENS_ID='DR:S-1844-FORFAIT'`, `CLEPERS='DR:S-1844 SAQ RDC'` | `DESC='S-1844 SAQ RDC - forfait travaux d'électricité'`, `COUUM='U'`, `PROFIT/TEMPUNI/TEMPSEC/TEMPUM=NULL` (non énoncés), `SYSTEM=0`, `USES_DISC=0`, `DATECREE=2026-09-27` | ligne sans clé produit → ensemble nommé d'après la ligne (règle de la tâche) ; **aucune composition** (`ENSCOMPO`/`SOUENSCO` = 0) parce que le PDF n'en donne pas |
| `SOUENS` (`up_SOUENS_Update`, V6:701) | `(SOU_ID, ENS_ID)` | copie de l'ensemble, `ENS_ORG_ID='DR:S-1844-FORFAIT'`, `QTETOT=1` | — |
| `SOUREL` (`up_SOUREL_Update`, V11:3515) | `TYPERELEVE='O'`, `TYPEITEM='O'`, `ORDRE='1000'` | `ITEM_ID='DR:S-1844-FORFAIT'`, `QTE=1`, `QTEUM='U'`, **`COUTANBRUT=238744.00`**, `PROFIT=0`, `CODEIMPR=''` | PDF p. 1 |

Pourquoi `O`/`O` et pas `A` : pour un ensemble (`TYPEITEM='A'`) le moteur calcule le coût par la somme des composants
`SOUENSCO × SOUPRO` (V36:313-385) — sans composition, il donnerait 0 et le seul chiffre du document serait perdu. Pour
une ligne `O`, le moteur prend `COUTANBRUT` tel quel : `SET @CoutantUnitaire = @COUTANBRUT` (V36:451-455). Le document
ne donne qu'un **vendant** ; avec `PROFIT=0` en mode `C`, `Vendant = Coûtant × (1 + 0/100) = 238 744,00` (V36:484-492).
Le `SOUREL.ITEM_ID` pointe sur l'ensemble nommé pour garder le lien ; le moteur n'utilise pas `ITEM_ID` pour une
ligne `O` (V36:451-455, 570-574), il ne sert qu'au log et au `UPDATE SOUPRO … WHERE PRO_ID = @ITEM_ID` (V36:661-699), sans effet ici.

### 2.2 1400 Industriel Laprairie — un produit avec prix fournisseur

| Table (procédure) | Clé | Valeurs copiées du document | Source |
|---|---|---|---|
| `SOUMIS` | `SOU_ID='1400-INDUSTRIEL'` | `NODOC=NULL` (aucun S-), `DESCDOC` = objet du courriel + « entrée électrique changée au complet (bâtisse de GE), avec Hydro-Québec », `SITECIE='GE'`, `SITERUE1='1400 Industriel'`, `SITEVILLE='La Prairie'`, `CLIENT*=NULL`, `NOTEINTERN` = faits du fil (96 298.36 $, 22-24 semaines, étude arc flash/coordination à venir, 65 kA, Sylvain Bédard / C Bédard), `MATCOUTREL=MATVENDCAL=96298.36` (sortie moteur), `TOTCALCULE=1` | `courriel.txt` |
| `SOUBLO`/`SOUDIV` | `'1'` « Entrée électrique » | grille minimale | — |
| `SOUPRO` (`up_SOUPRO_Update`, V15:307) | `PRO_ID='DR:SB2-1400IND'` | `CLEMANU='gemmox000_12222500_00_00_M00'` (n° de cotation Siemens), `CLEDIST='FRANKLIN EMPIRE INC'`, `CLEPERS='DR:SB2 4 sect. 2000A'`, `DESC='PPD--SB2 SWITCHBOARD - 4 SECTIONS 600Y/347 2000A 65kA'`, **`COUBRUTUNI=96298.36`**, `COUUM='U'`, `QPP=1`, `DATECOUT=2025-12-22`, `QTEOTH=1`, `COUESC/PROMCOUNET/TEMPUNI=NULL` | PDF p. 1-2 (Line 20000, Qty 1) ; prix : courriel |
| `SOUREL` | `TYPERELEVE='P'`, `TYPEITEM='P'`, `ORDRE='1000'` | `ITEM_ID='DR:SB2-1400IND'`, `QTE=1`, `QTEUM='U'`, `PROFIT=0`, `CODEIMPR=''`, `COUTANBRUT=NULL` (le moteur lit `SOUPRO`, V36:287-311) | — |

Le prix est un **coût d'achat** ; c'est exactement la sémantique de `SOUPRO.COUBRUTUNI` (« prix figé au moment de la
soumission », SCHEMA.md). Les 15 composants du SB2 (disjoncteurs, compartiment de mesurage HQ) n'ont ni prix ni clé
produit : ils restent dans `lignes.csv` (prix vides) et ne sont pas chargés.

## 3. Preuve d'exécution (moteur officiel)

`eewin/soumissions-dr/preuves/load-2026-09-27.log` (sortie brute de `sqlcmd -i load_dr_submissions.sql`) :

```
ITEM_ID|BLO_ID|DIV_ID|TypeItem|QTE|QTEUM|COUTANBRUT|...|fCoutantTotal|fCoutantTotalPortionTVP|fVendantTotal|fLaborTotal|...
DR:S-1844-FORFAIT|1|1|O|1.000000|U|238744.000000|...|238744.000000|-238744.000000|238744.000000|.000000|...
fCoutantTotal|fCoutantTotalPortionTVP|fVendantTotal|fLaborTotal
238744.000000|-238744.000000|238744.000000|.000000
S-1844 engine (O): fCoutantTotal=238744.00 fVendantTotal=238744.00
DR:SB2-1400IND|1|1|P|1.000000|U|.000000|...|96298.360000|-96298.360000|96298.360000|.000000|...
96298.360000|-96298.360000|96298.360000|.000000
1400-INDUSTRIEL engine (P): fCoutantTotal=96298.36 fVendantTotal=96298.36
Loaded: SOUMIS S-1844 (O forfait 238744.00) and 1400-INDUSTRIEL (P SB2 96298.36).
```

`preuves/verify-2026-09-27.log` (`verify_dr_submissions.sql`) : `SOUMIS` 2 lignes, `SOUREL` 2, `SOUPRO` 1
(`UnitSelling=96298.36`, écrit par le moteur avec `@DoLog=1`, V36:661-699), `SOUENS` 1, `ENSEMBLE` 1, `CLIENTS` 1,
`SOUBLO` 2, `SOUDIV` 2, `ENSCOMPO`/`SOUENSCO` 0. Le script refuse de se rejouer (`RAISERROR` si `SOU_ID` existe) ;
`unload` puis `load` ont été rejoués une fois de bout en bout (`preuves/unload-2026-09-27.log`).

Paramètres moteur utilisés : `@EE_CALGARY=0`, `@ModeCalcul='C'`, `@VendantUAvantVendantT=1`, `@VPM=2`. Avec
`PROFIT=0` les modes `C` et `G` donnent le même vendant (V36:484-492).

## 4. Constats sur le moteur, faits pendant le chargement

1. `sp_SOU_CalculTotaux` retourne **deux jeux de résultats** quand `@DoLog=1` (le `@log` puis les 4 totaux,
   `select * from @Log` V36:655-657, puis « Retour des resultats » V36:703-708) : `INSERT … EXEC` échoue (`Msg 213`). Le script appelle donc le moteur deux fois :
   `@DoLog=1` pour la preuve et `SOUPRO.UnitSelling`, `@DoLog=0` pour capturer les 4 totaux.
2. Le moteur **n'écrit pas** `SOUMIS.MATCOUTREL/MATVENDCAL/AUTCOUTCAL/AUTVENDCAL` ; il ne met à jour que
   `MATTAXAB1..5`/`SERTAXAB1..5`/`AUTTAXAB1..5` (V36:622-652). Ces totaux sont posés par l'application cliente ; ici
   ils sont posés par `up_SOUMIS_Update` avec les valeurs retournées par le moteur.
3. Sans `TAXDEF` (table vide, `SOUMIS.TAX_ID=NULL`), `@TVPSurCoutPermise` reste `NULL`, `VendantTotalIncluantTVP`
   reste 0 et `fCoutPortionTVP = 0 − VendantTotal` = **−238 744,00** / **−96 298,36** dans le log (V36:525-556,
   570-574). Valeur parasite à ignorer tant qu'aucune définition de taxe n'est chargée.
4. `sp_SOUPRO_Quantity_V2 @REPLACE_FILTER=0` → `Msg 16916` (`CUR_2`), conforme à CALCUL-SOUMISSION.md §8/§11 :
   appelée avec `@REPLACE_FILTER=1` et `SOUREL.CODEIMPR=''`.
5. `SOUPRO.CALCTIMSTP` reste `NULL` après `sp_SOUPRO_Quantity_V2` : le curseur `CUR_1` ne réécrit que les produits
   dont `QTEOTH` change (`CAST(SPP.QTEOTH AS NUMERIC(18,2)) != CAST(BB.New_QTE …)`), et `QTEOTH=1` était déjà posé.

## 5. Ce qui manque pour aller plus loin

- **S-1857** : il faut le PDF binaire (Outlook / OneDrive) ou l'export Plan Expert chiffré de Dupuis ; le connecteur ne
  peut pas l'extraire. Ce dossier est le seul des quatre susceptible de contenir un relevé chiffré ligne par ligne.
- **Lien avec les 132 `ENS…` du recensement QPL** (`data/apprentissage/qpl-2021-2026/recensement-complet/ensembles-ee.csv`) :
  aucun des deux documents chiffrés ne cite un `ENS_ID` ni un `PRO_ID` du catalogue DR ; les deux clés créées ici sont
  préfixées `DR:` pour rester distinguables des identifiants Plan Expert (`ENS` + 17 hex) et du catalogue.
- **`TAXDEF`** vide : aucune TPS/TVQ calculable (constat 3).
