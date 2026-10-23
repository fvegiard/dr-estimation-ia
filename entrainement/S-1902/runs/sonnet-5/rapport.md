# Rapport S-1902 — sonnet-5 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 59 759.04 | -6 890.03 | -10.34 % |
| heures_relevees | 1 045.85 | 997.18 | -48.67 | -4.65 % |
| heures_chargees | 1 050.00 | 1 000.00 | -50.00 | -4.76 % |
| total_acceo | 155 899.07 | 144 759.04 | -11 140.03 | -7.15 % |
| prix_vente | 194 000.00 | 180 000.00 | -14 000.00 | -7.22 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -7.22 % | ±3.0 % | non |
| heures chargées | -4.76 % | ±5.0 % (≥ 52.5 h) | oui |
| articles hors seuil | 3.22, 3.23, 3.24, 3.25, 3.27, 3.28, 3.29, 3.30, 3.33, 3.34, 3.36, 3.37, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.726 / 0.5955 | — | — |

Lignes : réf 73, run 89, communes 53, écarts 37, manquantes 20, en plus 36

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 89.0 | 0.0 | 0.0 | -1659.94 | non |
| 3.23 | 53.66 | 96.5944 | 2799.08 | 2833.29 | +3688.88 | non |
| 3.24 | 27.5 | 21.0 | 6335.0 | 3400.0 | -3491.74 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2731.07 | non |
| 3.26 | 4.0 | 3.391 | 30.0 | 266.78 | +184.48 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1653.01 | non |
| 3.28 | 92.0 | 29.375 | 4259.79 | 1620.25 | -7986.24 | non |
| 3.29 | 25.85 | None | 1689.82 | None | -3895.80 | non |
| 3.30 | 1.3 | 28.6 | 65.38 | 1438.36 | +3699.92 | non |
| 3.31 | 299.65 | 325.698 | 14431.68 | 13998.65 | +1757.82 | oui |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | -0.20 | oui |
| 3.33 | 131.27 | 57.85 | 3310.75 | 1450.8 | -8131.25 | non |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2758.07 | non |
| 3.35 | 178.75 | 174.2882 | 18678.93 | 18699.38 | -377.01 | oui |
| 3.36 | 9.27 | 29.932 | 779.1 | 1052.53 | +2033.96 | non |
| 3.37 | 20.0 | 8.0 | 0.0 | 0.0 | -1024.83 | non |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | -0.78 | oui |
| 5.19 | 38.4 | 35.15 | 0.0 | 0.0 | -280.77 | oui |
| 6.1 | None | 56.0 | None | 1250.0 | +6023.47 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9639.25 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2758.07 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -377.01 | 3.35 |
| eae_hors_plan | releve | comptes | -1940.71 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (-2684.55 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO +3575.00 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-01 | 39/0/0.5 | 40/0.0/0.5 | Catalogue Dupuis « EQUIPEMENT A ENLEVER » (dernier Dupuis 20 |
| A-03 | 34/0/0.35 | 28/0.0/0.35 | Catalogue Dupuis « ENLEVER PRISE » (dernier Dupuis 2026-08-2 |
| A-05 | 13/0/1.5 | 12/0.0/1.5 | Catalogue Dupuis « RELO PRISE » (dernier Dupuis 2026-05-05,  |
| A-06 | 7/0/1.0 | 4/0.0/1.0 | Catalogue Dupuis « RELO ENCASTRE » (dernier Dupuis 2026-06-0 |
| A-07 | 1/0/6.0 | 4/0.0/1.5 | Catalogue Dupuis « RELO INT » (dernier Dupuis 2026-05-05, s- |
| A-08 | 21/0/0.85 | 21/0.0/1.0 | Catalogue Dupuis « RELO ENCASTRE » (dernier Dupuis 2026-06-0 |
| A-09 | 24/0/0.75 | 24/0.0/1.0 | Catalogue Dupuis « RELO ENCASTRE » (dernier Dupuis 2026-06-0 |
| A-10 | 6/0/4.0 | 6/0.0/8.0 | Catalogue Dupuis « DISCONNECTER ET RECON » (dernier Dupuis 2 |
| B-01b | 14/0/0.75 | 1/0.0/4.0 | Catalogue Dupuis « ENL PANN 42CCT 120/208V » (dernier Dupuis |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | Catalogue Dupuis « DISJ15A1P » (dernier Dupuis 2026-03-09, 2 |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | Catalogue Dupuis « DISJ 100A 3P 120/240V 22 K » (dernier Dup |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | Catalogue Dupuis « DISJ 100A 3P 120/240V 22 K » (dernier Dup |
| B-09 | 9/15.0/1.0 | 9/0.0/1 | jugement (Estimation_2) — Détail B-09, 1 h/u à valider |
| C-03 | 2/15.0/0.5 | 2/25.0/0.75 | Catalogue Dupuis « MOTEUR » (dernier Dupuis 2026-02-19, S-16 |
| C-04 | 3/15.0/0.35 | 3/25.0/0.75 | Catalogue Dupuis « MOTEUR » (dernier Dupuis 2026-02-19, S-16 |
| C-04b | 3/133.49/1.0 | 3/165.61/0.75 | Catalogue Dupuis « SECTIONNEUR POR ENTRETIEN HUBHBL13R22 » ( |
| C-07 | 262.4672/4.2441/0.1128 | 115/2.8997/0.076 | Catalogue Dupuis « CONDUIT 3/4 04C12 » (dernier Dupuis 2026- |
| D-01 | 18/156.39000000000001/3.5300000000000002 | 23/64.81/1.175 | Catalogue Dupuis « PRISE DUPLEX 15A 120V » (dernier Dupuis 2 |
| D-02 | 5/439.42/6.85 | 20/77.45/1.125 | Catalogue Dupuis « PRISE USB 125V 15 AMP » (dernier Dupuis 2 |
| D-07 | 1/65.38/1.3 | 20/65.38/1.3 | Catalogue Dupuis « PRISE DUPLEX 20A 125V GFI » (dernier Dupu |
| D-08 | 41/22.32/0.89 | 45/22.32/0.89 | Catalogue Dupuis « TEL/DATA 3/4 » (dernier Dupuis 2026-09-23 |
| D-09 | 1/60.0/4.0 | 1/0.0/6 | jugement (Estimation_2) — Détail D-09, 6 h à valider |
| D-10 | 1/17.43/1.0 | 3/6.1778/0.25 | Catalogue Dupuis « BOITE CARRE 2-1/8PO KO 1 » (dernier Dupui |
| D-11 | 4/15.0/0.5 | 1/15.0/0.5 | Catalogue Dupuis « BOUTON HANDICAPE » (dernier Dupuis 2026-0 |
| D-12 | 23/150.0/1.0 | 16/150.0/1.0 | Catalogue Dupuis « PERCEMENT PLANCHER » (dernier Dupuis 2026 |
| D-12b | 8/13.53/0.5 | 16/13.53/0.5 | Catalogue Dupuis « COUPE FEU TUBE 10.1 FL O » (dernier Dupui |
| D-13 | 2148.9501999999998/4.1197/0.091 | 1575/3.4197/0.081 | Catalogue Dupuis « CONDUIT 3/4 05C12 » (dernier Dupuis 2026- |
| D-14 | 1656.8242/1.4097/0.056 | 1083/1.4097/0.056 | Catalogue Dupuis « CONDUIT VIDE 3/4 » (dernier Dupuis 2026-0 |
| D-16 | 23/9.26/0.25 | 32/6.1778/0.25 | Catalogue Dupuis « BOITE CARRE 2-1/8PO KO 1 » (dernier Dupui |
| E-01 | 2/143.58/2.98 | 2/64.81/1.175 | Catalogue Dupuis « PRISE DUPLEX 15A 120V » (dernier Dupuis 2 |
| E-02 | 2/1461.22/1.0 | 3/250.0/1.0 | Catalogue Dupuis « MONUMENT PLANCHER » (dernier Dupuis 2026- |
| F-02 | 33/0/0.75 | 12/0.0/0.75 | Catalogue Dupuis « FIXTURE TYPE C1 » (dernier Dupuis 2026-07 |
| F-05 | 20/50.0/1.0 | 20/0.0/1 | jugement (Estimation_2) — Détail F-05, 1 h/rangée à valider; |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | Catalogue Dupuis « CONDUIT 3/4 03C12 » (dernier Dupuis 2026- |
| F-10 | 46/8.0/0.25 | 35/7.963/0.2 | Catalogue Dupuis « BOITE OCTOG 1-1/2PO KO 1 » (dernier Dupui |
| G-01b | 2/300.0/0 | 1/0.0/0.75 | Catalogue Dupuis « RELO DETECTEUR A FUME » (dernier Dupuis 2 |
| G-02 | 98.4252/1.8196999999999999/0.084 | 99/1.4097/0.056 | Catalogue Dupuis « CONDUIT VIDE 3/4 » (dernier Dupuis 2026-0 |