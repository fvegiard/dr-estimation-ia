"""EXEMPLE-format relevé PDF renderer (HR26-14 target look, see docs/FORMAT-EXEMPLE.md).

For every sheet with counted symbols: the original vector plan page with one marker per symbol, its repère
label and the "RELEVE <sheet> - MATERIEL" box, followed by its "BORDEREAU MATERIEL - <sheet>" table pages.
"""
from __future__ import annotations

from pathlib import Path

import pymupdf

from .bordereau import add_bordereau
from .data import Sheet, load_input
from .plan import annotate_page
from . import style as S


def render(sheets: list[Sheet], plans_pdf: Path, out_pdf: Path, log=print) -> dict:
    """Write out_pdf: for each sheet (in the given order) its annotated plan page then its bordereau pages.

    The plan pages are the original page objects of plans_pdf (kept with `select`, so vector content, seal
    widgets and existing layers survive); every overlay is added as vector content in RELEVE layers."""
    out = pymupdf.open(plans_pdf)
    for sh in sheets:
        if not 1 <= sh.page <= out.page_count:
            raise ValueError(f"sheet {sh.name}: page {sh.page} not in {plans_pdf} ({out.page_count} pages)")
    wanted = [sh.page - 1 for sh in sheets]
    uniq = list(dict.fromkeys(wanted))
    out.select(uniq)
    for k, p in enumerate(wanted):           # a page shared by two sheets gets its own copy
        if wanted.index(p) != k:
            out.fullcopy_page(uniq.index(p))
    slot = {}
    extra = len(uniq)
    for k, p in enumerate(wanted):
        if wanted.index(p) == k:
            slot[k] = uniq.index(p)
        else:
            slot[k] = extra
            extra += 1
    if extra > len(uniq):                    # move duplicated copies into sheet order
        out.select([slot[k] for k in range(len(wanted))])
    out.set_toc([])

    legend_oc = out.add_ocg(S.LEGEND_LAYER, on=True)
    ocgs: dict[tuple[str, str], int] = {}
    toc, report = [], []
    pos = 0
    for sh in sheets:
        plan = out[pos]
        layers = {}
        for f in sh.families():
            key = (f.code, f.materiel)
            if key not in ocgs:
                ocgs[key] = out.add_ocg(f"RELEVE {f.code} - {f.materiel}", on=True)
            layers[f.code] = ocgs[key]
        box = annotate_page(plan, sh, pos + 2, layers, legend_oc)
        bpages = add_bordereau(out, sh, plan.rect.width, plan.rect.height, at=pos + 1)
        toc.append([1, f"{sh.name} - plan", pos + 1])
        toc.append([2, f"Bordereau materiel {sh.name}", bpages[0] + 1])
        fams = sh.families()
        report.append({"sheet": sh.name, "plan_page": pos + 1, "bordereau_pages": [p + 1 for p in bpages],
                       "reperes": len(sh.items), "familles": len(fams), "res": sh.n_reserves,
                       "box": [round(v, 1) for v in box.rect], "box_layout": [box.ncols, box.col_w, box.pitch],
                       "box_in_free_space": box.fits})
        log(f"{sh.name}: {len(sh.items)} reperes / {len(fams)} familles / RES {sh.n_reserves} "
            f"-> page {pos + 1} + bordereau {len(bpages)} p." + ("" if box.fits else " (box overlaps drawing)"))
        pos = bpages[-1] + 1
    out.set_toc(toc)
    out_pdf = Path(out_pdf)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_pdf, garbage=3, deflate=True)
    return {"pages": out.page_count, "sheets": report}


__all__ = ["render", "load_input"]
