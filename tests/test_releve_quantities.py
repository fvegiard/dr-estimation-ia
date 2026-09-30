"""Aggregate quantities must never silently become a single counted device."""
import csv
import json

import pytest
from PIL import Image

from releve import build_qpl, commun, render_pdf


def workdir(tmp_path, quantity="20"):
    rows = {
        "occurrences-visuel.csv": [["feuille", "label", "x_pt", "y_pt", "qte"],
                                   ["E01", "DEMO", "25", "30", quantity],
                                   ["E01", "DEMO", "50", "60", ""]],
        "nomenclature.csv": [["label", "famille"], ["DEMO", "autre"]],
        "feuilles.csv": [["feuille", "largeur_pt", "hauteur_pt"], ["E01", "100", "100"]],
        "feuilles-classement.csv": [["feuille", "type"], ["E01", "plan"]],
    }
    for name, data in rows.items():
        with (tmp_path / name).open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerows(data)
    (tmp_path / "rasters").mkdir()
    Image.new("RGB", (100, 100), "white").save(tmp_path / "rasters/E01.png")
    return tmp_path


def test_loader_preserves_quantity_and_defaults_one(tmp_path):
    assert [o["qte"] for o in commun.load_occurrences(workdir(tmp_path))] == [20, 1]


@pytest.mark.parametrize("value", ["0", "-2", "nan", "inf", "not-a-number"])
def test_invalid_quantity_blocks_instead_of_dropping_occurrence(tmp_path, value):
    with pytest.raises(ValueError, match="qte"):
        commun.load_occurrences(workdir(tmp_path, value))


def test_pdf_report_sums_quantity_without_duplicating_marks(tmp_path):
    work = workdir(tmp_path)
    render_pdf.main(str(work), "Test", str(work / "out"))
    report = (work / "out/Test-Rapport-de-metre.md").read_text(encoding="utf-8")
    assert "| DEMO | autre | 21 |" in report
    assert "| E01 | 2 | 21 | 1 |" in report


def test_qpl_rejects_unsupported_multiplier_before_writing_output(tmp_path):
    work = workdir(tmp_path)
    with pytest.raises(ValueError, match="QPL.*qte"):
        build_qpl.main(str(work), "Test", str(work / "out"))
    assert not list((work / "out").glob("*.qpl"))
    assert not list((work / "out").glob("*.png"))


def test_legacy_unit_quantities_still_export_to_qpl(tmp_path):
    work = workdir(tmp_path, "1")
    build_qpl.main(str(work), "Test", str(work / "out"))
    audit = json.loads((work / "out/Test.qpl.audit.json").read_text(encoding="utf-8"))
    assert audit["marques"] == 2
    assert audit["par_feuille"]["E01"]["DEMO"] == 2
