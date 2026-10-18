# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "pillow>=10"]
# ///
"""Planches de vignettes des signatures de blocs (`blocs_vectoriels.py`) : UNE vignette par signature (son instance la
plus centrale), avec son identifiant court, le nombre d'occurrences par feuille, la description de légende si la
signature est aussi dessinée dans la légende, et la lettre contenue. L'agent (ou Francis) étiquette ensuite chaque
signature UNE fois dans `blocs-familles.csv` (sig_id,label,code,forme,materiel,note) — toutes les occurrences suivent.

Usage : uv run releve/blocs_vignettes.py WORKDIR PDF SORTIE [--min 2] [--feuilles E101 …] [--par-planche 30]
Écrit SORTIE/signatures-NN.png, WORKDIR/blocs-index.csv (sig_id, signature, n_plans, par_feuille, legende, lettre, exemple) et
WORKDIR/blocs-ids.json (mémoire cumulative signature → sig_id, pour des identifiants stables d'une passe à l'autre).
"""
from __future__ import annotations
import argparse, csv, json, os, sys
from collections import defaultdict
import pymupdf
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import PagesFeuilles  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("pdf"); ap.add_argument("sortie")
    ap.add_argument("--min", type=int, default=2); ap.add_argument("--feuilles", nargs="+", default=None)
    ap.add_argument("--par-planche", type=int, default=30); ap.add_argument("--taille", type=float, default=40.0); ap.add_argument("--zoom", type=float, default=6.0)
    a = ap.parse_args()
    work = os.path.abspath(a.workdir); os.makedirs(a.sortie, exist_ok=True)
    feuilles = {r["feuille"]: r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8"))}
    plans = [f for f, r in feuilles.items() if r.get("role") == "plan" and (not a.feuilles or f in a.feuilles)]
    sigs = json.load(open(os.path.join(work, "blocs-signatures.json"), encoding="utf-8"))
    inst = defaultdict(list)
    for f in plans:
        p = os.path.join(work, "blocs", f + ".csv")
        if os.path.exists(p):
            for b in csv.DictReader(open(p, encoding="utf-8")):
                inst[b["signature"]].append(b)
    rows = []
    for k, s in sigs.items():
        n = sum(s["par_feuille"].get(f, 0) for f in plans)
        leg = (s.get("legende") or {}).get("description", "")
        sig = json.loads(k); lettre = sig[2] if len(sig) > 2 else ""
        if n >= a.min or (leg and n >= 1) or (lettre and n >= 1):
            rows.append((n, k, leg, lettre))
    rows.sort(key=lambda r: -r[0])
    # identifiants STABLES : une signature déjà indexée garde son sig_id (blocs-familles.csv s'y réfère) ; les
    # nouvelles reçoivent des numéros au-delà du plus grand existant (revue Codex PR #27)
    # `blocs-ids.json` = mémoire CUMULATIVE signature → sig_id : une signature qui disparaît d'une passe (réglage de
    # fusion) et réapparaît à la suivante retrouve son identifiant au lieu d'en recevoir un nouveau
    anciens = {}
    p_idx = os.path.join(work, "blocs-index.csv")
    if os.path.exists(p_idx):
        anciens.update({r["signature"]: r["sig_id"] for r in csv.DictReader(open(p_idx, encoding="utf-8"))})
    p_ids = os.path.join(work, "blocs-ids.json")
    if os.path.exists(p_ids):
        anciens.update(json.load(open(p_ids, encoding="utf-8")))      # la mémoire cumulative fait foi
    prochain = max([int(v[1:]) for v in anciens.values()] + [0]) + 1
    ids = {}
    for n, k, leg, lettre in rows:
        if k in anciens:
            ids[k] = anciens[k]
        else:
            ids[k] = f"S{prochain:03d}"; prochain += 1
    anciens.update(ids)
    json.dump(anciens, open(p_ids, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    pages = PagesFeuilles(work, a.pdf)      # chaque feuille dans son document source (revue Codex PR #28)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        fontb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except Exception:  # noqa
        font = fontb = ImageFont.load_default()
    index = []
    tw = int(a.taille * a.zoom); th = tw + 58; cols = 6
    for k0 in range(0, len(rows), a.par_planche):
        sub = rows[k0:k0 + a.par_planche]
        nrows = (len(sub) + cols - 1) // cols
        img = Image.new("RGB", (cols * (tw + 12), nrows * (th + 10)), "white"); d = ImageDraw.Draw(img)
        for i, (n, k, leg, lettre) in enumerate(sub):
            sid = ids[k]
            ex = inst[k]
            # instance « la plus centrale » de la feuille qui en a le plus
            par = defaultdict(int)
            for b in ex: par[b["feuille"]] += 1
            f_best = max(par, key=par.get)
            cand = [b for b in ex if b["feuille"] == f_best]
            cx = sum(float(b["x_pt"]) for b in cand) / len(cand); cy = sum(float(b["y_pt"]) for b in cand) / len(cand)
            b = min(cand, key=lambda b: (float(b["x_pt"]) - cx) ** 2 + (float(b["y_pt"]) - cy) ** 2)
            page = pages.page(feuilles[f_best])
            x, y = float(b["x_pt"]), float(b["y_pt"]); t = max(a.taille, float(b["diametre_pt"]) * 1.6)
            z = tw / t
            clip = pymupdf.Rect(x - t / 2, y - t / 2, x + t / 2, y + t / 2) * page.rotation_matrix     # blocs = repère non tourné ; pixmap = repère affiché
            pm = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip)
            v = Image.frombytes("RGB", (pm.width, pm.height), pm.samples).resize((tw, tw))
            vd = ImageDraw.Draw(v)
            w, h = float(b["w_pt"]) * z, float(b["h_pt"]) * z
            vd.rectangle([tw / 2 - w / 2 - 2, tw / 2 - h / 2 - 2, tw / 2 + w / 2 + 2, tw / 2 + h / 2 + 2], outline=(220, 0, 0), width=2)
            cxp, cyp = (i % cols) * (tw + 12), (i // cols) * (th + 10)
            img.paste(v, (cxp, cyp + 40))
            d.text((cxp + 2, cyp + 2), f"{sid}  n={n}  ø{b['diametre_pt']} pt" + (f"  [{lettre}]" if lettre else ""), fill="black", font=fontb)
            det = " ".join(f"{f}:{c}" for f, c in sorted(par.items()))
            d.text((cxp + 2, cyp + 20), det[:52], fill=(60, 60, 60), font=font)
            if leg:
                d.text((cxp + 2, cyp + 40 + tw + 2), ("LÉG: " + leg)[:50], fill=(0, 90, 0), font=font)
            index.append({"sig_id": sid, "signature": k, "n_plans": n, "par_feuille": det, "legende": leg, "lettre": lettre,
                          "exemple": f"{f_best} ({x:.1f},{y:.1f})", "diametre_pt": b["diametre_pt"]})
        out = os.path.join(a.sortie, f"signatures-{k0 // a.par_planche + 1:02d}.png"); img.save(out)
    with open(os.path.join(work, "blocs-index.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["sig_id", "signature", "n_plans", "par_feuille", "legende", "lettre", "exemple", "diametre_pt"]); w.writeheader(); w.writerows(index)
    print(f"{len(rows)} signatures sur {(len(rows) + a.par_planche - 1) // a.par_planche} planche(s) → {a.sortie} ; blocs-index.csv")


if __name__ == "__main__":
    main()
