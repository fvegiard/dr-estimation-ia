# releve/ — relevé de quantités automatique (« je donne un dossier, je reçois mon PDF »)

Branche `releve-auto`. Tout vit dans le dépôt ; les données de Francis vivent dans `D:\claude\releve-auto\{INBOX,OUTBOX}`
(miroir Google Drive `G:\My Drive\AI\Releves-auto\`). Mode d'emploi pour Francis : `D:\claude\releve-auto\MODE-EMPLOI.md`.

## Chaîne

| étape | fichier | nature | entrée → sortie |
|---|---|---|---|
| 0 | `run.py` | lanceur, verrou, journal, STATUT.md, copie Drive | `INBOX/<nom>` → `OUTBOX/<nom>` |
| 1 | `prepare.py` | déterministe (pymupdf) | PDF → feuilles, rasters 5694 px, tuiles graduées, mots vectoriels, légendes de l'estimateur |
| 2 | agent Claude Code headless, compétence `.claude/skills/releve-planexpert/SKILL.md` | jugement (lecture des légendes, classement, contrôle visuel) | → `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`, `reserves.md`, `rapport-releve.md`, `comparaison-estimateur.md` |
| 2a | `extract_occurrences.py` | déterministe | nomenclature (regex) × mots → occurrences texte |
| 2b | `zoom.py` | outil de l'agent | zone d'une feuille avec règles et marques déjà relevées |
| 3 | `build_qpl.py` | déterministe | occurrences → `.qpl` Plan Expert (+ rasters à côté), audit JSON |
| 4 | `render_pdf.py` | déterministe | `.qpl` logique → `Plans-annotes.pdf`, `Rapport-de-metre.pdf/.md`, `Dossier-complet.pdf` |
| 5 | `../mcp/planexpert_vm/server.py --cli natif` | VM Plan Expert (MCP planexpert-vm) | `.qpl` → export natif (rapport PDF/XLS/XML + PDF des plans) dans `OUTBOX/<nom>/export-natif-planexpert/` ; `resultat.json` ; jamais bloquant |

Agent (étape 2) : **Claude Agent SDK** officiel, `releve/agent_sdk.py` (PyPI `claude-agent-sdk` 0.2.154, `query()` + `ClaudeAgentOptions`,
`setting_sources=["project"]` pour charger la compétence, `add_dirs=[travail]`, `permission_mode="acceptEdits"`, `allowed_tools` restreints,
`mcp_servers={}`), authentifié par la connexion claude.ai (Max) de `claude auth login` — pas de clé API. Repli : `RELEVE_AGENT=cli`
→ `claude -p "/releve-planexpert <travail>" --output-format json --permission-mode acceptEdits --permission-prompts none …`
(doc `docs/code.claude.com_docs_en_headless.md`). Variables : `RELEVE_MODEL` (opus), `RELEVE_MAX_TURNS` (800), `RELEVE_BUDGET_USD` (0 = illimité),
`RELEVE_NATIF` (1 = export natif par la VM, 0 = sauter).

## Conventions reprises du relevé S-1857 (REPRODUCTION.md, HANDOFF §3b)
- Raster 5694 px de large par feuille ; `px = pt × 5694 / largeur_pt` ; `Element X,Y` = coin haut-gauche, taille 26.
- Formes : 0 cercle, 1 carré, 2 losange, 3 triangle, 4 triangle inversé, 5 trapèze, 6 trapèze inversé ; couleurs ARGB signées.
- Légende Plan Expert à X = 0,746 × largeur, Y = 0,336 × hauteur (4250/1350 sur 5694 × 4022).
- Palette par famille alignée sur les pastilles de M. Dupuis (`commun.py::PALETTE_FAMILLE`, source `verification/rules_dupuis.py`).

## Limites (réelles)
- Le `.qpl` est généré par script ; l'étape 5 l'ouvre dans Plan Expert (VM) et exporte rapport + plans natifs **si la VM répond et
  si le pilotage graphique (vncdo, coordonnées fixes 1280×800) réussit** ; sinon `STATUT.md` dit « export natif : non » et le PDF
  « Plans annotés » de `render_pdf.py` (rendu équivalent) reste le livrable. Le `.qpl` n'est pas ré-enregistré par Plan Expert.
- Le relevé est celui de l'agent : compte d'objets à partir des étiquettes texte et de la lecture visuelle des tuiles ; pas de
  métrage de câble ni d'artères. Les réserves de l'agent sont dans `STATUT.md`.
- Consommation : un relevé complet utilise le forfait Max de Francis (quota 5 h / 7 jours) ; coût estimé dans `STATUT.md`.
