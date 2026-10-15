# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Livrables PNG d'une feuille annotée (règle de Francis, 2026-10-15 : « on reste en PNG, laisse tomber le PDF ») :
- `<feuille>_annote.png`   : la page « Plans annotés » rastérisée (plan + pastilles + étiquettes) ;
- `<feuille>_calque.png`   : les pastilles SEULES sur fond transparent (RGBA) — l'image du plan est retirée de la
  page avant le rendu, ce qui laisse exactement le calque vectoriel (overlay) à superposer sur le plan d'origine.

Usage : uv run releve/calque_png.py PLANS_ANNOTES.pdf SORTIE_DIR [--page 1] [--largeur 4967]
(`--page` = numéro de page 1-based de la feuille ; la largeur par défaut est celle d'un A1 à 150 dpi.)
"""
from __future__ import annotations
import argparse, os
import pymupdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("sortie"); ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--largeur", type=int, default=4967); ap.add_argument("--nom", default=None)
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    doc = pymupdf.open(a.pdf); page = doc[a.page - 1]
    z = a.largeur / page.rect.width
    nom = a.nom or f"p{a.page:02d}"
    page.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(os.path.join(a.sortie, f"{nom}_annote.png"))
    for img in page.get_images(full=True):          # retire le plan raster : il ne reste que le calque vectoriel
        page.delete_image(img[0])
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=True).save(os.path.join(a.sortie, f"{nom}_calque.png"))
    print(f"{nom}_annote.png + {nom}_calque.png ({a.largeur} px de large) → {a.sortie}")


if __name__ == "__main__":
    main()
