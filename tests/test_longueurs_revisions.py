"""Contrats du métré sur la source et de sélection de révisions."""
import json
from pathlib import Path
from types import SimpleNamespace

import pymupdf
import pytest

from releve import prepare  # initialise les chemins des scripts releve/
from releve import longueurs, revisions


def trace_rectangulaire():
    a, b, c, d = [pymupdf.Point(x, y) for x, y in ((10, 10), (110, 10), (110, 14), (10, 14))]
    return {"seqno": 3, "fill": (0, 0, 0), "rect": pymupdf.Rect(a, c), "items": [
        ("l", a, b), ("l", b, c), ("l", c, a), ("l", a, c), ("l", c, d), ("l", d, a)]}


def profil_traces(points):
    return {"feuille": "E400", "page": 1, "texte_echelle": "1:100", "zone_echelle": [0, 0, 40, 10],
            "echelle": 100, "traces": [[3, "EMT", points]], "specifications": {"EMT": "témoin"}}


def test_metre_ne_mesure_que_le_trace_sourcé():
    page = SimpleNamespace(rotation=0, get_text=lambda **k: "Échelle 1:100",
                           get_drawings=lambda: [trace_rectangulaire()])
    p = profil_traces([[11, 12], [109, 12]])
    [r] = longueurs.calculer(p, page, {"page": 1, "fichier": "plans.pdf"})
    assert r["longueur_m"] == pytest.approx(98 * 100 * .0254 / 72, abs=1e-6)
    assert r["statut"] == "horizontal tracé seulement" and "p.1" in r["source"]
    with pytest.raises(ValueError, match="hors|en dehors"):
        longueurs.calculer(profil_traces([[11, 8], [109, 8]]), page, {"page": 1, "fichier": "plans.pdf"})
    page.get_text = lambda **k: "échelle absente"
    with pytest.raises(ValueError, match="échelle introuvable"):
        longueurs.calculer(p, page, {"page": 1, "fichier": "plans.pdf"})


def test_pas_de_longueur_zero_sans_source(tmp_path):
    r = longueurs.produire(tmp_path, {}, tmp_path)
    assert not r["complet"] and r["reserves"] and r["lignes"] == []
    assert (tmp_path / "metre-longueurs.csv").read_text().count("\n") == 1


def test_jeu_s1715_12_feuilles_actives_et_9_remplacees():
    p = Path(prepare.__file__).with_name("profils_revisions") / "s1715-feuilles.json"
    regles = json.loads(p.read_text(encoding="utf-8"))["documents"]
    inv = {}
    for i, (h, r) in enumerate(regles.items()):
        inv[f"doc-{i}.pdf"] = {"sha256": h, "pages": len(r["actives"]) + len(r["remplacees"]),
                               "classement": "plans" if i == 0 else "addenda"}
    selection = revisions.selection(inv)
    assert sum(map(len, selection["actives"].values())) == 12
    assert sum(map(len, selection["remplacees"].values())) == 9
    assert selection["actives"]["doc-2.pdf"]["5"] == "E201"
    with pytest.raises(ValueError, match="jeu de révisions vérifié"):
        revisions.selection({nom: e for nom, e in inv.items() if nom != "doc-2.pdf"})