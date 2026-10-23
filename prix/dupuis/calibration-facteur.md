# Calibration du facteur « sommaire ACCEO → prix remis » (Daniel Dupuis)

Généré par `entrainement/calibrer_facteur.py` depuis `prix/dupuis/couples-sommaire-prix-remis.csv`. Le facteur en vigueur reste
celui de `parametres.json` (1.244) tant que Jo n'en décide pas autrement.

| Dossier | Date | Sommaire ACCEO ($) | Prix remis ($) | Ratio | Plus bas ($) | Dupuis vs plus bas | Gagnant | Source | À vérifier |
|---|---|---|---|---|---|---|---|---|---|
| S-1844 | 2026-08-26 | 191 909.19 | 238 744 | 1.244 | — | — | — | METHODE.md §7 — courriel Dupuis 2026-08-26 (sommaire 191 909,19 $ → prix remis 238 744 $) |  |

## Facteur

Un seul couple exploitable (ratio 1.244) : écart-type indéfini, le facteur n'est pas calibré, il est posé. Il faut au moins 5 dossiers remis par Daniel avec leur sommaire ACCEO pour parler de calibration.

Sensibilité sur un sommaire de 155 899 $ :

| Facteur | Prix de vente ($) | vs facteur actuel |
|---|---|---|
| 1.200 | 187 000 | -3.5 % |
| 1.244 | 194 000 | +0.0 % |
| 1.300 | 203 000 | +4.5 % |
| 1.350 | 210 000 | +8.5 % |

## Position par rapport au plus bas soumissionnaire

Aucun résultat d'ouverture avec le prix du plus bas soumissionnaire dans le fichier.
