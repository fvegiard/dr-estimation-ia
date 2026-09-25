# Standard de relevé « expert estimateur » — référence d'entraînement HR26-14

Ce document définit le **format et les conventions cibles** d'un relevé produit par l'IA, tels
qu'observés dans l'exemplaire de référence `EXEMPLE.pdf` (dossier HR26-14). Il est la « bonne
réponse » de forme : tout relevé généré doit reproduire cette structure, ce vocabulaire et ces
règles. Toutes les valeurs citées ici sont **extraites du PDF** (aucune inventée) et recoupées
aux en-têtes (voir `VERIFICATION.md`).

## 1. Le dossier

- **HR26-14** — « Réfection des cuisines et salles de bain et divers travaux »
- Client : **Office municipal d'habitation du Haut-Richelieu** — 145 rue Latour, Saint-Jean-sur-Richelieu (QC)
- Consultant : **ARI Bureau d'études** — émission « Pour appel d'offres » (2026-08-31)
- 4 bâtiments = 4 lots : **LOT A** 145 St-Georges · **LOT B** 155 Mercier · **LOT C** 290 Montcalm · **LOT D** 291 Chaussé
- 26 feuilles relevées, 3 disciplines :
  - **DSI01 → DSI08** — détection et signalisation incendie (2 feuilles par lot : une vue en plan, un diagramme unifilaire)
  - **E01 → E14** — électricité (puissance, éclairage, chauffage, distribution)
  - **EU01 → EU04** — éclairage d'urgence (une feuille par lot)

## 2. Anatomie d'une feuille relevée

Chaque feuille produit **deux pages** :

1. **Page « plan » (ou diagramme)** — le plan d'origine avec les **marques par appareil** posées
   dessus (ancrage PDF exact de chaque symbole), plus un encadré **`RELEVE <feuille> - MATERIEL`** :
   - en-tête compteur : `N reperes / M familles / RES R`
     (`reperes` = symboles retenus ; `familles` = types distincts ; `RES` = nombre en réserve)
   - une **légende partielle** : un pastille de couleur par famille, son libellé, et `qté / Rxx`
   - la mention : *« RES = reserve source, modele, position, portee ou reconciliation ; \* = identification a revalider »*
2. **Page(s) « bordereau »** — le tableau détaillé (3 formats, §4), suivi du bloc
   **`RESERVES ET COMPLEMENTS`** (§6).

## 3. Règles d'or (non négociables)

1. **Rien n'est inventé.** Chaque quantité vient d'un élément lu : symbole vu, étiquette, cédule,
   note, légende. L'incertain va **en réserve**, jamais en quantité ferme silencieuse.
2. **Ancrage PDF exact.** *« Tous les symboles retenus ont un ancrage PDF exact. »* Une marque = une
   position réelle sur le plan.
3. **Les renvois ne s'additionnent pas.** *« Les renvois et composants de panneaux ne constituent pas
   des ensembles supplementaires a additionner. »* Un appareil compté sur une feuille et **renvoyé**
   sur une autre n'est **pas** recompté (portées `RENVOI_*`, §5).
4. **Diagrammes ≠ quantité physique.** Sur les unifilaires : *« reperes extremes et ellipses ne
   donnent pas une quantite physique ; plan de niveau maitre. »* Le diagramme sert à la configuration,
   pas au décompte.
5. **Relevé = identification + quantités, sans prix.** *« Releve identification et quantites sans prix. »*
   Les prix viennent après, de la base SQL (§7).
6. **Modèle non nommé → réservé, pas deviné.** `MODELE NON PRECISE` / `EXISTANT - MODELE NON INDIQUE` ;
   *« reference du devis conservee litteralement avec underscores ; aucune substitution inventee. »*
7. **Un rapport d'agent n'est pas une preuve.** Vérifier le fichier produit (compte, zoom, en-tête)
   avant de déclarer « fait ».

## 4. Les trois formats de bordereau

### 4a. Bordereau MATÉRIEL — **une ligne par repère** (DSI01-08 ; E02/E07/E10/E13)
Colonnes : `Repère / source · Materiel · Designation · Qte · Portee · Modele · Prescription / reserve · Parent`
- `Repère` = identifiant famille+séquence (`I01-01`, `M03-12`) ; `source` = identifiant d'origine du
  symbole sur le plan (`DSI01-044`, `E02-007`).
- `Qte` vaut presque toujours `1` (une ligne = un symbole physiquement posé).
- Une ligne par symbole ⇒ **nombre de lignes = `reperes` de l'en-tête** (vérifié exact sur 12/12 feuilles).

### 4b. Bordereau MATÉRIEL — **agrégé par famille** (E01, E06, E09, E11, E12, E14 ; grilles E03/E04/E05/E08)
Colonnes : `ID · Qte · Famille · Modele / type · Prescription du devis · Source / reserve`
- Utilisé pour les appareils **existants conservés** (CH chauffage, I commutateur, PC prise, T thermostat)
  et les feuilles à grande cardinalité. `Qte` = total de la famille sur la feuille.
- `Σ Qte` doit égaler `reperes` de l'en-tête (vérifié : E01=80, E06=51, E11=172, E14=172 ✅ ;
  E09/E12 divergents — voir §8).

### 4c. Bordereau TRAVAUX / ACHATS — **une ligne par famille + portée** (EU01-04)
Colonnes : `ID · Famille · Portee · Lieux · A fournir · Modele · Prescription · Source / relation`
- En-tête : `N emplacements de travaux ; M appareils a fournir (configurations a confirmer)`.
- `Lieux` = emplacements de travaux ; `A fournir` = appareils réellement achetés (les portées
  `ENLEVER`/`CONVERTIR` ont `A fournir = 0`).
- Vérifié exact sur 4/4 : `Σ Lieux = emplacements` **et** `Σ A fournir = appareils`.

## 5. Vocabulaire des portées (colonne `Portee`)

- **Actions** : `INSTALLER` (neuf posé), `ENLEVER` (dépose), `REMPLACER`, `CONVERTIR`,
  `CONSERVER` (existant gardé), `TEMPORAIRE` (chantier), `A PRECISER` (réserve de portée).
- **Renvois** (comptés ailleurs, ne pas additionner) : `RENVOI_LOGEMENTS`,
  `RENVOI_LOGEMENTS_LOT_A`, `RENVOI_DSI01/03/05/07` (renvoi vers la feuille de plan maître),
  `RENVOI_E08/E11/E14` (renvoi vers la feuille de distribution).

## 6. Vocabulaire des familles (codes → matériel)

**Incendie (DSI)** : `A` avertisseur de fumée autonome 120V mural · `K` avertisseur incendie klaxon ·
`F` déclencheur manuel adressable · `DF` détecteur de fumée adressable · `DT` détecteur thermique 57C fixe ·
`MA` module adressable simple · `MA2` module adressable double · `MIBA` module isolateur de boucle adressable ·
`RFL` résistance fin de ligne · `PAI` panneau alarme incendie · `RA` relais adressable.

**Électricité — existants agrégés** : `CH` chauffage électrique · `I` commutateur unipolaire ·
`PC` prise double · `T` thermostat. **Neufs (série M, par repère)** : luminaires `LA…LG`,
prises `CT/CG/CP/GF/SE/PC`, `CU` commutateur, `AF` avert. fumée mural, `EV` évacuateur, `IC` intercom,
`TE` téléphone, `TV` câblo, `TH` thermostat, `PL` plinthe, `PN` panneau logement, `BJ` boîte de jonction.
**Distribution** : `CDP` panneau principal, `HQ` boîtier de mesurage, `S/PS/PE` panneaux de service,
`SP` sectionneur principal, `CE1-3` disjoncteurs CDP, `COL*` départs fusibles, `TRANSFERT`/`TEMP250`/`G`
(temporaires), `MIN` minuterie astronomique, `SEL` sélecteur, `V` voyant DEL, `REP` répartiteur.

**Éclairage d'urgence (EU)** : `AC` appareil autonome à convertir · `BD` bloc alimentation à enlever ·
`BN` bloc alimentation basse tension neuf · `IS` indicateur de sortie · `PD` phare double basse tension ·
`PS` phare simple basse tension.

## 7. Grammaire des réserves et prescriptions

- **Modèle** : `MODELE NON PRECISE` (832 lignes), `EXISTANT`, sinon référence exacte du devis
  conservée littéralement (`EMERGY LITE EA_WU`, `EMERGY LITE 24LC400_LL`, `E15 SCHNEIDER…`).
- **Prescriptions types** (recopiées telles quelles, jamais reformulées en quantité) :
  `« 57C/135F fixe suivant legende »` · `« Klaxon selon legende ; sonore/visuel a confirmer au schema/devis »` ·
  `« 120V montage mural, interconnexion 3#14 suivant notes »` · `« Selon DSI09 ; aucun fabricant/modele nomme »` ·
  `« Quantite des symboles dessines seulement ; configuration finale selon notes du diagramme »` ·
  `« Schema partiel : reperes extremes et ellipses ne donnent pas une quantite physique. »`
- **Bloc `RESERVES ET COMPLEMENTS`** (fin de bordereau) : identification sans prix, ancrage PDF exact,
  renvois, contradictions classes A/B et surveillance à distance mises en réserve, longueurs de
  câbles/conduits et dépose de l'ancien système **non quantifiables** sur les diagrammes,
  vérification native Plan Expert indisponible (contrôle des fichiers et du rendu PDF seulement).

## 8. Prix (à compléter — QPL + SQL dans Google Drive)

L'exemplaire ne contient **aucun prix** (les grilles `$` des feuilles E03/E04/E05/E08 sont **vides**).
Pour compléter l'entraînement côté prix :
- **QPL** (relevés Plan Expert 2021-2026) : corpus d'apprentissage des symboles/libellés — voir
  `apprentissage/qpl-2021-2026/`.
- **SQL** : base de prix (ACCEO EEWin), désormais accessible via **Google Drive**. À brancher pour
  alimenter les colonnes `$` par famille (main-d'œuvre + matériel), sans jamais inventer de prix
  manquant (réserve si absent).

## 9. Constats à réconcilier par l'estimateur

- **E09 / E12** : le bordereau matériel n'itemise que 4 familles (E09 Σ98, E12 Σ107) alors que le
  bloc RELEVE du plan annonce 6 familles / 103 (E09) et 6 / 110 (E12). Familles comptées ailleurs
  (renvoi) ou en réserve ? À trancher.
- **E03/E04/E05/E08** : grilles de prix vides → à alimenter depuis le SQL.

## 10. Entrée dans le jeu de référence

Ce dossier gold sert de cible de forme et de contenu. Les données structurées
(`bordereau-*.csv`, `feuilles.csv`) et les vérifications chiffrées (`VERIFICATION.md`) permettent de
comparer, feuille par feuille et famille par famille, tout relevé IA futur à cet exemplaire —
critère d'amélioration de l'agent (cf. `CLAUDE.md`, jeu de référence). Régénération :
`python outils/extract_exemple.py EXEMPLE.pdf .` (depuis le PDF) ou
`python outils/regen_derives.py .` (dérivés depuis les CSV).
