# Écart relevé humain (Dupuis) / relevé IA — S-1844

_Généré le 2026-09-24 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `dossiers/S-1844/reference/S-1844-Dupuis-PlanExpert.qpl`
- IA : `dossiers/S-1844/planexpert/S-1844.qpl`
- Dimensions : `dossiers/S-1844/reference/dupuis-png-dimensions.txt` ; feuilles : `dossiers/S-1844/reference/feuilles-ia.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 42 / 7 |
| Feuilles IA (toutes / avec marques) | 12 / 7 |
| Pages humaines marquées appariées / non appariées | 7 / 0 |
| Feuilles IA marquées avec / sans page humaine | 5 / 2 |
| Marques humaines brutes | 716 |
| … dont exclues (pages en double, versions remplacées) | 8 |
| **Marques humaines retenues** | **708** |
| **Marques IA** | **773** |
| **Appariées** (seuil 1.2 % diag.) | **564** |
| Manquantes côté IA (humain seul) | 144 |
| En trop côté IA (IA seul) | 209 |
| Rappel (appariées / humaines) | 79.7 % |
| Précision (appariées / IA) | 73.0 % |
| … manquantes sur pages humaines non appariées | 0 |
| … en trop sur feuilles IA sans page humaine | 2 |
| Couples « même position, libellé différent » | 195 |
| Lignes (longueurs) humain / IA — non appariées | 15 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 436 | 272 | 337 | 61.6 % | 56.4 % |
| 1.2 % | 564 | 144 | 209 | 79.7 % | 73.0 % |
| 2.5 % | 652 | 56 | 121 | 92.1 % | 84.3 % |

## Anomalies et signalements

- Page humaine « 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 » : taille du raster inconnue et non estimable.
- Recalage géométrique, document « 23347_selection_global_soum_2026-08-13 » : 4 page(s) sûre(s), échelle relative médiane 0.844 × nominal, orientation(s) 0°, translation médiane (4.1 %, 6.0 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- page EN DOUBLE : « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 » → feuille E300 : 8/8 marques exclues, référence « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 » (doublons exclus du décompte, le reste est ajouté).
- Page « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 » → E200D (géométrie) : AMBIGU : E300 obtient 0.96.
- Page « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 » → E300D (géométrie) : AMBIGU : E300 obtient 0.78.
- Page « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 » → E200 (géométrie) : AMBIGU : E300 obtient 0.91.
- Page « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 6 » → E400 (géométrie) : AMBIGU : E300D obtient 0.88.
- Page « 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 » → E300 (géométrie) : AMBIGU : E300D obtient 1.00.
- Page « 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 » → E103 (nom) : taille du raster humain inconnue : marques non positionnables.

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| FIXTURE ENLEVER | Démo luminaire R (22 %) | 204 | 134 | 70 | 32 | -172 | 105 |
| FIXTURE D3-N | Projecteur D3-N (79 %) | 122 | 113 | 9 | 102 | -23 (groupe) | 24 |
| PRISE DEPLACER | Démo appareil prises/services (E.D.) (100 %) | 49 | 40 | 9 | 82 | +29 (groupe) | 0 |
| FIXTURE TYPE P2 | Panneau P2 (100 %) | 29 | 29 | 0 | 31 | +2 | 0 |
| FIXTURE TYPE D4-N | Projecteur D4-N (70 %) | 27 | 27 | 0 | 27 | -3 (groupe) | 8 |
| COUPLING | Projecteur D4-NT1 (27 %) | 23 | 15 | 8 | 22 | -7 (groupe) | 11 |
| prise | Prise duplex 15A (73 %) | 23 | 22 | 1 | 16 | -7 | 6 |
| FIXTURE TYPE R12-NS | Rail R12-NS (63 %) | 22 | 19 | 3 | 23 | +1 | 7 |
| FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 (58 %) | 19 | 19 | 0 | 21 | +2 | 8 |
| prise contrler np | Prise duplex BX caisse (64 %) | 14 | 14 | 0 | 11 | -3 | 5 |
| 4X4 | Descente EMT + boîte 4x4 (90 %) | 12 | 10 | 2 | 10 | -2 | 1 |
| FIXTURE TYPE T | Profilé T (100 %) | 12 | 11 | 1 | 20 | +8 | 0 |
| INFORMATIQUE | Sortie conduit dalle télécom (50 %) | 10 | 10 | 0 | 5 | -5 | 5 |
| SN | Haut-parleur suspendu SN (90 %) | 10 | 10 | 0 | 9 | -1 | 1 |
| FIXTURE TYPE R8-NS | Rail R8-NS (86 %) | 9 | 7 | 2 | 8 | -1 | 1 |
| TETE DOUBLE | Phare double U2 (78 %) | 9 | 9 | 0 | 7 | -2 | 2 |
| DP1 | — | 8 | 0 | 8 | 0 | — | 0 |
| FIXTURE TYPE J1 | Troffer J1 (100 %) | 8 | 8 | 0 | 8 | +0 | 0 |
| MONUMENT PLANCHER D | — | 7 | 0 | 7 | 0 | — | 0 |
| FIXTURE TYPE D3-NT1 | Projecteur D4-NT1 (83 %) | 6 | 6 | 0 | 22 | -7 (groupe) | 1 |
| BOITE 8X8 | Boîte de tirage 8x8 (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| EXIT U9 | Enseigne sortie U1 (25 %) | 5 | 4 | 1 | 3 | -2 | 3 |
| FIXTURE TYPE R4-NS | Rail R4-NS (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| FIXTURE TYPE S20-N | Linéaire S20-N (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| TETE SIMPLE | Phare simple U3 (75 %) | 5 | 4 | 1 | 6 | +1 | 1 |
| DP2 | — | 4 | 0 | 4 | 0 | — | 0 |
| FIXTURE TYPE P1 | Panneau P1 (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| NPP-20 | Boîte de jonction profilé T (67 %) | 4 | 3 | 1 | 5 | -2 (groupe) | 1 |
| PLINTHE RELO | Démo appareil prises/services (E.D.) (100 %) | 4 | 2 | 2 | 82 | +29 (groupe) | 0 |
| S04 | — | 4 | 0 | 4 | 0 | — | 0 |
| WSXA | Détecteur WSXA (100 %) | 4 | 4 | 0 | 6 | +1 (groupe) | 0 |
| FIXTURE TYPE G4 | Boîte de jonction profilé T (33 %) | 3 | 3 | 0 | 5 | -2 (groupe) | 2 |
| FIXTURE TYPE K3 | Réglette K3 (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| FIXTURE TYPE R6-NS | Projecteur D3-N (50 %) | 3 | 2 | 1 | 102 | -23 (groupe) | 1 |
| WSXA-G | Détecteur WSXA-G (100 %) | 3 | 2 | 1 | 4 | +1 | 0 |
| FIXTURE R6-NS | Projecteur D4-N (50 %) | 2 | 2 | 0 | 27 | -3 (groupe) | 1 |
| FIXTURE TYPE O8-N | Linéaire O8-N (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| NPP-16 | Batterie U6 (50 %) | 2 | 2 | 0 | 1 | -1 | 1 |
| PP1 | — | 2 | 0 | 2 | 0 | — | 0 |
| RELO FIXTURE TYPE BB | Encastré B-B (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| S03 | — | 2 | 0 | 2 | 0 | — | 0 |
| SECHOIRE | Sèche-mains SM (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| SW1 | — | 2 | 0 | 2 | 0 | — | 0 |
| 90DEGRE | Projecteur D4-N (100 %) | 1 | 1 | 0 | 27 | -3 (groupe) | 0 |
| FIXTURE TYPE G3 | Réglette G3 (100 %) | 1 | 1 | 0 | 2 | +1 | 0 |
| NPOD | Contrôleur NPOD (100 %) | 1 | 1 | 0 | 2 | +1 | 0 |
| NPODMA | Interrupteur NPODMA (100 %) | 1 | 1 | 0 | 3 | +2 | 0 |
| NPP-PCD | — | 1 | 0 | 1 | 0 | — | 0 |
| SW6 | — | 1 | 0 | 1 | 0 | — | 0 |
| T | — | 1 | 0 | 1 | 0 | — | 0 |
| TH | Détecteur WSXA (100 %) | 1 | 1 | 0 | 6 | +1 (groupe) | 0 |

**Libellés humains sans correspondance** (10) : DP1 (8), MONUMENT PLANCHER D (7), DP2 (4), S04 (4), PP1 (2), S03 (2), SW1 (2), NPP-PCD (1), SW6 (1), T (1).

**Libellés IA sans correspondance** (55) : Démo luminaire H (34), Démo luminaire C (32), Démo projecteur sur rail (27), Démo rail existant (21), Démo luminaire W (18), Démo luminaire J (10), Relais NPP16 (10), Applique extérieure AA (bailleur) (9), Démo luminaire S2 (9), Démo carré-cercle — à classer (7), Démo luminaire A1 (7), Démo luminaire sans type (6), Réglette G4 (6), Sortie télécom (6), Plinthe électrique (5), Démo luminaire D2 (4), Prise duplex circuit indépendant (4), Prise existante relocalisée (4), Rail R6-NS (4), Relais basse tension CVC (4), Démo luminaire C1 (3), Démo luminaire D1 (3), Démo luminaire FS (3), Démo phare d'urgence (3), Relais NPP PCD (3), Thermostat électricien (3), Démo interrupteur (2), Démo luminaire M (2), Raccordement serpentin SE (2), Relais NPP20 (2), Thermostat programmable (par CVAC) (2), BX 4 pi — à confirmer (1), Boîte 2x2 conduit 3/4 (fenêtres) (1), Contrôle de volume (1), Démarreur manuel (1), Démo enseigne de sortie (1), Démo luminaire A2 (1), Démo luminaire E (1), Enseigne sortie U9 (1), Enseigne sortie — type à confirmer (1), Linéaire sans étiquette — à classer (1), Minuterie évacuation (1), Mise en route nLight (forfait) (1), Prise 30A L5-30R (UPS) (1), Prise duplex affleurement plancher (1), Raccordement boîte à volume BV-01 (1), Raccordement chauffe-eau CE-1 (1), Raccordement pompe PR-1 (1), Raccordement ventilateur VE-01 — à confirmer (1), Raccordement ventilateur VE-02 (1), Raccordement volet motorisé (1), Sortie haut-parleur (1), Symbole double cercle cyan — à classer (1), Thermostat action inversée (raccordement) (1), Thermostat existant relocalisé (1).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | géométrie | 0.943 | 53 | 0 | 82 | 42 | 11 | 40 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | géométrie | 0.853 | 204 | 0 | 226 | 134 | 70 | 92 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | géométrie | 1.000 | 57 | 0 | 79 | 49 | 8 | 30 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 6 | E400 | géométrie | 0.882 | 17 | 0 | 16 | 15 | 2 | 1 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | géométrie | 1.000 | 354 | 0 | 368 | 324 | 30 | 44 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | E300 | géométrie | 1.000 | 8 | 8 | 368 | 0 | 0 | 44 |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | nom |  | 23 | 0 | 0 | 0 | 23 | 0 |
| — | E201 | feuille IA sans page humaine |  | 0 | 0 | 1 | 0 | 0 | 1 |
| — | E101 | feuille IA sans page humaine |  | 0 | 0 | 1 | 0 | 0 | 1 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PLINTHE RELO | 0.094 | 0.768 | 731 | 3043 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PLINTHE RELO | 0.376 | 0.865 | 2087 | 3387 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.442 | 0.414 | 2408 | 1780 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.253 | 0.697 | 1494 | 2791 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.251 | 0.706 | 1488 | 2823 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.245 | 0.748 | 1459 | 2970 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.332 | 0.785 | 1877 | 3102 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.496 | 0.786 | 2669 | 3106 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.457 | 0.787 | 2481 | 3109 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.413 | 0.787 | 2267 | 3111 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | E200D | PRISE DEPLACER | 0.376 | 0.788 | 2088 | 3113 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.221 | 0.175 | 1283 | 939 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.302 | 0.260 | 1676 | 1224 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.375 | 0.268 | 2034 | 1253 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.362 | 0.283 | 1971 | 1301 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.439 | 0.304 | 2345 | 1373 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.219 | 0.313 | 1275 | 1403 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.424 | 0.314 | 2272 | 1405 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.404 | 0.329 | 2172 | 1457 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.390 | 0.339 | 2106 | 1491 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.495 | 0.345 | 2617 | 1510 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.482 | 0.356 | 2552 | 1547 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.454 | 0.382 | 2415 | 1634 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.136 | 0.384 | 870 | 1643 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.218 | 0.388 | 1266 | 1656 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.441 | 0.395 | 2354 | 1677 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.362 | 0.398 | 1967 | 1690 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.525 | 0.410 | 2763 | 1730 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.413 | 0.421 | 2215 | 1767 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.503 | 0.434 | 2657 | 1809 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.542 | 0.436 | 2845 | 1816 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.333 | 0.443 | 1827 | 1840 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.490 | 0.453 | 2594 | 1874 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.223 | 0.463 | 1293 | 1907 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.477 | 0.463 | 2528 | 1908 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.138 | 0.469 | 881 | 1928 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.548 | 0.487 | 2875 | 1988 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.571 | 0.499 | 2987 | 2028 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.414 | 0.510 | 2223 | 2065 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.340 | 0.516 | 1864 | 2086 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.516 | 0.531 | 2719 | 2137 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.502 | 0.547 | 2652 | 2188 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.386 | 0.559 | 2085 | 2228 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.369 | 0.574 | 2004 | 2278 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.530 | 0.574 | 2787 | 2278 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.412 | 0.575 | 2214 | 2284 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.546 | 0.592 | 2863 | 2341 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.332 | 0.620 | 1825 | 2435 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.377 | 0.622 | 2043 | 2440 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.278 | 0.623 | 1563 | 2445 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.409 | 0.630 | 2198 | 2469 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.238 | 0.662 | 1368 | 2576 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.217 | 0.664 | 1265 | 2583 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.464 | 0.667 | 2466 | 2593 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.137 | 0.669 | 874 | 2597 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.421 | 0.671 | 2258 | 2605 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.373 | 0.680 | 2024 | 2634 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.456 | 0.685 | 2426 | 2652 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.485 | 0.698 | 2569 | 2695 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.218 | 0.721 | 1266 | 2773 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.605 | 0.725 | 3154 | 2785 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.614 | 0.730 | 3197 | 2804 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.177 | 0.735 | 1071 | 2822 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.322 | 0.739 | 1774 | 2834 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.238 | 0.740 | 1364 | 2837 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.136 | 0.742 | 871 | 2845 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.107 | 0.743 | 730 | 2849 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.433 | 0.752 | 2317 | 2879 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.504 | 0.752 | 2658 | 2879 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.362 | 0.758 | 1969 | 2899 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.339 | 0.765 | 1855 | 2921 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.590 | 0.783 | 3080 | 2983 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.132 | 0.795 | 852 | 3022 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.110 | 0.796 | 741 | 3027 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.456 | 0.798 | 2426 | 3033 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.273 | 0.799 | 1535 | 3036 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.296 | 0.817 | 1649 | 3095 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.565 | 0.818 | 2959 | 3100 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.302 | 0.852 | 1676 | 3214 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.532 | 0.853 | 2794 | 3218 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | E300D | FIXTURE ENLEVER | 0.215 | 0.864 | 1255 | 3252 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.434 | 0.304 | 2358 | 1234 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.320 | 0.304 | 1793 | 1235 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.564 | 0.642 | 3004 | 2440 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.498 | 0.849 | 2677 | 3174 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.417 | 0.850 | 2276 | 3177 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.469 | 0.850 | 2531 | 3179 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | MONUMENT PLANCHER D | 0.387 | 0.851 | 2122 | 3183 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | E200 | prise | 0.529 | 0.904 | 2832 | 3371 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 6 | E400 | 4X4 | 0.301 | 0.855 | 1568 | 3123 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 6 | E400 | 4X4 | 0.574 | 0.883 | 2927 | 3223 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.365 | 0.273 | 2006 | 1133 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.549 | 0.273 | 2921 | 1133 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.504 | 0.273 | 2700 | 1134 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.535 | 0.404 | 2855 | 1597 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.535 | 0.500 | 2853 | 1935 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.535 | 0.696 | 2853 | 2624 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.358 | 0.733 | 1972 | 2754 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | COUPLING | 0.430 | 0.822 | 2328 | 3068 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | EXIT U9 | 0.492 | 0.844 | 2639 | 3148 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.537 | 0.326 | 2861 | 1322 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.357 | 0.415 | 1965 | 1633 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.359 | 0.629 | 1979 | 2387 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.357 | 0.728 | 1967 | 2739 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.362 | 0.890 | 1990 | 3308 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.523 | 0.891 | 2793 | 3311 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.386 | 0.891 | 2112 | 3312 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.417 | 0.891 | 2266 | 3312 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE D3-N | 0.492 | 0.891 | 2640 | 3312 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R12-NS | 0.598 | 0.374 | 3165 | 1492 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R12-NS | 0.360 | 0.407 | 1980 | 1606 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R12-NS | 0.537 | 0.601 | 2861 | 2291 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R6-NS | 0.246 | 0.278 | 1413 | 1151 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R8-NS | 0.551 | 0.275 | 2931 | 1142 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE R8-NS | 0.461 | 0.757 | 2486 | 2839 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | FIXTURE TYPE T | 0.576 | 0.248 | 3057 | 1047 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | NPP-20 | 0.366 | 0.724 | 2010 | 2722 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | NPP-PCD | 0.364 | 0.716 | 2002 | 2695 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | T | 0.224 | 0.807 | 1307 | 3014 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | TETE SIMPLE | 0.327 | 0.825 | 1819 | 3081 |
| 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 | E300 | WSXA-G | 0.203 | 0.828 | 1203 | 3091 |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP2 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP2 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP2 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | DP2 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | PP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | PP1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S03 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S03 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S04 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S04 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S04 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | S04 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | SW1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | SW1 |  |  |  |  |
| 26-0108-02_ELECTRICITE_POUR SOUMISSION-page-00006 | E103 | SW6 |  |  |  |  |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.540 | 0.235 | 3075 | 1004 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.495 | 0.235 | 2817 | 1005 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.360 | 0.236 | 2048 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.378 | 0.236 | 2150 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.401 | 0.236 | 2286 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.419 | 0.236 | 2387 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.434 | 0.236 | 2472 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.439 | 0.236 | 2501 | 1009 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.456 | 0.236 | 2596 | 1010 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.445 | 0.246 | 2533 | 1051 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.570 | 0.253 | 3243 | 1081 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.297 | 0.279 | 1689 | 1193 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.570 | 0.282 | 3243 | 1205 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.570 | 0.347 | 3243 | 1482 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.524 | 0.358 | 2983 | 1530 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.277 | 0.421 | 1579 | 1796 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.504 | 0.593 | 2869 | 2533 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.198 | 0.625 | 1126 | 2668 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.251 | 0.625 | 1427 | 2671 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.574 | 0.629 | 3268 | 2687 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.636 | 1402 | 2718 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.642 | 1402 | 2743 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.151 | 0.652 | 861 | 2783 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.157 | 0.652 | 892 | 2783 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.652 | 1402 | 2784 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.291 | 0.653 | 1658 | 2789 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.160 | 0.657 | 911 | 2805 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.658 | 1402 | 2811 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.664 | 1402 | 2836 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.246 | 0.670 | 1402 | 2860 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.227 | 0.686 | 1295 | 2929 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.312 | 0.695 | 1778 | 2970 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.281 | 0.696 | 1600 | 2971 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.157 | 0.698 | 892 | 2983 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.416 | 0.701 | 2367 | 2992 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.182 | 0.723 | 1035 | 3089 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.265 | 0.726 | 1509 | 3102 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.300 | 0.738 | 1708 | 3151 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.196 | 0.739 | 1115 | 3156 |
| E200D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 2 | Démo appareil prises/services (E.D.) | 0.341 | 0.788 | 1940 | 3365 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo carré-cercle — à classer | 0.294 | 0.467 | 1672 | 1995 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo interrupteur | 0.139 | 0.148 | 794 | 633 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo interrupteur | 0.139 | 0.153 | 794 | 654 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire A1 | 0.558 | 0.400 | 3179 | 1709 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire A1 | 0.558 | 0.428 | 3179 | 1830 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire A1 | 0.558 | 0.485 | 3179 | 2070 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire A1 | 0.558 | 0.513 | 3179 | 2191 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.416 | 0.294 | 2366 | 1254 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.347 | 0.339 | 1974 | 1448 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.447 | 0.420 | 2543 | 1792 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.488 | 0.560 | 2777 | 2392 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.304 | 0.572 | 1729 | 2445 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.406 | 0.627 | 2311 | 2677 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.551 | 0.628 | 3135 | 2684 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.472 | 0.630 | 2686 | 2692 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.378 | 0.666 | 2154 | 2845 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C | 0.524 | 0.682 | 2984 | 2911 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C1 | 0.317 | 0.379 | 1804 | 1619 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C1 | 0.519 | 0.598 | 2953 | 2552 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire C1 | 0.564 | 0.678 | 3210 | 2894 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D1 | 0.292 | 0.392 | 1663 | 1674 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D1 | 0.292 | 0.448 | 1663 | 1912 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D2 | 0.530 | 0.395 | 3017 | 1688 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D2 | 0.516 | 0.397 | 2938 | 1697 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D2 | 0.543 | 0.404 | 3090 | 1724 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire D2 | 0.540 | 0.420 | 3072 | 1794 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire FS | 0.253 | 0.716 | 1438 | 3056 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire FS | 0.186 | 0.740 | 1057 | 3162 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire FS | 0.206 | 0.787 | 1175 | 3363 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.570 | 0.673 | 3246 | 2876 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.281 | 0.681 | 1602 | 2907 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.551 | 0.718 | 3136 | 3065 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.417 | 0.731 | 2373 | 3120 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.498 | 0.731 | 2835 | 3120 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.317 | 0.741 | 1807 | 3164 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.381 | 0.741 | 2171 | 3164 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.452 | 0.741 | 2575 | 3164 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.529 | 0.747 | 3010 | 3191 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.330 | 0.775 | 1878 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.362 | 0.775 | 2060 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.401 | 0.775 | 2283 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.433 | 0.775 | 2464 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.472 | 0.775 | 2687 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire H | 0.498 | 0.775 | 2835 | 3312 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire R | 0.475 | 0.701 | 2706 | 2993 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire R | 0.273 | 0.784 | 1552 | 3348 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire R | 0.297 | 0.784 | 1692 | 3348 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire S2 | 0.429 | 0.275 | 2440 | 1174 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire S2 | 0.456 | 0.286 | 2594 | 1221 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire S2 | 0.459 | 0.299 | 2615 | 1278 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire S2 | 0.494 | 0.320 | 2812 | 1366 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire S2 | 0.486 | 0.320 | 2765 | 1368 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.225 | 0.249 | 1283 | 1062 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.225 | 0.360 | 1283 | 1536 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.225 | 0.415 | 1283 | 1773 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.152 | 0.419 | 868 | 1789 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.225 | 0.582 | 1283 | 2485 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.152 | 0.586 | 868 | 2501 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire W | 0.152 | 0.641 | 868 | 2738 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire sans type | 0.128 | 0.151 | 728 | 646 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire sans type | 0.269 | 0.421 | 1531 | 1799 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo luminaire sans type | 0.298 | 0.686 | 1694 | 2931 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo phare d'urgence | 0.303 | 0.327 | 1728 | 1396 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo phare d'urgence | 0.577 | 0.627 | 3285 | 2676 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.339 | 0.334 | 1928 | 1425 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.327 | 0.342 | 1864 | 1462 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.339 | 0.372 | 1928 | 1587 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.349 | 0.418 | 1990 | 1786 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.372 | 0.463 | 2119 | 1977 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.314 | 0.473 | 1789 | 2020 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.399 | 0.510 | 2274 | 2178 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.553 | 0.532 | 3149 | 2274 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.426 | 0.548 | 2424 | 2341 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.314 | 0.550 | 1786 | 2351 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.488 | 0.560 | 2781 | 2392 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.295 | 0.583 | 1679 | 2488 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.462 | 0.592 | 2628 | 2528 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.553 | 0.595 | 3149 | 2541 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.322 | 0.627 | 1836 | 2676 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.327 | 0.634 | 1864 | 2709 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.390 | 0.650 | 2218 | 2775 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo projecteur sur rail | 0.521 | 0.650 | 2966 | 2776 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.449 | 0.283 | 2554 | 1207 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.504 | 0.336 | 2871 | 1433 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.399 | 0.369 | 2272 | 1577 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.303 | 0.414 | 1726 | 1767 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.286 | 0.442 | 1630 | 1888 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.301 | 0.487 | 1714 | 2082 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.286 | 0.546 | 1630 | 2333 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.353 | 0.592 | 2009 | 2530 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.554 | 0.594 | 3155 | 2539 |
| E300D | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 3 | Démo rail existant | 0.448 | 0.661 | 2549 | 2822 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | BX 4 pi — à confirmer | 0.247 | 0.622 | 1409 | 2658 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Contrôle de volume | 0.313 | 0.768 | 1781 | 3279 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Démarreur manuel | 0.205 | 0.748 | 1167 | 3193 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Minuterie évacuation | 0.122 | 0.147 | 695 | 626 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Plinthe électrique | 0.578 | 0.652 | 3289 | 2783 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Plinthe électrique | 0.338 | 0.790 | 1926 | 3376 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Plinthe électrique | 0.376 | 0.790 | 2139 | 3376 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Plinthe électrique | 0.452 | 0.790 | 2575 | 3376 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Plinthe électrique | 0.482 | 0.790 | 2743 | 3376 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement boîte à volume BV-01 | 0.304 | 0.737 | 1733 | 3149 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement chauffe-eau CE-1 | 0.194 | 0.734 | 1106 | 3134 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement pompe PR-1 | 0.204 | 0.743 | 1163 | 3172 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement serpentin SE | 0.148 | 0.691 | 840 | 2953 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement serpentin SE | 0.303 | 0.752 | 1728 | 3210 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement ventilateur VE-01 — à confirmer | 0.131 | 0.155 | 745 | 661 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Raccordement volet motorisé | 0.213 | 0.709 | 1211 | 3030 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Relais basse tension CVC | 0.576 | 0.625 | 3277 | 2671 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Relais basse tension CVC | 0.118 | 0.692 | 671 | 2954 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Relais basse tension CVC | 0.261 | 0.743 | 1488 | 3175 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Relais basse tension CVC | 0.392 | 0.788 | 2233 | 3365 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Sortie haut-parleur | 0.324 | 0.723 | 1845 | 3089 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Sortie télécom | 0.144 | 0.152 | 819 | 651 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Symbole double cercle cyan — à classer | 0.253 | 0.696 | 1442 | 2974 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat action inversée (raccordement) | 0.130 | 0.148 | 743 | 631 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat existant relocalisé | 0.313 | 0.771 | 1783 | 3295 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat programmable (par CVAC) | 0.160 | 0.698 | 911 | 2982 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat programmable (par CVAC) | 0.310 | 0.771 | 1763 | 3292 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat électricien | 0.239 | 0.700 | 1359 | 2989 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat électricien | 0.185 | 0.723 | 1053 | 3088 |
| E200 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 5 | Thermostat électricien | 0.206 | 0.764 | 1173 | 3261 |
| E400 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 6 | Descente EMT + boîte 4x4 | 0.319 | 0.645 | 1816 | 2753 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.157 | 0.102 | 895 | 435 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.278 | 0.166 | 1582 | 711 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.354 | 0.206 | 2014 | 880 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.099 | 0.219 | 566 | 936 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.594 | 0.337 | 3381 | 1440 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.099 | 0.590 | 565 | 2522 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.594 | 0.601 | 3385 | 2568 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.379 | 0.806 | 2157 | 3443 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Applique extérieure AA (bailleur) | 0.221 | 0.812 | 1257 | 3468 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Boîte de jonction profilé T | 0.568 | 0.228 | 3236 | 972 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Boîte de jonction profilé T | 0.576 | 0.237 | 3282 | 1012 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Contrôleur NPOD | 0.308 | 0.770 | 1753 | 3287 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Détecteur WSXA-G | 0.156 | 0.705 | 888 | 3010 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Détecteur WSXA-G | 0.308 | 0.765 | 1753 | 3267 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Enseigne sortie U1 | 0.275 | 0.587 | 1568 | 2508 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Interrupteur NPODMA | 0.121 | 0.609 | 687 | 2599 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Linéaire sans étiquette — à classer | 0.526 | 0.490 | 2995 | 2093 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Panneau P2 | 0.204 | 0.393 | 1160 | 1680 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Panneau P2 | 0.204 | 0.602 | 1162 | 2570 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Phare simple U3 | 0.197 | 0.738 | 1124 | 3150 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.274 | 0.423 | 1562 | 1807 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.577 | 0.546 | 3284 | 2332 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.577 | 0.562 | 3284 | 2400 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.577 | 0.578 | 3284 | 2467 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.577 | 0.593 | 3284 | 2534 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Profilé T | 0.275 | 0.703 | 1566 | 3003 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Projecteur D3-NT1 | 0.326 | 0.440 | 1857 | 1880 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Projecteur D4-NT1 | 0.309 | 0.255 | 1760 | 1088 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Rail R12-NS | 0.504 | 0.689 | 2872 | 2943 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP PCD | 0.539 | 0.484 | 3069 | 2068 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.398 | 0.341 | 2267 | 1457 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.412 | 0.341 | 2347 | 1457 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.573 | 0.367 | 3262 | 1568 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.185 | 0.543 | 1052 | 2320 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.185 | 0.543 | 1052 | 2320 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.564 | 0.566 | 3209 | 2416 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.278 | 0.608 | 1585 | 2597 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.537 | 0.727 | 3057 | 3105 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Relais NPP16 | 0.424 | 0.745 | 2417 | 3184 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Réglette G3 | 0.208 | 0.790 | 1187 | 3375 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Réglette G4 | 0.131 | 0.169 | 747 | 720 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Réglette G4 | 0.131 | 0.169 | 747 | 720 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Réglette G4 | 0.251 | 0.724 | 1427 | 3094 |
| E300 | 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 8 + 23347_SELECTION_GLOBAL_SOUM_2026-08-13 - 9 | Réglette G4 | 0.251 | 0.724 | 1427 | 3094 |
| E201 | — (aucune page humaine) | Raccordement ventilateur VE-02 | 0.223 | 0.739 | 1267 | 3157 |
| E101 | — (aucune page humaine) | Mise en route nLight (forfait) | 0.478 | 0.377 | 2722 | 1610 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| E200 | INFORMATIQUE | Sortie conduit dalle télécom | Sortie télécom | 1523 | 1794 |
| E200 | INFORMATIQUE | Sortie conduit dalle télécom | Sortie télécom | 775 | 2824 |
| E200 | INFORMATIQUE | Sortie conduit dalle télécom | Sortie télécom | 1557 | 3088 |
| E200 | INFORMATIQUE | Sortie conduit dalle télécom | Sortie télécom | 1776 | 3088 |
| E200 | INFORMATIQUE | Sortie conduit dalle télécom | Sortie télécom | 1595 | 3369 |
| E200 | SN | Haut-parleur suspendu SN | Prise duplex affleurement plancher | 3025 | 2457 |
| E200 | prise | Prise duplex 15A | Prise duplex BX caisse | 2386 | 1249 |
| E200 | prise | Prise duplex 15A | Prise duplex BX caisse | 1826 | 1254 |
| E200 | prise | Prise duplex 15A | Prise existante relocalisée | 2402 | 1771 |
| E200 | prise | Prise duplex 15A | Prise existante relocalisée | 3282 | 2920 |
| E200 | prise | Prise duplex 15A | Prise existante relocalisée | 2633 | 3358 |
| E200 | prise | Prise duplex 15A | Prise existante relocalisée | 2033 | 3361 |
| E200 | prise contrler np | Prise duplex BX caisse | Prise duplex circuit indépendant | 1523 | 1753 |
| E200 | prise contrler np | Prise duplex BX caisse | Prise 30A L5-30R (UPS) | 1470 | 2244 |
| E200 | prise contrler np | Prise duplex BX caisse | Prise duplex circuit indépendant | 793 | 2824 |
| E200 | prise contrler np | Prise duplex BX caisse | Prise duplex circuit indépendant | 1513 | 3088 |
| E200 | prise contrler np | Prise duplex BX caisse | Prise duplex circuit indépendant | 1732 | 3088 |
| E300 | COUPLING | Projecteur D4-NT1 | Rail R12-NS | 2374 | 1124 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D4-N | 3160 | 1463 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D3-NT1 | 1665 | 1483 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D3-N | 1957 | 1590 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D4-N | 3160 | 1819 |
| E300 | COUPLING | Projecteur D4-NT1 | Rail R12-NS | 1974 | 1897 |
| E300 | COUPLING | Projecteur D4-NT1 | Rail R12-NS | 2856 | 2243 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D3-N | 1957 | 2297 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D4-N | 1622 | 2732 |
| E300 | COUPLING | Projecteur D4-NT1 | Projecteur D3-N | 2431 | 2822 |
| E300 | COUPLING | Projecteur D4-NT1 | Enseigne sortie U1 | 2667 | 3093 |
| E300 | EXIT U9 | Enseigne sortie U1 | Enseigne sortie — type à confirmer | 1068 | 761 |
| E300 | EXIT U9 | Enseigne sortie U1 | Interrupteur NPODMA | 1419 | 2459 |
| E300 | EXIT U9 | Enseigne sortie U1 | Enseigne sortie U9 | 704 | 2498 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1785 | 1125 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1665 | 1180 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1665 | 1281 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1665 | 1382 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R12-NS | 3174 | 1435 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 1517 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R12-NS | 1988 | 1551 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-N | 3160 | 1582 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 1618 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-N | 3160 | 1700 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 1719 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1665 | 1887 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1848 | 1898 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 1921 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Relais NPP PCD | 1851 | 1924 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D3-NT1 | 1665 | 1988 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R12-NS | 1678 | 2128 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R12-NS | 3160 | 2128 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 2224 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R12-NS | 1974 | 2244 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Projecteur D4-NT1 | 1647 | 2325 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Relais NPP PCD | 2361 | 2902 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Rail R6-NS | 2770 | 3077 |
| E300 | FIXTURE D3-N | Projecteur D3-N | Relais NPP16 | 2415 | 3298 |
| E300 | FIXTURE R6-NS | Projecteur D4-N | Projecteur D4-NT1 | 1701 | 1109 |
| E300 | FIXTURE TYPE D3-NT1 | Projecteur D4-NT1 | Rail R12-NS | 3174 | 2821 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Rail R6-NS | 1852 | 1125 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Projecteur D3-N | 3142 | 1261 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Projecteur D3-N | 3142 | 1512 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Projecteur D3-N | 3142 | 1628 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Rail R12-NS | 3141 | 1751 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Projecteur D3-N | 3142 | 1931 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Profilé T | 3218 | 2239 |
| E300 | FIXTURE TYPE D4-N | Projecteur D4-N | Profilé T | 1566 | 2788 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Projecteur D4-NT1 | 1647 | 1113 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Projecteur D4-NT1 | 1647 | 1214 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Projecteur D4-NT1 | 1647 | 1315 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Projecteur D4-NT1 | 1647 | 1416 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Relais NPP20 | 1590 | 1922 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Relais NPP20 | 1590 | 1922 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Projecteur D4-NT1 | 1647 | 2022 |
| E300 | FIXTURE TYPE D4-NT1 | Projecteur D3-NT1 | Rail R8-NS | 1666 | 2363 |
| E300 | FIXTURE TYPE G4 | Boîte de jonction profilé T | Détecteur WSXA | 770 | 641 |
| E300 | FIXTURE TYPE G4 | Boîte de jonction profilé T | Réglette G4 | 989 | 3163 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Rail R6-NS | 1681 | 1124 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Rail R8-NS | 3120 | 1126 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Projecteur D3-N | 2838 | 1241 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Projecteur D3-N | 1975 | 1253 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Projecteur D3-N | 3142 | 1892 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Projecteur D3-N | 1957 | 1994 |
| E300 | FIXTURE TYPE R12-NS | Rail R12-NS | Projecteur D4-N | 3160 | 2180 |
| E300 | FIXTURE TYPE R6-NS | Projecteur D3-N | Rail R6-NS | 2692 | 3329 |
| E300 | FIXTURE TYPE R8-NS | Rail R8-NS | Projecteur D3-NT1 | 1665 | 2190 |
| E300 | NPP-16 | Batterie U6 | Projecteur D3-N | 1975 | 2675 |
| E300 | NPP-20 | Boîte de jonction profilé T | Profilé T | 3284 | 2598 |
| E300 | TETE DOUBLE | Phare double U2 | Phare simple U3 | 686 | 1096 |
| E300 | TETE DOUBLE | Phare double U2 | Phare simple U3 | 1481 | 1885 |
| E300 | TETE SIMPLE | Phare simple U3 | Réglette G4 | 989 | 3163 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 957 | 809 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 1283 | 824 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2001 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2179 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2357 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2535 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2713 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2891 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3068 | 1057 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 868 | 1077 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire E | 2681 | 1088 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire S2 | 2485 | 1156 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 1748 | 1163 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 2824 | 1179 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3076 | 1179 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3187 | 1179 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 1812 | 1227 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 2422 | 1249 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2208 | 1290 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire S2 | 2706 | 1290 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 1283 | 1299 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 868 | 1314 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2170 | 1351 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2089 | 1359 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3069 | 1361 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3187 | 1361 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire S2 | 2849 | 1401 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2592 | 1424 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire S2 | 2854 | 1471 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3187 | 1532 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 868 | 1552 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 1867 | 1559 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2352 | 1564 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3069 | 1578 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2744 | 1641 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2978 | 1664 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 3121 | 1672 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2111 | 1703 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire A2 | 1624 | 1718 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 1806 | 1756 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2461 | 1818 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2916 | 1835 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 3155 | 1852 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2107 | 1887 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2342 | 1943 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 1964 | 1951 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 2341 | 1997 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 3101 | 2008 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2735 | 2009 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 1283 | 2011 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 868 | 2026 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2658 | 2043 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 1761 | 2085 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire A1 | 1655 | 2090 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2109 | 2152 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2318 | 2165 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2554 | 2184 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2939 | 2200 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 3155 | 2207 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire A1 | 1655 | 2238 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2866 | 2242 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 1283 | 2248 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 868 | 2263 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 1919 | 2298 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 1838 | 2324 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2266 | 2336 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire D1 | 1668 | 2364 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2547 | 2399 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire A1 | 3179 | 2461 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2088 | 2498 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2467 | 2510 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo enseigne de sortie | 1564 | 2521 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2990 | 2569 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2801 | 2608 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire sans type | 1564 | 2636 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 1910 | 2659 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 3154 | 2689 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo phare d'urgence | 1651 | 2702 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2943 | 2720 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2199 | 2755 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 3246 | 2757 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 1728 | 2781 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2798 | 2791 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire M | 1438 | 2803 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo rail existant | 2823 | 2811 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire sans type | 1592 | 2826 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2098 | 2855 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire C | 2550 | 2867 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo projecteur sur rail | 2495 | 2878 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 2213 | 2880 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire sans type | 1794 | 2931 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire M | 1385 | 2952 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire W | 1057 | 2992 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire H | 1969 | 3120 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 1850 | 3142 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2032 | 3142 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2255 | 3142 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2436 | 3142 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2659 | 3142 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo carré-cercle — à classer | 1603 | 3208 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 1850 | 3231 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2031 | 3231 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2255 | 3231 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2436 | 3231 |
| E300D | FIXTURE ENLEVER | Démo luminaire R | Démo luminaire J | 2659 | 3231 |
| E400 | 4X4 | Descente EMT + boîte 4x4 | Boîte 2x2 conduit 3/4 (fenêtres) | 2358 | 3378 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
