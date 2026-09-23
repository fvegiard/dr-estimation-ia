# Écart relevé humain (Dupuis) / relevé IA — S-1769

_Généré le 2026-09-23 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `dossiers/S-1769/reference/S-1769-Dupuis-PlanExpert.qpl`
- IA : `dossiers/S-1769/planexpert/S-1769.qpl`
- Dimensions : `dossiers/S-1769/reference/dupuis-png-dimensions.txt` ; feuilles : `dossiers/S-1769/reference/feuilles-ia.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 7 / 2 |
| Feuilles IA (toutes / avec marques) | 7 / 5 |
| Pages humaines marquées appariées / non appariées | 2 / 0 |
| Feuilles IA marquées avec / sans page humaine | 2 / 3 |
| Marques humaines brutes | 116 |
| … dont exclues (pages en double, versions remplacées) | 0 |
| **Marques humaines retenues** | **116** |
| **Marques IA** | **141** |
| **Appariées** (seuil 1.2 % diag.) | **113** |
| Manquantes côté IA (humain seul) | 3 |
| En trop côté IA (IA seul) | 28 |
| Rappel (appariées / humaines) | 97.4 % |
| Précision (appariées / IA) | 80.1 % |
| … manquantes sur pages humaines non appariées | 0 |
| … en trop sur feuilles IA sans page humaine | 10 |
| Couples « même position, libellé différent » | 6 |
| Lignes (longueurs) humain / IA — non appariées | 8 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 103 | 13 | 38 | 88.8 % | 73.0 % |
| 1.2 % | 113 | 3 | 28 | 97.4 % | 80.1 % |
| 2.5 % | 115 | 1 | 26 | 99.1 % | 81.6 % |

## Anomalies et signalements

- Plan IA « E201 » pointe sur le raster 250075EPER-p06.png : la feuille retenue est 250075EPER-p06.
- Plan IA « E401 » pointe sur le raster E004.png : la feuille retenue est E004.
- Plan IA « E002 » pointe sur le raster 250075EPER-p02.png : la feuille retenue est 250075EPER-p02.
- Plan IA « E003 » pointe sur le raster 250075EPER-p03.png : la feuille retenue est 250075EPER-p03.
- Plan IA « E004 » pointe sur le raster 250075EPER-p04.png : la feuille retenue est 250075EPER-p04.
- Plan IA « E101 » pointe sur le raster 250075EPER-p05.png : la feuille retenue est 250075EPER-p05.

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| FIXTURE TYPE A | Luminaire A 2x2 30W (100 %) | 18 | 18 | 0 | 18 | +0 | 0 |
| PRISE | Prise double 15A @48po (82 %) | 11 | 11 | 0 | 10 | -2 (groupe) | 2 |
| FIXTURE TYPE B | Luminaire B encastré 6po 18W (100 %) | 8 | 8 | 0 | 8 | +0 | 0 |
| PLINTHE A 1500W | Chauffage type A 1500W (100 %) | 7 | 7 | 0 | 7 | +0 | 0 |
| DÉTECTEUR FUMÉE | Détecteur de fumée (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| FIXTURE TYPE A1 | Luminaire A1 2x2 40W (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| FIXTURE TYPE E | Luminaire E encastré ext. 4po (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| GRADATEUR | Gradateur à glissière (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| INT 1 VOIE | Commande éclairage ($) (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| SERPENTIN | Serpentin électrique SE (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| TRIAC | Relais bas voltage RT (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| FIXTURE TYPE B1 | Luminaire B1 encastré 6po 12W (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| FIXTURE TYPE C | Luminaire C applique ext. (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| KLAXON | Klaxon alarme-incendie (100 %) | 3 | 2 | 1 | 2 | -1 | 0 |
| PRISE 15/20A GFI | Prise 15-20A DDFT @48po (67 %) | 3 | 3 | 0 | 2 | -1 | 1 |
| TETE DOUBLE | Unité urgence UA plafond (67 %) | 3 | 3 | 0 | 2 | -1 | 1 |
| 30A NF WP | Sectionneur 30A sans fusible (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| CONDENSEUR | Raccordement condenseur CD (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| ECHANGEUR AIR | — | 2 | 0 | 2 | 0 | — | 0 |
| EVAPORATEUR | Raccordement unité AC (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| PLINTHE A 900W | Chauffage type A 900W (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| SORTIE TEL | Raccordement échangeur d'air ECH (50 %) | 2 | 2 | 0 | 2 | +0 | 1 |
| TETE SIMPLE | Unité urgence UA mur tête simple (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| THERMOSTAT | Thermostat unipolaire (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| THERMOSTAT PLANCHER CHAUFFANT | Thermostat esclave plancher — à confirmer (50 %) | 2 | 2 | 0 | 1 | -1 | 1 |
| CHAUFFE-EAU | Raccordement chauffe-eau CE-1 (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| ENSEIGNE SORTIE COMBO | Enseigne sortie mur tête double (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| FIXTURE TYPE D | Luminaire D applique ext. (100 %) | 1 | 1 | 0 | 2 | +1 | 0 |
| FIXTURE TYPE F | Luminaire F sous armoire (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| FIXTURE TYPE F1 | Luminaire F1 sous armoire (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| FIXTURE TYPE G | Luminaire G applique toilette (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| PRISE 15/20A | Prise micro-onde 5-20R (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| PRISE GFI | Prise double 15A @48po (100 %) | 1 | 1 | 0 | 10 | -2 (groupe) | 0 |
| RELO FORCE FLOW | Aéroconvecteur existant relocalisé (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| RELO STATION MANUEL | Boîtier protection station manuelle (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |

**Libellés humains sans correspondance** (1) : ECHANGEUR AIR (2).

**Libellés IA sans correspondance** (26) : Démol. luminaire encastré (5), Détecteur de présence — à confirmer (2), Plancher chauffant zone (2), Artère panneau C — à métrer (1), Boîte alimentation porte (BA) (1), Boîte de jonction porte (BJ) (1), Cercle gras — à classer (1), Démol. applique (1), Démol. chauffage — à confirmer (1), Démol. prise (1), Démol. station manuelle (1), Interrupteur 200A F200A (1), Minuterie astronomique (1), Panneau C 225A (1), Prise double 15A (1), Prise extérieure DDFT EI (1), Prise réfrigérateur (1), Raccordement mécanique circ. 22 — à confirmer (1), Raccordement porte électrifiée (1), Relais adressable porte (RA) (1), Remplacement borniers (1), Sonde plancher chauffant (1), Sortie data murale (1), Station manuelle existante relocalisée (1), Thermostat maître plancher (1), Unité urgence UA mur tête double (1).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 25-0075_E_PERM_SOUM_20260507_Signed - 6 | 250075EPER-p06 | nom | 1.000 | 8 | 0 | 8 | 8 | 0 | 0 |
| 25-0075_E_PERM_SOUM_20260507_Signed - 7 | E004 | nom | 0.991 | 108 | 0 | 123 | 105 | 3 | 18 |
| — | 250075EPER-p03 | feuille IA sans page humaine |  | 0 | 0 | 3 | 0 | 0 | 3 |
| — | 250075EPER-p04 | feuille IA sans page humaine |  | 0 | 0 | 3 | 0 | 0 | 3 |
| — | 250075EPER-p05 | feuille IA sans page humaine |  | 0 | 0 | 4 | 0 | 0 | 4 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| 25-0075_E_PERM_SOUM_20260507_Signed - 7 | E004 | ECHANGEUR AIR | 0.492 | 0.312 | 2803 | 1183 |
| 25-0075_E_PERM_SOUM_20260507_Signed - 7 | E004 | ECHANGEUR AIR | 0.521 | 0.318 | 2964 | 1208 |
| 25-0075_E_PERM_SOUM_20260507_Signed - 7 | E004 | KLAXON | 0.248 | 0.268 | 1413 | 1016 |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Cercle gras — à classer | 0.478 | 0.413 | 2720 | 1566 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. applique | 0.221 | 0.653 | 1257 | 2478 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. chauffage — à confirmer | 0.471 | 0.645 | 2682 | 2450 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. luminaire encastré | 0.221 | 0.568 | 1257 | 2155 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. luminaire encastré | 0.224 | 0.624 | 1274 | 2368 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. luminaire encastré | 0.224 | 0.666 | 1274 | 2529 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. luminaire encastré | 0.223 | 0.708 | 1268 | 2689 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. luminaire encastré | 0.221 | 0.772 | 1257 | 2931 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. prise | 0.486 | 0.655 | 2766 | 2485 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Démol. station manuelle | 0.208 | 0.684 | 1184 | 2597 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Luminaire D applique ext. | 0.153 | 0.310 | 870 | 1175 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Panneau C 225A | 0.481 | 0.286 | 2737 | 1085 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Plancher chauffant zone | 0.621 | 0.338 | 3537 | 1283 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Plancher chauffant zone | 0.625 | 0.341 | 3559 | 1296 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Raccordement porte électrifiée | 0.489 | 0.221 | 2786 | 839 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Raccordement échangeur d'air ECH | 0.503 | 0.264 | 2863 | 1002 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Sonde plancher chauffant | 0.547 | 0.235 | 3115 | 892 |
| E004 | 25-0075_E_PERM_SOUM_20260507_Signed - 7 | Station manuelle existante relocalisée | 0.217 | 0.236 | 1237 | 896 |
| 250075EPER-p03 | — (aucune page humaine) | Détecteur de présence — à confirmer | 0.268 | 0.213 | 1525 | 809 |
| 250075EPER-p03 | — (aucune page humaine) | Détecteur de présence — à confirmer | 0.276 | 0.320 | 1569 | 1215 |
| 250075EPER-p03 | — (aucune page humaine) | Minuterie astronomique | 0.296 | 0.248 | 1687 | 943 |
| 250075EPER-p04 | — (aucune page humaine) | Boîte alimentation porte (BA) | 0.449 | 0.437 | 2557 | 1659 |
| 250075EPER-p04 | — (aucune page humaine) | Boîte de jonction porte (BJ) | 0.449 | 0.459 | 2557 | 1744 |
| 250075EPER-p04 | — (aucune page humaine) | Relais adressable porte (RA) | 0.463 | 0.420 | 2634 | 1595 |
| 250075EPER-p05 | — (aucune page humaine) | Artère panneau C — à métrer | 0.767 | 0.673 | 4365 | 2553 |
| 250075EPER-p05 | — (aucune page humaine) | Interrupteur 200A F200A | 0.747 | 0.698 | 4253 | 2649 |
| 250075EPER-p05 | — (aucune page humaine) | Raccordement mécanique circ. 22 — à confirmer | 0.345 | 0.263 | 1964 | 998 |
| 250075EPER-p05 | — (aucune page humaine) | Remplacement borniers | 0.587 | 0.212 | 3344 | 806 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| E004 | PRISE | Prise double 15A @48po | Prise réfrigérateur | 2904 | 736 |
| E004 | PRISE | Prise double 15A @48po | Prise double 15A | 2755 | 1083 |
| E004 | PRISE 15/20A GFI | Prise 15-20A DDFT @48po | Prise extérieure DDFT EI | 2896 | 690 |
| E004 | SORTIE TEL | Raccordement échangeur d'air ECH | Sortie data murale | 2922 | 998 |
| E004 | TETE DOUBLE | Unité urgence UA plafond | Unité urgence UA mur tête double | 1360 | 778 |
| E004 | THERMOSTAT PLANCHER CHAUFFANT | Thermostat esclave plancher — à confirmer | Thermostat maître plancher | 3155 | 892 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
