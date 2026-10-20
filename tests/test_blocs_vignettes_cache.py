"""Les vignettes gardent leurs pixels et ne réinterprètent chaque page qu'une fois."""
from __future__ import annotations

import csv
import json
import sys

import pymupdf
import pytest

from releve import blocs_vignettes
from releve.blocs_vignettes import _pixmap_cache


@pytest.mark.parametrize("rotation", [0, 90, 180, 270])
def test_cache_pixels_clips_tournes_et_annotations(rotation, monkeypatch):
    with pymupdf.open() as document:
        page = document.new_page(width=300, height=220)
        page.draw_rect((25, 30, 90, 85), color=(1, 0, 0), fill=(0.8, 0.9, 1))
        page.draw_circle((125, 110), 18, color=(0, 0.4, 0))
        page.insert_text((40, 70), "A1", fontsize=14)
        annotation = page.add_rect_annot((100, 90, 150, 135))
        annotation.set_colors(stroke=(0, 0, 1))
        annotation.update()
        page.set_cropbox((10, 15, 290, 210))
        page.set_rotation(rotation)
        clips = [
            pymupdf.Rect(5, 5, 100, 100),
            pymupdf.Rect(80, 65, 155, 140),
            pymupdf.Rect(-20, -10, 40, 40),
            pymupdf.Rect(240, 160, 310, 230),
        ]
        matrix = pymupdf.Matrix(3.125, 3.125)
        clips = [clip * page.rotation_matrix for clip in clips]
        attendus = [page.get_pixmap(matrix=matrix, clip=clip) for clip in clips]
        original = pymupdf.Page.get_displaylist
        appels = []

        def compter(page, *args, **kwargs):
            appels.append((page.number, kwargs))
            return original(page, *args, **kwargs)

        monkeypatch.setattr(pymupdf.Page, "get_displaylist", compter)
        cache = {}
        for clip, attendu in zip(clips, attendus, strict=True):
            # PagesFeuilles recharge lui aussi l'objet Page à chaque vignette.
            obtenu = _pixmap_cache(document[0], cache, matrix=matrix, clip=clip)
            assert (obtenu.irect, obtenu.n, obtenu.alpha) == (
                attendu.irect, attendu.n, attendu.alpha,
            )
            assert obtenu.samples == attendu.samples
        assert appels == [(0, {"annots": True})]


def test_cache_distingue_documents_et_pages():
    with pymupdf.open() as premier, pymupdf.open() as second:
        for document, couleurs in (
            (premier, [(1, 0, 0), (0, 1, 0)]),
            (second, [(0, 0, 1)]),
        ):
            for couleur in couleurs:
                page = document.new_page(width=80, height=80)
                page.draw_rect((0, 0, 80, 80), color=couleur, fill=couleur)
        cache = {}
        pixels = []
        for document, numero in ((premier, 0), (premier, 1), (second, 0)):
            page = document[numero]
            matrix = pymupdf.Matrix(2, 2)
            clip = pymupdf.Rect(10, 10, 40, 40)
            attendu = page.get_pixmap(matrix=matrix, clip=clip)
            obtenu = _pixmap_cache(page, cache, matrix=matrix, clip=clip)
            assert obtenu.samples == attendu.samples
            pixels.append(obtenu.samples)
        assert len(cache) == 3
        assert len(set(pixels)) == 3


def test_planches_et_index_identiques_avec_cache(tmp_path, monkeypatch):
    source = tmp_path / "source.pdf"
    with pymupdf.open() as document:
        page = document.new_page(width=200, height=160)
        page.draw_circle((60, 70), 8)
        page.draw_rect((110, 64, 126, 76))
        document.save(source)
    travail = tmp_path / "travail"
    (travail / "blocs").mkdir(parents=True)
    (travail / "feuilles.csv").write_text(
        "feuille,fichier,page,role\nE1,source.pdf,1,plan\n", encoding="utf-8",
    )
    signatures = [json.dumps([forme, 1, lettre]) for forme, lettre in (
        ("cercle", "A"), ("rectangle", "B"),
    )]
    (travail / "blocs-signatures.json").write_text(json.dumps({
        signature: {"par_feuille": {"E1": 1}, "legende": {"description": "Appareil"}}
        for signature in signatures
    }), encoding="utf-8")
    with (travail / "blocs" / "E1.csv").open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=[
            "signature", "feuille", "x_pt", "y_pt", "diametre_pt", "w_pt", "h_pt",
        ])
        writer.writeheader()
        for signature, x in zip(signatures, (60, 118), strict=True):
            writer.writerow({
                "signature": signature, "feuille": "E1", "x_pt": x, "y_pt": 70,
                "diametre_pt": 16, "w_pt": 16, "h_pt": 16,
            })
    original = pymupdf.Page.get_displaylist
    appels = []

    def compter(page, *args, **kwargs):
        appels.append(page.number)
        return original(page, *args, **kwargs)

    monkeypatch.setattr(pymupdf.Page, "get_displaylist", compter)
    index_cache = ids_cache = b""
    for mode in ("cache", "direct"):
        if mode == "direct":
            monkeypatch.setattr(
                blocs_vignettes, "_pixmap_cache",
                lambda page, cache, **options: page.get_pixmap(**options),
            )
        sortie = tmp_path / mode
        monkeypatch.setattr(sys, "argv", [
            "blocs_vignettes", str(travail), str(source), str(sortie),
            "--min", "1", "--par-planche", "1",
        ])
        blocs_vignettes.main()
        if mode == "cache":
            assert appels == [0]
            index_cache = (travail / "blocs-index.csv").read_bytes()
            ids_cache = (travail / "blocs-ids.json").read_bytes()
        else:
            assert appels == [0, 0, 0]
            assert (travail / "blocs-index.csv").read_bytes() == index_cache
            assert (travail / "blocs-ids.json").read_bytes() == ids_cache
    for numero in (1, 2):
        nom = f"signatures-{numero:02d}.png"
        assert (tmp_path / "cache" / nom).read_bytes() == (tmp_path / "direct" / nom).read_bytes()
