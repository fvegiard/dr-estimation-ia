"""src.estimer.plan_index — synthetic pages only (no client data).

A rotated synthetic PDF with a title block (sheet number, title, scale) checks
that the title block is read in DISPLAYED coordinates, and the pure helpers
(OCR token repair, sheet-list extraction, DND drawing numbers) are exercised on
strings.
"""
from __future__ import annotations

import pymupdf
import pytest

from src.estimer import plan_index as PI


def _pdf_with_title_block(path, rotation: int):
    """Landscape sheet whose title block sits bottom-right AS DISPLAYED, whatever
    the /Rotate of the page (like the S-1714 and S-1769 originals)."""
    doc = pymupdf.open()
    if rotation in (90, 270):
        page = doc.new_page(width=700, height=1000)     # portrait media box displayed landscape
    else:
        page = doc.new_page(width=1000, height=700)
    page.set_rotation(rotation)
    m = page.derotation_matrix                          # displayed -> unrotated coordinates
    def put(x, y, text, size):
        page.insert_text(pymupdf.Point(x, y) * m, text, fontsize=size, rotate=rotation)
    put(40, 60, "NOTES GÉNÉRALES : voir devis", 10)
    put(780, 560, "Titre du dessin", 6)
    put(780, 580, "ÉCLAIRAGE : PLAN DU RDC", 12)
    put(780, 610, "Échelle: 1 : 100", 7)
    put(780, 660, "A1", 8)                               # revision-like token, smaller
    put(900, 670, "E-301", 20)                           # the sheet number, tallest
    doc.save(path)
    doc.close()


@pytest.mark.parametrize("rotation", [0, 90, 270])
def test_title_block_read_in_displayed_coordinates(tmp_path, rotation):
    pdf = tmp_path / "plan.pdf"
    _pdf_with_title_block(pdf, rotation)
    pages = PI.inventory_pdf(pdf, pdf.name, ocr=False)
    assert len(pages) == 1
    p = pages[0]
    assert p.sheet == "E301" and p.sheet_source == "text"
    assert p.title == "ÉCLAIRAGE : PLAN DU RDC"
    assert p.scale == "1 : 100"
    assert p.text_layer == "partial" or p.text_layer == "yes"
    assert p.rotation == rotation
    assert (p.width_pt, p.height_pt) == (1000.0, 700.0)   # displayed size, not the media box


def test_ocr_token_repair():
    assert PI._ocr_token("EOO1") == "E001"
    assert PI._ocr_token("E4O1") == "E401"
    assert PI._ocr_token("EQ02") == "E002"
    assert PI._ocr_token("E-101") == "E101"
    assert PI._ocr_token("E200D") == "E200D"
    assert PI._ocr_token("DOIT") is None       # a word: no digit at all
    assert PI._ocr_token("SSION") is None
    assert PI._ocr_token("2026") is None


def test_dnd_drawing_number_joined_from_two_words():
    words = [(900, 600, 980, 610, "L-S267-1302-01-", 8.0), (982, 600, 1000, 610, "503B", 8.0),
             (900, 500, 950, 510, "QS-000428-B", 8.0)]
    assert PI.find_sheet(words) == ("L-S267-1302-01-503B", "dwg")


def test_sheet_list_from_cover_text():
    text = ("No.\nFEUILLE\nDESCRIPTION\nRÉVISION\nDATE\nE100\nDEVIS\n1\n2026-08-17\n"
            "E103\nLÉGENDE\n1\n2026-08-17\nE400\nSOUS-SOL - ÉCLAIRAGE\n1\n2026-08-17\n"
            "E600\nPANNEAUX\n1\n2026-08-17\n")
    assert PI.extract_sheet_list(text) == [["E100", "DEVIS"], ["E103", "LÉGENDE"],
                                           ["E400", "SOUS-SOL - ÉCLAIRAGE"], ["E600", "PANNEAUX"]]


def test_sheet_list_rejects_spec_pages_full_of_part_numbers():
    text = "FEUILLE DESCRIPTION C802 prise d'ajustement B915 module bosch MP300 batterie E101 devis RS485 bus"
    assert PI.extract_sheet_list(text) == []
    assert PI.extract_sheet_list("E100 DEVIS E101 DEVIS E102 SPEC E103 LEGENDE") == []   # no header


def test_legend_check_ignores_colour_legend_and_sentences():
    assert PI.legend_check([], "LÉGENDE - SUITE")[0]
    assert not PI.legend_check([], "SERVICES NIVEAU 1 LÉGENDE DES COULEURS")[0]
    sentence = [(0, 0, 10, 10, "RÉFÉRER À LA LÉGENDE ET AUX ANNOTATIONS ASSOCIÉES POUR", 12.0)]
    assert not PI.legend_check(sentence, None)[0]
    heading = [(0, 0, 10, 10, "LÉGENDE - ALARME INCENDIE", 12.0)]
    assert PI.legend_check(heading, None)[0]
