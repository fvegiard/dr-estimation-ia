"""Conservation du gel v3 et limites de la proposition graphique E-3."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'releve-page-par-page'
PACKAGE = ROOT / 'paquet'
BASELINE = json.loads((ROOT / 'baseline-v3.json').read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def data(path):
    spec = importlib.util.spec_from_file_location('reviewed_pilot_data', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SHEETS


def test_historical_sixteen_business_files_stay_untouched():
    assert len(BASELINE['files']) == 16
    for name, expected in BASELINE['files'].items():
        assert sha(BASE / name) == expected, name


def test_only_e3_image_changes_among_business_files():
    changed = [name for name, expected in BASELINE['files'].items()
               if sha(PACKAGE / name) != expected]
    assert changed == ['S-0922-E-3-releve.jpg']


def test_rendered_e3_csv_preserves_every_field_and_coordinate():
    before = BASE / 'S-0922-E-3-equipment.csv'
    after = ROOT / 'travail/S-0922-E-3-equipment.csv'
    assert before.read_bytes() == after.read_bytes()
    with after.open(encoding='utf-8-sig', newline='') as stream:
        records = list(csv.DictReader(stream))
    assert len(records) == len({r['Repère / source'] for r in records}) == 223


def test_reviewed_data_and_e5_correction_are_preserved():
    before = data(BASE / 'methode/sheet_data.py')
    after = data(PACKAGE / 'methode/sheet_data.py')
    assert before == after
    markers = after['E-5']['markers']
    assert len(markers) == 72
    assert markers[-1]['id'] == 'E-5-072'
    assert markers[-1] == before['E-5']['markers'][-1]
    assert all('DO NOT USE FOR CONSTRUCTION' in m['reserve']
               and m['scope'] == 'À PRÉCISER' for m in markers)


def test_whole_page_and_empty_internal_legend_region():
    source = ROOT / 'travail/sources/23-357-E-CO-CH-E1 (1) - 3.png'
    assert sha(source) == BASELINE['source_sha256']
    report = json.loads((ROOT / 'travail/inspection/E-3/layout-report.json').read_text(encoding='utf-8'))
    with Image.open(source) as original, Image.open(PACKAGE / 'S-0922-E-3-releve.jpg') as output:
        assert original.size == output.size == tuple(BASELINE['source_size'])
        x, y, w, h = report['legend_box']
        scale = original.width / 1800
        box = tuple(round(v * scale) for v in (x, y, x + w, y + h))
        assert 0 <= box[0] < box[2] <= original.width
        assert 0 <= box[1] < box[3] <= original.height
        assert sum(original.crop(box).convert('L').histogram()[:200]) == 0


def test_legend_keeps_quantities_notes_and_two_numeric_columns():
    report = json.loads((ROOT / 'travail/inspection/E-3/layout-report.json').read_text(encoding='utf-8'))
    sheet = data(BASE / 'methode/sheet_data.py')['E-3']
    assert report['notes'] == sheet['notes']
    assert {r['family'] for r in report['rows']} == set(sheet['families'])
    assert sum(r['quantity'] for r in report['rows']) == 223
    assert len({r['quantity_right'] for r in report['rows']}) == 2
    assert report['qpl_global'] == 'BLOCKED'
    assert report['construction_validation'] is False


def test_fourteen_linear_shapes_keep_the_frozen_anchor_inside():
    report = json.loads((ROOT / 'travail/inspection/E-3/layout-report.json').read_text(encoding='utf-8'))
    sheet = data(BASE / 'methode/sheet_data.py')['E-3']
    linears = {m['id']: m for m in sheet['markers'] if m['family'] == 'G'}
    assert set(report['linear_boxes']) == set(linears)
    assert len(linears) == 14
    for identifier, marker in linears.items():
        left, top, right, bottom = report['linear_boxes'][identifier]
        assert left < marker['x'] < right
        assert top < marker['y'] < bottom
        if identifier == 'E-3-176':
            assert right - left > bottom - top
        else:
            assert bottom - top > right - left


def test_pilot_explicitly_refuses_other_sheets():
    method = PACKAGE / 'methode'
    sys.path.insert(0, str(method))
    try:
        spec = importlib.util.spec_from_file_location('pilot_renderer', method / 'render_sheet.py')
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)
        with pytest.raises(ValueError, match='limité à E-3'):
            renderer.render('E-5', pilot=True)
    finally:
        sys.path.pop(0)
