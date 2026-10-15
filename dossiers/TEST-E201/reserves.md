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
