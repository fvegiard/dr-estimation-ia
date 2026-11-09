"""MCP server exposing the DRE Électrique catalog to Claude (or any MCP client).

The model searches and chooses codes/quantities; all prices, unit conversions and totals
are computed by code (Store.estimate), never by the model.
"""
from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from .store import DEFAULT_RATE, Store
from .xlsx import write_quote

INSTRUCTIONS = """Estimating tool for DRE Électrique (data from ACCEO Estimation / EEWin, Lumen prices).
Workflow: 1) break the job into items with quantities; 2) prefer search_assemblies (installed items with
their boxes, connectors, wire and labor) and fall back to search_products; 3) call price_estimate with the
chosen codes - never compute prices, unit conversions or totals yourself; 4) show the user EVERY warning and ask
for a review: NO PRICE, NO LABOR TIME, labor estimated, QTY 0, failed unit conversion ("no conversion from"),
"mfr no. X matches N products, used Y" (confirm the product), and INVALID LINE / UNKNOWN CODE (that line is
priced 0 and is NOT in the totals); 5) export_estimate_xlsx when asked, and show every entry of unpriced_lines.
Units: U=each, C=per 100, K=per 1000, F=foot, CF=100 ft, M=metre, KM=km. Quantities are in the unit you pass;
default is each (U) for items priced per 100/1000, feet for per-100/1000-ft, metres for per-km, and the
assembly's own unit for assemblies. Descriptions are abbreviated FR/EN (PRISE=receptacle, BOITE=box, TMEC=EMT)."""

mcp = MCPServer("dre-estimation", instructions=INSTRUCTIONS)
_store: Store | None = None


def store() -> Store:
    global _store
    if _store is None:
        _store = Store()
    return _store


@mcp.tool()
def search_products(query: str, limit: int = 10, priced_only: bool = False) -> list[dict]:
    """Fuzzy search of the 32k-product catalog (FR/EN, abbreviations, mfr numbers).
    Returns code, description, price per price_unit, labor hours per labor_unit, labor_source
    (catalog / past quotes / same mfr no. / none) and times_quoted (how often DRE used it)."""
    return store().search_products(query, limit, priced_only)


@mcp.tool()
def search_assemblies(query: str, limit: int = 10) -> list[dict]:
    """Search the 1,461 EEWin assemblies (e.g. 'prise duplex 15A', 'TMEC 3/4').
    Each result includes material cost for 1 unit, labor hours and its warnings (component without price, labor
    time or unit conversion, missing component): show them, the material cost leaves those components out."""
    return store().search_assemblies(query, limit)


@mcp.tool()
def get_item(code: str) -> dict:
    """Details for a product code, manufacturer number or assembly code (assemblies list their components).
    A manufacturer number carried by several products adds `warning` and `matches` (their codes): ask which one."""
    s = store()
    a = s.assembly(code)
    if a:
        return {"type": "assembly", "code": a.code, "description": a.description, "unit": a.unit,
                "labor_hours": a.labor_hours, "section_hours": a.section_hours,
                "components": [vars(c) | {"description": (p.description if (p := s.product(c.product_code)) else "?")}
                               for c in a.components]}
    p = s.product(code)
    if p is None:
        return {"error": f"unknown code {code}"}
    item = {"type": "product"} | vars(p)
    if p.code != code and len(matches := s.mfr_matches(code)) > 1:
        item |= {"warning": f"mfr no. {code} matches {len(matches)} products, used {p.code}", "matches": matches}
    return item


@mcp.tool()
def labor_rates() -> list[dict]:
    """Hourly labor rates from EEWin (default estimate rate: electrician 72 $/h)."""
    return store().labor_rates()


@mcp.tool()
def price_estimate(lines: list[dict], labor_rate: float = DEFAULT_RATE, material_markup_pct: float = 0.0,
                   labor_markup_pct: float = 0.0) -> dict:
    """Price a list of lines deterministically.
    lines: [{"code": str, "qty": number, "unit": optional str, "sections": optional number, "note": optional str}]
    code = product code, manufacturer number or assembly code. Returns per-line material, hours, labor cost,
    warnings, and totals (material_cost, labor_hours, labor_cost, cost_total, sell_total).
    Show the user every entry of the top-level `warnings`: INVALID LINE and UNKNOWN CODE lines are priced 0 and
    left out of the totals; QTY 0, NO PRICE, NO LABOR TIME, a failed unit conversion and an ambiguous
    manufacturer number ("mfr no. X matches N products, used Y") each make the total incomplete or uncertain."""
    return store().estimate(lines, labor_rate, material_markup_pct, labor_markup_pct)


@mcp.tool()
def export_estimate_xlsx(title: str, lines: list[dict], labor_rate: float = DEFAULT_RATE,
                         material_markup_pct: float = 0.0, labor_markup_pct: float = 0.0) -> dict:
    """Price the lines (same input as price_estimate) and save an Excel quote in the project's out/ folder.
    unpriced_lines names every line left out of the totals (invalid line or unknown code): show them to the user."""
    est = store().estimate(lines, labor_rate, material_markup_pct, labor_markup_pct)
    path = write_quote(est, title)
    left_out = {r["line"] for r in est["lines"] if {"INVALID LINE", "UNKNOWN CODE"} & set(r["warnings"])}
    unpriced = [w for w in est["warnings"] if int(w.split(":")[0].split()[1]) in left_out]
    return {"file": str(path), "totals": est["totals"], "warnings": len(est["warnings"]), "unpriced_lines": unpriced}


def main():
    mcp.run("stdio")


if __name__ == "__main__":
    main()
