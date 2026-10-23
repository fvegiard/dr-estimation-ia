# Entraînement S-1902 à l'aveugle — synthèse (2026-10-21)

Référence gelée (`dossiers/S-1902/soumission/`) : matériel 66 649,07 $ ; 1 045,85 h → 1 050 h ; ACCEO 155 899,07 $ ; **194 000 $**.
Kit identique pour tous les runs (`kit/`, sans la réponse) ; aucune fuite détectée (sources citées = kit seulement).

## Résultats

| Run | Modèle | Prix de vente | Δ prix | Δ matériel | Δ heures | Lignes |
|---|---|---|---|---|---|---|
| opus-1 | Opus 5.5 | 168 000 $ | −13,4 % | −14,6 % | −12,3 % | 79 |
| opus-2 | Opus 5.5 | 168 000 $ | −13,4 % | −16,5 % | −11,6 % | 73 |
| opus-3 | Opus 5.5 | 180 000 $ | −7,2 % | −9,5 % | −5,6 % | 79 |
| sonnet-1 | Sonnet 5.5 | 170 000 $ | −12,4 % | −13,0 % | −11,3 % | 83 |
| sonnet-2 | Sonnet 5.5 | 175 000 $ | −9,8 % | −10,6 % | −9,3 % | 89 |
| sonnet-3 | Sonnet 5.5 | 169 000 $ | −12,9 % | −13,8 % | −13,0 % | 83 |
| sonnet-4 | Sonnet 5.5 | 176 000 $ | −9,3 % | −12,3 % | −6,5 % | 85 |
| sonnet-5 | Sonnet 5.5 | 180 000 $ | -7.2 % | -10.3 % | -4.7 % | 89 |
| essaim-1 | Opus 5.5 seul (5 lots en séquence) | 170 000 $ | −12,4 % | −13,0 % | −11,3 % | 73 |
| essaim-2 | Fable 5.1 → 2 Opus → 6 Sonnet → 18 Haiku (relais par fichiers) | 175 000 $ | −9,8 % | −12,2 % | −7,6 % | 82 |

Aucun run dans la tolérance (±1 %), essaims compris : 27 agents en pyramide (essaim 2) donnent exactement le résultat de sonnet-2 seul
(175 000 $), pour ≈ 25× le coût et 1 h 41 au lieu de 9 min. Tous sortent **sous** la référence, de −7 % à −13 %. Opus et Sonnet font les mêmes choix ; l'écart
n'est pas aléatoire, il est **systématique** : ce sont des règles de portée qui manquent à `METHODE.md`, pas des erreurs de calcul.

## D'où vient l'écart (par article du bordereau, moyenne des 8 runs)

| Article | Δ moyen | Stable ? | Cause (ce que la référence fait / ce que les runs font) |
|---|---|---|---|
| 3.28 | −7 986 $ | oui (min −7 993, max −7 967) | Référence : lignes composites « poste de travail » de la feuille Détail (D-01 ×18 à 156,39 $/3,53 h, E-01, D-03…D-06). Runs : les 7 les ont **écartées** comme double compte avec le relevé, gardant seulement les prises du relevé. |
| 3.27 | −1 653 $ | oui | Même cause : D-02 tables avec boîte d'électrification (5 × 439,42 $ / 6,85 h) écartées. |
| 3.34 | −2 758 $ | oui | Monuments poke-through : référence au prix **Lumen** 1 461,22 $ (E-02 ×2) ; runs au prix Dupuis « MONUMENT PLANCHER » 250 $. |
| 3.22 | −2 947 $ | non (−6 227 à +359) | Démantèlement/relocalisation : certains runs sautent A-01…A-06 (E.A.E) en pensant que le relevé les couvre. |
| 3.33 / 3.31 | −3 574 / −2 044 $ | non | Conduits : pas de colonne TEMPSEC au catalogue → temps/pi seulement ; familles 03C12 vs 05C12 ; longueurs hypothétiques du Détail. |
| 3.24 / 3.25 | −3 656 / +2 846 $ | oui | **Allocation seulement** : lot distribution 6 200 $ entier en 3.24 (référence) vs ventilé 3 400 / 2 800 (runs). Net ≈ 0. |
| 6.1 | +6 219 $ | oui | **Allocation seulement** : nacelle / frais de chantier mis en 6.1 par les runs, répartis ailleurs par la référence. |

Hors allocation, l'écart réel tient à **trois décisions d'estimateur** : (1) garder ou non les postes de travail composites du Détail en
plus du relevé ; (2) monuments au prix fournisseur ou au prix Dupuis ; (3) portée du démantèlement et temps des conduits.

## Incohérence trouvée dans la référence (signalée par 8 runs sur 8)

`outils/soumission/README.md` §2 : le lot éclairage est donné à **11 893 $**, mais son détail (A1 ×11 à 185 + SL1 4′ ×12 à 290 + 3′ ×15 à 230
+ 1′ ×6 à 110 + trousses 1 500 + E ×3 à 475 + Z6 ×3 à 161,60) totalise **13 034,80 $**. Écart 1 141,80 $. À trancher par Francis.

## Décisions à prendre (Francis) — chaque réponse devient une règle écrite dans METHODE.md / README

1. Postes de travail composites (D-01, D-02, E-01…) : à compter **en plus** du relevé (comme la référence) ou le relevé les couvre ?
2. Monuments poke-through : prix Lumen (1 461,22 $) ou prix Dupuis (250 $) ?
3. Lot éclairage : 11 893 $ ou 13 034,80 $ ?
4. Démantèlement E.A.E : toujours hors plan, à compter depuis le Détail (règle à écrire noir sur blanc).
5. Conduits : confirmer la formule sans TEMPSEC et la famille (03C12 vs 05C12) par usage.

Une fois ces 5 règles écrites, relancer le même banc : l'objectif est 8/8 dans ±1 %.

## Mise à jour 2026-10-23 — protocole v2

Les constats ci-dessus sont confirmés par la relecture automatisée des 10 runs : tous ont écarté les postes composites, pris les
monuments au prix Dupuis, gardé le lot éclairage à 11 893 $ et compté le démantèlement aux quantités du relevé. La table des écarts
par décision est maintenant générée (`SYNTHESE-auto.md`, `entrainement/synthese_runs.py`) : postes composites −9 641 $ (stable sur
10 runs), monuments −2 758 $ (stable), conduits et démantèlement instables, et en moyenne +5 634 $ d'écart non attribué sur les
autres articles. Les cinq décisions sont écrites dans `kit/METHODE.md` §8, le prix sort d'un moteur commun
(`entrainement/chiffrage_commun.py`, test doré : il redonne les 194 000 $ gelés) et le verdict porte sur le prix, les heures et
chaque article (`entrainement/comparer.py`). Voir `entrainement/README.md`.
