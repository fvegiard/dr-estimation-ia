from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from conftest import ROOT
from outils import assembler_dossier
from releve import build_qpl, extract_occurrences, prepare, run as releve_run, tool_guard, zoom
from src.validation import jeu_reference


def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


def _make_workdir(tmp_path: Path) -> Path:
    work = tmp_path / "travail"
    work.mkdir()
    _write_csv(
        work / "nomenclature.csv",
        ["label", "famille", "forme", "rgb", "jeton_regex", "description", "source"],
        [["DS1", "luminaire", "", "", "DS1", "Luminaire", "E100"]],
    )
    _write_csv(
        work / "feuilles.csv",
        ["feuille", "fichier", "page", "largeur_pt", "hauteur_pt", "raster_px", "classement_fichier"],
        [["E100", "plans.pdf", "1", "1000", "700", "1000x700", "plans"]],
    )
    _write_csv(work / "feuilles-classement.csv", ["feuille", "type", "echelle", "note"], [["E100", "plan", "100", ""]])
    return work


def test_tool_guard_denies_access_outside_workdir(tmp_path):
    work = tmp_path / "travail"
    work.mkdir()
    reason = tool_guard.validate("Read", {"file_path": str(tmp_path / "secret.txt")}, str(work), str(work))
    assert "hors du dossier de travail" in reason


def test_tool_guard_allows_expected_releve_commands(tmp_path):
    work = tmp_path / "travail"
    work.mkdir()
    ok = tool_guard.validate(
        "Bash",
        {"command": f"uv run releve/zoom.py {work} E100 0 0 100 100"},
        str(ROOT),
        str(work),
    )
    bad = tool_guard.validate(
        "Bash",
        {"command": f"uv run releve/zoom.py /etc E100 0 0 100 100"},
        str(ROOT),
        str(work),
    )
    chained = tool_guard.validate("Bash", {"command": "cat a.txt && cat b.txt"}, str(work), str(work))
    assert ok is None
    assert "hors du dossier de travail" in bad
    assert "chaînée" in chained


def test_extract_occurrences_invalid_regex_aborts(tmp_path):
    work = _make_workdir(tmp_path)
    _write_csv(
        work / "nomenclature.csv",
        ["label", "famille", "forme", "rgb", "jeton_regex", "description", "source"],
        [["DS1", "luminaire", "", "", "[", "Luminaire", "E100"]],
    )
    with pytest.raises(SystemExit, match="regex invalide"):
        extract_occurrences.main(str(work))


def test_build_qpl_refuses_marked_sheet_without_raster(tmp_path):
    work = _make_workdir(tmp_path)
    _write_csv(
        work / "occurrences-texte.csv",
        ["feuille", "label", "x_pt", "y_pt", "source", "note"],
        [["E100", "DS1", "10", "20", "texte", "mot 'DS1'"]],
    )
    with pytest.raises(SystemExit, match="rasters absents"):
        build_qpl.main(str(work), "S-TEST", str(tmp_path / "out"))


def test_prepare_cleans_stale_outputs(dossier_inbox, tmp_path):
    work = tmp_path / "travail"
    work.mkdir()
    (work / "occurrences-visuel.csv").write_text("stale\n", encoding="utf-8")
    (work / "zooms").mkdir()
    (work / "zooms" / "old.png").write_bytes(b"old")
    prepare.main(str(dossier_inbox), str(work))
    assert not (work / "occurrences-visuel.csv").exists()
    assert not (work / "zooms").exists()
    assert (work / "inventaire.json").is_file()
    assert (work / "rasters").is_dir()


def test_run_process_stops_after_agent_failure(monkeypatch, tmp_path):
    inbox = tmp_path / "INBOX" / "S-TEST"
    inbox.mkdir(parents=True)
    outbox = tmp_path / "OUTBOX"
    commands: list[list[str]] = []

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(inbox)))
    monkeypatch.setattr(releve_run, "prepare_a_jour", lambda inbox, workdir: False)
    monkeypatch.setattr(releve_run, "run", lambda cmd, **kwargs: (commands.append(cmd) or True) and (0, ""))
    monkeypatch.setattr(releve_run, "agent", lambda workdir, log_path: (1, {"subtype": "error"}, 0.01))
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args, **kwargs: None)
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    ok = releve_run.process("S-TEST")

    assert not ok
    assert any("releve/prepare.py" in part for cmd in commands for part in cmd)
    assert not any("releve/build_qpl.py" in part for cmd in commands for part in cmd)
    assert not any("releve/render_pdf.py" in part for cmd in commands for part in cmd)


def test_run_process_skips_native_export_when_component_missing(monkeypatch, tmp_path):
    outbox = tmp_path / "OUTBOX"
    outdir = outbox / "S-TEST"
    workdir = outdir / "travail"
    workdir.mkdir(parents=True)
    (workdir / "agent-resultat.json").write_text("{}", encoding="utf-8")
    commands: list[list[str]] = []

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(tmp_path / "INBOX" / "S-TEST")))
    monkeypatch.setattr(releve_run, "PLANEXPERT_VM_CLI", str(tmp_path / "missing-planexpert.py"))
    monkeypatch.setattr(releve_run, "run", lambda cmd, **kwargs: (commands.append(cmd) or True) and (0, "{}"))
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args, **kwargs: None)
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    ok = releve_run.process("S-TEST", reprendre=True)

    assert ok
    assert any("releve/build_qpl.py" in part for cmd in commands for part in cmd)
    assert any("releve/render_pdf.py" in part for cmd in commands for part in cmd)
    assert not any("planexpert_vm" in part for cmd in commands for part in cmd)


def test_jeu_reference_requires_baseline(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(jeu_reference, "SORTIE", tmp_path / "_jeu-reference")
    monkeypatch.setattr(jeu_reference, "dossiers_du_jeu", lambda: ["S-TEST"])
    monkeypatch.setattr(
        jeu_reference,
        "evaluer",
        lambda s: {"humaines": 1, "ia": 1, "appariees": 1, "manquantes": 0, "en_trop": 0, "rappel": 100.0, "precision": 100.0},
    )

    code = jeu_reference.main([])

    assert code == 2
    assert "ligne de base absente" in capsys.readouterr().err


def test_jeu_reference_requires_all_baseline_keys(monkeypatch, tmp_path, capsys):
    sortie = tmp_path / "_jeu-reference"
    sortie.mkdir()
    (sortie / "ligne-de-base.json").write_text(
        json.dumps(
            {
                "S-TEST": {"rappel": 100.0, "precision": 100.0},
                "S-MISSING": {"rappel": 100.0, "precision": 100.0},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(jeu_reference, "SORTIE", sortie)
    monkeypatch.setattr(jeu_reference, "dossiers_du_jeu", lambda: ["S-TEST"])
    monkeypatch.setattr(
        jeu_reference,
        "evaluer",
        lambda s: {"humaines": 1, "ia": 1, "appariees": 1, "manquantes": 0, "en_trop": 0, "rappel": 100.0, "precision": 100.0},
    )

    code = jeu_reference.main([])

    assert code == 2
    assert "S-MISSING" in capsys.readouterr().err


def test_jeu_reference_refuses_new_baseline_on_regression(monkeypatch, tmp_path, capsys):
    sortie = tmp_path / "_jeu-reference"
    sortie.mkdir()
    base_path = sortie / "ligne-de-base.json"
    base_path.write_text(
        json.dumps({"S-TEST": {"rappel": 100.0, "precision": 100.0}}, indent=1),
        encoding="utf-8",
    )
    monkeypatch.setattr(jeu_reference, "SORTIE", sortie)
    monkeypatch.setattr(jeu_reference, "dossiers_du_jeu", lambda: ["S-TEST"])
    monkeypatch.setattr(
        jeu_reference,
        "evaluer",
        lambda s: {"humaines": 10, "ia": 10, "appariees": 8, "manquantes": 2, "en_trop": 2, "rappel": 80.0, "precision": 80.0},
    )

    code = jeu_reference.main(["--nouvelle-base"])

    assert code == 1
    assert "régressions détectées" in capsys.readouterr().err
    assert json.loads(base_path.read_text(encoding="utf-8"))["S-TEST"]["rappel"] == 100.0


def test_assembler_dossier_refuses_conflicting_reference_csv(monkeypatch, tmp_path):
    out = tmp_path / "OUTBOX" / "S-TEST"
    (out / "travail").mkdir(parents=True)
    (out / "reference-quantites.csv").write_text("a\n", encoding="utf-8")
    (out / "dupuis-quantites.csv").write_text("b\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit, match="conflit"):
        assembler_dossier.main("S-TEST", str(out), str(tmp_path / "reference"))


def test_zoom_open_sheet_page_returns_document_handle(monkeypatch, tmp_path):
    class DummyDoc:
        def __init__(self):
            self.page = object()

        def __getitem__(self, index):
            assert index == 0
            return self.page

    doc = DummyDoc()
    monkeypatch.setattr(zoom.pymupdf, "open", lambda path: doc)
    got_doc, got_page = zoom.open_sheet_page(str(tmp_path), "E100")
    assert got_doc is doc
    assert got_page is doc.page


def test_static_policy_files_updated():
    inventaire = (ROOT / ".claude" / "agents" / "inventaire.md").read_text(encoding="utf-8")
    releveur = (ROOT / ".claude" / "agents" / "releveur.md").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "claude.yml").read_text(encoding="utf-8")
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    sdk_smoke = (ROOT / "releve" / "tests" / "sdk_smoke.py").read_text(encoding="utf-8")
    traits_py = (ROOT / "releve" / "traits.py").read_text(encoding="utf-8")

    assert "tools: Glob, Bash(find *), Bash(stat *), Bash(du *), Bash(ls *)" in inventaire
    assert "tools: Read, Write, Edit, Glob, Grep, Bash(uv run releve/zoom.py *)" in releveur
    assert "author_association" in workflow
    assert settings["hooks"]["PreToolUse"][0]["hooks"][0]["args"][0].endswith("releve/tool_guard.py")
    assert 'cwd=str(REPO)' in sdk_smoke
    assert '"/mnt/d/claude/releve-auto/repo"' not in sdk_smoke
    assert "doc = pymupdf.open(src)" in traits_py
    assert "pymupdf.open(src)[" not in traits_py
