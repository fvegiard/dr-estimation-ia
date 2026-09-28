# Écart relevé humain (Dupuis) / relevé IA — S-1715

_Généré le 2026-09-24 par `src.validation.compare_qpl` — comparaison déterministe marque par marque ; aucun chiffre saisi à la main._

- Humain : `dossiers/S-1715/reference/S-1715-Dupuis-PlanExpert.qpl`
- IA : `dossiers/S-1715/planexpert/S-1715.qpl`
- Dimensions : `dossiers/S-1715/reference/dupuis-png-dimensions.txt` ; feuilles : `dossiers/S-1715/reference/feuilles-ia.csv`

## Résumé

| Indicateur | Valeur |
|---|---:|
| Pages humaines (toutes / avec marques) | 29 / 6 |
| Feuilles IA (toutes / avec marques) | 21 / 6 |
| Pages humaines marquées appariées / non appariées | 6 / 0 |
| Feuilles IA marquées avec / sans page humaine | 5 / 1 |
| Marques humaines brutes | 401 |
| … dont exclues (pages en double, versions remplacées) | 0 |
| **Marques humaines retenues** | **401** |
| **Marques IA** | **359** |
| **Appariées** (seuil 1.2 % diag.) | **313** |
| Manquantes côté IA (humain seul) | 88 |
| En trop côté IA (IA seul) | 46 |
| Rappel (appariées / humaines) | 78.1 % |
| Précision (appariées / IA) | 87.2 % |
| … manquantes sur pages humaines non appariées | 0 |
| … en trop sur feuilles IA sans page humaine | 4 |
| Couples « même position, libellé différent » | 42 |
| Lignes (longueurs) humain / IA — non appariées | 34 / 0 |

## Sensibilité au seuil d'appariement des marques

| Seuil (% diagonale IA) | Appariées | Manquantes IA | En trop IA | Rappel | Précision |
|---:|---:|---:|---:|---:|---:|
| 0.6 % | 296 | 105 | 63 | 73.8 % | 82.5 % |
| 1.2 % | 313 | 88 | 46 | 78.1 % | 87.2 % |
| 2.5 % | 324 | 77 | 35 | 80.8 % | 90.3 % |

## Anomalies et signalements

- Plan IA « E201 » pointe sur le raster E201_ADD.png : la feuille retenue est E201_ADD.
- Plan IA « E301 » pointe sur le raster E301_ADD.png : la feuille retenue est E301_ADD.
- Plan IA « E001_2 » pointe sur le raster E001.png : la feuille retenue est E001.
- Plan IA « E001 » pointe sur le raster E001_ADD.png : la feuille retenue est E001_ADD.
- Plan IA « E002_3 » pointe sur le raster E002.png : la feuille retenue est E002.
- Plan IA « E002 » pointe sur le raster E002_ADD.png : la feuille retenue est E002_ADD.
- Plan IA « E002_2 » pointe sur le raster E002_ADD_2.png : la feuille retenue est E002_ADD_2.
- Plan IA « E003 » pointe sur le raster E003_ADD.png : la feuille retenue est E003_ADD.
- Plan IA « E101_3 » pointe sur le raster E101.png : la feuille retenue est E101.
- Plan IA « E101 » pointe sur le raster E101_ADD.png : la feuille retenue est E101_ADD.
- Plan IA « E101_2 » pointe sur le raster E101_ADD_2.png : la feuille retenue est E101_ADD_2.
- Plan IA « E201_3 » pointe sur le raster E201.png : la feuille retenue est E201.
- Plan IA « E201_2 » pointe sur le raster E201_ADD_2.png : la feuille retenue est E201_ADD_2.
- Plan IA « E301_3 » pointe sur le raster E301.png : la feuille retenue est E301.
- Plan IA « E301_2 » pointe sur le raster E301_ADD_2.png : la feuille retenue est E301_ADD_2.
- Recalage géométrique, document « electrique_plans pour soumission » : 2 page(s) sûre(s), échelle relative médiane 1.002 × nominal, orientation(s) 0°, translation médiane (0.6 %, -0.6 %) du raster IA — imposées à toutes les pages du document (± 5 % d'échelle, ± 3 % de diagonale).
- Page « Électrique_Plans pour soumission - 4 » → E102 (nom) : recalage faible (identité 0.18) : aucune autre feuille IA ne dépasse 0.8 ; appariement par nom conservé.
- Page « Électrique_Plans pour soumission - 5 » → E201_ADD (géométrie) : le nom désignait E201 (score identité 0.00) ; la géométrie désigne E201_ADD.
- Page « Électrique_Plans pour soumission - 6 » → E301_ADD (géométrie) : le nom désignait E301 (score identité 0.00) ; la géométrie désigne E301_ADD ; AMBIGU : E201_ADD obtient 0.99.
- Page « Électrique_Addenda ELE-001_Plans - 3 » → E201_ADD (géométrie) : le nom désignait E201_ADD_2 (score identité 0.00) ; la géométrie désigne E201_ADD ; AMBIGU : E301_ADD obtient 1.00.

## Correspondance des libellés et décompte par libellé humain

Libellé IA = libellé majoritaire parmi les marques IA appariées aux marques de ce libellé humain (proportion entre parenthèses). « IA total » = toutes les marques IA de ce libellé ; si plusieurs libellés humains pointent vers le même libellé IA, l'écart est calculé sur le groupe.

| Libellé humain | Libellé IA (part) | Humain | Appariées | Manquantes IA | IA total | Écart groupe | Même pos., autre libellé |
|---|---|---:|---:|---:|---:|---:|---:|
| Compteur J HOOCK | Barre MALT télécom (note 7) (100 %) | 45 | 1 | 44 | 1 | -44 | 0 |
| FIXT TYPE R1 | Luminaire suspendu R1 (100 %) | 30 | 30 | 0 | 30 | +0 | 0 |
| PRISE | Prise double 15A (42 %) | 19 | 19 | 0 | 8 | -11 | 11 |
| RSP-C-347-Z1 | Contrôleur WaveLinx RSP-C-347-Z1 (100 %) | 19 | 19 | 0 | 19 | +0 | 0 |
| fixt type l3 | Luminaire L3 (71 %) | 14 | 14 | 0 | 10 | -4 | 4 |
| DETECTEUR FUMÉ | Détecteur de fumée (75 %) | 12 | 12 | 0 | 10 | -3 (groupe) | 3 |
| BG | Boîte de groupe sécurité BG (100 %) | 11 | 11 | 0 | 11 | +0 | 0 |
| DECT 360 | Détecteur de présence 360° (100 %) | 11 | 11 | 0 | 11 | +0 | 0 |
| PORTE | Porte contrôlée (100 %) | 11 | 11 | 0 | 11 | +0 | 0 |
| OSC-C-P | — | 10 | 0 | 10 | 0 | — | 0 |
| fixt type a1 | Luminaire A1 (100 %) | 10 | 10 | 0 | 10 | +0 | 0 |
| fixt type l4 | Luminaire L4 (80 %) | 10 | 10 | 0 | 8 | -2 | 2 |
| INT 1 VOIE | Interrupteur basse tension (62 %) | 9 | 8 | 1 | 7 | -9 (groupe) | 3 |
| RELAIS | Relais triac RT (100 %) | 9 | 9 | 0 | 9 | +0 | 0 |
| FIXT TYPE P1 | Projecteur P1 (100 %) | 8 | 8 | 0 | 8 | +0 | 0 |
| HP | Haut-parleur — fourni par autres (86 %) | 7 | 7 | 0 | 6 | -1 | 1 |
| SERPENTIN | Raccordement serpentin SE (80 %) | 7 | 5 | 2 | 7 | -1 (groupe) | 1 |
| TEL | Sortie télécom (note) (29 %) | 7 | 7 | 0 | 2 | -5 | 5 |
| TETE DOUBLE | Tête d'éclairage double (86 %) | 7 | 7 | 0 | 7 | +0 | 1 |
| FIXT TYPE R3 | Luminaire R3 (100 %) | 6 | 6 | 0 | 6 | +0 | 0 |
| GFI | Prise DDFT (83 %) | 6 | 6 | 0 | 5 | -1 | 1 |
| SORTIE VIDEOSURVEILLANCE | Sortie télécom VS (100 %) | 6 | 6 | 0 | 8 | +2 | 0 |
| B500W | Plinthe B5 (67 %) | 5 | 3 | 2 | 5 | +0 | 1 |
| CL1 | Clavier d'intrusion CLI (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| DETECT MOUV | Détecteur de mouvement (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| ENSEIGNE SORTIE | Indicateur d'issue Z1 (mur) — à confirmer (80 %) | 5 | 5 | 0 | 4 | -1 | 1 |
| FIXT TYPE M1 | Luminaire mural M1 (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| HPEXT | — | 5 | 0 | 5 | 0 | — | 0 |
| STATION MANUEL | Poste manuel (100 %) | 5 | 5 | 0 | 5 | +0 | 0 |
| WST-C-3D | — | 5 | 0 | 5 | 0 | — | 0 |
| FIXT TYPE R2 | Interrupteur basse tension (25 %) | 4 | 4 | 0 | 7 | -9 (groupe) | 3 |
| INT 3 VOIE | Poste BT double (a/b) (67 %) | 4 | 3 | 1 | 3 | -1 | 1 |
| INT GR | Gradateur basse tension (100 %) | 4 | 4 | 0 | 4 | +0 | 0 |
| INT WST-C-1 | — | 4 | 0 | 4 | 0 | — | 0 |
| A1500W | Aérotherme mural A15 (100 %) | 3 | 2 | 1 | 3 | +0 | 0 |
| CHAUFFE-EAU | Raccordement ventilateur VE (100 %) | 3 | 1 | 2 | 4 | +0 (groupe) | 0 |
| FIXT  TYPE L2 | Luminaire L2 (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| GFI WP | Prise DDFT intempéries (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| INT WST-C-3 | — | 3 | 0 | 3 | 0 | — | 0 |
| PRISE 15/20A | Prise 15/20A (5-20R) (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| SORTIE CONTROL BATIMENT | Sortie télécom CB (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| SÉCHOIRE | Sèche-mains (100 %) | 3 | 3 | 0 | 3 | +0 | 0 |
| TETE SIMPLE | Interrupteur basse tension (33 %) | 3 | 3 | 0 | 7 | -9 (groupe) | 2 |
| 3 | — | 2 | 0 | 2 | 0 | — | 0 |
| B1250W | Plinthe B12 (50 %) | 2 | 2 | 0 | 2 | +0 | 1 |
| FIXT TYPE L1 | Luminaire L1 (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| KLAXON | Klaxon alarme incendie (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| LAMPADAIRE D1 | Lampadaire D1 (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| MOTEUR 1 HP 120V | Raccordement VA (50 %) | 2 | 2 | 0 | 2 | -1 (groupe) | 1 |
| PRISE USB | Prise double USB (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| RA | Relais adressable RA (100 %) | 2 | 2 | 0 | 2 | +0 | 0 |
| VIDEO | — | 2 | 0 | 2 | 0 | — | 0 |
| 2510 | Interrupteur unipolaire (100 %) | 1 | 1 | 0 | 2 | +1 | 0 |
| B1000W | Plinthe B10 (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| B1500W | Raccordement VC (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| B2500W | — | 1 | 0 | 1 | 0 | — | 0 |
| BARRE MISE A LA TERRE | — | 1 | 0 | 1 | 0 | — | 0 |
| BATTERIE UNIT 2T | Accumulateur AUBX (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| BOITIER CAMLOCK | Boîtier Camlock 200A (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| CAB | Cabinet mural télécom — fourni par autres (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| CONDENSEUR | Raccordement COND (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| CONTROL VOLUME | Sortie contrôle de volume (100 %) | 1 | 1 | 0 | 2 | +1 | 0 |
| INT WST-C-5D | — | 1 | 0 | 1 | 0 | — | 0 |
| MOTEUR .25HP 120V | Prise au-dessus du comptoir (100 %) | 1 | 1 | 0 | 6 | +5 | 0 |
| MOTEUR .5 HP 120V | Raccordement DEV (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| MOTEUR ECH | Raccordement ECH (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| MOTEUR PERC | Raccordement PECR (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| MOTEUR VA-2 | Raccordement VA (100 %) | 1 | 1 | 0 | 2 | -1 (groupe) | 0 |
| MOTEUR VC | Raccordement serpentin SE (100 %) | 1 | 1 | 0 | 7 | -1 (groupe) | 0 |
| MOTEUR VE-1 | Raccordement ventilateur VE (100 %) | 1 | 1 | 0 | 4 | +0 (groupe) | 0 |
| MOTEUR VE-3 | Transformateur RC-TRNO-600 (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| P.R | Détecteur de fumée (100 %) | 1 | 1 | 0 | 10 | -3 (groupe) | 0 |
| PCA | Panneau de contrôle d'accès PCA (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| PDI | Panneau de détection d'intrusion PDI (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| SORTIE MICROPHONE | Sortie microphone (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| STROB | Klaxon + stroboscope (100 %) | 1 | 1 | 0 | 1 | +0 | 0 |
| T1500W | Raccordement chauffe-eau CE (36 kW) (100 %) | 1 | 1 | 0 | 3 | +2 | 0 |
| T4000W | — | 1 | 0 | 1 | 0 | — | 0 |

**Libellés humains sans correspondance** (11) : OSC-C-P (10), HPEXT (5), WST-C-3D (5), INT WST-C-1 (4), INT WST-C-3 (3), 3 (2), VIDEO (2), B2500W (1), BARRE MISE A LA TERRE (1), INT WST-C-5D (1), T4000W (1).

**Libellés IA sans correspondance** (35) : Terminaison ACC-C-TP (12), Luminaire L3A (4), Luminaire R2 (4), Prise au plafond (4), Sortie télécom WF (3), Tête d'éclairage simple (3), Concentrateur WAH-C-POE-ID (2), Détecteur de fumée de conduit (note 2) (2), Interrupteur de sûreté 600A (2), Luminaire L4A (2), Puits de tirage (2), Raccordement régulation (2), Sortie télécom D (2), Armoire de relais BT (P.R.) (1), Aérotherme plafond T15 (1), Aérotherme plafond T4 (1), Barre de mise à la terre (1), Boîtier borne de recharge future (1), Cabinet de mesurage HQ (1), Commutateur PoE GS308PP (1), Contrôleur de zone WAC2-POE (1), Indicateur d'issue Z2 (plafond) — à confirmer (1), Interrupteur de sûreté 400A SF (réfrigération) (1), Panneau RC-PDNO-600 (1), Panneau RC-PSNO-200 (1), Panneau d'alarme incendie (PAI) (1), Panneau de contrôle P1 (note 1) (1), Plinthe B15 (1), Plinthe B25 (1), Poteau client — fourni par autres (1), Prise DDFT fontaine réfrigérée (1), Prise hauteur spéciale (1), Raccordement RCFFM — à confirmer (1), Raccordement réfrigération de la glace (1), Sortie télécom CA (1).

## Par page

| Page humaine | Feuille IA | Méthode | Score | Humain | Doublons | IA feuille | Appariées | Manquantes IA | En trop IA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Électrique_Plans pour soumission - 4 | E102 | nom | 0.182 | 11 | 0 | 6 | 2 | 9 | 4 |
| Électrique_Plans pour soumission - 5 | E201_ADD | géométrie | 1.000 | 154 | 0 | 160 | 152 | 2 | 2 |
| Électrique_Plans pour soumission - 6 | E301_ADD | géométrie | 1.000 | 82 | 0 | 90 | 73 | 9 | 17 |
| Électrique_Plans pour soumission - 11 | T201 | nom | 0.943 | 106 | 0 | 64 | 61 | 45 | 3 |
| Électrique_Addenda ELE-001_Plans - 3 | E201_ADD | géométrie | 1.000 | 6 | 0 | 160 | 6 | 0 | 2 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | nom | 0.452 | 42 | 0 | 35 | 19 | 23 | 16 |
| ELectrique_Addenda ELE-002_Plans - 5 | E201_ADD | nom |  | 0 | 0 | 160 | 0 | 0 | 2 |
| — | E002_ADD | feuille IA sans page humaine |  | 0 | 0 | 4 | 0 | 0 | 4 |

Les transformations de recalage (orientation, échelles, translation) sont dans `pages.csv`.

## Marques manquantes côté IA (humain seul)

| Page humaine | Feuille IA | Libellé humain | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| Électrique_Plans pour soumission - 4 | E102 | 3 | 0.412 | 0.446 | 2349 | 1796 |
| Électrique_Plans pour soumission - 4 | E102 | 3 | 0.470 | 0.518 | 2675 | 2085 |
| Électrique_Plans pour soumission - 4 | E102 | HPEXT | 0.391 | 0.448 | 2224 | 1805 |
| Électrique_Plans pour soumission - 4 | E102 | HPEXT | 0.334 | 0.545 | 1900 | 2195 |
| Électrique_Plans pour soumission - 4 | E102 | HPEXT | 0.469 | 0.553 | 2672 | 2228 |
| Électrique_Plans pour soumission - 4 | E102 | HPEXT | 0.334 | 0.729 | 1900 | 2935 |
| Électrique_Plans pour soumission - 4 | E102 | HPEXT | 0.418 | 0.827 | 2381 | 3330 |
| Électrique_Plans pour soumission - 4 | E102 | VIDEO | 0.412 | 0.828 | 2346 | 3333 |
| Électrique_Plans pour soumission - 4 | E102 | VIDEO | 0.441 | 0.828 | 2511 | 3335 |
| Électrique_Plans pour soumission - 5 | E201_ADD | INT 1 VOIE | 0.660 | 0.326 | 3756 | 1305 |
| Électrique_Plans pour soumission - 5 | E201_ADD | INT 3 VOIE | 0.597 | 0.324 | 3394 | 1293 |
| Électrique_Plans pour soumission - 6 | E301_ADD | A1500W | 0.539 | 0.339 | 3071 | 1367 |
| Électrique_Plans pour soumission - 6 | E301_ADD | B2500W | 0.553 | 0.340 | 3153 | 1374 |
| Électrique_Plans pour soumission - 6 | E301_ADD | B500W | 0.540 | 0.216 | 3079 | 857 |
| Électrique_Plans pour soumission - 6 | E301_ADD | B500W | 0.557 | 0.216 | 3172 | 859 |
| Électrique_Plans pour soumission - 6 | E301_ADD | CHAUFFE-EAU | 0.653 | 0.220 | 3715 | 873 |
| Électrique_Plans pour soumission - 6 | E301_ADD | CHAUFFE-EAU | 0.652 | 0.231 | 3713 | 920 |
| Électrique_Plans pour soumission - 6 | E301_ADD | SERPENTIN | 0.508 | 0.296 | 2896 | 1190 |
| Électrique_Plans pour soumission - 6 | E301_ADD | SERPENTIN | 0.506 | 0.322 | 2886 | 1299 |
| Électrique_Plans pour soumission - 6 | E301_ADD | T4000W | 0.712 | 0.332 | 4053 | 1339 |
| Électrique_Plans pour soumission - 11 | T201 | BARRE MISE A LA TERRE | 0.605 | 0.282 | 3442 | 1138 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.621 | 0.252 | 3533 | 1021 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.632 | 0.252 | 3594 | 1021 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.610 | 0.253 | 3472 | 1022 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.641 | 0.253 | 3644 | 1022 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.607 | 0.258 | 3451 | 1043 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.522 | 0.267 | 2972 | 1079 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.551 | 0.278 | 3138 | 1121 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.592 | 0.278 | 3370 | 1122 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.562 | 0.279 | 3195 | 1125 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.573 | 0.279 | 3259 | 1125 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.582 | 0.279 | 3310 | 1126 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.522 | 0.281 | 2969 | 1135 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.541 | 0.284 | 3080 | 1145 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.521 | 0.286 | 2963 | 1152 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.531 | 0.286 | 3024 | 1156 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.602 | 0.292 | 3422 | 1176 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.517 | 0.297 | 2941 | 1197 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.541 | 0.299 | 3080 | 1204 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.602 | 0.306 | 3425 | 1235 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.516 | 0.309 | 2936 | 1247 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.541 | 0.314 | 3078 | 1265 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.603 | 0.320 | 3429 | 1287 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.517 | 0.324 | 2941 | 1306 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.541 | 0.328 | 3078 | 1318 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.550 | 0.330 | 3129 | 1329 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.603 | 0.333 | 3428 | 1341 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.615 | 0.338 | 3500 | 1358 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.635 | 0.338 | 3609 | 1358 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.645 | 0.338 | 3668 | 1358 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.662 | 0.338 | 3764 | 1358 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.671 | 0.338 | 3816 | 1358 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.605 | 0.338 | 3439 | 1359 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.625 | 0.338 | 3552 | 1359 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.682 | 0.338 | 3876 | 1359 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.517 | 0.339 | 2943 | 1362 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.692 | 0.339 | 3936 | 1362 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.549 | 0.343 | 3126 | 1380 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.696 | 0.344 | 3957 | 1383 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.657 | 0.345 | 3738 | 1387 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.517 | 0.352 | 2941 | 1414 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.549 | 0.358 | 3124 | 1438 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.656 | 0.358 | 3732 | 1438 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.696 | 0.358 | 3958 | 1438 |
| Électrique_Plans pour soumission - 11 | T201 | Compteur J HOOCK | 0.555 | 0.359 | 3156 | 1443 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-1 | 0.566 | 0.547 | 3279 | 2132 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-1 | 0.686 | 0.573 | 3961 | 2234 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-1 | 0.566 | 0.674 | 3277 | 2643 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-1 | 0.711 | 0.700 | 4103 | 2746 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-3 | 0.167 | 0.291 | 1007 | 1103 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-3 | 0.312 | 0.292 | 1833 | 1106 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-3 | 0.167 | 0.419 | 1007 | 1617 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | INT WST-C-5D | 0.311 | 0.675 | 1824 | 2644 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.205 | 0.306 | 1220 | 1164 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.566 | 0.308 | 3280 | 1170 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.717 | 0.335 | 4139 | 1278 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.204 | 0.433 | 1217 | 1674 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.566 | 0.434 | 3275 | 1676 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.239 | 0.434 | 1413 | 1678 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.782 | 0.460 | 4507 | 1782 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.753 | 0.461 | 4341 | 1785 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.808 | 0.463 | 4656 | 1792 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | OSC-C-P | 0.684 | 0.715 | 3951 | 2807 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | WST-C-3D | 0.592 | 0.291 | 3428 | 1103 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | WST-C-3D | 0.744 | 0.318 | 4294 | 1212 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | WST-C-3D | 0.591 | 0.419 | 3422 | 1617 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | WST-C-3D | 0.843 | 0.446 | 4856 | 1724 |
| ELectrique_Addenda ELE-002_Plans - 3 | E003_ADD | WST-C-3D | 0.715 | 0.446 | 4127 | 1725 |

## Marques en trop côté IA (IA seul)

| Feuille IA | Page(s) humaine(s) | Libellé IA | x_norm | y_norm | x px IA | y px IA |
|---|---|---|---:|---:|---:|---:|
| E102 | Électrique_Plans pour soumission - 4 | Boîtier borne de recharge future | 0.519 | 0.585 | 2955 | 2357 |
| E102 | Électrique_Plans pour soumission - 4 | Poteau client — fourni par autres | 0.181 | 0.201 | 1033 | 808 |
| E102 | Électrique_Plans pour soumission - 4 | Puits de tirage | 0.331 | 0.425 | 1886 | 1712 |
| E102 | Électrique_Plans pour soumission - 4 | Puits de tirage | 0.568 | 0.440 | 3232 | 1774 |
| E201_ADD | Électrique_Plans pour soumission - 5 + Électrique_Addenda ELE-001_Plans - 3 | Interrupteur unipolaire | 0.539 | 0.335 | 3067 | 1350 |
| E201_ADD | Électrique_Plans pour soumission - 5 + Électrique_Addenda ELE-001_Plans - 3 | Panneau de contrôle P1 (note 1) | 0.510 | 0.335 | 2905 | 1349 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Aérotherme mural A15 | 0.537 | 0.361 | 3056 | 1453 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Aérotherme plafond T15 | 0.665 | 0.268 | 3784 | 1079 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Aérotherme plafond T4 | 0.728 | 0.331 | 4147 | 1335 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Barre de mise à la terre | 0.614 | 0.227 | 3494 | 913 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Cabinet de mesurage HQ | 0.610 | 0.211 | 3473 | 850 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Interrupteur de sûreté 400A SF (réfrigération) | 0.714 | 0.235 | 4067 | 948 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Interrupteur de sûreté 600A | 0.604 | 0.205 | 3442 | 827 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Interrupteur de sûreté 600A | 0.614 | 0.211 | 3498 | 850 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Panneau RC-PDNO-600 | 0.599 | 0.213 | 3410 | 857 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Panneau RC-PSNO-200 | 0.613 | 0.219 | 3492 | 884 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B12 | 0.468 | 0.324 | 2667 | 1307 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B15 | 0.468 | 0.280 | 2667 | 1128 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B25 | 0.563 | 0.361 | 3204 | 1453 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B5 | 0.554 | 0.187 | 3153 | 754 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B5 | 0.544 | 0.188 | 3100 | 756 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Plinthe B5 | 0.596 | 0.188 | 3391 | 756 |
| E301_ADD | Électrique_Plans pour soumission - 6 | Raccordement chauffe-eau CE (36 kW) | 0.667 | 0.190 | 3796 | 765 |
| T201 | Électrique_Plans pour soumission - 11 | Sortie télécom VS | 0.214 | 0.608 | 1221 | 2450 |
| T201 | Électrique_Plans pour soumission - 11 | Sortie télécom VS | 0.747 | 0.609 | 4253 | 2452 |
| T201 | Électrique_Plans pour soumission - 11 | Sortie télécom WF | 0.307 | 0.461 | 1748 | 1856 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Commutateur PoE GS308PP | 0.422 | 0.181 | 2404 | 728 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Concentrateur WAH-C-POE-ID | 0.404 | 0.222 | 2300 | 893 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Concentrateur WAH-C-POE-ID | 0.460 | 0.222 | 2618 | 893 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Contrôleur de zone WAC2-POE | 0.465 | 0.181 | 2646 | 728 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.160 | 0.344 | 913 | 1384 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.612 | 0.344 | 3483 | 1384 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.764 | 0.371 | 4350 | 1493 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.160 | 0.471 | 913 | 1897 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.612 | 0.471 | 3483 | 1897 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.863 | 0.498 | 4916 | 2006 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.308 | 0.599 | 1755 | 2411 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.586 | 0.599 | 3338 | 2411 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.706 | 0.626 | 4018 | 2520 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.586 | 0.726 | 3338 | 2924 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.091 | 0.726 | 516 | 2925 |
| E003_ADD | ELectrique_Addenda ELE-002_Plans - 3 | Terminaison ACC-C-TP | 0.731 | 0.753 | 4163 | 3033 |
| E002_ADD | — (aucune page humaine) | Raccordement RCFFM — à confirmer | 0.375 | 0.852 | 2133 | 3430 |
| E002_ADD | — (aucune page humaine) | Raccordement réfrigération de la glace | 0.309 | 0.721 | 1761 | 2905 |
| E002_ADD | — (aucune page humaine) | Raccordement régulation | 0.555 | 0.835 | 3163 | 3362 |
| E002_ADD | — (aucune page humaine) | Raccordement régulation | 0.555 | 0.840 | 3163 | 3384 |

## Même position, libellé différent (probable mauvais type)

| Feuille IA | Libellé humain | Libellé IA attendu | Libellé IA posé | x px IA | y px IA |
|---|---|---|---|---:|---:|
| E201_ADD | DETECTEUR FUMÉ | Détecteur de fumée | Détecteur de fumée de conduit (note 2) | 2930 | 849 |
| E201_ADD | DETECTEUR FUMÉ | Détecteur de fumée | Détecteur de fumée de conduit (note 2) | 2878 | 867 |
| E201_ADD | DETECTEUR FUMÉ | Détecteur de fumée | Luminaire L3A | 3424 | 925 |
| E201_ADD | ENSEIGNE SORTIE | Indicateur d'issue Z1 (mur) — à confirmer | Indicateur d'issue Z2 (plafond) — à confirmer | 2995 | 1320 |
| E201_ADD | FIXT TYPE R2 | Interrupteur basse tension | Tête d'éclairage simple | 3156 | 913 |
| E201_ADD | FIXT TYPE R2 | Interrupteur basse tension | Luminaire R2 | 3103 | 962 |
| E201_ADD | FIXT TYPE R2 | Interrupteur basse tension | Tête d'éclairage double | 3236 | 994 |
| E201_ADD | INT 1 VOIE | Interrupteur basse tension | Tête d'éclairage simple | 3075 | 913 |
| E201_ADD | INT 1 VOIE | Interrupteur basse tension | Luminaire R2 | 3276 | 962 |
| E201_ADD | INT 1 VOIE | Interrupteur basse tension | Poste BT double (a/b) | 3771 | 1331 |
| E201_ADD | INT 3 VOIE | Poste BT double (a/b) | Luminaire L4A | 3544 | 858 |
| E201_ADD | PRISE | Prise double 15A | Prise hauteur spéciale | 3481 | 984 |
| E201_ADD | TETE DOUBLE | Tête d'éclairage double | Luminaire R2 | 3190 | 962 |
| E201_ADD | TETE SIMPLE | Interrupteur basse tension | Panneau d'alarme incendie (PAI) | 3057 | 888 |
| E201_ADD | TETE SIMPLE | Interrupteur basse tension | Tête d'éclairage simple | 3330 | 913 |
| E201_ADD | fixt type l3 | Luminaire L3 | Luminaire L3A | 3427 | 847 |
| E201_ADD | fixt type l3 | Luminaire L3 | Luminaire L3A | 3661 | 848 |
| E201_ADD | fixt type l3 | Luminaire L3 | Luminaire R2 | 3365 | 938 |
| E201_ADD | fixt type l3 | Luminaire L3 | Luminaire L3A | 3661 | 949 |
| E201_ADD | fixt type l4 | Luminaire L4 | Armoire de relais BT (P.R.) | 3498 | 910 |
| E201_ADD | fixt type l4 | Luminaire L4 | Luminaire L4A | 3544 | 947 |
| E301_ADD | B1250W | Plinthe B12 | Raccordement serpentin SE | 2813 | 1285 |
| E301_ADD | B500W | Plinthe B5 | Raccordement ventilateur VE | 3433 | 933 |
| E301_ADD | GFI | Prise DDFT | Prise DDFT fontaine réfrigérée | 3064 | 1029 |
| E301_ADD | MOTEUR 1 HP 120V | Raccordement VA | Raccordement ventilateur VE | 3937 | 1077 |
| E301_ADD | PRISE | Prise double 15A | Raccordement serpentin SE | 3825 | 905 |
| E301_ADD | PRISE | Prise double 15A | Prise au-dessus du comptoir | 3631 | 920 |
| E301_ADD | PRISE | Prise double 15A | Prise au-dessus du comptoir | 3484 | 938 |
| E301_ADD | PRISE | Prise double 15A | Prise au plafond | 2884 | 958 |
| E301_ADD | PRISE | Prise double 15A | Prise au-dessus du comptoir | 2906 | 1046 |
| E301_ADD | PRISE | Prise double 15A | Prise au-dessus du comptoir | 4064 | 1109 |
| E301_ADD | PRISE | Prise double 15A | Prise au plafond | 2910 | 1137 |
| E301_ADD | PRISE | Prise double 15A | Prise au plafond | 3582 | 1192 |
| E301_ADD | PRISE | Prise double 15A | Prise au-dessus du comptoir | 3749 | 1229 |
| E301_ADD | PRISE | Prise double 15A | Prise au plafond | 2910 | 1261 |
| E301_ADD | SERPENTIN | Raccordement serpentin SE | Raccordement chauffe-eau CE (36 kW) | 3796 | 819 |
| T201 | HP | Haut-parleur — fourni par autres | Sortie contrôle de volume | 2910 | 1242 |
| T201 | TEL | Sortie télécom (note) | Sortie télécom CA | 3412 | 1049 |
| T201 | TEL | Sortie télécom (note) | Sortie télécom D | 2902 | 1176 |
| T201 | TEL | Sortie télécom (note) | Sortie télécom WF | 3148 | 1291 |
| T201 | TEL | Sortie télécom (note) | Sortie télécom D | 2903 | 1418 |
| T201 | TEL | Sortie télécom (note) | Sortie télécom WF | 3707 | 1463 |

## Méthode et limites

- Pages : nom (PDF, page) puis recalage géométrique (seuil 1.5 % diag., score ≥ 0.4, 8 orientations, échelle uniforme ± ajustement par axe). Marques : affectation optimale sur la distance, seuil 1.2 % de la diagonale du raster IA, sans tenir compte des libellés.
- Les coordonnées `X`/`Y` des éléments sont prises telles quelles (pas de correction de centre de symbole : l'écart est inférieur à 0,3 % de la diagonale).
- Les lignes (longueurs) sont seulement comptées ; elles ne sont pas comparées.
