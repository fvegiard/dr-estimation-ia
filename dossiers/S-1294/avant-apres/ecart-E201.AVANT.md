# Écart E201 — relevé visuel IA vs QPL humain (S-1294)

Référence : `reference/S-1294-E201-human-reference.qpl` (GitHub, branche main) — un seul plan « STAM23A - E - Pour construction - 2024-1 »
(échelle 1/16"), 3E et 2E sur la même page. 32 compteurs, 345 marques ; raster humain ≈ 2 × mon raster (calé sur les 24 OS3, résidu ≤ 5 px).
Script : `comparer_reference_E201.py` (appariement glouton, 40 px humain). Les correspondances compteur↔libellé sont déduites de la
géométrie, pas d'une légende : à confirmer.

**Résultat : 263 marques humaines sur 297 (hors types de logements A–G) retrouvées à ≤ 40 px dans mon relevé (88 %).**

| Compteur humain | Humain | Apparié à mon relevé | Mon libellé provisoire |
|---|--:|--:|---|
| SERV  TYPE H | 79 | 72 | Luminaire cercle+support (corridor/hall) — à classer |
| SERV PRISE | 36 | 32 | Appareil mural de porte (cercle à tige) — à classer |
| SERV TYPE E | 12 | 11 | Boîte à diagonale + E (escalier) — à classer |
| SERV EXIT | 10 | 8 | Enseigne de sortie |
| SERV OS3 | 24 | 24 | Capteur OS3 (étiqueté) |
| SERV STATION | 10 | 8 | Carré F |
| SERV KLAXON | 10 | 9 | Carré K (station/module) — à classer |
| SERV TYPE K | 4 | 3 | Carré K (station/module) — à classer |
| SERV DP2 | 6 | 6 | Boîtier DP2 avec batterie — à classer |
| SERV DECT | 25 | 23 | Disque B1-xxx (secours ou détecteur) — à classer |
| SERV TH | 5 | 5 | Carré T (étiqueté) |
| SERV TH R | 2 | 2 | Carré T (étiqueté) |
| SERV DECT GAINE | 2 | 0 | Carré T (étiqueté) |
| SERV MX2 | 8 | 8 | Module Mx2 |
| SW1 | 5 | 4 | SW1 (étiqueté) |
| SERV ISO | 8 | 8 | Module ISO |
| SERV RM | 8 | 8 | Module RM |
| SERV MRA | 6 | 6 | Module MRA |
| SERV C 1250W | 9 | 8 | Hexagone C (chauffage 1250 W ?) — à classer |
| SERV C 750W | 6 | 4 | Hexagone C (chauffage 1250 W ?) — à classer |
| SERV C 1750W | 3 | 3 | Hexagone C (chauffage 1250 W ?) — à classer |
| SERV RELAIS | 6 | 6 | Carré R — à classer |
| SERV DIRECT | 6 | 4 | Bulle B (boîtiers quincaillerie) |
| SERV VE-12 | 1 | 1 | Boîte VE-12 (étiquetée) |
| SERV DEBIT | 6 | 0 | (aucun) |

Sans équivalent humain (mon relevé) :
- Appareil mural de porte (cercle à tige) — à classer : 2 / 34 sans appariement
- Avertisseur rectangle à pointes — à classer : 36 (aucun compteur humain)
- Boîte à diagonale + E (escalier) — à classer : 1 / 12 sans appariement
- Bulle 1 (renvoi) : 2 / 2 sans appariement
- Bulle 2 (renvoi) : 2 / 2 sans appariement
- Bulle A : 6 / 6 sans appariement
- Carré K (station/module) — à classer : 1 / 13 sans appariement
- Carré T (étiqueté) : 4 / 11 sans appariement
- Carré à croix PSU1A-41 (étiqueté) : 2 / 2 sans appariement
- Disque B1-xxx (secours ou détecteur) — à classer : 1 / 24 sans appariement

Humain non apparié (px humain) : [('SERV  TYPE H', 4408, 1596), ('SERV  TYPE H', 4505, 1620), ('SERV  TYPE H', 5333, 1616), ('SERV  TYPE H', 4409, 5345), ('SERV  TYPE H', 4504, 5365), ('SERV  TYPE H', 5336, 5362), ('SERV  TYPE H', 4664, 5220), ('SERV PRISE', 1697, 1342), ('SERV PRISE', 8143, 1345), ('SERV PRISE', 8145, 5096), ('SERV PRISE', 1691, 5083), ('SERV TYPE E', 8213, 5135), ('SERV EXIT', 4870, 1645), ('SERV EXIT', 4868, 5367), ('SERV STATION', 4622, 1672), ('SERV STATION', 4618, 5421), ('SERV KLAXON', 5980, 5316), ('SERV TYPE K', 4617, 5896), ('SERV DECT', 1615, 5082), ('SERV DECT', 8224, 5106), ('SERV DECT GAINE', 4701, 1422), ('SERV DECT GAINE', 4701, 5189), ('SW1', 4706, 5274), ('SERV C 1250W', 4872, 1694), ('SERV C 750W', 8201, 1043), ('SERV C 750W', 1596, 1046), ('SERV DIRECT', 4687, 1457), ('SERV DIRECT', 4688, 5226), ('SERV DEBIT', 1691, 1425), ('SERV DEBIT', 5222, 1396), ('SERV DEBIT', 8146, 1428), ('SERV DEBIT', 8147, 5175), ('SERV DEBIT', 5224, 5148), ('SERV DEBIT', 1694, 5175)]
A..G : {'A': 4, 'B': 8, 'C': 8, 'D': 4, 'E': 18, 'F': 4, 'G': 2} total 48


## Lecture des écarts (hypothèses à confirmer)
- **Avertisseurs (36, mon plus gros poste)** : aucun compteur humain n'y correspond ; l'estimateur ne les compte pas sur cette feuille
  (ou les range ailleurs). Ils ne sont donc pas une quantité de référence : à retirer ou à garder en réserve.
- **Types de logements A–G (48 marques, taille 150)** : l'estimateur marque chaque logement par type (A 4, B 8, C 8, D 4, E 18, F 4, G 2) ; je ne l'ai pas relevé.
- **TYPE H (79 vs mes 72)** : les 7 manquants sont mes « cercles simples » non comptés (R-005, ≈ 3 par étage près du hall) + 1 cercle du local technique 2E.
- **DEBIT (6, aucun chez moi)** : un par cage d'escalier et par étage, aux positions des petites icônes sous Mx2/T que j'avais notées non identifiées (R-006).
- **PRISE (36 vs mes 32 appariés)** : 4 appareils muraux aux extrémités des ailes (x ≈ 1691 et 8145) que j'ai manqués ; 2 de mes 34 sans équivalent (hall).
- **TYPE K (4)** : confirme le 4e « K○ » autour du sas ascenseur du 2E que je soupçonnais (R-004).
- **EXIT 10 vs 8 ; STATION 10 vs 8 ; DIRECT 6 vs 4 ; C 750 W 6 vs 4 ; DECT 25 vs 23 ; SW1 5 vs 4 ; TYPE E 12 vs 11 ; DECT GAINE 2 vs 0** :
  un ou deux oublis chacun, surtout autour de la cage centrale (x humain ≈ 4600–4900), voir la liste ci-dessus.
- Chez moi sans équivalent : bulles A (6), 1 et 2 (4), PSU1A-41 (2) — l'estimateur ne les compte pas (renvois et notes).
- Le relevé humain n'a ni prise duplex ni interrupteur sur cette feuille : mon R-003 était juste.
