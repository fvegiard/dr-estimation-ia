# Provenance des documentations officielles (texte intégral, format Markdown servi par le site)

Téléchargées le 2026-09-17 depuis WSL Ubuntu-26.04 (`curl -L "<url>.md"`), empreintes `sha256sum` calculées sur place.
Les pages `platform.claude.com/docs/en/agent-sdk/*` redirigent vers la vue d'ensemble de `code.claude.com` (même sha256
f2b47a95…) ; `slash-commands` redirige vers la page `skills` (même sha256 94f93f72…).

| fichier | source | sha256 |
|---|---|---|
| code.claude.com_docs_en_agent-sdk_overview.md | https://code.claude.com/docs/en/agent-sdk/overview | f2b47a950ecc99e9cc41183838b81bd3916645f392839fb18dcf5594c266eaf5 |
| code.claude.com_docs_en_agent-sdk_python.md | https://code.claude.com/docs/en/agent-sdk/python | fbc3c3392e5be35c6ed28f2db8502ff4626a927f75ec47a24b91ba19e1633dae |
| code.claude.com_docs_en_agent-sdk_skills.md | https://code.claude.com/docs/en/agent-sdk/skills | 367d6194fc6145c1ff77c583c7bd375f7830f42655350628df6b60fd9c32c482 |
| code.claude.com_docs_en_agent-sdk_cost-tracking.md | https://code.claude.com/docs/en/agent-sdk/cost-tracking | 28f74ba243aa7319c7df0cbcd3ff7f30a46f75eaecb09d543bc3cf18aefe93fc |
| code.claude.com_docs_en_headless.md | https://code.claude.com/docs/en/headless | 72521df6ef71d978d8c8298e518db15a4362b4fbf97f32a36626e31d088675a1 |
| code.claude.com_docs_en_skills.md | https://code.claude.com/docs/en/skills | 94f93f724453ef8bd9cb94af5fe9cb73aa77b3573019f6f06e7a7844bbb49af1 |
| code.claude.com_docs_en_hooks.md | https://code.claude.com/docs/en/hooks | e19530ebc7709e76ace04022835e8dc55c46247152f1e4b3449e84c6ebdcb5a4 |
| code.claude.com_docs_en_slash-commands.md | https://code.claude.com/docs/en/slash-commands (→ skills) | 94f93f724453ef8bd9cb94af5fe9cb73aa77b3573019f6f06e7a7844bbb49af1 |
| platform.claude.com_docs_en_agent-sdk_*.md | https://platform.claude.com/docs/en/agent-sdk/… (→ overview) | f2b47a950ecc99e9cc41183838b81bd3916645f392839fb18dcf5594c266eaf5 |

## Passages qui fondent les choix techniques (numéros de ligne dans les fichiers ci-dessus)

- **Pourquoi `claude -p` (mode headless) et non le SDK Python** :
  `agent-sdk_overview.md:22` — « To drive the same agent loop from another language, run the CLI as a subprocess with the `-p` flag and `--output-format json`. »
  `agent-sdk_overview.md:43-45` — « Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods… » → le lanceur reste **Claude Code lui-même** (connexion Max de Francis), pas une application SDK.
- **Mode `-p`, code de sortie, JSON** : `headless.md:21-33`, `headless.md:124-160` (`--output-format json`, champ `total_cost_usd` : `headless.md:100`).
- **`--bare` non retenu** : `headless.md:43-49` — « Set ANTHROPIC_API_KEY before running it, because bare mode doesn't use your subscription login » ; « In bare mode, Claude Code never reads OAuth credentials ».
- **Permissions sans personne au clavier** : `headless.md:259-298` — `--allowedTools`, `--permission-mode acceptEdits`, `--permission-prompts none` (≥ v2.1.259 ; installé 2.1.274).
- **Compétence (skill) invoquée comme commande** : `skills.md:308-351` (frontmatter `name`, `description`, `disable-model-invocation`, `allowed-tools`), `skills.md:393-401` (`$ARGUMENTS`), `skills.md:520-537` (pré-approbation d'outils par la compétence, y compris en `-p`).
- **Coût** : `agent-sdk_cost-tracking.md` (estimation client, peut différer de la facture) ; le résultat JSON est archivé dans `travail/agent-resultat.json` de chaque relevé.

## Ajouts du 2026-09-17 (session Fable 5.1, `curl -sL` depuis WSL, `sha256sum`)

| fichier | source | sha256 |
|---|---|---|
| code.claude.com_docs_en_authentication.md | https://code.claude.com/docs/en/authentication (264 lignes) | 9505ac4d159739837c481d3e9bed18cd7a4ca7332f626264f5dd067a633e66ee |
| code.claude.com_docs_en_agent-sdk_sessions.md | https://code.claude.com/docs/en/agent-sdk/sessions | f0bc3b89f2dacc9c9d45bcd3d35333744eca350e0dd5e190b1eea4772cc3c088 |
| code.claude.com_docs_en_agent-sdk_custom-tools.md | https://code.claude.com/docs/en/agent-sdk/custom-tools | d512ca722c2f9b8242f05d6c0d69a9b4bd08971a68a8e220ec0d72fde966fc32 |
| code.claude.com_docs_en_agent-sdk_mcp.md | https://code.claude.com/docs/en/agent-sdk/mcp | c6c92f6d55a03b8c0dd198833b29885a7827441d834db438b83b0e33b37c38a8 |
| py.sdk.modelcontextprotocol.io_v2_migration_.html | https://py.sdk.modelcontextprotocol.io/v2/migration/ (FastMCP → MCPServer) | 8b245d3a0aebaa4ccc6c2859b78caf3ab657c5c86231c0ec874bc1a0dce11f73 |
| py.sdk.modelcontextprotocol.io_v2_.html | https://py.sdk.modelcontextprotocol.io/v2/ | 63020069b7db601eefc36a3c1520a662b38f8459cbf39788337516a82daec057 |
| py.sdk.modelcontextprotocol.io_v2_servers_.html | https://py.sdk.modelcontextprotocol.io/v2/servers/ | ceec7daaf009f2f0a8f17ad4ff1503e6ab2ec71f53a5df2d078d2dcc36dcd9d7 |

Versions vérifiées sur PyPI (JSON `https://pypi.org/pypi/<paquet>/json`, 2026-09-17) : `claude-agent-sdk` **0.2.154** (publié 2026-09-17T00:25Z),
`mcp` **2.2.0** (2026-09-07), `vncdotool` 1.4.2. Claude Code CLI installé : 2.1.274 ; `claude auth status` → loggedIn, authMethod claude.ai,
subscriptionType max.

### Passages fondant le choix « Agent SDK + OAuth » (révision de la décision du matin)
- `agent-sdk_python.md:807` (`allowed_tools`), `:811` (`permission_mode`), `:815` (`max_turns`), `:816` (`max_budget_usd`), `:819` (`model`),
  `:824` (`cwd`), `:827` (`add_dirs` → `--add-dir`, charge les compétences du dossier avec la source `project`), `:828` (`env`),
  `:832` (`stderr`), `:845` (`setting_sources`) ; `:1582-1596` (`ResultMessage` : `subtype`, `num_turns`, `session_id`, `total_cost_usd`).
- `authentication.md:248-259` : `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN`, « authenticates with your Claude subscription and requires a
  Pro, Max, Team, or Enterprise plan » ; `:262-263` : le mode `--bare` ne lit pas ce jeton. Le SDK lance le même CLI, qui lit le profil OAuth
  courant : preuve empirique `_tmp/sdk_smoke.py` (aucune variable `ANTHROPIC_API_KEY`/`CLAUDE_CODE_OAUTH_TOKEN`, réponse « OK-SDK »,
  `total_cost_usd` 0.032633, session 2a08bde1-2218-4cdf-8ec6-3a7a9ba781c5).
- `agent-sdk_overview.md:44` (interdiction d'offrir la connexion claude.ai à des tiers) : sans objet ici — outil interne de Francis, sur son
  propre abonnement, sur son propre poste. Le repli `claude -p` (`RELEVE_AGENT=cli`) reste disponible.
