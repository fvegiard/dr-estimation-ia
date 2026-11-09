"""Integration tests on the built data/dre.sqlite (skipped if not built)."""
import pytest

from dre_estimation.store import DB, Store

pytestmark = pytest.mark.skipif(not DB.exists(), reason="run scripts/build_db.py first")


@pytest.fixture(scope="module")
def s():
    return Store()


def test_search_finds_common_items(s):
    assert s.search_products("boite 4 po carre", 3)[0]["description"].lower().startswith("square box")
    assert "BREAKER" in s.search_products("disjoncteur 15A 1P", 1)[0]["description"]
    assert "ARMORED" in s.search_products("cable armé 14/2 alu", 1)[0]["description"]


def test_default_quantity_unit_is_each(s):
    est = s.estimate([{"code": "LQE012185", "qty": 40}])  # priced per 100
    ln = est["lines"][0]
    assert ln["unit"] == "U" and ln["material"] < 100


def test_known_assembly_total(s):
    est = s.estimate([{"code": "ENS110F48C2159103C10", "qty": 1}])
    assert est["totals"]["labor_hours"] == pytest.approx(1.4)
    assert est["lines"][0]["material"] > 0
    assert est["warnings"]  # receptacle without price must be reported


def test_unknown_code_is_reported(s):
    est = s.estimate([{"code": "NOPE", "qty": 1}])
    assert est["totals"]["cost_total"] == 0 and "unknown code" in est["warnings"][0]


def test_markups(s):
    base = s.estimate([{"code": "LQE012185", "qty": 100}])["totals"]
    up = s.estimate([{"code": "LQE012185", "qty": 100}], material_markup_pct=10, labor_markup_pct=20)["totals"]
    assert up["sell_total"] == pytest.approx(base["material_cost"] * 1.1 + base["labor_cost"] * 1.2, abs=0.02)


@pytest.mark.parametrize("search", ["search_products", "search_assemblies"])
def test_search_limit_is_clamped(s, search):
    assert len(getattr(s, search)("prise", -1)) == 1  # negative = unlimited in SQLite
    assert len(getattr(s, search)("prise", 0)) == 1
    assert len(getattr(s, search)("prise", 1000)) == 50
    assert len(getattr(s, search)("prise", 3)) == 3


@pytest.mark.parametrize("search", ["search_products", "search_assemblies"])
def test_search_limit_is_coerced(s, search):
    assert len(getattr(s, search)("prise", "5")) == 5
    assert len(getattr(s, search)("prise", 3.9)) == 3
    for bad in ("abc", None, [5], float("nan"), float("inf")):
        assert len(getattr(s, search)("prise", bad)) == 10  # default


def ambiguous_mfr_no(s) -> tuple[str, int]:
    """A manufacturer number carried by several products, and how many (read from the catalog)."""
    r = s.con.execute("SELECT mfr_no, count(*) FROM products WHERE mfr_no <> '' GROUP BY mfr_no "
                      "HAVING count(*) > 1 ORDER BY (mfr_no = 'HUB01304029') DESC, mfr_no LIMIT 1").fetchone()
    if r is None:
        pytest.skip("no manufacturer number is shared by several products")
    return r[0], r[1]


def test_ambiguous_mfr_no_is_reported(s):
    mfr, n = ambiguous_mfr_no(s)
    est = s.estimate([{"code": mfr, "qty": 2}])
    ln = est["lines"][0]
    used = s.product(mfr).code
    by_code = s.estimate([{"code": used, "qty": 2}])["lines"][0]
    assert n > 1 and ln["code"] == used != mfr and ln["material"] == by_code["material"]
    assert f"mfr no. {mfr} matches {n} products, used {used}" in ln["warnings"]
    assert f"line 1 ({used}): mfr no. {mfr} matches {n} products, used {used}" in est["warnings"]


def test_unique_mfr_no_and_product_code_are_not_reported(s):
    by_mfr = s.estimate([{"code": "APPTW75DC", "qty": 40}])  # only LQE012185 carries this mfr no.
    by_code = s.estimate([{"code": "LQE012185", "qty": 40}])
    assert by_mfr["lines"][0]["code"] == "LQE012185" and by_mfr["totals"] == by_code["totals"]
    by_code2 = s.estimate([{"code": "NQE080928", "qty": 2}])  # its mfr no. is ambiguous, the code is not
    for est in (by_mfr, by_code, by_code2):
        assert not [w for w in est["warnings"] if "mfr no." in w]


@pytest.mark.parametrize("bad", ["LQE012185", None, 7, ["LQE012185", 40], {"code": "LQE012185", "qty": "abc"},
                                 {"code": "LQE012185", "qty": [1]}, {"code": "LQE012185", "qty": float("nan")},
                                 {"code": "LQE012185", "qty": "inf"}, {"code": "LQE012185", "qty": 10 ** 400},
                                 {"code": "LQE012185", "qty": 1, "sections": "x"},
                                 {"code": "LQE012185", "qty": 1, "sections": float("-inf")},
                                 {"code": "LQE012185", "qty": 1e27}, {"code": "LQE012185", "qty": -1e27},
                                 {"code": "LQE012185", "qty": 1, "sections": 1e27},
                                 {"code": "LQE012185", "qty": 1, "unit": 5},
                                 {"code": "LQE012185", "qty": 1, "unit": ["U"]}])
def test_invalid_line_does_not_break_the_estimate(s, bad):
    good = {"code": "LQE012185", "qty": 40}
    est = s.estimate([good, bad, good])
    one = s.estimate([good])
    assert [r["line"] for r in est["lines"]] == [1, 2, 3]
    row = est["lines"][1]
    assert row["warnings"] == ["INVALID LINE"] and row["material"] == 0 and row["hours"] == 0 and row["total"] == 0
    assert est["lines"][0] == one["lines"][0] and est["lines"][2] == one["lines"][0] | {"line": 3}
    assert est["totals"]["material_cost"] == pytest.approx(2 * one["totals"]["material_cost"])
    assert [w for w in est["warnings"] if w.startswith("line 2: invalid line")]


def test_invalid_row_has_the_shape_of_a_valid_row(s):
    est = s.estimate([{"code": "LQE012185", "qty": 40, "note": "ok"}, {"code": "LQE012185", "qty": "x", "note": "keep"},
                      {"code": "LQE012185", "qty": 1, "sections": "x", "note": "me too"}, "LQE012185"])
    good, bad, bad2, not_a_dict = est["lines"]
    for row in (bad, bad2, not_a_dict):
        assert list(row) == list(good)
        assert {k: type(v) for k, v in row.items()} == {k: type(v) for k, v in good.items()}
        assert row["qty"] == 0.0 and row["sections"] == 0.0 and row["components"] == []
    assert (bad["code"], bad["note"], bad2["note"], not_a_dict["note"]) == ("LQE012185", "keep", "me too", "")


def test_largest_accepted_quantity_can_be_rounded(s):
    big = s.estimate([{"code": "LQE012185", "qty": 1e9},
                      {"code": "ENS110F48C2159103C10", "qty": -1e9, "sections": 1e9}])
    assert not [w for w in big["warnings"] if "invalid" in w] and big["lines"][0]["material"] > 0


def test_zero_quantity_is_reported(s):
    est = s.estimate([{"code": "LQE012185", "qty": 0}, {"code": "LQE012185"},
                      {"code": "ENS110F48C2159103C10", "qty": 0}])
    assert all("QTY 0" in r["warnings"] for r in est["lines"])
    assert "line 1 (LQE012185): QTY 0" in est["warnings"] and est["totals"]["cost_total"] == 0
    assert "line 3 (ENS110F48C2159103C10): QTY 0" in est["warnings"]


def test_numeric_strings_and_negative_quantities_stay_valid(s):
    pos = s.estimate([{"code": "LQE012185", "qty": 40}])
    neg = s.estimate([{"code": "LQE012185", "qty": -40}])  # credit
    txt = s.estimate([{"code": "LQE012185", "qty": "40", "sections": "0"}])
    assert neg["lines"][0]["material"] == -pos["lines"][0]["material"] < 0
    assert neg["lines"][0]["warnings"] == pos["lines"][0]["warnings"] == txt["lines"][0]["warnings"]
    assert txt["totals"] == pos["totals"]
    assert not [w for w in pos["warnings"] + neg["warnings"] if "QTY 0" in w or "invalid" in w]
