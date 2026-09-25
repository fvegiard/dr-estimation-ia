# Relevé automatique — mode d'emploi (Francis)

1. **Déposer** le dossier de la soumission (plans PDF, addendas, et si tu l'as le relevé de l'estimateur en PDF) dans
   `D:\claude\releve-auto\INBOX\<nom-de-la-soumission>\` (ou `G:\My Drive\AI\Releves-auto\INBOX\<nom>\`, le dossier est copié en local).
2. **Dire à Claude Code (WSL)** : `relève automatique de <nom-de-la-soumission>` — ou lancer toi-même
   `cd /mnt/d/claude/releve-auto/repo && uv run releve/run.py <nom>` (ou `--watch` pour surveiller l'INBOX en continu).
3. **Attendre** : ~30 à 60 min par dossier (agent Claude sur ton forfait Max, puis export Plan Expert dans la VM).
4. **Récupérer** dans `D:\claude\releve-auto\OUTBOX\<nom>\` (copie sur `G:\My Drive\AI\Releves-auto\OUTBOX\<nom>\`) :
   `<nom>-Plans-annotes.pdf`, `<nom>-Rapport-de-metre.pdf`, `<nom>-Dossier-complet.pdf`, le projet Plan Expert `<nom>-planexpert\<nom>.qpl`,
   et `export-natif-planexpert\` (rapport PDF/XLS/XML + PDF des plans faits par Plan Expert lui-même, quand la VM a répondu).
5. **Lire `STATUT.md`** en premier : état (TERMINÉ / ÉCHEC), « Export natif Plan Expert : oui/non », réserves de l'agent, coût, durées, sha256.

---

## Section technique

### Pièces (dépôt `fvegiard/saint-michel-planexpert-s1857`, branche `releve-auto`, clone `D:\claude\releve-auto\repo`)
- **A — pipeline** `releve/` : `run.py` (lanceur, verrou, journal, STATUT, Drive) → `prepare.py` → **`agent_sdk.py` (Claude Agent SDK
  `claude-agent-sdk` 0.2.154, OAuth claude.ai/Max, compétence `.claude/skills/releve-planexpert/SKILL.md`)** → `build_qpl.py` → `render_pdf.py`
  → export natif par la VM. Détails : `releve/README.md`. Docs officielles citées : `D:\claude\releve-auto\docs\` (+ `PROVENANCE-DOCS.md`, sha256).
- **B — MCP `planexpert-vm`** `mcp/planexpert_vm/server.py` (SDK `mcp` 2.2.0) : `etat`, `upload_project`, `open_qpl`, `export_reports`,
  `export_plans_pdf`, `screenshot`, `download`, `vnc_raw`. Enregistré dans Claude Code WSL (portée utilisateur). Détails : `mcp/planexpert_vm/README.md`.

### Authentification
`claude auth status` (WSL Ubuntu-26.04) → `loggedIn: true`, `authMethod: claude.ai`, `subscriptionType: max`. Le SDK lance le CLI Claude Code, qui
utilise ce profil ; aucune clé API, aucune variable d'environnement. Pour un poste sans connexion interactive : `claude setup-token` →
`CLAUDE_CODE_OAUTH_TOKEN` (doc `authentication.md` L.248-259). Ne jamais mettre ce jeton dans Git.

### Variables utiles (`run.py`)
`RELEVE_MODEL` (opus), `RELEVE_MAX_TURNS` (800), `RELEVE_BUDGET_USD` (0 = illimité), `RELEVE_AGENT` (`sdk` | `cli`), `RELEVE_NATIF` (1 | 0),
`RELEVE_BASE`, `RELEVE_DRIVE`. Reprise sans relancer l'agent : `uv run releve/run.py --reprendre <nom>`.

### VM Plan Expert
mxlinux 100.96.185.59 (Tailscale) : conteneur Podman `planexpert` (Windows Server 2025, Plan Expert 3.0.17), visionneuse http://100.96.185.59:8006,
SSH `ssh winsrv` (port 2222, PowerShell 5.1), partage `/srv/planexpert/shared/` = `\\host.lan\Data` dans la VM. Un seul utilisateur à la fois :
l'export natif ferme le projet ouvert dans Plan Expert. Captures : `D:\claude\releve-auto\work\captures\`.

### Journal et preuves
`D:\claude\releve-auto\journal.log` (toutes les commandes), `OUTBOX\<nom>\journal-etapes.log` (sorties complètes), `OUTBOX\<nom>\travail\agent-journal.log`
(chaque outil appelé par l'agent), `travail\agent-resultat.json` (tours, coût, session).
