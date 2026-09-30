import json
from pathlib import Path

import pymupdf
import pytest
from PIL import Image

from releve import zoom


def source_page(tmp_path, rotation=0):
    sheets = tmp_path / "feuilles"
    sheets.mkdir()
    with pymupdf.open() as doc:
        page = doc.new_page(width=240, height=180)
        page.draw_circle((130.25, 90.75), 2, color=(1, 0, 0), fill=(1, 0, 0))
        page.set_rotation(rotation)
        doc.save(sheets / "P1.pdf")
    return tmp_path


@pytest.mark.parametrize("bounds,px", [
    ((40, 30, 200, 150), 800),
    ((40.3, 30.6, 200.8, 150.2), 800),
    ((-15.4, -12.7, 260.6, 200.3), 800),
    ((40.3, 30.6, 200.8, 150.2), 1200),
])
def test_zoom_reports_exact_pixel_frame_without_ruler_padding(tmp_path, monkeypatch, capsys, bounds, px):
    work = source_page(tmp_path)
    monkeypatch.setattr(zoom.sys, "argv", ["zoom.py", str(work), "P1", *map(str, bounds), "--px", str(px), "--sans-marques"])
    zoom.main()
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert Path(lines[0]).is_file()  # Existing callers retain the path on the first line.
    assert len(lines) == 1
    metadata = json.loads(captured.err)
    assert metadata["requested_bounds_pt"] == list(bounds)
    assert metadata["effective_clip_bounds_pt"] == list(pymupdf.Rect(bounds) & pymupdf.Rect(0, 0, 240, 180))
    assert metadata["rulers_overlay"] is True
    assert metadata["added_padding_px"] == [0, 0, 0, 0]
    with Image.open(lines[0]) as im:
        assert metadata["image_size_px"] == list(im.size)
        z = metadata["pixels_per_pdf_point"]
        ox, oy = metadata["pixmap_origin_px"]
        u, v = 130.25 * z - ox, 90.75 * z - oy
        red, green, blue = im.getpixel((round(u), round(v)))
        assert red > 220 and green < 50 and blue < 50
        assert (ox + u) / z == pytest.approx(130.25)
        assert (oy + v) / z == pytest.approx(90.75)
        assert metadata["raster_bounds_pt"] == pytest.approx([ox/z, oy/z, (ox+im.width)/z, (oy+im.height)/z])


@pytest.mark.parametrize("bounds", [
    (0, 0, 0, 100), (100, 0, 10, 100), (0, 100, 100, 10),
    (0, 0, float("nan"), 100), (0, 0, float("inf"), 100), (250, 0, 300, 100),
])
def test_zoom_rejects_invalid_or_off_page_bounds(tmp_path, monkeypatch, bounds):
    work = source_page(tmp_path)
    monkeypatch.setattr(zoom.sys, "argv", ["zoom.py", str(work), "P1", *map(str, bounds), "--sans-marques"])
    with pytest.raises(ValueError, match="bounds"):
        zoom.main()
    assert not (work / "zooms").exists()


@pytest.mark.parametrize("rotation", [90, 180, 270])
def test_zoom_mapping_uses_displayed_frame_on_rotated_page(tmp_path, monkeypatch, capsys, rotation):
    work = source_page(tmp_path, rotation)
    with pymupdf.open(work / "feuilles/P1.pdf") as doc:
        bounds = list(doc[0].rect)
        center = pymupdf.Point(130.25, 90.75) * doc[0].rotation_matrix
    monkeypatch.setattr(zoom.sys, "argv", ["zoom.py", str(work), "P1", *map(str, bounds), "--px", "800", "--sans-marques"])
    zoom.main()
    captured = capsys.readouterr()
    metadata = json.loads(captured.err)
    assert metadata["source_rotation_degrees"] == rotation
    assert metadata["coordinate_frame"] == "displayed_page_pdf_points"
    z = metadata["pixels_per_pdf_point"]
    ox, oy = metadata["pixmap_origin_px"]
    with Image.open(captured.out.strip()) as im:
        u, v = round(center.x*z-ox), round(center.y*z-oy)
        red, green, blue = im.getpixel((u, v))
        assert red > 220 and green < 50 and blue < 50


def test_zoom_marker_uses_actual_pixmap_origin(tmp_path, monkeypatch, capsys):
    work = source_page(tmp_path)
    drawn = []
    monkeypatch.setattr(zoom, "load_nomenclature", lambda work: {})
    monkeypatch.setattr(zoom, "load_occurrences", lambda work: [
        {"feuille": "P1", "label": "known", "x": 130.25, "y": 90.75}])
    monkeypatch.setattr(zoom, "draw_mark", lambda dr, shape, x, y, *args, **kwargs: drawn.append((x, y)))
    monkeypatch.setattr(zoom.sys, "argv", ["zoom.py", str(work), "P1", "40.3", "30.6", "200.8", "150.2", "--px", "800"])
    zoom.main()
    metadata = json.loads(capsys.readouterr().err)
    z = metadata["pixels_per_pdf_point"]
    ox, oy = metadata["pixmap_origin_px"]
    assert drawn == [pytest.approx((130.25*z-ox, 90.75*z-oy))]
