# NOTES — chiffrage à l'aveugle S-1902 (Bibliothèque Georgette-Lepage, Brossard)

**Modèle ayant produit ce travail : Claude Sonnet 5.5** (claude-sonnet-5-5), sans sous-agent, uniquement avec les fichiers du dossier.

## Résultat (chiffrage.py → chiffrage.json, code de sortie 0)
83 lignes | matériel 57 975,33 $ | heures relevées 927,18 h | heures chargées 930 h | main-d'œuvre 79 050 $ (930 h × 85 $/h)
| total ACCEO 137 025,33 $ | facteur 1,244 | prix de vente 170 000 $.
Contrôles passés dans le script : matériel + heures chargées × taux = total ACCEO; prix de vente = arrondi au millier de total ACCEO × facteur;
Σ par article = totaux; quantités du relevé = rapport-releve.md = Par libellé = nombre de Marques.
Contrôle de vraisemblance METHODE §6 : part MO 58 % (plage 30–69 %); 930 h / 170 k$ = 547 h par 100 k$ (un peu au-dessus de 450–520 : conduits sous dalle et data pèsent lourd).

## Conventions
- `p` et `h` des lignes = prix unitaire et temps unitaire (comme les colonnes « Prix mat. unit. » / « h / unité » du Détail); matériel = Σ q × p + lots; heures = Σ q × h.
- Conduits : le CSV n'a pas de colonne TEMPSEC → temps/pi (formule par sections de 10 pi non applicable). Longueurs du Détail (m, hypothèses de l'estimation du 2026-10-08) converties en pi (÷ 0,3048).
- Taux 85 $/h (dossiers août–octobre 2026, METHODE §5; le 124 $/h du Sommaire de l'estimation de référence n'est pas retenu). Facteur 1,244.
- Quantités sur plan : releve.xlsx + portées de rapport-releve.md. Portées : INSTALLER = fournir/installer, ENLEVER = temps de démantèlement, RELOCALISER = temps de relocalisation, CONSERVER = rien. Hors plan : Détail (A-07, A-08, A-09, A-11, B, C, D-09…D-16, E-06…E-11, F-05, F-08, G, H).
- Les lignes « poste de travail » du Détail (D-01 à D-08, E-01 à E-05) NE sont PAS reprises : leurs appareils sont déjà comptés par famille au relevé (évite le double compte). Conservées seulement les lignes sans équivalent au relevé.
- Codes : ceux du Détail quand la ligne en vient (suffixe b/c si une ligne du Détail est scindée); « P-xx » pour les appareils venant du relevé (absents du Détail); D-17 (scan) nouveau.
- Lots (METHODE §2, confirmés par Francis le 2026-10-20) comptés au matériel : éclairage 11 893, distribution 6 200 (panneau 3 400 → 3.24; EDB+EJB 2 800 → 3.25), JCI 7 400 (3.38), 2 détecteurs 600 (3.36), GPR 1 250 (3.32). Luminaires, enseigne Z6, têtes, détecteurs, panneaux, disjoncteurs : 0 $ en ligne + temps.

## Hypothèses principales / ventilation par article
- 5.19 = retrait définitif (E.A.E) + continuité de service; 3.22 = relocalisations, retraits temporaires (FabLab 210), toit; 3.23 = raccordements mécaniques + thermostats; 3.26 (MCC) = chaudières (tiroirs CCM-1); 3.27 USB, 3.28 prises 15 A, 3.30 DDFT, 3.31 percements/conduits/filage/JB/lecteurs/boutons, 3.33 data, 3.34 monuments, 3.35 éclairage + interrupteurs + conduit d'alimentation des luminaires, 3.36–3.38 alarme, 6.1 frais de chantier (H). Admin/profit = 0 % (METHODE §1).
- Prises DDFT : le relevé ne sépare pas DDFT et MALT isolée → tout en 3.30 (3.29 = 0 $). 15 A/20 A non distinguées → « PRISE DUPLEX 15A 120V » (64,81 $) pour les 25 prises doubles; DDFT = « PRISE DUPLEX 20A 125V GFI » (65,38 $).
- Sorties data (65 neuves) : « TEL/DATA 3/4 » (22,32 $ / 0,89 h, avec conduit 3/4" vers l'entreplafond, Détail D-08) plutôt que « TEL/DATA » plaque seule (13,96 $ / 0,63 h). Si c'était la plaque seule : environ −540 $ et −17 h.
- Conduits : assemblage exact du catalogue quand il existe (CONDUIT 1 04C08 pour UTA-01; 3/4 04C12 VE-02N; 3/4 03C12 humidificateurs et luminaires — les lignes de fils C-06, C-08, F-09 sont donc fondues); sinon conduit TME 1" + fil 12 AWG solide en lignes séparées (D-13/D-15, E-08/E-10, cinq conducteurs par course : aucun assemblage 1" à 5 #12). Conduits de données et boucle AI : « CONDUIT VIDE 3/4 ».
- Scan dalle : le prix catalogue 1 250 $ = lot GPR confirmé, compté une seule fois (lots); la ligne D-17 ne porte que le temps (2 h) à 0 $. Quantité : 1 scan.
- Moteurs : 4 triphasés + 3 monophasés INSTALLER = UTA-01 (MOTEUR UAF-1, 1 h), VE-02N (MOTEUR VE-2 120V, 1 h), chaudières ×2 (MOTEUR, 0,75 h), humidificateurs ×3 (HUMIDIFICATEUR 0,35 h + sectionneur Hubbell 165,61 $ / 0,75 h). Toit : 6 moteurs monophasés RELOCALISER = ENLEVER MOTEUR (0,25 h) + MOTEUR (0,75 h, 25 $).
- Nacelle : H-01 remplacé par « NACELLE » (1 250 $ / 16 h), même temps que le Détail.
- Percements : 23 × « PERCEMENT PLANCHER » (150 $ / 1 h); coupe-feu Hilti/3M non ajouté (le 150 $ est réputé l'assemblage).
- Lumen (famille absente du catalogue) : boîtes de tirage 4-11/16" + couvercles (IBE72171K + IBE72C1, 46 u = 2 par percement, temps 0,25 h/u par jugement) et ancrages drop-in USCAN (2 pk, 32,26 $). Les autres articles de la liste Lumen (couvercles/connecteurs/marrettes/coupleurs/corde de tirage, câbles…) sont réputés inclus dans les assemblages Dupuis, ou ont un libellé catalogue (tige filetée, conduit flexible étanche, raccords étanches, boîtes octogonales).

## Lignes où j'ai hésité
- **Lot éclairage** : les composantes données (A1 ×11 à 185, Axis 4′ ×12 à 290, 3′ ×15 à 230, 1′ ×6 à 110, trousses 1 500, E ×3 à 475, Z6 ×3 à 161,60) totalisent 13 034,80 $, pas 11 893 $. J'ai retenu le total confirmé de 11 893 $ (METHODE §2) et traité Z6 comme inclus; écart de 1 141,80 $ à faire valider.
- **Temps de démantèlement des luminaires** : catalogue = 0,35 h (ENLEVER FIXTURE ENCAST / 2X2 / 1X4, dernier 2026-08-26); METHODE cite « luminaire enlevé 0,5 h » sans ligne correspondante au catalogue → 0,35 h retenu (si 0,5 h : +6 h environ).
- **Panneau PP-3** (B-01) : « PANN PS2 225A 120/208V 3F » (10 h, 0 $, standard, 2026-09-25) + « ENL PANN 42CCT » (4 h); METHODE dit « panneau 8 h », le Détail 24 h.
- **Luminaires C1_1 / C1_3** : pas de libellé au catalogue → « FIXTURE TYPE C1 » 0,75 h (le Détail jugeait 0,5 h et 0,6 h). Rangées Axis : 20 × 1 h de suspension/alimentation (jugement, Détail F-05) en plus du 0,75 h par module.
- **Luminaire E** : 3 au relevé et au lot (l'estimation en comptait 4; une étiquette « E » écartée en R-004).
- **A-08 FabLab linéaires** : « RELO FIXTURE TYPE S7 » (1,0 h) par analogie; A-09 : « RELO ENCASTRE » 1,0 h (le Détail jugeait 0,6 h et 0,5 h).
- **Disjoncteurs 3P** : temps 1,0 h pris sur « DISJ 100A 3P 120/240V 22 K », prix ramené à 0 $ (déjà dans le lot distribution EJB 3P). 19 disjoncteurs 1P au Détail pour 20 au lot (1 de réserve).
- **Retrait de petits dispositifs** (détecteur de mouvement, détecteur de fumée, haut-parleur) : 0,35 h par jugement, sans libellé catalogue; sorties data / JB / boîtiers C / monuments retirés : libellé ENLEVER PRISE par analogie.
- **Quantité du relevé « à VÉRIFIER »** (rapport-releve.md) : le relevé automatique n'est pas validé sur planches; ses quantités sont utilisées telles quelles (ex. 26 encastrés + 8 LED 2X2 + 6 LED 1X4 enlevés = 40 luminaires contre 46 au Détail; 12 relocalisations de services contre 13).

## Familles introuvables au catalogue Dupuis (source écrite dans chaque ligne)
- Boîtes de tirage 4-11/16" + couvercles, ancrages drop-in → prix Lumen + temps par jugement.
- Retrait de détecteur / HP, relocalisation d'interrupteurs maîtres (A-07), traçage et continuité (A-11), rangées Axis (F-05), mise à jour des fiches de panneaux (B-09), barrière anti-vol (D-09), bornes de prêt (D-10), assistance AI (G-05, G-06), coordination / essais / nettoyage (H-02 à H-04) → heures « à valider » du Détail (jugement Estimation_2).
- Aucun libellé « luminaire C1_1 / C1_3 », « enlever détecteur », « sectionneur sans fusible 30 A 1Ø » exact (Hubbell retenu), ni assemblage conduit 1" à 5 #12.
- Non chiffré (hors relevé / hors bordereau électrique) : option câblage data Cat6 (OPT-1), parasismique (OPT-2), prime hors heures (OPT-3), postes temporaires (OPT-4), vérification AI des dispositifs existants (AI-07, option).
