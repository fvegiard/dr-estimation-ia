# Rapport S-1902 — sonnet-3 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 57 439.99 | -9 209.08 | -13.82 % |
| heures_relevees | 1 045.85 | 910.31 | -135.53 | -12.96 % |
| heures_chargees | 1 050.00 | 920.00 | -130.00 | -12.38 % |
| total_acceo | 155 899.07 | 135 639.99 | -20 259.08 | -12.99 % |
| prix_vente | 194 000.00 | 169 000.00 | -25 000.00 | -12.89 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -12.89 % | ±3.0 % | non |
| heures chargées | -12.38 % | ±5.0 % (≥ 52.5 h) | non |
| articles hors seuil | 3.22, 3.23, 3.24, 3.25, 3.27, 3.28, 3.29, 3.30, 3.33, 3.34, 3.36, 5.19, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.6438 / 0.5663 | — | — |

Lignes : réf 73, run 83, communes 47, écarts 30, manquantes 26, en plus 36

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 35.15 | 0.0 | 0.0 | -6226.79 | non |
| 3.23 | 53.66 | 43.7544 | 2799.08 | 2514.63 | -1104.82 | non |
| 3.24 | 27.5 | 17.0 | 6335.0 | 3400.0 | -3821.41 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2735.58 | non |
| 3.26 | 4.0 | 1.5 | 30.0 | 50.0 | -192.49 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1638.06 | non |
| 3.28 | 92.0 | 29.375 | 4259.79 | 1620.25 | -7966.73 | non |
| 3.29 | 25.85 | None | 1689.82 | None | -3895.80 | non |
| 3.30 | 1.3 | 28.6 | 65.38 | 1438.36 | +3718.92 | non |
| 3.31 | 299.65 | 296.617 | 14431.68 | 14686.24 | +163.55 | oui |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | +1.13 | oui |
| 3.33 | 131.27 | 51.95 | 3310.75 | 1081.0 | -8969.46 | non |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2756.08 | non |
| 3.35 | 178.75 | 174.2882 | 18678.93 | 16449.38 | -2511.24 | oui |
| 3.36 | 9.27 | 17.876 | 779.1 | 1051.12 | +1016.76 | non |
| 3.37 | 20.0 | 20.0 | 0.0 | 0.0 | +11.34 | oui |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | +4.54 | oui |
| 5.19 | 38.4 | 95.9 | 0.0 | 150.0 | +5111.30 | non |
| 6.1 | None | 56.0 | None | 1250.0 | +6060.67 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9604.79 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2756.08 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -2511.24 | 3.35 |
| eae_hors_plan | releve | comptes | -1115.49 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (-9910.73 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO -4271.49 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-01 | 39/0/0.5 | 40/0.0/0.5 | catalogue Dupuis «EQUIPEMENT A ENLEVER» (PRIX À UTILISER 0.0 |
| A-03 | 34/0/0.35 | 28/0.0/0.35 | catalogue Dupuis «ENLEVER PRISE» (PRIX À UTILISER 0.0 $, TEM |
| A-05 | 13/0/1.5 | 12/0.0/1.5 | catalogue Dupuis «RELO PRISE» (PRIX À UTILISER 0.0 $, TEMPS  |
| A-06 | 7/0/1.0 | 4/0.0/1.0 | catalogue Dupuis «RELO ENCASTRE» (PRIX À UTILISER 0.0 $, TEM |
| A-08 | 21/0/0.85 | 21/0.0/1.0 | catalogue Dupuis «RELO ENCASTRE» (PRIX À UTILISER 0.0 $, TEM |
| A-09 | 24/0/0.75 | 24/0.0/1.0 | catalogue Dupuis «RELO ENCASTRE» (PRIX À UTILISER 0.0 $, TEM |
| A-10 | 6/0/4.0 | 6/0.0/0.4 | catalogue Dupuis «DEBRANCHEMENT APPAREILAGE MECANIQUE» (PRIX |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | catalogue Dupuis «DISJ15A1P» (PRIX À UTILISER 0.0 $, TEMPS À |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | catalogue Dupuis «DISJ 100A 3P 120/240V 22 K» (PRIX À UTILIS |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | catalogue Dupuis «DISJ 100A 3P 120/240V 22 K» (PRIX À UTILIS |
| B-09 | 9/15.0/1.0 | 9/0.0/1 | jugement (Estimation_2, feuille Détail B-09 : 1 h/u) — mise  |
| C-03 | 2/15.0/0.5 | 2/25.0/0.75 | catalogue Dupuis «MOTEUR» (PRIX À UTILISER 25.0 $, TEMPS À U |
| C-04 | 3/15.0/0.35 | 3/25.0/0.75 | catalogue Dupuis «MOTEUR» (PRIX À UTILISER 25.0 $, TEMPS À U |
| C-07 | 262.4672/4.2441/0.1128 | 115/2.8997/0.076 | catalogue Dupuis «CONDUIT 3/4 04C12» (PRIX À UTILISER 2.8997 |
| D-02 | 5/439.42/6.85 | 20/77.45/1.125 | catalogue Dupuis «PRISE USB 125V 15 AMP» (PRIX À UTILISER 77 |
| D-06 | 8/64.81/1.175 | 25/64.81/1.175 | catalogue Dupuis «PRISE DUPLEX 15A 120V» (PRIX À UTILISER 64 |
| D-07 | 1/65.38/1.3 | 22/65.38/1.3 | catalogue Dupuis «PRISE DUPLEX 20A 125V GFI» (PRIX À UTILISE |
| D-08 | 41/22.32/0.89 | 10/22.32/0.89 | catalogue Dupuis «TEL/DATA 3/4» (PRIX À UTILISER 22.32 $, TE |
| D-09 | 1/60.0/4.0 | 1/0.0/6 | jugement (Estimation_2, feuille Détail D-09 : 6 h/lot) — rac |
| D-11 | 4/15.0/0.5 | 1/15.0/0.35 | catalogue Dupuis «DECLENCHEUR APPEL» (PRIX À UTILISER 15.0 $ |
| D-12 | 23/150.0/1.0 | 16/150.0/1.0 | catalogue Dupuis «PERCEMENT PLANCHER» (PRIX À UTILISER 150.0 |
| D-13 | 2148.9501999999998/4.1197/0.091 | 1575/1.8378/0.05 | catalogue Dupuis «COND TME 1PO» (PRIX À UTILISER 1.8378 $, T |
| D-14 | 1656.8242/1.4097/0.056 | 1083/1.4097/0.056 | catalogue Dupuis «CONDUIT VIDE 3/4» (PRIX À UTILISER 1.4097  |
| D-16 | 23/9.26/0.25 | 32/7.68/0.15 | catalogue Dupuis «BOITE CARREES 4 PO» (PRIX À UTILISER 7.68  |
| E-02 | 2/1461.22/1.0 | 3/250.0/1.0 | catalogue Dupuis «MONUMENT PLANCHER» (PRIX À UTILISER 250.0  |
| F-02 | 33/0/0.75 | 12/0.0/0.75 | catalogue Dupuis «FIXTURE TYPE C1» (PRIX À UTILISER 0.0 $, T |
| F-05 | 20/50.0/1.0 | 20/0.0/1 | jugement (Estimation_2, feuille Détail F-05 : 1 h/rangée) —  |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | catalogue Dupuis «CONDUIT 3/4 03C12» (PRIX À UTILISER 4.2441 |
| F-10 | 46/8.0/0.25 | 35/7.963/0.2 | catalogue Dupuis «BOITE OCTOG 1-1/2PO KO 1» (PRIX À UTILISER |
| G-02 | 98.4252/1.8196999999999999/0.084 | 98/1.4097/0.056 | catalogue Dupuis «CONDUIT VIDE 3/4» (PRIX À UTILISER 1.4097  |