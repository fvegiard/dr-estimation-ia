"""Blocs vectoriels (revue Copilot/Codex PR #27) : lettre contenue relative au bloc et jamais un texte de fond, bloc plat
rejeté, contraintes de fusion sur la composante, identifiants de signature cumulatifs."""
import csv, json, os, subprocess, sys
import pymupdf
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "releve"))
import blocs_vectoriels as bv  # noqa: E402


def _page_avec(dessin):
    doc = pymupdf.open(); page = doc.new_page(width=400, height=400)
    dessin(page.new_shape(), page)
    return doc, page


def test_lettre_centree_relative_et_texte_de_fond_exclu():
    def dessin(sh, page):
        sh.draw_rect(pymupdf.Rect(100, 100, 124, 124)); sh.finish(width=0.5); sh.commit()     # carré 24 pt, lettres ANN
        page.insert_text((104, 116), "ANN", fontsize=9, color=(0, 0, 0))
        sh = page.new_shape(); sh.draw_rect(pymupdf.Rect(200, 100, 208, 108)); sh.finish(width=0.5); sh.commit()   # carré 8 pt, lettre F
        page.insert_text((202, 106.5), "F", fontsize=5, color=(0.25, 0.25, 0.25))
        sh = page.new_shape(); sh.draw_circle((300, 300), 9); sh.finish(width=0.7); sh.commit()                   # moteur sous « STR » gris clair
        page.insert_text((292, 303), "STR", fontsize=8, color=(0.75, 0.75, 0.75))
    doc, page = _page_avec(dessin)
    blocs = bv.texte_dans(bv.blocs_page(page), page)
    par = {(round(b["x_pt"]), round(b["y_pt"])): json.loads(b["signature"]) for b in blocs}
    assert par[(112, 112)][2] == "ANN"          # gros bloc : lettre acceptée (critère relatif, pas 14 pt absolus)
    assert par[(204, 104)][2] == "F"
    assert len(par[(300, 300)]) == 2            # texte de fond gris clair : pas de lettre dans la signature


def test_bloc_plat_rejete_et_segments_colineaires():
    def dessin(sh, page):
        sh.draw_line((50, 50), (70, 50)); sh.draw_line((72, 50), (90, 50)); sh.finish(width=0.3); sh.commit()   # deux traits colinéaires
        sh = page.new_shape(); sh.draw_rect(pymupdf.Rect(200, 200, 240, 210)); sh.draw_line((205, 205), (235, 205)); sh.finish(width=0.4); sh.commit()
    doc, page = _page_avec(dessin)
    blocs = bv.blocs_page(page)
    assert all(min(b["w_pt"], b["h_pt"]) >= 0.5 for b in blocs)
    assert any(abs(b["x_pt"] - 220) < 1 for b in blocs)


def test_fusion_bornee_par_la_composante():
    # chaîne de 25 petits « V » ouverts (8 pt) qui se touchent sur 200 pt : jamais un bloc > max_cote (60), même par
    # chaînage de paires toutes admissibles deux à deux
    def dessin(sh, page):
        for i in range(25):
            sh = page.new_shape(); x = 20 + i * 8
            sh.draw_polyline([(x, 100), (x + 4, 106), (x + 8, 100)]); sh.finish(width=0.4); sh.commit()
    doc, page = _page_avec(dessin)
    blocs = bv.blocs_page(page, max_cote=60)
    assert blocs and all(b["w_pt"] <= 60 for b in blocs)
    assert sum(1 for b in blocs) >= 4


def test_sig_id_cumulatifs(tmp_path):
    work = tmp_path / "w"; work.mkdir(); (work / "blocs").mkdir()
    (work / "feuilles.csv").write_text("feuille,page,role\nE1,1,plan\n", encoding="utf-8")
    sigA, sigB = json.dumps([[[0.5, 0.0, 1, False, False]], 0.0]), json.dumps([[[0.9, 0.0, 1, True, False]], 0.0])
    pdf = tmp_path / "p.pdf"; d = pymupdf.open(); d.new_page(width=200, height=200); d.save(pdf)

    def ecrire(sigs):
        json.dump({s: {"par_feuille": {"E1": 3}} for s in sigs}, open(work / "blocs-signatures.json", "w"))
        with open(work / "blocs" / "E1.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["feuille", "signature", "x_pt", "y_pt", "w_pt", "h_pt", "diametre_pt", "angle_deg", "n_parties", "trait_pt", "texte", "description"])
            w.writeheader()
            for s in sigs:
                for k in range(3):
                    w.writerow({"feuille": "E1", "signature": s, "x_pt": 50 + 20 * k, "y_pt": 50, "w_pt": 8, "h_pt": 8, "diametre_pt": 11.3, "angle_deg": 0, "n_parties": 1, "trait_pt": 0.4, "texte": "", "description": ""})
        subprocess.run([sys.executable, os.path.join(REPO, "releve", "blocs_vignettes.py"), str(work), str(pdf), str(tmp_path / "s"), "--min", "1"], check=True, capture_output=True)
        return {r["signature"]: r["sig_id"] for r in csv.DictReader(open(work / "blocs-index.csv", encoding="utf-8"))}

    i1 = ecrire([sigA, sigB]); i2 = ecrire([sigB]); i3 = ecrire([sigA, sigB])
    assert i1[sigA] == "S001" and i1[sigB] == "S002"
    assert i2[sigB] == "S002"
    assert i3[sigA] == "S001" and i3[sigB] == "S002"      # une signature disparue puis revenue garde son identifiant
