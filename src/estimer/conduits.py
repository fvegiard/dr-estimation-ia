"""Sheet scale and conduit-length estimate.

Scale: read from the page text layer ("ÉCHELLE 1/8\\" = 1'-0\\"", "1:100") when
the PDF has one, or given per sheet by the caller (`--sheets` CSV). Without a
scale no length is produced — the sheet is flagged "scale_unknown".

Length: the estimator draws conduit/circuit runs as Plan Expert lines. We do
not trace wiring on the drawing; we estimate the run length as
    conduit_ft = ratio x (rectilinear minimum spanning tree of the detected
                          devices on the sheet, in feet)
where `ratio` is learnt on the training references (median over sheets of
estimator line feet / tree feet over his own marks). This is an estimate and
is always reported as such.
"""
from __future__ import annotations

import re
from fractions import Fraction

import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import cdist

_IMPERIAL = re.compile(r"(\d+(?:\s*\d+)?/\d+|\d+(?:[.,]\d+)?)\s*(?:\"|''|”|po|in)\s*=\s*1\s*'\s*-?\s*0?\s*(?:\"|''|”)?",
                       re.IGNORECASE)
_METRIC = re.compile(r"\b1\s*:\s*(\d{2,4})\b")


def _to_float(txt: str) -> float:
    txt = txt.replace(",", ".").strip()
    parts = txt.split()
    total = 0.0
    for p in parts:
        total += float(Fraction(p)) if "/" in p else float(p)
    return total


def parse_scale(text: str) -> float | None:
    """Scale ratio real/paper from a title-block string, None if absent or ambiguous."""
    found = set()
    for m in _IMPERIAL.finditer(text or ""):
        try:
            inch = _to_float(m.group(1))
        except (ValueError, ZeroDivisionError):
            continue
        if inch > 0:
            found.add(round(12.0 / inch, 3))
    for m in _METRIC.finditer(text or ""):
        v = float(m.group(1))
        if 10 <= v <= 2000:
            found.add(v)
    if len(found) == 1:
        return found.pop()
    return None


def px_to_ft(px: float, page_width_px: float, paper_width_pt: float, ratio: float) -> float:
    paper_in = px * (paper_width_pt / page_width_px) / 72.0
    return paper_in * ratio / 12.0


def tree_length_px(xy: np.ndarray) -> tuple[float, list[tuple[int, int]]]:
    """Rectilinear (L1) minimum spanning tree over points: total length and edges."""
    if len(xy) < 2:
        return 0.0, []
    d = cdist(xy, xy, metric="cityblock")
    mst = minimum_spanning_tree(d).tocoo()
    return float(mst.data.sum()), list(zip(mst.row.tolist(), mst.col.tolist()))


def learn_ratio(pairs: list[tuple[float, float]]) -> float | None:
    """Median of estimator_ft / tree_ft over sheets where both are > 0."""
    r = [a / b for a, b in pairs if a > 0 and b > 0]
    return float(np.median(r)) if r else None


def is_conduit_line(name: str) -> bool:
    """Estimator lines named "Distance N" are measurements, not runs."""
    return not re.match(r"^\s*distance\b", name or "", re.IGNORECASE)
