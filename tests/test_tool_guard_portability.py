"""Check POSIX shell parsing independently of the machine running pytest."""
import posixpath
from types import SimpleNamespace

import pytest

from releve import tool_guard


@pytest.mark.parametrize("command", [
    r"cat ..\secret.txt",
    r"cat '..\secret.txt'",
    r'cat "..\secret.txt"',
    r"cat C:\Windows\win.ini",
    "cat ../secret.txt",
    "cat /etc/passwd",
])
def test_posix_rejects_foreign_and_escaping_paths(monkeypatch, command):
    monkeypatch.setattr(tool_guard, "os", SimpleNamespace(name="posix", path=posixpath))
    assert "hors du dossier de travail" in (
        tool_guard.validate("Bash", {"command": command}, "/work", "/work") or "")


@pytest.mark.parametrize("command", ["cat /work/a.csv", 'cat "/work/a b.csv"', "cat ./a.csv"])
def test_posix_preserves_confined_paths(monkeypatch, command):
    monkeypatch.setattr(tool_guard, "os", SimpleNamespace(name="posix", path=posixpath))
    assert tool_guard.validate("Bash", {"command": command}, "/work", "/work") is None
