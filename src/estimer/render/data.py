"""Renderer input model: load an estimer output directory into per-sheet items.

Input directory layout (the `python -m src.estimer` output, optionally enriched):

  estimate.json   required. `sheets[]` gives page (1-based, in the plans PDF), sheet name and the
                  raster size the positions are expressed in (width_px / height_px). `counters[].elements[]`
                  gives one detected symbol each: sheet, page, x, y (raster px, top-left origin).
                  Optional per-element keys understood here: repere, source, bbox [x0, y0, x1, y1]
                  (same units as x/y), shape (circle | rect | diamond), code, flags.
  bordereau.csv   optional. One row per repere, columns
                  feuille,repere,source,materiel,designation,qte,portee,modele,prescription,parent[,reserve]
                  (the HR26-14 gold `bordereau-materiel.csv` schema). Joined on (feuille, repere); gives the
                  descriptive bordereau fields. Without it, fields are derived from the estimator family.
  reserves.md     optional. `## <sheet>` sections; each following non-empty line is printed in the
                  "RESERVES ET COMPLEMENTS" block of that sheet's bordereau.

Positions are converted to PDF points of the plans page at render time (see `to_points`).
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPERE_RE = re.compile(r"^([A-Z]+\d{2})-(\d+)$")

# Default bordereau wording when only the estimator's family counts are available.
DEFAULT_MODEL = "MODELE NON PRECISE"
DEFAULT_PORTEE = "A PRECISER"
DEFAULT_PRESCRIPTION = "Detection automatique; identification a revalider sur le plan"


@dataclass
class Item:
    """One counted symbol = one bordereau row = one marker on the plan."""
    sheet: str
    page: int                      # 1-based page in the plans PDF
    x: float                       # position in source units (see Sheet.width_px)
    y: float
    code: str                      # family code shown in the legend (I01, M03, ...)
    repere: str                    # I01-03
    source: str = ""               # source symbol id (DSI01-044)
    materiel: str = ""
    designation: str = ""
    qte: float = 1
    portee: str = ""
    modele: str = ""
    prescription: str = ""
    parent: str = ""
    bbox: tuple[float, float, float, float] | None = None
    shape: str = "circle"
    flags: list[str] = field(default_factory=list)
    reserve_override: bool | None = None

    @property
    def reserve(self) -> bool:
        """RES = reserve on source, model, position, scope or reconciliation (FORMAT-EXEMPLE).

        Every repere is in reserve unless the input explicitly clears it (`reserve` = 0/false): the EXEMPLE
        marks all 886 repere rows RES (12/12 sheet headers: RES = reperes), since native Plan Expert
        verification is unavailable and an automatic detection is always to be revalidated.
        """
        return True if self.reserve_override is None else self.reserve_override

    @property
    def seq(self) -> int:
        m = REPERE_RE.match(self.repere)
        return int(m.group(2)) if m else 0


@dataclass
class Family:
    code: str
    materiel: str
    shape: str
    qty: float
    reserves: int
    index: int                     # position in the sheet's family order (colour cycle)


@dataclass
class Sheet:
    name: str
    page: int
    width_px: float | None
    height_px: float | None
    items: list[Item] = field(default_factory=list)
    reserves_text: list[str] = field(default_factory=list)

    def families(self) -> list[Family]:
        by: dict[str, list[Item]] = defaultdict(list)
        for it in self.items:
            by[it.code].append(it)
        out = []
        for i, code in enumerate(sorted(by, key=_code_key)):
            its = by[code]
            shapes = defaultdict(int)
            for it in its:
                shapes[it.shape] += 1
            shape = max(shapes, key=lambda s: (shapes[s], s == "circle"))
            mat = next((it.materiel for it in its if it.materiel), code)
            qty = len(its)          # EXEMPLE legend counts reperes; Qte multipliers stay in the bordereau
            out.append(Family(code, mat, shape, qty, sum(1 for it in its if it.reserve), i))
        return out

    @property
    def n_reserves(self) -> int:
        return sum(1 for it in self.items if it.reserve)

    def sorted_items(self) -> list[Item]:
        return sorted(self.items, key=lambda it: (_code_key(it.code), it.seq, it.repere))


def _code_key(code: str):
    m = re.match(r"^([A-Z]+)(\d+)$", code)
    return (m.group(1), int(m.group(2))) if m else (code, 0)


def fmt_qty(q: float) -> str:
    return str(int(q)) if float(q).is_integer() else f"{q:g}"


def read_reserves_md(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\S+)", line)
        if m:
            cur = m.group(1)
            continue
        if cur and line.strip() and not line.startswith("#"):
            out[cur].append(line.strip())
    return dict(out)


def read_bordereau_csv(path: Path) -> dict[tuple[str, str], dict]:
    rows = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows[(r["feuille"].strip(), r["repere"].strip())] = r
    return rows


def _parse_bool(v) -> bool | None:
    if v is None or str(v).strip() == "":
        return None
    return str(v).strip().lower() in ("1", "true", "oui", "yes", "r", "res")


def _parse_qte(v, default: float = 1) -> float:
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return default


def load_input(in_dir: Path) -> list[Sheet]:
    """Read estimate.json (+ bordereau.csv, reserves.md when present) -> sheets with items, page order."""
    in_dir = Path(in_dir)
    est = json.loads((in_dir / "estimate.json").read_text(encoding="utf-8"))
    bpath = in_dir / "bordereau.csv"
    bord = read_bordereau_csv(bpath) if bpath.is_file() else {}
    rpath = in_dir / "reserves.md"
    reserves = read_reserves_md(rpath) if rpath.is_file() else {}

    sheets: dict[str, Sheet] = {}
    for s in est.get("sheets", []):
        sheets[s["sheet"]] = Sheet(s["sheet"], int(s["page"]), s.get("width_px"), s.get("height_px"))

    # family codes for plain estimator output: one code per estimator family, stable across sheets
    fam_codes: dict[str, str] = {}
    seq: dict[tuple[str, str], int] = defaultdict(int)
    n_in_sheet: dict[str, int] = defaultdict(int)
    for counter in est.get("counters", []):
        family = counter.get("family") or counter.get("name", "")
        for el in counter.get("elements", []):
            name = el["sheet"]
            sh = sheets.get(name)
            if sh is None:
                sh = sheets[name] = Sheet(name, int(el["page"]), None, None)
            n_in_sheet[name] += 1
            repere = el.get("repere")
            code = el.get("code")
            if not repere:
                if not code:
                    code = fam_codes.setdefault(family, f"F{len(fam_codes) + 1:02d}")
                seq[(name, code)] += 1
                repere = f"{code}-{seq[(name, code)]:02d}"
            elif not code:
                m = REPERE_RE.match(repere)
                code = m.group(1) if m else repere
            row = bord.get((name, repere), {})
            bbox = el.get("bbox")
            it = Item(
                sheet=name, page=int(el.get("page", sh.page)), x=float(el["x"]), y=float(el["y"]),
                code=code, repere=repere,
                source=row.get("source") or el.get("source") or f"{name}-{n_in_sheet[name]:03d}",
                materiel=(row.get("materiel") or counter.get("name") or family).strip(),
                designation=(row.get("designation") or el.get("designation") or family).strip(),
                qte=_parse_qte(row.get("qte", el.get("qte", 1))),
                portee=(row.get("portee") if row else el.get("portee", DEFAULT_PORTEE)) or "",
                modele=(row.get("modele") if row else el.get("modele", DEFAULT_MODEL)) or "",
                prescription=(row.get("prescription") if row else el.get("prescription", DEFAULT_PRESCRIPTION)) or "",
                parent=(row.get("parent") or el.get("parent") or "").strip(),
                bbox=tuple(bbox) if bbox else None,
                shape=el.get("shape", "circle"),
                flags=list(el.get("flags", [])) if not row else [],
                reserve_override=_parse_bool(row.get("reserve")) if row else _parse_bool(el.get("reserve")),
            )
            sh.items.append(it)
    for name, lines in reserves.items():
        if name in sheets:
            sheets[name].reserves_text = lines
    return sorted((s for s in sheets.values() if s.items), key=lambda s: (s.page, s.name))


def to_points(sheet: Sheet, page_w: float, page_h: float):
    """Return f(x, y) -> (x_pt, y_pt) mapping source units of `sheet` onto a page of page_w x page_h points."""
    kx = page_w / sheet.width_px if sheet.width_px else 1.0
    ky = page_h / sheet.height_px if sheet.height_px else kx
    return lambda x, y: (x * kx, y * ky)
