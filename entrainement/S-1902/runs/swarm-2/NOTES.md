# NOTES — essaim 2, chiffrage à l'aveugle S-1902 (méthode Dupuis)

Chef : Claude Fable 5.1 (claude-fable-5-1, réflexion élevée). Résultat : `chiffrage.json`, produit par `chiffrage.py`
(code de sortie 0, 82 lignes, 47 lignes à libellé unique revérifiées au catalogue sans écart, cohérences passées).

## 1. Résultat

| | |
|---|--:|
| Matériel (lots inclus une fois) | 58 511,22 $ |
| Heures relevées | 960,36 h |
| Heures chargées (dizaine supérieure) | 970 h |
| Taux (METHODE.md §5, août–octobre 2026) | 85 $/h |
| Main-d'œuvre | 82 450,00 $ |
| Total sommaire ACCEO | 140 961,22 $ |
| Facteur (METHODE.md §7) | 1,244 |
| **Prix de vente (arrondi au millier)** | **175 000 $** |

Contrôles METHODE.md §6 : part main-d'œuvre 58,5 % (plage 30–69 % : OK) ; 554 h par 100 k$ de prix de vente (plage
450–520 : au-dessus, non forcé — les 5 plus grosses lignes d'heures sont des conduits dont la longueur est une
hypothèse de Détail : D-13 149,6 h, F-08 103,7 h, D-14 60,6 h, SD-I 57,9 h, E-08 54,5 h).

## 2. Organigramme RÉEL (qui a tourné, effort demandé, scores remontés)

Mécanique : aucun niveau n'a l'outil Agent (vérifié : `claude -p` imbriqué plafonne à la profondeur 1 et le
classificateur refuse `acceptEdits`). Chaque niveau a donc ÉCRIT les prompts et choisi l'effort de ses subalternes
(`prompts/…`, en-tête `effort:` / `modele:`) ; la session principale a lancé les agents avec ces prompts tels quels,
puis relancé chaque niveau pour consolider. Modèles : chef Claude Fable 5.1 ; directeurs Claude Opus 5.5 ;
chefs de lot Claude Sonnet 5.5 ; releveurs Claude Haiku 5.5. 2 + 6 + 18 = 26 agents, tous lancés et tous rendus.

```
Chef — Claude Fable 5.1 (réflexion élevée) — ARCHITECTURE.md, prompts/directeur-A.md, prompts/directeur-B.md
├── Directeur A (Opus, effort high) — QUANTITÉS — lots/directeur-A.json : 81 lignes, 45 exclusions
│   contrôle du directeur : A1 7/7, A2 7/7, A3 7/7 (kit rouvert), aucun lot revu
│   ├── Chef A1 (Sonnet, high) — services sur plan — chef-A1.json 23 lignes ; contrôle 5/5, 5/5, 5/5
│   │   ├── A1-1 (Haiku, high)  PC/PU/PG + D-01…D-08, A-05 → releveur-A1-1.json 7 lignes
│   │   ├── A1-2 (Haiku, xhigh) SD/TV/MP/BJ + A-03, A-04, E-01…E-05, D-09, D-10 → 9 lignes
│   │   └── A1-3 (Haiku, high)  INT/TH/LC/GA/DM/BC + A-07 → 7 lignes
│   ├── Chef A2 (Sonnet, xhigh) — éclairage/urgence/alarme/mécanique/distribution — 34 lignes ; 5/5, 5/5, 5/5
│   │   ├── A2-1 (Haiku, high)  ENC/ENCU/L14/L22/L4/LLIN/HP + A-01, A-02, A-06, A-08, A-09, B-01…B-09 → 16 lignes
│   │   ├── A2-2 (Haiku, high)  LA1/LC1/LC11/LC13/LE/Z6 + F-01…F-07, F-10 → 8 lignes
│   │   └── A2-3 (Haiku, xhigh) DF/SM/PA/MM/MT + G-01, G-04…G-06, A-10, C-01…C-04, X-03 → 10 lignes
│   └── Chef A3 (Sonnet, high) — hors plan Détail — 26 lignes, 11 exclusions ; 6/6, 9/9, 5/5
│       ├── A3-1 (Haiku, xhigh) conduits/fils C-05…E-10 (m → pi) → 6 lignes
│       ├── A3-2 (Haiku, high)  F-08, F-09, G-02, G-03, D-11, D-12, D-16, E-06, E-07, E-11 → 9 lignes
│       │   (a aussi laissé prompts/releveur-A3-2-generer.py : script de contrôle/génération de son JSON)
│       └── A3-3 (Haiku, high)  A-11, H-01…H-04, G-07, OPT, lots, X-01, X-02 → 11 lignes
└── Directeur B (Opus, effort xhigh) — PRIX ET TEMPS — lots/directeur-B.json : 81 codes + 61 hors A, 5 lots
    contrôle du directeur : B1 5/5, B2 5/5, B3 5/5 + contrôle complet 43/43, 68/68, 6/6 ; aucun lot revu
    ├── Chef B1 (Sonnet, xhigh) — dispositifs — chef-B1.json 44 lignes ; 5/5, 5/5, 5/5 (graine 1902)
    │   ├── B1-1 (Haiku, xhigh) PC/PU/PG/TH → 15 lignes
    │   ├── B1-2 (Haiku, xhigh) SD/TV/INT/LC/GA/DM → 15 lignes
    │   └── B1-3 (Haiku, xhigh) BJ/MP/BC + D-09, D-10, D-11, E-03, E-06 → 14 lignes
    ├── Chef B2 (Sonnet, xhigh) — éclairage/alarme/mécanique/distribution/conduits/Lumen — 76 lignes ; 5/5 ×3 + 66/66
    │   ├── B2-1 (Haiku, high)  luminaires et enlèvements/relocalisations → 26 lignes
    │   ├── B2-2 (Haiku, xhigh) DF/SM/PA/MM/MT, B-01…B-09, HP → 28 lignes
    │   └── B2-3 (Haiku, xhigh) conduits/fils, percements, scan, nacelle, lots → 22 lignes
    └── Chef B3 (Sonnet, xhigh) — articles et doubles comptes — 21 lignes composées/jugement, 141 articles, 44 doubles
        ├── B3-1 (Haiku, xhigh) articles 120 codes + 13 règles + 20 doubles Lumen (0 ligne de prix)
        ├── B3-2 (Haiku, xhigh) lignes Détail composées/jugement (A-07…H-04) → 21 lignes
        └── B3-3 (Haiku, xhigh) doubles comptes plan/Détail (30) + 25 exclusions (0 ligne de prix)
```
Scores « x/5 » : chaque chef a rouvert le kit pour ≥ 5 lignes par releveur ; chaque directeur pour ≥ 5 (A : 7) lignes
par chef ; le chef (ce fichier) a revérifié au catalogue, par script, les 47 lignes à libellé unique du résultat final
(0 écart) et relu les 26 arbitrages des directeurs. Aucune erreur de valeur n'a été trouvée à aucun niveau ; les
désaccords sont des arbitrages (ci-dessous), pas des fautes de lecture.

## 3. Arbitrages de chaque niveau (résumé)

- **Chefs de lot A** : exclusion de 45 lignes Détail qui recomptent le plan (le plan gagne) ; LE-I 3 et non 4 ;
  PA-R (relocalisation) et non PA-I ; MT-I 4 / MM-I 3 / MM-R 6 remplacent C-01…C-04 et A-10 ; X-03 (sectionneurs HUM)
  créé ; fils RW90 exclus comme inclus dans l'assemblage du conduit apparié ; D-09 repris, D-10 exclu (BJ-I 3).
- **Directeur A** : E-03 et A-07 exclues (mêmes objets que MP et INT) ; X-01 exclu (= LOT-GPR) ; X-02 et H-01 gardés ;
  G-05 et G-06 gardés ; efforts A1 high / A2 xhigh / A3 high.
- **Chefs de lot B** : libellés Dupuis à la dernière valeur (jamais la médiane) ; analogues notés quand le libellé exact
  manque (ENLEVER PRISE pour SD-E/BJ-E/MP-E/DM-E, STATION ENL pour HP-E/DF-E) ; 0 $ forcé pour tout appareil couvert par un
  lot ; table d'articles R0–R13 (B3) ; 44 doubles comptes classés (ferme / tranché / à confirmer).
- **Directeur B** : D-13/E-08 passés en « CONDUIT 3/4 05C12 » (fil exclu par A) ; C-07 tout en 03C12 ; MM-R au composé
  (1,65 h) ; D-09 réduit au raccord ; A-11 réduit à 12 h ; coupe-feu inclus dans « PERCEMENT PLANCHER » ; Lumen jamais
  ajouté en plus d'un équivalent Dupuis ; LOT-ECL gardé à 11 893 $ ; efforts B1/B2/B3 xhigh.
- **Chef (Fable)** — 2 modifications et 1 ajout, le reste confirmé (`decisions` de chiffrage.json) :
  1. D-13 et E-08 : EMT 1 po + 5 #12 → composé « CONDUIT VIDE 1 » + 5 × « 12AWG SOLIDE RW90 600V » (4,3787 $/pi,
     0,095 h/pi) au lieu de « CONDUIT 3/4 05C12 » : on garde le diamètre du plan, option que B avait calculée.
  2. X-01 rétabli à 0 $ + 2 h (temps Dupuis du scan de dalle) ; LOT-GPR garde les 1 250 $ : un objet, payé une fois.
  3. Taux 85 $/h (METHODE.md), pas 124 $/h (Sommaire Jo) ; facteur 1,244 ; LOT-DIST ventilé 3 400 $ → 3.24, 2 800 $ → 3.25.

## 4. Hypothèses, hésitations, familles introuvables

- Quantités sur plan = relevé automatique « à VÉRIFIER » ; portées lues à ≤ 14 pt (R-002). CONSERVER = 0 travail.
- Longueurs de conduits : hypothèses de Détail (30 m / 25 m par course, 8 m × 35 points), non relevées.
- Heures « jugement (Estimation_2) » sans libellé Dupuis : A-11 (12 h), G-05 (12 h), G-06 (8 h), H-01…H-04 (56 h).
- Aucun libellé Dupuis direct : SD-E, BJ-E, MP-E, DM-E (→ ENLEVER PRISE 0,35 h), SD-R, MP-R (→ RELO PRISE 1,5 h),
  BC-E (→ CONTACT DE PORTE ENL 0,5 h), HP-E, DF-E (→ STATION ENL 0,5 h), boîte de jonction (→ BOITE CARRE 2-1/8PO),
  corde de tirage (→ Lumen GRE430 81,68 $ dans D-16), conduit 1 po à 5 conducteurs (composé).
- Contradictions du kit reprises dans `incoherences` (A-01/02 46 vs 40, A-03/04 44 vs 35, USB 10 vs 20, 19 vs 20
  disjoncteurs 1P, B-04 40 A vs 35 A, Z6 à l'étage, détecteurs E-007 vs plans, DDFT/M.A.L.T., LOT-ECL 13 034,80 vs 11 893).
- Hors total : AI-07 (option JCI), OPT-1…OPT-4, poke-through Lumen HUBS1R6PTDEHBLK (MP-I au repère Dupuis 250 $).

## 5. Ce que je changerais dans l'architecture

1. **Un seul schéma de codes, publié AVANT le lancement, avec la liste des codes attendus** — ça a marché (jointure
   81/81 sans trou), mais X-03 a dû être inventé par A puis rattrapé par B ; prévoir une règle « code X-nn » dans les
   deux briefs dès le départ.
2. **Donner au directeur B la liste des exclusions de A avant qu'il consolide** (ici il l'a lue lui-même dans lots/,
   ce qui a provoqué l'arbitrage D-13 « 05C12 ») ; mieux : faire tourner A, puis B sur la sortie de A, et garder le
   parallélisme seulement au niveau des chefs de lot.
3. **Les releveurs B3-1 et B3-3 n'ont produit aucune ligne de prix** (articles et doubles comptes seulement) : le lot
   « bordereau + doubles comptes » est un lot de règles, pas de relevé — 2 releveurs suffisent, le 3e aurait été plus
   utile sur les conduits (la plus grosse incertitude : 5 lignes = 42 % des heures).
4. **Effort** : les niveaux inférieurs ont presque tous choisi `xhigh` (15 des 18 releveurs B et A à high/xhigh) ;
   la grille §7 n'a pas assez discriminé — imposer un budget (ex. au plus un `xhigh` par chef) forcerait un vrai choix.
5. **Vérification croisée automatique** : le script du chef revérifie 47 lignes au catalogue ; cette vérification
   devrait être fournie comme outil (`verifier.py`) aux chefs de lot et directeurs, au lieu que chacun réécrive sa
   fonction `ligne(desc, um)`.
6. **Relevé des longueurs** : tant que les conduits viennent d'hypothèses, l'essaim ne peut pas faire mieux que le
   Détail sur 42 % des heures ; la prochaine itération doit relever les tracés sur plan (ou au moins les courses).
