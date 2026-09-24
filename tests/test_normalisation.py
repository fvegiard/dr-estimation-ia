"""Tests for src/qpl/normalisation.py (canonical labels learnt from the 2021-2026 corpus)."""
import json

from src.qpl.normalisation import NORMALISATION_JSON, Normaliseur, canonique, nettoyer
from src.validation import compare_qpl as cq


def test_nettoyer_case_accents_spaces():
    assert nettoyer("  Détecteur   fumée ") == "DETECTEUR FUMEE"
    assert nettoyer("") == ""


def test_fusion_simple_and_case_insensitive():
    n = Normaliseur({"PRISE GFI": "PRISE"}, [])
    assert n.canonique("prise  gfi") == "PRISE"
    assert n.canonique("PRISE") == "PRISE"
    assert n.canonique("Inconnu") == "INCONNU"


def test_fusion_transitive_and_cycle_safe():
    assert Normaliseur({"A": "B", "B": "C"}, []).canonique("a") == "C"
    assert Normaliseur({"A": "B", "B": "A"}, []).canonique("A") in {"A", "B"}


def test_rebut_returns_none():
    n = Normaliseur({"X": "COMPTEUR 1"}, ["Compteur 1", "6"])
    assert n.canonique("COMPTEUR 1") is None
    assert n.canonique("6") is None
    assert n.canonique("x") is None          # fused into noise
    assert n.canonique("   ") is None
    assert n.est_rebut("6")


def test_real_file_every_variant_resolves():
    d = json.loads(NORMALISATION_JSON.read_text(encoding="utf-8"))
    assert canonique("PRISE GFI") == "PRISE"
    for r in d["rebut"]:
        assert canonique(r) is None
    for variante in d["fusion"]:
        k = canonique(variante)
        assert k is None or k not in d["fusion"]   # fully resolved


def _plan(labels):
    return cq.Plan(nom="p", fichier="", lignes=[],
                   marques=[cq.Marque(str(i), "ia", "p", l, 0.0, 0.0) for i, l in enumerate(labels)])


def test_filtrer_rebut_in_place():
    p = _plan(["PRISE", "COMPTEUR 3", "6"])
    assert cq.filtrer_rebut([p], canonique) == 2
    assert [m.libelle for m in p.marques] == ["PRISE"]
