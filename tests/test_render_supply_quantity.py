import csv
import json

import pymupdf
import pytest

from src.estimer.render import load_input, render
from src.estimer.render.bordereau import aggregate_rows
from src.estimer.render.data import Item, Sheet
from src.estimer.render.from_releve import build


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def make_work(tmp_path, supply="0", scope="RACCORDER"):
    work = tmp_path / "work"
    (work / "feuilles").mkdir(parents=True)
    with pymupdf.open() as doc:
        doc.new_page(width=1000, height=700)
        doc.save(work / "feuilles/P1.pdf")
    write_csv(work / "feuilles.csv", ["feuille", "fichier", "page", "largeur_pt", "hauteur_pt"],
              [{"feuille": "P1", "fichier": "source.pdf", "page": 1, "largeur_pt": 1000, "hauteur_pt": 700}])
    write_csv(work / "feuilles-classement.csv", ["feuille", "type", "note", "bordereau"],
              [{"feuille": "P1", "type": "plan", "note": "cartouche=EU01", "bordereau": "travaux"}])
    write_csv(work / "nomenclature.csv", ["label", "code", "materiel", "portee"],
              [{"label": "Equipment", "code": "EQ", "materiel": "EQUIPEMENT EXISTANT", "portee": scope}])
    write_csv(work / "occurrences-visuel.csv", ["feuille", "label", "x_pt", "y_pt", "qte", "qte_fourniture"],
              [{"feuille": "P1", "label": "Equipment", "x_pt": 100, "y_pt": 100, "qte": 4, "qte_fourniture": supply}])
    return work


def test_zero_supply_preserves_connection_work_through_csv_estimate_and_pdf(tmp_path):
    work = make_work(tmp_path)
    out = tmp_path / "output"
    build(work, out, ancrage=False)
    sheet, = load_input(out)
    row, = aggregate_rows(sheet)
    assert row["afournir"] == "0"
    assert row["portee"] == "RACCORDER"
    assert sheet.items[0].qte == 4
    assert sheet.items[0].qte_fourniture == 0
    estimate = json.loads((out / "estimate.json").read_text(encoding="utf-8"))
    assert estimate["counters"][0]["elements"][0]["qte_fourniture"] == 0
    pdf = tmp_path / "raccorder-zero-supply.pdf"
    render([sheet], out / "plans.pdf", pdf)
    with pymupdf.open(pdf) as doc:
        text = " ".join(page.get_text() for page in doc)
    assert "RACCORDER" in text
    assert "0 appareils a fournir" in text


@pytest.mark.parametrize("supply", ["-1", "nan", "inf", "-inf", "invalid"])
def test_invalid_explicit_supply_is_rejected_at_bridge(tmp_path, supply):
    with pytest.raises(ValueError, match="qte_fourniture"):
        build(make_work(tmp_path, supply), tmp_path / "out", ancrage=False)


@pytest.mark.parametrize("scope", ["à enlever", "A ENLEVER", "existant conservé", " EXISTANT   CONSERVE "])
def test_precise_no_purchase_scope_variants(scope):
    item = Item("EU01", 1, 0, 0, "EQ", "EQ-01", qte=4, portee=scope)
    sheet = Sheet("EU01", 1, 1000, 700, items=[item], format="travaux")
    row, = aggregate_rows(sheet)
    assert row["afournir"] == "0"
    assert row["portee"] == scope


def test_supply_sum_keeps_zero_explicit_nonunit_and_default_quantities():
    items = []
    for index, (qte, supply) in enumerate([(4, 0), (2, 3), (5, None), (1, 0.5)], 1):
        item = Item("EU01", 1, 0, 0, "EQ", f"EQ-{index:02d}", qte=qte, portee="RACCORDER")
        item.qte_fourniture = supply
        items.append(item)
    row, = aggregate_rows(Sheet("EU01", 1, 1000, 700, items=items, format="travaux"))
    assert row["afournir"] == "8.5"
    assert row["lieux"] == "4"


@pytest.mark.parametrize("scope", ["REMPLACER", "NE PAS CONSERVER", "ENLEVER ET FOURNIR NEUF"])
def test_no_substring_scope_guessing(scope):
    item = Item("EU01", 1, 0, 0, "EQ", "EQ-01", qte=4, portee=scope)
    row, = aggregate_rows(Sheet("EU01", 1, 1000, 700, items=[item], format="travaux"))
    assert row["afournir"] == "4"


@pytest.mark.parametrize("supply", [None, "", "2.5", "0"])
def test_optional_supply_defaults_and_nonunit_values_round_trip(tmp_path, supply):
    out = tmp_path / "out"
    build(make_work(tmp_path, supply), out, ancrage=False)
    sheet, = load_input(out)
    row, = aggregate_rows(sheet)
    assert row["afournir"] == ("4" if supply in (None, "") else supply)


@pytest.mark.parametrize("target", ["csv", "estimate"])
@pytest.mark.parametrize("invalid", ["nan", "-1", "bad"])
def test_renderer_loader_rejects_invalid_supply(tmp_path, target, invalid):
    out = tmp_path / "out"
    build(make_work(tmp_path), out, ancrage=False)
    if target == "csv":
        path = out / "bordereau.csv"
        with path.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fields, rows = reader.fieldnames, list(reader)
        rows[0]["qte_fourniture"] = invalid
        write_csv(path, fields, rows)
    else:
        (out / "bordereau.csv").unlink()
        path = out / "estimate.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["counters"][0]["elements"][0]["qte_fourniture"] = invalid
        path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="qte_fourniture"):
        load_input(out)


def test_explicit_supply_overrides_scope_inference():
    item = Item("EU01", 1, 0, 0, "EQ", "EQ-01", qte=4, portee="CONSERVER", qte_fourniture=2)
    row, = aggregate_rows(Sheet("EU01", 1, 1000, 700, items=[item], format="travaux"))
    assert row["afournir"] == "2"
    assert row["portee"] == "CONSERVER"


def test_supply_sum_overflow_is_rejected():
    items = [Item("EU01", 1, 0, 0, "EQ", f"EQ-{i}", qte_fourniture=1e308) for i in (1, 2)]
    with pytest.raises(ValueError, match="qte_fourniture"):
        aggregate_rows(Sheet("EU01", 1, 1000, 700, items=items, format="travaux"))
