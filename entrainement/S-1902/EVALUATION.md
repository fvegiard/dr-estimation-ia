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
| essaim-2 | Fable → 2 Opus → 6 Sonnet → 18 Haiku | **1 h 41 min** (mur d'horloge, 08:13 → 09:55) | ≥ 2,07 M mesurés (Fable 516 006, Opus A 439 441, Opus B 815 851, chef B3 168 685 pour sa seule 2e passe ; les 5 autres chefs et les 18 Haiku ≈ 1,2 M + 1,1 M estimés) | ≥ 94 (4 agents de tête) | 175 000 $ | −9,8 % |

Moyennes : Opus solo 8 min 13 s / 243 k jetons ; Sonnet solo 9 min 02 s / 251 k jetons. **Même temps, mêmes jetons, même précision** :
Sonnet n'est ni plus vite ni moins bon qu'Opus sur cette tâche.

Coût (tarif de base, hors cache ; les jetons rapportés ne séparent pas entrée/sortie, hypothèse 85 % entrée / 15 % sortie) :

| Modèle | Entrée | Sortie | Coût estimé par run (≈245 k jetons) |
|---|---|---|---|
| Opus 5.5 | 4 $/MTok | 20 $/MTok | ≈ 1,57 $ |
| Sonnet 5.5 | 2 $/MTok | 10 $/MTok | ≈ 0,78 $ |
| Haiku 5.5 (≤100 k) | 0,10 $/MTok | 0,50 $/MTok | ≈ 0,04 $ |
| Fable 5.1 | 10 $/MTok | 50 $/MTok | ≈ 3,9 $ |

Banc de 8 solos ≈ 8,6 $. **Essaim 2 ≈ 20 $ à lui seul** (Fable 8,3 $ + Opus 8,0 $ + Sonnet ≈ 3,8 $ + Haiku ≈ 0,2 $) pour le même
175 000 $ que sonnet-2 (0,78 $) : 25× le coût, 11× le temps, zéro gain de précision. Avec cache (0,05× sur Opus/Sonnet 5.5 pour les lectures), le kit relu 8 fois coûterait une fraction.

## 2. Canaux de communication entre modèles

- Solo : aucun canal, un agent, un dossier. Simple, mesurable, reproductible (chaque script ré-exécuté donne le même JSON).
- Essaim 1 (prévu : Opus → 5 Sonnet) : **le canal n'existe pas** dans cet environnement, un sous-agent n'a pas l'outil Agent.
  L'Opus a fait les 5 lots seul, en séquence ; son « vérificateur » (lot 5) est la même instance qui se relit : aucune indépendance.
- Essaim 2 (Fable → 2 Opus → 6 Sonnet → 18 Haiku) : converti en **relais par fichiers** : chaque niveau écrit les prompts et l'effort
  de ses subalternes dans `prompts/`, la session principale lance les agents, les sorties remontent par `lots/`. Le canal est
  donc : prompt écrit → fichier → agent → fichier JSON → niveau supérieur. Pas de dialogue aller-retour ; une seule passe par niveau.
- Essaim 2, mesuré : 27 agents, ~45 lancements (chaque chef et directeur est relancé une fois pour consolider), 4 niveaux
  de prompts réécrits (ARCHITECTURE.md → directeur → chef → releveur, règles d'aveugle recopiées 27 fois). Ce que le relais a
  donné : contrôles 5/5 à chaque niveau, une table d'articles de bordereau (B3) et 44 doubles comptes documentés — de la
  **traçabilité**, pas de la **précision** : le prix final (175 000 $) tombe sur les mêmes trois décisions manquantes que les
  solos (postes composites, monuments, E.A.E/conduits). Un niveau de plus ne crée pas la règle que METHODE.md ne contient pas.
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

Exécution, solos : 3 tracebacks en tout (opus-2 ×1, sonnet-5 ×2 avec 4 KeyError), 1 erreur d'outil (sonnet-5). Essaim 2 : 3 tracebacks
chez Fable (étape 2) et 1 chez le directeur B, 0 chez le chef B3 — corrigés en une itération chacun. Les agents ont corrigé
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
| essaim-2 (Fable) | **0** | — (18 Ko, lit lots/*.json + kit, 47 libellés revérifiés au catalogue par le script lui-même) |

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
| Précision (écart prix) | −7 à −13 % | −7 à −13 % | −12,4 % | −9,8 % |
| Temps | 8 min | 9 min | 11 min | 1 h 41 |
| Coût | ≈ 1,6 $ | ≈ 0,8 $ | ≈ 1,6 $ | ≈ 20 $ |
| Reproductibilité du script | oui (9/9) | oui | oui | oui (pyright 0 erreur) |
| Indépendance de vérification | aucune | aucune | aucune (même instance) | réelle (5/5 à 3 niveaux, 44 doubles comptes tracés) |

Sur cette tâche, **Sonnet 5.5 solo = Opus 5.5 solo à la moitié du prix**, et **l'essaim 2 = sonnet-2 à 25× le prix**. La pyramide
vaut pour ce qu'elle produit en plus (traçabilité, table d'articles, doubles comptes arbitrés par écrit) — pas pour le chiffre final. Ce qui ferait gagner les derniers pourcentages n'est ni
le modèle ni l'essaim : ce sont les 5 règles à trancher (SYNTHESE.md), un comparateur ligne à ligne avec codes imposés, et un LSP
branché pour que les scripts survivent au dossier suivant.

## Mise à jour 2026-10-23 — protocole v2

La « suggestion d'architecture » ci-dessus (trois Sonnet en parallèle, Opus arbitre) est remplacée par le protocole v2
(`entrainement/README.md`) : trois runs d'accord entre eux ne prouvent rien quand ils partagent la même règle manquante (les
10 runs v1 étaient d'accord pour sortir 7 à 13 % sous la référence). Le prix sort maintenant d'un moteur commun
(`chiffrage_commun.py`) ; le modèle relève et tranche (`quantites.json`, `decisions.json`) ; le comparateur juge sur le prix,
les heures et chaque article et attribue l'écart par décision. Le kit est identique d'un run à l'autre et le prompt est
construit avec sa partie commune en tête (`prompt-run.md`) pour profiter du cache de préfixe du fournisseur.
