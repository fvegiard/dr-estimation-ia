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


def test_structured_occurrences_escape_commas(tmp_path):
    w = _work(tmp_path)
    row = {"feuille": "P1", "label": "KLAXON", "x_pt": 12.5, "y_pt": 23.75, "note": "[K1.1], corridor"}
    an.outil(w, "ajouter_occurrences", {"occurrences": [row]})
    with (tmp_path / "occurrences-visuel.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1 and rows[0]["note"] == row["note"]
    assert rows[0]["source"] == "visuel" and None not in rows[0]


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


@pytest.mark.parametrize("tools_after_two_empty,expected_calls", [(False, 3), (True, 6)])
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
