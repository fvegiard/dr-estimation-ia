"""Témoins synthétiques pour le profil plans seuls; aucun relevé humain."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pymupdf as pdf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releve"))
import profil_s1715 as s  # noqa: E402


def segments(paires):
    return [{"items": [("l", pdf.Point(a), pdf.Point(b)) for a, b in paires]}]


@pytest.mark.parametrize("ouverture, attendu", [(0, 1), (2.64, 1), (4., 0)])
def test_rectangle_a1_dessine_et_pas_seulement_deux_montants(ouverture, attendu):
    x, y = 34.56, 17.28
    traits = [((0, 0), (0, y)), ((x, 0), (x, y)), ((0, y), (x, y)),
              ((0, .1), (x/2, 0)), ((x/2+ouverture, 0), (x, 0))]
    assert len(s.rectangles_a1(segments(traits + [(b, a) for a, b in traits]))) == attendu


@pytest.mark.parametrize("angle", [0, 90, 180, 270])
def test_prise_usb_glyphe_tourne_et_tiges_de_meme_cote(angle):
    tourner = pdf.Matrix(angle)
    points = [pdf.Point(4.92*math.cos(i*math.pi/8), 4.92*math.sin(i*math.pi/8)) * tourner for i in range(16)]
    cercle = list(zip(points, points[1:] + points[:1]))
    tiges = [(pdf.Point(-4.75, y)*tourner, pdf.Point(8.98, y)*tourner) for y in (-1.44, 1.44)]
    assert len(s.prises_usb(segments(cercle))) == 0
    assert len(s.prises_usb(segments(tiges + cercle))) == 1
    a, b = tiges[0]
    assert len(s.prises_usb(segments([(-b, -a), tiges[1], *cercle]))) == 0


def test_pca_encadre_et_refus_d_un_glyphe_dispute():
    pts = [(30, 30), (38.52, 30), (38.52, 48.12), (30, 48.12)]
    r = s._rectangles_pca(segments(zip(pts, pts[1:] + pts[:1])))
    mot = (31, 31, 37, 47, "PCA")
    autre = (120, 80, 150, 100, "PCA")
    lie = lambda m, b: b.contains(m)
    assert list(s._univoques([mot, autre], r, lie)) == [(mot, r[0]), (autre, None)]
    assert list(s._univoques([mot, mot], r, lie)) == [(mot, None), (mot, None)]


def test_raccordement_typique_hors_compte_meme_si_glyphe_identique(monkeypatch):
    bon = np.zeros((12, 18), dtype=bool)
    bon[2:10, 3:13] = True
    patron = (820, 678, 852, 688.3, s.RSP)
    copie = (950, 678, 982, 688.3, s.RSP)
    sans_glyphe = (1400, 678, 1432, 688.3, s.RSP)
    typique = (2563, 1507, 2621, 1517, s.RSP)

    class Page:
        def search_for(self, texte, **_):
            return [pdf.Rect(2540, 1529, 2975, 1549)] if texte == s.TITRE_TYPIQUE else []

        def get_text(self, mode):
            assert mode == "words"
            return [sans_glyphe, typique, patron, copie]

    def image(page, mot):
        b = bon if mot != sans_glyphe else np.zeros_like(bon)
        return b, pdf.Rect(mot[0], mot[3], mot[0] + 9, mot[3] + 6)

    monkeypatch.setattr(s, "_image_rsp", image)
    retour = {m: (r, raison) for m, r, raison in s.controleurs(Page())}
    assert retour[patron][0] and retour[copie][0]
    assert retour[sans_glyphe][0] is None and "sans glyphe" in retour[sans_glyphe][1]
    assert retour[typique][0] is None and "raccordement typique" in retour[typique][1]


def test_le_profil_refuse_un_mauvais_jeu_avant_toute_ecriture(tmp_path):
    (tmp_path / "inventaire.json").write_text(json.dumps({"plans_seuls": True, "fichiers": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="trois PDF attestés"):
        s.appliquer(tmp_path, {})
    assert not (tmp_path / "occurrences-visuel.csv").exists()


def test_le_profil_ne_recrit_pas_un_travail_gele(tmp_path):
    (tmp_path / "gel.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="déjà gelée"):
        s.appliquer(tmp_path, {})