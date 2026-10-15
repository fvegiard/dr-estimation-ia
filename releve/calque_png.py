# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Livrables PNG d'une feuille annotée (règle de Francis, 2026-10-15 : « on reste en PNG, laisse tomber le PDF ») :
- `<feuille>_annote.png`   : la page « Plans annotés » rastérisée (plan + pastilles + étiquettes) ;
- `<feuille>_calque.png`   : les pastilles SEULES sur fond transparent (RGBA) — le calque (overlay) à superposer
  sur le plan d'origine.

Le calque est isolé par les CALQUES OCG du relevé, pas en effaçant des images : `render_vectoriel.py` dessine chaque
famille dans un flux de contenu propre, balisé `/OC /MCn BDC … EMC` vers une OCG nommée « RELEVE … » (une par famille
+ `style.LEGEND_LAYER`). Ne sont gardés que les flux de contenu de la page qui référencent une de ces OCG ; le fond —
image raster d'un scan OU traits/textes d'un plan vectoriel OU calques CAO d'origine — est retiré. (Revue Codex/Copilot
PR #25 : supprimer les images laissait tout le plan vectoriel dans le calque.)

Usage : uv run releve/calque_png.py PLANS_ANNOTES.pdf SORTIE_DIR [--page 1] [--largeur 4967] [--nom E201]
(`--page` = numéro de page 1-based de la feuille DANS « Plans annotés » (`plan_page` du rapport de rendu, pas la page
de `vecteur/plans.pdf`) ; la largeur par défaut est celle d'un A1 à 150 dpi.)
"""
from __future__ import annotations
import argparse, os, re, sys
import pymupdf

PREFIXE_CALQUE = "RELEVE"          # nom des OCG écrites par src/estimer/render (familles + légende)


def flux_releve(doc: pymupdf.Document, page: pymupdf.Page) -> tuple[list[int], list[int]]:
    """(xrefs de contenu à garder, xrefs retirés) : un flux est gardé s'il balise au moins un bloc /OC vers une OCG
    « RELEVE … » de la page."""
    noms = {x: v.get("name", "") for x, v in doc.get_ocgs().items()}
    props = {}
    ok, props_raw = doc.xref_get_key(page.xref, "Resources/Properties")
    if ok == "dict":
        for m in re.finditer(r"/(\w+)\s+(\d+)\s+0\s+R", props_raw):
            props[m.group(1)] = int(m.group(2))
    releve = {n for n, x in props.items() if noms.get(x, "").startswith(PREFIXE_CALQUE)}
    garder, retirer = [], []
    for x in page.get_contents():
        c = doc.xref_stream(x).decode("latin-1", errors="replace")
        refs = set(re.findall(r"/OC\s*/(\w+)\s+BDC", c))
        (garder if refs & releve else retirer).append(x)
    return garder, retirer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("sortie"); ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--largeur", type=int, default=4967); ap.add_argument("--nom", default=None)
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    doc = pymupdf.open(a.pdf)
    if not 1 <= a.page <= doc.page_count:
        sys.exit(f"page {a.page} hors du PDF ({doc.page_count} pages)")
    page = doc[a.page - 1]
    z = a.largeur / page.rect.width
    nom = a.nom or f"p{a.page:02d}"
    page.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(os.path.join(a.sortie, f"{nom}_annote.png"))
    garder, retirer = flux_releve(doc, page)
    if not garder:
        sys.exit(f"aucun flux de contenu « {PREFIXE_CALQUE} » sur la page {a.page} : pas un PDF de render_vectoriel.py ?")
    doc.xref_set_key(page.xref, "Contents", "[ " + " ".join(f"{x} 0 R" for x in garder) + " ]")
    page = doc.reload_page(page)
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=True).save(os.path.join(a.sortie, f"{nom}_calque.png"))
    print(f"{nom}_annote.png + {nom}_calque.png ({a.largeur} px de large ; calque = {len(garder)} flux RELEVE gardés, "
          f"{len(retirer)} flux de fond retirés) → {a.sortie}")


if __name__ == "__main__":
    main()
