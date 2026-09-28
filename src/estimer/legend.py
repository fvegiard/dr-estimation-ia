"""Legend / schedule reading for PDFs that carry a text layer.

Engineers' legends and fixture schedules list a short code followed by its
description ("DS1  STANPRO L2STR-48 linéaire LED 38W", "PH1  Phare d'urgence
simple"). The same code is then written next to each symbol on the plans. For
a PDF with a text layer this gives, without any training:

1. `learn_codes`: code -> family, the family being that of the description
   (keyword categoriser `src.qpl.categorie`, built from the 2021-2026 corpus);
   a code is kept only if its legend lines agree on one family and it also
   appears as a stand-alone tag somewhere else in the set;
2. `tag_detections`: every stand-alone occurrence of a learnt code outside the
   legend lines, as a detection at the word centre (flag "from_text_tag").

Image-only PDFs have no words; these functions then return nothing and the
visual detector works alone. Nothing here is specific to a dossier.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass

from src.qpl.categorie import INDETERMINE, categoriser

CODE = re.compile(r"^(?=.*[A-Z])[A-Z0-9]{2,6}(?:-[A-Z0-9]{1,3})?$")
SHEET_NO = re.compile(r"^[A-Z]{1,2}-?\d{3,4}[A-Z]?$")
MIN_DESC_WORDS = 2


@dataclass
class TagHit:
    page: int
    x: float
    y: float
    code: str
    family: str


def _lines(words: list[tuple], tol: float) -> list[list[tuple]]:
    """Group words (x0, y0, x1, y1, text) into text lines by vertical centre."""
    ws = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines: list[list[tuple]] = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if lines and abs(((lines[-1][0][1] + lines[-1][0][3]) / 2) - yc) <= tol:
            lines[-1].append(w)
        else:
            lines.append([w])
    for ln in lines:
        ln.sort(key=lambda w: w[0])
    # split a line where the horizontal gap is large (separate columns)
    out = []
    for ln in lines:
        cur = [ln[0]]
        for a, b in zip(ln, ln[1:]):
            h = max(a[3] - a[1], 1.0)
            if b[0] - a[2] > 6 * h:
                out.append(cur); cur = []
            cur.append(b)
        out.append(cur)
    return out


def _is_code(t: str) -> bool:
    t = t.strip().upper()
    return bool(CODE.match(t)) and not SHEET_NO.match(t) and not t.isdigit()


def learn_codes(pages_words: dict[int, list[tuple]]) -> tuple[dict[str, str], set[tuple[int, int]]]:
    """Returns (code -> family, set of (page, word index) that are legend-line codes)."""
    votes: dict[str, Counter] = defaultdict(Counter)
    legend_words: set[tuple[int, int]] = set()
    for pg, words in pages_words.items():
        if not words:
            continue
        index = {id(w): i for i, w in enumerate(words)}
        heights = sorted(w[3] - w[1] for w in words)
        tol = 0.5 * heights[len(heights) // 2]
        for ln in _lines(words, tol):
            if len(ln) < 1 + MIN_DESC_WORDS:
                continue
            code = ln[0][4].strip().upper()
            if not _is_code(code):
                continue
            desc = " ".join(w[4] for w in ln[1:])
            fam = categoriser(desc).categorie
            if fam == INDETERMINE:
                continue
            votes[code][fam] += 1
            legend_words.add((pg, index[id(ln[0])]))
    # stand-alone occurrences outside legend lines
    seen = Counter()
    for pg, words in pages_words.items():
        for i, w in enumerate(words):
            t = w[4].strip().upper()
            if t in votes and (pg, i) not in legend_words:
                seen[t] += 1
    codes = {}
    for code, c in votes.items():
        fam, n = c.most_common(1)[0]
        if n == sum(c.values()) and seen[code] > 0:
            codes[code] = fam
    return codes, legend_words


def tag_detections(pages_words: dict[int, list[tuple]]) -> tuple[list[TagHit], dict[str, str]]:
    codes, legend_words = learn_codes(pages_words)
    hits = []
    for pg, words in pages_words.items():
        for i, w in enumerate(words):
            t = w[4].strip().upper()
            if t in codes and (pg, i) not in legend_words:
                hits.append(TagHit(pg, (w[0] + w[2]) / 2, (w[1] + w[3]) / 2, t, codes[t]))
    return hits, codes
