"""Lecture des tableaux de bordereau d'un PDF au format EXEMPLE (cellule par cellule).

Sert deux fois : `from_exemple` y lit les lignes de famille des feuilles agrégées / travaux de l'EXEMPLE,
et `verify_exemple` compare, cellule par cellule, notre rendu à l'EXEMPLE corrigé. Les lignes d'une cellule
sont recollées en paragraphes : une ligne suivie d'une autre qui aurait tenu sur la même largeur est une fin
de paragraphe ("\\n"), sinon c'est un retour à la ligne automatique (" ").
"""
from __future__ import annotations

import re

import pymupdf

from . import style as S

TITLE_RE = re.compile(r"^BORDEREAU (MATERIEL|TRAVAUX / ACHATS) - (\S+)")
NOTES_TITLE = "Notes de reserve source"


def _spans(page: pymupdf.Page):
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for sp in line["spans"]:
                yield sp


def _w(text: str, size: float) -> float:
    return pymupdf.get_text_length(text, fontname="helv", fontsize=size)


def join_lines(lines: list[str], size: float, width: float) -> str:
    out = ""
    for k, line in enumerate(lines):
        if k == 0:
            out = line
            continue
        first = line.split(" ", 1)[0]
        prev = out.rsplit("\n", 1)[-1]
        out += ("\n" if _w(prev.rsplit("\n", 1)[-1] + " " + first, size) <= width else " ") + line
    return out


def page_kind(page: pymupdf.Page) -> tuple[str, str] | None:
    """(format, feuille) d'une page de bordereau, sinon None."""
    first = page.get_text()[:120]
    m = TITLE_RE.match(first)
    if not m:
        return None
    if m.group(1).startswith("TRAVAUX"):
        return "travaux", m.group(2)
    sizes = {round(sp["size"], 1) for sp in _spans(page) if sp["text"].startswith("BORDEREAU")}
    return ("agrege" if 28.0 in sizes else "materiel"), m.group(2)


def spec_of(fmt: str, width: float):
    """[(clé, x début colonne, largeur d'habillage)], taille du texte des lignes, y bas de l'en-tête."""
    if fmt == "materiel":
        tw = width - 2 * S.B_MARGIN
        starts = [S.B_MARGIN + f * tw for _, _, f in S.B_COLUMNS]
        ends = starts[1:] + [width - S.B_MARGIN]
        cols = [(k, x0, x1 - x0 - 2 * S.B_CELL_PAD) for (k, _, _), x0, x1 in zip(S.B_COLUMNS, starts, ends)]
        return cols, S.B_ROW_SIZE, S.B_HEAD_TOP + S.B_HEAD_H
    from .bordereau import AGREGE, TRAVAUX
    spec = AGREGE if fmt == "agrege" else TRAVAUX
    m = spec["margin"]
    tw = width - 2 * m
    starts = [m + f * tw for _, _, f in spec["cols"]]
    ends = starts[1:] + [width - m]
    cols = [(k, x0, x1 - x0 - 10) for (k, _, _), x0, x1 in zip(spec["cols"], starts, ends)]
    return cols, spec["row_size"], spec["head_top"] + spec["head_h"]


def read_table(pages: list[pymupdf.Page], fmt: str) -> dict:
    """Lignes (dict colonne -> texte), notes de réserve et sous-titres des pages de bordereau d'une feuille."""
    rows, notes, subtitles = [], [], []
    for page in pages:
        W = page.rect.width
        cols, size, head_bottom = spec_of(fmt, W)
        spans = list(_spans(page))
        body = [sp for sp in spans if abs(sp["size"] - size) < 0.05 and sp["origin"][1] > head_bottom]
        notes_y = next((sp["origin"][1] for sp in spans if sp["text"] == NOTES_TITLE
                        or sp["text"] == S.B_RES_TITLE), None)
        if notes_y is not None:
            body = [sp for sp in body if sp["origin"][1] < notes_y]
        subtitles += [sp["text"] for sp in spans if sp["origin"][1] < head_bottom - 25
                      and not sp["text"].startswith("BORDEREAU") and sp["size"] > 11.5 and sp["size"] < 14]
        seps = sorted({round(it[1].y, 1) for d in page.get_drawings() for it in d["items"]
                       if it[0] == "l" and abs(it[1].y - it[2].y) < 0.1 and abs(it[2].x - it[1].x) > 0.8 * W
                       and it[1].y > head_bottom})
        bounds = [head_bottom] + seps
        starts = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
        for y0, y1 in starts:
            cell = {k: [] for k, _, _ in cols}
            for sp in body:
                y = sp["origin"][1]
                if not (y0 < y < y1):
                    continue
                x = sp["origin"][0]
                k = max((c for c in cols if x >= c[1] - 1.5), key=lambda c: c[1], default=cols[0])[0]
                cell[k].append((y, x, sp["text"]))
            row = {}
            for k, x_, width in cols:
                lines = [t for _, _, t in sorted(cell[k])]
                row[k] = join_lines(lines, size, width)
            rows.append(row)
        if notes_y is not None:
            tw = W - 2 * (65.0 if fmt != "materiel" else S.B_MARGIN)
            nsize = 10.0
            nl = [sp["text"] for sp in sorted(spans, key=lambda s: s["origin"][1])
                  if sp["origin"][1] > notes_y and abs(sp["size"] - nsize) < 0.05]
            notes += join_lines(nl, nsize, tw).split("\n") if nl else []
    return {"rows": rows, "notes": notes, "subtitles": list(dict.fromkeys(subtitles))}


def sheet_bordereaux(doc: pymupdf.Document) -> dict[str, dict]:
    """feuille -> {format, pages (0-based)} pour toutes les pages de bordereau du document."""
    out: dict[str, dict] = {}
    for pno in range(doc.page_count):
        k = page_kind(doc[pno])
        if k:
            out.setdefault(k[1], {"format": k[0], "pages": []})["pages"].append(pno)
    return out


def norm(text: str) -> str:
    return " ".join(str(text).split())
