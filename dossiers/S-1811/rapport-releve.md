# Rapport de relevé — S-1811

**Projet :** STJ-Construire 6 nouveaux bâtiments d'hébergement, Garnison Saint-Jean, QC (NORR / Pageau Morel), dossier QS-000428-B.

**Date du relevé :** 2026-09-22.

**Résultat :** 811 marques actives (815 lignes, dont 4 exclues) et 38 réserves (R-001 à R-038). **Les quantités valent pour UN bâtiment (#1, type A) plus le site.** Pour la soumission, il faut prévoir 6 bâtiments (note A du 502B, voir R-001).

## Méthode

1. **Classement.** Lecture des 36 pages : 11 pages de soumission, 20 de l'addenda MEP-01 et 5 de MEP-02. Le numéro et le titre ont été lus dans le cartouche de chaque page. Pour chaque feuille, la version retenue est la plus récente d'après le bloc de révision. Les versions antérieures sont classées `remplacee`, et les 13 feuilles mécaniques (402B–416B) `autre` (fichier `feuilles-classement.csv`).
2. **Nomenclature.** Tirée de la légende 501B (MEP-02), de la liste des appareils d'éclairage et de la liste de chauffage : 79 libellés dans `nomenclature.csv`.
   - Une ligne de légende correspond à un compteur. La même règle vaut pour chaque variante : urgence (plein gris), DDFT cercle ou triangle, suffixes de chauffage .1 et .2.
3. **Occurrences texte.** Faites à la main, parce que l'exécution de `extract_occurrences.py` a été refusée (R-005). On a lu les étiquettes A1…X1, FL-TX/RX, G2/G3, L2/L3/L5, les puissances de plinthes (500W…8000W) et les candelas (30/75/115cd) dans `texte/*-mots.csv`.
   - Chaque étiquette a été contrôlée sur les tuiles.
   - L'état « urgence » a été attribué appareil par appareil.
   - 4 faux positifs sont exclus : un « A1 » isolé et trois « 500W » qui sont en fait des serpentins.
4. **Occurrences visuelles.** Toutes les tuiles des feuilles `plan` ont été parcourues, ainsi que le détail 2 des feuilles 505B et 506B. On y a relevé les éléments suivants :
   - commandes et prises ;
   - points de raccordement ;
   - équipements mécaniques, sectionneurs et appareillage de distribution ;
   - alarme incendie (détecteurs, déclencheurs, modules) ;
   - poteaux et puits d'accès.
5. **Addendas.** Seules les versions en vigueur ont été relevées. Aucune comparaison tuile par tuile avec les versions de base n'a été faite (R-003).
5b. **Sans symbole au plan.** Toutes les lignes des tableaux 511B et les départs du schéma 502B ont été appariées aux symboles des plans. Éléments ajoutés sans symbole au plan :
   - mesurage client pour la GTB (note B) ;
   - 3 barres de mise à la terre ;
   - 3 départs futurs EF ;
   - 5 poteaux de la note D.

## Feuilles traitées (version en vigueur)

| feuille | cartouche | type | marques |
|---|---|---|--:|
| S267_ADD_2 | 501B Légende (MEP-02) | legende | 0 |
| S267_ADD_3 | 502B Distribution électrique (MEP-02) | schema | 4 |
| S267_ADD_4 | 503B Multidisciplinaire site (MEP-02), 1:250 | plan | 65 |
| S267_4 | 504B Détails site | detail | 0 |
| S267_ADD_21 | 505B Éclairage niveau 1 (MEP-01), 1:100 | plan | 272 |
| S267_ADD_22 | 506B Services niveau 1 (MEP-01), 1:100 | plan | 305 |
| S267_ADD_23 | 507B Services toit (MEP-01), 1:100 | plan | 12 |
| S267_ADD_24 | 508B Services auxiliaires niveau 1 (MEP-01), 1:100 | plan | 150 |
| S267_9 | 509B Diagramme d'alarme incendie | schema | 0 (indicatif) |
| S267_ADD_5 | 510B Détails (MEP-02) | detail | 0 |
| S267_ADD_25 | 511B Panneaux (MEP-01) | tableau | 3 |
| **Total** | | | **811** |

## Totaux par libellé (un bâtiment + site)

**Éclairage (505B)**

| Libellé | Normal | Urgence |
|---|--:|--:|
| A1 | 53 | 6 |
| B1 | 4 | — |
| C1 | 24 | 4 |
| C2 | 36 | — |
| C3 | 10 | 7 |
| D1 | 29 | 14 |
| E1 | 12 | 4 |

Autres : X1 enseignes 18 ; mini-onduleurs 2.

**Commandes (505B)**
- Interrupteurs unipolaires : 4
- Interrupteurs avec détecteur : 37
- Gradateurs : 6
- Détecteurs de présence au plafond : 2

**Prises et télécom (506B)**
- 5-15R : 108
- 5-15R WP : 1
- 5-20R : 25
- 5-15R triangle : 2
- DDFT cercle : 8
- DDFT triangle : 2
- Sorties télécom : 15

**Raccordements (506B)**
- Plomberie : 32
- Volets coupe-feu : 6
- Portes automatiques : 4
- Panneau de contrôle : 1

**Chauffage (506B)**
- C1.1 500W : 34
- C4.1 1500W : 11
- C6.1 1000W : 4
- C2.2 4000W : 3
- C5.1 : 2
- C5.2 : 1
- C3.2 8000W : 1
- Serpentins : EHC1 19 kW × 3, EHC2 15 kW × 3, EHC3 3 kW × 1, EHC1-006 500W × 3

**Mécanique (506B, 507B)**
- HVLS CF : 4
- EV : 2
- CS : 3
- HU : 3
- TF : 2
- PU1 : 1
- WH : 3
- RT1 : 3
- HE1 : 3
- Prises des UTA (fournies par le fabricant) : 3

**Distribution (502B, 506B, 511B)**
- Panneaux 120/208 V : 2
- Panneau 347/600 V : 1
- Transformateur 112,5 kVA : 1
- Interrupteur principal 400 A : 1
- Armoire HQ type B : 1
- Mesurage GTB : 1
- Barres de mise à la terre : 3
- Sectionneurs ≤240 V : 8
- Sectionneurs WP : 3
- Départs futurs EF : 3

**Alarme incendie (507B, 508B)**
- Klaxons/stroboscopes : 63
- Stroboscopes seuls : 6
- Détecteurs de fumée : 50
- Faisceaux : FL-TX 3, FL-RX 3
- Déclencheurs manuels : 9
- ARM : 13 (10 au 508B, 3 au 507B)
- AIM : 2
- PS : 2
- FAP : 1
- FAAP : 1

**Site (503B)**
- Appliques : G2 20, G3 11
- Lampadaires : L2 3, L3 4, L5 9
- Poteaux de bois : 8 dessinés + 5 selon la note D
- Puits d'accès : 5

## Ce qui n'a pas pu être relevé

- **Éléments linéaires, à métrer :**
  - artères et câblage ;
  - conduits et massifs souterrains ;
  - ligne aérienne ;
  - chemins de câbles.
- **Variantes à ventiler :** X1 (R-013) et la nature exacte des symboles « gradateur » et « ▽ » (R-014, R-019, R-020).
- **Écarts plan / tableaux sur les prises :** R-016 à R-018.
- **Différentiel base / addenda :** non fait tuile par tuile (R-003). Il n'y a pas de document texte d'addenda.
- **Comparaison avec l'estimateur :** impossible, aucun export fourni (R-007).

## Temps et limites

- Travail sur les aperçus et les tuiles 3×4 seulement. Sans `zoom.py`, les symboles de petite taille (remplissage d'urgence en bord de tuile, variantes de X1) portent une incertitude, signalée en réserve.
- Les coordonnées visuelles sont lues sur les règles graduées, à environ 5 pt près. Les coordonnées texte correspondent au centre du mot (étiquette, puissance ou candela), qui peut être à 10–25 pt du symbole.
- Contrôle final fait : les 79 libellés utilisés dans `occurrences-texte.csv` et `occurrences-visuel.csv` existent tous dans `nomenclature.csv` (`cut -d, -f2 … | sort | uniq -c`).
