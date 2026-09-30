"""Whole reserve identifiers and standard-library-only quality checks."""
import subprocess
import sys
from pathlib import Path

import pytest

from test_controle_qualite import OCC, cq, dossier
from test_releve_source_identifiers import document, fixture


@pytest.mark.parametrize('reserve', ['K1.20 absent', 'AK1.2 absent', 'K1.2A absent', 'K1.2_3 absent', 'K1.2.1 absent'])
def test_q6_different_identifier_cannot_excuse_gap(tmp_path, reserve):
    result = cq.controler(dossier(tmp_path, occ=OCC.replace('[K1.2]', '[K1.3]'), reserves=reserve))
    assert any(error.startswith('Q6') and 'K1.2' in error for error in result['erreurs'])


@pytest.mark.parametrize('reserve', ['[K1.2]: absent', 'K1.2, absent', 'K1.2; absent', 'Absent: K1.2.'])
def test_q6_whole_identifier_in_prose_excuses_gap(tmp_path, reserve):
    result = cq.controler(dossier(tmp_path, occ=OCC.replace('[K1.2]', '[K1.3]'), reserves=reserve))
    assert result['conforme'], result['erreurs']


def run_without_site_packages(work):
    script = Path(__file__).resolve().parents[1] / 'releve/controle_qualite.py'
    return subprocess.run([sys.executable, '-S', str(script), str(work)], capture_output=True, text=True)


def test_quality_without_image_evidence_works_without_pillow(tmp_path):
    dossier(tmp_path)
    result = run_without_site_packages(tmp_path)
    assert result.returncode == 0, result.stderr


def test_image_evidence_without_pillow_fails_closed_with_quality_report(tmp_path):
    _, entry = fixture(tmp_path)
    document(tmp_path, entry)
    result = run_without_site_packages(tmp_path)
    assert result.returncode == 2, result.stderr
    assert 'Q5' in result.stdout and 'Pillow' in result.stdout
    assert (tmp_path / 'qualite.json').is_file()
