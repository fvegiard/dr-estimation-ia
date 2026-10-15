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
        [--mesures travail/occurrences-visuel.csv]   (écart contour→encre en pt et couverture, mesurés par ancrage_raster.py)
        [--rapport <NOM>-rendu-rapport.json]          (page réelle de chaque feuille dans « Plans annotés » — obligatoire dès 2 feuilles)
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
    ap.add_argument("--mesures", default=None, help="occurrences-visuel.csv d'ancrage_raster.py : écart/couverture dans la légende de chaque vignette")
    ap.add_argument("--rapport", default=None, help="<NOM>-rendu-rapport.json de render_vectoriel.py : page RÉELLE de chaque feuille dans « Plans annotés » (plan_page)")
    a = ap.parse_args()
    mesures = []
    if a.mesures:
        import csv
        mesures = [r for r in csv.DictReader(open(a.mesures, encoding="utf-8")) if (r.get("ecart_pt") or "").strip()]

    def mesure(feuille, x, y):
        for r in mesures:
            if r.get("feuille") == feuille and abs(float(r["x_pt"]) - x) < 0.6 and abs(float(r["y_pt"]) - y) < 0.6:
                return f"  e={r['ecart_pt']} c={r['couverture']} ({r.get('mesure', '')[:4]})"
        return ""
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
    # Page de chaque feuille DANS « Plans annotés » : `plan_page` du rapport de rendu. Les `page` d'estimate.json sont
    # celles de vecteur/plans.pdf, AVANT insertion des bordereaux — fausses dès la 2e feuille (revues Codex/Copilot PR #25).
    sheets_pages = {}
    if a.rapport:
        for sh in json.load(open(a.rapport, encoding="utf-8")).get("sheets", []):
            sheets_pages[sh["sheet"]] = int(sh["plan_page"])
    else:
        for sh in json.load(open(a.estimate, encoding="utf-8")).get("sheets", []):
            sheets_pages[sh.get("sheet") or sh.get("name")] = int(sh.get("plan_page") or sh.get("page") or 1)
        if len(sheets_pages) > 1:
            print("ATTENTION : plusieurs feuilles sans --rapport : les pages viennent d'estimate.json (avant bordereaux) et peuvent être fausses")
    n_planches = 0
    for feuille, lst in par_feuille.items():
        pg = sheets_pages.get(feuille) or int(lst[0].get("page") or 1)      # page de la feuille dans « Plans annotés »
        if not 1 <= pg <= doc.page_count:
            raise SystemExit(f"feuille {feuille} : page {pg} hors du PDF ({doc.page_count} pages)")
        page = doc[pg - 1]
        page_av = avant[pg - 1] if avant else None
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
                d.text((cx + 4, cy + 2), f"{it['repere']}  ({it['x']:.0f}, {it['y']:.0f}){mesure(feuille, it['x'], it['y'])}", fill="black", font=font)
            out = os.path.join(a.sortie, f"{feuille}-planche-{k // par + 1:02d}.png"); img.save(out); n_planches += 1
    print(f"{len(items)} vignettes sur {n_planches} planche(s) → {a.sortie}")


if __name__ == "__main__":
    main()
