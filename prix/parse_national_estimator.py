#!/usr/bin/env python3
"""Deterministic parser of the National Electrical Estimator 2025 (Craftsman) into a CSV.

Input : /home/claude/data/livres/national estimator 2025.pdf (text layer, 553 pages)
Output: prix/national-estimator-2025.csv with columns
        section,page,item,crew,manhours,unit,material_usd,labor_usd,installed_usd,raw
        prix/national-estimator-2025.report.md (validation report)

How the book is laid out (verified on the PDF, see report):
  * every table page has a column header line "Material  Craft@Hrs  Unit  Cost  Cost  Cost" (Arial 10)
    with the group names "Material / [Equipment] / Labor / Installed" on the line above;
  * the page title is the 16 pt AvantGarde line at the top (used as `section`);
  * sub-headings are 12 pt AvantGarde lines ("Insulated steel set screw EMT connectors");
    the item rows under them carry only the size (' 1/2"'), so item = heading + " " + size;
  * a data row is: <item text> <Lx@h.hh> <unit> <numbers...>, all on one baseline;
  * labor cost = manhours x 46.59 USD rounded by the publisher to 3 significant digits (p.5 printed);
  * notes paragraphs are 7 pt Arial and are ignored;
  * page 423 (PDF) has an extra "Equipment" cost column: the equipment number stays in `raw` only.

Nothing is invented: every CSV row carries the PDF page and the raw text of the row it came from.
`page` is the 1-based PDF page index (printed page number = PDF page - 1 on every table page).
"""
from __future__ import annotations

import csv
import math
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf

BOOK = Path("/home/claude/data/livres/national estimator 2025.pdf")
HERE = Path(__file__).resolve().parent
OUT_CSV = HERE / "national-estimator-2025.csv"
OUT_REPORT = HERE / "national-estimator-2025.report.md"

RATE = 46.59  # USD per manhour, book p.5 (printed)
CRAFT_RE = re.compile(r"^(L\d)@(\d*\.?\d+)$")
NUM_RE = re.compile(r"^-?\d{1,3}(,\d{3})*(\.\d+)?$|^-?\.\d+$|^-?\d+\.\d*$")
DASH = {"—", "-", "–"}
Y_TOL = 3.0  # points: words within this vertical distance share a row

COLUMNS = ["section", "page", "item", "crew", "manhours", "unit",
           "material_usd", "labor_usd", "installed_usd", "raw"]


def to_num(tok: str) -> float | None:
    if tok in DASH:
        return None
    if NUM_RE.match(tok):
        return float(tok.replace(",", ""))
    return None


def page_lines(page: pymupdf.Page):
    """Lines with font info: (bbox, size, font, text)."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            spans = [s for s in l["spans"] if s["text"].strip()]
            if not spans:
                continue
            txt = " ".join(s["text"].strip() for s in spans)
            # spans are split before punctuation ("bolts , wing") - glue them back
            txt = re.sub(r"\s+([,.;:'\"])(?=\s|$)", r"\1", txt)
            out.append((l["bbox"], spans[0]["size"], spans[0]["font"], txt))
    return out


def group_rows(words):
    """Group pymupdf words by baseline into rows; each row sorted left to right."""
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    rows, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= Y_TOL:
            cur.append(w)
            cy = y if cy is None else cy
        else:
            rows.append(cur)
            cur, cy = [w], y
    if cur:
        rows.append(cur)
    return [sorted(r, key=lambda w: w[0]) for r in rows]


def parse_page(page: pymupdf.Page, pno: int, stats: Counter, issues: list):
    lines = page_lines(page)
    hdr = [l for l in lines if l[3] == "Craft@Hrs"]
    if not hdr:
        return []
    stats["pages_with_header"] += 1
    hdr_y = hdr[0][0][1]

    # group names above the "Cost" cells: Material / [Equipment] / Labor / Installed
    groups = [l for l in lines if abs(l[0][1] - (hdr_y - 12)) < 4 and l[3] in ("Material", "Equipment", "Labor", "Installed")]
    groups.sort(key=lambda l: l[0][0])
    group_names = [l[3] for l in groups]
    group_x1 = [l[0][2] for l in groups]
    if group_names not in (["Material", "Labor", "Installed"], ["Material", "Equipment", "Labor", "Installed"]):
        issues.append(f"page {pno}: unexpected cost columns {group_names}")
    right_edge = max(group_x1) + 8 if group_x1 else page.rect.width

    # section = 16 pt title(s) at the top of the page
    titles = [l[3] for l in lines if round(l[1]) == 16 and l[0][1] < 70]
    section = " ".join(titles).strip()

    # sub-headings: 12 pt AvantGarde lines, keyed by baseline y
    headings = [(l[0][1], l[0][3], l[3]) for l in lines if round(l[1]) == 12 and "AvantGarde" in l[2]]
    headings.sort()

    words = [w for w in page.get_text("words") if w[0] < right_edge]
    rows = group_rows(words)

    out = []
    heading, heading_y = "", None
    hi = 0
    n_rows = 0
    for r in rows:
        y = (r[0][1] + r[0][3]) / 2
        # advance heading pointer: merge consecutive heading lines (wrapped headings)
        while hi < len(headings) and headings[hi][1] <= y + 1:
            hy0, hy1, ht = headings[hi]
            if heading_y is not None and hy0 - heading_y < 20:
                heading = (heading + " " + ht).strip()
            else:
                heading = ht
            heading_y = hy1
            hi += 1
        toks = [w[4] for w in r]
        k = [i for i, t in enumerate(toks) if CRAFT_RE.match(t)]
        if not k:
            continue
        if len(k) > 1:
            issues.append(f"page {pno}: two crew codes on one row: {' '.join(toks)}")
            continue
        k = k[0]
        m = CRAFT_RE.match(toks[k])
        crew, manhours = m.group(1), float(m.group(2))
        item_txt = " ".join(toks[:k]).strip()
        after = toks[k + 1:]
        if not after:
            issues.append(f"page {pno}: no unit after crew code: {' '.join(toks)}")
            continue
        unit = after[0]
        nums_tok = after[1:]
        vals = [to_num(t) for t in nums_tok]
        if any(v is None and t not in DASH for v, t in zip(vals, nums_tok)):
            issues.append(f"page {pno}: non-numeric cost cell: {' '.join(toks)}")
            continue
        if len(vals) != len(group_names):
            issues.append(f"page {pno}: {len(vals)} cost cells for {len(group_names)} columns: {' '.join(toks)}")
            if len(vals) < len(group_names):
                continue
            vals = vals[:len(group_names)]
        cells = dict(zip(group_names, vals))
        # item: heading + size line (a heading is only reused for rows below it on this page)
        item = (heading + " " + item_txt).strip() if heading else item_txt
        if not item:
            issues.append(f"page {pno}: empty item: {' '.join(toks)}")
        raw = " ".join(toks)
        out.append({
            "section": section,
            "page": pno,
            "item": re.sub(r"\s+", " ", item),
            "crew": crew,
            "manhours": f"{manhours:g}",
            "unit": unit,
            "material_usd": "" if cells["Material"] is None else f"{cells['Material']:.2f}",
            "labor_usd": "" if cells["Labor"] is None else f"{cells['Labor']:.2f}",
            "installed_usd": "" if cells["Installed"] is None else f"{cells['Installed']:.2f}",
            "raw": raw,
        })
        n_rows += 1
    if n_rows == 0:
        issues.append(f"page {pno}: Craft@Hrs header but 0 rows parsed")
        stats["header_pages_zero_rows"] += 1
    return out


def sig3(x: float) -> float:
    if x == 0:
        return 0.0
    e = math.floor(math.log10(abs(x)))
    q = 10 ** (e - 2)
    return round(x / q) * q


def validate(rows):
    """Three nested criteria: strict (+-0.02 USD), publisher rounding to 3 significant digits,
    and within one unit of the 3rd significant digit (the book sometimes truncates instead of rounding)."""
    strict = book = ulp = 0
    fails = []
    for r in rows:
        if r["labor_usd"] == "":
            fails.append((r, "no labor"))
            continue
        mh = float(r["manhours"])
        lab = float(r["labor_usd"])
        exp = mh * RATE
        unit3 = 10 ** (math.floor(math.log10(exp)) - 2) if exp > 0 else 0.01
        if abs(lab - exp) <= 0.02:
            strict += 1
        if abs(lab - sig3(exp)) <= 0.011 or abs(lab - exp) <= 0.02:
            book += 1
        if abs(lab - exp) <= unit3 + 0.001:
            ulp += 1
        else:
            fails.append((r, f"expected {exp:.4f} (3 s.f. {sig3(exp):.2f})"))
    return strict, book, ulp, fails


def main() -> int:
    doc = pymupdf.open(BOOK)
    stats: Counter = Counter()
    issues: list[str] = []
    rows = []
    for i, page in enumerate(doc):
        rows.extend(parse_page(page, i + 1, stats, issues))

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    strict, book, ulp, fails = validate(rows)
    n = len(rows)
    zero_pages = [ln for ln in issues if "0 rows parsed" in ln]
    size_only = sum(1 for r in rows if re.fullmatch(r'[\d\s/#"\-.x]+', r["item"]))
    lines = [
        "# National Electrical Estimator 2025 — parse report",
        "",
        f"- source: `{BOOK}` ({doc.page_count} pages)",
        f"- output: `{OUT_CSV.name}` — {n} rows",
        f"- pages with a `Craft@Hrs` header: {stats['pages_with_header']}",
        f"- header pages yielding 0 rows: {stats['header_pages_zero_rows']}" + (" -> " + "; ".join(zero_pages) if zero_pages else ""),
        f"- crew codes: {dict(Counter(r['crew'] for r in rows))}",
        f"- units: {dict(Counter(r['unit'] for r in rows).most_common())}",
        f"- rows whose item is still a bare size (no heading found above on the page): {size_only}",
        "",
        "## Labor check (labor_usd vs manhours x 46.59)",
        "",
        f"- strict |diff| <= 0.02 USD: {strict}/{n} = {100 * strict / n:.2f}%",
        f"- publisher rounding (3 significant digits, book p.5 printed) or |diff| <= 0.02: {book}/{n} = {100 * book / n:.2f}%",
        f"- within one unit of the 3rd significant digit (book sometimes truncates, e.g. 0.39 x 46.59 = 18.17 printed 18.10): {ulp}/{n} = {100 * ulp / n:.2f}%",
        f"- rows failing all three (book errata candidates, kept as printed): {len(fails)}",
        "",
    ]
    for r, why in fails[:200]:
        lines.append(f"  - p.{r['page']} `{r['raw']}` -> {why}")
    lines += [
        "",
        "## Notes",
        "",
        "- `page` = 1-based PDF page; printed page number = PDF page - 1 (checked on every table page; PDF 540 and 542 carry no printed number).",
        "- PDF p.342 `#1 horz. elbows, 30 L1@0.20 ... 11.60`: 11.60 USD is 0.25 h x 46.59, not 0.20 h — printed inconsistency in the book, kept as printed.",
        "- PDF p.445 `5/8\" dia x 8' long L1@1.70 ... 73.30`: 73.30 USD is 1.57 h x 46.59 — printed inconsistency, kept as printed.",
        "- Rows repeated verbatim in the book (same heading printed twice on PDF p.217 and p.251) are kept: 5 duplicate rows.",
        "- Units `100`, `500`, `1000`, `50` are per-package quantities printed in the Unit column (wire connectors, PDF p.116-118).",
        "- PDF p.423 has an Equipment cost column; its value is in `raw` only.",
    ]
    lines += ["", "## Parser issues", ""]
    lines += [f"- {x}" for x in issues] or ["- none"]
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:16]))
    print(f"issues: {len(issues)} (see {OUT_REPORT})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
