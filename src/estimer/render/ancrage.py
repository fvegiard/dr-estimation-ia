"""Symbol anchoring: move a mark from its text tag to the vector symbol it labels (EXEMPLE: the marker
surrounds the SYMBOL, "ancrage PDF exact").

CAD exports merge thousands of same-style strokes into one PDF path, so `page.get_drawings()` rectangles are
useless on their own. Every path item (line, curve, rectangle, quad) is turned into graph edges between its
end points (snapped to 0.25 pt). A symbol is a small CLOSED shape: the 2-edge-connected components of that
graph (bridges removed: wire tails, stems between a box and its circle, leaders) whose bounding box is 3-30 pt.
A lone arc (door swing, piece of a large circle) is not closed and is never a candidate.

Resolution order for a text tag (`anchor`):
  1. the tag letters sit inside strokes on all four sides (F in its box, RT, P.R., D in its ring, T15 in its
     hexagon) -> centre of that enclosure;
  2. a closed symbol touching the tag box -> that symbol;
  3. the closest closed symbol within `radius`, score = distance + COLOR_PENALTY when its colour differs from
     the tag's; grey (background architecture) shapes are skipped unless the tag itself is grey; the result is
     flagged ambiguous when a distinct second symbol scores within AMBIGUITY pt;
  4. nothing -> None (the caller keeps the text position and puts the line in reserve with '*').
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

import pymupdf

EPS = 0.05             # half-thickness given to zero-width strokes (an empty Rect never intersects in PyMuPDF)
SNAP = 0.25            # end points closer than this are the same graph node
CELL = 40.0            # spatial grid cell (pt)
MAX_PRIM = 150.0       # primitives longer than this are walls, grids, long leaders: never part of a symbol
SYM_MIN, SYM_MAX = 3.0, 30.0
LINEAR_MAX, LINEAR_W = 150.0, 12.0   # closed elongated shapes: linear fixtures, baseboard heaters
ENCLOSE_REACH = 25.0   # tag letters with strokes on all 4 sides within 25 pt sit inside their symbol
ENCLOSE_MAX = 50.0
COLOR_PENALTY = 10.0   # extra pt of distance for a symbol whose colour differs from the tag's
AMBIGUITY = 1.5        # two distinct symbols whose scores differ by less than this: ambiguous (*)


@dataclass
class Anchor:
    x: float
    y: float
    bbox: tuple[float, float, float, float]
    dist: float
    ambiguous: bool = False       # another symbol scores almost as well: identification to revalidate (*)


def _is_grey(c) -> bool:
    return c is not None and max(c) - min(c) < 0.03 and 0.35 < c[0] < 0.95


def _rect_dist(r: pymupdf.Rect, box: pymupdf.Rect) -> float:
    dx = max(box.x0 - r.x1, r.x0 - box.x1, 0.0)
    dy = max(box.y0 - r.y1, r.y0 - box.y1, 0.0)
    return math.hypot(dx, dy)


def _edges(it) -> list[tuple[pymupdf.Point, pymupdf.Point]]:
    kind = it[0]
    if kind == "l":
        return [(it[1], it[2])]
    if kind == "c":
        return [(it[1], it[4])]
    if kind == "re":
        r = pymupdf.Rect(it[1])
        return [(r.tl, r.tr), (r.tr, r.br), (r.br, r.bl), (r.bl, r.tl)]
    if kind == "qu":
        q = it[1]
        return [(q.ul, q.ur), (q.ur, q.lr), (q.lr, q.ll), (q.ll, q.ul)]
    return []


def _bridges(n_nodes: int, adj: list[list[tuple[int, int]]]) -> set[int]:
    """Edge ids that are bridges (iterative Tarjan; parallel edges handled by edge id)."""
    disc = [-1] * n_nodes
    low = [0] * n_nodes
    out: set[int] = set()
    t = 0
    for root in range(n_nodes):
        if disc[root] != -1 or not adj[root]:
            continue
        disc[root] = low[root] = t
        t += 1
        stack = [(root, -1, iter(adj[root]))]
        while stack:
            v, pe, it = stack[-1]
            advanced = False
            for w, e in it:
                if e == pe:
                    continue
                if disc[w] == -1:
                    disc[w] = low[w] = t
                    t += 1
                    stack.append((w, e, iter(adj[w])))
                    advanced = True
                    break
                low[v] = min(low[v], disc[w])
            if not advanced:
                stack.pop()
                if stack:
                    u = stack[-1][0]
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        out.add(pe)
    return out


def _cells(r: pymupdf.Rect):
    for gx in range(int(r.x0 // CELL), int(r.x1 // CELL) + 1):
        for gy in range(int(r.y0 // CELL), int(r.y1 // CELL) + 1):
            yield gx, gy


class SymbolIndex:
    """Closed vector shapes (symbol candidates) and short strokes of a page, in page.rect coordinates."""

    def __init__(self, page: pymupdf.Page):
        M = page.rotation_matrix              # drawings come unrotated; marks live in page.rect coordinates
        rot = bool(page.rotation)
        nodes: dict[tuple[int, int], int] = {}
        pts: list[pymupdf.Point] = []
        edges: list[tuple[int, int, object]] = []
        self.cells: dict[tuple[int, int], list[int]] = defaultdict(list)
        self.rects: list[pymupdf.Rect] = []   # short strokes, for the enclosure rays
        self.colors: list = []

        def node(p: pymupdf.Point) -> int:
            key = (round(p.x / SNAP), round(p.y / SNAP))
            k = nodes.get(key)
            if k is None:
                k = nodes[key] = len(pts)
                pts.append(p)
            return k

        for d in page.get_drawings():
            col, fill = d.get("color"), d.get("fill")
            if col is None and fill is not None and min(fill) > 0.97:
                continue                                    # white text masks behind tags
            c = col if col is not None else fill
            for it in d["items"]:
                for a, b in _edges(it):
                    if rot:
                        a, b = a * M, b * M
                    r = pymupdf.Rect(a, b).normalize()
                    if max(r.width, r.height) > MAX_PRIM:
                        continue
                    edges.append((node(a), node(b), c))
                    r = r + (-EPS, -EPS, EPS, EPS)
                    k = len(self.rects)          # stroke k == edge k
                    self.rects.append(r)
                    self.colors.append(c)
                    for cell in _cells(r):
                        self.cells[cell].append(k)

        adj: list[list[tuple[int, int]]] = [[] for _ in pts]
        for e, (a, b, _) in enumerate(edges):
            if a != b:
                adj[a].append((b, e))
                adj[b].append((a, e))
        br = _bridges(len(pts), adj)
        comp = [-1] * len(pts)                  # 2-edge-connected components = closed shapes
        self.edge_comp = [-1] * len(edges)      # closed shape id of each stroke (-1: bridge, open line)
        self.shapes: list[tuple[pymupdf.Rect, object]] = []
        self.shape_cells: dict[tuple[int, int], list[int]] = defaultdict(list)
        for s in range(len(pts)):
            if comp[s] != -1 or not adj[s]:
                continue
            comp[s] = s
            todo, members, cols, n_edges = [s], [s], [], set()
            while todo:
                v = todo.pop()
                for w, e in adj[v]:
                    if e in br:
                        continue
                    n_edges.add(e)
                    self.edge_comp[e] = s
                    if edges[e][2] is not None:
                        cols.append(edges[e][2])
                    if comp[w] == -1:
                        comp[w] = s
                        todo.append(w)
                        members.append(w)
            if len(n_edges) < 2:
                continue                                    # no cycle through this node
            r = pymupdf.Rect(pts[members[0]], pts[members[0]])
            for m in members[1:]:
                r.include_point(pts[m])
            big, small = max(r.width, r.height), min(r.width, r.height)
            linear = big > SYM_MAX and big <= LINEAR_MAX and small <= LINEAR_W and big >= 3 * small
            if small < 1.5 or not (SYM_MIN <= big <= SYM_MAX or linear):
                continue                                    # linear = strip light, baseboard heater (PL)
            k = len(self.shapes)
            self.shapes.append((r, cols[0] if cols else None))
            for cell in _cells(r):
                self.shape_cells[cell].append(k)

    def near(self, area: pymupdf.Rect) -> list[int]:
        out = set()
        for cell in _cells(area):
            for k in self.cells.get(cell, ()):
                if self.rects[k].intersects(area):
                    out.add(k)
        return sorted(out)

    def shapes_near(self, area: pymupdf.Rect):
        seen = set()
        for cell in _cells(area):
            for k in self.shape_cells.get(cell, ()):
                if k not in seen and self.shapes[k][0].intersects(area):
                    seen.add(k)
                    yield self.shapes[k]

    def enclosure(self, p: pymupdf.Point, reach: float = ENCLOSE_REACH, same_shape: bool = True):
        """Box drawn around point p: nearest non-grey stroke crossing each of the 4 rays (left, right, up,
        down) within `reach` pt. Returns that box, or None when one side is open. `same_shape=False` accepts
        4 sides from different outlines (a baseboard drawn against a wall shares its edge with the wall)."""
        area = pymupdf.Rect(p.x - reach, p.y - reach, p.x + reach, p.y + reach)
        hit = {"l": None, "r": None, "u": None, "d": None}      # side -> (coordinate, closed shape id)
        for k in self.near(area):
            if _is_grey(self.colors[k]):
                continue
            r, cid = self.rects[k], self.edge_comp[k]
            if r.y0 <= p.y <= r.y1:
                if r.x1 < p.x - 0.5 and (hit["l"] is None or r.x1 > hit["l"][0]):
                    hit["l"] = (r.x1, cid)
                if r.x0 > p.x + 0.5 and (hit["r"] is None or r.x0 < hit["r"][0]):
                    hit["r"] = (r.x0, cid)
            if r.x0 <= p.x <= r.x1:
                if r.y1 < p.y - 0.5 and (hit["u"] is None or r.y1 > hit["u"][0]):
                    hit["u"] = (r.y1, cid)
                if r.y0 > p.y + 0.5 and (hit["d"] is None or r.y0 < hit["d"][0]):
                    hit["d"] = (r.y0, cid)
        if any(v is None for v in hit.values()):
            return None
        ids = {v[1] for v in hit.values()}
        if same_shape and (len(ids) != 1 or -1 in ids):
            return None                   # the 4 sides are not one closed outline (open area between strokes)
        return pymupdf.Rect(hit["l"][0], hit["u"][0], hit["r"][0], hit["d"][0])


def anchor(index: SymbolIndex, tag: pymupdf.Rect, radius: float, tag_color=None,
           words: list | None = None) -> Anchor | None:
    """Symbol designated by a text tag (see module docstring), or None. `words` (word_boxes of the page):
    a closed shape around OTHER text (revision delta "1", another tag's box, a circuit number) belongs to
    that text and is never the tag's symbol."""
    cpt = pymupdf.Point((tag.x0 + tag.x1) / 2, (tag.y0 + tag.y1) / 2)
    box = index.enclosure(cpt)
    if box is not None and max(box.width, box.height) <= ENCLOSE_MAX \
            and box.width >= 0.8 * tag.width and box.height >= 0.8 * tag.height:
        c = (box.tl + box.br) / 2                           # (1)
        return Anchor(c.x, c.y, (box.x0, box.y0, box.x1, box.y1), 0.0)
    tag_grey = _is_grey(tag_color)
    area = pymupdf.Rect(tag) + (-radius, -radius, radius, radius)
    scored = []
    others = [w[0] for w in (words or []) if w[0].intersects(area) and not w[0].intersects(tag)]
    for r, col in index.shapes_near(area):
        if _is_grey(col) and not tag_grey:
            continue                                        # background architecture
        if any(r.contains(pymupdf.Point((w.x0 + w.x1) / 2, (w.y0 + w.y1) / 2)) for w in others):
            continue                                        # shape drawn around other text
        d = _rect_dist(r, tag)
        score = d
        if tag_color is not None and col is not None and max(abs(a - b) for a, b in zip(col, tag_color)) > 0.1:
            score += COLOR_PENALTY
        if score > radius:
            continue
        c = (r.tl + r.br) / 2
        scored.append((score, math.hypot(c.x - cpt.x, c.y - cpt.y), c, r, d))
    if not scored:
        return None
    scored.sort(key=lambda t: (t[0], t[1]))
    s0, _, c, r, d = scored[0]
    if d == 0.0:                                            # (2) touching the tag
        return Anchor(c.x, c.y, (r.x0, r.y0, r.x1, r.y1), 0.0)
    amb = any(t[0] - s0 < AMBIGUITY and not t[3].intersects(r) and math.hypot(t[2].x - c.x, t[2].y - c.y) > 4.0
              for t in scored[1:])
    return Anchor(c.x, c.y, (r.x0, r.y0, r.x1, r.y1), d, amb)   # (3)


def word_boxes(page: pymupdf.Page) -> list[tuple[pymupdf.Rect, str, tuple]]:
    """Words of the page in page.rect coordinates (rotation handled), with their text colour."""
    M = page.rotation_matrix
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                c = s["color"]
                rgb = ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
                x0, y0, x1, y1 = s["bbox"]
                out.append((pymupdf.Rect(x0, y0, x1, y1) * M, s["text"], rgb))
    return out
