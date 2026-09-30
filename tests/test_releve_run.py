"""Fresh agent evidence and all-or-rollback publication, with no provider calls."""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('releve_run_transaction', Path(__file__).resolve().parents[1] / 'releve/run.py')
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


@pytest.mark.parametrize('provider', ['nvidia', 'sdk'])
@pytest.mark.parametrize('fresh', [None, '{}', '[]', 'null', '{broken', '{"is_error":false}',
                                   '{"is_error":false,"subtype":"success"}'])
def test_agent_requires_a_new_valid_result(tmp_path, monkeypatch, provider, fresh):
    result = tmp_path / 'agent-resultat.json'
    result.write_text('{"is_error":false,"subtype":"success","result":"STALE"}', encoding='utf-8')
    removed_before_dispatch = []

    def invoke(*args, **kwargs):
        removed_before_dispatch.append(not result.exists())
        if fresh is not None:
            result.write_text(fresh, encoding='utf-8')
        return 0, ''

    monkeypatch.setenv('RELEVE_AGENT', provider)
    monkeypatch.setattr(launcher, 'run', invoke)
    monkeypatch.setattr(launcher, 'log', lambda *_: None)
    _, report, _ = launcher.agent(str(tmp_path), str(tmp_path / 'log'))
    assert removed_before_dispatch == [True]
    assert report['is_error'] is (fresh != '{"is_error":false,"subtype":"success"}')
    assert report.get('result') != 'STALE'


@pytest.mark.parametrize('output', ['[null]', '[1,[]]', 'null', '"text"',
    '[null,{"type":"result","is_error":false,"subtype":"success"}]'])
def test_cli_malformed_shapes_fail_closed_without_attribute_crash(tmp_path, monkeypatch, output):
    monkeypatch.setenv('RELEVE_AGENT', 'cli')
    monkeypatch.setattr(launcher, 'run', lambda *args, **kwargs: (0, output))
    monkeypatch.setattr(launcher, 'log', lambda *_: None)
    _, report, _ = launcher.agent(str(tmp_path), str(tmp_path / 'log'))
    assert report['is_error'] is ('success' not in output)


@pytest.mark.parametrize('old_exists', [True, False])
@pytest.mark.parametrize('nested_exists', [True, False])
@pytest.mark.parametrize('failure', ['copy', 'replace', None])
def test_publication_preserves_previous_set_on_later_failure(tmp_path, monkeypatch, old_exists, nested_exists, failure):
    outbox = tmp_path / 'out'
    public = outbox / 'demo'
    public.mkdir(parents=True)
    relatives = ['a.pdf', 'new/b.pdf', 'z.pdf']
    if old_exists:
        for name in ('a.pdf', 'z.pdf'):
            (public / name).write_bytes(('old-' + name).encode())
    if nested_exists:
        (public / 'new').mkdir()
        (public / 'new/b.pdf').write_bytes(b'old-nested-pdf')
    baseline = {p.relative_to(public).as_posix(): p.read_bytes() for p in public.rglob('*') if p.is_file()}
    statuses = []

    def stage(cmd, **kwargs):
        if 'releve/render_pdf.py' in cmd:
            generation = Path(cmd[-1])
            for relative in relatives:
                path = generation / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(('new-' + relative).encode())
        return 0, ''

    original_copy, original_replace = launcher.shutil.copy2, launcher.os.replace
    injected = []

    def copy(src, dst, *args, **kwargs):
        if failure == 'copy' and Path(src).name == 'z.pdf' and Path(src).read_bytes() == b'new-z.pdf':
            Path(dst).write_bytes(b'partial')
            injected.append(True)
            raise OSError('injected later copy failure')
        return original_copy(src, dst, *args, **kwargs)

    def replace(src, dst):
        if failure == 'replace' and Path(dst) == public / 'z.pdf' and not injected:
            injected.append(True)
            raise OSError('injected later replace failure')
        return original_replace(src, dst)

    monkeypatch.setenv('RELEVE_NATIF', '0')
    monkeypatch.setattr(launcher, 'OUTBOX', str(outbox))
    monkeypatch.setattr(launcher, 'resolve_inbox', lambda _: ('demo', str(tmp_path / 'input')))
    monkeypatch.setattr(launcher, 'run', stage)
    monkeypatch.setattr(launcher, 'current_outputs', lambda *args: relatives)
    monkeypatch.setattr(launcher, 'drive_mounted', lambda: False)
    monkeypatch.setattr(launcher, 'log', lambda *_: None)
    monkeypatch.setattr(launcher, 'statut', lambda *args, **kwargs: statuses.append(args[6]))
    monkeypatch.setattr(launcher.shutil, 'copy2', copy)
    monkeypatch.setattr(launcher.os, 'replace', replace)
    ok = launcher.process('demo', reprendre=True)
    assert ok is (failure is None)
    actual = {relative: (public / relative).read_bytes() for relative in relatives if (public / relative).is_file()}
    if failure:
        assert injected
        assert actual == baseline
        assert statuses == [False]
        assert (public / 'new').exists() is nested_exists, 'Rollback must preserve old directories and remove new ones'
    else:
        assert actual == {relative: ('new-' + relative).encode() for relative in relatives}
        assert statuses == [True]
    assert not list(public.glob('.publication-*')), 'Completed staging/rollback must clean its transaction'
