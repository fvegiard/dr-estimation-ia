"""Source geometry evidence must not move or invent occurrence coordinates."""
import csv

import pymupdf
import pytest

from releve import traits


def test_candidates_are_source_centers_sorted_by_distance():
    with pymupdf.open() as doc:
        page = doc.new_page(width=200, height=200)
        page.draw_rect(pymupdf.Rect(10, 10, 20, 20))
        page.draw_rect(pymupdf.Rect(70, 70, 80, 80))
        result = traits.closed_shape_candidates(page, 16, 15)
        assert result[0]["center_pt"] == [15.0, 15.0]
        assert result[0]["distance_pt"] == 1.0
        assert result[1]["center_pt"] == [75.0, 75.0]
        assert result[1]["distance_pt"] > 80


def test_raster_page_has_no_closed_vector_candidates():
    with pymupdf.open() as source:
        page = source.new_page(width=100, height=100)
        page.draw_rect(pymupdf.Rect(10, 10, 20, 20))
        png = page.get_pixmap().tobytes("png")
    with pymupdf.open() as doc:
        page = doc.new_page(width=100, height=100)
        page.insert_image(page.rect, stream=png)
        assert traits.closed_shape_candidates(page, 15, 15) == []


def test_candidates_use_rotated_page_coordinates():
    with pymupdf.open() as doc:
        page = doc.new_page(width=200, height=100)
        page.draw_rect(pymupdf.Rect(10, 10, 20, 20))
        page.set_rotation(90)
        result = traits.closed_shape_candidates(page, 85, 15)
        assert result[0]["center_pt"] == [85.0, 15.0]
        assert result[0]["distance_pt"] == 0.0


def test_traits_preserves_existing_sections_and_prints_geometry(tmp_path, monkeypatch, capsys):
    pdf = tmp_path / "source.pdf"
    with pymupdf.open() as doc:
        page = doc.new_page(width=100, height=100)
        page.draw_rect(pymupdf.Rect(10, 10, 20, 20))
        doc.save(pdf)
    with (tmp_path / "feuilles.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["feuille", "fichier", "page"])
        writer.writerow(["P1", "source.pdf", 1])
    monkeypatch.setenv("RELEVE_INBOX", str(tmp_path))
    before = pdf.read_bytes()
    traits.main(str(tmp_path), "P1", 16, 15)
    output = capsys.readouterr().out
    assert "## Texte" in output and "## Tracés" in output
    assert "## Formes fermées candidates" in output
    assert '"center_pt": [15.0, 15.0]' in output
    assert pdf.read_bytes() == before


@pytest.mark.parametrize("rotation,point", [(0, (15, 15)), (90, (85, 15))])
def test_traits_reads_prepared_page_without_external_inbox(tmp_path, monkeypatch, capsys, rotation, point):
    (tmp_path / "feuilles").mkdir()
    with pymupdf.open() as doc:
        page = doc.new_page(width=200, height=100)
        page.draw_rect(pymupdf.Rect(10, 10, 20, 20))
        page.set_rotation(rotation)
        doc.save(tmp_path / "feuilles" / "P1.pdf")
    (tmp_path / "feuilles.csv").write_text("feuille,fichier,page\nP1,external.pdf,42\n", encoding="utf-8")
    monkeypatch.setenv("RELEVE_INBOX", str(tmp_path / "unavailable"))
    traits.main(str(tmp_path), "P1", *point)
    assert '"distance_pt": 0.0' in capsys.readouterr().out
