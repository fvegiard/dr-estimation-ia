# RAPPORT — mapping des familles Dupuis vers les livres de prix (National Estimator 2025 / NECA 2021-2022)

Généré le 2026-09-27 par `prix/merge_mapping.py` à partir des 37 fichiers `prix/mapping/chunk-*.csv` (branche `prix-main-doeuvre`).

Règle du dossier : **aucun nombre inventé**. Chaque ligne tarifée porte le livre, la page et la ligne source brute du livre ; les nombres des colonnes ont été recoupés avec les tables extraites du PDF (`prix/national-estimator-2025.csv`, `prix/neca-2022.csv`) — une ligne dont les nombres ne se retrouvent pas à la page citée est rejetée.

## 1. Fichiers produits

| Fichier | Contenu |
|---|---|
| `prix/mapping-familles.csv` | Fusion des 37 chunks : **557 lignes**, 435 familles. Colonnes : `chunk, family, ee_codes, ne_page, ne_item, ne_material_usd, ne_manhours, ne_unit, neca_page, neca_item, neca_normal_hours, neca_unit, confidence, note, ne_raw, ne_raw_src, neca_raw, neca_raw_src`. |
| `prix/mapping-rejets.csv` | Lignes rejetées à la fusion (0 ligne) avec la raison. |
| `prix/merge_mapping.py` | Script de fusion et de contrôle ; `python3 prix/merge_mapping.py` réécrit les deux CSV et imprime les statistiques en JSON. |
| `prix/mapping/chunk-N.verification.md` | Vérification visuelle (page rendue) des lignes high/medium, un fichier par chunk (34 chunks sur 37 ; chunk-25 vérifié dans le commit `a92ad21` sans fichier ; chunks 27 et 33 non vérifiés visuellement). |

Conventions de page (identiques aux CSV des livres) : `ne_page` = page PDF (1-based) du National Estimator 2025, **folio imprimé = ne_page − 1** ; `neca_page` = folio imprimé du NECA (= index PDF + 1).

Colonnes `*_raw` : ligne brute du livre, telle qu'imprimée. `*_raw_src` dit d'où elle vient : `item` = écrite par l'agent de mapping dans la colonne item (marqueur `|| raw:`) et retrouvée à l'identique dans la table extraite du livre ; `note` = citée entre guillemets dans la note de l'agent et retrouvée à l'identique dans la table ; `book` = absente du chunk, reprise de la table extraite à la page citée (même nombres, même unité, même libellé). Répartition : NE — item 260, note 41, book 1 ; NECA — item 326, note 66, book 2. Aucune ligne `-unconfirmed` (toutes les lignes brutes citées par les agents existent bien à la page citée).

## 2. Couverture

Poids = `marks_total` de `prix/families.json` (nombre de marques dans le corpus Dupuis 2021-2026, 186 378 marques, 435 familles).

| Mesure | Familles | Part | Marques | Part |
|---|---|---|---|---|
| Familles couvertes par un chunk | 435 / 435 | 100.0 % | 186 378 | 100.0 % |
| **Familles tarifées** (≥ 1 ligne de livre, NE et/ou NECA) | **281 / 435** | **64.6 %** | **132 332** | **71.0 %** |
| — dont NE + NECA | 203 | 46.7 % | 97 064 | 52.1 % |
| — dont NECA seulement (heures, pas de matériel) | 72 | 16.6 % | 32 693 | 17.5 % |
| — dont NE seulement | 6 | 1.4 % | 2 575 | 1.4 % |
| Familles à `none` (aucune ligne de livre sélectionnable) | 154 / 435 | 35.4 % | 54 046 | 29.0 % |
| Familles absentes de tous les chunks | 0 | — | 0 | — |

### 2.1 Par catégorie Dupuis

| Catégorie | Familles tarifées / total | Marques tarifées / total | Part des marques |
|---|---|---|---|
| dispositif | 49 / 52 | 69 444 / 72 424 | 95.9 % |
| luminaire | 15 / 118 | 5 701 / 46 975 | 12.1 % |
| securite_incendie | 35 / 35 | 19 180 / 19 180 | 100.0 % |
| telecom_donnees | 15 / 15 | 17 767 / 17 767 | 100.0 % |
| chauffage | 12 / 13 | 9 942 / 10 184 | 97.6 % |
| indetermine | 7 / 49 | 783 / 9 986 | 7.8 % |
| distribution | 11 / 14 | 3 915 / 4 258 | 91.9 % |
| mecanique_moteur | 32 / 32 | 2 209 / 2 209 | 100.0 % |
| autre | 9 / 9 | 1 700 / 1 700 | 100.0 % |
| conduit_filage | 96 / 98 | 1 691 / 1 695 | 99.8 % |

### 2.2 Par niveau de confiance (meilleure ligne de la famille)

| Confiance | Familles | Marques | Part des marques |
|---|---|---|---|
| high | 96 | 59 607 | 32.0 % |
| medium | 85 | 38 493 | 20.7 % |
| low | 100 | 34 232 | 18.4 % |
| none | 154 | 54 046 | 29.0 % |

Lecture : 71 % des marques du corpus ont au moins une ligne de livre ; 32 % avec une correspondance `high`. Le trou principal est le **luminaire** (118 familles, 47 000 marques, 12 % tarifées) : les étiquettes `FIXT TYPE X` ne sont que des codes de légende, la ligne de livre dépend de la cédule de luminaires de chaque projet.

Unités rencontrées : NE `Ea`, `CLF` (100 pi), `KLF` (1 000 pi) ; NECA `E` (l'unité), `C` (par 100), `M` (par 1 000).

## 3. Lignes rejetées et corrections

Contrôles appliqués à chaque ligne : famille connue de `families.json` ; côté tarifé → page numérique, nombres numériques, unité présente, ligne brute trouvée (item, note ou table du livre) **et** nombres de la ligne (NE : matériel + heures ; NECA : heures normales) égaux à ceux de la table extraite à la page citée ; côté `none` → aucun nombre ni unité (une page seule est tolérée comme renvoi à la table consultée) ; `confidence` ∈ {high, medium, low, none}.

Résultat : **0 ligne rejetée sur 557 lues**. `prix/mapping-rejets.csv` est vide (en-tête seulement).

Corrections faites avant la fusion (commit `ef76e62`, données inchangées) :
- `chunk-0.csv` ligne 20 (ENSEIGNE SORTIE) et `chunk-17.csv` ligne 4 (EXIT COMBO) : virgule non protégée dans `neca_item` (« …header row, Rev X) » / « …own heading, 26 52 00… ») qui décalait les colonnes → cellule mise entre guillemets.
- `chunk-32.csv` (2 EMT 3#1) : matériel NE imprimé « 2,250.00 » → écrit `2250.00` (séparateur de milliers retiré ; la ligne brute garde « 2,250.00 »).
- 3 côtés sans ligne brute ni dans l'item ni dans la note (HP et HP RELO → NECA p390 « Speaker - Ceiling - Note: Includes Cutting Hole 0.75 0.95 1.15 E » ; ENCASTRE → NE p167-PDF « Downlight 6" 50R20 L1@0.60 Ea 88.00 28.00 116.00 » et NECA « LED 1.25 1.56 1.95 E ») : ligne reprise de la table extraite du livre (`*_raw_src = book`), nombres identiques à ceux du chunk.
- Lignes brutes identiques sous plusieurs tables d'une même page (ex. NECA p318 « 15 Amp 3 Wire 25.00 31.25 37.50 C » sous *Single Receptacle* et *Duplex Receptacle*) : la table est choisie par le titre écrit dans `neca_item` (« Duplex Receptacle - Straight Blade: 15 Amp 3 Wire »).

Réserves connues (non rejetées, à lire dans `note`) :
- Lignes `low` (100 familles) : proxy assumé (ampérage, tension, montage ou grade absents de l'étiquette) ; la note donne les alternatives de la même page.
- Séries `B500W…B2500W`, `750W`, `1500W` : dictionnaire Dupuis dit « luminaire », corpus dit « plinthe » ; laissées `none` avec renvoi NECA p78 (plinthes tarifées par longueur, pas par puissance).
- Familles multi-lignes (ex. `3/4 EMT 3#12` : ligne conduit NECA p202 + ligne compagnon fils #12 NECA p150) : les heures NECA se **somment** entre les lignes d'une même famille ; côté NE l'assemblage p449 est déjà groupé (`none` sur la ligne compagnon).

## 4. Familles à `none` (154 familles, 54 046 marques)

Aucune ligne de livre sélectionnable sans inventer la spécification. Motifs : code de légende (`FIXT TYPE …`, cédule requise), abréviation non résolue (catégorie `indetermine`), appareil hors des deux livres, ou sortie de câblage dont l'équipement raccordé n'est pas connu.

### luminaire — 103 familles, 41 274 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| FIXT TYPE A | 4060 | 0 | Luminaire type A is defined per project fixture schedule (type letter, not a product). No book line can match without the schedule -> none i… |
| FIXT TYPE L1 | 2474 | 1 | Plan legend type code only (Dupuis: luminaire type L1, famille L) - no fixture spec (size/lamp/mount) so no book line can be selected; needs… |
| FIXT TYPE B | 2136 | 1 | Plan legend type code only (Dupuis: luminaire type B) - no fixture spec; needs fixture schedule |
| FIXT TYPE E1 | 1911 | 1 | Plan legend type code only (Dupuis: luminaire type E1) - no fixture spec; needs fixture schedule |
| FIXT TYPE D | 1753 | 1 | Plan legend type code only (Dupuis: luminaire type D) - no fixture spec; needs fixture schedule |
| FIXT TYPE E | 1536 | 1 | Plan legend type code only (Dupuis: luminaire type E) - no fixture spec; needs fixture schedule |
| FIXT TYPE C | 1467 | 2 | Plan legend type code only (Dupuis: luminaire type C, variant TYPE C) - no fixture spec (size/lamp/mount) so no book line can be selected; n… |
| FIXT TO REMOVE | 1140 | 2 | Dupuis: luminaire existant a enlever (demolition). NE 2025 has no demolition/removal line (grep demoli/remov -> 0). NECA 2022 26 05 05 Selec… |
| FIXT ENL | 1131 | 2 | Dupuis: luminaire existant a enlever (ENL = a enlever), same scope as FIXT TO REMOVE. No whole-fixture removal line in NE 2025 (no demolitio… |
| B1000W | 1123 | 2 | Dupuis: luminaire type B, 1000W (plan legend type + wattage only, no fixture type/mount/lamp). 1000 W points to an HID/high-bay class but th… |
| FIXT TYPE A1 | 974 | 3 | Plan legend type code only (Dupuis: luminaire type A1) - no fixture spec (size/lamp/mount) so no book line can be selected; needs fixture sc… |
| FIXT TYPE L6 | 970 | 3 | Plan legend type code only (Dupuis: luminaire type L6) - no fixture spec; needs fixture schedule |
| FIXT TYPE L3 | 931 | 3 | Plan legend type code only (Dupuis: luminaire type L3, variants TYPE L3, L3A, L3B) - no fixture spec; needs fixture schedule |
| B300W | 858 | 4 | Dupuis: luminaire type B, 300W (plan legend type + wattage only, no fixture type/mount). Book lines differ by mount and cannot be chosen fro… |
| FIXT TYPE L2 | 847 | 4 | Plan legend type code only (Dupuis: luminaire type L2, variant TYPE L2) - no fixture spec (size/lamp/mount) so no book line can be selected;… |
| FIXT TYPE F | 828 | 4 | Plan legend type code only (Dupuis: luminaire type F, variant fixt type f) - no fixture spec (size/lamp/mount) so no book line can be select… |
| FIXT TYPE G | 672 | 5 | Plan legend type code only (Dupuis: luminaire type G, variants TYPE G, G, FIXT TYPE G1/G2/G6, FIXTR TYPE G) - no fixture spec (size/lamp/mou… |
| TYPE B | 622 | 5 | Plan legend type code only (Dupuis: luminaire type B abrege, = FIXT TYPE B already none in chunk-1; variants TYPE B1/B2) - no fixture spec; … |
| FIXT TYPE L8 | 574 | 5 | Plan legend type code only (Dupuis: luminaire type L8, variants TYPE L8, L8A, L8W, L8-1) - no fixture spec (size/lamp/mount) so no book line… |
| FIXT TYPE L4 | 525 | 6 | Plan legend type code only (Dupuis: luminaire type L4, famille L) - no fixture spec (lamp/wattage/mount/size) on the label, so no National E… |
| FIXT TYPE E2 | 499 | 6 | Plan legend type code only (Dupuis: luminaire type E2) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| B1250W | 495 | 6 | Dupuis dictionary files B1250W as "luminaire serie/prefixe B, 1250W" but flags the B prefix as uncertain; the label corpus (B500W/B750W/B100… |
| FIXT TYPE I | 473 | 6 | Plan legend type code only (Dupuis: luminaire type I; bare label "I" normalised to FIXT TYPE I) - no fixture spec (lamp/wattage/mount/size) … |
| FIXT TYPE H | 473 | 6 | Plan legend type code only (Dupuis: luminaire type H (selon legende du plan)) - no fixture spec (lamp/wattage/mount/size) on the label, so n… |
| FIXT TYPE B1 | 464 | 6 | Plan legend type code only (Dupuis: luminaire type B1) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| TYPE A | 446 | 6 | Dupuis: "luminaire type A (forme abregee probable)" = abbreviated FIXT TYPE A (variants Type A1..A7, A2.1, A3G, AL, AR). Plan legend type le… |
| FIXT TYPE L10 | 436 | 6 | Plan legend type code only (Dupuis: luminaire type L10, famille L) - no fixture spec (lamp/wattage/mount/size) on the label, so no National … |
| FIXT TYPE D1 | 410 | 6 | Plan legend type code only (Dupuis: luminaire type D1) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| FIXT TYPE J2 | 409 | 7 | Plan legend type code only (Dupuis: luminaire type J2) - no fixture spec (size/lamp/mount) so no book line can be selected; needs fixture sc… |
| FIXT TYPE C1 | 399 | 7 | Plan legend type code only (Dupuis: luminaire type C1, variant TYPE C1) - no fixture spec (size/lamp/mount) so no book line can be selected;… |
| FIXT TYPE L5 | 387 | 7 | Plan legend type code only (Dupuis: luminaire type L5 (famille L)) - no fixture spec (size/lamp/mount) so no book line can be selected; need… |
| FIXT TYPE T1 | 380 | 7 | Plan legend type code only (Dupuis: luminaire type T1 (abrege), variant T1) - no fixture spec (size/lamp/mount) so no book line can be selec… |
| FIXT TYPE A2 | 365 | 7 | Plan legend type code only (Dupuis: luminaire type A2) - no fixture spec (size/lamp/mount) so no book line can be selected; needs fixture sc… |
| FIXT TYPE D2 | 339 | 8 | Plan legend type code only (Dupuis: luminaire type D2) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| FIXT TYPE L9 | 336 | 8 | Plan legend type code only (Dupuis: luminaire type L9 (famille L); variant with double space FIXT TYPE  L9) - no fixture spec (lamp/wattage/… |
| FIXT TYPE J | 310 | 8 | Plan legend type code only (Dupuis: luminaire type J; variants TYPE J, Type J, fixt type j; bare "J" flagged non-tranchable by Dupuis) - no … |
| FIXT TYPE 1 | 307 | 8 | Plan legend type code only (Dupuis: luminaire type 1 (numerotation numerique)) - no fixture spec (lamp/wattage/mount/size) on the label, so … |
| FIXT TYPE L1A | 299 | 8 | Plan legend type code only (Dupuis: luminaire type L1A) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 2… |
| FIXT TYPE D4 | 298 | 8 | Plan legend type code only (Dupuis: luminaire type D4) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| FIXT TYPE L7 | 291 | 8 | Plan legend type code only (Dupuis: luminaire type L7 (famille L)) - no fixture spec (lamp/wattage/mount/size) on the label, so no National … |
| FIXT TYPE R1 | 283 | 8 | Plan legend type code only (Dupuis: luminaire type R1) - no fixture spec (lamp/wattage/mount/size) on the label, so no National Estimator 20… |
| 750W | 254 | 8 | Dupuis dictionary files 750W as "luminaire cote par puissance, 750W" (variant 750W 347V), but the label corpus reads as electric heating: B7… |
| FIXT TYPE E3 | 238 | 9 | Plan legend type code only (Dupuis: luminaire type E3 (selon legende); 386 occ / 23 projets; corpus FIXT TYPE E3 235 marks / 13 projects + F… |
| FIXT TYPE L | 229 | 9 | Plan legend type code only (Dupuis: luminaire type L (sans numero), famille L; 316 occ / 28 projets; corpus FIXT TYPE L 215 marks / 14 proje… |
| B500W | 229 | 9 | Dupuis dictionary files B500W as "luminaire type B, designe par puissance (500W)" (312 occ / 13 projets; corpus 229 marks / 9 projects), but… |
| FIXT TYPE L12 | 208 | 10 | Plan legend type code only (Dupuis: luminaire type L12, 234 marks / 15 projets) - no fixture spec (size/lamp/mount) so no book line can be s… |
| FIXT TYPE S1 | 207 | 10 | Plan legend type code only (Dupuis: luminaire type S1, 378 marks / 25 projets; variants Type S1, FIXTURE TYPE S1A) - no fixture spec so no b… |
| FIXT TYPE B3 | 197 | 10 | Plan legend type code only (Dupuis: luminaire type B3, 240 marks / 8 projets) - no fixture spec so no book line can be selected; needs the f… |
| FIXT TYPE D3 | 188 | 11 | Plan legend type code only (Dupuis: luminaire type D3; 279 occ / 14 projets; corpus FIXT TYPE D3 188 marks / 8 projects) - no fixture spec (… |
| FIXT TYPE L14 | 184 | 11 | Plan legend type code only (Dupuis: luminaire type L14 (famille L); 335 occ / 13 projets; corpus FIXT TYPE L14 180 marks / 9 projects + fixt… |
| FIXT TYPE S3 | 183 | 11 | Plan legend type code only (Dupuis: luminaire type S3; 353 occ / 16 projets; corpus FIXT TYPE S3 183 marks / 9 projects) - no fixture spec (… |
| FIXT TYPE L11 | 178 | 11 | Plan legend type code only (Dupuis: luminaire type L11 (famille L); 296 occ / 23 projets; corpus FIXT TYPE L11 178 marks / 13 projects) - no… |
| FIXT TYPE K | 176 | 11 | Plan legend type code only (Dupuis: luminaire type K; 331 occ / 39 projets; corpus FIXT TYPE K 150 marks / 20 projects + TYPE K 13, Type K 1… |
| FIXT TYPE M | 174 | 11 | Plan legend type code only (Dupuis: luminaire type M (selon legende); 288 occ / 33 projets; corpus FIXT TYPE M 116 marks / 19 projects + TYP… |
| FIXT TYPE X1 | 169 | 12 | Plan legend type code only (Dupuis: luminaire type X1, 169 marks / 5 projets; variants X1 39, TYPE X1 N 10, XA1 21, XB1 30 separate) - no fi… |
| FIXT TYPE X | 158 | 12 | Plan legend type code only (Dupuis: luminaire type X, 158 marks / 7 projets; variants Type X 14, TYPE X 4, X2 16 etc. separate) - no fixture… |
| FIXT TYPE C3 | 157 | 12 | Plan legend type code only (Dupuis: luminaire type C3, 157 marks / 6 projets; variant FIXT TYPE C3 303 1) - no fixture spec so no book line … |
| FIXT TYPE F1 | 154 | 12 | Plan legend type code only (Dupuis: luminaire type F1, 154 marks / 7 projets, "variante de la famille F, type distinct au catalogue"; varian… |
| FIXT TYPE N | 152 | 13 | Plan legend type code only (Dupuis: luminaire type N; 278 occ / 25 projets; corpus 152 marks, variants N / n) - no fixture spec (lamp/wattag… |
| FIXT TYPE E5 | 143 | 13 | Plan legend type code only (Dupuis: luminaire type E5; 236 occ / 10 projets; corpus 143 marks) - no fixture spec (lamp/wattage/mount/size) o… |
| FIXT TYPE C2 | 142 | 13 | Plan legend type code only (Dupuis: luminaire type C2; 276 occ / 25 projets; corpus 142 marks) - no fixture spec (lamp/wattage/mount/size) o… |
| FIXT TYPE P1 | 135 | 13 | Plan legend type code only (Dupuis: luminaire type P1 (selon legende); 262 occ / 13 projets; corpus 135 marks) - no fixture spec (lamp/watta… |
| FIXT TYPE N1 | 131 | 13 | Plan legend type code only (Dupuis: luminaire type N1; 246 occ / 12 projets; corpus 131 marks) - no fixture spec (lamp/wattage/mount/size) o… |
| FIXT TYPE R | 130 | 14 | Plan legend type code only (Dupuis: luminaire type R; 211 occ / 16 projets; corpus 130 marks / 9 projects) - no fixture spec (lamp/wattage/m… |
| FIXT TYPE L15 | 126 | 14 | Plan legend type code only (Dupuis: luminaire type L15 (famille L); 252 occ / 10 projets; corpus 126 marks / 5 projects) - no fixture spec (… |
| FIXT TYPE S6 | 121 | 14 | Plan legend type code only (Dupuis: luminaire type S6; 242 occ / 12 projets; corpus 121 marks / 6 projects) - no fixture spec (lamp/wattage/… |
| FIXT TYPE L4A | 120 | 14 | Plan legend type code only (Dupuis: luminaire type L4A; 240 occ / 8 projets; corpus 120 marks / 4 projects) - no fixture spec (lamp/wattage/… |
| FIXT TYPE P | 113 | 15 | Plan legend type code only (Dupuis: luminaire type P selon legende, 226 occ / 16 projets) - no fixture spec (size/lamp/mount) so no book lin… |
| MONUMENT | 107 | 15 | Dupuis MONUMENT = enseigne-monument exterieure (signaletique illuminee de site), luminaire BT, 202 occ / 23 projets (categories.json: "ensei… |
| LAMPADAIRE | 103 | 16 | Dupuis dictionary: lampadaire exterieur (poteau d'eclairage), categorie luminaire, BT (206 occ / 12 projets; corpus LAMPADAIRE 103 marks / 6… |
| FIXT TYPE D7 | 99 | 16 | Plan legend type code only (Dupuis: luminaire type D7; 172 occ / 9 projets; corpus 99 marks / 6 projects) - no fixture spec (lamp/wattage/mo… |
| FIXT TYPE A3 | 97 | 16 | Plan legend type code only (Dupuis: luminaire type A3; 134 occ / 12 projets; corpus 97 marks / 7 projects) - no fixture spec (lamp/wattage/m… |
| FIXT TYPE S | 92 | 16 | Plan legend type code only (Dupuis: luminaire type S (sans numero); 107 occ / 12 projets; corpus FIXT TYPE S 70 marks / 7 projects + fixt ty… |
| FIXT TYPE B2 | 91 | 17 | Plan legend type code only (Dupuis: luminaire type B2 (selon legende); 173 occ / 23 projets; corpus 91 marks / 12 projects) - no fixture spe… |
| FIXT TYPE R2 | 83 | 17 | Plan legend type code only (Dupuis: luminaire type R2 (serie R); 157 occ / 12 projets; corpus 83 marks / 7 projects) - no fixture spec (lamp… |
| FIXT TYPE L13 | 80 | 17 | Plan legend type code only (Dupuis: luminaire type L13; 156 occ / 12 projets; corpus 80 marks / 7 projects) - no fixture spec (lamp/wattage/… |
| FIXT TYPE H1 | 79 | 17 | Plan legend type code only (Dupuis: luminaire type H1 (au catalogue du releve); 156 occ / 19 projets; corpus 79 marks / 10 projects) - no fi… |
| FIXT TYPE K2 | 75 | 18 | Plan legend type code only (Dupuis: luminaire type K2; 150 occ / 8 projets; corpus FIXT TYPE K2 50 marks / 3 projects + fixt type k2 25 / 1 … |
| FIXT TYPE D6 | 74 | 18 | Plan legend type code only (Dupuis: luminaire type D6; 130 occ / 9 projets; corpus 74 marks / 6 projects) - no fixture spec (lamp/wattage/mo… |
| B 1500W | 72 | 18 | Dupuis dictionary: "luminaire type B, designe par puissance (1500W)" (117 occ / 16 projets; corpus B 1500W 68 marks / 10 projects + b 1500w … |
| FIXT TYPE D5 | 69 | 19 | Plan legend type code only (Dupuis: luminaire type D5; 121 occ / 8 projets; corpus 69 marks / 5 projects; categories.json: sous-variante D5 … |
| FIXTURE TYPE B | 69 | 19 | Plan legend type code only (Dupuis: luminaire type B (orthographe complete FIXTURE vs FIXT); 69 occ / 9 projets; corpus 69 marks / 9 project… |
| FIXT TYPE BB | 66 | 19 | Plan legend type code only (Dupuis: luminaire type BB; 122 occ / 8 projets; corpus 66 marks / 5 projects) - no fixture spec (lamp/wattage/mo… |
| FIXT TYPE N2 | 66 | 19 | Plan legend type code only (Dupuis: luminaire type N2; 120 occ / 15 projets; corpus 64 marks / 8 projects; lowercase fixt type n2 2 marks / … |
| FIXT TYPE S2 | 64 | 19 | Plan legend type code only (Dupuis: luminaire type S2; 120 occ / 13 projets; corpus 64 marks / 8 projects) - no fixture spec (lamp/wattage/m… |
| FIXT TYPE G1 | 62 | 20 | Plan legend type code only (Dupuis: luminaire type G1 selon legende, BT; 124 occ / 10 projets; corpus 62 marks / 5 projects; categories.json… |
| FIXT TYPE F3 | 57 | 20 | Plan legend type code only (Dupuis: luminaire type F3, BT; 114 occ / 8 projets; corpus 57 marks / 4 projects) - no fixture spec (lamp/wattag… |
| FIXT TYPE F2 | 54 | 20 | Plan legend type code only (Dupuis: luminaire type F2, BT; 108 occ / 12 projets; corpus 54 marks / 6 projects) - no fixture spec (lamp/watta… |
| FIXT TYPE C4 | 50 | 21 | Plan legend type code only (Dupuis: luminaire type C4, serie C; corpus 50 marks / 5 projects; variants C4A 22, C4B 23 excluded; "C4 2KW" 11 … |
| FIXT TYPE G2 | 49 | 22 | Plan legend type code only (Dupuis: luminaire type G2, BT; 98 occ / 8 projets; corpus 49 marks / 4 projects; categories.json: "Sous-variante… |
| FIXT TYPE E7 | 47 | 22 | Plan legend type code only (Dupuis: luminaire type E7, BT; 90 occ / 8 projets; corpus 47 marks / 5 projects) - no fixture spec (lamp/wattage… |
| FIXT TYPE M1 | 47 | 22 | Plan legend type code only (Dupuis: luminaire type M1, BT; 83 occ / 16 projets; corpus 47 marks / 9 projects; categories.json: "Type de lumi… |
| FIXT TYPE Q | 46 | 22 | Plan legend type code only (Dupuis: luminaire type Q, BT; 92 occ / 14 projets; corpus 46 marks / 7 projects; categories.json: "luminaire typ… |
| FIXT TYPE L3A | 44 | 23 | Plan legend type code only (Dupuis: luminaire type L3A, famille L; categories.json "luminaire type L3A", dictionnaire 88 occ / 10 projets; c… |
| FIXT TYPE P3 | 32 | 24 | Plan legend type code only (Dupuis: luminaire type P3, "Type de luminaire au catalogue du releve"; 64 occ / 8 projets; corpus 32 marks / 4 p… |
| FIXT TYPE P2 | 30 | 24 | Plan legend type code only (Dupuis: luminaire type P2; 60 occ / 18 projets; corpus 30 marks / 9 projects) - no fixture spec (lamp/wattage/mo… |
| FIXT TYPE M2 | 29 | 25 | Plan legend type code only (Dupuis dictionnaire: luminaire type M2, BT, 54 occ / 11 projets; categories.json note empty; corpus FIXT TYPE M2… |
| FIXT TYPE L3B | 25 | 26 | Plan legend type code only (Dupuis dictionnaire-symboles: luminaire type L3B, famille L, BT, 50 occ / 8 projets; categories.json: "Variante … |
| FIXTURE TYPE C | 25 | 26 | Plan legend type code only (Dupuis dictionnaire-symboles: luminaire type C, BT, 25 occ / 8 projets; categories.json: "FIXTURE=orthographe co… |
| FIXT TYPE R3 | 21 | 26 | Plan legend type code only (Dupuis dictionnaire-symboles: luminaire type R3, BT, 31 occ / 8 projets; categories.json note on the single lett… |
| FIXT TYPE S4 | 18 | 27 | Plan legend type code only (Dupuis dictionnaire: luminaire type S4 (selon legende), 35 occ / 15 projets; etiquettes.csv FIXT TYPE S4 18 mark… |
| TYPE F | 16 | 28 | Plan legend type code only (Dupuis dictionnaire-symboles: "luminaire type F (forme abregee probable)", luminaire, BT, 23 occ / 9 projets; ca… |
| FIXT TYPE S5 | 9 | 30 | Plan legend type code only (Dupuis dictionnaire: luminaire type S5 (selon legende), luminaire, BT, 17 occ / 9 projets; etiquettes.csv FIXT T… |

### indetermine — 42 familles, 9 203 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| KS | 2691 | 0 | Dupuis dictionary: KS = abreviation non resolue (categorie indetermine). Cannot map -> none. |
| MA | 790 | 4 | Dupuis dictionary: MA = abreviation non resolue (categorie indetermine, 16 projets). Nothing to match in either book until the legend of the… |
| P | 696 | 4 | Dupuis dictionary: P = lettre seule ambigue (repere ou fixture P ?), categorie indetermine, 19 projets. Nothing to match in either book unti… |
| A | 555 | 5 | Dupuis: lettre isolee non resolue (dictionary: "Pourrait lier a TYPE A mais aucune confirmation"). No product identity -> nothing to look up… |
| ECH | 541 | 5 | Dupuis: sens incertain (echangeur d air? ou ECL/eclairage?). Census hints echangeur: separate labels ECHANGEUR (613 marks) and PRISE ECH (18… |
| DM | 385 | 7 | Dupuis dictionary: DM = abreviation non resolue, categorie indetermine (561 marks / 25 projets). Census variants INT DM, STATION DM, DM1-5, … |
| RA | 277 | 8 | Dupuis dictionary: categorie indetermine, "abreviation ambigue (signification incertaine)", note "2 lettres sans contexte suffisant pour tra… |
| MIA | 249 | 9 | Dupuis dictionary: categorie indetermine, sous_type "signification inconnue" (459 occ / 13 projets; corpus 249 marks / 8 projects, no EE ens… |
| MRA | 230 | 9 | Dupuis dictionary: categorie indetermine, sous_type "abreviation non identifiee (MRA)" (413 occ / 16 projets; corpus 230 marks / 10 projects… |
| PORTE | 214 | 10 | Dupuis PORTE = porte (fonction electrique non precisee), categorie indetermine, 239 marks / 18 projets. Label alone does not say which devic… |
| DD | 182 | 11 | Dupuis dictionary: categorie indetermine, sous_type "abreviation non resolue" (218 occ / 16 projets; corpus DD 182 marks / 11 projects; cens… |
| DV | 177 | 11 | Dupuis dictionary: categorie indetermine, sous_type "abreviation non resolue" (201 occ / 8 projets; corpus DV 177 marks / 7 projects; census… |
| S | 165 | 12 | Dupuis S = lettre seule, sens incertain, categorie indetermine, 165 marks / 28 projets (S 155 + s 10); categories.json hypotheses: interrupt… |
| B | 143 | 13 | Dupuis dictionary: categorie indetermine, sous_type 'lettre seule, sens incertain' (229 occ / 21 projets; corpus B 142 marks / 11 projects, … |
| PP | 141 | 13 | Dupuis dictionary: categorie indetermine, sous_type 'sigle de 2 lettres, sens incertain' (270 occ / 18 projets; corpus PP 141 marks / 10 pro… |
| VC | 129 | 14 | Dupuis dictionary: categorie indetermine, sous_type 'abreviation non resolue' (229 occ / 17 projets; corpus VC 129 marks / 11 projects; no v… |
| K | 126 | 14 | Dupuis dictionary: categorie indetermine, sous_type 'abreviation non resolue', variante K1 (248 occ / 17 projets; corpus K 62 + k1 55 + K1 8… |
| RT | 116 | 15 | Dupuis RT = abreviation non identifiee, categorie indetermine, 210 occ / 13 projets (categories.json: "reflecteur? retour? type de luminaire… |
| M | 111 | 15 | Dupuis M = lettre seule, sens incertain, categorie indetermine, 216 occ / 25 projets (M 111 marks in this batch incl. lowercase m; categorie… |
| E | 111 | 15 | Dupuis E = lettre seule ambigue (repere ou fixture E?), categorie indetermine, 213 occ / 21 projets (categories.json: "pourrait etre FIXT TY… |
| C | 106 | 15 | Dupuis C = lettre seule, sens incertain, categorie indetermine, 210 occ / 21 projets (categories.json: "type de luminaire C (cf. FIXT TYPE C… |
| RM | 98 | 16 | Dupuis dictionary: categorie indetermine, sous_type 'sigle de 2 lettres, sens incertain', no variants (126 occ / 19 projets; corpus RM 98 ma… |
| BORNE | 86 | 17 | Dupuis BORNE = borne electrique, type incertain, categorie indetermine (172 occ / 8 projets; corpus bare BORNE 86 marks / 4 projects; catego… |
| BA | 79 | 17 | Dupuis BA = abreviation ambigue, signification incertaine, categorie indetermine (102 occ / 17 projets; corpus 79 marks / 10 projects; categ… |
| J | 78 | 17 | Dupuis J = lettre seule ambigue (repere ou fixture "J"?), categorie indetermine (148 occ / 15 projets; corpus J 77 + j 1 = 78 marks / 7 proj… |
| H | 74 | 18 | Dupuis H = lettre isolee non resolue, categorie indetermine (109 occ / 18 projets; corpus H 66 marks / 10 projects + h 8 / 1 = 74). Could be… |
| F | 71 | 18 | Dupuis F = lettre isolee non resolue, categorie indetermine (137 occ / 21 projets; corpus F 70 marks / 11 projects + f 1 / 1 = 71; categorie… |
| RS | 69 | 19 | Dupuis RS = abreviation non resolue, categorie indetermine (100 occ / 8 projets; corpus 69 marks / 5 projects; categories.json: "Significati… |
| R | 67 | 19 | Dupuis R = lettre seule ambigue (repere ou fixture "R"?), categorie indetermine (124 occ / 11 projets; corpus R 60 + r 7 = 67 marks / 4 proj… |
| L | 60 | 20 | Dupuis L = lettre isolee non resolue, categorie indetermine (116 occ / 13 projets; corpus L 55 marks / 6 projects + l 5 marks / 1 project; c… |
| D | 59 | 20 | Dupuis D = lettre seule ambigue (repere ou fixture "D"?), categorie indetermine (117 occ / 23 projets; corpus D 46 marks / 10 projects + d 1… |
| TEE | 50 | 21 | Dupuis TEE = abreviation non resolue, categorie indetermine (corpus 50 marks / 5 projects; categories.json: "Possible raccord de conduit en … |
| LC | 45 | 22 | Dupuis LC = sigle de 2 lettres, sens incertain, categorie indetermine (84 occ / 11 projets; corpus LC 35 marks / 5 projects + lc 10 marks / … |
| V | 41 | 23 | Dupuis V = lettre isolee non resolue, categorie indetermine (categories.json: "Signification incertaine (volt? ventilateur?); non inventee";… |
| T | 38 | 23 | Dupuis T = lettre seule ambigue, categorie indetermine (categories.json: "Aucun indice suffisant (ni TEL, ni TH selon le lexique du brief)";… |
| CP | 35 | 24 | Dupuis CP = abreviation non resolue, categorie indetermine (dictionnaire-symboles: 69 occ / 11 projets; categories.json: "Possible lien avec… |
| CR10 | 33 | 24 | Dupuis CR10 = code ambigu (relais de controle ou reference de circuit), categorie indetermine (dictionnaire-symboles: 64 occ / 11 projets; c… |
| PC | 26 | 25 | Dupuis dictionnaire + categories.json: PC = indetermine, abreviation ambigue (43 occ / 16 projets; note: "2 lettres sans contexte suffisant … |
| CL | 18 | 27 | Dupuis dictionnaire classifies "CL" as indetermine - "abreviation non identifiee (CL)" (32 occ / 8 projets; etiquettes.csv CL 18 marks / 5 p… |
| VA | 16 | 28 | Dupuis dictionnaire-symboles: VA = "sigle incertain", categorie indetermine (24 occ / 12 projets; corpus 16 marks / 7 projects); categories.… |
| TA | 13 | 29 | Dupuis dictionnaire classifies "TA" as indetermine - "sigle incertain" (16 occ / 9 projets; etiquettes.csv TA 13 marks / 6 projects, no EE e… |
| PANN CONTROL | 12 | 29 | Dupuis dictionnaire: "PANN CONTROL" = panneau de controle, type non precise, categorie indetermine (24 occ / 8 projets; etiquettes.csv 12 ma… |

### dispositif — 3 familles, 2 980 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| RACCORD DIRECT | 1724 | 1 | Dupuis: sortie de cablage - raccordement direct (sans prise). No generic "direct connection / hard-wired outlet" line in NE 2025 (Equipment … |
| INT ENL | 893 | 3 | Dupuis INT ENL = interrupteur existant a enlever (demolition). NE 2025: no demolition/removal lines (grep remov/demol -> prose only). NECA 2… |
| RACCORD PARTITION | 363 | 7 | Dupuis: raccordement electrique dans cloison/partition (466 marks / 13 projets; sibling label RACCORD PARTITION TEL). Ambiguous: systems-fur… |

### distribution — 3 familles, 343 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| PANN | 141 | 13 | Dupuis: panneau electrique de distribution, categorie distribution (282 occ / 8 projets; corpus PANN 141 marks / 4 projects; census variants… |
| PULL BOX | 128 | 14 | Dupuis: boite de tirage (pull box), categorie distribution (222 occ / 8 projets; corpus PULL BOX 128 marks / 5 projects; sized variants exis… |
| TR | 74 | 18 | Dupuis TR = transformateur (distribution, BT; 148 occ / 16 projets; corpus 74 marks / 8 projects). Label carries no kVA, phase, voltage or m… |

### chauffage — 1 familles, 242 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| B750W | 242 | 9 | Dupuis dictionary: plinthe electrique chauffante 750W (serie/type B) (chauffage, BT; 362 occ / 18 projets; corpus B750W 234 marks / 12 proje… |

### conduit_filage — 2 familles, 4 marques

| Famille | Marques | Chunk | Motif (début de la note) |
|---|---|---|---|
| 3/1 EMT 2#3 | 3 | 33 | Dupuis conduit spec "3/1 2c3" (conduits-spec.csv: 3 occurrences, 122,966.4 px total length - long runs); no EE ensemble code for this spec. … |
| 3/1 EMT 6#3 | 1 | 35 | Dupuis conduit spec "3/1 6c3" (conduits-spec.csv: 1 occurrence, 633.0 px total length); no EE ensemble code for this spec (no "6c3" ensemble… |

## 5. Formule de conversion en coût canadien

Sources : National Estimator 2025, page imprimée 5 (PDF 6), « Labor Costs » : « *Costs in the Labor Cost column are the result of multiplying the manhours per unit by the rate of $46.59 per hour* » ; ce 46,59 $/h est le coût horaire **chargé** du livre (Journeyman Electrician : base 35,57 + avantages imposables 2,02 + taxes et assurances 7,21 + avantages non imposables 1,79 = 46,59 $/h). Matériel : « *estimates of what most electrical contractors who buy in moderate volume will pay suppliers in early-2025* », en USD. NECA, page imprimée 10 : « *All labor data in this manual are in units of man-hours* » ; E = l'unité, C = par 100 unités ou 100 pi lin., M = par 1 000, LF = pied linéaire, CY = verge cube.

Paramètres (à fournir, **aucune valeur n'est fixée ici**) :
- `TAUX_QC` — taux horaire électricien au Québec en CAD/h, **chargé** (salaire CCQ + avantages sociaux + charges patronales + CNESST) pour être comparable au 46,59 $/h du livre qui inclut ces éléments ;
- `FX_USDCAD` — taux de change USD→CAD retenu pour le matériel ;
- `Q` — quantité relevée (nombre de marques, ou longueur en pieds pour les conduits/fils) ;
- `k` — facteur de conditions NECA optionnel (colonne Normal = 1 ; Difficult / Very Difficult imprimées dans `neca_raw`).

Diviseur d'unité `d(u)` : NE `Ea` → 1, `CLF` → 100 pi, `KLF` → 1 000 pi ; NECA `E` → 1, `C` → 100, `M` → 1 000, `LF` → 1.

```
# National Estimator 2025 (ligne ne_*)
heures_NE        = ne_manhours × Q / d(ne_unit)                    # heures-personne, indépendantes de la devise
main_doeuvre_CAD = heures_NE × TAUX_QC
#   équivalent depuis la colonne Labor Cost du livre : (labor_usd / 46.59) × TAUX_QC
#   (labor_usd est arrondi au 10 cents dans le livre ; préférer ne_manhours)
materiel_CAD     = ne_material_usd × Q / d(ne_unit) × FX_USDCAD    # prix fournisseur début 2025, USD
cout_installe_CAD = materiel_CAD + main_doeuvre_CAD

# NECA 2021-2022 (ligne neca_*) — heures seulement, pas de matériel
heures_NECA      = neca_normal_hours × Q / d(neca_unit) × k        # k = 1 pour la colonne Normal
main_doeuvre_CAD = heures_NECA × TAUX_QC
#   famille à plusieurs lignes (conduit + fils) : sommer heures_NECA de chaque ligne
```

Exemple de mécanique (sans taux) : famille PRISE, NE p240-PDF « Ivory L1@0.20 Ea 1.05 9.32 10.37 » → 0,20 h × Q × TAUX_QC + 1,05 USD × Q × FX_USDCAD ; NECA p318 « 15 Amp 3 Wire 25.00 31.25 37.50 C » → 25,00 h / 100 × Q × TAUX_QC = 0,25 h par prise × TAUX_QC. Contrôle : 9,32 / 46,59 = 0,2000 h, cohérent avec la colonne Craft@Hrs.

Ce que la formule **ne** fait **pas** : indexation du matériel 2025 → date de la soumission, taxes de vente, frais généraux et profit, facteur de productivité local (le livre NE indique lui-même que si le coût horaire local est 25 % plus bas, réduire les chiffres de main-d'œuvre de 25 % — c'est exactement ce que fait le remplacement de 46,59 par `TAUX_QC`).
