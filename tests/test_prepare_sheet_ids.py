import pymupdf
import pytest

from releve.prepare import sheet_id


@pytest.mark.parametrize('name,expected', [('DSI01', 'DSI01'), ('EU04', 'EU04'), ('E-01', 'E01'), ('E401', 'E401')])
def test_source_sheet_number_in_title_block(name, expected):
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((850, 650), name, fontsize=24)
        assert sheet_id(page) == expected


def test_device_label_above_title_block_does_not_override_sheet():
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((850, 550), 'DF01', fontsize=24)
        page.insert_text((850, 650), 'E401', fontsize=14)
        assert sheet_id(page) == 'E401'


def test_sheet_reference_in_page_body_is_not_its_identifier():
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((100, 100), 'SEE E401', fontsize=24)
        assert sheet_id(page) is None
