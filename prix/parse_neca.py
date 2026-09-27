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
NUM_RE = re.compile(r"^\d+\.\d{1,2}$|^\d+$")
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


def page_spans(page: pymupdf.Page) -> tuple[list[Span], str]:
    """Visible (native) word tokens of a page; fall back to the invisible OCR layer if there is none."""
    native, ocr = [], []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                words = _split_span_into_words(s)
                if not words:
                    continue
                (native if s["alpha"] > 0 else ocr).extend(words)
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
                if PAGE_NUM_RE.match(t) and LEFT_MARGIN_MAX < s.x0 < RIGHT_MARGIN_MIN:
                    cands.append(int(t))
    # the folio is normally page_index + 1 in this file; prefer a candidate consistent with that
    for c in cands:
        if c == page_index + 1:
            return c
    return cands[0] if cands else None


@dataclass
class ParseState:
    section: str = ""
    division: str = ""
    table_title: str = ""
    note: str = ""
    pending_desc: list[str] = field(default_factory=list)
    title_open: bool = False        # last row was a title line (a following bold line continues it)


def parse_page(page: pymupdf.Page, page_index: int, state: ParseState, stats: dict) -> list[dict]:
    spans, layer = page_spans(page)
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
        # Not a table page.  Divisions may still be announced on intro pages, but only bold,
        # centred lines on table pages are trusted for the division; nothing else to do.
        return []

    out: list[dict] = []
    n_rows_page = 0
    page_has_title_only = False
    state.pending_desc = []
    for r in rows:
        if r.y <= cols.header_y + 1:
            continue                                   # running header + column header
        if r.y > 740:
            continue                                   # footer
        content = [s for s in r.spans if LEFT_MARGIN_MAX < s.x0 < RIGHT_MARGIN_MIN]
        if not content:
            continue
        r = Row(r.y, content)
        text = re.sub(r"\s+", " ", r.text).strip()
        if not text:
            continue
        if text.startswith("©") or text.startswith("NECA Manual of Labor Units") or text == "2021-2022 Edition":
            continue
        if PAGE_NUM_RE.match(text):
            continue

        # Division line: bold, "26 05 33: Raceway and Boxes for Electrical Systems"
        m = DIVISION_RE.match(text)
        if m and r.bold:
            state.division = f"{m.group(1)}: {m.group(2).strip()}"
            state.table_title = ""
            state.note = ""
            state.title_open = False
            state.pending_desc = []
            continue

        # Split spans: description zone (left of Rev column) vs numeric/unit zone.
        left = [s for s in r.spans if s.xc < cols.rev - 6]
        right = [s for s in r.spans if s.xc >= cols.rev - 6]
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
            # a unit token slightly off the unit column, or an unknown token
            u = normalise_unit(tok)
            if u and unit is None and s.xc > cols.very + 10:
                unit = u
                continue
            bad_tokens.append(tok)

        desc = re.sub(r"\s+", " ", " ".join(s.text for s in left)).strip()

        if not nums and not unit:
            # Text-only row: title, note, continuation of a title, or a wrapped item description.
            if r.bold:
                if state.title_open:
                    state.table_title = (state.table_title + " " + text).strip()
                else:
                    state.table_title = text
                    state.note = ""
                    state.title_open = True
                    page_has_title_only = True
                state.pending_desc = []
            elif r.italic or text.lower().startswith("note"):
                state.note = (state.note + " " + text).strip() if state.note else text
                state.title_open = False
            else:
                state.pending_desc.append(text)
                state.title_open = False
            continue

        state.title_open = False
        # Data row.
        if state.pending_desc:
            desc = (" ".join(state.pending_desc) + " " + desc).strip()
            state.pending_desc = []
        if not desc:
            stats["rows_without_item"].append((page_label, text))
        if len(nums) != 3:
            stats["rows_bad_numbers"].append((page_label, text, dict(nums)))
        if bad_tokens:
            stats["rows_bad_tokens"].append((page_label, text, bad_tokens))
        if unit is None:
            stats["rows_no_unit"].append((page_label, text))
        title = state.table_title
        if state.note:
            title = f"{title} | {state.note}" if title else state.note
        row = {
            "section": state.section,
            "division": state.division,
            "page": page_label,
            "table_title": title,
            "item": desc,
            "unit": unit or "",
            "normal_hours": nums.get("normal", ""),
            "difficult_hours": nums.get("difficult", ""),
            "very_difficult_hours": nums.get("very", ""),
            "raw": text,
        }
        if rev:
            row["raw"] = row["raw"]  # Rev flag is kept implicitly in raw ("X" token)
        out.append(row)
        n_rows_page += 1

    if n_rows_page == 0:
        stats["header_zero_rows"].append(page_label)
    stats["rows_per_page"][page_label] = n_rows_page
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
    args = ap.parse_args(argv)

    doc = pymupdf.open(args.pdf)
    stats = {
        "ocr_pages": [], "no_folio": [], "rows_without_item": [], "rows_bad_numbers": [],
        "rows_bad_tokens": [], "rows_no_unit": [], "header_zero_rows": [], "rows_per_page": {},
    }
    state = ParseState()
    rows: list[dict] = []
    for i, page in enumerate(doc):
        rows.extend(parse_page(page, i, state, stats))

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

    lines = [
        f"# NECA 2021-2022 parse report",
        "",
        f"- Source: `{args.pdf}` (sha256 `{sha256(args.pdf)}`), {len(doc)} PDF pages",
        f"- Output: `{args.out.name}`, **{len(rows)} rows**, {complete} with all three labor units",
        f"- Pages with a table header: {len(stats['rows_per_page'])}; pages read from the OCR layer only: "
        f"{len(stats['ocr_pages'])} {stats['ocr_pages'] if stats['ocr_pages'] else ''}",
        f"- Units: " + ", ".join(f"{u or '(none)'}={c}" for u, c in units.most_common()),
        f"- Sections: {len(sections)}; divisions: {len(divisions)}",
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
    lines += ["", f"## Pages without a printed folio (PDF index+1 used): {len(stats['no_folio'])}",
              ", ".join(str(p) for p in stats["no_folio"]) or "(none)"]
    lines += ["", "## Rows per section"]
    lines += [f"- {s or '(none)'}: {c}" for s, c in sorted(sections.items())]
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(rows)} rows -> {args.out}")
    print(f"monotonicity violations: {len(viol)}; header pages with 0 rows: {len(stats['header_zero_rows'])}; "
          f"bad-number rows: {len(stats['rows_bad_numbers'])}; no-unit rows: {len(stats['rows_no_unit'])}; "
          f"bad tokens: {len(stats['rows_bad_tokens'])}; no-item rows: {len(stats['rows_without_item'])}")
    print(f"report -> {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
