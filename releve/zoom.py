# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "pillow>=10"]
# ///
"""Outil de lecture visuelle : rend une zone d'une feuille avec règles graduées (points PDF)
et, par-dessus, les occurrences déjà relevées (pour vérifier / compléter).

Usage : uv run releve/zoom.py WORKDIR FEUILLE X0 Y0 X1 Y1 [--px 1800] [--sans-marques]
Sortie : WORKDIR/zooms/<FEUILLE>_<X0>_<Y0>_<X1>_<Y1>.png (le chemin est imprimé).
"""
import os
import sys
import json
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf
from PIL import Image, ImageDraw
from commun import load_nomenclature, load_occurrences, draw_mark
from prepare import draw_rulers, font

def open_sheet_page(work, feuille):
    doc = pymupdf.open(os.path.join(work, "feuilles", feuille + ".pdf"))
    return doc, doc[0]

def main():
    a = sys.argv[1:]
    px = 1800; marks = True
    if "--px" in a:
        i = a.index("--px"); px = int(a[i + 1]); del a[i:i + 2]
    if "--sans-marques" in a:
        a.remove("--sans-marques"); marks = False
    work, f = a[0], a[1]
    x0, y0, x1, y1 = map(float, a[2:6])
    if not all(math.isfinite(v) for v in (x0, y0, x1, y1)) or x1 <= x0 or y1 <= y0:
        raise ValueError("zoom bounds must be finite with x1 > x0 and y1 > y0")
    if px <= 0:
        raise ValueError("zoom pixel width must be positive")
    doc, page = open_sheet_page(work, f)
    requested = pymupdf.Rect(x0, y0, x1, y1)
    clip = requested & page.rect
    if clip.is_empty:
        doc.close()
        raise ValueError("zoom bounds do not intersect the source page")
    z = px / (x1 - x0)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, alpha=False)
    # Integer raster rounding can extend the pixel frame slightly beyond the clip.
    raster_bounds = [pix.x / z, pix.y / z, (pix.x + pix.width) / z, (pix.y + pix.height) / z]
    metadata = {
        "sheet": f, "requested_bounds_pt": list(requested),
        "effective_clip_bounds_pt": list(clip), "raster_bounds_pt": raster_bounds,
        "source_page_bounds_pt": list(page.rect), "source_rotation_degrees": page.rotation,
        "coordinate_frame": "displayed_page_pdf_points",
        "image_size_px": [pix.width, pix.height], "pixmap_origin_px": [pix.x, pix.y],
        "pixels_per_pdf_point": z, "rulers_overlay": True, "added_padding_px": [0, 0, 0, 0],
        "pixel_to_pdf": "x=(pixmap_origin_px[0]+u)/pixels_per_pdf_point; y=(pixmap_origin_px[1]+v)/pixels_per_pdf_point",
        "instructions": "Use original PNG pixels from its top-left. Rulers overlay the source: subtract NO margin. If displayed resized, convert display pixels to original PNG pixels first.",
    }
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im, "RGBA")
    if marks:
        nom = load_nomenclature(work)
        fnt = font(16)
        for o in load_occurrences(work):
            if o["feuille"] != f or not clip.contains(pymupdf.Point(o["x"], o["y"])):
                continue
            n = nom.get(o["label"], {"forme": 2, "rgb": (255, 0, 255)})
            cx, cy = o["x"] * z - pix.x, o["y"] * z - pix.y
            draw_mark(dr, n["forme"], cx, cy, max(7, 6 * z), n["rgb"], outline=(0, 0, 0), width=2)
            dr.text((cx + 8, cy - 8), o["label"][:28], fill=(120, 0, 0, 255), font=fnt)
    step = 50 if (x1 - x0) > 300 else (20 if (x1 - x0) > 120 else 10)
    draw_rulers(im, *raster_bounds, step)
    os.makedirs(os.path.join(work, "zooms"), exist_ok=True)
    out = os.path.join(work, "zooms", f"{f}_{int(x0)}_{int(y0)}_{int(x1)}_{int(y1)}.png")
    im.save(out); print(out)
    # Keep stdout path-only for existing callers (including NVIDIA's last-line parser).
    print(json.dumps(metadata, ensure_ascii=False), file=sys.stderr)
    doc.close()

if __name__ == "__main__":
    main()
