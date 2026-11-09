"""Build data/dre.sqlite from the raw EEWin CSVs (data/raw).

Adds: net price, usage counts from past quotes, labor-time fallback from past quotes,
and a normalized search text for fuzzy FR/EN matching.
"""
from __future__ import annotations

import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dre_estimation.engine import UnitError, norm_unit  # noqa: E402
from dre_estimation.raw import load_units, net_price, num, rows  # noqa: E402
from dre_estimation.search import compact, words  # noqa: E402

DB = ROOT / "data" / "dre.sqlite"

SCHEMA = """
CREATE TABLE products(code TEXT PRIMARY KEY, mfr_no TEXT, supplier TEXT, category TEXT, category_desc TEXT,
  description TEXT, price REAL, price_unit TEXT, price_date TEXT, labor_hours REAL, labor_unit TEXT,
  labor_source TEXT, times_quoted INTEGER, last_quoted TEXT, preferred_orig INTEGER, search_text TEXT,
  search_words TEXT);
CREATE TABLE assemblies(code TEXT PRIMARY KEY, description TEXT, unit TEXT, labor_hours REAL, labor_unit TEXT,
  section_hours REAL, times_quoted INTEGER, search_text TEXT, search_words TEXT);
CREATE TABLE assembly_components(assembly_code TEXT, ord TEXT, product_code TEXT, qty REAL, qty_unit TEXT,
  kind TEXT, div REAL, div_unit TEXT);
CREATE INDEX ix_comp ON assembly_components(assembly_code);
CREATE TABLE unit_ratios(unit_from TEXT, unit_to TEXT, ratio REAL, PRIMARY KEY(unit_from, unit_to));
CREATE TABLE units(code TEXT PRIMARY KEY, description_en TEXT, description_fr TEXT);
CREATE TABLE labor_rates(code TEXT PRIMARY KEY, description TEXT, rate REAL);
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
"""


def main():
    units = load_units()
    cats = {r["CODECAT"]: r["DESC"].strip() for r in rows("categories")}
    quote_date = {r["SOU_ID"]: r["DATEDOC"] for r in rows("quotes")}

    usage = defaultdict(int); last = {}; hist_labor = defaultdict(list)
    for r in rows("quote_products"):
        code = r["PRO_ID"]
        usage[code] += 1
        d = quote_date.get(r["SOU_ID"], "")
        if d and (code not in last or _dkey(d) > _dkey(last[code])):
            last[code] = d
        if num(r["TEMPUNI"]) > 0:
            hist_labor[code].append((num(r["TEMPUNI"]), norm_unit(r["TEMPUM"])))
    asm_usage = defaultdict(int)
    for r in rows("quote_assemblies"):
        asm_usage[r["ENS_ORG_ID"] or r["ENS_ID"]] += 1

    prods = list(rows("products"))
    by_mfr = defaultdict(list)
    for r in prods:
        if r["CLEMANU"].strip() and num(r["TEMPUNI"]) > 0:
            by_mfr[r["CLEMANU"].strip().upper()].append((num(r["TEMPUNI"]), norm_unit(r["TEMPUM"])))

    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    out = []
    for r in prods:
        code, unit = r["PRO_ID"], norm_unit(r["COUUM"])
        lh, lu, src = num(r["TEMPUNI"]), norm_unit(r["TEMPUM"]), "catalog"
        if lh <= 0:
            lh, lu, src = _fallback(hist_labor.get(code), units, lu, "past quotes")
        if lh <= 0 and r["CLEMANU"].strip():
            lh, lu, src = _fallback(by_mfr.get(r["CLEMANU"].strip().upper()), units, lu, "same mfr no.")
        if lh <= 0:
            src = "none"
        cat = r["CODECAT"]
        text = " ".join([r["DESC"], r["CLEMANU"], code, cats.get(cat, "")])
        out.append((code, r["CLEMANU"].strip(), r["CODEFOUR"], cat, cats.get(cat, ""), r["DESC"].strip(),
                    round(net_price(r), 4), unit, _iso(r["DATECOUT"]), lh, lu, src, usage.get(code, 0),
                    _iso(last.get(code, "")), int(r["PREFERED_ORIG"] == "1"), compact(text), words(text)))
    con.executemany("INSERT INTO products VALUES(" + ",".join("?" * 17) + ")", out)

    con.executemany("INSERT INTO assemblies VALUES(?,?,?,?,?,?,?,?,?)", [
        (r["ENS_ID"], r["DESC"].strip(), norm_unit(r["COUUM"]), num(r["TEMPUNI"]), norm_unit(r["TEMPUM"]),
         num(r["TEMPSEC"]), asm_usage.get(r["ENS_ID"], 0), compact(r["DESC"] + " " + r["ENS_ID"]),
         words(r["DESC"] + " " + r["ENS_ID"]))
        for r in rows("assemblies")])
    con.executemany("INSERT INTO assembly_components VALUES(?,?,?,?,?,?,?,?)", [
        (r["ENS_ID"], r["ORDRE"], r["PRO_ID"], num(r["QTE"]), norm_unit(r["QTEUM"]), (r["TYPRATIO"] or "L").upper(),
         num(r["DIV"]) or 1.0, norm_unit(r["DIVUM"])) for r in rows("assembly_components")])

    codes = sorted(set(units.base) | {u for pair in units.direct for u in pair})
    ratios = []
    for a in codes:
        for b in codes:
            try:
                ratios.append((a, b, units.ratio(a, b)))
            except UnitError:
                pass
    con.executemany("INSERT INTO unit_ratios VALUES(?,?,?)", ratios)
    con.executemany("INSERT INTO units VALUES(?,?,?)", [
        (norm_unit(r["CodeEN"]), r["DescriptionEN"], r["DescriptionFR"]) for r in rows("units")])
    con.executemany("INSERT INTO labor_rates VALUES(?,?,?)", [
        (r["ORDRE"], r["DESCTAUX"].strip(), num(r["COUTUNI"])) for r in rows("labor_rates")
        if r["DESCTAUX"].strip() and num(r["COUTUNI"]) > 0])
    newest = max((p[8] for p in out if p[6] > 0), default="")
    con.executemany("INSERT INTO meta VALUES(?,?)", [("prices_as_of", newest), ("source", "EEWin2_zip")])
    con.commit()
    src_count = defaultdict(int)
    for p in out:
        src_count[p[11]] += 1
    print(f"products {len(out)}  priced {sum(1 for p in out if p[6] > 0)}  labor sources {dict(src_count)}")
    print(f"assemblies {con.execute('select count(*) from assemblies').fetchone()[0]}  unit ratios {len(ratios)}  -> {DB}")
    con.close()


def _fallback(samples, units, target_unit, label):
    """Median past labor time, converted to one unit."""
    if not samples:
        return 0.0, target_unit, "none"
    unit = samples[0][1]
    vals = []
    for h, u in samples:
        try:
            vals.append(h * units.ratio(unit, u))  # hours per `u` x (`u` per `unit`) = hours per `unit`
        except UnitError:
            pass
    return (round(statistics.median(vals), 4), unit, label) if vals else (0.0, target_unit, "none")


def _dkey(d: str):
    try:
        m, dd, rest = d.split("/")
        return (int(rest[:4]), int(m), int(dd))
    except ValueError:
        return (0, 0, 0)


def _iso(d: str) -> str:
    y, m, dd = _dkey(d) if d else (0, 0, 0)
    return f"{y:04d}-{m:02d}-{dd:02d}" if y else ""


if __name__ == "__main__":
    main()
