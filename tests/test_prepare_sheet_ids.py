import pymupdf
import pytest

from releve.prepare import classify, sheet_id


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


def test_multipage_blank_plan_is_input_not_estimator_reference():
    with pymupdf.open() as doc:
        for _ in range(2):
            page = doc.new_page(width=2998, height=1999)
            page.draw_rect(pymupdf.Rect(10, 10, 100, 100))
        assert classify('HR26-14-projet-vide-Plans.pdf', doc) == 'scan'
        assert classify('estimateur-reference.pdf', doc) == 'estimateur'


@pytest.mark.parametrize('name', ['référence-take off.pdf', 'reference.pdf', 'takeoff.pdf', 'take-off.pdf',
                                'bordereau.pdf', 'EXEMPLE.pdf', 'EXEMPLE HR26-14.pdf'])
def test_explicit_reference_filename_cannot_become_raster_source(name):
    with pymupdf.open() as doc:
        page = doc.new_page(width=2998, height=1999)
        page.draw_rect(pymupdf.Rect(10, 10, 100, 100))
        assert classify(name, doc) == 'estimateur'


@pytest.mark.parametrize('field', ['FEUILLE', 'SHEET'])
def test_sheet_field_wins_over_lower_larger_revision(field):
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((850, 555), field, fontsize=10)
        page.insert_text((850, 580), 'E401', fontsize=14)
        page.insert_text((850, 625), 'REVISION', fontsize=10)
        page.insert_text((850, 670), 'R01', fontsize=28)
        assert sheet_id(page) == 'E401'


def test_known_revision_field_is_excluded_without_sheet_heading():
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((850, 580), 'E401', fontsize=14)
        page.insert_text((850, 625), 'REVISION', fontsize=10)
        page.insert_text((850, 670), 'R01', fontsize=28)
        assert sheet_id(page) == 'E401'


def test_adjacent_sheet_and_revision_fields_remain_distinct():
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((730, 625), 'SHEET E401', fontsize=14)
        page.insert_text((900, 625), 'REV. R01', fontsize=14)
        assert sheet_id(page) == 'E401'


def test_conflicting_explicit_sheet_fields_use_provisional_name():
    with pymupdf.open() as doc:
        page = doc.new_page(width=1000, height=700)
        page.insert_text((730, 560), 'SHEET E401', fontsize=14)
        page.insert_text((730, 645), 'SHEET E402', fontsize=14)
        assert sheet_id(page) is None


def test_rotated_page_keeps_sheet_and_revision_field_associations():
    with pymupdf.open() as doc:
        page = doc.new_page(width=700, height=1000)
        page.insert_text((555, 150), 'FEUILLE', fontsize=10, rotate=90)
        page.insert_text((580, 150), 'E401', fontsize=14, rotate=90)
        page.insert_text((625, 150), 'REVISION', fontsize=10, rotate=90)
        page.insert_text((670, 150), 'R01', fontsize=28, rotate=90)
        page.set_rotation(90)
        assert sheet_id(page) == 'E401'


@pytest.mark.parametrize('name', ['sample plan.pdf', 'prereference.pdf', 'exemplerie.pdf', 'HR26-14-projet-vide-Plans.pdf'])
def test_unrelated_or_ambiguous_name_does_not_imply_estimator(name):
    with pymupdf.open() as doc:
        doc.new_page(width=2998, height=1999)
        assert classify(name, doc) == 'scan'


def test_explicit_reference_name_wins_over_addendum_name():
    with pymupdf.open() as doc:
        doc.new_page()
        assert classify('addenda-reference.pdf', doc) == 'estimateur'
