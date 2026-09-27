"""Ground truth (M. Dupuis' reference takeoffs) placed on the pages of the
ORIGINAL bid-package plan PDFs, through `src/estimer/data/plan_index.json`
(built by `python -m src.estimer.plan_index`).

Inputs, per dossier `<root>/<S>/`:
  entree/plans-originaux/*.pdf      original vector PDFs (never `Plans-annotes.pdf`)
  reference/*Dupuis*.qpl            estimator's Plan Expert project (position gold)
  reference/dupuis-png-dimensions.txt   size of the rasters he marked
  reference/feuilles-ia.csv         IA sheet -> (pdf, page) — only used to place the
                                    marks that cannot be placed directly (below)
  planexpert/<S>.qpl                the other (automatic) takeoff — only used for
                                    the label -> family co-location votes and for
                                    the registration of the remainder
  reference-quantites.csv           count-only gold (S-1857: no Dupuis .qpl)

Placement of a Dupuis mark (PNG pixel of his raster) on a page raster
(WORK_WIDTH = 2997 px wide render of the PDF page):
1. DIRECT (default): his plan is paired to a PDF page by the index (plan name
   `<pdf> - n` / `<pdf>-page-000n`, aspect ratio checked) and his raster size is
   known -> x * page_w / png_w, y * page_h / png_h. Nothing from any other
   takeoff enters these coordinates.
2. REGISTERED (remainder, flagged in the notes): his raster size is unknown
   (JPG exports absent from the dimensions file) or his plan is a page of a
   document that is not in plans-originaux (S-1844: the electrical sheets inside
   the global bid set). `src.validation.compare_qpl` registers such pages
   geometrically on the other takeoff's rasters (scale + translation), and
   feuilles-ia.csv gives the PDF page of that raster. The registration is a
   global similarity per page; it moves no individual mark.
3. Otherwise the mark is counted as unplaced (its family still enters the
   "all estimator marks" totals).
Two Dupuis plans on the same PDF page (he imported some pages twice) are merged;
the second copy's marks that fall within DUP_RADIUS px of a mark of the first
copy are duplicates and dropped (compare_qpl's rule, one-to-one assignment).
Marks on an original sheet and on its addendum re-issue are BOTH kept: both
pages are in the input and the detector sees both.

Several PDFs per dossier are concatenated (page order = index order) into one
cached PDF so the pipeline runs unchanged; the mapping is kept in the notes.
"""
from __future__ import annotations

import csv
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pymupdf
from scipy.optimize import linear_sum_assignment

from src.qpl.normalisation import canonique
from src.validation import compare_qpl as C

from . import conduits as K
from .families import INDETERMINE, keyword_family
from .gold import (DATA_ROOT, DossierGold, GoldLine, GoldMark, SheetInfo, _dupuis_scales, _read_csv,
                   counter_styles, paper_to_feet)
from .pages import WORK_WIDTH

INDEX_JSON = Path(__file__).resolve().parent / "data" / "plan_index.json"
DEFAULT_CACHE = Path("/home/claude/data/dossiers/_cache-plans-originaux")
DUP_RADIUS_FRACTION = 0.012        # compare_qpl SEUIL_MARQUE: 1.2 % of the page diagonal
ASPECT_TOL = 0.02


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).upper().strip()


def load_index(path: Path = INDEX_JSON) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ pages
def pdfs_with_plans(idx: dict) -> list[str]:
    """PDFs of plans-originaux that hold at least one paired reference plan, index order."""
    used = {p["pdf"] for p in idx["plans"] if p.get("pdf")}
    return [f for f in idx["pdfs"] if f in used]


def page_table(idx: dict) -> list[dict]:
    """One row per page of the evaluated (possibly concatenated) PDF, in order."""
    keep = pdfs_with_plans(idx)
    rows = [p for f in keep for p in idx["pages"] if p["pdf"] == f]
    rows.sort(key=lambda p: (keep.index(p["pdf"]), p["page"]))
    return rows


def concatenated_pdf(idx: dict, pdf_dir: Path, cache_dir: Path) -> tuple[Path, list[tuple[str, int]]]:
    """The PDF the pipeline reads: the single original when the dossier has one,
    else a cached concatenation. Returns (path, [(pdf, page 1-based)] per page)."""
    keep = pdfs_with_plans(idx)
    order = [(p["pdf"], p["page"]) for p in page_table(idx)]
    if len(keep) == 1:
        return pdf_dir / keep[0], order
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / f"{idx['dossier']}-plans-originaux.pdf"
    stamp = cache_dir / f"{idx['dossier']}-plans-originaux.json"
    want = {"pdfs": keep, "sha256": {f: idx["pdf_sha256"][f] for f in keep}, "pages": order}
    if out.is_file() and stamp.is_file() and json.loads(stamp.read_text(encoding="utf-8")) == want:
        return out, order
    doc = pymupdf.open()
    for f in keep:
        src = pymupdf.open(pdf_dir / f)
        doc.insert_pdf(src)
        src.close()
    doc.save(out, garbage=1, deflate=True)
    doc.close()
    stamp.write_text(json.dumps(want, ensure_ascii=False, indent=1), encoding="utf-8")
    return out, order


def sheet_table(idx: dict) -> list[SheetInfo]:
    rows = page_table(idx)
    seen: Counter = Counter()
    out = []
    for i, p in enumerate(rows):
        disp = p.get("sheet") or f"P{i + 1}"
        seen[disp] += 1
        if seen[disp] > 1:
            disp = f"{disp}_{seen[disp]}"
        w_pt, h_pt = float(p["width_pt"]), float(p["height_pt"])
        kind = "legende" if p.get("legend_page") else "plan"
        out.append(SheetInfo(disp, disp, i, kind, K.parse_scale(p.get("scale") or ""), w_pt,
                             float(WORK_WIDTH), WORK_WIDTH * h_pt / w_pt))
    return out


# ------------------------------------------------------------------ marks
def dedupe(first_xy: np.ndarray, second_xy: np.ndarray, radius: float) -> np.ndarray:
    """Boolean mask over `second_xy`: True = duplicate of a mark of `first_xy`
    (optimal one-to-one assignment within `radius`)."""
    dup = np.zeros(len(second_xy), bool)
    if not len(first_xy) or not len(second_xy):
        return dup
    d = np.hypot(second_xy[:, None, 0] - first_xy[None, :, 0], second_xy[:, None, 1] - first_xy[None, :, 1])
    big = 1e9
    cost = np.where(d <= radius, d, big)
    r, c = linear_sum_assignment(cost)
    dup[r[cost[r, c] < big]] = True
    return dup


def _comparison(dossier_dir: Path, ref: Path):
    """compare_qpl comparison of the Dupuis project with the other takeoff (label votes,
    geometric registration of the remainder). None when the other takeoff is missing."""
    s = dossier_dir.name
    ia_qpl = dossier_dir / "planexpert" / f"{s}.qpl"
    fi = dossier_dir / "reference" / "feuilles-ia.csv"
    if not ia_qpl.is_file() or not fi.is_file():
        return None, {}
    humains = C.lire_qpl(ref, "humain")
    ias = C.lire_qpl(ia_qpl, "ia")
    C.filtrer_rebut(humains, canonique)
    C.filtrer_rebut(ias, canonique)
    C.preparer_humain(humains, C.lire_dimensions(dossier_dir / "reference" / "dupuis-png-dimensions.txt", s))
    feuilles = C.lire_feuilles(fi)
    anomalies = C.preparer_ia(ias, feuilles, None)
    return C.comparer(humains, ias, anomalies), feuilles


def load_position_gold(dossier_dir: Path, idx: dict, cache_dir: Path) -> DossierGold:
    s = dossier_dir.name
    ref = dossier_dir / Path(idx["reference_qpl"]).relative_to(s)
    pdf_dir = dossier_dir / "entree" / "plans-originaux"
    pdf, order = concatenated_pdf(idx, pdf_dir, cache_dir)
    sheets = sheet_table(idx)
    page_of = {(f, n): i for i, (f, n) in enumerate(order)}
    gold = DossierGold(s, pdf, sheets)
    gold.styles = counter_styles(ref)
    gold.notes.append(f"input: {', '.join(pdfs_with_plans(idx))} ({len(sheets)} pages"
                      + (", concatenated)" if len(pdfs_with_plans(idx)) > 1 else ")"))

    humains = C.lire_qpl(ref, "humain")
    rebut = C.filtrer_rebut(humains, canonique)
    if rebut:
        gold.notes.append(f"{rebut} Dupuis marks with junk labels removed (normalisation.json rebut list)")
    plan_by_name = {p.nom: p for p in humains}
    scales = _dupuis_scales(ref)

    comp, feuilles = _comparison(dossier_dir, ref)
    for feuille, row in feuilles.items():
        try:
            pg = page_of.get((row["fichier"], int(row["page"])))
        except (KeyError, ValueError):
            pg = None
        if pg is not None:
            gold.ia_sheet_page[feuille] = pg
    if comp is not None:
        for res in comp.resultats[C.SEUIL_MARQUE].values():
            for c in res.couples:
                gold.label_map.add_vote(c.humain.marque.libelle, keyword_family(c.ia.libelle))

    # 1. direct placement
    direct_plans: set[str] = set()
    per_page_xy: dict[int, list[np.ndarray]] = defaultdict(list)
    n_direct = n_dup = 0
    for pm in idx["plans"]:
        plan = plan_by_name.get(pm["name"])
        if plan is None or pm.get("pdf") is None or not pm.get("png_size"):
            continue
        pg = page_of.get((pm["pdf"], pm["page"]))
        if pg is None:
            continue
        sh = sheets[pg]
        png_w, png_h = pm["png_size"]
        if abs((png_w / png_h) / (sh.page_width_px / sh.page_height_px) - 1) > ASPECT_TOL:
            gold.notes.append(f"{pm['name']}: raster aspect {png_w / png_h:.3f} differs from page "
                              f"{sh.page_width_px / sh.page_height_px:.3f}; placed by registration instead")
            continue
        direct_plans.add(plan.nom)
        kx, ky = sh.page_width_px / png_w, sh.page_height_px / png_h
        xy = np.array([(m.x * kx, m.y * ky) for m in plan.marques], float).reshape(-1, 2)
        keep = np.ones(len(xy), bool)
        if per_page_xy[pg]:
            radius = DUP_RADIUS_FRACTION * np.hypot(sh.page_width_px, sh.page_height_px)
            keep = ~dedupe(np.concatenate(per_page_xy[pg]), xy, radius)
            n_dup += int((~keep).sum())
        for m, (x, y), k in zip(plan.marques, xy, keep):
            if not k:
                continue
            if not (0 <= x < sh.page_width_px and 0 <= y < sh.page_height_px):
                gold.unplaced[gold.label_map.family(m.libelle)] += 1
                continue
            gold.marks.append(GoldMark(pg, float(x), float(y), m.libelle, gold.label_map.family(m.libelle)))
            n_direct += 1
        if len(xy):
            per_page_xy[pg].append(xy[keep])
        # his conduit lines, converted with his own scale
        value, typ = scales.get(plan.nom, (0.0, 0))
        dpi = png_w / (sh.paper_width_pt / 72.0) if sh.paper_width_pt else None
        for ln in plan.lignes:
            ft = paper_to_feet(ln.longueur_px / dpi, value, typ) if (dpi and value > 0) else None
            gold.lines.append(GoldLine(pg, ln.libelle, ln.longueur_px * kx, ft))

    # 2. remainder through the compare_qpl registration on the other takeoff's rasters
    n_reg = n_reg_dup = 0
    reg_pages: Counter = Counter()
    handled: set[str] = set()
    remaining = {p.nom for p in humains if p.marques} - direct_plans
    if remaining and comp is not None:
        ia_by_sheet = comp.ia_par_feuille()
        for feuille, recalees in comp.humaines_par_feuille.items():
            ia = ia_by_sheet.get(feuille)
            row = feuilles.get(feuille)
            if ia is None or row is None or not ia.largeur:
                continue
            try:
                pg = page_of.get((row["fichier"], int(row["page"])))
            except (KeyError, ValueError):
                pg = None
            if pg is None:
                continue
            sh = sheets[pg]
            if abs((ia.largeur / ia.hauteur) / (sh.page_width_px / sh.page_height_px) - 1) > ASPECT_TOL:
                gold.notes.append(f"IA raster {feuille} aspect differs from page {sh.display}: not used")
                continue
            kx, ky = sh.page_width_px / ia.largeur, sh.page_height_px / ia.hauteur
            for r in recalees:
                if r.marque.plan not in remaining:
                    continue
                handled.add(r.marque.plan)
                fam = gold.label_map.family(r.marque.libelle)
                if r.doublon_de is not None:
                    n_reg_dup += 1
                    continue
                if r.x_ia is None:
                    gold.unplaced[fam] += 1
                    continue
                x, y = r.x_ia * kx, r.y_ia * ky
                if not (0 <= x < sh.page_width_px and 0 <= y < sh.page_height_px):
                    gold.unplaced[fam] += 1
                    continue
                gold.marks.append(GoldMark(pg, float(x), float(y), r.marque.libelle, fam))
                n_reg += 1
                reg_pages[(r.marque.plan, sh.display)] += 1
        for p in remaining - handled:
            for m in plan_by_name[p].marques:
                gold.unplaced[gold.label_map.family(m.libelle)] += 1
    elif remaining:
        for p in remaining:
            for m in plan_by_name[p].marques:
                gold.unplaced[gold.label_map.family(m.libelle)] += 1

    # families are final only now (votes collected above); refresh the direct marks
    for m in gold.marks:
        m.family = gold.label_map.family(m.label)
    gold.notes.append(f"marks placed directly (his raster -> page, no other takeoff involved): {n_direct}"
                      + (f"; duplicates of a page imported twice dropped: {n_dup}" if n_dup else ""))
    if n_reg or n_reg_dup:
        detail = ", ".join(f"{p} -> {d} ({n})" for (p, d), n in sorted(reg_pages.items()))
        gold.notes.append(f"marks placed through the geometric registration of compare_qpl on the other "
                          f"takeoff's rasters (raster size unknown or document absent from plans-originaux): "
                          f"{n_reg}" + (f", {n_reg_dup} duplicates dropped" if n_reg_dup else "") + f" — {detail}")
    if gold.unplaced:
        gold.notes.append(f"estimator marks that cannot be placed on any input page: {sum(gold.unplaced.values())}")
    return gold


def load_count_gold(dossier_dir: Path, idx: dict, cache_dir: Path) -> DossierGold:
    pdf_dir = dossier_dir / "entree" / "plans-originaux"
    pdf, _order = concatenated_pdf(idx, pdf_dir, cache_dir)
    sheets = sheet_table(idx)
    gold = DossierGold(dossier_dir.name, pdf, sheets, has_positions=False)
    for r in _read_csv(dossier_dir / "reference-quantites.csv"):
        try:
            q = int(float(r["quantite"]))
        except (KeyError, ValueError):
            continue
        gold.counts.append((r.get("feuille", "").strip(), r["objet"].strip(), INDETERMINE, q))
    gold.notes.append(f"input: {', '.join(pdfs_with_plans(idx))} ({len(sheets)} pages, concatenated)")
    gold.notes.append("no Dupuis .qpl under reference/ for this dossier: count-only gold = reference-quantites.csv "
                      "(transcription of the estimator's printed takeoff); the index pairs planexpert/"
                      f"{dossier_dir.name}.qpl (the automatic takeoff, NOT a reference) to the pages — it is not "
                      "used as gold")
    return gold


def load(dossier: str, root: Path = DATA_ROOT, index_path: Path = INDEX_JSON,
         cache_dir: Path = DEFAULT_CACHE) -> DossierGold:
    idx = load_index(index_path)[dossier]
    d = root / dossier
    if idx.get("reference_kind") == "dupuis":
        return load_position_gold(d, idx, cache_dir)
    if (d / "reference-quantites.csv").is_file():
        return load_count_gold(d, idx, cache_dir)
    raise FileNotFoundError(f"{dossier}: no Dupuis reference and no reference-quantites.csv")
