# Rapport S-1902 — sonnet-4 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 58 473.25 | -8 175.82 | -12.27 % |
| heures_relevees | 1 045.85 | 978.19 | -67.65 | -6.47 % |
| heures_chargees | 1 050.00 | 980.00 | -70.00 | -6.67 % |
| total_acceo | 155 899.07 | 141 773.25 | -14 125.82 | -9.06 % |
| prix_vente | 194 000.00 | 176 000.00 | -18 000.00 | -9.28 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -9.28 % | ±3.0 % | non |
| heures chargées | -6.67 % | ±5.0 % (≥ 52.5 h) | non |
| articles hors seuil | 3.23, 3.24, 3.25, 3.27, 3.28, 3.29, 3.30, 3.34, 3.37, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.8082 / 0.6941 | — | — |

Lignes : réf 73, run 85, communes 59, écarts 42, manquantes 14, en plus 26

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 113.0 | 0.0 | 0.0 | +358.66 | oui |
| 3.23 | 53.66 | 41.31 | 2799.08 | 2023.81 | -1843.00 | non |
| 3.24 | 27.5 | 17.0 | 6335.0 | 3400.0 | -3836.79 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2729.43 | non |
| 3.26 | 4.0 | 1.5 | 30.0 | 50.0 | -193.85 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1658.42 | non |
| 3.28 | 92.0 | 29.38 | 4259.79 | 1620.25 | -7992.88 | non |
| 3.29 | 25.85 | None | 1689.82 | None | -3895.80 | non |
| 3.30 | 1.3 | 28.6 | 65.38 | 1438.36 | +3693.04 | non |
| 3.31 | 299.65 | 275.18 | 14431.68 | 14339.91 | -2273.30 | oui |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | -0.68 | oui |
| 3.33 | 131.27 | 136.4 | 3310.75 | 3328.28 | +409.07 | oui |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2758.79 | non |
| 3.35 | 178.75 | 174.29 | 18678.93 | 16449.38 | -2668.77 | oui |
| 3.36 | 9.27 | 20.08 | 779.1 | 824.25 | +961.06 | oui |
| 3.37 | 20.0 | 8.0 | 0.0 | 0.0 | -1026.75 | non |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | -2.70 | oui |
| 5.19 | 38.4 | 35.15 | 0.0 | 0.0 | -289.22 | oui |
| 6.1 | None | 56.0 | None | 1250.0 | +6010.00 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9651.3 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2758.79 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -2668.77 | 3.35 |
| eae_hors_plan | releve | comptes | 69.44 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (-3707.23 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO +729.73 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-01 | 39/0/0.5 | 40/0.0/0.5 | METHODE.md §3 « luminaire enlevé 0,5 h » (libellé absent du  |
| A-03 | 34/0/0.35 | 28/0.0/0.35 | catalogue Dupuis « ENLEVER PRISE » (PRIX/TEMPS À UTILISER, d |
| A-05 | 13/0/1.5 | 12/0.0/1.5 | catalogue Dupuis « RELO PRISE » (PRIX/TEMPS À UTILISER, dern |
| A-06 | 7/0/1.0 | 4/0.0/1.0 | catalogue Dupuis « RELO ENCASTRE » (PRIX/TEMPS À UTILISER, d |
| A-08 | 21/0/0.85 | 21/0.0/1.0 | catalogue Dupuis « RELO ENCASTRE » (PRIX/TEMPS À UTILISER, d |
| A-09 | 24/0/0.75 | 24/0.0/1.0 | catalogue Dupuis « RELO ENCASTRE » (PRIX/TEMPS À UTILISER, d |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | catalogue Dupuis « DISJ15A1P » (PRIX/TEMPS À UTILISER, derni |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | catalogue Dupuis « DISJ 100A 3P 120/240V 22 K » (PRIX/TEMPS  |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | catalogue Dupuis « DISJ 100A 3P 120/240V 22 K » (PRIX/TEMPS  |
| B-09 | 9/15.0/1.0 | 9/0.0/1.0 | jugement (Estimation_2) — Détail B-09, 1 h/u à valider |
| C-03 | 2/15.0/0.5 | 2/25.0/0.75 | catalogue Dupuis « MOTEUR » (PRIX/TEMPS À UTILISER, dernier  |
| C-04 | 3/15.0/0.35 | 3/25.0/0.75 | catalogue Dupuis « MOTEUR » (PRIX/TEMPS À UTILISER, dernier  |
| C-04b | 3/133.49/1.0 | 3/117.84/2.0 | prix Lumen HUBHBL1372 « HUBBELL HBL1372 SECTIONNEUR 30A 2P » |
| C-07 | 262.4672/4.2441/0.1128 | 263/1.4097/0.056 | catalogue Dupuis « CONDUIT VIDE 3/4 » (PRIX/TEMPS À UTILISER |
| C-08 | 7/40.0/0.25 | 903/0.3896/0.005 | catalogue Dupuis « 12AWG SOLIDE RW90 600V » (PRIX/TEMPS À UT |
| D-01 | 18/156.39000000000001/3.5300000000000002 | 18/35.43/0.9 | catalogue Dupuis « DROP DE PRISE » (PRIX/TEMPS À UTILISER, d |
| D-02 | 5/439.42/6.85 | 20/77.45/1.125 | catalogue Dupuis « PRISE USB 125V 15 AMP » (PRIX/TEMPS À UTI |
| D-03 | 2/64.81/1.175 | 2/35.43/0.9 | catalogue Dupuis « DROP DE PRISE » (PRIX/TEMPS À UTILISER, d |
| D-06 | 8/64.81/1.175 | 25/64.81/1.175 | catalogue Dupuis « PRISE DUPLEX 15A 120V » (PRIX/TEMPS À UTI |
| D-07 | 1/65.38/1.3 | 22/65.38/1.3 | catalogue Dupuis « PRISE DUPLEX 20A 125V GFI » (PRIX/TEMPS À |
| D-08 | 41/22.32/0.89 | 10/22.32/0.89 | catalogue Dupuis « TEL/DATA 3/4 » (PRIX/TEMPS À UTILISER, de |
| D-09 | 1/60.0/4.0 | 1/0.0/6.0 | jugement (Estimation_2) — Détail D-09, 6 h/u à valider; 2 bo |
| D-10 | 1/17.43/1.0 | 1/0.0/2.0 | jugement (Estimation_2) — Détail D-10, 2 h/u à valider; 1 bo |
| D-11 | 4/15.0/0.5 | 4/7.68/0.0 | catalogue Dupuis « BOITE CARREES 4 PO » (PRIX/TEMPS À UTILIS |
| D-12 | 23/150.0/1.0 | 16/150.0/1.0 | catalogue Dupuis « PERCEMENT PLANCHER » (PRIX/TEMPS À UTILIS |
| D-13 | 2148.9501999999998/4.1197/0.091 | 1575/2.4307/0.07 | catalogue Dupuis « CONDUIT VIDE 1 » (PRIX/TEMPS À UTILISER,  |
| D-14 | 1656.8242/1.4097/0.056 | 1083/1.4097/0.056 | catalogue Dupuis « CONDUIT VIDE 3/4 » (PRIX/TEMPS À UTILISER |
| D-16 | 23/9.26/0.25 | 1/0.0/8.0 | jugement (Estimation_2) — Détail D-16, 8 h/u à valider |
| D-17 | 22/76.81/1.175 | 55/13.96/0.63 | catalogue Dupuis « TEL/DATA » (PRIX/TEMPS À UTILISER, dernie |
| D-19 | 1/1250.0/2.0 | 2/35.0/0.4 | catalogue Dupuis « THERMOSTAT » (PRIX/TEMPS À UTILISER, dern |
| D-20 | 7/30.0/0.85 | 2/15.0/0.5 | catalogue Dupuis « LECTEUR DE CARTE » (PRIX/TEMPS À UTILISER |
| D-21 | 6/35.0/0.4 | 1/0.0/2.0 | catalogue Dupuis « SCAN DALLE BETON » (PRIX/TEMPS À UTILISER |
| E-01 | 2/143.58/2.98 | 2/35.43/0.9 | catalogue Dupuis « DROP DE PRISE » (PRIX/TEMPS À UTILISER, d |
| E-02 | 2/1461.22/1.0 | 3/250.0/1.0 | catalogue Dupuis « MONUMENT PLANCHER » (PRIX/TEMPS À UTILISE |
| E-04 | 3/64.81/1.175 | 3/35.43/0.9 | catalogue Dupuis « DROP DE PRISE » (PRIX/TEMPS À UTILISER, d |
| F-02 | 33/0/0.75 | 12/0.0/0.75 | catalogue Dupuis « FIXTURE TYPE C1 » (PRIX/TEMPS À UTILISER, |
| F-05 | 20/50.0/1.0 | 20/0.0/1.0 | jugement (Estimation_2) — Détail F-05, 1 h/u à valider; trou |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | catalogue Dupuis « CONDUIT 3/4 03C12 » (PRIX/TEMPS À UTILISE |
| F-10 | 46/8.0/0.25 | 35/7.963/0.2 | catalogue Dupuis « BOITE OCTOG 1-1/2PO KO 1 » (PRIX/TEMPS À  |
| G-01b | 2/300.0/0 | 1/0.0/0.75 | catalogue Dupuis « RELO DETECTEUR A FUME » (PRIX/TEMPS À UTI |
| G-02 | 98.4252/1.8196999999999999/0.084 | 99/1.4097/0.056 | catalogue Dupuis « CONDUIT VIDE 3/4 » (PRIX/TEMPS À UTILISER |
| G-07 | 1/7400.0/0 | 1/0.0/0.0 | jugement (Estimation_2) — Détail G-07, 0 h/u à valider |