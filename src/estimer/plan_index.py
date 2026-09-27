"""Inventory of the ORIGINAL bid-package plan PDFs and mapping of every
Plan Expert reference plan (Dupuis `.qpl`, `<Plan FileName=...>`) to a page of
those PDFs.

Inputs (per dossier, under DATA_ROOT/<S>/):
  entree/plans-originaux/*.pdf      original vector PDFs (never the annotated renders)
  reference/*Dupuis*.qpl            estimator's takeoff (gold); S-1857 has none ->
                                    planexpert/S-1857*.qpl is used and flagged
  reference/dupuis-png-dimensions.txt   `project|png name|width|height` of the
                                    rasters Dupuis marked (used to check the pairing)

Outputs:
  <repo>/dossiers/<S>/entree/plans-originaux/INDEX.md    human index (one per dossier)
  <repo>/src/estimer/data/plan_index.json                machine index (all dossiers)

Everything is computed from the PDFs: sheet number, title and scale are read in
the title block of the text layer (words mapped through the page rotation so the
title block is really the displayed bottom-right corner); pages whose title
block carries no text (fonts drawn as outlines) are OCR'd with tesseract on a
render of the title block, and that is flagged (`sheet_source`).

Pairing rule (same as src.validation.compare_qpl): a reference plan named
`<PDF stem> - <n>[ (k)]` or `<PDF stem>[-unlocked]-page-000nn` is page n of the
PDF whose stem matches (accents/case ignored). The pairing is then checked
against the raster aspect ratio Dupuis worked on. Plans whose stem matches no
PDF in plans-originaux are reported unmatched, with their mark counts, so the
reader knows how much gold cannot be placed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pymupdf

from src.validation.compare_qpl import analyser_nom_humain, lire_dimensions, normaliser_nom

DATA_ROOT = Path("/home/claude/data/dossiers")
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOSSIERS = ("S-1714", "S-1715", "S-1769", "S-1811", "S-1844", "S-1857")

SHEET_NO = re.compile(r"^[A-Z]{1,2}-?\d{2,4}[A-Z]?$")
# S-1811 (DND): "L-S267-1302-01-" followed by "404B" in a separate word
DWG_PREFIX = re.compile(r"^[A-Z]-S\d{3}-\d{4}-\d{2}-$")
DWG_SUFFIX = re.compile(r"^\d{3}[A-Z]?$")
SCALE_PATTERNS = [
    re.compile(r"\b1\s*[:/]\s*\d{2,4}\b"),
    re.compile(r"\d+(?:/\d+)?\s*\"\s*=\s*\d+'\s*-?\s*\d*\"?"),
    re.compile(r"\b(?:AUCUNE|N\.?A\.?E\.?|N\.?T\.?S\.?|INDIQUÉE|INDIQUEE|AS SHOWN|AS NOTED|SANS ÉCHELLE|SANS ECHELLE)\b", re.I),
]
LEGEND_WORDS = ("LÉGENDE", "LEGENDE", "LEGEND", "SYMBOLE", "SYMBOLS", "SYMBOLES")
TITLE_LABELS = ("DRAWING TITLE", "TITRE DU DESSIN", "TITRE DU PLAN", "SUBJECT | SUJET", "TITRE:", "TITRE :", "TITRE", "TITLE")
STOP_LABELS = ("DISCIPLINE", "CONÇU PAR", "PRÉPARÉ PAR", "DESSINÉ PAR", "ÉCHELLE", "ECHELLE", "SCALE",
               "PRODUCTION", "REVIEWED", "DATE", "NO DE PROJET", "DOSSIER", "PLAN NO", "PLAN:", "SCEAU",
               "SCEAUX", "WWW.", "DESSIN NO", "PAGE", "CONTROL NO", "DESSINÉ PAR", "DESSINE PAR",
               "VÉRIFIÉ", "VERIFIE", "APPROUVÉ", "TITRE DU PROJET", "PROJET", "PROJECT", "CLIENT", "AUTODESK",
               "DOCS://", "DWG. NO", "NO. DESSIN")
MIN_TEXT_CHARS = 300


@dataclass
class PageInfo:
    pdf: str
    page: int                    # 1-based
    width_pt: float              # displayed (rotation applied)
    height_pt: float
    rotation: int
    chars: int
    text_layer: str              # yes / partial / no
    vectors: int                 # len(page.get_cdrawings())
    images: int
    sheet: str | None            # E101, T000, L-S267-1302-01-505B ...
    sheet_short: str | None      # last token of a DND drawing number (505B), else = sheet
    sheet_source: str            # text / dwg / ocr / none
    title: str | None
    scale: str | None            # title-block scale
    scales_on_page: list[str]
    legend_page: bool
    legend_evidence: str | None
    sheet_list: list[list[str]]  # [sheet, description] rows when the page is a sheet list / cover
    ocr_text: str | None         # full-page OCR (image-only pages), truncated
    title_block_text: str


@dataclass
class PlanMatch:
    name: str
    file_name: str
    marks: int
    lines: int
    png_size: list[int] | None
    pdf: str | None
    page: int | None
    sheet: str | None
    method: str                  # name / sheet / none
    check: str                   # aspect ratio check or reason when unmatched
    prior_sheet: str | None = None   # feuille_ia of the earlier compare_qpl pairing (comparaison-dupuis-qpl/pages.csv)
    prior_method: str | None = None
    prior_score: float | None = None
    prior_agrees: bool | None = None # title-block sheet == prior feuille_ia (None when not comparable)
    geometry_hint: str | None = None # unmatched plans: sheet the earlier geometric registration found


@dataclass
class DossierIndex:
    dossier: str
    reference_qpl: str
    reference_kind: str          # dupuis / planexpert-ia
    pdfs: list[str]
    pdf_sha256: dict[str, str]
    pages: list[PageInfo]
    plans: list[PlanMatch]
    unmatched: list[PlanMatch] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


# --- text helpers -------------------------------------------------------------

def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).upper()


def displayed_words(page: pymupdf.Page) -> list[tuple[float, float, float, float, str, float]]:
    """(x0, y0, x1, y1, text, font_size) in displayed coordinates."""
    m = page.rotation_matrix
    out = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                txt = sp["text"].strip()
                if not txt:
                    continue
                r = pymupdf.Rect(sp["bbox"]) * m
                out.append((r.x0, r.y0, r.x1, r.y1, txt, float(sp["size"])))
    return out


def title_block_words(words, w: float, h: float):
    return [t for t in words if t[0] >= 0.72 * w and t[1] >= 0.62 * h]


def reading_order(words):
    return sorted(words, key=lambda t: (round(t[1] / 6), t[0]))


def find_sheet(tb_words) -> tuple[str | None, str]:
    """Sheet number in the title block: largest font among sheet-number-like
    tokens; DND style `L-S267-1302-01-` + `404B` handled explicitly."""
    tokens = []
    for x0, y0, x1, y1, txt, size in tb_words:
        for tok in txt.split():
            tokens.append((x0, y0, x1, y1, tok.upper(), size))
    # DND drawing numbers
    for i, t in enumerate(tokens):
        if DWG_PREFIX.match(t[4]):
            for u in tokens:
                if u is not t and DWG_SUFFIX.match(u[4]) and abs(u[1] - t[1]) < 12 and u[0] >= t[0]:
                    return t[4] + u[4], "dwg"
    best = None
    for x0, y0, x1, y1, tok, size in tokens:
        if not SHEET_NO.match(tok):
            continue
        # revision-like tokens "A1", "R0" excluded by requiring >= 3 chars incl. digits >= 2
        key = (size, y0, x0)
        if best is None or key > best[0]:
            best = (key, tok)
    return (best[1], "text") if best else (None, "none")


def ocr_sheet(page: pymupdf.Page) -> tuple[str | None, str, str]:
    """(sheet, source, ocr text of the title block)."""
    r = page.rect
    clip = pymupdf.Rect(r.x0 + 0.72 * r.width, r.y0 + 0.62 * r.height, r.x1, r.y1)
    pix = page.get_pixmap(dpi=200, clip=clip)
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "tb.png"
        pix.save(str(png))
        try:
            txt = subprocess.run(["tesseract", str(png), "-", "--psm", "11"], capture_output=True,
                                 text=True, timeout=120).stdout
        except (OSError, subprocess.TimeoutExpired):
            return None, "ocr-failed", ""
    txt = re.sub(r"\s+", " ", txt).strip()
    cands = [t for t in (_ocr_token(w) for w in re.findall(r"[A-Za-z0-9-]{3,7}", txt)) if t]
    if not cands:
        return None, "ocr-none", txt
    # the sheet number is usually the last one printed (bottom-right cell)
    return cands[-1], "ocr", txt


_OCR_ZERO, _OCR_ONE = "OQ", "IL|"


def _ocr_token(raw: str) -> str | None:
    """Sheet number from an OCR token: fixes O/Q->0 and I/L->1 inside the digit
    part. A token with no real digit at all ("DOIT") is a word, not a sheet."""
    t = raw.upper().replace("-", "")
    if not re.search(r"[0-9]", t) or not t[0].isalpha() or len(t) < 3:
        return None
    prefix = t[0]
    rest = t[1:]
    if rest and rest[0].isalpha() and rest[0] not in _OCR_ZERO + _OCR_ONE:
        prefix, rest = t[:2], t[2:]
    suffix = ""
    if rest and rest[-1].isalpha() and rest[-1] not in _OCR_ZERO + _OCR_ONE:
        suffix, rest = rest[-1], rest[:-1]
    digits = "".join("0" if c in _OCR_ZERO else "1" if c in _OCR_ONE else c for c in rest)
    tok = prefix + digits + suffix
    return tok if (SHEET_NO.match(tok) and digits.isdigit() and len(digits) >= 2) else None


SHEET_LIST_TOKEN = re.compile(r"^[A-Z]{1,2}-?\d{3}[A-Z]?$")
SHEET_LIST_HEADERS = ("LISTE DES DESSINS", "LISTE DES PLANS", "LISTE DES FEUILLES", "DRAWING LIST", "SHEET LIST",
                      "SHEET INDEX", "NO. FEUILLE", "FEUILLE DESCRIPTION", "LIST OF DRAWINGS")


def ocr_page(page: pymupdf.Page, dpi: int = 150) -> str:
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "page.png"
        pix.save(str(png))
        try:
            txt = subprocess.run(["tesseract", str(png), "-", "--psm", "6"], capture_output=True,
                                 text=True, timeout=300).stdout
        except (OSError, subprocess.TimeoutExpired):
            return ""
    return re.sub(r"[ \t]+", " ", txt).replace("£", "E").strip()   # tesseract reads the plotted E as £


def extract_sheet_list(text: str, min_rows: int = 4, require_header: bool = True) -> list[list[str]]:
    """Rows `<sheet> <description>` of a drawing list (cover sheet, "liste des
    dessins"): a sheet-number token starts a row, the words up to the next one
    are its description (trailing revision number / date dropped)."""
    flat = re.sub(r"\s+", " ", _fold(text))
    if require_header and not any(h in flat for h in SHEET_LIST_HEADERS):
        return []
    rows: list[list[str]] = []
    cur: list[str] | None = None
    for tok in text.split():
        t = tok.strip("()|=,.;:").upper()
        if SHEET_LIST_TOKEN.match(t) and (cur is None or len(cur[1]) > 0):
            if cur:
                rows.append(cur)
            cur = [t.replace("-", ""), ""]
        elif cur is not None:
            cur[1] = (cur[1] + " " + tok).strip()
    if cur:
        rows.append(cur)
    cleaned = []
    for sheet, desc in rows:
        desc = re.sub(r"(\s+\S{1,2})?\s+\d{4}-\d{2}-\d{2}.*$", "", desc).strip(" -|=")
        desc = re.sub(r"\s+\d{1,3}$", "", desc).strip(" -|=.")     # row number of the next line (OCR)
        if desc:
            cleaned.append([sheet, desc[:90]])
    if len(cleaned) < min_rows:
        return []
    # one discipline per list: the sheet prefixes must agree (spec pages full of part numbers do not)
    prefixes = Counter(re.match(r"[A-Z]+", r[0]).group(0) for r in cleaned)
    if prefixes.most_common(1)[0][1] < 0.8 * len(cleaned):
        return []
    return cleaned


def find_scale(text: str) -> str | None:
    up = _fold(text)
    for lab in ("ECHELLE:", "ECHELLE :", "ECHELLE", "SCALE"):
        i = up.find(lab)
        while i >= 0:
            seg = text[i + len(lab): i + len(lab) + 60]
            for pat in SCALE_PATTERNS:
                m = pat.search(seg)
                if m:
                    return m.group(0).strip()
            i = up.find(lab, i + 1)
    return None


def scales_anywhere(text: str) -> list[str]:
    found = Counter()
    for pat in SCALE_PATTERNS[:2]:
        for m in pat.finditer(text):
            found[m.group(0).strip()] += 1
    return [f"{k} ×{v}" for k, v in found.most_common(6)]


def find_title(tb_text: str) -> str | None:
    up = _fold(tb_text)
    for lab in TITLE_LABELS:
        i = up.find(_fold(lab))
        if i < 0:
            continue
        seg = tb_text[i + len(lab):].lstrip(" :|")
        segu = _fold(seg)
        cut = len(seg)
        for stop in STOP_LABELS:
            j = segu.find(_fold(stop))
            if 0 < j < cut:
                cut = j
        cand = seg[:cut].strip(" :|-")
        cand = re.sub(r"^[ÉEé]chelle\s*:?\s*(?:1\s*:\s*\d+|NAE|N\.A\.E\.?|AUCUNE)?\s*", "", cand).strip(" :|-")
        cand = re.sub(r"\s*\d?\s*L[ÉE]GENDE DES COULEURS.*$", "", cand, flags=re.I).strip(" :|-")
        cand = re.sub(r"^.*?\(\d{3}\)-?\d{3}-\d{4}\s*", "", cand).strip(" :|-")   # phone/URL line of the firm
        if 3 <= len(cand) <= 120:
            return cand
    return None


def _legend_text(s: str) -> bool:
    u = re.sub(r"L[EÉ]GENDE DES COULEURS", "", _fold(s))
    return any(k in u for k in LEGEND_WORDS)


def legend_check(words, title: str | None) -> tuple[bool, str | None]:
    """Title says legend/symbols, or a short large-font heading does (a
    sentence merely mentioning the legend, or the colour legend of the title
    block, does not count)."""
    if title and _legend_text(title):
        return True, f"title: {title}"
    big = [t for t in words if t[5] >= 11 and len(t[4]) <= 40 and _legend_text(t[4])]
    if big:
        return True, "large-font heading: " + " | ".join(sorted({t[4] for t in big})[:4])
    return False, None


# --- inventory ----------------------------------------------------------------

def inventory_pdf(pdf: Path, rel_name: str, ocr: bool = True) -> list[PageInfo]:
    doc = pymupdf.open(pdf)
    out = []
    for i, page in enumerate(doc):
        r = page.rect
        text = page.get_text()
        words = displayed_words(page)
        tb = reading_order(title_block_words(words, r.width, r.height))
        tb_text = " ".join(t[4] for t in tb)
        sheet, src = find_sheet(tb)
        if sheet is None and ocr:
            sheet, src, ocr_text = ocr_sheet(page)
            if ocr_text:
                tb_text = "OCR: " + ocr_text
        title = find_title(tb_text)
        legend, ev = legend_check(words, title)
        chars = len(text.strip())
        ocr_text = ocr_page(page) if (ocr and chars < 50) else None
        sheet_list = extract_sheet_list(text) or (extract_sheet_list(ocr_text, min_rows=6, require_header=False)
                                                  if ocr_text else [])
        layer = "yes" if (chars >= MIN_TEXT_CHARS and src in ("text", "dwg")) else ("partial" if chars >= 50 else "no")
        if sheet and src != "dwg":
            sheet = sheet.replace("-", "")
        short = sheet.rsplit("-", 1)[-1] if (sheet and src == "dwg") else sheet
        out.append(PageInfo(
            pdf=rel_name, page=i + 1, width_pt=round(r.width, 2), height_pt=round(r.height, 2),
            rotation=page.rotation, chars=chars, text_layer=layer,
            vectors=len(page.get_cdrawings()), images=len(page.get_images()),
            sheet=sheet, sheet_short=short, sheet_source=src, title=title,
            scale=find_scale(tb_text), scales_on_page=scales_anywhere(text),
            legend_page=legend, legend_evidence=ev, sheet_list=sheet_list,
            ocr_text=(ocr_text[:1500] if ocr_text else None), title_block_text=tb_text[:400]))
    return out


# --- reference plans ----------------------------------------------------------

def read_plans(qpl: Path) -> list[dict]:
    root = ET.fromstring(qpl.read_bytes().decode("utf-8-sig"))
    plans = []
    for el in root.findall("./Plans/Plan"):
        marks = sum(len(c.findall("Element")) for c in el.iter("Counter"))
        lines = len(list(el.iter("Line")))
        plans.append({"name": el.get("Name", ""), "file": el.get("FileName", ""), "marks": marks, "lines": lines})
    return plans


def reference_for(dossier: str) -> tuple[Path, str, list[str]]:
    notes = []
    refs = sorted((DATA_ROOT / dossier / "reference").glob("*Dupuis*.qpl")) if (DATA_ROOT / dossier / "reference").exists() else []
    if refs:
        return refs[0], "dupuis", notes
    alt = sorted((DATA_ROOT / dossier / "planexpert").glob(f"{dossier}*.qpl"))
    if alt:
        notes.append(f"NO Dupuis reference QPL under reference/ for {dossier}; using {alt[0].relative_to(DATA_ROOT)} "
                     "(the chain's own Plan Expert project, NOT the estimator's gold). Its plan names are AI sheet "
                     "ids, matched on the title-block sheet number.")
        return alt[0], "planexpert-ia", notes
    raise FileNotFoundError(f"no reference qpl for {dossier}")


def read_prior_pairing(dossier: str) -> dict[str, dict]:
    """Earlier compare_qpl page pairing (name + geometric registration), keyed by human plan name."""
    csv_path = REPO_ROOT / "dossiers" / dossier / "comparaison-dupuis-qpl" / "pages.csv"
    if not csv_path.exists():
        return {}
    import csv
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        return {r["page_humaine"]: r for r in csv.DictReader(fh) if r.get("page_humaine")}


def _same_sheet(a: str | None, b: str | None) -> bool | None:
    if not a or not b or not SHEET_NO.match(b.upper()):
        return None
    return a.upper().replace("-", "") == b.upper().replace("-", "")


def match_plans(dossier: str, plans: list[dict], pages: list[PageInfo], kind: str,
                dims: dict[str, tuple[float, float]]) -> tuple[list[PlanMatch], list[PlanMatch]]:
    prior = read_prior_pairing(dossier)
    by_stem: dict[str, list[PageInfo]] = {}
    for p in pages:
        by_stem.setdefault(normaliser_nom(Path(p.pdf).stem), []).append(p)
    by_sheet: dict[str, list[PageInfo]] = {}
    for p in pages:
        if p.sheet:
            by_sheet.setdefault(p.sheet.upper(), []).append(p)
    matched, unmatched = [], []
    for pl in plans:
        png = dims.get(pl["file"])
        size = [int(png[0]), int(png[1])] if png else None
        hit: PageInfo | None = None
        method, check = "none", ""
        if kind == "dupuis":
            base, num = analyser_nom_humain(pl["name"], pl["file"])
            key = normaliser_nom(base)
            if key in by_stem and num is not None:
                cands = [p for p in by_stem[key] if p.page == num]
                if cands:
                    hit, method = cands[0], "name"
                else:
                    check = f"page {num} out of range ({len(by_stem[key])} pages in {by_stem[key][0].pdf})"
            elif key in by_stem:
                check = "plan name carries no page number"
            else:
                check = f"document '{base}' not in plans-originaux"
        else:
            # AI project: Name is the sheet id read on the title block (E401, E600_2 = first
            # version, E600 + FileName E600_ADD.png = addendum version); FileName may be misnamed.
            sid = re.sub(r"_(ADD|\d)$", "", pl["name"]).upper()
            want_add = "_ADD" in pl["file"].upper()
            cands = by_sheet.get(sid, [])
            if cands:
                adds = [p for p in cands if "ADDENDA" in _fold(p.pdf)]
                pick = adds if want_add else [p for p in cands if p not in adds] or cands
                hit, method = pick[0], "sheet"
            elif sid.endswith("000"):
                covers = [p for p in pages if p.sheet is None and p.sheet_list and p.chars >= MIN_TEXT_CHARS
                          and ("ADDENDA" in _fold(p.pdf)) == want_add]
                if covers:
                    hit, method = covers[0], "cover"
                    check = "cover sheet: no sheet number printed, matched as the page carrying the sheet list"
            if hit is None and not check:
                check = f"no PDF page whose title block reads '{sid}'"
        if hit is not None and not check:
            if png:
                ratio_png = png[0] / png[1]
                ratio_pdf = hit.width_pt / hit.height_pt
                dev = abs(ratio_png - ratio_pdf) / ratio_pdf
                check = f"aspect {ratio_png:.3f} vs pdf {ratio_pdf:.3f} ({'ok' if dev < 0.03 else 'MISMATCH'} {dev * 100:.1f}%)"
            else:
                check = "png size unknown (not in dupuis-png-dimensions.txt)"
        pm = PlanMatch(name=pl["name"], file_name=pl["file"], marks=pl["marks"], lines=pl["lines"], png_size=size,
                       pdf=hit.pdf if hit else None, page=hit.page if hit else None,
                       sheet=hit.sheet if hit else None, method=method, check=check)
        pr = prior.get(pl["name"])
        if pr:
            pm.prior_sheet, pm.prior_method = pr.get("feuille_ia") or None, pr.get("methode") or None
            try:
                pm.prior_score = float(pr["score"]) if pr.get("score") else None
            except ValueError:
                pm.prior_score = None
            if hit is not None:
                pm.prior_agrees = _same_sheet(hit.sheet_short or hit.sheet, pm.prior_sheet)
            elif pm.prior_method == "géométrie" and pm.prior_sheet:
                where = [p for p in pages if (p.sheet_short or p.sheet or "").upper() == pm.prior_sheet.upper()]
                pm.geometry_hint = (f"earlier geometric registration (score {pm.prior_score}) put this raster on sheet "
                                    f"{pm.prior_sheet}" + (f" = {where[0].pdf} p.{where[0].page}" if where else
                                    " (no page of plans-originaux reads that sheet)") +
                                    "; different document, so marks need re-registration, not a page number")
        (matched if hit else unmatched).append(pm)
    return matched, unmatched


# --- outputs ------------------------------------------------------------------

def write_index_md(idx: DossierIndex, path: Path) -> None:
    L = []
    L.append(f"# {idx.dossier} — index des plans originaux\n")
    L.append("Généré par `python -m src.estimer.plan_index` (tout est lu dans les PDF ; rien n'est saisi à la main).\n")
    L.append(f"- Référence : `{idx.reference_qpl}` ({idx.reference_kind})")
    for name in idx.pdfs:
        L.append(f"- PDF : `{name}` — sha256 `{idx.pdf_sha256[name]}`")
    for n in idx.notes:
        L.append(f"- NOTE : {n}")
    L.append("\n## Feuilles (une ligne par page PDF)\n")
    marks_on = Counter()
    for m in idx.plans:
        marks_on[(m.pdf, m.page)] += m.marks
    L.append("| PDF | page | feuille (cartouche) | source | titre | échelle cartouche | texte | vecteurs | images | légende ? | marques réf. |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for p in idx.pages:
        L.append(f"| {p.pdf} | {p.page} | {p.sheet or '—'} | {p.sheet_source} | {(p.title or '—')[:60]} | {p.scale or '—'} "
                 f"| {p.text_layer} ({p.chars}) | {p.vectors} | {p.images} | {'OUI — ' + (p.legend_evidence or '') if p.legend_page else ''} "
                 f"| {marks_on.get((p.pdf, p.page), 0)} |")
    leg = [p for p in idx.pages if p.legend_page]
    L.append("\n## Pages légende / tableau de symboles\n")
    L.extend(f"- {p.pdf} p.{p.page} ({p.sheet or '?'}) — {p.legend_evidence}" for p in leg) if leg else L.append("- aucune détectée")
    lists = [p for p in idx.pages if p.sheet_list]
    L.append("\n## Listes de feuilles trouvées (page couverture / « liste des plans »)\n")
    for p in lists:
        L.append(f"- {p.pdf} p.{p.page} ({'OCR' if p.ocr_text else 'texte'}) : " +
                 "; ".join(f"{a} {b}" for a, b in p.sheet_list))
    if not lists:
        L.append("- aucune")
    L.append("\n## Appariement des plans de la référence → page PDF\n")
    L.append("| Plan (Name) | FileName | marques | lignes | PNG px | → PDF | page | feuille | méthode | contrôle | appariement antérieur (compare_qpl) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for m in idx.plans:
        prior = "—" if not m.prior_sheet else (f"{m.prior_sheet} ({m.prior_method}, {m.prior_score}) "
                 + ("OK" if m.prior_agrees else ("DÉSACCORD" if m.prior_agrees is False else "n/c")))
        L.append(f"| {m.name} | {m.file_name} | {m.marks} | {m.lines} | {('%dx%d' % tuple(m.png_size)) if m.png_size else '?'} "
                 f"| {m.pdf} | {m.page} | {m.sheet or '—'} | {m.method} | {m.check} | {prior} |")
    L.append("\n## Plans de la référence SANS page PDF correspondante\n")
    if idx.unmatched:
        L.append("| Plan (Name) | FileName | marques | lignes | raison | indice |")
        L.append("|---|---|---|---|---|---|")
        for m in idx.unmatched:
            L.append(f"| {m.name} | {m.file_name} | {m.marks} | {m.lines} | {m.check} | {m.geometry_hint or ''} |")
        tot = sum(m.marks for m in idx.unmatched)
        tot_all = tot + sum(m.marks for m in idx.plans)
        L.append(f"\nMarques non plaçables : {tot} / {tot_all} ({(100 * tot / tot_all if tot_all else 0):.1f} %).")
    else:
        L.append("- aucun")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def build(dossier: str, ocr: bool = True) -> DossierIndex:
    src = DATA_ROOT / dossier / "entree" / "plans-originaux"
    pdfs = sorted(src.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"no PDF in {src}")
    pages = []
    for pdf in pdfs:
        pages.extend(inventory_pdf(pdf, pdf.name, ocr=ocr))
    qpl, kind, notes = reference_for(dossier)
    plans = read_plans(qpl)
    dims_file = DATA_ROOT / dossier / "reference" / "dupuis-png-dimensions.txt"
    dims = lire_dimensions(dims_file, dossier) if dims_file.exists() else {}
    matched, unmatched = match_plans(dossier, plans, pages, kind, dims)
    shas = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in pdfs}
    return DossierIndex(dossier=dossier, reference_qpl=str(qpl.relative_to(DATA_ROOT)), reference_kind=kind,
                        pdfs=[p.name for p in pdfs], pdf_sha256=shas, pages=pages, plans=matched,
                        unmatched=unmatched, notes=notes)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dossiers", nargs="+", default=list(DEFAULT_DOSSIERS))
    ap.add_argument("--json", type=Path, default=REPO_ROOT / "src" / "estimer" / "data" / "plan_index.json")
    ap.add_argument("--md-root", type=Path, default=REPO_ROOT / "dossiers",
                    help="INDEX.md goes to <md-root>/<S>/entree/plans-originaux/INDEX.md")
    ap.add_argument("--no-ocr", action="store_true")
    a = ap.parse_args(argv)
    result = {}
    for d in a.dossiers:
        idx = build(d, ocr=not a.no_ocr)
        write_index_md(idx, a.md_root / d / "entree" / "plans-originaux" / "INDEX.md")
        result[d] = asdict(idx)
        print(f"{d}: {len(idx.pages)} pages, {len(idx.plans)} plans matched, {len(idx.unmatched)} unmatched "
              f"({sum(m.marks for m in idx.unmatched)} marks)")
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
