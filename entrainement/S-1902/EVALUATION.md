# Évaluation des runs S-1902 — temps, jetons, coût, canaux, prompts, outils, erreurs (2026-10-21)

Mesures prises sur les transcriptions réelles des agents (durée, jetons rapportés par l'outil, appels d'outils) et sur les scripts
produits (`chiffrage.py`, diagnostic statique pyright 1.1.414). Prix : `platform.claude.com/docs/en/about-claude/pricing` lu le 2026-10-21.

## 1. Temps, jetons, coût par run

| Run | Modèle | Durée | Jetons (rapportés) | Appels d'outils | Prix de vente | Écart |
|---|---|---|---|---|---|---|
| opus-1 | Opus 5.5 | 8 min 42 s | 255 313 | 22 | 168 000 $ | −13,4 % |
| opus-2 | Opus 5.5 | 7 min 42 s | 232 968 | 25 | 168 000 $ | −13,4 % |
| opus-3 | Opus 5.5 | 8 min 15 s | 241 739 | 19 | 180 000 $ | −7,2 % |
| sonnet-1 | Sonnet 5.5 | 8 min 49 s | 253 111 | 22 | 170 000 $ | −12,4 % |
| sonnet-2 | Sonnet 5.5 | 8 min 53 s | 236 837 | 26 | 175 000 $ | −9,8 % |
| sonnet-3 | Sonnet 5.5 | 7 min 57 s | 241 402 | 21 | 169 000 $ | −12,9 % |
| sonnet-4 | Sonnet 5.5 | 8 min 49 s | 234 083 | 25 | 176 000 $ | −9,3 % |
| sonnet-5 | Sonnet 5.5 | 10 min 43 s | 289 409 | 25 | 180 000 $ | −7,2 % |
| essaim-1 | Opus 5.5 (seul, 5 lots) | 11 min 19 s | 256 885 | 39 | 170 000 $ | −12,4 % |

Moyennes : Opus solo 8 min 13 s / 243 k jetons ; Sonnet solo 9 min 02 s / 251 k jetons. **Même temps, mêmes jetons, même précision** :
Sonnet n'est ni plus vite ni moins bon qu'Opus sur cette tâche.

Coût (tarif de base, hors cache ; les jetons rapportés ne séparent pas entrée/sortie, hypothèse 85 % entrée / 15 % sortie) :

| Modèle | Entrée | Sortie | Coût estimé par run (≈245 k jetons) |
|---|---|---|---|
| Opus 5.5 | 4 $/MTok | 20 $/MTok | ≈ 1,57 $ |
| Sonnet 5.5 | 2 $/MTok | 10 $/MTok | ≈ 0,78 $ |
| Haiku 5.5 (≤100 k) | 0,10 $/MTok | 0,50 $/MTok | ≈ 0,04 $ |
| Fable 5.1 | 10 $/MTok | 50 $/MTok | ≈ 3,9 $ |

Banc de 8 solos ≈ 8,6 $. Avec cache (0,05× sur Opus/Sonnet 5.5 pour les lectures), le kit relu 8 fois coûterait une fraction.

## 2. Canaux de communication entre modèles

- Solo : aucun canal, un agent, un dossier. Simple, mesurable, reproductible (chaque script ré-exécuté donne le même JSON).
- Essaim 1 (prévu : Opus → 5 Sonnet) : **le canal n'existe pas** dans cet environnement, un sous-agent n'a pas l'outil Agent.
  L'Opus a fait les 5 lots seul, en séquence ; son « vérificateur » (lot 5) est la même instance qui se relit : aucune indépendance.
- Essaim 2 (Fable → 2 Opus → 6 Sonnet → 18 Haiku) : converti en **relais par fichiers** : chaque niveau écrit les prompts et l'effort
  de ses subalternes dans `prompts/`, la session principale lance les agents, les sorties remontent par `lots/`. Le canal est
  donc : prompt écrit → fichier → agent → fichier JSON → niveau supérieur. Pas de dialogue aller-retour ; une seule passe par niveau.
- Conséquence : dans Claude Code, la profondeur de délégation est 1 (session → sous-agents). Une pyramide à la oh-my-pi exige un
  orchestrateur externe (OMC `omc team`, ou un script Agent SDK) qui lance chaque niveau lui-même. À tester dans la nuit.

## 3. Prompts

- Un seul brief pour 8 solos (CONSIGNES.md + METHODE.md + prompt de lancement) : il a suffi pour que 8/8 produisent un script
  déterministe, un JSON au bon schéma, des sources par ligne, et signalent la même incohérence (lot éclairage). Les prompts n'ont
  pas causé l'écart ; **l'écart vient de ce que le brief ne dit pas** (postes composites, monuments, E.A.E, conduits).
- Les 8 ont inventé des codes de ligne différents quand la feuille Détail n'en donnait pas (R-01, A-10d, D-11/E-06…) : il faut
  imposer une nomenclature de codes dans CONSIGNES.md pour que le comparateur rapproche ligne à ligne.
- Variance intra-modèle (168 → 180 k$ chez Opus, 169 → 180 k$ chez Sonnet) = décisions de portée prises différemment avec le même
  brief. C'est la mesure de ce qui manque à la méthode écrite.

## 4. Outils et bibliothèques disponibles

- Utilisés : Bash (15 à 28 appels par run), Read (2 à 5), Write/Edit (6 à 12), python3 + openpyxl + stdlib. Aucun agent n'a eu
  besoin d'autre chose. Aucune tentative de sortir du kit (0 fuite sur 9).
- Manquant observé : `ModuleNotFoundError` ×2 dans **chaque** run (9/9) — même import raté deux fois par agent au début
  (bibliothèque absente testée à tâtons, ex. pandas). Coût : 2 appels Bash par run, ≈ 20 s. Remède : écrire dans CONSIGNES.md
  la liste exacte des bibliothèques disponibles (openpyxl, stdlib) et interdites.
- Manquant structurel : pas d'outil de diagnostic de code avant exécution ; pas d'accès Lumen ; catalogue sans colonne TEMPSEC.

## 5. Erreurs de code — et ce qu'un agent-lsp aurait changé

Exécution : 3 tracebacks en tout (opus-2 ×1, sonnet-5 ×2 avec 4 KeyError), 1 erreur d'outil (sonnet-5). Les agents ont corrigé
eux-mêmes en 1 à 2 itérations ; aucun script final ne plante.

Diagnostic statique pyright sur les scripts **finaux** (ceux qui tournent) :

| Run | Erreurs pyright | Types d'erreurs |
|---|---|---|
| opus-1 | 3 | argument None / Optional |
| opus-2 | 2 | idem |
| opus-3 | 8 | reportArgumentType ×4, reportOptional* ×4 |
| sonnet-1 | 1 | |
| sonnet-2 | 4 | |
| sonnet-3 | 2 | |
| sonnet-4 | 4 | |
| sonnet-5 | 4 | reportArgumentType ×4 (valeur de cellule → int) |
| essaim-1 | 10 | reportPossiblyUnboundVariable ×4, Optional ×4, ArgumentType ×2 |

Lecture : 38 défauts de typage latents dans 9 scripts qui « marchent ». Ce sont exactement les cas qui plantent au prochain
dossier (cellule vide → None, variable non définie dans une branche). **Un agent-lsp branché (pyright via `agent-lsp`) les aurait
montrés à l'agent avant l'exécution**, et aurait évité les 3 tracebacks et les 4 KeyError de sonnet-5. Gain estimé : 1 à 2 itérations
par run (≈ 1 min, ≈ 20 k jetons), et surtout des scripts réutilisables sur le dossier suivant.

Ce que l'agent aurait eu besoin d'avoir installé, liste exacte :
- `agent-lsp` (binaire Go) : `go install github.com/blackwell-systems/agent-lsp/cmd/agent-lsp@latest` ou le script curl ; `agent-lsp init`
  pour écrire la config MCP ; `agent-lsp doctor` pour vérifier.
- Serveurs de langage : `pyright` (Python, npm) ; pour les scripts PowerShell du poste : `powershell-editor-services` ; pour JSON/YAML :
  `vscode-langservers-extracted`, `yaml-language-server` (déjà dans l'environnement isolé).
- Permission Claude Code : `"mcp__lsp__*"` dans `permissions.allow`.
- Et, hors LSP, ce qui aurait évité le plus d'écart : **une règle écrite par décision manquante** (section SYNTHESE.md). Aucun outil ne
  remplace ça.

## 6. Verdict d'évaluation

| Critère | Solo Opus | Solo Sonnet | Essaim 1 | Essaim 2 |
|---|---|---|---|---|
| Précision (écart prix) | −7 à −13 % | −7 à −13 % | −12 % | en cours |
| Temps | 8 min | 9 min | 11 min | en cours |
| Coût | ≈ 1,6 $ | ≈ 0,8 $ | ≈ 1,6 $ | en cours |
| Reproductibilité du script | oui (9/9) | oui | oui | |
| Indépendance de vérification | aucune | aucune | aucune (même instance) | par niveaux |

Sur cette tâche, **Sonnet 5.5 solo = Opus 5.5 solo à la moitié du prix**. Ce qui ferait gagner les derniers pourcentages n'est ni
le modèle ni l'essaim : ce sont les 5 règles à trancher (SYNTHESE.md), un comparateur ligne à ligne avec codes imposés, et un LSP
branché pour que les scripts survivent au dossier suivant.
