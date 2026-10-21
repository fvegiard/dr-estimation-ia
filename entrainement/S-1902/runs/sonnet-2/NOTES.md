# NOTES — chiffrage à l'aveugle S-1902 (méthode Dupuis)

**Modèle ayant produit ce travail : Claude Sonnet 5.5** (claude-sonnet-5-5), sans sous-agent, en lisant uniquement le kit du dossier.

## Résultat (chiffrage.json, produit par chiffrage.py, code de sortie 0, sortie identique sur deux exécutions)
- Matériel 59 569,54 $ (dont lots 27 343 $) ; heures relevées 948,69 h -> chargées 950 h ; MO 950 x 85 = 80 750 $
- Total ACCEO 140 319,54 $ ; facteur 1,244 ; prix de vente 175 000 $ ; 89 lignes
- Contrôles dans le script : matériel + heures chargées x taux = total ACCEO ; prix de vente = arrondi au millier ; Σ par article = totaux ; lots = lignes LOT-*.

## Hypothèses principales
1. Taux 85 $/h (METHODE : dossiers août–octobre 2026), pas les 124 $/h du Sommaire d'Estimation_2. Facteur 1,244.
2. Quantités sur plan = relevé : totaux de releve.xlsx recoupés avec les portées de rapport-releve.md (le classeur n'a pas de portée par marque). INSTALLER -> matériel + temps ; ENLEVER -> temps de dépose ; RELOCALISER -> temps de relocalisation ; CONSERVER -> rien. Le relevé est marqué « à vérifier sur les planches » : non vérifié ici (pas d'accès aux plans).
3. Hors plan (conduits, filage, percements, raccordements mécaniques, panneau/disjoncteurs, FabLab, alarme, frais de chantier) = quantités et heures « à valider » de la feuille Détail ; mètres convertis en pieds (x 3,28084). Les lignes composites par poste (D-01..D-07, E-01, E-03..E-05) sont remplacées par les lignes d'appareils du relevé pour éviter le double compte.
4. Lots confirmés posés tels quels (11 893 / 6 200 / 7 400 / 600 / 1 250) ; luminaires, enseignes Z6, détecteurs, panneau et disjoncteurs à 0 $ en ligne (temps seulement). Scan de dalle : ligne à 0 $ + lot GPR 1 250 $ (même prix, pas compté deux fois).
5. Articles : démontage et relocalisation -> 3.22 ; FabLab temporaire et continuité de service -> 5.19 ; frais de chantier (H) -> 6.1 ; données -> 3.33 ; percements/conduits d'alimentation sous dalle -> 3.31 ; lots JCI -> 3.38 (certification) et 3.36 (2 détecteurs).

## Lignes où j'ai hésité
- **Luminaire enlevé** : METHODE donne 0,5 h ; j'ai pris « EQUIPEMENT A ENLEVER » (0,5 h) plutôt que « ENLEVER FIXTURE ENCAST » (0,35 h, plus spécifique). Écart d'environ 6 h.
- **Lot éclairage** : les composantes listées dans METHODE totalisent 13 034,80 $, pas 11 893 $. J'ai gardé 11 893 $ (montant confirmé).
- **Panneau PP-3** : « PANNEAU 100A 347/600V 3F » (8 h, METHODE) ; le retrait de l'ancien panneau et le transfert des charges (24 h dans Estimation_2) ne sont pas chiffrés à part (« PANNEAU A CHANGER » 16 h aurait été l'alternative).
- **Sorties data** : 10 en « TEL/DATA 3/4 » (qté D-08, avec conduit) et 55 en « TEL/DATA » (0,63 h) ; la répartition 3/4 vs standard est un jugement.
- **Prises DDFT vs MALT isolée** : le relevé ne les sépare pas ; tout est en 3.30 (GFI), 3.29 est vide.
- **Moteurs/raccordements** : relevé MOTEUR TRIPHASE INSTALLER 4 = UTA (MOTEUR UAF-1, 1 h) + VE-02N + 2 chaudières (MOTEUR 0,75 h) ; MONOPHASE INSTALLER 3 = humidificateurs ; RELOCALISER 6 = toit E-103 (débranchement 0,4 h + MOTEUR 0,75 h au lieu des 4 h/u d'Estimation_2).
- **Axis C1_1 et C1_3** : pas de libellé catalogue propre, « FIXTURE TYPE C1 » (0,75 h) pour les trois. **Luminaire E** : 3 (relevé et lot) contre 4 (Estimation_2).
- **FabLab 210** : retrait (0,5 h) + réinstallation (« FIXTURE 2X2 EXISTANT RE » 0,25 h) = 0,75 h/u, contre 0,5–0,6 h/u dans Estimation_2.
- **Conduits 1" avec 5 #12** (D-13/D-15, E-08/E-10) : pas d'assemblage catalogue 1"/5C12, donc « CONDUIT VIDE 1 » + « 12AWG SOLIDE RW90 600V » séparés. Longueurs = hypothèses d'Estimation_2 (30 m / 25 m par course), qui pèsent environ 297 h (conduits et filage sous dalle, y compris data) : c'est le poste le plus incertain.
- **Fusions** : A-01/A-02 et A-03/A-04 (RDC/2e) fusionnés, car le relevé ne donne pas la portée par feuille ; E-02/E-03 (monuments) fusionnés sur les 3 du relevé ; F-09 compris dans l'assemblage 03C12 ; C-05/C-06 et C-07/C-08 scindés par section de conduit.
- **H-02..H-04** (coordination, essais, nettoyage, 40 h) gardés comme jugement Estimation_2, alors que Dupuis met l'administration à 0 % : à confirmer.
- Ratio de contrôle : 948,69 h pour 175 k$ = environ 540 h par 100 k$, un peu au-dessus de la plage 450–520 de METHODE ; part MO 58 %.

## Introuvable au catalogue Dupuis (prix Lumen ou jugement, source écrite dans chaque ligne)
- Prix Lumen : sectionneur HBL1372 (C-04.2), connecteurs Conseal 5333, corde de tirage, boîtes de tirage 4-11/16 + couvercles (D-16), ancrages drop-in, flexible 3/8" et connecteurs BX (F-08.2/F-08.3).
- Temps par jugement (Estimation_2) : A-07, A-11, G-05, G-06, B-09, F-05 (suspension des rangées), D-09, D-10, D-16, H-02..H-04. Familles sans libellé : barrière anti-vol, bornes de prêts, mise à jour des fiches de panneaux, continuité de service, coordination.
- Le catalogue n'a pas de colonne TEMPSEC : conduits au temps/pi seulement (pas de formule ACCEO par sections de 10 pi).
- Non chiffré, hors des lignes du relevé : options OPT-1 à OPT-4 d'Estimation_2, panneaux E-501/E-502 et schémas non relevés (tableaux), câblage data Cat6 (contradiction devis 36.1 vs plans), câble des moteurs hors lignes C.

## Ventilation par article
Total d'un article = matériel + heures brutes x 85. La somme des articles est donc inférieure d'environ 110 $ au total ACCEO (arrondi des heures au multiple de 10 non réparti). L'article 3.29 est à zéro (voir plus haut).
