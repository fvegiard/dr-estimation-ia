# NOTES — chiffrage à l'aveugle S-1902 (Bibliothèque Georgette-Lepage), méthode Dupuis

**Modèle :** Claude Opus 5.5 (claude-opus-5-5), session Claude Code, 2026-10-21. Travail fait uniquement à partir du kit (aucun sous-agent, aucune source externe).

## Résultat (`python3 chiffrage.py`, code de sortie 0)
| clé | valeur |
|---|--:|
| taux | 85 $/h |
| materiel (lignes 29 978,90 + lots 27 343) | 56 921,90 $ |
| heures_relevees | 916,74 h |
| heures_chargees | 920 h |
| main_doeuvre | 78 200,00 $ |
| total_acceo | 135 121,90 $ |
| facteur | 1,244 |
| prix_vente | 168 000 $ (135 121,90 × 1,244 = 168 091,64) |
| lignes | 79 |

Contrôles METHODE §6 : part MO = 57,9 % (plage 30–69 %, OK) ; 546 h par 100 k$ de prix (plage 450–520 : **un peu haut**, voir les conduits ci-dessous).
Dans `lignes`, `p` = prix unitaire et `h` = temps unitaire (totaux = q×p, q×h). `par_article.total` = matériel + heures × taux × (920 / 916,74) : l'arrondi des heures chargées est réparti au prorata, de sorte que Σ totaux = total ACCEO.

## Hypothèses principales
1. **Taux 85 $/h** (dossiers Dupuis août–oct. 2026) et non 124 $/h (« référence Jo » de l'Estimation_2). **Facteur 1,244** (seul couple observé, S-1844).
2. **Lots confirmés** (METHODE §2) : éclairage 11 893 $, distribution 6 200 $ (3 400 $ → 3.24 ; 2 800 $ → 3.25), JCI 7 400 $ (3.38), 2 détecteurs 600 $ au total (3.36), GPR 1 250 $ (3.32). Total lots 27 343 $. Les lignes correspondantes (luminaires, enseigne, détecteurs, panneau, disjoncteurs, scan) sont à 0 $ avec le temps Dupuis.
3. **Quantités sur plan = relevé** (feuille Par libellé, contrôlée contre Marques ; portées du tableau de rapport-releve.md). Quantités hors plan (conduits, percements, rangées, frais de chantier) = feuille Détail de l'Estimation_2. Longueurs en m converties en pi (× 3,28084), arrondies vers le haut à la section de 10 pi.
4. **Conduits** : le catalogue n'a pas de colonne TEMPSEC → temps/pi seulement. Le filage (D-15, E-10, F-09, C-06, C-08) est inclus dans les assemblages « CONDUIT x/y nnCmm » (pas de ligne de fil séparée). Les courses sous dalle (D-13/E-08, 5 #12) sont prises en « CONDUIT 3/4 05C12 » (pas de 1 po 05C12 au catalogue). Les longueurs restent les hypothèses de l'Estimation_2 (30 m/course RDC, 25 m étage, 8 m/point d'éclairage) : c'est le poste qui pèse le plus (≈ 430 h sur 917) et la cause du ratio h/100 k$ élevé.
5. **PRISE DDFT INSTALLER 22** (E-104/E-105) : 1 DDFT (fontaine P2-61, D-07) en « PRISE DUPLEX 20A 125V GFI » → 3.30 ; les 21 autres comptées comme **prises 15 A M.A.L.T. isolée des postes** (R-007 : les deux symboles tombent dans la même famille ; le bordereau a un article 3.29) au prix/temps « PRISE DUPLEX 15A 120V ».
6. Sorties data INSTALLER 65 : 10 murales/colonne en « TEL/DATA 3/4 » (D-08, boîte + conduit vers l'entreplafond), 55 en « TEL/DATA ». Boutons d'appel/panique (D-11 + E-06 = 4) aussi en « TEL/DATA 3/4 » (boîte + conduit vide).
7. Pour éviter le double comptage, les lignes Détail D-01 à D-08, E-01 à E-05, A-01 à A-06 ne sont pas reprises : leurs dispositifs sont déjà comptés au relevé (installer / enlever / relocaliser).

## Hésitations
- **Lot éclairage** : le détail de METHODE (A1 2 035 + 4′ 3 480 + 3′ 3 450 + 1′ 660 + trousses 1 500 + E 1 425 + Z6 484,80) totalise 13 034,80 $, pas 11 893 $. J'ai retenu le montant confirmé **11 893 $** ; écart de 1 141,80 $ à valider avec Francis.
- « JCI 7 400 $ + 2 détecteurs 600 $ » lu comme 600 $ pour les deux détecteurs (et non 600 $ chacun).
- LUMINAIRE E : 3 (relevé, = lot) contre 4 (Estimation_2). Retenu 3.
- Temps luminaires : « FIXTURE TYPE A1 / C1 / E » à 0,75 h (conforme au « luminaire 0,75 h » de METHODE) plutôt que « LUMINAIRE A1 » 0,4 h / « LUMINAIRE C1 » 1,0 h (libellés identiques mais vus sur un seul autre projet).
- Annonciateur : « RELO PANN ANNOCIATEUR » 0 $ / 8 h (Standard, 2 projets) plutôt que « RELO PANNEAU ANNONCIA » 550 $ / 8 h (1 projet, plus récent). +550 $ si Dupuis voulait la rallonge de câble.
- Enlèvement de luminaires : 0,35 h (« ENLEVER FIXTURE ENCAST/1X4/2X2 », dernière valeur) alors que METHODE résume « luminaire enlevé 0,5 h ». Écart ≈ 6 h.
- Lecteurs de carte : « LECTEUR DE CARTE » 15 $ / 0,5 h (5 projets) plutôt que « LECTEUR CARTE » 0,35 h. Ventilés en 3.33 (faible tension), faute d'article dédié.
- Toit (6 moteurs E.A.R, A-10) : débranchement 0,4 h + sectionneur 1,2 h + rebranchement « MOTEUR » 0,75 h = 2,35 h/u au lieu des 4 h/u de l'Estimation.
- Chaudières (3.26 MCC) : « MOTEUR » 0,75 h chacune + TECK 10 m et 4 connecteurs Lumen ; les 6 h/u de l'Estimation (vérification des tiroirs CCM) non retenues.
- Retrait temporaire FabLab (A-08 21 × 0,6 h, A-09 24 × 0,5 h) : aucune famille « retrait/réinstallation temporaire » au catalogue, temps de l'Estimation gardés (jugement). « RELO ENCASTRE » 1 h aurait donné +20 h.
- Gardé en jugement (Estimation_2, à valider) : F-05 rangées 20 h, A-07 6 h, A-11 16 h, B-09 9 h, G-05 12 h, G-06 8 h, H-02 20 h, H-03 12 h, H-04 8 h. H-01 remplacé par « NACELLE » 1 250 $ / 16 h.
- Démontage (3.22 = relocalisations + retraits temporaires) et démolition (5.19 = E.A.E) : partage par jugement entre les deux articles du bordereau.

## Familles introuvables au catalogue Dupuis (prix Lumen 2026-10-07 + temps par jugement)
- Câble TECK90 3C #12 (CAB12TECK3C600V, 9,1875 $/m, 0,03 h/m) et connecteurs Star Teck 3/4 (IBETEK75120, 42,2247 $, 0,25 h).
- Corde de tirage Poly Line 430 (GRE430, 81,68 $, 0 h).
- Ancrages drop-in 3/8-16 (VISDIA3/816BX50, 32,26 $/pqt, 0 h : pose dans F-05).
- Pas d'assemblage « prise M.A.L.T. isolée » ni « retrait temporaire » (voir plus haut). Le sectionneur Hubbell HBL1372 a été trouvé au catalogue (« INTERR 30A 2P 600V CEMA1 », 117,84 $ = prix Lumen).
- Non chiffrés (inclus dans les assemblages Dupuis ou hors total) : flexible 3/8 des luminaires, Hydrotite/LFMC et connecteurs 5333 (raccord compris dans « MOTEUR »), marrettes, plaques Decora ; options OPT-1 à OPT-4 (câblage Cat6, parasismique, temps supplémentaire, postes temporaires).
