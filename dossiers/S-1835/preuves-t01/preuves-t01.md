# Addenda T-01 — preuves (généré par `analyse_t01.py`)

## Haut-parleurs par feuille, avant / après

| feuille | avant | après | écart |
|---|--:|--:|--:|
| D400 | 0 | 0 | +0 |
| D401 | 0 | 0 | +0 |
| D402 | 0 | 0 | +0 |
| D403 | 0 | 0 | +0 |
| D410 | 23 | 23 | +0 |
| D411 | 27 | 27 | +0 |
| D412 | 3 | 0 | -3 |
| D413 | 13 | 13 | +0 |
| D420 | 41 | 0 | -41 |
| D421 | 36 | 0 | -36 |
| D422 | 9 | 0 | -9 |
| D420_ADD | 0 | 38 | +38 |
| D421_ADD | 0 | 32 | +32 |
| D422_ADD | 0 | 9 | +9 |
| TOTAL | 152 | 142 | -10 |

## Tous les libellés, avant / après

| libellé | avant | après | écart |
|---|--:|--:|--:|
| Alarme existante — à classer | 4 | 4 | +0 |
| Dém. chauffage — à classer | 3 | 3 | +0 |
| Dém. luminaire 1x4 / segment linéaire | 1888 | 1888 | +0 |
| Dém. luminaire 2x2 | 6 | 6 | +0 |
| Dém. luminaire 2x4 | 554 | 554 | +0 |
| Dém. luminaire rond encastré | 85 | 85 | +0 |
| Dém. prise plafond projecteur | 13 | 13 | +0 |
| Dém. éclairage — à classer | 27 | 27 | +0 |
| Détecteur fumée existant — dépose/repose temp. | 192 | 192 | +0 |
| Détecteur sécurité (M) — par autres | 13 | 13 | +0 |
| Haut-parleur classe — par autres | 3 | 3 | +0 |
| Haut-parleur existant — dépose/entreposage | 152 | 142 | -10 |
| Luminaire 24h existant — dépose/repose temp. | 218 | 218 | +0 |
| Prise existante — à classer | 4 | 4 | +0 |
| Repère EAC — existant à conserver | 54 | 54 | +0 |
| Station manuelle existante (F) — à confirmer | 32 | 32 | +0 |
| Éclairage existant carré — à classer | 55 | 55 | +0 |
| Éclairage existant — à classer | 5 | 5 | +0 |
| TOTAL | 3308 | 3298 | -10 |

## Feuilles révisées par T-01 (comparaison vectorielle)

| original → T-01 | décalage (pt) | tracés communs | tracés seulement orig. / T-01 | HP orig. | HP T-01 | identiques | absents de T-01 | nouveaux | tracé fibre (m à 1:100) |
|---|---|--:|---|--:|--:|--:|--:|--:|--:|
| D420 → D420_ADD | 0.0, 0.0 | 81.9% | 4617 / 1771 | 41 | 38 | 38 | 3 | 0 | 47.1 |
| D421 → D421_ADD | 0.0, 0.0 | 86.9% | 4892 / 2020 | 36 | 32 | 32 | 4 | 0 | 55.8 |
| D422 → D422_ADD | 239.7, 0.0 | 94.5% | 2575 / 2337 | 9 | 9 | 9 | 0 | 0 | 12.7 |

Mots ajoutés / retirés par T-01 : voir `comparaison-t01.csv`.

## Haut-parleurs absents des feuilles T-01

| feuille orig. | x | y | vu aussi sur | position sur l'autre feuille | présent sur T-01 | conclusion |
|---|--:|--:|---|---|---|---|
| D420 | 2218.6 | 386.8 | D421 | 788.8, 385.3 | D421_ADD | doublon du chevauchement original, conservé une fois sur D421_ADD |
| D420 | 2083.6 | 1860.9 | D421 | 653.8, 1859.4 | non | retiré du dessin par T-01 (absent des deux feuilles révisées) |
| D420 | 2187.0 | 2055.0 | D421 | 757.2, 2053.5 | D421_ADD | doublon du chevauchement original, conservé une fois sur D421_ADD |
| D421 | 549.6 | 612.4 | D420 | 1979.4, 613.9 | D420_ADD | doublon du chevauchement original, conservé une fois sur D420_ADD |
| D421 | 544.8 | 702.1 | D420 | 1974.6, 703.6 | D420_ADD | doublon du chevauchement original, conservé une fois sur D420_ADD |
| D421 | 545.1 | 1497.7 | D420 | 1974.9, 1499.2 | D420_ADD | doublon du chevauchement original, conservé une fois sur D420_ADD |
| D421 | 653.9 | 1859.5 | D420 | 2083.7, 1861.0 | non | retiré du dessin par T-01 (absent des deux feuilles révisées) |

Appareils distincts retirés du dessin par T-01 : 1 (une ligne par feuille où il figurait). Au recalage original D420/D421 (1429.8, 1.5 pt), les vues T-01 ne partagent qu'une bande de raccord : 3.1% de tracés communs, 0 haut-parleur en double.

## Recouvrement des vues d'un même étage (seuil 10% de tracés communs)

| étage | feuilles | translations testées | meilleure part commune | décalage (pt) | recouvrement | doublons |
|---|---|--:|--:|---|---|--:|
| RDC | D410 / D411 | 617 | 1.5% | 190.9, 60.0 | non | 0 |
| RDC | D410 / D412 | 69 | 1.6% | -207.1, -832.9 | non | 0 |
| RDC | D410 / D413 | 299 | 1.6% | -232.4, -41.5 | non | 0 |
| RDC | D411 / D412 | 79 | 22.3% | -519.0, -903.5 | oui | 3 |
| RDC | D411 / D413 | 351 | 2.2% | -362.0, -176.9 | non | 0 |
| RDC | D412 / D413 | 39 | 1.7% | 170.5, -953.2 | non | 0 |
| ÉTAGE (original) | D420 / D421 | 1471 | 20.8% | 1429.8, 1.5 | oui | 6 |
| ÉTAGE (original) | D420 / D422 | 369 | 1.5% | 268.3, 173.0 | non | 0 |
| ÉTAGE (original) | D421 / D422 | 324 | 2.1% | 203.2, 41.8 | non | 0 |
| ÉTAGE (T-01) | D420_ADD / D421_ADD | 1215 | 3.1% | 520.9, 1.5 | non | 0 |
| ÉTAGE (T-01) | D420_ADD / D422_ADD | 342 | 1.2% | 788.1, 43.3 | non | 0 |
| ÉTAGE (T-01) | D421_ADD / D422_ADD | 288 | 2.0% | 274.7, 41.8 | non | 0 |

## Sous-sol (T-D400 à T-D403)

| feuille | disques noirs Ø 9,5–11,8 pt |
|---|--:|
| D400 | 0 |
| D401 | 0 |
| D402 | 0 |
| D403 | 0 |
