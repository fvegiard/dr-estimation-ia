"""Repères lus dans la boîte (blocs_etiquettes_texte.py) : un bloc inconnu de 6 à 24 pt qui contient un repère
`AAA99` est un appareil ; sa famille est le repère, son matériel le texte lu sous la boîte, son numéro le « #NN »."""
import csv, json, os, subprocess, sys
import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "releve"))
import blocs_vectoriels as bv  # noqa: E402

SCRIPT = os.path.join(REPO, "releve", "blocs_etiquettes_texte.py")


def _dossier(tmp_path):
    """Feuille E1 : 2 boîtes DP1 (+ matériel et #NN), 1 SW1, un grand meuble « J1 » et un carré « A » : seuls les 3 appareils comptent."""
    work = tmp_path / "travail"; (work / "feuilles").mkdir(parents=True); (work / "blocs").mkdir()
    doc = pymupdf.open(); page = doc.new_page(width=600, height=400)
    for (x, y, tag, num, mat) in ((100, 100, "DP1", "#30", "NPP16 D EFP 347"), (300, 100, "DP1", "#31", "NPP16 D EFP 347"),
                                  (100, 250, "SW1", "#34", "NPODMA WH")):
        sh = page.new_shape(); sh.draw_rect(pymupdf.Rect(x, y, x + 12, y + 12)); sh.finish(width=0.7); sh.commit()
        page.insert_text((x + 1, y + 8.5), tag, fontsize=5)
        page.insert_text((x - 12, y + 20), mat, fontsize=5)
        page.insert_text((x + 1, y + 26), num, fontsize=5)
    sh = page.new_shape(); sh.draw_rect(pymupdf.Rect(400, 200, 460, 240)); sh.finish(width=0.7); sh.commit()
    page.insert_text((420, 222), "J1", fontsize=8)                      # meuble : trop grand pour un appareil
    sh = page.new_shape(); sh.draw_rect(pymupdf.Rect(500, 300, 512, 312)); sh.finish(width=0.7); sh.commit()
    page.insert_text((503, 309), "A", fontsize=6)                       # lettre seule : pas un repère AAA99
    doc.save(str(work / "feuilles" / "E1.pdf"))
    blocs = bv.texte_dans(bv.blocs_page(page), page)
    with open(work / "blocs" / "E1.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["feuille", "signature", "x_pt", "y_pt", "w_pt", "h_pt"], extrasaction="ignore")
        w.writeheader(); w.writerows({"feuille": "E1", **b} for b in blocs)
    (work / "feuilles.csv").write_text("feuille,role,fichier,page\nE1,plan,E1.pdf,1\n", encoding="utf-8")
    return work


def _lancer(work, biblio):
    r = subprocess.run([sys.executable, SCRIPT, str(work), "--bibliotheque", str(biblio)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return list(csv.DictReader(open(work / "blocs-etiquettes-auto.csv", encoding="utf-8")))


def test_appareils_lus_par_repere_materiel_et_numero(tmp_path):
    work = _dossier(tmp_path)
    lignes = _lancer(work, tmp_path / "absente.csv")
    assert sorted(r["label"] for r in lignes) == ["DP1", "DP1", "SW1"]          # ni « J1 » (trop grand) ni « A » (pas un repère)
    dp1 = [r for r in lignes if r["label"] == "DP1"]
    assert {r["materiel"] for r in dp1} == {"NPP16 D EFP 347"}
    assert sorted(r["designation"] for r in dp1) == ["#30", "#31"]
    assert next(r for r in lignes if r["label"] == "SW1")["materiel"] == "NPODMA WH"
    assert all(r["reserve"] == "1" and "a confirmer" in r["note"] for r in lignes)    # toujours en réserve, motif dans la note
    assert all(float(r["x1_pt"]) - float(r["x0_pt"]) > 11 for r in lignes)              # boîte du symbole conservée
    assert json.load(open(work / "blocs-etiquettes-traitees.json", encoding="utf-8"))["signatures"]


def test_signature_deja_connue_de_la_bibliotheque_est_laissee_a_la_bibliotheque(tmp_path):
    work = _dossier(tmp_path)
    sigs = {r["signature"] for r in csv.DictReader(open(work / "blocs" / "E1.csv", encoding="utf-8"))}
    biblio = tmp_path / "biblio.csv"
    with open(biblio, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["signature", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min",
                                           "diam_max", "feuilles_regex", "portee", "tolerance", "source", "note"])
        w.writeheader()
        for s in sigs:
            w.writerow({"signature": s, "label": "IGNORER", "tolerance": "0", "source": "test"})
    assert _lancer(work, biblio) == []          # la bibliothèque a déjà jugé ces formes : aucun relevé par le texte
