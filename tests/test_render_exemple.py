"""src.estimer.render — EXEMPLE-format relevé renderer, synthetic plans only (no client data).

A synthetic E-size plan (2594 x 1729 pt, like HR26-14) is drawn with pymupdf: rooms, device symbols, a
title-block frame on the right. The renderer must put one marker per symbol at the exact position, a
repère label, the RELEVE box in empty space (never on the title block) and the bordereau pages.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pymupdf
import pytest

from src.estimer.render import from_exemple as FX
from src.estimer.render import load_input, render
from src.estimer.render import style as S
from src.estimer.render.verify_exemple import verify, main as verify_main
from src.estimer.render.bordereau import rows_per_page, wrap
from src.estimer.render.data import Item, Sheet

from conftest import run_cli

W, H = 2594.0, 1729.0
TITLE_X = 2216.0
FIELDS = ["feuille", "repere", "source", "materiel", "designation", "qte", "portee", "modele", "prescription",
          "parent"]
FAMS = [("I01", "AVERTISSEUR DE FUMEE AUTONOME 120V MURAL", "A"), ("I02", "AVERTISSEUR INCENDIE KLAXON", "K"),
          ("I03", "DECLENCHEUR MANUEL ADRESSABLE", "F")]


def test_verify_rejects_missing_sheets_even_with_matching_page_count(tmp_path: Path):
    pdf = tmp_path / "pages.pdf"
    doc = pymupdf.open()
    doc.new_page()
    doc.save(pdf)
    doc.close()
    report = tmp_path / "report.json"
    report.write_text('{"sheets": []}', encoding="utf-8")
    gold = tmp_path / "gold"
    gold.mkdir()
    (gold / "provenance.json").write_text('{"sheets": [{"sheet": "E01", "exemple_page": 1}]}', encoding="utf-8")

    result = verify(pdf, report, pdf, gold)

    assert not result["ok"]
    assert not result["sheets_ok"]


@pytest.mark.parametrize("extra", [{"sheet": "EXTRA"}, {"sheet": "EXTRA", "plan_page": 1}])
def test_verify_reports_extra_sheet_and_still_checks_known_sheet(tmp_path: Path, extra):
    pdf = tmp_path / "pages.pdf"
    with pymupdf.open() as doc:
        doc.new_page()
        doc.save(pdf)
    report = tmp_path / "report.json"
    known = {"sheet": "E01", "plan_page": 1, "format": "materiel", "box": [0, 0, 10, 10], "bordereau_pages": []}
    report.write_text(json.dumps({"sheets": [extra, known]}), encoding="utf-8")
    gold = tmp_path / "gold"
    gold.mkdir()
    (gold / "provenance.json").write_text('{"sheets": [{"sheet": "E01", "exemple_page": 1}]}', encoding="utf-8")

    result = verify(pdf, report, pdf, gold)

    assert result["ok"] is False and result["sheets_ok"] is False
    assert result["unexpected_sheets"] == ["EXTRA"]
    assert result["actual_sheets"] == ["EXTRA", "E01"]
    assert [row["sheet"] for row in result["sheets"]] == ["E01"]
    assert result["sheets"][0]["header_ok"] is False
    output = tmp_path / "verification.json"
    assert verify_main([str(pdf), str(report), str(pdf), str(gold), "--json", str(output)]) == 1
    assert json.loads(output.read_text(encoding="utf-8"))["unexpected_sheets"] == ["EXTRA"]


def draw_plan(path: Path, n_pages: int = 1) -> list[list[tuple[float, float]]]:
    """Plan with rooms in the upper half, symbols inside rooms, empty lower-left band, title block right."""
    doc = pymupdf.open()
    pts = []
    for p in range(n_pages):
        page = doc.new_page(width=W, height=H)
        page.draw_rect(pymupdf.Rect(40, 40, W - 40, H - 40), width=1.5)
        page.draw_line((TITLE_X, 40), (TITLE_X, H - 40), width=1.5)          # title-block frame
        page.insert_text((TITLE_X + 20, H - 80), f"E{100 + p}", fontsize=30)
        page.insert_text((TITLE_X + 20, H - 140), "NE PAS UTILISER POUR CONSTRUCTION", fontsize=9)
        for i in range(6):                                                       # rooms
            r = pymupdf.Rect(150 + i * 320, 120, 150 + i * 320 + 300, 520)
            page.draw_rect(r, width=1)
            page.insert_text((r.x0 + 100, r.y0 + 40), f"LOGEMENT {201 + i}", fontsize=12)
        sym = []
        for i in range(6):
            for j in range(4):
                x, y = 200 + i * 320 + j * 60, 300 + (j % 2) * 90
                page.draw_circle((x, y), 4, width=0.8)
                sym.append((x, y))
        pts.append(sym)
    doc.save(path)
    return pts


def write_input(d: Path, pts: list[tuple[float, float]], sheet: str = "DSI01", reserve_cleared: int = 0) -> None:
    d.mkdir(parents=True, exist_ok=True)
    counters, rows = {}, []
    seq = {}
    for k, (x, y) in enumerate(pts):
        code, mat, des = FAMS[k % len(FAMS)]
        seq[code] = seq.get(code, 0) + 1
        rep = f"{code}-{seq[code]:02d}"
        src = f"{sheet}-{k + 1:03d}"
        counters.setdefault((code, mat), []).append(
            {"sheet": sheet, "page": 1, "x": x, "y": y, "bbox": [x - 4.19, y - 4.19, x + 4.19, y + 4.19],
             "shape": "circle", "repere": rep, "source": src})
        rows.append({"feuille": sheet, "repere": rep, "source": src, "materiel": mat, "designation": des, "qte": 1,
                     "portee": "RENVOI_LOGEMENTS" if code == "I01" else "INSTALLER",
                     "modele": "MODELE NON PRECISE", "prescription": "120V montage mural suivant notes " * (k % 3),
                     "parent": "", "reserve": "0" if k < reserve_cleared else ""})
    est = {"sheets": [{"page": 1, "sheet": sheet, "width_px": W, "height_px": H}],
           "counters": [{"family": c, "name": m, "elements": els} for (c, m), els in counters.items()]}
    (d / "estimate.json").write_text(json.dumps(est), encoding="utf-8")
    with open(d / "bordereau.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS + ["reserve"])
        w.writeheader()
        w.writerows(rows)
    (d / "reserves.md").write_text(f"## {sheet}\nReleve identification et quantites sans prix.\n"
                                   "Verification native indisponible.\n", encoding="utf-8")


def marker_centres(page: pymupdf.Page, box: pymupdf.Rect) -> list[tuple[float, float]]:
    return [((d["rect"].x0 + d["rect"].x1) / 2, (d["rect"].y0 + d["rect"].y1) / 2) for d in page.get_drawings()
            if d.get("fill_opacity") and abs(d["fill_opacity"] - S.FILL_OPACITY) < 0.01
            and not box.intersects(d["rect"])]


@pytest.fixture
def rendered(tmp_path):
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans)[0]
    write_input(tmp_path / "in", pts)
    out = tmp_path / "out.pdf"
    rep = render(load_input(tmp_path / "in"), plans, out, log=lambda *a: None)
    return pts, out, rep


def test_plan_page_markers_at_exact_positions(rendered):
    pts, out, rep = rendered
    doc = pymupdf.open(out)
    page = doc[0]
    box = pymupdf.Rect(rep["sheets"][0]["box"])
    got = marker_centres(page, box)
    assert len(got) == len(pts)
    for x, y in pts:
        assert min(math.hypot(x - a, y - b) for a, b in got) < 0.01


def test_plan_page_keeps_original_vector_content(rendered, tmp_path):
    _, out, _ = rendered
    text = pymupdf.open(out)[0].get_text()
    assert "LOGEMENT 201" in text and "NE PAS UTILISER POUR CONSTRUCTION" in text
    assert pymupdf.open(out)[0].get_images() == []          # nothing rasterised


def test_releve_box_header_and_placement(rendered):
    pts, out, rep = rendered
    s = rep["sheets"][0]
    page = pymupdf.open(out)[0]
    text = page.get_text()
    assert "RELEVE DSI01 - MATERIEL" in text
    assert f"{len(pts)} reperes / 3 familles / RES {len(pts)}" in text
    assert "Calques activables; modeles, prescriptions et reserves completes page 2" in text
    assert S.WARN_TEXT in text.replace("\n", " ")
    for code, mat, _ in FAMS:
        assert code in text and mat in text
    assert "8 / R8" in text                                     # 24 symbols / 3 families, all in reserve
    box = pymupdf.Rect(s["box"])
    assert s["box_in_free_space"]
    assert box.x1 < TITLE_X                                     # never on the title block
    for x, y in pts:
        assert not box.contains(pymupdf.Point(x, y))


def test_labels_and_layers(rendered):
    pts, out, _ = rendered
    doc = pymupdf.open(out)
    words = {w[4] for w in doc[0].get_text("words")}
    assert {"I01-01", "I02-08", "I03-08"} <= words
    names = {v["name"] for v in doc.get_ocgs().values()}
    assert {f"RELEVE {c} - {m}" for c, m, _ in FAMS} <= names
    assert S.LEGEND_LAYER in names


def test_bordereau_pages(rendered):
    pts, out, rep = rendered
    doc = pymupdf.open(out)
    s = rep["sheets"][0]
    assert rows_per_page(H) == 21
    assert s["bordereau_pages"] == [2, 3]                      # 24 rows -> 21 + 3
    assert doc.page_count == 3
    for pno in s["bordereau_pages"]:
        t = doc[pno - 1].get_text()
        assert "BORDEREAU MATERIEL - DSI01" in t
        for head in ("Repere / source", "Materiel", "Designation", "Qte", "Portee", "Modele",
                     "Prescription / reserve", "Parent"):
            assert head in t
    allt = "".join(doc[p - 1].get_text() for p in s["bordereau_pages"])
    for k in range(len(pts)):
        assert f"DSI01-{k + 1:03d}" in allt
    assert "RESERVES ET COMPLEMENTS" in doc[2].get_text()
    toc = doc.get_toc()
    assert toc[0][1:] == ["DSI01 - plan", 1] and toc[1][1:] == ["Bordereau materiel DSI01", 2]


def test_bordereau_header_fill_and_row_order(rendered):
    _, out, _ = rendered
    page = pymupdf.open(out)[1]
    fills = [d for d in page.get_drawings() if d.get("fill") and d["rect"].height > 20]
    assert fills and all(abs(a - b) < 0.01 for a, b in zip(fills[0]["fill"], S.B_HEAD_FILL))
    ys = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for sp in l["spans"]:
                ys.setdefault(sp["text"], sp["origin"][1])
    assert ys["I01-01"] < ys["I01-02"] < ys["I02-01"] < ys["I03-01"]


def test_reserve_override(tmp_path):
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans)[0]
    write_input(tmp_path / "in", pts, reserve_cleared=5)
    sheets = load_input(tmp_path / "in")
    assert sheets[0].n_reserves == len(pts) - 5


def test_plain_estimator_output_px_scaling(tmp_path):
    """No repere / bordereau.csv: codes F01.., default wording, raster px mapped onto PDF points."""
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans)[0]
    d = tmp_path / "est"
    d.mkdir()
    est = {"sheets": [{"page": 1, "sheet": "E100", "width_px": 2 * W, "height_px": 2 * H}],
           "counters": [{"family": "dispositif", "name": "DISPOSITIF",
                         "elements": [{"sheet": "E100", "page": 1, "x": 2 * x, "y": 2 * y, "flags": []}
                                      for x, y in pts]}]}
    (d / "estimate.json").write_text(json.dumps(est), encoding="utf-8")
    out = tmp_path / "o.pdf"
    run_cli("-m", "src.estimer.render", str(d), str(plans), str(out), "--report", str(tmp_path / "r.json"))
    rep = json.loads((tmp_path / "r.json").read_text())
    doc = pymupdf.open(out)
    got = marker_centres(doc[0], pymupdf.Rect(rep["sheets"][0]["box"]))
    assert len(got) == len(pts)
    for x, y in pts:
        assert min(math.hypot(x - a, y - b) for a, b in got) < 0.01
    t = doc[1].get_text()
    assert "F01-01" in t and "E100-001" in t and "MODELE NON PRECISE" in t and "A PRECISER" in t
    assert f"{len(pts)} reperes / 1 familles / RES {len(pts)}" in doc[0].get_text()


def test_two_sheets_order(tmp_path):
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans, n_pages=2)
    d = tmp_path / "in"
    write_input(d, pts[0], "DSI01")
    est = json.loads((d / "estimate.json").read_text())
    est["sheets"].append({"page": 2, "sheet": "DSI02", "width_px": W, "height_px": H})
    est["counters"].append({"family": "I01", "name": "X",
                            "elements": [{"sheet": "DSI02", "page": 2, "x": x, "y": y} for x, y in pts[1][:3]]})
    (d / "estimate.json").write_text(json.dumps(est))
    rep = render(load_input(d), plans, tmp_path / "o.pdf", log=lambda *a: None)
    assert [s["plan_page"] for s in rep["sheets"]] == [1, 4]
    doc = pymupdf.open(tmp_path / "o.pdf")
    assert "E101" in doc[3].get_text() and "RELEVE DSI02 - MATERIEL" in doc[3].get_text()
    assert "page 5" in doc[3].get_text()


def test_wrap_never_truncates_long_cells():
    """Plus de '...' : la ligne du bordereau grandit (correction des cellules tronquées de l'EXEMPLE)."""
    lines = wrap("mot " * 400, 9, 300)
    assert " ".join(lines).split() == ["mot"] * 400 and not lines[-1].endswith("...")
    assert len(wrap("mot " * 400, 9, 300, max_lines=S.B_MAX_CELL_LINES)) == S.B_MAX_CELL_LINES


def test_corrections_exemple_journal():
    from src.estimer.render import corrections_exemple as C
    j = []
    assert C.corriger_cellule("E01", "T", "source", "voir note7 lotA circuit120V15A", {}, j) \
        == "voir note 7 lot A circuit 120V 15A"
    assert C.corriger_cellule("E03", "AF", "modele", "Non renseigne", {}, j) == C.MODELE_NON_INDIQUE
    assert C.corriger_cellule("E01", "I", "source", "quantite physique a confirme...", {}, j) \
        == "quantite physique a confirmer."
    assert C.corriger_cellule("E06", "CH", "source", "Conserve (note 8). Forme compacte...", {}, j) \
        == "Conserve (note 8). " + C.RENVOI_NOTES
    assert C.corriger_cellule("EU", "BD", "source", "A enlever. B. A enlever. C.", {}, j) == "A enlever. B. C."
    assert C.corriger_cellule("E01", "I", "source", "7,8,9 NEMA5-20R", {}, j) == "7,8,9 NEMA 5-20R"
    assert {r for e in j for r in e["regles"]} >= {"ESPACE-MOT-CHIFFRE", "MODELE-VIDE", "TRONCATURE",
                                                     "PHRASE-DOUBLEE", "ESPACE-NORME"}


def test_item_reserve_default_and_seq():
    it = Item(sheet="A", page=1, x=0, y=0, code="I01", repere="I01-07")
    assert it.reserve and it.seq == 7
    it.reserve_override = False
    assert not it.reserve
    sh = Sheet("A", 1, None, None, [it, Item("A", 1, 0, 0, "I02", "I02-01", shape="rect")])
    fams = sh.families()
    assert [f.code for f in fams] == ["I01", "I02"] and fams[1].shape == "rect"


# ---------------------------------------------------------------- gold input builder
def make_exemple(path: Path) -> list[tuple[str, float, float]]:
    """EXEMPLE-like PDF: plan content + PyMuPDF overlay in 'RELEVE ...' layers, one stream per primitive."""
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    page.draw_rect(pymupdf.Rect(100, 100, 900, 600), width=1)
    page.insert_text((200, 200), "SALLE ELECTRIQUE", fontsize=14)
    oc = doc.add_ocg("RELEVE I01 - AVERTISSEUR", on=True)
    legend = doc.add_ocg(S.LEGEND_LAYER, on=True)
    marks = [("I01-01", 300.0, 300.0), ("I01-02", 500.0, 420.0)]
    for rep, x, y in marks:
        page.draw_circle((x, y), 4.1859, color=(1, 0.69, 0), fill=(1, 0.69, 0), fill_opacity=0.28, oc=oc)
        page.draw_line((x, y), (x + 6.19, y), color=(1, 0.69, 0), width=0.35, oc=oc)
        page.draw_rect(pymupdf.Rect(x + 6.19, y - 4, x + 22.8, y + 4), color=None, fill=(1, 1, 1),
                       fill_opacity=0.88, oc=oc)
        page.insert_text((x + 7.19, y + 1.16), rep, fontsize=4.8, oc=oc)
    page.draw_rect(pymupdf.Rect(1000, 1000, 1500, 1100), color=(0.25, 0.3, 0.35), fill=(1, 1, 1), oc=legend)
    page.insert_text((1010, 1016), "RELEVE DSI01 - MATERIEL", fontname="hebo", fontsize=12, oc=legend)
    doc.save(path)
    return marks


def test_from_exemple_extracts_gold_and_strips_overlay(tmp_path):
    ex = tmp_path / "EXEMPLE.pdf"
    marks = make_exemple(ex)
    bcsv, fcsv = tmp_path / "b.csv", tmp_path / "f.csv"
    with open(bcsv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for k, (rep, _, _) in enumerate(marks):
            w.writerow({"feuille": "DSI01", "repere": rep, "source": f"DSI01-{k + 40}", "materiel": "AVERTISSEUR",
                        "designation": "A", "qte": 1, "portee": "INSTALLER", "modele": "MODELE NON PRECISE",
                        "prescription": "p", "parent": ""})
    fcsv.write_text("feuille,discipline,lot,batiment,reperes,familles,res,page,af_entete\n"
                    "DSI01,INCENDIE,LOT A,X,2,1,2,1,\n")
    out = tmp_path / "gold"
    prov = FX.build(ex, bcsv, fcsv, out, log=lambda *a: None)
    s = prov["sheets"][0]
    assert s["markers"] == 2 and not s["missing_markers"] and not s["markers_without_row"]
    est = json.loads((out / "estimate.json").read_text())
    els = {e["repere"]: e for c in est["counters"] for e in c["elements"]}
    for rep, x, y in marks:
        assert abs(els[rep]["x"] - x) < 0.01 and abs(els[rep]["y"] - y) < 0.01 and els[rep]["shape"] == "circle"
    assert els["I01-01"]["source"] == "DSI01-40"
    clean = pymupdf.open(out / "plans.pdf")
    assert "SALLE ELECTRIQUE" in clean[0].get_text() and "RELEVE" not in clean[0].get_text()
    assert not [d for d in clean[0].get_drawings() if d.get("fill_opacity") and d["fill_opacity"] < 0.5]
    assert not [v for v in clean.get_ocgs().values() if v["name"].startswith("RELEVE")]
    # and the renderer puts the markers back where the gold had them
    rep = render(load_input(out), out / "plans.pdf", tmp_path / "r.pdf", log=lambda *a: None)
    got = marker_centres(pymupdf.open(tmp_path / "r.pdf")[0], pymupdf.Rect(rep["sheets"][0]["box"]))
    assert sorted((round(a, 2), round(b, 2)) for a, b in got) == [(300.0, 300.0), (500.0, 420.0)]


def test_legend_counts_reperes_not_multipliers(tmp_path):
    """EXEMPLE E02 M07: 8 reperes whose Qte sum is 23 -> legend '8 / R8'; Qte stays in the bordereau."""
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans)[0]
    write_input(tmp_path / "in", pts)
    rows = list(csv.DictReader(open(tmp_path / "in" / "bordereau.csv", newline="")))
    rows[0]["qte"] = "5"
    with open(tmp_path / "in" / "bordereau.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    render(load_input(tmp_path / "in"), plans, tmp_path / "o.pdf", log=lambda *a: None)
    doc = pymupdf.open(tmp_path / "o.pdf")
    assert "8 / R8" in doc[0].get_text() and "12 / R12" not in doc[0].get_text()
