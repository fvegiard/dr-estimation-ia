"""Load the estimator's (M. Dupuis) reference takeoffs as ground truth placed
on the pages of a dossier's plan PDF.

Default source (`load(..., source="original")`): the original bid-package PDFs,
see gold_original.py. What follows describes the legacy `source="annotes"` path
on the annotated renders (kept for comparison; never the input of new runs).

Position gold (dossiers with `reference/*Dupuis*.qpl`):
  Dupuis marks are pixels of his own PNG rasters (8051-13012 px wide). The
  only plan images available for these dossiers are `Plans-annotes.pdf`
  (one 2997 px wide raster page per sheet). Dupuis pages are registered to
  sheets with `src.validation.compare_qpl` (page pairing + scale/translation
  registration, already used for the published comparisons), then scaled from
  the sheet raster to the page raster. Duplicate marks (same device marked
  twice on an original + addendum page) are dropped exactly as compare_qpl
  drops them.

Count gold (dossiers with only `reference-quantites.csv` transcribed from the
estimator's printed takeoff, e.g. S-1857): label, quantity, sheet — no
positions, used for count-error metrics only.

`Plans-annotes.pdf` page order is reproduced from `releve/render_pdf.py`:
sorted sheet names whose type is "plan" or that carry marks.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from src.qpl.normalisation import canonique
from src.validation import compare_qpl as C

from .families import INDETERMINE, LabelFamilyMap, keyword_family

DATA_ROOT = Path("/home/claude/data/dossiers")
POSITION_DOSSIERS = ("S-1714", "S-1715", "S-1769", "S-1811", "S-1844")
COUNT_DOSSIERS = ("S-1857",)
ALL_DOSSIERS = POSITION_DOSSIERS + COUNT_DOSSIERS


@dataclass
class GoldMark:
    page: int
    x: float
    y: float
    label: str
    family: str = INDETERMINE


@dataclass
class SheetInfo:
    name: str             # AI sheet id (feuilles-classement)
    display: str          # sheet number read in the title block (E401 ...)
    page: int             # 0-based page in Plans-annotes.pdf
    kind: str             # plan / legende / schema / ...
    scale_ratio: float | None   # real / paper (96 = 1/8" = 1'-0"), from feuilles-classement
    paper_width_pt: float | None
    page_width_px: float
    page_height_px: float


@dataclass
class GoldLine:
    page: int
    name: str
    length_px_page: float        # total length in page pixels
    length_ft: float | None      # Dupuis' own scale, None when he set none


@dataclass
class DossierGold:
    dossier: str
    pdf: Path
    sheets: list[SheetInfo]
    marks: list[GoldMark] = field(default_factory=list)
    lines: list[GoldLine] = field(default_factory=list)
    # marks Dupuis placed on pages that are not in the PDF (sheet absent / page unpaired)
    unplaced: Counter = field(default_factory=Counter)        # family -> n
    # count-only gold: (sheet display name or "", label, family, qty)
    counts: list[tuple[str, str, str, int]] = field(default_factory=list)
    has_positions: bool = True
    label_map: LabelFamilyMap = field(default_factory=LabelFamilyMap)
    styles: dict[str, tuple[int, int, int]] = field(default_factory=dict)   # label -> (Shape, DefaultSize, Color)
    notes: list[str] = field(default_factory=list)
    # other (automatic) takeoff: its sheet id (feuilles-ia.csv) -> page of `pdf`; empty = match by sheet name
    ia_sheet_page: dict[str, int] = field(default_factory=dict)

    def page_of_display(self) -> dict[str, int]:
        return {s.display: s.page for s in self.sheets}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _display_name(row: dict[str, str]) -> str:
    m = re.search(r"cartouche\s*=\s*([A-Za-z]{1,3}-?\d{2,4}[A-Za-z]?)", row.get("note") or "")
    return m.group(1).upper().replace("-", "") if m else row["feuille"]


def _scale_ratio(txt: str) -> float | None:
    try:
        v = float((txt or "").replace(",", "."))
    except ValueError:
        return None
    return v if v > 0 else None


def sheet_table(dossier_dir: Path) -> list[SheetInfo]:
    """Sheets of Plans-annotes.pdf in page order (render_pdf.py rule)."""
    s = dossier_dir.name
    cls = {r["feuille"]: r for r in _read_csv(dossier_dir / "feuilles-classement.csv")}
    ia_qpl = dossier_dir / "planexpert" / f"{s}.qpl"
    marked: set[str] = set()
    if ia_qpl.is_file():
        for plan in C.lire_qpl(ia_qpl, "ia"):
            if plan.marques:
                marked.add(Path(plan.fichier).stem if plan.fichier else plan.nom)
    names = sorted(f for f in cls if cls[f].get("type", "").strip() == "plan" or f in marked)
    widths: dict[str, float] = {}
    fi = dossier_dir / "reference" / "feuilles-ia.csv"
    if fi.is_file():
        for r in _read_csv(fi):
            try:
                widths[r["feuille"]] = float(r["largeur_pt"])
            except (KeyError, ValueError):
                pass
    doc = pymupdf.open(dossier_dir / "Plans-annotes.pdf")
    if doc.page_count != len(names):
        raise ValueError(f"{s}: Plans-annotes.pdf has {doc.page_count} pages, sheet rule gives {len(names)}")
    seen: Counter = Counter()
    out = []
    for i, f in enumerate(names):
        disp = _display_name(cls[f])
        seen[disp] += 1
        if seen[disp] > 1:
            disp = f"{disp}_{seen[disp]}"
        r = doc[i].rect
        out.append(SheetInfo(f, disp, i, cls[f].get("type", "").strip(), _scale_ratio(cls[f].get("echelle", "")),
                             widths.get(f), float(r.width), float(r.height)))
    return out


def _dupuis_scales(path: Path) -> dict[str, tuple[float, int]]:
    """Plan Name -> (Scale Value, Type) of the Dupuis project (0 = no scale)."""
    root = C._lire_racine(path)
    out = {}
    for plan in root.findall("./Plans/Plan"):
        sc = plan.find("Scale")
        if sc is None:
            continue
        try:
            v = float((sc.get("Value") or "0").replace(",", "."))
            t = int(sc.get("Type") or "0")
        except ValueError:
            continue
        out[plan.get("Name", "")] = (v, t)
    return out


def counter_styles(path: Path) -> dict[str, tuple[int, int, int]]:
    """Counter Name -> (Shape, DefaultSize, Color) as the estimator drew it."""
    out = {}
    for c in C._lire_racine(path).iter("Counter"):
        try:
            out[(c.get("Name") or "").strip()] = (int(c.get("Shape") or 0), int(float(c.get("DefaultSize") or 20)),
                                                  int(c.get("Color") or 0))
        except ValueError:
            continue
    return out


def paper_to_feet(length_paper_in: float, value: float, typ: int) -> float | None:
    """Plan Expert scale: Type 1 = imperial, Value inches of paper per foot;
    Type 0 = metric 1:Value."""
    if value <= 0:
        return None
    if typ == 1:
        return length_paper_in / value
    return length_paper_in * value / 12.0


def load_position_gold(dossier_dir: Path) -> DossierGold:
    s = dossier_dir.name
    ref = next(iter(sorted((dossier_dir / "reference").glob("*Dupuis*.qpl"))))
    sheets = sheet_table(dossier_dir)
    by_name = {sh.name: sh for sh in sheets}
    humains = C.lire_qpl(ref, "humain")
    ias = C.lire_qpl(dossier_dir / "planexpert" / f"{s}.qpl", "ia")
    rebut = C.filtrer_rebut(humains, canonique)
    C.filtrer_rebut(ias, canonique)
    C.preparer_humain(humains, C.lire_dimensions(dossier_dir / "reference" / "dupuis-png-dimensions.txt", s))
    anomalies = C.preparer_ia(ias, C.lire_feuilles(dossier_dir / "reference" / "feuilles-ia.csv"), None)
    comp = C.comparer(humains, ias, anomalies)
    gold = DossierGold(s, dossier_dir / "Plans-annotes.pdf", sheets)
    gold.styles = counter_styles(ref)
    if rebut:
        gold.notes.append(f"{rebut} Dupuis marks with junk labels removed (normalisation.json rebut list)")

    # Co-location votes: human label <- keyword family of the co-located other-takeoff label.
    for res in comp.resultats[C.SEUIL_MARQUE].values():
        for c in res.couples:
            gold.label_map.add_vote(c.humain.marque.libelle, keyword_family(c.ia.libelle))

    ia_by_sheet = comp.ia_par_feuille()
    for feuille, recalees in comp.humaines_par_feuille.items():
        sh = by_name.get(feuille)
        ia = ia_by_sheet[feuille]
        for r in recalees:
            if r.doublon_de is not None:
                continue
            fam = gold.label_map.family(r.marque.libelle)
            if sh is None or r.x_ia is None or not ia.largeur:
                gold.unplaced[fam] += 1
                continue
            kx = sh.page_width_px / ia.largeur
            ky = sh.page_height_px / ia.hauteur
            x, y = r.x_ia * kx, r.y_ia * ky
            if not (0 <= x < sh.page_width_px and 0 <= y < sh.page_height_px):
                gold.unplaced[fam] += 1
                continue
            gold.marks.append(GoldMark(sh.page, x, y, r.marque.libelle, fam))
    for m in comp.manquantes_hors_page:
        gold.unplaced[gold.label_map.family(m.libelle)] += 1

    # Lines: total length per Dupuis page, converted with his own scale.
    scales = _dupuis_scales(ref)
    for paire in comp.pages.paires:
        h = paire.humain
        if not h.lignes or paire.feuille is None or paire.transfo is None:
            continue
        sh = by_name.get(paire.feuille)
        ia = ia_by_sheet.get(paire.feuille)
        if sh is None or ia is None or not ia.largeur or not h.largeur:
            continue
        k_page = (sh.page_width_px / ia.largeur) * paire.transfo.echelle
        value, typ = scales.get(h.nom, (0.0, 0))
        for ln in h.lignes:
            ft = None
            if value > 0 and sh.paper_width_pt:
                dpi = h.largeur / (sh.paper_width_pt / 72.0)
                ft = paper_to_feet(ln.longueur_px / dpi, value, typ)
            gold.lines.append(GoldLine(sh.page, ln.libelle, ln.longueur_px * k_page, ft))
    return gold


def load_count_gold(dossier_dir: Path) -> DossierGold:
    sheets = sheet_table(dossier_dir)
    gold = DossierGold(dossier_dir.name, dossier_dir / "Plans-annotes.pdf", sheets, has_positions=False)
    for r in _read_csv(dossier_dir / "reference-quantites.csv"):
        try:
            q = int(float(r["quantite"]))
        except (KeyError, ValueError):
            continue
        lab = r["objet"].strip()
        gold.counts.append((r.get("feuille", "").strip(), lab, INDETERMINE, q))
    gold.notes.append("count-only gold: reference-quantites.csv (transcription of the estimator's printed takeoff)")
    return gold


GOLD_SOURCES = ("original", "annotes")


def load(dossier: str, root: Path = DATA_ROOT, source: str = "original") -> DossierGold:
    """`source="original"`: the estimator's marks placed on the ORIGINAL bid-package
    PDFs through src/estimer/data/plan_index.json (gold_original.py, the default);
    `source="annotes"`: the legacy path on the annotated renders `Plans-annotes.pdf`."""
    if source == "original":
        from . import gold_original
        return gold_original.load(dossier, root)
    if source != "annotes":
        raise ValueError(f"unknown gold source {source!r} (expected one of {GOLD_SOURCES})")
    d = root / dossier
    if list((d / "reference").glob("*Dupuis*.qpl")) if (d / "reference").is_dir() else []:
        return load_position_gold(d)
    if (d / "reference-quantites.csv").is_file():
        return load_count_gold(d)
    raise FileNotFoundError(f"{dossier}: no Dupuis reference")


def finalize_count_families(gold: DossierGold, label_map: LabelFamilyMap) -> None:
    """Families of count-only gold labels, with a label map learnt elsewhere."""
    gold.counts = [(sh, lab, label_map.family(lab), q) for sh, lab, _f, q in gold.counts]
