"""Build per-sheet take-off records from a vector plan PDF whose devices carry printed type tags.

Every quoted tag printed on the sheet ('FGG1') is one record, paired with the circuit label printed
under it (NA-7, SA-10) and anchored on the symbol drawn between them; when the symbol is drawn beside
the tag instead, the pastille sits next to the tag and the record is flagged (never a guessed symbol). Nothing is inferred from symbols
alone. The record layout is the one consumed by render_sheet.py (same as the S-1294 / Granby deliveries).
"""
import math
import re
from collections import defaultdict

import pymupdf

TAG_RE = re.compile(r"^['‘’]([A-Z]{1,4}\d{0,2})['‘’]$")
CIRCUIT_RE = re.compile(r"^[A-Z]{2}-\d+(?:\.\d+)?$")
UNITS = 1920  # records are expressed on a 1920-unit-wide sheet, like the reference deliveries
CELL = 50     # grid size (points) of the spatial index
RAY = 45       # how far (points) a symbol outline may be from the point it encloses
MIN_GAP = 4    # free height (points) needed between a tag and its circuit label to hold a symbol
MAX_SHIFT = 8  # a circuit label further sideways than this is not stacked under its tag
STROKE = 90    # longest stroke (points) still considered part of a device symbol


def _view_rect(page, rect):
    r = pymupdf.Rect(rect) * page.rotation_matrix
    r.normalize()
    return r


def sheet_title(page):
    blocks = [(_view_rect(page, b[:4]), b[4]) for b in page.get_text("blocks") if b[6] == 0]
    label = next(r for r, t in blocks if "Titre Du Dessin" in t)
    below = sorted((r.y0, t) for r, t in blocks if 0 <= r.y0 - label.y1 < 80 and abs(r.x0 - label.x0) < 60)
    return " ".join(" ".join(t.split()) for _, t in below).replace("’", "'")


def tagged_devices(page, max_dist=60):
    """Yield (tag, circuit, target_x, target_y, tag_rect, stacked).

    The target is where the symbol is expected: midway between the tag and its circuit label; stacked
    tells that the label sits right under the tag with room for a symbol between them.
    """
    tags, circuits = [], []
    for w in page.get_text("words"):
        r = _view_rect(page, w[:4])
        centre = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        m = TAG_RE.match(w[4])
        if m:
            tags.append((m.group(1), centre, r))
        elif CIRCUIT_RE.match(w[4]):
            circuits.append((w[4], centre, r))
    # closest pairs first, one circuit label per tag; the label sits level with or below its tag
    pairs = sorted((math.dist(tc, cc), ti, ci) for ti, (_, tc, _) in enumerate(tags)
                   for ci, (_, cc, _) in enumerate(circuits) if math.dist(tc, cc) <= max_dist and cc[1] >= tc[1] - 3)
    assigned, used = {}, set()
    for _, ti, ci in pairs:
        if ti not in assigned and ci not in used:
            assigned[ti] = ci
            used.add(ci)
    for ti, (tag, tc, rect) in enumerate(tags):
        if ti in assigned:
            label, cc, crect = circuits[assigned[ti]]
            stacked = crect.y0 - rect.y1 >= MIN_GAP and abs(tc[0] - cc[0]) <= MAX_SHIFT
            yield tag, label, (tc[0] + cc[0]) / 2, (tc[1] + cc[1]) / 2, rect, stacked
        else:
            yield tag, "", tc[0], tc[1], rect, False


class SymbolIndex:
    """Small drawn shapes of the sheet (fixture outlines, hatches, exit-sign glyphs), indexed on a grid."""

    def __init__(self, page):
        self.cells = defaultdict(list)
        for d in page.get_drawings():
            r = _view_rect(page, d["rect"])
            if 3 <= max(r.width, r.height) <= STROKE:
                self.cells[(int(r.x0 // CELL), int(r.y0 // CELL))].append(r)
        self.words = [_view_rect(page, w[:4]) for w in page.get_text("words")]

    def on_text(self, x, y):
        return any(w.x0 <= x <= w.x1 and w.y0 <= y <= w.y1 for w in self.words)

    def _near(self, x, y):
        cx, cy = int(x // CELL), int(y // CELL)
        return [r for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2) for r in self.cells.get((cx + i, cy + j), ())
                if abs((r.x0 + r.x1) / 2 - x) <= STROKE and abs((r.y0 + r.y1) / 2 - y) <= STROKE]

    def enclosed(self, x, y):
        """True when strokes bound (x, y) on its four sides: the point is inside a drawn symbol outline."""
        left = right = up = down = False
        for r in self._near(x, y):
            in_rows = r.y0 - .5 <= y <= r.y1 + .5
            in_cols = r.x0 - .5 <= x <= r.x1 + .5
            left |= in_rows and r.x0 <= x + .5 and x - r.x1 <= RAY
            right |= in_rows and r.x1 >= x - .5 and r.x0 - x <= RAY
            up |= in_cols and r.y0 <= y + .5 and y - r.y1 <= RAY
            down |= in_cols and r.y1 >= y - .5 and r.y0 - y <= RAY
        return left and right and up and down

    def ink_near(self, x, y, reach=6):
        """True when some small stroke lies within reach of (x, y)."""
        return any(r.x0 - reach <= x <= r.x1 + reach and r.y0 - reach <= y <= r.y1 + reach for r in self._near(x, y))


def _circuit_class(circuit):
    if not circuit:
        return "circuit non indiqué"
    return {"N": "normal", "S": "secours", "U": "UPS"}.get(circuit[:1], "autre circuit")


def build(project, sheet):
    page = pymupdf.open(sheet["pdf"])[0]
    to_units = UNITS / page.rect.width
    replaced = project["replaced_tags"]
    kept = set(sheet.get("kept_tags", []))
    symbols = SymbolIndex(page)
    devices = sorted(tagged_devices(page, project.get("max_dist", 60)),
                     key=lambda d: (d[0] not in replaced, d[0], _circuit_class(d[1]), d[3], d[2]))
    records = []
    for tag, circuit, tx, ty, tag_rect, stacked in devices:
        located = (bool(circuit) and not symbols.on_text(tx, ty) and symbols.ink_near(tx, ty)
                   and (stacked or symbols.enclosed(tx, ty)))
        if located:  # the symbol is drawn between the tag and its circuit label
            x, y = tx, ty
        else:  # symbol drawn beside the tag: never guess which one, sit next to the tag and flag it
            cy = (tag_rect.y0 + tag_rect.y1) / 2
            spots = [(tag_rect.x0 - 7, cy), (tag_rect.x1 + 7, cy), ((tag_rect.x0 + tag_rect.x1) / 2, tag_rect.y0 - 7)]
            x, y = next((p for p in spots if not symbols.on_text(*p)), spots[0])
        rec = {"tag": tag, "label": circuit, "x": round(x * to_units, 2), "y": round(y * to_units, 2), "quantity": 1,
               "circuits": circuit, "radius": 4.2, "parent": "", "on_symbol": located,
               "mid_x": round(tx * to_units, 2), "mid_y": round(ty * to_units, 2)}
        if tag in replaced:
            rec["family"] = f"{tag} {_circuit_class(circuit)} — à remplacer par DEL"
            rec["scope"] = "REMPLACER"
            rec["model"] = sheet["model"]
        else:
            rec["family"] = f"{tag} existant"
            rec["scope"] = "CONSERVER" if tag in kept else "A PRECISER"
            rec["model"] = "EXISTANT - MODELE NON INDIQUE"
        reserve = []
        if not circuit:
            reserve.append("Circuit non indiqué près du repère au plan.")
        if not located:
            reserve.append("Symbole adjacent au repère; pastille posée à côté du repère, à revalider.")
        rec["reserve"] = " ".join(reserve)
        records.append(rec)
    notes = [n.format(model=sheet["model"]) for n in project["notes"]] + sheet.get("notes", [])
    return {"key": sheet["sheet"], "page": 1, "title": sheet_title(page), "type": "equipment", "pdf": sheet["pdf"],
            "scope": project["scope"], "records": records, "notes": notes}
