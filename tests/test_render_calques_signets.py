"""Écarts E3, E5, E6 de docs/FORMAT-EXEMPLE.md §6 (le gold gagne) — plans synthétiques, aucune donnée client.

- E5 : un calque `RELEVE <code> - <materiel>` par famille ET par feuille + un calque légende par feuille ; la
  page plan ET les pages de bordereau de la feuille dessinent dans ces calques (en-tête, filets et notes dans la
  légende, cellules d'une ligne dans le calque de sa famille) ; panneau des calques : familles puis légende.
- E6 : un signet de niveau 1 `<projet>-<feuille>-annote-v<n>` par feuille sur sa page plan, les signets d'origine
  du plan rangés dessous.
- E3 : l'encadré renvoie à la `page 2` de la feuille (son bordereau), jamais au numéro absolu ; lignes de
  l'encadré du gold (1 ligne ou empilé selon la largeur, pied propre à la feuille, pied v6).
"""
from __future__ import annotations

import csv
import json
import re

import pymupdf

from src.estimer.render import from_exemple as FX
from src.estimer.render import load_input, render
from src.estimer.render import style as S
from src.estimer.render import verify_exemple as VE
from src.estimer.render.data import Item, Sheet

from test_render_exemple import FAMS, FIELDS, H, W, draw_plan, make_exemple, write_input

NOMS = [f"RELEVE {c} - {m}" for c, m, _ in FAMS] + [S.LEGEND_LAYER]


def _deux_feuilles(tmp_path, toc=None):
    """DSI01 (page 1) et DSI02 (page 2) avec les MÊMES familles I01-I03 : leurs calques restent distincts."""
    plans = tmp_path / "plans.pdf"
    pts = draw_plan(plans, n_pages=2)
    if toc is not None:
        doc = pymupdf.open(plans)
        doc.set_toc(toc)
        doc.save(tmp_path / "plans-toc.pdf")
        plans = tmp_path / "plans-toc.pdf"
    d = tmp_path / "in"
    write_input(d, pts[0], "DSI01")
    est = json.loads((d / "estimate.json").read_text(encoding="utf-8"))
    est["sheets"].append({"page": 2, "sheet": "DSI02", "width_px": W, "height_px": H})
    for k, (code, mat, _) in enumerate(FAMS):
        els = [{"sheet": "DSI02", "page": 2, "x": x, "y": y, "code": code, "repere": f"{code}-{j + 1:02d}"}
               for j, (x, y) in enumerate(pts[1][k * 3:k * 3 + 3])]
        est["counters"].append({"family": code, "name": mat, "elements": els})
    (d / "estimate.json").write_text(json.dumps(est), encoding="utf-8")
    return plans, d


def _calques(doc):
    return VE.releve_ocgs(doc)


def _textes_par_calque(doc, pno) -> dict[str, list[str]]:
    """Texte dessiné dans chaque calque RELEVE de la page (blocs /OC ... BDC ... EMC du flux de contenu)."""
    rel = _calques(doc)
    kind, val = doc.xref_get_key(doc[pno].xref, "Resources/Properties")
    props = doc.xref_object(int(val.split()[0])) if kind == "xref" else val
    nom = {n: rel[int(x)]["name"] for n, x in re.findall(r"/(\w+)\s+(\d+)\s+0\s+R", props) if int(x) in rel}
    out: dict[str, list[str]] = {}
    for x in doc[pno].get_contents():
        for m in re.finditer(rb"/OC\s*/(\w+)\s*BDC(.*?)EMC", doc.xref_stream(x), re.S):
            textes = [bytes.fromhex(t.decode()).decode("latin-1") for t in re.findall(rb"<([0-9a-fA-F]+)>", m.group(2))]
            out.setdefault(nom.get(m.group(1).decode(), "?"), []).extend(textes)
    return out


# ---------------------------------------------------------------- E5 calques
def test_calques_par_famille_et_par_feuille(tmp_path):
    plans, d = _deux_feuilles(tmp_path)
    out = tmp_path / "o.pdf"
    rep = render(load_input(d), plans, out, log=lambda *a: None)
    doc = pymupdf.open(out)
    rel = _calques(doc)
    # gold : 344 calques famille (un par famille ET par feuille) + 26 calques légende (un par feuille)
    assert sorted(v["name"] for v in rel.values()) == sorted(NOMS * 2)
    assert all(v["on"] for v in rel.values())
    own = {}
    for s in rep["sheets"]:
        plan = s["plan_page"] - 1
        own[s["sheet"]] = set(VE.page_ocgs(doc, plan, rel))
        assert sorted(rel[x]["name"] for x in own[s["sheet"]]) == sorted(NOMS)
        for p in s["bordereau_pages"]:                           # bordereau : calques de SA feuille seulement
            assert set(VE.page_ocgs(doc, p - 1, rel)) <= own[s["sheet"]]
    assert own["DSI01"].isdisjoint(own["DSI02"])
    # panneau des calques (gold) : familles dans l'ordre de la légende puis la légende, feuille par feuille
    assert [rel[x]["name"] for x in VE.order_ocgs(doc) if x in rel] == NOMS * 2


def test_bordereau_dessine_dans_les_calques_de_la_feuille(tmp_path):
    """Gold p.2 / p.63 : en-tête, bande, titres de colonnes, filets et notes dans la légende ; les cellules
    d'une ligne dans le calque de la famille de la ligne."""
    plans, d = _deux_feuilles(tmp_path)
    out = tmp_path / "o.pdf"
    rep = render(load_input(d), plans, out, log=lambda *a: None)
    doc = pymupdf.open(out)
    b1 = rep["sheets"][0]["bordereau_pages"]
    t = _textes_par_calque(doc, b1[0] - 1)
    assert "BORDEREAU MATERIEL - DSI01" in t[S.LEGEND_LAYER] and "Repere / source" in t[S.LEGEND_LAYER]
    assert "I01-01" in t[NOMS[0]] and "DSI01-001" in t[NOMS[0]] and "I02-01" in t[NOMS[1]]
    assert not any(x.startswith("I0") for x in t[S.LEGEND_LAYER])
    assert "RESERVES ET COMPLEMENTS" in _textes_par_calque(doc, b1[-1] - 1)[S.LEGEND_LAYER]
    # aucune ligne du bordereau hors calque
    tout = "".join(doc[b1[0] - 1].get_text().split())
    dans = "".join("".join(v) for v in t.values()).replace(" ", "")
    assert len(dans) >= len(tout) - 5


def test_bordereau_agrege_dans_les_calques(tmp_path):
    plans = tmp_path / "plans.pdf"
    draw_plan(plans)
    b = S.PALETTE_B["PC"][0]
    items = [Item("E08", 1, 300 + 40 * k, 300, code, f"{code}-01", materiel=f"FAMILLE {code}", color=b)
             for k, code in enumerate(("AF", "PC"))]
    out = tmp_path / "o.pdf"
    rep = render([Sheet("E08", 1, W, H, items=items, format="agrege")], plans, out, log=lambda *a: None)
    doc = pymupdf.open(out)
    t = _textes_par_calque(doc, rep["sheets"][0]["bordereau_pages"][0] - 1)
    assert "BORDEREAU MATERIEL - E08" in t[S.LEGEND_LAYER] and "Famille" in t[S.LEGEND_LAYER]
    assert "AF" in t["RELEVE AF - FAMILLE AF"] and "FAMILLE PC" in t["RELEVE PC - FAMILLE PC"]


# ---------------------------------------------------------------- E6 signets
def test_signets_annote_et_signets_d_origine_du_plan(tmp_path):
    """Sans signets donnés par l'entrée : ceux du PDF de plans qui visent la page de la feuille, avec leurs
    parents (sans destination quand ils visent une autre page), rangés sous le signet annote."""
    toc = [[1, "JEU DE PLANS", 1], [2, "E100 PLAN", 1], [2, "E101 PLAN", 2]]
    plans, d = _deux_feuilles(tmp_path, toc=toc)
    est = json.loads((d / "estimate.json").read_text(encoding="utf-8"))
    est["projet"] = "S-TEST"
    est["sheets"][1]["version"] = 3
    (d / "estimate.json").write_text(json.dumps(est), encoding="utf-8")
    out = tmp_path / "o.pdf"
    rep = render(load_input(d), plans, out, log=lambda *a: None)
    p1, p2 = (s["plan_page"] for s in rep["sheets"])
    assert VE.signets(pymupdf.open(out)) == [
        (1, "S-TEST-DSI01-annote-v1", p1), (2, "JEU DE PLANS", p1), (3, "E100 PLAN", p1),
        (1, "S-TEST-DSI02-annote-v3", p2), (2, "JEU DE PLANS", -1), (3, "E101 PLAN", p2)]


def test_signets_donnes_par_l_entree(tmp_path):
    """Gold HR26-14 : `sheets[].signets` = signets du PDF d'origine de la feuille (page 1 = sa page plan,
    -1 = sans destination) ; sans projet, le signet est `<feuille>-annote-v<n>`."""
    plans, d = _deux_feuilles(tmp_path, toc=[[1, "A IGNORER", 1]])
    est = json.loads((d / "estimate.json").read_text(encoding="utf-8"))
    est["sheets"][0]["signets"] = [[1, "HR24-13 ME pr AO", -1], [2, "DSI", 1], [3, "DSI-DSI01", 1]]
    est["sheets"][1]["signets"] = []
    (d / "estimate.json").write_text(json.dumps(est), encoding="utf-8")
    out = tmp_path / "o.pdf"
    rep = render(load_input(d), plans, out, log=lambda *a: None)
    p1, p2 = (s["plan_page"] for s in rep["sheets"])
    assert VE.signets(pymupdf.open(out)) == [
        (1, "DSI01-annote-v1", p1), (2, "HR24-13 ME pr AO", -1), (3, "DSI", p1), (4, "DSI-DSI01", p1),
        (1, "DSI02-annote-v1", p2)]


def test_from_exemple_lit_signets_projet_version_et_pied(tmp_path):
    ex = tmp_path / "EXEMPLE.pdf"
    marks = make_exemple(ex)
    doc = pymupdf.open(ex)
    doc.set_toc([[1, "HR26-14-DSI01-annote-v4", 1], [2, "HR24-13 ME pr AO", -1], [3, "DSI", 1]])
    legend = [x for x, v in doc.get_ocgs().items() if v["name"] == S.LEGEND_LAYER][0]
    doc[0].insert_text((1010, 1100 - 6.475), "Reperes source; quantites et reserves au bordereau.", fontsize=7.0,
                       oc=legend)
    doc.save(tmp_path / "EXEMPLE2.pdf")
    bcsv, fcsv = tmp_path / "b.csv", tmp_path / "f.csv"
    with open(bcsv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for k, (rep, _, _) in enumerate(marks):
            w.writerow({"feuille": "DSI01", "repere": rep, "source": f"DSI01-{k + 40}", "materiel": "AVERTISSEUR",
                        "designation": "A", "qte": 1, "portee": "INSTALLER", "modele": "MODELE NON PRECISE",
                        "prescription": "p", "parent": ""})
    fcsv.write_text("feuille,discipline,lot,batiment,reperes,familles,res,page,af_entete\n"
                    "DSI01,INCENDIE,LOT A,X,2,1,2,1,\n")
    out = tmp_path / "gold"
    FX.build(tmp_path / "EXEMPLE2.pdf", bcsv, fcsv, out, log=lambda *a: None)
    est = json.loads((out / "estimate.json").read_text(encoding="utf-8"))
    s = est["sheets"][0]
    assert (s["projet"], s["version"]) == ("HR26-14", 4)
    assert s["signets"] == [[1, "HR24-13 ME pr AO", -1], [2, "DSI", 1]]
    assert s["pied"] == "Reperes source; quantites et reserves au bordereau."
    sheets = load_input(out)
    render(sheets, out / "plans.pdf", tmp_path / "r.pdf", log=lambda *a: None)
    assert VE.signets(pymupdf.open(tmp_path / "r.pdf")) == [
        (1, "HR26-14-DSI01-annote-v4", 1), (2, "HR24-13 ME pr AO", -1), (3, "DSI", 1)]


# ---------------------------------------------------------------- E3 renvoi de page et lignes de l'encadré
def _spans(page):
    return [sp for b in page.get_text("dict")["blocks"] for line in b.get("lines", []) for sp in line["spans"]]


def test_renvoi_page_2_sur_chaque_feuille(tmp_path):
    """Gold : « page 2 » (2e page de la feuille = son bordereau) partout, y compris sur la 2e feuille."""
    plans, d = _deux_feuilles(tmp_path)
    out = tmp_path / "o.pdf"
    rep = render(load_input(d), plans, out, log=lambda *a: None)
    doc = pymupdf.open(out)
    for s in rep["sheets"]:
        refs = VE.renvois(doc[s["plan_page"] - 1], pymupdf.Rect(s["box"]))
        assert refs and all(re.search(r"\bpage 2\b", t) for t in refs), refs
    assert rep["sheets"][1]["bordereau_pages"][0] != 2                 # page absolue 5, renvoi « page 2 »


def _feuille_cadre(largeur: float, fmt: str = "materiel", pied: str | None = None) -> Sheet:
    items = [Item("DSI03", 1, 300 + 40 * k, 300, "I01", f"I01-{k + 1:02d}", materiel="AVERTISSEUR")
             for k in range(3)]
    return Sheet("DSI03", 1, W, H, items=items, format=fmt, box_hint=(100.0, 1000.0, 100.0 + largeur, 1400.0),
                 pied=pied)


def test_encadre_une_ligne_ou_empile_selon_la_largeur(tmp_path):
    """Gold : titre, compteur et renvoi sur une ligne dès que le renvoi tient dans le cadre (800 pt EU01 ...
    2020 pt DSI01) ; empilé en dessous (780 pt E01/E09/E12, 390 E02, 260 E07) avec le renvoi court et la
    ligne RES courte en noir 8,2 (spec §3.1, §3.2). Pied à 6,475 pt du bas du cadre."""
    plans = tmp_path / "plans.pdf"
    draw_plan(plans)
    for largeur, une_ligne in ((800.0, True), (780.0, False)):
        out = tmp_path / f"o{int(largeur)}.pdf"
        rep = render([_feuille_cadre(largeur)], plans, out, log=lambda *a: None)
        box = pymupdf.Rect(rep["sheets"][0]["box"])
        sp = {s["text"]: s for s in _spans(pymupdf.open(out)[0]) if pymupdf.Point(s["origin"]) in box}
        titre = sp["RELEVE DSI03 - MATERIEL"]["origin"][1] - box.y0
        if une_ligne:
            renvoi = sp["Calques activables; modeles, prescriptions et reserves completes page 2"]
            res = sp[S.WARN_TEXT]
            assert abs(renvoi["origin"][1] - box.y0 - titre) < 0.01 and abs(renvoi["origin"][0] - box.x0 - 530) < 0.01
            assert abs(res["size"] - 7.2) < 0.01 and res["color"] == 0x8C1A1A
        else:
            renvoi = sp["Calques activables; prescriptions completes page 2."]
            res = sp["RES = reserve source, modele, position ou portee; * = identification a revalider"]
            assert abs(renvoi["origin"][1] - box.y0 - 39.952) < 0.01
            assert abs(res["origin"][1] - box.y0 - 50.089) < 0.01
            assert abs(res["size"] - 8.2) < 0.01 and res["color"] == 0
        pied = sp[S.FOOTER_TEXT]
        assert abs(pied["origin"][1] - box.y1 + 6.475) < 0.01


def test_pied_propre_a_la_feuille(tmp_path):
    """Gold : pied propre à la feuille (E10 « Reperes source; ... », EU03 « Bordereau complet et reserves page
    2. ») ; à défaut, le pied par défaut du format."""
    plans = tmp_path / "plans.pdf"
    draw_plan(plans)
    out = tmp_path / "o.pdf"
    render([_feuille_cadre(870.0, pied="Reperes source; quantites et reserves au bordereau.")], plans, out,
           log=lambda *a: None)
    text = pymupdf.open(out)[0].get_text()
    assert "Reperes source; quantites et reserves au bordereau." in text and S.FOOTER_TEXT not in text
    render([_feuille_cadre(930.0, fmt="travaux")], plans, tmp_path / "t.pdf", log=lambda *a: None)
    assert ("Emplacements de travaux sur calques; achats, prescriptions et reserves detaillees page 2."
            in pymupdf.open(tmp_path / "t.pdf")[0].get_text())


def test_encadre_v6_pied_et_designation_r001(tmp_path):
    """Gold E03/E04/E05/E08 : ligne R-001 dès qu'une famille est hors légende (« (hors legende - R-001) »,
    libellé de légende « [R-001] ») ; 1re ligne du pied à 71,4 pt du bas du cadre (6 ou 7 lignes)."""
    plans = tmp_path / "plans.pdf"
    draw_plan(plans)
    b = S.PALETTE_B["PL"][0]
    items = [Item("E03", 1, 300 + 40 * k, 300, code, f"{code}-01", materiel=mat, color=b)
             for k, (code, mat) in enumerate((("PL", "PLINTHE DE CHAUFFAGE (hors legende - R-001)"),
                                              ("PC", "PRISE DE COURANT DOUBLE 15A-125V")))]
    sh = Sheet("E03", 1, W, H, items=items, format="agrege", box_hint=(1690.0, 640.0, 2160.0, 1570.0))
    out = tmp_path / "o.pdf"
    rep = render([sh], plans, out, log=lambda *a: None)
    assert rep["sheets"][0]["encadre"] == "v6"
    box = pymupdf.Rect(rep["sheets"][0]["box"])
    sp = {s["text"]: s for s in _spans(pymupdf.open(out)[0]) if pymupdf.Point(s["origin"]) in box}
    assert "R-001 : designation conservee au registre des reserves." in sp
    assert "PLINTHE DE CHAUFFAGE [R-001]" in sp
    premier = sp["PL : rectangles aux dimensions graphiques du plan."]
    assert abs(premier["origin"][1] - box.y1 + 71.4) < 0.01
    assert "Modeles, prescriptions et sources : bordereau page 2." in sp


# ---------------------------------------------------------------- lignes de famille de la légende (gold)
def _legende(tmp_path, sheet: Sheet):
    plans = tmp_path / f"plans-{sheet.name}.pdf"            # un fichier par appel : jamais réécrit
    draw_plan(plans)
    out = tmp_path / f"leg-{sheet.name}.pdf"
    rep = render([sheet], plans, out, log=lambda *a: None)
    box = pymupdf.Rect(rep["sheets"][0]["box"])
    return box, [s for s in _spans(pymupdf.open(out)[0]) if pymupdf.Point(s["origin"]) in box]


def test_legende_quantite_a_74_pt_de_la_fin_de_cellule(tmp_path):
    """Gold : quantité à 74 pt avant la fin de la cellule — DSI05 cellules de 220 pt (156 depuis le cadre),
    E07 une colonne de 260 pt = le cadre entier (196) ; libellé coupé avant la quantité (« AVERTISSEUR
    INCENDIE » / « KLAXON »), 1re ligne sur la ligne du code."""
    items = [Item("DSI05", 1, 300 + 40 * k, 300, code, f"{code}-01", materiel=mat)
             for k, (code, mat) in enumerate((("I01", "AVERTISSEUR DE FUMEE AUTONOME 120V MURAL"),
                                              ("I02", "AVERTISSEUR INCENDIE KLAXON"), ("I03", "DECLENCHEUR"),
                                              ("I04", "DETECTEUR")))]
    sh = Sheet("DSI05", 1, W, H, items=items, box_hint=(100.0, 1000.0, 980.0, 1440.0),
               legend_rows=(48.1 + 0.905 - 0.0, 27.0, 4, 220.0))
    box, sp = _legende(tmp_path, sh)
    qty = sorted(round(s["origin"][0] - box.x0, 1) for s in sp if abs(s["size"] - S.ROW_QTY_SIZE) < 0.01)
    assert qty == [156.0, 376.0, 596.0, 816.0]
    lab = {s["text"]: s for s in sp if abs(s["size"] - S.ROW_LABEL_SIZE) < 0.01}
    code = next(s for s in sp if s["text"] == "I02")
    assert "AVERTISSEUR INCENDIE" in lab and "KLAXON" in lab
    assert abs(lab["AVERTISSEUR INCENDIE"]["origin"][1] - (code["origin"][1] - 3.905)) < 0.01
    assert abs(lab["KLAXON"]["origin"][1] - lab["AVERTISSEUR INCENDIE"]["origin"][1] - 7.4498) < 0.001
    une = Sheet("E07", 1, W, H, items=[Item("E07", 1, 300, 300, "M01", "M01-01", materiel="DISJONCTEUR")],
                box_hint=(100.0, 1000.0, 360.0, 1680.0))
    box, sp = _legende(tmp_path, une)
    assert [round(s["origin"][0] - box.x0, 1) for s in sp if abs(s["size"] - S.ROW_QTY_SIZE) < 0.01] == [196.0]


def test_legende_pas_de_colonne_impose(tmp_path):
    """Gold DSI02 : 9 familles sur 3 colonnes au pas de 500 pt (grille de 4 dans un cadre de 2000 pt)."""
    items = [Item("DSI02", 1, 300 + 30 * k, 300, f"I0{k + 1}", f"I0{k + 1}-01", materiel=f"FAMILLE {k}")
             for k in range(9)]
    sh = Sheet("DSI02", 1, W, H, items=items, box_hint=(100.0, 1000.0, 2100.0, 1340.0),
               legend_rows=(49.0, 27.0, 3, 500.0))
    box, sp = _legende(tmp_path, sh)
    codes = sorted({round(s["origin"][0] - box.x0, 1) for s in sp if s["text"].startswith("I0") and "Bold" in s["font"]})
    assert codes == [25.0, 525.0, 1025.0]


def test_legende_v6_coupe_du_gold(tmp_path):
    """Gold E08 (cadre de 235 pt) : « PRISE DE COURANT AU » / « DESSUS D'UN COMPTOIR - » / « DDFT »."""
    b = S.PALETTE_B["CG"][0]
    it = Item("E08", 1, 300, 300, "CG", "CG-01", materiel="PRISE DE COURANT AU DESSUS D'UN COMPTOIR - DDFT", color=b)
    sh = Sheet("E08", 1, W, H, items=[it], format="agrege", box_hint=(668.0, 780.0, 903.0, 1660.0))
    box, sp = _legende(tmp_path, sh)
    lab = [s["text"] for s in sorted(sp, key=lambda s: s["origin"][1]) if abs(s["size"] - S.V6_LABEL_SIZE) < 0.01]
    assert lab == ["PRISE DE COURANT AU", "DESSUS D'UN COMPTOIR -", "DDFT"]

