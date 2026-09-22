# Rapport de relevé — S-1715

**Projet :** Construction d'infrastructures sportives au parc Lionel-Groulx : chalet, patinoire et stationnement (Ville de Salaberry-de-Valleyfield). Électricité par BPA, dossier 25-13561.
**Date :** 2026-09-22
**Documents :**
- Plans pour soumission (11 feuilles, 2026-02-06)
- Addenda ELE-001 (4 feuilles, 2026-03-02)
- Addenda ELE-002 (6 feuilles, 2026-03-12)

## Méthode

1. **Classement.** Les 21 pages ont été classées (`feuilles-classement.csv`), avec le vrai numéro lu au cartouche. ELE-002 réémet et remplace ELE-001 et la version de base. Neuf pages sont donc `remplacee` (R-001).
2. **Nomenclature.** Elle a été construite à partir de trois sources :
   - la légende d'E-002 (ELE-002) ;
   - les tableaux de luminaires et de chauffage d'E-101 (ELE-002) ;
   - la légende télécom de T-001, plus les notes d'E-201, E-301, E-102 et T-201.
   Elle compte 96 libellés. Chaque ligne de légende ou chaque type du tableau correspond à un compteur.
3. **Étiquettes texte.** `extract_occurrences.py` a été lancé sur les 4 feuilles `plan` (E-102, E-201, E-301, T-201). Les résultats ont ensuite été contrôlés au zoom. Retirés comme faux positifs : les bulles d'axes D et F, et les PCA/PDI du texte des notes. Deux « F » avec triangle ont été relabellisés « klaxon ».
4. **Relevé visuel.** Toutes les zones dessinées du chalet ont été parcourues en zooms d'environ 250 × 280 pt. La patinoire et le site ont été parcourus en aperçu et en zooms ciblés. Relevés sans étiquette :
   - détecteurs de fumée, têtes et accumulateur de secours ;
   - interrupteurs et gradateurs BT ;
   - prises (par variante de légende), sèche-mains ;
   - panneaux, transformateur, sectionneurs, Camlock ;
   - puits de tirage, boîtier de borne VE ;
   - détecteurs de mouvement, haut-parleurs, sorties télécom annotées.
5. **Ce qui n'a pas de symbole au plan.** Trois sources ont été lues :
   - les cédules RC-PDNO-600 et RC-PSNO-200 et l'unifilaire (E-002). En sortent 4 raccordements : réfrigération, régulation ×2 et RCFFM. Tous les autres départs ont été appariés à une étiquette du plan ;
   - le schéma WaveLinx (E-003) : contrôleurs RSP, terminaisons, concentrateurs, commutateur, WAC2 ;
   - les notes du plan : note 1 et note 2 d'E-201, Camlock, note 7 de T-201, poteau client, borne future.
6. **Addendas.** Seule la dernière version (ELE-002) est relevée. Les zones en nuage sont listées en R-001.

## Feuilles traitées

| feuille | type | échelle | marques texte | marques visuelles | total |
|---|---|---|--:|--:|--:|
| E102 (E-102 plan d'implantation) | plan | 1:200 | 2 | 4 | 6 |
| E201_ADD (E-201 éclairage et alarme incendie) | plan | 1:100 | 123 | 37 | 160 |
| E301_ADD (E-301 services) | plan | 1:100 | 49 | 41 | 90 |
| T201 (T-201 câblage structuré) | plan | 1:100 | 47 | 17 | 64 |
| E002_ADD (E-002 légende, cédules, unifilaire) | legende | — | 0 | 4 | 4 |
| E003_ADD (E-003 schéma WaveLinx) | schema | — | 0 | 35 | 35 |
| **Total** | | | **221** | **138** | **359** |

Les autres feuilles ne portent aucune marque :
- E001_ADD et T000 (frontispices, `autre`) ;
- T001 (légende télécom) ;
- E101_ADD, T100 et T101 (détails et tableaux) ;
- 9 pages classées `remplacee`.

## Totaux par libellé

**Luminaires (E-201, E-102)**

| Libellé | Qté |
|---|--:|
| R1 (patinoire) | 30 |
| A1 | 10 |
| L3 | 10 |
| L4 | 8 |
| P1 | 8 |
| R3 | 6 |
| M1 | 5 |
| L3A | 4 |
| R2 | 4 |
| L2 | 3 |
| L1 | 2 |
| L4A | 2 |
| D1 (lampadaires, E-102) | 2 |

**Secours**

| Libellé | Qté |
|---|--:|
| Indicateur d'issue Z1 (à confirmer) | 4 |
| Indicateur d'issue Z2 (à confirmer) | 1 |
| Accumulateur AUBX | 1 |
| Tête double | 7 |
| Tête simple | 3 |

**Commandes**

| Libellé | Qté |
|---|--:|
| Détecteur de présence | 11 |
| Interrupteur BT | 7 |
| Poste BT double (a/b) | 3 |
| Gradateur BT | 4 |
| Interrupteur unipolaire | 2 (1 sur E-201, 1 sur E-301) |
| Panneau P1 | 1 |
| Armoire de relais P.R. | 1 |
| RSP-C-347-Z1 | 19 |
| ACC-C-TP | 12 |
| WAH-C-POE-ID | 2 |
| GS308PP | 1 |
| WAC2-POE | 1 |

**Alarme incendie**

| Libellé | Qté |
|---|--:|
| Poste manuel | 5 |
| Klaxon | 2 |
| Klaxon + strobe | 1 |
| Détecteur de fumée | 10 |
| Détecteur de fumée de conduit | 2 |
| Relais adressable RA | 2 |
| PAI | 1 |

**Prises (E-301, sauf mention)**

| Libellé | Qté |
|---|--:|
| Prise double 15A | 8 |
| Prise au-dessus du comptoir | 6 |
| Prise DDFT | 5 |
| Prise au plafond | 4 |
| Prise 15/20A | 3 |
| Prise DDFT intempéries | 3 |
| Prise USB | 2 |
| Prise DDFT fontaine | 1 |
| Prise hauteur spéciale (E-201) | 1 |

**Chauffage (E-301)**

| Libellé | Qté |
|---|--:|
| Relais triac RT | 9 |
| Raccordement serpentin SE | 7 |
| Plinthe B5 | 5 |
| Aérotherme A15 | 3 |
| Plinthe B12 | 2 |
| Plinthe B10 | 1 |
| Plinthe B15 | 1 |
| Plinthe B25 | 1 |
| Aérotherme T4 | 1 |
| Aérotherme T15 | 1 |

**Mécanique**

| Libellé | Qté |
|---|--:|
| Raccordement VE | 4 |
| Raccordement CE 36 kW | 3 |
| Raccordement VA | 2 |
| Raccordement régulation | 2 |
| Raccordement VC | 1 |
| Raccordement ECH | 1 |
| Raccordement PECR | 1 |
| Raccordement COND | 1 |
| Raccordement DEV | 1 |
| Raccordement réfrigération | 1 |
| Raccordement RCFFM (à confirmer) | 1 |
| Sèche-mains | 3 |

**Distribution**

| Libellé | Qté |
|---|--:|
| RC-PDNO-600 | 1 |
| RC-PSNO-200 | 1 |
| RC-TRNO-600 | 1 |
| Cabinet de mesurage HQ | 1 |
| Interrupteur de sûreté 600A | 2 |
| Interrupteur de sûreté 400A SF | 1 |
| Barre de MALT | 1 |
| Camlock | 1 |
| Boîtier borne VE future | 1 |
| Puits de tirage | 2 |
| Poteau client (fourni par autres) | 1 |

**Télécom et sécurité (T-201)**

| Libellé | Qté |
|---|--:|
| Boîte de groupe BG | 11 |
| Porte contrôlée | 11 |
| Sortie VS | 8 |
| Haut-parleur (fourni par autres) | 6 |
| CLI | 5 |
| Détecteur de mouvement | 5 |
| Sortie WF | 3 |
| Sortie CB | 3 |
| Sortie D | 2 |
| Sortie (note) | 2 |
| Contrôle de volume | 2 |
| Sortie CA | 1 |
| Microphone | 1 |
| PCA | 1 |
| PDI | 1 |
| Cabinet (fourni par autres) | 1 |
| Barre MALT télécom | 1 |

## Non relevé et limites

- **Linéaires non métrés** (R-025) :
  - conduits souterrains et vides (E-102) ;
  - CAT5e ;
  - conduits de vidéosurveillance ;
  - crochets en J ;
  - câblage des départs de cédule.
- **Détails E-101 non chiffrés** (R-024) : prise de terre artificielle (nombre de tiges) et béton des bases D1.
- **Composantes de porte** (lecteurs, gâches, contacts…) des élévations T-101 : non dénombrées, une marque par porte seulement (R-027).
- **Textes d'addenda non reçus** (R-002). Pas de comparaison tuile par tuile entre les versions : seule la dernière version est relevée (R-001).
- **Pas d'export estimateur** : aucune comparaison produite (R-005).
- **Symboles d'interprétation incertaine** :
  - types Z1/Z2 ;
  - variantes DDFT ;
  - interrupteurs des salles 107 et 110 ;
  - RCFFM.
  Voir R-006, R-010, R-018 et R-019.
- **Précision des coordonnées** : environ 5 pt, lues sur les règles des zooms.
- **Contrôle des libellés** : chaque libellé utilisé dans les deux fichiers d'occurrences figure dans `nomenclature.csv`. La vérification a été faite à la main, en recoupant ligne par ligne ; `cut` n'a pas pu être exécuté dans cet environnement (Bash restreint à `uv run releve/*.py`).
