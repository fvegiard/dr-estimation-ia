"""Bridge releve/ -> EXEMPLE renderer (src/estimer/render/from_releve.py) on a synthetic relevé workdir."""
import csv
import json

import pymupdf

from src.estimer.render import load_input, render
from src.estimer.render.from_releve import build, reserves_by_sheet
from releve.commun import load_feuilles

W, H = 800.0, 500.0
# (feuille, label, x, y)
OCC = [("P1", "Detecteur fumee", 100, 100), ("P1", "Detecteur fumee", 300, 100), ("P1", "Klaxon", 200, 300),
       ("P1", "Panneau alarme", 500, 200), ("P2", "Prise existante", 150, 150), ("P2", "Prise existante", 250, 150),
       ("P2", "Thermostat existant", 400, 300)]


def _write(path, rows, cols):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def make_workdir(tmp_path):
    work = tmp_path / "travail"
    (work / "feuilles").mkdir(parents=True)
    for fid, title in (("P1", "DSI01"), ("P2", "E01")):
        doc = pymupdf.open()
        page = doc.new_page(width=W, height=H)
        page.insert_text((650, 480), title, fontsize=14)
        page.draw_line((20, 20), (780, 20))
        doc.save(str(work / "feuilles" / f"{fid}.pdf"))
    _write(work / "feuilles.csv", [{"feuille": f, "fichier": "plans.pdf", "page": i + 1, "largeur_pt": W,
                                    "hauteur_pt": H} for i, f in enumerate(("P1", "P2"))],
           ["feuille", "fichier", "page", "largeur_pt", "hauteur_pt"])
    _write(work / "feuilles-classement.csv",
           [{"feuille": "P1", "type": "plan", "echelle": "", "note": "cartouche=DSI01 · RDC incendie"},
            {"feuille": "P2", "type": "plan", "echelle": "", "note": "cartouche=E01 · RDC"}],
           ["feuille", "type", "echelle", "note"])
    nom = [
        {"label": "Detecteur fumee", "famille": "alarme", "code": "DF", "materiel": "Détecteur de fumée adressable",
         "portee": "INSTALLER", "modele": "", "prescription": "Selon DSI09; aucun fabricant/modele nomme"},
        {"label": "Klaxon", "famille": "alarme", "code": "K", "materiel": "Avertisseur incendie klaxon",
         "portee": "INSTALLER", "modele": "", "prescription": "Klaxon selon legende"},
        {"label": "Panneau alarme", "famille": "alarme", "code": "PAI", "materiel": "Panneau alarme incendie",
         "portee": "CONSERVER", "modele": "", "prescription": ""},
        {"label": "Prise existante", "famille": "prise", "code": "PC", "materiel": "Prise de courant double existante",
         "portee": "CONSERVER", "modele": "EXISTANT - MODELE NON INDIQUE", "prescription": "Appareil existant conserve"},
        {"label": "Thermostat existant", "famille": "chauffage", "code": "T", "materiel": "Thermostat existant",
         "portee": "CONSERVER", "modele": "EXISTANT - MODELE NON INDIQUE", "prescription": "Appareil existant conserve"},
    ]
    _write(work / "nomenclature.csv", nom, ["label", "famille", "forme", "rgb", "jeton_regex", "description", "source",
                                            "code", "materiel", "portee", "modele", "prescription"])
    occ = [{"feuille": f, "label": l, "x_pt": x, "y_pt": y, "source": "visuel", "note": ""} for f, l, x, y in OCC]
    occ[3].update({"x0_pt": 490, "y0_pt": 190, "x1_pt": 510, "y1_pt": 215})
    _write(work / "occurrences-visuel.csv", occ, ["feuille", "label", "x_pt", "y_pt", "source", "note",
                                                  "x0_pt", "y0_pt", "x1_pt", "y1_pt"])
    _write(work / "occurrences-texte.csv", [], ["feuille", "label", "x_pt", "y_pt", "source", "note"])
    (work / "reserves.md").write_text("# Reserves\n\n- **R-001** · DSI01 · Klaxon sonore/visuel a confirmer.\n"
                                      "- **R-002** · Général · Verification native Plan Expert indisponible.\n",
                                      encoding="utf-8")
    return work


def test_build_writes_renderer_input(tmp_path):
    work = make_workdir(tmp_path)
    out = tmp_path / "out"
    res = build(work, out)
    assert res == {"sheets": 2, "reperes": 7, "plans_pages": 2}
    est = json.loads((out / "estimate.json").read_text(encoding="utf-8"))
    assert [s["sheet"] for s in est["sheets"]] == ["DSI01", "E01"]
    assert est["sheets"][0]["width_px"] == W
    rows = list(csv.DictReader(open(out / "bordereau.csv", encoding="utf-8")))
    dsi = [r for r in rows if r["feuille"] == "DSI01"]
    # materiel format on an incendie sheet: I-codes in alphabetical order of the family name
    assert {r["repere"]: r["materiel"] for r in dsi} == {
        "I01-01": "AVERTISSEUR INCENDIE KLAXON", "I02-01": "DETECTEUR DE FUMEE ADRESSABLE",
        "I02-02": "DETECTEUR DE FUMEE ADRESSABLE", "I03-01": "PANNEAU ALARME INCENDIE"}
    assert {r["format"] for r in dsi} == {"materiel"}
    df = [r for r in dsi if r["designation"] == "DF"]
    assert len(df) == 2 and all(r["modele"] == "MODELE NON PRECISE" and r["portee"] == "INSTALLER" for r in df)
    # plain plan of existing devices -> aggregated format, letter codes
    e01 = [r for r in rows if r["feuille"] == "E01"]
    assert sorted(r["repere"] for r in e01) == ["PC-01", "PC-02", "T-01"]
    assert {r["format"] for r in e01} == {"agrege"}
    # source ids are unique and in reading order
    assert sorted(r["source"] for r in dsi) == ["DSI01-001", "DSI01-002", "DSI01-003", "DSI01-004"]
    pai = [e for c in est["counters"] if c["family"] == "Panneau alarme" for e in c["elements"]]
    assert pai[0]["shape"] == "rect" and pai[0]["bbox"] == [490, 190, 510, 215]
    assert pymupdf.open(out / "plans.pdf").page_count == 2


def test_reserves_split_by_sheet(tmp_path):
    work = make_workdir(tmp_path)
    text = reserves_by_sheet(work, ["DSI01", "E01"], load_feuilles(str(work)))
    dsi, e01 = text.split("## E01")
    assert "Klaxon sonore" in dsi and "Klaxon sonore" not in e01
    assert "native Plan Expert" in dsi and "native Plan Expert" in e01


def test_render_from_bridge(tmp_path):
    work = make_workdir(tmp_path)
    out = tmp_path / "out"
    build(work, out)
    sheets = load_input(out)
    assert [(s.name, len(s.items)) for s in sheets] == [("DSI01", 4), ("E01", 3)]
    pdf = tmp_path / "rendu.pdf"
    rep = render(sheets, out / "plans.pdf", pdf)
    doc = pymupdf.open(pdf)
    assert rep["sheets"][0]["reperes"] == 4 and rep["sheets"][1]["reperes"] == 3
    plan = doc[rep["sheets"][0]["plan_page"] - 1].get_text()
    assert "RELEVE DSI01 - MATERIEL" in plan and "4 reperes / 3 familles / RES 4" in plan
    for rep_id in ("I01-01", "I02-01", "I02-02", "I03-01"):
        assert rep_id in plan
    assert "DSI01" in plan                     # original page content kept


def test_texte_lisible_garde_les_accents():
    """Le texte libre garde ses accents ; seuls les signes hors Latin-1 sont remplacés.

    L'EXEMPLE a perdu les siens (« Calibre et caracteristiques a verifier ») ; c'est un
    défaut de son export, pas une présentation à reproduire — la police `helv` du rendu
    est en Latin-1 et restitue les accents sans perte (vérifié par aller-retour PDF)."""
    from src.estimer.render.from_releve import texte_lisible
    assert texte_lisible("échelle « AUCUNE » → à métrer (§5b), ≈9 vus") == 'échelle "AUCUNE" -> à métrer (par. 5b), ~9 vus'
    assert texte_lisible("Détecteur de fumée exécuté déjà à côté du boîtier") == "Détecteur de fumée exécuté déjà à côté du boîtier"


def test_texte_lisible_remplace_les_ligatures():
    """`œ` n'est pas en Latin-1 et NFKD ne le décompose pas : sans table il disparaissait."""
    from src.estimer.render.from_releve import texte_lisible
    assert texte_lisible("œuvre — cœur") == "oeuvre - coeur"


def test_accents_rendus_par_la_police_du_pdf():
    """Preuve que l'écart corrigé en est bien un : `helv` restitue les accents."""
    import pymupdf
    phrase = "Détecteur de fumée exécuté déjà à côté du boîtier"
    doc = pymupdf.open()
    doc.new_page(width=400, height=80).insert_text((20, 40), phrase, fontname="helv", fontsize=10)
    relu = pymupdf.open("pdf", doc.tobytes())
    assert phrase in relu[0].get_text()


def test_ascii_upper_reste_plie():
    """Écart conservé : les colonnes de code servent de clé de jointure avec le bordereau
    de l'estimateur, lui-même sans accents. Les plier des deux côtés garde le rapprochement."""
    from src.estimer.render.from_releve import ascii_upper
    assert ascii_upper("Réserve × 2") == "RESERVE X 2"
