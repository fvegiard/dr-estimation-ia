# Apprentissage — corpus Plan Expert 2021-2026

Source : `Z:\Soumission\mes projets` (856 .qpl rapatriés le 2026-09-24 ; 664 avec marques, 596 502 symboles).

| Fichier | Contenu |
|---|---|
| `dictionnaire-symboles.json` | 337 symboles canoniques : catégorie, sous-type, variantes fusionnées, occurrences, nb projets |
| `normalisation.json` | carte de fusion (87 variantes → canonique) + 16 étiquettes de bruit à ignorer |
| `categories.json` | classification brute des 439 étiquettes récurrentes (≥ 8 projets) |
| `profiles.json` | 601 projets profilés par mélange de catégories |
| `outils/` | `parse.py`, `catalog.py` (reproductibles), brief de classification |

Limites :
- Les .qpl ne contiennent aucun prix (Price CostEach = 0 partout) : les prix sont dans la base ACCEO EEWin (SQL Server), non extraite — accès à obtenir.
- Classification faite par agents à partir des libellés seuls ; les « indetermine » (66) et les codes courts (KS, RA, BA…) sont à valider par l'estimateur.
- Le dictionnaire n'est pas encore branché dans `releve/` ni mesuré sur le jeu de référence.
