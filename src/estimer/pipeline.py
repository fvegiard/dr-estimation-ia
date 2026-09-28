"""PDF -> SheetResult list (detections, scale, conduit estimate, flags)."""
from __future__ import annotations

import csv
import re
from pathlib import Path

import numpy as np
import pymupdf

from . import conduits as K
from . import legend as L
from . import pages as P
from scipy import ndimage

from .export import (FLAG_MARKUP_PAGE, FLAG_NO_SYMBOL, FLAG_SCALE_UNKNOWN, FLAG_UNREADABLE, SheetResult)
from .model import Model

MARKUP_PAGE_MIN = 0.001        # overlay fraction above which a page is flagged
TAG_MERGE_PX = 40.0            # a legend code this close to a visual detection labels it
ZONE_AREA = (40, 4000)         # px area of a symbol-sized mark-up blob (an unreadable zone)


def unreadable_zones(overlay: np.ndarray) -> int:
    """Symbol-sized blobs of coloured mark-up: places where a symbol may be hidden."""
    lab, n = ndimage.label(overlay)
    if n == 0:
        return 0
    areas = ndimage.sum_labels(np.ones_like(lab, dtype=np.int32), lab, index=np.arange(1, n + 1))
    return int(((areas >= ZONE_AREA[0]) & (areas <= ZONE_AREA[1])).sum())
_SHEET_NO = re.compile(r"^[A-Z]{1,2}-?\d{2,4}[A-Z]?$")


def guess_sheet_number(words: list[tuple], width: float, height: float) -> str | None:
    """Tallest sheet-number-like word in the title-block band (right 25 % or bottom 15 %)."""
    best = None
    for x0, y0, x1, y1, txt in words:
        t = txt.strip().upper()
        if not _SHEET_NO.match(t):
            continue
        if x0 < 0.75 * width and y0 < 0.85 * height:
            continue
        h = y1 - y0
        if best is None or h > best[0]:
            best = (h, t.replace("-", ""))
    return best[1] if best else None


def all_words(doc: pymupdf.Document, indices: list[int]) -> dict[int, list[tuple]]:
    """Text-layer words of every page, in working px (empty for image-only pages)."""
    out = {}
    for i in indices:
        page = doc[i]
        k = P.WORK_WIDTH / page.rect.width
        out[i] = [(w[0] * k, w[1] * k, w[2] * k, w[3] * k, w[4]) for w in page.get_text("words")]
    return out


def merge_tags(dets: list, hits: list[L.TagHit], page_index: int):
    """Legend codes written on the plan: label the nearest visual detection, or add one."""
    from .model import Detection
    free = list(range(len(dets)))
    for h in hits:
        best, bd = None, TAG_MERGE_PX
        for j in free:
            d = np.hypot(dets[j].x - h.x, dets[j].y - h.y)
            if d <= bd:
                best, bd = j, d
        if best is not None:
            d = dets[best]
            d.family, d.source, d.tag, d.family_prob = h.family, "visual+text_tag", h.code, 1.0
            free.remove(best)
        else:
            dets.append(Detection(page_index, h.x, h.y, h.family, 1.0, 1.0, False, "text_tag", h.code))
    return dets


def read_sheets_csv(path: Path | None) -> dict[int, dict]:
    """Optional per-page metadata: page (1-based), name, scale_ratio, paper_width_pt, skip."""
    if path is None:
        return {}
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                out[int(r["page"]) - 1] = r
            except (KeyError, ValueError):
                continue
    return out


def _float(v) -> float | None:
    try:
        f = float(str(v).replace(",", "."))
        return f if f > 0 else None
    except (TypeError, ValueError):
        return None


def run(pdf: Path, model: Model, sheets_csv: Path | None = None, pages: list[int] | None = None,
        keep_gray: bool = True, log=print) -> tuple[list[SheetResult], dict[int, np.ndarray], dict[str, str]]:
    """Returns (sheet results, page rasters for export, legend code -> family)."""
    meta = read_sheets_csv(sheets_csv)
    doc = pymupdf.open(pdf)
    indices = pages if pages is not None else list(range(doc.page_count))
    hits, codes = L.tag_detections(all_words(doc, indices))
    hits_by_page: dict[int, list] = {}
    for h in hits:
        hits_by_page.setdefault(h.page, []).append(h)
    if codes:
        log(f"  legend codes learnt from the text layer: {len(codes)} ({', '.join(sorted(codes)[:12])}...)")
    results: list[SheetResult] = []
    grays: dict[int, np.ndarray] = {}
    for i in indices:
        m = meta.get(i, {})
        if str(m.get("skip", "")).strip().lower() in ("1", "true", "yes", "oui"):
            continue
        page = P.load_page(doc, i)
        h, w = page.shape
        text = " ".join(wd[4] for wd in page.words)
        name = (m.get("name") or "").strip() or guess_sheet_number(page.words, w, h) or f"P{i + 1}"
        ratio = _float(m.get("scale_ratio"))
        scale_source = "sheets-csv" if ratio else ""
        if ratio is None:
            ratio = K.parse_scale(text)
            if ratio:
                scale_source = "text-layer-" + ("imperial" if abs(ratio - round(ratio)) > 0 or ratio in (
                    24, 32, 48, 64, 96, 128, 192, 384) else "metric")
        if ratio and scale_source == "sheets-csv":
            scale_source = "sheets-csv-imperial" if ratio in (24, 32, 48, 64, 96, 128, 192, 384) else "sheets-csv-metric"
        paper = _float(m.get("paper_width_pt")) or (page.width_pt if page.source == "rendered" else None)
        ovf = float(page.overlay.mean())
        sr = SheetResult(i, name, w, h, page.source, ratio, scale_source or "none", paper, ovf)
        sr.detections = merge_tags(model.detect(page), hits_by_page.get(i, []), i)
        if ovf >= MARKUP_PAGE_MIN:
            sr.flags.append(FLAG_MARKUP_PAGE)
            sr.unreadable_zones = unreadable_zones(page.overlay)
            if sr.unreadable_zones:
                sr.flags.append(FLAG_UNREADABLE)
        if not sr.detections:
            sr.flags.append(FLAG_NO_SYMBOL)
        if ratio and paper:
            xy = np.array([(d.x, d.y) for d in sr.detections]).reshape(-1, 2)
            tree_px, edges = K.tree_length_px(xy)
            sr.tree_ft = K.px_to_ft(tree_px, w, paper, ratio)
            sr.tree_edges = [((round(xy[a][0]), round(xy[a][1])), (round(xy[b][0]), round(xy[b][1]))) for a, b in edges]
            if model.conduit_ratio is not None:
                sr.conduit_ft = sr.tree_ft * model.conduit_ratio
        else:
            sr.flags.append(FLAG_SCALE_UNKNOWN)
        if keep_gray:
            grays[i] = page.original if page.original is not None else page.gray
        log(f"  page {i + 1} ({name}): {len(sr.detections)} symbols, overlay {ovf:.3%}, "
            f"scale {ratio or '-'} ({sr.scale_source})")
        results.append(sr)
    return results, grays, codes
