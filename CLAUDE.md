# CLAUDE.md — DR Estimation IA

Relevé de quantités électrique automatique (Groupe DR Électrique) : plans PDF → marques par appareil → projet Plan Expert
(`.qpl`) → comparaison au relevé de l'estimateur. Lu par Claude Code, Cowork et l'action GitHub à chaque session.

## Règles du projet
- Tout est public dans ce dépôt : plans, prix, relevés humains, projets Plan Expert (décision de Francis, 22/09/2026).
  Jamais de clé, de jeton ni d'installateur/licence.
- Français partout (code commenté, rapports, commits).
- Rien n'est inventé : chaque quantité vient d'un fichier lu (étiquette, symbole vu, cédule, note) ; l'incertain va en réserve.
- Un rapport d'agent n'est pas une preuve : vérifier le fichier produit (compte, zoom, capture) avant de dire « fait ».
- Toute modification de `releve/` ou de `.claude/skills/releve-planexpert/` doit passer le jeu de référence sans régression
  (`python -m src.validation.jeu_reference`) — c'est le test qui dit si l'agent s'améliore.

## Autonomie et auto-supervision (obligatoire — Francis ne coache pas)
Francis n'est pas superviseur : il fait seulement des contrôles au hasard. Tu fais toi-même la supervision visuelle.
1. Après chaque rendu, OUVRE l'image (Read du PNG), zoome repère par repère et juge : pastille visible (cercle pastel
   r≈4,2 pt + contour 0,7 pt couleur famille, dessinée PAR-DESSUS le plan) ? sur le BON symbole (type = famille) ?
   1 symbole = 1 repère ? étiquette lisible ? réserve * si doute ? Jamais sur un texte, un arc ou une ligne longue.
2. Compare à l'exemplaire (même pastille, encadré « RELEVE <feuille> - MATERIEL », bordereau 8 colonnes) — sauf pendant
   l'essai à l'aveugle HR26-14 où tu ne compares qu'à la fin (étape 4). Cible visuelle approuvée par Francis,
   ancrée et vérifiable : `apprentissage/hr26-14-exemplaire/SOURCE.txt` (E08 = p.62, E09 = p.64 de EXEMPLE.pdf,
   sha256 0861bc3a…) et `apprentissage/hr26-14-exemplaire/STANDARD-RELEVE.md` (format, vocabulaire, règles).
   Chaque dossier doit produire ce format via `releve/render_vectoriel.py` (pas de rastérisation) — vérifie le
   fichier PDF réellement produit, jamais seulement le journal de l'agent.
3. Écris toi-même le score x/N avec la liste des cases fausses et corrige jusqu'au seuil (≥ 17/18 sur une planche d'essai,
   ≥ 95 % ensuite) sans attendre de message. Une régression (case bonne avant, fausse après) bloque le passage.
4. Pour les vérifs importantes, lance le sous-agent `verificateur` sur les images seules (sans ton raisonnement).
5. Rapport : l'image + ton score + le score du vérificateur. Jamais « fait » sans ces trois éléments.
6. Enchaîne les étapes sans rendre la main. Fin = livrable prouvé OU blocage que seul Francis peut lever.
   À chaque étape prouvée : commit + push + ligne « ÉTAPE n — FAIT ». Plus de 30 min sans commit → commit `wip` avec
   l'état et les preuves. Si un tour dépasse 20 min sans sortie, découpe le travail (moins d'images par tour).

## Carte du dépôt
- `releve/` — la chaîne qui marche : `prepare.py` (rasters, tuiles, mots) → agent (compétence `releve-planexpert`) →
  `extract_occurrences.py` → `build_qpl.py` → `render_vectoriel.py` (PDF « Plans annotés » vectoriel — pastilles OCG
  par-dessus le plan d'origine, encadré RELEVE-MATERIEL, bordereau 8 colonnes ; `src/estimer/render/`) →
  `render_pdf.py` (rapport de métré + dossier complet) ; `run.py` orchestre, `run.py --reprendre <S>` refait qpl + PDF.
- `src/validation/compare_qpl.py` — comparaison marque par marque humain/IA ; `jeu_reference.py` — la rejoue sur tous les dossiers.
- `dossiers/<S>/` — un dossier de soumission : `releve.xlsx`, `ecart.md`, `planexpert/<S>.qpl`, `export-natif/` (sorties du vrai
  Plan Expert), `reference/` (projet de l'estimateur + dimensions + feuilles), `comparaison-dupuis-qpl/`.
- `dossiers/_jeu-reference/` — résultats et ligne de base du jeu de référence.
- `src/` (autres modules), `tests/` (pytest, fixtures synthétiques), `docs/`, `infra/` (VM Plan Expert sur mxlinux).

## Contrôles de conformité (du plus léger au plus profond)
1. `python -m pytest tests -q` et `python -m src.validation.jeu_reference` — déterministes, tournent partout (y compris en bac
   à sable cloud), gate officiel de non-régression (quantité/position, jamais le rendu visuel).
2. `releve/render_vectoriel.py` écrit `<SORTIE>/<NOM>-rendu-rapport.json` à chaque rendu (repères/familles/RES par feuille,
   encadré hors espace libre ou non) — à relire avant de livrer, pas seulement le journal texte de l'agent.
3. Auto-supervision visuelle (§Autonomie ci-dessus) + sous-agent `verificateur` sur les images seules.
4. `python -m src.estimer.render.verify_exemple RENDU.pdf RENDU.report.json EXEMPLE.pdf GOLD_INPUT_DIR` — comparaison
   octet-près au gold HR26-14 (marqueurs à 0,05 pt, bordereau cellule par cellule). Exige le EXEMPLE.pdf complet
   (87 p., non versionné, sur le Drive/PC de Francis) : **indisponible en bac à sable cloud**, à lancer sur un poste
   qui a le fichier.
5. `infra/pe-batch.ps1` — ouvre le `.qpl` dans le vrai Plan Expert (VM mxlinux, PowerShell + SSH + pilotage VNC) et
   exporte son propre rapport/PDF natifs : la vérification la plus forte (le logiciel du client accepte le fichier),
   mais **Windows + VM uniquement**, aucun équivalent possible en bac à sable cloud.

## Commandes
Action unique pour un nouveau dossier (parcours canonique — tout le reste orchestré par `run.py` lui-même :
`prepare.py` → son propre agent (§Agents, processus séparé — pas un sous-agent de session) → `build_qpl.py`
→ `render_vectoriel.py` → `render_pdf.py` → `STATUT.md`) :
```bash
uv run releve/run.py <NOM>                       # dépose d'abord les PDF dans INBOX/<NOM>/ — c'est tout
```
Reste (débogage, développement) :
```bash
pip install -r requirements.txt
python -m pytest tests -q                       # tests unitaires
python -m src.validation.jeu_reference          # jeu de référence (code 1 si régression)
uv run releve/prepare.py INBOX/<S> OUTBOX/<S>/travail
uv run releve/run.py --reprendre <S>            # rejoue seulement qpl + render_vectoriel + render_pdf (sans agent)
```

## Agents (`.claude/agents/`)
Le parcours canonique (`uv run releve/run.py <NOM>`, §Commandes) ne passe PAS par ces sous-agents : `run.py`
lance lui-même un agent séparé pour la lecture du plan (`releve/agent_sdk.py` par défaut — voir
`RELEVE_AGENT`/`RELEVE_MODEL` dans `releve/run.py`), un processus indépendant de toute session interactive.

**Deux routes existent pour cette étape « agent », selon l'environnement — vérifier laquelle est active
avant d'agir, ne jamais supposer** (`python3 -c "import claude_agent_sdk"`, `which claude`, présence de
`CLAUDE_CODE_OAUTH_TOKEN`/`NVIDIA_API_KEY` dans l'environnement) :
- **Poste authentifié** (ex. le poste de Francis, avec `claude auth login` fait ou `CLAUDE_CODE_OAUTH_TOKEN`
  exporté, et accès réseau pour que `uv run` installe `claude-agent-sdk`) : `uv run releve/run.py <NOM>`
  fonctionne de bout en bout, agent inclus. Le modèle utilisé est celui **demandé** par `RELEVE_MODEL`
  (défaut `"opus"` dans le code) — une valeur demandée, pas une preuve du modèle réellement exécuté ; ne
  l'affirmer qu'après avoir lu le `session_id`/`usage` du résultat réel (`agent-resultat.json`), jamais
  déduite du défaut du code.
- **Session cloud OpenHands sans ces accès** (vérifié absents dans ce bac à sable le 2026-09-30 :
  `claude_agent_sdk` non installé, `CLAUDE_CODE_OAUTH_TOKEN`/`NVIDIA_API_KEY` absents, binaire `claude`
  introuvable — à revérifier, ça peut changer) : aucun agent imbriqué n'est disponible ; ne jamais prétendre
  que `uv run releve/run.py <NOM>` seul suffira ici, l'étape agent échouera. La session interactive tient
  lieu d'agent elle-même, avec les **mêmes scripts déterministes partagés** (aucune nouvelle architecture,
  aucun nouveau serveur) :
  1. `python3 releve/prepare.py INBOX/<NOM> OUTBOX/<NOM>/travail` (réel).
  2. La session écrit et vérifie au zoom (jamais recopié d'une réponse déjà vue) `nomenclature.csv`,
     `occurrences-texte.csv`/`occurrences-visuel.csv`, `feuilles-classement.csv`, `reserves.md`, en
     appliquant elle-même la méthode du fichier SKILL.md de la compétence `releve-planexpert`.
  3. `python3 releve/build_qpl.py`, puis `python3 releve/render_vectoriel.py`, puis
     `python3 releve/render_pdf.py` — les mêmes scripts que la route automatisée, appelés directement.
  Preuve de ce parcours, avec sa portée exacte : `preuve-mecanisme-E103/README.md`. Le modèle réellement
  exécuté est celui observé dans le contexte système de la session elle-même (jamais déduit d'un défaut de
  code) — le consigner dans tout rapport produit par ce parcours.

Ces sous-agents servent une session interactive (Claude Code, OpenHands) qui travaille directement dans ce
dépôt. **Par défaut, une session interactive travaille elle-même** — lit les tuiles, écrit les CSV, exécute
les scripts — sans déléguer. Ne lancer un sous-agent que si Francis le demande explicitement, ou pour la
tâche de lecture visuelle longue elle-même (relever un dossier entier, tuile par tuile), où un contexte
dédié est justifié par la taille de la tâche, pas par défaut :
- `releveur` (Opus) : relève un dossier déjà préparé par `prepare.py`, en appliquant la compétence
  `releve-planexpert` — utilisé quand la session fait elle-même ce travail (hors `run.py`).
- `verificateur` (Opus) : compare un relevé IA au relevé humain, prouve chaque écart sur le plan, et juge
  les rendus à l'œil — à lancer pour toute vérification importante (§Autonomie point 4), quel que soit le
  parcours utilisé pour produire le relevé.
- `inventaire` (Haiku) : listages, tailles, dates, métadonnées — lecture seule.
Toujours passer par l'outil Agent d'une session interactive, jamais par `claude -p` détaché en arrière-plan
(meurt après ~10 min dans le bac à sable cloud).

## Ajouter un dossier
Le parcours canonique (§Commandes) couvre tout sauf le classement final dans le dépôt :
1. Plans + addendas seulement dans `INBOX/<S>/` (le relevé humain va dans `dossiers/<S>/reference/`, jamais dans l'INBOX).
2. `uv run releve/run.py <S>` (§Commandes) — résultat dans `OUTBOX/<S>/`, hors du dépôt.
3. `outils/assembler_dossier.py <S> OUTBOX/<S> <dossier reference>` — copie les livrables dans `dossiers/<S>/` (le dépôt).
4. Si l'estimateur fournit son projet Plan Expert : `reference/<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt` +
   `feuilles-ia.csv` → le dossier entre automatiquement dans le jeu de référence.

Débogage étape par étape (à la place de l'étape 2, seulement si `run.py` échoue ou qu'une inspection entre
étapes est nécessaire) : `prepare.py` → agent `releveur` (§Agents, session interactive seulement) →
`run.py --reprendre <S>` (rejoue qpl + render) → étape 3 ci-dessus.
