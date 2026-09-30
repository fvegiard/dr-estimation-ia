"""Tests hors réseau de releve/agent_nvidia.py : confinement au dossier de travail, sorties autorisées, contrôle de couverture, reprises journalisées."""
import importlib.util
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
    an.VUS.clear(); an.VUS.append(("P1", 0, 0, 600, 600))
    assert an.manquantes(w)["P1"] == [(600, 0, 1200, 600)]
    an.VUS.append(("P1", 600, 0, 1200, 600))
    assert an.manquantes(w) == {}


def test_cle_absente_echec_propre(tmp_path, monkeypatch):
    w = _work(tmp_path)
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    out = os.path.join(w, "res.json")
    assert an.run(w, out, "m", 1) == 1
    assert "absente" in open(out, encoding="utf-8").read()


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
    assert an.appel({}, "cle", j=lignes.append) == {"ok": 1}
    assert n["v"] == 3
    assert [l[:8] for l in lignes] == ["reprise ", "reprise "] and "503" in lignes[0]

    def refuse(req, timeout=0):
        raise urllib.error.HTTPError("u", 400, "bad", {}, io.BytesIO("multimodal non activé".encode()))

    monkeypatch.setattr(an.urllib.request, "urlopen", refuse)
    with pytest.raises(RuntimeError, match="HTTP 400"):
        an.appel({}, "cle", j=lignes.append)
