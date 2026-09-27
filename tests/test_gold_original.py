"""src.estimer.gold_original — synthetic index + PDFs only (no client data).

Checks the pure parts of the loader: which PDFs enter the evaluation, page
order and sheet naming of the concatenated input, the duplicate rule for a
page imported twice, and the direct raster -> page conversion of marks
(including a rotated page) through a synthetic Dupuis .qpl.
"""
from __future__ import annotations

import json

import numpy as np
import pymupdf
import pytest

from src.estimer import gold_original as GO
from src.estimer.pages import WORK_WIDTH


def _index(dossier="S-0001"):
    pages = [
        {"pdf": "A.pdf", "page": 1, "width_pt": 1000.0, "height_pt": 700.0, "rotation": 0, "sheet": "E100",
         "legend_page": True, "scale": "AUCUNE"},
        {"pdf": "A.pdf", "page": 2, "width_pt": 1000.0, "height_pt": 700.0, "rotation": 90, "sheet": "E201",
         "legend_page": False, "scale": "1/8\" = 1'-0\""},
        {"pdf": "B.pdf", "page": 1, "width_pt": 1000.0, "height_pt": 700.0, "rotation": 0, "sheet": "E201",
         "legend_page": False, "scale": "1 : 100"},
        {"pdf": "liste.pdf", "page": 1, "width_pt": 600.0, "height_pt": 800.0, "rotation": 0, "sheet": None,
         "legend_page": False, "scale": None},
    ]
    plans = [
        {"name": "A - 1", "file_name": "A - 1.png", "marks": 0, "lines": 0, "png_size": [2000, 1400],
         "pdf": "A.pdf", "page": 1, "sheet": "E100", "method": "name", "check": "ok"},
        {"name": "A - 2", "file_name": "A - 2.png", "marks": 3, "lines": 1, "png_size": [2000, 1400],
         "pdf": "A.pdf", "page": 2, "sheet": "E201", "method": "name", "check": "ok"},
        {"name": "A - 2 (2)", "file_name": "A - 2 (2).png", "marks": 2, "lines": 0, "png_size": [2000, 1400],
         "pdf": "A.pdf", "page": 2, "sheet": "E201", "method": "name", "check": "ok"},
        {"name": "B - 1", "file_name": "B - 1.png", "marks": 1, "lines": 0, "png_size": [4000, 2800],
         "pdf": "B.pdf", "page": 1, "sheet": "E201", "method": "name", "check": "ok"},
    ]
    return {"dossier": dossier, "reference_qpl": f"{dossier}/reference/{dossier}-Dupuis-PlanExpert.qpl",
            "reference_kind": "dupuis", "pdfs": ["A.pdf", "B.pdf", "liste.pdf"],
            "pdf_sha256": {"A.pdf": "a" * 64, "B.pdf": "b" * 64, "liste.pdf": "c" * 64},
            "pages": pages, "plans": plans, "unmatched": [], "notes": []}


def _qpl(path):
    def plan(name, counters):
        body = "".join(f'<Counter Name="{lab}" Shape="0" DefaultSize="20" Color="-65536">'
                       + "".join(f'<Element X="{x}" Y="{y}"/>' for x, y in pts) + "</Counter>"
                       for lab, pts in counters)
        return (f'<Plan Name="{name}" FileName="{name}.png"><Scale Value="0,125" Type="1"/>'
                f'<Layers><Layer Name="L">{body}</Layer></Layers></Plan>')
    plans = [
        plan("A - 1", []),
        # page 2: three marks; the copy "(2)" repeats two of them (duplicates) and adds nothing
        plan("A - 2", [("PRISE", [(200, 140), (1000, 700)]), ("LUMINAIRE", [(1800, 1260)])]),
        plan("A - 2 (2)", [("PRISE", [(203, 142), (1002, 698)])]),
        plan("B - 1", [("LUMINAIRE", [(2000, 1400)])]),
    ]
    path.write_text('<?xml version="1.0"?><Project><Plans>' + "".join(plans) + "</Plans></Project>",
                    encoding="utf-8")


def _pdfs(pdf_dir):
    pdf_dir.mkdir(parents=True)
    doc = pymupdf.open()
    doc.new_page(width=1000, height=700)
    p = doc.new_page(width=700, height=1000)
    p.set_rotation(90)
    doc.save(pdf_dir / "A.pdf"); doc.close()
    doc = pymupdf.open(); doc.new_page(width=1000, height=700); doc.save(pdf_dir / "B.pdf"); doc.close()
    doc = pymupdf.open(); doc.new_page(width=600, height=800); doc.save(pdf_dir / "liste.pdf"); doc.close()


def test_pages_and_sheets_of_the_evaluated_input():
    idx = _index()
    assert GO.pdfs_with_plans(idx) == ["A.pdf", "B.pdf"]          # liste.pdf holds no estimator plan
    rows = GO.page_table(idx)
    assert [(r["pdf"], r["page"]) for r in rows] == [("A.pdf", 1), ("A.pdf", 2), ("B.pdf", 1)]
    sheets = GO.sheet_table(idx)
    assert [s.display for s in sheets] == ["E100", "E201", "E201_2"]   # same sheet in original + addendum
    assert [s.kind for s in sheets] == ["legende", "plan", "plan"]
    assert sheets[1].scale_ratio == 96.0 and sheets[2].scale_ratio == 100.0 and sheets[0].scale_ratio is None
    assert sheets[1].page_width_px == WORK_WIDTH and sheets[1].page_height_px == pytest.approx(WORK_WIDTH * 0.7)


def test_dedupe_is_one_to_one_within_radius():
    first = np.array([(0.0, 0.0), (100.0, 0.0)])
    second = np.array([(2.0, 1.0), (3.0, 0.0), (300.0, 0.0)])
    dup = GO.dedupe(first, second, radius=10.0)
    assert dup.tolist() == [True, False, False]     # only one of the two near (0,0) can be its duplicate


def test_marks_placed_directly_from_the_estimator_raster(tmp_path):
    dossier = "S-0001"
    root = tmp_path / "data"
    d = root / dossier
    (d / "reference").mkdir(parents=True)
    _qpl(d / "reference" / f"{dossier}-Dupuis-PlanExpert.qpl")
    _pdfs(d / "entree" / "plans-originaux")
    idx = _index(dossier)
    index_path = tmp_path / "plan_index.json"
    index_path.write_text(json.dumps({dossier: idx}), encoding="utf-8")
    cache = tmp_path / "cache"
    g = GO.load(dossier, root, index_path, cache)
    # concatenated input: A p1, A p2, B p1 (liste.pdf excluded), cached with its stamp
    assert g.pdf == cache / f"{dossier}-plans-originaux.pdf"
    assert pymupdf.open(g.pdf).page_count == 3
    assert len(g.sheets) == 3
    # 3 marks on page 2 (+2 duplicates dropped), 1 on page 3
    by_page = {}
    for m in g.marks:
        by_page.setdefault(m.page, []).append(m)
    assert sorted(by_page) == [1, 2]
    assert len(by_page[1]) == 3 and len(by_page[2]) == 1
    k = WORK_WIDTH / 2000
    xs = sorted((m.x, m.y) for m in by_page[1])
    assert xs[0] == pytest.approx((200 * k, 140 * k))
    assert xs[-1] == pytest.approx((1800 * k, 1260 * k))
    assert by_page[2][0].x == pytest.approx(2000 * WORK_WIDTH / 4000)    # other raster size, other scale
    assert sum(g.unplaced.values()) == 0
    assert any("duplicates of a page imported twice dropped: 2" in n for n in g.notes)
    # his line on page 2: 1/8" = 1'-0" (Type 1, value 0.125 in/ft); paper 1000 pt wide -> raster 2000 px = 144 dpi
    assert g.lines == []          # no <Line> in the synthetic project
    assert g.ia_sheet_page == {}  # no other takeoff in the synthetic dossier
    # a second load reuses the cache (same stamp) and gives the same marks
    g2 = GO.load(dossier, root, index_path, cache)
    assert len(g2.marks) == len(g.marks)


def test_load_dispatch_rejects_unknown_source():
    from src.estimer import gold as G
    with pytest.raises(ValueError):
        G.load("S-0000", source="whatever")
