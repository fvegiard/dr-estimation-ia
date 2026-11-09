"""Read EEWin raw CSV exports (data/raw) into engine objects."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from .engine import Assembly, Component, Product, Units, norm_unit

RAW = Path(__file__).resolve().parents[1] / "eewin" / "catalogue-llm" / "data" / "raw"


def rows(name: str, raw: Path = RAW):
    with open(raw / f"{name}.csv", encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def num(s: str | None) -> float:
    try:
        return float(s) if s not in (None, "") else 0.0
    except ValueError:
        return 0.0


def load_units(raw: Path = RAW) -> Units:
    base = {norm_unit(r["CodeEN"]): (norm_unit(r["BaseUnitCodeEN"]), num(r["BaseUnitRatio"]), r["CompatibilityGroup"])
            for r in rows("units", raw)}
    direct = {(norm_unit(r["UnitFrom"]), norm_unit(r["UnitTo"])): num(r["Ratio"])
              for r in rows("unit_conversions", raw) if r["UnitToUnit"] == "True"}
    return Units(base, direct)


def net_price(r: dict) -> float:
    promo = num(r.get("PROMCOUNET"))
    if promo > 0:
        return promo
    return num(r["COUBRUTUNI"]) * (1 - num(r["COUESC"]) / 100)


def product_from(r: dict) -> Product:
    return Product(
        code=r["PRO_ID"], description=r["DESC"].strip(), price=net_price(r), price_unit=norm_unit(r["COUUM"]),
        labor_hours=num(r["TEMPUNI"]), labor_unit=norm_unit(r["TEMPUM"]), supplier=r.get("CODEFOUR", ""),
        mfr_no=r.get("CLEMANU", ""), price_date=r.get("DATECOUT", ""))


def component_from(r: dict) -> Component:
    return Component(r["PRO_ID"], num(r["QTE"]), norm_unit(r["QTEUM"]), (r["TYPRATIO"] or "L").upper(),
                     num(r["DIV"]) or 1.0, norm_unit(r["DIVUM"]))


def assembly_from(r: dict, comps: list[Component]) -> Assembly:
    return Assembly(r["ENS_ID"], r["DESC"].strip(), norm_unit(r["COUUM"]), num(r["TEMPUNI"]),
                    norm_unit(r["TEMPUM"]), num(r["TEMPSEC"]), comps)


def load_catalog(raw: Path = RAW):
    products = {r["PRO_ID"]: product_from(r) for r in rows("products", raw)}
    comps = defaultdict(list)
    for r in sorted(rows("assembly_components", raw), key=lambda r: (r["ENS_ID"], r["ORDRE"])):
        comps[r["ENS_ID"]].append(component_from(r))
    assemblies = {r["ENS_ID"]: assembly_from(r, comps[r["ENS_ID"]]) for r in rows("assemblies", raw)}
    return products, assemblies
