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
    first_row: float | None = None   # imposed offset of the first legend row (EXEMPLE)


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


def _hint_points(sheet: Sheet, to_pt) -> pymupdf.Rect | None:
    if not sheet.box_hint:
        return None
    a = to_pt(sheet.box_hint[0], sheet.box_hint[1]); b = to_pt(sheet.box_hint[2], sheet.box_hint[3])
    return pymupdf.Rect(a, b)


def place_box(page: pymupdf.Page, fams: list[Family], avoid: list[pymupdf.Rect], head: Header,
              layouts=None, hint: pymupdf.Rect | None = None, rows=None) -> PlacedBox:
    """Put the RELEVE box in empty drawing space, left of the title block; most EXEMPLE-like layout first.
    When nothing is empty, the layout/position with the least ink under it is used and `fits` is False.
    `hint` (EXEMPLE box) imposes the position: the layout whose size is closest to it fills that rectangle."""
    layouts = layouts if layouts is not None else box_layouts(fams, head)
    if hint is not None:
        if rows is not None and len(rows) > 2 and rows[2]:
            layouts = [lay for lay in layouts if lay[0] == rows[2]] or layouts
        fit = [lay for lay in layouts if lay[3] <= hint.width + 1 and lay[4] <= hint.height + 1] or layouts
        ncols, col_w, pitch, _, _ = min(fit, key=lambda lay: abs(lay[3] - hint.width) + abs(lay[4] - hint.height))
        col_w = (hint.width - (2 * S.BOX_PAD_X if ncols == 1 else 0.0)) / ncols
        nrows = -(-max(1, len(fams)) // ncols)
        _, first_row = _header_lines(head, hint.width)
        if rows is not None:
            first_row, pitch = max(rows[0], first_row), (rows[1] or pitch)   # jamais sous l'en-tete
        elif nrows > 1:
            pitch = max(pitch, (hint.height - first_row - 34.0) / (nrows - 1))
        return PlacedBox(pymupdf.Rect(hint), ncols, col_w, pitch, True, first_row if rows else None)
    title_x = title_block_x(page)
    occ = occupancy(page, avoid, title_x)
    ii = _integral(occ.astype(np.float64))
    fi = _integral((~occ).astype(np.float64))
    best = None
    for ncols, col_w, pitch, w, h in layouts:
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
        ncols, col_w, pitch, w, h = layouts[-1]
        return PlacedBox(pymupdf.Rect(20, 20, 20 + w, 20 + h), ncols, col_w, pitch, False)
    return best[1]


# ---------------------------------------------------------------- markers
def marker_rect(cx: float, cy: float, bbox, radius: float | None = None) -> pymupdf.Rect:
    if bbox is not None:
        return pymupdf.Rect(bbox)
    # EXEMPLE: circle r = 4.186 pt around the symbol; an anchored symbol larger than that gets a circle
    # around its whole outline (capped) so the pastel marker stays visible over the symbol's own fill
    r = min(max(S.MARK_RADIUS, radius or 0.0), S.MARK_RADIUS_MAX)
    return pymupdf.Rect(cx - r, cy - r, cx + r, cy + r)


def draw_mark(shape: pymupdf.Shape, kind: str, rect: pymupdf.Rect, color, oc: int) -> None:
    if kind in ("rect", "square"):
        shape.draw_rect(rect)
    elif kind == "diamond":
        c = (rect.tl + rect.br) / 2
        shape.draw_polyline([pymupdf.Point(c.x, rect.y0), pymupdf.Point(rect.x1, c.y),
                             pymupdf.Point(c.x, rect.y1), pymupdf.Point(rect.x0, c.y)])
    elif kind == "triangle":
        shape.draw_polyline([pymupdf.Point((rect.x0 + rect.x1) / 2, rect.y0), pymupdf.Point(rect.x1, rect.y1),
                             pymupdf.Point(rect.x0, rect.y1)])
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
    colors = {f.code: f.color or S.family_color(f.index) for f in fams}
    to_pt = to_points(sheet, page.rect.width, page.rect.height)
    shape = page.new_shape()

    marks = []
    for it in sheet.sorted_items():
        cx, cy = to_pt(it.x, it.y)
        bb = None
        if it.bbox is not None:
            a = to_pt(it.bbox[0], it.bbox[1]); b = to_pt(it.bbox[2], it.bbox[3])
            bb = (a[0], a[1], b[0], b[1])
        mr = marker_rect(cx, cy, bb, it.radius)
        marks.append((it, mr))
        # pas d'anneau blanc autour de la pastille : le gold n'en a sur aucune des 2177 (écart E8 résorbé)
        draw_mark(shape, it.shape, mr, colors[it.code], layers[it.code])

    taken = [mr for _, mr in marks]
    # plan text (tags such as [K2.2], often vector strokes) is kept readable: labels avoid inked areas
    inky = InkMap(page)
    labels = []
    for it, mr in marks:
        text = it.repere + ("*" if S.REVALIDER in it.flags else "")
        texts = [text] + [t for t in it.label_lines if t]       # E sheets: circuit / puissance under the repere
        size = it.label_size or S.LABEL_SIZE                    # plinthes PL des feuilles en palette B : 5,2 pt
        k_sz = size / S.LABEL_SIZE
        w = max(text_width(t, size) for t in texts) + 2 * S.LABEL_PAD
        h = (S.LABEL_BOX_H + S.LABEL_LINE_H * (len(texts) - 1)) * k_sz
        own = [o for o in taken if o is not mr]
        choice = None
        if it.label_bbox is not None:            # position imposee (EXEMPLE) : etiquette et attache recopiees
            a = to_pt(it.label_bbox[0], it.label_bbox[1]); b = to_pt(it.label_bbox[2], it.label_bbox[3])
            lr = pymupdf.Rect(a[0], a[1], max(b[0], a[0] + w), max(b[1], a[1] + h))
            end = pymupdf.Point(*to_pt(*it.leader_end)) if it.leader_end else pymupdf.Point(lr.x0, (lr.y0 + lr.y1) / 2)
            choice = (end, lr)
        for end, lr in (() if choice else _label_candidates(mr, w, h)):
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
        for k, t in enumerate(texts):
            shape.insert_text(pymupdf.Point(lr.x0 + S.LABEL_PAD, lr.y0 + (5.16 + k * S.LABEL_LINE_STEP) * k_sz), t,
                              fontname=S.LABEL_FONT, fontsize=size, color=S.LABEL_COLOR, oc=oc)
    shape.commit(overlay=True)

    if encadre_v6(sheet):                    # gold E03/E04/E05/E08 : encadré v6 sans RES (spec §3.3)
        head = Header(f"RELEVE {sheet.name} - MATERIEL", "", "")
        box = place_box_v6(page, sheet, fams, taken + labels, head, _hint_points(sheet, to_pt), bordereau_page)
        draw_box_v6(page, sheet, fams, box, head, colors, layers, legend_oc, bordereau_page)
        return box
    counter = f"{len(sheet.items)} reperes / {len(fams)} familles / RES {sheet.n_reserves}"
    head = Header(f"RELEVE {sheet.name} - MATERIEL", counter, S.HINT_TEXT.format(page=bordereau_page))
    footer = S.TRAVAUX_FOOTER_TEXT.format(page=bordereau_page) if sheet.format == "travaux" else S.FOOTER_TEXT
    box = place_box(page, fams, taken + labels, head, hint=_hint_points(sheet, to_pt), rows=sheet.legend_rows)
    draw_box(page, fams, box, head, colors, layers, legend_oc, footer)
    return box


# ---------------------------------------------------------------- encadré v6 sans RES (spec §3.3, gold E03-E05, E08)
def encadre_v6(sheet: Sheet) -> bool:
    """Variante v6 de l'encadré, règle mesurée sur les 26 feuilles du gold : feuille agrégée, palette B (une
    couleur hors du cycle de la palette A) et RES non partiel. Donne v6 sur E03/E04/E05/E08 ; E11/E14
    (palette B, RES 64 sur 172) restent en encadré standard, E01/E06/E09/E12 (palette A) aussi.
    Le bordereau de ces feuilles n'a ni ligne RESERVES ni bloc de notes (gold p.51, 53, 55, 63)."""
    fams = sheet.families()
    if sheet.format != "agrege" or not fams or S.is_palette_a([f.color or S.family_color(f.index) for f in fams]):
        return False
    return sheet.n_reserves in (0, len(sheet.items))


def v6_header_lines(sheet: Sheet, fams: list[Family]) -> list[tuple[float, str, float, tuple]]:
    """(baseline, texte, corps, couleur) sous le titre. Lignes rouges seulement si l'entrée donne le compte."""
    n_ni = sum(1 for it in sheet.items if it.code == "NI")
    n_rv = sum(1 for it in sheet.items if S.REVALIDER in it.flags)
    black = (0, 0, 0)
    out = [(S.V6_COUNTER_Y, f"{len(sheet.items)} reperes / {len(fams)} familles / calques activables",
            S.V6_COUNTER_SIZE, black),
           (S.V6_IDENT_Y, f"{n_ni} non identifies - {n_rv} identifications a revalider (*)", S.V6_IDENT_SIZE, black)]
    y = S.V6_RED_Y
    if sheet.divergences:
        out.append((y, f"{sheet.divergences} divergences plan/cedule A RESOUDRE", S.V6_RED_SIZE, S.V6_RED))
        y += S.V6_RED_STEP
    if sheet.calibres:
        out.append((y, f"{sheet.calibres} calibres distincts dans les sources - voir bordereau", 8.0, S.V6_RED))
    return out


def v6_footer(sheet: Sheet, fams: list[Family], width: float, bordereau_page: int) -> list[str]:
    logements = " de logements types" if "LOGEMENTS TYPES" in (sheet.note or "").upper() else ""
    lines = []
    for t in S.V6_FOOTER:
        if t.startswith("R-001") and not any("[R-" in f.materiel for f in fams):
            continue                               # pas de désignation au registre des réserves : note sans objet
        lines += wrap_text(t.format(page=bordereau_page, type=logements), S.V6_FOOT_SIZE, width - 2 * S.V6_PAD_X)
    return lines


def v6_label(f: Family, width: float) -> list[str]:
    lw = width - S.V6_QTY_FROM_RIGHT - S.V6_LABEL_X - 6
    lines = wrap_text(f.materiel.upper(), S.V6_LABEL_SIZE, lw)
    if f.modele and len(lines) < 3 and text_width(f.modele, S.V6_LABEL_SIZE) <= lw:
        lines.append(f.modele)                     # E03 : ligne modele sous le nom (LEVITON T5820-W)
    if len(lines) > 3:
        lines = lines[:2] + [_fit(" ".join(lines[2:]), S.V6_LABEL_SIZE, lw)]
    return lines


def v6_height(nrows: int, pitch: float, n_footer: int) -> float:
    return (S.V6_FIRST_ROW + 2.5 + (nrows - 1) * pitch + S.V6_FOOT_GAP + (n_footer - 1) * S.V6_FOOT_STEP
            + S.V6_FOOT_BOTTOM)


def place_box_v6(page: pymupdf.Page, sheet: Sheet, fams: list[Family], avoid: list[pymupdf.Rect],
                 head: Header, hint: pymupdf.Rect | None, bordereau_page: int) -> PlacedBox:
    """Cadre vertical d'une colonne (E08 : 235 x 880) dans l'espace libre ; plus large ou en 2 colonnes
    seulement si rien ne tient. Position imposée (`hint`, gold) : ce rectangle, 1re ligne et pas imposés."""
    if hint is not None:
        rows = sheet.legend_rows
        ncols = int(rows[2]) if rows and len(rows) > 2 and rows[2] else 1
        first = rows[0] if rows else S.V6_FIRST_ROW
        nrows = -(-max(1, len(fams)) // ncols)
        pitch = rows[1] if rows and rows[1] else S.V6_PITCHES[0]
        return PlacedBox(pymupdf.Rect(hint), ncols, (hint.width - 2 * S.V6_PAD_X) / ncols, pitch, True,
                         first)
    layouts = []
    for ncols in (1, 2):
        for pitch in S.V6_PITCHES:
            for w in S.V6_WIDTHS:
                width = w * ncols
                nrows = -(-max(1, len(fams)) // ncols)
                nf = len(v6_footer(sheet, fams, width, bordereau_page))
                layouts.append((ncols, w - 2 * S.V6_PAD_X, pitch, width, v6_height(nrows, pitch, nf)))
    box = place_box(page, fams, avoid, head, layouts=layouts)
    box.first_row = S.V6_FIRST_ROW
    return box


def draw_box_v6(page: pymupdf.Page, sheet: Sheet, fams: list[Family], box: PlacedBox, head: Header, colors,
                layers: dict[str, int], legend_oc: int, bordereau_page: int) -> None:
    r = box.rect
    shape = page.new_shape()
    shape.draw_rect(r)
    shape.finish(width=S.BOX_BORDER_W, color=S.BOX_BORDER, fill=(1, 1, 1), oc=legend_oc)
    x = r.x0 + S.V6_PAD_X
    shape.insert_text((x, r.y0 + S.V6_TITLE_Y), head.title, fontname="hebo", fontsize=S.V6_TITLE_SIZE,
                      color=(0, 0, 0), oc=legend_oc)
    for dy, text, size, color in v6_header_lines(sheet, fams):
        shape.insert_text((x, r.y0 + dy), _fit(text, size, r.width - 2 * S.V6_PAD_X), fontsize=size, color=color,
                          oc=legend_oc)
    col_w = r.width / box.ncols
    nrows = -(-len(fams) // box.ncols)
    first = box.first_row if box.first_row is not None else S.V6_FIRST_ROW
    for i, f in enumerate(fams):
        col, row = divmod(i, nrows)
        x0 = r.x0 + col * col_w
        cy = r.y0 + first + row * box.pitch
        base = cy + 2.5
        oc = layers[f.code]
        g = S.V6_GLYPH
        draw_mark(shape, f.shape, pymupdf.Rect(x0 + S.V6_PAD_X, cy - g / 2, x0 + S.V6_PAD_X + g, cy + g / 2),
                  colors[f.code], oc)
        shape.insert_text((x0 + S.V6_CODE_X, base), f.code, fontname="hebo", fontsize=S.V6_CODE_SIZE,
                          color=(0, 0, 0), oc=oc)
        for k, t in enumerate(v6_label(f, col_w)):
            shape.insert_text((x0 + S.V6_LABEL_X, base - S.V6_LABEL_UP + k * S.V6_LABEL_STEP), t,
                              fontsize=S.V6_LABEL_SIZE, color=(0, 0, 0), oc=oc)
        shape.insert_text((x0 + col_w - S.V6_QTY_FROM_RIGHT, base), fmt_qty(f.qty), fontsize=S.V6_QTY_SIZE,
                          color=(0, 0, 0), oc=oc)
    foot = v6_footer(sheet, fams, r.width, bordereau_page)
    y = r.y1 - S.V6_FOOT_BOTTOM - (len(foot) - 1) * S.V6_FOOT_STEP
    for k, t in enumerate(foot):
        shape.insert_text((x, y + k * S.V6_FOOT_STEP), t, fontsize=S.V6_FOOT_SIZE, color=(0, 0, 0), oc=legend_oc)
    shape.commit(overlay=True)


def draw_box(page: pymupdf.Page, fams: list[Family], box: PlacedBox, head: Header, colors,
             layers: dict[str, int], legend_oc: int, footer: str = S.FOOTER_TEXT) -> None:
    r = box.rect
    shape = page.new_shape()
    shape.draw_rect(r)
    shape.finish(width=S.BOX_BORDER_W, color=S.BOX_BORDER, fill=(1, 1, 1), oc=legend_oc)
    x = r.x0 + S.BOX_PAD_X
    lines, first_row = _header_lines(head, r.width)
    first_row = box.first_row if box.first_row is not None else first_row
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
        if f.modele and len(label) == 1 and box.pitch >= 14 and text_width(f.modele, S.ROW_LABEL_SIZE) <= lw:
            label.append(f.modele)             # E03-E08 : ligne modele sous le nom (LEVITON T5820-W)
        y0 = cy - 0.905 - (len(label) - 1) * 3.6
        for k, t in enumerate(label):
            shape.insert_text((label_x, y0 + k * 7.2), t, fontsize=S.ROW_LABEL_SIZE, color=(0, 0, 0), oc=oc)
        qty = fmt_qty(f.qty) + (f" / R{f.reserves}" if f.reserves else "")
        shape.insert_text((qx, cy + 3), qty, fontsize=S.ROW_QTY_SIZE, color=(0, 0, 0), oc=oc)
    shape.insert_text((x, r.y1 - 4.5), _fit(footer, S.FOOTER_SIZE, r.width - 2 * S.BOX_PAD_X),
                      fontsize=S.FOOTER_SIZE, color=(0, 0, 0), oc=legend_oc)
    shape.commit(overlay=True)


def _fit(text: str, size: float, width: float, font: str = "helv") -> str:
    if text_width(text, size, font) <= width:
        return text
    while text and text_width(text + "...", size, font) > width:
        text = text[:-1]
    return text.rstrip() + "..."
