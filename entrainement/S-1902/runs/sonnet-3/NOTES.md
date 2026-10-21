# NOTES — chiffrage « méthode Dupuis » à l'aveugle, S-1902

Modèle ayant produit ce travail : **Claude Sonnet 5.5** (claude-sonnet-5-5).
Sources lues : uniquement le kit (CONSIGNES, METHODE, releve.xlsx, rapport-releve.md, reserves.md, entree/*, catalogue). Aucun sous-agent, aucun accès web ou extérieur au dossier.

## Résultat (chiffrage.py, code de sortie 0, JSON identique à chaque exécution)
Matériel 57 439,99 $ (dont lots 27 343 $) ; heures relevées 910,31 h → chargées 920 h ; taux 85 $/h → MO 78 200 $ ;
total ACCEO 135 639,99 $ ; facteur 1,244 → prix de vente 169 000 $ ; 83 lignes.
Contrôles internes : matériel + 920 × 85 = total ; prix de vente = arrondi au millier de 168 736,15 ; Σ par_article = totaux.
Ratio 910 h / 169 k$ = 539 h par 100 k$ (un peu au-dessus de la plage 450–520 de METHODE §6, voir hésitations).

## Hypothèses
1. **Quantités sur plan** : releve.xlsx « Par libellé » (contrôlé contre « Marques ») + répartition par portée lue dans rapport-releve.md (la feuille Marques n'a pas de colonne portée; le script vérifie que Σ portées = total relevé pour chaque famille). Le relevé est marqué « à VÉRIFIER » : je l'ai pris tel quel.
2. **Quantités hors plan et heures de jugement** : feuille Détail (longueurs de conduits/fils, percements, disjoncteurs/panneau, A-07, A-08/A-09, A-11, B-09, D-09, F-05, G-05, G-06, H-02 à H-04). Ces heures « à valider » sont reprises telles quelles (source « jugement (Estimation_2) »).
3. **Lignes Détail remplacées par le relevé** (pour ne pas compter deux fois les symboles) : D-01, D-03, D-04, D-05, D-10, E-01, E-03, E-04, E-05 (postes/écrans/cabines = prises, data et JB déjà au relevé), A-02 et A-04 (fusionnés dans A-01 et A-03 : le relevé n'a pas de split par étage), F-09, C-08 (fils inclus dans les libellés conduit « nnC12 »), G-04 conservé. D-02, D-06, D-07, D-08, E-02, F-01 à F-07 gardent leur code mais la quantité vient du relevé (INSTALLER).
4. **Conduits** : le catalogue n'a pas de colonne TEMPSEC → temps/pi (CONSIGNES règle 3). Mètres du Détail convertis en pi (× 3,28084, arrondi). Sous-dalle 1" = « COND TME 1PO » + « 12AWG SOLIDE RW90 600V » (5 conducteurs) comme au Détail; data = « CONDUIT VIDE 3/4 »; raccordement luminaires = « CONDUIT 3/4 03C12 »; raccordements mécaniques = libellés « CONDUIT 1 03C08 » et « CONDUIT 3/4 04C12/03C12 ».
5. **Articles** : 3.22 = démontage E.A.E; 5.19 = relocalisations, travaux temporaires et continuité de service (E.A.R, FabLab, toit); 3.23 = UTA, VE, humidificateurs, thermostats; 3.26 = chaudières (MCC); 3.24/3.25 = panneau/disjoncteurs; 3.27/3.28/3.30 = prises USB/15 A/DDFT; 3.31 = percements, conduits, fils, JB, coupe-feu; 3.32 = scan; 3.33 = data, lecteurs, boutons d'appel, barrière anti-vol; 3.34 = monuments; 3.35 = luminaires, urgence, interrupteurs; 3.36–3.38 = alarme incendie; 6.1 = frais de chantier (H). Les heures chargées sont réparties au prorata des heures relevées pour que Σ total par article = total ACCEO (par_article.heures = heures relevées de l'article).
6. **Lots** : lot éclairage, distribution (réparti 3 400 $ panneau 3.24 / 2 800 $ disjoncteurs 3.25), JCI 7 400 $ (3.38), 2 détecteurs 600 $ (3.36), GPR 1 250 $ (3.32) sont des lignes de matériel (code LOT-*, G-07); les lignes d'appareils correspondantes sont à 0 $ (prix forcé à 0 quand le libellé catalogue avait un prix, ex. DISJ 3P 719,60 $).

## Hésitations
- **Lot éclairage** : METHODE donne 11 893 $ confirmé, mais le détail entre parenthèses (A1 ×11 à 185 + SL1 4′ ×12 à 290 + 3′ ×15 à 230 + 1′ ×6 à 110 + trousses 1 500 + E ×3 à 475 + Z6 ×3 à 161,60) totalise 13 034,80 $ (écart 1 141,80 $). J'ai retenu le total confirmé 11 893 $.
- **Luminaire enlevé 0,5 h** : aucun libellé « enlever luminaire » à 0,5 h; j'ai pris « EQUIPEMENT A ENLEVER » (0,5 h). Les « ENLEVER FIXTURE … » sont à 0,35 h (écart ≈ 6 h).
- **Panneau 8 h** : « PANNEAU 225A 347/600V 3 » est à temps 0 au catalogue → « PANNEAU 100A 347/600V 3F » (8 h). Le Détail jugeait 24 h (démantèlement de l'ancien PP-3 + transfert des charges); « PANNEAU A CHANGER » = 16 h serait l'alternative.
- **3 types de luminaires Axis** (C1_1, C1_3 sans libellé propre) → « FIXTURE TYPE C1 » 0,75 h. LUMINAIRE E : 3 au relevé (4 au Détail, lot E ×3) → 3.
- **Monuments** : 250 $ (METHODE) au lieu du Hubbell Lumen 1 461,22 $ × 3 (≈ +3 600 $ si on prenait Lumen).
- **Data** : 10 sorties murales/colonne (D-08) en « TEL/DATA 3/4 » 22,32 $ / 0,89 h, les 55 autres (mobilier, plaque seulement) en « TEL/DATA » 13,96 $ / 0,63 h.
- **FabLab (A-08/A-09)** : retrait + réinstallation assimilés à « RELO ENCASTRE » 1 h (45 h) alors que le Détail estimait 24,6 h. A-10 : débranchement 0,4 h + rebranchement « MOTEUR » 0,75 h (≈ 6,9 h vs 24 h au Détail).
- **Heures de jugement** (≈ 160 h : A-07, A-11, B-09, D-09, F-05, G-05, G-06, H-02/03/04) reprises du Détail sans les contester : elles expliquent en partie le dépassement du ratio h/100 k$.
- **Conduits hors plan** : longueurs = hypothèses du Détail (30 m/course, 8 m/point…), non vérifiées. F-08 (919 pi de 03C12) pèse 104 h.
- **Répartition 3.22 / 5.19** : le bordereau a deux postes de démolition électrique; la coupure (démontage vs relocalisation/temporaire) est mon choix.
- **Disjoncteurs 1P** : 19 au Détail vs 20 dans le lot (EDB ×20); lot gardé tel quel.

## Non trouvé dans le catalogue
- Corde de tirage (famille absente) → prix Lumen GRE430 81,68 $ + temps par jugement 0,5 h (ligne N-14). C'est la seule ligne Lumen.
- BOITIER C (famille « hors légende » du relevé, 2 à enlever) : traité comme « EQUIPEMENT A ENLEVER »; 2 à conserver sans travaux.
- Prises DDFT vs « MALT isolées » (3.29) non distinguées au relevé (R-007) : tout est en GFI (3.30); 3.29 reste vide.
- Libellés exacts C1_1 / C1_3 / Z6 d'enseigne avec prix, UTA-01, panneau 225 A 600 V (temps 0) : voir ci-dessus.
- Hors total (non chiffrés) : OPT-1 à OPT-4 du Détail, parasismique, câblage Cat6 salle serveurs, options JCI AI-07.
- Conduits : pas de colonne TEMPSEC dans le catalogue fourni → formule ACCEO non applicable.
