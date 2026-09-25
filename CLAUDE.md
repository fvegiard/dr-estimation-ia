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

## Carte du dépôt
- `releve/` — la chaîne qui marche : `prepare.py` (rasters, tuiles, mots) → agent (compétence `releve-planexpert`) →
  `extract_occurrences.py` → `build_qpl.py` → `render_pdf.py` ; `run.py` orchestre, `run.py --reprendre <S>` refait qpl + PDF.
- `src/validation/compare_qpl.py` — comparaison marque par marque humain/IA ; `jeu_reference.py` — la rejoue sur tous les dossiers.
- `dossiers/<S>/` — un dossier de soumission : `releve.xlsx`, `ecart.md`, `planexpert/<S>.qpl`, `export-natif/` (sorties du vrai
  Plan Expert), `reference/` (projet de l'estimateur + dimensions + feuilles), `comparaison-dupuis-qpl/`.
- `dossiers/_jeu-reference/` — résultats et ligne de base du jeu de référence.
- `src/` (autres modules), `tests/` (pytest, fixtures synthétiques), `docs/`, `infra/` (VM Plan Expert sur mxlinux).

## Commandes
```bash
pip install -r requirements.txt
python -m pytest tests -q                       # tests unitaires
python -m src.validation.jeu_reference          # jeu de référence (code 1 si régression)
uv run releve/prepare.py INBOX/<S> OUTBOX/<S>/travail
uv run releve/run.py --reprendre <S>            # après l'agent : qpl + PDF
```

## Agents (`.claude/agents/`)
- `releveur` (Opus) : relève un dossier préparé en appliquant la compétence `releve-planexpert`.
- `verificateur` (Opus) : compare un relevé IA au relevé humain, prouve chaque écart sur le plan.
- `inventaire` (Haiku) : listages, tailles, dates, métadonnées — lecture seule.
Lancer le relevé par sous-agent, pas par `claude -p` en arrière-plan (meurt après ~10 min dans le bac à sable cloud).

## Ajouter un dossier
1. Plans + addendas seulement dans `INBOX/<S>/` (le relevé humain va dans `dossiers/<S>/reference/`, jamais dans l'INBOX).
2. `prepare.py` → agent `releveur` → `run.py --reprendre` → `outils/assembler_dossier.py`.
3. Si l'estimateur fournit son projet Plan Expert : `reference/<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt` +
   `feuilles-ia.csv` → le dossier entre automatiquement dans le jeu de référence.
