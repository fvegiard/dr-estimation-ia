# /// script
# requires-python = ">=3.12"
# dependencies = ["mcp==2.2.0", "pillow>=10"]
# ///
r"""MCP « planexpert-vm » : emballe la VM Windows Server 2025 (Plan Expert 3.0.17) qui tourne dans Podman sur mxlinux.

Serveur MCP officiel (paquet PyPI `mcp` 2.2.0, `MCPServer`, transport stdio ; doc : docs/py.sdk.modelcontextprotocol.io_v2_*.html).
Tout passe par SSH depuis WSL Ubuntu-26.04 (~/.ssh/config : `mx` = root@mxlinux, `winsrv` = francis@VM :2222) :
  - fichiers : scp vers /srv/planexpert/shared/<projet>/ sur mxlinux = \\host.lan\Data\<projet> dans la VM ;
  - PowerShell dans la VM : `powershell -EncodedCommand` (aucun problème de guillemets, sortie UTF-8) ;
  - interface graphique : `vncdo` (vncdotool 1.4.2, venv /home/fvegiard/.venv-vnc sur mxlinux) sur le VNC de QEMU
    (IP du conteneur :5900, lue par `podman inspect`) — même écran que la visionneuse noVNC http://100.96.185.59:8006 ;
  - clavier de la VM en AZERTY/FRA : on ne tape jamais de chemin ; l'ouverture d'un projet passe par une tâche planifiée
    interactive (`Register-ScheduledTask` + `New-ScheduledTaskPrincipal -LogonType Interactive`, fiche mxlinux).
Coordonnées d'écran (1280×800, ruban Plan Expert) mesurées sur captures du 2026-09-17 : voir COORD ci-dessous.

Utilisation : serveur MCP  `uv run mcp/planexpert_vm/server.py`
              ligne de commande (pipeline releve/run.py) : `uv run mcp/planexpert_vm/server.py --cli <commande> …`
"""
import os, sys, json, time, shlex, base64, hashlib, subprocess, datetime
from mcp.server.mcpserver import MCPServer, Image

SHARED = "/srv/planexpert/shared"                       # sur mxlinux
VNCDO = "/home/fvegiard/.venv-vnc/bin/vncdo"             # sur mxlinux
VM_PROJETS = r"C:\Projets"
VM_DOCS = r"C:\Users\francis\Documents\Plan Expert"
PE_EXE = r"C:\Program Files (x86)\Plan Expert\PlanExpert.exe"
LOCAL_SHOTS = os.environ.get("PLANEXPERT_VM_SHOTS", "/mnt/d/claude/releve-auto/work/captures")
STATE = os.path.expanduser("~/.planexpert-vm-state.json")
COORD = {  # écran 1280×800
    "onglet_plans": (152, 43), "onglet_rapports": (212, 43),
    "rapports_excel": (257, 95), "rapports_xml": (316, 95), "rapports_html": (378, 95), "rapports_pdf": (437, 95),
    "plans_export_pdf": (538, 95), "plans_selectionner_tout": (596, 714), "plans_confirmer": (868, 715), "plans_annuler": (933, 715),
    "rapport_metre": (68, 192),
}
KILL_VIEWERS = "Stop-Process -Name msedge,notepad,Notepad,EXCEL,wordpad,OpenWith -Force -ErrorAction SilentlyContinue"
def now(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def sh(cmd, timeout=120, check=False):
    p = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if check and p.returncode: raise RuntimeError(f"{cmd!r} → code {p.returncode}: {p.stderr[-500:]}")
    return p
def mx(cmd, timeout=120):
    return sh(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "mx", cmd], timeout)
def vm_ps(script, timeout=120):
    """PowerShell 5.1 dans la VM par SSH, script encodé (UTF-16LE base64) → texte UTF-8."""
    full = "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; $ErrorActionPreference='Continue'\n" + script
    enc = base64.b64encode(full.encode("utf-16-le")).decode()
    p = sh(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "winsrv", f"powershell -NoProfile -NonInteractive -OutputFormat Text -EncodedCommand {enc}"], timeout)
    out = (p.stdout or "").replace("\x00", "")
    return "\n".join(l for l in out.splitlines() if not l.startswith("**")).strip(), p.returncode
_vnc_ip = None
def vnc_target():
    global _vnc_ip
    if not _vnc_ip:
        p = mx("podman inspect planexpert -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'")
        _vnc_ip = (p.stdout.strip() or "10.89.0.2")
    return f"{_vnc_ip}::5900"
def vnc(actions, capture=None, timeout=90):
    """actions : chaîne vncdo (ex. 'move 152 43 click 1 pause 2'). capture : chemin local PNG facultatif."""
    cmd = f"{VNCDO} -s {vnc_target()} --timeout 60 {actions}"
    if capture: cmd += " pause 1 capture /tmp/pe-shot.png"
    p = mx(cmd, timeout)
    if p.returncode: raise RuntimeError(f"vncdo : {p.stderr[-400:]}")
    if capture:
        os.makedirs(os.path.dirname(capture), exist_ok=True)
        sh(["scp", "-q", "mx:/tmp/pe-shot.png", capture], 60, check=True)
    return p.stdout
def click(name, pause=2): return f"move {COORD[name][0]} {COORD[name][1]} click 1 pause {pause} "
def load_state():
    try: return json.load(open(STATE))
    except Exception: return {}
def save_state(**kw):
    s = load_state(); s.update(kw); json.dump(s, open(STATE, "w"), indent=1); return s
def shot_path(tag):
    return os.path.join(LOCAL_SHOTS, f"{datetime.datetime.now():%Y%m%d-%H%M%S}-{tag}.png")

# ---------------------------------------------------------------- opérations
def op_etat():
    r = {"date": now()}
    p = mx("hostname; podman ps --format '{{.Names}} {{.Status}}' ; ss -ltn | grep -c ':8006'", 30)
    r["mxlinux"] = p.stdout.strip() if p.returncode == 0 else f"injoignable : {p.stderr[-200:]}"
    out, code = vm_ps("hostname; (Get-Process PlanExpert -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { 'PlanExpert PID ' + $_.Id + ' RAM ' + [int]($_.WorkingSet64/1MB) + ' Mo' }); (query session 2>&1 | Out-String)", 40)
    r["vm"] = out if code == 0 else f"ssh winsrv code {code}: {out[-300:]}"
    r["vnc"] = vnc_target()
    r["projet_ouvert"] = load_state().get("projet")
    return r

def op_upload_project(dossier_local):
    """Copie un dossier (qpl + PNG) vers mxlinux:/srv/planexpert/shared/<nom>/ puis dans la VM C:\\Projets\\<nom>\\ (disque local, plus rapide)."""
    dossier_local = os.path.abspath(dossier_local)
    if not os.path.isdir(dossier_local): raise FileNotFoundError(dossier_local)
    name = os.path.basename(dossier_local.rstrip("/"))
    qpls = [f for f in os.listdir(dossier_local) if f.lower().endswith(".qpl")]
    if not qpls: raise RuntimeError("aucun .qpl dans " + dossier_local)
    mx(f"mkdir -p {shlex.quote(SHARED + '/' + name)}", 30)
    sh(["scp", "-q", "-r", dossier_local + "/.", f"mx:{SHARED}/{name}/"], 900, check=True)
    local_sums = {f: sha256(os.path.join(dossier_local, f)) for f in sorted(os.listdir(dossier_local)) if os.path.isfile(os.path.join(dossier_local, f))}
    out, code = vm_ps(f"""$src = '\\\\host.lan\\Data\\{name}'; $dst = '{VM_PROJETS}\\{name}'
New-Item -ItemType Directory -Force $dst | Out-Null
robocopy $src $dst /E /R:2 /W:2 /NP /NJH /NJS /NFL /NDL | Out-Null
Get-ChildItem $dst -File | ForEach-Object {{ $_.Name + ' ' + (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower() }}""", 600)
    vm_sums = dict(l.split(" ", 1) for l in out.splitlines() if " " in l)
    diff = [f for f, h in local_sums.items() if vm_sums.get(f) != h]
    if diff: raise RuntimeError(f"sha256 différents après copie dans la VM : {diff[:5]}")
    qpl_vm = f"{VM_PROJETS}\\{name}\\{qpls[0]}"
    save_state(projet=os.path.splitext(qpls[0])[0], qpl_vm=qpl_vm, dossier_vm=f"{VM_PROJETS}\\{name}")
    return {"nom": name, "fichiers": len(local_sums), "qpl_vm": qpl_vm, "sha256_verifies": True, "partage_mx": f"{SHARED}/{name}"}

def op_open_qpl(chemin_vm=None, attente=45):
    """Ferme Plan Expert s'il tourne, le relance sur le .qpl par une tâche planifiée interactive (session 1), capture l'écran."""
    chemin_vm = chemin_vm or load_state().get("qpl_vm")
    if not chemin_vm: raise RuntimeError("aucun chemin de .qpl (upload_project d'abord)")
    out, code = vm_ps(f"""$qpl = '{chemin_vm}'
if (-not (Test-Path -LiteralPath $qpl)) {{ 'INTROUVABLE ' + $qpl; exit 2 }}
Stop-Process -Name PlanExpert,msedge -Force -ErrorAction SilentlyContinue; Start-Sleep 3
Unregister-ScheduledTask -TaskName 'PE-Open' -Confirm:$false -ErrorAction SilentlyContinue
$a = New-ScheduledTaskAction -Execute '{PE_EXE}' -Argument ('"' + $qpl + '"') -WorkingDirectory 'C:\\Program Files (x86)\\Plan Expert'
$p = New-ScheduledTaskPrincipal -UserId 'francis' -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName 'PE-Open' -Action $a -Principal $p -Force | Out-Null
Start-ScheduledTask -TaskName 'PE-Open'
Start-Sleep {int(attente)}
$pr = Get-Process PlanExpert -ErrorAction SilentlyContinue
if ($pr) {{ 'PID ' + $pr.Id + ' RAM ' + [int]($pr.WorkingSet64/1MB) + ' Mo' }} else {{ 'ABSENT' }}""", int(attente) + 90)
    if "ABSENT" in out or code: raise RuntimeError("Plan Expert ne s'est pas lancé : " + out[-300:])
    shot = shot_path("open"); vnc("pause 1", capture=shot)
    save_state(qpl_vm=chemin_vm, projet=os.path.splitext(os.path.basename(chemin_vm.replace("\\", "/")))[0])
    return {"processus": out.strip(), "qpl": chemin_vm, "capture": shot, "note": "vérifier sur la capture que le titre de la fenêtre porte le nom du .qpl"}

def _vm_files(dir_vm, pattern, since_epoch=0):
    out, _ = vm_ps(f"""Get-ChildItem -LiteralPath '{dir_vm}' -Filter '{pattern}' -File -ErrorAction SilentlyContinue | ForEach-Object {{ $_.FullName + '|' + $_.Length + '|' + [int64](Get-Date $_.LastWriteTimeUtc -UFormat %s) }}""", 60)
    res = []
    for l in out.splitlines():
        if l.count("|") == 2:
            p, n, t = l.rsplit("|", 2)
            if int(t) >= since_epoch: res.append({"chemin": p, "octets": int(n)})
    return res

def op_export_reports(formats=("pdf", "xls", "xml")):
    """Onglet Rapports → Exporter vers PDF / Excel / XML. Chaque export ouvre Edge (PDF/HTML) ou la boîte « Ouvrir avec » (XLS) : on ferme Edge, on envoie Échap."""
    projet = load_state().get("projet")
    if not projet: raise RuntimeError("aucun projet ouvert connu (open_qpl d'abord)")
    t0 = int(time.time()) - 5
    vnc(click("onglet_rapports", 3) + click("rapport_metre", 8))          # génère le rapport Métré
    done = {}
    for f in formats:
        key = {"pdf": "rapports_pdf", "xls": "rapports_excel", "xml": "rapports_xml", "html": "rapports_html"}[f]
        vnc("move 700 14 click 1 pause 1 " + click("onglet_rapports", 2) + click(key, 6))   # clic de focus d'abord (voir export_plans_pdf)
        vm_ps(KILL_VIEWERS, 30)     # Edge (PDF/HTML), Bloc-notes/Excel (« Ouvrir avec » du .xls) : à fermer, sinon ils couvrent le ruban
        vnc("key esc pause 1")
        vm_ps(KILL_VIEWERS, 30)
        for _ in range(12):                                                  # attend le fichier (≤ 60 s)
            found = [x for x in _vm_files(VM_DOCS + r"\Mes rapports", f"{projet}*.{f}", t0)]
            if found and found[-1]["octets"] > 0: done[f] = found[-1]; break
            time.sleep(5)
        else: done[f] = None
    shot = shot_path("rapports"); vnc(click("onglet_plans", 1), capture=shot)
    return {"projet": projet, "exports": done, "capture": shot, "dossier_vm": VM_DOCS + r"\Mes rapports"}

def _barre_export_visible(png):
    """Vrai si la barre d'exportation des plans est affichée : le X rouge « Annuler » est en (933,700) sur l'écran 1280×800."""
    from PIL import Image as PILImage
    r, g, b = PILImage.open(png).convert("RGB").getpixel((933, 700))
    return r > 150 and g < 100 and b < 100

def op_export_plans_pdf(attente_max=900):
    """Onglet Plans → Exporter vers PDF → Sélectionner tout → un seul fichier → Confirmer. Attend le PDF (taille stable)."""
    projet = load_state().get("projet")
    if not projet: raise RuntimeError("aucun projet ouvert connu (open_qpl d'abord)")
    target = f"{VM_DOCS}\\Mes plans PDF\\Fichiers exportés\\{projet}"
    vm_ps(f"Remove-Item -LiteralPath '{target}\\{projet}.pdf' -Force -ErrorAction SilentlyContinue; {KILL_VIEWERS}", 30)
    for essai in range(3):   # le 1er clic après la fermeture d'Edge ne fait parfois que redonner le focus à Plan Expert (constaté 2026-09-17)
        shot = shot_path(f"plans-export-dialogue-{essai + 1}")
        vnc("move 700 14 click 1 pause 1 " + click("onglet_plans", 2) + click("plans_export_pdf", 4), capture=shot)
        if _barre_export_visible(shot): break
    else:
        raise RuntimeError(f"barre « Confirmer l'exportation » non affichée après 3 essais (capture {shot})")
    vnc(click("plans_selectionner_tout", 2) + click("plans_confirmer", 3))
    t0 = time.time(); last = -1; stable = 0; found = None
    while time.time() - t0 < attente_max:
        time.sleep(10)
        fs = _vm_files(target, f"{projet}.pdf")
        if fs:
            if fs[0]["octets"] == last and last > 0: stable += 1
            else: stable = 0
            last = fs[0]["octets"]; found = fs[0]
            if stable >= 2: break
    vm_ps(KILL_VIEWERS, 30)
    if not found: raise RuntimeError(f"PDF des plans non produit après {attente_max} s ({target})")
    return {"projet": projet, "pdf_vm": found["chemin"], "octets": found["octets"], "duree_s": int(time.time() - t0), "capture_dialogue": shot}

def op_screenshot():
    shot = shot_path("ecran"); vnc("pause 0.5", capture=shot); return shot

def op_download(outbox_local, projet=None):
    """Rapports (Mes rapports\\<projet>*) + PDF des plans → \\\\host.lan\\Data\\sorties\\<projet>\\ → scp → outbox_local. Retourne fichiers + sha256."""
    projet = projet or load_state().get("projet")
    if not projet: raise RuntimeError("nom de projet inconnu")
    out, code = vm_ps(f"""$dst = '\\\\host.lan\\Data\\sorties\\{projet}'
New-Item -ItemType Directory -Force $dst | Out-Null
Get-ChildItem $dst -File | Remove-Item -Force
Get-ChildItem -LiteralPath '{VM_DOCS}\\Mes rapports' -File | Where-Object {{ ($_.Name -like '{projet}-Rapport-de-m*') -or ($_.Name -like '{projet}-M*[[]Class*') }} | Copy-Item -Destination $dst -Force
$p = '{VM_DOCS}\\Mes plans PDF\\Fichiers exportés\\{projet}\\{projet}.pdf'
if (Test-Path -LiteralPath $p) {{ Copy-Item -LiteralPath $p -Destination ($dst + '\\{projet}-Plans-natif-PlanExpert.pdf') -Force }}
Get-ChildItem $dst -File | ForEach-Object {{ $_.Name }}""", 300)
    os.makedirs(outbox_local, exist_ok=True)
    for f in os.listdir(outbox_local):
        if f != "resultat.json" and os.path.isfile(os.path.join(outbox_local, f)): os.remove(os.path.join(outbox_local, f))
    sh(["scp", "-q", "-r", f"mx:{SHARED}/sorties/{projet}/.", outbox_local + "/"], 600, check=True)
    files = {f: {"octets": os.path.getsize(os.path.join(outbox_local, f)), "sha256": sha256(os.path.join(outbox_local, f))}
             for f in sorted(os.listdir(outbox_local)) if os.path.isfile(os.path.join(outbox_local, f)) and f.startswith(projet)}
    return {"projet": projet, "dossier": outbox_local, "fichiers": files, "liste_vm": out.splitlines()}

def op_export_natif(pe_dir, outbox_dir):
    """Enchaînement complet pour le pipeline : upload → open → rapports → plans PDF → download. Retourne un dict (jamais d'exception : 'ok': False + erreur)."""
    r = {"ok": False, "etapes": {}}
    try:
        r["etapes"]["upload"] = op_upload_project(pe_dir)
        r["etapes"]["open"] = op_open_qpl()
        r["etapes"]["rapports"] = op_export_reports()
        r["etapes"]["plans_pdf"] = op_export_plans_pdf()
        r["etapes"]["download"] = op_download(os.path.join(outbox_dir, "export-natif-planexpert"))
        r["ok"] = all(r["etapes"]["rapports"]["exports"].get(k) for k in ("pdf", "xls", "xml")) and bool(r["etapes"]["download"]["fichiers"])
    except Exception as e:  # noqa
        r["erreur"] = f"{type(e).__name__}: {e}"
        try: r["capture_erreur"] = op_screenshot()
        except Exception: pass
    return r

# ---------------------------------------------------------------- serveur MCP
def build_server():
    srv = MCPServer("planexpert-vm", instructions="Pilote Plan Expert 3.0.17 dans la VM Windows (mxlinux). Un seul utilisateur à la fois : open_qpl ferme le projet en cours.")
    @srv.tool()
    def etat() -> dict:
        """État réel : mxlinux, conteneur, VM (SSH), processus Plan Expert, projet ouvert connu."""
        return op_etat()
    @srv.tool()
    def upload_project(dossier: str) -> dict:
        """Copie un dossier local (fichier .qpl + rasters PNG à côté) vers la VM (C:\\Projets\\<nom>) avec vérification sha256."""
        return op_upload_project(dossier)
    @srv.tool()
    def open_qpl(chemin: str = "") -> dict:
        """Ouvre un .qpl dans Plan Expert (chemin Windows dans la VM ; par défaut le dernier upload). Redémarre Plan Expert."""
        return op_open_qpl(chemin or None)
    @srv.tool()
    def export_reports(formats: list[str] = ["pdf", "xls", "xml"]) -> dict:
        """Rapports → Exporter vers PDF / Excel / XML du projet ouvert (fichiers dans Mes rapports de la VM)."""
        return op_export_reports(tuple(formats))
    @srv.tool()
    def export_plans_pdf() -> dict:
        """Plans → Exporter vers PDF (tous les plans, un seul fichier) ; attend la fin de l'écriture."""
        return op_export_plans_pdf()
    @srv.tool()
    def screenshot() -> Image:
        """Capture de l'écran de la VM (PNG 1280×800), aussi enregistrée sous work/captures/."""
        return Image(path=op_screenshot())
    @srv.tool()
    def download(outbox: str, projet: str = "") -> dict:
        """Rapatrie les exports natifs (rapports + PDF des plans) du projet vers un dossier local, avec sha256."""
        return op_download(outbox, projet or None)
    @srv.tool()
    def vnc_raw(actions: str) -> Image:
        """Actions vncdo brutes (ex. 'move 100 100 click 1 key esc'), puis capture. Clavier AZERTY : pas de chemins tapés."""
        shot = shot_path("raw"); vnc(actions, capture=shot); return Image(path=shot)
    return srv

def main():
    a = sys.argv[1:]
    if a and a[0] == "--cli":
        ops = {"etat": lambda: op_etat(), "upload": lambda: op_upload_project(a[2]), "open": lambda: op_open_qpl(a[2] if len(a) > 2 else None),
               "rapports": lambda: op_export_reports(), "plans": lambda: op_export_plans_pdf(), "shot": lambda: op_screenshot(),
               "download": lambda: op_download(a[2], a[3] if len(a) > 3 else None), "natif": lambda: op_export_natif(a[2], a[3])}
        print(json.dumps(ops[a[1]](), indent=1, ensure_ascii=False)); return
    build_server().run(transport="stdio")

if __name__ == "__main__":
    main()
