"""Outil de lecture visuelle : rend une zone d'une feuille avec règles graduées (points PDF)
et, par-dessus, les occurrences déjà relevées (pour vérifier / compléter).

Porté depuis planexpert-core/releve/zoom.py (imports relatifs de package).

Usage : python -m src.pipeline.zoom WORKDIR FEUILLE X0 Y0 X1 Y1 [--px 1800] [--sans-marques]
Sortie : WORKDIR/zooms/<FEUILLE>_<X0>_<Y0>_<X1>_<Y1>.png (le chemin est imprimé).
"""
import os, sys
import pymupdf
from PIL import Image, ImageDraw
from .commun import load_nomenclature, load_occurrences, draw_mark
from .prepare import draw_rulers, font

def main():
    a = sys.argv[1:]
    px = 1800; marks = True
    if "--px" in a:
        i = a.index("--px"); px = int(a[i + 1]); del a[i:i + 2]
    if "--sans-marques" in a:
        a.remove("--sans-marques"); marks = False
    work, f = a[0], a[1]
    x0, y0, x1, y1 = map(float, a[2:6])
    page = pymupdf.open(os.path.join(work, "feuilles", f + ".pdf"))[0]
    z = px / (x1 - x0)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(x0, y0, x1, y1), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im, "RGBA")
    if marks:
        nom = load_nomenclature(work)
        fnt = font(16)
        for o in load_occurrences(work):
            if o["feuille"] != f or not (x0 <= o["x"] <= x1 and y0 <= o["y"] <= y1):
                continue
            n = nom.get(o["label"], {"forme": 2, "rgb": (255, 0, 255)})
            cx, cy = (o["x"] - x0) * z, (o["y"] - y0) * z
            draw_mark(dr, n["forme"], cx, cy, max(7, 6 * z), n["rgb"], outline=(0, 0, 0), width=2)
            dr.text((cx + 8, cy - 8), o["label"][:28], fill=(120, 0, 0, 255), font=fnt)
    step = 50 if (x1 - x0) > 300 else (20 if (x1 - x0) > 120 else 10)
    draw_rulers(im, x0, y0, x1, y1, step)
    os.makedirs(os.path.join(work, "zooms"), exist_ok=True)
    out = os.path.join(work, "zooms", f"{f}_{int(x0)}_{int(y0)}_{int(x1)}_{int(y1)}.png")
    im.save(out); print(out)

if __name__ == "__main__":
    main()
