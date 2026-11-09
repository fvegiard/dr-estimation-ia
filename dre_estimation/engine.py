"""Deterministic pricing engine: unit conversion, product lines, assembly expansion.

The LLM never does arithmetic. It picks product/assembly codes and quantities;
everything here is plain code so the same input always gives the same total.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class UnitError(ValueError):
    pass


@dataclass
class Units:
    """Unit codes and conversion ratios, loaded from EEWin's Sys_Units / Sys_UnitsConversion."""
    base: dict[str, tuple[str, float, str]]  # code -> (base unit, ratio to base, compatibility group)
    direct: dict[tuple[str, str], float]      # (from, to) -> how many `to` in one `from`

    def ratio(self, frm: str, to: str) -> float:
        """How many `to` units are in one `frm` unit (e.g. ratio('U','C') == 0.01)."""
        frm, to = norm_unit(frm), norm_unit(to)
        if frm == to:
            return 1.0
        if (frm, to) in self.direct and self.direct[(frm, to)] > 0:
            return self.direct[(frm, to)]
        if frm in self.base and to in self.base:
            bf, rf, gf = self.base[frm]
            bt, rt, gt = self.base[to]
            if bf == bt:
                return rf / rt
            if gf == gt and (bf, bt) in self.direct:  # e.g. metre <-> foot
                return rf * self.direct[(bf, bt)] / rt
        raise UnitError(f"no conversion from {frm!r} to {to!r}")


# Packaged price units -> the unit people count in (qty 40 of a "per 100" item = 40 each).
COUNT_UNIT = {"C": "U", "K": "U", "HM": "M", "KM": "M", "CF": "F", "KF": "F", "CL": "L", "CB": "LB", "CK": "KG"}


def count_unit(u: str) -> str:
    u = norm_unit(u)
    return COUNT_UNIT.get(u, u)


def norm_unit(u: str | None) -> str:
    u = (u or "").strip().upper()
    return {"P": "F", "CP": "CF", "KP": "KF", "PQ": "PG", "H": "U", "": "U"}.get(u, u)


@dataclass
class Product:
    code: str
    description: str
    price: float          # net price per `price_unit` (0 = no price)
    price_unit: str
    labor_hours: float    # hours per `labor_unit` (0 = unknown)
    labor_unit: str
    supplier: str = ""
    mfr_no: str = ""
    price_date: str = ""
    labor_source: str = "catalog"


@dataclass
class Component:
    product_code: str
    qty: float
    qty_unit: str
    kind: str      # 'L' = per assembly unit (qty per `div` `div_unit`), 'S' = per section
    div: float = 1.0
    div_unit: str = ""


@dataclass
class Assembly:
    code: str
    description: str
    unit: str
    labor_hours: float     # stored hours per assembly unit
    labor_unit: str
    section_hours: float   # extra hours per section
    components: list[Component] = field(default_factory=list)


@dataclass
class Line:
    code: str
    description: str
    qty: float
    unit: str
    material: float
    hours: float
    warnings: list[str] = field(default_factory=list)
    kind: str = "product"
    children: list["Line"] = field(default_factory=list)


def price_product(p: Product, qty: float, unit: str, units: Units, mult: float = 1.0,
                  estimated_labor: bool = True) -> Line:
    unit = norm_unit(unit or p.price_unit)
    warnings: list[str] = []
    material = hours = 0.0
    if p.price > 0:
        try:
            material = qty * units.ratio(unit, p.price_unit) * p.price * mult
        except UnitError as e:
            warnings.append(f"price unit: {e}")
    else:
        warnings.append("NO PRICE")
    if p.labor_hours > 0 and (estimated_labor or p.labor_source == "catalog"):
        try:
            hours = qty * units.ratio(unit, p.labor_unit) * p.labor_hours * mult
        except UnitError as e:
            warnings.append(f"labor unit: {e}")
        if p.labor_source != "catalog":
            warnings.append(f"labor estimated ({p.labor_source})")
    elif estimated_labor:
        warnings.append("NO LABOR TIME")
    return Line(p.code, p.description, qty, unit, material, hours, warnings)


def price_assembly(a: Assembly, qty: float, unit: str, sections: float,
                   products: dict[str, Product], units: Units, mult: float = 1.0) -> Line:
    unit = norm_unit(unit or a.unit)
    children: list[Line] = []
    warnings: list[str] = []

    def warn(w: str) -> None:
        if w not in warnings:
            warnings.append(w)

    for c in a.components:
        used = bool((sections if c.kind == "S" else qty) * c.qty)  # a zero-quantity component never warns
        p = products.get(c.product_code)
        if p is None:
            if used:
                warn(f"missing component {c.product_code}")
            continue
        if c.kind == "S":
            cqty = sections * c.qty
        else:
            div_unit = norm_unit(c.div_unit or a.unit)
            try:
                per = units.ratio(unit, div_unit) / (c.div or 1.0)
            except UnitError as e:
                if used:
                    warn(f"{c.product_code}: {e}")
                continue
            cqty = qty * per * c.qty
        # Inside assemblies EEWin uses catalog labor only (0 = intentionally no labor, e.g. connectors).
        children.append(price_product(p, cqty, c.qty_unit, units, mult, estimated_labor=False))
    material = sum(ch.material for ch in children)
    # EEWin quotes use the assembly's stored labor time (validated on past quotes); the
    # component sum is only a fallback when the assembly has none.
    hours = sum(ch.hours for ch in children)
    stored = failed = False  # stored labor replaced the component hours / its unit conversion failed
    if a.labor_hours > 0:
        try:
            hours = qty * units.ratio(unit, a.labor_unit or a.unit) * a.labor_hours * mult
            stored = True
        except UnitError as e:
            failed = True
            warn(f"assembly labor unit: {e}")
    hours += sections * a.section_hours * mult
    for ch in children:
        if not ch.qty:
            continue
        for w in ch.warnings:
            if stored and w.startswith("labor unit:"):  # those hours were discarded
                continue
            warn(f"{ch.code} {w.lower() if w == 'NO PRICE' else w}")
    if (qty or sections) and not hours and a.section_hours <= 0 and not failed:
        warn("NO LABOR TIME")
    return Line(a.code, a.description, qty, unit, material, hours, warnings, "assembly", children)
