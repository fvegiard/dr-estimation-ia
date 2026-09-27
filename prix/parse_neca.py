#!/usr/bin/env python3
"""Deterministic parser of the NECA Manual of Labor Units 2021-2022 (PDF with OCR layer).

Output: prix/neca-2022.csv with one row per labor-unit line of the book
    section, division, page, table_title, item, unit,
    normal_hours, difficult_hours, very_difficult_hours, raw

Design (verified on the file /home/claude/data/livres/'Neca 2022 OCR.pdf', 531 pages):
- Every page carries TWO text layers: the publisher's native text (span alpha == 255, embedded
  Arial subsets) and an invisible OCR layer added on top (span alpha == 0, non-embedded fonts).
  The native layer is clean; the OCR layer contains classic errors ("10O-foot").  The parser
  therefore reads the native layer and falls back to the OCR layer only on pages that have no
  visible text at all.  OCR normalisation is applied to every numeric / unit token regardless of
  the layer, so the parser also works on a pure-OCR copy of the book.
- Table pages have a running header row "Description | Rev | Normal | Difficult | Very Difficult |
  Company Experience | Unit".  Column x-positions are read from that header on each page, and each
  numeric span is assigned to the nearest column.
- Bold left-column rows without numbers are table titles; italic rows starting with "Note" are
  notes attached to the title; bold centred rows "26 05 33: Raceway and Boxes ..." are MasterFormat
  divisions; the bold running header "Section 8: Division 26—Electrical" gives the section.
- No number is invented: every CSV row carries the printed page and the raw source line as read.

Usage:  python3 prix/parse_neca.py [--pdf PATH] [--out prix/neca-2022.csv] [--report prix/neca-2022-report.md]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

DEFAULT_PDF = Path("/home/claude/data/livres/Neca 2022 OCR.pdf")
HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "neca-2022.csv"
DEFAULT_REPORT = HERE / "neca-2022-report.md"

BOOK = "NECA Manual of Labor Units 2021-2022"
UNITS = {"E", "C", "M", "LF", "CY", "SF", "FT"}   # SF and FT appear on p.35-36, 182, 415, 437
# Units as sometimes mangled by OCR -> canonical unit (page 10 of the book defines E, C, M, LF, CY).
UNIT_FIX = {"E": "E", "C": "C", "M": "M", "LF": "LF", "CY": "CY", "LE": "LF", "L F": "LF", "IF": "LF",
            "1F": "LF", "CV": "CY", "0": "C", "O": "C", "£": "E", "F": "E", "É": "E"}
# OCR confusions inside numeric tokens.
OCR_DIGITS = str.maketrans({"O": "0", "o": "0", "D": "0", "Q": "0", "l": "1", "I": "1", "|": "1", "i": "1",
                            "S": "5", "s": "5", "B": "8", "Z": "2", "z": "2", "g": "9", "G": "6", ",": "."})
NUM_RE = re.compile(r"^-?\d+\.\d{1,3}$|^-?\d+$")   # "-0.15" deducts (p.353), "4.000" (p.410)
DIVISION_RE = re.compile(r"^(\d\d \d\d \d\d(?:\.\d\d)?)\s*[:\-–—]\s*(.+)$")
SECTION_RE = re.compile(r"^Section \d+:\s*Division\s+\d+.*", re.I)
PAGE_NUM_RE = re.compile(r"^\d{1,3}$")
BOLD = 16
ITALIC = 2
ROW_TOL = 2.6           # points: spans whose baselines differ by less are on the same row
LEFT_MARGIN_MAX = 40    # side tab digits ("8 ") sit at x<40 or x>580 and are not table content
RIGHT_MARGIN_MIN = 580


def normalise_number(tok: str) -> str | None:
    """Return a clean decimal string for a labor-unit token, or None if it is not a number.

    Handles OCR confusions (O->0, l->1, S->5, comma decimal, stray spaces) but never changes a
    token that is already a well-formed number.
    """
    t = tok.strip().replace(" ", "")
    if NUM_RE.match(t):
        return t
    t2 = t.translate(OCR_DIGITS)
    t2 = re.sub(r"\.+", ".", t2)
    if t2.startswith("."):          # ",28" printed for "0.28" (p.200)
        t2 = "0" + t2
    if NUM_RE.match(t2):
        return t2
    # "2 .50" / "2. 50" already collapsed; "250" without a dot on a hours column is left to the caller
    return None


def normalise_unit(tok: str) -> str | None:
    t = tok.strip().replace(".", "").upper()
    if t in UNITS:
        return t
    return UNIT_FIX.get(t)


@dataclass
class Span:
    text: str
    x0: float
    x1: float
    y: float
    bold: bool
    italic: bool
    size: float

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2


@dataclass
class Row:
    y: float
    spans: list[Span] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(s.text.strip() for s in self.spans if s.text.strip())

    @property
    def x0(self) -> float:
        return min(s.x0 for s in self.spans)

    @property
    def bold(self) -> bool:
        return all(s.bold for s in self.spans if s.text.strip())

    @property
    def italic(self) -> bool:
        return all(s.italic for s in self.spans if s.text.strip())


def _split_span_into_words(s: dict) -> list[Span]:
    """Split one rawdict span into whitespace-separated tokens, each with its own x-extent.

    Needed because the book sometimes emits the three labor units as a single span
    ("       1.00        1.25        1.50 "); token positions decide the column.
    """
    words: list[Span] = []
    cur: list[dict] = []
    bold, italic, size, y = bool(s["flags"] & BOLD), bool(s["flags"] & ITALIC), s["size"], s["origin"][1]

    def flush():
        if cur:
            words.append(Span("".join(c["c"] for c in cur), cur[0]["bbox"][0], cur[-1]["bbox"][2],
                              y, bold, italic, size))
            cur.clear()

    for ch in s["chars"]:
        if ch["c"].isspace():
            flush()
        else:
            cur.append(ch)
    flush()
    return words


def page_spans(page: pymupdf.Page, layer: str = "auto") -> tuple[list[Span], str]:
    """Word tokens of a page from the requested text layer.

    layer="auto": visible native text, falling back to the invisible OCR layer when a page has none;
    "native" / "ocr": that layer only (used to measure the OCR layer against the native one).
    """
    native, ocr = [], []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                words = _split_span_into_words(s)
                if not words:
                    continue
                (native if s["alpha"] > 0 else ocr).extend(words)
    if layer == "native":
        return native, "native"
    if layer == "ocr":
        return ocr, "ocr"
    if native:
        return native, "native"
    return ocr, "ocr"


def group_rows(spans: list[Span]) -> list[Row]:
    spans = sorted(spans, key=lambda s: (s.y, s.x0))
    rows: list[Row] = []
    for s in spans:
        if rows and abs(s.y - rows[-1].y) <= ROW_TOL:
            rows[-1].spans.append(s)
        else:
            rows.append(Row(s.y, [s]))
    for r in rows:
        r.spans.sort(key=lambda s: s.x0)
    return rows


def merge_split_decimals(tokens: list[Span]) -> list[Span]:
    """OCR sometimes splits "1.25" into "1" + ".25" (or "1" + "," + "25"); glue adjacent pieces back."""
    out: list[Span] = []
    for t in tokens:
        if out and t.x0 - out[-1].x1 < 4 and re.fullmatch(r"-?\d+", out[-1].text) \
                and re.fullmatch(r"[.,]\d{1,3}", t.text):
            prev = out.pop()
            out.append(Span(prev.text + t.text, prev.x0, t.x1, prev.y, prev.bold, prev.italic, prev.size))
        else:
            out.append(t)
    return out


@dataclass
class Columns:
    rev: float
    normal: float
    difficult: float
    very: float
    unit: float
    header_y: float

    def nearest(self, xc: float) -> str:
        cands = {"normal": self.normal, "difficult": self.difficult, "very": self.very}
        return min(cands, key=lambda k: abs(cands[k] - xc))


def find_columns(rows: list[Row]) -> Columns | None:
    """Locate the table header ("Normal", "Difficult", "Difficult", "Unit") and return column centres."""
    for r in rows:
        if r.y > 200:
            break
        texts = [s.text.strip() for s in r.spans]
        if "Normal" in texts and "Unit" in texts and texts.count("Difficult") >= 1:
            normal = next(s for s in r.spans if s.text.strip() == "Normal")
            diffs = [s for s in r.spans if s.text.strip() == "Difficult"]
            unit = next(s for s in r.spans if s.text.strip() == "Unit")
            revs = [s for s in r.spans if s.text.strip() == "Rev"]
            rev_x = revs[0].xc if revs else normal.x0 - 14
            if len(diffs) >= 2:
                difficult, very = diffs[0].xc, diffs[1].xc
            else:
                # "Very Difficult" wrapped: "Very" on the row above, "Difficult" below it
                difficult = diffs[0].xc
                very = difficult + (difficult - normal.xc)
            return Columns(rev_x, normal.xc, difficult, very, unit.xc, r.y)
    return None


def printed_page_number(rows: list[Row], page_index: int) -> int | None:
    """Printed folio: a 1-3 digit token on the footer/header line of the page."""
    cands = []
    for r in rows:
        if r.y < 60 or r.y > 730:
            for s in r.spans:
                t = s.text.strip()
                if PAGE_NUM_RE.match(t) and (s.x0 < 60 or s.x0 > 520):   # outer corner of the footer
                    cands.append(int(t))
    # Verified on this file: every printed folio equals page_index + 1 (517 pages, 0 mismatch);
    # the 14 pages without folio are adverts/blank pages.
    for c in cands:
        if c == page_index + 1:
            return c
    return None


@dataclass
class ParseState:
    section: str = ""
    division: str = ""
    table_title: str = ""
    note: str = ""
    subheader: str = ""             # plain (non-bold) label line printed between the title and its items


@dataclass
class Line:
    """One classified content row of a table page."""
    kind: str                       # division | title | note | plain | data
    y: float
    text: str                       # whole row, as printed (used for `raw`)
    x0: float = 0.0                 # left edge of the row (titles/items ~146, centred lines > 200)
    desc: str = ""                  # tokens left of the Rev column
    nums: dict = field(default_factory=dict)
    unit: str | None = None
    rev: str = ""
    bad_tokens: list = field(default_factory=list)


def classify_rows(rows: list[Row], cols: Columns) -> list[Line]:
    lines: list[Line] = []
    for r in rows:
        if r.y <= cols.header_y + 1 or r.y > 765:
            continue                                   # running header, column header, footer (folio baseline ~777; last data row can sit at ~742)
        content = [s for s in r.spans if LEFT_MARGIN_MAX < s.x0 < RIGHT_MARGIN_MIN]
        if not content:
            continue
        r = Row(r.y, content)
        text = re.sub(r"\s+", " ", r.text).strip()
        if not text or text.startswith("©") or text.startswith("NECA Manual of Labor Units") \
                or text == "2021-2022 Edition" or PAGE_NUM_RE.match(text):
            continue

        m = DIVISION_RE.match(text)
        if m and r.bold:
            lines.append(Line("division", r.y, f"{m.group(1)}: {m.group(2).strip()}", r.x0))
            continue

        left = [s for s in r.spans if s.xc < cols.rev - 6]
        right = merge_split_decimals([s for s in r.spans if s.xc >= cols.rev - 6])
        nums: dict[str, str] = {}
        unit = None
        rev = ""
        bad_tokens = []
        for s in right:
            tok = s.text.strip()
            if abs(s.xc - cols.unit) < 18 and normalise_unit(tok):
                unit = normalise_unit(tok)
                continue
            if abs(s.xc - cols.rev) < 10 and tok.upper() in {"X", "×"}:
                rev = "X"
                continue
            n = normalise_number(tok)
            if n is not None and s.xc < cols.unit - 18:
                col = cols.nearest(s.xc)
                if col in nums:
                    bad_tokens.append(tok)
                else:
                    nums[col] = n
                continue
            u = normalise_unit(tok)                    # unit token slightly off its column
            if u and unit is None and s.xc > cols.very + 10:
                unit = u
                continue
            bad_tokens.append(tok)
        desc = re.sub(r"\s+", " ", " ".join(s.text for s in left)).strip()

        if nums or unit:
            lines.append(Line("data", r.y, text, r.x0, desc, nums, unit, rev, bad_tokens))
            continue
        # Text-only row.  Bold/italic is judged on the description tokens; a lone "X" in the Rev
        # column is the revision flag, not text.
        left_spans = left or r.spans
        bold = all(s.bold for s in left_spans)
        italic = all(s.italic for s in left_spans)
        if right and all(s.text.strip().upper() == "X" for s in right):
            text = desc
        if not text:
            continue                                   # a row holding only the Rev flag (p.271)
        if bold:
            lines.append(Line("title", r.y, text, r.x0, desc))
        elif italic or text.lower().startswith("note"):
            lines.append(Line("note", r.y, text, r.x0, desc))
        else:
            lines.append(Line("plain", r.y, text, r.x0, desc))
    return lines


def parse_page(page: pymupdf.Page, page_index: int, state: ParseState, stats: dict,
               layer: str = "auto") -> list[dict]:
    spans, layer = page_spans(page, layer)
    if layer == "ocr":
        stats["ocr_pages"].append(page_index + 1)
    rows = group_rows(spans)
    cols = find_columns(rows)
    folio = printed_page_number(rows, page_index)
    page_label = folio if folio is not None else page_index + 1
    if folio is None:
        stats["no_folio"].append(page_index + 1)

    # running header: section
    for r in rows:
        if r.y < 80 and SECTION_RE.match(r.text):
            state.section = re.sub(r"\s+", " ", r.text).strip()
            break

    if cols is None:
        return []                                      # not a table page

    lines = classify_rows(rows, cols)
    out: list[dict] = []
    pending: list[Line] = []        # plain lines not yet emitted
    title_open = False
    last_kind = ""
    last_y = -1.0
    TWO_LINE_CELL = 6.0             # pt: numbers vertically centred between two description lines
    ROW_PITCH = 12.0                # pt: consecutive printed rows are ~8 pt apart

    def title_context() -> str:
        title = state.table_title
        if state.note:
            title = f"{title} | {state.note}" if title else state.note
        return title

    def emit(desc: str, ln: Line, raw: str):
        if not desc:
            stats["rows_without_item"].append((page_label, raw))
        if ln.kind == "plain":
            stats["rows_no_numbers"].append((page_label, raw))
        else:
            if len(ln.nums) != 3:
                stats["rows_bad_numbers"].append((page_label, raw, dict(ln.nums)))
            if ln.bad_tokens:
                stats["rows_bad_tokens"].append((page_label, raw, ln.bad_tokens))
            if ln.unit is None:
                stats["rows_no_unit"].append((page_label, raw))
        out.append({
            "section": state.section,
            "division": state.division,
            "page": page_label,
            "table_title": title_context(),
            "item": desc,
            "unit": ln.unit or "",
            "normal_hours": ln.nums.get("normal", ""),
            "difficult_hours": ln.nums.get("difficult", ""),
            "very_difficult_hours": ln.nums.get("very", ""),
            "raw": raw,
        })

    def flush_pending():
        """Plain lines the book prints as rows with blank labor-unit cells -> rows without numbers."""
        for pl in pending:
            emit(pl.text, pl, pl.text)
        pending.clear()

    i = 0
    while i < len(lines):
        ln = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else None
        if ln.kind == "division":
            flush_pending()
            state.division = ln.text
            # centred bold second line of a long division name (p.384 "... Devices and" / "Adapters")
            if nxt is not None and nxt.kind == "title" and nxt.x0 > 200 and 0 < nxt.y - ln.y < ROW_PITCH:
                state.division = f"{ln.text} {nxt.text}"
                stats["division_wraps"].append((page_label, state.division))
                i += 1
            state.table_title, state.note = "", ""
            title_open = False
        elif ln.kind == "title":
            prefix = ""
            if pending and 0 < ln.y - pending[-1].y < ROW_PITCH:
                # non-bold first line of a title wrapped onto a bold second line (p.200)
                prefix = pending.pop().text
                stats["title_prefix"].append((page_label, prefix, ln.text))
            flush_pending()
            if title_open:
                state.table_title = (state.table_title + " " + ln.text).strip()
            else:
                state.table_title, state.note = (prefix + " " + ln.text).strip(), ""
                title_open = True
        elif ln.kind == "note":
            flush_pending()
            title_open = False
            state.note = (state.note + " " + ln.text).strip() if state.note else ln.text
        elif ln.kind == "plain":
            title_open = False
            if last_kind == "note" and 0 < ln.y - last_y < ROW_PITCH \
                    and (state.note.endswith(":") or ln.text[:1] in "-*•"):
                # note continued on plain bullet lines (p.335 "Note: ... websites:" / "- www...")
                state.note = (state.note + " " + ln.text).strip()
                stats["note_continuations"].append((page_label, ln.text))
                last_kind, last_y = "note", ln.y
                i += 1
                continue
            pending.append(ln)
        else:  # data
            title_open = False
            desc = ln.desc
            raw = ln.text
            consumed_next = False
            if not desc:
                # Description printed on the line(s) around the numbers: the line just above
                # (tall cell, p.310) and/or the line just below (two-line cell, p.181).
                if pending and 0 < ln.y - pending[-1].y < ROW_PITCH:
                    above = pending.pop()
                    desc = above.text
                    raw = f"{above.text} {raw}"
                if nxt is not None and nxt.kind == "plain" and 0 < nxt.y - ln.y < TWO_LINE_CELL:
                    desc = (desc + " " + nxt.text).strip()
                    raw = f"{raw} {nxt.text}"
                    consumed_next = True
                if desc:
                    stats["wrapped_items"].append((page_label, desc))
            flush_pending()
            emit(desc, ln, raw)
            if consumed_next:
                i += 1
        last_kind, last_y = ln.kind, ln.y
        i += 1
    flush_pending()

    if not out:
        stats["header_zero_rows"].append(page_label)
    stats["rows_per_page"][page_label] = len(out)
    return out


def check_monotonic(rows: list[dict]) -> list[dict]:
    viol = []
    for r in rows:
        try:
            n, d, v = float(r["normal_hours"]), float(r["difficult_hours"]), float(r["very_difficult_hours"])
        except ValueError:
            continue
        if d < n or v < d:
            viol.append(r)
    return viol


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    ap.add_argument("--layer", choices=["auto", "native", "ocr"], default="auto",
                    help="text layer to read (default auto = native, OCR only where no native text)")
    args = ap.parse_args(argv)

    doc = pymupdf.open(args.pdf)
    stats = {
        "ocr_pages": [], "no_folio": [], "rows_without_item": [], "rows_bad_numbers": [],
        "rows_bad_tokens": [], "rows_no_unit": [], "header_zero_rows": [], "rows_per_page": {},
        "wrapped_items": [], "rows_no_numbers": [], "title_prefix": [], "note_continuations": [], "division_wraps": [],
    }
    state = ParseState()
    rows: list[dict] = []
    for i, page in enumerate(doc):
        rows.extend(parse_page(page, i, state, stats, args.layer))

    fieldnames = ["section", "division", "page", "table_title", "item", "unit",
                  "normal_hours", "difficult_hours", "very_difficult_hours", "raw"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fieldnames})

    viol = check_monotonic(rows)
    units = Counter(r["unit"] for r in rows)
    sections = Counter(r["section"] for r in rows)
    divisions = Counter(r["division"] for r in rows)
    complete = sum(1 for r in rows if r["normal_hours"] and r["difficult_hours"] and r["very_difficult_hours"])
    blank = sum(1 for r in rows if not (r["normal_hours"] or r["difficult_hours"] or r["very_difficult_hours"]))

    lines = [
        f"# NECA 2021-2022 parse report (layer: {args.layer})",
        "",
        f"- Source: `{args.pdf}` (sha256 `{sha256(args.pdf)}`), {len(doc)} PDF pages",
        f"- Output: `{args.out.name}`, **{len(rows)} rows**, {complete} with all three labor units, {blank} printed with blank cells",
        f"- Pages with a table header: {len(stats['rows_per_page'])}; pages read from the OCR layer only: "
        f"{len(stats['ocr_pages'])} {stats['ocr_pages'] if stats['ocr_pages'] else ''}",
        f"- Units: " + ", ".join(f"{u or '(none)'}={c}" for u, c in units.most_common()),
        f"- Sections: {len(sections)}; divisions: {len(divisions)}",
        "",
        "## Method",
        "- `page` is the folio printed in the book (checked equal to PDF index + 1 on every page that prints one).",
        "- Text is read from the book's native text layer (span alpha 255); the invisible OCR layer (alpha 0) is used",
        "  only on pages without native text (cover, adverts). Run with `--layer ocr` to parse the OCR layer instead.",
        "- Numeric/unit tokens go through OCR normalisation (O->0, l/I->1, S->5, comma decimal, split decimals,",
        "  E/C/M/LF/CY/SF/FT variants); a token already well-formed is never altered.",
        "- Rows printed with blank labor-unit cells are kept with empty numbers; nothing is filled in.",
        "- `table_title` = bold table title [+ ` | Note: ...` printed under it]; `raw` = the printed line, including the",
        "  Rev flag `X` when present.",
        "",
        f"## Monotonicity violations (difficult < normal or very_difficult < difficult): {len(viol)}",
    ]
    for r in viol:
        lines.append(f"- p.{r['page']} [{r['division']}] {r['table_title']} / {r['item']}: "
                     f"{r['normal_hours']} / {r['difficult_hours']} / {r['very_difficult_hours']}  <- `{r['raw']}`")
    lines += ["", f"## Pages with a table header but 0 rows: {len(stats['header_zero_rows'])}",
              ", ".join(str(p) for p in stats["header_zero_rows"]) or "(none)"]
    lines += ["", f"## Rows with fewer/more than 3 numbers: {len(stats['rows_bad_numbers'])}"]
    lines += [f"- p.{p}: `{t}` -> {n}" for p, t, n in stats["rows_bad_numbers"]]
    lines += ["", f"## Rows without unit: {len(stats['rows_no_unit'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["rows_no_unit"]]
    lines += ["", f"## Rows with unrecognised tokens in the numeric zone: {len(stats['rows_bad_tokens'])}"]
    lines += [f"- p.{p}: `{t}` -> {b}" for p, t, b in stats["rows_bad_tokens"]]
    lines += ["", f"## Rows without item description: {len(stats['rows_without_item'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["rows_without_item"]]
    lines += ["", f"## Rows printed with blank labor-unit cells (kept, no numbers): {len(stats['rows_no_numbers'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["rows_no_numbers"]]
    lines += ["", f"## Items whose description spans two lines around the numbers (joined): {len(stats['wrapped_items'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["wrapped_items"]]
    lines += ["", f"## Titles whose first line is not bold (joined): {len(stats['title_prefix'])}"]
    lines += [f"- p.{p}: `{a}` + `{b}`" for p, a, b in stats["title_prefix"]]
    lines += ["", f"## Division names wrapped on two lines (joined): {len(stats['division_wraps'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["division_wraps"]]
    lines += ["", f"## Notes continued on a plain line: {len(stats['note_continuations'])}"]
    lines += [f"- p.{p}: `{t}`" for p, t in stats["note_continuations"]]
    lines += ["", f"## Pages without a printed folio (PDF index+1 used): {len(stats['no_folio'])}",
              ", ".join(str(p) for p in stats["no_folio"]) or "(none)"]
    lines += ["", "## Rows per section"]
    lines += [f"- {s or '(none)'}: {c}" for s, c in sorted(sections.items())]
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(rows)} rows -> {args.out}")
    print(f"monotonicity violations: {len(viol)}; header pages with 0 rows: {len(stats['header_zero_rows'])}; "
          f"bad-number rows: {len(stats['rows_bad_numbers'])}; no-unit rows: {len(stats['rows_no_unit'])}; "
          f"bad tokens: {len(stats['rows_bad_tokens'])}; no-item rows: {len(stats['rows_without_item'])}; "
          f"blank-cell rows: {len(stats['rows_no_numbers'])}")
    print(f"report -> {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
