# Écart relevé humain (Dupuis) / relevé IA — S-1714

_Généré le 2026-09-23 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `dossiers/S-1714/reference/S-1714-Dupuis-PlanExpert.qpl`
- IA : `dossiers/S-1714/planexpert/S-1714.qpl`
- Dimensions : `dossiers/S-1714/reference/dupuis-png-dimensions.txt` ; feuilles : `dossiers/S-1714/reference/feuilles-ia.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 52 / 36 |
| Feuilles IA (toutes / avec marques) | 44 / 29 |
| Pages humaines marquées appariées / non appariées | 36 / 0 |
| Feuilles IA marquées avec / sans page humaine | 28 / 1 |
| Marques humaines brutes | 8503 |
| … dont exclues (pages en double, versions remplacées) | 1001 |
| **Marques humaines retenues** | **7502** |
| **Marques IA** | **7385** |
| **Appariées** (seuil 1.2 % diag.) | **7219** |
| Manquantes côté IA (humain seul) | 283 |
| En trop côté IA (IA seul) | 166 |
| Rappel (appariées / humaines) | 96.2 % |
| Précision (appariées / IA) | 97.8 % |
| … manquantes sur pages humaines non appariées | 0 |
| … en trop sur feuilles IA sans page humaine | 15 |
| Couples « même position, libellé différent » | 1557 |
| Lignes (longueurs) humain / IA — non appariées | 54 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 6965 | 537 | 420 | 92.8 % | 94.3 % |
| 1.2 % | 7219 | 283 | 166 | 96.2 % | 97.8 % |
| 2.5 % | 7250 | 252 | 135 | 96.6 % | 98.2 % |

## Anomalies et signalements

- page EN DOUBLE : « 01-PLANS - 34 2 » → feuille E401 : 156/156 marques exclues, référence « 01-PLANS - 34 2 1 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 35 2 » → feuille E402 : 137/137 marques exclues, référence « 01-PLANS - 35 2 1 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 36 2 1 » → feuille E403 : 139/139 marques exclues, référence « 01-PLANS - 36 2 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 37 2 1 » → feuille E404 : 138/138 marques exclues, référence « 01-PLANS - 37 2 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 38 2 1 » → feuille E405 : 140/140 marques exclues, référence « 01-PLANS - 38 2 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 39 2 1 » → feuille E406 : 141/141 marques exclues, référence « 01-PLANS - 39 2 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 40 2 1 » → feuille E407 : 84/84 marques exclues, référence « 01-PLANS - 40 2 » (doublons exclus du décompte, le reste est ajouté).
- page EN DOUBLE : « 01-PLANS - 41 2 1 » → feuille E408 : 66/66 marques exclues, référence « 01-PLANS - 41 2 » (doublons exclus du décompte, le reste est ajouté).

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| LO PRISE | Prise double (62 %) | 2167 | 2167 | 0 | 1616 | -945 (groupe) | 820 |
| LO PRISE CONTROLÉ | Prise demi-commandée (95 %) | 588 | 587 | 1 | 586 | -2 | 32 |
| TH | Thermostat (94 %) | 398 | 398 | 0 | 398 | +0 | 22 |
| AF1-5 | Avertisseur de fumée (87 %) | 387 | 383 | 4 | 336 | -51 | 48 |
| KS | Klaxon/stroboscope (100 %) | 363 | 361 | 2 | 362 | -1 | 0 |
| LO PRISE GFI | Prise salle de bain (47 %) | 334 | 334 | 0 | 179 | -155 | 177 |
| INT | Avertisseur fumée/CO (67 %) | 227 | 6 | 221 | 52 | -175 | 2 |
| FIXT TYPE UE2 | Luminaire — à classer (77 %) | 214 | 212 | 2 | 325 | -178 (groupe) | 48 |
| PLAFONNIER | Luminaire — à classer (55 %) | 207 | 206 | 1 | 325 | -178 (groupe) | 93 |
| B 1000W | Plinthe 1000W (87 %) | 203 | 203 | 0 | 232 | -1 (groupe) | 27 |
| LO TEL | Sortie câblo/informatique (71 %) | 193 | 192 | 1 | 140 | -53 | 55 |
| B 300W | Plinthe 300W (98 %) | 157 | 157 | 0 | 159 | +0 (groupe) | 3 |
| LO PRISE GFI WP | Prise étanche (98 %) | 156 | 156 | 0 | 163 | +0 (groupe) | 3 |
| LO CONENSEUR | Raccordement condenseur (97 %) | 144 | 143 | 1 | 145 | -2 (groupe) | 4 |
| LO P3000 | Prise double (26 %) | 142 | 140 | 2 | 1616 | -945 (groupe) | 103 |
| LO PRISE POELE | Prise cuisinière (99 %) | 141 | 141 | 0 | 140 | -1 | 1 |
| LO PRISE SÉCHEUSE | Prise sécheuse (99 %) | 141 | 141 | 0 | 140 | -1 | 1 |
| LO HOTTE | Raccordement hotte (100 %) | 140 | 140 | 0 | 140 | +0 | 0 |
| LO TV | Prise double (71 %) | 139 | 136 | 3 | 1616 | -945 (groupe) | 40 |
| LO EVAP | Raccordement évaporateur (98 %) | 125 | 125 | 0 | 147 | +0 (groupe) | 3 |
| SERV PRISE | Prise double (99 %) | 111 | 110 | 1 | 1616 | -945 (groupe) | 1 |
| DF1 | Détecteur de fumée (100 %) | 105 | 105 | 0 | 106 | +1 | 0 |
| exit | Luminaire — à classer (54 %) | 72 | 72 | 0 | 325 | -178 (groupe) | 33 |
| RWF 1500W | Aéroconvecteur 1500W (72 %) | 71 | 71 | 0 | 71 | +0 | 20 |
| KLAXON | Klaxon (100 %) | 50 | 50 | 0 | 52 | +2 | 0 |
| B 1250W | Plinthe 1250W (98 %) | 46 | 46 | 0 | 47 | +1 | 1 |
| RWF 2000W | Aéroconvecteur 2000W (76 %) | 38 | 38 | 0 | 38 | +0 | 9 |
| DM | Déclencheur manuel (100 %) | 36 | 36 | 0 | 36 | +0 | 0 |
| LO VENT | Raccordement ventilateur (100 %) | 35 | 35 | 0 | 62 | +22 (groupe) | 0 |
| DF2 | Détecteur de fumée de gaine (97 %) | 34 | 34 | 0 | 33 | -1 | 1 |
| RELAIS | Relais adressable (100 %) | 31 | 30 | 1 | 31 | +0 | 0 |
| b 1000w 347v | Plinthe 1000W (100 %) | 30 | 30 | 0 | 232 | -1 (groupe) | 0 |
| MA | Module adressable (96 %) | 28 | 28 | 0 | 27 | -1 | 1 |
| B 500W | Plinthe 500W (100 %) | 26 | 26 | 0 | 26 | +0 | 0 |
| RWF 1250W | Aéroconvecteur 1250W (92 %) | 25 | 25 | 0 | 25 | +0 | 2 |
| DV | Supervision vanne gicleur (100 %) | 22 | 22 | 0 | 22 | +0 | 0 |
| PLAFOND | — | 21 | 0 | 21 | 0 | — | 0 |
| L EVAP | Raccordement évaporateur (89 %) | 18 | 18 | 0 | 147 | +0 (groupe) | 2 |
| DD | Détecteur débit gicleur (100 %) | 17 | 17 | 0 | 17 | +0 | 0 |
| INX | Panneau INX (100 %) | 14 | 14 | 0 | 14 | +0 | 0 |
| RWF1000W | Aéroconvecteur 1000W (100 %) | 14 | 14 | 0 | 14 | +0 | 0 |
| VCFF | Raccordement volet motorisé (64 %) | 14 | 14 | 0 | 14 | +0 | 5 |
| APPLIQUE MURAL EXT | Luminaire — à classer (100 %) | 10 | 9 | 1 | 325 | -178 (groupe) | 0 |
| B 1500W | Plinthe 1500W (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| EVG | Raccordement évaporateur (100 %) | 4 | 4 | 0 | 147 | +0 (groupe) | 0 |
| serv gfi wp | Prise étanche (100 %) | 4 | 4 | 0 | 163 | +0 (groupe) | 0 |
| SERV PRISE GFI WP | Prise étanche (100 %) | 3 | 3 | 0 | 163 | +0 (groupe) | 0 |
| B 300W 347V | Plinthe 300W (100 %) | 2 | 2 | 0 | 159 | +0 (groupe) | 0 |
| PANN POMPE | Raccordement équipement mécanique (100 %) | 2 | 1 | 1 | 28 | +19 (groupe) | 0 |
| SERPENTIN | Raccordement équipement mécanique (100 %) | 2 | 2 | 0 | 28 | +19 (groupe) | 0 |
| SERV TEL | Sortie informatique (100 %) | 2 | 2 | 0 | 55 | +53 | 0 |
| WF 4000W 347V | Aéroconvecteur commun (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| AF-1 | Raccordement équipement mécanique (100 %) | 1 | 1 | 0 | 28 | +19 (groupe) | 0 |
| AG-1A | — | 1 | 0 | 1 | 0 | — | 0 |
| AG-1B | — | 1 | 0 | 1 | 0 | — | 0 |
| COND BUREAU | Raccordement condenseur (100 %) | 1 | 1 | 0 | 145 | -2 (groupe) | 0 |
| COND CONF | Raccordement condenseur (100 %) | 1 | 1 | 0 | 145 | -2 (groupe) | 0 |
| COND YOGA | Raccordement condenseur (100 %) | 1 | 1 | 0 | 145 | -2 (groupe) | 0 |
| DF3 | Détecteur fumée/CO (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| EA-1 | Raccordement équipement mécanique (100 %) | 1 | 1 | 0 | 28 | +19 (groupe) | 0 |
| GSM | — | 1 | 0 | 1 | 0 | — | 0 |
| P--1A | — | 1 | 0 | 1 | 0 | — | 0 |
| P-1B | Raccordement ventilateur (100 %) | 1 | 1 | 0 | 62 | +22 (groupe) | 0 |
| P-2A | Raccordement ventilateur (100 %) | 1 | 1 | 0 | 62 | +22 (groupe) | 0 |
| P-2B | — | 1 | 0 | 1 | 0 | — | 0 |
| P-3 | — | 1 | 0 | 1 | 0 | — | 0 |
| P-4 | Prise double (100 %) | 1 | 1 | 0 | 1616 | -945 (groupe) | 0 |
| PORTE GARAGE | — | 1 | 0 | 1 | 0 | — | 0 |
| V-10 | Raccordement équipement mécanique (100 %) | 1 | 1 | 0 | 28 | +19 (groupe) | 0 |
| V-11 | Sectionneur (100 %) | 1 | 1 | 0 | 148 | +146 (groupe) | 0 |
| V-12 | Équipement salle électrique — à classer (100 %) | 1 | 1 | 0 | 11 | +9 (groupe) | 0 |
| V-13 | — | 1 | 0 | 1 | 0 | — | 0 |
| V-14A | — | 1 | 0 | 1 | 0 | — | 0 |
| V-14B | — | 1 | 0 | 1 | 0 | — | 0 |
| V-14C | — | 1 | 0 | 1 | 0 | — | 0 |
| V-15 | Raccordement ventilateur (100 %) | 1 | 1 | 0 | 62 | +22 (groupe) | 0 |
| V-16 | — | 1 | 0 | 1 | 0 | — | 0 |
| V-1A | Raccordement ventilateur (100 %) | 1 | 1 | 0 | 62 | +22 (groupe) | 0 |
| V-1B | — | 1 | 0 | 1 | 0 | — | 0 |
| V-1C | — | 1 | 0 | 1 | 0 | — | 0 |
| V-1D | — | 1 | 0 | 1 | 0 | — | 0 |
| V-2A | Équipement salle électrique — à classer (100 %) | 1 | 1 | 0 | 11 | +9 (groupe) | 0 |
| V-2B | Transformateur (100 %) | 1 | 1 | 0 | 11 | +10 | 0 |
| V-2C | — | 1 | 0 | 1 | 0 | — | 0 |
| V-3 | Prise double (100 %) | 1 | 1 | 0 | 1616 | -945 (groupe) | 0 |
| V-4 | Sectionneur (100 %) | 1 | 1 | 0 | 148 | +146 (groupe) | 0 |
| V-5A | Raccordement équipement mécanique (100 %) | 1 | 1 | 0 | 28 | +19 (groupe) | 0 |
| V-5B | — | 1 | 0 | 1 | 0 | — | 0 |
| V-6 | — | 1 | 0 | 1 | 0 | — | 0 |
| V-7 | — | 1 | 0 | 1 | 0 | — | 0 |
| V-8 | — | 1 | 0 | 1 | 0 | — | 0 |
| V-9 | Raccordement ventilateur (100 %) | 1 | 1 | 0 | 62 | +22 (groupe) | 0 |
| serv af-2 | Raccordement équipement mécanique (100 %) | 1 | 1 | 0 | 28 | +19 (groupe) | 0 |

**Libellés humains sans correspondance** (21) : PLAFOND (21), AG-1A (1), AG-1B (1), GSM (1), P--1A (1), P-2B (1), P-3 (1), PORTE GARAGE (1), V-13 (1), V-14A (1), V-14B (1), V-14C (1), V-16 (1), V-1B (1), V-1C (1), V-1D (1), V-2C (1), V-5B (1), V-6 (1), V-7 (1), V-8 (1).

**Libellés IA sans correspondance** (12) : Prise comptoir (278), Panneau de logement (140), Prise laveuse (140), Prise micro-onde (140), Prise réfrigérateur (140), Raccordement lave-vaisselle (140), Luminaire encastré urgence (94), Résistance fin de ligne (56), Luminaire linéaire applique urgence (48), Enseigne sortie (33), Panneau de distribution (17), Aérotherme (2).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 01-PLANS - 27 2 | E304 | nom | 1.000 | 31 | 0 | 31 | 31 | 0 | 0 |
| 01-PLANS - 14 | E201 | nom | 0.999 | 792 | 0 | 789 | 788 | 4 | 1 |
| 01-PLANS - 15 | E202 | nom | 1.000 | 800 | 0 | 810 | 800 | 0 | 10 |
| 01-PLANS - 16 | E203 | nom | 1.000 | 818 | 0 | 819 | 818 | 0 | 1 |
| 01-PLANS - 17 2 | E204 | nom | 1.000 | 818 | 0 | 821 | 818 | 0 | 3 |
| 01-PLANS - 18 2 | E205 | nom | 1.000 | 817 | 0 | 819 | 815 | 2 | 4 |
| 01-PLANS - 19 2 | E206 | nom | 1.000 | 819 | 0 | 820 | 817 | 2 | 3 |
| 01-PLANS - 20 2 | E207 | nom | 1.000 | 422 | 0 | 427 | 422 | 0 | 5 |
| 01-PLANS - 13 | E200 | nom | 0.824 | 74 | 0 | 114 | 53 | 21 | 61 |
| 01-PLANS - 21 2 | E208 | nom | 1.000 | 300 | 0 | 304 | 300 | 0 | 4 |
| 01-PLANS - 22 2 | E209 | nom | 1.000 | 2 | 0 | 2 | 2 | 0 | 0 |
| 01-PLANS - 23 2 | E300 | nom | 1.000 | 187 | 0 | 187 | 187 | 0 | 0 |
| 01-PLANS - 24 2 | E301 | nom | 0.976 | 123 | 0 | 119 | 119 | 4 | 0 |
| 01-PLANS - 25 2 | E302 | nom | 1.000 | 30 | 0 | 31 | 30 | 0 | 1 |
| 01-PLANS - 26 2 | E303 | nom | 1.000 | 31 | 0 | 31 | 31 | 0 | 0 |
| 01-PLANS - 28 2 | E305 | nom | 1.000 | 31 | 0 | 31 | 31 | 0 | 0 |
| 01-PLANS - 29 2 | E306 | nom | 1.000 | 31 | 0 | 31 | 31 | 0 | 0 |
| 01-PLANS - 30 2 | E307 | nom | 1.000 | 24 | 0 | 24 | 24 | 0 | 0 |
| 01-PLANS - 31 2 | E308 | nom | 1.000 | 15 | 0 | 15 | 15 | 0 | 0 |
| 01-PLANS - 33 2 | E400 | nom | 1.000 | 88 | 0 | 99 | 87 | 1 | 12 |
| 01-PLANS - 34 2 | E401 | nom | 1.000 | 156 | 156 | 161 | 0 | 0 | 7 |
| 01-PLANS - 35 2 | E402 | nom | 1.000 | 137 | 137 | 144 | 0 | 0 | 5 |
| 01-PLANS - 36 2 | E403 | nom | 1.000 | 139 | 0 | 145 | 139 | 0 | 6 |
| 01-PLANS - 37 2 | E404 | nom | 1.000 | 138 | 0 | 145 | 138 | 0 | 7 |
| 01-PLANS - 38 2 | E405 | nom | 1.000 | 140 | 0 | 146 | 140 | 0 | 6 |
| 01-PLANS - 39 2 | E406 | nom | 1.000 | 141 | 0 | 146 | 141 | 0 | 5 |
| 01-PLANS - 40 2 | E407 | nom | 1.000 | 84 | 0 | 90 | 83 | 1 | 7 |
| 01-PLANS - 41 2 | E408 | nom | 1.000 | 66 | 0 | 69 | 66 | 0 | 3 |
| 01-PLANS - 41 2 1 | E408 | nom | 1.000 | 66 | 66 | 69 | 0 | 0 | 3 |
| 01-PLANS - 40 2 1 | E407 | nom | 1.000 | 84 | 84 | 90 | 0 | 0 | 7 |
| 01-PLANS - 39 2 1 | E406 | nom | 1.000 | 141 | 141 | 146 | 0 | 0 | 5 |
| 01-PLANS - 38 2 1 | E405 | nom | 1.000 | 140 | 140 | 146 | 0 | 0 | 6 |
| 01-PLANS - 37 2 1 | E404 | nom | 1.000 | 138 | 138 | 145 | 0 | 0 | 7 |
| 01-PLANS - 36 2 1 | E403 | nom | 1.000 | 139 | 139 | 145 | 0 | 0 | 6 |
| 01-PLANS - 35 2 1 | E402 | nom | 0.952 | 314 | 0 | 144 | 139 | 175 | 5 |
| 01-PLANS - 34 2 1 | E401 | nom | 0.934 | 227 | 0 | 161 | 154 | 73 | 7 |
| — | E101 | feuille IA sans page humaine |  | 0 | 0 | 15 | 0 | 0 | 15 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| 01-PLANS - 14 | E201 | LO P3000 | 0.687 | 0.702 | 3905 | 2993 |
| 01-PLANS - 14 | E201 | LO PRISE CONTROLÉ | 0.526 | 0.998 | 2992 | 4254 |
| 01-PLANS - 14 | E201 | LO TV | 0.623 | 0.286 | 3543 | 1216 |
| 01-PLANS - 14 | E201 | LO TV | 0.770 | 0.430 | 4382 | 1830 |
| 01-PLANS - 18 2 | E205 | LO CONENSEUR | 0.669 | 0.434 | 3808 | 1850 |
| 01-PLANS - 18 2 | E205 | LO TV | 0.519 | 0.281 | 2951 | 1194 |
| 01-PLANS - 19 2 | E206 | LO P3000 | 0.749 | 0.386 | 4259 | 1642 |
| 01-PLANS - 19 2 | E206 | LO TEL | 0.516 | 0.283 | 2933 | 1204 |
| 01-PLANS - 13 | E200 | AG-1A | 0.823 | 0.656 | 4688 | 2804 |
| 01-PLANS - 13 | E200 | AG-1B | 0.206 | 0.379 | 1171 | 1617 |
| 01-PLANS - 13 | E200 | P--1A | 0.569 | 0.384 | 3241 | 1638 |
| 01-PLANS - 13 | E200 | P-2B | 0.330 | 0.601 | 1878 | 2568 |
| 01-PLANS - 13 | E200 | P-3 | 0.220 | 0.659 | 1252 | 2813 |
| 01-PLANS - 13 | E200 | PANN POMPE | 0.316 | 0.595 | 1797 | 2542 |
| 01-PLANS - 13 | E200 | PORTE GARAGE | 0.770 | 0.770 | 4387 | 3287 |
| 01-PLANS - 13 | E200 | SERV PRISE | 0.263 | 0.550 | 1495 | 2348 |
| 01-PLANS - 13 | E200 | V-13 | 0.566 | 0.285 | 3225 | 1218 |
| 01-PLANS - 13 | E200 | V-14A | 0.276 | 0.758 | 1571 | 3236 |
| 01-PLANS - 13 | E200 | V-14B | 0.625 | 0.710 | 3561 | 3034 |
| 01-PLANS - 13 | E200 | V-14C | 0.789 | 0.272 | 4493 | 1164 |
| 01-PLANS - 13 | E200 | V-16 | 0.715 | 0.326 | 4070 | 1393 |
| 01-PLANS - 13 | E200 | V-1B | 0.227 | 0.551 | 1290 | 2354 |
| 01-PLANS - 13 | E200 | V-1C | 0.208 | 0.520 | 1183 | 2219 |
| 01-PLANS - 13 | E200 | V-1D | 0.227 | 0.519 | 1290 | 2217 |
| 01-PLANS - 13 | E200 | V-2C | 0.317 | 0.598 | 1806 | 2555 |
| 01-PLANS - 13 | E200 | V-5B | 0.641 | 0.422 | 3647 | 1804 |
| 01-PLANS - 13 | E200 | V-6 | 0.644 | 0.276 | 3667 | 1179 |
| 01-PLANS - 13 | E200 | V-7 | 0.506 | 0.291 | 2883 | 1245 |
| 01-PLANS - 13 | E200 | V-8 | 0.204 | 0.284 | 1164 | 1213 |
| 01-PLANS - 24 2 | E301 | APPLIQUE MURAL EXT | 0.277 | 0.568 | 1589 | 2425 |
| 01-PLANS - 24 2 | E301 | FIXT TYPE UE2 | 0.271 | 0.568 | 1560 | 2427 |
| 01-PLANS - 24 2 | E301 | FIXT TYPE UE2 | 0.241 | 0.570 | 1386 | 2433 |
| 01-PLANS - 24 2 | E301 | PLAFONNIER | 0.582 | 0.489 | 3327 | 2091 |
| 01-PLANS - 33 2 | E400 | RELAIS | 0.590 | 0.686 | 3362 | 2929 |
| 01-PLANS - 34 2 1 | E401 | AF1-5 | 0.769 | 0.326 | 4374 | 1392 |
| 01-PLANS - 34 2 1 | E401 | AF1-5 | 0.700 | 0.409 | 3985 | 1746 |
| 01-PLANS - 34 2 1 | E401 | AF1-5 | 0.734 | 0.413 | 4177 | 1761 |
| 01-PLANS - 34 2 1 | E401 | AF1-5 | 0.761 | 0.416 | 4333 | 1773 |
| 01-PLANS - 34 2 1 | E401 | GSM | 0.642 | 0.635 | 3657 | 2712 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.643 | 0.271 | 3664 | 1157 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.519 | 0.272 | 2955 | 1158 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.705 | 0.272 | 4012 | 1158 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.621 | 0.284 | 3534 | 1212 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.620 | 0.286 | 3530 | 1220 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.522 | 0.289 | 2972 | 1234 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.521 | 0.291 | 2970 | 1242 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.653 | 0.298 | 3719 | 1273 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.652 | 0.299 | 3714 | 1274 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.790 | 0.299 | 4497 | 1275 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.713 | 0.299 | 4058 | 1277 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.715 | 0.300 | 4070 | 1278 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.720 | 0.300 | 4100 | 1279 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.679 | 0.300 | 3868 | 1280 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.537 | 0.300 | 3056 | 1281 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.613 | 0.300 | 3491 | 1281 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.755 | 0.312 | 4296 | 1332 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.755 | 0.314 | 4296 | 1338 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.653 | 0.321 | 3719 | 1367 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.685 | 0.321 | 3899 | 1371 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.571 | 0.322 | 3249 | 1374 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.654 | 0.323 | 3724 | 1378 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.685 | 0.324 | 3899 | 1381 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.570 | 0.325 | 3247 | 1385 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.773 | 0.327 | 4399 | 1396 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.548 | 0.346 | 3119 | 1476 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.550 | 0.346 | 3132 | 1477 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.520 | 0.352 | 2962 | 1501 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.521 | 0.352 | 2970 | 1501 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.754 | 0.363 | 4292 | 1547 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.772 | 0.365 | 4394 | 1556 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.750 | 0.368 | 4267 | 1568 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.792 | 0.368 | 4509 | 1569 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.749 | 0.369 | 4265 | 1575 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.792 | 0.369 | 4508 | 1576 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.582 | 0.372 | 3316 | 1585 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.582 | 0.373 | 3315 | 1592 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.583 | 0.375 | 3318 | 1601 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.698 | 0.376 | 3975 | 1604 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.770 | 0.379 | 4381 | 1616 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.771 | 0.379 | 4388 | 1616 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.697 | 0.379 | 3970 | 1618 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.699 | 0.379 | 3980 | 1618 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.665 | 0.387 | 3786 | 1651 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.665 | 0.390 | 3787 | 1663 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.560 | 0.390 | 3188 | 1665 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.561 | 0.390 | 3198 | 1665 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.738 | 0.395 | 4200 | 1687 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.736 | 0.396 | 4190 | 1688 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.589 | 0.400 | 3357 | 1707 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.590 | 0.402 | 3358 | 1715 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.599 | 0.407 | 3408 | 1736 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.699 | 0.409 | 3977 | 1747 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.658 | 0.412 | 3745 | 1759 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.803 | 0.413 | 4567 | 1763 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.582 | 0.414 | 3317 | 1767 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.761 | 0.414 | 4333 | 1767 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.762 | 0.414 | 4339 | 1768 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.707 | 0.415 | 4022 | 1770 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.582 | 0.416 | 3315 | 1774 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.542 | 0.418 | 3089 | 1782 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.729 | 0.419 | 4151 | 1789 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.729 | 0.421 | 4151 | 1796 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.665 | 0.423 | 3787 | 1805 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.665 | 0.425 | 3787 | 1814 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.670 | 0.437 | 3814 | 1863 |
| 01-PLANS - 34 2 1 | E401 | INT | 0.726 | 0.437 | 4133 | 1865 |
| 01-PLANS - 34 2 1 | E401 | KS | 0.646 | 0.289 | 3679 | 1233 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.664 | 0.270 | 3775 | 1149 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.580 | 0.271 | 3302 | 1153 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.622 | 0.271 | 3540 | 1153 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.542 | 0.282 | 3092 | 1200 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.668 | 0.282 | 3802 | 1200 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.712 | 0.282 | 4047 | 1200 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.543 | 0.284 | 3094 | 1209 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.711 | 0.284 | 4042 | 1209 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.668 | 0.285 | 3800 | 1210 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.622 | 0.285 | 3543 | 1213 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.748 | 0.287 | 4251 | 1218 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.622 | 0.287 | 3543 | 1221 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.748 | 0.289 | 4253 | 1228 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.592 | 0.294 | 3373 | 1251 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.595 | 0.294 | 3388 | 1251 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.500 | 0.296 | 2856 | 1259 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.557 | 0.297 | 3173 | 1265 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.791 | 0.299 | 4492 | 1270 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.742 | 0.302 | 4218 | 1285 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.712 | 0.304 | 4048 | 1293 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.714 | 0.304 | 4059 | 1293 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.617 | 0.305 | 3514 | 1296 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.619 | 0.305 | 3525 | 1296 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.588 | 0.312 | 3352 | 1329 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.759 | 0.321 | 4310 | 1365 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.758 | 0.323 | 4308 | 1375 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.679 | 0.324 | 3860 | 1380 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.677 | 0.325 | 3849 | 1383 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.553 | 0.326 | 3150 | 1388 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.551 | 0.327 | 3139 | 1391 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.774 | 0.333 | 4396 | 1419 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.575 | 0.337 | 3276 | 1434 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.524 | 0.338 | 2991 | 1440 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.774 | 0.339 | 4396 | 1444 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.575 | 0.340 | 3276 | 1446 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.525 | 0.341 | 2994 | 1453 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.524 | 0.345 | 2991 | 1470 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.547 | 0.351 | 3117 | 1495 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.543 | 0.351 | 3098 | 1497 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.772 | 0.365 | 4387 | 1554 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.793 | 0.366 | 4503 | 1558 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.574 | 0.368 | 3268 | 1567 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.792 | 0.368 | 4499 | 1569 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.595 | 0.372 | 3386 | 1584 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.676 | 0.372 | 3843 | 1586 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.748 | 0.372 | 4249 | 1586 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.708 | 0.373 | 4027 | 1591 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.594 | 0.374 | 3383 | 1593 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.675 | 0.374 | 3842 | 1593 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.708 | 0.376 | 4025 | 1601 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.748 | 0.376 | 4248 | 1601 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.561 | 0.382 | 3197 | 1626 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.561 | 0.384 | 3199 | 1638 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.572 | 0.393 | 3260 | 1676 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.730 | 0.396 | 4147 | 1686 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.573 | 0.396 | 3263 | 1687 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.730 | 0.398 | 4149 | 1694 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.603 | 0.404 | 3434 | 1721 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.603 | 0.406 | 3435 | 1732 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.739 | 0.407 | 4197 | 1734 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.687 | 0.413 | 3905 | 1760 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.761 | 0.413 | 4322 | 1760 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.766 | 0.413 | 4353 | 1761 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.686 | 0.415 | 3903 | 1769 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.766 | 0.415 | 4351 | 1771 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.802 | 0.415 | 4555 | 1771 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.541 | 0.419 | 3086 | 1786 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.725 | 0.419 | 4124 | 1788 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.601 | 0.420 | 3422 | 1790 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.671 | 0.421 | 3819 | 1795 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.644 | 0.422 | 3664 | 1797 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.606 | 0.423 | 3448 | 1805 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.606 | 0.427 | 3450 | 1819 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.689 | 0.427 | 3920 | 1819 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.731 | 0.428 | 4156 | 1825 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.607 | 0.614 | 3456 | 2622 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.561 | 0.614 | 3199 | 2624 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.537 | 0.620 | 3064 | 2646 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.644 | 0.628 | 3664 | 2683 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.486 | 0.629 | 2777 | 2686 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.489 | 0.629 | 2792 | 2686 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.491 | 0.629 | 2805 | 2687 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.666 | 0.629 | 3791 | 2687 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.447 | 0.631 | 2555 | 2694 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.707 | 0.631 | 4019 | 2696 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.667 | 0.632 | 3792 | 2699 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.605 | 0.633 | 3444 | 2705 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.563 | 0.634 | 3211 | 2709 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.522 | 0.635 | 2976 | 2712 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.605 | 0.636 | 3447 | 2714 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.563 | 0.637 | 3210 | 2720 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.521 | 0.637 | 2974 | 2721 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.638 | 0.641 | 3633 | 2739 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.656 | 0.643 | 3730 | 2747 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.654 | 0.644 | 3721 | 2748 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.684 | 0.654 | 3888 | 2792 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.685 | 0.654 | 3896 | 2792 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.492 | 0.658 | 2807 | 2810 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.455 | 0.659 | 2598 | 2815 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.453 | 0.659 | 2589 | 2816 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.523 | 0.663 | 2982 | 2834 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.572 | 0.666 | 3257 | 2847 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.664 | 0.666 | 3780 | 2847 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.530 | 0.667 | 3023 | 2849 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.485 | 0.669 | 2770 | 2856 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.615 | 0.669 | 3502 | 2856 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.486 | 0.669 | 2777 | 2858 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.530 | 0.669 | 3025 | 2858 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.665 | 0.669 | 3782 | 2859 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.615 | 0.672 | 3502 | 2869 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.699 | 0.700 | 3974 | 2991 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.700 | 0.702 | 3978 | 3000 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.597 | 0.704 | 3399 | 3007 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.489 | 0.704 | 2792 | 3008 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.506 | 0.710 | 2888 | 3033 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.507 | 0.710 | 2894 | 3034 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.475 | 0.718 | 2715 | 3070 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.474 | 0.719 | 2708 | 3072 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.594 | 0.721 | 3382 | 3080 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.749 | 0.721 | 4257 | 3080 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.594 | 0.723 | 3384 | 3087 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.678 | 0.726 | 3859 | 3101 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.678 | 0.728 | 3854 | 3108 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.698 | 0.728 | 3972 | 3110 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.699 | 0.730 | 3975 | 3117 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.504 | 0.730 | 2875 | 3120 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.504 | 0.732 | 2877 | 3126 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.459 | 0.734 | 2624 | 3136 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.552 | 0.735 | 3148 | 3142 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.551 | 0.736 | 3141 | 3143 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.536 | 0.739 | 3055 | 3159 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.649 | 0.740 | 3690 | 3162 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.513 | 0.742 | 2925 | 3171 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.529 | 0.743 | 3015 | 3175 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.743 | 0.743 | 4223 | 3176 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.640 | 0.744 | 3643 | 3179 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.595 | 0.745 | 3388 | 3182 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.744 | 0.746 | 4225 | 3188 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.729 | 0.748 | 4145 | 3197 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.545 | 0.749 | 3105 | 3200 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.547 | 0.749 | 3118 | 3200 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.730 | 0.750 | 4147 | 3205 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.689 | 0.753 | 3916 | 3217 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.603 | 0.753 | 3432 | 3219 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.498 | 0.754 | 2843 | 3222 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.688 | 0.755 | 3915 | 3226 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.602 | 0.757 | 3431 | 3234 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.498 | 0.757 | 2845 | 3236 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.647 | 0.759 | 3682 | 3244 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.647 | 0.761 | 3684 | 3251 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.537 | 0.769 | 3061 | 3285 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.663 | 0.769 | 3770 | 3286 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.621 | 0.769 | 3536 | 3287 |
| 01-PLANS - 35 2 1 | E402 | INT | 0.565 | 0.770 | 3221 | 3288 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.471 | 0.609 | 2693 | 2602 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.464 | 0.612 | 2654 | 2613 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.490 | 0.614 | 2795 | 2624 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.471 | 0.618 | 2693 | 2638 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.452 | 0.624 | 2586 | 2663 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.463 | 0.624 | 2648 | 2665 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.471 | 0.625 | 2690 | 2667 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.532 | 0.631 | 3032 | 2696 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.494 | 0.634 | 2817 | 2708 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.509 | 0.640 | 2904 | 2735 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.484 | 0.643 | 2762 | 2745 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.457 | 0.645 | 2610 | 2756 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.469 | 0.647 | 2679 | 2762 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.492 | 0.650 | 2810 | 2776 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.510 | 0.659 | 2911 | 2814 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.483 | 0.660 | 2759 | 2817 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.502 | 0.660 | 2865 | 2817 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.493 | 0.671 | 2815 | 2868 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.480 | 0.674 | 2741 | 2879 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.456 | 0.677 | 2607 | 2892 |
| 01-PLANS - 35 2 1 | E402 | PLAFOND | 0.478 | 0.679 | 2732 | 2901 |
| 01-PLANS - 40 2 | E407 | KS | 0.778 | 0.373 | 4433 | 1593 |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E201 | 01-PLANS - 14 | Sectionneur | 0.810 | 0.432 | 4611 | 1846 |
| E202 | 01-PLANS - 15 | Panneau de logement | 0.631 | 0.340 | 3592 | 1452 |
| E202 | 01-PLANS - 15 | Raccordement condenseur | 0.634 | 0.486 | 3612 | 2076 |
| E202 | 01-PLANS - 15 | Raccordement condenseur | 0.634 | 0.540 | 3612 | 2307 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.670 | 0.260 | 3813 | 1110 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.628 | 0.260 | 3575 | 1111 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.496 | 0.269 | 2824 | 1150 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.799 | 0.293 | 4549 | 1253 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.636 | 0.486 | 3622 | 2076 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.636 | 0.540 | 3622 | 2307 |
| E202 | 01-PLANS - 15 | Sectionneur | 0.455 | 0.725 | 2589 | 3095 |
| E203 | 01-PLANS - 16 | Sectionneur | 0.494 | 0.272 | 2812 | 1160 |
| E204 | 01-PLANS - 17 2 | Prise double | 0.786 | 0.273 | 4475 | 1164 |
| E204 | 01-PLANS - 17 2 | Sectionneur | 0.496 | 0.272 | 2822 | 1160 |
| E204 | 01-PLANS - 17 2 | Sectionneur | 0.603 | 0.777 | 3436 | 3319 |
| E205 | 01-PLANS - 18 2 | Sectionneur | 0.495 | 0.271 | 2817 | 1158 |
| E205 | 01-PLANS - 18 2 | Sectionneur | 0.441 | 0.604 | 2511 | 2580 |
| E205 | 01-PLANS - 18 2 | Sectionneur | 0.454 | 0.727 | 2583 | 3103 |
| E205 | 01-PLANS - 18 2 | Sectionneur | 0.603 | 0.776 | 3431 | 3316 |
| E206 | 01-PLANS - 19 2 | Sectionneur | 0.492 | 0.270 | 2804 | 1152 |
| E206 | 01-PLANS - 19 2 | Sectionneur | 0.807 | 0.397 | 4597 | 1695 |
| E206 | 01-PLANS - 19 2 | Sectionneur | 0.753 | 0.737 | 4288 | 3146 |
| E207 | 01-PLANS - 20 2 | Panneau de distribution | 0.649 | 0.652 | 3694 | 2785 |
| E207 | 01-PLANS - 20 2 | Panneau de distribution | 0.657 | 0.652 | 3743 | 2785 |
| E207 | 01-PLANS - 20 2 | Prise double | 0.684 | 0.406 | 3892 | 1734 |
| E207 | 01-PLANS - 20 2 | Sectionneur | 0.627 | 0.260 | 3571 | 1110 |
| E207 | 01-PLANS - 20 2 | Sectionneur | 0.495 | 0.269 | 2821 | 1149 |
| E200 | 01-PLANS - 13 | Aérotherme | 0.189 | 0.343 | 1075 | 1465 |
| E200 | 01-PLANS - 13 | Aérotherme | 0.845 | 0.642 | 4813 | 2743 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.584 | 0.297 | 3325 | 1267 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.591 | 0.299 | 3366 | 1279 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.595 | 0.299 | 3388 | 1279 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.598 | 0.299 | 3407 | 1279 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.587 | 0.300 | 3343 | 1280 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.668 | 0.715 | 3801 | 3053 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.486 | 0.728 | 2766 | 3108 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.494 | 0.728 | 2814 | 3108 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.461 | 0.731 | 2624 | 3120 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.495 | 0.734 | 2820 | 3135 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.495 | 0.744 | 2820 | 3178 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.460 | 0.744 | 2620 | 3179 |
| E200 | 01-PLANS - 13 | Panneau de distribution | 0.475 | 0.768 | 2702 | 3278 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.803 | 0.245 | 4570 | 1047 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.633 | 0.254 | 3604 | 1083 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.190 | 0.258 | 1080 | 1100 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.552 | 0.270 | 3144 | 1153 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.484 | 0.296 | 2754 | 1264 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.650 | 0.304 | 3699 | 1298 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.733 | 0.314 | 4172 | 1342 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.657 | 0.398 | 3741 | 1699 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.657 | 0.413 | 3741 | 1762 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.243 | 0.496 | 1383 | 2119 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.195 | 0.502 | 1109 | 2146 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.242 | 0.566 | 1376 | 2418 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.661 | 0.597 | 3763 | 2550 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.178 | 0.688 | 1014 | 2938 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.729 | 0.722 | 4152 | 3085 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.627 | 0.738 | 3571 | 3154 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.292 | 0.778 | 1665 | 3322 |
| E200 | 01-PLANS - 13 | Raccordement ventilateur | 0.440 | 0.778 | 2503 | 3324 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.584 | 0.364 | 3328 | 1553 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.327 | 0.570 | 1862 | 2436 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.344 | 0.574 | 1957 | 2450 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.362 | 0.594 | 2059 | 2535 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.252 | 0.645 | 1436 | 2753 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.636 | 0.648 | 3622 | 2766 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.578 | 0.688 | 3292 | 2937 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.240 | 0.698 | 1365 | 2983 |
| E200 | 01-PLANS - 13 | Raccordement équipement mécanique | 0.214 | 0.702 | 1221 | 2998 |
| E200 | 01-PLANS - 13 | Sectionneur | 0.630 | 0.443 | 3590 | 1894 |
| E200 | 01-PLANS - 13 | Sectionneur | 0.635 | 0.597 | 3618 | 2549 |
| E200 | 01-PLANS - 13 | Sectionneur | 0.472 | 0.729 | 2686 | 3113 |
| E200 | 01-PLANS - 13 | Sectionneur | 0.475 | 0.729 | 2705 | 3113 |
| E200 | 01-PLANS - 13 | Transformateur | 0.605 | 0.296 | 3443 | 1266 |
| E200 | 01-PLANS - 13 | Transformateur | 0.612 | 0.296 | 3484 | 1266 |
| E200 | 01-PLANS - 13 | Transformateur | 0.675 | 0.702 | 3845 | 3000 |
| E200 | 01-PLANS - 13 | Transformateur | 0.682 | 0.702 | 3886 | 3000 |
| E200 | 01-PLANS - 13 | Transformateur | 0.690 | 0.702 | 3927 | 3000 |
| E200 | 01-PLANS - 13 | Transformateur | 0.490 | 0.728 | 2789 | 3108 |
| E200 | 01-PLANS - 13 | Transformateur | 0.461 | 0.738 | 2625 | 3152 |
| E200 | 01-PLANS - 13 | Transformateur | 0.495 | 0.739 | 2821 | 3155 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.619 | 0.273 | 3526 | 1167 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.587 | 0.273 | 3342 | 1168 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.602 | 0.273 | 3429 | 1168 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.478 | 0.729 | 2724 | 3114 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.482 | 0.729 | 2747 | 3115 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.681 | 0.735 | 3878 | 3138 |
| E200 | 01-PLANS - 13 | Équipement salle électrique — à classer | 0.465 | 0.767 | 2650 | 3276 |
| E208 | 01-PLANS - 21 2 | Panneau de distribution | 0.586 | 0.329 | 3335 | 1404 |
| E208 | 01-PLANS - 21 2 | Sectionneur | 0.668 | 0.260 | 3803 | 1111 |
| E208 | 01-PLANS - 21 2 | Sectionneur | 0.536 | 0.298 | 3053 | 1271 |
| E208 | 01-PLANS - 21 2 | Sectionneur | 0.753 | 0.427 | 4286 | 1822 |
| E302 | 01-PLANS - 25 2 | Luminaire encastré urgence | 0.595 | 0.354 | 3388 | 1510 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.229 | 0.310 | 1306 | 1325 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.622 | 0.330 | 3539 | 1409 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.701 | 0.338 | 3994 | 1444 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.621 | 0.341 | 3538 | 1455 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.597 | 0.350 | 3402 | 1493 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.302 | 0.537 | 1717 | 2293 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.273 | 0.543 | 1554 | 2321 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.649 | 0.691 | 3696 | 2952 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.215 | 0.697 | 1227 | 2975 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.377 | 0.706 | 2149 | 3017 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.630 | 0.709 | 3588 | 3028 |
| E400 | 01-PLANS - 33 2 | Résistance fin de ligne | 0.630 | 0.720 | 3590 | 3075 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Détecteur de fumée | 0.273 | 0.580 | 1556 | 2476 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.620 | 0.330 | 3530 | 1409 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.620 | 0.340 | 3530 | 1454 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.630 | 0.513 | 3587 | 2189 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.611 | 0.618 | 3477 | 2638 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.630 | 0.707 | 3589 | 3018 |
| E401 | 01-PLANS - 34 2 + 01-PLANS - 34 2 1 | Résistance fin de ligne | 0.630 | 0.718 | 3589 | 3068 |
| E402 | 01-PLANS - 35 2 + 01-PLANS - 35 2 1 | Résistance fin de ligne | 0.620 | 0.330 | 3530 | 1410 |
| E402 | 01-PLANS - 35 2 + 01-PLANS - 35 2 1 | Résistance fin de ligne | 0.620 | 0.340 | 3530 | 1454 |
| E402 | 01-PLANS - 35 2 + 01-PLANS - 35 2 1 | Résistance fin de ligne | 0.659 | 0.348 | 3752 | 1485 |
| E402 | 01-PLANS - 35 2 + 01-PLANS - 35 2 1 | Résistance fin de ligne | 0.631 | 0.704 | 3591 | 3007 |
| E402 | 01-PLANS - 35 2 + 01-PLANS - 35 2 1 | Résistance fin de ligne | 0.631 | 0.715 | 3592 | 3054 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.620 | 0.330 | 3528 | 1411 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.620 | 0.341 | 3528 | 1457 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.659 | 0.348 | 3751 | 1486 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.579 | 0.680 | 3295 | 2904 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.630 | 0.705 | 3586 | 3013 |
| E403 | 01-PLANS - 36 2 + 01-PLANS - 36 2 1 | Résistance fin de ligne | 0.630 | 0.716 | 3586 | 3059 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Klaxon/stroboscope | 0.731 | 0.695 | 4160 | 2969 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.620 | 0.330 | 3531 | 1408 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.620 | 0.340 | 3530 | 1452 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.659 | 0.347 | 3750 | 1483 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.578 | 0.680 | 3293 | 2904 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.630 | 0.704 | 3585 | 3007 |
| E404 | 01-PLANS - 37 2 + 01-PLANS - 37 2 1 | Résistance fin de ligne | 0.630 | 0.714 | 3586 | 3051 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.618 | 0.329 | 3521 | 1405 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.618 | 0.340 | 3521 | 1451 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.657 | 0.347 | 3739 | 1480 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.574 | 0.680 | 3269 | 2903 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.628 | 0.705 | 3577 | 3012 |
| E405 | 01-PLANS - 38 2 + 01-PLANS - 38 2 1 | Résistance fin de ligne | 0.628 | 0.716 | 3577 | 3058 |
| E406 | 01-PLANS - 39 2 + 01-PLANS - 39 2 1 | Résistance fin de ligne | 0.623 | 0.329 | 3547 | 1405 |
| E406 | 01-PLANS - 39 2 + 01-PLANS - 39 2 1 | Résistance fin de ligne | 0.623 | 0.340 | 3546 | 1451 |
| E406 | 01-PLANS - 39 2 + 01-PLANS - 39 2 1 | Résistance fin de ligne | 0.661 | 0.348 | 3763 | 1486 |
| E406 | 01-PLANS - 39 2 + 01-PLANS - 39 2 1 | Résistance fin de ligne | 0.633 | 0.706 | 3603 | 3014 |
| E406 | 01-PLANS - 39 2 + 01-PLANS - 39 2 1 | Résistance fin de ligne | 0.633 | 0.716 | 3603 | 3059 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Avertisseur de fumée | 0.613 | 0.399 | 3492 | 1706 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.620 | 0.329 | 3531 | 1404 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.620 | 0.338 | 3531 | 1444 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.664 | 0.346 | 3778 | 1476 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.671 | 0.683 | 3819 | 2919 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.631 | 0.705 | 3593 | 3012 |
| E407 | 01-PLANS - 40 2 + 01-PLANS - 40 2 1 | Résistance fin de ligne | 0.631 | 0.715 | 3593 | 3052 |
| E408 | 01-PLANS - 41 2 + 01-PLANS - 41 2 1 | Klaxon | 0.649 | 0.400 | 3696 | 1710 |
| E408 | 01-PLANS - 41 2 + 01-PLANS - 41 2 1 | Résistance fin de ligne | 0.616 | 0.328 | 3510 | 1399 |
| E408 | 01-PLANS - 41 2 + 01-PLANS - 41 2 1 | Résistance fin de ligne | 0.616 | 0.337 | 3510 | 1439 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.911 | 0.313 | 5187 | 1338 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.584 | 0.314 | 3327 | 1340 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.464 | 0.318 | 2643 | 1359 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.911 | 0.318 | 5187 | 1359 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.584 | 0.319 | 3327 | 1361 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.801 | 0.319 | 4562 | 1361 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.914 | 0.324 | 5206 | 1382 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.690 | 0.329 | 3931 | 1406 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.436 | 0.334 | 2481 | 1427 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.690 | 0.334 | 3931 | 1427 |
| E101 | — (aucune page humaine) | Raccordement équipement mécanique | 0.109 | 0.370 | 620 | 1582 |
| E101 | — (aucune page humaine) | Transformateur | 0.916 | 0.329 | 5218 | 1406 |
| E101 | — (aucune page humaine) | Transformateur | 0.916 | 0.391 | 5218 | 1668 |
| E101 | — (aucune page humaine) | Équipement salle électrique — à classer | 0.320 | 0.334 | 1821 | 1427 |
| E101 | — (aucune page humaine) | Équipement salle électrique — à classer | 0.549 | 0.410 | 3124 | 1750 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| E200 | SERV PRISE | Prise double | Raccordement ventilateur | 4064 | 3267 |
| E201 | B 1250W | Plinthe 1250W | Sectionneur | 3308 | 3319 |
| E201 | B 300W | Plinthe 300W | Prise comptoir | 2951 | 1342 |
| E201 | B 300W | Plinthe 300W | Panneau de logement | 3829 | 1653 |
| E201 | L EVAP | Raccordement évaporateur | Panneau de logement | 4345 | 1243 |
| E201 | L EVAP | Raccordement évaporateur | Panneau de logement | 3669 | 1278 |
| E201 | LO P3000 | Prise double | Panneau de logement | 3937 | 1278 |
| E201 | LO P3000 | Prise double | Panneau de logement | 3206 | 1345 |
| E201 | LO P3000 | Prise double | Prise salle de bain | 3087 | 1431 |
| E201 | LO P3000 | Prise double | Plinthe 300W | 3771 | 1693 |
| E201 | LO P3000 | Prise double | Prise laveuse | 3995 | 1708 |
| E201 | LO P3000 | Prise double | Panneau de logement | 4395 | 1728 |
| E201 | LO P3000 | Prise double | Thermostat | 2760 | 2716 |
| E201 | LO P3000 | Prise double | Prise laveuse | 2928 | 2717 |
| E201 | LO P3000 | Prise double | Prise comptoir | 3879 | 2800 |
| E201 | LO P3000 | Prise double | Prise salle de bain | 3290 | 3081 |
| E201 | LO P3000 | Prise double | Panneau de logement | 3990 | 3106 |
| E201 | LO P3000 | Prise double | Panneau de logement | 3519 | 3125 |
| E201 | LO P3000 | Prise double | Prise demi-commandée | 3340 | 3136 |
| E201 | LO P3000 | Prise double | Prise laveuse | 3696 | 3164 |
| E201 | LO PRISE | Prise double | Sectionneur | 2976 | 1118 |
| E201 | LO PRISE | Prise double | Sectionneur | 3214 | 1118 |
| E201 | LO PRISE | Prise double | Sectionneur | 3685 | 1118 |
| E201 | LO PRISE | Prise double | Aéroconvecteur 1250W | 4480 | 1248 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4432 | 1298 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3089 | 1301 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3536 | 1301 |
| E201 | LO PRISE | Prise double | Prise laveuse | 4050 | 1301 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2922 | 1343 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3162 | 1344 |
| E201 | LO PRISE | Prise double | Raccordement évaporateur | 3702 | 1347 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 4411 | 1354 |
| E201 | LO PRISE | Prise double | Prise comptoir | 4464 | 1354 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 4384 | 1355 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3103 | 1358 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3103 | 1384 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 2872 | 1399 |
| E201 | LO PRISE | Prise double | Prise comptoir | 2920 | 1399 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 2943 | 1401 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3964 | 1402 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3050 | 1410 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3579 | 1425 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3282 | 1429 |
| E201 | LO PRISE | Prise double | Prise laveuse | 4254 | 1450 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 4004 | 1454 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3597 | 1458 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3644 | 1458 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3935 | 1459 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3980 | 1459 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3831 | 1562 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3879 | 1562 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3807 | 1563 |
| E201 | LO PRISE | Prise double | Prise comptoir | 4051 | 1563 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 4099 | 1563 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 4121 | 1563 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3701 | 1600 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4082 | 1615 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3851 | 1621 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3345 | 1630 |
| E201 | LO PRISE | Prise double | Thermostat | 3212 | 1636 |
| E201 | LO PRISE | Prise double | Prise comptoir | 4402 | 1638 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 4450 | 1638 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 4473 | 1638 |
| E201 | LO PRISE | Prise double | Sectionneur | 3055 | 1664 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3120 | 1688 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3183 | 1688 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3213 | 1688 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4445 | 1692 |
| E201 | LO PRISE | Prise double | Prise laveuse | 4287 | 1693 |
| E201 | LO PRISE | Prise double | Panneau de logement | 3235 | 1719 |
| E201 | LO PRISE | Prise double | Panneau de logement | 4092 | 1728 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3163 | 1749 |
| E201 | LO PRISE | Prise double | Sectionneur | 4030 | 1895 |
| E201 | LO PRISE | Prise double | Prise comptoir | 2700 | 2598 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2641 | 2623 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 2698 | 2647 |
| E201 | LO PRISE | Prise double | Panneau de logement | 2665 | 2676 |
| E201 | LO PRISE | Prise double | Sortie informatique | 3210 | 2705 |
| E201 | LO PRISE | Prise double | Panneau de logement | 3904 | 2709 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3237 | 2718 |
| E201 | LO PRISE | Prise double | Panneau de logement | 3023 | 2723 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3806 | 2747 |
| E201 | LO PRISE | Prise double | Sectionneur | 4069 | 2757 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3697 | 2791 |
| E201 | LO PRISE | Prise double | Prise laveuse | 2813 | 2796 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3827 | 2800 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3909 | 2801 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3012 | 2820 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3143 | 2825 |
| E201 | LO PRISE | Prise double | Prise salle de bain | 2698 | 2871 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 2994 | 2875 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3133 | 2878 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3158 | 2878 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3089 | 2879 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3017 | 2880 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3062 | 2880 |
| E201 | LO PRISE | Prise double | Aéroconvecteur 1500W | 2561 | 2921 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3456 | 2980 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3457 | 3001 |
| E201 | LO PRISE | Prise double | Prise salle de bain | 2774 | 3006 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3337 | 3015 |
| E201 | LO PRISE | Prise double | Prise laveuse | 3290 | 3016 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3456 | 3048 |
| E201 | LO PRISE | Prise double | Prise laveuse | 4050 | 3060 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3454 | 3095 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3610 | 3106 |
| E201 | LO PRISE | Prise double | Sortie informatique | 2839 | 3109 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3548 | 3109 |
| E201 | LO PRISE | Prise double | Panneau de logement | 3179 | 3110 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3657 | 3111 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3053 | 3125 |
| E201 | LO PRISE | Prise double | Prise comptoir | 2648 | 3126 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 2710 | 3126 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 2740 | 3126 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4043 | 3129 |
| E201 | LO PRISE | Prise double | Prise laveuse | 2876 | 3135 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3053 | 3143 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3984 | 3153 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2694 | 3187 |
| E201 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3047 | 3189 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3984 | 3206 |
| E201 | LO PRISE | Prise double | Prise réfrigérateur | 3983 | 3234 |
| E201 | LO PRISE | Prise double | Prise comptoir | 3053 | 3253 |
| E201 | LO PRISE | Prise double | Aéroconvecteur 1500W | 3585 | 3264 |
| E201 | LO PRISE | Prise double | Prise demi-commandée | 4229 | 3274 |
| E201 | LO PRISE | Prise double | Prise micro-onde | 3053 | 3278 |
| E201 | LO PRISE | Prise double | Plinthe 1250W | 3251 | 3278 |
| E201 | LO PRISE | Prise double | Sectionneur | 2855 | 3319 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 4043 | 1118 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3077 | 2539 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3097 | 2539 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise double | 2578 | 2933 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 4304 | 3268 |
| E201 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3334 | 3319 |
| E201 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 2944 | 1278 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4344 | 1297 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3160 | 1312 |
| E201 | LO PRISE GFI | Prise salle de bain | Plinthe 300W | 3002 | 1348 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3683 | 1398 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3930 | 1398 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4051 | 1617 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4121 | 1617 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3822 | 1619 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4358 | 1692 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3194 | 1747 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2642 | 2704 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3774 | 2746 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2979 | 2820 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3172 | 2822 |
| E201 | LO PRISE GFI | Prise salle de bain | Thermostat | 2739 | 2906 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise demi-commandée | 2700 | 3004 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise micro-onde | 3472 | 3085 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise micro-onde | 3668 | 3093 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4049 | 3101 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3566 | 3107 |
| E201 | LO PRISE GFI | Prise salle de bain | Thermostat | 3249 | 3109 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3562 | 3161 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2727 | 3182 |
| E201 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3053 | 3237 |
| E201 | LO PRISE SÉCHEUSE | Prise sécheuse | Raccordement lave-vaisselle | 3652 | 1400 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3887 | 1287 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4167 | 1696 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4543 | 1849 |
| E201 | LO TEL | Sortie câblo/informatique | Panneau de logement | 3140 | 2676 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2938 | 2752 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3966 | 2803 |
| E201 | LO TEL | Sortie câblo/informatique | Panneau de logement | 2775 | 3142 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3325 | 3231 |
| E201 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3524 | 3271 |
| E201 | LO TV | Prise double | Aéroconvecteur 1500W | 3943 | 1170 |
| E201 | LO TV | Prise double | Raccordement évaporateur | 4271 | 1259 |
| E201 | LO TV | Prise double | Aéroconvecteur 1500W | 3826 | 1842 |
| E201 | LO TV | Prise double | Aéroconvecteur 1500W | 2992 | 2594 |
| E201 | LO TV | Prise double | Aéroconvecteur 1500W | 3161 | 2594 |
| E201 | LO TV | Prise double | Panneau de logement | 3436 | 3201 |
| E201 | RWF 1250W | Aéroconvecteur 1250W | Sectionneur | 4543 | 1259 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 3994 | 1158 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3794 | 1895 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 3107 | 2579 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 3045 | 2580 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 2512 | 2926 |
| E201 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3571 | 3319 |
| E201 | TH | Thermostat | Prise double | 3177 | 1644 |
| E201 | TH | Thermostat | Prise réfrigérateur | 2701 | 2672 |
| E201 | TH | Thermostat | Prise double | 2769 | 2922 |
| E201 | TH | Thermostat | Prise double | 3217 | 3163 |
| E202 | B 1000W | Plinthe 1000W | Prise double | 3108 | 1618 |
| E202 | B 1000W | Plinthe 1000W | Sectionneur | 3349 | 1849 |
| E202 | B 1000W | Plinthe 1000W | Sectionneur | 3586 | 1849 |
| E202 | B 300W | Plinthe 300W | Panneau de logement | 4259 | 1287 |
| E202 | LO CONENSEUR | Raccordement condenseur | Prise demi-commandée | 3825 | 1774 |
| E202 | LO CONENSEUR | Raccordement condenseur | Sectionneur | 4308 | 3144 |
| E202 | LO P3000 | Prise double | Panneau de logement | 3338 | 1254 |
| E202 | LO P3000 | Prise double | Prise laveuse | 3822 | 1278 |
| E202 | LO P3000 | Prise double | Thermostat | 4317 | 1372 |
| E202 | LO P3000 | Prise double | Prise réfrigérateur | 3935 | 1403 |
| E202 | LO P3000 | Prise double | Panneau de logement | 4185 | 1569 |
| E202 | LO P3000 | Prise double | Plinthe 1000W | 3093 | 1572 |
| E202 | LO P3000 | Prise double | Prise réfrigérateur | 3702 | 1583 |
| E202 | LO P3000 | Prise double | Panneau de logement | 4343 | 1588 |
| E202 | LO P3000 | Prise double | Panneau de logement | 3430 | 1674 |
| E202 | LO P3000 | Prise double | Thermostat | 2779 | 2673 |
| E202 | LO P3000 | Prise double | Panneau de logement | 3447 | 2745 |
| E202 | LO P3000 | Prise double | Panneau de logement | 2974 | 2748 |
| E202 | LO P3000 | Prise double | Panneau de logement | 3208 | 2748 |
| E202 | LO P3000 | Prise double | Panneau de logement | 2733 | 3061 |
| E202 | LO P3000 | Prise double | Prise réfrigérateur | 3789 | 3107 |
| E202 | LO P3000 | Prise double | Prise comptoir | 4023 | 3112 |
| E202 | LO P3000 | Prise double | Panneau de logement | 3421 | 3160 |
| E202 | LO P3000 | Prise double | Thermostat | 3053 | 3189 |
| E202 | LO PRISE | Prise double | Sectionneur | 3337 | 1111 |
| E202 | LO PRISE | Prise double | Sectionneur | 4049 | 1111 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3813 | 1264 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4452 | 1287 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3068 | 1288 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3659 | 1290 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3939 | 1290 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3227 | 1295 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3412 | 1298 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3282 | 1317 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2943 | 1321 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3227 | 1343 |
| E202 | LO PRISE | Prise double | Prise comptoir | 4417 | 1349 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 4390 | 1350 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3584 | 1358 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 4481 | 1359 |
| E202 | LO PRISE | Prise double | Prise laveuse | 4011 | 1361 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3227 | 1364 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 2870 | 1374 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 2898 | 1375 |
| E202 | LO PRISE | Prise double | Prise comptoir | 2954 | 1375 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3935 | 1379 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3650 | 1380 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3740 | 1392 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3652 | 1403 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3705 | 1452 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3776 | 1452 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3751 | 1453 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3913 | 1453 |
| E202 | LO PRISE | Prise double | Prise laveuse | 4251 | 1458 |
| E202 | LO PRISE | Prise double | Raccordement ventilateur | 3094 | 1475 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3471 | 1556 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3517 | 1556 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3538 | 1556 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3839 | 1583 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3301 | 1590 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3702 | 1601 |
| E202 | LO PRISE | Prise double | Prise laveuse | 4137 | 1606 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3497 | 1612 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 4456 | 1632 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 4478 | 1632 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3702 | 1641 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3938 | 1641 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3983 | 1641 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 4006 | 1641 |
| E202 | LO PRISE | Prise double | Sectionneur | 3061 | 1657 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3413 | 1664 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3190 | 1674 |
| E202 | LO PRISE | Prise double | Raccordement ventilateur | 4178 | 1685 |
| E202 | LO PRISE | Prise double | Prise comptoir | 4365 | 1686 |
| E202 | LO PRISE | Prise double | Prise laveuse | 4293 | 1687 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4450 | 1687 |
| E202 | LO PRISE | Prise double | Sectionneur | 4617 | 1692 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3705 | 1696 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3987 | 1698 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3301 | 1746 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3246 | 1769 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3301 | 1794 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3302 | 1818 |
| E202 | LO PRISE | Prise double | Prise étanche | 4136 | 1830 |
| E202 | LO PRISE | Prise double | Sectionneur | 2515 | 2571 |
| E202 | LO PRISE | Prise double | Prise comptoir | 2709 | 2590 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2652 | 2612 |
| E202 | LO PRISE | Prise double | Prise demi-commandée | 3054 | 2655 |
| E202 | LO PRISE | Prise double | Prise demi-commandée | 3288 | 2655 |
| E202 | LO PRISE | Prise double | Prise demi-commandée | 3525 | 2655 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 2710 | 2664 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3747 | 2694 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3936 | 2703 |
| E202 | LO PRISE | Prise double | Sortie informatique | 2765 | 2737 |
| E202 | LO PRISE | Prise double | Sectionneur | 4073 | 2747 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3913 | 2755 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3941 | 2755 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3994 | 2755 |
| E202 | LO PRISE | Prise double | Prise laveuse | 2994 | 2762 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3228 | 2762 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3473 | 2762 |
| E202 | LO PRISE | Prise double | Raccordement ventilateur | 3742 | 2765 |
| E202 | LO PRISE | Prise double | Prise laveuse | 2706 | 2818 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2912 | 2820 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3149 | 2820 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3386 | 2820 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3874 | 2833 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 2867 | 2872 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 2891 | 2872 |
| E202 | LO PRISE | Prise double | Prise comptoir | 2935 | 2872 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3105 | 2872 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3172 | 2872 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3353 | 2872 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3374 | 2872 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3420 | 2872 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3128 | 2873 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3480 | 2979 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3503 | 2979 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3555 | 2979 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3367 | 2983 |
| E202 | LO PRISE | Prise double | Prise salle de bain | 3951 | 2988 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3503 | 3036 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3241 | 3040 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 3295 | 3042 |
| E202 | LO PRISE | Prise double | Prise laveuse | 2964 | 3048 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4106 | 3058 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3294 | 3065 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 2626 | 3086 |
| E202 | LO PRISE | Prise double | Prise comptoir | 2655 | 3086 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 2708 | 3086 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3021 | 3096 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3657 | 3106 |
| E202 | LO PRISE | Prise double | Prise comptoir | 3718 | 3106 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3766 | 3106 |
| E202 | LO PRISE | Prise double | Prise laveuse | 3949 | 3109 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 3296 | 3112 |
| E202 | LO PRISE | Prise double | Prise micro-onde | 4078 | 3112 |
| E202 | LO PRISE | Prise double | Prise réfrigérateur | 4105 | 3114 |
| E202 | LO PRISE | Prise double | Raccordement condenseur | 4298 | 3144 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2701 | 3146 |
| E202 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3755 | 3164 |
| E202 | LO PRISE | Prise double | Panneau de logement | 3921 | 3165 |
| E202 | LO PRISE | Prise double | Panneau de logement | 4157 | 3165 |
| E202 | LO PRISE | Prise double | Thermostat | 3680 | 3237 |
| E202 | LO PRISE | Prise double | Aéroconvecteur 2000W | 3472 | 3258 |
| E202 | LO PRISE | Prise double | Aéroconvecteur 1250W | 3226 | 3263 |
| E202 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise laveuse | 3829 | 1631 |
| E202 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3076 | 2575 |
| E202 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3313 | 2575 |
| E202 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3550 | 2575 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3923 | 1278 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3279 | 1285 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4356 | 1291 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2972 | 1315 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3935 | 1335 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3649 | 1337 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3767 | 1393 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3467 | 1614 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4408 | 1632 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3688 | 1685 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3935 | 1696 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise double | 3657 | 1698 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3251 | 1739 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2651 | 2693 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3905 | 2702 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2941 | 2817 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3178 | 2817 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3415 | 2817 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3241 | 3004 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3473 | 3035 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4135 | 3056 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2734 | 3143 |
| E202 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3789 | 3159 |
| E202 | LO PRISE GFI WP | Prise étanche | Aéroconvecteur 2000W | 4064 | 1772 |
| E202 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3068 | 1359 |
| E202 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4547 | 1850 |
| E202 | LO TEL | Sortie câblo/informatique | Panneau de logement | 2732 | 2661 |
| E202 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3884 | 2766 |
| E202 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2808 | 3106 |
| E202 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3175 | 3107 |
| E202 | LO TV | Prise double | Panneau de logement | 3091 | 1266 |
| E202 | LO TV | Prise double | Plinthe 1000W | 3618 | 1785 |
| E202 | LO TV | Prise double | Plinthe 1000W | 3381 | 1786 |
| E202 | RWF 1250W | Aéroconvecteur 1250W | Sectionneur | 3199 | 3309 |
| E202 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4060 | 1849 |
| E202 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 3438 | 3309 |
| E202 | TH | Thermostat | Plinthe 300W | 4288 | 1301 |
| E202 | TH | Thermostat | Prise micro-onde | 2707 | 2639 |
| E202 | TH | Thermostat | Panneau de logement | 3061 | 3192 |
| E202 | TH | Thermostat | Sectionneur | 3673 | 3309 |
| E203 | B 1000W | Plinthe 1000W | Sectionneur | 3337 | 1859 |
| E203 | B 1000W | Plinthe 1000W | Sectionneur | 3574 | 1859 |
| E203 | B 1000W | Plinthe 1000W | Sectionneur | 3537 | 2585 |
| E203 | B 1000W | Plinthe 1000W | Prise demi-commandée | 3689 | 2603 |
| E203 | B 1000W | Plinthe 1000W | Sectionneur | 3662 | 3319 |
| E203 | LO EVAP | Raccordement évaporateur | Panneau de logement | 2745 | 3169 |
| E203 | LO P3000 | Prise double | Panneau de logement | 3587 | 1254 |
| E203 | LO P3000 | Prise double | Raccordement lave-vaisselle | 3927 | 1300 |
| E203 | LO P3000 | Prise double | Prise salle de bain | 3164 | 1311 |
| E203 | LO P3000 | Prise double | Prise salle de bain | 4294 | 1402 |
| E203 | LO P3000 | Prise double | Prise réfrigérateur | 3922 | 1413 |
| E203 | LO P3000 | Prise double | Panneau de logement | 3441 | 1594 |
| E203 | LO P3000 | Prise double | Panneau de logement | 3746 | 1610 |
| E203 | LO P3000 | Prise double | Prise laveuse | 4125 | 1616 |
| E203 | LO P3000 | Prise double | Prise laveuse | 4281 | 1697 |
| E203 | LO P3000 | Prise double | Thermostat | 2766 | 2683 |
| E203 | LO P3000 | Prise double | Prise laveuse | 2982 | 2772 |
| E203 | LO P3000 | Prise double | Prise laveuse | 3216 | 2772 |
| E203 | LO P3000 | Prise double | Sortie informatique | 4038 | 3094 |
| E203 | LO P3000 | Prise double | Prise salle de bain | 3412 | 3112 |
| E203 | LO P3000 | Prise double | Thermostat | 3040 | 3199 |
| E203 | LO PRISE | Prise double | Sectionneur | 3562 | 1122 |
| E203 | LO PRISE | Prise double | Sectionneur | 3792 | 1122 |
| E203 | LO PRISE | Prise double | Sectionneur | 4036 | 1122 |
| E203 | LO PRISE | Prise double | Aéroconvecteur 1500W | 3267 | 1177 |
| E203 | LO PRISE | Prise double | Panneau de logement | 3961 | 1261 |
| E203 | LO PRISE | Prise double | Aéroconvecteur 1500W | 4451 | 1261 |
| E203 | LO PRISE | Prise double | Panneau de logement | 3719 | 1288 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3809 | 1288 |
| E203 | LO PRISE | Prise double | Panneau de logement | 2887 | 1291 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4440 | 1297 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3646 | 1300 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3041 | 1308 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2984 | 1352 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3041 | 1356 |
| E203 | LO PRISE | Prise double | Prise comptoir | 4405 | 1359 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3571 | 1368 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 4469 | 1369 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3999 | 1372 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3042 | 1381 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3122 | 1381 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3207 | 1401 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3240 | 1402 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3755 | 1403 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3639 | 1413 |
| E203 | LO PRISE | Prise double | Prise laveuse | 2966 | 1457 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3250 | 1462 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3321 | 1462 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3693 | 1462 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3764 | 1462 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3295 | 1463 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3739 | 1463 |
| E203 | LO PRISE | Prise double | Prise laveuse | 4238 | 1468 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3459 | 1566 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3504 | 1566 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3526 | 1567 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3689 | 1594 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3289 | 1600 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3485 | 1622 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3816 | 1641 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 4443 | 1642 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 4466 | 1642 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3926 | 1651 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3971 | 1651 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3994 | 1651 |
| E203 | LO PRISE | Prise double | Sectionneur | 3049 | 1668 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3400 | 1674 |
| E203 | LO PRISE | Prise double | Prise comptoir | 4353 | 1696 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4437 | 1697 |
| E203 | LO PRISE | Prise double | Sectionneur | 4605 | 1703 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3693 | 1706 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3975 | 1708 |
| E203 | LO PRISE | Prise double | Prise salle de bain | 4174 | 1709 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3239 | 1748 |
| E203 | LO PRISE | Prise double | Panneau de logement | 4388 | 1749 |
| E203 | LO PRISE | Prise double | Panneau de logement | 4068 | 1753 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3289 | 1756 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3234 | 1778 |
| E203 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4052 | 1783 |
| E203 | LO PRISE | Prise double | Plinthe 1000W | 3606 | 1795 |
| E203 | LO PRISE | Prise double | Plinthe 1000W | 3369 | 1796 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3289 | 1803 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3290 | 1828 |
| E203 | LO PRISE | Prise double | Sectionneur | 2505 | 2583 |
| E203 | LO PRISE | Prise double | Aéroconvecteur 1500W | 2917 | 2598 |
| E203 | LO PRISE | Prise double | Prise comptoir | 2696 | 2601 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2640 | 2622 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 2695 | 2649 |
| E203 | LO PRISE | Prise double | Panneau de logement | 2882 | 2701 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3936 | 2702 |
| E203 | LO PRISE | Prise double | Prise comptoir | 2639 | 2704 |
| E203 | LO PRISE | Prise double | Panneau de logement | 3896 | 2712 |
| E203 | LO PRISE | Prise double | Prise demi-commandée | 3042 | 2737 |
| E203 | LO PRISE | Prise double | Prise demi-commandée | 3276 | 2737 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3767 | 2737 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3928 | 2754 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3901 | 2756 |
| E203 | LO PRISE | Prise double | Sectionneur | 4060 | 2757 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3992 | 2764 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3527 | 2809 |
| E203 | LO PRISE | Prise double | Prise laveuse | 2693 | 2828 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2899 | 2830 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3136 | 2830 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3527 | 2833 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3324 | 2845 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3475 | 2848 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3527 | 2881 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 2855 | 2882 |
| E203 | LO PRISE | Prise double | Prise comptoir | 2922 | 2882 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3092 | 2882 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3160 | 2882 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 2878 | 2883 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3115 | 2883 |
| E203 | LO PRISE | Prise double | Raccordement volet motorisé | 3324 | 2956 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3466 | 2989 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3538 | 2989 |
| E203 | LO PRISE | Prise double | Prise laveuse | 4072 | 2996 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3889 | 3020 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3833 | 3036 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3228 | 3050 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3482 | 3050 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3283 | 3052 |
| E203 | LO PRISE | Prise double | Prise laveuse | 2952 | 3058 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3889 | 3066 |
| E203 | LO PRISE | Prise double | Prise comptoir | 3282 | 3075 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 3889 | 3091 |
| E203 | LO PRISE | Prise double | Prise comptoir | 4152 | 3091 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 4198 | 3092 |
| E203 | LO PRISE | Prise double | Prise réfrigérateur | 2614 | 3096 |
| E203 | LO PRISE | Prise double | Prise comptoir | 2642 | 3096 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 2696 | 3096 |
| E203 | LO PRISE | Prise double | Thermostat | 3412 | 3097 |
| E203 | LO PRISE | Prise double | Sectionneur | 2577 | 3105 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3009 | 3106 |
| E203 | LO PRISE | Prise double | Panneau de logement | 3805 | 3119 |
| E203 | LO PRISE | Prise double | Prise micro-onde | 3284 | 3123 |
| E203 | LO PRISE | Prise double | Panneau de logement | 4109 | 3142 |
| E203 | LO PRISE | Prise double | Panneau de logement | 3185 | 3147 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4163 | 3154 |
| E203 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2689 | 3156 |
| E203 | LO PRISE | Prise double | Prise laveuse | 3760 | 3161 |
| E203 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4211 | 3184 |
| E203 | LO PRISE | Prise double | Raccordement évaporateur | 2810 | 3217 |
| E203 | LO PRISE | Prise double | Sectionneur | 3187 | 3319 |
| E203 | LO PRISE | Prise double | Sectionneur | 3425 | 3319 |
| E203 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3063 | 2585 |
| E203 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3300 | 2585 |
| E203 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 3602 | 2586 |
| E203 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise double | 2737 | 2593 |
| E203 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3212 | 1281 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3910 | 1288 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4344 | 1301 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3922 | 1345 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3637 | 1347 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise réfrigérateur | 4377 | 1360 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2985 | 1384 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise micro-onde | 3922 | 1389 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise micro-onde | 3638 | 1390 |
| E203 | LO PRISE GFI | Prise salle de bain | Raccordement lave-vaisselle | 3727 | 1402 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise micro-onde | 3689 | 1611 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3454 | 1624 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4395 | 1642 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3689 | 1651 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3676 | 1695 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3923 | 1706 |
| E203 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3185 | 1749 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3902 | 2700 |
| E203 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 2635 | 2712 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3456 | 2820 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2929 | 2827 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3166 | 2827 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3830 | 3005 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3228 | 3014 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3451 | 3049 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2722 | 3153 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4132 | 3154 |
| E203 | LO PRISE GFI | Prise salle de bain | Prise double | 3443 | 3177 |
| E203 | LO PRISE POELE | Prise cuisinière | Prise comptoir | 3489 | 2989 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4534 | 1854 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2752 | 2740 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3795 | 2762 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3574 | 2775 |
| E203 | LO TEL | Sortie câblo/informatique | Prise réfrigérateur | 4128 | 3093 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2796 | 3107 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3572 | 3107 |
| E203 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3162 | 3111 |
| E203 | LO TV | Prise double | Panneau de logement | 4333 | 1268 |
| E203 | LO TV | Prise double | Plinthe 1000W | 3721 | 2586 |
| E203 | LO TV | Prise double | Panneau de logement | 3129 | 2703 |
| E203 | LO TV | Prise double | Panneau de logement | 3481 | 2733 |
| E203 | LO TV | Prise double | Plinthe 1000W | 3603 | 3280 |
| E203 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3325 | 1122 |
| E203 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 4536 | 1263 |
| E203 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 2862 | 2585 |
| E203 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4048 | 1859 |
| E203 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4296 | 3154 |
| E203 | TH | Thermostat | Prise réfrigérateur | 2697 | 2674 |
| E203 | TH | Thermostat | Panneau de logement | 3455 | 3147 |
| E203 | TH | Thermostat | Prise double | 3107 | 3175 |
| E203 | VCFF | Raccordement volet motorisé | Prise laveuse | 3332 | 3033 |
| E204 | B 1000W | Plinthe 1000W | Sectionneur | 3573 | 1122 |
| E204 | B 1000W | Plinthe 1000W | Plinthe 1250W | 4206 | 1163 |
| E204 | B 1000W | Plinthe 1000W | Sectionneur | 3347 | 1859 |
| E204 | B 1000W | Plinthe 1000W | Sectionneur | 3584 | 1859 |
| E204 | B 1000W | Plinthe 1000W | Sectionneur | 3548 | 2585 |
| E204 | B 1000W | Plinthe 1000W | Prise double | 2747 | 2593 |
| E204 | B 1000W | Plinthe 1000W | Prise demi-commandée | 3700 | 2603 |
| E204 | B 1000W | Plinthe 1000W | Sectionneur | 3673 | 3319 |
| E204 | LO CONENSEUR | Raccordement condenseur | Prise demi-commandée | 3823 | 1784 |
| E204 | LO EVAP | Raccordement évaporateur | Panneau de logement | 2755 | 3169 |
| E204 | LO P3000 | Prise double | Prise laveuse | 3820 | 1288 |
| E204 | LO P3000 | Prise double | Thermostat | 3185 | 1329 |
| E204 | LO P3000 | Prise double | Prise laveuse | 4009 | 1372 |
| E204 | LO P3000 | Prise double | Prise salle de bain | 4305 | 1402 |
| E204 | LO P3000 | Prise double | Panneau de logement | 3452 | 1594 |
| E204 | LO P3000 | Prise double | Prise laveuse | 4135 | 1616 |
| E204 | LO P3000 | Prise double | Prise laveuse | 4291 | 1697 |
| E204 | LO P3000 | Prise double | Thermostat | 2777 | 2683 |
| E204 | LO P3000 | Prise double | Prise laveuse | 2992 | 2772 |
| E204 | LO P3000 | Prise double | Prise laveuse | 3226 | 2772 |
| E204 | LO P3000 | Prise double | Thermostat | 2729 | 3041 |
| E204 | LO P3000 | Prise double | Sortie informatique | 4048 | 3094 |
| E204 | LO P3000 | Prise double | Thermostat | 3422 | 3097 |
| E204 | LO P3000 | Prise double | Thermostat | 3051 | 3199 |
| E204 | LO PRISE | Prise double | Sectionneur | 3803 | 1122 |
| E204 | LO PRISE | Prise double | Sectionneur | 4047 | 1122 |
| E204 | LO PRISE | Prise double | Aéroconvecteur 1500W | 3277 | 1177 |
| E204 | LO PRISE | Prise double | Panneau de logement | 3972 | 1261 |
| E204 | LO PRISE | Prise double | Aéroconvecteur 1500W | 4461 | 1261 |
| E204 | LO PRISE | Prise double | Panneau de logement | 3729 | 1288 |
| E204 | LO PRISE | Prise double | Panneau de logement | 2898 | 1291 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4450 | 1297 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3657 | 1300 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3937 | 1300 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3052 | 1308 |
| E204 | LO PRISE | Prise double | Prise salle de bain | 3175 | 1311 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2994 | 1352 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3051 | 1356 |
| E204 | LO PRISE | Prise double | Prise comptoir | 4415 | 1359 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3582 | 1368 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 4479 | 1369 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3053 | 1381 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3132 | 1381 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3933 | 1389 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3648 | 1390 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3250 | 1402 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3738 | 1402 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3650 | 1413 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3933 | 1413 |
| E204 | LO PRISE | Prise double | Prise laveuse | 2977 | 1457 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3260 | 1462 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3331 | 1462 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3703 | 1462 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3306 | 1463 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3749 | 1463 |
| E204 | LO PRISE | Prise double | Prise laveuse | 4249 | 1468 |
| E204 | LO PRISE | Prise double | Raccordement volet motorisé | 3810 | 1490 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3469 | 1566 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3515 | 1566 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3536 | 1567 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3700 | 1594 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3299 | 1601 |
| E204 | LO PRISE | Prise double | Panneau de logement | 3756 | 1610 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3700 | 1611 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3495 | 1622 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3827 | 1641 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 4454 | 1642 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 4476 | 1642 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3937 | 1651 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3981 | 1651 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 4004 | 1651 |
| E204 | LO PRISE | Prise double | Sectionneur | 3059 | 1668 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3411 | 1674 |
| E204 | LO PRISE | Prise double | Prise comptoir | 4363 | 1696 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4448 | 1697 |
| E204 | LO PRISE | Prise double | Sectionneur | 4615 | 1703 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3703 | 1706 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3985 | 1708 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3250 | 1749 |
| E204 | LO PRISE | Prise double | Panneau de logement | 4398 | 1749 |
| E204 | LO PRISE | Prise double | Panneau de logement | 4079 | 1753 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3299 | 1756 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3244 | 1779 |
| E204 | LO PRISE | Prise double | Plinthe 1000W | 3616 | 1795 |
| E204 | LO PRISE | Prise double | Plinthe 1000W | 3379 | 1796 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3299 | 1804 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3300 | 1828 |
| E204 | LO PRISE | Prise double | Prise étanche | 4134 | 1840 |
| E204 | LO PRISE | Prise double | Sectionneur | 2516 | 2583 |
| E204 | LO PRISE | Prise double | Aéroconvecteur 1500W | 2928 | 2598 |
| E204 | LO PRISE | Prise double | Prise comptoir | 2707 | 2601 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2651 | 2622 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 2705 | 2649 |
| E204 | LO PRISE | Prise double | Panneau de logement | 2892 | 2701 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3947 | 2702 |
| E204 | LO PRISE | Prise double | Panneau de logement | 2646 | 2712 |
| E204 | LO PRISE | Prise double | Panneau de logement | 3907 | 2712 |
| E204 | LO PRISE | Prise double | Prise demi-commandée | 3052 | 2737 |
| E204 | LO PRISE | Prise double | Prise demi-commandée | 3286 | 2737 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3777 | 2737 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3939 | 2754 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3911 | 2756 |
| E204 | LO PRISE | Prise double | Sectionneur | 4071 | 2757 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 4003 | 2764 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3537 | 2809 |
| E204 | LO PRISE | Prise double | Prise laveuse | 2704 | 2828 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2910 | 2830 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3147 | 2830 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3538 | 2833 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3334 | 2845 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3485 | 2848 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3537 | 2881 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 2865 | 2882 |
| E204 | LO PRISE | Prise double | Prise comptoir | 2933 | 2882 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3103 | 2882 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3170 | 2882 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 2889 | 2883 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3126 | 2883 |
| E204 | LO PRISE | Prise double | Raccordement volet motorisé | 3336 | 2963 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3476 | 2989 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3500 | 2989 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3549 | 2989 |
| E204 | LO PRISE | Prise double | Prise laveuse | 4083 | 2996 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3899 | 3020 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3343 | 3033 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3843 | 3036 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3239 | 3050 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3492 | 3050 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3293 | 3052 |
| E204 | LO PRISE | Prise double | Prise laveuse | 2963 | 3058 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3899 | 3066 |
| E204 | LO PRISE | Prise double | Prise comptoir | 3292 | 3075 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 3900 | 3091 |
| E204 | LO PRISE | Prise double | Prise comptoir | 4163 | 3091 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 4208 | 3092 |
| E204 | LO PRISE | Prise double | Prise réfrigérateur | 2625 | 3096 |
| E204 | LO PRISE | Prise double | Prise comptoir | 2653 | 3096 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 2707 | 3096 |
| E204 | LO PRISE | Prise double | Sectionneur | 2587 | 3105 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3020 | 3106 |
| E204 | LO PRISE | Prise double | Prise salle de bain | 3423 | 3112 |
| E204 | LO PRISE | Prise double | Panneau de logement | 3816 | 3119 |
| E204 | LO PRISE | Prise double | Prise micro-onde | 3294 | 3122 |
| E204 | LO PRISE | Prise double | Panneau de logement | 4119 | 3142 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4173 | 3154 |
| E204 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2700 | 3156 |
| E204 | LO PRISE | Prise double | Prise laveuse | 3770 | 3161 |
| E204 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4222 | 3184 |
| E204 | LO PRISE | Prise double | Prise demi-commandée | 3169 | 3212 |
| E204 | LO PRISE | Prise double | Raccordement évaporateur | 2821 | 3217 |
| E204 | LO PRISE | Prise double | Sectionneur | 3197 | 3319 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 3614 | 1163 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise double | 3772 | 1687 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3074 | 2585 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3311 | 2585 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 3613 | 2586 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 2783 | 2587 |
| E204 | LO PRISE CONTROLÉ | Prise demi-commandée | Panneau de logement | 3196 | 3147 |
| E204 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3222 | 1281 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3921 | 1288 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4354 | 1301 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3933 | 1345 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3647 | 1347 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise réfrigérateur | 4388 | 1360 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2995 | 1384 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3217 | 1401 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3766 | 1403 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3465 | 1624 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4406 | 1642 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3700 | 1651 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3686 | 1695 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3933 | 1706 |
| E204 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3195 | 1749 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3912 | 2700 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2649 | 2704 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3467 | 2820 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2939 | 2827 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3176 | 2827 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3841 | 3005 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3239 | 3014 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3462 | 3049 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2733 | 3153 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4142 | 3154 |
| E204 | LO PRISE GFI | Prise salle de bain | Prise double | 3453 | 3177 |
| E204 | LO PRISE GFI WP | Prise étanche | Sectionneur | 4058 | 1859 |
| E204 | LO TEL | Sortie câblo/informatique | Prise double | 2942 | 1228 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4544 | 1854 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2762 | 2740 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3804 | 2762 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3584 | 2775 |
| E204 | LO TEL | Sortie câblo/informatique | Prise réfrigérateur | 4138 | 3093 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2806 | 3107 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3582 | 3107 |
| E204 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3172 | 3111 |
| E204 | LO TV | Prise double | Aéroconvecteur 1500W | 3755 | 1175 |
| E204 | LO TV | Prise double | Sortie câblo/informatique | 2953 | 1196 |
| E204 | LO TV | Prise double | Panneau de logement | 3598 | 1254 |
| E204 | LO TV | Prise double | Panneau de logement | 4344 | 1268 |
| E204 | LO TV | Prise double | Plinthe 1000W | 3731 | 2586 |
| E204 | LO TV | Prise double | Panneau de logement | 3139 | 2703 |
| E204 | LO TV | Prise double | Panneau de logement | 3492 | 2733 |
| E204 | LO TV | Prise double | Plinthe 1000W | 3613 | 3280 |
| E204 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3336 | 1122 |
| E204 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 3698 | 1176 |
| E204 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 4547 | 1263 |
| E204 | RWF 1500W | Aéroconvecteur 1500W | Prise demi-commandée | 2872 | 2585 |
| E204 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4306 | 3154 |
| E204 | TH | Thermostat | Prise double | 3174 | 1234 |
| E204 | TH | Thermostat | Prise réfrigérateur | 2708 | 2674 |
| E204 | TH | Thermostat | Prise double | 2673 | 3054 |
| E204 | TH | Thermostat | Panneau de logement | 3465 | 3147 |
| E204 | TH | Thermostat | Prise double | 3041 | 3220 |
| E204 | VCFF | Raccordement volet motorisé | Prise réfrigérateur | 3774 | 1462 |
| E204 | VCFF | Raccordement volet motorisé | Prise double | 3369 | 3027 |
| E205 | B 1000W | Plinthe 1000W | Sectionneur | 3342 | 1857 |
| E205 | B 1000W | Plinthe 1000W | Sectionneur | 3580 | 1857 |
| E205 | B 1000W | Plinthe 1000W | Sectionneur | 3668 | 3316 |
| E205 | LO P3000 | Prise double | Panneau de logement | 3593 | 1252 |
| E205 | LO P3000 | Prise double | Prise laveuse | 3815 | 1286 |
| E205 | LO P3000 | Prise double | Prise salle de bain | 3170 | 1308 |
| E205 | LO P3000 | Prise double | Prise laveuse | 4004 | 1369 |
| E205 | LO P3000 | Prise double | Prise salle de bain | 4300 | 1400 |
| E205 | LO P3000 | Prise double | Thermostat | 3015 | 1480 |
| E205 | LO P3000 | Prise double | Prise réfrigérateur | 3695 | 1591 |
| E205 | LO P3000 | Prise double | Panneau de logement | 3447 | 1592 |
| E205 | LO P3000 | Prise double | Prise laveuse | 4130 | 1614 |
| E205 | LO P3000 | Prise double | Prise laveuse | 4286 | 1694 |
| E205 | LO P3000 | Prise double | Thermostat | 2772 | 2681 |
| E205 | LO P3000 | Prise double | Prise laveuse | 2988 | 2770 |
| E205 | LO P3000 | Prise double | Prise laveuse | 3222 | 2770 |
| E205 | LO P3000 | Prise double | Prise micro-onde | 3894 | 3017 |
| E205 | LO P3000 | Prise double | Sortie informatique | 4045 | 3093 |
| E205 | LO P3000 | Prise double | Prise salle de bain | 3418 | 3110 |
| E205 | LO P3000 | Prise double | Thermostat | 3046 | 3197 |
| E205 | LO PRISE | Prise double | Sectionneur | 3568 | 1119 |
| E205 | LO PRISE | Prise double | Sectionneur | 3798 | 1119 |
| E205 | LO PRISE | Prise double | Sectionneur | 4042 | 1119 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3967 | 1258 |
| E205 | LO PRISE | Prise double | Aéroconvecteur 1500W | 4456 | 1259 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3725 | 1285 |
| E205 | LO PRISE | Prise double | Panneau de logement | 2893 | 1289 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4446 | 1295 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3652 | 1298 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3932 | 1298 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3047 | 1306 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2990 | 1349 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3046 | 1353 |
| E205 | LO PRISE | Prise double | Prise comptoir | 4411 | 1356 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3577 | 1366 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 4474 | 1366 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3048 | 1379 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3127 | 1379 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3928 | 1387 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3643 | 1388 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3246 | 1400 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3733 | 1400 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3645 | 1410 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3928 | 1410 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3255 | 1460 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3326 | 1460 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3698 | 1460 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3769 | 1460 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3301 | 1461 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3744 | 1461 |
| E205 | LO PRISE | Prise double | Prise laveuse | 4244 | 1466 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3465 | 1564 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3510 | 1564 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3531 | 1564 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3294 | 1598 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3695 | 1609 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3491 | 1619 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3822 | 1638 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 4449 | 1640 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 4472 | 1640 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3695 | 1648 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3932 | 1649 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3977 | 1649 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 4000 | 1649 |
| E205 | LO PRISE | Prise double | Sectionneur | 3054 | 1665 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3406 | 1672 |
| E205 | LO PRISE | Prise double | Prise comptoir | 4359 | 1694 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4443 | 1694 |
| E205 | LO PRISE | Prise double | Sectionneur | 4610 | 1700 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3698 | 1704 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3980 | 1706 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3245 | 1746 |
| E205 | LO PRISE | Prise double | Panneau de logement | 4393 | 1747 |
| E205 | LO PRISE | Prise double | Panneau de logement | 4074 | 1750 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3294 | 1754 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3239 | 1776 |
| E205 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4057 | 1780 |
| E205 | LO PRISE | Prise double | Plinthe 1000W | 3374 | 1793 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3295 | 1801 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3296 | 1826 |
| E205 | LO PRISE | Prise double | Prise comptoir | 2702 | 2598 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2646 | 2619 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 2700 | 2647 |
| E205 | LO PRISE | Prise double | Aéroconvecteur 1500W | 3521 | 2658 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3942 | 2699 |
| E205 | LO PRISE | Prise double | Panneau de logement | 2641 | 2709 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3902 | 2709 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3487 | 2730 |
| E205 | LO PRISE | Prise double | Prise demi-commandée | 3048 | 2734 |
| E205 | LO PRISE | Prise double | Prise demi-commandée | 3281 | 2734 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3772 | 2734 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3934 | 2752 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3907 | 2753 |
| E205 | LO PRISE | Prise double | Sectionneur | 4066 | 2755 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3998 | 2762 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3532 | 2807 |
| E205 | LO PRISE | Prise double | Prise laveuse | 2699 | 2826 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2905 | 2828 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3142 | 2828 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3533 | 2831 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3329 | 2842 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3480 | 2845 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 2861 | 2879 |
| E205 | LO PRISE | Prise double | Prise comptoir | 2928 | 2879 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3098 | 2879 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3165 | 2879 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3533 | 2879 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 2884 | 2880 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3121 | 2880 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3495 | 2986 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3471 | 2987 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3544 | 2987 |
| E205 | LO PRISE | Prise double | Prise laveuse | 4078 | 2993 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3338 | 3031 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3839 | 3034 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3234 | 3047 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3487 | 3048 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3288 | 3050 |
| E205 | LO PRISE | Prise double | Prise laveuse | 2958 | 3055 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3894 | 3063 |
| E205 | LO PRISE | Prise double | Prise comptoir | 3287 | 3072 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 3895 | 3088 |
| E205 | LO PRISE | Prise double | Prise comptoir | 4158 | 3089 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 4204 | 3089 |
| E205 | LO PRISE | Prise double | Prise réfrigérateur | 2620 | 3094 |
| E205 | LO PRISE | Prise double | Prise comptoir | 2648 | 3094 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 2702 | 3094 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3015 | 3104 |
| E205 | LO PRISE | Prise double | Sortie informatique | 2803 | 3106 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3811 | 3117 |
| E205 | LO PRISE | Prise double | Prise micro-onde | 3290 | 3120 |
| E205 | LO PRISE | Prise double | Panneau de logement | 4114 | 3139 |
| E205 | LO PRISE | Prise double | Panneau de logement | 3191 | 3145 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4169 | 3151 |
| E205 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2694 | 3153 |
| E205 | LO PRISE | Prise double | Prise laveuse | 3766 | 3159 |
| E205 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4217 | 3181 |
| E205 | LO PRISE | Prise double | Sectionneur | 3192 | 3316 |
| E205 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3069 | 2582 |
| E205 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3306 | 2582 |
| E205 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3217 | 1278 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3916 | 1286 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4350 | 1299 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3928 | 1342 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3642 | 1344 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise réfrigérateur | 4383 | 1358 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2990 | 1382 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3213 | 1398 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3761 | 1401 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3460 | 1621 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4401 | 1640 |
| E205 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3751 | 1666 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3682 | 1692 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3929 | 1704 |
| E205 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3190 | 1747 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3908 | 2698 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2645 | 2701 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3462 | 2818 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2935 | 2825 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3172 | 2825 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3836 | 3003 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3234 | 3011 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3457 | 3047 |
| E205 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3461 | 3145 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2728 | 3150 |
| E205 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4137 | 3151 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4541 | 1852 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2758 | 2738 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3801 | 2760 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3580 | 2773 |
| E205 | LO TEL | Sortie câblo/informatique | Prise réfrigérateur | 4134 | 3091 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3579 | 3106 |
| E205 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3168 | 3109 |
| E205 | LO TEL | Sortie câblo/informatique | Panneau de logement | 2750 | 3167 |
| E205 | LO TV | Prise double | Aéroconvecteur 1500W | 3272 | 1174 |
| E205 | LO TV | Prise double | Panneau de logement | 4339 | 1266 |
| E205 | LO TV | Prise double | Plinthe 1000W | 3612 | 1793 |
| E205 | LO TV | Prise double | Panneau de logement | 2888 | 2699 |
| E205 | LO TV | Prise double | Panneau de logement | 3134 | 2700 |
| E205 | LO TV | Prise double | Plinthe 1000W | 3608 | 3278 |
| E205 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3331 | 1119 |
| E205 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 4542 | 1261 |
| E205 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3543 | 2582 |
| E205 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4054 | 1857 |
| E205 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4302 | 3151 |
| E205 | TH | Thermostat | Prise laveuse | 2972 | 1454 |
| E205 | TH | Thermostat | Prise réfrigérateur | 2703 | 2672 |
| E205 | TH | Thermostat | Prise double | 3112 | 3173 |
| E206 | B 1000W | Plinthe 1000W | Sectionneur | 3329 | 1851 |
| E206 | B 1000W | Plinthe 1000W | Sectionneur | 3566 | 1851 |
| E206 | B 1000W | Plinthe 1000W | Sectionneur | 3530 | 2577 |
| E206 | B 1000W | Plinthe 1000W | Sectionneur | 4053 | 2749 |
| E206 | B 1000W | Plinthe 1000W | Sectionneur | 3655 | 3311 |
| E206 | LO CONENSEUR | Raccordement condenseur | Prise demi-commandée | 3805 | 1776 |
| E206 | LO P3000 | Prise double | Panneau de logement | 3580 | 1246 |
| E206 | LO P3000 | Prise double | Raccordement lave-vaisselle | 3919 | 1292 |
| E206 | LO P3000 | Prise double | Prise laveuse | 3991 | 1364 |
| E206 | LO P3000 | Prise double | Prise laveuse | 3114 | 1373 |
| E206 | LO P3000 | Prise double | Prise salle de bain | 4286 | 1394 |
| E206 | LO P3000 | Prise double | Thermostat | 3002 | 1475 |
| E206 | LO P3000 | Prise double | Panneau de logement | 3434 | 1586 |
| E206 | LO P3000 | Prise double | Prise laveuse | 4117 | 1608 |
| E206 | LO P3000 | Prise double | Prise réfrigérateur | 2690 | 2666 |
| E206 | LO P3000 | Prise double | Prise laveuse | 3208 | 2764 |
| E206 | LO P3000 | Prise double | Prise laveuse | 2999 | 3097 |
| E206 | LO P3000 | Prise double | Prise salle de bain | 3404 | 3105 |
| E206 | LO PRISE | Prise double | Sectionneur | 3555 | 1114 |
| E206 | LO PRISE | Prise double | Sectionneur | 3784 | 1114 |
| E206 | LO PRISE | Prise double | Sectionneur | 4029 | 1114 |
| E206 | LO PRISE | Prise double | Panneau de logement | 3954 | 1253 |
| E206 | LO PRISE | Prise double | Aéroconvecteur 1500W | 4443 | 1254 |
| E206 | LO PRISE | Prise double | Panneau de logement | 3711 | 1280 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3802 | 1280 |
| E206 | LO PRISE | Prise double | Panneau de logement | 2880 | 1283 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4432 | 1290 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3639 | 1292 |
| E206 | LO PRISE | Prise double | Thermostat | 4032 | 1295 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3034 | 1300 |
| E206 | LO PRISE | Prise double | Prise salle de bain | 3157 | 1303 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2976 | 1344 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3033 | 1348 |
| E206 | LO PRISE | Prise double | Prise comptoir | 4397 | 1351 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3564 | 1361 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 4461 | 1361 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3035 | 1373 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3630 | 1382 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3915 | 1382 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3720 | 1394 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3232 | 1395 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3632 | 1405 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3915 | 1405 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3242 | 1454 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3313 | 1454 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3685 | 1454 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3288 | 1455 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3731 | 1455 |
| E206 | LO PRISE | Prise double | Prise laveuse | 4230 | 1461 |
| E206 | LO PRISE | Prise double | Raccordement volet motorisé | 3790 | 1492 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3451 | 1558 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3497 | 1558 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3518 | 1559 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3682 | 1586 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3281 | 1593 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3682 | 1603 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3477 | 1614 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3809 | 1633 |
| E206 | LO PRISE | Prise double | Prise comptoir | 4388 | 1634 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 4436 | 1634 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 4458 | 1634 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3918 | 1643 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3963 | 1643 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3986 | 1644 |
| E206 | LO PRISE | Prise double | Sectionneur | 3041 | 1660 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3393 | 1666 |
| E206 | LO PRISE | Prise double | Prise laveuse | 4273 | 1689 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4430 | 1689 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3685 | 1698 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3967 | 1700 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3231 | 1741 |
| E206 | LO PRISE | Prise double | Panneau de logement | 4380 | 1741 |
| E206 | LO PRISE | Prise double | Panneau de logement | 4061 | 1745 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3281 | 1749 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3226 | 1771 |
| E206 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4044 | 1775 |
| E206 | LO PRISE | Prise double | Plinthe 1000W | 3598 | 1787 |
| E206 | LO PRISE | Prise double | Plinthe 1000W | 3361 | 1788 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3281 | 1796 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3282 | 1821 |
| E206 | LO PRISE | Prise double | Sectionneur | 2497 | 2575 |
| E206 | LO PRISE | Prise double | Prise comptoir | 2689 | 2593 |
| E206 | LO PRISE | Prise double | Prise demi-commandée | 3682 | 2595 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2633 | 2614 |
| E206 | LO PRISE | Prise double | Thermostat | 2759 | 2675 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3928 | 2694 |
| E206 | LO PRISE | Prise double | Panneau de logement | 2627 | 2704 |
| E206 | LO PRISE | Prise double | Panneau de logement | 3888 | 2704 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3759 | 2723 |
| E206 | LO PRISE | Prise double | Prise demi-commandée | 3034 | 2729 |
| E206 | LO PRISE | Prise double | Prise demi-commandée | 3268 | 2729 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3921 | 2746 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3893 | 2748 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3985 | 2756 |
| E206 | LO PRISE | Prise double | Prise laveuse | 2974 | 2764 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3521 | 2805 |
| E206 | LO PRISE | Prise double | Prise laveuse | 2686 | 2820 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2893 | 2820 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3129 | 2822 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3520 | 2828 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3316 | 2837 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3460 | 2837 |
| E206 | LO PRISE | Prise double | Prise demi-commandée | 3995 | 2857 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 2847 | 2874 |
| E206 | LO PRISE | Prise double | Prise comptoir | 2915 | 2874 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 2870 | 2875 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3084 | 2875 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3108 | 2875 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3152 | 2875 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3520 | 2876 |
| E206 | LO PRISE | Prise double | Raccordement volet motorisé | 3319 | 2948 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3458 | 2981 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3481 | 2981 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3530 | 2981 |
| E206 | LO PRISE | Prise double | Prise laveuse | 4064 | 2988 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3881 | 3010 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3324 | 3025 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3825 | 3028 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3221 | 3042 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3474 | 3043 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3275 | 3044 |
| E206 | LO PRISE | Prise double | Prise laveuse | 2945 | 3047 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3881 | 3054 |
| E206 | LO PRISE | Prise double | Prise comptoir | 3274 | 3064 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 3882 | 3079 |
| E206 | LO PRISE | Prise double | Prise comptoir | 4144 | 3083 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 4190 | 3084 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 4120 | 3085 |
| E206 | LO PRISE | Prise double | Prise réfrigérateur | 2607 | 3088 |
| E206 | LO PRISE | Prise double | Prise comptoir | 2635 | 3088 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 2689 | 3088 |
| E206 | LO PRISE | Prise double | Sectionneur | 2569 | 3097 |
| E206 | LO PRISE | Prise double | Prise salle de bain | 3081 | 3097 |
| E206 | LO PRISE | Prise double | Prise micro-onde | 3276 | 3110 |
| E206 | LO PRISE | Prise double | Panneau de logement | 3798 | 3111 |
| E206 | LO PRISE | Prise double | Panneau de logement | 4101 | 3134 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4155 | 3146 |
| E206 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2682 | 3148 |
| E206 | LO PRISE | Prise double | Prise laveuse | 3752 | 3153 |
| E206 | LO PRISE | Prise double | Panneau de logement | 2737 | 3161 |
| E206 | LO PRISE | Prise double | Sectionneur | 3418 | 3311 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Panneau de logement | 3726 | 1652 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3055 | 2577 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3293 | 2577 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 3595 | 2578 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Plinthe 1000W | 4001 | 2835 |
| E206 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise double | 3398 | 3264 |
| E206 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3204 | 1273 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3903 | 1281 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4336 | 1293 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3915 | 1337 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3629 | 1339 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise réfrigérateur | 4370 | 1352 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2977 | 1376 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3199 | 1393 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3747 | 1395 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3447 | 1616 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3682 | 1643 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3668 | 1687 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4345 | 1688 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3915 | 1698 |
| E206 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3177 | 1741 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3892 | 2692 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2631 | 2696 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3449 | 2813 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2921 | 2819 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3158 | 2819 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3823 | 2997 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3220 | 3006 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3443 | 3041 |
| E206 | LO PRISE GFI | Prise salle de bain | Sortie informatique | 3154 | 3103 |
| E206 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3447 | 3139 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2714 | 3145 |
| E206 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4124 | 3146 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4526 | 1845 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2745 | 2732 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3798 | 2753 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3567 | 2765 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4030 | 3075 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3564 | 3099 |
| E206 | LO TEL | Sortie câblo/informatique | Sortie informatique | 2776 | 3101 |
| E206 | LO TEL | Sortie câblo/informatique | Panneau de logement | 3178 | 3139 |
| E206 | LO TV | Prise double | Aéroconvecteur 1500W | 3259 | 1169 |
| E206 | LO TV | Prise double | Sortie câblo/informatique | 2935 | 1188 |
| E206 | LO TV | Prise double | Panneau de logement | 4326 | 1260 |
| E206 | LO TV | Prise double | Panneau de logement | 2874 | 2693 |
| E206 | LO TV | Prise double | Panneau de logement | 3121 | 2695 |
| E206 | LO TV | Prise double | Panneau de logement | 3473 | 2725 |
| E206 | LO TV | Prise double | Plinthe 1000W | 3595 | 3273 |
| E206 | LO TV | Prise double | Sectionneur | 3179 | 3311 |
| E206 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3317 | 1114 |
| E206 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 4529 | 1255 |
| E206 | RWF 2000W | Aéroconvecteur 2000W | Sectionneur | 4040 | 1851 |
| E206 | TH | Thermostat | Prise double | 4039 | 1197 |
| E206 | TH | Thermostat | Prise laveuse | 2959 | 1449 |
| E206 | TH | Thermostat | Prise micro-onde | 2687 | 2641 |
| E206 | VCFF | Raccordement volet motorisé | Prise réfrigérateur | 3756 | 1454 |
| E206 | VCFF | Raccordement volet motorisé | Prise double | 3274 | 2965 |
| E207 | B 1000W | Plinthe 1000W | Sectionneur | 3346 | 1848 |
| E207 | B 1000W | Plinthe 1000W | Sectionneur | 3583 | 1848 |
| E207 | LO P3000 | Prise double | Prise laveuse | 3819 | 1277 |
| E207 | LO P3000 | Prise double | Prise laveuse | 4008 | 1361 |
| E207 | LO P3000 | Prise double | Prise salle de bain | 4304 | 1391 |
| E207 | LO P3000 | Prise double | Panneau de logement | 3216 | 1408 |
| E207 | LO P3000 | Prise double | Panneau de logement | 4065 | 1579 |
| E207 | LO P3000 | Prise double | Prise comptoir | 3464 | 1613 |
| E207 | LO P3000 | Prise double | Panneau de logement | 3739 | 1617 |
| E207 | LO P3000 | Prise double | Panneau de logement | 4346 | 1623 |
| E207 | LO PRISE | Prise double | Sectionneur | 3807 | 1110 |
| E207 | LO PRISE | Prise double | Sectionneur | 4046 | 1110 |
| E207 | LO PRISE | Prise double | Aéroconvecteur 1500W | 3277 | 1166 |
| E207 | LO PRISE | Prise double | Panneau de logement | 3976 | 1227 |
| E207 | LO PRISE | Prise double | Aéroconvecteur 1500W | 4460 | 1250 |
| E207 | LO PRISE | Prise double | Panneau de logement | 3739 | 1259 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4450 | 1286 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3656 | 1289 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3051 | 1297 |
| E207 | LO PRISE | Prise double | Prise salle de bain | 3174 | 1300 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3932 | 1334 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 2994 | 1340 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3050 | 1344 |
| E207 | LO PRISE | Prise double | Prise comptoir | 4415 | 1348 |
| E207 | LO PRISE | Prise double | Prise laveuse | 3581 | 1357 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 4478 | 1358 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3052 | 1370 |
| E207 | LO PRISE | Prise double | Prise laveuse | 3131 | 1370 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3932 | 1378 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3648 | 1379 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3250 | 1391 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3737 | 1391 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3649 | 1402 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3932 | 1402 |
| E207 | LO PRISE | Prise double | Prise laveuse | 2976 | 1446 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3259 | 1451 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3331 | 1451 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3702 | 1451 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3774 | 1451 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3305 | 1452 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3748 | 1452 |
| E207 | LO PRISE | Prise double | Prise laveuse | 4248 | 1457 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3468 | 1555 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3514 | 1555 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3536 | 1555 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3699 | 1583 |
| E207 | LO PRISE | Prise double | Prise laveuse | 3298 | 1590 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3699 | 1600 |
| E207 | LO PRISE | Prise double | Prise laveuse | 4134 | 1605 |
| E207 | LO PRISE | Prise double | Prise salle de bain | 4000 | 1610 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3495 | 1611 |
| E207 | LO PRISE | Prise double | Prise laveuse | 3826 | 1630 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 4453 | 1631 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 4476 | 1631 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3936 | 1640 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3981 | 1640 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 4004 | 1641 |
| E207 | LO PRISE | Prise double | Sectionneur | 3058 | 1656 |
| E207 | LO PRISE | Prise double | Prise laveuse | 3410 | 1663 |
| E207 | LO PRISE | Prise double | Prise comptoir | 4363 | 1685 |
| E207 | LO PRISE | Prise double | Prise laveuse | 4290 | 1686 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4447 | 1686 |
| E207 | LO PRISE | Prise double | Sectionneur | 4615 | 1692 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3702 | 1695 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3984 | 1697 |
| E207 | LO PRISE | Prise double | Panneau de logement | 3198 | 1720 |
| E207 | LO PRISE | Prise double | Prise micro-onde | 3298 | 1745 |
| E207 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3243 | 1768 |
| E207 | LO PRISE | Prise double | Plinthe 1000W | 3379 | 1785 |
| E207 | LO PRISE | Prise double | Prise comptoir | 3299 | 1793 |
| E207 | LO PRISE | Prise double | Prise réfrigérateur | 3300 | 1817 |
| E207 | LO PRISE | Prise double | Prise étanche | 4133 | 1829 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3920 | 1277 |
| E207 | LO PRISE GFI | Prise salle de bain | Raccordement lave-vaisselle | 3936 | 1289 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4354 | 1290 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise double | 3216 | 1309 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3647 | 1336 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise réfrigérateur | 4387 | 1349 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 2994 | 1373 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3217 | 1390 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3765 | 1392 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4405 | 1631 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3699 | 1640 |
| E207 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 3505 | 1680 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3686 | 1684 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3933 | 1695 |
| E207 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3249 | 1738 |
| E207 | LO PRISE GFI WP | Prise étanche | Sectionneur | 4058 | 1848 |
| E207 | LO TEL | Sortie câblo/informatique | Panneau de logement | 2898 | 1256 |
| E207 | LO TEL | Sortie câblo/informatique | Sortie informatique | 4544 | 1842 |
| E207 | LO TV | Prise double | Sortie câblo/informatique | 2953 | 1186 |
| E207 | LO TV | Prise double | Panneau de logement | 3605 | 1226 |
| E207 | LO TV | Prise double | Panneau de logement | 4346 | 1239 |
| E207 | LO TV | Prise double | Plinthe 1000W | 3616 | 1784 |
| E207 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 3335 | 1110 |
| E207 | RWF 1500W | Aéroconvecteur 1500W | Sectionneur | 4546 | 1252 |
| E208 | B 1000W | Plinthe 1000W | Sectionneur | 3782 | 1111 |
| E208 | LO EVAP | Raccordement évaporateur | Panneau de logement | 3181 | 1477 |
| E208 | LO P3000 | Prise double | Sortie informatique | 3682 | 1290 |
| E208 | LO P3000 | Prise double | Prise laveuse | 3251 | 1427 |
| E208 | LO P3000 | Prise double | Prise laveuse | 4319 | 1440 |
| E208 | LO P3000 | Prise double | Prise réfrigérateur | 4030 | 1554 |
| E208 | LO P3000 | Prise double | Panneau de logement | 3486 | 1649 |
| E208 | LO PRISE | Prise double | Plinthe 1000W | 3721 | 1153 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4057 | 1264 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3507 | 1266 |
| E208 | LO PRISE | Prise double | Panneau de logement | 3946 | 1268 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 3518 | 1323 |
| E208 | LO PRISE | Prise double | Prise réfrigérateur | 3545 | 1323 |
| E208 | LO PRISE | Prise double | Prise réfrigérateur | 4024 | 1323 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 4108 | 1323 |
| E208 | LO PRISE | Prise double | Prise comptoir | 3461 | 1326 |
| E208 | LO PRISE | Prise double | Prise comptoir | 4046 | 1326 |
| E208 | LO PRISE | Prise double | Prise réfrigérateur | 3204 | 1341 |
| E208 | LO PRISE | Prise double | Prise laveuse | 3579 | 1341 |
| E208 | LO PRISE | Prise double | Prise laveuse | 3987 | 1344 |
| E208 | LO PRISE | Prise double | Prise comptoir | 4360 | 1347 |
| E208 | LO PRISE | Prise double | Prise comptoir | 3203 | 1372 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4421 | 1403 |
| E208 | LO PRISE | Prise double | Panneau de distribution | 3315 | 1404 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3143 | 1405 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 4360 | 1405 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 3201 | 1420 |
| E208 | LO PRISE | Prise double | Prise réfrigérateur | 4360 | 1429 |
| E208 | LO PRISE | Prise double | Panneau de logement | 4367 | 1477 |
| E208 | LO PRISE | Prise double | Prise comptoir | 3457 | 1554 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 4115 | 1554 |
| E208 | LO PRISE | Prise double | Prise micro-onde | 3504 | 1555 |
| E208 | LO PRISE | Prise double | Prise comptoir | 4058 | 1556 |
| E208 | LO PRISE | Prise double | Prise réfrigérateur | 3526 | 1557 |
| E208 | LO PRISE | Prise double | Raccordement évaporateur | 3182 | 1561 |
| E208 | LO PRISE | Prise double | Prise comptoir | 4040 | 1611 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 3476 | 1614 |
| E208 | LO PRISE | Prise double | Raccordement lave-vaisselle | 4130 | 1615 |
| E208 | LO PRISE | Prise double | Prise laveuse | 3400 | 1635 |
| E208 | LO PRISE | Prise double | Prise laveuse | 4170 | 1645 |
| E208 | LO PRISE | Prise double | Prise demi-commandée | 4229 | 1688 |
| E208 | LO PRISE | Prise double | Aéroconvecteur 2000W | 4476 | 1762 |
| E208 | LO PRISE | Prise double | Prise demi-commandée | 3755 | 1767 |
| E208 | LO PRISE CONTROLÉ | Prise demi-commandée | Prise double | 4353 | 1729 |
| E208 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 4258 | 1822 |
| E208 | LO PRISE CONTROLÉ | Prise demi-commandée | Sectionneur | 3783 | 1825 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4115 | 1260 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4026 | 1264 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3535 | 1266 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 4421 | 1435 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3138 | 1447 |
| E208 | LO PRISE GFI | Prise salle de bain | Prise comptoir | 3445 | 1613 |
| E208 | LO PRISE GFI | Prise salle de bain | Panneau de logement | 4072 | 1649 |
| E208 | LO TEL | Sortie câblo/informatique | Panneau de logement | 3610 | 1268 |
| E208 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3880 | 1287 |
| E208 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3882 | 1626 |
| E208 | LO TEL | Sortie câblo/informatique | Sortie informatique | 3205 | 1628 |
| E208 | LO TEL | Sortie câblo/informatique | Prise demi-commandée | 4397 | 1731 |
| E208 | RWF 2000W | Aéroconvecteur 2000W | Sortie informatique | 4439 | 1781 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3509 | 1386 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4192 | 1386 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4062 | 1398 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3381 | 1406 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3134 | 2993 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3738 | 2994 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3597 | 3012 |
| E302 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3000 | 3040 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3262 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3507 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3629 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3752 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3874 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3996 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4119 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4241 | 1507 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3753 | 2922 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 2881 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3017 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3141 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3263 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3385 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3508 | 2931 |
| E302 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3630 | 2931 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 3387 | 1486 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 4208 | 1492 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 3589 | 1527 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 3589 | 2943 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 3754 | 2948 |
| E302 | exit | Luminaire — à classer | Enseigne sortie | 3012 | 2951 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3506 | 1382 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4184 | 1382 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4060 | 1394 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3379 | 1402 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3131 | 2989 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3735 | 2990 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3595 | 3007 |
| E303 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 2997 | 3036 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3260 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3504 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3627 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3749 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3871 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3994 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4116 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4238 | 1502 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3378 | 1513 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3750 | 2918 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 2879 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3015 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3138 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3260 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3383 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3505 | 2927 |
| E303 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3627 | 2927 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 3384 | 1482 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 4206 | 1488 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 3586 | 1522 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 3587 | 2938 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 3752 | 2944 |
| E303 | exit | Luminaire — à classer | Enseigne sortie | 3010 | 2947 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3495 | 1375 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4179 | 1375 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4049 | 1387 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3368 | 1395 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3120 | 2982 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3724 | 2983 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3584 | 3000 |
| E304 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 2986 | 3029 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3249 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3493 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3616 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3738 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3860 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3983 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4105 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4227 | 1495 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3373 | 1497 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3739 | 2911 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3004 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3127 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3249 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3372 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3494 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3616 | 2919 |
| E304 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 2868 | 2920 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 4195 | 1480 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 3379 | 1481 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 3575 | 1519 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 3576 | 2936 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 3741 | 2936 |
| E304 | exit | Luminaire — à classer | Enseigne sortie | 2999 | 2940 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3504 | 1377 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4187 | 1377 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4057 | 1388 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3376 | 1396 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3129 | 2983 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3733 | 2984 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3592 | 3002 |
| E305 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 2995 | 3030 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3257 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3502 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3624 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3747 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3869 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3991 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4114 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4236 | 1497 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3383 | 1498 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3748 | 2912 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 2876 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3012 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3136 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3258 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3380 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3503 | 2921 |
| E305 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3625 | 2921 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 3381 | 1477 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 4203 | 1482 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 3586 | 1519 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 3584 | 2937 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 3749 | 2938 |
| E305 | exit | Luminaire — à classer | Enseigne sortie | 3007 | 2941 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3500 | 1386 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4178 | 1386 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4054 | 1397 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3373 | 1405 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3128 | 2993 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3729 | 2993 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3589 | 2994 |
| E306 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 2994 | 3039 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3254 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3498 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3621 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3743 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3865 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3988 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4110 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4232 | 1506 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3380 | 1510 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3744 | 2921 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 2873 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3009 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3132 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3254 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3377 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3499 | 2930 |
| E306 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3621 | 2930 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 3378 | 1486 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 4200 | 1491 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 3581 | 1525 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 3746 | 2947 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 3579 | 2950 |
| E306 | exit | Luminaire — à classer | Enseigne sortie | 3004 | 2951 |
| E307 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3508 | 1379 |
| E307 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4187 | 1379 |
| E307 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4062 | 1390 |
| E307 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3381 | 1398 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3262 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3507 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3629 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3751 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3874 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3996 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4118 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 4241 | 1499 |
| E307 | PLAFONNIER | Luminaire — à classer | Luminaire encastré urgence | 3388 | 1500 |
| E307 | exit | Luminaire — à classer | Enseigne sortie | 3386 | 1478 |
| E307 | exit | Luminaire — à classer | Enseigne sortie | 4208 | 1484 |
| E307 | exit | Luminaire — à classer | Enseigne sortie | 3589 | 1519 |
| E308 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3512 | 1383 |
| E308 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4188 | 1387 |
| E308 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 4056 | 1398 |
| E308 | FIXT TYPE UE2 | Luminaire — à classer | Luminaire linéaire applique urgence | 3382 | 1407 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2941 | 1194 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4444 | 1210 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3595 | 1213 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4068 | 1231 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3150 | 1239 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3275 | 1239 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3970 | 1246 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3006 | 1250 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3514 | 1251 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3709 | 1252 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3879 | 1253 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3028 | 1495 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2950 | 1516 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4411 | 1582 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3176 | 1626 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3855 | 1739 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4448 | 1741 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3357 | 1755 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3777 | 1767 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4064 | 1804 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3281 | 1813 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2997 | 2643 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3129 | 2646 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3918 | 2646 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3803 | 2649 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3240 | 2653 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2928 | 2676 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2790 | 2678 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2766 | 2698 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2630 | 2768 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3993 | 2852 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2589 | 2855 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2818 | 2944 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3526 | 3020 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2947 | 3022 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3908 | 3032 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4136 | 3035 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2723 | 3087 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4184 | 3104 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3952 | 3156 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2886 | 3193 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3153 | 3193 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3379 | 3199 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3247 | 3200 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3730 | 3208 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 4171 | 3216 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 3549 | 3238 |
| E401 | AF1-5 | Avertisseur de fumée | Avertisseur fumée/CO | 2817 | 3239 |
| E402 | INT | Avertisseur fumée/CO | Klaxon | 3613 | 2665 |
| E402 | INT | Avertisseur fumée/CO | Résistance fin de ligne | 3299 | 2906 |
| E404 | MA | Module adressable | Relais adressable | 3352 | 2923 |
| E408 | DF2 | Détecteur de fumée de gaine | Résistance fin de ligne | 3727 | 1473 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
