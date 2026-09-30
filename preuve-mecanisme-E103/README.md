# Preuve de mécanisme — PREUVE01/E103 (2026-09-30)

Ce dossier n'est **pas un relevé de production**. C'est la preuve, exécutée directement (sans sous-agent,
sans passer par un dossier déjà relevé), que la chaîne déterministe produit bien le format cible approuvé
par Francis (`apprentissage/hr26-14-exemplaire/SOURCE.txt`, E08/E09) à partir d'un PDF source non annoté.

## Source

- `dossiers/S-1844-essai/E103/E103-page6.pdf` — page d'ingénierie brute (nLight, SAQ Varennes), **sans
  aucune marque de relevé** au départ. sha256 `26609226bb2ba3a5d99b7ec28e299052e2af31e177386c09a39652a457f40438`.
- ⚠️ Limite d'honnêteté : ce fichier avait déjà été utilisé plus tôt dans la même conversation pour un autre
  test (preuve de branchement du moteur, avec le vrai relevé `dossiers/S-1844-essai/E103/nomenclature.csv`
  déjà consulté). Ce n'est donc **pas un test à l'aveugle** de justesse d'identification — c'est une preuve
  de mécanisme : les 6 repères ci-dessous ont été relus et vérifiés au zoom sur cette page dans ce run-ci,
  sans recopier les fichiers déjà vus, mais je ne peux pas garantir une absence totale d'influence mémorielle
  sur le choix des 6 symboles. Pour un vrai test à l'aveugle, utiliser un PDF jamais vu dans la conversation.

## Ce qui a été fait, moi-même, sans délégation

1. `python3 releve/prepare.py` (réel, pas simulé) → `rasters/`, `tuiles/`, `texte/E103-mots.csv` frais.
2. Identification de 6 repères par lecture directe des mots vectoriels (`texte/E103-mots.csv`) + vérification
   visuelle au zoom 10× sur chaque coordonnée avant de l'écrire (`nomenclature.csv`, `occurrences-visuel.csv`
   écrits à la main, voir ces fichiers dans ce dossier). Portée posée `A PRECISER` partout (non confirmée) —
   voir `reserves.md`.
3. `python3 releve/build_qpl.py` → `PREUVE01-planexpert/PREUVE01.qpl`.
4. `python3 releve/render_vectoriel.py` → `PREUVE01-Plans-annotes.pdf` (+ `PREUVE01-rendu-rapport.json`,
   contrôle de conformité : `encadre_hors_espace_libre: []`).
5. `python3 releve/render_pdf.py` → `PREUVE01-Rapport-de-metre.pdf/.md`, `PREUVE01-Dossier-complet.pdf`.
6. Ouvert et vérifié moi-même (`apercu-plan-page1.png`, `apercu-zoom-6-reperes.png`) : les 6 pastilles
   (M01-01 à M06-01) sont sur les 6 bons symboles carrés, l'encadré « RELEVE E103 - MATERIEL » est lisible,
   le bordereau 8 colonnes est généré.

## Routage réel utilisé pour cette preuve (pas celui de `run.py --watch`)

Scripts lancés directement en Python (pas `uv run` : l'environnement de cette session a déjà tous les
paquets requis installés globalement — voir le rapport de routage dans la conversation pour le détail des
vérifications de disponibilité). **Aucun agent Claude n'a été invoqué** (`releve/agent_sdk.py`,
`agent_nvidia.py`, `claude -p` sont tous indisponibles dans ce bac à sable — voir audit de routage) :
l'étape « agent » a été remplacée par mon identification directe (§2 ci-dessus), conformément à la demande
explicite de Francis de travailler sans délégation pour cette preuve.

## Cible visuelle de comparaison

`apprentissage/hr26-14-exemplaire/cible-visuelle/HR26-14-E08-E09-approuve.pdf` (E08/E09, approuvé par
Francis) — comparaison de style uniquement (pastille pastel, encadré, calques), pas de comparaison de
contenu (projets différents).
