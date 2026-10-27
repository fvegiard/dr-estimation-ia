# Synthèse automatique — S-1902 (10 runs)

Référence : 194 000 $. Généré par `entrainement/synthese_runs.py` depuis `runs/*/rapport.json` (comparateur v2 : prix ±total_pct, heures ±heures_pct, chaque article ±article_pct). Un run est OK seulement si les trois critères passent.

| Run | Protocole | Prix ($) | Δ prix | Δ heures chargées | Articles hors seuil | Codes rappel / précision | ±1 % | Verdict |
|---|---|---|---|---|---|---|---|---|
| opus-1 | ancien | 168 000 | -13.4 % | -12.4 % | 10 (3.22, 3.24, 3.25, 3.27, 3.28, 3.33…) | 0.3973 / 0.3671 | non | ÉCART |
| opus-2 | ancien | 168 000 | -13.4 % | -11.4 % | 9 (3.24, 3.25, 3.27, 3.28, 3.31, 3.34…) | 0.6712 / 0.8033 | non | ÉCART |
| opus-3 | ancien | 180 000 | -7.2 % | -5.7 % | 11 (3.22, 3.23, 3.24, 3.25, 3.27, 3.28…) | 0.5616 / 0.519 | non | ÉCART |
| sonnet-1 | ancien | 170 000 | -12.4 % | -11.4 % | 12 (3.22, 3.24, 3.25, 3.27, 3.28, 3.29…) | 0.6575 / 0.5783 | non | ÉCART |
| sonnet-2 | ancien | 175 000 | -9.8 % | -9.5 % | 10 (3.22, 3.24, 3.25, 3.27, 3.28, 3.29…) | 0.6164 / 0.5056 | non | ÉCART |
| sonnet-3 | ancien | 169 000 | -12.9 % | -12.4 % | 13 (3.22, 3.23, 3.24, 3.25, 3.27, 3.28…) | 0.6438 / 0.5663 | non | ÉCART |
| sonnet-4 | ancien | 176 000 | -9.3 % | -6.7 % | 10 (3.23, 3.24, 3.25, 3.27, 3.28, 3.29…) | 0.8082 / 0.6941 | non | ÉCART |
| sonnet-5 | ancien | 180 000 | -7.2 % | -4.8 % | 13 (3.22, 3.23, 3.24, 3.25, 3.27, 3.28…) | 0.726 / 0.5955 | non | ÉCART |
| swarm-1 | ancien | 170 000 | -12.4 % | -11.4 % | 12 (3.22, 3.23, 3.24, 3.25, 3.27, 3.28…) | 0.5479 / 0.4301 | non | ÉCART |
| swarm-2 | ancien | 175 000 | -9.8 % | -7.6 % | 14 (3.23, 3.24, 3.25, 3.27, 3.28, 3.29…) | 0.3425 / 0.3049 | non | ÉCART |

Écart moyen sur le prix : -10.8 % ; écart-type 2.42 points (échantillon, n−1)
 ; 0/10 OK.

## Écart attribué aux décisions de portée (Δ ACCEO, $ ; Δ = run − référence)

Mode(s) : approximation par articles (ancien protocole).

| Décision | Runs où elle diffère | Moyenne | Min | Max | Stable ? |
|---|---|---|---|---|---|
| postes_composites | 10 | -9 641 | -9 652 | -9 605 | oui |
| monuments | 10 | -2 758 | -2 759 | -2 756 | oui |
| lot_eclairage | 10 | -3 195 | -16 741 | -377 | non |
| eae_hors_plan | 10 | -2 350 | -6 062 | +69 | non |
| conduits | 0 (identique à la référence dans 10 runs) | — | — | — | — |
| autres articles et décisions identiques (non attribués) | 10 | +1 033 | -4 617 | +16 227 | — |

Lecture : en mode « approximation par articles » (ancien protocole), l'effet d'une décision est l'écart des articles qu'elle touche, pas son effet exact ; en mode « exact » (nouveau protocole), c'est le run rechiffré avec la décision de la référence.
