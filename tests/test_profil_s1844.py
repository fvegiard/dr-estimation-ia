"""Témoins synthétiques aux dimensions et styles lus sur les plans, aucun relevé humain."""
from pathlib import Path
import sys

import pymupdf as pdf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releve"))
from profil_s1844 import COULEURS, PRISE, prises, projecteurs, recouper_prises  # noqa: E402


def mot(x, y, nom):
    return (x, y, x + 11, y + 5, nom)


def prises_trace(style, avec_traverses=True, avec_cadre=False):
    doc = pdf.open()
    page = doc.new_page()
    col = COULEURS[style]
    page.draw_circle((50, 50), 6.3, color=col, width=1.08)
    if avec_traverses:
        for y in (48.25, 51.75):
            page.draw_line((43.2, y), (62.8, y), color=col, width=1.08)
    if avec_cadre:
        page.draw_rect((44, 44, 56, 56), color=col, width=1.08)
    return page.get_drawings()


@pytest.mark.parametrize("style, tag, feuille, portee", [
    ("cyan", "N.", "E200", "INSTALLER"), ("cyan", "E.C.", "E200", "CONSERVER"),
    ("gris", "E.C.", "E200D", "CONSERVER"), ("rouge", "N.", "E200D", ""),
    ("cyan", "E.D.", "E200", ""), ("cyan", "N.", "E200D", ""),
])
def test_prise_portee_pas_de_couleur_seule(style, tag, feuille, portee):
    [c] = prises(prises_trace(style), [mot(63, 48, tag)], feuille)
    assert c.portee == portee
    assert c.label == (PRISE if portee else "")
    assert bool(c.motif) != bool(portee)


def test_variantes_glyphe_incomplet_et_etiquette_absente():
    mots = [mot(63, 48, "N.")]
    assert not prises(prises_trace("cyan", avec_traverses=False), mots, "E200")[0].label
    assert not prises(prises_trace("cyan", avec_cadre=True), mots, "E200")[0].label
    assert not prises(prises_trace("cyan"), [], "E200")[0].label


def test_doublon_entre_feuilles_est_unique_ou_reserve():
    mots = [mot(63, 48, "E.C.")]
    nouveau = prises(prises_trace("cyan"), mots, "E200")
    demolition = prises(prises_trace("gris"), mots, "E200D")
    recouper_prises(nouveau, demolition)
    assert len([r for r in nouveau + demolition if r.label]) == 1
    assert "même existant" in nouveau[0].motif
    nouveau = prises(prises_trace("cyan"), [mot(63, 48, "N.")], "E200")
    recouper_prises(nouveau, demolition)
    assert nouveau[0].label == "" and "non résolu" in nouveau[0].motif


def traces_projecteur(rail=True, style="vert"):
    doc = pdf.open()
    p = doc.new_page()
    col = COULEURS[style]
    if rail:
        p.draw_quad(pdf.Quad((10, 47.7), (90, 47.7), (10, 50), (90, 50)), color=col, width=1.08)
    p.draw_polyline([(48, 54.5), (53.2, 54.5), (50.6, 50), (48, 54.5)], color=col, width=1.08)
    return p.get_drawings()


@pytest.mark.parametrize("tag", ["D3-N", "D4-NT1", "D3-BT2", "D4-B"])
def test_meme_triangle_type_lu_dans_etiquette(tag):
    [c] = projecteurs(traces_projecteur(), [mot(55, 50, tag)], "E300")
    assert c.label == f"PROJECTEUR {tag}" and c.portee == "INSTALLER"


def test_projecteur_negatifs():
    mots = [mot(55, 50, "D3-N")]
    assert not projecteurs(traces_projecteur(rail=False), mots, "E300")[0].label
    assert not projecteurs(traces_projecteur(style="pâle"), mots, "E300")[0].label
    assert not projecteurs(traces_projecteur(), mots, "E300D")[0].label
    assert not projecteurs(traces_projecteur(), [mot(55, 50, "D2")], "E300")[0].label
    assert not projecteurs(traces_projecteur(), mots + [mot(55, 51, "D4-N")], "E300")[0].label


def test_etiquette_de_l_autre_cote_du_rail_ne_prend_pas_le_triangle():
    traces = traces_projecteur()
    # D4 plus proche du centre du triangle, mais au-dessus du rail horizontal.
    [c] = projecteurs(traces, [mot(47, 43, "D4-N"), mot(55, 50, "D3-N")], "E300")
    assert c.label == "PROJECTEUR D3-N"


def test_etiquette_centree_au_devant_de_la_tete():
    [c] = projecteurs(traces_projecteur(), [mot(45, 56, "D4-N")], "E300")
    assert (c.label, c.portee) == ("PROJECTEUR D4-N", "INSTALLER")
    assert "centrée au-devant" in c.preuve


@pytest.mark.parametrize("mots, feuille", [
    ([mot(45, 39, "D4-N")], "E300"),                     # autre côté du rail
    ([mot(42, 56, "D4-N")], "E300"),                     # pas centré
    ([mot(45, 56, "D4-N"), mot(45, 57, "D3-N")], "E300"),  # disputé
    ([mot(45, 56, "D4-N")], "E300D"),                    # aucune pose en dépose
])
def test_etiquette_devant_reste_en_reserve_si_non_univoque(mots, feuille):
    [c] = projecteurs(traces_projecteur(), mots, feuille)
    assert not c.label and not c.portee and c.motif


def test_couloir_lateral_ne_change_pas_de_type():
    [c] = projecteurs(traces_projecteur(), [mot(45, 56, "D4-N"), mot(55, 50, "D3-N")], "E300")
    assert c.label == "PROJECTEUR D3-N"