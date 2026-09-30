"""Regression checks for fractional coverage, zero coordinates and contextual IDs."""
import json

import pytest

from test_agent_nvidia import an, _work, _tool_reply
from test_controle_qualite import cq, dossier


def test_coverage_tool_preserves_fractional_page_edge(tmp_path):
    work = _work(tmp_path)
    (tmp_path / 'feuilles.csv').write_text('feuille,largeur_pt,hauteur_pt\nP1,600.5,600\n', encoding='utf-8')
    text, _ = an.outil(work, 'couverture', {})
    assert json.loads(text)['P1'][-1][-2] == 600.5


def test_finish_refusal_returns_exact_coverage_bounds(tmp_path, monkeypatch):
    work = _work(tmp_path)
    (tmp_path / 'feuilles.csv').write_text('feuille,largeur_pt,hauteur_pt\nP1,600.5,600\n', encoding='utf-8')
    monkeypatch.setenv('NVIDIA_API_KEY', 'test-only')
    requests = []
    def reply(body, *_args, **_kwargs):
        requests.append(json.loads(json.dumps(body)))
        return _tool_reply('terminer', {'resume': 'done'})
    monkeypatch.setattr(an, 'appel', reply)
    assert an.run(work, str(tmp_path / 'result.json'), 'test/model', 2) == 1
    text = next(m['content'] for m in requests[1]['messages'] if m['role'] == 'tool')
    assert json.loads(text[text.index('{'):])['P1'][-1][-2] == 600.5


@pytest.mark.parametrize('row,expected', [
    ({'x_pt': 0, 'y_pt': 0}, (0, 0)),
    ({'x_pt': 0, 'y_pt': 4, 'x': 99, 'y': 88}, (0, 4)),
    ({'x_pt': 4, 'y_pt': 0, 'x': 99, 'y': 88}, (4, 0)),
    ({'x_pt': '', 'y_pt': None, 'x': 2, 'y': 3}, (2, 3)),
    ({'x': 2, 'y': 3}, (2, 3)),
])
def test_coordinates_preserve_zero_and_legacy_fallback(row, expected):
    assert cq.coordonnees(row) == expected


@pytest.mark.parametrize('explicit,note', [('', '[DT1.1] reference contextuelle'),
                                           ('K1.1', '[DT1.1] reference contextuelle'),
                                           (None, 'pres de DT1.1')])
def test_reference_comparison_uses_own_id_not_context(tmp_path, explicit, note):
    header = 'feuille,label,x_pt,y_pt,source,note'
    row = f'P1,KLAXON,12.3,24.6,visuel,{note}'
    if explicit is not None:
        header += ',repere'
        row += ',' + explicit
    work = dossier(tmp_path, occ=header + '\n' + row + '\n', reserves='DETECTEUR THERMIQUE absent')
    ref = tmp_path / 'reference.csv'
    ref.write_text('feuille,designation,qte\nP1,K,1\nP1,DT,0\n', encoding='utf-8')
    result = cq.controler(work, str(ref), 'P1', 'P1')
    assert result['conforme'], result['erreurs']
    assert result['comparaison_reference']['K']['ia'] == 1


def test_invalid_own_id_stays_blocking_with_reference(tmp_path):
    work = dossier(tmp_path, occ='feuille,label,x_pt,y_pt,source,note,repere\nP1,KLAXON,12.3,24.6,visuel,,invalid\n',
                   reserves='DETECTEUR THERMIQUE absent')
    ref = tmp_path / 'reference.csv'
    ref.write_text('feuille,designation,qte\nP1,K,1\n', encoding='utf-8')
    result = cq.controler(work, str(ref), 'P1', 'P1')
    assert not result['conforme']
    assert any(e.startswith('Q4') for e in result['erreurs'])
