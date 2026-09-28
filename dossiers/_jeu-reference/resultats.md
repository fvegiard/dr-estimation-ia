# Jeu de référence — relevé IA vs projets Plan Expert de l'estimateur

_Généré par `python -m src.validation.jeu_reference` ; seuil d'appariement 1,2 % de la diagonale._

| S- | Marques humaines | Marques IA | Appariées | Manquantes IA | En trop IA | Rappel | Précision | Δ rappel | Δ précision |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| S-1714 | 7502 | 7385 | 7219 | 283 | 166 | 96.2 % | 97.8 % | +0.0 | +0.0 |
| S-1715 | 401 | 359 | 313 | 88 | 46 | 78.1 % | 87.2 % | +0.0 | +0.0 |
| S-1769 | 116 | 141 | 113 | 3 | 28 | 97.4 % | 80.1 % | +0.0 | +0.0 |
| S-1811 | 681 | 811 | 676 | 5 | 135 | 99.3 % | 83.4 % | +0.0 | +0.0 |
| S-1844 | 708 | 773 | 564 | 144 | 209 | 79.7 % | 73.0 % | +0.0 | +0.0 |

Régressions (> 1.0 point) : aucune

## Normalised labels (apprentissage/qpl-2021-2026/normalisation.json) — informative only

| S- | Label agreement raw | Label agreement canonical | Noise dropped H/IA | Recall (no noise) | Precision (no noise) |
|---|--:|--:|--:|--:|--:|
| S-1714 | 0.0 % | 0.7 % | 0/0 | 96.2 % | 97.8 % |
| S-1715 | 0.0 % | 1.0 % | 2/0 | 78.4 % | 87.2 % |
| S-1769 | 0.0 % | 0.0 % | 0/0 | 97.4 % | 80.1 % |
| S-1811 | 0.0 % | 0.0 % | 14/0 | 99.3 % | 83.4 % |
| S-1844 | 0.0 % | 0.0 % | 0/0 | 79.7 % | 73.0 % |

## Category agreement (src.qpl.categorie — rule-based, informative only)

Among matched couples (position-based, unchanged), share whose category (dispositif / luminaire / securite_incendie / telecom_donnees / chauffage / distribution / mecanique_moteur / autre / indetermine) agrees — regardless of exact label wording.

| S- | Matched couples | Category agreement |
|---|--:|--:|
| S-1714 | 7219 | 63.6 % |
| S-1715 | 313 | 70.0 % |
| S-1769 | 113 | 85.8 % |
| S-1811 | 676 | 87.1 % |
| S-1844 | 564 | 72.3 % |

### Top 5 disagreeing category pairs (all projects combined)

| Human category | AI category | Occurrences |
|---|---|--:|
| indetermine | securite_incendie | 907 |
| indetermine | dispositif | 452 |
| chauffage | dispositif | 409 |
| dispositif | luminaire | 239 |
| telecom_donnees | luminaire | 199 |
