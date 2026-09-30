"""Tests hors réseau de releve/agent_nvidia.py : confinement au dossier de travail, sorties autorisées, contrôle de couverture, reprises journalisées."""
import importlib.util
import csv
import io
import json
import os
import pathlib
import urllib.error

import pytest

SPEC = importlib.util.spec_from_file_location("agent_nvidia", pathlib.Path(__file__).resolve().parents[1] / "releve" / "agent_nvidia.py")
an = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(an)


def _work(tmp_path):
    (tmp_path / "feuilles.csv").write_text("feuille,fichier,page,largeur_pt,hauteur_pt\nP1,a.pdf,1,1200,600\n", encoding="utf-8")
    (tmp_path / "feuilles-classement.csv").write_text("feuille,type,echelle,note\nP1,plan,,\n", encoding="utf-8")
    (tmp_path / "nomenclature.csv").write_text("label,famille\nKLAXON,alarme\n", encoding="utf-8")
    an.VUS.clear()
    return str(tmp_path)


def test_hors_dossier_refuse(tmp_path):
    with pytest.raises(ValueError):
        an.dans(str(tmp_path), "../secret.txt")


def test_ecrire_limite_aux_sorties(tmp_path):
    w = _work(tmp_path)
    assert an.outil(w, "ecrire", {"chemin": "MANIFESTE.md", "contenu": "x"})[0].startswith("refusé")
    assert an.outil(w, "ecrire", {"chemin": "reserves.md", "contenu": "R-001"})[0].startswith("écrit")


def test_ajouter_occurrences_entete_unique(tmp_path):
    w = _work(tmp_path)
    an.outil(w, "ajouter_occurrences", {"lignes": ["P1,KLAXON,10,20,visuel,[K1.1]"]})
    an.outil(w, "ajouter_occurrences", {"lignes": ["feuille,label,x_pt,y_pt,source,note", "P1,KLAXON,30,20,visuel,[K1.2]"]})
    lignes = open(os.path.join(w, "occurrences-visuel.csv"), encoding="utf-8").read().splitlines()
    assert lignes == [an.ENTETE_VISUEL, "P1,KLAXON,10,20,visuel,[K1.1]", "P1,KLAXON,30,20,visuel,[K1.2]"]


def test_couverture_exige_zooms_fins(tmp_path):
    w = _work(tmp_path)
    assert set(an.manquantes(w)) == {"P1"}                      # rien vu : 2 fenêtres de 600 pt manquent
    an.VUS.append(("P1", 0, 0, 1200, 600))                       # un zoom grossier ne compte pas (non ajouté par `zoom`)
    assert len(an.manquantes(w)["P1"]) == 2
    an.VUS.clear(); an.VUS.append(("P1", 0, 0, 600, 600))
    assert an.manquantes(w)["P1"] == [(600, 0, 1200, 600)]
    an.VUS.append(("P1", 600, 0, 1200, 600))
    assert an.manquantes(w) == {}


def test_tiny_center_zoom_is_not_full_coverage(tmp_path):
    w = _work(tmp_path)
    an.VUS.extend([("P1", 299, 299, 301, 301), ("P1", 899, 299, 901, 301)])
    assert len(an.manquantes(w)["P1"]) == 2


def test_four_quarter_zooms_cover_full_window(tmp_path):
    w = _work(tmp_path)
    an.VUS.extend([("P1", x, y, x + 300, y + 300) for x in (0, 300) for y in (0, 300)])
    assert an.manquantes(w)["P1"] == [(600, 0, 1200, 600)]
    an.VUS.append(("P1", 600, 0, 1200, 600))
    assert an.manquantes(w) == {}


def test_union_rejects_central_hole_then_accepts_repair(tmp_path):
    w = _work(tmp_path)
    an.VUS.extend([("P1", 0, 0, 600, 299), ("P1", 0, 301, 600, 600),
                   ("P1", 0, 299, 299, 301), ("P1", 301, 299, 600, 301),
                   ("P1", 600, 0, 1200, 600)])
    assert an.manquantes(w)["P1"] == [(0, 0, 600, 600)]
    an.VUS.append(("P1", 299, 299, 301, 301))
    assert an.manquantes(w) == {}


@pytest.mark.parametrize("requested,expected", [
    ((1900, 100, 2200, 700), (1750, 100, 2350, 700)),
    ((2800, 100, 3000, 700), (2400, 100, 3000, 700)),
    ((0, 0, 600, 600), (0, 0, 600, 600)),
])
def test_zoom_expands_to_square_preserving_requested_area(tmp_path, monkeypatch, requested, expected):
    w = _work(tmp_path)
    (tmp_path / "feuilles.csv").write_text("feuille,largeur_pt,hauteur_pt\nP1,3000,2000\n", encoding="utf-8")
    image = tmp_path / "zoom.png"
    image.write_bytes(b"image-test-only")
    calls = []
    def fake_script(workdir, name, args):
        calls.append(args)
        return 0, str(image)
    monkeypatch.setattr(an, "script", fake_script)
    args = dict(zip(("x0", "y0", "x1", "y1"), requested), feuille="P1")
    description, actual_image = an.outil(w, "zoom", args)
    assert calls == [["P1", *expected]]
    assert actual_image == str(image)
    assert an.VUS == []  # Rendering alone is not delivery to the model.
    assert json.loads(description)["bounds_pt"] == list(expected)
    assert json.loads(description)["coordinate_system"] == "absolute PDF points"
    assert expected[0] <= requested[0] < requested[2] <= expected[2]
    assert expected[1] <= requested[1] < requested[3] <= expected[3]


@pytest.mark.parametrize("bounds", [
    (-1, 0, 100, 100), (0, 0, 1201, 100), (0, 0, 100, 601),
    (100, 0, 100, 100), (200, 0, 100, 100), (0, 100, 100, 50),
    (float("nan"), 0, 100, 100), (0, 0, float("inf"), 100),
    (0, 0, 800, 300),  # Cannot expand to an 800-point square on a 600-point-high page.
])
def test_invalid_or_unfittable_square_zoom_rejected(tmp_path, monkeypatch, bounds):
    w = _work(tmp_path)
    monkeypatch.setattr(an, "script", lambda *_: pytest.fail("invalid zoom must not render"))
    args = dict(zip(("x0", "y0", "x1", "y1"), bounds), feuille="P1")
    with pytest.raises(ValueError):
        an.outil(w, "zoom", args)
    assert an.VUS == []


def test_tall_request_renders_actual_square_image(tmp_path):
    import pymupdf
    from PIL import Image
    w = _work(tmp_path)
    (tmp_path / "feuilles.csv").write_text("feuille,largeur_pt,hauteur_pt\nP1,3000,2000\n", encoding="utf-8")
    (tmp_path / "feuilles").mkdir()
    with pymupdf.open() as doc:
        page = doc.new_page(width=3000, height=2000)
        page.draw_rect(pymupdf.Rect(1900, 100, 2200, 700))
        doc.save(tmp_path / "feuilles" / "P1.pdf")
    description, path = an.outil(w, "zoom", {"feuille": "P1", "x0": 1900, "y0": 100, "x1": 2200, "y1": 700})
    assert json.loads(description)["bounds_pt"] == [1750, 100, 2350, 700]
    with Image.open(path) as image:
        assert image.size == (1800, 1800)


def test_structured_occurrences_escape_commas(tmp_path):
    w = _work(tmp_path)
    row = {"feuille": "P1", "label": "KLAXON", "x_pt": 12.5, "y_pt": 23.75, "note": "[K1.1], corridor"}
    an.outil(w, "ajouter_occurrences", {"occurrences": [row]})
    with (tmp_path / "occurrences-visuel.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1 and rows[0]["note"] == row["note"]
    assert rows[0]["source"] == "visuel" and None not in rows[0]


def test_occurrence_metadata_migrates_legacy_and_reaches_loader(tmp_path):
    from commun import load_occurrences
    from src.estimer.render.from_releve import read_occurrences
    w = _work(tmp_path)
    original = "P1,KLAXON,10,20,visuel,[K1.1]"
    an.outil(w, "ajouter_occurrences", {"lignes": [original]})
    metadata = {"designation": "Deux commandes", "portee": "À remplacer", "modele": "M,2",
                "prescription": "Fournir deux commandes, même emplacement", "parent": "PA",
                "qte": 2, "reserve": "Calibre à confirmer",
                "x0_pt": 20, "y0_pt": 30, "x1_pt": 40, "y1_pt": 50}
    an.outil(w, "ajouter_occurrences", {"occurrences": [
        {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40, "note": "[K1.2]", **metadata}]})
    an.outil(w, "ajouter_occurrences", {"lignes": ["P1,KLAXON,60,70,visuel,[K1.3]"]})
    with (tmp_path / "occurrences-visuel.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 3
    assert [rows[0][k] for k in an.ENTETE_VISUEL.split(",")] == next(csv.reader([original]))
    assert all(rows[1][k] == str(v) for k, v in metadata.items())
    assert rows[0]["qte"] == rows[2]["qte"] == ""
    loaded = load_occurrences(w)
    assert [r["qte"] for r in loaded] == [1, 2, 1]
    assert read_occurrences(tmp_path)[1]["prescription"] == metadata["prescription"]
    properties = next(t for t in an.OUTILS if t["function"]["name"] == "ajouter_occurrences")["function"]["parameters"]["properties"]["occurrences"]["items"]["properties"]
    assert set(metadata) <= set(properties)


@pytest.mark.parametrize("qte", [0, -1, float("nan"), float("inf"), "invalid", True])
def test_invalid_quantity_preserves_whole_existing_file(tmp_path, qte):
    w = _work(tmp_path)
    an.outil(w, "ajouter_occurrences", {"lignes": ["P1,KLAXON,10,20,visuel,old"]})
    path = tmp_path / "occurrences-visuel.csv"
    before = path.read_bytes()
    good = {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40, "qte": 2}
    with pytest.raises(ValueError):
        an.outil(w, "ajouter_occurrences", {"occurrences": [good, {**good, "qte": qte}]})
    assert path.read_bytes() == before


def test_migration_preserves_unknown_existing_columns_and_failed_replace(tmp_path, monkeypatch):
    w = _work(tmp_path)
    path = tmp_path / "occurrences-visuel.csv"
    path.write_text(an.ENTETE_VISUEL + ',custom\nP1,KLAXON,10,20,visuel,"old, note",kept\n', encoding="utf-8")
    before = path.read_bytes()
    row = {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40, "qte": 2}
    original_replace = an.os.replace
    def failed_replace(*args):
        raise OSError("simulated replace failure")
    monkeypatch.setattr(an.os, "replace", failed_replace)
    with pytest.raises(OSError):
        an.outil(w, "ajouter_occurrences", {"occurrences": [row]})
    assert path.read_bytes() == before
    assert not list(tmp_path.glob(".occurrences-*.tmp"))
    monkeypatch.setattr(an.os, "replace", original_replace)
    an.outil(w, "ajouter_occurrences", {"occurrences": [row]})
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]["custom"] == "kept" and rows[0]["note"] == "old, note"
    assert rows[1]["qte"] == "2" and rows[1]["custom"] == ""


@pytest.mark.parametrize("qte,expected", [(0.5, 0.5), ("2.5", 2.5), ("", 1), (None, 1)])
def test_optional_quantity_matches_loader_defaults(tmp_path, qte, expected):
    from commun import load_occurrences
    w = _work(tmp_path)
    an.outil(w, "ajouter_occurrences", {"occurrences": [
        {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40, "qte": qte}]})
    assert load_occurrences(w)[0]["qte"] == expected


@pytest.mark.parametrize("suffix", [",extra\nP1,KLAXON,10,20,visuel,note\n",
                                     "\nP1,KLAXON,10,20,visuel,note,unexpected\n"])
def test_malformed_existing_csv_is_not_migrated(tmp_path, suffix):
    w = _work(tmp_path)
    path = tmp_path / "occurrences-visuel.csv"
    path.write_text(an.ENTETE_VISUEL + suffix, encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(ValueError):
        an.outil(w, "ajouter_occurrences", {"occurrences": [
            {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40, "qte": 2}]})
    assert path.read_bytes() == before


@pytest.mark.parametrize("change", [{"x0_pt": float("nan")}, {"x1_pt": 1300},
                                     {"y1_pt": 20}, {"x1_pt": None}])
def test_invalid_optional_bbox_is_atomic(tmp_path, change):
    w = _work(tmp_path)
    row = {"feuille": "P1", "label": "KLAXON", "x_pt": 30, "y_pt": 40,
           "x0_pt": 20, "y0_pt": 30, "x1_pt": 40, "y1_pt": 50}
    with pytest.raises(ValueError):
        an.outil(w, "ajouter_occurrences", {"occurrences": [row, {**row, **change}]})
    assert not (tmp_path / "occurrences-visuel.csv").exists()


@pytest.mark.parametrize("bad", [
    "P1,UNKNOWN,10,20,visuel,note", "MISSING,KLAXON,10,20,visuel,note",
    "P1,KLAXON,nan,20,visuel,note", "P1,KLAXON,10,inf,visuel,note",
    "P1,KLAXON,-1,20,visuel,note", "P1,KLAXON,1201,20,visuel,note",
    "P1,KLAXON,10,601,visuel,note", "P1,KLAXON,10,20,visuel,note,unescaped",
])
def test_bad_occurrence_batch_is_atomic(tmp_path, bad):
    w = _work(tmp_path)
    good = "P1,KLAXON,10,20,visuel,[K1.1]"
    an.outil(w, "ajouter_occurrences", {"lignes": [good]})
    before = (tmp_path / "occurrences-visuel.csv").read_bytes()
    with pytest.raises(ValueError):
        an.outil(w, "ajouter_occurrences", {"lignes": [good, bad]})
    assert (tmp_path / "occurrences-visuel.csv").read_bytes() == before


@pytest.mark.parametrize("change", [{"label": "UNKNOWN"}, {"x_pt": float("nan")}, {"y_pt": 601}])
def test_bad_structured_batch_creates_no_output(tmp_path, change):
    w = _work(tmp_path)
    good = {"feuille": "P1", "label": "KLAXON", "x_pt": 0, "y_pt": 600, "note": "boundary"}
    with pytest.raises(ValueError):
        an.outil(w, "ajouter_occurrences", {"occurrences": [good, {**good, **change}]})
    assert not (tmp_path / "occurrences-visuel.csv").exists()
    an.outil(w, "ajouter_occurrences", {"occurrences": [good]})
    assert (tmp_path / "occurrences-visuel.csv").exists()


def test_cle_absente_echec_propre(tmp_path, monkeypatch):
    w = _work(tmp_path)
    an.VUS.append(("P1", 0, 0, 600, 600))
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    out = os.path.join(w, "res.json")
    assert an.run(w, out, "m", 1) == 1
    assert "absente" in open(out, encoding="utf-8").read()
    assert an.VUS == []
    assert "T" in (tmp_path / "agent-journal.log").read_text(encoding="utf-8").split()[0]


def test_reprise_journalisee_et_erreur_fatale(monkeypatch):
    """Une attente longue doit être discernable d'un blocage : chaque reprise est journalisée."""
    monkeypatch.setattr(an.time, "sleep", lambda *_: None)
    lignes, n = [], {"v": 0}

    class Rep:
        def __enter__(self):
            return io.BytesIO(json.dumps({"ok": 1}).encode())
        def __exit__(self, *a):
            return False

    def repond(req, timeout=0):
        n["v"] += 1
        if n["v"] < 3:
            raise urllib.error.HTTPError("u", 503, "busy", {}, io.BytesIO(b"service indisponible"))
        return Rep()

    monkeypatch.setattr(an.urllib.request, "urlopen", repond)
    assert an.appel({}, "cle", essais=3, j=lignes.append) == {"ok": 1}
    assert n["v"] == 3
    reprises = [line for line in lignes if line.startswith("reprise ")]
    assert len(reprises) == 2 and "503" in reprises[0]
    assert sum(line.startswith("API début") for line in lignes) == 3
    assert sum(line.startswith("API fin") for line in lignes) == 3

    def refuse(req, timeout=0):
        raise urllib.error.HTTPError("u", 400, "bad", {}, io.BytesIO("multimodal non activé".encode()))

    monkeypatch.setattr(an.urllib.request, "urlopen", refuse)
    with pytest.raises(RuntimeError, match="HTTP 400"):
        an.appel({}, "cle", j=lignes.append)


def test_api_defaults_are_bounded_and_logs_do_not_echo_secrets(monkeypatch):
    monkeypatch.delenv("RELEVE_NVIDIA_ATTEMPTS", raising=False)
    monkeypatch.delenv("RELEVE_NVIDIA_TIMEOUT", raising=False)
    monkeypatch.setattr(an.time, "sleep", lambda *_: None)
    timeouts, logs = [], []
    def unavailable(req, timeout):
        timeouts.append(timeout)
        raise urllib.error.HTTPError("u", 503, "busy", {}, io.BytesIO(b"echoed-secret"))
    monkeypatch.setattr(an.urllib.request, "urlopen", unavailable)
    with pytest.raises(RuntimeError, match="HTTP 503") as exc:
        an.appel({}, "echoed-secret", j=logs.append)
    assert timeouts == [120, 120]
    assert "echoed-secret" not in str(exc.value) + " ".join(logs)
    assert sum(line.startswith("API fin") for line in logs) == 2


def test_api_timeout_configuration(monkeypatch):
    monkeypatch.setenv("RELEVE_NVIDIA_ATTEMPTS", "1")
    monkeypatch.setenv("RELEVE_NVIDIA_TIMEOUT", "25")
    timeouts = []
    def timed_out(req, timeout):
        timeouts.append(timeout)
        raise TimeoutError("secret in network exception")
    monkeypatch.setattr(an.urllib.request, "urlopen", timed_out)
    with pytest.raises(RuntimeError, match="réseau : TimeoutError"):
        an.appel({}, "secret")
    assert timeouts == [25]


@pytest.mark.parametrize("model,effort,expected", [
    ("moonshotai/kimi-k3", None, "high"),
    ("moonshotai/kimi-k3", "low", "low"),
    ("moonshotai/kimi-k3", "max", "max"),
    ("z-ai/glm-5.3-flash", "low", None),
])
def test_multiturn_preserves_complete_assistant_message(tmp_path, monkeypatch, model, effort, expected):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    if effort is None:
        monkeypatch.delenv("RELEVE_NVIDIA_REASONING", raising=False)
    else:
        monkeypatch.setenv("RELEVE_NVIDIA_REASONING", effort)
    message = {"role": "assistant", "content": None, "reasoning_content": "private-reasoning-marker",
               "tool_calls": [{"id": "call-1", "type": "function", "function": {
                   "name": "lister", "arguments": '{"motif":"*.csv"}'}}]}
    requests = []
    def fake_call(body, key, **kwargs):
        requests.append(json.loads(json.dumps(body)))
        return {"choices": [{"message": message if len(requests) == 1 else {"role": "assistant", "content": ""},
                             "finish_reason": "tool_calls" if len(requests) == 1 else "length"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 20}}
    monkeypatch.setattr(an, "appel", fake_call)
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), model, 2) == 1
    assert requests[1]["messages"][2] == message
    assert all(req.get("reasoning_effort") == expected for req in requests)
    assert "private-reasoning-marker" not in (tmp_path / "agent-journal.log").read_text(encoding="utf-8")
    assert "private-reasoning-marker" not in out.read_text(encoding="utf-8")
    journal = (tmp_path / "agent-journal.log").read_text(encoding="utf-8")
    assert "finish_reason=tool_calls tool_calls=1 input_tokens=10 output_tokens=20" in journal
    assert "finish_reason=length tool_calls=0 input_tokens=10 output_tokens=20" in journal


def test_invalid_kimi_reasoning_rejected_before_api(tmp_path, monkeypatch):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    monkeypatch.setenv("RELEVE_NVIDIA_REASONING", "disabled")
    monkeypatch.setattr(an, "appel", lambda *_args, **_kwargs: pytest.fail("API must not be called"))
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "moonshotai/kimi-k3", 1) == 1
    assert "RELEVE_NVIDIA_REASONING" in json.loads(out.read_text(encoding="utf-8"))["subtype"]


@pytest.mark.parametrize("task", [None, "Review existing CSV against source diagnostics. Correct only demonstrated errors."])
def test_initial_task_override_keeps_default_and_quality_gates(tmp_path, monkeypatch, task):
    work = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    requests = []
    def fake_call(body, key, **kwargs):
        requests.append(json.loads(json.dumps(body)))
        return {"choices": [{"message": {"role": "assistant", "content": None, "tool_calls": [{
            "id": "finish", "type": "function", "function": {"name": "terminer", "arguments": '{"resume":"done"}'}}]}}]}
    monkeypatch.setattr(an, "appel", fake_call)
    an.VUS.extend([("P1", 0, 0, 600, 600), ("P1", 600, 0, 1200, 600)])
    result = tmp_path / "result.json"
    kwargs = {} if task is None else {"task": task}
    assert an.run(work, str(result), "test/model", 1, **kwargs) == 1
    expected = task if task is not None else "Relève le dossier de travail « . ». Commence par lire MANIFESTE.md."
    assert requests[0]["messages"][1] == {"role": "user", "content": expected}
    assert requests[0]["tools"] == an.OUTILS
    assert an.VUS == []
    assert an.manquantes(work)
    assert json.loads(result.read_text(encoding="utf-8"))["qualite"]["conforme"] is False
    assert "contrôle couverture : terminer refusé" in (tmp_path / "agent-journal.log").read_text(encoding="utf-8")


def test_cli_forwards_explicit_task(monkeypatch, tmp_path):
    task = "Review current occurrences using the source plan."
    monkeypatch.setattr(an.sys, "argv", ["agent_nvidia.py", str(tmp_path), "result.json", "--task", task])
    calls = []
    monkeypatch.setattr(an, "run", lambda *args, **kwargs: calls.append((args, kwargs)) or 0)
    with pytest.raises(SystemExit) as exc:
        an.main()
    assert exc.value.code == 0
    assert calls[0][1] == {"task": task}


@pytest.mark.parametrize("tools_after_two_empty,expected_calls", [(False, 6), (True, 9)])
def test_empty_replies_stop_with_quality_failure(tmp_path, monkeypatch, tools_after_two_empty, expected_calls):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    monkeypatch.setenv("RELEVE_NVIDIA_REASONING", "low")
    calls = []
    def fake_call(body, key, **kwargs):
        calls.append(body)
        message = {"role": "assistant", "content": None, "reasoning_content": "private-marker"}
        reason = "length"
        if tools_after_two_empty and len(calls) == 3:
            message["tool_calls"] = [{"id": "progress", "type": "function", "function": {
                "name": "lister", "arguments": '{"motif":"*.csv"}'}}]
            reason = "tool_calls"
        return {"choices": [{"message": message, "finish_reason": reason}]}
    monkeypatch.setattr(an, "appel", fake_call)
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "moonshotai/kimi-k3", 20) == 1
    result = json.loads(out.read_text(encoding="utf-8"))
    assert len(calls) == expected_calls
    assert result["subtype"].startswith("error_no_progress")
    assert "finish_reason=length" in result["subtype"]
    assert result["qualite"] == {"conforme": False, "erreurs": 1, "detail": "qualite.json"}
    assert result["is_error"] is True
    assert "private-marker" not in out.read_text(encoding="utf-8")


def _empty_reply():
    return {"choices": [{"message": {"role": "assistant", "content": None,
                         "reasoning_content": "old-private-history"}, "finish_reason": "stop"}]}


def _tool_reply(name, arguments):
    return {"choices": [{"message": {"role": "assistant", "content": None, "tool_calls": [
        {"id": "call", "type": "function", "function": {"name": name, "arguments": json.dumps(arguments)}}]},
        "finish_reason": "tool_calls"}]}


def test_fresh_recovery_keeps_files_task_and_can_resume_valid_tool(tmp_path, monkeypatch):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    (tmp_path / "occurrences-visuel.csv").write_bytes(b"existing-output-must-not-be-reset")
    (tmp_path / ".env").write_text("SECRET-MUST-NOT-BE-READ", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    requests = []
    def fake_call(body, *_args, **_kwargs):
        requests.append(json.loads(json.dumps(body)))
        if len(requests) <= 3:
            return _empty_reply()
        if len(requests) == 4:
            return _tool_reply("lister", {"motif": "feuilles.csv"})
        return _tool_reply("terminer", {"resume": "done"})
    monkeypatch.setattr(an, "appel", fake_call)
    monkeypatch.setattr(an, "manquantes", lambda *_: {})
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": True, "erreurs": []})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "test/model", 5, task="Continue existing takeoff; do not reset.") == 0
    assert len(requests) == 5
    fresh = requests[3]["messages"]
    assert [m["role"] for m in fresh] == ["system", "user", "user"]
    assert fresh[0] == requests[0]["messages"][0]
    assert fresh[1] == requests[0]["messages"][1]
    assert "occurrences-visuel.csv" in fresh[2]["content"]
    assert "old-private-history" not in json.dumps(fresh)
    assert "SECRET-MUST-NOT-BE-READ" not in json.dumps(fresh) and ".env" not in fresh[2]["content"]
    assert all((tmp_path / name).read_bytes() == content for name, content in before.items())
    assert json.loads(out.read_text(encoding="utf-8"))["fresh_recoveries"] == 1


def test_fresh_recovery_preserves_global_turn_budget(tmp_path, monkeypatch):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    calls = []
    monkeypatch.setattr(an, "appel", lambda body, *_a, **_kw: calls.append(body) or _empty_reply())
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "test/model", 4) == 1
    result = json.loads(out.read_text(encoding="utf-8"))
    assert len(calls) == result["num_turns"] == 4
    assert result["subtype"] == "error_max_turns"
    assert result["fresh_recoveries"] == 1


@pytest.mark.parametrize("max_turns,expected_calls,recoveries", [(3, 3, 0), (20, 7, 1)])
def test_fresh_recovery_never_restarts_twice_after_progress(tmp_path, monkeypatch, max_turns, expected_calls, recoveries):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    calls = []
    def fake_call(body, *_args, **_kwargs):
        calls.append(body)
        return _tool_reply("lister", {"motif": "feuilles.csv"}) if len(calls) == 4 else _empty_reply()
    monkeypatch.setattr(an, "appel", fake_call)
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "test/model", max_turns) == 1
    result = json.loads(out.read_text(encoding="utf-8"))
    assert len(calls) == expected_calls
    assert result["fresh_recoveries"] == recoveries
    assert result["subtype"].startswith("error_no_progress")


def test_fresh_recovery_keeps_pending_region_uncredited_and_qa_blocking(tmp_path, monkeypatch):
    w = _work(tmp_path)
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only")
    acquired = ("P1", 0, 0, 600, 600)
    pending = ("P1", 600, 0, 1200, 600)
    requests = []
    def fake_call(body, *_args, **_kwargs):
        requests.append(json.loads(json.dumps(body)))
        n = len(requests)
        if n == 1:
            an.VUS.append(acquired)
            return _tool_reply("terminer", {"resume": "not yet"})
        if n == 2:
            return _tool_reply("zoom", {"feuille": "P1", "x0": 600, "y0": 0, "x1": 1200, "y1": 600})
        if n <= 5:
            return _empty_reply()
        assert an.VUS == [acquired]
        fresh = body["messages"]
        assert len(fresh) == 3 and not any(m["role"] in {"tool", "assistant"} for m in fresh)
        assert '"regions_a_revoir": [["P1", 600, 0, 1200, 600]]' in fresh[2]["content"]
        assert '"refus_qualite": 1' in fresh[2]["content"]
        assert all(isinstance(m["content"], str) for m in fresh)
        return _tool_reply("terminer", {"resume": "still not valid"})
    monkeypatch.setattr(an, "appel", fake_call)
    monkeypatch.setattr(an, "manquantes", lambda *_: {})
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": False, "erreurs": ["unfinished"]})
    monkeypatch.setattr(an, "outil", lambda *_: (json.dumps({"feuille": "P1", "bounds_pt": list(pending[1:])}), "fake.png"))
    monkeypatch.setattr(an, "image_msg", lambda *_: {"role": "user", "content": [
        {"type": "text", "text": "pending image"}, {"type": "image_url", "image_url": {"url": "data:image/png;base64,AA=="}}]})
    out = tmp_path / "result.json"
    assert an.run(w, str(out), "test/model", 6) == 1
    assert len(requests) == 6 and an.VUS == [acquired]
    assert json.loads(out.read_text(encoding="utf-8"))["qualite"]["conforme"] is False
    assert "terminer refusé" in (tmp_path / "agent-journal.log").read_text(encoding="utf-8")


def test_image_absente_ne_tue_pas_le_releve(tmp_path):
    """Une image manquante est une erreur d'outil, pas la fin du relevé.

    Essai réel du 2026-09-29 : `apercus/HR2614plan-p01.png` avait été oublié dans la copie
    du dossier de travail. `lire` renvoyait le chemin sans vérifier, `image_msg` l'ouvrait
    hors du try du dispatch et le run mourait au 3e tour sur `subtype=erreur API`.
    """
    w = _work(tmp_path)
    texte, img = an.outil(w, "lire", {"chemin": "apercus/absente.png"})
    assert img is None
    assert "absente" in texte and texte.startswith("erreur")


def test_image_presente_est_jointe(tmp_path):
    """Contre-épreuve : une image existante est bien transmise au modèle."""
    w = _work(tmp_path)
    d = tmp_path / "apercus"; d.mkdir()
    (d / "p1.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    texte, img = an.outil(w, "lire", {"chemin": "apercus/p1.png"})
    assert img is not None and texte.startswith("image jointe")
