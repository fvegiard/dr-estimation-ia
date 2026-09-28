# /// script
# requires-python = ">=3.12"
# ///
"""Lanceur unique du relevé automatique : « je donne un dossier, je reçois mon PDF ».

    uv run releve/run.py <nom-de-soumission | chemin-du-dossier>     traite un dossier
    uv run releve/run.py --watch                                      surveille les INBOX et traite les nouveaux dossiers
    uv run releve/run.py --reprendre <nom>                            rejoue seulement build_qpl + render_pdf (sans agent)

Dossiers (hors du dépôt, données de Francis) :
    D:\\claude\\releve-auto\\INBOX\\<nom>\\      dépôt des PDF (plans, addendas, relevé de l'estimateur)
    D:\\claude\\releve-auto\\OUTBOX\\<nom>\\     résultat : .qpl + rasters, Plans-annotes.pdf, Rapport-de-metre.pdf, STATUT.md
    G:\\My Drive\\AI\\Releves-auto\\INBOX|OUTBOX  miroir Google Drive (utilisé si G: est monté dans WSL)

Étapes : prepare.py (déterministe) → agent Claude Code en mode headless (`claude -p "/releve-planexpert …"`,
doc : docs/code.claude.com_docs_en_headless.md) → build_qpl.py → render_pdf.py → STATUT.md.
Un seul relevé à la fois (verrou). Journal : D:\\claude\\releve-auto\\journal.log
"""
from __future__ import annotations
import os, sys, json, time, shutil, subprocess, datetime, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("RELEVE_BASE", "/mnt/d/claude/releve-auto")
INBOX, OUTBOX = os.path.join(BASE, "INBOX"), os.path.join(BASE, "OUTBOX")
DRIVE = os.environ.get("RELEVE_DRIVE", "/mnt/g/My Drive/AI/Releves-auto")
LOCK = os.path.join(BASE, ".verrou")
LOG = os.path.join(BASE, "journal.log")
MODEL = os.environ.get("RELEVE_MODEL", "opus")
MAX_TURNS = os.environ.get("RELEVE_MAX_TURNS", "800")
WSL_EXE = "/mnt/c/Windows/System32/wsl.exe"
PLANEXPERT_VM_CLI = os.path.join(REPO, "mcp", "planexpert_vm", "server.py")

def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    os.makedirs(BASE, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def run(cmd, cwd=REPO, log_path=None, env=None):
    """Exécute une commande, journalise, retourne (code, stdout)."""
    log("$ " + " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                       env={**os.environ, **(env or {})})
    if log_path:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(f"\n### {' '.join(cmd)}\n--- stdout\n{p.stdout}\n--- stderr\n{p.stderr}\n")
    if p.returncode != 0:
        log(f"  -> code {p.returncode} ; stderr: {p.stderr.strip()[-800:]}")
    return p.returncode, p.stdout

def drive_mounted():
    if os.path.isdir(os.path.dirname(DRIVE)):          # G:\My Drive\AI monté → crée Releves-auto/{INBOX,OUTBOX} au besoin
        for d in ("INBOX", "OUTBOX"):
            os.makedirs(os.path.join(DRIVE, d), exist_ok=True)
        return True
    if os.path.exists(WSL_EXE) and DRIVE.startswith("/mnt/g/"):
        try:
            subprocess.run([WSL_EXE, "-d", "Ubuntu-26.04", "-u", "root", "--", "sh", "-c", "mkdir -p /mnt/g && (mountpoint -q /mnt/g || mount -t drvfs G: /mnt/g)"],
                           capture_output=True, timeout=60)
        except Exception:  # noqa
            pass
    return os.path.isdir(DRIVE)

def resolve_inbox(arg):
    """Nom ou chemin → (nom, dossier d'entrée local). Un dossier du miroir Drive est copié dans l'INBOX local."""
    if os.path.isdir(arg):
        return os.path.basename(os.path.normpath(arg)), os.path.abspath(arg)
    local = os.path.join(INBOX, arg)
    if os.path.isdir(local):
        return arg, local
    if drive_mounted() and os.path.isdir(os.path.join(DRIVE, "INBOX", arg)):
        shutil.copytree(os.path.join(DRIVE, "INBOX", arg), local, dirs_exist_ok=True)
        log(f"dossier copié depuis Drive : {arg}")
        return arg, local
    sys.exit(f"dossier introuvable : {arg} (ni chemin, ni {local}, ni Drive INBOX)")

def acquire_lock():
    if os.path.exists(LOCK):
        try:
            pid = int(open(LOCK).read().strip())
            os.kill(pid, 0)
            sys.exit(f"un relevé est déjà en cours (pid {pid}, verrou {LOCK})")
        except (ValueError, ProcessLookupError, PermissionError):
            pass
    open(LOCK, "w").write(str(os.getpid()))

def release_lock():
    try: os.remove(LOCK)
    except FileNotFoundError: pass

def agent(workdir, log_path):
    """Lance l'agent de relevé avec la compétence releve-planexpert (.claude/skills/releve-planexpert/SKILL.md).
    Par défaut : Claude Agent SDK (releve/agent_sdk.py, OAuth claude.ai). RELEVE_AGENT=cli : `claude -p` headless (repli)."""
    res_path = os.path.join(workdir, "agent-resultat.json")
    t0 = time.time()
    agent_env = {"RELEVE_TOOL_GUARD_ROOT": workdir}
    if os.environ.get("RELEVE_AGENT", "sdk") == "sdk":
        cmd = ["uv", "run", "releve/agent_sdk.py", workdir, res_path, "--model", MODEL, "--max-turns", MAX_TURNS]
        code, out = run(cmd, cwd=REPO, log_path=log_path, env=agent_env)
        try:
            res = json.load(open(res_path, encoding="utf-8"))
        except Exception:  # noqa
            res = {"result": out[-2000:], "is_error": True, "subtype": "agent_sdk sans résultat"}
    else:
        cmd = ["claude", "-p", f"/releve-planexpert {workdir}", "--output-format", "json", "--permission-mode", "acceptEdits",
               "--permission-prompts", "none",
               "--allowedTools", "Read,Write,Edit,Glob,Grep,Bash(uv run releve/zoom.py *),Bash(uv run releve/extract_occurrences.py *),Bash(uv run releve/traits.py *),Bash(head *),Bash(sort *),Bash(cut *),Bash(cat *)",
               "--add-dir", workdir, "--max-turns", MAX_TURNS, "--model", MODEL,
               "--mcp-config", '{"mcpServers":{}}', "--strict-mcp-config"]
        code, out = run(cmd, cwd=REPO, log_path=log_path, env=agent_env)
        try:
            data = json.loads(out)
            if isinstance(data, list):
                data = next((d for d in data if d.get("type") == "result"), data[-1] if data else {})
            res = data
        except json.JSONDecodeError:
            res = {"result": out[-2000:], "is_error": True, "subtype": "sortie non JSON"}
        json.dump(res, open(res_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    dur = time.time() - t0
    usage = res.get("usage", {}) or {}
    log(f"agent terminé en {dur / 60:.1f} min ; tours {res.get('num_turns')} ; coût estimé {res.get('total_cost_usd')} $ ; "
        f"entrée {usage.get('input_tokens')} + cache {usage.get('cache_read_input_tokens')} / sortie {usage.get('output_tokens')} ; subtype {res.get('subtype')}")
    return code, res, dur

def statut(name, inbox, outdir, workdir, steps, res, ok, err=None):
    L = [f"# STATUT — relevé automatique « {name} »", "", f"Date : {datetime.datetime.now():%Y-%m-%d %H:%M} · État : **{'TERMINÉ' if ok else 'ÉCHEC'}**"]
    if err: L += ["", f"Erreur : `{err}`"]
    L += ["", "## Entrées", "", "| fichier | octets | sha256 |", "|---|--:|---|"]
    for dp, _, fs in os.walk(inbox):
        for f in sorted(fs):
            p = os.path.join(dp, f); L.append(f"| {os.path.relpath(p, inbox)} | {os.path.getsize(p)} | {sha256(p)} |")
    L += ["", "## Sorties", "", "| fichier | octets | sha256 |", "|---|--:|---|"]
    for f in sorted(os.listdir(outdir)):
        p = os.path.join(outdir, f)
        if os.path.isfile(p) and not f.endswith(".png") and f != "STATUT.md" and not f.startswith("."):
            L.append(f"| {f} | {os.path.getsize(p)} | {sha256(p)} |")
    pe = os.path.join(outdir, f"{name}-planexpert", f"{name}.qpl")
    if os.path.exists(pe):
        L.append(f"| {name}-planexpert/{name}.qpl | {os.path.getsize(pe)} | {sha256(pe)} |")
    L += ["", f"Le projet Plan Expert `{name}.qpl` est dans `{name}-planexpert/` avec ses rasters PNG : copier le dossier entier, "
          "puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.", ""]
    natif = os.path.join(outdir, "export-natif-planexpert", "resultat.json")
    if os.path.exists(natif):
        n = json.load(open(natif, encoding="utf-8"))
        L += [f"**Export natif Plan Expert (VM mxlinux, MCP planexpert-vm) : {'oui' if n.get('ok') else 'non'}**"]
        if n.get("erreur"): L += [f"- erreur : `{n['erreur']}`" + (f" · capture `{n.get('capture_erreur')}`" if n.get("capture_erreur") else "")]
        for k, v in (n.get("etapes", {}).get("download", {}) or {}).get("fichiers", {}).items():
            L += [f"- `export-natif-planexpert/{k}` · {v['octets']} o · sha256 {v['sha256']}"]
        L += [""]
    else:
        L += ["**Export natif Plan Expert : non** (étape non exécutée)", ""]
    L += ["## Étapes", "", "| étape | durée | résultat |", "|---|--:|---|"] + [f"| {s} | {d / 60:.1f} min | {r} |" for s, d, r in steps]
    usage = (res or {}).get("usage", {}) or {}
    L += ["", f"## Agent de relevé — {(res or {}).get('lanceur') or 'claude -p (headless)'}", "", f"- modèle : `{MODEL}` · tours : {(res or {}).get('num_turns')} · sous-type : {(res or {}).get('subtype')}",
          f"- coût estimé (client, `total_cost_usd`) : {(res or {}).get('total_cost_usd')} $ US",
          f"- jetons : entrée {usage.get('input_tokens')}, cache créé {usage.get('cache_creation_input_tokens')}, cache lu {usage.get('cache_read_input_tokens')}, sortie {usage.get('output_tokens')}",
          f"- session : `{(res or {}).get('session_id')}` · dossier de travail : `{workdir}`", ""]
    if res and res.get("result"):
        L += ["### Résumé de l'agent", "", str(res["result"]).strip(), ""]
    for extra in ("reserves.md", "comparaison-estimateur.md"):
        p = os.path.join(workdir, extra)
        if os.path.exists(p):
            L += [f"## {extra}", "", open(p, encoding="utf-8").read(), ""]
    open(os.path.join(outdir, "STATUT.md"), "w", encoding="utf-8").write("\n".join(L))

def prepare_a_jour(inbox, workdir):
    """Vrai si inventaire.json du dossier de travail décrit exactement les fichiers actuels de l'INBOX (mêmes sha256)."""
    p = os.path.join(workdir, "inventaire.json")
    if not os.path.exists(p) or not os.path.exists(os.path.join(workdir, "feuilles.csv")):
        return False
    try:
        old = {e["fichier"]: e["sha256"] for e in json.load(open(p, encoding="utf-8"))["fichiers"]}
    except Exception:  # noqa
        return False
    now = {os.path.relpath(os.path.join(dp, f), inbox): sha256(os.path.join(dp, f)) for dp, _, fs in os.walk(inbox) for f in fs}
    return old == now

def process(arg, reprendre=False):
    name, inbox = resolve_inbox(arg)
    outdir = os.path.join(OUTBOX, name); workdir = os.path.join(outdir, "travail"); pe_dir = os.path.join(outdir, f"{name}-planexpert")
    os.makedirs(outdir, exist_ok=True)
    marker = os.path.join(outdir, ".en-cours"); open(marker, "w").write(str(os.getpid()))
    log_path = os.path.join(outdir, "journal-etapes.log")
    steps, res, ok, err = [], None, False, None
    T = time.time()
    try:
        if not reprendre:
            if prepare_a_jour(inbox, workdir):
                log("préparation déjà à jour (mêmes fichiers d'entrée), étape prepare sautée")
                steps.append(("prepare", 0, "déjà à jour"))
            else:
                t = time.time(); code, _ = run(["uv", "run", "releve/prepare.py", inbox, workdir], log_path=log_path)
                steps.append(("prepare", time.time() - t, "ok" if code == 0 else f"code {code}"))
                if code: raise RuntimeError("prepare.py a échoué")
            code, res, dur = agent(workdir, log_path)
            steps.append(("agent Claude", dur, f"{res.get('subtype')} / code {code}"))
            if code:
                raise RuntimeError(f"agent en échec (code {code}, subtype {res.get('subtype')})")
            for f in ("nomenclature.csv", "feuilles-classement.csv"):
                if not os.path.exists(os.path.join(workdir, f)):
                    raise RuntimeError(f"l'agent n'a pas produit {f}")
        t = time.time(); code, _ = run(["uv", "run", "releve/build_qpl.py", workdir, name, pe_dir], log_path=log_path)
        steps.append(("build_qpl", time.time() - t, "ok" if code == 0 else f"code {code}"))
        if code: raise RuntimeError("build_qpl.py a échoué")
        t = time.time(); code, _ = run(["uv", "run", "releve/render_pdf.py", workdir, name, outdir], log_path=log_path)
        steps.append(("render_pdf", time.time() - t, "ok" if code == 0 else f"code {code}"))
        if code: raise RuntimeError("render_pdf.py a échoué")
        ok = True
        if os.environ.get("RELEVE_NATIF", "1") == "1":     # export natif Plan Expert par la VM (MCP planexpert-vm) ; jamais bloquant
            if os.path.exists(PLANEXPERT_VM_CLI):
                t = time.time(); code, out = run(["uv", "run", PLANEXPERT_VM_CLI, "--cli", "natif", pe_dir, outdir], log_path=log_path)
                nat_dir = os.path.join(outdir, "export-natif-planexpert"); os.makedirs(nat_dir, exist_ok=True)
                try:
                    nat = json.loads(out)
                except json.JSONDecodeError:
                    nat = {"ok": False, "erreur": "sortie non JSON : " + out[-500:]}
                json.dump(nat, open(os.path.join(nat_dir, "resultat.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
                steps.append(("export natif Plan Expert", time.time() - t, "oui" if nat.get("ok") else f"non — {nat.get('erreur', '')[:120]}"))
            else:
                log(f"export natif ignoré : composant absent ({PLANEXPERT_VM_CLI})")
                steps.append(("export natif Plan Expert", 0, "ignoré — composant absent"))
    except Exception as e:  # noqa
        err = str(e); log("ÉCHEC : " + err)
    if reprendre and os.path.exists(os.path.join(workdir, "agent-resultat.json")):
        res = json.load(open(os.path.join(workdir, "agent-resultat.json"), encoding="utf-8"))
    steps.append(("total", time.time() - T, ""))
    statut(name, inbox, outdir, workdir, steps, res, ok, err)
    try: os.remove(marker)
    except FileNotFoundError: pass
    if drive_mounted():
        try:
            dst = os.path.join(DRIVE, "OUTBOX", name); os.makedirs(dst, exist_ok=True)
            for f in os.listdir(outdir):
                p = os.path.join(outdir, f)
                if os.path.isfile(p): shutil.copy2(p, dst)
            if os.path.isdir(pe_dir): shutil.copytree(pe_dir, os.path.join(dst, os.path.basename(pe_dir)), dirs_exist_ok=True)
            log(f"copié sur Drive : {dst}")
        except Exception as e:  # noqa
            log(f"copie Drive impossible : {e}")
    log(f"{'TERMINÉ' if ok else 'ÉCHEC'} {name} → {outdir}")
    return ok

def ready_dirs():
    """Dossiers INBOX (local + Drive) non traités et stables depuis 2 minutes."""
    roots = [INBOX] + ([os.path.join(DRIVE, "INBOX")] if drive_mounted() else [])
    out = []
    for root in roots:
        if not os.path.isdir(root): continue
        for n in sorted(os.listdir(root)):
            d = os.path.join(root, n)
            if not os.path.isdir(d) or n.startswith((".", "_")): continue
            if os.path.exists(os.path.join(OUTBOX, n, "STATUT.md")) or os.path.exists(os.path.join(OUTBOX, n, ".en-cours")): continue
            files = [os.path.join(dp, f) for dp, _, fs in os.walk(d) for f in fs]
            if not files: continue
            if time.time() - max(os.path.getmtime(f) for f in files) < 120: continue
            if n not in out: out.append(n)
    return out

def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    os.makedirs(INBOX, exist_ok=True); os.makedirs(OUTBOX, exist_ok=True)
    acquire_lock()
    try:
        if a[0] == "--watch":
            log("surveillance des INBOX (Ctrl-C pour arrêter)")
            while True:
                for n in ready_dirs():
                    process(n)
                time.sleep(60)
        elif a[0] == "--reprendre":
            process(a[1], reprendre=True)
        else:
            process(a[0])
    finally:
        release_lock()

if __name__ == "__main__":
    main()
