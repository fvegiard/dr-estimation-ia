# MCP « planexpert-vm » — Plan Expert 3.0.17 dans la VM Windows Server 2025 (mxlinux)

Serveur MCP minimal (SDK officiel Python `mcp` 2.2.0, `MCPServer`, stdio) qui emballe la VM : `mcp/planexpert_vm/server.py`.
Enregistré dans Claude Code WSL (portée utilisateur, `~/.claude.json`) :

    claude mcp add -s user planexpert-vm -- /home/fvegi/.local/share/mise/shims/uv run /mnt/d/claude/releve-auto/repo/mcp/planexpert_vm/server.py
    claude mcp get planexpert-vm      →  Status: ✔ Connected   (vérifié 2026-09-17 03:54)

Le pipeline `releve/run.py` l'appelle sans protocole MCP : `uv run mcp/planexpert_vm/server.py --cli natif <dossier-planexpert> <OUTBOX/nom>`.

## Outils

| outil | fait quoi | comment |
|---|---|---|
| `etat()` | mxlinux, conteneur `planexpert`, SSH VM, processus Plan Expert, sessions | `ssh mx`, `ssh winsrv` (PowerShell 5.1 par `-EncodedCommand`) |
| `upload_project(dossier)` | dossier local (.qpl + PNG) → `mxlinux:/srv/planexpert/shared/<nom>/` (= `\\host.lan\Data\<nom>`) → `C:\Projets\<nom>` ; sha256 comparés | `scp`, `robocopy`, `Get-FileHash` |
| `open_qpl(chemin="")` | ferme Plan Expert + Edge, relance `PlanExpert.exe "<qpl>"` dans la session interactive 1 ; capture | tâche planifiée `PE-Open` (`-LogonType Interactive`) |
| `export_reports(formats=[pdf,xls,xml])` | onglet Rapports → Métré → Exporter vers PDF / Excel / XML ; ferme Edge ; attend les fichiers `Mes rapports\<qpl>-…` | `vncdo` clics à coordonnées fixes |
| `export_plans_pdf()` | onglet Plans → Exporter vers PDF → Sélectionner tout → Confirmer ; attend `Mes plans PDF\Fichiers exportés\<qpl>\<qpl>.pdf` (taille stable) | `vncdo` |
| `screenshot()` | capture PNG 1280×800 (retournée en image + `work/captures/`) | `vncdo capture` sur mxlinux, `scp` |
| `download(outbox, projet="")` | exports → `\\host.lan\Data\sorties\<projet>\` → `scp` → dossier local ; sha256 | PowerShell + `scp` |
| `vnc_raw(actions)` | actions vncdo libres (`move x y click 1 key esc …`) + capture | dépannage |

## Choix (et pourquoi)
- **VNC direct de QEMU** (`<IP conteneur>::5900`, IP lue par `podman inspect planexpert`) avec `vncdo` déjà installé sur mxlinux
  (`/home/fvegiard/.venv-vnc`), plutôt que `vncdotool` à travers noVNC `:8006/websockify` : vncdotool ne parle pas WebSocket, et le VNC
  de QEMU est le même écran que la visionneuse noVNC.
- **Jamais de saisie de chemin au clavier** (clavier VM en FRA/AZERTY) : ouverture par tâche planifiée avec le .qpl en argument ;
  fichiers par partage `\\host.lan\Data` ; PowerShell par `-EncodedCommand` (UTF-16LE base64) — les guillemets imbriqués `ssh winsrv "…"`
  se coupaient et bloquaient la session (constaté 2026-09-17).
- Coordonnées mesurées sur captures (écran 1280×800, ruban Plan Expert) : Plans (152,43), Rapports (212,43), Exporter Excel/XML/HTML/PDF
  (257/316/378/437, 95), Plans → Exporter vers PDF (538,95), Sélectionner tout (596,714), Confirmer (868,715), Annuler (933,715), Métré (68,192).
  Si la fenêtre n'est pas maximisée ou la résolution change, les clics tombent à côté : `screenshot()` d'abord.
- Chaque export de rapport ouvre Edge (PDF/HTML) ou « Ouvrir avec » (XLS) : Edge est tué par SSH, Échap envoyé.

## Ce qui n'est pas fait / limites
- Pas de lecture de la barre de titre par SSH (session non interactive) : la vérification « bon projet ouvert » se fait sur la capture.
- Un seul utilisateur : `open_qpl` ferme le projet en cours sans sauvegarder.
- Doc Plan Expert : `/srv/planexpert/oem/PlanExpert/Help/fr-FR/PlanExpert.chm` sur mxlinux (non extraite ici).
