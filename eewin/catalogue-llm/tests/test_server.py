"""MCP tool functions on the built data/dre.sqlite (skipped if not built)."""
import pytest

from openpyxl import load_workbook

from dre_estimation import server
from dre_estimation.store import DB
from dre_estimation.xlsx import write_quote

pytestmark = pytest.mark.skipif(not DB.exists(), reason="run scripts/build_db.py first")


@pytest.fixture
def no_file(monkeypatch, tmp_path):
    monkeypatch.setattr(server, "write_quote", lambda est, title: tmp_path / f"{title}.xlsx")


def test_export_names_the_lines_left_out_of_the_totals(no_file):
    res = server.export_estimate_xlsx("t", [{"code": "LQE012185", "qty": 40}, {"code": "LQE012185", "qty": "12,5"},
                                            {"code": "NOPE", "qty": 1}])
    assert res["unpriced_lines"] == ["line 2: invalid line (could not convert string to float: '12,5')",
                                     "line 3: unknown code NOPE"]
    assert res["warnings"] >= 2 and res["totals"]["material_cost"] > 0


def test_export_of_a_clean_quote_has_no_unpriced_lines(no_file):
    res = server.export_estimate_xlsx("t", [{"code": "LQE012185", "qty": 40}])
    assert res["unpriced_lines"] == []


def test_search_tools_honour_limit():
    assert len(server.search_products("prise", 3)) == 3
    assert len(server.search_products("prise")) == 10
    assert len(server.search_assemblies("prise", 2)) == 2


def test_get_item_reports_an_ambiguous_mfr_no():
    s = server.store()
    r = s.con.execute("SELECT mfr_no FROM products WHERE mfr_no <> '' GROUP BY mfr_no HAVING count(*) > 1 "
                      "ORDER BY (mfr_no = 'HUB01304029') DESC, mfr_no LIMIT 1").fetchone()
    if r is None:
        pytest.skip("no manufacturer number is shared by several products")
    codes = [c[0] for c in s.con.execute("SELECT code FROM products WHERE mfr_no = ? ORDER BY code", (r[0],))]
    item = server.get_item(r[0])
    assert item["type"] == "product" and item["code"] in codes and item["matches"] == codes
    assert item["warning"] == f"mfr no. {r[0]} matches {len(codes)} products, used {item['code']}"
    for unambiguous in (server.get_item(item["code"]), server.get_item("APPTW75DC"), server.get_item("NOPE")):
        assert "warning" not in unambiguous and "matches" not in unambiguous


def test_tool_texts_tell_the_client_to_show_every_warning():
    for word in ("INVALID LINE", "UNKNOWN CODE", "QTY 0", "mfr no.", "unit conversion", "unpriced_lines"):
        assert word in server.INSTRUCTIONS, word
    for word in ("INVALID LINE", "UNKNOWN CODE", "QTY 0", "mfr no.", "unit conversion"):
        assert word in (server.price_estimate.__doc__ or ""), word
    doc = server.search_assemblies.__doc__ or ""
    assert "warnings for missing component prices" not in doc and "labor" in doc.split("warnings")[1]


@pytest.mark.parametrize("evil", ["=1+1", "+1+1", "-1+1", "@SUM(1)", '=HYPERLINK("http://x","y")'])
def test_export_writes_user_text_as_text_not_formulas(tmp_path, evil):
    est = server.store().estimate([{"code": "LQE012185", "qty": 40, "note": evil, "unit": evil},
                                   {"code": evil, "qty": 1, "note": evil}, {"code": evil, "qty": "x", "note": evil},
                                   {"code": "ENS110F48C2159103C10", "qty": 1}])
    est["lines"][1]["warnings"].insert(0, evil)
    est["lines"][3]["components"][0] |= {"description": evil, "warnings": [evil]}
    est["warnings"].append(evil)
    wb = load_workbook(write_quote(est, evil, tmp_path / "q.xlsx"))
    main, det, warn = wb["Estimation"], wb["Détail assemblages"], wb["Avertissements"]
    text = [main["A1"], main["F5"], main["M5"], main["B6"], main["L6"], main["M6"], main["B7"], main["M7"],
            det["D2"], det["I2"], warn.cell(warn.max_row, 1)]
    assert [(c.coordinate, c.data_type) for c in text] == [(c.coordinate, "s") for c in text]
    assert main["A1"].value == main["B6"].value == main["M5"].value == main["B7"].value == evil
    assert main["L6"].value == f"{evil}; UNKNOWN CODE" and det["D2"].value == det["I2"].value == evil
    assert warn.cell(warn.max_row, 1).value == evil
    for sheet in wb:
        formulas = [c.coordinate for row in sheet.iter_rows() for c in row if c.data_type == "f"]
        assert formulas == (["K9", "K10", "K12", "K13", "K16"] if sheet is main else [])
