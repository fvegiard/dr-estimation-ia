"""Tests for src/qpl/categorie.py (rule-based, keyword-driven categoriser)."""
from __future__ import annotations

from src.qpl.categorie import CATEGORIES, INDETERMINE, categoriser, nettoyer


def test_nettoyer_case_accents_ponctuation():
    assert nettoyer("  Détecteur - fumée ") == "DETECTEUR FUMEE"
    assert nettoyer("A/C UNIT") == "A C UNIT"
    assert nettoyer("") == ""


def test_ai_descriptive_labels():
    assert categoriser("Prise double 5-15R").categorie == "dispositif"
    assert categoriser("A1 Troffer 2x4").categorie == "luminaire"
    assert categoriser("Détecteur de fumée mur").categorie == "securite_incendie"


def test_human_short_codes_with_prefixes():
    assert categoriser("ADD PRISE").categorie == "dispositif"
    assert categoriser("ADD FIXTURE TYPE A1").categorie == "luminaire"
    assert categoriser("D PRISE").categorie == "dispositif"      # dictionary prefix
    assert categoriser("B INT").categorie == "dispositif"


def test_demolition_flag_ai_and_human_wording():
    assert categoriser("Démo luminaire R").demolition is True
    assert categoriser("FIXTURE ENLEVER").demolition is True
    assert categoriser("FIXT ENL").demolition is True
    assert categoriser("PRISE").demolition is False


def test_relocation_flag():
    assert categoriser("RELO PRISE").relocation is True
    assert categoriser("EXIT RELO").relocation is True
    assert categoriser("HP RELO").relocation is True
    assert categoriser("PRISE").relocation is False


def test_demolition_and_category_are_independent():
    c = categoriser("FIXTURE ENLEVER")
    assert c.categorie == "luminaire"
    assert c.demolition is True
    assert c.relocation is False


def test_case_and_language_insensitive_same_category():
    a = categoriser("prise gfi")
    b = categoriser("PRISE GFI 15/20")
    assert a.categorie == b.categorie == "dispositif"


def test_telecom_securite_distribution_mecanique_chauffage():
    assert categoriser("TEL").categorie == "telecom_donnees"
    assert categoriser("Speaker outlet").categorie == "telecom_donnees"
    assert categoriser("DETECTEUR FUMEE").categorie == "securite_incendie"
    assert categoriser("Smoke detector ceiling").categorie == "securite_incendie"
    assert categoriser("PANN").categorie == "distribution"
    assert categoriser("Electrical panel 200A").categorie == "distribution"
    assert categoriser("MOTEUR").categorie == "mecanique_moteur"
    assert categoriser("Exhaust fan motor").categorie == "mecanique_moteur"
    assert categoriser("TH").categorie == "chauffage"
    assert categoriser("Baseboard heater 1000W").categorie == "chauffage"


def test_unknown_label_is_indetermine_not_a_crash():
    c = categoriser("XYZ12-QQQ")
    assert c.categorie == INDETERMINE
    assert c.categorie not in CATEGORIES
    assert c.demolition is False and c.relocation is False


def test_empty_label():
    c = categoriser("")
    assert c.categorie == INDETERMINE


def test_every_dictionary_category_is_reachable_by_its_own_label():
    import json

    from src.qpl.categorie import DICTIONNAIRE_JSON

    d = json.loads(DICTIONNAIRE_JSON.read_text(encoding="utf-8"))
    manques = []
    for entree in d["symboles"]:
        if entree["categorie"] == INDETERMINE:
            continue
        obtenu = categoriser(entree["label"]).categorie
        if obtenu != entree["categorie"]:
            manques.append((entree["label"], entree["categorie"], obtenu))
    # A handful of genuinely ambiguous single labels (e.g. shared by two
    # categories, like EXIT) is expected; most must resolve correctly.
    assert len(manques) / len(d["symboles"]) < 0.1, manques[:20]
