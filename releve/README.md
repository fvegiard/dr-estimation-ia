# releve/ — relevé de quantités automatique (« je donne un dossier, je reçois mon PDF »)

Le code vit dans le dépôt. Le lanceur accepte un dossier local contenant les PDF ou un nom de dossier déjà
dans `INBOX`. Sous Windows, les résultats vont par défaut dans `D:\claude\releve-auto\OUTBOX\<nom>`;
`RELEVE_BASE` permet de changer la racine. Sous WSL, la valeur par défaut est `/mnt/d/claude/releve-auto`.
Le traitement NVIDIA et les PDF générés ne nécessitent ni VM Plan Expert ni lecteur Google Drive.

## Utilisation NVIDIA sous Windows

Depuis la racine du dépôt, dans PowerShell 7, avec `uv` disponible et `NVIDIA_API_KEY` déjà présente dans
l'environnement du processus. Ne jamais mettre la valeur de la clé dans une commande, un journal ou le dépôt.
Si la variable vient d'être configurée dans Windows, ouvrir un nouveau terminal pour qu'il l'hérite.

```powershell
if (-not $env:NVIDIA_API_KEY) { throw 'NVIDIA_API_KEY absente de ce processus' }
$env:RELEVE_NATIF = '0'
$env:RELEVE_MAX_TURNS = '40'
$env:RELEVE_NVIDIA_TIMEOUT = '120'
$env:RELEVE_NVIDIA_ATTEMPTS = '2'
$env:RELEVE_NVIDIA_REASONING = 'high'
uv run releve/run.py 'C:\Plans\Mon-projet' --agent nvidia --model moonshotai/kimi-k3
```

Remplacer le dossier par celui à traiter. `--model` choisit explicitement le modèle NVIDIA; sans cette option,
`RELEVE_NVIDIA_MODEL` s'applique, puis le défaut du code `moonshotai/kimi-k3`. Cet identifiant configuré
ne constitue pas une preuve de disponibilité actuelle ni de précision sur un plan donné.
Pour Kimi K3, `RELEVE_NVIDIA_REASONING` accepte `low`, `high` ou `max` (défaut `high`).
Le délai réseau par tentative est réglable de 1 à 600 secondes (défaut 120); le nombre total de tentatives
va de 1 à 5 (défaut 2). Les reprises admissibles sont journalisées. Ces bornes et le maximum de tours
ne constituent pas une durée maximale globale du traitement. L'exemple limite le relevé à 40 tours;
le lanceur utilise 800 tours si `RELEVE_MAX_TURNS` n'est pas défini.

Un échec de l'agent ou du contrôle qualité arrête la génération et renvoie un code de sortie non nul.
Consulter `STATUT.md`, `journal-etapes.log`, `travail/agent-journal.log`, `travail/agent-resultat.json`
et `travail/qualite.json`. Le statut indique le fournisseur et le modèle réellement rapportés.
Si tous les contrôles passent, les sorties comprennent `<nom>-format-exemple.pdf`,
`<nom>-format-exemple.report.json`, le dossier intermédiaire `format-exemple/`, les PDF historiques et le QPL.

`uv run releve/run.py --reprendre '<nom>'` réutilise le travail existant, refait le contrôle qualité puis les
sorties; il ne refait pas le relevé IA. `--watch` surveille les dossiers INBOX et accepte aussi `--agent` et `--model`.

## Chaîne

| étape | fichier | nature | entrée → sortie |
|---|---|---|---|
| 0 | `run.py` | lanceur, verrou, journal, STATUT.md, copie Drive | `INBOX/<nom>` → `OUTBOX/<nom>` |
| 1 | `prepare.py` | déterministe (pymupdf) | PDF → feuilles, rasters 5694 px, tuiles graduées, mots vectoriels, légendes de l'estimateur |
| 2 | `agent_nvidia.py` ou Claude OAuth, compétence `.claude/skills/releve-planexpert/SKILL.md` | jugement (lecture des légendes, classement, contrôle visuel) | → `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`, `reserves.md`, `rapport-releve.md`, éventuellement `comparaison-estimateur.md` |
| 2a | `extract_occurrences.py` | déterministe | nomenclature (regex) × mots → occurrences texte |
| 2b | `zoom.py` | outil de l'agent | zone d'une feuille avec règles et marques déjà relevées |
| 2c | `controle_qualite.py` | bloquant, y compris en reprise | feuilles, nomenclature, occurrences et réserves → `qualite.json` |
| 3 | `build_qpl.py` | déterministe | occurrences → `.qpl` Plan Expert (+ rasters à côté), audit JSON |
| 4 | `render_pdf.py` | déterministe | `.qpl` logique → `Plans-annotes.pdf`, `Rapport-de-metre.pdf/.md`, `Dossier-complet.pdf` |
| 5 | `src.estimer.render.from_releve` | déterministe | travail → `<nom>-format-exemple.pdf` et rapport JSON; formats matériel, agrégé ou travaux selon le classement des feuilles |
| 6 (option) | `../mcp/planexpert_vm/server.py --cli natif` | VM Plan Expert (MCP planexpert-vm) | `.qpl` → export natif dans `OUTBOX/<nom>/export-natif-planexpert/` si le composant est présent; jamais bloquant |

## Modes historiques optionnels

Sans `--agent`, le lanceur lit `RELEVE_AGENT`, avec `sdk` comme défaut pour conserver la compatibilité Claude.
`--agent sdk` utilise `releve/agent_sdk.py` et l'authentification Claude OAuth existante;
`--agent cli` utilise `claude -p`. `--model` ou `RELEVE_MODEL` sélectionne leur modèle (défaut `opus`).
`RELEVE_BUDGET_USD` concerne le SDK Claude, pas NVIDIA. Aucun remplacement de clé dans le SDK Claude n'est nécessaire
pour NVIDIA : c'est un agent distinct.

`RELEVE_NATIF=0` désactive l'export VM. Le défaut reste `1`, mais l'export est ignoré si son composant est absent.
Le miroir Drive historique est utilisé seulement s'il est accessible; son chemin est réglable par `RELEVE_DRIVE`
(défaut WSL `/mnt/g/My Drive/AI/Releves-auto`). Il s'agit d'un miroir de fichiers, pas d'une connexion API cloud.

## Conventions reprises du relevé S-1857 (REPRODUCTION.md, HANDOFF §3b)
- Raster 5694 px de large par feuille ; `px = pt × 5694 / largeur_pt` ; `Element X,Y` = coin haut-gauche, taille 26.
- Formes : 0 cercle, 1 carré, 2 losange, 3 triangle, 4 triangle inversé, 5 trapèze, 6 trapèze inversé ; couleurs ARGB signées.
- Légende Plan Expert à X = 0,746 × largeur, Y = 0,336 × hauteur (4250/1350 sur 5694 × 4022).
- Palette par famille alignée sur les pastilles de M. Dupuis (`commun.py::PALETTE_FAMILLE`, source `verification/rules_dupuis.py`).

## Limites (réelles)
- Le `.qpl` est généré par script ; l'étape optionnelle 6 l'ouvre dans Plan Expert (VM) et exporte rapport + plans natifs **si la VM répond et
  si le pilotage graphique (vncdo, coordonnées fixes 1280×800) réussit** ; sinon `STATUT.md` dit « export natif : non » et
  les PDF générés directement restent disponibles. Le `.qpl` n'est pas ré-enregistré par Plan Expert.
- Le relevé est celui de l'agent : compte d'objets à partir des étiquettes texte et de la lecture visuelle des tuiles ; pas de
  métrage de câble ni d'artères. Les réserves de l'agent sont dans `STATUT.md`.
- Un contrôle qualité réussi ne prouve pas à lui seul l'exactitude du relevé. Le rejeu des données de référence et
  la conformité du rendu ne remplacent pas l'essai sur un PDF vierge comparé à un relevé humain vérifié.
  La validation complète en conditions réelles reste à établir.
- Consommation : elle dépend du fournisseur sélectionné et de ses limites. Les tours et jetons sont rapportés;
  un coût absent ne veut pas dire que l'usage est gratuit.
