# Rapport S-1902 — opus-2 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 55 655.69 | -10 993.38 | -16.49 % |
| heures_relevees | 1 045.85 | 924.71 | -121.14 | -11.58 % |
| heures_chargees | 1 050.00 | 930.00 | -120.00 | -11.43 % |
| total_acceo | 155 899.07 | 134 705.69 | -21 193.38 | -13.59 % |
| prix_vente | 194 000.00 | 168 000.00 | -26 000.00 | -13.40 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -13.40 % | ±3.0 % | non |
| heures chargées | -11.43 % | ±5.0 % (≥ 52.5 h) | non |
| articles hors seuil | 3.24, 3.25, 3.27, 3.28, 3.31, 3.34, 3.37, 5.19, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.6712 / 0.8033 | — | — |

Lignes : réf 73, run 73, communes 49, écarts 31, manquantes 24, en plus 12

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 102.15 | 0.0 | 0.0 | -563.59 | oui |
| 3.23 | 53.66 | 66.554 | 2799.08 | 2329.51 | +608.44 | oui |
| 3.24 | 27.5 | 21.0 | 6335.0 | 3400.0 | -3496.79 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2729.43 | non |
| 3.26 | 4.0 | 1.5 | 30.0 | 50.0 | -193.85 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1658.42 | non |
| 3.28 | 92.0 | 29.375 | 4259.79 | 1620.25 | -7993.30 | non |
| 3.29 | 25.85 | 25.725 | 1689.82 | 1263.99 | -445.18 | oui |
| 3.30 | 1.3 | 1.3 | 65.38 | 65.38 | -0.44 | oui |
| 3.31 | 299.65 | 221.129 | 14431.68 | 11202.39 | -10005.15 | non |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | -0.68 | oui |
| 3.33 | 131.27 | 136.342 | 3310.75 | 3326.87 | +402.73 | oui |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2758.79 | non |
| 3.35 | 178.75 | 178.288 | 18678.93 | 16642.6 | -2135.72 | oui |
| 3.36 | 9.27 | 19.042 | 779.1 | 755.69 | +804.27 | oui |
| 3.37 | 20.0 | 8.0 | 0.0 | 0.0 | -1026.75 | non |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | -2.70 | oui |
| 5.19 | 38.4 | 16.0 | 0.0 | 0.0 | -1916.97 | non |
| 6.1 | None | 56.0 | None | 1250.0 | +6010.00 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9651.72 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2758.79 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -2135.72 | 3.35 |
| eae_hors_plan | releve | comptes | -2480.56 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (-8993.98 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO -4616.67 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-01 | 39/0/0.5 | 8/0.0/0.35 | Dupuis « ENLEVER FIXTURE 2X2 » (prix 0.0 / temps 0.35 à util |
| A-03 | 34/0/0.35 | 10/0.0/0.5 | Dupuis « EQUIPEMENT A ENLEVER » (prix 0.0 / temps 0.5 à util |
| A-05 | 13/0/1.5 | 12/0.0/1.5 | Dupuis « RELO PRISE » (prix 0.0 / temps 1.5 à utiliser) ; qt |
| A-06 | 7/0/1.0 | 4/0.0/1.0 | Dupuis « RELO ENCASTRE » (prix 0.0 / temps 1.0 à utiliser) ; |
| A-08 | 21/0/0.85 | 21/0.0/1.0 | Dupuis « RELO ENCASTRE » (prix 0.0 / temps 1.0 à utiliser) ; |
| A-09 | 24/0/0.75 | 24/0.0/1.0 | Dupuis « RELO ENCASTRE » (prix 0.0 / temps 1.0 à utiliser) ; |
| B-01 | 1/0/8.0 | 1/0.0/4.0 | Dupuis « ENL PANN 42CCT 120/208V » (prix 0.0 / temps 4.0 à u |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | Dupuis « DISJ15A1P » (prix 0.0 / temps 0.2 à utiliser) — 0 $ |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | Dupuis « DISJ 100A 3P 120/240V 22 K » (prix 719.6 / temps 1. |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | Dupuis « DISJ 100A 3P 120/240V 22 K » (prix 719.6 / temps 1. |
| B-09 | 9/15.0/1.0 | 9/0.0/1.0 | jugement (Estimation_2, Détail B-09 : 1 h/u) ; qté : Détail |
| C-03 | 2/15.0/0.5 | 2/25.0/0.75 | Dupuis « MOTEUR » (prix 25.0 / temps 0.75 à utiliser) ; qté  |
| C-04 | 3/15.0/0.35 | 3/165.61/0.75 | Dupuis « SECTIONNEUR POR ENTRETIEN HUBHBL13R22 » (prix 165.6 |
| C-07 | 262.4672/4.2441/0.1128 | 148/4.2441/0.1128 | Dupuis « CONDUIT 3/4 03C12 » (prix 4.2441 / temps 0.1128 à u |
| D-01 | 18/156.39000000000001/3.5300000000000002 | 55/13.96/0.63 | Dupuis « TEL/DATA » (prix 13.96 / temps 0.63 à utiliser) ; q |
| D-02 | 5/439.42/6.85 | 20/77.45/1.125 | Dupuis « PRISE USB 125V 15 AMP » (prix 77.45 / temps 1.125 à |
| D-06 | 8/64.81/1.175 | 25/64.81/1.175 | Dupuis « PRISE DUPLEX 15A 120V » (prix 64.81 / temps 1.175 à |
| D-08 | 41/22.32/0.89 | 10/22.32/0.89 | Dupuis « TEL/DATA 3/4 » (prix 22.32 / temps 0.89 à utiliser) |
| D-09 | 1/60.0/4.0 | 1/0.0/6.0 | jugement (Estimation_2, Détail D-09 : 6 h/lot) ; qté : Détai |
| D-10 | 1/17.43/1.0 | 1/0.0/2.0 | jugement (Estimation_2, Détail D-10 : 2 h/u) ; qté : Détail |
| D-11 | 4/15.0/0.5 | 4/22.32/0.89 | Dupuis « TEL/DATA 3/4 » (prix 22.32 / temps 0.89 à utiliser) |
| D-13 | 2148.9501999999998/4.1197/0.091 | 2149/3.4197/0.081 | Dupuis « CONDUIT 3/4 05C12 » (prix 3.4197 / temps 0.081 à ut |
| D-14 | 1656.8242/1.4097/0.056 | 1657/1.4097/0.056 | Dupuis « CONDUIT VIDE 3/4 » (prix 1.4097 / temps 0.056 à uti |
| D-16 | 23/9.26/0.25 | 32/6.1778/0.25 | Dupuis « BOITE CARRE 2-1/8PO KO 1 » (prix 6.1778 / temps 0.2 |
| E-02 | 2/1461.22/1.0 | 3/250.0/1.0 | Dupuis « MONUMENT PLANCHER » (prix 250.0 / temps 1.0 à utili |
| F-02 | 33/0/0.75 | 12/0.0/0.75 | Dupuis « FIXTURE TYPE C1 » (prix 0.0 / temps 0.75 à utiliser |
| F-05 | 20/50.0/1.0 | 20/0.0/1.0 | jugement (Estimation_2, Détail F-05 : 1 h/rangée) ; qté : Dé |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | Dupuis « CONDUIT 3/4 03C12 » (prix 4.2441 / temps 0.1128 à u |
| F-10 | 46/8.0/0.25 | 2/32.26/0.0 | Lumen VISDIA3/816BX50 « USCAN ANCRAGE DROP-IN 3/8-16 (pqt 50 |
| G-02 | 98.4252/1.8196999999999999/0.084 | 98/1.5887/0.054 | Dupuis « COND ALARME 3/16 FT4 » (prix 1.5887 / temps 0.054 à |
| G-07 | 1/7400.0/0 | 1/0.0/0.0 | jugement (Estimation_2, Détail G-07 : 0 h/lot) ; qté : Détai |