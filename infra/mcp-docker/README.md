# Docker MCP Toolkit ↔ Claude Desktop (poste yogafv) — correctif du 2026-10-20

## Symptôme
Claude Desktop : `MCP_DOCKER` en « retrying… Connection closed ». Log `%LOCALAPPDATA%\Claude\logs\mcp-server-MCP_DOCKER.log` :
`Cannot activate profile 'Claude'. Validation failed for 2 server(s): desktop-commander: paths (missing) ; markitdown: paths (missing)`.
Ce n'était **pas** le PATH : Claude Desktop résout bien `docker.exe` (`…\DockerDesktop\resources\bin\docker.exe`).

## Cause
Docker MCP Toolkit v0.44 fonctionne par **profils** ; le profil `claude` (11 serveurs) contenait deux serveurs dont la config obligatoire
`paths` était vide → le gateway quitte à l'init → Claude Desktop voit « Connection closed ».

## Correctif appliqué (scripts ici, exécutés dans l'environnement du raccourci « Google Cloud SDK Shell », sans toucher au PATH)
```
docker mcp profile export claude <sauvegarde.json>                      # sauvegarde d'abord
docker mcp profile config claude --set desktop-commander.paths=["D:/github/dr-estimation-ia"] --set markitdown.paths=["D:/github/dr-estimation-ia"]
docker mcp profile config claude --set rust-mcp-filesystem.allowed_directories=["D:/github/dr-estimation-ia"] --set rust-mcp-filesystem.allow_write=true --set rust-mcp-filesystem.enable_roots=false
docker mcp gateway run --profile claude --dry-run                       # attendu : exit 0, « 82 tools listed »
```
Dans `%APPDATA%\Claude\claude_desktop_config.json` (sauvegarde `.bak-<date>` faite), `mcpServers.MCP_DOCKER.env` reçoit en plus :
`MCP_GATEWAY_DOCKER_BIND_ALLOW_WRITABLE_PATHS = D:/github/dr-estimation-ia` (liste séparée par `;` sur Windows ; correspondance exacte,
insensible à la casse ; un chemin « writable » dispense aussi de la liste lecture-seule — `pkg/gateway/docker_binds.go` du dépôt
docker/mcp-gateway). Redémarrer Claude Desktop complètement après modification de l'`env`.

## État après correctif
`MCP_DOCKER` connecté (playwright, n8n, dockerhub, sequentialthinking, node-code-sandbox, hyperbrowser, next-devtools : 82 outils).
Reste ouvert : `desktop-commander`, `markitdown`, `rust-mcp-filesystem` passent la validation mais leur conteneur meurt à l'init
(« initialize: EOF ») — montage d'un chemin Windows tel quel dans un conteneur Linux ; `cloud-run-mcp` attend
`gcloud auth application-default login` (puis `--set cloud-run-mcp.credentials_path=<ADC>`).

## Fichiers
- `diag_mcp.cmd` : lance un `.ps1` dans l'environnement `cloud_env.bat` du Google Cloud SDK (pwsh 7, sortie dans `_claude_mcp_diag.txt`).
- `diag_mcp_passe5_correction.ps1` : la passe de correction (profil + env + dry-run), avec sauvegardes et validation JSON avant écriture.
