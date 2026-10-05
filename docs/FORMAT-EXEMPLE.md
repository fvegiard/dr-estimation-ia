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
61 pages de bordereau = 87 pages. Signets du gold : un signet de niveau 1 `HR26-14-<feuille>-annote-v<n>` par
feuille, sur la page plan (ex. `HR26-14-E03-annote-v6` p.50, `HR26-14-E08-annote-v1` p.62), plus les signets
d'origine des plans (136 entrées au total).

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
  feuille** plus `RELEVE - Legende et avertissements` par feuille, soit 344 + 26 = **370 calques `RELEVE`** sur les
  1670 calques du gold.
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
  en palette B.

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
  E10/E13 `Reperes source; quantites et reserves au bordereau.` ; EU01/EU04 `Emplacements de travaux sur calques;
  achats, prescriptions et reserves detaillees page 2.` ; EU03 `Bordereau complet et reserves page 2.`

### 3.2 Standard « empilé » (7 feuilles : DSI03, E01, E02, E07, E09, E12, EU02)
Ex. E01 p.44 et E09 p.64 : 780 x 320 pt (2 colonnes) ; E02 p.46 : 390 x 705 (1 colonne) ; DSI03 p.12 : 360 x 900.
- +3,2 titre Helvetica-Bold 12 ; +21,0 `103 reperes / 6 familles / RES 103` Helvetica 8,2 ; +31,1
  `Calques activables; prescriptions completes page 2.` 8,2 ; +41,3 en noir 8,2 `RES = reserve source, modele,
  position ou portee; * = identification a revalider` (formulation courte).
- Familles à partir de +87 pt, même style qu'en §3.1 ; pas de 22,4 pt sur E02, 22,3 sur E07, 72,7 sur E09/E12.
- Pied 7,0 propre à la feuille : E01 `Materiel existant; quantites physiques reservees pour les deux glyphes
  superposes.`, E02/E07 `Quantites et reserves au bordereau.`, E09/E12 `Reperes source; quantites et reserves au
  bordereau.`, EU02 `Bordereau complet et reserves page 2.`

### 3.3 Variante v6 sans RES (E03, E04, E05, E08 — dont la cible approuvée E08)
Cadres : E03 p.50 470 x 930 pt ; E04 p.52 et E05 p.54 295 x 990 pt ; E08 p.62 235 x 880 pt.
- +5,0 `RELEVE E08 - MATERIEL` Helvetica-Bold **14**.
- +28,3 `128 reperes / 22 familles / calques activables` Helvetica **9** — **aucun compteur RES**.
- +43,9 `0 non identifies - 2 identifications a revalider (*)` Helvetica 8,5 (E03/E04/E05 : `0 ... - 0 ...`).
- +56,9 en rouge (0,70 0,10 0,10) Helvetica 8,5 : `5 divergences plan/cedule A RESOUDRE` (E04 : 10, E05 : 6, E08 : 5 ;
  absente sur E03) ; E04/E05 ajoutent en rouge 8,0 `2 calibres distincts dans les sources - voir bordereau`.
- Familles en 1 colonne : glyphe de légende **13 pt** (cercle r 6,5, carré ou losange 13 pt), code Helvetica-Bold
  **10** à x+33, libellé Helvetica **8,7** à x+62 (renvoyé à la ligne ; E03 ajoute une ligne modèle, ex.
  `LEVITON T5820-W`), quantité Helvetica **10** sans `/ Rn` ; pas de 36,6 (E03), 34,9 (E04/E05), 32,05 pt (E08).
  Les désignations hors légende portent `[R-001]` (ex. `PLINTHE DE CHAUFFAGE [R-001]`).
- Notes de bas Helvetica 8,0 (6 lignes) : `PL : rectangles aux dimensions graphiques du plan.` / `W et circuits
  affiches uniquement si verifies.` / `* : identification heritee a revalider ; NI : materiel non identifie.` /
  `Les quantites concernent cette feuille de logements types.` / `R-001 : designation conservee au registre des
  reserves.` / `Modeles, prescriptions et sources : bordereau page 2.`

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
- Corps Helvetica **11** ; séparateurs **0,5 pt** ; une ligne par famille (E08 p.63 : 22 lignes pour 22 familles) ;
  1 page par feuille.
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
  Résultat du 2026-10-05 : `TOTAL pages 87/87, reperes 2177, cellules 8196/8196 (identiques brutes 7887),
  troncatures 0, spans exacts 9039 (diff 785, info) -> OK` ; marqueurs à 0,001 pt au plus. `verify_exemple` compare
  centres de pastilles, compteurs, légendes et cellules : il **ne compare pas** la forme des pastilles ni la mise en
  page de l'encadré (d'où le §6).

## 6. Écarts restants entre le moteur et le gold (mesurés le 2026-10-05)
Rendu comparé : sortie de la preuve §5 (`HR26-14-rendu.pdf`, 87 pages) contre le gold, page par page, avec la même
méthode qu'au §0. Le gold gagne : chaque ligne ci-dessous est un écart à résorber, pas une règle.

| # | Écart | Feuilles | Chiffres | État |
|---|---|---|---|---|
| E1 | **Encadré v6 remplacé par l'encadré standard** : titre 12 au lieu de 14 ; compteur `N reperes / F familles / RES N` au lieu de `... / calques activables` ; lignes `non identifies / identifications a revalider`, `divergences plan/cedule A RESOUDRE` et `calibres distincts` absentes ; glyphes de légende 10 pt au lieu de 13 ; code 8,2 / libellé 6,6 / quantité 7,1 pt au lieu de 10 / 8,7 / 10 ; ligne RES et pied standard au lieu des 6 notes v6 | E03, E04, E05, E08 (dont la cible E08) | 4 encadrés sur 26 ; RES affiché 126 / 112 / 116 / 128 là où le gold n'en a pas ; divergences non affichées 10 / 6 / 5 (E04 / E05 / E08) ; 57 glyphes de légende r 5,0 au lieu de r 6,5 (13 + 15 + 15 + 14). Mêmes cadres (470 x 930, 295 x 990, 295 x 990, 235 x 880) et mêmes pastilles sur le plan | **ouvert** — reproduire v6 demande des données que l'entrée du moteur n'a pas (`non identifies`, `divergences plan/cedule`, `calibres distincts` n'existent ni dans `estimate.json` ni dans le relevé de `releve/`) : décision de schéma hors de la portée de la PR de réalignement |
| E2 | Pastilles triangulaires dessinées en losanges | E01, E06, E09, E12, EU01-04 | 88 pastilles sur 8 feuilles avant correction | **corrigé** (`from_exemple._shape_bbox` reconnaît 3 sommets ; `plan.draw_halo` gère le triangle) : 0 écart de forme après |
| E3 | Renvoi de page de l'encadré : le moteur écrit le numéro absolu (`page 51`), le gold `page 2` partout (la 2e page de la feuille) | 25 feuilles (DSI01 coïncide : son bordereau est la page 2) | 25 encadrés sur 26 | ouvert (choix hérité du moteur, à trancher par Francis) |
| E4 | Texte des cellules corrigé au lieu d'être recopié (`corrections_exemple.py` : espaces manquants, troncatures, `Non renseigne`, sources fictives) | 26 feuilles | 309 cellules sur 8196 diffèrent du gold brut (7887 identiques) ; `spans exacts 9039 (diff 785)` | ouvert (choix hérité, à trancher par Francis) |
| E5 | Calques `RELEVE` moins nombreux que dans le gold (le gold a un calque par famille et par feuille + un calque légende par feuille) | 26 feuilles | 89 calques `RELEVE` (132 au total) au lieu de 370 (1670 avec les calques CAD) | ouvert |
| E6 | Signets : `<feuille> - plan` + `Bordereau materiel <feuille>` au lieu de `HR26-14-<feuille>-annote-v<n>` et des signets d'origine | 26 feuilles | 52 signets au lieu de 136 | ouvert |
| E7 | Hors gold (dossier réel par `from_releve`) : palette B appliquée à **toutes** les feuilles agrégées (couleur du relevé) alors que le gold met E01/E06/E09/E12 en palette A ; cercle par défaut r 4,1859 sur toutes les feuilles quand le symbole n'est pas ancré, alors que le gold utilise 5,0231 et plus sur les feuilles E/EU | dossiers réels | non mesurable sur le gold (le gold n'a pas de règle écrite pour choisir la palette) | ouvert |

Rayons : les cercles DSI du moteur sont à 4,1859 pt comme le gold (écart de centre ≤ 0,001 pt, arrondi à la
2e décimale seulement : 4,18 / 4,19).
