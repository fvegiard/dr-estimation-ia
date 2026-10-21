# NOTES — chiffrage « méthode Dupuis » à l'aveugle, S-1902

**Modèle ayant produit ce travail : Claude Sonnet 5.5** (claude-sonnet-5-5).

## Résultat (chiffrage.py -> chiffrage.json, code de sortie 0, deux exécutions identiques)
| | |
|---|--:|
| Matériel (lignes + lots) | 59 759,04 $ |
| Heures relevées | 997,18 h |
| Heures chargées (arrondi au 10 supérieur) | 1 000 h |
| Main-d'œuvre (1 000 h x 85 $) | 85 000,00 $ |
| Total ACCEO | 144 759,04 $ |
| Prix de vente (x 1,244, arrondi au millier) | 180 000 $ |

89 lignes. Contrôles : matériel + heures chargées x taux = total ACCEO; prix de vente = arrondi au millier de total x 1,244; part MO 58,7 % (plage 30-69 %); 556 h par 100 k$ de prix (un peu au-dessus de la plage 450-520).
Dans `lignes`, `p` = prix unitaire et `h` = temps unitaire (comme « Prix mat. unit. » et « h / unité » du Détail); `q` en pieds (`pi`) pour les conduits/câbles.

## Hypothèses principales
1. **Taux 85 $/h** (dossiers août-octobre 2026 de METHODE.md) et non les 124 $/h du Sommaire d'Estimation_2 (« référence Jo »). Facteur 1,244 (seul couple observé).
2. **Quantités sur plan = releve.xlsx + portées de rapport-releve.md** (INSTALLER / ENLEVER / RELOCALISER; CONSERVER = 0 $, 0 h). Les familles « nouveau travail » sont réparties RDC (E-104) / étage (E-105) avec les comptes par feuille, validés par le script (E104 + E105 = INSTALLER pour chaque famille). Le relevé n'indique pas la portée par feuille pour les feuilles existant/démolition : les lignes A-02/A-04 du Détail (2e étage) sont donc **fusionnées** dans A-01/A-03 (totaux RDC + 2e). Les composites « poste de travail » D-01 à D-06, D-08, D-15, E-01, E-03 à E-05, E-10, C-06, C-08, F-09 sont remplacés par les lignes d'appareils du relevé ou absorbés dans les assemblages conduit + fil du catalogue (jamais comptés deux fois).
3. **Hors plan (Détail)** : longueurs de conduits (hypothèses 30 m / 25 m par course, 35 m mécanique, 8 m x 35 points éclairage, 30 m / 60 m boucle AI), nombre de courses/percements (16 + 7), quantités FabLab (21 + 24), pièces de la feuille Matériel Lumen (LFMC 14 m, 20 connecteurs, câble armé 10 m); heures « à valider » gardées telles quelles pour A-11, B-09, D-09, F-05, G-05, G-06, H-02, H-03, H-04 (source « jugement (Estimation_2) »).
4. **Lots confirmés** (11 893 + 6 200 + 7 400 + 600 + 1 250 = 27 343 $) : luminaires, enseignes, détecteurs, panneau et disjoncteurs à 0 $ en ligne (temps seulement). Lot distribution scindé en panneau 3 400 $ (art. 3.24) et disjoncteurs 2 800 $ (art. 3.25). **GPR 1 250 $ = ligne catalogue SCAN DALLE BETON (1 250 $ / 2 h), comptée une seule fois** (METHODE cite les deux). Note : la somme des prix détaillés du lot éclairage (A1 2 035 + 4' 3 480 + 3' 3 450 + 1' 660 + trousses 1 500 + E 1 425 + Z6 485 = 13 035 $) ne retombe pas sur 11 893 $ : j'ai retenu le montant du lot, confirmé tel quel.
5. **Heures unitaires suivent les valeurs données dans METHODE.md** quand elles diffèrent du libellé le plus spécifique du catalogue : luminaire enlevé 0,5 h (libellé EQUIPEMENT A ENLEVER; les ENLEVER FIXTURE ... donnent 0,35 h), moteur 0,75 h (MOTEUR), UTA 1 h (UNITER UC AU TOIT), panneau 8 h, annonciateur relocalisé 8 h, disjoncteur 3P 1 h.

## Lignes où j'ai hésité
- **A-10** (6 moteurs monophasés toit à relocaliser) : DISCONNECTER ET RECON = 8 h chacun (48 h) vs 4 h du Détail.
- **A-08 / A-09** FabLab : pas de libellé « luminaire linéaire retiré/réinstallé »; RELO ENCASTRE (1 h) par analogie.
- **B-03 à B-05** disjoncteurs 3P : seul le temps (1 h) est pris sur DISJ 100A 3P (719,60 $ au catalogue, ramené à 0 $ car le matériel est dans le lot distribution). B-08 (20 A) pris sur DISJ15A1P (0,2 h). Le lot parle de 20 disjoncteurs 1P, le Détail en compte 19.
- **Prises DDFT (22)** : le relevé confond DDFT et MALT isolée (R-007); tout est chiffré DDFT (65,38 $ / 1,3 h) et classé art. 3.30; **3.29 (MALT isolées) reste à 0 $ et n'apparaît pas dans par_article**.
- **Conduits sous dalle** : Détail = EMT 1" ; j'ai pris CONDUIT 3/4 05C12 (assemblage 5 #12) faute de libellé 1" à 5 conducteurs; UTA : CONDUIT 1 04C08.
- **Luminaires C1_1 / C1_3** : pas de libellé propre, FIXTURE TYPE C1 (0,75 h). LUMINAIRE E = 3 (relevé et lot) et non 4 (Détail).
- **LECTEUR DE CARTE (0,5 h)** vs LECTEUR CARTE (0,35 h) : même prix 15 $, j'ai pris le premier. Monument : MONUMENT PLANCHER 250 $ (pas le Hubbell à ~1 461 $ de Lumen), selon METHODE.
- **QUINCAILLERIE 2 250 $** (classe Jugement / forfait) pour F-10; peut être généreux.
- **H-01** = NACELLE 1 250 $ / 16 h (correspond aux 16 h du Détail).
- **Répartition par article du bordereau** (par_article) : choix de ma part, le kit ne la donne pas. 5.19 = enlèvements (A-01, A-03*); 3.22 = relocalisations/travaux temporaires (A-05 à A-09, A-11); 3.23 = raccordements mécaniques + thermostats + A-10; 3.24 = panneau PP-3; 3.25 = disjoncteurs; 3.26 = MCC (chaudières); 3.27 USB; 3.28 prises 15 A; 3.30 DDFT; 3.31 percements/conduits/filage/JB, boutons, lecteurs de carte; 3.32 scan; 3.33 data; 3.34 monuments; 3.35 éclairage, enseignes, interrupteurs, lot éclairage; 3.36 détecteurs + boucle AI; 3.37 annonciateur; 3.38 lot JCI + assistance; 6.1 frais de chantier (H-01 à H-04). Les heures par article sont les heures relevées; `total` = matériel + heures x (heures chargées / heures relevées) x taux, de sorte que la somme des articles égale le total ACCEO.

## Introuvable au catalogue Dupuis (prix Lumen + temps par jugement)
- Connecteurs Star Teck 3/4" (IBETEK75120, 42,2247 $, 0,25 h) — ligne C-10b.
- Corde de tirage Poly Line 430 (GRE430, 81,68 $, 0,5 h) — ligne N-05.
Autres familles Lumen (prises Leviton, plaques, EMT, coupleurs, boîtes, RW90, tige filetée, Hubbell) : couvertes par des assemblages du catalogue, non rajoutées.

## Exclus du total (comme dans le Détail)
OPT-1 câblage data Cat6, OPT-2 conception parasismique, OPT-3 prime hors heures, OPT-4 postes temporaires; frais généraux et profit de l'Estimation_2 (0 % dans la méthode Dupuis); taxes.
