# /// script
# requires-python = ">=3.12"
# ///
"""Lanceur unique du relevé automatique : « je donne un dossier, je reçois mon PDF ».

    uv run releve/run.py <nom-de-soumission | chemin-du-dossier>     traite un dossier
    uv run releve/run.py --watch                                      surveille les INBOX et traite les nouveaux dossiers
    uv run releve/run.py --reprendre <nom>                            rejoue build_qpl + render_vectoriel + render_pdf (sans agent)

Dossiers (hors du dépôt, données de Francis) :
    D:\\claude\\releve-auto\\INBOX\\<nom>\\      dépôt des PDF (plans, addendas, relevé de l'estimateur)
    D:\\claude\\releve-auto\\OUTBOX\\<nom>\\     résultat : .qpl + rasters, Plans-annotes.pdf, Rapport-de-metre.pdf, STATUT.md
    G:\\My Drive\\AI\\Releves-auto\\INBOX|OUTBOX  miroir Google Drive (utilisé si G: est monté dans WSL)

Étapes : prepare.py (déterministe) → agent Claude Code en mode headless (`claude -p "/releve-planexpert …"`,
doc : docs/code.claude.com_docs_en_headless.md) → build_qpl.py → render_vectoriel.py → render_pdf.py →
boucle_acceptation (si `dossiers/<nom>/` est assemblé dans le dépôt : aveugle → gel → comparaison →
classement → justifications → ACCEPTATION.md ; jamais bloquante — VÉRIFICATION INCOMPLÈTE si la
référence de l'estimateur est absente) → STATUT.md.
Un seul relevé à la fois (verrou). Journal : D:\\claude\\releve-auto\\journal.log
"""
from __future__ import annotations
import os, sys, json, time, shutil, subprocess, datetime, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_WIN = os.name == "nt"   # poste Windows natif (hors WSL) : mêmes dossiers, chemins D:\ et G:\ au lieu de /mnt/d et /mnt/g
BASE = os.environ.get("RELEVE_BASE", r"D:\claude\releve-auto" if _WIN else "/mnt/d/claude/releve-auto")
INBOX, OUTBOX = os.path.join(BASE, "INBOX"), os.path.join(BASE, "OUTBOX")
DRIVE = os.environ.get("RELEVE_DRIVE", r"G:\My Drive\AI\Releves-auto" if _WIN else "/mnt/g/My Drive/AI/Releves-auto")
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
    """Exécute une commande, journalise, retourne (code, stdout).

    Les étapes Python écrivent en UTF-8 (PYTHONIOENCODING) et leur sortie est décodée en UTF-8 : avec
    l'encodage local (cp1252 sous Windows), « GEL VIOLÉ » arrivait illisible et une « → » faisait planter la
    boucle d'acceptation, dont le verdict était alors perdu (« non déterminé »)."""
    log("$ " + " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace",
                       stdin=subprocess.DEVNULL, env={**os.environ, "PYTHONIOENCODING": "utf-8", **(env or {})})
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

def processus_vivant(pid):
    """Vrai si le processus `pid` tourne encore. Sous Windows, `os.kill(pid, 0)` n'est pas un test : il appelle
    TerminateProcess (ou lève WinError 87) ; on interroge donc le noyau (OpenProcess + GetExitCodeProcess)."""
    if os.name == "nt":
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(0x1000, False, pid)        # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        try:
            code = ctypes.c_ulong()
            return bool(k32.GetExitCodeProcess(h, ctypes.byref(code))) and code.value == 259   # STILL_ACTIVE
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True

def acquire_lock():
    if os.path.exists(LOCK):
        try:
            pid = int(open(LOCK).read().strip())
        except ValueError:
            pid = None
        if pid and processus_vivant(pid):
            sys.exit(f"un relevé est déjà en cours (pid {pid}, verrou {LOCK})")
    open(LOCK, "w").write(str(os.getpid()))

def release_lock():
    try: os.remove(LOCK)
    except FileNotFoundError: pass

def agent(workdir, log_path):
    """Lance l'agent de relevé avec la compétence releve-planexpert (.claude/skills/releve-planexpert/SKILL.md).
    Par défaut : Claude Agent SDK (releve/agent_sdk.py, OAuth claude.ai). RELEVE_AGENT=nvidia : API NVIDIA (releve/agent_nvidia.py). RELEVE_AGENT=cli : `claude -p` headless (repli)."""
    res_path = os.path.join(workdir, "agent-resultat.json")
    t0 = time.time()
    agent_env = {"RELEVE_TOOL_GUARD_ROOT": workdir}
    if os.environ.get("RELEVE_AGENT", "sdk") in ("nvidia", "gemini"):
        os.environ.setdefault("RELEVE_FOURNISSEUR", os.environ["RELEVE_AGENT"])
        # Clé NVIDIA_API_KEY héritée du processus ; sous WSL : WSLENV=NVIDIA_API_KEY/u au lancement (jamais journalisée).
        cmd = [sys.executable, "releve/agent_nvidia.py", workdir, res_path, "--max-turns", MAX_TURNS]
        code, out = run(cmd, cwd=REPO, log_path=log_path, env=agent_env)
        try:
            res = json.load(open(res_path, encoding="utf-8"))
        except Exception:  # noqa
            res = {"result": out[-2000:], "is_error": True, "subtype": "agent_nvidia sans résultat"}
    elif os.environ.get("RELEVE_AGENT", "sdk") == "sdk":
        cmd = ["uv", "run", "releve/agent_sdk.py", workdir, res_path, "--model", MODEL, "--max-turns", MAX_TURNS]
        code, out = run(cmd, cwd=REPO, log_path=log_path, env=agent_env)
        try:
            res = json.load(open(res_path, encoding="utf-8"))
        except Exception:  # noqa
            res = {"result": out[-2000:], "is_error": True, "subtype": "agent_sdk sans résultat"}
    else:
        cmd = ["claude", "-p", f"/releve-planexpert {workdir}", "--output-format", "json", "--permission-mode", "acceptEdits",
               "--permission-prompts", "none",
               "--allowedTools", "Read,Write,Edit,Glob,Grep,Bash(uv run releve/zoom.py *),Bash(uv run releve/extract_occurrences.py *),Bash(uv run releve/traits.py *),Bash(uv run releve/controle_qualite.py *),Bash(head *),Bash(sort *),Bash(cut *),Bash(cat *)",
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

def statut(name, inbox, outdir, workdir, steps, res, ok, err=None, a_verifier=None, *, acceptation=None):
    a_verifier = a_verifier or []
    n_raster = raster_ouverts(workdir) if ok else 0
    etat = "ÉCHEC" if not ok else ("TERMINÉ — À VÉRIFIER" if (a_verifier or n_raster) else "TERMINÉ")
    if ok and acceptation:     # boucle d'acceptation exécutée : l'état intègre son verdict
        if "INVALIDE" in acceptation:
            etat = "TERMINÉ — ACCEPTATION INVALIDE"
        elif not acceptation.startswith("PRÊT POUR DÉCISION FRANCIS") \
                and not acceptation.startswith("non exécutée"):
            # VÉRIFICATION INCOMPLÈTE (référence absente) ou JUSTIFICATIONS
            # REQUISES (désaccords non tranchés) : le relevé reste à vérifier
            etat = "TERMINÉ — À VÉRIFIER"
    L = [f"# STATUT — relevé automatique « {name} »", "", f"Date : {datetime.datetime.now():%Y-%m-%d %H:%M} · État : **{etat}**"]
    if err: L += ["", f"Erreur : `{err}`"]
    if n_raster:
        L += ["", f"⚠️ **{n_raster} constat(s) des contrôles raster à trancher au zoom** (symboles non retrouvés, pastilles hors "
              "seuil d'alignement, familles suspectes — détail §Contrôles raster) avant de considérer ce livrable terminé."]
    if a_verifier:
        L += ["", f"⚠️ **Encadré RELEVE-MATERIEL hors de l'espace libre du plan sur : {', '.join(a_verifier)}** "
              f"(voir `{name}-rendu-rapport.json`) — vérifier visuellement (Read du PDF, zoome) avant de "
              "considérer ce livrable terminé ou de le diffuser au client, conformément à l'auto-supervision (CLAUDE.md)."]
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
          "puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » (pastilles vectorielles, calques OCG, bordereau) est rendu par "
          "`releve/render_vectoriel.py` à partir des mêmes CSV ; le rapport de métré ci-dessus par `releve/render_pdf.py`.", ""]
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
    cr = controles_raster(workdir, outdir)
    if cr:
        L += ["## Contrôles raster (ancrage, légende, planches)", ""] + cr + [""]
    L += ["## Étapes", "", "| étape | durée | résultat |", "|---|--:|---|"] + [f"| {s} | {d / 60:.1f} min | {r} |" for s, d, r in steps]
    if acceptation:
        L += ["", f"**Boucle d'acceptation : {acceptation}** — verdict détaillé dans "
              f"`dossiers/{name}/ACCEPTATION.md` (aveugle → gel → comparaison → classement → "
              "justifications ; un INVALIDE est cohérent avec le critère d'acceptation, il est "
              "consigné, jamais réduit au silence)."]
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

def planches_et_png(outdir, workdir, annote, estimate, rapport_path, steps, log_path):
    """Planches de contrôle (vignettes ×8 avec mesures) + livrables PNG (annoté + calque) — un échec est FATAL :
    sans planche, pas de contrôle visuel, donc jamais « TERMINÉ » (revues Codex/Copilot PR #25)."""
    # Pages RÉELLES de chaque feuille dans « Plans annotés » (`plan_page` du rapport de rendu : les bordereaux insérés
    # après chaque plan décalent tout dès la 2e feuille — les `page` d'estimate.json sont celles d'avant rendu).
    pages = [(sh["sheet"], int(sh["plan_page"])) for sh in json.load(open(rapport_path, encoding="utf-8")).get("sheets", [])]
    for sous in ("controle", "png"):                     # --reprendre : jamais une planche ou un PNG d'une feuille disparue
        shutil.rmtree(os.path.join(outdir, sous), ignore_errors=True)
    t = time.time(); code, out = run(["uv", "run", "releve/planche_controle.py", annote, estimate, os.path.join(outdir, "controle"),
                                      "--mesures", os.path.join(workdir, "occurrences-visuel.csv"), "--rapport", rapport_path], log_path=log_path)
    steps.append(("planche_controle", time.time() - t, (out.strip().splitlines() or ["?"])[-1][:160]))
    if code: raise RuntimeError("planche_controle.py a échoué (planches de contrôle visuel obligatoires avant « fait »)")
    # Livrables PNG (règle de Francis : plan annoté + calque transparent, pas de PDF à relire) : une paire par feuille plan
    t = time.time()
    for nom_f, pg in pages:
        code, _ = run(["uv", "run", "releve/calque_png.py", annote, os.path.join(outdir, "png"), "--page", str(pg), "--nom", str(nom_f)], log_path=log_path)
        if code: raise RuntimeError(f"calque_png.py a échoué sur la feuille {nom_f} (page {pg})")
    steps.append(("calque_png", time.time() - t, f"{len(pages)} feuille(s) → png/"))

def feuilles_raster(workdir):
    """Feuilles sans couche texte (scan, PNG) selon `feuilles.csv` de prepare.py : `nb_mots` = 0 ou classement `scan`."""
    p = os.path.join(workdir, "feuilles.csv")
    if not os.path.exists(p):
        return []
    import csv
    return [r["feuille"] for r in csv.DictReader(open(p, encoding="utf-8"))
            if (r.get("nb_mots") or "0").strip() in ("", "0") or (r.get("classement_fichier") or "") == "scan"]

def raster_ouverts(workdir):
    """Nombre de constats raster à trancher au zoom avant « fait » : symboles non retrouvés, pastilles hors seuil
    d'alignement, familles suspectes (revue Codex PR #25 : ils doivent mettre le dossier À VÉRIFIER, jamais TERMINÉ)."""
    n = 0
    p = os.path.join(workdir, "ancrage-raster.json")
    if os.path.exists(p):
        a = json.load(open(p, encoding="utf-8"))
        n += len(a.get("non_ancres", [])) + len((a.get("alignement") or {}).get("hors_seuil", []))
    p = os.path.join(workdir, "comparaison-legende.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8"))
        # comparaison incomplète = contrôle de famille non fait : à vérifier aussi (non exécutée, numéros de légende
        # ambigus, occurrences sans taille, glyphe attendu non reconnu)
        n += len(c.get("suspectes", [])) + int(bool(c.get("non_executee"))) + int(c.get("ambigues") or 0) + int(c.get("sans_taille") or 0)
        n += sum(int(v.get("non_reconnues") or 0) for v in (c.get("par_famille") or {}).values())
    return n

def controles_raster(workdir, outdir):
    """Lignes STATUT.md issues des correctifs raster : symboles non retrouvés, familles suspectes, planches de contrôle."""
    L = []
    p = os.path.join(workdir, "ancrage-raster.json")
    if os.path.exists(p):
        a = json.load(open(p, encoding="utf-8"))
        al = a.get("alignement") or {}
        if al:
            L.append(f"- alignement empirique : {al.get('mesures')} pastilles mesurées, écart moyen contour → encre {al.get('ecart_moyen_pt')} pt, "
                     f"{len(al.get('hors_seuil', []))} hors seuil (e > {al.get('seuil_ecart_pt')} pt ou couverture < {al.get('seuil_couverture')}) : "
                     + ", ".join(f"{h['label']} ({h['x_pt']},{h['y_pt']}) e={h['ecart_pt']} c={h['couverture']}" for h in al.get("hors_seuil", [])[:12]))
        L.append(f"- ancrage raster : {a.get('ancres', 0)} pastilles recalées sur leur symbole (déplacement max {a.get('deplacement_max_pt')} pt), "
                 f"{len(a.get('non_ancres', []))} non retrouvées (gardées aux coordonnées de l'agent — à vérifier au zoom) : "
                 + ", ".join(f"{n['label']} ({n['x_pt']},{n['y_pt']})" for n in a.get("non_ancres", [])[:12]))
    p = os.path.join(workdir, "comparaison-legende.json")
    if os.path.exists(p):
        c = json.load(open(p, encoding="utf-8"))
        if c.get("non_executee"):
            L.append(f"- comparaison à la légende : non exécutée — {c.get('raison', '')}")
            c = {}
        else:
            L.append(f"- comparaison à la légende : {c.get('occurrences', 0)} symboles comparés, {len(c.get('suspectes', []))} famille(s) suspecte(s)")
        for s in c.get("suspectes", []):
            L.append(f"  - ⚠️ {s['label']} ({s['x_pt']},{s['y_pt']}) ressemble plus à la ligne {s['meilleur']} « {s['description']} » "
                     f"({s['score_meilleur']}) qu'à la sienne {s['attendu']} ({s['score_attendu']}) — trancher au zoom, corriger TOUTES les occurrences semblables")
    ctrl = os.path.join(outdir, "controle")
    if os.path.isdir(ctrl):
        n = len([f for f in os.listdir(ctrl) if f.endswith(".png")])
        L.append(f"- planches de contrôle : {n} PNG dans `controle/` (une vignette ×8 par pastille) — à OUVRIR et relire avant « fait »")
    return L

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
    steps, res, ok, err, a_verifier, acceptation = [], None, False, None, [], None
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
            # Feuilles RASTER (scan / PNG : 0 mot extrait) — correctifs du 2026-10-15 (TEST-E201, vérificateur indépendant) :
            # 1) ancrage_raster.py recale chaque pastille sur le cercle (Hough) ou le rectangle minimal (minAreaRect) du
            #    symbole et mesure son rayon → plus de pastille décalée ni 2× trop grosse ;
            # 2) comparer_legende.py corrèle chaque symbole aux glyphes de sa section de légende → une famille attribuée
            #    au mauvais glyphe (A03 avertisseur vs A04 détecteur de fumée) est signalée AVANT le rendu.
            # Jamais bloquants : les symboles non retrouvés et les familles suspectes vont dans STATUT.md, à vérifier au zoom.
            raster = feuilles_raster(workdir)
            if not raster:                                   # entrée redevenue vectorielle : aucun constat raster périmé
                for f_ in ("ancrage-raster.json", "comparaison-legende.json"):
                    try: os.remove(os.path.join(workdir, f_))
                    except FileNotFoundError: pass
            if raster:
                # seulement les feuilles raster : dans un dossier mixte, les occurrences des feuilles vectorielles restent
                # à l'ancrage vectoriel de render_vectoriel.py (revues Codex/Copilot PR #25)
                t = time.time(); code, out = run(["uv", "run", "releve/ancrage_raster.py", workdir, "--feuilles", *raster], log_path=log_path)
                steps.append(("ancrage_raster", time.time() - t, (out.strip().splitlines() or ["?"])[-1][:160]))
                if code: raise RuntimeError("ancrage_raster.py a échoué (exécution) — symboles non retrouvés et hors seuil ne sont pas des échecs, un plantage oui")
                t = time.time(); code, out = run(["uv", "run", "releve/comparer_legende.py", workdir, "--feuilles", *raster], log_path=log_path)
                steps.append(("comparer_legende", time.time() - t, (out.strip().splitlines() or ["?"])[0][:160]))
                if code: raise RuntimeError("comparer_legende.py a échoué (exécution)")
            # contrôle qualité à l'aveugle (Q1-Q14) : non bloquant ici, mais journalisé et repris dans STATUT.md
            t = time.time(); code, out = run(["uv", "run", "releve/controle_qualite.py", workdir], log_path=log_path)
            steps.append(("controle_qualite", time.time() - t, (out.strip().splitlines() or ["?"])[0][:160]))
        t = time.time(); code, _ = run(["uv", "run", "releve/build_qpl.py", workdir, name, pe_dir], log_path=log_path)
        steps.append(("build_qpl", time.time() - t, "ok" if code == 0 else f"code {code}"))
        if code: raise RuntimeError("build_qpl.py a échoué")
        t = time.time(); code, _ = run(["uv", "run", "releve/render_vectoriel.py", workdir, name, outdir], log_path=log_path)
        steps.append(("render_vectoriel", time.time() - t, "ok" if code == 0 else f"code {code}"))
        if code: raise RuntimeError("render_vectoriel.py a échoué (PDF « Plans annotés » vectoriel)")
        rapport_path = os.path.join(outdir, f"{name}-rendu-rapport.json")
        if os.path.exists(rapport_path):
            a_verifier = json.load(open(rapport_path, encoding="utf-8")).get("conformite", {}).get("encadre_hors_espace_libre") or []
        t = time.time(); code, _ = run(["uv", "run", "releve/render_pdf.py", workdir, name, outdir], log_path=log_path)
        steps.append(("render_pdf", time.time() - t, "ok" if code == 0 else f"code {code}"))
        if code: raise RuntimeError("render_pdf.py a échoué")
        # Planche de contrôle : une vignette ×8 par pastille (CLAUDE.md §Autonomie point 1 — c'est à cette échelle
        # qu'un décalage de 5 pt ou une mauvaise famille se voit ; jamais sur la vue d'ensemble). À relire avant « fait ».
        annote = os.path.join(outdir, f"{name}-Plans-annotes.pdf"); estimate = os.path.join(outdir, "vecteur", "estimate.json")
        if os.path.exists(annote) and os.path.exists(estimate) and os.path.exists(rapport_path):
            planches_et_png(outdir, workdir, annote, estimate, rapport_path, steps, log_path)
        else:
            steps.append(("planche_controle", 0, "non exécutée : Plans-annotes.pdf, vecteur/estimate.json ou le rapport de rendu manque"))
        ok = True
        # Boucle d'acceptation (critère d'acceptation, étapes 1 à 8) : lancée
        # seulement si le dossier de la soumission est déjà assemblé dans le
        # dépôt (dossiers/<name> existe — il contient au moins l'emplacement
        # reference/ de l'estimateur). JAMAIS bloquante : VÉRIFICATION INCOMPLÈTE si la référence
        # est absente ; INVALIDE (« gel violé », relevé non aveugle) est
        # consigné dans STATUT.md et ACCEPTATION.md, jamais réduit au silence.
        dossier_dir = os.path.join(REPO, "dossiers", name)
        if os.path.isdir(dossier_dir):
            t = time.time()
            code_b, out_b = run(["uv", "run", "python", "-m", "src.validation.boucle_acceptation",
                                 name, "--workdir", workdir, "--dossier", dossier_dir],
                                log_path=log_path)
            verdict = ""
            for ligne in (out_b or "").splitlines():
                if ligne.startswith("VERDICT : "):
                    verdict = ligne[len("VERDICT : "):].strip()
            if not verdict:
                verdict = f"non déterminé (code {code_b})"
            acceptation = verdict
            steps.append(("boucle_acceptation", time.time() - t, f"code {code_b} — {verdict}"))
            log(f"boucle_acceptation {name} : code {code_b}, verdict {verdict}")
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
    # Appel identique à l'ancien comportement tant que la boucle d'acceptation
    # n'a pas tourné (dossiers/<name> absent) ; sinon le verdict voyage.
    kwargs = {"acceptation": acceptation} if acceptation else {}
    statut(name, inbox, outdir, workdir, steps, res, ok, err, a_verifier, **kwargs)
    try: os.remove(marker)
    except FileNotFoundError: pass
    if drive_mounted():
        try:
            dst = os.path.join(DRIVE, "OUTBOX", name); os.makedirs(dst, exist_ok=True)
            for f in os.listdir(outdir):
                p = os.path.join(outdir, f)
                if os.path.isfile(p): shutil.copy2(p, dst)
            if os.path.isdir(pe_dir): shutil.copytree(pe_dir, os.path.join(dst, os.path.basename(pe_dir)), dirs_exist_ok=True)
            for sous in ("png", "controle"):                 # livrables PNG et planches de contrôle (revue Codex PR #25)
                shutil.rmtree(os.path.join(dst, sous), ignore_errors=True)        # miroir : pas de fichier périmé
                if os.path.isdir(os.path.join(outdir, sous)):
                    shutil.copytree(os.path.join(outdir, sous), os.path.join(dst, sous), dirs_exist_ok=True)
            log(f"copié sur Drive : {dst}")
        except Exception as e:  # noqa
            log(f"copie Drive impossible : {e}")
    etat = "ÉCHEC" if not ok else ("TERMINÉ — À VÉRIFIER" if (a_verifier or raster_ouverts(workdir)) else "TERMINÉ")
    log(f"{etat} {name} → {outdir}")
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
