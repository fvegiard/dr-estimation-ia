# Regroupement des dépôts d'estimation (2026-11-09)

`dr-estimation-ia` est LE dépôt d'estimation : sa chaîne `releve/` + `src/estimer/render/` produit le PDF vectoriel
à calques OCG (sortie attendue par Francis). Les autres dépôts y ont été comparés fichier par fichier ; seul le code
unique et utile a été importé, avec sa provenance (commit source) ci-dessous.

## Importé

| Source (commit) | Destination | Contenu |
|---|---|---|
| `fvegiard/dre-estimation` (6102e4a) | `dre_estimation/`, `eewin/catalogue-llm/` | Catalogue EEWin pour LLM : moteur de prix (unités, ensembles, main-d'œuvre), recherche FR/EN, serveur MCP, devis Excel, scripts d'extraction VM → SQLite → Supabase. Ses tests exigent les vraies données EEWin (`eewin/catalogue-llm/data/`, non versionnées, reconstruites par `scripts/refresh.ps1` sur le poste qui a la VM) : ils vivent dans `eewin/catalogue-llm/tests/`, hors du gate CI. |
| `fvegiard/estimation-v2` (6287bbf) | `estimation_v2/`, `docs/estimation-v2/`, `tests/test_estimation_v2_exports.py` | Export déterministe des relevés aux profils Granby et CHUM (41 tests, fixtures synthétiques). |
| `fvegiard/planexpert-core` (c33bf2e) | `serveur_mcp/planexpert_vm/` | Serveur MCP de pilotage de la VM Plan Expert. |
| branches `agent/openhands/releve-S-0844`, `-S-0922`, `-S-1294` | `dossiers/S-*/releve-page-par-page/` | Relevés page par page d'OpenHands (ajouts seulement, fusion sans conflit). |

## Non importé (et pourquoi)

- `electrical-estimator-openai` : son moteur (`releve/`, `src/estimer/render/`) est une copie PLUS ANCIENNE de celui-ci
  (règles d'encadré simplifiées, sans les mesures du gold) ; ses `jobs/` (259 Mo de sorties S1830/E103) restent
  dans le dépôt archivé.
- `dr-releves-2026`, `planexpert-atelier`, `planexpert-hr26-14`, `planexpert-s1787-bioscript`,
  `planexpert-s1857-saint-michel`, `planexpert-infra-mxlinux`, `dr-estimation-releves` : anciennes copies de la chaîne
  ou données de projet déjà couvertes par `dossiers/` ; archivés en lecture seule sur GitHub (réversible).
- `lena-ai-jo-openagent`, `site-semantic-index`, `electrical-estimation-mcp` : autres outils, hors estimation.

## Clés

Aucune clé factice : gitleaks = 0 sur les 15 dépôts et sur toutes les branches. Le seul exemple d'identifiant,
`infra/mxlinux/.env.example` (`WIN_PASSWORD=changez-moi`), a été retiré au profit d'une consigne : la vraie valeur va
dans `infra/mxlinux/.env` (ignoré par git) sur le poste mxlinux. `eewin/catalogue-llm/scripts/sync_cloud.py`
échoue explicitement si `SUPABASE_SERVICE_ROLE_KEY` est absente — jamais de valeur par défaut.
