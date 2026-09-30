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


def wrap(text: str, size: float, width: float, max_lines: int | None = None) -> list[str]:
    """Coupe en lignes de largeur `width`. Sans `max_lines`, rien n'est tronqué : la ligne du tableau grandit."""
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
    if max_lines and len(lines) > max_lines:
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


def row_height(n_lines: int) -> float:
    """Hauteur d'une ligne de bordereau : 65 pt (EXEMPLE) tant que les cellules tiennent, sinon elle grandit."""
    return max(S.B_ROW_H, S.B_ROW_BASELINE + (n_lines - 1) * S.B_LINE_STEP + 8.0)


def add_bordereau(doc: pymupdf.Document, sheet: Sheet, width: float, height: float, at: int = -1) -> list[int]:
    """Insert the bordereau pages of `sheet` at page index `at` (-1 = append); return their 0-based numbers."""
    cols = column_x(width)
    items = sheet.sorted_items()
    res_lines = [S.B_RES_TITLE] + sheet.reserves_text if sheet.reserves_text else []
    pages = []
    bottom = height - S.B_ROWS_BOTTOM + 0.5

    def new_page():
        pno = -1 if at < 0 else at + len(pages)
        page = doc.new_page(pno=pno, width=width, height=height)
        pages.append(page.number)
        return page

    page = new_page()
    _page_header(page, sheet, cols)
    y = S.B_HEAD_TOP + S.B_HEAD_H
    for it in items:
        cells = [(x, cell_lines(key, it, S.B_ROW_SIZE, w)) for key, _, x, w in cols]
        h = row_height(max(len(c) for _, c in cells))
        if y + h > bottom and y > S.B_HEAD_TOP + S.B_HEAD_H:
            page = new_page()
            _page_header(page, sheet, cols)
            y = S.B_HEAD_TOP + S.B_HEAD_H
        for x, lines in cells:
            for k, line in enumerate(lines):
                page.insert_text((x, y + S.B_ROW_BASELINE + k * S.B_LINE_STEP), line, fontsize=S.B_ROW_SIZE,
                                 color=(0, 0, 0))
        y += h
        page.draw_line((S.B_MARGIN, y), (width - S.B_MARGIN, y), color=S.B_SEP_COLOR, width=S.B_SEP_W)
    if res_lines:
        if y + reserves_height(len(res_lines) - 1) > height - 20:
            page = new_page()
            page.insert_text((S.B_MARGIN, S.B_TITLE_Y), f"BORDEREAU MATERIEL - {sheet.name}", fontname="hebo",
                             fontsize=S.B_TITLE_SIZE, color=(0, 0, 0))
            y = S.B_HEAD_TOP - S.B_RES_GAP
        for k, line in enumerate(res_lines):
            page.insert_text((S.B_MARGIN, y + S.B_RES_GAP + k * S.B_RES_STEP), line, fontsize=S.B_RES_SIZE,
                             color=(0, 0, 0))
    return pages


# ---------------------------------------------------------------- aggregated formats (EXEMPLE E01-E14, EU01-04)
# Geometry read from EXEMPLE.pdf page 45 (BORDEREAU MATERIEL - E01, one row per family) and page 81
# (BORDEREAU TRAVAUX / ACHATS - EU01, one row per family + portee). Column starts are fractions of the
# 2464 pt table (65 -> 2529); header text at start + 6, cell text at start + 5.
NO_PURCHASE = ("ENLEVER", "CONVERTIR", "CONSERVER")        # portees with nothing to buy (A fournir = 0)

AGREGE = {
    "title": "BORDEREAU MATERIEL - {sheet}",
    "margin": 65.0, "title_size": 28.0, "title_y": 70.0,
    "head_top": 148.0, "head_h": 30.0, "head_baseline": 20.0, "head_size": 12.0,
    "row_h": 66.0, "row_size": 11.0, "row_baseline": 16.825, "line_step": 13.244, "bottom": 85.0,
    "cols": (("id", "ID", 0.0), ("qte", "Qte", 0.035), ("famille", "Famille", 0.065),
             ("modele", "Modele / type", 0.245), ("prescription", "Prescription du devis", 0.445),
             ("source", "Source / reserve", 0.81)),
}
TRAVAUX = {
    "title": "BORDEREAU TRAVAUX / ACHATS - {sheet}",
    "margin": 65.0, "title_size": 28.0, "title_y": 70.0,
    "head_top": 132.0, "head_h": 30.0, "head_baseline": 20.0, "head_size": 12.0,
    "row_h": 100.0, "row_size": 9.2, "row_baseline": 14.89, "line_step": 10.681, "bottom": 85.0,
    "cols": (("id", "ID", 0.0), ("famille", "Famille", 0.04), ("portee", "Portee", 0.19),
             ("lieux", "Lieux", 0.285), ("afournir", "A fournir", 0.355), ("modele", "Modele", 0.43),
             ("prescription", "Prescription", 0.56), ("source", "Source / relation", 0.79)),
}
NOTES_TITLE = "Notes de reserve source"


def _distinct(values) -> list[str]:
    return list(dict.fromkeys(v.strip() for v in values if v and v.strip()))


def _source_cell(its: list[Item]) -> str:
    refs = _distinct(it.ref for it in its)
    n_res = sum(1 for it in its if it.reserve)
    k_mod = sum(1 for it in its if not it.modele or it.modele == "MODELE NON PRECISE")
    parts = ["; ".join(refs) or "Preuve du releve (voir occurrences)"]
    if n_res:
        parts.append(f"RESERVES: {n_res} reperes" + (f" - modele a confirmer x{k_mod}" if k_mod else ""))
    motifs = _distinct(it.note for it in its)
    if motifs:
        parts.append("Motifs: " + "; ".join(motifs))
    return "\n".join(parts)


def _modele_cell(its: list[Item], code: str, materiel: str) -> str:
    desig = [d for d in _distinct(it.designation for it in its) if d not in (code, materiel)]
    mods = _distinct(it.modele for it in its) or ["MODELE NON PRECISE"]
    return "\n".join(["; ".join(desig)] if desig else [] + []) + ("\n" if desig else "") + "; ".join(mods)


def aggregate_rows(sheet: Sheet) -> list[dict]:
    """One row per family (agrege) or per family + portee (travaux), in legend order."""
    by: dict = {}
    for it in sheet.sorted_items():
        key = it.code if sheet.format == "agrege" else (it.code, it.portee or "A PRECISER")
        by.setdefault(key, []).append(it)
    rows = []
    for key, its in by.items():
        code = key if isinstance(key, str) else key[0]
        mat = next((it.materiel for it in its if it.materiel), code)
        presc = "; ".join(_distinct(it.prescription for it in its)) or "Aucune prescription ajoutee au releve."
        row = {"id": code, "famille": mat, "modele": _modele_cell(its, code, mat), "prescription": presc,
               "source": _source_cell(its), "items": its}
        qte = sum(it.qte for it in its)
        if sheet.format == "agrege":
            row["qte"] = fmt_qty(qte)
        else:
            portee = key[1]
            row["portee"] = portee
            row["lieux"] = str(len(its))
            buy = 0 if portee in NO_PURCHASE or portee.startswith("RENVOI") else qte
            row["afournir"] = fmt_qty(buy)
        rows.append(row)
    return rows


AGREGE_SUB1 = "{n} reperes sur cette feuille - prescriptions recopiees du devis et du releve verifie."
AGREGE_SUB2 = "Les modeles non renseignes restent a preciser. Les circuits divergents exigent une clarification."
TRAVAUX_SUB = "{lieux} emplacements de travaux; {af} appareils a fournir (configurations a confirmer)"


def _cell_wrap(text: str, size: float, width: float) -> list[str]:
    out = []
    for para in str(text).split("\n"):
        out += wrap(para, size, width) if para.strip() else []
    return out


def _num(v) -> float:
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return 0.0


def family_rows(sheet: Sheet) -> list[dict]:
    """Lignes données (familles.csv, recopiées de l'EXEMPLE ou du relevé) ; à défaut, agrégées des repères."""
    return [r for r in sheet.rows if r.get("format", sheet.format) == sheet.format] or aggregate_rows(sheet)


def add_bordereau_agrege(doc: pymupdf.Document, sheet: Sheet, width: float, height: float,
                         at: int = -1) -> list[int]:
    spec = AGREGE if sheet.format == "agrege" else TRAVAUX
    m = spec["margin"]
    table_w = width - 2 * m
    starts = [m + f * table_w for _, _, f in spec["cols"]]
    ends = starts[1:] + [width - m]
    rows = family_rows(sheet)
    if sheet.format == "agrege":
        subs = [(13.0, 98.0, AGREGE_SUB1.format(n=len(sheet.items))), (12.0, 120.0, AGREGE_SUB2)]
    else:
        lieux = sum(_num(r.get("lieux")) for r in rows)
        af = sum(_num(r.get("afournir")) for r in rows)
        subs = [(13.0, 98.0, TRAVAUX_SUB.format(lieux=fmt_qty(lieux), af=fmt_qty(af)))]
    pages = []
    head_bottom = spec["head_top"] + spec["head_h"]
    bottom = height - spec["bottom"]

    def new_page(table: bool = True):
        pno = -1 if at < 0 else at + len(pages)
        pg = doc.new_page(pno=pno, width=width, height=height)
        pages.append(pg.number)
        pg.insert_text((m, spec["title_y"]), spec["title"].format(sheet=sheet.name), fontname="hebo",
                       fontsize=spec["title_size"], color=(0, 0, 0))
        if table:
            for size, yy, t in subs:
                pg.insert_text((m, yy), t, fontsize=size, color=(0, 0, 0))
            pg.draw_rect(pymupdf.Rect(m, spec["head_top"], width - m, head_bottom),
                         color=None, fill=S.B_HEAD_FILL, width=0)
            for (_, head, _), x0 in zip(spec["cols"], starts):
                pg.insert_text((x0 + 6, spec["head_top"] + spec["head_baseline"]), head, fontname="hebo",
                               fontsize=spec["head_size"], color=(0, 0, 0))
        return pg

    page = new_page()
    y = head_bottom
    table = [[(x0, _cell_wrap(row.get(key, ""), spec["row_size"], x1 - x0 - 10))
              for (key, _, _), x0, x1 in zip(spec["cols"], starts, ends)] for row in rows]
    need = [spec["row_baseline"] + (max((len(c) for _, c in cells), default=1) - 1) * spec["line_step"] + 8.0
            for cells in table]
    # EXEMPLE E04/E05 : 23 lignes resserrees a 63,75 pt pour tenir sur une page ; sinon 66 pt et pages suivantes
    room = bottom - head_bottom
    base = spec["row_h"]
    if rows and sum(max(base, n) for n in need) > room:
        squeezed = room / len(rows)
        if sum(max(squeezed, n) for n in need) <= room:
            base = squeezed
    for cells, n in zip(table, need):
        h = max(base, n)
        if y + h > bottom + 0.5 and y > head_bottom:
            page = new_page()
            y = head_bottom
        for x0, lines in cells:
            for k, line in enumerate(lines):
                page.insert_text((x0 + 5, y + spec["row_baseline"] + k * spec["line_step"]), line,
                                 fontsize=spec["row_size"], color=(0, 0, 0))
        y += h
        page.draw_line((m, y), (width - m, y), color=S.B_SEP_COLOR, width=0.5)
    notes = []
    for line in sheet.reserves_text:
        notes += wrap(line, 10.0, table_w)
    if notes:
        if y + 38.75 + S.B_RES_STEP > height - 20:
            page = new_page(table=False)
            y = spec["head_top"] - 38.75
        page.insert_text((m, y + 18.0), NOTES_TITLE, fontname="hebo", fontsize=12.0, color=(0, 0, 0))
        yy = y + 38.75
        for line in notes:
            if yy > height - 20:
                page = new_page(table=False)
                yy = spec["head_top"]
            page.insert_text((m, yy), line, fontsize=10.0, color=(0, 0, 0))
            yy += S.B_RES_STEP
    return pages
