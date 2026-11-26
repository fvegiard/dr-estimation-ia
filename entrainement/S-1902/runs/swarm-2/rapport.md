# Rapport S-1902 — swarm-2 : **ÉCART** (protocole ancien)

Δ = run − référence (négatif : le run est en dessous).

| Total | Référence | Run | Δ | % |
|---|---|---|---|---|
| materiel | 66 649.07 | 58 511.22 | -8 137.85 | -12.21 % |
| heures_relevees | 1 045.85 | 960.36 | -85.49 | -8.17 % |
| heures_chargees | 1 050.00 | 970.00 | -80.00 | -7.62 % |
| total_acceo | 155 899.07 | 140 961.22 | -14 937.85 | -9.58 % |
| prix_vente | 194 000.00 | 175 000.00 | -19 000.00 | -9.79 % |

| Critère | Mesure | Seuil | OK |
|---|---|---|---|
| prix de vente | -9.79 % | ±3.0 % | non |
| heures chargées | -7.62 % | ±5.0 % (≥ 52.5 h) | non |
| articles hors seuil | 3.23, 3.24, 3.25, 3.27, 3.28, 3.29, 3.30, 3.31, 3.33, 3.34, 3.35, 3.37, 5.19, 6.1 | ±10.0 % ou 1000 $ | non |
| dans ±1 % (historique) | non | — | — |
| codes : rappel / précision | 0.3425 / 0.3049 | — | — |

Lignes : réf 73, run 82, communes 25, écarts 19, manquantes 48, en plus 57

| Article | h réf | h run | mat réf | mat run | Δ total | dans le seuil |
|---|---|---|---|---|---|---|
| 3.22 | 108.35 | 114.0 | 0.0 | 0.0 | +443.66 | oui |
| 3.23 | 53.66 | 17.45 | 2799.08 | 748.52 | -5146.39 | non |
| 3.24 | 27.5 | 35.0 | 6335.0 | 3400.0 | -2306.79 | non |
| 3.25 | 7.6 | 6.8 | 0.0 | 2800.0 | +2729.43 | non |
| 3.26 | 4.0 | None | 30.0 | None | -371.35 | oui |
| 3.27 | 34.25 | 22.5 | 2197.1 | 1549.0 | -1658.42 | non |
| 3.28 | 92.0 | 29.375 | 4259.79 | 1620.25 | -7993.31 | non |
| 3.29 | 25.85 | None | 1689.82 | None | -3895.80 | non |
| 3.30 | 1.3 | 28.6 | 65.38 | 1438.36 | +3693.04 | non |
| 3.31 | 299.65 | 485.76 | 14431.68 | 21615.23 | +22901.32 | non |
| 3.32 | 2.0 | 2.0 | 1250.0 | 1250.0 | -0.68 | oui |
| 3.33 | 131.27 | 60.25 | 3310.75 | 1540.8 | -7851.16 | non |
| 3.34 | 4.0 | 3.0 | 3422.44 | 750.0 | -2758.79 | non |
| 3.35 | 178.75 | 54.625 | 18678.93 | 12549.06 | -16740.62 | non |
| 3.36 | 9.27 | 1.0 | 779.1 | 600.0 | -884.99 | oui |
| 3.37 | 20.0 | 8.0 | 0.0 | 0.0 | -1026.75 | non |
| 3.38 | 8.0 | 8.0 | 7400.0 | 7400.0 | -2.70 | oui |
| 5.19 | 38.4 | None | 0.0 | None | -3276.97 | non |
| 6.1 | None | 84.0 | None | 1250.0 | +8390.00 | non |

## Écart attribué aux décisions — approximation par articles (ancien protocole)

| Décision | Run | Référence | Δ ACCEO ($) | Δ prix ($) / articles |
|---|---|---|---|---|
| postes_composites | couverts | en_plus | -9651.73 | 3.27, 3.28 |
| monuments | dupuis | lumen | -2758.79 | 3.34 |
| lot_eclairage | readme_11893 | detail_13034_80 | -16740.62 | 3.35 |
| eae_hors_plan | releve | comptes | -2833.31 | 3.22, 5.19 |
| conduits | temps_pi | temps_pi | 0.0 | identique, non imputé (+9903.77 $ sur 3.23, 3.31, 3.33) |

Autres articles et décisions identiques (non attribués) : Δ ACCEO +16227.18 $

## Écarts par ligne (code commun)
| code | réf q/p/h | run q/p/h | source run |
|---|---|---|---|
| A-08 | 21/0/0.85 | 21/0.0/1.0 | q : entree/reference-Estimation_2.xlsx Détail A-08 (ligne Ex |
| A-09 | 24/0/0.75 | 24/0.0/1.0 | q : entree/reference-Estimation_2.xlsx Détail A-09 (ligne Ex |
| A-11 | 1/0/16.0 | 1/0.0/12.0 | q : Estimation_2 Détail A-11 (ligne 18) : Qté (D) = 1, Unité |
| B-02 | 17/0/0.2 | 14/0.0/0.2 | q : entree/reference-Estimation_2.xlsx Détail B-02 (ligne Ex |
| B-03 | 3/0/1.0 | 1/0.0/1.0 | q : entree/reference-Estimation_2.xlsx Détail B-03 (ligne Ex |
| B-04 | 3/0/0.4 | 1/0.0/1.0 | q : entree/reference-Estimation_2.xlsx Détail B-04 (ligne Ex |
| B-09 | 9/15.0/1.0 | 9/0.0/3.0 | q : entree/reference-Estimation_2.xlsx Détail B-09 (ligne Ex |
| C-07 | 262.4672/4.2441/0.1128 | 262/4.2441/0.1128 | q : Estimation_2 Détail C-07 (ligne 40) : Qté lue 80 m × 3,2 |
| D-09 | 1/60.0/4.0 | 1/25.0/0.5 | q : entree/reference-Estimation_2.xlsx Détail D-09 Qté 1 lot |
| D-11 | 4/15.0/0.5 | 1/15.0/0.35 | q : Estimation_2 Détail D-11 Qté 1 u ; note L : Aide au lect |
| D-12 | 23/150.0/1.0 | 16/150.0/1.0 | q : Estimation_2 Détail D-12 Qté 16 u ; note L : 1 percement |
| D-13 | 2148.9501999999998/4.1197/0.091 | 1575/4.3787/0.095 | q : Estimation_2 Détail D-13 (ligne 57) : Qté lue 480 m × 3, |
| D-14 | 1656.8242/1.4097/0.056 | 1083/1.4097/0.056 | q : Estimation_2 Détail D-14 (ligne 58) : Qté lue 330 m × 3, |
| D-16 | 23/9.26/0.25 | 1/327.3216/9.6 | q : Estimation_2 Détail D-16 Qté 1 lot ; note L : vide ; Réf |
| F-05 | 20/50.0/1.0 | 20/0.0/0.2 | q : entree/reference-Estimation_2.xlsx Détail F-05 (ligne Ex |
| F-08 | 918.6351999999999/4.2441/0.1128 | 919/4.2441/0.1128 | q : Estimation_2 Détail F-08 Qté 280 m × 3,2808 = 918,62 → 9 |
| F-10 | 46/8.0/0.25 | 1/278.705/7.0 | q : entree/reference-Estimation_2.xlsx Détail F-10 (ligne Ex |
| G-02 | 98.4252/1.8196999999999999/0.084 | 98/1.4097/0.056 | q : Estimation_2 Détail G-02 Qté 30 m × 3,2808 = 98,42 → 98  |
| H-01 | 1/1250.0/16.0 | 1/0.0/16.0 | q : Estimation_2 Détail H-01 (ligne 101) : Qté (D) = 1, Unit |