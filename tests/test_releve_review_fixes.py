from __future__ import annotations

import csv
import json
from collections import Counter
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
    relative = tool_guard.validate(
        "Bash",
        {"command": "uv run releve/extract_occurrences.py ./travail"},
        str(tmp_path),
        str(work),
    )
    bad = tool_guard.validate(
        "Bash",
        {"command": "uv run releve/zoom.py /etc E100 0 0 100 100"},
        str(ROOT),
        str(work),
    )
    chained = tool_guard.validate("Bash", {"command": "cat a.txt && cat b.txt"}, str(work), str(work))
    extra = tool_guard.validate(
        "Bash",
        {"command": f"uv run releve/extract_occurrences.py {work} subdir"},
        str(ROOT),
        str(work),
    )
    globbed = tool_guard.validate("Bash", {"command": "cat *.csv"}, str(work), str(work))
    assert ok is None
    assert relative is None
    assert "hors du dossier de travail" in bad
    assert "chaînée" in chained
    assert "n'accepte qu'un seul argument" in extra
    assert "hors du dossier de travail" in globbed


def test_tool_guard_refuse_chemin_absolu_hors_travail(tmp_path):
    """Un chemin absolu hors du dossier de travail doit être refusé, y compris en écriture Windows.

    Les chemins Windows n'ont pas de « / » : tant que le garde ne regardait que ce séparateur,
    « cat C:\\Windows\\win.ini » passait pour un nom de fichier simple et était autorisé.
    """
    work = tmp_path / "travail"
    work.mkdir()
    dehors = tmp_path / "secret.txt"
    for commande in (f"cat {dehors}", f"cat {str(dehors).replace(chr(92), '/')}", "cat ..{}secret.txt".format(chr(92))):
        assert "hors du dossier de travail" in (tool_guard.validate("Bash", {"command": commande}, str(work), str(work)) or "")
    dedans = work / "a.csv"
    assert tool_guard.validate("Bash", {"command": f"cat {dedans}"}, str(work), str(work)) is None
    assert tool_guard.validate("Bash", {"command": f'cat "{work / "a b.csv"}"'}, str(work), str(work)) is None


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


@pytest.mark.parametrize("exit_code,is_error", [(1, False), (0, True)])
def test_run_process_stops_after_agent_failure(monkeypatch, tmp_path, exit_code, is_error):
    inbox = tmp_path / "INBOX" / "S-TEST"
    inbox.mkdir(parents=True)
    outbox = tmp_path / "OUTBOX"
    work = outbox / "S-TEST" / "travail"
    work.mkdir(parents=True)
    for filename in ("nomenclature.csv", "feuilles-classement.csv"):
        (work / filename).write_text("existing stale output\n", encoding="utf-8")
    commands: list[list[str]] = []

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(inbox)))
    monkeypatch.setattr(releve_run, "prepare_a_jour", lambda inbox, workdir: False)
    monkeypatch.setattr(releve_run, "run", lambda cmd, **kwargs: (commands.append(cmd) or True) and (0, ""))
    monkeypatch.setattr(releve_run, "agent", lambda workdir, log_path: (exit_code, {"subtype": "error", "is_error": is_error}, 0.01))
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args, **kwargs: None)
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    ok = releve_run.process("S-TEST")

    assert not ok
    assert any("releve/prepare.py" in part for cmd in commands for part in cmd)
    assert not any("releve/build_qpl.py" in part for cmd in commands for part in cmd)
    assert not any("releve/render_pdf.py" in part for cmd in commands for part in cmd)


def test_run_agent_rejects_unknown_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("RELEVE_AGENT", "nvida")
    monkeypatch.setattr(releve_run, "run", lambda *args, **kwargs: pytest.fail("must not launch Claude"))
    with pytest.raises(ValueError, match="RELEVE_AGENT"):
        releve_run.agent(str(tmp_path), str(tmp_path / "log"))


def test_run_nvidia_uses_selected_model_and_reports_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("RELEVE_AGENT", "nvidia")
    monkeypatch.setenv("RELEVE_NVIDIA_MODEL", "candidate/vision-model")
    commands = []
    def fake_run(cmd, **kwargs):
        commands.append(cmd)
        (tmp_path / "agent-resultat.json").write_text(json.dumps({
            "model": "candidate/vision-model", "is_error": False, "subtype": "success",
        }), encoding="utf-8")
        return 0, ""
    monkeypatch.setattr(releve_run, "run", fake_run)
    monkeypatch.setattr(releve_run, "log", lambda *args: None)
    code, result, _ = releve_run.agent(str(tmp_path), str(tmp_path / "log"))
    assert code == 0
    assert result["provider"] == "nvidia"
    assert commands[0][commands[0].index("--model") + 1] == "candidate/vision-model"


def _write_required_outputs(outdir, name="demo"):
    files = [f"{name}-{suffix}" for suffix in (
        "Plans-annotes.pdf", "Rapport-de-metre.pdf", "Rapport-de-metre.md", "Dossier-complet.pdf",
        "format-exemple.pdf", "format-exemple.report.json")]
    files += [f"format-exemple/{f}" for f in ("estimate.json", "bordereau.csv", "plans.pdf", "reserves.md", "feuilles.json")]
    files += [f"{name}-planexpert/{name}.qpl.audit.json", f"{name}-planexpert/P1.png"]
    for relative in files:
        path = outdir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"current")
    (outdir / f"{name}-planexpert/{name}.qpl").write_text(
        '<QuoterPlanSession><Plans><Plan FileName="P1.png"/></Plans></QuoterPlanSession>', encoding="utf-8")


@pytest.mark.parametrize("missing", [
    "demo-Plans-annotes.pdf", "demo-Rapport-de-metre.pdf", "demo-format-exemple.report.json",
    "demo-planexpert/demo.qpl", "demo-planexpert/demo.qpl.audit.json", "demo-planexpert/P1.png",
    "format-exemple/estimate.json",
])
def test_missing_required_output_fails_pipeline_and_does_not_publish(monkeypatch, tmp_path, missing):
    outbox, drive = tmp_path / "out", tmp_path / "drive"
    outdir = outbox / "demo"
    (outdir / "travail").mkdir(parents=True)
    _write_required_outputs(outdir)
    (outdir / missing).unlink()
    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "DRIVE", str(drive))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("demo", str(tmp_path / "input")))
    monkeypatch.setattr(releve_run, "run", lambda *args, **kwargs: (0, ""))
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: True)
    monkeypatch.setattr(releve_run, "log", lambda *args: None)
    monkeypatch.setenv("RELEVE_NATIF", "0")
    assert not releve_run.process("demo", reprendre=True)
    mirror = drive / "OUTBOX" / "demo"
    assert [p.name for p in mirror.iterdir()] == ["STATUT.md"]
    status = (mirror / "STATUT.md").read_text(encoding="utf-8")
    assert "ÉCHEC" in status and missing in status


def test_run_status_reports_actual_nvidia_model(tmp_path):
    inbox, outdir = tmp_path / "in", tmp_path / "out"
    inbox.mkdir()
    outdir.mkdir()
    releve_run.statut("demo", str(inbox), str(outdir), str(tmp_path / "work"), [],
                      {"provider": "nvidia", "model": "candidate/vision-model"}, True)
    status = (outdir / "STATUT.md").read_text(encoding="utf-8")
    assert "candidate/vision-model" in status
    assert "nvidia" in status
    assert "claude -p" not in status


def test_native_manifest_rejects_traversal_and_keeps_nested_current_files(tmp_path):
    native = tmp_path / "export-natif-planexpert"
    (native / "reports").mkdir(parents=True)
    (native / "reports" / "current.pdf").write_bytes(b"current")
    (tmp_path / "partial.pdf").write_bytes(b"stale")
    names = ["reports/current.pdf", "../partial.pdf", r"..\partial.pdf", str(tmp_path / "partial.pdf")]
    (native / "resultat.json").write_text(json.dumps({
        "etapes": {"download": {"fichiers": dict.fromkeys(names, {})}},
    }), encoding="utf-8")
    result = releve_run.current_outputs("demo", str(tmp_path), [("export natif Plan Expert", 0, "oui")])
    assert result == ["export-natif-planexpert/reports/current.pdf", "export-natif-planexpert/resultat.json"]
    releve_run.statut("demo", str(tmp_path / "input"), str(tmp_path), str(tmp_path / "work"),
                      [("export natif Plan Expert", 0, "oui")], None, True, outputs=result)
    assert "partial.pdf" not in (tmp_path / "STATUT.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("relative", ["../old.png", r"..\old.png", "/old.png", r"C:\old.png", "C:old.png", r"\\server\old.png"])
def test_output_child_rejects_foreign_paths_on_every_platform(tmp_path, relative):
    assert not releve_run.confined_output_child(str(tmp_path), relative)


def test_qpl_manifest_only_publishes_flat_current_raster_names(tmp_path):
    project = tmp_path / "demo-planexpert"
    project.mkdir()
    (tmp_path / "old.png").write_bytes(b"stale")
    (project / "current.png").write_bytes(b"current")
    (project / "demo.qpl.audit.json").write_text("{}", encoding="utf-8")
    (project / "demo.qpl").write_text(
        '<QuoterPlanSession><Plans><Plan FileName="current.png"/>'
        '<Plan FileName="../old.png"/><Plan FileName="..\\old.png"/></Plans></QuoterPlanSession>', encoding="utf-8")
    assert releve_run.current_outputs("demo", str(tmp_path), [("build_qpl", 0, "ok")]) == [
        "demo-planexpert/current.png", "demo-planexpert/demo.qpl", "demo-planexpert/demo.qpl.audit.json"]


def test_run_keeps_claude_oauth_sdk_as_existing_default(monkeypatch, tmp_path):
    monkeypatch.delenv("RELEVE_AGENT", raising=False)
    monkeypatch.setenv("RELEVE_MODEL", "claude-choice")
    commands = []
    def fake_run(cmd, **kwargs):
        commands.append(cmd)
        (tmp_path / "agent-resultat.json").write_text('{"is_error": false}', encoding="utf-8")
        return 0, ""
    monkeypatch.setattr(releve_run, "run", fake_run)
    monkeypatch.setattr(releve_run, "log", lambda *args: None)
    code, result, _ = releve_run.agent(str(tmp_path), str(tmp_path / "log"))
    assert code == 0
    assert "releve/agent_sdk.py" in commands[0]
    assert commands[0][commands[0].index("--model") + 1] == "claude-choice"
    assert result["provider"] == "sdk"
    assert result["model"] == "claude-choice"


def test_run_main_explicit_provider_and_failure_exit(monkeypatch, tmp_path):
    monkeypatch.setattr(releve_run.sys, "argv", ["run.py", "demo", "--agent", "nvidia", "--model", "candidate/vision-model"])
    monkeypatch.setattr(releve_run, "INBOX", str(tmp_path / "in"))
    monkeypatch.setattr(releve_run, "OUTBOX", str(tmp_path / "out"))
    monkeypatch.setattr(releve_run, "acquire_lock", lambda: None)
    monkeypatch.setattr(releve_run, "release_lock", lambda: None)
    def fake_process(arg, reprendre=False):
        assert arg == "demo"
        assert releve_run.os.environ.get("RELEVE_AGENT") == "nvidia"
        assert releve_run.os.environ.get("RELEVE_NVIDIA_MODEL") == "candidate/vision-model"
        return False
    monkeypatch.setattr(releve_run, "process", fake_process)
    monkeypatch.delenv("RELEVE_AGENT", raising=False)
    monkeypatch.delenv("RELEVE_NVIDIA_MODEL", raising=False)
    assert releve_run.main() == 1


def test_run_process_skips_native_export_when_component_missing(monkeypatch, tmp_path):
    outbox = tmp_path / "OUTBOX"
    outdir = outbox / "S-TEST"
    workdir = outdir / "travail"
    workdir.mkdir(parents=True)
    (workdir / "agent-resultat.json").write_text("{}", encoding="utf-8")
    _write_required_outputs(outdir, "S-TEST")
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


def test_run_process_blocks_resume_when_quality_fails(monkeypatch, tmp_path):
    outbox = tmp_path / "OUTBOX"
    (outbox / "S-TEST" / "travail").mkdir(parents=True)
    commands: list[list[str]] = []

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(tmp_path / "INBOX" / "S-TEST")))
    monkeypatch.setattr(releve_run, "run", lambda cmd, **kwargs: (commands.append(cmd), (2, "quality failed"))[1]
                    if "releve/controle_qualite.py" in cmd else (commands.append(cmd), (0, ""))[1])
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args, **kwargs: None)
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    assert not releve_run.process("S-TEST", reprendre=True)
    assert any("releve/controle_qualite.py" in cmd for cmd in commands)
    assert not any("releve/build_qpl.py" in cmd for cmd in commands)


@pytest.mark.parametrize("reprendre", [False, True])
@pytest.mark.parametrize("failure", ["releve/controle_qualite.py", "src.estimer.render.from_releve"])
def test_failed_attempt_preserves_but_does_not_publish_outputs(monkeypatch, tmp_path, reprendre, failure):
    outbox, drive = tmp_path / "out", tmp_path / "drive"
    outdir, mirror = outbox / "demo", drive / "OUTBOX" / "demo"
    workdir = outdir / "travail"
    workdir.mkdir(parents=True)
    mirror.mkdir(parents=True)
    for name in ("nomenclature.csv", "feuilles-classement.csv"):
        (workdir / name).write_text("placeholder", encoding="utf-8")
    (outdir / "previous.pdf").write_bytes(b"local previous output")
    (mirror / "previous.pdf").write_bytes(b"previous accepted mirror")
    project = outdir / "demo-planexpert"
    project.mkdir()
    (project / "demo.qpl").write_bytes(b"previous QPL")
    native = outdir / "export-natif-planexpert"
    native.mkdir()
    (native / "resultat.json").write_text('{"ok": true}', encoding="utf-8")

    def fake_run(cmd, **kwargs):
        if failure == "src.estimer.render.from_releve" and "releve/render_pdf.py" in cmd:
            (outdir / "partial.pdf").write_bytes(b"partial new output")
        return (2, "failed") if failure in cmd else (0, "")

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "DRIVE", str(drive))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("demo", str(tmp_path / "input")))
    monkeypatch.setattr(releve_run, "prepare_a_jour", lambda *args: True)
    monkeypatch.setattr(releve_run, "agent", lambda *args: (0, {"is_error": False}, 0))
    monkeypatch.setattr(releve_run, "run", fake_run)
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: True)
    monkeypatch.setattr(releve_run, "log", lambda *args: None)
    monkeypatch.setenv("RELEVE_NATIF", "0")

    assert not releve_run.process("demo", reprendre=reprendre)
    assert (outdir / "previous.pdf").read_bytes() == b"local previous output"
    assert (project / "demo.qpl").read_bytes() == b"previous QPL"
    assert (mirror / "previous.pdf").read_bytes() == b"previous accepted mirror"
    assert set(p.name for p in mirror.iterdir()) == {"previous.pdf", "STATUT.md"}
    status = (outdir / "STATUT.md").read_text(encoding="utf-8")
    assert "ÉCHEC" in status and "Aucun livrable validé" in status
    assert "previous.pdf" not in status and "demo.qpl" not in status and "partial.pdf" not in status
    assert "Plan Expert (VM mxlinux, MCP planexpert-vm) : oui" not in status
    assert (mirror / "STATUT.md").read_text(encoding="utf-8") == status

    (project / "stale.png").write_bytes(b"keep old raster")
    def successful_run(cmd, **kwargs):
        if "releve/build_qpl.py" in cmd:
            _write_required_outputs(outdir)
            (project / "demo.qpl").write_text('<QuoterPlanSession><Plans><Plan FileName="P1.png"/></Plans></QuoterPlanSession>', encoding="utf-8")
            (project / "P1.png").write_bytes(b"current raster")
        if "releve/render_pdf.py" in cmd:
            (outdir / "demo-Plans-annotes.pdf").write_bytes(b"current PDF")
        if "src.estimer.render.from_releve" in cmd:
            (outdir / "demo-format-exemple.pdf").write_bytes(b"current example")
            (outdir / "demo-format-exemple.report.json").write_text("{}", encoding="utf-8")
        return 0, ""

    monkeypatch.setattr(releve_run, "run", successful_run)
    assert releve_run.process("demo", reprendre=True)
    status = (outdir / "STATUT.md").read_text(encoding="utf-8")
    assert "previous.pdf" not in status and "partial.pdf" not in status and "stale.png" not in status
    assert "demo-format-exemple.pdf" in status and "demo-planexpert/demo.qpl" in status
    assert (mirror / "previous.pdf").read_bytes() == b"previous accepted mirror"
    assert not (mirror / "partial.pdf").exists()
    assert not (mirror / "demo-planexpert" / "stale.png").exists()
    assert (project / "stale.png").read_bytes() == b"keep old raster"
    assert (mirror / "demo-planexpert" / "P1.png").read_bytes() == b"current raster"
    assert (mirror / "demo-format-exemple.pdf").read_bytes() == b"current example"


def test_run_process_creates_example_format(monkeypatch, tmp_path):
    outbox = tmp_path / "OUTBOX"
    (outbox / "S-TEST" / "travail").mkdir(parents=True)
    _write_required_outputs(outbox / "S-TEST", "S-TEST")
    commands: list[list[str]] = []

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(tmp_path / "INBOX" / "S-TEST")))
    monkeypatch.setattr(releve_run, "PLANEXPERT_VM_CLI", str(tmp_path / "missing-planexpert.py"))
    monkeypatch.setattr(releve_run, "run", lambda cmd, **kwargs: (commands.append(cmd), (0, ""))[1])
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args, **kwargs: None)
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    assert releve_run.process("S-TEST", reprendre=True)
    assert any("src.estimer.render.from_releve" in cmd for cmd in commands)


def test_jeu_reference_requires_baseline(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(jeu_reference, "SORTIE", tmp_path / "_jeu-reference")
    monkeypatch.setattr(jeu_reference, "dossiers_du_jeu", lambda: ["S-TEST"])
    monkeypatch.setattr(
        jeu_reference,
        "evaluer",
        lambda s: (
            {"humaines": 1, "ia": 1, "appariees": 1, "manquantes": 0, "en_trop": 0, "rappel": 100.0, "precision": 100.0},
            Counter(),
        ),
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
        lambda s: (
            {"humaines": 1, "ia": 1, "appariees": 1, "manquantes": 0, "en_trop": 0, "rappel": 100.0, "precision": 100.0},
            Counter(),
        ),
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
        lambda s: (
            {
                "humaines": 10, "ia": 10, "appariees": 8, "manquantes": 2, "en_trop": 2, "rappel": 80.0, "precision": 80.0,
                "normalise": {
                    "accord_libelle_brut": 0.0, "accord_libelle_canonique": 0.0,
                    "rebut_humain": 0, "rebut_ia": 0, "rappel": 80.0, "precision": 80.0,
                },
                "categorie": {"couples": 8, "accord": 8, "pourcentage": 100.0, "confusions": []},
            },
            Counter(),
        ),
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
    assert "finally:" in traits_py and "doc.close()" in traits_py
    assert "pymupdf.open(src)[" not in traits_py
