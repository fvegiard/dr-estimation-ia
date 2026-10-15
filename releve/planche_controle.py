# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "pillow>=10"]
# ///
"""Planche de contrôle visuel : une vignette par pastille du PDF « Plans annotés », à relire AVANT de dire « fait ».
Auto-supervision (CLAUDE.md §Autonomie) : l'œil du modèle ne voit pas un décalage de 5 pt sur une feuille entière,
il le voit sur une vignette à ×8. Le 2026-10-15 (TEST-E201), 8 pastilles décalées et 4 familles fausses sont passées
inaperçues sur les vues d'ensemble et ont été vues du premier coup sur des vignettes.

Produit SORTIE/controle/<feuille>-planche-NN.png (grille 6 × 5, 30 vignettes de 36 × 36 pt à ×8, repère en légende)
et, avec --avant ANCIEN.pdf, des paires avant/après pour montrer ce qui a changé.

Usage : uv run releve/planche_controle.py PLANS_ANNOTES.pdf ESTIMATE_JSON SORTIE [--avant ANCIEN.pdf] [--taille 36]
(ESTIMATE_JSON = vecteur/estimate.json écrit par render_vectoriel.py : repère + x, y de chaque pastille.)
"""
from __future__ import annotations
import argparse, json, os
import pymupdf
from PIL import Image, ImageDraw, ImageFont


def reperes(estimate_json):
    e = json.load(open(estimate_json, encoding="utf-8"))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "repere" in o and "x" in o:
                out.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(e)
    return out


def vignette(page, x, y, taille, z):
    pm = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(x - taille / 2, y - taille / 2, x + taille / 2, y + taille / 2))
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("estimate"); ap.add_argument("sortie")
    ap.add_argument("--avant", default=None); ap.add_argument("--taille", type=float, default=36.0); ap.add_argument("--zoom", type=float, default=8.0)
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    doc = pymupdf.open(a.pdf); avant = pymupdf.open(a.avant) if a.avant else None
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except Exception:  # noqa
        font = ImageFont.load_default()
    items = reperes(a.estimate)
    par_feuille = {}
    for it in items:
        par_feuille.setdefault(it.get("sheet", ""), []).append(it)
    sheets_pages = {}
    for sh in json.load(open(a.estimate, encoding="utf-8")).get("sheets", []):
        sheets_pages[sh.get("name") or sh.get("sheet")] = sh.get("plan_page", 1)
    n_planches = 0
    for feuille, lst in par_feuille.items():
        page = doc[(sheets_pages.get(feuille, 1) or 1) - 1]
        page_av = avant[(sheets_pages.get(feuille, 1) or 1) - 1] if avant else None
        lst.sort(key=lambda o: o["repere"])
        cols, rows_, par = 6, 5, 30
        if avant:
            cols, par = 3, 15
        for k in range(0, len(lst), par):
            sub = lst[k:k + par]
            tw = int(a.taille * a.zoom); th = tw + 22
            cell_w = tw * 2 + 8 if avant else tw
            img = Image.new("RGB", (cols * (cell_w + 10), rows_ * (th + 10)), "white"); d = ImageDraw.Draw(img)
            for i, it in enumerate(sub):
                cx, cy = (i % cols) * (cell_w + 10), (i // cols) * (th + 10)
                v = vignette(page, it["x"], it["y"], a.taille, a.zoom)
                if avant:
                    va = vignette(page_av, it["x"], it["y"], a.taille, a.zoom)
                    img.paste(va, (cx, cy + 22)); img.paste(v, (cx + tw + 8, cy + 22))
                    d.rectangle([cx, cy + 22, cx + tw - 1, cy + 22 + tw - 1], outline=(200, 0, 0), width=2)
                    d.rectangle([cx + tw + 8, cy + 22, cx + tw + 8 + tw - 1, cy + 22 + tw - 1], outline=(0, 150, 0), width=2)
                else:
                    img.paste(v, (cx, cy + 22))
                d.text((cx + 4, cy + 2), f"{it['repere']}  ({it['x']:.0f}, {it['y']:.0f})", fill="black", font=font)
            out = os.path.join(a.sortie, f"{feuille}-planche-{k // par + 1:02d}.png"); img.save(out); n_planches += 1
    print(f"{len(items)} vignettes sur {n_planches} planche(s) → {a.sortie}")


if __name__ == "__main__":
    main()
