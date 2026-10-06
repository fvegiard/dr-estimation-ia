from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path

import pytest

import pymupdf

from conftest import ROOT
from outils import assembler_dossier
from releve import build_qpl, extract_occurrences, prepare, render_pdf, run as releve_run, tool_guard, zoom
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
        {"command": f"uv run releve/zoom.py /etc E100 0 0 100 100"},
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


def _simuler_windows(monkeypatch):
    """Remplace `os` dans le module tool_guard par un faux `os` (name='nt', path=ntpath), sans toucher
    le vrai module `os` global (donc sans risque pour le reste du test ou de pytest) : ntpath fait de la
    pure manipulation de chaînes, sans accès disque, donc utilisable tel quel sur un hôte Linux pour
    vérifier la résolution de chemins Windows natifs sans machine Windows réelle."""
    import ntpath
    import types
    monkeypatch.setattr(tool_guard, "os", types.SimpleNamespace(name="nt", path=ntpath))


def test_tool_guard_accepts_legitimate_windows_path_inside_workdir(monkeypatch):
    """Régression constatée par Francis sur poste Windows réel (commit da9da39) : un chemin absolu Windows
    LÉGITIME et DANS le dossier de travail (ex. C:\\...\\travail\\a.csv) était refusé, parce que le refus
    de tout antislash ne distinguait pas Windows natif (où « \\ » est le vrai séparateur) de POSIX (où il
    ne l'est jamais). Sur Windows natif, un tel chemin doit être accepté."""
    _simuler_windows(monkeypatch)
    root = r"C:\work\S-TEST\travail"
    dedans = root + r"\a.csv"
    assert tool_guard.validate("Bash", {"command": f"cat {dedans}"}, root, root) is None


def test_tool_guard_still_refuses_windows_path_outside_workdir(monkeypatch):
    """Ne pas relâcher le refus hors-dossier en corrigeant la régression ci-dessus : sur Windows natif,
    un chemin absolu hors du dossier de travail, ou une remontée `..\\..\\`, doivent rester refusés."""
    _simuler_windows(monkeypatch)
    root = r"C:\work\S-TEST\travail"
    dehors = r"C:\work\secret.txt"
    remontee = root + r"\..\..\secret.txt"     # travail -> S-TEST -> work : sort bien du dossier de travail
    for commande in (f"cat {dehors}", f"cat {remontee}"):
        reason = tool_guard.validate("Bash", {"command": commande}, root, root)
        assert reason and "hors du dossier de travail" in reason


@pytest.mark.skipif(os.name == "nt", reason="vérifie le comportement POSIX réel ; sans objet sous Windows")
def test_tool_guard_refuses_disguised_windows_traversal_on_posix():
    """Sur POSIX (l'hôte réel de ce test), un antislash reste refusé d'office : il ne peut jamais y être
    un séparateur légitime (aucun nom de fichier du dépôt n'en contient) et pourrait déguiser une
    tentative d'évasion écrite en syntaxe Windows — non couvert par la simulation `_simuler_windows`
    ci-dessus, qui ne s'applique que quand `os.name == "nt"`."""
    reason = tool_guard.validate("Bash", {"command": r"cat ..\secret.txt"}, "/tmp/travail", "/tmp/travail")
    assert reason and "hors du dossier de travail" in reason


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


def test_dossier_complet_keeps_ocg_layers(tmp_path):
    """Dossier-complet.pdf must keep the RELEVE family layers of Plans-annotes.pdf, not just their ink.

    pymupdf's insert_pdf() does not carry a source document's /OCProperties catalog entry into an
    unrelated destination: starting from a fresh document and inserting the annotated plans into it
    silently dropped every optional-content group (verified empirically before this fix)."""
    work = _make_workdir(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    plans = pymupdf.open()
    oc = plans.add_ocg("RELEVE M01 - TEST", on=True)
    page = plans.new_page(width=200, height=100)
    page.draw_circle((50, 50), 10, color=(1, 0, 0), oc=oc)
    plans.save(out / "S-TEST-Plans-annotes.pdf")

    render_pdf.main(str(work), "S-TEST", str(out))

    complet = pymupdf.open(out / "S-TEST-Dossier-complet.pdf")
    ocgs = complet.get_ocgs()
    assert ocgs, "Dossier-complet.pdf a perdu les calques OCG de Plans-annotes.pdf"
    assert any(v["name"] == "RELEVE M01 - TEST" for v in ocgs.values())


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


def test_statut_flags_box_overlap_as_a_verifier(tmp_path):
    """A box overlapping the drawing must show 'TERMINÉ — À VÉRIFIER', not a plain 'TERMINÉ' that reads as
    a validated, shippable deliverable when nobody has looked at the render yet."""
    inbox = tmp_path / "INBOX"; inbox.mkdir()
    outdir = tmp_path / "OUTBOX"; outdir.mkdir()
    workdir = outdir / "travail"; workdir.mkdir()
    releve_run.statut("S-TEST", str(inbox), str(outdir), str(workdir), [("total", 1.0, "")], None, True,
                      None, ["E204"])
    texte = (outdir / "STATUT.md").read_text(encoding="utf-8")
    assert "TERMINÉ — À VÉRIFIER" in texte
    assert "E204" in texte and "espace libre" in texte

    clean = tmp_path / "OUTBOX2"; clean.mkdir()
    releve_run.statut("S-TEST", str(inbox), str(clean), str(workdir), [("total", 1.0, "")], None, True, None, [])
    texte_propre = (clean / "STATUT.md").read_text(encoding="utf-8")
    assert "État : **TERMINÉ**" in texte_propre and "À VÉRIFIER" not in texte_propre


def test_run_process_propagates_box_overlap_from_rendu_rapport(monkeypatch, tmp_path):
    """process() must read <NOM>-rendu-rapport.json and pass its overlap list on to statut(), not just log
    render_vectoriel.py's own stderr warning where nothing downstream (STATUT.md, Drive copy) sees it."""
    inbox = tmp_path / "INBOX" / "S-TEST"
    inbox.mkdir(parents=True)
    outbox = tmp_path / "OUTBOX"
    outdir = outbox / "S-TEST"
    workdir = outdir / "travail"
    workdir.mkdir(parents=True)
    (workdir / "nomenclature.csv").write_text("label\n", encoding="utf-8")
    (workdir / "feuilles-classement.csv").write_text("feuille\n", encoding="utf-8")
    statut_calls = []

    def _run(cmd, **kwargs):
        if "releve/render_vectoriel.py" in cmd:
            os.makedirs(outdir, exist_ok=True)
            (outdir / "S-TEST-rendu-rapport.json").write_text(
                json.dumps({"conformite": {"encadre_hors_espace_libre": ["E204"]}}), encoding="utf-8")
        return 0, ""

    monkeypatch.setattr(releve_run, "OUTBOX", str(outbox))
    monkeypatch.setattr(releve_run, "resolve_inbox", lambda arg: ("S-TEST", str(inbox)))
    monkeypatch.setattr(releve_run, "prepare_a_jour", lambda inbox, workdir: True)
    monkeypatch.setattr(releve_run, "run", _run)
    monkeypatch.setattr(releve_run, "agent", lambda workdir, log_path: (0, {"subtype": "success"}, 0.01))
    monkeypatch.setattr(releve_run, "drive_mounted", lambda: False)
    monkeypatch.setattr(releve_run, "statut", lambda *args: statut_calls.append(args))
    monkeypatch.setattr(releve_run, "log", lambda *args, **kwargs: None)

    ok = releve_run.process("S-TEST")

    assert ok
    assert statut_calls and statut_calls[0][-1] == ["E204"]


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
