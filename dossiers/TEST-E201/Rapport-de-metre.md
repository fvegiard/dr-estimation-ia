# Rapport de métré (par plans) — TEST-E201

Généré le 2026-10-15 par le pipeline `releve/` (relevé automatique Claude + scripts déterministes). Chaque marque est une occurrence relevée sur le plan (étiquette texte vectorielle ou lecture visuelle) ; les quantités sont des comptes d'objets, sans métrage de câble.

## Résumé

| Feuille | Marques | Libellés |
|---|--:|--:|
| E201 | 121 | 20 |
| **Total** | **121** | **20** |

## Tous les plans

| Libellé | Famille | Quantité |
|---|---|--:|
| ACCUMULATEUR | secours | 1 |
| AVERTISSEUR FUMEE 120V CO | alarme | 4 |
| BOITE JONCTION | distribution | 2 |
| BOITIER C | autre | 4 |
| CERCLE SANS ETIQUETTE | luminaire | 2 |
| DETECTEUR FUMEE | alarme | 1 |
| DETECTEUR MOUVEMENT | commande | 3 |
| ENCASTRE | luminaire | 28 |
| ENSEIGNE SORTIE MUR | secours | 5 |
| ENSEIGNE SORTIE PLAFOND | secours | 2 |
| HP ENCASTRE PLAFOND | alarme | 2 |
| INT 3 VOIES | commande | 5 |
| INT MAITRES | commande | 1 |
| INT SIMPLE | commande | 2 |
| LED 1X4 | luminaire | 6 |
| LED 2X2 | luminaire | 45 |
| PANNEAU ANNONCIATEUR | alarme | 1 |
| PIEZO STROBE | alarme | 2 |
| RAIL ECLAIRAGE | luminaire | 2 |
| STATION MANUELLE | alarme | 3 |

## E201

| Libellé | Ce plan | Tous les plans |
|---|--:|--:|
| ACCUMULATEUR | 1 | 1 |
| AVERTISSEUR FUMEE 120V CO | 4 | 4 |
| BOITE JONCTION | 2 | 2 |
| BOITIER C | 4 | 4 |
| CERCLE SANS ETIQUETTE | 2 | 2 |
| DETECTEUR FUMEE | 1 | 1 |
| DETECTEUR MOUVEMENT | 3 | 3 |
| ENCASTRE | 28 | 28 |
| ENSEIGNE SORTIE MUR | 5 | 5 |
| ENSEIGNE SORTIE PLAFOND | 2 | 2 |
| HP ENCASTRE PLAFOND | 2 | 2 |
| INT 3 VOIES | 5 | 5 |
| INT MAITRES | 1 | 1 |
| INT SIMPLE | 2 | 2 |
| LED 1X4 | 6 | 6 |
| LED 2X2 | 45 | 45 |
| PANNEAU ANNONCIATEUR | 1 | 1 |
| PIEZO STROBE | 2 | 2 |
| RAIL ECLAIRAGE | 2 | 2 |
| STATION MANUELLE | 3 | 3 |

## Nomenclature (libellé → source de la lecture)

| Libellé | Famille | Description | Source |
|---|---|---|---|
| ACCUMULATEUR | secours | Rectangle + - (R-009). | E-001 legende ; E-201 plan |
| AVERTISSEUR FUMEE 120V CO | alarme | Cercle 3/4 noir (R-004). | E-001 legende ; E-201 plan |
| BOITE JONCTION | distribution | Carre X en tete de rail. | E-001 legende ; E-201 plan |
| BOITIER C | autre | C dans carre, hors legende. | E-001 legende ; E-201 plan |
| CERCLE SANS ETIQUETTE | luminaire | Cercle simple ~8 pt sans etiquette ni circuit (R-005). | E-001 legende ; E-201 plan |
| DETECTEUR FUMEE | alarme | Cercle 1/2 noir (R-004). | E-001 legende ; E-201 plan |
| DETECTEUR MOUVEMENT | commande | Ovale DM. | E-001 legende ; E-201 plan |
| ENCASTRE | luminaire | Cercle + croix. Variante pleine = PP-U1 (urgence) : en designation. | E-001 legende ; E-201 plan |
| ENSEIGNE SORTIE MUR | secours | Cercle X mi-noir sur tige. | E-001 legende ; E-201 plan |
| ENSEIGNE SORTIE PLAFOND | secours | Cercle X mi-noir avec fleche, sans tige. | E-001 legende ; E-201 plan |
| HP ENCASTRE PLAFOND | alarme | Cercle avec carre. | E-001 legende ; E-201 plan |
| INT 3 VOIES | commande | $ avec 3 ; lettre de zone en designation. | E-001 legende ; E-201 plan |
| INT MAITRES | commande | $ dans un carre + bulle 1 ; note specifique 1 : a relocaliser. | E-001 legende ; E-201 plan |
| INT SIMPLE | commande | $ seul. | E-001 legende ; E-201 plan |
| LED 1X4 | luminaire | Rectangle a diagonale ; variante mi-noire = PP-U1 (urgence) en designation. | E-001 legende ; E-201 plan |
| LED 2X2 | luminaire | Carre a diagonale. Variante mi-noire = alimente par PP-U1 (urgence) : en designation. | E-001 legende ; E-201 plan |
| PANNEAU ANNONCIATEUR | alarme | ANN dans carre ; E.A.R. | E-001 legende ; E-201 plan |
| PIEZO STROBE | alarme | F dans carre avec rayons. | E-001 legende ; E-201 plan |
| RAIL ECLAIRAGE | luminaire | Rail courbe avec tetes orientables ; 1 repere par rail, nb de tetes en designation (R-008). | E-001 legende ; E-201 plan |
| STATION MANUELLE | alarme | F dans carre. | E-001 legende ; E-201 plan |

# Méthode et constats de l'agent

# Rapport de relevé — E-201 « ÉCLAIRAGE ET ALARME INCENDIE — EXISTANT/DÉMOLITION — REZ-DE-CHAUSSÉE »

**Projet** : Technologie RFID — Bibliothèque Georgette-Lepage, Brossard — SP-GTER-26-0080 (HF experts-conseils, dossier 26-29)
**Feuilles** : E-001 (légende et liste de plans, rôle `legende`), E-201 (plan, échelle 1:100, émission 01 2026-09-16 « émis pour appel d'offre »)
**Entrée** : 2 pages PNG (7946 × 5613 px) converties en PDF A1 raster — aucune couche texte, relevé 100 % visuel.
**Dossier de travail** : `OUTBOX/TEST-E201/travail`

## 1. Méthode
1. Classement : E-001 `legende`, E-201 `plan` (feuille existant/démolition ; zones grises hors portée, R-002).
2. Légende d'abord : les sections ÉCLAIRAGE, ALARME INCENDIE, ÉCLAIRAGE D'URGENCE de E-001 lues au zoom et
   transcrites dans `legende.csv` (42 lignes, 20 comptées, 22 absentes avec zone vérifiée).
3. Appareils répétitifs (2'×2', encastrés) : appariement de gabarit sur le raster (OpenCV), puis lecture de
   chaque étiquette sur des planches de vignettes (72 vignettes) pour `designation` et `portee` (R-003).
4. Autres appareils : grille de 30 zooms de 170 × 130 pt (règles graduées) sur toute la zone blanche ; coordonnées
   interpolées entre graduations, centre du symbole.
5. Contrôle : `controle_qualite.py` → conforme.

## 2. Totaux E-201 (121 repères, 20 familles)

| Code | Famille | Conserver | Enlever | Relocaliser | À préciser | Total |
|---|---|--:|--:|--:|--:|--:|
| L2 | Appareil d'éclairage 2'×2' LED (dont 7 sur PP-U1) | 37 | 8 | | | 45 |
| EN | Appareil d'éclairage encastré (cercle + croix, dont 6 sur PP-U1) | 9 | 19 | | | 28 |
| EC | Cercle simple sans étiquette (R-005) | | | | 2 | 2 |
| LX | Appareil d'éclairage 'x4' (dont 3 sur PP-U1) | | 6 | | | 6 |
| RL | Rail d'éclairage (5 + 3 têtes, R-008) | | 2 | | | 2 |
| I3 | Interrupteur à 3 voies | 4 | 1 | | | 5 |
| IS | Interrupteur simple | 2 | | | | 2 |
| DM | Détecteur de mouvement | 2 | 1 | | | 3 |
| IM | Interrupteurs maîtres — note 1 (R-007) | | | 1 | | 1 |
| BC | Boîtier « C » hors légende (R-006) | 3 | 1 | | | 4 |
| EM | Enseigne de sortie au mur | 4 | 1 | | | 5 |
| EP | Enseigne de sortie au plafond | 2 | | | | 2 |
| AC | Accumulateur (R-009) | 1 | | | | 1 |
| SM | Station manuelle | 3 | | | | 3 |
| PZ | Piezo combiné à un strobe | 2 | | | | 2 |
| AF | Avertisseur de fumée 120 V CO (R-004) | 3 | | 1 | | 4 |
| DF | Détecteur de fumée (R-004) | 1 | | | | 1 |
| HP | Haut-parleur encastré au plafond | 2 | | | | 2 |
| ANN | Panneau annonciateur | | | 1 | | 1 |
| BJ | Boîte de jonction (tête de rail) | | 2 | | | 2 |
| | **Total** | **75** | **41** | **3** | **2** | **121** |

Circuits lus en `designation` : PP-2 3/5/6, PP-U1 2/7, P-2 39/41 ; zones (h,i)/(j,k)/(n)/(Mf)/(Ma).

## 3. Contrôles
- Décompte croisé 2'×2' : 44 appariements + 1 lecture manuelle = 45 ; 3 faux candidats écartés au zoom.
- Encastrés : 28 appariements, aucun doublon à < 4 pt ; 6 pleins (PP-U1) confirmés par mesure d'anneau et par
  l'étiquette PP-U1 lue sur la vignette.
- Chaque label des occurrences existe dans `nomenclature.csv` ; chaque famille cite sa ligne de légende.
- Aucune coordonnée sur grille mentale (Q10) : positions issues des centroïdes raster ou interpolées.

## 4. Ce qui n'a pas pu être relevé
- Neuf : sur E-203 (non fournie). Luminaires des zones grises : hors portée (R-002).
- Longueurs des rails : estimées depuis 1:100, à métrer (R-008).
- Distinction avertisseur/détecteur de fumée : par proportion de noir, à confirmer (R-004).
- Aucun devis, addenda ni référence d'estimateur : vérification incomplète au sens du critère d'acceptation.

## 5. Outils et modèle
Session interactive (route « session = agent », CLAUDE.md §Agents), modèle **Claude Fable 5.1** (observé dans le
contexte système). `prepare.py`, `zoom.py` (≈ 50 zooms), OpenCV (appariement de gabarit), `controle_qualite.py`.
`traits.py` inutilisable (entrée raster).

**STATUT : relevé complet de l'existant/démolition de E-201 ; À VÉRIFIER pour R-004, R-005, R-006, R-009.**


# Réserves

# Réserves — E-201 (Bibliothèque Georgette-Lepage, SP-GTER-26-0080)

Dossier de travail : `OUTBOX/TEST-E201/travail`. Entrée : deux pages PNG (E-001 légende, E-201 plan) converties en PDF
raster A1 (841 × 594 mm = 2383,9 × 1683,8 pt, image 7946 × 5613 px). Aucune couche texte : tout le relevé est visuel.

## R-001 — Feuille EXISTANT/DÉMOLITION : tout est existant, la portée vient des étiquettes
Cartouche E-201 : « ÉCLAIRAGE ET ALARME INCENDIE — EXISTANT/DÉMOLITION — REZ-DE-CHAUSSÉE ». Note générale 1 : « sauf
indications contraires, tous les équipements sont existants à conserver ». Portées appliquées : `CONSERVER` par défaut,
`ENLEVER` quand l'étiquette E.A.E est lue à côté du symbole, `RELOCALISER` pour E.A.R (abréviations de E-001). Aucun
appareil neuf sur cette feuille ; le neuf est sur E-203 (non fournie). `materiel` porte EXISTANT (règle R11).

## R-002 — Zones grises non relevées
Les zones grisées (bibliothèque adultes 115, salle d'animation 108, secteur jeunesse 118, moitié sud) sont hors
portée : aucun appareil n'y est dessiné en noir. Zone relevée : x 300-1270 / y 150-990 pt (bureaux 110.x, hall 107,
réception 110.18, corridor 110.12, aide au lecteur 116, escaliers, ascenseur).

## R-003 — Luminaires 2'×2' : 45 appariés par gabarit raster, 1 ajouté à la main
44 carrés à diagonale trouvés par appariement de gabarit (score ≥ 0,81) sur le raster, 1 ajouté après balayage
(réception des marchandises, 1026 ; 370 — texte superposé). Les 3 candidats à score 0,55-0,56 ont été vérifiés
au zoom : vides (pas de symbole). Les 28 encastrés (cercle + croix) : 28 appariés (score ≥ 0,74), classés
pleins/vides par mesure de l'anneau (noir < 120 → PP-U1). Étiquettes (PP-2 3, PP-U1 2, (h,i)/(j,k)/(n)/(Mf)/(Ma),
E.A.E) lues une à une sur 3 planches de 25 vignettes.

## R-004 — Avertisseur 120 V CO (3/4 noir) vs détecteur de fumée (1/2 noir)
Les 5 petits cercles (4,6 pt) ont été mesurés sur le raster : 86-92 % noir pour 4 d'entre eux → ligne A03
« avertisseur de fumée à ionisation 120 V combiné CO » ; 63 % pour celui de l'ascenseur (1146 ; 513) → A04
« détecteur de fumée ». La lecture repose sur la proportion de noir d'un symbole de 4,6 pt : **à confirmer** par
l'estimateur sur le plan vectoriel. L'avertisseur (882 ; 704) porte E.A.R → RELOCALISER.

## R-005 — Deux cercles simples sans étiquette (905 ; 656) et (1083 ; 575)
Cercles noirs ~8 pt dans le corridor, sans PP ni circuit ni E.A.E. La légende L04 « appareil d'éclairage encastré »
est un cercle simple, mais tous les autres encastrés de la feuille portent une croix et une étiquette. Relevés sous
« CERCLE SANS ETIQUETTE », portée `A PRECISER`. À trancher : luminaire ou symbole architectural.

## R-006 — Boîtier « C » (4 occurrences) hors légende
Carré portant « C », toujours près d'une porte (1143 ; 334), (1109 ; 367), (1017 ; 542), (582 ; 816 — E.A.E).
Absent des légendes E-001 (ni ÉLECTRICITÉ, ni ALARME INCENDIE/INTRUSION, ni SERVICES). Relevé sous « BOITIER C »,
famille `autre`, matériel suffixé (hors legende). À identifier (contact de porte ? bouton de sortie ?).

## R-007 — Interrupteurs maîtres (note spécifique 1)
Symbole « $ » dans un carré avec bulle 1 et E.A.R à (1003 ; 552). Note spécifique 1 : « Interrupteurs maîtres, à
relocaliser. Tout l'éclairage de la zone principale du hall est commandé à partir de ce panneau. Système de
dénomination : Ma (Main a). » Relevé 1 repère `RELOCALISER`, hors légende. Les suffixes (Ma)/(Mf) des encastrés
renvoient à ce système.

## R-008 — Rails d'éclairage : quantité = 2 rails, têtes en désignation
Deux rails courbes (P-2 39 : 5 têtes, ~125 pt ≈ 4,4 m à 1:100 ; P-2 41 : 3 têtes, ~55 pt ≈ 1,9 m), tous deux
E.A.E. Longueur estimée depuis l'échelle 1:100 du cartouche (1 pt = 0,0353 m) : **à métrer** avant chiffrage.
Boîte de jonction (carré X) en tête de chaque rail relevée séparément (S01).

## R-009 — Accumulateur (476 ; 610) sans étiquette
Rectangle « + − » avec un petit cercle accolé, à l'entrée du bureau 110.5. Relevé sous U04 « ACCUMULATEUR »,
`CONSERVER` (aucune mention E.A.E lue). Le petit cercle pourrait indiquer un phare : à confirmer.

## R-010 — Lignes de légende absentes
L02 (rectangle sans description), L03 réglette 4', L08 gradateur, L09 mural, L10/L11 réglettes murales, L13
(hachuré, sans description), L15 347 V, L17 daylight, A02, A05, A07, A08, A10-A13, U03, U05-U10 : cherchées sur toute
la zone blanche, aucune occurrence. Les sections SERVICES, DISTRIBUTION, CHAUFFAGE, FORCE MOTRICE de E-001 ne
s'appliquent pas à une feuille d'éclairage/alarme (seule S01 boîte de jonction y figure).

## R-011 — Limites du relevé
- Entrée raster (PNG), pas le PDF vectoriel : `traits.py` inutilisable, coordonnées lues sur les règles des
  zooms (précision ≈ ±1 pt) et par centroïde raster pour les appariements.
- Aucun devis ni addenda fourni : colonne `modele` = EXISTANT CONSERVE - MODELE NON INDIQUE.
- Aucune référence d'estimateur : critère d'acceptation à l'étape 1 (identification à l'aveugle),
  **vérification incomplète**.
- Modèle exécutant ce relevé : Claude Fable 5.1 (session interactive, route « session = agent » de CLAUDE.md).
