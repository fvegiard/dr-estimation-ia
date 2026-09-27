"""Bordereau pages: "BORDEREAU MATERIEL - <sheet>" table, one row per repère, header repeated on every page,
"RESERVES ET COMPLEMENTS" block after the last row (EXEMPLE.pdf pages 2-7, 30-32)."""
from __future__ import annotations

import pymupdf

from . import style as S
from .data import Item, Sheet, fmt_qty
from .plan import text_width


def rows_per_page(page_h: float) -> int:
    return max(1, int((page_h - (S.B_HEAD_TOP + S.B_HEAD_H) - S.B_ROWS_BOTTOM) // S.B_ROW_H))


def column_x(page_w: float) -> list[tuple[str, str, float, float]]:
    """(key, header, x_text, max_text_width) per column."""
    table_w = page_w - 2 * S.B_MARGIN
    starts = [S.B_MARGIN + S.B_CELL_PAD + f * table_w for _, _, f in S.B_COLUMNS]
    ends = starts[1:] + [page_w - S.B_MARGIN]
    return [(k, h, x0, x1 - x0 - 2 * S.B_CELL_PAD) for (k, h, _), x0, x1 in zip(S.B_COLUMNS, starts, ends)]


def wrap(text: str, size: float, width: float, max_lines: int = S.B_MAX_CELL_LINES) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if text_width(t, size) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and text_width(last + "...", size) > width:
            last = last[:-1]
        lines[-1] = last + "..."
    return lines


def cell_lines(key: str, it: Item, size: float, width: float) -> list[str]:
    if key == "repere":
        return [it.repere] + ([it.source] if it.source else [])
    if key == "qte":
        return [fmt_qty(it.qte)]
    return wrap(str(getattr(it, key) or ""), size, width)


def _page_header(page: pymupdf.Page, sheet: Sheet, cols) -> None:
    W = page.rect.width
    page.insert_text((S.B_MARGIN, S.B_TITLE_Y), f"BORDEREAU MATERIEL - {sheet.name}", fontname="hebo",
                     fontsize=S.B_TITLE_SIZE, color=(0, 0, 0))
    page.insert_text((S.B_MARGIN, S.B_SUB1_Y), S.B_SUB1, fontsize=S.B_SUB1_SIZE, color=(0, 0, 0))
    page.insert_text((S.B_MARGIN, S.B_SUB2_Y), S.B_SUB2, fontsize=S.B_SUB2_SIZE, color=(0, 0, 0))
    page.draw_rect(pymupdf.Rect(S.B_MARGIN, S.B_HEAD_TOP, W - S.B_MARGIN, S.B_HEAD_TOP + S.B_HEAD_H),
                   color=None, fill=S.B_HEAD_FILL, width=0)
    for _, head, x, _ in cols:
        page.insert_text((x, S.B_HEAD_TOP + S.B_HEAD_BASELINE), head, fontname="hebo", fontsize=S.B_HEAD_SIZE,
                         color=(0, 0, 0))


def reserves_height(n_lines: int) -> float:
    return S.B_RES_GAP + n_lines * S.B_RES_STEP + 10 if n_lines else 0.0


def add_bordereau(doc: pymupdf.Document, sheet: Sheet, width: float, height: float, at: int = -1) -> list[int]:
    """Insert the bordereau pages of `sheet` at page index `at` (-1 = append); return their 0-based numbers."""
    cols = column_x(width)
    items = sheet.sorted_items()
    per = rows_per_page(height)
    chunks = [items[i:i + per] for i in range(0, len(items), per)] or [[]]
    res_lines = [S.B_RES_TITLE] + sheet.reserves_text if sheet.reserves_text else []
    pages = []
    y = S.B_HEAD_TOP + S.B_HEAD_H
    def new_page():
        pno = -1 if at < 0 else at + len(pages)
        return doc.new_page(pno=pno, width=width, height=height)

    for chunk in chunks:
        page = new_page()
        pages.append(page.number)
        _page_header(page, sheet, cols)
        y = S.B_HEAD_TOP + S.B_HEAD_H
        for it in chunk:
            for key, _, x, w in cols:
                for k, line in enumerate(cell_lines(key, it, S.B_ROW_SIZE, w)):
                    page.insert_text((x, y + S.B_ROW_BASELINE + k * S.B_LINE_STEP), line, fontsize=S.B_ROW_SIZE,
                                     color=(0, 0, 0))
            y += S.B_ROW_H
            page.draw_line((S.B_MARGIN, y), (width - S.B_MARGIN, y), color=S.B_SEP_COLOR, width=S.B_SEP_W)
    if res_lines:
        page = doc[pages[-1]]
        if y + reserves_height(len(res_lines) - 1) > height - 20:
            page = new_page()
            pages.append(page.number)
            page.insert_text((S.B_MARGIN, S.B_TITLE_Y), f"BORDEREAU MATERIEL - {sheet.name}", fontname="hebo",
                             fontsize=S.B_TITLE_SIZE, color=(0, 0, 0))
            y = S.B_HEAD_TOP - S.B_RES_GAP
        for k, line in enumerate(res_lines):
            page.insert_text((S.B_MARGIN, y + S.B_RES_GAP + k * S.B_RES_STEP), line, fontsize=S.B_RES_SIZE,
                             color=(0, 0, 0))
    return pages
