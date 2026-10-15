#!/usr/bin/env python3
"""Mesure la couleur primaire (et secondaire) d'un logo PNG et prépare une version imprimable.

Usage:
  python extract_brand.py assets/logo_xxx.png            -> affiche les couleurs dominantes
  python extract_brand.py logo_web.png --print-safe out.png --dark 2B2B2B
      recolore les pixels blancs/gris pâles (texte prévu pour fond foncé) en gris foncé.
"""
import argparse
import json
from collections import Counter

from PIL import Image


def dominant_colors(path, n=3):
    im = Image.open(path).convert("RGBA")
    px = [p for p in im.getdata() if p[3] > 200 and max(p[:3]) < 240 and (max(p[:3]) - min(p[:3])) > 20]
    c = Counter((p[0] // 8 * 8, p[1] // 8 * 8, p[2] // 8 * 8) for p in px)
    out = []
    for (r, g, b), cnt in c.most_common(40):
        hx = "#%02X%02X%02X" % (r, g, b)
        # regroupe les teintes proches
        if all(abs(r - rr) + abs(g - gg) + abs(b - bb) > 60 for (rr, gg, bb), _ in out):
            out.append(((r, g, b), cnt))
        if len(out) >= n:
            break
    return [("#%02X%02X%02X" % k, v) for k, v in out]


def print_safe(src, dst, dark="2B2B2B", max_w=700):
    d = tuple(int(dark[i:i + 2], 16) for i in (0, 2, 4))
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a > 0 and min(r, g, b) > 170 and max(r, g, b) - min(r, g, b) < 25:
                px[x, y] = (*d, a)
    im.thumbnail((max_w, max_w))
    im.save(dst, optimize=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("logo")
    ap.add_argument("--print-safe", metavar="OUT")
    ap.add_argument("--dark", default="2B2B2B")
    a = ap.parse_args()
    cols = dominant_colors(a.logo)
    print(json.dumps({"primary": cols[0][0], "secondary": (cols[1][0] if len(cols) > 1 else cols[0][0]), "all": cols}, indent=2))
    if a.print_safe:
        print_safe(a.logo, a.print_safe, a.dark)
        print("print-safe ->", a.print_safe)
