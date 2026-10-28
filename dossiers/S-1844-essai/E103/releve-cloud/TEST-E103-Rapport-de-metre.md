# Rapport de métré (par plans) — TEST-E103

Généré le 2026-10-19 par le pipeline `releve/` (relevé automatique Claude + scripts déterministes). Chaque marque est une occurrence relevée sur le plan (étiquette texte vectorielle ou lecture visuelle) ; les quantités sont des comptes d'objets, sans métrage de câble.

## Résumé

| Feuille | Marques | Libellés |
|---|--:|--:|
| E103 | 23 | 2 |
| **Total** | **23** | **2** |

## Tous les plans

| Libellé | Famille | Quantité |
|---|---|--:|
| BOITIER NLIGHT | commande | 20 |
| INTERRUPTEUR NLIGHT | commande | 3 |

## E103

| Libellé | Ce plan | Tous les plans |
|---|--:|--:|
| BOITIER NLIGHT | 20 | 20 |
| INTERRUPTEUR NLIGHT | 3 | 3 |

## Nomenclature (libellé → source de la lecture)

| Libellé | Famille | Description | Source |
|---|---|---|---|
| BOITIER NLIGHT | commande | BOITIER DE CONTROLE NLIGHT (DP1 NPP16 D EFP 347 / DP2 NPP PCD EFP / PP1 NPP20 PL BP / SO3-SO4 WSXA MWO PDT) | E-001 légende ; bloc S004 |
| INTERRUPTEUR NLIGHT | commande | INTERRUPTEUR MURAL NLIGHT (SW1 NPODMA WH / SW6 NPOD TOUCH WH) | E-001 légende ; bloc S059 |

# Méthode et constats de l'agent

# Rapport de relevé — S-1902 Bibliothèque Georgette-Lepage (SP-GTER-26-0080, HF experts-conseils 26-29)

Entrée : P-D Électricité_2026-09-22.pdf, 21 feuilles A1 vectorielles. Méthode : blocs vectoriels (R-001). 23 occurrences, 2 familles.

| feuille | occurrences |
|---|--:|
| E103 | 23 |

| famille | total | portées |
|---|--:|---|
| BOITIER NLIGHT | 20 | CONSERVER 20 |
| INTERRUPTEUR NLIGHT | 3 | CONSERVER 3 |

Étiquetage des signatures : automatique-mcp. Outils déterministes : prepare.py, blocs_vectoriels.py, blocs_vignettes.py, blocs_vers_releve.py, controle_qualite.py.

**STATUT : relevé automatique à VÉRIFIER sur les planches de contrôle avant chiffrage.**

# Réserves

# Réserves — relevé par blocs vectoriels (blocs_vectoriels.py → blocs_vers_releve.py)

## R-001 — Méthode
Chaque symbole est un bloc CAO ; les blocs de même signature (invariante à la position, la rotation et l'échelle, lettre contenue incluse) sont étiquetés une fois (`blocs-familles.csv`, planches `signatures-NN.png`), puis chaque instance devient une occurrence au centre exact du bloc, avec sa boîte tournée. Validé sur E-201 contre le relevé vérifié TEST-E201 : 116/121 repères retrouvés à ≤ 5 pt, précision par signature 34/34, 17/17, 11/11.

## R-002 — Portée
E.A.E → ENLEVER, E.A.R → RELOCALISER, E.A.C → CONSERVER lus à ≤ 14 pt du bloc ; sans étiquette : CONSERVER sur une feuille EXISTANT/DÉMOLITION, INSTALLER sur une feuille NOUVEAU — sauf luminaire sans lettre de type sur feuille NOUVEAU (existant dessiné pour contexte → CONSERVER). À confirmer famille par famille sur les planches de contrôle.

## R-003 — Luminaires typés (E-203/E-204)
L'unité est l'ÉTIQUETTE (A1, C1, C1_1, C1_3, E) : une rangée linéaire « C1 + C1_1 » = 2 modules. E-203 : A1 11, C1 12, C1_1 6, C1_3 15 = tableau E-008 et relevé d'éclairage du 2026-10-07. LUMINAIRE E : 3 étiquettes sur bloc (l'estimation en compte 4) — à trancher au zoom.

## R-005 — Pictogrammes (instances manuelles, `blocs-instances.csv`)
Enseignes Z6 (3, tracé pointillé : confirmer neuf — E-008 en liste 3), détecteurs de fumée (3 existants pointillés + neufs pleins), encastrés sur circuit d'urgence PP-U1 (quart noir). Les pictogrammes ont des signatures uniques (courbes, remplissages), ils ne se regroupent pas automatiquement.

## Q12 — familles par type sur une même ligne de légende (justification)
HORS LEGENDE (encastré) → ENCASTRE (existant), ENCASTRE URGENCE (quart noir, circuit PP-U1) et LUMINAIRE E (type E du tableau E-008) ; HORS LEGENDE ('x4) → LED 1X4 (existant) et LUMINAIRE A1 (type A1 neuf) ; HORS LEGENDE (prise double 15 A) → PRISE DOUBLE 15A, HORS LEGENDE (symbole « USB ») → PRISE USB. Une famille par type de luminaire est voulue : le chiffrage est par type (E-008), pas par symbole (règle R7 : nommer comme la légende/le tableau).

## R-007 — Prises (cercles vectoriels, feuilles E-10x)
Détectées au niveau de la partie (cercle fermé 3,3–5 pt, trait ≥ 0,35 pt) parce que deux prises côte à côte ou une prise collée à une sortie data fusionnent en un seul bloc. PRISE DDFT = cercle contenant une partie remplie (légende : demi-cercle plein = DDFT ; barre pleine = M.A.L.T. isolée — les deux variantes tombent ici dans PRISE DDFT, à départager au zoom) ; PRISE DOUBLE 15A = cercle traversé d'au moins un trait (15 A et 20 A non distingués : le crochet 20 A est un petit trait à côté du cercle, à vérifier sur les planches). Comptoir/standard non distingués (même cercle, trait de comptoir à côté).

## Q14 — code PU (PRISE USB)
`code_attendu` donne PC pour la description « PRISE DE COURANT DOUBLE 15A- 120V TYPE Leviton Decora USB » (HORS LEGENDE), déjà pris par PRISE DOUBLE 15A (HORS LEGENDE) ; le bordereau groupant par (code, portée), PU est conservé pour ne pas fondre 20 USB et 23 prises ordinaires en une ligne.

## R-006 — Hors relevé
Sorties data : triangle plein ≤ 6,5 pt seulement (les grandes flèches sont des renvois de circuit). Cercles nus, bulles d'axes, numéros de locaux, mobilier : ignorés. Longueurs de conduits/filage : hors relevé (estimation du 2026-10-08). Panneaux E-501/E-502, schémas E-006/E-007 : non relevés (tableaux).
