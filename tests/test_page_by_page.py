"""Acceptance tests for the page-by-page take-off (Granby / S-1294 render_sheet format)."""
import csv
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
Image.MAX_IMAGE_PIXELS = None

PROJECT = ROOT / "projects" / "S-1849-CHUM.json"
# FGG1 tags printed on each sheet (normal, emergency, no circuit label), counted on the source PDFs.
EXPECTED_FGG1 = {
    "1-B1-EL-50-01-2-0": (7, 8, 0), "1-B1-EL-50-RC-0-0": (14, 17, 1), "1-D-EL-50-P1-2-0": (34, 30, 0),
    "1-D-EL-50-P2-2-0": (37, 31, 0), "1-D-EL-50-P2-3-0": (23, 14, 0), "1-D-EL-50-P3-2-0": (35, 32, 0),
    "1-D-EL-50-P3-3-0": (23, 14, 0), "1-D-EL-50-P4-2-0": (37, 32, 0), "1-D-EL-50-P4-3-0": (23, 14, 0),
    "1-D-EL-50-P5-2-0": (35, 31, 0), "1-D-EL-50-P5-3-0": (16, 11, 0),
}
BORDEREAU_HEADER = ["Repère / source", "Matériel", "Désignation", "Qté", "Portée", "Modèle", "Prescription / réserve",
                    "Parent", "X pixels source", "Y pixels source", "Pastille", "Circuits", "Ampères", "Pôles",
                    "Protection source"]


@pytest.fixture(scope="session")
def project():
    cfg = json.loads(PROJECT.read_text(encoding="utf-8"))
    if not all(Path(s["pdf"]).exists() for s in cfg["sheets"]):
        pytest.skip("source plans not on this machine")
    return cfg


@pytest.fixture(scope="session")
def built(project, tmp_path_factory):
    import tag_records, render_sheet
    out = tmp_path_factory.mktemp("out")
    results = {}
    for sheet in project["sheets"]:
        data = tag_records.build(project, sheet)
        results[sheet["sheet"]] = (data, render_sheet.render(data, project, out))
    return out, results


def test_project_lists_the_eleven_sheets(project):
    assert sorted(s["sheet"] for s in project["sheets"]) == sorted(EXPECTED_FGG1)


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_fgg1_counts_match_the_plan(built, sheet):
    data, _ = built[1][sheet]
    fgg1 = [r for r in data["records"] if r["tag"] == "FGG1"]
    normal = sum(r["circuits"].startswith("N") for r in fgg1)
    emergency = sum(r["circuits"].startswith("S") for r in fgg1)
    assert (normal, emergency, len(fgg1) - normal - emergency) == EXPECTED_FGG1[sheet]


def test_every_printed_tag_family_is_marked(built):
    data, _ = built[1]["1-D-EL-50-P4-2-0"]
    by_tag = {}
    for r in data["records"]:
        by_tag[r["tag"]] = by_tag.get(r["tag"], 0) + 1
    assert by_tag == {"FGG1": 69, "FS": 10, "X2": 10, "FR1": 2}


def test_record_without_circuit_is_a_reserve(built):
    data, _ = built[1]["1-B1-EL-50-RC-0-0"]
    loose = [r for r in data["records"] if not r["circuits"]]
    assert loose and all(r["reserve"] for r in loose)


def test_fgg1_scope_and_model(built):
    for sheet, (data, _) in built[1].items():
        expected = "SWZCSH" if ("P4" in sheet or "P5" in sheet) else "SSL"
        for r in data["records"]:
            if r["tag"] == "FGG1":
                assert r["scope"] == "REMPLACER" and r["model"].endswith(expected)
            else:
                assert r["scope"] in ("CONSERVER", "A PRECISER")


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_plan_is_untouched_and_legend_is_appended_below(built, sheet):
    data, res = built[1][sheet]
    final = Image.open(res["jpg"])
    base_w, base_h = res["base_size"]
    assert final.width == base_w == 6854 and final.height > base_h
    # the legend strip starts under the plan: last plan row is still drawing, never white box over it
    assert res["legend_top"] == base_h
    # no pastille is drawn inside the legend strip
    assert all(r["y"] * base_w / 1920 < base_h for r in data["records"])


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_legend_counts_equal_pastilles_and_bordereau(built, sheet):
    data, res = built[1][sheet]
    marked = [r for r in data["records"] if r.get("mark", True)]
    assert sum(res["legend"].values()) == len(marked)
    assert res["header"].startswith(f"{len(marked)} pastilles / {len(res['legend'])} familles / RES ")
    rows = list(csv.reader(open(res["csv"], encoding="utf-8-sig", newline="")))
    assert rows[0] == BORDEREAU_HEADER
    assert len(rows) - 1 == len(data["records"])
    assert sum(int(r[3]) for r in rows[1:]) == len(marked)
    assert len({r[0] for r in rows[1:]}) == len(rows) - 1


def test_title_follows_the_reference_format(built):
    _, res = built[1]["1-D-EL-50-P4-2-0"]
    assert res["title"] == "RELEVÉ 1-D-EL-50-P4-2-0 — NIVEAU P4 NE - PLAN D'ÉCLAIRAGE"


def test_family_colours_are_distinct(built):
    _, res = built[1]["1-B1-EL-50-01-2-0"]
    assert len(set(res["palette"].values())) == len(res["palette"])


def test_proof_boards_cover_every_pastille(built):
    data, res = built[1]["1-D-EL-50-P4-2-0"]
    marked = sum(r.get("mark", True) for r in data["records"])
    assert len(res["boards"]) == -(-marked // 30) and all(Path(b).exists() for b in res["boards"])


def _word_boxes(pdf):
    import pymupdf
    import tag_records
    page = pymupdf.open(pdf)[0]
    k = 1920 / page.rect.width
    return [tuple(v * k for v in tag_records._view_rect(page, w[:4])) for w in page.get_text("words")]


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_no_pastille_sits_on_a_text(built, sheet):
    data, _ = built[1][sheet]
    boxes = _word_boxes(data["pdf"])
    on_text = [r["id"] for r in data["records"]
               if any(x0 <= r["x"] <= x1 and y0 <= r["y"] <= y1 for x0, y0, x1, y1 in boxes)]
    assert on_text == []


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_reserve_only_when_identification_is_uncertain(built, sheet):
    data, res = built[1][sheet]
    for r in data["records"]:
        assert bool(r["reserve"]) == (not r["circuits"] or not r["on_symbol"]), r["id"]


def test_replaced_families_lead_the_legend(built):
    _, res = built[1]["1-B1-EL-50-01-2-0"]
    names = list(res["legend"])
    assert all(n.startswith("FGG1") for n in names[:2]) and not names[2].startswith("FGG1")


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_fgg1_pastille_stays_on_its_own_fixture(built, sheet):
    # a paired FGG1 fixture lies between its tag and its circuit label: the pastille must stay there
    data, _ = built[1][sheet]
    paired = [r for r in data["records"] if r["tag"] == "FGG1" and r["circuits"]]
    far = [r["id"] for r in paired if ((r["x"] - r["mid_x"]) ** 2 + (r["y"] - r["mid_y"]) ** 2) ** .5 > 6]
    assert len(far) <= max(1, len(paired) // 30), far


@pytest.mark.parametrize("sheet", sorted(EXPECTED_FGG1))
def test_every_located_pastille_sits_on_a_drawn_symbol(built, sheet):
    import pymupdf
    import tag_records
    data, _ = built[1][sheet]
    page = pymupdf.open(data["pdf"])[0]
    index = tag_records.SymbolIndex(page)
    k = page.rect.width / 1920
    off = [r["id"] for r in data["records"] if r["on_symbol"] and not index.ink_near(r["x"] * k, r["y"] * k)]
    assert off == []


def test_symbol_beside_its_tag_is_flagged_not_guessed(built):
    # seen on the proof board: these two exit signs are drawn beside their tag, not between tag and circuit
    data, _ = built[1]["1-D-EL-50-P5-3-0"]
    by_id = {r["id"]: r for r in data["records"]}
    for rid in ("1-D-EL-50-P5-3-0-0030", "1-D-EL-50-P5-3-0-0033"):
        assert by_id[rid]["tag"] == "X2" and not by_id[rid]["on_symbol"] and by_id[rid]["reserve"]
