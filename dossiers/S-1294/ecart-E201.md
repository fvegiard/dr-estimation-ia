# Écart E201 — relevé visuel corrigé vs QPL humain (S-1294)

Comparaison relevé visuel E201 ↔ QPL humain (jamais modifié). Méthode explicite :
1. Repère : humain = 2 × mon raster − (11, 15) px (calé sur les 24 OS3, résidu ≤ 5 px).
2. Appareils : chaque compteur humain est relié à un ou plusieurs de mes libellés (table CORR, déduite de la géométrie, à confirmer).
   Toutes les paires (marque humaine, marque IA) de classes compatibles à ≤ 40 px humain sont triées par distance et appariées
   une à une (chaque marque sert une seule fois). Rappel = marques humaines appariées / marques humaines ; précision = idem côté IA.
3. Repères de logements A–G : séparés, appariés par type identique à ≤ 150 px humain ; non mélangés aux appareils.
4. Exclus de la comparaison : bulles A, 1, 2 (annotations) et les 36 avertisseurs (retirés, sans équivalent humain).

**Appareils** : rappel 295/297 = 99.3 % ; précision 295/298 = 99.0 % (tolérance 40 px humain, appariement un-à-un par distance croissante).

| Compteur humain | Humain | Apparié | Mes libellés rattachés |
|---|--:|--:|---|
| SERV  TYPE H | 79 | 79 | Luminaire cercle+support, Cercle à point |
| SERV PRISE | 36 | 36 | Appareil mural |
| SERV DECT GAINE | 2 | 2 | Appareil mural |
| SERV TYPE E | 12 | 12 | Boîte à diagonale |
| SERV EXIT | 10 | 10 | Enseigne de sortie |
| SERV OS3 | 24 | 24 | Capteur OS3 |
| SERV STATION | 10 | 10 | Carré F |
| SERV KLAXON | 10 | 10 | Carré K |
| SERV TYPE K | 4 | 4 | Symbole K○ |
| SERV DP2 | 6 | 6 | Boîtier DP2 |
| SERV DECT | 25 | 25 | Disque B1 |
| SERV TH | 5 | 5 | Carré T |
| SERV TH R | 2 | 2 | Carré T |
| SERV MX2 | 8 | 8 | Module Mx2 |
| SW1 | 5 | 5 | SW1, Icône ≈ |
| SERV ISO | 8 | 8 | Module ISO |
| SERV RM | 8 | 8 | Module RM |
| SERV MRA | 6 | 6 | Module MRA |
| SERV C 1250W | 9 | 8 | Hexagone C |
| SERV C 750W | 6 | 5 | Hexagone C |
| SERV C 1750W | 3 | 3 | Hexagone C |
| SERV RELAIS | 6 | 6 | Carré R |
| SERV DIRECT | 6 | 6 | Bulle B, Carré à croix |
| SERV VE-12 | 1 | 1 | Boîte VE-12 |
| SERV DEBIT | 6 | 6 | Icône sous Mx2 |

Humain non apparié (px humain) : [('SERV C 1250W', 4872, 1694), ('SERV C 750W', 1596, 1046)]

Mes appareils sans appariement : Counter({'Carré T (étiqueté)': 2, 'Disque B1-xxx (secours ou détecteur) — à classer': 1})

**Repères de logements A–G (séparés)** : 48/48 appariés par type identique à ≤ 150 px humain ; types par étage lus sur le plan : {'A': 4, 'B': 8, 'C': 8, 'D': 4, 'E': 18, 'F': 4, 'G': 2}.
