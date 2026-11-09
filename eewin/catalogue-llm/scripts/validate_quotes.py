"""Recompute past EEWin quotes with the engine and compare to EEWin's own totals.

Uses each quote's saved product/assembly snapshot (SOUPRO/SOUENS/SOUENSCO), so the
comparison tests the arithmetic (units, assemblies, block multipliers), not price freshness.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dre_estimation.engine import price_assembly, price_product  # noqa: E402
from dre_estimation.raw import assembly_from, component_from, load_units, num, product_from, rows  # noqa: E402


def main(limit_year: int = 2015, show: int = 15):
    units = load_units()
    quotes = {r["SOU_ID"]: r for r in rows("quotes") if r["TOTCALCULE"] == "True" and num(r["MATCOUTREL"]) > 0
              and r["DATEDOC"].count("/") == 2 and int(r["DATEDOC"].split("/")[2][:4]) >= limit_year}
    prods = defaultdict(dict)
    for r in rows("quote_products"):
        if r["SOU_ID"] in quotes:
            prods[r["SOU_ID"]][r["PRO_ID"]] = product_from(r)
    comps = defaultdict(list)
    for r in sorted(rows("quote_assembly_components"), key=lambda r: r["ORDRE"]):
        if r["SOU_ID"] in quotes:
            comps[(r["SOU_ID"], r["ENS_ID"])].append(component_from(r))
    asms = defaultdict(dict)
    for r in rows("quote_assemblies"):
        if r["SOU_ID"] in quotes:
            asms[r["SOU_ID"]][r["ENS_ID"]] = assembly_from(r, comps[(r["SOU_ID"], r["ENS_ID"])])
    mult = {(r["SOU_ID"], r["BLO_ID"]): num(r["MULT"]) or 1.0 for r in rows("quote_blocks")}
    mat = defaultdict(float); hrs = defaultdict(float); miss = defaultdict(int)
    for r in rows("quote_lines"):
        sid = r["SOU_ID"]
        if sid not in quotes or r["TYPERELEVE"] != "P":
            continue
        m = mult.get((sid, r["BLO_ID"]), 1.0)
        qty = num(r["QTE"])
        if r["TYPEITEM"] in ("P", "N"):
            p = prods[sid].get(r["ITEM_ID"])
            if p is None:
                miss[sid] += 1; continue
            ln = price_product(p, qty, r["QTEUM"], units, m)
        elif r["TYPEITEM"] == "A":
            a = asms[sid].get(r["ITEM_ID"])
            if a is None:
                miss[sid] += 1; continue
            ln = price_assembly(a, qty, r["QTEUM"], num(r["SECTION"]), prods[sid], units, m)
        else:
            continue
        mat[sid] += ln.material; hrs[sid] += ln.hours
    res = []
    for sid, q in quotes.items():
        em, eh = num(q["MATCOUTREL"]), num(q["SERHRESCAL"])
        res.append((sid, q["NODOC"], q["DESCDOC"][:32], em, mat[sid], eh, hrs[sid], miss[sid]))
    ok_m = sum(1 for r in res if abs(r[4] - r[3]) <= max(1.0, 0.005 * r[3]))
    ok_h = sum(1 for r in res if abs(r[6] - r[5]) <= max(0.5, 0.02 * r[5]))
    print(f"quotes checked (>= {limit_year}): {len(res)}")
    print(f"material within 0.5%: {ok_m} ({ok_m / len(res):.1%})")
    print(f"hours within 2% (EEWin hours are often rounded/overridden): {ok_h} ({ok_h / len(res):.1%})")
    bad = sorted(res, key=lambda r: -abs(r[4] - r[3]) / max(r[3], 1))[:show]
    print("\nworst material mismatches:")
    for r in bad:
        print(f"  {r[1]:>10} {r[2]:<32} eewin={r[3]:>11.2f} ours={r[4]:>11.2f}  h eewin={r[5]:>7.1f} ours={r[6]:>7.1f} missing={r[7]}")
    return res


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))
