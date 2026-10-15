# STATUT — TEST-E201 (Bibliothèque Georgette-Lepage, SP-GTER-26-0080, feuille E-201)

Date : 2026-10-15 · État : **EN VALIDATION** (Francis pointe les corrections dans le visualiseur ; 10 épingles au commit)

- Entrée : E-001 (légende) et E-201 (plan) en PNG raster → PDF A1 (pas de couche texte).
- Relevé : 121 repères, 20 familles, `conforme=True` — session interactive Claude Fable 5.1 (route « session = agent »), OpenCV pour l'appariement des symboles répétitifs.
- Rendu : pastilles carrées/rectangulaires alignées sur le symbole (colonne `angle_deg`, commit b41eb29) ; livraison **PNG** (calque alpha + plan annoté), PDF conservé pour archive.
- Épingles de Francis (10, 11:35-11:41) : M02-01…06 + M04-28, M07-04 « cercle trop gros, pas aligné », M04-04, M04-01 → **appliquées** 12:05 : 46 cercles ajustés par Hough (rayon = symbole, colonne `rayon_pt`, plancher 2,6 pt), 4 boîtes orientées, 6 rectangles 'x4 recentrés sur le contour (le remplissage mi-noir biaisait le centroïde). Balayage visuel complet après rendu : conforme. Reste : rail M06 marqué par un point, pas sur sa longueur (R-008).
- Critère d'acceptation : étape 1 (aveugle), aucune référence estimateur → vérification incomplète.
