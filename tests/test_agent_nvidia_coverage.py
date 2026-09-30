"""Coverage means image delivery, never merely a successful local render.

All requests are mocked. These checks do not claim the model understood an image.
"""
import base64
import copy
import importlib.util
import json
from pathlib import Path

import pytest


SPEC = importlib.util.spec_from_file_location(
    "agent_nvidia_coverage", Path(__file__).resolve().parents[1] / "releve" / "agent_nvidia.py")
an = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(an)


def _call(name, args, identifier):
    return {"id": identifier, "type": "function", "function": {
        "name": name, "arguments": json.dumps(args)}}


def _reply(calls):
    return {"choices": [{"message": {"role": "assistant", "content": None, "tool_calls": calls},
                         "finish_reason": "tool_calls"}]}


def _work(tmp_path, monkeypatch, windows=1):
    (tmp_path / "feuilles.csv").write_text(
        f"feuille,largeur_pt,hauteur_pt\nP1,{windows * 600},600\n", encoding="utf-8")
    (tmp_path / "feuilles-classement.csv").write_text("feuille,type\nP1,plan\n", encoding="utf-8")
    (tmp_path / "nomenclature.csv").write_text("label,famille\nLIGHT,luminaire\n", encoding="utf-8")
    monkeypatch.setenv("NVIDIA_API_KEY", "unit-test-only")
    monkeypatch.setattr(an, "controler", lambda *_: {"conforme": True, "erreurs": []})
    rendered = {}

    def fake_render(workdir, name, args):
        assert name == "zoom"
        # Distinct bytes identify exactly which region appears in an API payload.
        region = tuple(args)
        image = tmp_path / f"zoom-{args[1]}.png"
        image.write_bytes(repr(region).encode())
        rendered[region] = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode()
        return 0, str(image)

    monkeypatch.setattr(an, "script", fake_render)
    an.VUS.clear()
    return str(tmp_path), rendered


def _zoom(index):
    return _call("zoom", dict(feuille="P1", x0=index * 600, y0=0,
                               x1=(index + 1) * 600, y1=600), f"zoom-{index}")


def _images(requests):
    return {part["image_url"]["url"] for req in requests for msg in req["messages"]
            if isinstance(msg.get("content"), list) for part in msg["content"]
            if part.get("type") == "image_url"}


@pytest.mark.parametrize('width,height', [(1200.5, 600), (600, 1200.5), (1200.5, 1200.5), (0.5, 0.5)])
def test_fractional_page_edges_remain_missing_until_delivered(tmp_path, monkeypatch, width, height):
    work, _ = _work(tmp_path, monkeypatch)
    monkeypatch.setattr(an, 'feuilles_plan', lambda _: [('P1', width, height)])
    missing = an.manquantes(work)['P1']
    assert max(r[2] for r in missing) == width
    assert max(r[3] for r in missing) == height
    assert all(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height for x0, y0, x1, y1 in missing)
    an.VUS[:] = [('P1', *r) for r in missing if r[2] <= int(width) and r[3] <= int(height)]
    assert 'P1' in an.manquantes(work), 'Fractional edge strips have not been delivered'
    an.VUS[:] = [('P1', *r) for r in missing]
    assert an.manquantes(work) == {}


def test_local_zoom_render_without_api_delivery_does_not_credit_coverage(tmp_path, monkeypatch):
    work, _ = _work(tmp_path, monkeypatch)
    args = json.loads(_zoom(0)["function"]["arguments"])
    _, image = an.outil(work, "zoom", args)
    assert image and Path(image).is_file()
    assert an.VUS == [], "Rendering locally is not delivery to the model"
    assert an.manquantes(work) == {"P1": [(0, 0, 600, 600)]}


def test_five_zoom_batch_cannot_credit_an_image_never_sent(tmp_path, monkeypatch):
    work, rendered = _work(tmp_path, monkeypatch, windows=5)
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        return _reply([_zoom(i) for i in range(5)] if len(requests) == 1 else [
            _call("terminer", {"resume": "done"}, "finish")])

    monkeypatch.setattr(an, "appel", fake_api)
    an.run(work, str(tmp_path / "result.json"), "unit-test/model", 2)
    delivered = _images(requests)
    unproven = [region for region in an.VUS if rendered[tuple(region)] not in delivered]
    assert unproven == [], f"Coverage credited images never sent: {unproven}"
    result = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))
    if result["subtype"] == "success":
        assert set(rendered.values()) <= delivered


@pytest.mark.parametrize("same_batch", [True, False])
def test_unsubmitted_or_unreadable_image_cannot_finish(tmp_path, monkeypatch, same_batch):
    work, _ = _work(tmp_path, monkeypatch)
    requests = []
    finish = _call("terminer", {"resume": "done"}, "finish")

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        if len(requests) == 1:
            return _reply([_zoom(0), finish] if same_batch else [_zoom(0)])
        return _reply([finish])

    monkeypatch.setattr(an, "appel", fake_api)
    if not same_batch:
        def unreadable(*_):
            raise OSError("image unreadable in test")
        monkeypatch.setattr(an, "image_msg", unreadable)
    code = an.run(work, str(tmp_path / "result.json"), "unit-test/model", 1 if same_batch else 2)
    assert not _images(requests)
    assert code == 1, "terminer must refuse regions whose images were never delivered"
    assert an.manquantes(work)


def test_one_delivered_zoom_can_finish_with_independent_quality_pass(tmp_path, monkeypatch):
    work, rendered = _work(tmp_path, monkeypatch)
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        return _reply([_zoom(0)] if len(requests) == 1 else [
            _call("terminer", {"resume": "done"}, "finish")])

    monkeypatch.setattr(an, "appel", fake_api)
    assert an.run(work, str(tmp_path / "result.json"), "unit-test/model", 2) == 0
    assert set(rendered.values()) <= _images(requests)
    assert an.manquantes(work) == {}


def test_batch_freezes_each_zoom_before_shared_image_path_is_overwritten(tmp_path, monkeypatch):
    work, _ = _work(tmp_path, monkeypatch, windows=2)
    requests, rendered = [], {}

    def render_same_path(workdir, name, args):
        assert name == "zoom"
        region = tuple(args)
        # Like zoom.py's integer-based names, these fractional crops collide.
        image = tmp_path / ("zoom-" + "-".join(str(int(v)) for v in args[1:]) + ".png")
        image.write_bytes(repr(region).encode())
        rendered[region] = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode()
        return 0, str(image)

    calls = [_call("zoom", dict(feuille="P1", x0=x, y0=0, x1=x + 599, y1=599), f"zoom-{i}")
             for i, x in enumerate((0.1, 0.2))]

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        return _reply(calls if len(requests) == 1 else [_call("couverture", {}, "coverage")])

    monkeypatch.setattr(an, "script", render_same_path)
    monkeypatch.setattr(an, "appel", fake_api)
    an.run(work, str(tmp_path / "result.json"), "unit-test/model", 2)
    assert len(list(tmp_path.glob("zoom-*.png"))) == 1, "Fixture must overwrite one path"
    assert len(rendered) == 2 and len(set(rendered.values())) == 2
    assert _images(requests) == set(rendered.values()), "Each crop's original bytes must reach the API"
    assert set(an.VUS) == set(rendered), "Credited regions must match the distinct delivered crops"
    batch = requests[1]["messages"][3:]
    assert [message["role"] for message in batch] == ["tool", "tool", "user", "user"]
    assert [message["tool_call_id"] for message in batch[:2]] == ["zoom-0", "zoom-1"]


def test_failed_api_exchange_does_not_confirm_image_delivery(tmp_path, monkeypatch):
    work, _ = _work(tmp_path, monkeypatch)
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        if len(requests) == 1:
            return _reply([_zoom(0)])
        raise TimeoutError("mock provider response unavailable")

    monkeypatch.setattr(an, "appel", fake_api)
    assert an.run(work, str(tmp_path / "result.json"), "unit-test/model", 2) == 1
    assert _images(requests), "Fixture must attempt to submit the image"
    assert an.VUS == [], "An unsuccessful API exchange cannot confirm delivery"
    assert an.manquantes(work)


def test_empty_api_reply_does_not_confirm_image_coverage(tmp_path, monkeypatch):
    work, _ = _work(tmp_path, monkeypatch)
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        return _reply([_zoom(0)] if len(requests) == 1 else [])

    monkeypatch.setattr(an, "appel", fake_api)
    assert an.run(work, str(tmp_path / "result.json"), "unit-test/model", 2) == 1
    assert _images(requests)
    assert an.VUS == []
    assert an.manquantes(work)


def test_delivered_regions_survive_context_eviction_without_duplicate_credit(tmp_path, monkeypatch):
    work, rendered = _work(tmp_path, monkeypatch, windows=5)
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        number = len(requests)
        return _reply([_zoom(number - 1)] if number <= 5 else [
            _call("terminer", {"resume": "done"}, "finish")])

    monkeypatch.setattr(an, "appel", fake_api)
    assert an.run(work, str(tmp_path / "result.json"), "unit-test/model", 6) == 0
    assert set(rendered.values()) <= _images(requests)
    assert len(_images([requests[-1]])) == 4
    assert len(an.VUS) == len(set(an.VUS)) == 5
    assert an.manquantes(work) == {}
    for request in requests:
        for message in request["messages"]:
            if isinstance(message.get("content"), list):
                assert set(message) == {"role", "content"}, "Private coverage tracking must not enter API messages"


@pytest.mark.parametrize('side,credited', [(600.0000000000002, True), (601.0, False)])
def test_window_width_float_noise_does_not_drop_delivered_zoom(tmp_path, monkeypatch, side, credited):
    work, _ = _work(tmp_path, monkeypatch, windows=2)
    (tmp_path / 'feuilles.csv').write_text('feuille,largeur_pt,hauteur_pt\nP1,1200,1200\n', encoding='utf-8')
    requests = []

    def fake_api(body, key, **kwargs):
        requests.append(copy.deepcopy(body))
        if len(requests) == 1:
            return _reply([_call('zoom', dict(feuille='P1', x0=0, y0=0, x1=side, y1=side), 'zoom')])
        return _reply([_call('couverture', {}, 'coverage')])

    monkeypatch.setattr(an, 'appel', fake_api)
    an.run(work, str(tmp_path / 'result.json'), 'unit-test/model', 2)
    assert _images(requests)
    assert bool(an.VUS) is credited


@pytest.mark.parametrize('side,covered', [(600.0000000000002, True), (601.0, False)])
def test_coverage_union_tolerates_roundoff_but_not_larger_windows(tmp_path, monkeypatch, side, covered):
    work, _ = _work(tmp_path, monkeypatch, windows=2)
    (tmp_path / 'feuilles.csv').write_text('feuille,largeur_pt,hauteur_pt\nP1,1200,1200\n', encoding='utf-8')
    an.VUS.extend([('P1', 0, 0, side, side), ('P1', 600, 0, 1200, 600),
                   ('P1', 0, 600, 600, 1200), ('P1', 600, 600, 1200, 1200)])
    assert (an.manquantes(work) == {}) is covered
