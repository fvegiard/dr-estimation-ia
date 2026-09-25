# Écart relevé humain (Dupuis) / relevé IA — S-1811

_Généré le 2026-09-23 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `dossiers/S-1811/reference/S-1811-Dupuis-PlanExpert.qpl`
- IA : `dossiers/S-1811/planexpert/S-1811.qpl`
- Dimensions : `dossiers/S-1811/reference/dupuis-png-dimensions.txt` ; feuilles : `dossiers/S-1811/reference/feuilles-ia.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 67 / 10 |
| Feuilles IA (toutes / avec marques) | 36 / 7 |
| Pages humaines marquées appariées / non appariées | 10 / 0 |
| Feuilles IA marquées avec / sans page humaine | 5 / 2 |
| Marques humaines brutes | 1411 |
| … dont exclues (pages en double, versions remplacées) | 730 |
| **Marques humaines retenues** | **681** |
| **Marques IA** | **811** |
| **Appariées** (seuil 1.2 % diag.) | **676** |
| Manquantes côté IA (humain seul) | 5 |
| En trop côté IA (IA seul) | 135 |
| Rappel (appariées / humaines) | 99.3 % |
| Précision (appariées / IA) | 83.4 % |
| … manquantes sur pages humaines non appariées | 0 |
| … en trop sur feuilles IA sans page humaine | 7 |
| Couples « même position, libellé différent » | 44 |
| Lignes (longueurs) humain / IA — non appariées | 46 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 670 | 11 | 141 | 98.4 % | 82.6 % |
| 1.2 % | 676 | 5 | 135 | 99.3 % | 83.4 % |
| 2.5 % | 678 | 3 | 133 | 99.6 % | 83.6 % |

## Anomalies et signalements

- Page humaine « 00 Addenda MEP01_Plans-unlocked-page-00015 » : raster absent du fichier de dimensions, taille estimées (médiane du document) ≈ 6991×4943 px.
- Page humaine « 00 Addenda MEP01_Plans-unlocked-page-00016 » : raster absent du fichier de dimensions, taille estimées par recalage sur S267_ADD_21 (score 1.00) ≈ 7036×4954 px.
- Page humaine « 00 Addenda MEP01_Plans-unlocked-page-00017 » : raster absent du fichier de dimensions, taille estimées par recalage sur S267_ADD_22 (score 1.00) ≈ 6973×4933 px.
- Page humaine « 00 Addenda MEP01_Plans-unlocked-page-00018 » : raster absent du fichier de dimensions, taille estimées par recalage sur S267_ADD_23 (score 1.00) ≈ 6935×5026 px.
- Page humaine « 00 Addenda MEP01_Plans-unlocked-page-00019 » : raster absent du fichier de dimensions, taille estimées par recalage sur S267_ADD_24 (score 1.00) ≈ 7009×4921 px.
- Recalage géométrique, document « 00 addenda mep01_plans » : 1 page(s) sûre(s), échelle relative médiane 0.998 × nominal, orientation(s) 0°, translation médiane (0.1 %, -0.6 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « 00 electricite_plans_pour ao » : 4 page(s) sûre(s), échelle relative médiane 0.985 × nominal, orientation(s) 0°, translation médiane (0.7 %, 0.5 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- VERSION REMPLACÉE : « 00 Électricité_Plans_pour AO - 3 » → feuille S267_ADD_4 : 47/47 marques exclues, référence « 00 Addenda MEP01_Plans-unlocked-page-00015 » (page entière exclue du décompte (autre document, même feuille IA)).
- VERSION REMPLACÉE : « 00 Électricité_Plans_pour AO - 5 » → feuille S267_ADD_21 : 270/270 marques exclues, référence « 00 Addenda MEP01_Plans-unlocked-page-00016 » (page entière exclue du décompte (autre document, même feuille IA)).
- VERSION REMPLACÉE : « 00 Électricité_Plans_pour AO - 6 » → feuille S267_ADD_22 : 262/262 marques exclues, référence « 00 Addenda MEP01_Plans-unlocked-page-00017 » (page entière exclue du décompte (autre document, même feuille IA)).
- VERSION REMPLACÉE : « 00 Électricité_Plans_pour AO - 7 » → feuille S267_ADD_23 : 9/9 marques exclues, référence « 00 Addenda MEP01_Plans-unlocked-page-00018 » (page entière exclue du décompte (autre document, même feuille IA)).
- VERSION REMPLACÉE : « 00 Électricité_Plans_pour AO - 8 » → feuille S267_ADD_24 : 142/142 marques exclues, référence « 00 Addenda MEP01_Plans-unlocked-page-00019 » (page entière exclue du décompte (autre document, même feuille IA)).
- Page « 00 Électricité_Plans_pour AO - 3 » → S267_ADD_4 (géométrie) : le nom désignait S267_3 (score identité 0.00) ; la géométrie désigne S267_ADD_4.
- Page « 00 Électricité_Plans_pour AO - 5 » → S267_ADD_21 (géométrie) : le nom désignait S267_5 (score identité 0.00) ; la géométrie désigne S267_ADD_21.
- Page « 00 Électricité_Plans_pour AO - 6 » → S267_ADD_22 (géométrie) : le nom désignait S267_6 (score identité 0.00) ; la géométrie désigne S267_ADD_22.
- Page « 00 Électricité_Plans_pour AO - 7 » → S267_ADD_23 (géométrie) : le nom désignait S267_7 (score identité 0.00) ; la géométrie désigne S267_ADD_23 ; AMBIGU : S267_ADD_22 obtient 1.00.
- Page « 00 Électricité_Plans_pour AO - 8 » → S267_ADD_24 (géométrie) : le nom désignait S267_8 (score identité 0.00) ; la géométrie désigne S267_ADD_24.
- Page « 00 Addenda MEP01_Plans-unlocked-page-00015 » → S267_ADD_4 (géométrie) : le nom désignait S267_ADD_20 (score identité 0.00) ; la géométrie désigne S267_ADD_4.

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| ADD PRISE | Prise double 5-15R (100 %) | 110 | 108 | 2 | 108 | -2 | 0 |
| ADD KLAXON STROB | Klaxon/stroboscope (100 %) | 63 | 63 | 0 | 63 | +0 | 0 |
| ADD FIXTURE TYPE A1 | A1 Troffer 2x4 (90 %) | 59 | 59 | 0 | 53 | -6 | 6 |
| ADD DETECTEUR FUMÉE | Détecteur de fumée photoélectrique (100 %) | 44 | 44 | 0 | 50 | +0 (groupe) | 0 |
| ADD FIXTURE TYPE D1 | D1 High bay (67 %) | 43 | 43 | 0 | 29 | -14 | 14 |
| ADD FIXTURE TYPE C2 | C2 Spot lieux humides (100 %) | 36 | 36 | 0 | 36 | +0 | 0 |
| ADD C1.1 500W | C1.1 Plinthe 500W (100 %) | 34 | 34 | 0 | 34 | +0 | 0 |
| ADD INT DETEC | Interrupteur avec détecteur de présence (100 %) | 34 | 34 | 0 | 37 | +3 | 0 |
| ADD FIXTURE TYPE C1 | C1 Spot encastré (86 %) | 28 | 28 | 0 | 24 | -4 | 4 |
| ADD FIXTURE G2 | G2 Applique de zone type 2 (100 %) | 20 | 20 | 0 | 20 | +0 | 0 |
| ADD EXIT | X1 Enseigne d'issue (100 %) | 18 | 18 | 0 | 18 | +0 | 0 |
| ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h (62 %) | 16 | 16 | 0 | 10 | -6 | 6 |
| ADD FIXTURE TYPE E1 | E1 Réglette 4 pi (75 %) | 16 | 16 | 0 | 12 | -4 | 4 |
| ADD FIXTURE TYPE G3 | G3 Applique de zone type 3 (100 %) | 11 | 10 | 1 | 11 | -3 (groupe) | 0 |
| ADD ARM | Module de relais ARM (100 %) | 10 | 10 | 0 | 13 | +3 | 0 |
| ADD C4.1  1500W | C4.1 Plinthe 1500W (100 %) | 10 | 10 | 0 | 11 | +0 (groupe) | 0 |
| ADD SERPENTIN | Serpentin EHC1 19 kW (30 %) | 10 | 10 | 0 | 3 | -7 | 7 |
| ADD FIXTURE TYPE L5 | L5 Lampadaire type 5 (100 %) | 9 | 9 | 0 | 9 | +0 | 0 |
| ADD STATION MANUEL | Déclencheur manuel (100 %) | 9 | 9 | 0 | 9 | +0 | 0 |
| ADD  30A 20A | Sectionneur ≤240V (100 %) | 8 | 8 | 0 | 8 | +0 | 0 |
| ADD INT | Interrupteur unipolaire (57 %) | 7 | 7 | 0 | 4 | -3 | 3 |
| ADD DETECTEUR GAINE | Détecteur de fumée photoélectrique (100 %) | 6 | 6 | 0 | 50 | +0 (groupe) | 0 |
| ADD GRADATEUR | Gradateur (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| ADD STROB | Stroboscope mural (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| ADD PUIT ACCES | Puits d'accès électrique/télécom (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| ADD C6.1 1000W | C6.1 Plinthe 1000W (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| ADD FIXTURE TYPE B1 | B1 Troffer 2x2 (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| ADDFIXTURE TYPE L3 | L3 Lampadaire type 3 (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| ADD 30A NF WP | Sectionneur ≤240V WP (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD C2.2  4000W | C2.2 Convecteur 4000W (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD DETECTEUR FL -RX | Détecteur faisceau récepteur FL-RX (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD DETECTEUR FL-TX | Détecteur faisceau émetteur FL-TX (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD FIXTURE TYPE L2 | L2 Lampadaire type 2 (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD HE | Raccordement unité HE toit (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD HU1 | Raccordement humidificateur HU (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADD RT | Raccordement UTA toit RT (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| ADDCS1 | Raccordement condenseur CS (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| B2  2/6 1X12 | G3 Applique de zone type 3 (100 %) | 3 | 1 | 2 | 11 | -3 (groupe) | 0 |
| ADD AIM | Module d'interface AIM (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ADD C5.1   2000W | C5.1 Convecteur 2000W (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ADD DETEC 360 | Détecteur de présence plafond (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ADD EV1 | Raccordement évaporateur EV (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ADD TF2 | Raccordement ventilateur TF (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ONDULATEUR | Mini-onduleur 12V (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ADD C 5.2 2000W | C5.2 Convecteur 2000W (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ADD C1.1 1500W | C4.1 Plinthe 1500W (100 %) | 1 | 1 | 0 | 11 | +0 (groupe) | 0 |
| ADD C3.2 8000W | C3.2 Aérotherme 8000W (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ADD FAAP | Annonciateur FAAP (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ADD FAP | Panneau d'alarme incendie FAP (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ADD PAN CONTROL | Point de raccordement panneau de contrôle (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ADD PS1 | Bloc d'alimentation AI PS (100 %) | 1 | 1 | 0 | 2 | +0 (groupe) | 0 |
| ADD PS2 | Bloc d'alimentation AI PS (100 %) | 1 | 1 | 0 | 2 | +0 (groupe) | 0 |
| ADD PU1-REC | Raccordement pompe PU1 (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |

**Libellés humains sans correspondance** (0) : aucun.

**Libellés IA sans correspondance** (30) : Point de raccordement plomberie (32), Prise double 5-20R (25), Sortie télécom (15), D1 High bay urgence (14), Poteau de bois (8), Prise DDFT 5-15R (cercle) (8), C3 Spot boîtier 2h urgence (7), A1 Troffer 2x4 urgence (6), Point de raccordement volet coupe-feu (6), Poteau de bois additionnel note D (5), C1 Spot encastré urgence (4), E1 Réglette 4 pi urgence (4), Point de raccordement porte automatique (4), Raccordement ventilateur HVLS CF (4), Barre de mise à la terre (3), Départ futur ventilateur EF (3), Raccordement chauffe-eau WH (3), Raccordement prise UTA toit (fournie par fabricant) (3), Serpentin EHC1-006 500W (3), Serpentin EHC2 15 kW (3), Panneau 120/208V (2), Prise DDFT 5-15R (triangle) (2), Prise double 5-15R (triangle) (2), Armoire de mesurage HQ type B (1), Dispositif de mesurage GTB (1), Interrupteur principal 400A (1), Panneau 347/600V (1), Prise double 5-15R WP (1), Serpentin EHC3 3 kW douche (1), Transformateur sec 112.5 kVA (1).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 00 Électricité_Plans_pour AO - 3 | S267_ADD_4 | géométrie | 1.000 | 47 | 47 | 65 | 0 | 0 | 13 |
| 00 Électricité_Plans_pour AO - 5 | S267_ADD_21 | géométrie | 1.000 | 270 | 270 | 272 | 0 | 0 | 1 |
| 00 Électricité_Plans_pour AO - 6 | S267_ADD_22 | géométrie | 1.000 | 262 | 262 | 305 | 0 | 0 | 108 |
| 00 Électricité_Plans_pour AO - 7 | S267_ADD_23 | géométrie | 1.000 | 9 | 9 | 12 | 0 | 0 | 6 |
| 00 Électricité_Plans_pour AO - 8 | S267_ADD_24 | géométrie | 0.986 | 142 | 142 | 150 | 0 | 0 | 0 |
| 00 Addenda MEP01_Plans-unlocked-page-00015 | S267_ADD_4 | géométrie | 0.982 | 55 | 0 | 65 | 52 | 3 | 13 |
| 00 Addenda MEP01_Plans-unlocked-page-00016 | S267_ADD_21 | nom | 1.000 | 271 | 0 | 272 | 271 | 0 | 1 |
| 00 Addenda MEP01_Plans-unlocked-page-00017 | S267_ADD_22 | nom | 1.000 | 199 | 0 | 305 | 197 | 2 | 108 |
| 00 Addenda MEP01_Plans-unlocked-page-00018 | S267_ADD_23 | nom | 1.000 | 6 | 0 | 12 | 6 | 0 | 6 |
| 00 Addenda MEP01_Plans-unlocked-page-00019 | S267_ADD_24 | nom | 1.000 | 150 | 0 | 150 | 150 | 0 | 0 |
| 00 Addenda MEP-02_Plans - 4 | S267_ADD_4 | nom |  | 0 | 0 | 65 | 0 | 0 | 13 |
| — | S267_ADD_25 | feuille IA sans page humaine |  | 0 | 0 | 3 | 0 | 0 | 3 |
| — | S267_ADD_3 | feuille IA sans page humaine |  | 0 | 0 | 4 | 0 | 0 | 4 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| 00 Addenda MEP01_Plans-unlocked-page-00015 | S267_ADD_4 | ADD FIXTURE TYPE G3 | 0.498 | 0.406 | 2822 | 1617 |
| 00 Addenda MEP01_Plans-unlocked-page-00015 | S267_ADD_4 | B2  2/6 1X12 | 0.496 | 0.401 | 2814 | 1598 |
| 00 Addenda MEP01_Plans-unlocked-page-00015 | S267_ADD_4 | B2  2/6 1X12 | 0.496 | 0.454 | 2813 | 1811 |
| 00 Addenda MEP01_Plans-unlocked-page-00017 | S267_ADD_22 | ADD PRISE | 0.255 | 0.697 | 1441 | 2787 |
| 00 Addenda MEP01_Plans-unlocked-page-00017 | S267_ADD_22 | ADD PRISE | 0.255 | 0.783 | 1443 | 3132 |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.625 | 0.854 | 3557 | 3439 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.019 | 0.866 | 110 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.120 | 0.866 | 683 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.221 | 0.866 | 1256 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.322 | 0.866 | 1834 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.423 | 0.866 | 2406 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.524 | 0.866 | 2983 | 3489 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois | 0.625 | 0.886 | 3557 | 3569 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois additionnel note D | 0.024 | 0.848 | 139 | 3417 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois additionnel note D | 0.029 | 0.848 | 164 | 3417 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois additionnel note D | 0.033 | 0.848 | 190 | 3417 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois additionnel note D | 0.038 | 0.848 | 215 | 3417 |
| S267_ADD_4 | 00 Électricité_Plans_pour AO - 3 + 00 Addenda MEP01_Plans-unlocked-page-00015 | Poteau de bois additionnel note D | 0.042 | 0.848 | 240 | 3417 |
| S267_ADD_21 | 00 Électricité_Plans_pour AO - 5 + 00 Addenda MEP01_Plans-unlocked-page-00016 | C3 Spot boîtier 2h urgence | 0.385 | 0.701 | 2192 | 2825 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Armoire de mesurage HQ type B | 0.553 | 0.847 | 3150 | 3413 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Interrupteur principal 400A | 0.553 | 0.837 | 3148 | 3373 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Panneau 120/208V | 0.252 | 0.847 | 1437 | 3410 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Panneau 120/208V | 0.567 | 0.850 | 3229 | 3425 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Panneau 347/600V | 0.553 | 0.856 | 3148 | 3449 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.407 | 0.843 | 2319 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.412 | 0.843 | 2344 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.431 | 0.843 | 2454 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.435 | 0.843 | 2479 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.454 | 0.843 | 2587 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.459 | 0.843 | 2613 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.478 | 0.843 | 2721 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.482 | 0.843 | 2746 | 3395 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.289 | 0.845 | 1643 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.301 | 0.845 | 1712 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.313 | 0.845 | 1780 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.324 | 0.845 | 1847 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.336 | 0.845 | 1915 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.348 | 0.845 | 1982 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.360 | 0.845 | 2050 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.372 | 0.845 | 2118 | 3403 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.289 | 0.893 | 1643 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.301 | 0.893 | 1712 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.313 | 0.893 | 1780 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.324 | 0.893 | 1847 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.336 | 0.893 | 1915 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.348 | 0.893 | 1982 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.360 | 0.893 | 2050 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.372 | 0.893 | 2118 | 3599 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.407 | 0.896 | 2319 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.412 | 0.896 | 2344 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.431 | 0.896 | 2454 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.435 | 0.896 | 2479 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.454 | 0.896 | 2587 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.459 | 0.896 | 2613 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.478 | 0.896 | 2721 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement plomberie | 0.482 | 0.896 | 2746 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement porte automatique | 0.753 | 0.724 | 4289 | 2917 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement porte automatique | 0.030 | 0.803 | 168 | 3234 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement porte automatique | 0.082 | 0.803 | 465 | 3234 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement porte automatique | 0.753 | 0.915 | 4289 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.199 | 0.783 | 1133 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.269 | 0.783 | 1533 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.460 | 0.783 | 2621 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.555 | 0.783 | 3158 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.738 | 0.878 | 4201 | 3537 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Point de raccordement volet coupe-feu | 0.738 | 0.896 | 4201 | 3611 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.320 | 0.816 | 1824 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.330 | 0.816 | 1881 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.340 | 0.816 | 1937 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.435 | 0.816 | 2476 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.445 | 0.816 | 2533 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.455 | 0.816 | 2591 | 3288 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.204 | 0.842 | 1163 | 3391 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (cercle) | 0.204 | 0.856 | 1163 | 3447 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (triangle) | 0.215 | 0.865 | 1227 | 3483 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise DDFT 5-15R (triangle) | 0.215 | 0.905 | 1227 | 3645 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-15R (triangle) | 0.731 | 0.869 | 4164 | 3501 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-15R (triangle) | 0.804 | 0.899 | 4578 | 3623 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-15R WP | 0.583 | 0.924 | 3321 | 3721 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.742 | 0.747 | 4223 | 3008 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.101 | 0.783 | 575 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.224 | 0.783 | 1273 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.364 | 0.783 | 2074 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.478 | 0.783 | 2719 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.597 | 0.783 | 3397 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.720 | 0.783 | 4099 | 3153 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.221 | 0.822 | 1256 | 3312 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.244 | 0.822 | 1389 | 3312 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.563 | 0.823 | 3207 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.544 | 0.837 | 3096 | 3373 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.544 | 0.846 | 3096 | 3407 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.528 | 0.851 | 3008 | 3429 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.742 | 0.868 | 4223 | 3496 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.205 | 0.882 | 1168 | 3552 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.380 | 0.890 | 2165 | 3586 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.205 | 0.891 | 1168 | 3589 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.528 | 0.896 | 3008 | 3609 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.254 | 0.900 | 1447 | 3625 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.205 | 0.900 | 1168 | 3626 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.166 | 0.915 | 948 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.173 | 0.915 | 986 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.180 | 0.915 | 1023 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.187 | 0.915 | 1062 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Prise double 5-20R | 0.193 | 0.915 | 1099 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement chauffe-eau WH | 0.077 | 0.473 | 438 | 1906 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement chauffe-eau WH | 0.102 | 0.473 | 578 | 1906 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement chauffe-eau WH | 0.127 | 0.473 | 722 | 1906 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement ventilateur HVLS CF | 0.121 | 0.734 | 688 | 2956 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement ventilateur HVLS CF | 0.292 | 0.734 | 1663 | 2956 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement ventilateur HVLS CF | 0.482 | 0.734 | 2744 | 2956 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Raccordement ventilateur HVLS CF | 0.654 | 0.734 | 3723 | 2956 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.576 | 0.823 | 3277 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.619 | 0.823 | 3525 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.634 | 0.823 | 3611 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.650 | 0.823 | 3699 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.665 | 0.823 | 3785 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.680 | 0.823 | 3871 | 3315 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.576 | 0.908 | 3280 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.605 | 0.908 | 3446 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.620 | 0.908 | 3532 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.636 | 0.908 | 3620 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.651 | 0.908 | 3706 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.666 | 0.908 | 3794 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.681 | 0.908 | 3880 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.697 | 0.908 | 3966 | 3658 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Sortie télécom | 0.811 | 0.915 | 4616 | 3685 |
| S267_ADD_22 | 00 Électricité_Plans_pour AO - 6 + 00 Addenda MEP01_Plans-unlocked-page-00017 | Transformateur sec 112.5 kVA | 0.561 | 0.863 | 3197 | 3478 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Module de relais ARM | 0.249 | 0.803 | 1420 | 3236 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Module de relais ARM | 0.525 | 0.803 | 2988 | 3236 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Module de relais ARM | 0.834 | 0.803 | 4746 | 3236 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Raccordement prise UTA toit (fournie par fabricant) | 0.226 | 0.809 | 1288 | 3258 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Raccordement prise UTA toit (fournie par fabricant) | 0.829 | 0.811 | 4718 | 3266 |
| S267_ADD_23 | 00 Électricité_Plans_pour AO - 7 + 00 Addenda MEP01_Plans-unlocked-page-00018 | Raccordement prise UTA toit (fournie par fabricant) | 0.519 | 0.811 | 2956 | 3268 |
| S267_ADD_25 | — (aucune page humaine) | Départ futur ventilateur EF | 0.304 | 0.162 | 1729 | 653 |
| S267_ADD_25 | — (aucune page humaine) | Départ futur ventilateur EF | 0.193 | 0.167 | 1097 | 671 |
| S267_ADD_25 | — (aucune page humaine) | Départ futur ventilateur EF | 0.193 | 0.181 | 1097 | 729 |
| S267_ADD_3 | — (aucune page humaine) | Barre de mise à la terre | 0.421 | 0.591 | 2395 | 2379 |
| S267_ADD_3 | — (aucune page humaine) | Barre de mise à la terre | 0.472 | 0.591 | 2690 | 2379 |
| S267_ADD_3 | — (aucune page humaine) | Barre de mise à la terre | 0.740 | 0.872 | 4211 | 3513 |
| S267_ADD_3 | — (aucune page humaine) | Dispositif de mesurage GTB | 0.321 | 0.809 | 1825 | 3260 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 4685 | 2850 |
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 4551 | 3079 |
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 4551 | 3309 |
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 3760 | 3431 |
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 780 | 3491 |
| S267_ADD_21 | ADD FIXTURE TYPE A1 | A1 Troffer 2x4 | A1 Troffer 2x4 urgence | 4685 | 3539 |
| S267_ADD_21 | ADD FIXTURE TYPE C1 | C1 Spot encastré | C1 Spot encastré urgence | 1296 | 3450 |
| S267_ADD_21 | ADD FIXTURE TYPE C1 | C1 Spot encastré | C1 Spot encastré urgence | 1395 | 3507 |
| S267_ADD_21 | ADD FIXTURE TYPE C1 | C1 Spot encastré | C1 Spot encastré urgence | 1395 | 3592 |
| S267_ADD_21 | ADD FIXTURE TYPE C1 | C1 Spot encastré | C1 Spot encastré urgence | 1296 | 3650 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 4270 | 2837 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 248 | 3178 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 359 | 3178 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 248 | 3264 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 359 | 3264 |
| S267_ADD_21 | ADD FIXTURE TYPE C3 | C3 Spot boîtier 2h | C3 Spot boîtier 2h urgence | 4270 | 3635 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 302 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 1062 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 1791 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 2633 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 3360 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 4091 | 2936 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 530 | 3215 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 1305 | 3215 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 2209 | 3215 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 3118 | 3215 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 3848 | 3215 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 4289 | 3217 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 1791 | 3482 |
| S267_ADD_21 | ADD FIXTURE TYPE D1 | D1 High bay | D1 High bay urgence | 2633 | 3482 |
| S267_ADD_21 | ADD FIXTURE TYPE E1 | E1 Réglette 4 pi | E1 Réglette 4 pi urgence | 3045 | 3347 |
| S267_ADD_21 | ADD FIXTURE TYPE E1 | E1 Réglette 4 pi | E1 Réglette 4 pi urgence | 1351 | 3356 |
| S267_ADD_21 | ADD FIXTURE TYPE E1 | E1 Réglette 4 pi | E1 Réglette 4 pi urgence | 360 | 3488 |
| S267_ADD_21 | ADD FIXTURE TYPE E1 | E1 Réglette 4 pi | E1 Réglette 4 pi urgence | 3066 | 3542 |
| S267_ADD_21 | ADD INT | Interrupteur unipolaire | Interrupteur avec détecteur de présence | 438 | 3403 |
| S267_ADD_21 | ADD INT | Interrupteur unipolaire | Interrupteur avec détecteur de présence | 3013 | 3422 |
| S267_ADD_21 | ADD INT | Interrupteur unipolaire | Interrupteur avec détecteur de présence | 3013 | 3572 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC2 15 kW | 1266 | 3224 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC2 15 kW | 2996 | 3224 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC2 15 kW | 4735 | 3224 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC1-006 500W | 3366 | 3378 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC1-006 500W | 3366 | 3576 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC1-006 500W | 4074 | 3587 |
| S267_ADD_22 | ADD SERPENTIN | Serpentin EHC1 19 kW | Serpentin EHC3 3 kW douche | 2043 | 3614 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
