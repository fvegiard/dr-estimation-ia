"""dossiers/S-1835/preuves-t01/publier_t01.py — isolated unit test for a_verifier_de().

This script rebuilds one specific historical dossier (S-1835) from real Drive/git-revision fixtures
that aren't available here, so main() itself isn't unit-tested. a_verifier_de() is a small, pure,
isolated function (reads a JSON report from a directory) and is testable on its own: it's the piece
that was missing before this fix, letting the script publish an unqualified "TERMINÉ" even when
render_vectoriel.py's own report said the RELEVE-MATERIEL box overlapped the drawing.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "publier_t01", ROOT / "dossiers" / "S-1835" / "preuves-t01" / "publier_t01.py")
publier_t01 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(publier_t01)


def test_a_verifier_de_reads_overlap_list(tmp_path):
    (tmp_path / "S-1835-rendu-rapport.json").write_text(
        json.dumps({"conformite": {"encadre_hors_espace_libre": ["E204"]}}), encoding="utf-8")
    assert publier_t01.a_verifier_de(str(tmp_path), "S-1835") == ["E204"]


def test_a_verifier_de_empty_when_report_clean(tmp_path):
    (tmp_path / "S-1835-rendu-rapport.json").write_text(
        json.dumps({"conformite": {"encadre_hors_espace_libre": []}}), encoding="utf-8")
    assert publier_t01.a_verifier_de(str(tmp_path), "S-1835") == []


def test_a_verifier_de_empty_when_report_absent(tmp_path):
    assert publier_t01.a_verifier_de(str(tmp_path), "S-1835") == []


def test_main_wires_a_verifier_into_statut_call():
    """main() itself isn't unit-tested (needs real S-1835 Drive/git fixtures), but the wiring that
    was missing — reading a_verifier_de() and passing it to runmod.statut() — must stay in place.
    A source check is a deliberately lighter substitute for a full integration test here."""
    import inspect
    src = inspect.getsource(publier_t01.main)
    assert "a_verifier_de(outbox, S)" in src
    assert "runmod.statut(S, inbox, outbox, work, steps, None, True, None, a_verifier)" in src
