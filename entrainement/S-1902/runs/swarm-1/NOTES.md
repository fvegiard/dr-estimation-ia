# NOTES — chiffrage à l'aveugle S-1902 (swarm-1)

## Modèles et organisation (à lire en premier)
- Chef d'équipe : **Claude Opus 5.5** (`claude-opus-5-5`, observé dans le contexte système de la session).
- Équipiers prévus : 5 × Claude Sonnet 5.5 via l'outil Agent. **Cet outil n'était pas disponible dans la session**
  (absent de la liste des outils ; une recherche `select:Agent` ne renvoie rien). Aucun sous-agent n'a donc été lancé.
  Les 5 lots ont été rédigés par le chef (Opus 5.5) selon le découpage prévu ; chaque `lots/lot-N.json` l'indique
  dans son champ `equipier`. Le lot 5 (vérificateur) est une relecture faite par la même instance : elle ne vaut
  pas une vérification indépendante.
- Aucun fichier lu hors de `swarm-1/` ; le kit n'a pas été modifié.

## Résultat (`python3 chiffrage.py`, code de sortie 0)
| clé | valeur |
|---|--:|
| taux | 85 $/h |
| materiel | 57 584,46 $ (lots fournisseur compris : 27 343 $) |
| heures_relevees | 929,15 h |
| heures_chargees | 930 h |
| main_doeuvre | 79 050,00 $ |
| total_acceo | 136 634,46 $ |
| facteur | 1,244 |
| prix_vente | 170 000 $ (136 634,46 × 1,244 = 169 973,27) |

93 lignes. Contrôles : part de la MO 57,9 % (Dupuis : 30 à 69 %) ; **547 h par 100 k$, au-dessus de la plage Dupuis
(450 à 520)**, à cause des conduits sous dalle à longueur supposée (D-13/D-14/E-08/E-09 = 266,9 h, soit 29 % des heures).

## Découpage
| lot | contenu | lignes |
|---|---|--:|
| 1 | Appareils sur plan avec portées (INSTALLER, ENLEVER, RELOCALISER) + démantèlement A-07..A-11 + luminaires neufs (temps) | 30 |
| 2 | Conduits/filage (D-13/14, E-08/09, F-08), percements + coupe-feu, boîtes (D-16, E-11, F-10), JB, boutons | 24 |
| 3 | Panneau PP-3, disjoncteurs (B-), raccordements mécaniques (C-), frais de chantier (H-), lot distribution | 24 |
| 4 | Data, alarme incendie (G-), enseignes Z6, lots éclairage / JCI / détecteurs, GPR | 15 |
| 5 | Vérification croisée (13 remarques V-01..V-13) + ventilation par article — aucune ligne | 0 |

`chiffrage.py` relit les lots et **recontrôle chaque ligne contre sa source** : catalogue (PRIX/TEMPS À UTILISER),
feuille Matériel Lumen, heures du Détail, lots de METHODE.md. Il vérifie aussi que chaque famille × portée
non CONSERVER du relevé est citée (38/38, contrôle testé avec un cas manquant), qu'aucun code n'est en double et
que matériel + heures chargées × taux = total ACCEO. Il s'arrête en erreur sinon.
Dans `lignes`, **p et h sont unitaires** ($/unité, h/unité).

## Décisions du chef sur les remarques du vérificateur
- V-01 (DDFT / M.A.L.T. isolée) : **maintenu** en GFI (Dupuis PRISE DUPLEX 20A 125V GFI). **L'article 3.29 reste à 0 $**
  alors que le bordereau exige un montant à chaque article : il faut départager les 22 prises au zoom sur E-104 avant le dépôt.
- V-02 (relevé contre Détail D-01..D-07, E-01, E-04, E-05) : **le relevé fait foi**. Ces lignes du Détail ne sont pas reprises,
  puisqu'il s'agit des mêmes appareils regroupés en postes. Écart signalé : 67 prises neuves au relevé contre environ 78
  impliquées par le Détail.
- V-03, V-04, V-05 (F-05 suspension, recouvrement JB / D-09-D-10 ≤ 0,9 h, coupe-feu à part) : **maintenus**. Ce sont des travaux
  exigés au devis, distincts du temps unitaire de l'appareil.
- V-06 (lot éclairage) : **montant confirmé 11 893 $ retenu**. Sa décomposition (METHODE.md) fait 13 034,80 $ ; l'écart de 1 141,80 $
  est à faire confirmer par Francis.
- V-07 : « 2 détecteurs 600 $ » est lu comme 600 $ pour les deux (la lecture « 600 $ chacun » ajouterait 600 $).
- V-08, V-09, V-11, V-12 : catalogue Dupuis prioritaire (monument 250 $ et non Hubbell 1 461 $ ; enlever luminaire 0,35 h et non
  0,5 h ; 3/4 05C12 pour les courses à 5 #12) ; A-10 compté une seule fois.
- V-10 (frais H- ventilés à l'article 6.1 ou au prorata) : **6.1 conservé**. La répartition au prorata reste possible sans changer
  le total.
- V-13 : taux de 85 $/h (METHODE, Dupuis d'août à octobre 2026) et non 124 $/h (référence Jo de l'Estimation_2).

## Hypothèses
- Portées : tableau familles × portées de `rapport-releve.md` (la feuille Marques ne porte pas la portée).
- Les quantités hors plan viennent de la feuille Détail (Estimation_2), mais **les heures sont remplacées par le temps Dupuis**
  quand la famille existe au catalogue. Le jugement de l'Estimation_2 n'est gardé que pour les familles absentes :
  A-07..A-11, B-09, D-09..D-11, D-16, E-06, E-11, F-05, G-05, G-06, H-02..H-04.
- Longueurs de conduits : hypothèses de l'Estimation_2 (30 m par course au RDC, 25 m à l'étage, 8 m par point d'éclairage),
  converties à 3,28084 pi/m. Il n'y a pas de colonne TEMPSEC au catalogue, donc le temps est compté au pied (règle 3).
  Les libellés CONDUIT xxCyy incluent les conducteurs : D-15, E-10, F-09, C-06 et C-08 ne sont pas comptés à part.
- Lots (METHODE.md, confirmés le 2026-10-20) : éclairage 11 893 $ ; distribution 6 200 $ (3 400 $ à l'article 3.24 et 2 800 $
  à l'article 3.25) ; JCI 7 400 $ ; détecteurs 600 $ ; GPR 1 250 $ (= ligne SCAN DALLE BETON, avec 2 h, comptée une seule fois).
- Panneaux, disjoncteurs, luminaires, enseignes et détecteurs sont à 0 $ en ligne (temps seulement). Panneau : temps de
  PANNEAU 225A 120/208V 3F (8 h). Le libellé « PANNEAU 225A 347/600V 3 » porte 0 h, il n'est donc pas retenu.
- Nacelle (catalogue : 1 250 $ et 16 h) à la place de H-01 (16 h jugées, plateforme comprise).
- Data : 10 sorties murales (D-08) en TEL/DATA 3/4 ; les 55 autres sorties INSTALLER du relevé en TEL/DATA.
- Le relevé compte 3 luminaires E, le Détail 4 : 3 sont retenus (R-003 et lot éclairage).
- Exclus, comme au Détail : OPT-1 (Cat6), OPT-2 (parasismique), OPT-3 (prime hors heures), OPT-4 (temporaires).

## Familles introuvables au catalogue Dupuis
| besoin | traitement |
|---|---|
| boîtes de tirage 4-11/16 + couvercles (D-16, E-11) | Lumen IBE72171K + IBE72C1 ; heures jugées (Détail) |
| corde de tirage | Lumen GRE430 |
| boîtes de boutons d'appel (D-11, E-06) | Lumen IBE52151K + IBE52C13 ; 1 h jugée |
| flexible 3/8 et connecteurs BX des descentes de luminaires | Lumen THOABRH03830, IBE2210 ; temps compris dans le luminaire |
| ancrages drop-in 3/8 | Lumen VISDIA3/816BX50 |
| enlever une sortie data, enlever un détecteur de mouvement | jugement, par analogie avec ENLEVER PRISE / ENLEVER INTERRUPTEUR (0,35 h) |
| relocaliser une sortie data | jugement, par analogie avec RELO PRISE (1,5 h) |
| suspension des rangées linéaires (F-05) ; travaux de toit (A-10) ; FabLab (A-08, A-09) | jugement (Estimation_2) |
| prise M.A.L.T. isolée | non départagée (V-01) |

## Lignes où le chef a hésité
- RL-02 (GFI ou MALT isolée), F-05 (risque de double compte), D-12-CF (coupe-feu en plus d'un prix d'assemblage),
  D-13/E-08 (EMT 1" du Détail chiffré avec un libellé 3/4), C-03 (6 h jugées remplacées par 0,75 h Dupuis).
- LECTEUR DE CARTE (0,5 h, 5 projets) retenu plutôt que LECTEUR CARTE (0,35 h, 2 projets).
- Contradiction UTA-1 : disjoncteur 40 A (E-502) contre MOCP 35 A (E-009), à clarifier avec l'ingénieur. Sans effet sur le chiffrage.
