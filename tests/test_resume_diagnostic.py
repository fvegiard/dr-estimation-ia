"""A damaged historical diagnostic must not break resume finalization."""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('resume_diagnostic', Path(__file__).resolve().parents[1] / 'releve/run.py')
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


@pytest.mark.parametrize('content', ['{broken', 'null', '[]', '42', '"text"', b'\xff', '{"result":"prior diagnostic"}'])
@pytest.mark.parametrize('qa_ok', [True, False])
def test_resume_handles_unusable_historical_diagnostic(tmp_path, monkeypatch, content, qa_ok):
    public = tmp_path / 'out/demo'
    work = public / 'travail'
    work.mkdir(parents=True)
    diagnostic = work / 'agent-resultat.json'
    diagnostic.write_bytes(content if isinstance(content, bytes) else content.encode())
    original = diagnostic.read_bytes()
    monkeypatch.setenv('RELEVE_NATIF', '0')
    monkeypatch.setattr(launcher, 'OUTBOX', str(public.parent))
    monkeypatch.setattr(launcher, 'resolve_inbox', lambda _: ('demo', str(tmp_path / 'input')))
    monkeypatch.setattr(launcher, 'drive_mounted', lambda: False)
    monkeypatch.setattr(launcher, 'log', lambda *_: None)
    monkeypatch.setattr(launcher, 'current_outputs', lambda *args: ['a.pdf'])

    def stage(cmd, **kwargs):
        if 'releve/controle_qualite.py' in cmd and not qa_ok:
            return 1, ''
        if 'releve/render_pdf.py' in cmd:
            (Path(cmd[-1]) / 'a.pdf').write_bytes(b'new artifact')
        return 0, ''

    monkeypatch.setattr(launcher, 'run', stage)
    assert launcher.process('demo', reprendre=True) is qa_ok
    assert not (public / '.en-cours').exists()
    status = (public / 'STATUT.md').read_text(encoding='utf-8')
    assert ('TERMINÉ' in status) is qa_ok
    assert (public / 'a.pdf').exists() is qa_ok
    assert diagnostic.read_bytes() == original
