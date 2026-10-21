# NOTES — chiffrage « méthode Dupuis » à l'aveugle, S-1902 (Bibliothèque Georgette-Lepage, Brossard)

Modèle : **Claude Opus 5.5** (claude-opus-5-5), sans sous-agent, sans lecture hors du dossier de travail.

## Résultat (chiffrage.py → chiffrage.json, code de sortie 0, sortie identique sur deux exécutions)

| poste | valeur |
|---|--:|
| Matériel (lots inclus) | 60 322,08 $ |
| Heures relevées | 987,29 h |
| Heures chargées (arrondi sup. à 10) | 990 h |
| Main-d'œuvre (990 h × 85 $/h) | 84 150,00 $ |
| Total ACCEO | 144 472,08 $ |
| Prix de vente (× 1,244 = 179 723 $, arrondi au millier) | **180 000 $** |
| Lignes | 79 |

Contrôles METHODE : part MO 58,2 % (dans la plage 30–69 %); 550 h par 100 k$, **au-dessus** de la plage 450–520 h.
L'écart vient des longueurs de conduits hypothétiques de la feuille Détail (3 069 pi de 3/4 03C12 ≈ 346 h); voir hésitations.

Convention des lignes : `p` = prix unitaire, `h` = heures unitaires (total = q × p, q × h). `par_article.total` =
matériel + heures × taux × (990 / 987,29), pour que Σ des articles = total ACCEO (les 2,71 h d'arrondi sont réparties au prorata).

## Hypothèses principales
1. **Taux 85 $/h** (dossiers Dupuis août–octobre 2026, METHODE §5), pas les 124 $/h « référence Jo » d'Estimation_2. Facteur 1,244.
2. **Lots confirmés (27 343 $)** : éclairage 11 893, distribution 6 200 (ventilé 3 400 $ panneau → 3.24, 2 800 $ disjoncteurs → 3.25),
   JCI 7 400 (→ 3.38), 2 détecteurs 600 (→ 3.36), GPR 1 250 (= scan de dalle, ligne D-17, → 3.32). Luminaires, enseigne, détecteurs,
   panneau et disjoncteurs : 0 $ en ligne, temps Dupuis seulement.
3. **Quantités sur plan = relevé** (portées du tableau de rapport-releve.md) : elles remplacent les comptes de la feuille Détail
   A-01 à A-06, D-01 à D-10, E-01 à E-05 (sinon double compte). Seules les portées INSTALLER / ENLEVER / RELOCALISER sont chiffrées; CONSERVER = 0.
4. **Hors plan = feuille Détail** : longueurs de conduits (m → pi, arrondi au pied sup.), percements 16 + 7, FabLab, toit, lots de jugement
   (A-07, A-11, B-09, D-16, E-11, F-05, F-10, G-05, G-06, H-02 à H-04) avec les heures « à valider » telles quelles.
5. **Conduits = assemblages Dupuis filage inclus** : les lignes de conducteurs C-06, C-08, D-15, E-10, F-09 ne sont pas chiffrées à part.
   Le catalogue n'a pas de colonne TEMPSEC → temps/pi seulement (règle 3, cas « sinon »).
6. **PRISE DDFT INSTALLER 22** → 1 DDFT fontaine (D-07, « PRISE DUPLEX 20A 125V GFI ») + 21 prises M.A.L.T. isolée (art. 3.29, prix
   « PRISE DUPLEX 15A 120V ») : R-007 dit que la barre pleine M.A.L.T. isolée tombe dans la famille DDFT, et Détail ne prévoit qu'une DDFT.
7. **SORTIE DATA INSTALLER 65** → 10 « TEL/DATA 3/4 » (sorties murales avec conduit, D-08) + 55 « TEL/DATA » (postes/mobilier).
8. Disjoncteurs : quantités du lot confirmé (20 × 1P, 3 × 3P) plutôt que Détail (19 × 1P).

## Correspondance relevé → catalogue (libellés exacts)
- Enlèvements : ENLEVER FIXTURE ENCAST / 1X4 / 2X2, ENLEVER PRISE (prises + data), ENLEVER INTERRUPTEUR, EQUIPEMENT A ENLEVER
  (monuments 3, JB 2, boîtiers C 2, détecteur mouvement 1, détecteur fumée 1, HP 1).
- Relocalisations : RELO PRISE (prises 9, data 3), RELO ENCASTRE 4, RELO DETECTEUR A FUME 1, RELO PANN ANNOCIATEUR 1.
- Toit (6 E.A.R) : DEBRANCHEMENT APPAREILAGE MECANIQUE + SECTIONNEUR ENL + MOTEUR (1,65 h/équipement).
- Mécanique : UNITER UC AU TOIT (UTA-01), MOTEUR (VE-02N), CHAUDIERE ×2, HUMIDIFICATEUR ×3 + INTERR 30A 2P 600V CEMA1 ×3.
- Dispositifs : PRISE DUPLEX 15A 120V, PRISE USB 125V 15 AMP, PRISE DUPLEX 20A 125V GFI, TEL/DATA, TEL/DATA 3/4, INTERRUPTEUR 15A 120V,
  LECTEUR DE CARTE, THERMOSTAT, MONUMENT PLANCHER, RACCORD DIRECT (JB barrière/bornes), DECLENCHEUR APPEL (boutons).
- Éclairage : FIXTURE TYPE A1, FIXTURE TYPE C1 (C1, C1_1, C1_3), FIXTURE TYPE E, ENSEIGNE SORTIE Z6, ALIMENTATION ECLAIRAGE ×35, TIGE FILETE 3/8PO.
- Conduits : CONDUIT 3/4 03C12, 04C12, CONDUIT 1 03C08, CONDUIT VIDE 3/4, COND ALARME 3/16 FT4; PERCEMENT PLANCHER, COUPE FEU TUBE 10.1 FL O,
  QUINCAILLERIE (forfait 2 250 $), NACELLE, PANNEAU A CHANGER, DISJ15A1P, DISJ 100A 3P 120/240V 22 K, SCAN DALLE BETON (temps).

## Lignes où j'ai hésité
- **Lot éclairage** : le détail donné (A1 2 035 + 4′ 3 480 + 3′ 3 450 + 1′ 660 + trousses 1 500 + E 1 425 + Z6 484,80) totalise **13 034,80 $**,
  pas 11 893 $. J'ai retenu le montant confirmé 11 893 $; à faire valider par Francis (écart 1 141,80 $).
- **Panneau PP-3** : « PANNEAU A CHANGER » 16 h (remplacement + démantèlement de l'ancien) plutôt que le « panneau 8 h » générique de METHODE
  (Détail : 24 h). Avec 8 h : −8 h.
- **Luminaires enlevés** : libellés exacts ENLEVER FIXTURE … = 0,35 h; METHODE cite 0,5 h « luminaire enlevé » (aucun libellé luminaire à 0,5 h).
- **Conduits de circuits** : « CONDUIT 3/4 03C12 » (assemblage cité par METHODE) alors que Détail prévoit 1″ avec 5 conducteurs;
  « CONDUIT 3/4 05C12 » (3,4197 $ / 0,081 h) sur D-13/E-08 (2 150 pi) ferait environ −68 h et −1 770 $. Longueurs (30 m/course RDC, 25 m étage, 8 m/point éclairage) = hypothèses
  Détail non vérifiées : c'est le principal facteur de risque (et la cause du ratio 550 h/100 k$).
- **Monument de plancher** : 250 $ Dupuis, alors que le Hubbell S1R6PT (poke-through) vaut 1 461,22 $ chez Lumen; risque ≈ 3 600 $ sur 3 unités.
- **Disjoncteurs 3P** : temps de « DISJ 100A 3P 120/240V 22 K » (1 h, 719,60 $ mis à 0 car fourni dans le lot); aucun libellé 3P à 600 V à 0 $.
- **Luminaire E** : 3 (relevé et lot) contre 4 (Détail F-06). **Monuments** : 3 (relevé) contre 2 + 2 (Détail E-02/E-03).
- **Sorties data enlevées / relocalisées** : temps de prise (pas de libellé data).
- **Ventilation 3.22 / 5.19** : enlèvements définitifs → 5.19 (démolition); démontage-réinstallation, relocalisations, toit → 3.22.
  Chaudières (tiroirs CCM-1) → 3.26 MCC. Lecteurs de carte → 3.33.

## Introuvable dans le catalogue Dupuis (traité au jugement Estimation_2)
Relocalisation interrupteurs maîtres (A-07), retrait/réinstallation FabLab (A-08, A-09), maintien de service et traçage (A-11),
fiches de panneaux (B-09), suspension des rangées Axis (F-05), boîtes et chaînes d'éclairage (F-10), boîtes étage (E-11),
manutention AI et assistance à la vérification (G-05, G-06), coordination, essais, nettoyage (H-02 à H-04).
Aucune famille n'a demandé un prix Lumen : la feuille Matériel Lumen sert de contrôle (monuments, sectionneurs 117,84 $ = Dupuis)
et de quantité pour la tige filetée (200 pi).

## Exclus (hors total, comme dans Estimation_2)
OPT-1 câblage Cat6, OPT-2 parasismique, OPT-3 prime hors heures, OPT-4 postes temporaires. Contradiction UTA-1 40 A vs MOCP 35 A non tranchée.
