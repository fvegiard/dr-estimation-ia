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


def test_blocs_familles_auto_bibliotheque(tmp_path):
    """Étiquetage automatique : signature exacte → famille ; IGNORER → absente ; pictogramme proche (tolérance) → famille ;
    signature fréquente inconnue → blocs-a-etiqueter.md."""
    work = tmp_path / "w"; work.mkdir(); (work / "blocs").mkdir()
    (work / "feuilles.csv").write_text("feuille,page,role\nE1,1,plan\n", encoding="utf-8")
    sigA = json.dumps([[[0.5, 0.0, 1, False, False]], 0.0]); sigMur = json.dumps([[[0.9, 0.0, 1, True, False]], 0.0])
    sigInc = json.dumps([[[0.7, 0.1, 2, False, False]], 0.3]); sigPic = json.dumps([[[1.3, 0.0, 6, False, True], [1.9, 0.0, 6, False, True]], 0.6])
    sigPic2 = json.dumps([[[1.4, 0.0, 6, False, True], [2.0, 0.0, 6, False, True]], 0.5])      # ≤ 0,25 de sigPic
    bib = tmp_path / "bib.csv"
    with open(bib, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["signature", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles_regex", "portee", "tolerance", "source", "note"])
        w.writeheader()
        w.writerow({"signature": sigA, "label": "PRISE DOUBLE 15A", "famille": "prise", "forme": "cercle", "code": "PC", "materiel": "PRISE", "legende_no": "", "diam_min": 0, "diam_max": 99, "feuilles_regex": "", "portee": "", "tolerance": 0, "source": "t", "note": ""})
        w.writerow({"signature": sigMur, "label": "IGNORER", "famille": "", "forme": "", "code": "", "materiel": "", "legende_no": "", "diam_min": "", "diam_max": "", "feuilles_regex": "", "portee": "", "tolerance": 0, "source": "t", "note": ""})
        w.writerow({"signature": sigPic, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "legende_no": "", "diam_min": 5, "diam_max": 20, "feuilles_regex": "", "portee": "CONSERVER", "tolerance": 0.25, "source": "t", "note": ""})
    with open(work / "blocs-index.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["sig_id", "signature", "n_plans", "par_feuille", "legende", "lettre", "exemple", "diametre_pt"]); w.writeheader()
        w.writerow({"sig_id": "S001", "signature": sigA, "n_plans": 5, "par_feuille": "E1:5", "legende": "", "lettre": "", "exemple": "E1 (1,1)", "diametre_pt": 4})
        w.writerow({"sig_id": "S002", "signature": sigMur, "n_plans": 9, "par_feuille": "E1:9", "legende": "", "lettre": "", "exemple": "E1 (1,1)", "diametre_pt": 30})
        w.writerow({"sig_id": "S003", "signature": sigInc, "n_plans": 4, "par_feuille": "E1:4", "legende": "", "lettre": "", "exemple": "E1 (1,1)", "diametre_pt": 8})
    with open(work / "blocs" / "E1.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["feuille", "signature", "x_pt", "y_pt", "w_pt", "h_pt", "diametre_pt", "angle_deg", "n_parties", "trait_pt", "texte", "description"]); w.writeheader()
        w.writerow({"feuille": "E1", "signature": sigPic2, "x_pt": 50, "y_pt": 50, "w_pt": 8, "h_pt": 8, "diametre_pt": 11.3, "angle_deg": 0, "n_parties": 2, "trait_pt": 0.4, "texte": "", "description": ""})
    subprocess.run([sys.executable, os.path.join(REPO, "releve", "blocs_familles_auto.py"), str(work), "--bibliotheque", str(bib)], check=True, capture_output=True)
    fam = {r["label"]: r for r in csv.DictReader(open(work / "blocs-familles.csv", encoding="utf-8"))}
    assert fam["PRISE DOUBLE 15A"]["sig_id"] == "S001"
    assert "IGNORER" not in fam and not any(r["sig_id"] == "S002" for r in fam.values())
    assert fam["DETECTEUR FUMEE"]["portee"] == "CONSERVER" and fam["DETECTEUR FUMEE"]["sig_id"] == "S004"     # pictogramme rare apparié, ajouté à l'index
    assert "S003" in (work / "blocs-a-etiqueter.md").read_text(encoding="utf-8")
    assert any(r["sig_id"] == "S004" for r in csv.DictReader(open(work / "blocs-index.csv", encoding="utf-8")))


def _bib(path, rows):
    cols = ["signature", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles_regex", "portee", "tolerance", "source", "note"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows:
            w.writerow({**{c: "" for c in cols}, **r})


def _work(tmp_path, index_rows, blocs_rows, feuilles="E1"):
    work = tmp_path / "w"; work.mkdir(); (work / "blocs").mkdir()
    (work / "feuilles.csv").write_text("feuille,page,role\n" + "".join(f"{f},1,plan\n" for f in feuilles.split()), encoding="utf-8")
    with open(work / "blocs-index.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["sig_id", "signature", "n_plans", "par_feuille", "legende", "lettre", "exemple", "diametre_pt"]); w.writeheader(); w.writerows(index_rows)
    for f in feuilles.split():
        with open(work / "blocs" / f"{f}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["feuille", "signature", "x_pt", "y_pt", "w_pt", "h_pt", "diametre_pt", "angle_deg", "n_parties", "trait_pt", "texte", "description"]); w.writeheader()
            w.writerows([r for r in blocs_rows if r["feuille"] == f])
    return work


def _auto(work, bib):
    subprocess.run([sys.executable, os.path.join(REPO, "releve", "blocs_familles_auto.py"), str(work), "--bibliotheque", str(bib)], check=True, capture_output=True)
    return list(csv.DictReader(open(work / "blocs-familles.csv", encoding="utf-8")))


PIC = json.dumps([[[1.3, 0.0, 6, False, True], [1.9, 0.0, 6, False, True]], 0.6])
PIC2 = json.dumps([[[1.4, 0.0, 6, False, True], [2.0, 0.0, 6, False, True]], 0.5])      # ≤ 0,25 de PIC
PIC3 = json.dumps([[[1.2, 0.0, 6, False, True], [1.8, 0.0, 6, False, True]], 0.7])      # ≤ 0,25 de PIC et de PIC2
BLOC = lambda f, sg: {"feuille": f, "signature": sg, "x_pt": 50, "y_pt": 50, "w_pt": 8, "h_pt": 8, "diametre_pt": 11.3, "angle_deg": 0, "n_parties": 2, "trait_pt": 0.4, "texte": "", "description": ""}  # noqa: E731


def test_appariement_tolerant_ambigu_et_portee_contradictoire(tmp_path):
    bib = tmp_path / "bib.csv"
    _bib(bib, [{"signature": PIC, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "diam_min": 5, "diam_max": 20, "portee": "CONSERVER", "tolerance": 0.25, "source": "a"},
               {"signature": PIC3, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "diam_min": 5, "diam_max": 20, "portee": "INSTALLER", "tolerance": 0.25, "source": "b"}])
    work = _work(tmp_path, [], [BLOC("E1", PIC2)])
    fam = _auto(work, bib)
    # même appareil, portées contradictoires → relevé avec la portée par défaut de la feuille et une réserve *
    assert len(fam) == 1 and fam[0]["label"] == "DETECTEUR FUMEE" and fam[0]["portee"] == "" and "portée à confirmer" in fam[0]["reserve"]
    # labels contradictoires → ambigu, pas relevé, listé
    _bib(bib, [{"signature": PIC, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "diam_min": 5, "diam_max": 20, "tolerance": 0.25, "source": "a"},
               {"signature": PIC3, "label": "ENSEIGNE SORTIE", "famille": "urgence", "forme": "cercle", "code": "Z6", "materiel": "Z6", "diam_min": 5, "diam_max": 20, "tolerance": 0.25, "source": "b"}])
    (tmp_path / "2").mkdir()
    work2 = _work(tmp_path / "2", [], [BLOC("E1", PIC2)])
    fam2 = _auto(work2, bib)
    assert fam2 == [] and "AMBIGUS" in (work2 / "blocs-a-etiqueter.md").read_text(encoding="utf-8")


def test_restriction_de_feuilles_sans_correspondance_et_index_vide(tmp_path):
    sigA = json.dumps([[[0.5, 0.0, 1, False, False]], 0.0])
    bib = tmp_path / "bib.csv"
    _bib(bib, [{"signature": sigA, "label": "ENCASTRE", "famille": "eclairage", "forme": "cercle", "code": "EN", "materiel": "EN", "diam_min": 0, "diam_max": 99, "feuilles_regex": "E20[34]", "tolerance": 0, "source": "a"},
               {"signature": PIC, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "diam_min": 5, "diam_max": 20, "feuilles_regex": "E20[34]", "tolerance": 0.25, "source": "b"}])
    # dossier sans E203/E204 : la restriction ne devient pas « toutes les feuilles », ni pour l'index ni pour les blocs rares
    work = _work(tmp_path, [{"sig_id": "S001", "signature": sigA, "n_plans": 5, "par_feuille": "E101:5", "legende": "", "lettre": "", "exemple": "E101 (1,1)", "diametre_pt": 4}],
                 [BLOC("E101", PIC2)], feuilles="E101")
    assert _auto(work, bib) == []
    # index VIDE (en-tête seul) + un bloc rare connu : pas d'IndexError, le bloc entre dans l'index
    (tmp_path / "v").mkdir()
    work2 = _work(tmp_path / "v", [], [BLOC("E203", PIC2)], feuilles="E203")
    fam = _auto(work2, bib)
    assert [r["label"] for r in fam] == ["DETECTEUR FUMEE"] and fam[0]["feuilles"] == "E203"
    assert any(r["signature"] == PIC2 for r in csv.DictReader(open(work2 / "blocs-index.csv", encoding="utf-8")))


def test_regle_manuelle_d_un_bloc_rare_conservee_a_la_relance(tmp_path):
    bib = tmp_path / "bib.csv"
    _bib(bib, [{"signature": PIC, "label": "DETECTEUR FUMEE", "famille": "alarme", "forme": "cercle", "code": "DF", "materiel": "DF", "diam_min": 5, "diam_max": 20, "tolerance": 0.25, "source": "a"}])
    work = _work(tmp_path, [], [BLOC("E1", PIC2)])
    fam = _auto(work, bib)
    assert fam[0]["label"] == "DETECTEUR FUMEE" and fam[0]["sig_id"] == "S001"
    # correction humaine : c'est un détecteur THERMIQUE, portée ENLEVER
    fam[0].update({"label": "DETECTEUR THERMIQUE", "code": "DT", "portee": "ENLEVER", "note": "corrigé à la main"})
    with open(work / "blocs-familles.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fam[0].keys())); w.writeheader(); w.writerows(fam)
    # relance : blocs_vignettes reconstruit un index SANS la signature rare (sous le seuil) — la règle manuelle doit survivre
    with open(work / "blocs-index.csv", "w", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=["sig_id", "signature", "n_plans", "par_feuille", "legende", "lettre", "exemple", "diametre_pt"]).writeheader()
    fam2 = _auto(work, bib)
    assert [(r["sig_id"], r["label"], r["portee"]) for r in fam2] == [("S001", "DETECTEUR THERMIQUE", "ENLEVER")]
    assert any(r["sig_id"] == "S001" for r in csv.DictReader(open(work / "blocs-index.csv", encoding="utf-8")))


def test_pages_feuilles_document_source(tmp_path):
    """Chaque feuille est lue dans SON document : travail/feuilles/<F>.pdf d'abord, puis <inbox>/<fichier> page n,
    jamais « page n du PDF passé en argument » quand ce n'est pas son fichier."""
    from commun import PagesFeuilles
    inbox = tmp_path / "INBOX"; inbox.mkdir(); work = tmp_path / "travail"; (work / "feuilles").mkdir(parents=True)
    a = pymupdf.open(); a.new_page(width=100, height=100); pa = a.new_page(width=200, height=200); pa.insert_text((10, 20), "ADDENDA-2"); a.save(inbox / "addenda.pdf")
    b = pymupdf.open(); pb = b.new_page(width=300, height=300); pb.insert_text((10, 20), "PLAN-1"); b.save(inbox / "plans.pdf")
    (work / "inventaire.json").write_text(json.dumps({"inbox": str(inbox), "fichiers": []}), encoding="utf-8")
    s = pymupdf.open(); ps = s.new_page(width=400, height=400); ps.insert_text((10, 20), "SEULE"); s.save(work / "feuilles" / "E1.pdf")
    pages = PagesFeuilles(str(work), str(inbox / "plans.pdf"))
    assert "SEULE" in pages.page({"feuille": "E1", "fichier": "plans.pdf", "page": "1"}).get_text()          # page seule d'abord
    assert "ADDENDA-2" in pages.page({"feuille": "A2", "fichier": "addenda.pdf", "page": "2"}).get_text()   # son fichier, sa page
    assert "PLAN-1" in pages.page({"feuille": "P1", "fichier": "plans.pdf", "page": "1"}).get_text()
    with pytest.raises(FileNotFoundError):
        pages.page({"feuille": "X", "fichier": "inconnu.pdf", "page": "7"})
