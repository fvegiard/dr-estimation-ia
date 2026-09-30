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
`prepare.py` → agent `releveur` → `build_qpl.py` → `render_vectoriel.py` → `render_pdf.py` → `STATUT.md`) :
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
- `releveur` (Opus) : relève un dossier préparé en appliquant la compétence `releve-planexpert`.
- `verificateur` (Opus) : compare un relevé IA au relevé humain, prouve chaque écart sur le plan, et juge les rendus à l'œil.
- `inventaire` (Haiku) : listages, tailles, dates, métadonnées — lecture seule.
Lancer le relevé par sous-agent, pas par `claude -p` en arrière-plan (meurt après ~10 min dans le bac à sable cloud).

## Ajouter un dossier
1. Plans + addendas seulement dans `INBOX/<S>/` (le relevé humain va dans `dossiers/<S>/reference/`, jamais dans l'INBOX).
2. `prepare.py` → agent `releveur` → `run.py --reprendre` → `outils/assembler_dossier.py`.
3. Si l'estimateur fournit son projet Plan Expert : `reference/<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt` +
   `feuilles-ia.csv` → le dossier entre automatiquement dans le jeu de référence.
