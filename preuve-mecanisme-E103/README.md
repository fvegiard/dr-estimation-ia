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
   le bordereau de cette feuille, au format matériel (une ligne par repère, voir `docs/FORMAT-EXEMPLE.md` §4.1),
   est généré.

## Routage réel utilisé pour cette preuve (pas celui de `run.py --watch`)

Scripts lancés directement en Python (pas `uv run` : l'environnement de cette session a déjà tous les
paquets requis installés globalement — voir le rapport de routage dans la conversation pour le détail des
vérifications de disponibilité). **Aucun agent Claude imbriqué n'a été invoqué** (`releve/agent_sdk.py`,
`agent_nvidia.py`, `claude -p` sont tous indisponibles dans ce bac à sable — vérifié : `claude_agent_sdk`
non installé, `CLAUDE_CODE_OAUTH_TOKEN`/`NVIDIA_API_KEY` absents, binaire `claude` introuvable) : l'étape
« agent » de `run.py` n'a PAS tourné. Elle a été remplacée par mon identification directe (§2 ci-dessus),
conformément à la demande explicite de Francis de travailler sans délégation — c'est la route documentée
pour toute session OpenHands cloud sans ces accès (voir `CLAUDE.md` §Agents, « Session cloud OpenHands »).

**Modèle demandé vs modèle réellement exécuté** : `releve/run.py` demande `RELEVE_MODEL` (défaut `"opus"`
dans le code) pour SA route automatisée — non pertinent ici puisque cette route n'a pas tourné. Le modèle
qui a réellement produit ce dossier est celui de la session elle-même, tel qu'observé dans son propre
contexte système au moment de l'exécution (pas déduit d'un défaut de code) : Claude Sonnet 5
(`claude-sonnet-5`), session OpenHands Cloud, 2026-09-30.

## Régénéré le 2026-09-30 après les corrections issues de la revue de PR #9

Les livrables ont été reproduits avec les mêmes données sources (`nomenclature.csv`, `occurrences-visuel.csv`,
`feuilles-classement.csv`, `reserves.md` — inchangés) mais le moteur corrigé, pour rester une preuve à jour :
- `PREUVE01-Dossier-complet.pdf` garde maintenant ses 7 calques OCG (0 avant le correctif — voir §Contrôles
  de conformité de `CLAUDE.md`).
- `PREUVE01-rendu-rapport.json` porte désormais un champ `reperes` au niveau racine (6), lu par le serveur
  MCP sans refaire le rendu une seconde fois.
Sans effet visible sur cet échantillon (une seule feuille, format `materiel`, 0 chevauchement d'encadré) :
le correctif des feuilles à zéro repère (rien à ajouter ici, la feuille en a 6), le correctif du bordereau
`agrege`/portée (cette feuille est en format `materiel`, non concerné) et le statut « À VÉRIFIER » (aucun
chevauchement sur cette feuille).

## Cible visuelle de comparaison

`apprentissage/hr26-14-exemplaire/cible-visuelle/HR26-14-E08-E09-approuve.pdf` (E08/E09, approuvé par
Francis) — comparaison de style uniquement (pastille pastel, encadré, calques), pas de comparaison de
contenu (projets différents).
