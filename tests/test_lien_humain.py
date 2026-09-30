"""Lien humain ↔ plan : un .qpl + les pages PNG de son document reçu → connaissance, galerie, pratiques."""
import json

from PIL import Image, ImageDraw

from pathlib import Path

from src.apprentissage.lien_humain import construire, document_page, lier_recus, numero

QPL = """<?xml version="1.0" encoding="utf-8"?>
<Project><Plans>
 <Plan Name="01-PLANS - 3" FileName="01-PLANS - 3.png"><Layer>
  <Counter Name="Prise duplex" Shape="0" Color="-65536" DefaultSize="20">
   <Element X="100" Y="100" Width="20" Height="20"/><Element X="300" Y="120" Width="20" Height="20"/>
  </Counter>
  <Counter Name="KS" Shape="1" Color="-16776961" DefaultSize="20"><Element X="130" Y="100" Width="20" Height="20"/></Counter>
 </Layer></Plan>
 <Plan Name="01-PLANS - 4" FileName="01-PLANS - 4.png"/>
</Plans></Project>"""


def _projet(racine, nom):
    d = racine / nom
    d.mkdir(parents=True)
    (d / f"{nom}.qpl").write_text(QPL, encoding="utf-8-sig")
    im = Image.new("RGB", (400, 300), "white")
    ImageDraw.Draw(im).rectangle((95, 95, 105, 105), outline="black")
    im.save(d / "01-PLANS - 3.png")


def test_document_page():
    assert document_page("01-PLANS - 14 (3).png") == ("01-PLANS", 14)
    assert document_page("21-153 Document d'appel d'offres_Addenda 1 - 10 - Copie.png") == (
        "21-153 Document d'appel d'offres_Addenda 1", 10)


def test_construire(tmp_path):
    racine, sortie, appr = tmp_path / "projets", tmp_path / "sortie", tmp_path / "appr"
    appr.mkdir()
    (appr / "normalisation.json").write_text(json.dumps({"fusion": {"Prise duplex": "PRISE"}, "rebut": []}))
    (appr / "dictionnaire-symboles.json").write_text(json.dumps({"symboles": [
        {"label": "PRISE", "categorie": "prises", "sous_type": "duplex", "variantes": []}]}))
    _projet(racine, "S-1")
    _projet(racine, "S-2")
    conn = construire(racine, sortie, par_libelle=4, min_projets=2, fils=1, appr=appr, journal=lambda *_: None,
                      galerie_min=2)
    assert set(conn) == {"PRISE", "KS"}
    p = conn["PRISE"]
    assert (p["occurrences"], p["projets"], p["categorie"]) == (4, 2, "prises")
    assert p["variantes"] == ["PRISE DUPLEX"]
    assert p["voisins"][0]["libelle"] == "KS"
    assert p["exemples"][0]["document"] == "01-PLANS" and p["exemples"][0]["page"] == 3
    assert (sortie / p["galerie"]).is_file()
    docs = json.loads((sortie / "documents.json").read_text(encoding="utf-8"))
    assert docs["S-1"]["01-PLANS"] == {"pages_marquees": {"3": 3}, "pages_sans_marque": [4]}
    assert "document reçu" in (sortie / "PRATIQUES.md").read_text(encoding="utf-8")


def test_page_distante_telechargee_puis_effacee(tmp_path):
    """PNG absent du disque mais connu en ligne : téléchargé pour la découpe, puis effacé."""
    racine, sortie, appr = tmp_path / "projets", tmp_path / "sortie", tmp_path / "appr"
    appr.mkdir()
    (appr / "normalisation.json").write_text("{}")
    _projet(racine, "S-1")
    _projet(racine, "S-2")
    distants, reserve = {}, tmp_path / "en-ligne"
    reserve.mkdir()
    for png in racine.rglob("*.png"):
        cible = reserve / f"{png.parent.name}.png"
        png.replace(cible)
        distants[png] = (str(cible), cible.stat().st_size)
    vus = []

    def telecharger(ref, dest):
        vus.append(dest)
        dest.write_bytes(Path(ref[0]).read_bytes())

    conn = construire(racine, sortie, par_libelle=4, min_projets=2, fils=1, appr=appr, journal=lambda *_: None,
                      galerie_min=2, distants=distants, telecharger=telecharger)
    assert conn["PRISE DUPLEX"]["galerie"] and len(vus) == 2
    assert not any(v.exists() for v in vus)


def test_lier_recus():
    class FauxDrive:
        def lister(self, _):
            return [{"id": "a", "nom": "S-1645 ANNEXE-BOURASSA", "dossier": True, "url": "u/a"},
                    {"id": "b", "nom": "autre", "dossier": True, "url": "u/b"}]

        def fichiers(self, _):
            return [{"nom": "091_TAB_AO_ELE_Plans_23p..pdf", "chemin": "091_TAB_AO_ELE_Plans_23p..pdf", "url": "f"}]

    lien = lier_recus({"S-1645 (9-Janvier-2026)": {"091_TAB_AO_ELE_Plans_23p.": {}}, "S-9 (x)": {}}, FauxDrive(), "r",
                      journal=lambda *_: None)
    assert list(lien) == ["S-1645 (9-Janvier-2026)"]
    assert lien["S-1645 (9-Janvier-2026)"]["document_qpl_vers_recu"]["091_TAB_AO_ELE_Plans_23p."]["fichier"] \
        == "S-1645 ANNEXE-BOURASSA/091_TAB_AO_ELE_Plans_23p..pdf"
    assert numero("s-1646_Ville") == "1646" and numero("S- BR 1515") is None
