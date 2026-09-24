"""Review finding 22: an addendum filed in Drive must be ingested by the takeoff or explicitly declared."""
from __future__ import annotations

import json

from conftest import ROOT
from src.validation import addenda

S1835_INVENTORY = ROOT / "docs" / "inventaire-drive-2026-09-23" / "dossiers" / "s-1835 esbg  rehabilitation inbterieur.json"
S1835_STATUS = ROOT / "dossiers" / "S-1835" / "STATUT.md"

STATUS = """# STATUT

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| X - Addenda - E-01.pdf | 100 | aa |

## Addendas non intégrés

- `X - Addenda - ADM-01.pdf` — administrative addendum, no drawing
- `Y - Addenda - Z.pdf`
"""


def _inventory(*files):
    return {"fichiers": [{"chemin": c, "octets": o} for c, o in files]}


def test_ingested_by_size_despite_copy_suffix():
    inv = _inventory(("X - Addenda - E-01 (2).pdf", 100))
    assert addenda.missing_addenda(inv, STATUS) == []


def test_missing_addendum_is_reported():
    inv = _inventory(("X - Addenda - T-01 (2).pdf", 200), ("plans.pdf", 300))
    assert addenda.missing_addenda(inv, STATUS) == ["X - Addenda - T-01 (2).pdf"]


def test_declaration_needs_a_reason_and_matches_copy_suffix():
    inv = _inventory(("X - Addenda - ADM-01 (1).pdf", 5), ("Y - Addenda - Z.pdf", 6))
    assert addenda.missing_addenda(inv, STATUS) == ["Y - Addenda - Z.pdf"]


def test_undetailed_addenda_folder_must_be_declared():
    inv = _inventory(("Addenda/ (sous-dossier non détaillé)", 0))
    assert addenda.missing_addenda(inv, STATUS) == ["Addenda/"]
    declared = STATUS + "- `Addenda/` — sub-folder not listed by the inventory\n"
    assert addenda.missing_addenda(inv, declared) == []


def test_s1835_every_drive_addendum_is_ingested_or_declared():
    inv = json.loads(S1835_INVENTORY.read_text(encoding="utf-8"))
    assert addenda.missing_addenda(inv, S1835_STATUS.read_text(encoding="utf-8")) == []


def test_s1835_telecom_addendum_t01_is_an_input():
    """T-01 is two documents (text + plans). Drive holds several copies of each ("(1)", "(2)", Addenda/ sub-folder);
    identical copies have the same byte size (and the same extracted text, checked through the Drive connector),
    so they collapse to one document per size. Both documents must be takeoff inputs."""
    sizes = addenda.status_input_sizes(S1835_STATUS.read_text(encoding="utf-8"))
    inv = json.loads(S1835_INVENTORY.read_text(encoding="utf-8"))
    t01 = [a for a in addenda.inventory_addenda(inv) if "T-01" in a["name"]]
    documents = {a["size"] for a in t01}
    assert len(documents) == 2
    assert documents <= sizes
