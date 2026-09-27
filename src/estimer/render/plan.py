"""Annotated plan page: markers + repère labels + "RELEVE <sheet> - MATERIEL" box, drawn as vector
content on the original PDF page, one optional-content layer (OCG) per family plus one for the legend."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pymupdf
from scipy.ndimage import binary_dilation

from . import style as S
from .data import Family, Sheet, fmt_qty, to_points

MASK_ZOOM = 0.2          # free-space search raster: 1 px = 5 pt
INK_LEVEL = 242          # grey level under which a pixel counts as ink
BOX_CLEARANCE_PT = 6.0   # empty margin required around the RELEVE box
TITLE_BLOCK_FALLBACK = 0.84
INK_ZOOM = 2.0           # label-placement ink map: 2 px per pt
LABEL_MAX_INK = 0.04     # a label may cross a wall line, not sit on plan text


@dataclass
class PlacedBox:
    rect: pymupdf.Rect
    ncols: int
    col_w: float
    pitch: float
    fits: bool           # False when no empty area was large enough (box drawn over the least-ink area)


def text_width(text: str, size: float, font: str = "helv") -> float:
    return pymupdf.get_text_length(text, fontname=font, fontsize=size)


def title_block_x(page: pymupdf.Page) -> float:
    """x of the title-block frame: the right-most long vertical line in the right third of the sheet."""
    W, H = page.rect.width, page.rect.height
    best = None
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                if abs(p.x - q.x) < 1 and abs(p.y - q.y) > 0.6 * H and 0.66 * W < p.x < 0.97 * W:
                    best = p.x if best is None else max(best, p.x)
            elif it[0] == "re":
                r = it[1]
                if r.height > 0.6 * H and 0.66 * W < r.x0 < 0.97 * W and r.width < 0.3 * W:
                    best = r.x0 if best is None else max(best, r.x0)
    return best if best is not None else TITLE_BLOCK_FALLBACK * W


def occupancy(page: pymupdf.Page, extra: list[pymupdf.Rect], title_x: float) -> np.ndarray:
    """Boolean mask (True = occupied) of the page at MASK_ZOOM: drawing ink, markers/labels, title block."""
    pix = page.get_pixmap(matrix=pymupdf.Matrix(MASK_ZOOM, MASK_ZOOM), colorspace=pymupdf.csGRAY, alpha=False)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    occ = img < INK_LEVEL
    for r in extra:
        x0, y0 = int(r.x0 * MASK_ZOOM), int(r.y0 * MASK_ZOOM)
        x1, y1 = int(np.ceil(r.x1 * MASK_ZOOM)), int(np.ceil(r.y1 * MASK_ZOOM))
        occ[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] = True
    occ[:, int(title_x * MASK_ZOOM) - 1:] = True
    m = max(1, int(round(BOX_CLEARANCE_PT * MASK_ZOOM)))
    occ = binary_dilation(occ, iterations=m)
    occ[:m, :] = occ[-m:, :] = True
    occ[:, :m] = occ[:, -m:] = True
    return occ


def _integral(a: np.ndarray) -> np.ndarray:
    ii = np.zeros((a.shape[0] + 1, a.shape[1] + 1), dtype=np.float64)
    ii[1:, 1:] = a.cumsum(0).cumsum(1)
    return ii


def _window_sums(ii: np.ndarray, h: int, w: int) -> np.ndarray:
    return ii[h:, w:] - ii[:-h, w:] - ii[h:, :-w] + ii[:-h, :-w]


@dataclass
class Header:
    title: str
    counter: str
    hint: str


def _header_lines(h: Header, width: float) -> tuple[list[tuple[float, str, str, float, tuple]], float]:
    """(dy_baseline, text, font, size, color) of the header, and the dy of the first legend row centre.

    Wide boxes put title/counter/hint on one line (EXEMPLE DSI01); narrow ones stack and wrap them (E02, E07)."""
    inner = width - 2 * S.BOX_PAD_X
    black = (0, 0, 0)
    if width >= 1000:
        tw = text_width(h.title, S.TITLE_SIZE, S.TITLE_FONT)
        cx = max(185.0, tw + 20)
        hx = cx + max(335.0, text_width(h.counter, S.COUNTER_SIZE) + 30)
        return [(16.0, h.title, S.TITLE_FONT, S.TITLE_SIZE, black, 0.0),
                (16.0, h.counter, "helv", S.COUNTER_SIZE, black, cx),
                (16.0, h.hint, "helv", S.HINT_SIZE, black, hx),
                (29.0, S.WARN_TEXT, "helv", S.WARN_SIZE, S.WARN_COLOR, 0.0)], 49.0
    lines = [(16.0, h.title, S.TITLE_FONT, S.TITLE_SIZE, black, 0.0),
             (29.8, h.counter, "helv", S.COUNTER_SIZE, black, 0.0)]
    y = 29.8
    for t in wrap_text(h.hint, S.HINT_SIZE, inner):
        y += 10.1
        lines.append((y, t, "helv", S.HINT_SIZE, black, 0.0))
    for t in wrap_text(S.WARN_TEXT, S.WARN_SIZE, inner):
        y += 9.0
        lines.append((y, t, "helv", S.WARN_SIZE, S.WARN_COLOR, 0.0))
    return lines, y + 22.0


def wrap_text(text: str, size: float, width: float, font: str = "helv") -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if not cur or text_width(t, size, font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def qty_offset(col_w: float) -> float:
    return col_w - (74.0 if col_w >= 390 else 48.0)


def box_layouts(fams: list[Family], head: Header):
    """Candidate (ncols, col_w, pitch, width, height) layouts, most EXEMPLE-like first
    (DSI01: 4 x 505 pt columns, 27 pt rows; E02: 1 x 390 pt column, 22.3 pt rows; E07: 1 x 250, ~13 pt)."""
    n = max(1, len(fams))
    out = []
    for pitch in S.ROW_PITCHES:
        for col_w in S.COL_WIDTHS:
            for ncols in range(min(S.MAX_COLS, n), 0, -1):
                nrows = -(-n // ncols)
                w = ncols * col_w + (2 * S.BOX_PAD_X if ncols == 1 else 0.0)
                out.append((ncols, col_w, pitch, w, box_height(nrows, w, pitch, head)))
    return out


def box_height(nrows: int, width: float, pitch: float, head: Header) -> float:
    _, first_row = _header_lines(head, width)
    return first_row + (nrows - 1) * pitch + 34.0


def place_box(page: pymupdf.Page, fams: list[Family], avoid: list[pymupdf.Rect], head: Header) -> PlacedBox:
    """Put the RELEVE box in empty drawing space, left of the title block; most EXEMPLE-like layout first.
    When nothing is empty, the layout/position with the least ink under it is used and `fits` is False."""
    title_x = title_block_x(page)
    occ = occupancy(page, avoid, title_x)
    ii = _integral(occ.astype(np.float64))
    fi = _integral((~occ).astype(np.float64))
    best = None
    for ncols, col_w, pitch, w, h in box_layouts(fams, head):
        pw, ph = int(np.ceil(w * MASK_ZOOM)), int(np.ceil(h * MASK_ZOOM))
        if pw >= occ.shape[1] or ph >= occ.shape[0]:
            continue
        sums = _window_sums(ii, ph, pw)
        ok = np.argwhere(sums == 0)
        if len(ok):
            # among empty positions, keep the one with the most empty space around it
            pad = max(pw, ph) // 2
            ys, xs = ok[:, 0], ok[:, 1]
            y0 = np.clip(ys - pad, 0, occ.shape[0]); y1 = np.clip(ys + ph + pad, 0, occ.shape[0])
            x0 = np.clip(xs - pad, 0, occ.shape[1]); x1 = np.clip(xs + pw + pad, 0, occ.shape[1])
            around = fi[y1, x1] - fi[y0, x1] - fi[y1, x0] + fi[y0, x0]
            y, x = ok[int(np.argmax(around))]
            r = pymupdf.Rect(x / MASK_ZOOM, y / MASK_ZOOM, x / MASK_ZOOM + w, y / MASK_ZOOM + h)
            return PlacedBox(r, ncols, col_w, pitch, True)
        k = int(np.argmin(sums))
        y, x = np.unravel_index(k, sums.shape)
        frac = sums[y, x] / (pw * ph)
        if best is None or frac < best[0]:
            r = pymupdf.Rect(x / MASK_ZOOM, y / MASK_ZOOM, x / MASK_ZOOM + w, y / MASK_ZOOM + h)
            best = (frac, PlacedBox(r, ncols, col_w, pitch, False))
    if best is None:
        ncols, col_w, pitch, w, h = box_layouts(fams, head)[-1]
        return PlacedBox(pymupdf.Rect(20, 20, 20 + w, 20 + h), ncols, col_w, pitch, False)
    return best[1]


# ---------------------------------------------------------------- markers
def marker_rect(cx: float, cy: float, bbox) -> pymupdf.Rect:
    if bbox is not None:
        return pymupdf.Rect(bbox)
    r = S.MARK_RADIUS
    return pymupdf.Rect(cx - r, cy - r, cx + r, cy + r)


def draw_mark(shape: pymupdf.Shape, kind: str, rect: pymupdf.Rect, color, oc: int) -> None:
    if kind == "rect":
        shape.draw_rect(rect)
    elif kind == "diamond":
        c = (rect.tl + rect.br) / 2
        shape.draw_polyline([pymupdf.Point(c.x, rect.y0), pymupdf.Point(rect.x1, c.y),
                             pymupdf.Point(c.x, rect.y1), pymupdf.Point(rect.x0, c.y)])
    else:
        c = (rect.tl + rect.br) / 2
        shape.draw_circle(c, min(rect.width, rect.height) / 2)
    shape.finish(width=S.MARK_LINE_W, color=color, fill=color, fill_opacity=S.FILL_OPACITY,
                 stroke_opacity=S.STROKE_OPACITY, closePath=True, oc=oc)


def _label_candidates(mr: pymupdf.Rect, w: float, h: float):
    """(leader_end, label_rect) for right, left, above, below, at growing distances."""
    c = (mr.tl + mr.br) / 2
    for k in (1.0, 2.5, 4.5, 8.0):
        g = S.LEADER_GAP * k
        yield pymupdf.Point(mr.x1 + g, c.y), pymupdf.Rect(mr.x1 + g, c.y - h / 2, mr.x1 + g + w, c.y + h / 2)
        yield pymupdf.Point(mr.x0 - g, c.y), pymupdf.Rect(mr.x0 - g - w, c.y - h / 2, mr.x0 - g, c.y + h / 2)
        yield pymupdf.Point(c.x, mr.y0 - g), pymupdf.Rect(c.x - w / 2, mr.y0 - g - h, c.x + w / 2, mr.y0 - g)
        yield pymupdf.Point(c.x, mr.y1 + g), pymupdf.Rect(c.x - w / 2, mr.y1 + g, c.x + w / 2, mr.y1 + g + h)


class InkMap:
    """Ink of the original page at 1 px/pt, with an integral image for O(1) rectangle queries."""

    def __init__(self, page: pymupdf.Page):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(INK_ZOOM, INK_ZOOM), colorspace=pymupdf.csGRAY, alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        self.ii = _integral((img < INK_LEVEL).astype(np.float64))
        self.h, self.w = img.shape

    def fraction(self, r: pymupdf.Rect) -> float:
        x0 = int(np.clip(r.x0 * INK_ZOOM, 0, self.w)); x1 = int(np.clip(np.ceil(r.x1 * INK_ZOOM), 0, self.w))
        y0 = int(np.clip(r.y0 * INK_ZOOM, 0, self.h)); y1 = int(np.clip(np.ceil(r.y1 * INK_ZOOM), 0, self.h))
        if x1 <= x0 or y1 <= y0:
            return 1.0                       # off the page
        ink = self.ii[y1, x1] - self.ii[y0, x1] - self.ii[y1, x0] + self.ii[y0, x0]
        return float(ink) / ((x1 - x0) * (y1 - y0))


def _hits(r: pymupdf.Rect, rects: list[pymupdf.Rect]) -> bool:
    return any(r.intersects(o) for o in rects)


def annotate_page(page: pymupdf.Page, sheet: Sheet, bordereau_page: int, layers: dict[str, int],
                  legend_oc: int) -> PlacedBox:
    """Draw markers, labels and the RELEVE box on `page`. `layers` maps family code -> OCG xref."""
    fams = sheet.families()
    colors = {f.code: S.family_color(f.index) for f in fams}
    to_pt = to_points(sheet, page.rect.width, page.rect.height)
    shape = page.new_shape()

    marks = []
    for it in sheet.sorted_items():
        cx, cy = to_pt(it.x, it.y)
        bb = None
        if it.bbox is not None:
            a = to_pt(it.bbox[0], it.bbox[1]); b = to_pt(it.bbox[2], it.bbox[3])
            bb = (a[0], a[1], b[0], b[1])
        mr = marker_rect(cx, cy, bb)
        marks.append((it, mr))
        draw_mark(shape, it.shape, mr, colors[it.code], layers[it.code])

    taken = [mr for _, mr in marks]
    # plan text (tags such as [K2.2], often vector strokes) is kept readable: labels avoid inked areas
    inky = InkMap(page)
    labels = []
    for it, mr in marks:
        w = text_width(it.repere, S.LABEL_SIZE) + 2 * S.LABEL_PAD
        h = S.LABEL_BOX_H
        own = [o for o in taken if o is not mr]
        choice = None
        for end, lr in _label_candidates(mr, w, h):
            if not _hits(lr, labels) and not _hits(lr, own) and inky.fraction(lr) <= LABEL_MAX_INK:
                choice = (end, lr)
                break
        if choice is None:                   # crowded: accept plan text under the label, never another label
            choice = next(((e, r) for e, r in _label_candidates(mr, w, h)
                           if not _hits(r, labels) and not _hits(r, own)), None)
        if choice is None:
            choice = next(_label_candidates(mr, w, h))
        end, lr = choice
        labels.append(lr)
        c = (mr.tl + mr.br) / 2
        oc = layers[it.code]
        shape.draw_line(c, end)
        shape.finish(width=S.LEADER_W, color=colors[it.code], oc=oc)
        shape.draw_rect(lr)
        shape.finish(width=0, color=None, fill=(1, 1, 1), fill_opacity=S.LABEL_BOX_OPACITY, oc=oc)
        shape.insert_text(pymupdf.Point(lr.x0 + S.LABEL_PAD, lr.y0 + 5.16), it.repere, fontname=S.LABEL_FONT,
                          fontsize=S.LABEL_SIZE, color=S.LABEL_COLOR, oc=oc)
    shape.commit(overlay=True)

    head = Header(f"RELEVE {sheet.name} - MATERIEL",
                  f"{len(sheet.items)} reperes / {len(fams)} familles / RES {sheet.n_reserves}",
                  S.HINT_TEXT.format(page=bordereau_page))
    box = place_box(page, fams, taken + labels, head)
    draw_box(page, fams, box, head, colors, layers, legend_oc)
    return box


def draw_box(page: pymupdf.Page, fams: list[Family], box: PlacedBox, head: Header, colors,
             layers: dict[str, int], legend_oc: int) -> None:
    r = box.rect
    shape = page.new_shape()
    shape.draw_rect(r)
    shape.finish(width=S.BOX_BORDER_W, color=S.BOX_BORDER, fill=(1, 1, 1), oc=legend_oc)
    x = r.x0 + S.BOX_PAD_X
    lines, first_row = _header_lines(head, r.width)
    for dy, text, font, size, color, dx in lines:
        shape.insert_text((x + dx, r.y0 + dy), text, fontname=font, fontsize=size, color=color, oc=legend_oc)
    nrows = -(-len(fams) // box.ncols)
    for i, f in enumerate(fams):
        col, row = divmod(i, nrows)
        cx0 = x + col * box.col_w
        cy = r.y0 + first_row + row * box.pitch
        oc = layers[f.code]
        half = S.LEGEND_MARK / 2
        draw_mark(shape, f.shape, pymupdf.Rect(cx0, cy - half, cx0 + S.LEGEND_MARK, cy + half), colors[f.code], oc)
        shape.insert_text((cx0 + 15, cy + 3), f.code, fontname="hebo", fontsize=S.ROW_CODE_SIZE, color=(0, 0, 0),
                          oc=oc)
        qx = cx0 + qty_offset(box.col_w)
        label_x = cx0 + 50
        lw = qx - label_x - 6
        label = wrap_text(f.materiel.upper(), S.ROW_LABEL_SIZE, lw)
        if len(label) > 2 or box.pitch < 14 and len(label) > 1:
            label = [_fit(f.materiel.upper(), S.ROW_LABEL_SIZE, lw)]
        y0 = cy - 0.905 - (len(label) - 1) * 3.6
        for k, t in enumerate(label):
            shape.insert_text((label_x, y0 + k * 7.2), t, fontsize=S.ROW_LABEL_SIZE, color=(0, 0, 0), oc=oc)
        qty = fmt_qty(f.qty) + (f" / R{f.reserves}" if f.reserves else "")
        shape.insert_text((qx, cy + 3), qty, fontsize=S.ROW_QTY_SIZE, color=(0, 0, 0), oc=oc)
    shape.insert_text((x, r.y1 - 4.5), _fit(S.FOOTER_TEXT, S.FOOTER_SIZE, r.width - 2 * S.BOX_PAD_X),
                      fontsize=S.FOOTER_SIZE, color=(0, 0, 0), oc=legend_oc)
    shape.commit(overlay=True)


def _fit(text: str, size: float, width: float, font: str = "helv") -> str:
    if text_width(text, size, font) <= width:
        return text
    while text and text_width(text + "...", size, font) > width:
        text = text[:-1]
    return text.rstrip() + "..."
