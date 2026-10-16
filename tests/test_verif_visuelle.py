"""Tests hors réseau de releve/verif_visuelle.py (étape 4b, vision NVIDIA corrective) : extraction du JSON du
modèle, lecture de la direction, candidats vectoriels, correction d'une marque hors symbole, réserve `*` quand
aucun candidat n'est accepté, re-rendu du PDF, clé absente. Fixtures synthétiques seulement."""
import importlib.util
import json
import os
import pathlib
import sys

import pymupdf
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.estimer.render import load_input, render  # noqa: E402
from src.estimer.render.from_releve import build  # noqa: E402
from tests.test_from_releve import make_workdir  # noqa: E402

SPEC = importlib.util.spec_from_file_location("verif_visuelle", ROOT / "releve" / "verif_visuelle.py")
vv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vv)


def _dossier_rendu(tmp_path):
    """Un dossier OUTBOX synthétique : feuille P1 avec un carré (symbole) à (100, 100) sous la marque « Detecteur
    fumee » et un carré à (170, 300) à GAUCHE de la marque « Klaxon » (200, 300) posée sur du vide."""
    work = make_workdir(tmp_path)
    p1 = work / "feuilles" / "P1.pdf"
    doc = pymupdf.open(str(p1))
    page = doc[0]
    page.draw_rect(pymupdf.Rect(94, 94, 106, 106), color=(0, 0, 0), width=0.8)
    page.draw_rect(pymupdf.Rect(164, 294, 176, 306), color=(0, 0, 0), width=0.8)
    page.insert_text((195, 303), "K", fontsize=6)
    doc.save(str(p1), incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    out = tmp_path / "out"
    vec = out / "vecteur"
    build(work, vec)
    sheets = load_input(vec)
    rep = render(sheets, vec / "plans.pdf", out / "T-Plans-annotes.pdf", log=lambda *a, **k: None)
    (out / "T-rendu-rapport.json").write_text(json.dumps(rep), encoding="utf-8")
    return out


def _juge_scripte(scenario):
    """Remplace `juger` : le scénario décide par le libellé ; les aperçus de candidats sont reconnus par
    leur pastille synthétique (fenêtre = FENETRE et appel après un verdict négatif)."""
    appels = []

    def juger(png, modele, cle, fenetre, j=None):
        appels.append(fenetre)
        return scenario(png, fenetre, appels)
    return juger, appels


def test_extraire_json_tolere_cloture_et_prose():
    assert vv.extraire_json('```json\n{"sur_symbole": true, "confiance": 1}\n```')["sur_symbole"] is True
    assert vv.extraire_json('Voici : {"sur_symbole": false}')["sur_symbole"] is False
    with pytest.raises(ValueError):
        vv.extraire_json("aucun json")


def test_direction_lue_dans_le_texte():
    assert vv.direction("boîtier DP1, gauche, 30 points") == (-1.0, 0.0)
    dx, dy = vv.direction("symbole en haut à droite, 20 pt")
    assert dx > 0 and dy < 0
    assert vv.direction("") is None
    assert vv.direction("boîtier DP1, 30 points") is None


def test_candidats_filtres_par_direction(tmp_path):
    out = _dossier_rendu(tmp_path)
    page = pymupdf.open(str(out / "vecteur" / "plans.pdf"))[0]
    idx = vv.SymbolIndex(page)
    a_gauche = vv.candidats(idx, 200, 300, (-1.0, 0.0))
    assert a_gauche and abs(a_gauche[0][0] - 170) < 1 and abs(a_gauche[0][1] - 300) < 1
    assert vv.candidats(idx, 200, 300, (1.0, 0.0)) == []            # rien à droite
    assert vv.candidats(idx, 100, 100, None) == []                  # le carré sous la marque (d < 2) n'est pas un candidat


def test_marque_hors_symbole_corrigee_et_pdf_re_rendu(tmp_path, monkeypatch):
    out = _dossier_rendu(tmp_path)
    avant = (out / "T-Plans-annotes.pdf").stat().st_mtime_ns
    est = json.loads((out / "vecteur" / "estimate.json").read_text(encoding="utf-8"))
    klaxon = next(e for c in est["counters"] for e in c["elements"] if c["family"].lower().startswith("klaxon"))
    assert (klaxon["x"], klaxon["y"]) == (200.0, 300.0)

    def scenario(png, fenetre, appels):
        n = len(appels)
        # ordre des appels : chaque marque est jugée une fois ; Klaxon est négatif (2 jugements), puis l'aperçu
        # du candidat à (170, 300) est accepté. Les marques sont traitées en série (parallele=1).
        if n in (3, 4):          # Klaxon : verdict puis confirmation, tous deux négatifs
            return {"sur_symbole": False, "pastille_visible": True, "symbole_decrit": "lettre K",
                    "symbole_proche": "carré, gauche, 30 points", "confiance": 0.9, "brut": ""}
        return {"sur_symbole": True, "pastille_visible": True, "symbole_decrit": "carré", "symbole_proche": "",
                "confiance": 1.0, "brut": ""}
    juger, appels = _juge_scripte(scenario)
    monkeypatch.setattr(vv, "juger", juger)
    r = vv.executer(out, "T", "modele-test", "cle", parallele=1, j=lambda *a: None)
    assert r["marques"] == 7 and r["corrigees"] == 1 and r["reserves"] == 0 and r["pdf_re_rendu"] is True
    assert r["reperes_corriges"] == ["P1 I02-01"] or len(r["reperes_corriges"]) == 1
    est = json.loads((out / "vecteur" / "estimate.json").read_text(encoding="utf-8"))
    klaxon = next(e for c in est["counters"] for e in c["elements"] if c["family"].lower().startswith("klaxon"))
    assert abs(klaxon["x"] - 170) < 1 and abs(klaxon["y"] - 300) < 1 and "corrigee" in klaxon["note"]
    assert (out / "T-Plans-annotes.pdf").stat().st_mtime_ns >= avant
    assert (out / "T-verification-visuelle.json").exists() and (out / "T-verification-visuelle.md").exists()
    assert (out / "verification-visuelle").is_dir() and list((out / "verification-visuelle").glob("*.png"))
    rapport = json.loads((out / "T-rendu-rapport.json").read_text(encoding="utf-8"))
    assert rapport["verification_visuelle"]["corrigees"] == 1


def test_sans_candidat_accepte_la_marque_passe_en_reserve(tmp_path, monkeypatch):
    out = _dossier_rendu(tmp_path)

    def scenario(png, fenetre, appels):
        n = len(appels)
        if n >= 3:               # Klaxon négatif, confirmation négative, candidat refusé
            return {"sur_symbole": False, "pastille_visible": True, "symbole_decrit": "texte",
                    "symbole_proche": "carré, gauche, 30 points", "confiance": 0.8, "brut": ""}
        return {"sur_symbole": True, "pastille_visible": True, "symbole_decrit": "carré", "symbole_proche": "",
                "confiance": 1.0, "brut": ""}
    juger, appels = _juge_scripte(scenario)
    monkeypatch.setattr(vv, "juger", juger)
    r = vv.executer(out, "T", "modele-test", "cle", parallele=1, max_marques=3, j=lambda *a: None)
    assert r["marques"] == 3 and r["reserves"] == 1 and r["corrigees"] == 0
    est = json.loads((out / "vecteur" / "estimate.json").read_text(encoding="utf-8"))
    klaxon = next(e for c in est["counters"] for e in c["elements"] if c["family"].lower().startswith("klaxon"))
    assert vv.REVALIDER in klaxon["flags"] and "hors symbole" in klaxon["note"]
    assert (klaxon["x"], klaxon["y"]) == (200.0, 300.0)           # jamais déplacée sans candidat accepté
    md = (out / "T-verification-visuelle.md").read_text(encoding="utf-8")
    assert "reserve" in md and "Score : 2/3" in md


def test_sans_correction_ne_deplace_jamais(tmp_path, monkeypatch):
    out = _dossier_rendu(tmp_path)
    monkeypatch.setattr(vv, "juger", lambda *a, **k: {"sur_symbole": False, "pastille_visible": True,
                                                      "symbole_decrit": "", "symbole_proche": "gauche 30 points",
                                                      "confiance": 1.0, "brut": ""})
    r = vv.executer(out, "T", "m", "cle", parallele=1, max_marques=3, corriger=False, j=lambda *a: None)
    assert r["corrigees"] == 0 and r["reserves"] == 3


def test_verdict_negatif_isole_ne_compte_pas(tmp_path, monkeypatch):
    """Un faux négatif du modèle (vu sur TEST-E103) est rattrapé par le second jugement."""
    out = _dossier_rendu(tmp_path)

    def scenario(png, fenetre, appels):
        neg = fenetre == vv.FENETRE and len(appels) == 1
        return {"sur_symbole": not neg, "pastille_visible": True, "symbole_decrit": "carré",
                "symbole_proche": "", "confiance": 1.0, "brut": ""}
    juger, appels = _juge_scripte(scenario)
    monkeypatch.setattr(vv, "juger", juger)
    r = vv.executer(out, "T", "m", "cle", parallele=1, max_marques=1, j=lambda *a: None)
    assert r["ok"] == 1 and r["reserves"] == 0 and r["pdf_re_rendu"] is False
    assert r["verdicts"][0]["etat"].startswith("ok") and r["verdicts"][0]["confirmation"] is not None


def test_dry_run_sans_cle_et_cli(tmp_path, monkeypatch):
    out = _dossier_rendu(tmp_path)
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", ["verif_visuelle.py", str(out), "T"])
    assert vv.main() == 4                                            # non exécutée, jamais une exception
    monkeypatch.setattr(sys, "argv", ["verif_visuelle.py", str(out), "T", "--dry-run"])
    assert vv.main() == 0
    assert len(list((out / "verification-visuelle").glob("*.png"))) == 7


def test_reprise_journalisee_et_erreur_fatale(monkeypatch):
    import io
    import urllib.error
    monkeypatch.setattr(vv.time, "sleep", lambda *_: None)
    etats = iter([503, 200])
    lignes = []

    def repond(req, timeout=0):
        code = next(etats)
        if code != 200:
            raise urllib.error.HTTPError(req.full_url, code, "busy", {}, io.BytesIO(b"ResourceExhausted"))
        return io.BytesIO(b'{"ok": 1}')
    monkeypatch.setattr(vv.urllib.request, "urlopen", repond)
    assert vv.appel({}, "cle", j=lignes.append) == {"ok": 1}
    assert lignes and "503" in lignes[0]
    monkeypatch.setattr(vv.urllib.request, "urlopen",
                        lambda req, timeout=0: (_ for _ in ()).throw(
                            urllib.error.HTTPError(req.full_url, 401, "no", {}, io.BytesIO(b"bad key"))))
    with pytest.raises(RuntimeError, match="HTTP 401"):
        vv.appel({}, "cle")


def test_chaine_de_modeles_repli_sur_echec_seulement(monkeypatch):
    """m2 ne juge que si m1 a échoué (HTTP, sans JSON, tronqué) ; un verdict rendu par m1 n'est jamais contredit."""
    vus = []

    def appel(corps, cle, essais=5, j=None):
        vus.append(corps["model"])
        if corps["model"] == "m1-casse":
            raise RuntimeError("HTTP 500 : Failed to generate completions")
        if corps["model"] == "m1-tronque":
            return {"choices": [{"finish_reason": "length", "message": {"content": "", "reasoning_content": "..."}}]}
        return {"choices": [{"finish_reason": "stop", "message": {"content": '{"sur_symbole": true, "confiance": 0.9}'}}]}
    monkeypatch.setattr(vv, "appel", appel)
    v = vv.juger(b"png", "m1-casse,m2", "cle", 120.0)
    assert v["modele"] == "m2" and v["sur_symbole"] is True and vus == ["m1-casse", "m2"]
    vus.clear()
    v = vv.juger(b"png", "m1-tronque,m2", "cle", 120.0)
    assert v["modele"] == "m2" and vus == ["m1-tronque", "m2"]
    vus.clear()
    v = vv.juger(b"png", "m2,m1-casse", "cle", 120.0)
    assert v["modele"] == "m2" and vus == ["m2"]                 # m1-casse jamais appelé : m2 a jugé
    with pytest.raises(RuntimeError, match="aucun modèle"):
        vv.juger(b"png", "m1-casse,m1-tronque", "cle", 120.0)
    assert vv.MAX_TOKENS >= 6000 and vv.PARALLELE == 1
