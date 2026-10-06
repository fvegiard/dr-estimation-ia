from __future__ import annotations

from conftest import ROOT
from outils import score_gold as SG


def test_pages_gold_lit_le_tableau_de_la_spec():
    pages = SG.pages_gold(str(ROOT / "docs" / "FORMAT-EXEMPLE.md"))
    assert pages["E08"] == 62 and pages["E09"] == 64 and pages["DSI01"] == 1 and pages["EU04"] == 86
    assert len(pages) == 26


def test_noter_feuille_famille_exacte_et_bon_code_au_bon_endroit():
    # given : 3 repères au gold, l'IA en place 3 dont un avec le mauvais code
    gold = [("CH", 100.0, 100.0), ("T", 200.0, 200.0), ("T", 300.0, 300.0)]
    ia = [("CH", 101.0, 100.0), ("T", 200.0, 202.0), ("CH", 300.0, 300.0)]
    # when
    r = SG.noter_feuille(gold, ia, {"CH": 1, "T": 2}, {"CH": 2, "T": 1})
    # then : tout est trouvé au bon endroit, mais 1 seul repère sur 3 n'a pas le bon code ; aucune famille exacte
    assert r["rappel"] == 100.0 and r["precision"] == 100.0
    assert r["rappel_meme_famille"] == 66.7
    assert r["familles_exactes"] == 0 and r["ecarts_legende"] == {"CH": [1, 2], "T": [2, 1]}


def test_noter_feuille_non_relevee_vaut_zero():
    r = SG.noter_feuille([("PC", 1.0, 1.0)], [], {"PC": 1}, {})
    assert r["rappel"] == 0.0 and r["reperes_ia"] == 0 and r["familles_exactes"] == 0
