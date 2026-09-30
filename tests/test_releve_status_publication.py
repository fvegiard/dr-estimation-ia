from pathlib import Path

import pytest

from releve import run


@pytest.fixture
def publication(monkeypatch, tmp_path):
    out = tmp_path / "out" / "demo"
    (out / "travail").mkdir(parents=True)
    (out / "result.pdf").write_bytes(b"old output")
    (out / "STATUT.md").write_bytes(b"old accepted status")
    drive = tmp_path / "drive"
    mirror = drive / "OUTBOX/demo"
    mirror.mkdir(parents=True)
    (mirror / "STATUT.md").write_bytes(b"old mirrored status")
    def stage(cmd, **kwargs):
        if "releve/render_pdf.py" in cmd:
            (Path(cmd[-1]) / "result.pdf").write_bytes(b"new output")
        return 0, ""
    monkeypatch.setattr(run, "OUTBOX", str(out.parent))
    monkeypatch.setattr(run, "DRIVE", str(drive))
    monkeypatch.setattr(run, "resolve_inbox", lambda arg: ("demo", str(tmp_path / "input")))
    monkeypatch.setattr(run, "current_outputs", lambda *args: ["result.pdf"])
    monkeypatch.setattr(run, "run", stage)
    monkeypatch.setattr(run, "drive_mounted", lambda: True)
    monkeypatch.setattr(run, "log", lambda *args: None)
    monkeypatch.setenv("RELEVE_NATIF", "0")
    return out, mirror


@pytest.mark.parametrize("error", [RuntimeError("template failed"), OSError("status write failed")])
def test_status_preparation_failure_preserves_previous_bundle(publication, monkeypatch, error):
    out, mirror = publication
    def fail_status(*args, **kwargs):
        raise error
    monkeypatch.setattr(run, "statut", fail_status)
    assert not run.process("demo", reprendre=True)
    assert (out / "result.pdf").read_bytes() == b"old output"
    assert (out / "STATUT.md").read_bytes() == b"old accepted status"
    assert (mirror / "STATUT.md").read_bytes() == b"old mirrored status"
    assert not (out / ".en-cours").exists()


def test_status_promotion_failure_rolls_back_outputs(publication, monkeypatch):
    out, mirror = publication
    original = run.os.replace
    failed = []
    def replace(src, dst):
        if ".publication-" in str(src) and str(src).split("new-")[-1].isdigit() and Path(dst) == out / "STATUT.md":
            failed.append(True)
            raise OSError("status promotion failed")
        return original(src, dst)
    monkeypatch.setattr(run.os, "replace", replace)
    assert not run.process("demo", reprendre=True)
    assert failed
    assert (out / "result.pdf").read_bytes() == b"old output"
    assert (out / "STATUT.md").read_bytes() == b"old accepted status"
    assert (mirror / "STATUT.md").read_bytes() == b"old mirrored status"


def test_success_status_contains_current_hash_but_not_itself(publication):
    out, mirror = publication
    assert run.process("demo", reprendre=True)
    status = (out / "STATUT.md").read_text(encoding="utf-8")
    assert "TERMINÉ" in status
    assert run.sha256(out / "result.pdf") in status
    assert "| STATUT.md |" not in status
    assert (out / "result.pdf").read_bytes() == b"new output"
    assert (mirror / "STATUT.md").read_text(encoding="utf-8") == status
    assert not list(out.glob(".publication-*"))


def test_failure_status_write_error_does_not_publish_old_status_as_current(publication, monkeypatch):
    out, mirror = publication
    monkeypatch.setattr(run, "run", lambda *args, **kwargs: (2, "quality failed"))
    def fail_status(*args, **kwargs):
        raise OSError("failure status unavailable")
    monkeypatch.setattr(run, "statut", fail_status)
    assert not run.process("demo", reprendre=True)
    assert (out / "STATUT.md").read_bytes() == b"old accepted status"
    assert (mirror / "STATUT.md").read_bytes() == b"old mirrored status"


def test_atomic_status_replace_failure_keeps_previous_bytes(tmp_path, monkeypatch):
    status = tmp_path / "STATUT.md"
    status.write_bytes(b"old accepted status")
    def fail_replace(*args):
        raise OSError("replace denied")
    monkeypatch.setattr(run.os, "replace", fail_replace)
    with pytest.raises(OSError, match="replace denied"):
        run.statut("demo", str(tmp_path / "input"), str(tmp_path), str(tmp_path / "work"), [], None, False)
    assert status.read_bytes() == b"old accepted status"
    assert list(tmp_path.iterdir()) == [status]


def test_partial_status_write_does_not_truncate_previous_status(tmp_path, monkeypatch):
    from contextlib import contextmanager
    status = tmp_path / "STATUT.md"
    status.write_bytes(b"old accepted status")
    original = run.tempfile.NamedTemporaryFile
    @contextmanager
    def partial_writer(*args, **kwargs):
        with original(*args, **kwargs) as fh:
            class Writer:
                name = fh.name
                def write(self, text):
                    fh.write(text[:12])
                    raise OSError("disk full during status write")
            yield Writer()
    monkeypatch.setattr(run.tempfile, "NamedTemporaryFile", partial_writer)
    with pytest.raises(OSError, match="disk full"):
        run.statut("demo", str(tmp_path / "input"), str(tmp_path), str(tmp_path / "work"), [], None, False)
    assert status.read_bytes() == b"old accepted status"
    assert list(tmp_path.iterdir()) == [status]
