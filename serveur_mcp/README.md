# Serveur MCP « Expert estimateur »

Le relevé de quantités électrique du Groupe DR Électrique, branché sur **n'importe quel LLM** compatible MCP
(Claude, GPT, Gemini, modèle local…), en local ou dans le nuage. Plus besoin de Claude Desktop, de Plan Expert ni de
machine virtuelle Hyper-V : on dépose un PDF de plans brut, on obtient le PDF annoté **au format de l'exemplaire
HR26-14** (pastilles sur chaque symbole + repère `I01-07`, encadré « RELEVE <feuille> - MATERIEL », pages
« BORDEREAU MATERIEL » 8 colonnes, réserves) et le projet Plan Expert `.qpl`.

Partage des rôles :
- **le LLM** fait le jugement visuel (légende, symboles, doute → réserve) en suivant la méthode
  `estimateur://methode` (la compétence `releve-planexpert`) ;
- **le serveur** fait tout le déterministe : préparation des pages, tuiles et mots, extraction par étiquettes,
  contrôles bloquants, `.qpl`, rendu PDF, comparaison à l'estimateur.

## Installation

```bash
pip install -r requirements.txt
```

## Local (stdio)

Configuration type d'un client MCP (Claude Desktop, VS Code / Copilot, Cursor, LM Studio…) :

```json
{
  "mcpServers": {
    "expert-estimateur": {
      "command": "python",
      "args": ["-m", "serveur_mcp"],
      "cwd": "D:/github/dr-estimation-ia",
      "env": { "ESTIMATEUR_BASE": "D:/estimations" }
    }
  }
}
```

## Nuage (Streamable HTTP)

```bash
export ESTIMATEUR_MCP_CLE="<clé aléatoire d'au moins 24 caractères>"
python -m serveur_mcp --transport http --hote 0.0.0.0 --port 8765 --hote-permis estim.mondomaine.ca
```

Point d'accès : `https://estim.mondomaine.ca/mcp`, en-tête `Authorization: Bearer <clé>`. La clé est obligatoire
dès que l'hôte n'est pas local ; la protection contre le « DNS rebinding » reste active (seuls les hôtes permis
passent). Mettre un proxy TLS devant (Caddy, nginx, Azure Container Apps…).

## Déroulement (ce que fait le LLM)

1. `deposer_fichier` (base64) ou `preparer_dossier(chemin_source=…)` en local → `preparer_dossier`.
2. Lire `estimateur://methode` (ou lancer le prompt `releve_planexpert`) et l'appliquer :
   `voir_image` des aperçus et tuiles, `zoomer` / `nature_traits` pour les zones denses,
   `ecrire_fichier` pour `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-visuel.csv`, `reserves.md`.
3. `extraire_occurrences` (étiquettes texte) → `verifier_releve` jusqu'à `"pret": true`
   (labels hors nomenclature, feuilles non classées, points hors page, doublons < 4 pt : bloquants).
4. `produire_livrables` → `sortie/<S>-RELEVE.pdf`, `<S>.qpl`, rapport de métré ; se contrôler soi-même avec
   `voir_image("sortie/<S>-RELEVE.pdf#1")`.
5. `comparer_estimateur` si le projet de l'estimateur est déposé dans `reference/`
   (`<S>-Dupuis-PlanExpert.qpl` + `dupuis-png-dimensions.txt`) ou présent dans `dossiers/<S>/reference/`.

Colonnes facultatives pour enrichir le bordereau (sinon « A PRECISER » / « MODELE NON PRECISE », jamais inventé) :
`nomenclature.csv` : `materiel, designation, portee, modele, prescription, code` ;
`occurrences-*.csv` : `portee, modele, prescription, parent, reserve`.

## Outils, ressources, prompt

| Outil | Rôle |
|---|---|
| `lister_dossiers`, `lister_fichiers`, `lire_fichier` | naviguer dans un dossier |
| `deposer_fichier`, `preparer_dossier` | entrée des plans / du projet de l'estimateur |
| `voir_image`, `zoomer`, `nature_traits` | lecture visuelle et vectorielle |
| `ecrire_fichier` | fichiers du relevé (liste fermée, dans `travail/`) |
| `extraire_occurrences`, `verifier_releve` | extraction par étiquettes, contrôles bloquants |
| `produire_livrables`, `recuperer_livrable` | PDF format exemplaire, `.qpl`, rapport ; téléchargement |
| `comparer_estimateur` | écart marque par marque avec l'estimateur |

Ressources : `estimateur://methode`, `estimateur://standard` (standard de l'exemplaire HR26-14),
`estimateur://libelles` (libellés Plan Expert appris des projets 2021-2026). Prompt : `releve_planexpert(dossier)`.

## Tests

```bash
python -m pytest tests/test_serveur_mcp.py -q
```

Chaîne complète sur un plan synthétique via un vrai client MCP, contrôles bloquants, et transport HTTP (401 sans clé).
