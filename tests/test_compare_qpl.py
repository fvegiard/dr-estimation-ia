"""Tests de `src.validation.compare_qpl` sur deux mini-projets Plan Expert
SYNTHÉTIQUES (aucune donnée client), générés ici :

- IA : 3 feuilles (E100, E200, E300) d'un PDF fictif « PLANS-TEST.pdf »,
  rasters 1000×700 px (taille lue dans feuilles.csv).
- Humain : rasters 2000×1400 px (échelle ×2) :
  * « PLANS-TEST - 1 » → E100 par le nom : 8 marques, dont 1 absente côté IA
    (libellé « TYPE Z ») ; 1 marque « TYPE A » posée par l'IA en « Luminaire B »
    (même position, autre libellé) ; l'IA a 1 marque en trop ;
  * « PLANS-TEST - 1 (1) » : copie exacte de la page 1 (page en double) ;
  * « AUTRE-DOC - 7 » : document inconnu de l'IA, raster portrait 1400×2000
    tourné d'un quart de tour → E200 par géométrie (20 marques) ;
  * « PLANS-TEST - 3 » → E300 par le nom, 6 marques décalées de quelques px.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from conftest import run_cli
from src.validation import compare_qpl as cq

IA_L, IA_H = 1000, 700


def _grille(n: int, x0: int, y0: int, pas: int = 90, colonnes: int = 5) -> list[tuple[int, int]]:
    return [(x0 + (i % colonnes) * pas + (i // colonnes) * 17, y0 + (i // colonnes) * pas) for i in range(n)]


def _qpl(plans: list[tuple[str, str, list[tuple[str, int, int]]]]) -> str:
    """plans : (Name, FileName, [(libellé, x, y)]) → XML Plan Expert minimal."""
    corps = []
    for nom, fichier, marques in plans:
        par_lib: dict[str, list[tuple[int, int]]] = {}
        for lib, x, y in marques:
            par_lib.setdefault(lib, []).append((x, y))
        compteurs = []
        for gid, (lib, pts) in enumerate(par_lib.items(), start=1):
            elements = "".join(f'<Element X="{x}" Y="{y}" Width="20" Height="20"/>' for x, y in pts)
            compteurs.append(f'<Counter Name="{lib}" GroupID="{gid}">{elements}</Counter>')
        ligne = '<Line Name="CONDUIT" GroupID="99"><Element X1="0" Y1="0" X2="30" Y2="40"/></Line>'
        corps.append(f'<Plan Name="{nom}" FileName="{fichier}"><Layers><Layer Index="0" Name="Calque">'
                     f'{"".join(compteurs)}{ligne}</Layer></Layers></Plan>')
    return ('<?xml version="1.0"?><QuoterPlanSession><Project Name="synthetique"/>'
            f'<Plans>{"".join(corps)}</Plans></QuoterPlanSession>')


@pytest.fixture(scope="module")
def projets(tmp_path_factory) -> dict[str, Path]:
    d = tmp_path_factory.mktemp("compare_qpl")
    # --- feuille 1 : noms, une manquante, une en trop, un mauvais type
    p1_ia = _grille(7, 150, 150)
    libs_ia_1 = ["Luminaire A"] * 4 + ["Luminaire B"] * 3
    libs_h_1 = ["TYPE A"] * 5 + ["TYPE B"] * 2      # la 5e « TYPE A » est posée « Luminaire B » par l'IA
    h1 = [(lib, 2 * x, 2 * y) for lib, (x, y) in zip(libs_h_1, p1_ia)] + [("TYPE Z", 2 * 800, 2 * 600)]
    ia1 = [(lib, x, y) for lib, (x, y) in zip(libs_ia_1, p1_ia)] + [("Luminaire A", 900, 80)]
    # --- feuille 2 : 20 marques, raster humain portrait tourné d'un quart de tour
    p2_ia = _grille(20, 120, 110, pas=110, colonnes=7)
    libs_2 = ["TYPE A"] * 12 + ["TYPE D"] * 8
    libs_ia_2 = ["Luminaire A"] * 12 + ["Détecteur"] * 8
    h2 = [(lib, 2 * (IA_H - y), 2 * x) for lib, (x, y) in zip(libs_2, p2_ia)]
    ia2 = [(lib, x, y) for lib, (x, y) in zip(libs_ia_2, p2_ia)]
    # --- feuille 3 : 6 marques, petits décalages ; une marque IA « Sortie » en trop
    p3_ia = _grille(6, 300, 300, pas=120, colonnes=3)
    h3 = [("TYPE C", 2 * x + 6, 2 * y - 4) for x, y in p3_ia]
    ia3 = [("Prise", x, y) for x, y in p3_ia] + [("Sortie", 60, 640)]

    humain = d / "S-9999-dupuis.qpl"
    humain.write_text(_qpl([
        ("PLANS-TEST - 1", "PLANS-TEST - 1.png", h1),
        ("PLANS-TEST - 1 1", "PLANS-TEST - 1 (1).png", h1),
        ("AUTRE-DOC - 7", "AUTRE-DOC - 7.png", h2),
        ("PLANS-TEST - 3", "PLANS-TEST - 3.png", h3),
        ("PLANS-TEST - 2", "PLANS-TEST - 2.png", []),
    ]), encoding="utf-8")
    ia = d / "ia" / "S-9999.qpl"
    ia.parent.mkdir()
    ia.write_text(_qpl([("E100", "E100.png", ia1), ("E200", "E200.png", ia2), ("E300", "E300.png", ia3)]),
                  encoding="utf-8")
    dims = d / "png-dimensions.txt"
    dims.write_text("\n".join([
        "S-9999 (fictif)|PLANS-TEST - 1.png|2000|1400",
        "S-9999 (fictif)|PLANS-TEST - 1 (1).png|2000|1400",
        "S-9999 (fictif)|PLANS-TEST - 2.png|2000|1400",
        "S-9999 (fictif)|PLANS-TEST - 3.png|2000|1400",
        "S-9999 (fictif)|AUTRE-DOC - 7.png|1400|2000",
        "S-1234 (autre dossier)|PLANS-TEST - 3.png|10|10",
    ]) + "\n", encoding="utf-8")
    feuilles = d / "feuilles.csv"
    with feuilles.open("w", encoding="utf-8", newline="") as flux:
        w = csv.writer(flux)
        w.writerow(["feuille", "fichier", "page", "largeur_pt", "hauteur_pt", "raster_px", "classement_fichier"])
        for i, f in enumerate(["E100", "E200", "E300"], start=1):
            w.writerow([f, "PLANS-TEST.pdf", i, "1000", "700", f"{IA_L}x{IA_H}", "plans"])
    return {"humain": humain, "ia": ia, "dims": dims, "feuilles": feuilles, "dossier": d}


@pytest.fixture(scope="module")
def comparaison(projets) -> cq.Comparaison:
    humains = cq.lire_qpl(projets["humain"], "humain")
    ias = cq.lire_qpl(projets["ia"], "ia")
    cq.preparer_humain(humains, cq.lire_dimensions(projets["dims"], "S-9999"))
    anomalies = cq.preparer_ia(ias, cq.lire_feuilles(projets["feuilles"]), None)
    return cq.comparer(humains, ias, anomalies)


def test_analyse_des_noms_de_pages():
    assert cq.analyser_nom_humain("01-PLANS - 41 2 1", "01-PLANS - 41 (2) (1).png") == ("01-PLANS", 41)
    assert cq.analyser_nom_humain("x", "00 Addenda MEP01_Plans-unlocked-page-00015.jpg") == \
        ("00 Addenda MEP01_Plans", 15)
    assert cq.normaliser_nom("ÉLECTRIQUE_Plans.pdf") == cq.normaliser_nom("electrique_plans")


def test_dimensions_filtrees_par_dossier(projets):
    dims = cq.lire_dimensions(projets["dims"], "S-9999")
    assert dims["PLANS-TEST - 3.png"] == (2000.0, 1400.0)


def test_appariement_des_pages(comparaison):
    paires = {p.humain.nom: p for p in comparaison.pages.paires}
    assert paires["PLANS-TEST - 1"].feuille == "E100" and paires["PLANS-TEST - 1"].methode == "nom"
    assert paires["PLANS-TEST - 3"].feuille == "E300" and paires["PLANS-TEST - 3"].methode == "nom"
    tourne = paires["AUTRE-DOC - 7"]
    assert tourne.feuille == "E200" and tourne.methode == "géométrie"
    assert tourne.score == pytest.approx(1.0)
    assert cq.ROTATIONS[tourne.transfo.k][0] != "0°"
    assert tourne.transfo.echelle == pytest.approx(0.5, rel=0.02)
    assert not comparaison.pages.non_appariees


def test_page_en_double(comparaison):
    assert len(comparaison.doublons) == 1
    d = comparaison.doublons[0]
    assert d.feuille == "E100" and d.nature == "copie" and d.doublons == d.total == 8
    tot = cq.totaux(comparaison)
    assert tot["humaines_brutes"] == 8 + 8 + 20 + 6
    assert tot["doublons"] == 8 and tot["humaines"] == 34


def test_appariement_des_marques(comparaison):
    res = comparaison.resultats[cq.SEUIL_MARQUE]
    assert len(res["E100"].couples) == 7
    assert [h.marque.libelle for h in res["E100"].manquantes] == ["TYPE Z"]
    assert [(m.x, m.y) for m in res["E100"].en_trop] == [(900.0, 80.0)]
    assert len(res["E200"].couples) == 20 and not res["E200"].manquantes and not res["E200"].en_trop
    assert len(res["E300"].couples) == 6 and [m.libelle for m in res["E300"].en_trop] == ["Sortie"]
    tot = cq.totaux(comparaison)
    assert (tot["ia"], tot["appariees"], tot["manquantes"], tot["en_trop"]) == (35, 33, 1, 2)
    # sensibilité : au seuil le plus strict, les marques décalées de E300 (~3,6 px IA,
    # 0,3 % de la diagonale) restent appariées
    assert cq.totaux(comparaison, 0.006)["appariees"] == 33


def test_table_des_libelles(comparaison):
    table = cq.table_libelles(comparaison)
    assert table["TYPE A"].libelle_ia == "Luminaire A"
    assert table["TYPE A"].appariees == 17 and table["TYPE A"].proportion == pytest.approx(16 / 17)
    assert table["TYPE B"].libelle_ia == "Luminaire B"
    assert table["TYPE C"].libelle_ia == "Prise" and table["TYPE C"].proportion == 1.0
    assert table["TYPE D"].libelle_ia == "Détecteur"
    assert table["TYPE Z"].libelle_ia is None


def test_cli_produit_les_quatre_sorties(projets):
    sortie = projets["dossier"] / "sortie"
    run_cli("-m", "src.validation.compare_qpl", "--humain", str(projets["humain"]), "--ia", str(projets["ia"]),
            "--dims", str(projets["dims"]), "--feuilles", str(projets["feuilles"]), "--sortie", str(sortie))
    for nom in ("ecart-dupuis.md", "appariement.csv", "correspondance-libelles.csv", "pages.csv"):
        assert (sortie / nom).is_file(), nom
    rapport = (sortie / "ecart-dupuis.md").read_text(encoding="utf-8")
    assert "**Appariées** (seuil 1.2 % diag.) | **33**" in rapport
    assert "page EN DOUBLE" in rapport and "Sortie (1)" in rapport and "TYPE Z (1)" in rapport
    with (sortie / "appariement.csv").open(encoding="utf-8") as flux:
        lignes = list(csv.DictReader(flux))
    assert len(lignes) == 42 + 35          # une ligne par marque des deux côtés
    mauvais = [l for l in lignes if l["cote"] == "humain" and l["statut"] == "appariée"
               and l["libelle"] == "TYPE A" and l["libelle_apparie"] == "Luminaire B"]
    assert len(mauvais) == 1
    with (sortie / "correspondance-libelles.csv").open(encoding="utf-8") as flux:
        corr = {l["libelle_humain"]: l for l in csv.DictReader(flux)}
    assert corr["TYPE A"]["meme_position_libelle_different"] == "1"
