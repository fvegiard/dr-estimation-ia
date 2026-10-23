# CLAUDE.md — DR Estimation IA

Relevé de quantités électrique automatique (Groupe DR Électrique) : plans PDF → marques par appareil → projet Plan Expert
(`.qpl`) → comparaison au relevé de l'estimateur. Lu par Claude Code, Cowork et l'action GitHub à chaque session.
Poste estimateur (MCP `expert-estimateur`) : `.claude/rules/estimateur.md`.

## Règles du projet
- Tout est public dans ce dépôt : plans, prix, relevés humains, projets Plan Expert (décision de Francis, 22/09/2026).
  Jamais de clé, de jeton ni d'installateur/licence.
- Français partout (code commenté, rapports, commits).
- Rien n'est inventé : chaque quantité vient d'un fichier lu (étiquette, symbole vu, cédule, note) ; l'incertain va en réserve.
- Un rapport d'agent n'est pas une preuve : vérifier le fichier produit (compte, zoom, capture) avant de dire « fait ».
- Toute modification de `releve/` ou de `.claude/skills/releve-planexpert/` doit passer le jeu de référence sans régression
  (`python -m src.validation.jeu_reference`) — c'est le test qui dit si l'agent s'améliore.

## Format du PDF de relevé : une seule spec
- La seule description du format (pastilles, palettes, étiquettes, encadré, bordereaux) est `docs/FORMAT-EXEMPLE.md`,
  mesurée sur le gold EXEMPLE.pdf (HR26-14, sha256 0861bc3a…). Quand une doc et le gold divergent, le gold gagne
  (décision de Francis, 2026-10-05) : on corrige la spec, jamais le gold.
- Ailleurs (CLAUDE.md, compétences, agents, docstrings, README), renvoyer à cette spec au lieu de recopier des chiffres.
  `tests/test_spec_format_unique.py` échoue si une affirmation concurrente réapparaît dans un `.md`.

## Autonomie et auto-supervision (obligatoire — Francis ne coache pas)
Francis n'est pas superviseur : il fait seulement des contrôles au hasard. Tu fais toi-même la supervision visuelle.
1. Après chaque rendu, OUVRE les planches de contrôle `OUTBOX/<S>/controle/*.png` (une vignette ×8 par pastille,
   écrites par `run.py` via `releve/planche_controle.py`) — c'est à cette échelle qu'un décalage de 5 pt ou une
   mauvaise famille se voit, jamais sur la feuille entière (TEST-E201, 2026-10-15 : 8 pastilles décalées et 4
   familles fausses invisibles sur la vue d'ensemble, vues du premier coup en vignettes). Juge : pastille visible
   (forme, rayon et palette selon le format de la feuille, `docs/FORMAT-EXEMPLE.md`) ? sur le BON symbole
   (type = famille) ? 1 symbole = 1 repère ? étiquette lisible ? réserve * si doute ? Jamais sur un texte, un arc
   ou une ligne longue.
2. Compare à la feuille équivalente de l'exemplaire, dans son format (pastilles, encadré, bordereau matériel 8 col. /
   agrégé 6 col. / travaux 8 col. — spec unique : `docs/FORMAT-EXEMPLE.md` ; E08 et E09 sont des feuilles agrégées
   6 colonnes) — sauf pendant l'essai à l'aveugle HR26-14 où tu ne compares qu'à la fin (étape 4). Cible visuelle
   approuvée par Francis : `apprentissage/hr26-14-exemplaire/SOURCE.txt` (E08 = p.62, E09 = p.64 de EXEMPLE.pdf,
   sha256 0861bc3a…) et `apprentissage/hr26-14-exemplaire/STANDARD-RELEVE.md` (format, vocabulaire, règles).
   Chaque dossier produit ce format via `releve/render_vectoriel.py` (pas de rastérisation) — vérifie le fichier
   PDF réellement produit, jamais seulement le journal de l'agent.
3. Écris toi-même le score x/N avec la liste des cases fausses et corrige jusqu'au seuil (≥ 17/18 sur une planche d'essai,
   ≥ 95 % ensuite) sans attendre de message. Une régression (case bonne avant, fausse après) bloque le passage.
4. Vérification visuelle directe, par toi-même (règle de délégation : §Agents).
5. Rapport : l'image + ton score. Jamais « fait » sans ces deux éléments.
6. Enchaîne les étapes sans rendre la main. Fin = livrable prouvé OU blocage que seul Francis peut lever.
   À chaque étape prouvée : commit + push + ligne « ÉTAPE n — FAIT ». Plus de 30 min sans commit → commit `wip` avec
   l'état et les preuves. Si un tour dépasse 20 min sans sortie, découpe le travail (moins d'images par tour).

## Carte du dépôt
- `releve/` — la chaîne qui marche : `prepare.py` (rasters, tuiles, mots) → agent (compétence `releve-planexpert`) →
  `extract_occurrences.py` → [feuilles raster seulement : `ancrage_raster.py` (pastille recalée sur le cercle/rectangle
  du symbole, rayon et angle mesurés) → `comparer_legende.py` (famille contrôlée par corrélation au glyphe de légende)] →
  `build_qpl.py` → `render_vectoriel.py` (PDF « Plans annotés » vectoriel — pastilles OCG par-dessus le plan
  d'origine, encadré RELEVE-MATERIEL, bordereau au format de la feuille, 3 formats ; `src/estimer/render/`) →
  `render_pdf.py` (rapport de métré + dossier complet) → `planche_controle.py` (vignettes ×8 de chaque pastille dans
  `controle/`) ; `run.py` orchestre, `run.py --reprendre <S>` refait qpl + PDF + planches. Les contrôles raster
  (symboles non retrouvés, familles suspectes) sont repris dans `STATUT.md`, jamais réduits au silence.
- `src/validation/compare_qpl.py` — comparaison marque par marque humain/IA ; `jeu_reference.py` — la rejoue sur tous les dossiers.
- `src/validation/boucle_acceptation.py` — orchestrateur du critère d'acceptation (étapes 1 à 8 : aveugle → gel →
  comparaison → classement → justifications → ACCEPTATION.md), avec ses modules : `aveugle.py` (scan du workdir du
  relevé IA, aucune référence estimateur), `gel.py` (gel sha256 des artefacts, revérifié à chaque relance),
  `classer_ecarts.py` (chaque désaccord classé, jamais un compte global seul), `justifier.py` (dossier de
  justifications à trancher sur le plan) — détails, verdicts et artefacts : `docs/boucle-acceptation.md`.
- `dossiers/<S>/` — un dossier de soumission : `releve.xlsx`, `ecart.md`, `planexpert/<S>.qpl`, `export-natif/` (sorties du vrai
  Plan Expert), `reference/` (projet de l'estimateur + dimensions + feuilles), `comparaison-dupuis-qpl/`.
- `dossiers/_jeu-reference/` — résultats et ligne de base du jeu de référence.
- `src/` (autres modules), `tests/` (pytest, fixtures synthétiques), `docs/`, `infra/` (VM Plan Expert sur mxlinux).

## Contrôles de conformité (du plus léger au plus profond)
1. `python -m pytest tests -q` et `python -m src.validation.jeu_reference` — déterministes, tournent partout (y compris en bac
   à sable cloud), gate officiel de non-régression (quantité/position, jamais le rendu visuel).
2. **Boucle d'acceptation** (`python -m src.validation.boucle_acceptation <S> --workdir W --dossier D`) — contrôle
   déterministe qui orchestre les étapes 1-2 du critère d'acceptation (`aveugle`, `gel`) et, quand la référence de
   l'estimateur est en place, enchaîne comparaison, classement et justifications jusqu'au verdict d'`ACCEPTATION.md` —
   tourne partout (y compris en bac à sable cloud), page dédiée : `docs/boucle-acceptation.md`.
3. `releve/render_vectoriel.py` écrit `<SORTIE>/<NOM>-rendu-rapport.json` à chaque rendu (repères/familles/RES par feuille,
   encadré hors espace libre ou non) — à relire avant de livrer, pas seulement le journal texte de l'agent.
4. Auto-supervision visuelle (§Autonomie ci-dessus).
5. `python -m src.estimer.render.verify_exemple RENDU.pdf RENDU.report.json EXEMPLE.pdf GOLD_INPUT_DIR` — comparaison
   octet-près au gold HR26-14 (marqueurs à 0,05 pt, bordereau cellule par cellule). Exige le EXEMPLE.pdf complet
   (87 p., non versionné, sur le Drive/PC de Francis) : **indisponible en bac à sable cloud**, à lancer sur un poste
   qui a le fichier.
6. `infra/pe-batch.ps1` — ouvre le `.qpl` dans le vrai Plan Expert (VM mxlinux, PowerShell + SSH + pilotage VNC) et
   exporte son propre rapport/PDF natifs : la vérification la plus forte (le logiciel du client accepte le fichier),
   mais **Windows + VM uniquement**, aucun équivalent possible en bac à sable cloud.

## Critère d'acceptation (obligatoire — jamais en dessous de l'estimateur)
Le relevé IA peut améliorer sur l'estimateur, mais **ne doit jamais être accepté s'il est pire** que son
relevé de référence (`.qpl`, `releve.xlsx` ou équivalent). C'est une porte mesurée, avec une procédure fixe, jamais
une affirmation de supériorité garantie.
1. **Identification d'abord, à l'aveugle.** Relève depuis les plans et addendas originaux SEULEMENT,
   avant d'ouvrir le `.qpl`/relevé de l'estimateur. Ne jamais lire la réponse de l'estimateur pendant
   l'identification — ça invalide la mesure (comme l'essai HR26-14, §Autonomie point 2).
2. **Geler ce premier résultat** (commit) avant toute comparaison.
3. **Comparer ensuite** au `.qpl`/relevé de l'estimateur (`src/validation/compare_qpl.py`).
4. **Classer chaque désaccord** : omission, doublon, mauvaise famille, mauvaise portée (scope), mauvais
   rattachement de feuille. Un simple compte global (rappel/précision) ne suffit pas comme preuve d'acceptation.
5. **Justifier chaque désaccord sur la source originale** (le plan, pas l'un ou l'autre relevé) : retourner
   au plan/à la cédule/à l'addenda pour trancher, y compris quand c'est l'ESTIMATEUR qui s'est trompé —
   une erreur constatée chez l'estimateur ne s'accepte pas sans preuve sur le plan non plus.
6. **Corriger et revérifier** avant d'accepter — pas seulement noter l'écart et livrer quand même.
7. **Une quantité plus élevée seule n'est jamais une amélioration.** Seule la justification plan-par-plan (étape 5) compte.
8. **Si le gold/la référence ou une portée nécessaire est indisponible**, le rapport dit « vérification
   incomplète » — ne jamais certifier « pas pire que l'estimateur » sans avoir pu vérifier.
9. Le format visuel approuvé (§Autonomie point 2, E08/E09) reste inchangé par ce critère : l'acceptation
   porte sur les quantités/positions, jamais sur une dégradation du rendu pour gagner du temps.

Les étapes 1 à 4 sont prouvées par des artefacts sur disque, jamais par le récit d'un agent (`controle-aveugle.json`,
`gel.json`, `comparaison-dupuis-qpl/ecarts-classes.csv`), le dossier de justifications couvrant les étapes 5 à 7 et
`ACCEPTATION.md` portant le verdict — tous écrits par la boucle d'acceptation (`docs/boucle-acceptation.md`, testé bout
en bout par `tests/test_boucle_acceptation_e2e.py`).

Sources cloud pour l'identification (procédure, rôle exact des dossiers et limites : `docs/sources-cloud-plans-originaux.md`) :
- Google Drive « plan expert qpl » (lien public, lecture anonyme) → sous-dossier `original` = dossiers de
  soumission, à rôle mixte ; `EXEMPLE SORTIE LLM AI` et `SORTIE LLM AI - S-*` = sorties déjà produites, jamais une
  entrée de relevé.
- SharePoint « Mes projets » (Daniel Dupuis, lien public, module `src/apprentissage/sharepoint.py::MesProjets`
  avec `racine="/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets"` —
  **pas** la racine par défaut du module, périmée). **C'est d'abord l'emplacement de la référence de
  l'estimateur** (`.qpl` et PNG marqués de Daniel Dupuis) — jamais un corpus de plans bruts.
Chaque fichier, dans l'une ou l'autre source, se vérifie individuellement avant d'être relevé : exclure
systématiquement un sous-dossier `Prix`/devis ou la réponse de l'estimateur (`.qpl`, PNG marqués). Un plan
ou un addenda réellement joint à un courriel reste une source légitime une fois son contenu extrait et son
rôle vérifié — la vérification porte sur le fichier, pas sur son type de contenant.

## Commandes
Action unique pour un nouveau dossier (parcours canonique — tout le reste orchestré par `run.py` :
`prepare.py` → son propre agent (§Agents, processus séparé) → `build_qpl.py` → `render_vectoriel.py` →
`render_pdf.py` → `STATUT.md`) :
```bash
uv run releve/run.py <NOM>                       # dépose d'abord les PDF dans INBOX/<NOM>/ — c'est tout
```
Route par défaut depuis 2026-10-18 (`RELEVE_AGENT=blocs`) : **déterministe, zéro agent, zéro jeton, zéro étiquetage** —
`blocs_vectoriels.py` (symboles = blocs CAO) → `blocs_vignettes.py` → `blocs_familles_auto.py` (familles depuis
`releve/bibliotheque-blocs.csv`, construite sur S-1902 : même bureau d'ingénieurs = mêmes blocs ; les signatures
inconnues vont dans `travail/blocs-a-etiqueter.md`, à étiqueter UNE fois puis à ajouter à la bibliothèque) →
`blocs_vers_releve.py` → qpl → PDF → planches → PNG. `RELEVE_AGENT=sdk` rend l'ancienne route par agent.
Preuve : S-1902 rejoué à l'aveugle par cette seule commande = 653 repères (645 validés + 8 pictogrammes existants
sur E201/E202), 0 inconnue.
Reste (débogage, développement) :
```bash
uv run --with-requirements requirements.txt python -m pytest tests -q   # tests unitaires (pas de pip global)
python -m src.validation.jeu_reference          # jeu de référence (code 1 si régression)
uv run releve/prepare.py INBOX/<S> OUTBOX/<S>/travail
uv run releve/run.py --reprendre <S>            # rejoue seulement qpl + render_vectoriel + render_pdf (sans agent)
```

## Agents (`.claude/agents/`)
**Règle de délégation (une seule) : une session interactive travaille elle-même** — lit les tuiles, écrit les CSV,
exécute les scripts, fait sa vérification visuelle — sans sous-agent. Ni la taille du dossier, ni la durée, ni
l'importance de la vérification ne justifient seules une délégation : une tâche longue se découpe en plusieurs tours
(§Autonomie point 6). Un sous-agent ne se lance QUE si Francis l'autorise explicitement, pour ce dossier précis, et
toujours par l'outil Agent d'une session interactive, jamais par `claude -p` détaché (meurt après ~10 min dans le bac
à sable cloud). Sans autorisation, l'absence du score d'un sous-agent ne bloque jamais un rapport.
Cette règle « sans sous-agent » du dépôt prime sur toute doctrine générique de délégation (orchestrateur, config utilisateur) pour les relevés d'estimation.

Sous-agents disponibles (sessions interactives Claude Code, OpenHands) :
- `releveur` (Opus) : relève un dossier déjà préparé par `prepare.py`, en appliquant la compétence `releve-planexpert`.
- `verificateur` (Opus) : compare un relevé IA au relevé humain, prouve chaque écart sur le plan, juge les rendus à l'œil.
- `inventaire` (Haiku) : listages, tailles, dates, métadonnées — lecture seule.

Le parcours canonique (`uv run releve/run.py <NOM>`) ne passe PAS par ces sous-agents : `run.py` lance lui-même un
agent séparé pour la lecture du plan (`releve/agent_sdk.py`, voir `RELEVE_AGENT`/`RELEVE_MODEL` dans `releve/run.py`),
processus indépendant de toute session interactive.

**Deux routes existent pour l'étape « agent », selon l'environnement — vérifier laquelle est active, ne jamais
supposer** (`python3 -c "import claude_agent_sdk"`, `which claude`, présence de `CLAUDE_CODE_OAUTH_TOKEN`/`NVIDIA_API_KEY`) :
- **Poste authentifié** (`claude auth login` fait ou `CLAUDE_CODE_OAUTH_TOKEN` exporté, réseau pour que `uv run`
  installe `claude-agent-sdk`) : `uv run releve/run.py <NOM>` fonctionne de bout en bout, agent inclus. Le modèle
  est celui **demandé** par `RELEVE_MODEL` (défaut `"opus"`) — une valeur demandée, pas une preuve ; ne l'affirmer
  qu'après lecture du `session_id`/`usage` de `agent-resultat.json`.
- **Session cloud OpenHands sans ces accès** (absents le 2026-09-30, à revérifier) : aucun agent imbriqué ;
  `uv run releve/run.py <NOM>` seul échouera à l'étape agent. La session interactive tient lieu d'agent, avec les
  **mêmes scripts déterministes** :
  1. `python3 releve/prepare.py INBOX/<NOM> OUTBOX/<NOM>/travail`.
  2. La session écrit et vérifie au zoom (jamais recopié d'une réponse déjà vue) `nomenclature.csv`,
     `occurrences-texte.csv`/`occurrences-visuel.csv`, `feuilles-classement.csv`, `reserves.md`, selon le SKILL.md de
     la compétence `releve-planexpert`.
  3. `python3 releve/build_qpl.py`, puis `python3 releve/render_vectoriel.py`, puis `python3 releve/render_pdf.py`.
  Preuve et portée exacte : `preuve-mecanisme-E103/README.md`. Consigner dans tout rapport le modèle observé dans le
  contexte système de la session (jamais déduit d'un défaut de code).

## Ajouter un dossier
1. Plans + addendas seulement dans `INBOX/<S>/` (le relevé humain va dans `dossiers/<S>/reference/`, jamais dans l'INBOX).
2. `uv run releve/run.py <S>` (§Commandes) — résultat dans `OUTBOX/<S>/`, hors du dépôt.
3. `outils/assembler_dossier.py <S> OUTBOX/<S> <dossier reference>` — copie les livrables dans `dossiers/<S>/` (le dépôt).
4. Si l'estimateur fournit son projet Plan Expert : `reference/<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt` +
   `feuilles-ia.csv` → le dossier entre automatiquement dans le jeu de référence.

Débogage (seulement si `run.py` échoue ou qu'une inspection entre étapes est nécessaire) : `prepare.py` → relevé par
la session (§Agents) → `run.py --reprendre <S>` → étape 3.

## Soumission et chiffrage (référence officielle, 2026-10-20)
- `outils/soumission/` — chiffrage « méthode Dupuis » + gabarit de soumission DR (ReportLab) + classeur imprimable ; processus complet dans `outils/soumission/README.md`.
- `dossiers/<S>/soumission/` — dossier gelé par soumission (S-1902 = première application, 194 000 $).
- `prix/dupuis/` — catalogue prix/temps de M. Dupuis (27 relevés ACCEO 2026) : sa dernière valeur fait foi.
- Règle : aperçu PNG regardé avant tout PDF ; commit direct sur `main`, pas de PR, pour ces dossiers.
