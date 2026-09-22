# Écart relevé humain (Dupuis) / relevé IA — S-1857

_Généré le 2026-09-22 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/S-1857-planexpert/S-1857.qpl`
- IA : `/home/claude/releve-auto/runs/S-1857-v3/OUTBOX/S-1857-v3/S-1857-v3-planexpert/S-1857-v3.qpl`
- Dimensions : `/tmp/claude-0/-home-claude/ee0971be-0747-5d2f-962e-a9f568c158d0/scratchpad/dims-v1.txt` ; feuilles : `/home/claude/releve-auto/runs/S-1857-v3/OUTBOX/S-1857-v3/travail/feuilles.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 22 / 11 |
| Feuilles IA (toutes / avec marques) | 22 / 11 |
| Pages humaines marquées appariées / non appariées | 9 / 2 |
| Feuilles IA marquées avec / sans page humaine | 7 / 4 |
| Marques humaines brutes | 1421 |
| … dont exclues (pages en double, versions remplacées) | 126 |
| **Marques humaines retenues** | **1295** |
| **Marques IA** | **1419** |
| **Appariées** (seuil 1.2 % diag.) | **1264** |
| Manquantes côté IA (humain seul) | 31 |
| En trop côté IA (IA seul) | 155 |
| Rappel (appariées / humaines) | 97.6 % |
| Précision (appariées / IA) | 89.1 % |
| … manquantes sur pages humaines non appariées | 5 |
| … en trop sur feuilles IA sans page humaine | 137 |
| Couples « même position, libellé différent » | 105 |
| Lignes (longueurs) humain / IA — non appariées | 0 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 1232 | 63 | 187 | 95.1 % | 86.8 % |
| 1.2 % | 1264 | 31 | 155 | 97.6 % | 89.1 % |
| 2.5 % | 1276 | 19 | 143 | 98.5 % | 89.9 % |

## Anomalies et signalements

- Plan IA « E000 » pointe sur le raster E600.png : la feuille retenue est E600.
- Plan IA « E600 » pointe sur le raster E600_ADD.png : la feuille retenue est E600_ADD.
- Recalage géométrique, document « e400 » : 1 page(s) sûre(s), échelle relative médiane 1.001 × nominal, orientation(s) 0°, translation médiane (-0.0 %, -0.1 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e401 » : 1 page(s) sûre(s), échelle relative médiane 1.034 × nominal, orientation(s) 0°, translation médiane (-0.9 %, -1.9 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e402 » : 1 page(s) sûre(s), échelle relative médiane 1.000 × nominal, orientation(s) 0°, translation médiane (-0.0 %, -0.0 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e403 » : 1 page(s) sûre(s), échelle relative médiane 1.000 × nominal, orientation(s) 0°, translation médiane (-0.0 %, -0.0 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e405 » : 1 page(s) sûre(s), échelle relative médiane 1.000 × nominal, orientation(s) 0°, translation médiane (-0.0 %, 0.0 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e406 » : 1 page(s) sûre(s), échelle relative médiane 1.000 × nominal, orientation(s) 0°, translation médiane (0.0 %, -0.0 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e407 » : 1 page(s) sûre(s), échelle relative médiane 0.974 × nominal, orientation(s) 0°, translation médiane (1.0 %, 1.7 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e408 » : 1 page(s) sûre(s), échelle relative médiane 0.686 × nominal, orientation(s) miroir 180°, translation médiane (11.3 %, 97.9 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Recalage géométrique, document « e600_add » : 1 page(s) sûre(s), échelle relative médiane 0.696 × nominal, orientation(s) 0°, translation médiane (16.0 %, 35.9 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- VERSION REMPLACÉE : « E600 » → feuille E402 : 36/36 marques exclues, référence « E402 » (page entière exclue du décompte (autre document, même feuille IA)).
- VERSION REMPLACÉE : « E408 » → feuille E403 : 90/90 marques exclues, référence « E403 » (page entière exclue du décompte (autre document, même feuille IA)).
- Page « E400 » → E400 (géométrie) : AMBIGU : E401 obtient 0.92.
- Page « E401 » → E401 (géométrie) : AMBIGU : E402 obtient 0.93.
- Page « E403 » → E403 (géométrie) : AMBIGU : E402 obtient 0.96.
- Page « E407 » → E407 (géométrie) : AMBIGU : E402 obtient 0.95.
- Page « E408 » → E403 (géométrie) : AMBIGU : E402 obtient 0.94.
- Page « E600 » → E402 (géométrie) : AMBIGU : E401 obtient 0.92.

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| Prise duplex | Prise duplex 20A (84 %) | 226 | 213 | 13 | 228 | +2 | 35 |
| Luminaire DS1 | Luminaire DS1 (97 %) | 201 | 201 | 0 | 195 | -6 | 6 |
| Luminaire DS0 | Luminaire DS0 (100 %) | 176 | 176 | 0 | 176 | +0 | 0 |
| Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) (74 %) | 98 | 98 | 0 | 73 | -25 | 25 |
| Klaxon | Klaxon alarme (K) (99 %) | 82 | 82 | 0 | 95 | +13 | 1 |
| Bouton-poussoir B | Bouton-poussoir (B) (100 %) | 58 | 58 | 0 | 58 | +0 | 0 |
| Luminaire DR5 | Luminaire DR5 (100 %) | 50 | 50 | 0 | 50 | +0 | 0 |
| Luminaire DR51 | Luminaire DR51 (100 %) | 43 | 43 | 0 | 43 | +0 | 0 |
| Sortie data | Sortie data (81 %) | 41 | 32 | 9 | 41 | +0 | 6 |
| Détecteur occupation Di | Détecteur infrarouge plafond (Di) (100 %) | 40 | 40 | 0 | 40 | +0 | 0 |
| Enseigne de sortie | Enseigne issue 1 face murale tout droit (43 %) | 28 | 28 | 0 | 12 | -16 | 16 |
| Raccord CC équipement | Raccord direct équipement (▲CC) (80 %) | 22 | 20 | 2 | 18 | -4 | 4 |
| Phare double | Phare urgence double mural (100 %) | 21 | 21 | 0 | 21 | +0 | 0 |
| Prise mobilier | Prise 20A dans mobilier (81 %) | 17 | 16 | 1 | 17 | +0 | 3 |
| Accumulateur 36W + enseigne | Accumulateur c/a 2 phares + enseigne (87 %) | 15 | 15 | 0 | 16 | -2 (groupe) | 2 |
| Prise duplex DDFT | Prise DDFT 20A (100 %) | 15 | 14 | 1 | 21 | +6 | 0 |
| Sortie data mobilier | Sortie data dans mobilier (64 %) | 12 | 11 | 1 | 9 | -3 | 4 |
| Luminaire DR52 | Luminaire DR52 service continu (91 %) | 11 | 11 | 0 | 10 | -1 | 1 |
| Phare simple PH1 | Phare urgence simple mural (100 %) | 11 | 11 | 0 | 12 | +0 (groupe) | 0 |
| Luminaire mural DMW1 | Luminaire DMW1 (100 %) | 10 | 10 | 0 | 10 | +0 | 0 |
| Poste manuel | Poste manuel (M) (100 %) | 9 | 9 | 0 | 11 | +2 | 0 |
| Prise micro-onde | Prise 20A micro-onde (MO) (100 %) | 9 | 9 | 0 | 11 | +2 | 0 |
| Luminaire DW4 | Luminaire DW4 (100 %) | 8 | 8 | 0 | 8 | +0 | 0 |
| Accumulateur 36W | Accumulateur c/a 2 phares (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| Interrupteur fin de course Ls | Interrupteur fin de course (Ls) (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| Module de supervision Sx | Module de supervision (Sx) (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| Raccord lave-vaisselle | Raccord lave-vaisselle (LV) (100 %) | 6 | 6 | 0 | 7 | +1 | 0 |
| Indicateur de débit ID | Indicateur de débit (ID) (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| Interrupteur | Interrupteur unipolaire (80 %) | 5 | 5 | 0 | 4 | -1 | 1 |
| Panneau | Panneau de dérivation (100 %) | 5 | 5 | 0 | 6 | +1 | 0 |
| Luminaire DR2 | Luminaire DR2 (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| Raccord sèche-main | Sèche-mains (SM) (100 %) | 4 | 4 | 0 | 6 | +2 | 0 |
| Accumulateur 18W + enseigne | Accumulateur c/a 2 phares + enseigne (100 %) | 3 | 3 | 0 | 16 | -2 (groupe) | 0 |
| Cercle barré fléché — à classer | Gradateur 3 voies (67 %) | 3 | 3 | 0 | 2 | -1 | 1 |
| Détecteur de fumée | Détecteur de fumée (F) (100 %) | 3 | 3 | 0 | 6 | +3 | 0 |
| Luminaire DS4 | Luminaire DS4 (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| Prise DDFT Ei | Prise DDFT intempéries (100 %) | 3 | 3 | 0 | 6 | +3 | 0 |
| Prise cuisinière C | Prise cuisinière 50A (C) (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| Raccord pompe | Raccord pompe (▼) — à classer (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| Avertisseur visuel | — | 2 | 0 | 2 | 0 | — | 0 |
| Bloc d'alimentation Ba | Bloc d'alimentation (Ba) (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| Luminaire DS2 | Luminaire DS2 (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| Luminaire ovale — à classer | Luminaire ovale suspendu — à classer (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| Sectionneur | Sectionneur 600A (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| Transformateur | Transformateur (Xfo) (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| Klaxon Ei | — | 1 | 0 | 1 | 0 | — | 0 |
| Luminaire DW42 | Luminaire DW42 service continu (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Luminaire extérieur — à classer | Cellule photoélectrique (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Mesurage Hydro-Québec | Boîte de mesurage HQ (MHQ) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Module transmission TRA | Module de transmission (TRA) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Panneau d'alarme PAI | Panneau alarme incendie (PAI) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Phare simple — sans étiquette | Phare urgence simple mural (100 %) | 1 | 1 | 0 | 12 | +0 (groupe) | 0 |
| Poste-maître intercom PMI | Poste maître intercom (PMI) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Raccord hotte Ht | Raccord hotte (Ht) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| Raccord équipement — cédule | — | 1 | 0 | 1 | 0 | — | 0 |
| Symbole vert pointillé — à classer | Aéroconvecteur plafond (ACP) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| TS — à classer | Thermostat tension secteur (Ts) (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |

**Libellés humains sans correspondance** (3) : Avertisseur visuel (2), Klaxon Ei (1), Raccord équipement — cédule (1).

**Libellés IA sans correspondance** (37) : Prise duplex 15A (26), Détecteur inoccupation mural (Do) (25), Prise duplex 20A à 1070mm (10), Raccordement ventilo-convecteur (VC) (8), Raccordement évier électrique (7), Luminaire DS1 service continu (6), Raccordement équipement PC (6), Avertisseur sonore/visuel (K) (5), Enseigne issue 1 face plafond tout droit (5), Enseigne issue 1 face murale (flèche) (4), Enseigne issue 2 faces murale (4), Raccordement chauffage (P-P1) (4), Raccordement équipement PREF — à confirmer (4), Avertisseur sonore/visuel intempéries (3), Prise 20A au plancher (3), Accumulateur c/a 2 phares + enseigne (flèche) (2), Borne de recharge VE (2), Coupe-circuit NEMA 3R (CC) (2), Enseigne issue 1 face plafond (flèche) (2), Prise — cercle vide à classer (2), Raccord chauffe-eau (CE) (2), Raccordement lave-vaisselle (cédule) (2), Raccordement serpentin (SE) (2), Raccordement station de pompage SPS-1 (2), Raccordement unité UAT (2), Carré plein « C » — à classer (1), Contacteur d'éclairage CME-01 (1), Détecteur thermique (T) (1), Enseigne issue 2 faces plafond (1), Gradateur 120V (1), Interrupteur c/a lampe témoin (1), Luminaire DR52 (1), Prise sécheuse 30A (S) (1), Raccordement PECD-1 — à confirmer (1), Raccordement ascenseur (1), Raccordement cuisson cuisine 140 (1), Raccordement ventilateur sécheuse (VE-SECH) (1).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| E400 | E400 | géométrie | 1.000 | 77 | 0 | 77 | 77 | 0 | 0 |
| E401 | E401 | géométrie | 1.000 | 248 | 0 | 249 | 248 | 0 | 1 |
| E402 | E402 | géométrie | 1.000 | 317 | 0 | 317 | 317 | 0 | 0 |
| E403 | E403 | géométrie | 1.000 | 161 | 0 | 161 | 161 | 0 | 0 |
| E405 | E405 | géométrie | 1.000 | 91 | 0 | 90 | 90 | 1 | 0 |
| E406 | E406 | géométrie | 1.000 | 216 | 0 | 218 | 216 | 0 | 2 |
| E407 | E407 | géométrie | 0.989 | 180 | 0 | 170 | 155 | 25 | 15 |
| E408 | E403 | géométrie | 0.978 | 90 | 90 | 161 | 0 | 0 | 0 |
| E600 | E402 | géométrie | 0.889 | 36 | 36 | 317 | 0 | 0 | 0 |
| E409 | — | non appariée |  | 4 | 0 |  | 0 | 4 |  |
| E200 | — | non appariée |  | 1 | 0 |  | 0 | 1 |  |
| — | E408 | feuille IA sans page humaine |  | 0 | 0 | 93 | 0 | 0 | 93 |
| — | E409 | feuille IA sans page humaine |  | 0 | 0 | 3 | 0 | 0 | 3 |
| — | E200 | feuille IA sans page humaine |  | 0 | 0 | 4 | 0 | 0 | 4 |
| — | E600_ADD | feuille IA sans page humaine |  | 0 | 0 | 37 | 0 | 0 | 37 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E405 | E405 | Avertisseur visuel | 0.231 | 0.688 | 1315 | 2766 |
| E407 | E407 | Prise duplex | 0.417 | 0.419 | 2383 | 1704 |
| E407 | E407 | Prise duplex | 0.493 | 0.577 | 2804 | 2328 |
| E407 | E407 | Prise duplex | 0.477 | 0.589 | 2716 | 2375 |
| E407 | E407 | Prise duplex | 0.417 | 0.592 | 2383 | 2389 |
| E407 | E407 | Prise duplex | 0.428 | 0.620 | 2441 | 2497 |
| E407 | E407 | Prise duplex | 0.468 | 0.620 | 2667 | 2497 |
| E407 | E407 | Prise duplex | 0.525 | 0.671 | 2983 | 2701 |
| E407 | E407 | Prise duplex | 0.517 | 0.680 | 2943 | 2734 |
| E407 | E407 | Prise duplex | 0.395 | 0.812 | 2256 | 3257 |
| E407 | E407 | Prise duplex | 0.246 | 0.836 | 1423 | 3351 |
| E407 | E407 | Prise duplex | 0.369 | 0.837 | 2113 | 3356 |
| E407 | E407 | Prise duplex | 0.396 | 0.839 | 2265 | 3363 |
| E407 | E407 | Prise duplex | 0.244 | 0.857 | 1415 | 3435 |
| E407 | E407 | Prise duplex DDFT | 0.173 | 0.828 | 1017 | 3320 |
| E407 | E407 | Prise mobilier | 0.437 | 0.563 | 2495 | 2274 |
| E407 | E407 | Sortie data | 0.548 | 0.526 | 3112 | 2126 |
| E407 | E407 | Sortie data | 0.600 | 0.526 | 3403 | 2126 |
| E407 | E407 | Sortie data | 0.541 | 0.651 | 3076 | 2619 |
| E407 | E407 | Sortie data | 0.541 | 0.699 | 3076 | 2809 |
| E407 | E407 | Sortie data | 0.546 | 0.802 | 3105 | 3217 |
| E407 | E407 | Sortie data | 0.476 | 0.810 | 2711 | 3248 |
| E407 | E407 | Sortie data | 0.484 | 0.816 | 2758 | 3273 |
| E407 | E407 | Sortie data | 0.516 | 0.816 | 2934 | 3273 |
| E407 | E407 | Sortie data | 0.385 | 0.857 | 2204 | 3435 |
| E407 | E407 | Sortie data mobilier | 0.437 | 0.573 | 2495 | 2312 |
| E409 | — (page non appariée) | Avertisseur visuel | 0.332 | 0.547 | | |
| E409 | — (page non appariée) | Klaxon Ei | 0.332 | 0.553 | | |
| E409 | — (page non appariée) | Raccord CC équipement | 0.322 | 0.744 | | |
| E409 | — (page non appariée) | Raccord CC équipement | 0.260 | 0.775 | | |
| E200 | — (page non appariée) | Raccord équipement — cédule | 0.609 | 0.671 | | |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E401 | E401 | Contacteur d'éclairage CME-01 | 0.266 | 0.871 | 1513 | 3505 |
| E406 | E406 | Borne de recharge VE | 0.522 | 0.411 | 2973 | 1652 |
| E406 | E406 | Borne de recharge VE | 0.522 | 0.424 | 2973 | 1707 |
| E407 | E407 | Prise DDFT 20A | 0.328 | 0.554 | 1867 | 2227 |
| E407 | E407 | Prise duplex 15A | 0.206 | 0.819 | 1174 | 3294 |
| E407 | E407 | Prise duplex 20A | 0.401 | 0.419 | 2283 | 1687 |
| E407 | E407 | Prise duplex 20A | 0.453 | 0.490 | 2578 | 1970 |
| E407 | E407 | Prise duplex 20A | 0.579 | 0.496 | 3295 | 1995 |
| E407 | E407 | Prise duplex 20A | 0.395 | 0.533 | 2250 | 2145 |
| E407 | E407 | Prise duplex 20A | 0.589 | 0.581 | 3354 | 2338 |
| E407 | E407 | Prise duplex 20A | 0.602 | 0.646 | 3427 | 2599 |
| E407 | E407 | Prise duplex 20A | 0.602 | 0.703 | 3427 | 2827 |
| E407 | E407 | Prise duplex 20A | 0.192 | 0.766 | 1094 | 3080 |
| E407 | E407 | Prise duplex 20A | 0.345 | 0.827 | 1962 | 3325 |
| E407 | E407 | Prise duplex 20A | 0.343 | 0.858 | 1954 | 3450 |
| E407 | E407 | Sortie data | 0.505 | 0.514 | 2874 | 2066 |
| E407 | E407 | Sortie data | 0.347 | 0.858 | 1974 | 3449 |
| E407 | E407 | Sortie data dans mobilier | 0.453 | 0.499 | 2578 | 2005 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel (K) | 0.511 | 0.633 | 2910 | 2547 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel (K) | 0.441 | 0.635 | 2510 | 2553 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel (K) | 0.441 | 0.783 | 2510 | 3149 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel (K) | 0.511 | 0.783 | 2910 | 3149 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel intempéries | 0.232 | 0.455 | 1322 | 1829 |
| E408 | — (aucune page humaine) | Avertisseur sonore/visuel intempéries | 0.561 | 0.545 | 3193 | 2190 |
| E408 | — (aucune page humaine) | Carré plein « C » — à classer | 0.163 | 0.607 | 926 | 2442 |
| E408 | — (aucune page humaine) | Détecteur de fumée (F) | 0.246 | 0.414 | 1403 | 1667 |
| E408 | — (aucune page humaine) | Détecteur de fumée (F) | 0.381 | 0.467 | 2167 | 1880 |
| E408 | — (aucune page humaine) | Détecteur de fumée (F) | 0.381 | 0.787 | 2170 | 3166 |
| E408 | — (aucune page humaine) | Détecteur thermique (T) | 0.381 | 0.419 | 2170 | 1686 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.364 | 0.414 | 2074 | 1667 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.394 | 0.502 | 2246 | 2020 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.327 | 0.515 | 1864 | 2071 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.452 | 0.542 | 2574 | 2179 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.533 | 0.542 | 3034 | 2179 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.219 | 0.544 | 1247 | 2186 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.347 | 0.581 | 1973 | 2335 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.252 | 0.587 | 1437 | 2359 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.241 | 0.596 | 1370 | 2399 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.347 | 0.641 | 1973 | 2579 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.257 | 0.655 | 1465 | 2634 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.312 | 0.655 | 1778 | 2634 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.394 | 0.671 | 2246 | 2700 |
| E408 | — (aucune page humaine) | Klaxon alarme (K) | 0.267 | 0.709 | 1522 | 2851 |
| E408 | — (aucune page humaine) | Panneau de dérivation | 0.238 | 0.660 | 1356 | 2655 |
| E408 | — (aucune page humaine) | Poste manuel (M) | 0.254 | 0.445 | 1448 | 1788 |
| E408 | — (aucune page humaine) | Poste manuel (M) | 0.381 | 0.768 | 2169 | 3087 |
| E408 | — (aucune page humaine) | Prise 20A dans mobilier | 0.265 | 0.526 | 1509 | 2117 |
| E408 | — (aucune page humaine) | Prise 20A dans mobilier | 0.265 | 0.549 | 1510 | 2210 |
| E408 | — (aucune page humaine) | Prise 20A dans mobilier | 0.190 | 0.678 | 1081 | 2726 |
| E408 | — (aucune page humaine) | Prise 20A dans mobilier | 0.207 | 0.678 | 1177 | 2726 |
| E408 | — (aucune page humaine) | Prise 20A micro-onde (MO) | 0.305 | 0.414 | 1734 | 1667 |
| E408 | — (aucune page humaine) | Prise 20A micro-onde (MO) | 0.471 | 0.478 | 2682 | 1921 |
| E408 | — (aucune page humaine) | Prise DDFT 20A | 0.299 | 0.421 | 1701 | 1694 |
| E408 | — (aucune page humaine) | Prise DDFT 20A | 0.372 | 0.430 | 2120 | 1729 |
| E408 | — (aucune page humaine) | Prise DDFT 20A | 0.440 | 0.478 | 2504 | 1921 |
| E408 | — (aucune page humaine) | Prise DDFT 20A | 0.328 | 0.554 | 1867 | 2227 |
| E408 | — (aucune page humaine) | Prise DDFT intempéries | 0.233 | 0.446 | 1326 | 1793 |
| E408 | — (aucune page humaine) | Prise DDFT intempéries | 0.560 | 0.552 | 3188 | 2221 |
| E408 | — (aucune page humaine) | Prise DDFT intempéries | 0.560 | 0.814 | 3188 | 3272 |
| E408 | — (aucune page humaine) | Prise duplex 15A | 0.305 | 0.401 | 1734 | 1613 |
| E408 | — (aucune page humaine) | Prise duplex 15A | 0.405 | 0.543 | 2308 | 2183 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.365 | 0.421 | 2078 | 1695 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.487 | 0.502 | 2775 | 2019 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.401 | 0.503 | 2283 | 2023 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.552 | 0.507 | 3141 | 2039 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.493 | 0.507 | 2807 | 2041 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.185 | 0.522 | 1053 | 2101 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.287 | 0.531 | 1635 | 2134 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.241 | 0.532 | 1373 | 2139 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.194 | 0.545 | 1105 | 2192 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.168 | 0.553 | 956 | 2224 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.187 | 0.553 | 1067 | 2224 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.207 | 0.553 | 1176 | 2224 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.342 | 0.596 | 1945 | 2396 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.355 | 0.640 | 2020 | 2575 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.395 | 0.643 | 2250 | 2585 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.298 | 0.646 | 1697 | 2599 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.299 | 0.654 | 1703 | 2630 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.365 | 0.666 | 2077 | 2678 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.257 | 0.666 | 1466 | 2679 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.240 | 0.677 | 1368 | 2723 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.276 | 0.678 | 1571 | 2727 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.331 | 0.678 | 1887 | 2728 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.202 | 0.700 | 1152 | 2815 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.293 | 0.700 | 1668 | 2815 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.304 | 0.700 | 1729 | 2815 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.227 | 0.708 | 1295 | 2847 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.273 | 0.708 | 1554 | 2847 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.330 | 0.708 | 1879 | 2847 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.354 | 0.741 | 2016 | 2981 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.162 | 0.788 | 922 | 3170 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.354 | 0.798 | 2016 | 3211 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.211 | 0.858 | 1199 | 3450 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.272 | 0.858 | 1547 | 3450 |
| E408 | — (aucune page humaine) | Prise duplex 20A | 0.337 | 0.858 | 1918 | 3450 |
| E408 | — (aucune page humaine) | Prise duplex 20A à 1070mm | 0.448 | 0.543 | 2551 | 2184 |
| E408 | — (aucune page humaine) | Prise — cercle vide à classer | 0.310 | 0.485 | 1767 | 1951 |
| E408 | — (aucune page humaine) | Prise — cercle vide à classer | 0.270 | 0.588 | 1535 | 2364 |
| E408 | — (aucune page humaine) | Raccord lave-vaisselle (LV) | 0.424 | 0.478 | 2416 | 1923 |
| E408 | — (aucune page humaine) | Sortie data | 0.171 | 0.553 | 976 | 2225 |
| E408 | — (aucune page humaine) | Sortie data | 0.191 | 0.553 | 1087 | 2225 |
| E408 | — (aucune page humaine) | Sortie data | 0.210 | 0.553 | 1196 | 2225 |
| E408 | — (aucune page humaine) | Sortie data | 0.265 | 0.556 | 1510 | 2238 |
| E408 | — (aucune page humaine) | Sortie data | 0.365 | 0.671 | 2077 | 2699 |
| E408 | — (aucune page humaine) | Sortie data | 0.194 | 0.678 | 1107 | 2727 |
| E408 | — (aucune page humaine) | Sortie data | 0.211 | 0.678 | 1203 | 2727 |
| E408 | — (aucune page humaine) | Sortie data | 0.297 | 0.700 | 1689 | 2814 |
| E408 | — (aucune page humaine) | Sortie data | 0.307 | 0.700 | 1750 | 2814 |
| E408 | — (aucune page humaine) | Sortie data dans mobilier | 0.265 | 0.533 | 1508 | 2145 |
| E408 | — (aucune page humaine) | Sèche-mains (SM) | 0.328 | 0.524 | 1865 | 2108 |
| E408 | — (aucune page humaine) | Sèche-mains (SM) | 0.328 | 0.533 | 1865 | 2144 |
| E409 | — (aucune page humaine) | Avertisseur sonore/visuel intempéries | 0.332 | 0.553 | 1888 | 2225 |
| E409 | — (aucune page humaine) | Raccord direct équipement (▲CC) | 0.316 | 0.744 | 1802 | 2992 |
| E409 | — (aucune page humaine) | Raccord direct équipement (▲CC) | 0.255 | 0.775 | 1454 | 3118 |
| E200 | — (aucune page humaine) | Raccordement ascenseur | 0.772 | 0.671 | 4394 | 2700 |
| E200 | — (aucune page humaine) | Raccordement serpentin (SE) | 0.609 | 0.671 | 3465 | 2700 |
| E200 | — (aucune page humaine) | Raccordement station de pompage SPS-1 | 0.734 | 0.658 | 4179 | 2645 |
| E200 | — (aucune page humaine) | Raccordement station de pompage SPS-1 | 0.749 | 0.658 | 4262 | 2645 |
| E600_ADD | — (aucune page humaine) | Raccordement PECD-1 — à confirmer | 0.198 | 0.087 | 1127 | 352 |
| E600_ADD | — (aucune page humaine) | Raccordement chauffage (P-P1) | 0.531 | 0.469 | 3026 | 1886 |
| E600_ADD | — (aucune page humaine) | Raccordement chauffage (P-P1) | 0.531 | 0.476 | 3026 | 1915 |
| E600_ADD | — (aucune page humaine) | Raccordement chauffage (P-P1) | 0.531 | 0.483 | 3026 | 1943 |
| E600_ADD | — (aucune page humaine) | Raccordement chauffage (P-P1) | 0.632 | 0.666 | 3596 | 2680 |
| E600_ADD | — (aucune page humaine) | Raccordement cuisson cuisine 140 | 0.632 | 0.661 | 3596 | 2659 |
| E600_ADD | — (aucune page humaine) | Raccordement lave-vaisselle (cédule) | 0.518 | 0.288 | 2950 | 1159 |
| E600_ADD | — (aucune page humaine) | Raccordement lave-vaisselle (cédule) | 0.318 | 0.637 | 1810 | 2561 |
| E600_ADD | — (aucune page humaine) | Raccordement serpentin (SE) | 0.531 | 0.666 | 3026 | 2680 |
| E600_ADD | — (aucune page humaine) | Raccordement unité UAT | 0.198 | 0.584 | 1127 | 2348 |
| E600_ADD | — (aucune page humaine) | Raccordement unité UAT | 0.632 | 0.702 | 3596 | 2826 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilateur sécheuse (VE-SECH) | 0.415 | 0.087 | 2361 | 352 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.518 | 0.137 | 2950 | 551 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.318 | 0.158 | 1810 | 637 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.632 | 0.158 | 3596 | 637 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.098 | 0.165 | 557 | 665 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.318 | 0.173 | 1810 | 694 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.632 | 0.205 | 3596 | 826 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.198 | 0.515 | 1127 | 2070 |
| E600_ADD | — (aucune page humaine) | Raccordement ventilo-convecteur (VC) | 0.098 | 0.529 | 557 | 2127 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.632 | 0.533 | 3596 | 2143 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.531 | 0.540 | 3026 | 2171 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.531 | 0.561 | 3026 | 2257 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.632 | 0.575 | 3596 | 2314 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.531 | 0.582 | 3026 | 2342 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PC | 0.632 | 0.596 | 3596 | 2399 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PREF — à confirmer | 0.531 | 0.604 | 3026 | 2431 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PREF — à confirmer | 0.632 | 0.618 | 3596 | 2488 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PREF — à confirmer | 0.531 | 0.626 | 3026 | 2517 |
| E600_ADD | — (aucune page humaine) | Raccordement équipement PREF — à confirmer | 0.632 | 0.640 | 3596 | 2574 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.632 | 0.087 | 3596 | 348 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.642 | 0.087 | 3653 | 348 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.308 | 0.087 | 1753 | 352 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.308 | 0.094 | 1753 | 380 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.205 | 0.123 | 1165 | 494 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.098 | 0.470 | 557 | 1892 |
| E600_ADD | — (aucune page humaine) | Raccordement évier électrique | 0.108 | 0.470 | 614 | 1892 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| E400 | Accumulateur 36W + enseigne | Accumulateur c/a 2 phares + enseigne | Accumulateur c/a 2 phares + enseigne (flèche) | 2015 | 1630 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2284 | 1800 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2065 | 2285 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1470 | 2387 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2065 | 2454 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1809 | 2458 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1773 | 2460 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1529 | 2692 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1502 | 2888 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1682 | 2888 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1775 | 3058 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1563 | 3134 |
| E400 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1367 | 3263 |
| E400 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 2 faces murale | 2060 | 2934 |
| E400 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face murale (flèche) | 2227 | 2958 |
| E400 | Luminaire DR52 | Luminaire DR52 service continu | Luminaire DR52 | 1411 | 1641 |
| E401 | Accumulateur 36W + enseigne | Accumulateur c/a 2 phares + enseigne | Accumulateur c/a 2 phares + enseigne (flèche) | 2834 | 3111 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1588 | 1659 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1697 | 1670 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2365 | 1755 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2722 | 2489 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1223 | 2766 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2986 | 2794 |
| E401 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2908 | 2977 |
| E401 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond tout droit | 990 | 1917 |
| E401 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond tout droit | 1119 | 1917 |
| E401 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 2 faces plafond | 2118 | 2065 |
| E401 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 2 faces murale | 2242 | 2067 |
| E401 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 2 faces murale | 2863 | 2875 |
| E401 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 2350 | 1853 |
| E401 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 2596 | 1853 |
| E401 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 1054 | 1954 |
| E401 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 2478 | 2745 |
| E402 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1649 | 1714 |
| E402 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1540 | 1719 |
| E402 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2428 | 2794 |
| E402 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2404 | 2908 |
| E402 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 2595 | 2952 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond tout droit | 1879 | 1833 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face murale (flèche) | 1912 | 2041 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face murale (flèche) | 2473 | 2256 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond (flèche) | 3221 | 2290 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face murale (flèche) | 2473 | 2304 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond tout droit | 2516 | 2942 |
| E402 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond (flèche) | 3228 | 3082 |
| E402 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 2398 | 2019 |
| E402 | Luminaire DS1 | Luminaire DS1 | Luminaire DS1 service continu | 2398 | 3077 |
| E403 | Cercle barré fléché — à classer | Gradateur 3 voies | Gradateur 120V | 1468 | 2201 |
| E403 | Détecteur inoccupation Do | Détecteur inoccupation plafond (Do) | Détecteur inoccupation mural (Do) | 1680 | 2641 |
| E403 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 1 face plafond tout droit | 2084 | 1907 |
| E403 | Enseigne de sortie | Enseigne issue 1 face murale tout droit | Enseigne issue 2 faces murale | 2430 | 1917 |
| E403 | Interrupteur | Interrupteur unipolaire | Interrupteur c/a lampe témoin | 2442 | 1812 |
| E405 | Klaxon | Klaxon alarme (K) | Avertisseur sonore/visuel (K) | 1365 | 2755 |
| E405 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 1564 | 2783 |
| E405 | Raccord CC équipement | Raccord direct équipement (▲CC) | Raccord chauffe-eau (CE) | 921 | 3238 |
| E405 | Raccord CC équipement | Raccord direct équipement (▲CC) | Raccord chauffe-eau (CE) | 921 | 3304 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 2304 | 2313 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2930 | 2390 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3004 | 2390 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3066 | 2391 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3125 | 2391 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3214 | 2391 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3329 | 2391 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3445 | 2391 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3330 | 2422 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 2906 | 2542 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2312 | 2614 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2380 | 2615 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2449 | 2615 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2510 | 2615 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2576 | 2615 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2666 | 2615 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 2906 | 2675 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3033 | 2769 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 3269 | 2769 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 1128 | 2778 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 1894 | 2786 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 1865 | 2805 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 1072 | 2874 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 20A à 1070mm | 2300 | 2947 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2536 | 2947 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2588 | 2947 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3072 | 2991 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 3106 | 2999 |
| E406 | Prise duplex | Prise duplex 20A | Prise sécheuse 30A (S) | 3072 | 3037 |
| E406 | Prise duplex | Prise duplex 20A | Prise DDFT 20A | 1510 | 3063 |
| E406 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 1232 | 3287 |
| E406 | Prise mobilier | Prise 20A dans mobilier | Prise 20A au plancher | 983 | 2243 |
| E406 | Prise mobilier | Prise 20A dans mobilier | Prise 20A au plancher | 946 | 3136 |
| E406 | Prise mobilier | Prise 20A dans mobilier | Prise 20A au plancher | 1054 | 3136 |
| E406 | Raccord CC équipement | Raccord direct équipement (▲CC) | Coupe-circuit NEMA 3R (CC) | 3006 | 1637 |
| E406 | Raccord CC équipement | Raccord direct équipement (▲CC) | Coupe-circuit NEMA 3R (CC) | 3006 | 1716 |
| E406 | Sortie data mobilier | Sortie data dans mobilier | Sortie data | 1694 | 2794 |
| E406 | Sortie data mobilier | Sortie data dans mobilier | Sortie data | 1760 | 2794 |
| E406 | Sortie data mobilier | Sortie data dans mobilier | Sortie data | 1037 | 3361 |
| E407 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2772 | 2734 |
| E407 | Prise duplex | Prise duplex 20A | Prise duplex 15A | 2827 | 2734 |
| E407 | Prise duplex | Prise duplex 20A | Prise DDFT 20A | 1174 | 3335 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 3167 | 2081 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 3425 | 2403 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 3427 | 2435 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 2575 | 3226 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 2283 | 3304 |
| E407 | Sortie data | Sortie data | Prise duplex 20A | 3077 | 3306 |
| E407 | Sortie data mobilier | Sortie data dans mobilier | Sortie data | 2467 | 1739 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
