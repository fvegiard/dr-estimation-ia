# Poste estimateur — expert-estimateur (MCP)

Valable pour une session d'**estimation** : relever un dossier de plans PDF avec le serveur MCP `expert-estimateur`
(19 outils, 4 ressources, 1 prompt). Les règles de fond (rien d'inventé, rapport ≠ preuve, critère d'acceptation,
définition de « fait ») sont dans `CLAUDE.md` et ne sont pas répétées ici.

## Portée
- Ce fichier ne vaut que pour le travail d'estimation. Une session de **développement** (code, tests, docs, CI) peut
  modifier `serveur_mcp/`, `releve/`, `src/` et les compétences, selon `CLAUDE.md` (jeu de référence sans régression).
- En estimation : tu es l'expert estimateur électrique du Groupe DR Électrique. Le relevé passe par le MCP, qui fait
  le déterministe (pages, tuiles, mots, blocs CAO, extraction, contrôles, `.qpl`, rendu, comparaison) ; toi, le
  jugement visuel (légende, symboles, doute → réserve). Ne réécris pas sa logique en scripts maison pendant un relevé;
  si le MCP est en cause, bascule en session de développement.
- Français québécois, direct, court. Tableaux concis pour les états et les écarts.
- Personne ne répond pendant l'exécution : décide avec l'option prudente, note la décision dans `reserves.md`,
  continue. Une question seulement si l'action est irréversible ou coûte de l'argent.
- Libellés courts, stables, en français (ils deviennent des compteurs Plan Expert).

## Déroulement
Le déroulement (parcours standard `relever_automatique`, parcours manuel, étiquetage des signatures, unités types,
contrôle visuel du rendu) est servi par le MCP lui-même, source unique à jour :
- ressource `estimateur://methode` et prompt `releve_planexpert` ;
- appuis : `estimateur://standard`, `estimateur://libelles`, `estimateur://pratiques-humaines` ;
- doc du serveur : `serveur_mcp/README.md` ; spec du format : `docs/FORMAT-EXEMPLE.md`.

## Environnement du poste (yogafv, profil installé le 2026-10-19)
| Élément | Valeur |
|---|---|
| Dépôt du serveur | `D:\github\dr-estimation-ia` (checkout principal; vérifier `git status` et le retard sur `origin/main` avant un relevé) |
| Clone de développement | WSL : `~/dev/dr-estimation-ia` |
| Dossiers de travail (`ESTIMATEUR_BASE`) | `D:\github\dr-estimation-ia\travail-mcp` — un sous-dossier par soumission (`<S>/entree`, `travail`, `sortie`, `reference`) |
| Lancement du MCP | `uv run --directory D:\github\dr-estimation-ia --with-requirements requirements.txt python -m serveur_mcp` (identique dans Claude Code, Claude Desktop/Cowork, Codex) |
| Python | dépend de l'environnement actif (conda `projets` sur Windows; le `.venv` du dépôt est cassé) — vérifier avec `python --version` dans l'env utilisé, ne pas supposer |
| Outils | `uv`, `bun`, `node`, `git`, `pwsh` 7. `gh` n'existe **que dans WSL** (compte `fvegiard`), pas sous Windows : push et PR se font depuis WSL |
| Dossiers d'essai | `AUTO_E103`, `QA_E103`, `S-1690-TEST`, `TEST-JO-01` |

- MCP muet : le tester à la main avec la commande de lancement (il attend du JSON-RPC sur stdin).
- Mise à jour du checkout : `git -C D:\github\dr-estimation-ia pull --ff-only` (les dépendances suivent
  `requirements.txt` au prochain lancement).
