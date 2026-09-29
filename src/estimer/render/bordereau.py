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


# ---------------------------------------------------------------- aggregated formats (EXEMPLE E01-E14, EU01-04)
# Geometry read from EXEMPLE.pdf page 45 (BORDEREAU MATERIEL - E01, one row per family) and page 81
# (BORDEREAU TRAVAUX / ACHATS - EU01, one row per family + portee). Column starts are fractions of the
# 2464 pt table (65 -> 2529); header text at start + 6, cell text at start + 5.
NO_PURCHASE = ("ENLEVER", "CONVERTIR", "CONSERVER")        # portees with nothing to buy (A fournir = 0)

AGREGE = {
    "title": "BORDEREAU MATERIEL - {sheet}",
    "margin": 65.0, "title_size": 28.0, "title_y": 70.0,
    "head_top": 148.0, "head_h": 30.0, "head_baseline": 20.0, "head_size": 12.0,
    "row_h": 66.0, "row_size": 11.0, "row_baseline": 16.825, "line_step": 13.244, "bottom": 140.0,
    "cols": (("id", "ID", 0.0), ("qte", "Qte", 0.035), ("famille", "Famille", 0.065),
             ("modele", "Modele / type", 0.245), ("prescription", "Prescription du devis", 0.445),
             ("source", "Source / reserve", 0.81)),
}
TRAVAUX = {
    "title": "BORDEREAU TRAVAUX / ACHATS - {sheet}",
    "margin": 65.0, "title_size": 28.0, "title_y": 70.0,
    "head_top": 132.0, "head_h": 30.0, "head_baseline": 20.0, "head_size": 12.0,
    "row_h": 100.0, "row_size": 9.2, "row_baseline": 14.89, "line_step": 10.681, "bottom": 140.0,
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


def _cell_wrap(text: str, size: float, width: float, max_lines: int) -> list[str]:
    out = []
    for para in str(text).split("\n"):
        out += wrap(para, size, width, max_lines=max_lines) if para else []
    if len(out) > max_lines:
        out = out[:max_lines]
        out[-1] = out[-1].rstrip(".") + "..."
    return out


def add_bordereau_agrege(doc: pymupdf.Document, sheet: Sheet, width: float, height: float,
                         at: int = -1) -> list[int]:
    spec = AGREGE if sheet.format == "agrege" else TRAVAUX
    m = spec["margin"]
    table_w = width - 2 * m
    starts = [m + f * table_w for _, _, f in spec["cols"]]
    ends = starts[1:] + [width - m]
    rows = aggregate_rows(sheet)
    max_lines = int((spec["row_h"] - spec["row_baseline"]) // spec["line_step"]) + 1
    per = max(1, int((height - spec["head_top"] - spec["head_h"] - spec["bottom"]) // spec["row_h"]))
    chunks = [rows[i:i + per] for i in range(0, len(rows), per)] or [[]]
    if sheet.format == "agrege":
        n = len(sheet.items)
        subs = [(13.0, 98.0, f"{n} reperes sur cette feuille - prescriptions recopiees du devis et du releve."),
                (12.0, 120.0, "Les modeles non renseignes restent a preciser (MODELE NON PRECISE); "
                              "chaque quantite est un compte de reperes du plan.")]
    else:
        lieux = sum(int(r["lieux"]) for r in rows)
        af = sum(float(r["afournir"]) for r in rows)
        subs = [(13.0, 98.0, f"{lieux} emplacements de travaux;{fmt_qty(af)} appareils a fournir "
                             "(configurations a confirmer)")]
    pages = []

    def new_page():
        pno = -1 if at < 0 else at + len(pages)
        pg = doc.new_page(pno=pno, width=width, height=height)
        pages.append(pg.number)
        pg.insert_text((m, spec["title_y"]), spec["title"].format(sheet=sheet.name), fontname="hebo",
                       fontsize=spec["title_size"], color=(0, 0, 0))
        return pg

    y = spec["head_top"] + spec["head_h"]
    for chunk in chunks:
        page = new_page()
        for size, yy, t in subs:
            page.insert_text((m, yy), t, fontsize=size, color=(0, 0, 0))
        page.draw_rect(pymupdf.Rect(m, spec["head_top"], width - m, spec["head_top"] + spec["head_h"]),
                       color=None, fill=S.B_HEAD_FILL, width=0)
        for (_, head, _), x0 in zip(spec["cols"], starts):
            page.insert_text((x0 + 6, spec["head_top"] + spec["head_baseline"]), head, fontname="hebo",
                             fontsize=spec["head_size"], color=(0, 0, 0))
        y = spec["head_top"] + spec["head_h"]
        for row in chunk:
            for (key, _, _), x0, x1 in zip(spec["cols"], starts, ends):
                lines = _cell_wrap(row.get(key, ""), spec["row_size"], x1 - x0 - 10, max_lines)
                for k, line in enumerate(lines):
                    page.insert_text((x0 + 5, y + spec["row_baseline"] + k * spec["line_step"]), line,
                                     fontsize=spec["row_size"], color=(0, 0, 0))
            y += spec["row_h"]
            page.draw_line((m, y), (width - m, y), color=S.B_SEP_COLOR, width=0.5)
    notes = []
    for line in sheet.reserves_text:
        notes += wrap(line, 10.0, table_w, max_lines=6)
    if notes:
        page = doc[pages[-1]]
        if y + 38.75 + len(notes) * S.B_RES_STEP > height - 20:
            page = new_page()
            y = spec["head_top"] - 18.0
        page.insert_text((m, y + 18.0), NOTES_TITLE, fontname="hebo", fontsize=12.0, color=(0, 0, 0))
        for k, line in enumerate(notes):
            yy = y + 38.75 + k * S.B_RES_STEP
            if yy > height - 20:
                page = new_page()
                y, k0 = spec["head_top"] - 38.75, k
                notes_left = notes[k:]
                for j, l2 in enumerate(notes_left):
                    page.insert_text((m, spec["head_top"] + j * S.B_RES_STEP), l2, fontsize=10.0, color=(0, 0, 0))
                break
            page.insert_text((m, yy), line, fontsize=10.0, color=(0, 0, 0))
    return pages
