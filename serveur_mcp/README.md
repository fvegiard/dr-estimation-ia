# Serveur MCP « Expert estimateur »

Le relevé de quantités électrique du Groupe DR Électrique, branché sur **n'importe quel LLM** compatible MCP
(Claude, GPT, Gemini, modèle local…), en local ou dans le nuage. Plus besoin de Claude Desktop, de Plan Expert ni de
machine virtuelle Hyper-V : on dépose un PDF de plans brut, on obtient le PDF annoté **au format de l'exemplaire
HR26-14** (pastilles sur chaque symbole + repère `I01-07`, encadré « RELEVE <feuille> - MATERIEL », pages de
bordereau au format de chaque feuille — matériel, agrégé ou travaux, spec unique `docs/FORMAT-EXEMPLE.md` —,
réserves) et le projet Plan Expert `.qpl`.

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

Images : `voir_image` et `zoomer` renvoient du JPEG (plus léger que PNG pour les plans).

## Nuage (Streamable HTTP)

```bash
export ESTIMATEUR_MCP_CLE="<clé aléatoire d'au moins 24 caractères>"
python -m serveur_mcp --transport http --hote 0.0.0.0 --port 8765 --hote-permis estim.mondomaine.ca
```

Point d'accès : `https://estim.mondomaine.ca/mcp`, en-tête `Authorization: Bearer <clé>`. La clé est obligatoire
dès que l'hôte n'est pas local ; la protection contre le « DNS rebinding » reste active (seuls les hôtes permis
passent). Mettre un proxy TLS devant (Caddy, nginx, Azure Container Apps…).

## Pour les collègues : n'importe quel Claude, même résultat

**Un seul serveur pour tous** (sinon chaque poste a sa bibliothèque de blocs et les résultats divergent).

Mise en service (une fois, par Francis) :
```bash
docker build -t expert-estimateur .
docker run -d -p 8765:8765 -v estim:/data -e ESTIMATEUR_MCP_CLE=<clé 24+ car.> \
  -e ESTIMATEUR_URL_PUBLIQUE=https://<hôte> -e ESTIMATEUR_HOTE_PERMIS=<hôte> expert-estimateur
```
(proxy TLS devant ; sans Docker : `python -m serveur_mcp --transport http --hote 0.0.0.0 --hote-permis <hôte>` avec
les mêmes variables.)

Chaque collègue, une fois : claude.ai ou Claude Desktop → Paramètres → Connecteurs → **Ajouter un connecteur
personnalisé** → URL `https://<hôte>/mcp?cle=<clé>` (le connecteur n'envoie pas d'en-tête : la clé passe dans l'URL).

Ensuite, dans n'importe quelle conversation : « Fais le relevé de S-1902 : <lien Google Drive du PDF ou du dossier
de plans> ». Claude appelle `relever_automatique(dossier, url_source)` — c'est écrit dans les instructions du serveur —
et rend `lien_zip` (PNG annotés, calques, bordereaux, BOM) et `lien_releve_pdf` (format HR26-14). Le lien Drive doit
être partagé « toute personne disposant du lien » ; dans un dossier, les sous-dossiers Prix / take off / relevés ne sont
jamais lus. Les liens de livrables portent un jeton propre au fichier, jamais la clé.

Même PDF = mêmes fichiers (vérifié : deux appels → BOM, occurrences et nomenclature identiques au sha256). Seule
exception voulue : un bureau d'ingénieurs inconnu demande un étiquetage, une fois ; il entre alors dans la
bibliothèque du serveur et sort ensuite seul pour tout le monde. `verification_vision` (Gemini/NVIDIA) est hors du
parcours standard parce qu'elle n'est pas déterministe.

## En un appel : `relever_automatique`

`relever_automatique(dossier, chemin_source="<PDF ou dossier>")` fait tout, sans agent ni jeton : préparation,
blocs CAO, familles depuis `releve/bibliotheque-blocs.csv`, relevé, `.qpl`, PDF au format de l'exemplaire, et
`sortie/<S>-LIVRABLES-PNG.zip` (`<F>_annote.png`, `<F>_calque.png`, `<F>_bordereau_NN.png`, `<S>-BOM.csv/.xlsx`,
CSV du relevé). `feuille_unique="E103"` : une seule feuille.

Plan d'un **bureau d'ingénieurs encore inconnu** (blocs absents de la bibliothèque) : la réponse donne
`a_etiqueter` (signatures + planches `sortie/signatures/signatures-NN.png`) et la suite à faire :
1. `voir_image` de chaque planche (le LLM client a la vision ; `GEMINI_API_KEY` sur le serveur en étiquette déjà une
   partie, jamais en IGNORER) ;
2. `etiqueter_signatures(dossier, [{"sig_id": "S002", "label": "APPAREIL NLIGHT DP1", "famille": "commande",
   "forme": "carre", "materiel": "…"}, {"sig_id": "S006", "label": "IGNORER"}, …])` — chaque signature nouvelle
   entre dans la bibliothèque (`apprendre`, défaut oui) : le dossier suivant du même bureau sort sans rien étiqueter.
   Une signature générique déjà connue avec une autre règle (un rectangle = mur chez un bureau, boîtier chez un
   autre) reste propre au dossier et revient dans `non_appris` ;
3. `relever_automatique(dossier, reprendre=True)` → ZIP. Les signatures non étiquetées restent en réserve R-008.

Penser à committer `releve/bibliotheque-blocs.csv` après un nouveau bureau. `ESTIMATEUR_BIBLIOTHEQUE` : autre
fichier de bibliothèque (essais).

## Déroulement manuel (ce que fait le LLM)

1. `deposer_fichier` (base64) ou `preparer_dossier(chemin_source=…)` en local → `preparer_dossier`.
2. Lire `estimateur://methode` (ou lancer le prompt `releve_planexpert`) et l'appliquer :
   `voir_image` des aperçus et tuiles, `zoomer` / `nature_traits` pour les zones denses,
   `ecrire_fichier` pour `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-visuel.csv`, `reserves.md`.
3. `extraire_occurrences` (étiquettes texte) → `verifier_releve` jusqu'à `"pret": true`
   (labels hors nomenclature, feuilles non classées, points hors page, doublons < 4 pt : bloquants).
3b. **Unités types** (logements, chambres, salles « TYPE ») : écrire `multiplicateurs.csv`
   (`feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source` — zone vide = toute la feuille, la plus petite zone gagne,
   `source` obligatoire). `verifier_releve` bloque une feuille dont le cartouche dit TYPE/TYPIQUE sans multiplicateur.
   `quantites` → `sortie/quantites.csv` : repères représentés × facteur = quantités à soumissionner.
   Exemple réel : `dossiers/S-1695/multiplicateurs.csv` (77 chambres, luminaires −82,8 % → −5,3 % vs l'estimateur).
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
| `relever_automatique`, `etiqueter_signatures` | tout en un appel ; étiquetage des blocs inconnus + apprentissage |
| `quantites` | repères × `multiplicateurs.csv` (unités types) |
| `produire_livrables`, `recuperer_livrable` | PDF format exemplaire, `.qpl`, rapport ; téléchargement |
| `comparer_estimateur` | écart marque par marque avec l'estimateur |
| `chercher_libelle` | nom employé par les estimateurs pour un texte de légende |
| `exemples_humains` | planche des vrais symboles cliqués par les estimateurs pour un libellé + habitudes |

Ressources : `estimateur://methode`, `estimateur://standard` (standard de l'exemplaire HR26-14),
`estimateur://libelles` (libellés Plan Expert appris des projets 2021-2026),
`estimateur://pratiques-humaines` (ce que les estimateurs font des documents reçus). Prompt : `releve_planexpert(dossier)`.

## Savoir des estimateurs : document reçu ↔ ce qu'on en fait dans Plan Expert

Deux choses distinctes : **le document reçu** (PDF du client) et **ce que l'estimateur en fait dans Plan Expert**
(le `.qpl` : Plan Expert rastérise chaque page reçue en `<document> - <page>.png` et l'estimateur y pose une marque
par appareil). Seuls les documents rattachés à un `.qpl` servent : ce sont eux qui disent ce qu'on a fait.
`python -m src.apprentissage.lien_humain --racine <dossier des projets Plan Expert>` relit chaque marque sur la page
même où elle a été cliquée et écrit `apprentissage/lien-humain/` (`connaissance.json`, `documents.json`,
`galerie/*.jpg`, `PRATIQUES.md`). Ce dossier est dans le dépôt public : un LLM en nuage y a accès sans le serveur
de fichiers.

Le rendu passe par `src.estimer.render.from_releve` (même pont que la chaîne Claude : ancrage de la pastille sur
le symbole vectoriel, formats materiel/agrege/travaux). Le test `test_parite_claude_e103` rend le relevé S-1844 E103
de Claude par le serveur MCP (23 repères, plan + bordereau materiel + 12 réserves).

## Tests

```bash
python -m pytest tests/test_serveur_mcp.py tests/test_etiquetage_mcp.py tests/test_multiplicateurs.py -q
```

Chaîne complète sur un plan synthétique via un vrai client MCP, contrôles bloquants, et transport HTTP (401 sans clé).
