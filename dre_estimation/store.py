"""Local catalog (data/dre.sqlite): search, lookups and deterministic estimates."""
from __future__ import annotations

import math
import sqlite3
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

from .engine import Assembly, Component, Line, Product, Units, count_unit, price_assembly, price_product
from .search import where_score

DB = Path(__file__).resolve().parents[1] / "eewin" / "catalogue-llm" / "data" / "dre.sqlite"
DEFAULT_RATE = 72.0
MAX_LIMIT = 50  # search results; SQLite treats a negative LIMIT as unlimited
MAX_QTY = 1e9   # per line; keeps every amount far below the 28 digits rnd() can quantize


def rnd(x: float, places: int = 2) -> float:
    """Round half up (money convention), not Python's half-even. Goes through 15 significant digits
    like Postgres' float8 -> numeric cast, so local and cloud estimates round identically."""
    return float(Decimal(f"{x:.15g}").quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def _limit(limit: Any, default: int = 10) -> int:
    try:
        n = int(limit)
    except (TypeError, ValueError, OverflowError):
        n = default
    return max(1, min(n, MAX_LIMIT))


class Store:
    def __init__(self, path: Path | str = DB):
        if not Path(path).exists():
            raise FileNotFoundError(f"{path} not found - run scripts/build_db.py first")
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        direct = {(r["unit_from"], r["unit_to"]): r["ratio"] for r in self.con.execute("SELECT * FROM unit_ratios")}
        self.units = Units({}, direct)

    # ---- search -------------------------------------------------------------------------
    def search_products(self, query: str, limit: int = 10, priced_only: bool = False) -> list[dict]:
        score, params, n = where_score(query)
        if not n:
            return []
        need = max(1, math.ceil(n * 0.6))
        sql = f"""SELECT code, mfr_no, description, supplier, category_desc, price, price_unit, price_date,
                         labor_hours, labor_unit, labor_source, times_quoted, {score} AS score
                  FROM products WHERE {"price > 0 AND " if priced_only else ""}({score}) >= ?
                  ORDER BY score DESC, (price > 0) DESC, times_quoted DESC, length(description), code LIMIT ?"""
        cur = self.con.execute(sql, params + params + [need, _limit(limit)])
        return [dict(r) | {"match": f"{r['score']}/{n}"} for r in cur]

    def search_assemblies(self, query: str, limit: int = 10) -> list[dict]:
        score, params, n = where_score(query)
        if not n:
            return []
        need = max(1, math.ceil(n * 0.6))
        sql = f"""SELECT code, description, unit, labor_hours, section_hours, times_quoted, {score} AS score
                  FROM assemblies WHERE ({score}) >= ? ORDER BY score DESC, times_quoted DESC, code LIMIT ?"""
        cur = self.con.execute(sql, params + params + [need, _limit(limit)])
        out = []
        for r in cur:
            est = self.estimate([{"code": r["code"], "qty": 1}])
            out.append(dict(r) | {"match": f"{r['score']}/{n}", "material_per_unit": est["lines"][0]["material"],
                                  "warnings": est["lines"][0]["warnings"]})
        return out

    # ---- lookups ------------------------------------------------------------------------
    def product(self, code: str) -> Product | None:
        r = self.con.execute("SELECT * FROM products WHERE code = ? OR (mfr_no = ? AND mfr_no <> '') "
                             "ORDER BY code = ? DESC, price > 0 DESC LIMIT 1", (code, code, code)).fetchone()
        if r is None:
            return None
        return Product(r["code"], r["description"], r["price"], r["price_unit"], r["labor_hours"], r["labor_unit"],
                       r["supplier"], r["mfr_no"], r["price_date"], r["labor_source"])

    def mfr_matches(self, mfr_no: str) -> list[str]:
        """Codes of the products carrying this manufacturer number (several = ambiguous)."""
        return [r[0] for r in self.con.execute("SELECT code FROM products WHERE mfr_no = ? ORDER BY code", (mfr_no,))]

    def assembly(self, code: str) -> Assembly | None:
        r = self.con.execute("SELECT * FROM assemblies WHERE code = ?", (code,)).fetchone()
        if r is None:
            return None
        comps = [Component(c["product_code"], c["qty"], c["qty_unit"], c["kind"], c["div"], c["div_unit"])
                 for c in self.con.execute("SELECT * FROM assembly_components WHERE assembly_code = ? ORDER BY ord",
                                           (code,))]
        return Assembly(r["code"], r["description"], r["unit"], r["labor_hours"], r["labor_unit"],
                        r["section_hours"], comps)

    def labor_rates(self) -> list[dict]:
        return [dict(r) for r in self.con.execute("SELECT * FROM labor_rates ORDER BY code")]

    def meta(self) -> dict:
        return {r["key"]: r["value"] for r in self.con.execute("SELECT * FROM meta")}

    # ---- estimate -----------------------------------------------------------------------
    def estimate(self, lines: list[dict], labor_rate: float = DEFAULT_RATE, material_markup_pct: float = 0.0,
                 labor_markup_pct: float = 0.0) -> dict:
        """lines: [{code, qty, unit?, sections?, note?}] - code = product code, mfr no. or assembly code."""
        out, warnings = [], []
        for i, ln in enumerate(lines, 1):
            try:
                if not isinstance(ln, dict):
                    raise TypeError(f"expected an object, got {type(ln).__name__}")
                code, qty = str(ln.get("code", "")).strip(), float(ln.get("qty") or 0)
                unit, sections = ln.get("unit") or "", float(ln.get("sections") or 0)
                if not isinstance(unit, str):
                    raise TypeError(f"unit must be a string, got {type(unit).__name__}")
                if not (abs(qty) <= MAX_QTY and abs(sections) <= MAX_QTY):  # also refuses nan and inf
                    raise ValueError(f"qty and sections must be finite numbers within +/-{MAX_QTY:g}")
            except (TypeError, ValueError, OverflowError) as e:
                code, note = (str(ln.get("code", "")).strip(), ln.get("note", "")) if isinstance(ln, dict) else ("", "")
                out.append(_row(i, Line(code, "INVALID LINE", 0.0, "", 0, 0, ["INVALID LINE"]), {"note": note},
                                labor_rate))
                warnings.append(f"line {i}: invalid line ({e})")
                continue
            a = self.assembly(code)
            if a is not None:
                res = price_assembly(a, qty, unit, sections, _ProductMap(self), self.units)
            else:
                p = self.product(code)
                if p is None:
                    out.append(_row(i, Line(code, "UNKNOWN CODE", qty, unit, 0, 0, ["UNKNOWN CODE"]), ln, labor_rate))
                    warnings.append(f"line {i}: unknown code {code}")
                    continue
                res = price_product(p, qty, unit or count_unit(p.price_unit), self.units)
                if p.code != code and (n := len(self.mfr_matches(code))) > 1:
                    res.warnings.append(f"mfr no. {code} matches {n} products, used {p.code}")
            if not qty:
                res.warnings.append("QTY 0")
            out.append(_row(i, res, ln, labor_rate))
            warnings += [f"line {i} ({res.code}): {w}" for w in res.warnings]
        material = sum(Decimal(repr(r["material"])) for r in out)  # totals = sum of the rounded lines
        hours = sum(Decimal(repr(r["hours"])) for r in out)
        rate = Decimal(repr(float(labor_rate)))
        labor = hours * rate
        sell = (material * (1 + Decimal(repr(float(material_markup_pct))) / 100)
                + labor * (1 + Decimal(repr(float(labor_markup_pct))) / 100))
        return {
            "lines": out,
            "totals": {"material_cost": rnd(float(material)), "labor_hours": rnd(float(hours)),
                       "labor_rate": labor_rate, "labor_cost": rnd(float(labor)),
                       "cost_total": rnd(float(material + labor)),
                       "material_markup_pct": material_markup_pct, "labor_markup_pct": labor_markup_pct,
                       "sell_total": rnd(float(sell))},
            "warnings": warnings,
            "prices_as_of": self.meta().get("prices_as_of", ""),
        }


class _ProductMap(dict):
    """Lazy product lookup for assembly components."""
    def __init__(self, store: Store):
        super().__init__()
        self.store = store

    def get(self, code, default=None):
        if code not in self:
            p = self.store.product(code)
            if p is None:
                return default
            self[code] = p
        return self[code]


def _row(i: int, ln: Line, src: dict, rate: float) -> dict:
    return {"line": i, "code": ln.code, "description": ln.description, "kind": ln.kind, "qty": ln.qty,
            "unit": ln.unit, "sections": float(src.get("sections") or 0), "note": src.get("note", ""),
            "material": (m := rnd(ln.material)), "hours": (h := rnd(ln.hours, 3)), "labor_cost": rnd(h * rate),
            "total": rnd(m + h * rate), "warnings": ln.warnings,
            "components": [{"code": c.code, "description": c.description, "qty": rnd(c.qty, 4), "unit": c.unit,
                            "material": rnd(c.material), "hours": rnd(c.hours, 3), "warnings": c.warnings}
                           for c in ln.children]}
