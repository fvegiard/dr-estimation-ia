# Rapport S-1902 — swarm-1 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 57 584.46 | -9 064.61 | -13.60 % |
| heures_relevees | 1 045.85 | 929.15 | -116.70 | -11.16 % |
| heures_chargees | 1 050.00 | 930.00 | -120.00 | -11.43 % |
| total_acceo | 155 899.07 | 136 634.46 | -19 264.61 | -12.36 % |
| prix_vente | 194 000.00 | 170 000.00 | -24 000.00 | -12.37 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -12.37 % | ±3.0 % | non |
| heures chargées | -11.43 % | ±5.0 % (≥ 52.5 h) | non |
| articles hors seuil | 3.22, 3.23, 3.24, 3.25, 3.27, 3.28, 3.29, 3.30, 3.33, 3.34, 3.36, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.5479 / 0.4301 | — | — |

Lignes : réf 73, run 93, communes 40, écarts 22, manquantes 33, en plus 53

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 92.6 | 0.0 | 0.0 | -1368.18 | non |
| 3.23 | 53.66 | 41.8 | 2799.08 | 2186.2 | -1635.35 | non |
| 3.24 | 27.5 | 21.0 | 6335.0 | 3400.0 | -3495.17 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2729.96 | non |
| 3.26 | 4.0 | 1.5 | 30.0 | 50.0 | -193.73 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1656.68 | non |
| 3.28 | 92.0 | 29.38 | 4259.79 | 1620.25 | -7991.03 | non |
| 3.29 | 25.85 | None | 1689.82 | None | -3895.80 | non |
| 3.30 | 1.3 | 28.6 | 65.38 | 1438.36 | +3695.25 | non |
| 3.31 | 299.65 | 327.26 | 14431.68 | 14044.01 | +1882.99 | oui |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | -0.53 | oui |
| 3.33 | 131.27 | 43.55 | 3310.75 | 991.0 | -9817.09 | non |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2758.56 | non |
| 3.35 | 178.75 | 178.29 | 18678.93 | 17254.51 | -1510.00 | oui |
| 3.36 | 9.27 | 29.88 | 779.1 | 1051.12 | +2022.91 | non |
| 3.37 | 20.0 | 8.0 | 0.0 | 550.0 | -476.13 | oui |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | -2.08 | oui |
| 5.19 | 38.4 | 29.0 | 0.0 | 0.0 | -809.73 | oui |
| 6.1 | None | 56.0 | None | 1250.0 | +6014.33 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9647.71 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2758.56 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -1510.0 | 3.35 |
| eae_hors_plan | releve | comptes | -2177.91 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (-9569.45 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO -3170.44 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-08 | 21/0/0.85 | 21/0.0/0.6 | jugement (Estimation_2) A-08 — luminaires CONSERVER au relev |
| A-09 | 24/0/0.75 | 24/0.0/0.5 | jugement (Estimation_2) A-09 |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | Dupuis-temps[DISJ15A1P] — qté Détail B-02 ; prix au lot dist |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | Dupuis-temps[DISJ 100A 3P 120/240V 22 K] — disjoncteur 3P 1  |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | Dupuis-temps[DISJ 100A 3P 120/240V 22 K] — prix au lot |
| B-09 | 9/15.0/1.0 | 9/0.0/1.0 | jugement (Estimation_2) B-09 |
| C-03 | 2/15.0/0.5 | 2/25.0/0.75 | Dupuis[MOTEUR] — releve MOTEUR TRIPHASE INSTALLER (E-105 2)  |
| D-08 | 41/22.32/0.89 | 10/22.32/0.89 | Dupuis[TEL/DATA 3/4] — qté Détail D-08 (incluse dans les 65  |
| D-09 | 1/60.0/4.0 | 1/0.0/6.0 | jugement (Estimation_2) D-09 |
| D-10 | 1/17.43/1.0 | 1/0.0/2.0 | jugement (Estimation_2) D-10 |
| D-11 | 4/15.0/0.5 | 1/9.3069/1.0 | Lumen[IBE52151K+IBE52C13] + jugement (Estimation_2) D-11 — f |
| D-12 | 23/150.0/1.0 | 16/150.0/1.0 | Dupuis[PERCEMENT PLANCHER] — qté Détail D-12 |
| D-13 | 2148.9501999999998/4.1197/0.091 | 1575/3.4197/0.081 | Dupuis[CONDUIT 3/4 05C12] — Détail D-13 480 m + D-15 (5 cond |
| D-14 | 1656.8242/1.4097/0.056 | 1083/1.4097/0.056 | Dupuis[CONDUIT VIDE 3/4] — Détail D-14 330 m |
| D-16 | 23/9.26/0.25 | 32/9.2625/0.0 | Lumen[IBE72171K+IBE72C1] — famille 4-11/16 absente du catalo |
| E-02 | 2/1461.22/1.0 | 3/250.0/1.0 | Dupuis[MONUMENT PLANCHER] — releve MONUMENT PLANCHER INSTALL |
| F-02 | 33/0/0.75 | 12/0.0/0.75 | Dupuis-temps[FIXTURE TYPE C1] — releve LUMINAIRE C1 INSTALLE |
| F-05 | 20/50.0/1.0 | 20/0.0/1.0 | jugement (Estimation_2) F-05 — famille absente du catalogue  |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | Dupuis[CONDUIT 3/4 03C12] — Détail F-08 280 m + F-09 (3 cond |
| F-10 | 46/8.0/0.25 | 35/7.963/0.2 | Dupuis[BOITE OCTOG 1-1/2PO KO 1] — base Lumen IBE54151L ×35  |
| G-02 | 98.4252/1.8196999999999999/0.084 | 98/1.4097/0.056 | Dupuis[CONDUIT VIDE 3/4] — Détail G-02 30 m |
| G-04 | 1/0/8.0 | 1/550.0/8.0 | Dupuis[RELO PANNEAU ANNONCIA] — releve PANNEAU ANNONCIATEUR  |