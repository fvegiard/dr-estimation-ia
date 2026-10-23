# `entrainement/` — banc de chiffrage à l'aveugle (protocole v2, 2026-10-23)

Le banc mesure si un modèle, avec le seul kit d'un dossier, retrouve le chiffrage de référence du dossier. Depuis le
protocole v2, **le modèle ne chiffre jamais** : il relève (`quantites.json`) et tranche (`decisions.json`) ; un moteur
commun et déterministe transforme ces deux fichiers en `chiffrage.json`. Le prix ne dépend plus du script que chaque
run réécrivait ; la variance entre runs mesure ce qui compte : le relevé et les décisions de portée.

## Pourquoi (contre-évaluation du banc v1, 2026-10-23)

- 10 runs v1 (8 solos, 2 essaims) : tous entre −7,2 % et −13,4 % de la référence, écart-type 2,65 points. Avec un tel
  écart-type, « 8/8 dans ±1 % » a une probabilité nulle même une fois le biais corrigé ; seul un chiffrage déterministe
  (écart-type résiduel sous 0,5 %) rend cette cible atteignable.
- Tous les runs ont pris les mêmes décisions de portée (postes composites écartés, monuments au prix Dupuis, lot
  éclairage 11 893 $, démantèlement aux quantités du relevé) : l'écart était dans la règle écrite, pas dans le modèle.
- Un total dans ±1 % peut cacher des erreurs qui se compensent (+6 219 $ en 6.1 contre −3 656 $ en 3.24 dans les runs v1) :
  le verdict porte maintenant sur le prix, les heures ET chaque article du bordereau.

## Fichiers

| Fichier | Rôle |
|---|---|
| `chiffrage_commun.py` | moteur : `quantites.json` + `decisions.json` + `parametres.json` + catalogue → `chiffrage.json` (stdlib, pyright strict) |
| `comparer.py` | run vs référence gelée : totaux, articles, lignes, critères (prix ±3 %, heures ±5 %, articles ±10 %), attribution de l'écart par décision |
| `extraire_reference.py` | référence gelée (`dossiers/<S>/soumission/chiffrage_dupuis.py`) → `quantites.json`, `decisions.json`, `parametres.json` du kit |
| `convertir_run.py` | run v1 (`chiffrage.json`) → `quantites.json` à prix fixes + contrôle que le moteur redonne ses totaux |
| `preparer_run.py` | dossier de run isolé hors dépôt : kit + moteur + `PROMPT.md` (préfixe commun cachable) + `run.json` |
| `prompt-run.md` | gabarit du prompt de lancement |
| `synthese_runs.py` | `runs/*/rapport.json` → `SYNTHESE-auto.md` (table des runs, écart par décision) |
| `calibrer_facteur.py` | `prix/dupuis/couples-sommaire-prix-remis.csv` → `prix/dupuis/calibration-facteur.md` (facteur, position vs plus bas) |
| `<S>/kit/` | entrées d'un run : relevé, Détail, bordereau, catalogue, `METHODE.md`, `CONSIGNES.md`, `parametres.json` |
| `<S>/runs/<run>/` | sorties d'un run + `rapport.json` / `rapport.md` du comparateur |

## Lancer un run (v2)

```bash
python3 entrainement/preparer_run.py S-1902 sonnet-6 --dest /chemin/hors/depot --modele sonnet --effort high
# → lancer l'agent sur /chemin/hors/depot/sonnet-6 avec PROMPT.md ; il écrit quantites.json, decisions.json, NOTES.md
python3 entrainement/chiffrage_commun.py /chemin/hors/depot/sonnet-6 --kit entrainement/S-1902/kit   # chiffrage.json
cp -r /chemin/hors/depot/sonnet-6 entrainement/S-1902/runs/sonnet-6
python3 entrainement/comparer.py S-1902 entrainement/S-1902/runs/sonnet-6                            # rapport.json, rapport.md
python3 entrainement/synthese_runs.py S-1902                                                           # SYNTHESE-auto.md
```

Modèle par défaut : Sonnet 5.5, effort `high` (sur le banc v1, Opus et Sonnet sont indiscernables : 3 contre 5 runs,
différence minimale détectable ≈ 5,7 points). Opus sert à arbitrer une règle manquante, pas à rechiffrer. Les essaims
n'ont plus de rôle dans le chiffrage ; s'il faut plusieurs agents, c'est pour couvrir les feuilles du relevé.

## Vérifier

```bash
python -m pytest tests/test_chiffrage_commun.py -q      # test doré : le moteur redonne la référence gelée (194 000 $) et les 10 runs v1
pyright entrainement/*.py                               # strict (en-tête « # pyright: strict » de chaque module)
ruff check --select E,F,W,B,UP --ignore UP009,E501 entrainement/*.py
```

## Contrat des fichiers

`quantites.json` : `{"dossier", "lignes": [{"code", "desc", "q", "u", "art", "src", "prix", "decision"?, "variantes"?, "lot"?}]}`.
`prix` = `{"type": "fixe", "p", "h"}` ou `{"type": "catalogue", "entrees": [{"desc", "mult"}], "supplement_p"?, "supplement_h"?}`
(colonnes « PRIX À UTILISER » / « TEMPS À UTILISER » du catalogue = dernière valeur de Dupuis). `decision` =
`{"cle", "actif_si": [...]}` : la ligne ne compte que si `decisions[cle]` est dans `actif_si`. `variantes` =
`{"cle", "options": {valeur: {"prix"?, "q"?}}}` : surcharge selon la décision. Les codes sont ceux de la référence
(`dossiers/<S>/soumission/quantites.json`) : un code inconnu ne se rapproche de rien.

`decisions.json` : une valeur par décision de portée (`METHODE.md` §8) + `justifications`. Valeurs connues dans
`chiffrage_commun.DECISIONS_CONNUES`.

`parametres.json` (kit) : `taux`, `facteur`, `arrondi_heures`, `arrondi_prix`, `seuils` (`total_pct`, `heures_pct`,
`article_pct`, `article_min_abs`, `historique_pct`).

## Effet des décisions de portée sur la référence gelée (hors kit)

Mesuré par contrefactuel avec le moteur (`tests/test_chiffrage_commun.py`) : `postes_composites = couverts` −17 506,89 $ ACCEO
(−22 000 $ de prix ; les runs v1 perdent ≈ 9 600 $ seulement, parce qu'ils gardent les prises du relevé) ; `monuments = dupuis`
−2 422,44 $ ; `lot_eclairage = readme_11893` −1 141,80 $ ; `eae_hors_plan = sautes` −5 100 $ (64,9 h, arrondi 1 050 → 990 h).
Ces montants restent hors du kit pour que les runs restent aveugles.

## Ce que le banc ne règle pas (décisions humaines)

- La référence 194 000 $ est une reconstitution du 20 octobre, pas le prix remis par Daniel Dupuis ; tant qu'un prix réel
  (prix remis, ouverture SEAO) n'est pas gelé à sa place, le banc mesure la conformité à cette reconstitution.
- Le facteur 1,244 repose sur un seul couple (S-1844) : `calibrer_facteur.py` le dit tant que le CSV n'a pas 5 couples.
- Les cinq décisions de portée sont celles de la référence gelée, à confirmer par Jo (`METHODE.md` §8).
- Les lots fournisseur (27 343 $) restent des montants confirmés oralement, sans soumission fournisseur.
