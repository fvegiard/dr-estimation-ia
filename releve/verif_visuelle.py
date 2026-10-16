# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "pillow>=10", "numpy>=1.24", "scipy>=1.11"]
# ///
"""Étape 4b (vision NVIDIA, corrective) : chaque pastille du PDF « Plans annotés » est jugée par un modèle de
vision (API NVIDIA build.nvidia.com, point d'accès compatible OpenAI) AVANT la révision finale par Claude :
« la pastille entoure-t-elle un symbole d'appareil, ou est-elle tombée sur un texte, une ligne, du vide ? »

Une pastille jugée hors symbole est CORRIGÉE sans rien inventer : les candidats sont les formes vectorielles
fermées du plan (`src/estimer/render/ancrage.py::SymbolIndex`, les mêmes que l'ancrage de l'étape 4a) dans la
direction indiquée par le modèle ; chaque candidat est montré au modèle avec la pastille déplacée dessus et le
premier accepté devient la nouvelle position (x, y, rayon). Sans candidat accepté, la marque reste où elle est
avec la réserve `*` (drapeau `revalider`) et sa note : c'est Claude (révision finale) ou Francis qui tranche.

Un verdict négatif isolé ne suffit pas : il est confirmé par un second jugement sur une fenêtre plus serrée
(gemma-4-31b-it a donné 1 faux négatif sur 10 marques de TEST-E103 le 2026-10-16 ; 0 faux positif sur 3
négatifs synthétiques — texte seul, vide, câble). nemotron-3-nano-omni acceptait 2 négatifs sur 3 : écarté.
Preuves réelles (TEST-E103, 2026-10-16) : 24/24 pastilles jugées sur leur symbole ; une pastille déplacée
volontairement sur son étiquette « Type P1 / P2 » est détectée aux deux jugements et ramenée sur le boîtier DP1
(écart final 0 pt) ; une pastille posée sur le cadre d'étiquette « NPP16 » n'est rejetée que depuis que la consigne
exclut explicitement les cadres d'étiquette (les boîtiers DP1/DP2 restent acceptés).

Entrées (SORTIE_DIR = dossier OUTBOX/<NOM>) : <NOM>-Plans-annotes.pdf, <NOM>-rendu-rapport.json,
vecteur/estimate.json, vecteur/plans.pdf. Sorties : <NOM>-verification-visuelle.json et .md (score, verdicts,
corrections, réserves), verification-visuelle/<feuille>-<repere>.png (les extraits jugés, pour la relecture),
et — s'il y a eu une correction ou une réserve — vecteur/estimate.json mis à jour et le PDF re-rendu.

Clé : variable d'environnement NVIDIA_API_KEY (jamais journalisée ni écrite ; absente → « non exécutée »,
code 4). Modèle : RELEVE_VISION_MODEL (défaut google/gemma-4-31b-it). Codes : 0 toutes les marques OK ou
corrigées ; 2 au moins une réserve `*` ; 4 non exécutée.

Usage : uv run releve/verif_visuelle.py SORTIE_DIR NOM [--model M] [--fenetre 120] [--max-marques N]
                                        [--parallele 2] [--sans-correction] [--dry-run]
"""
from __future__ import annotations

import argparse
import base64
import datetime
import io
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.estimer.render import load_input, render  # noqa: E402
from src.estimer.render.ancrage import SymbolIndex, _is_grey  # noqa: E402

URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1") + "/chat/completions"
MODELE = "google/gemma-4-31b-it"
REVALIDER = "revalider"          # même drapeau que src/estimer/render/from_releve.py (étiquette « * »)
FENETRE = 120.0                  # côté (pt) de l'extrait jugé, centré sur la marque
FENETRE_CONFIRMATION = 80.0      # fenêtre plus serrée du second jugement d'un verdict négatif
ZOOM = 7.0                       # px par pt (120 pt → 840 px)
RAYON_CANDIDATS = 50.0           # distance max (pt) d'un symbole candidat à la correction
MAX_CANDIDATS = 3
CONFIANCE_MIN = 0.6
PARALLELE = 2                    # requêtes simultanées (NVIDIA plafonne à 16 par compte, 503 au-delà)
VERSION_PROMPT = "2026-10-16"

PROMPT = (
    "Extrait d'un plan électrique ({fenetre:.0f} x {fenetre:.0f} points PDF). Au CENTRE exact de l'image, une "
    "pastille colorée (cercle pastel, contour sombre) a été dessinée par-dessus le plan pour marquer un appareil. "
    "Un appareil est un petit symbole vectoriel fermé (carré, cercle, rectangle, triangle, boîtier avec des lettres "
    "à l'intérieur comme DP1/DP2). Un texte seul (étiquette, cote, nom), une ligne, un câble ou un espace vide ne "
    "sont PAS un appareil. Attention : un cadre rectangulaire qui ne sert qu'à encadrer une étiquette de texte (un "
    "nom de type, un code de plusieurs caractères, une note) n'est pas un appareil non plus ; le symbole d'appareil "
    "est le petit carré ou cercle compact posé sur le tracé, à côté duquel les étiquettes sont écrites. "
    "Réponds UNIQUEMENT par un JSON : {{\"pastille_visible\": bool, \"sur_symbole\": bool "
    "(la pastille est centrée sur un symbole d'appareil), \"symbole_decrit\": str (ce qu'il y a sous la pastille, "
    "8 mots max), \"symbole_proche\": str (si sur_symbole est false : l'appareil le plus proche, sa direction depuis "
    "le centre (haut/bas/gauche/droite) et sa distance approximative en points ; sinon \"\"), \"confiance\": 0-1}}"
)

DIRECTIONS = {"haut": (0, -1), "bas": (0, 1), "gauche": (-1, 0), "droite": (1, 0),
              "nord": (0, -1), "sud": (0, 1), "ouest": (-1, 0), "est": (1, 0)}


# ----------------------------------------------------------------------------------------------- API NVIDIA
def appel(corps, cle, essais=5, j=None):
    """Appelle l'API ; reprises journalisées sur 429/5xx (une attente longue doit rester discernable d'un blocage)."""
    for k in range(essais):
        req = urllib.request.Request(URL, data=json.dumps(corps).encode(), headers={
            "Authorization": "Bearer " + cle, "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as f:
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
        time.sleep(10 * (k + 1))


def extraire_json(texte: str) -> dict:
    """Le JSON de la réponse, même entouré d'une clôture ```json ou de prose."""
    t = (texte or "").strip()
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        raise ValueError(f"réponse sans JSON : {t[:120]!r}")
    return json.loads(m.group(0))


def juger(png_bytes: bytes, modele: str, cle: str, fenetre: float, j=None) -> dict:
    """Verdict du modèle sur un extrait : dict normalisé (sur_symbole, pastille_visible, symbole_decrit,
    symbole_proche, confiance, brut)."""
    b = base64.b64encode(png_bytes).decode()
    corps = {"model": modele, "max_tokens": 400, "temperature": 0,
             "messages": [{"role": "user", "content": [
                 {"type": "text", "text": PROMPT.format(fenetre=fenetre)},
                 {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b}}]}]}
    r = appel(corps, cle, j=j)
    contenu = (r.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    d = extraire_json(contenu)
    conf = d.get("confiance")
    try:
        conf = float(conf)
    except (TypeError, ValueError):
        conf = 0.0
    return {"sur_symbole": bool(d.get("sur_symbole")), "pastille_visible": bool(d.get("pastille_visible", True)),
            "symbole_decrit": str(d.get("symbole_decrit") or "")[:120],
            "symbole_proche": str(d.get("symbole_proche") or "")[:160], "confiance": conf, "brut": contenu[:400]}


# ----------------------------------------------------------------------------------------------- extraits
def extrait(page: pymupdf.Page, x: float, y: float, fenetre: float, pastille=None) -> bytes:
    """PNG de la fenêtre centrée sur (x, y). `pastille` = (rayon_pt, rgb) : pastille synthétique dessinée au centre
    (page PROPRE de vecteur/plans.pdf — aperçu d'un candidat) ; None : la page annotée est montrée telle quelle."""
    h = fenetre / 2
    clip = pymupdf.Rect(x - h, y - h, x + h, y + h)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), clip=clip, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if pastille:
        r_pt, rgb = pastille
        dr = ImageDraw.Draw(im, "RGBA")
        cx, cy, r = pix.width / 2, pix.height / 2, max(r_pt, 3.0) * ZOOM
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(rgb) + (200,), outline=(30, 30, 30, 255), width=3)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def direction(texte: str):
    """Vecteur unitaire (dx, dy) lu dans « boîtier DP1, haut à gauche, 30 points » ; None si aucune direction."""
    t = (texte or "").lower()
    dx = dy = 0
    for mot, (vx, vy) in DIRECTIONS.items():
        if re.search(r"\b" + mot + r"\b", t):
            dx += vx
            dy += vy
    if dx == 0 and dy == 0:
        return None
    n = (dx * dx + dy * dy) ** 0.5
    return dx / n, dy / n


def candidats(idx: SymbolIndex, x: float, y: float, dir_: tuple | None, rayon: float = RAYON_CANDIDATS):
    """Symboles fermés du plan autour de (x, y), les plus proches d'abord, filtrés par la direction indiquée
    (le symbole visé est à moins de 90° de la direction lue) ; les formes grises (architecture de fond) sont
    exclues. Retourne [(cx, cy, rect)]."""
    area = pymupdf.Rect(x - rayon, y - rayon, x + rayon, y + rayon)
    out = []
    for r, col in idx.shapes_near(area):
        if _is_grey(col):
            continue
        c = (r.tl + r.br) / 2
        vx, vy = c.x - x, c.y - y
        d = (vx * vx + vy * vy) ** 0.5
        if d < 2.0 or d > rayon:
            continue                      # déjà dessus (le verdict négatif se réglera en réserve) ou trop loin
        if dir_ and (vx * dir_[0] + vy * dir_[1]) / d < 0.0:
            continue
        out.append((d, c.x, c.y, r))
    out.sort(key=lambda t: t[0])
    return [(cx, cy, r) for _, cx, cy, r in out[:MAX_CANDIDATS]]


# ----------------------------------------------------------------------------------------------- orchestration
def page_annotee(doc_annote: pymupdf.Document, rapport: dict, feuille: str, page_plan: int) -> pymupdf.Page:
    """Page « plan » de la feuille dans le PDF annoté (rendu-rapport `plan_page`, 1-based) ; sinon la page
    de même rang que dans plans.pdf."""
    for s in rapport.get("sheets", []):
        if s.get("sheet") == feuille and s.get("plan_page"):
            return doc_annote[int(s["plan_page"]) - 1]
    return doc_annote[min(page_plan, doc_annote.page_count) - 1]


def couleur_pastille(page: pymupdf.Page, x: float, y: float, rayon: float):
    """Couleur moyenne de la pastille déjà dessinée (page annotée), pour que l'aperçu d'un candidat lui ressemble."""
    try:
        r = max(rayon * 0.5, 1.0)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(x - r, y - r, x + r, y + r), alpha=False)
        n = pix.width * pix.height
        s = pix.samples
        return tuple(sum(s[i::3]) // n for i in range(3))
    except Exception:  # noqa
        return (180, 200, 240)


def executer(out_dir: Path, nom: str, modele: str, cle: str, fenetre: float = FENETRE, max_marques: int = 0,
             parallele: int = PARALLELE, corriger: bool = True, dry_run: bool = False, j=print) -> dict:
    vec = out_dir / "vecteur"
    p_est, p_plans = vec / "estimate.json", vec / "plans.pdf"
    p_annote = out_dir / f"{nom}-Plans-annotes.pdf"
    p_rapport = out_dir / f"{nom}-rendu-rapport.json"
    for p in (p_est, p_plans, p_annote):
        if not p.exists():
            raise FileNotFoundError(f"entrée manquante : {p}")
    est = json.loads(p_est.read_text(encoding="utf-8"))
    rapport = json.loads(p_rapport.read_text(encoding="utf-8")) if p_rapport.exists() else {}
    doc_annote, doc_plans = pymupdf.open(str(p_annote)), pymupdf.open(str(p_plans))
    dossier_png = out_dir / "verification-visuelle"
    dossier_png.mkdir(exist_ok=True)
    index: dict[int, SymbolIndex] = {}
    verrou = threading.Lock()

    def idx(page_no: int) -> SymbolIndex:
        with verrou:
            if page_no not in index:
                index[page_no] = SymbolIndex(doc_plans[page_no - 1])
            return index[page_no]

    marques = [(c, e) for c in est.get("counters", []) for e in c.get("elements", [])]
    if max_marques:
        marques = marques[:max_marques]
    j(f"vérification visuelle {nom} : {len(marques)} marques, modèle {modele}, fenêtre {fenetre:.0f} pt")

    def une(ce):
        c, e = ce
        feuille, page_plan = str(e.get("sheet")), int(e.get("page", 1))
        x, y, rep = float(e["x"]), float(e["y"]), str(e.get("repere") or "?")
        rayon = float(e.get("radius") or 6.0)
        page_a = page_annotee(doc_annote, rapport, feuille, page_plan)
        page_p = doc_plans[page_plan - 1]
        with verrou:
            png = extrait(page_a, x, y, fenetre)
            (dossier_png / f"{feuille}-{rep}.png").write_bytes(png)
        res = {"feuille": feuille, "repere": rep, "famille": c.get("family"), "x": x, "y": y,
               "flags_avant": list(e.get("flags") or []), "verdict": None, "confirmation": None,
               "etat": "ok", "candidats": [], "correction": None, "note": ""}
        if dry_run:
            res["etat"] = "non juge (dry-run)"
            return e, res
        res["verdict"] = v = juger(png, modele, cle, fenetre, j)
        if v["sur_symbole"] and v["pastille_visible"]:
            return e, res
        with verrou:
            png2 = extrait(page_a, x, y, FENETRE_CONFIRMATION)
        res["confirmation"] = v2 = juger(png2, modele, cle, FENETRE_CONFIRMATION, j)
        if v2["sur_symbole"] and v2["pastille_visible"]:
            res["etat"] = "ok (confirme au 2e jugement)"
            return e, res
        # verdict négatif confirmé : correction par les symboles vectoriels du plan, sinon réserve
        if corriger and not e.get("bbox"):
            rgb = couleur_pastille(page_a, x, y, rayon)
            for cx, cy, r in candidats(idx(page_plan), x, y, direction(v.get("symbole_proche") or v2.get("symbole_proche"))):
                r_c = max(r.width, r.height) / 2 + 1.0
                with verrou:
                    png_c = extrait(page_p, cx, cy, fenetre, pastille=(r_c, rgb))
                vc = juger(png_c, modele, cle, fenetre, j)
                res["candidats"].append({"x": cx, "y": cy, "rayon": r_c, "verdict": vc})
                if vc["sur_symbole"] and vc["pastille_visible"] and vc["confiance"] >= CONFIANCE_MIN:
                    res["correction"] = {"x_avant": x, "y_avant": y, "x": cx, "y": cy, "rayon": r_c,
                                         "symbole": vc["symbole_decrit"]}
                    res["etat"] = "corrige"
                    res["note"] = (f"position corrigee par verification visuelle ({modele}) : "
                                   f"{vc['symbole_decrit']} ; avant ({x:.1f}, {y:.1f})")
                    return e, res
        res["etat"] = "reserve"
        res["note"] = (f"verification visuelle ({modele}) : pastille hors symbole (*) — "
                       f"{v['symbole_decrit'] or 'rien de reconnu'} ; proche : {v['symbole_proche'] or '?'}")
        return e, res

    resultats = []
    with ThreadPoolExecutor(max_workers=max(1, parallele)) as ex:
        for e, res in ex.map(une, marques):
            resultats.append((e, res))
            if res["etat"] not in ("ok",):
                j(f"  {res['feuille']} {res['repere']} : {res['etat']}")

    n_ok = sum(1 for _, r in resultats if r["etat"].startswith("ok"))
    n_corr = sum(1 for _, r in resultats if r["etat"] == "corrige")
    n_res = sum(1 for _, r in resultats if r["etat"] == "reserve")
    n_err = len(resultats) - n_ok - n_corr - n_res
    modifie = False
    if not dry_run:
        for e, r in resultats:
            if r["etat"] == "corrige":
                e["x"], e["y"], e["radius"] = r["correction"]["x"], r["correction"]["y"], r["correction"]["rayon"]
                e["note"] = (e.get("note") + " ; " if e.get("note") else "") + r["note"]
                modifie = True
            elif r["etat"] == "reserve":
                flags = list(e.get("flags") or [])
                if REVALIDER not in flags:
                    flags.append(REVALIDER)
                e["flags"] = flags
                e["note"] = (e.get("note") + " ; " if e.get("note") else "") + r["note"]
                modifie = True
    doc_annote.close()
    if modifie:
        p_est.write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
        sheets = load_input(vec)
        rep = render(sheets, p_plans, p_annote, log=lambda *a, **k: None)
        if rapport:
            rapport["sheets"] = rep.get("sheets", rapport.get("sheets"))
            rapport["pages"] = rep.get("pages", rapport.get("pages"))
        j(f"  estimate.json mis a jour et PDF re-rendu : {p_annote.name}")
    doc_plans.close()

    resume = {"nom": nom, "date": datetime.datetime.now().isoformat(timespec="seconds"), "modele": modele,
              "prompt_version": VERSION_PROMPT, "fenetre_pt": fenetre, "marques": len(resultats), "ok": n_ok,
              "corrigees": n_corr, "reserves": n_res, "non_jugees": n_err, "pdf_re_rendu": modifie,
              "reperes_reserves": [f"{r['feuille']} {r['repere']}" for _, r in resultats if r["etat"] == "reserve"],
              "reperes_corriges": [f"{r['feuille']} {r['repere']}" for _, r in resultats if r["etat"] == "corrige"],
              "verdicts": [r for _, r in resultats]}
    (out_dir / f"{nom}-verification-visuelle.json").write_text(json.dumps(resume, ensure_ascii=False, indent=1),
                                                               encoding="utf-8")
    (out_dir / f"{nom}-verification-visuelle.md").write_text(rapport_md(resume), encoding="utf-8")
    if rapport:
        rapport["verification_visuelle"] = {k: resume[k] for k in ("modele", "marques", "ok", "corrigees",
                                                                   "reserves", "non_jugees", "pdf_re_rendu")}
        p_rapport.write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    return resume


def rapport_md(r: dict) -> str:
    L = [f"# Vérification visuelle — {r['nom']}", "",
         f"Date : {r['date']} · modèle : `{r['modele']}` (API NVIDIA) · fenêtre {r['fenetre_pt']:.0f} pt · "
         f"prompt {r['prompt_version']}", "",
         f"**Score : {r['ok'] + r['corrigees']}/{r['marques']}** — {r['ok']} pastilles jugées sur leur symbole, "
         f"{r['corrigees']} corrigées (déplacées sur un symbole vectoriel accepté par le modèle), "
         f"{r['reserves']} en réserve `*` (à trancher par Claude ou Francis), {r['non_jugees']} non jugées.", ""]
    if r["pdf_re_rendu"]:
        L += ["Le PDF « Plans annotés » a été re-rendu avec ces corrections et réserves.", ""]
    L += ["Les extraits jugés sont dans `verification-visuelle/<feuille>-<repere>.png` : ouvrir ceux listés "
          "ci-dessous avant de livrer.", ""]
    lignes = [v for v in r["verdicts"] if v["etat"] not in ("ok",)]
    if lignes:
        L += ["| feuille | repère | état | ce que le modèle a vu | note |", "|---|---|---|---|---|"]
        for v in lignes:
            vu = (v.get("verdict") or {}).get("symbole_decrit") or ""
            proche = (v.get("verdict") or {}).get("symbole_proche") or ""
            L.append(f"| {v['feuille']} | {v['repere']} | {v['etat']} | {vu} {('— proche : ' + proche) if proche else ''} "
                     f"| {v['note']} |")
    else:
        L.append("Aucune marque à revoir.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("sortie_dir")
    ap.add_argument("nom")
    ap.add_argument("--model", default=os.environ.get("RELEVE_VISION_MODEL", MODELE))
    ap.add_argument("--fenetre", type=float, default=FENETRE)
    ap.add_argument("--max-marques", type=int, default=0)
    ap.add_argument("--parallele", type=int, default=int(os.environ.get("RELEVE_VISION_PARALLELE", PARALLELE)))
    ap.add_argument("--sans-correction", action="store_true", help="juger et réserver seulement, ne jamais déplacer")
    ap.add_argument("--dry-run", action="store_true", help="extraits seulement, aucun appel à l'API")
    a = ap.parse_args()
    cle = os.environ.get("NVIDIA_API_KEY")
    if not cle and not a.dry_run:
        print("non exécutée : NVIDIA_API_KEY absente du processus")
        return 4
    try:
        r = executer(Path(a.sortie_dir), a.nom, a.model, cle or "", a.fenetre, a.max_marques, a.parallele,
                     corriger=not a.sans_correction, dry_run=a.dry_run)
    except Exception as e:  # noqa
        print(f"échec : {e}", file=sys.stderr)
        return 1
    print(f"vérification visuelle ({a.model}) : {r['marques']} marques, {r['ok']} OK, {r['corrigees']} corrigées, "
          f"{r['reserves']} réserves, {r['non_jugees']} non jugées")
    return 2 if r["reserves"] else 0


if __name__ == "__main__":
    sys.exit(main())
