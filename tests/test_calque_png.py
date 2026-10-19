"""Revues Codex/Copilot PR #25 : le calque PNG doit isoler les calques OCG « RELEVE » — supprimer les images laissait
tout un plan VECTORIEL (traits, textes, calques CAO) dans le calque « transparent » ; et la page de chaque feuille dans
« Plans annotés » est `plan_page` du rapport de rendu, pas la page d'avant insertion des bordereaux."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from test_from_releve import make_workdir  # noqa: E402
from src.estimer.render.from_releve import build  # noqa: E402
from src.estimer.render import load_input, render  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def _rendu(tmp_path):
    work = make_workdir(tmp_path)
    out = tmp_path / "out"
    build(work, out)
    pdf = tmp_path / "rendu.pdf"
    rep = render(load_input(out), out / "plans.pdf", pdf)
    (tmp_path / "rendu-rapport.json").write_text(json.dumps(rep), encoding="utf-8")
    return work, out, pdf, rep


def test_calque_vectoriel_sans_fond(tmp_path):
    work, out, pdf, rep = _rendu(tmp_path)
    assert [s["plan_page"] for s in rep["sheets"]] == [1, 4]       # bordereaux insérés après la 1re feuille
    for sh in rep["sheets"]:
        r = subprocess.run([sys.executable, str(REPO / "releve" / "calque_png.py"), str(pdf), str(tmp_path / "png"),
                            "--page", str(sh["plan_page"]), "--nom", sh["sheet"], "--largeur", "800"],
                           capture_output=True, text=True, cwd=REPO)
        assert r.returncode == 0, r.stderr
        calque = np.array(Image.open(tmp_path / "png" / f"{sh['sheet']}_calque.png"))
        annote = np.array(Image.open(tmp_path / "png" / f"{sh['sheet']}_annote.png"))
        assert calque.shape[2] == 4 and annote.shape[2] == 3
        # le fond vectoriel (titre + trait du gabarit) est parti : le calque est très majoritairement transparent,
        # mais pas vide (pastilles + encadré RELEVE)
        opaque = (calque[..., 3] > 0).mean()
        assert 0.01 < opaque < 0.5, opaque
    # le PDF source est intact (le script modifie sa copie en mémoire seulement)
    doc = pymupdf.open(pdf)
    assert "DSI01" in doc[0].get_text()


def test_calque_refuse_un_pdf_sans_calque_releve(tmp_path):
    work, out, pdf, rep = _rendu(tmp_path)
    r = subprocess.run([sys.executable, str(REPO / "releve" / "calque_png.py"), str(out / "plans.pdf"), str(tmp_path / "png"),
                        "--page", "1", "--largeur", "400"], capture_output=True, text=True, cwd=REPO)   # plan d'avant rendu : aucune OCG
    assert r.returncode != 0 and "RELEVE" in (r.stderr + r.stdout)


def test_planche_controle_lit_plan_page_du_rapport(tmp_path):
    work, out, pdf, rep = _rendu(tmp_path)
    r = subprocess.run([sys.executable, str(REPO / "releve" / "planche_controle.py"), str(pdf), str(out / "estimate.json"),
                        str(tmp_path / "controle"), "--rapport", str(tmp_path / "rendu-rapport.json"), "--zoom", "2"],
                       capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stderr
    planches = sorted(p.name for p in (tmp_path / "controle").glob("*.png"))
    assert planches == ["DSI01-planche-01.png", "E01-planche-01.png"]
