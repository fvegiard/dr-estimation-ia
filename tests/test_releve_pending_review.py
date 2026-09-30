import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('isolated_launcher', Path(__file__).resolve().parents[1] / 'releve/run.py')
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


@pytest.mark.parametrize('current', ['non — current native failure', 'oui', None])
@pytest.mark.parametrize('old_manifest', ['{"ok":true}', '{stale broken JSON'])
def test_native_status_uses_current_steps_only(tmp_path, current, old_manifest):
    out = tmp_path / 'out'
    (out / 'export-natif-planexpert').mkdir(parents=True)
    (out / 'export-natif-planexpert/resultat.json').write_text(old_manifest, encoding='utf-8')
    steps = [('export natif Plan Expert', 1, current)] if current else []
    launcher.statut('demo', str(tmp_path / 'in'), str(out), str(tmp_path / 'work'), steps, None, True, outputs=[])
    text = (out / 'STATUT.md').read_text(encoding='utf-8')
    native = [line for line in text.splitlines() if line.startswith('**Export natif')][0]
    assert (': oui**' in native) is (current == 'oui')
    if current and current.startswith('non'):
        assert 'current native failure' in text


@pytest.mark.parametrize('failure', [None, 'render', 'publication', 'native'])
def test_only_new_successful_generation_is_removed(tmp_path, monkeypatch, failure):
    outbox = tmp_path / 'out'
    public = outbox / 'demo'
    old = public / '.generation-previous'
    old.mkdir(parents=True)
    (old / 'evidence.txt').write_text('preserve previous failure')
    work = public / 'travail'
    work.mkdir()
    (work / 'evidence.txt').write_text('preserve work')
    generations = []

    def run(cmd, **kwargs):
        if '--cli' in cmd:
            return 1, '{"ok":false,"erreur":"current native failure"}'
        if 'releve/render_pdf.py' in cmd:
            generation = Path(cmd[-1])
            generations.append(generation)
            (generation / 'evidence.txt').write_text('current evidence')
            if failure == 'render':
                return 1, ''
        return 0, ''

    def publish(*args):
        if failure == 'publication':
            raise OSError('publication failed')

    monkeypatch.setenv('RELEVE_NATIF', '1' if failure == 'native' else '0')
    fake_cli = tmp_path / 'native.py'
    fake_cli.write_text('# mocked only')
    monkeypatch.setattr(launcher, 'PLANEXPERT_VM_CLI', str(fake_cli))
    monkeypatch.setattr(launcher, 'OUTBOX', str(outbox))
    monkeypatch.setattr(launcher, 'resolve_inbox', lambda _: ('demo', str(tmp_path / 'in')))
    monkeypatch.setattr(launcher, 'run', run)
    monkeypatch.setattr(launcher, 'current_outputs', lambda *_: [])
    monkeypatch.setattr(launcher, 'publish_outputs', publish)
    monkeypatch.setattr(launcher, 'statut', lambda *args, **kwargs: None)
    monkeypatch.setattr(launcher, 'drive_mounted', lambda: False)
    monkeypatch.setattr(launcher, 'log', lambda *_: None)
    assert launcher.process('demo', reprendre=True) is (failure in (None, 'native'))
    assert (old / 'evidence.txt').read_text() == 'preserve previous failure'
    assert (work / 'evidence.txt').read_text() == 'preserve work'
    assert len(generations) == 1
    assert generations[0].exists() is (failure is not None)
    if failure:
        assert (generations[0] / 'evidence.txt').read_text() == 'current evidence'


@pytest.mark.parametrize('target', ['root', 'work', 'outside'])
def test_cleanup_refuses_non_generation_or_unconfined_paths(tmp_path, target):
    public = tmp_path / 'out'
    public.mkdir()
    path = {'root': public, 'work': public / 'travail', 'outside': tmp_path / '.generation-other'}[target]
    path.mkdir(exist_ok=True)
    (path / 'keep.txt').write_text('keep')
    with pytest.raises(ValueError):
        launcher.cleanup_generation(str(path), str(public))
    assert (path / 'keep.txt').read_text() == 'keep'
