# NOTES — chiffrage « méthode Dupuis » à l'aveugle, S-1902 (Bibliothèque Georgette-Lepage, Brossard)

Modèle ayant produit ce travail : **Claude Opus 5.5** (claude-opus-5-5), 2026-10-21. Aucun sous-agent, aucune lecture hors du dossier.

## Résultat (chiffrage.py → chiffrage.json, code de sortie 0)

| Poste | Valeur |
|---|--:|
| Matériel (73 lignes 28 312,69 $ + lots 27 343,00 $) | 55 655,69 $ |
| Heures relevées | 924,71 h |
| Heures chargées (arrondi au 10 supérieur) | 930 h |
| Main-d'œuvre (930 h × 85 $/h) | 79 050,00 $ |
| Total ACCEO | 134 705,69 $ |
| Prix de vente (× 1,244, arrondi au millier) | **168 000 $** |

Contrôles METHODE §6 : part MO 58,7 % (dans 30–69 %); 554 h par 100 k$ de prix, **au-dessus** de la plage 450–520 h,
surtout à cause des conduits sous dalle (D-13/D-14/F-08 ≈ 370 h). Le script vérifie lui-même : matériel + heures chargées × taux
= total ACCEO; prix de vente = arrondi au millier de total × facteur; Σ par_article = matériel et heures; il s'exécute de façon déterministe (même md5 à deux exécutions).

## Hypothèses principales
1. **Taux 85 $/h** (dossiers Dupuis d'août à octobre 2026), pas le 124 $/h « référence Jo » du Sommaire d'Estimation_2. **Facteur 1,244.**
2. **Quantités sur plan = relevé** (totaux de releve.xlsx « Par libellé », ventilés par portée selon le tableau de rapport-releve.md; le script vérifie que les deux concordent).
   Les comptes de démantèlement de la feuille Détail (A-01 à A-04 : 39+7 luminaires, 34+10 services) sont donc remplacés par les ENLEVER du relevé
   (40 luminaires, 39 services ou dispositifs). Les codes A-02 et A-04 sont fusionnés dans A-01 et A-03.
3. **Assemblages Dupuis** : le prix d'assemblage inclut la boîte, la plaque et les raccords; un conduit « 3/4 0xC12 » inclut ses fils. Les fils de la feuille Détail
   (C-06, C-08, D-15, E-10, F-09, G-03) n'ont donc **pas de ligne séparée**. Longueurs en m de la feuille Détail × 3,28084, arrondies au pied.
   Le catalogue n'a pas de colonne TEMPSEC : temps/pi seulement (pas de « sections de 10 pi »).
4. **Lots confirmés** pris tels quels : éclairage 11 893 $, distribution 6 200 $, JCI 7 400 $, détecteurs 600 $, GPR 1 250 $. Les luminaires, l'enseigne, les détecteurs,
   le panneau, les disjoncteurs et le scan sont à 0 $ en ligne (temps seulement). Pour par_article, le lot distribution est scindé : panneau 3 400 $ → 3.24, disjoncteurs 2 800 $ → 3.25.
5. **« PRISE DDFT » INSTALLER 22 = 1 DDFT (fontaine, D-07) + 21 prises à M.A.L.T. isolée / 20 A Decora des postes.** Selon R-007, la barre pleine de la légende (M.A.L.T. isolée) tombe dans la famille DDFT.
   Le Détail ne prévoit qu'une seule DDFT. Ces 21 prises sont mises à l'article 3.29.

## Lignes où j'ai hésité
- **D-13 / E-08 conduit d'alimentation sous dalle** : le Détail dit EMT 1" avec 5 #12, mais le catalogue n'a pas de « CONDUIT 1 05C12 ». J'ai pris « CONDUIT 3/4 05C12 » (3,4197 $/pi; 0,081 h/pi),
  puisque 5 #12 passent dans un 3/4". Avec « CONDUIT 3/4 03C12 » (référence de METHODE, 4,24 $/pi; 0,113 h/pi), on ajouterait environ 1 772 $ et 68 h.
- **Sorties data** : 65 INSTALLER, soit 10 murales ou de colonne avec conduit (D-08) en « TEL/DATA 3/4 » (22,32 $; 0,89 h) et 55 sur postes ou mobilier en « TEL/DATA » (13,96 $; 0,63 h).
- **USB** : le relevé compte 20 symboles, alors que le Détail et la liste Lumen n'en comptent que 10 (5 tables × 2). J'ai pris le relevé.
- **Monuments** : 3 selon le relevé, alors que le Détail compte E-02 (2) + E-03 (2). Prix catalogue 250 $ « MONUMENT PLANCHER ». Le poke-through Hubbell coûte 1 461 $ chez Lumen, ce qui sous-estime peut-être le matériel.
- **FabLab A-08 / A-09** (retrait temporaire puis réinstallation) : j'ai utilisé « RELO ENCASTRE » 1,0 h plutôt que le jugement du Détail (0,6 et 0,5 h), soit +20 h.
- **Démantèlement** : « ENLEVER FIXTURE … » 0,35 h (dernier Dupuis), alors que METHODE cite « luminaire enlevé 0,5 h ». Les sorties data enlevées sont comptées comme « ENLEVER PRISE »,
  et les monuments, JB, boîtiers C, HP et détecteurs enlevés comme « EQUIPEMENT A ENLEVER » 0,5 h.
- **Lot éclairage** : le détail donné dans METHODE (A1 2 035 + 4′ 3 480 + 3′ 3 450 + 1′ 660 + trousses 1 500 + E 1 425 + Z6 484,80) totalise **13 034,80 $**, pas 11 893 $.
  J'ai retenu le montant confirmé (11 893 $). **Écart de 1 141,80 $ à faire vérifier par Francis.**
- **Disjoncteurs 1P** : le Détail en compte 19 (B-02 14, B-06 1, B-07 2, B-08 2), le lot distribution en compte 20. Les heures suivent le Détail (écart de 0,2 h).
- **Luminaire E** : 3 selon le relevé et le lot confirmé, alors que le Détail en compte 4. J'ai retenu 3.
- **Jugements conservés de la feuille Détail** (aucun équivalent au catalogue) : A-07 6 h, A-10 6 × 4 h (relevé MOTEUR MONOPHASE RELOCALISER 6), A-11 16 h, B-09 9 × 1 h, D-09 6 h, D-10 2 h,
  F-05 20 rangées × 1 h, G-05 12 h, G-06 8 h, H-02 20 h, H-03 12 h, H-04 8 h. H-01 est remplacé par « NACELLE » 1 250 $ / 16 h.
  F-05 chevauche peut-être en partie la ligne de tige filetée (4 h).
- **B-01** : panneau « PPM-N-01 PANN 225A 347/6 » 8 h, plus l'enlèvement de l'ancien PP-3 « ENL PANN 42CCT 120/208V » 4 h, au lieu des 24 h du Détail.
- **Coupe-feu** : aucune ligne séparée. Je suppose que le « PERCEMENT PLANCHER » à 150 $ (au lieu de 75 $ ailleurs) l'inclut.
- **JB du relevé (INSTALLER 3)** : aucune ligne séparée. Je les suppose couvertes par D-09 (barrière, 2 JB) et D-10 (bornes, 1 JB).
- **Ventilation par article** : 3.22 pour démantèlement et relocalisations; 5.19 pour A-11 (continuité de service, traçage); 3.23 pour raccordements mécaniques, toit et thermostats;
  3.26 (MCC) pour C-03 chaudières sur tiroirs CCM-1; 3.31 pour percements, conduits d'alimentation, boîtes, boutons d'appel et lecteurs de carte; 3.33 pour data et conduit vide;
  3.35 pour l'éclairage et ses interrupteurs; 3.36 à 3.38 pour l'alarme incendie; 6.1 pour les frais de chantier (H-01 à H-04).
  par_article.total = matériel + heures relevées × taux, sans l'arrondi aux 10 h. Σ par_article.total = 134 255,62 $, soit 450,07 $ (5,29 h × 85) de moins que le total ACCEO.

## Familles introuvables dans le catalogue Dupuis
- **Prise à M.A.L.T. isolée** : remplacée par « PRISE DUPLEX 15/20A 120V » (prise 20 A Decora des postes, Lumen LEV16352W).
- **Ancrages drop-in 3/8-16** : prix Lumen VISDIA3/816BX50, 32,26 $/pqt × 2. Temps : jugement 0 h (pose comprise dans la tige filetée et F-05).
- **Relocalisation d'équipement de ventilation au toit, interrupteurs maîtres, barrière anti-vol, fiches de panneaux, continuité de service, coordination, essais, nettoyage** :
  aucun libellé Dupuis, d'où le jugement de la feuille Détail (0 $).
- **Libellés approchés** :
  - C1_1 et C1_3 → « FIXTURE TYPE C1 »;
  - disjoncteur 3P → « DISJ 100A 3P 120/240V 22 K » (seul 3P à 1 h);
  - chaudières et VE-02N → « MOTEUR »;
  - sectionneur des humidificateurs → « SECTIONNEUR POR ENTRETIEN HUBHBL13R22 »;
  - boucle AI → « COND ALARME 3/16 FT4 ».
