"""EXEMPLE-format relevé PDF renderer (HR26-14 target look, see docs/FORMAT-EXEMPLE.md).

For every sheet with counted symbols: the original vector plan page with one marker per symbol, its repère
label and the "RELEVE <sheet> - MATERIEL" box, followed by its "BORDEREAU MATERIEL - <sheet>" table pages.
"""
from __future__ import annotations

from pathlib import Path

import pymupdf

from .bordereau import add_bordereau, add_bordereau_agrege
from .data import Sheet, load_input
from .plan import annotate_page, encadre_v6
from . import style as S


def signets_de_page(toc: list, page: int) -> list[list]:
    """Signets d'origine d'une page du PDF de plans : ceux qui la visent, avec leurs parents (niveaux gardés).

    [niveau, titre, 1] quand le signet vise la page, [niveau, titre, -1] (sans destination) pour un parent qui
    vise une autre page — comme un extrait d'une page qui garde le chemin de ses signets."""
    keep, stack = set(), []
    for i, t in enumerate(toc):
        while stack and toc[stack[-1]][0] >= t[0]:
            stack.pop()
        if t[2] == page:
            keep.update(stack)
            keep.add(i)
        stack.append(i)
    return [[t[0], t[1], 1 if t[2] == page else -1] for i, t in enumerate(toc) if i in keep]


def titre_signet(sh: Sheet) -> str:
    """Signet de niveau 1 de la feuille (gold `HR26-14-E03-annote-v6`) : <soumission>-<feuille>-annote-v<n> ;
    sans soumission connue, <feuille>-annote-v<n>."""
    return "-".join(x for x in (sh.projet, sh.name) if x) + f"-annote-v{sh.version}"


def render(sheets: list[Sheet], plans_pdf: Path, out_pdf: Path, log=print) -> dict:
    """Write out_pdf: for each sheet (in the given order) its annotated plan page then its bordereau pages.

    The plan pages are the original page objects of plans_pdf (kept with `select`, so vector content, seal
    widgets and existing layers survive); every overlay is added as vector content in RELEVE layers.

    Gold HR26-14 (docs/FORMAT-EXEMPLE.md §1, §2.1) : chaque feuille a SES calques — un `RELEVE <code> -
    <materiel>` par famille puis `RELEVE - Legende et avertissements` — dessinés sur sa page plan et sur ses
    pages de bordereau ; un signet `<soumission>-<feuille>-annote-v<n>` sur sa page plan, avec les signets
    d'origine de son plan dessous (`sheet.signets`, sinon ceux du PDF de plans qui visent sa page)."""
    out = pymupdf.open(plans_pdf)
    orig_toc = out.get_toc(simple=False)
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
    out.set_toc([])                          # reconstruits feuille par feuille ci-dessous (orig_toc)

    toc, report = [], []
    pos = 0
    for sh in sheets:
        plan = out[pos]
        fams = sh.families()
        # un calque par famille ET par feuille, puis le calque légende de la feuille (gold : 344 + 26 = 370 ;
        # panneau des calques : familles dans l'ordre de la légende, puis la légende)
        layers = {f.code: out.add_ocg(f"RELEVE {f.code} - {f.materiel}", on=True) for f in fams}
        legend_oc = out.add_ocg(S.LEGEND_LAYER, on=True)
        box = annotate_page(plan, sh, S.RENVOI_PAGE, layers, legend_oc)
        add = add_bordereau if sh.format == "materiel" else add_bordereau_agrege
        bpages = add(out, sh, plan.rect.width, plan.rect.height, at=pos + 1, layers=layers, legend_oc=legend_oc)
        titre = titre_signet(sh)
        toc.append([1, titre, pos + 1])
        origine = sh.signets if sh.signets is not None else signets_de_page(orig_toc, sh.page)
        toc += [[lvl + 1, t, pos + 1 if p == 1 else -1] for lvl, t, p in origine]
        report.append({"sheet": sh.name, "format": sh.format, "plan_page": pos + 1, "bordereau_pages": [p + 1 for p in bpages],
                       "reperes": len(sh.items), "familles": len(fams), "res": sh.n_reserves,
                       "box": [round(v, 1) for v in box.rect], "box_layout": [box.ncols, box.col_w, box.pitch],
                       "box_in_free_space": box.fits, "bordereau_troncatures": sh.troncatures,
                       "encadre": "v6" if encadre_v6(sh) else "standard",
                       "calques": len(layers) + 1, "signet": titre, "signets_origine": len(origine)})
        log(f"{sh.name}: {len(sh.items)} reperes / {len(fams)} familles / RES {sh.n_reserves} "
            f"-> page {pos + 1} + bordereau {len(bpages)} p." + ("" if box.fits else " (box overlaps drawing)"))
        pos = bpages[-1] + 1
    out.set_toc(toc)
    out_pdf = Path(out_pdf)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    # garbage=2, pas 3 : le niveau 3 fusionne les objets identiques, donc les calques de même nom des
    # différentes feuilles (26 x « RELEVE - Legende et avertissements ») en un seul — le gold en garde un par feuille
    out.save(out_pdf, garbage=2, deflate=True)
    pages = out.page_count
    out.close()                              # libère plans_pdf tout de suite (sans attendre le ramasse-miettes)
    return {"pages": pages, "sheets": report}


__all__ = ["render", "load_input"]
