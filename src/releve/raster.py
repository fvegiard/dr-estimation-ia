"""
Sous-commande `raster` — rend une page PDF en PNG au DPI voulu (ou à une
taille de raster imposée), et écrit à côté un JSON donnant le rapport
px <-> pt **par axe** — la formule à deux facteurs vérifiée dans
`src/qpl/import_counters.py` et documentée en PIPELINE §3.2 :

    x_px = round(x_pt * raster_width_px  / page_width_pt)
    y_px = round(y_pt * raster_height_px / page_height_pt)

(PIPELINE §3.2 signale qu'une formule à un seul facteur, utilisée ailleurs
dans le dépôt de référence, introduit un écart de 0,0107 % — négligeable au
rayon d'appariement utilisé là-bas, mais pas exact : le socle retient donc
toujours les deux facteurs, mesurés sur le PNG réellement écrit, jamais
supposés égaux.)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymupdf
from PIL import Image


def render_page(
    pdf_path: Path,
    page_index: int,
    out_png: Path,
    *,
    dpi: float | None = None,
    raster_width_px: int | None = None,
    raster_height_px: int | None = None,
) -> dict:
    doc = pymupdf.open(pdf_path)
    page = doc[page_index]
    page_width_pt = page.rect.width
    page_height_pt = page.rect.height

    if raster_width_px and raster_height_px:
        # Deux facteurs d'échelle indépendants (§3.2) : on vise une taille de
        # raster précise (ex. pour retomber sur les 5694x4022 px de Plan
        # Expert), au prix d'une éventuelle anisotropie négligeable.
        sx = raster_width_px / page_width_pt
        sy = raster_height_px / page_height_pt
    else:
        dpi = dpi or 150.0
        sx = sy = dpi / 72.0

    matrix = pymupdf.Matrix(sx, sy)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_png)
    doc.close()

    # Les dimensions réelles du raster sont RELUES dans le PNG écrit, jamais
    # supposées (même garde-fou que import_counters.py : les
    # dimensions viennent de PIL.Image.open(...).size + image.verify()).
    with Image.open(out_png) as img:
        img.verify()
    with Image.open(out_png) as img:
        real_w, real_h = img.size

    px_per_pt_x = real_w / page_width_pt
    px_per_pt_y = real_h / page_height_pt

    return {
        "pdf": str(pdf_path),
        "page_index": page_index,
        "png": str(out_png),
        "page_width_pt": page_width_pt,
        "page_height_pt": page_height_pt,
        "raster_width_px": real_w,
        "raster_height_px": real_h,
        "px_per_pt_x": px_per_pt_x,
        "px_per_pt_y": px_per_pt_y,
        "pt_per_px_x": 1.0 / px_per_pt_x,
        "pt_per_px_y": 1.0 / px_per_pt_y,
    }


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("pdf", type=Path, help="Fichier PDF source")
    sub.add_argument("--page", type=int, default=0, help="Index de page (0 = 1re page)")
    sub.add_argument("--out", type=Path, required=True, help="PNG à écrire")
    sub.add_argument("--out-json", type=Path, help="JSON du rapport px<->pt (sinon <out>.json)")
    sub.add_argument("--dpi", type=float, help="DPI isotrope (défaut 150 si aucune taille imposée)")
    sub.add_argument("--raster-width", type=int, help="Largeur de raster imposée (px)")
    sub.add_argument("--raster-height", type=int, help="Hauteur de raster imposée (px)")


def run(args: argparse.Namespace) -> int:
    if bool(args.raster_width) != bool(args.raster_height):
        raise SystemExit("--raster-width et --raster-height vont ensemble")

    report = render_page(
        args.pdf,
        args.page,
        args.out,
        dpi=args.dpi,
        raster_width_px=args.raster_width,
        raster_height_px=args.raster_height,
    )
    out_json = args.out_json or args.out.with_suffix(".json")
    Path(out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"OK : {args.out} ({report['raster_width_px']}x{report['raster_height_px']} px) "
        f"-> {out_json}"
    )
    return 0
