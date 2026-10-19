# FORMAT-EXEMPLE — spec unique du PDF de relevé (gold EXEMPLE.pdf, HR26-14)

**C'est la seule description du format du PDF « Plans annotés »** (pastilles, palettes, étiquettes, encadré
`RELEVE <feuille> - MATERIEL`, bordereaux). Toute autre doc du dépôt y renvoie au lieu de recopier des chiffres
(`tests/test_spec_format_unique.py` le vérifie). Règle de Francis (2026-10-05) : **quand une doc et le gold
divergent, le gold gagne** — on corrige cette spec, jamais le gold. Ce que le moteur ne reproduit pas encore est
listé et chiffré au §6.

## 0. Source et méthode de mesure
- Gold : `EXEMPLE.pdf` = `exemple-sortie-cible.pdf` (branche `data-hr26-14-plans`, `hr26-14/` ; copie sur le
  Drive `AI/Soumission 2026/_STANDARD_RELEVE/EXEMPLE.pdf`), sha256
  `0861bc3a0e9697f7f2764fba85f0cc35bc8c5b8a3d06ce3ff2b11b32432eb84b`, 87 pages de 2594 x 1729 pt. Non versionné
  sur `main` ; extrait approuvé E08/E09 : `apprentissage/hr26-14-exemplaire/cible-visuelle/` (ancre : `SOURCE.txt`).
- Cible visuelle approuvée par Francis : **E08 = p.62 (bordereau p.63) et E09 = p.64 (bordereau p.65)**. Les deux
  bordereaux sont au format **agrégé 6 colonnes** (§4.2).
- Mesures du 2026-10-05, PyMuPDF 1.28.2, sur le gold lui-même : pastilles = tracés de `page.get_drawings()` dont
  `fill_opacity` = 0,28 ; textes = `page.get_text("dict")` (police, corps, position du haut de ligne) ; encadré =
  rectangle blanc à bord 0,7 pt contenant `RELEVE `. « p.N » = numéro de page du gold (base 1).
- Le gold est en ASCII sans accents (`reperes`, `Quantites`) : le moteur reproduit ce texte tel quel.

## 1. Structure du document
Chaque feuille = **1 page plan suivie de 1 à 6 pages de bordereau** (même format de page) : 26 pages plan +
61 pages de bordereau = 87 pages. Signets du gold (136 entrées, `get_toc(simple=False)`) : un signet de niveau 1
`HR26-14-<feuille>-annote-v<n>` par feuille, sur la page plan (ex. `HR26-14-E03-annote-v6` p.50,
`HR26-14-E08-annote-v1` p.62 ; v1 partout sauf E03 v6 et E01, E04, E05, E06, E12, E14 v2), et dessous les
signets d'origine du plan de la feuille, décalés d'un niveau (110 entrées) : sur chaque feuille la chaîne
`HR24-13 ME pr AO` (2) > `Elect-A1-ARI` (3) > `Feuilles et vues` (4) > `A1-ARI` (5), **sans destination** ; en
plus, sur DSI01 `DSI` > `Feuilles et vues` > `DSI-DSI01 STGEORGES VEP` (p.1) et sur E01 `Elect` > `Feuilles et vues`
> `Elect-E01 LOT A` (p.44). Aucun signet ne vise une page de bordereau. Le moteur reproduit cette table : préfixe
= nom de la soumission (`projet`), v<n> = version de la feuille (`version`, v1 si inconnue), signets d'origine =
`signets` de la feuille, sinon ceux du PDF de plans qui visent sa page, avec leurs parents (`render.signets_de_page`).

| Feuille | Format bordereau | Page plan | Pages bordereau | Repères / familles / RES | Palette | Encadré |
|---|---|--:|---|---|---|---|
| DSI01 | matériel 8 col. | 1 | 2-7 (6) | 122 / 8 / 122 | A | standard 1 ligne |
| DSI02 | matériel 8 col. | 8 | 9-11 (3) | 62 / 9 / 62 | A | standard 1 ligne |
| DSI03 | matériel 8 col. | 12 | 13-17 (5) | 94 / 8 / 94 | A | standard empilé |
| DSI04 | matériel 8 col. | 18 | 19-21 (3) | 56 / 9 / 56 | A | standard 1 ligne |
| DSI05 | matériel 8 col. | 22 | 23-28 (6) | 122 / 8 / 122 | A | standard 1 ligne |
| DSI06 | matériel 8 col. | 29 | 30-32 (3) | 49 / 9 / 49 | A | standard 1 ligne |
| DSI07 | matériel 8 col. | 33 | 34-39 (6) | 121 / 8 / 121 | A | standard 1 ligne |
| DSI08 | matériel 8 col. | 40 | 41-43 (3) | 49 / 9 / 49 | A | standard 1 ligne |
| E01 | agrégé 6 col. | 44 | 45 (1) | 80 / 4 / 80 | A | standard empilé |
| E02 | matériel 8 col. | 46 | 47-49 (3) | 52 / 27 / 52 | A | standard empilé |
| E03 | agrégé 6 col. | 50 | 51 (1) | 126 / 21 / — | B | **v6 sans RES** |
| E04 | agrégé 6 col. | 52 | 53 (1) | 112 / 23 / — | B | **v6 sans RES** |
| E05 | agrégé 6 col. | 54 | 55 (1) | 116 / 23 / — | B | **v6 sans RES** |
| E06 | agrégé 6 col. | 56 | 57 (1) | 51 / 5 / 51 | A | standard 1 ligne |
| E07 | matériel 8 col. | 58 | 59-61 (3) | 53 / 26 / 53 | A | standard empilé |
| E08 | agrégé 6 col. | 62 | 63 (1) | 128 / 22 / — | B | **v6 sans RES** |
| E09 | agrégé 6 col. | 64 | 65 (1) | 103 / 6 / 103 | A | standard empilé |
| E10 | matériel 8 col. | 66 | 67-69 (3) | 53 / 26 / 53 | A | standard 1 ligne |
| E11 | agrégé 6 col. | 70 | 71 (1) | 172 / 20 / 64 | B | standard 1 ligne |
| E12 | agrégé 6 col. | 72 | 73 (1) | 110 / 6 / 110 | A | standard empilé |
| E13 | matériel 8 col. | 74 | 75-77 (3) | 53 / 26 / 53 | A | standard 1 ligne |
| E14 | agrégé 6 col. | 78 | 79 (1) | 172 / 20 / 64 | B | standard 1 ligne |
| EU01 | travaux / achats 8 col. | 80 | 81 (1) | 31 / 4 / 31 | A | standard 1 ligne |
| EU02 | travaux / achats 8 col. | 82 | 83 (1) | 28 / 5 / 4 | A | standard empilé |
| EU03 | travaux / achats 8 col. | 84 | 85 (1) | 32 / 6 / 32 | A | standard 1 ligne |
| EU04 | travaux / achats 8 col. | 86 | 87 (1) | 30 / 6 / 30 | A | standard 1 ligne |

Total : 2177 repères. Résumé : **matériel** = DSI01-08, E02, E07, E10, E13 (12 feuilles) ; **agrégé** = E01,
E03-E06, E08, E09, E11, E12, E14 (10 feuilles) ; **travaux / achats** = EU01-04 (4 feuilles). Le nom des feuilles
incendie est `DSI01`..`DSI08` (jamais `DS01`). RES = repères partout sauf E11/E14 (64) et EU02 (4) ; pas de
compteur RES sur E03/E04/E05/E08 (encadré v6, §3.3).

## 2. Page plan — pastilles, palettes, étiquettes, calques
### 2.1 Commun à toutes les feuilles
- La page vectorielle d'origine est conservée telle quelle (dessin, cartouche, sceau, calques CAD). La surcouche est
  vectorielle, dans des calques optionnels (OCG) : un calque `RELEVE <code> - <materiel>` **par famille et par
  feuille** plus `RELEVE - Legende et avertissements` par feuille, soit 344 + 26 = **370 calques `RELEVE`** (89 noms
  distincts : un même nom est un objet distinct sur chaque feuille) sur les 1670 calques du gold. Tous actifs
  (`/D/ON`, intention View, usage Artwork). Rattachement : la page plan d'une feuille déclare ses calques famille et
  sa légende ; **chaque page de bordereau** déclare la légende de sa feuille et les calques des familles dont elle
  porte une ligne (p.2 : légende + I01 ; p.63 : légende + 22 familles) ; aucune page n'utilise le calque d'une autre
  feuille. Dans le bordereau, titre, sous-titres, bande et titres de colonnes, filets et bloc de notes sont dans la
  légende ; les cellules d'une ligne dans le calque de sa famille. Panneau des calques (`/D/Order`) : pour chaque
  feuille, ses familles dans l'ordre de la légende puis sa légende, au premier niveau.
- **Style de pastille** (100 % des tracés à remplissage 0,28 des 26 pages plan) : remplissage = couleur du trait à
  **28 %** d'opacité, trait **0,7 pt** à **90 %** (aspect pastel).
- **Étiquette de repère** : Helvetica **4,8 pt**, gris 0,1, dans une boîte blanche à **88 %** d'opacité reliée au
  centre de la pastille par un **trait d'attache de 0,35 pt** de la couleur de la famille. Hauteur de boîte : 8 pt
  pour 1 ligne, 14 pt pour 2 lignes (15 et 20 pt sur certaines étiquettes des feuilles en palette B).
- Les pastilles de légende de l'encadré (10 pt de diamètre ou de côté ; 13 pt dans l'encadré v6) sont dessinées avec
  le même style : elles ne sont pas des repères.

### 2.2 Formes et rayons des pastilles par format
Le rayon **4,1859 pt n'est la règle que pour les feuilles incendie DSI** ; il n'y a pas de rayon unique.

| Groupe de feuilles | Formes des pastilles (repères seulement) | Rayon / taille | Étiquette | Preuve |
|---|---|---|---|---|
| Matériel incendie DSI01-08 | cercles seulement | r = **4,1859 pt** | 1 ligne `I01-01` | p.1 : 122 cercles r 4,1859 (+ 8 cercles r 5,0 = légende) |
| Matériel électricité E02, E07, E10, E13 | **rectangles** = boîte du symbole (panneaux, boîtiers) | variable (p.46 : de 4,5 x 16,8 à 917 x 58 pt) | 1 ligne `M01-01` | p.46 : 52 rectangles (+ 27 carrés 10 pt = légende) |
| Agrégé palette A : E01, E06, E09, E12 | cercles, **triangles pointe en haut**, rectangles (plinthes, panneaux) | cercles r = **5,0231 pt** ; triangles 10,05 pt ; rectangles 2,25 à 69 pt | 2 lignes `CH-01` / `1250 W S25,27` | p.64 (E09) : 53 cercles + 14 triangles + 36 rectangles = 103 |
| Agrégé palette B : E03, E04, E05, E08, E11, E14 | cercles, **losanges**, rectangles aux dimensions graphiques du plan (plinthes PL) | cercles r = **4,6045 / 5,0231 / 5,4417 / 5,8603 pt** selon la famille ; losanges 10,05 à 11,72 pt ; rectangles ex. 7,08 x 109 pt | 2 lignes `AF-01` / `C2` ; `PL-01` / `1000 W C13,15` en **Helvetica 5,2 pt** | p.62 (E08) : 100 cercles (68 x 5,4417, 20 x 4,6045, 8 x 5,0231, 4 x 5,8603) + 6 losanges + 22 rectangles = 128 |
| Travaux EU01-04 | cercles, triangles pointe en haut, losanges (EU02-04), carrés | cercles r = 5,0231 pt ; triangles 10,46 pt ; carrés 10,88 / 11,72 pt | 1 ligne `IS-01` | p.80 (EU01) : 18 cercles + 10 triangles + 3 carrés = 31 |

Autres décomptes vérifiés (repères = cercles + polygones + rectangles hors légende) : E01 p.44 = 38 + 13 triangles
+ 29 = 80 ; E03 p.50 = 98 + 6 losanges + 22 = 126 ; E11 p.70 = 128 + 12 losanges + 32 = 172. Triangle du gold :
sommets (milieu, haut), (droite, bas), (gauche, bas) de sa boîte.

### 2.3 Les deux palettes
- **Palette A — cycle de 6 couleurs** dans l'ordre des familles de la feuille (I01, I02, … puis on recommence) :
  orange (1, 0,6902, 0), bleu (0, 0,4471, 0,8078), vert (0, 0,651, 0,3176), violet (0,5569, 0,2667, 0,6784),
  ardoise (0,1725, 0,2431, 0,3137), rouge (0,9059, 0,298, 0,2353). Feuilles : DSI01-08, E01, E02, E06, E07, E09,
  E10, E12, E13, EU01-04 (20 feuilles). Preuve p.1 : orange 39 = I01 36 + I07 1 + 2 pastilles de légende ;
  bleu 32 = I02 29 + I08 1 + 2.
- **Palette B — une couleur par famille, palette du relevé** : E03, E04, E05, E08, E11, E14 (6 feuilles). 20 couleurs distinctes mesurées sur ces 6 pages : (0,078 0,078 0,078), (0,133 0,545 0,133),
  (0,145 0,388 0,922), (0,208 0,208 0,208), (0,208 0,208 0,62), (0,208 0,6 0,6), (0,322 0,702 0,886),
  (0,471 0,784 0,471), (0,478 0,38 0,576), (0,545 0,361 0,965), (0,588 0,784 0,98), (0,6 0,208 0,6),
  (0,635 0,42 0,267), (0,706 0,325 0,035), (0,753 0,204 0,804), (0,859 0,153 0,467), (0,867 0,529 0,741),
  (0,867 0,812 0,208), (0,871 0,871 0,208), (0,894 0,208 0,208). Trois d'entre elles sont exactement des couleurs de
  base de `releve/commun.py::PALETTE_FAMILLE` : alarme (53, 153, 153), télécom (53, 53, 158), distribution
  (228, 53, 53).
- La palette ne suit pas le format : E01/E06/E09/E12 sont agrégées en palette A, E03/E04/E05/E08/E11/E14 agrégées
  en palette B. Elle suit le titre de feuille du cartouche : palette B sur les 6 feuilles `LOGEMENTS TYPES`, A sur
  les 20 autres (`VUES EN PLAN`, `DIAGRAMMES`, `UNIFILAIRE ET CEDULES`) — mesure du §6 E7, règle non appliquée.
- En palette B, **même code de famille = même couleur, même forme et même taille sur les 6 feuilles** (mesuré
  p.50, 52, 54, 62, 70, 78) : ex. CU rose (0,867 0,529 0,741) cercle 9,21 pt ; PC brun (0,635 0,42 0,267) cercle
  10,88 ; CG/CT jaune cercle 10,05, GF jaune 10,88 ; CP/SE cercle 11,72 ; IC losange 11,72, TE losange 10,88, TV
  losange 10,05 ; BJ/EV carré 10,88 ; PN carré 12,56 ; PL et LC rectangles aux dimensions du symbole. Table
  complète (25 codes, 20 couleurs) : `src/estimer/render/style.py::PALETTE_B`.

### 2.4 Étiquettes par format
- Matériel : `<code famille>-<séquence>` sur 1 ligne (`I01-01`, `M01-01`), code famille = préfixe `I` (incendie) ou
  `M` (électricité) + numéro.
- Agrégé : code lettres de la famille + séquence (`CH-01`, `AF-01`, `PL-01`) et une 2e ligne de détail quand elle
  existe sur le plan : puissance et circuit (`2000 W S15,17` p.64), circuit seul (`C2` p.62), plinthes en 5,2 pt
  (`1250 W C13,15` p.62).
- Travaux : code lettres + séquence sur 1 ligne (`BD-01`, `IS-01`, `AC-01`).
- `*` après le repère = identification à revalider (ex. `CT-01*` p.62).

## 3. Encadré `RELEVE <feuille> - MATERIEL`
Cadre blanc, bord 0,7 pt (0,25 0,30 0,35), posé dans un espace vide du dessin, jamais sur le cartouche.
Positions ci-dessous = haut de ligne mesuré depuis le haut du cadre. Il existe **deux variantes** : standard (avec
compteur RES) et v6 (sans RES).

La taille du cadre varie d'une feuille à l'autre (de 235 x 880 à 2020 x 110 pt) : elle suit l'espace libre du
plan, pas le format du bordereau.

Communs aux deux variantes standard (mesurés sur les 22 encadrés standard) :
- **Renvoi de page** : `page 2` sur les 26 feuilles = 2e page de la feuille (son bordereau suit la page plan),
  jamais le numéro absolu dans le document (gold : `page 2` aussi sur E08, dont le bordereau est la p.63).
- **1 ligne ou empilé** : titre, compteur (x+195) et renvoi (x+530) sur la même ligne dès que le renvoi tient
  dans le cadre (530 + 265,2 pt de texte ≤ largeur) : 15 cadres de 800 (EU01) à 2020 pt ; sinon empilé : 7 cadres
  de 260 (E07) à 780 pt (E01, E09, E12). Règle exacte sur les 22 (`plan.une_ligne`).
- **Pied** Helvetica 7,0, baseline à **6,475 pt** au-dessus du bas du cadre ; texte propre à la feuille (liste
  ci-dessous), lu dans le gold par `from_exemple` (`pied`) ; un dossier réel garde le pied par défaut du format.
- **Lignes de famille** : quantité à **74 pt avant la fin de sa cellule** (cellule = largeur du cadre / colonnes
  de la grille : DSI01 505 → x+441, DSI05 220 → x+156 ; en 1 colonne la cellule est le cadre entier : E07 260 →
  x+196, E02 390 → x+326) ; libellé coupé 6 pt avant la quantité, 2e ligne **7,4498 pt** sous la 1re, la 1re
  restant sur la ligne du code (DSI05 `AVERTISSEUR INCENDIE` / `KLAXON`, E07 `DISJONCTEUR TRANSFERT` /
  `TEMPORAIRE`). DSI02/04/06/08 : 9 familles sur 3 colonnes au pas de 500 pt (grille de 4 dans 2000 pt). Une
  famille hors légende s'affiche `PLINTHE DE CHAUFFAGE [R-001]` (calque : `... (hors legende - R-001)`).

### 3.1 Standard « 1 ligne » (15 feuilles : DSI01, DSI02, DSI04-08, E06, E10, E11, E13, E14, EU01, EU03, EU04)
Ex. DSI01 p.1 : cadre 2020 x 110 pt ; E11 p.70 : 1700 x 200 ; E10 p.66 : 870 x 255 ; EU01 p.80 : 800 x 180.
- +3,2 : `RELEVE DSI01 - MATERIEL` Helvetica-Bold 12 ; sur la même ligne (+7,2) `122 reperes / 8 familles / RES 122`
  Helvetica 8,2 à x+195 et `Calques activables; modeles, prescriptions et reserves completes page 2` 8,2 à x+530.
- +21,3 : ligne rouge foncé (0,55 0,10 0,10) Helvetica 7,2 `RES = reserve source, modele, position, portee ou
  reconciliation; * = identification a revalider`.
- Familles en colonnes (505 pt sur DSI01, 425 pt sur E11 ; pas de 27 pt sur DSI01, 28,8 pt sur E11) : pastille
  10 pt, code Helvetica-Bold 8,2 à +15, libellé Helvetica 6,6 en majuscules à +50, quantité Helvetica 7,1
  `36 / R36` (ou le compte seul sans réserve, ex. E11 `CT 12`).
- Pied Helvetica 7,0, propre à la feuille : DSI `Quantites source et renvois; voir bordereau detaille.` ;
  E06 `Existant a conserver; renvois de panneaux et travaux non symbolises en reserves page 2.` ;
  E10/E13 `Reperes source; quantites et reserves au bordereau.` ; E11/E14 `PL = dimensions graphiques du plan;
  W/circuits affiches si verifies; NI = materiel non identifie.` ; EU01/EU04 `Emplacements de travaux sur calques;
  achats, prescriptions et reserves detaillees page 2.` ; EU03 `Bordereau complet et reserves page 2.`

### 3.2 Standard « empilé » (7 feuilles : DSI03, E01, E02, E07, E09, E12, EU02)
Ex. E01 p.44 et E09 p.64 : 780 x 320 pt (2 colonnes) ; E02 p.46 : 390 x 705 (1 colonne) ; DSI03 p.12 : 360 x 900.
- +3,2 titre Helvetica-Bold 12 ; +21,0 `103 reperes / 6 familles / RES 103` Helvetica 8,2 ; +31,1
  `Calques activables; prescriptions completes page 2.` 8,2 ; +41,3 en noir 8,2 `RES = reserve source, modele,
  position ou portee; * = identification a revalider` (formulation courte ; coupée en 2 lignes sur E07). Positions
  = haut de ligne ; baselines exactes 29,815 / 39,952 / 50,089 (+10,137 par ligne).
- Familles à partir de +87 pt, même style qu'en §3.1 ; pas de 22,4 pt sur E02, 22,3 sur E07, 72,7 sur E09/E12.
- Pied 7,0 propre à la feuille : E01 `Materiel existant; quantites physiques reservees pour les deux glyphes
  superposes.`, E02/E07 `Quantites et reserves au bordereau.`, E09/E12 `Reperes source; quantites et reserves au
  bordereau.`, EU02 `Bordereau complet et reserves page 2.`

### 3.3 Variante v6 sans RES (E03, E04, E05, E08 — dont la cible approuvée E08)
Cadres : E03 p.50 470 x 930 pt ; E04 p.52 et E05 p.54 295 x 990 pt ; E08 p.62 235 x 880 pt.
Règle de choix, vérifiée sur les 26 feuilles : **feuille agrégée + palette B + RES non partiel** (aucun repère ou
tous en réserve) → v6. Elle donne exactement E03/E04/E05/E08 ; E11/E14 (palette B mais RES 64 sur 172) et
E01/E06/E09/E12 (palette A) restent en encadré standard (`src/estimer/render/plan.py::encadre_v6`).
- +5,0 `RELEVE E08 - MATERIEL` Helvetica-Bold **14**.
- +28,3 `128 reperes / 22 familles / calques activables` Helvetica **9** — **aucun compteur RES**.
- +43,9 `0 non identifies - 2 identifications a revalider (*)` Helvetica 8,5 (E03/E04/E05 : `0 ... - 0 ...`).
- +56,9 en rouge (0,70 0,10 0,10) Helvetica 8,5 : `5 divergences plan/cedule A RESOUDRE` (E04 : 10, E05 : 6, E08 : 5 ;
  absente sur E03) ; E04/E05 ajoutent en rouge 8,0 `2 calibres distincts dans les sources - voir bordereau`.
- Familles en 1 colonne : glyphe de légende **13 pt** (cercle r 6,5, carré ou losange 13 pt), code Helvetica-Bold
  **10** à x+33, libellé Helvetica **8,7** à x+62, coupé **12 pt avant la quantité** (E08 : 134 pt ; coupe du gold
  mesurée entre 130,5 et 138,7 pt ; E04/E05 194 pt, entre 185,8 et 204,9), ligne modèle **sur E03 seulement** (ex.
  `LEVITON T5820-W` ; aucune sur E04, E05, E08), quantité Helvetica **10** sans `/ Rn` à x+largeur-27 ; pas de 36,6
  (E03), 34,9 (E04/E05), 32,05 pt (E08). Les désignations hors légende portent `[R-001]` (ex. `PLINTHE DE
  CHAUFFAGE [R-001]`).
- Notes de bas Helvetica 8,0 (6 lignes ; 7 sur E08 où `identifie.` est renvoyé) au pas de 10,32 pt, la 1re à
  **71,4 pt** au-dessus du bas du cadre (baseline) quel que soit le nombre de lignes : `PL : rectangles aux
  dimensions graphiques du plan.` / `W et circuits affiches uniquement si verifies.` / `* : identification heritee
  a revalider ; NI : materiel non identifie.` / `Les quantites concernent cette feuille de logements types.` /
  `R-001 : designation conservee au registre des reserves.` (présente sur les 4 feuilles : une famille au moins est
  `(hors legende - R-001)`) / `Modeles, prescriptions et sources : bordereau page 2.`

## 4. Pages de bordereau — 3 formats
Positions x = début du texte d'en-tête de colonne ; y = haut de ligne. Bande d'en-tête remplie (0,90 0,94 0,97) ;
séparateurs horizontaux (0,75 0,79 0,82), aucune ligne verticale. Le format est celui de la feuille (§1), jamais
un format unique pour tout le dossier.

### 4.1 Matériel — 8 colonnes, une ligne par repère (DSI01-08, E02, E07, E10, E13)
- Titre `BORDEREAU MATERIEL - DSI01` Helvetica-Bold 26 (haut y 32,2) ; sous-titres Helvetica 12
  `Quantites representees avec multiplicateurs; portees et composants de chaque ensemble conserves.` et Helvetica 11
  `Les renvois et composants de panneaux ne constituent pas des ensembles supplementaires a additionner.` (p.2).
- Bande d'en-tête de 27 pt ; en-têtes Helvetica-Bold 10 : `Repere / source` x 59 · `Materiel` 232,88 ·
  `Designation` 605,48 · `Qte` 754,52 · `Portee` 841,46 · `Modele` 1065,02 · `Prescription / reserve` 1437,62 ·
  `Parent` 2393,96 (p.2, identiques sur les 12 feuilles).
- Corps Helvetica 9 ; lignes de 65 pt, séparateur 0,4 pt ; **21 lignes par page pleine** (p.2 : 21 séparateurs) ;
  nombre de lignes = nombre de repères (DSI01 : 122 lignes sur 6 pages).
- Fin de la dernière page : bloc `RESERVES ET COMPLEMENTS` Helvetica 10 non gras (p.7, 11, 17, 21, 28, 32, 39, 43, 49,
  61, 69, 77).

### 4.2 Agrégé — 6 colonnes, une ligne par famille (E01, E03-E06, E08, E09, E11, E12, E14)
- Titre `BORDEREAU MATERIEL - E08` Helvetica-Bold **28** (haut y 40,0) ; sous-titres Helvetica 13
  `128 reperes sur cette feuille - prescriptions recopiees du devis et du releve verifie.` et Helvetica 12
  `Les modeles non renseignes restent a preciser. Les circuits divergents exigent une clarification.` (p.63).
- Bande d'en-tête de **30 pt** ; en-têtes Helvetica-Bold 12 : `ID` x 71 · `Qte` 157,24 · `Famille` 231,16 ·
  `Modele / type` 674,68 · `Prescription du devis` 1167,48 · `Source / reserve` 2066,84 (p.45, p.63, p.65).
- Corps Helvetica **11** ; séparateurs **0,5 pt** ; lignes de **66 pt** (p.63 : 22 lignes de 66 pt, de y 178 à
  1630) ; une ligne par famille (E08 p.63 : 22 lignes pour 22 familles) ; 1 page par feuille (E04/E05 : 23 lignes
  resserrées à 63,75 pt).
- Bloc de fin `Notes de reserve source` Helvetica-Bold 12 sur E01, E06, E09, E11, E12, E14 (p.45, 57, 65, 71, 73,
  79) ; **absent sur E03, E04, E05, E08** (p.51, 53, 55, 63).

### 4.3 Travaux / achats — 8 colonnes (EU01-04)
- Titre `BORDEREAU TRAVAUX / ACHATS - EU01` Helvetica-Bold 28 ; un seul sous-titre Helvetica 13
  `31 emplacements de travaux;29 appareils a fournir (configurations a confirmer)` (p.81).
- Bande d'en-tête de 30 pt ; en-têtes Helvetica-Bold 12 : `ID` x 71 · `Famille` 169,56 · `Portee` 539,16 ·
  `Lieux` 773,24 · `A fournir` 945,72 · `Modele` 1130,52 · `Prescription` 1450,84 · `Source / relation` 2017,56.
- Corps Helvetica **9,2** ; séparateurs 0,5 pt ; 1 page par feuille ; bloc de fin `Notes de reserve source`
  Helvetica-Bold 12 (p.81, 83, 85, 87).

## 5. Moteur qui produit ce format
- Parcours canonique : `uv run releve/run.py <NOM>` → `releve/render_vectoriel.py` (étape 4a) →
  `src/estimer/render/` (`from_releve.build` puis `render`) ; `releve/render_pdf.py` (étape 4b) ajoute le rapport de
  métré et le dossier complet sans redessiner de pastille. Constantes : `src/estimer/render/style.py`.
- Choix du format par feuille : `from_releve.sheet_format` (colonne `bordereau` de `feuilles-classement.csv`, sinon
  incendie ou schéma → matériel, toute la feuille en urgence → travaux, autre plan → agrégé) ; tableaux :
  `bordereau.add_bordereau` (matériel) et `bordereau.add_bordereau_agrege` (specs agrégé et travaux).
- Rendu direct : `python -m src.estimer.render <dossier-estimer> <plans.pdf> <sortie.pdf> [--report rapport.json]`.
- Preuve sur le gold (le EXEMPLE.pdf complet est requis : indisponible en bac à sable cloud) :
  ```
  python -m src.estimer.render.from_exemple EXEMPLE.pdf apprentissage/hr26-14-exemplaire/bordereau-materiel.csv \
      apprentissage/hr26-14-exemplaire/feuilles.csv OUT --reserves apprentissage/hr26-14-exemplaire/reserves.md
  python -m src.estimer.render OUT OUT/plans.pdf HR26-14-rendu.pdf --report HR26-14-rendu.report.json
  python -m src.estimer.render.verify_exemple HR26-14-rendu.pdf HR26-14-rendu.report.json EXEMPLE.pdf OUT
  ```
  Résultat du 2026-10-14 : `CALQUES RELEVE 370/370 (actifs 370/370) OK, signets 136/136 OK, renvois 26/26,
  encadres 26/26, lignes de legende 26/26` puis `TOTAL pages 87/87, reperes 2177, cellules 8196/8196 (identiques
  brutes 7887), troncatures 0, spans exacts 9039 (diff 785, info) -> OK` ; marqueurs à 0,001 pt au plus.
  `verify_exemple` compare centres de pastilles, compteurs, légendes et cellules, et depuis le 2026-10-14 : calques
  `RELEVE` de chaque feuille (noms sur la page plan et sur chaque page de bordereau, ordre du panneau, aucun calque
  partagé entre feuilles, 370 actifs), signets (niveau, titre, page des 136 entrées), renvois de page de l'encadré,
  lignes de l'encadré (titre, compteur, renvoi, RES, pied) et lignes de famille de la légende (code, libellé coupé,
  modèle, quantité) : texte, corps, couleur et position à 0,15 pt du coin du cadre. Il **ne compare pas** la forme
  des pastilles ni les calques CAD (§6). Sur le rendu d'avant le 2026-10-14 : `CALQUES RELEVE 89/370 DIFF, signets
  52/136 DIFF, renvois 1/26, encadres 0/26, lignes de legende 4/26 -> FAIL`.

## 6. Écarts restants entre le moteur et le gold (mesurés le 2026-10-05, mis à jour le 2026-10-14)
Rendu comparé : sortie de la preuve §5 (`HR26-14-rendu.pdf`, 87 pages) contre le gold, page par page, avec la même
méthode qu'au §0. Le gold gagne : chaque ligne ci-dessous est un écart à résorber, pas une règle.

| # | Écart | Feuilles | Chiffres | État |
|---|---|---|---|---|
| E1 | Encadré v6 remplacé par l'encadré standard (titre 12, compteur avec RES, glyphes 10 pt, ligne RES et pied standard) | E03, E04, E05, E08 (dont la cible E08) | 4 encadrés sur 26 avant correction | **corrigé** (`plan.encadre_v6` + `draw_box_v6`, règle du §3.3) : preuve gold 87/87, `verify_exemple` exige maintenant l'absence de RES sur ces 4 encadrés (`[128/22/RES None]`). Reste : les lignes rouges `divergences plan/cedule` et `calibres distincts` ne s'affichent que si l'entrée donne le compte (`estimate.json` `sheets[].divergences / calibres`) ; `from_exemple` les lit dans le gold, le relevé de `releve/` ne les produit pas encore → ligne omise sur un dossier réel (essai E08 : 5 au gold, 0 ligne au rendu) |
| E2 | Pastilles triangulaires dessinées en losanges | E01, E06, E09, E12, EU01-04 | 88 pastilles sur 8 feuilles avant correction | **corrigé** (`from_exemple._shape_bbox` reconnaît 3 sommets ; `plan.draw_mark` gère le triangle) : 0 écart de forme après |
| E3 | Renvoi de page de l'encadré : le moteur écrit le numéro absolu (`page 51`), le gold `page 2` partout (la 2e page de la feuille) | 25 feuilles (DSI01 coïncide : son bordereau est la page 2) | 25 encadrés sur 26 avant correction | **corrigé** (le gold gagne, 2026-10-14) : `style.RENVOI_PAGE = 2` pour le renvoi, le renvoi court des cadres empilés, les pieds et le pied v6 ; `verify_exemple` exige le texte du gold : `renvois 26/26` (1/26 avant) |
| E4 | Texte des cellules corrigé au lieu d'être recopié (`corrections_exemple.py` : espaces manquants, troncatures, `Non renseigne`, sources fictives) | 26 feuilles | 309 cellules sur 8196 diffèrent du gold brut (7887 identiques) ; `spans exacts 9039 (diff 785)` | ouvert (choix hérité, à trancher par Francis) |
| E5 | Calques `RELEVE` moins nombreux que dans le gold (le gold a un calque par famille et par feuille + un calque légende par feuille) | 26 feuilles | 89 calques `RELEVE` (132 au total) au lieu de 370 (1670 avec les calques CAD) avant correction ; bordereaux hors calque | **corrigé** (2026-10-14) : `render` crée les calques de chaque feuille (familles dans l'ordre de la légende puis légende, tous actifs) et les pages de bordereau dessinent dans ceux de leur feuille (§2.1) ; enregistrement en `garbage=2` (le niveau 3 refusionnait les calques de même nom). Preuve : `CALQUES RELEVE 370/370 (actifs 370/370) OK`, calques par feuille 26/26 (noms page plan et pages de bordereau, ordre, aucun partagé). Reste : E13 |
| E6 | Signets : `<feuille> - plan` + `Bordereau materiel <feuille>` au lieu de `HR26-14-<feuille>-annote-v<n>` et des signets d'origine | 26 feuilles | 52 signets au lieu de 136 avant correction | **corrigé** (2026-10-14, structure au §1) : `from_exemple` lit projet, version et signets d'origine de chaque feuille dans le gold ; `render` ne les efface plus. Preuve : `signets 136/136 OK` (niveau, titre, page de chaque entrée). Dossier réel (`from_releve`) : préfixe = nom de la soumission (`NOM_PROJET` de `render_vectoriel.py`, `--projet`), v<n> = colonne `version` de `feuilles-classement.csv` si l'agent l'écrit, sinon **v1** (le relevé n'a pas d'autre version par feuille) ; signets d'origine = ceux du PDF source (`inventaire.json`) qui visent la page, avec leurs parents |
| E7 | Hors gold (dossier réel par `from_releve`) : palette B appliquée à **toutes** les feuilles agrégées alors que le gold met E01/E06/E09/E12 en palette A | dossiers réels | règle mesurée le 2026-10-14 (analyse seulement, rien changé) : le titre de feuille du cartouche contient `LOGEMENTS TYPES` sur exactement les 6 feuilles en palette B (E03-E05 `LOGEMENTS TYPES, 1 DE 3` à `3 DE 3`, E08, E11, E14 ; texte vectoriel du dessin à x ≥ 2266, y 1457) et sur aucune des 20 en palette A (`VUES EN PLAN` : DSI01/03/04/05/07, E01, E06, E09, E12, EU01-04 ; `DIAGRAMMES` : DSI02/06/08 ; `UNIFILAIRE ET CEDULES` : E02, E07, E10, E13) : 26/26. Corroborent sans servir de règle : famille PL présente sur 6/6 B et 0/20 A ; 20 à 23 familles sur les B, 4 à 6 sur les agrégées A | **en partie corrigé** : les feuilles agrégées prennent la palette B du gold par code (couleur, forme, taille, §2.3 ; plinthes et linéaires en rectangles du symbole) au lieu de la couleur du relevé et du cercle r 4,1859 ; un code absent de la table garde la couleur du relevé en cercle de 10,88 pt. Choix A/B par feuille : règle candidate « titre du cartouche = logements types → B, sinon A » (lisible par `from_releve` dans la note `cartouche=` du classement), mesurée sur un seul projet : **à valider par Francis avant de l'appliquer** |
| E8 | Anneau blanc de 1 pt autour de chaque pastille ; le gold n'en a pas | 26 feuilles | 2177 pastilles avant correction | **corrigé** (anneau retiré : `plan.draw_halo` et `style.HALO_W` supprimés ; décision de Francis « applique le bon correctif », 2026-10-05) |
| E9 | Hors gold : `from_releve.anchor_sheet` recalait le glyphe `$` (interrupteur S, qui EST le symbole) sur le cercle fermé le plus proche | dossiers réels | essai E08 : 10 CU sur 20 sur les bulles de note 6/8 (15 à 22 pt) | **corrigé** : un jeton sans lettre ni chiffre garde le centre de son glyphe (0 marque déplacée) |
| E10 | Hors gold : un bordereau agrégé plus long que la page (plus de familles ou de texte que le gold) : le gold n'a qu'1 page par feuille | dossiers réels | essai E08 : 25 familles (22 au gold), 3 pages avant | **corrigé, avec un choix** : lignes resserrées comme E04/E05, puis cellules coupées (« ... ») au nombre de lignes qui tient ; le compte est dans `rendu-rapport.json` (`bordereau_troncatures`, 1 sur l'essai E08) et le texte complet reste dans `vecteur/bordereau.csv`. Sur les feuilles v6, ni ligne `RESERVES:` ni bloc `Notes de reserve source` (gold p.51, 53, 55, 63) ; les motifs listés sont ceux des repères en réserve, sans les notes de lieu des autres repères |
| E11 | Lignes de l'encadré standard différentes du gold : cadres de 800 à 999 pt empilés au lieu d'1 ligne (seuil 1000 pt), renvoi long et ligne RES rouge 7,2 dans les cadres empilés au lieu du renvoi court et de la ligne RES courte noire 8,2, pied par défaut au lieu du pied de la feuille, pied 2 pt trop bas ; encadré v6 sans la ligne `R-001` et pied ancré par le bas | 26 feuilles | `encadres 0/26` avant correction (mesure ajoutée le 2026-10-14) | **corrigé** (2026-10-14, règles au §3 et §3.3 : `plan.une_ligne`, `style.HINT_TEXT_PILE` / `WARN_TEXT_PILE`, `FOOTER_UP`, `V6_FOOT_MIN_STEPS`, pied lu dans le gold par `from_exemple`) : `encadres 26/26` (texte, corps, couleur, position à 0,15 pt) |
| E12 | Lignes de famille de la légende différentes du gold : quantité à 48 pt de la fin de cellule sous 390 pt (gold 74), 1re ligne d'un libellé coupé remontée de 3,6 pt et 2e ligne à 7,2 (gold 7,4498), pas de colonne recalculé (DSI02 666,7 au lieu de 500), `(hors legende - R-001)` au lieu de `[R-001]`, coupe v6 trop large, lignes modèle sur E04/E05/E08 | 22 feuilles (dont 9 par le texte) | `lignes de legende 4/26` avant correction | **corrigé** (2026-10-14, règles au §3) : `lignes de legende 26/26` (code, libellé, modèle, quantité à 0,15 pt) |
| E13 | Calques CAD : `from_exemple` enregistre `plans.pdf` en `garbage=3`, qui fusionne les calques CAD de même nom des 26 plans ; panneau des calques : le gold intercale les calques `RELEVE` de chaque feuille après les groupes CAD de son fichier (artefact de l'assemblage des 26 fichiers `...-annote-v<n>.pdf`), le moteur les met tous après les groupes CAD | 26 feuilles | gold 1670 calques (1300 CAD) ; rendu 413 (370 `RELEVE` + 43 CAD) ; ordre `RELEVE` par feuille identique au gold (26/26) | ouvert (hors moteur pour le compte CAD : entrée de la preuve ; sans effet sur les calques `RELEVE`) |

Rayons : les cercles DSI du moteur sont à 4,1859 pt comme le gold (écart de centre ≤ 0,001 pt, arrondi à la
2e décimale seulement : 4,18 / 4,19).
