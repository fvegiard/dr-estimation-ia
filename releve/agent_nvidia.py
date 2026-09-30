# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Étape 2 (variante NVIDIA) : l'agent de relevé sur l'API NVIDIA (build.nvidia.com, point d'accès compatible OpenAI
`https://integrate.api.nvidia.com/v1/chat/completions`), avec la compétence `.claude/skills/releve-planexpert/SKILL.md`
comme consigne et des outils limités au dossier de travail. Bibliothèque standard seulement (aucune installation).

Clé : variable d'environnement NVIDIA_API_KEY (jamais journalisée ni écrite). Sous WSL, la transmettre au processus
seulement (WSLENV=NVIDIA_API_KEY/u), sans configuration globale.

Modèle par défaut : moonshotai/kimi-k3 — choisi le 2026-09-29 sur feuille complète (voir MODELE ci-dessous).
gemma-4-31b-it gagnait l'essai du 2026-09-26 sur un extrait RDC (12/12, 39-58 s), mais l'essai sur la
feuille entière l'a écarté : 53 marques sur 122 et toutes ses coordonnées posées sur une grille de 10 pt.
Un bon résultat sur une vignette ne prédit pas un relevé de feuille.

Usage : python releve/agent_nvidia.py WORKDIR RESULTAT_JSON [--model M] [--max-turns 200]
Écrit RESULTAT_JSON (mêmes champs que agent_sdk.py) et WORKDIR/agent-journal.log. Code 0 si subtype == success.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import glob
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "releve"))
from controle_qualite import (
    controler,
)

REFUS_QUALITE_MAX = 3       # refus de `terminer` pour qualité avant d'accepter en « qualite_insuffisante »
URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1") + "/chat/completions"
MODELE = "moonshotai/kimi-k3"
# Essai DSI01 (HR26-14, 122 marques chez l'estimateur), 2026-09-29, même consigne et mêmes outils :
#   kimi-k3          104 marques, rappel 63 %, 38 tours, 49 min — DT/K/F/RA quasi exacts
#   gemma-4-31b-it    53 marques, rappel 33 %, 36 tours, 31 min — 53/53 coordonnées sur une grille
#                     de 10 pt (positions inventées, bloquées par Q10)
#   glm-5.3-flash      0 marque en 71 min, 7 zooms — abandonné
#   nemotron-3-nano-omni  HTTP 503 ResourceExhausted (16/16) — limite de concurrence NVIDIA
# Aucun modèle n'atteint le seuil : kimi-k3 reste « qualite_insuffisante » au contrôle aveugle
# (20 erreurs, dont la confusion AVERTISSEUR FUMEE AUTONOME → DETECTEUR FUMEE qui coûte 36 marques).
SORTIES = {"feuilles-classement.csv", "nomenclature.csv", "occurrences-texte.csv", "occurrences-visuel.csv",
           "reserves.md", "rapport-releve.md", "comparaison-estimateur.md"}
SCRIPTS = {"zoom": "releve/zoom.py", "extract_occurrences": "releve/extract_occurrences.py", "traits": "releve/traits.py"}
IMAGES_GARDEES = 4          # images conservées dans l'historique (les plus anciennes sont remplacées par leur chemin)
MAX_TEXTE = 30000           # troncature d'un fichier texte renvoyé au modèle
FENETRE = 600               # côté max (pt) d'un zoom qui compte pour la couverture : essai réel 2026-09-26, 480×500 pt → 12/12
COUVERTURE_MIN = 0.95       # part de chaque feuille « plan » à parcourir en zooms fins avant `terminer`
ENTETE_VISUEL = "feuille,label,x_pt,y_pt,source,note"

OUTILS = [
    {"type": "function", "function": {"name": "lister", "description": "Liste les fichiers du dossier de travail qui correspondent au motif glob (relatif au dossier).",
     "parameters": {"type": "object", "properties": {"motif": {"type": "string"}}, "required": ["motif"]}}},
    {"type": "function", "function": {"name": "lire", "description": "Lit un fichier du dossier de travail. Un .png est renvoyé comme image à regarder ; le reste comme texte.",
     "parameters": {"type": "object", "properties": {"chemin": {"type": "string"}, "debut": {"type": "integer"}, "lignes": {"type": "integer"}}, "required": ["chemin"]}}},
    {"type": "function", "function": {"name": "ecrire", "description": "Écrit (remplace) un fichier de sortie du dossier de travail : " + ", ".join(sorted(SORTIES)) + ".",
     "parameters": {"type": "object", "properties": {"chemin": {"type": "string"}, "contenu": {"type": "string"}}, "required": ["chemin", "contenu"]}}},
    {"type": "function", "function": {"name": "zoom", "description": "Rend la zone x0 y0 x1 y1 (points PDF) d'une feuille avec règles et marques déjà relevées, puis la montre.",
     "parameters": {"type": "object", "properties": {"feuille": {"type": "string"}, "x0": {"type": "number"}, "y0": {"type": "number"}, "x1": {"type": "number"}, "y1": {"type": "number"}},
                    "required": ["feuille", "x0", "y0", "x1", "y1"]}}},
    {"type": "function", "function": {"name": "ajouter_occurrences", "description": "Ajoute des lignes CSV `feuille,label,x_pt,y_pt,source,note` (source=visuel) à occurrences-visuel.csv, après chaque zoom.",
     "parameters": {"type": "object", "properties": {"lignes": {"type": "array", "items": {"type": "string"}}}, "required": ["lignes"]}}},
    {"type": "function", "function": {"name": "couverture", "description": "Indique, pour chaque feuille plan, les fenêtres de ≤600 pt pas encore zoomées.",
     "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "extract_occurrences", "description": "Applique nomenclature.csv aux mots des feuilles → occurrences-texte.csv.",
     "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "traits", "description": "Nature vectorielle (texte, tracé, gris/noir) autour du point x y d'une feuille.",
     "parameters": {"type": "object", "properties": {"feuille": {"type": "string"}, "x": {"type": "number"}, "y": {"type": "number"}}, "required": ["feuille", "x", "y"]}}},
    {"type": "function", "function": {"name": "terminer", "description": "Termine le relevé avec le résumé final (10 lignes max).",
     "parameters": {"type": "object", "properties": {"resume": {"type": "string"}}, "required": ["resume"]}}},
]

def dans(workdir, chemin):
    """Chemin absolu sous workdir, sinon ValueError (aucun accès hors du dossier de travail)."""
    p = os.path.realpath(os.path.join(workdir, chemin))
    if os.path.commonpath([os.path.realpath(workdir), p]) != os.path.realpath(workdir):
        raise ValueError(f"hors du dossier de travail : {chemin}")
    return p

def image_msg(chemin_abs, rel):
    b = base64.b64encode(open(chemin_abs, "rb").read()).decode()
    return {"role": "user", "content": [{"type": "text", "text": f"Image : {rel}"},
                                          {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b}}]}

def script(workdir, nom, args):
    p = subprocess.run([sys.executable, os.path.join(REPO, SCRIPTS[nom]), workdir, *map(str, args)], cwd=REPO,
                       capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)
    return p.returncode, (p.stdout + ("\n" + p.stderr if p.returncode else "")).strip()[-4000:]

VUS = []                    # zooms fins réalisés : (feuille, x0, y0, x1, y1)

def feuilles_plan(workdir):
    import csv
    p = os.path.join(workdir, "feuilles-classement.csv")
    if not os.path.isfile(p):
        return []
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    tailles = {r["feuille"]: (float(r["largeur_pt"]), float(r["hauteur_pt"])) for r in csv.DictReader(open(os.path.join(workdir, "feuilles.csv"), encoding="utf-8"))}
    return [(r["feuille"].strip(), *tailles[r["feuille"].strip()]) for r in rows
            if (r.get("type") or r.get(" type") or "").strip() == "plan" and r["feuille"].strip() in tailles]

def manquantes(workdir):
    """Fenêtres (grille de FENETRE pt) non couvertes par un zoom fin, par feuille plan."""
    res = {}
    for f, W, H in feuilles_plan(workdir):
        cases = [(x, y) for x in range(0, int(W), FENETRE) for y in range(0, int(H), FENETRE)]
        def vue(x, y, f=f, W=W, H=H):
            cx, cy = x + min(FENETRE, W - x) / 2, y + min(FENETRE, H - y) / 2
            return any(v[0] == f and v[1] <= cx <= v[3] and v[2] <= cy <= v[4] for v in VUS)
        reste = [(x, y, min(x + FENETRE, W), min(y + FENETRE, H)) for x, y in cases if not vue(x, y)]
        if len(reste) > (1 - COUVERTURE_MIN) * len(cases):
            res[f] = reste
    return res

def outil(workdir, nom, a):
    """Exécute un outil ; retourne (texte, chemin_image_ou_None)."""
    if nom == "ajouter_occurrences":
        p = dans(workdir, "occurrences-visuel.csv")
        neuf = not os.path.isfile(p) or os.path.getsize(p) == 0
        lignes = [l.strip() for l in a.get("lignes", []) if l.strip() and not l.startswith("feuille,")]
        with open(p, "a", encoding="utf-8", newline="\n") as fh:
            if neuf:
                fh.write(ENTETE_VISUEL + "\n")
            fh.writelines(l + "\n" for l in lignes)
        return f"{len(lignes)} lignes ajoutées", None
    if nom == "couverture":
        m = manquantes(workdir)
        return ("couverture complète" if not m else json.dumps({f: [[round(v) for v in r] for r in rs] for f, rs in m.items()})), None
    if nom == "lister":
        fs = sorted(os.path.relpath(f, workdir) for f in glob.glob(dans(workdir, a.get("motif", "*")), recursive=True))
        return "\n".join(fs[:400]) + (f"\n… {len(fs) - 400} de plus" if len(fs) > 400 else "") or "(aucun)", None
    if nom == "lire":
        p = dans(workdir, a["chemin"])
        if p.lower().endswith(".png"):
            return f"image jointe : {a['chemin']}", p
        L = open(p, encoding="utf-8", errors="replace").read().splitlines()
        d = int(a.get("debut") or 0); n = int(a.get("lignes") or 2000)
        t = "\n".join(L[d:d + n])
        return (t[:MAX_TEXTE] + ("\n[tronqué]" if len(t) > MAX_TEXTE else "") + f"\n[{len(L)} lignes au total]"), None
    if nom == "ecrire":
        rel = os.path.normpath(a["chemin"])
        if rel not in SORTIES:
            return f"refusé : seuls {sorted(SORTIES)} sont modifiables", None
        open(dans(workdir, rel), "w", encoding="utf-8", newline="\n").write(a["contenu"])
        return f"écrit {rel} ({len(a['contenu'])} caractères)", None
    if nom == "zoom":
        c, out = script(workdir, "zoom", [a["feuille"], a["x0"], a["y0"], a["x1"], a["y1"]])
        png = out.strip().splitlines()[-1] if c == 0 and out.strip() else ""
        png = png if os.path.isabs(png) else os.path.join(workdir, png)
        if c == 0 and max(a["x1"] - a["x0"], a["y1"] - a["y0"]) <= FENETRE + 1:
            VUS.append((a["feuille"], a["x0"], a["y0"], a["x1"], a["y1"]))
        return (out, png) if c == 0 and os.path.isfile(png) else (f"échec zoom : {out}", None)
    if nom == "extract_occurrences":
        return script(workdir, "extract_occurrences", [])[1] or "fait", None
    if nom == "traits":
        return script(workdir, "traits", [a["feuille"], a["x"], a["y"]])[1], None
    return f"outil inconnu : {nom}", None

def appel(corps, cle, essais=5, j=None):
    """Appelle l'API. Journalise chaque reprise : sans cela, une attente longue est indiscernable d'un blocage."""
    for k in range(essais):
        req = urllib.request.Request(URL, data=json.dumps(corps).encode(), headers={
            "Authorization": "Bearer " + cle, "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as f:
                return json.load(f)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code not in (429, 500, 502, 503, 504) or k == essais - 1:
                raise RuntimeError(f"HTTP {e.code} : {msg}")
            if j:
                j(f"reprise {k + 1}/{essais - 1} après HTTP {e.code} : {msg[:120]}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if k == essais - 1:
                raise RuntimeError(f"réseau : {e}")
            if j:
                j(f"reprise {k + 1}/{essais - 1} après erreur réseau : {str(e)[:120]}")
        time.sleep(15 * (k + 1))

def alleger(messages):
    """Ne garde que les IMAGES_GARDEES dernières images (contexte borné)."""
    idx = [i for i, m in enumerate(messages) if m["role"] == "user" and isinstance(m["content"], list)
           and any(c.get("type") == "image_url" for c in m["content"])]
    for i in idx[:-IMAGES_GARDEES]:
        messages[i] = {"role": "user", "content": messages[i]["content"][0]["text"] + " (déjà vue, retirée du contexte)"}

def run(workdir, out_json, model, max_turns):
    cle = os.environ.get("NVIDIA_API_KEY")
    log = open(os.path.join(workdir, "agent-journal.log"), "a", encoding="utf-8")
    def j(msg):
        log.write(f"{datetime.datetime.now():%H:%M:%S} {msg}\n"); log.flush()
    t0 = time.time(); usage = {"input_tokens": 0, "output_tokens": 0}
    data = {"lanceur": f"agent_nvidia.py (API NVIDIA, {model})", "model": model}
    if not cle:
        data.update(subtype="clé NVIDIA_API_KEY absente du processus", is_error=True, num_turns=0)
        j("fin  " + data["subtype"]); json.dump(data, open(out_json, "w", encoding="utf-8"), indent=1, ensure_ascii=False); return 1
    skill = open(os.path.join(REPO, ".claude", "skills", "releve-planexpert", "SKILL.md"), encoding="utf-8").read()
    skill = skill.split("---", 2)[2].replace("$ARGUMENTS", ".")
    systeme = (skill + "\n\n## Outils de cette exécution (API NVIDIA)\nTu n'as pas de Bash : utilise les outils fournis "
               "(lister, lire, ecrire, zoom, extract_occurrences, traits). Les chemins sont relatifs au dossier de travail « . ». "
               "Lis une image avec `lire` (tuiles/…, apercus/…) ou `zoom`. Écris chaque sortie avec `ecrire` (contenu complet). "
               "Plans raster (0 mot) : tout se relève à l'œil. Parcours CHAQUE feuille plan en zooms de 600 pt × 600 pt au plus "
               "(grille x=0,600,1200… ; y=0,600,…), et après chaque zoom ajoute avec `ajouter_occurrences` une ligne par symbole vu "
               "(coordonnées lues sur les règles, repère écrit entre crochets dans la colonne note). Ne saute aucune fenêtre ; "
               "`couverture` liste celles qui restent. `terminer` est refusé tant que la couverture n'est pas complète "
               "et tant que le contrôle qualité (un libellé par appareil, repère cohérent avec le libellé, pas de doublon ni de trou "
               "de numérotation non justifié, chaque appareil de la nomenclature relevé ou mis en réserve) échoue.")
    messages = [{"role": "system", "content": systeme},
                {"role": "user", "content": "Relève le dossier de travail « . ». Commence par lire MANIFESTE.md."}]
    j(f"début  modèle={model} max_tours={max_turns} workdir={workdir}")
    resume, tours, refus_q = None, 0, 0
    try:
        while tours < max_turns and resume is None:
            tours += 1
            alleger(messages)
            r = appel({"model": model, "messages": messages, "tools": OUTILS, "tool_choice": "auto",
                       "max_tokens": 16000, "temperature": 0.2}, cle, j=j)
            u = r.get("usage") or {}
            usage["input_tokens"] += u.get("prompt_tokens", 0); usage["output_tokens"] += u.get("completion_tokens", 0)
            m = r["choices"][0]["message"]
            appels = m.get("tool_calls") or []
            messages.append({"role": "assistant", "content": m.get("content") or "", **({"tool_calls": appels} if appels else {})})
            if (m.get("content") or "").strip():
                j("texte " + m["content"].strip()[:200].replace("\n", " "))
            if not appels:
                messages.append({"role": "user", "content": "Continue avec les outils ; appelle `terminer` quand toutes les sorties sont écrites."})
                continue
            images = []
            for tc in appels:
                nom = tc["function"]["name"]
                try:
                    a = json.loads(tc["function"].get("arguments") or "{}")
                except json.JSONDecodeError:
                    a = {}
                j(f"outil {nom} {json.dumps({k: (v if k != 'contenu' else f'<{len(v)} car.>') for k, v in a.items()}, ensure_ascii=False)[:200]}")
                if nom == "terminer" and manquantes(workdir):
                    texte, img = ("refusé : feuille(s) plan pas entièrement parcourues en zooms de ≤600 pt. Fenêtres restantes "
                                  "(x0,y0,x1,y1) : " + json.dumps({f: [[round(v) for v in r] for r in rs] for f, rs in manquantes(workdir).items()})), None
                    j("contrôle couverture : terminer refusé")
                elif nom == "terminer" and refus_q < REFUS_QUALITE_MAX and not controler(workdir)["conforme"]:
                    refus_q += 1
                    q = controler(workdir)
                    texte, img = (f"refusé ({refus_q}/{REFUS_QUALITE_MAX}) : contrôle qualité bloquant. Corrige puis rappelle `terminer` :\n- "
                                  + "\n- ".join(q["erreurs"][:30])), None
                    j(f"contrôle qualité : terminer refusé ({len(q['erreurs'])} erreurs)")
                elif nom == "terminer":
                    resume = a.get("resume", ""); texte, img = "terminé", None
                else:
                    try:
                        texte, img = outil(workdir, nom, a)
                    except Exception as e:  # noqa — l'erreur est renvoyée au modèle
                        texte, img = f"erreur : {e}", None
                messages.append({"role": "tool", "tool_call_id": tc.get("id", nom), "content": texte})
                if img:
                    images.append((img, os.path.relpath(img, workdir)))
            for img, rel in images:
                messages.append(image_msg(img, rel))
    except Exception as e:  # noqa
        data.update(subtype=f"erreur API : {e}", is_error=True)
    manquants = [f for f in ("feuilles-classement.csv", "nomenclature.csv") if not os.path.isfile(os.path.join(workdir, f))]
    qualite = controler(workdir) if os.path.isfile(os.path.join(workdir, "feuilles-classement.csv")) else {"conforme": False, "erreurs": ["aucune sortie"]}
    data["qualite"] = {"conforme": qualite["conforme"], "erreurs": len(qualite["erreurs"]), "detail": "qualite.json"}
    if "subtype" not in data and resume is not None and not manquants and not qualite["conforme"]:
        data.update(subtype="qualite_insuffisante", is_error=True)
    if "subtype" not in data:
        ok = resume is not None and not manquants
        data.update(subtype="success" if ok else ("error_max_turns" if resume is None else "sorties manquantes : " + ", ".join(manquants)),
                    is_error=not ok)
    data.update(num_turns=tours, duration_ms=int((time.time() - t0) * 1000), total_cost_usd=None, usage=usage,
                result=resume or "")
    j(f"fin  subtype={data['subtype']} tours={tours} jetons={usage}")
    json.dump(data, open(out_json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: data.get(k) for k in ("subtype", "num_turns", "model")}, ensure_ascii=False))
    return 0 if data["subtype"] == "success" else 1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workdir"); ap.add_argument("out_json")
    ap.add_argument("--model", default=os.environ.get("RELEVE_NVIDIA_MODEL", MODELE))
    ap.add_argument("--max-turns", type=int, default=int(os.environ.get("RELEVE_MAX_TURNS", "200")))
    a = ap.parse_args()
    sys.exit(run(os.path.abspath(a.workdir), a.out_json, a.model, a.max_turns))

if __name__ == "__main__":
    main()
