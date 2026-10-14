"""Tests de `src.validation.classer_ecarts` sur des mini-projets Plan Expert
SYNTHÉTIQUES (aucune donnée client), générés ici :

- Rasters IA 1000×700 px (raster_px de feuilles.csv), humains 2000×1400 px
  (fichier de dimensions, échelle ×2) — même montage que test_compare_qpl.
- Cas mixte : 2 omissions + 1 doublon + 1 mauvaise famille, comptes et liste
  exacts.
- Rattachement : page humaine nommée « PLANS-TEST - 2 » (→ E200 par le nom)
  dont le raster est tourné d'un quart de tour → recalée par la géométrie sur
  E100 (mauvais_rattachement_feuille) ; un couple EXISTANT vs FOURNI/INSTALLÉ
  ajoute une mauvaise_portee.
- Aucun désaccord → sorties vides sans erreur ; en_trop au-delà du seuil de
  doublon (1,2 % de la diagonale du raster IA, distance en pixels IA).
"""
from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

import pytest

from conftest import run_cli
from src.validation import classer_ecarts as ce
from src.validation import compare_qpl as cq

IA_L, IA_H = 1000, 700
ENTETE = ",".join(ce.EN_TETE_CSV)


def _grille(n: int, x0: int, y0: int, pas: int = 90, colonnes: int = 5) -> list[tuple[int, int]]:
    return [(x0 + (i % colonnes) * pas + (i // colonnes) * 17, y0 + (i // colonnes) * pas)
            for i in range(n)]


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
        corps.append(f'<Plan Name="{nom}" FileName="{fichier}"><Layers><Layer Index="0" Name="Calque">'
                     f'{"".join(compteurs)}</Layer></Layers></Plan>')
    return ('<?xml version="1.0"?><QuoterPlanSession><Project Name="synthetique"/>'
            f'<Plans>{"".join(corps)}</Plans></QuoterPlanSession>')


def _charger(d: Path, nom: str, humain_xml: str, ia_xml: str,
             dims_rows: list[str], feuilles_rows: list[tuple], dossier: str,
             rasters_ia: Path | None = None) -> cq.Comparaison:
    """Écrit les 4 fichiers d'entrée (qpl, dims, feuilles) et fait tourner le
    pipeline compare_qpl (lire → préparer → comparer), comme la CLI."""
    humain = d / f"{nom}-dupuis.qpl"
    humain.write_text(humain_xml, encoding="utf-8")
    ia = d / "ia" / f"{nom}.qpl"
    ia.parent.mkdir(parents=True, exist_ok=True)
    ia.write_text(ia_xml, encoding="utf-8")
    dims = d / "png-dimensions.txt"
    dims.write_text("\n".join(dims_rows) + "\n", encoding="utf-8")
    feuilles = d / "feuilles.csv"
    with feuilles.open("w", encoding="utf-8", newline="") as flux:
        w = csv.writer(flux)
        w.writerow(["feuille", "fichier", "page", "largeur_pt", "hauteur_pt", "raster_px",
                    "classement_fichier"])
        for i, (feuille, page) in enumerate(feuilles_rows, start=1):
            w.writerow([feuille, "PLANS-TEST.pdf", page, "1000", "700", f"{IA_L}x{IA_H}", "plans"])
    humains = cq.lire_qpl(humain, "humain")
    ias = cq.lire_qpl(ia, "ia")
    cq.preparer_humain(humains, cq.lire_dimensions(dims, dossier))
    anomalies = cq.preparer_ia(ias, cq.lire_feuilles(feuilles), rasters_ia)
    return cq.comparer(humains, ias, anomalies)


# --- Cas mixte : 2 omissions + 1 doublon + 1 mauvaise famille -------------------

@pytest.fixture(scope="module")
def comp_mixte(tmp_path_factory) -> cq.Comparaison:
    d = tmp_path_factory.mktemp("classer_mixte")
    ia = [("PRISE", 300, 300), ("TROFFER", 400, 300), ("PRISE", 500, 300), ("PRISE", 509, 300)]
    humain = [("PRISE", 2 * 300, 2 * 300), ("PRISE DOUBLE", 2 * 400, 2 * 300),
              ("PRISE", 2 * 500, 2 * 300), ("PRISE", 2 * 700, 2 * 300),
              ("PANNEAU", 2 * 800, 2 * 300)]
    return _charger(d, "S-8888", _qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png", humain)]),
                    _qpl([("E100", "E100.png", ia)]),
                    ["S-8888 (fictif)|PLANS-TEST - 1.png|2000|1400"],
                    [("E100", 1)], "S-8888")


def test_cas_mixte_comptes_et_liste_exacte(comp_mixte):
    ecarts = ce.classer(comp_mixte)
    assert Counter(e.classe for e in ecarts) == {"omission": 2, "doublon": 1, "mauvaise_famille": 1}
    assert isinstance(ecarts[0], ce.EcartClasse)
    omissions = [e for e in ecarts if e.classe == "omission"]
    # tri déterministe : par classe puis libellé humain (PANNEAU < PRISE)
    assert [(e.libelle_humain, e.position_humaine, e.position_ia, e.feuille_ia)
            for e in omissions] == [("PANNEAU", "800:300", "", "E100"),
                                    ("PRISE", "700:300", "", "E100")]
    assert all(e.feuille_humaine == "PLANS-TEST - 1" and e.libelle_ia == "" for e in omissions)
    doublon = [e for e in ecarts if e.classe == "doublon"][0]
    assert (doublon.feuille_humaine, doublon.feuille_ia) == ("PLANS-TEST - 1", "E100")
    assert (doublon.libelle_humain, doublon.libelle_ia) == ("PRISE", "PRISE")
    assert (doublon.position_humaine, doublon.position_ia) == ("500:300", "509:300")
    # 9 px < 1,2 % de la diagonale (14,6 px) → deux marques IA pour la même marque humaine
    assert "deux marques IA" in doublon.detail and "PRISE" in doublon.detail
    famille = [e for e in ecarts if e.classe == "mauvaise_famille"][0]
    assert (famille.libelle_humain, famille.libelle_ia) == ("PRISE DOUBLE", "TROFFER")
    assert famille.position_humaine == famille.position_ia == "400:300"
    assert "dispositif (humain)" in famille.detail and "luminaire (IA" in famille.detail
    # le couple PRISE/PRISE du doublon n'est ni famille ni portée divergente
    assert not [e for e in ecarts if e.classe == "mauvaise_portee"]
    assert not [e for e in ecarts if e.classe == "mauvais_rattachement_feuille"]
    assert not [e for e in ecarts if e.classe == "en_trop"]


def test_tri_deterministe(comp_mixte):
    a, b = ce.classer(comp_mixte), ce.classer(comp_mixte)
    assert a == b
    rangs = [ce.CLASSES.index(e.classe) for e in a]
    assert rangs == sorted(rangs)


@pytest.fixture(scope="module")
def projets_mixte(tmp_path_factory) -> dict[str, Path]:
    d = tmp_path_factory.mktemp("classer_cli")
    ia = [("PRISE", 300, 300), ("TROFFER", 400, 300), ("PRISE", 500, 300), ("PRISE", 509, 300)]
    humain = [("PRISE", 2 * 300, 2 * 300), ("PRISE DOUBLE", 2 * 400, 2 * 300),
              ("PRISE", 2 * 500, 2 * 300), ("PRISE", 2 * 700, 2 * 300),
              ("PANNEAU", 2 * 800, 2 * 300)]
    humain_qpl = d / "S-8888-dupuis.qpl"
    humain_qpl.write_text(_qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png", humain)]), encoding="utf-8")
    ia_qpl = d / "ia" / "S-8888.qpl"
    ia_qpl.parent.mkdir()
    ia_qpl.write_text(_qpl([("E100", "E100.png", ia)]), encoding="utf-8")
    dims = d / "png-dimensions.txt"
    dims.write_text("S-8888 (fictif)|PLANS-TEST - 1.png|2000|1400\n", encoding="utf-8")
    feuilles = d / "feuilles.csv"
    with feuilles.open("w", encoding="utf-8", newline="") as flux:
        w = csv.writer(flux)
        w.writerow(["feuille", "fichier", "page", "largeur_pt", "hauteur_pt", "raster_px",
                    "classement_fichier"])
        w.writerow(["E100", "PLANS-TEST.pdf", 1, "1000", "700", f"{IA_L}x{IA_H}", "plans"])
    return {"dossier": d, "humain": humain_qpl, "ia": ia_qpl, "dims": dims, "feuilles": feuilles}


def test_cli_ecarts_classes(projets_mixte):
    sortie = projets_mixte["dossier"] / "sortie"
    run_cli("-m", "src.validation.classer_ecarts", "--humain", str(projets_mixte["humain"]),
            "--ia", str(projets_mixte["ia"]), "--dims", str(projets_mixte["dims"]),
            "--feuilles", str(projets_mixte["feuilles"]), "--sortie", str(sortie))
    lignes = (sortie / "ecarts-classes.csv").read_text(encoding="utf-8").strip().splitlines()
    assert lignes[0] == ENTETE
    comptes = Counter(l.split(",")[0] for l in lignes[1:])
    assert comptes == {"omission": 2, "doublon": 1, "mauvaise_famille": 1}
    rapport = (sortie / "ecarts-classes.md").read_text(encoding="utf-8")
    assert "| omission | 2 |" in rapport and "| doublon | 1 |" in rapport
    assert "TROFFER" in rapport and "509:300" in rapport


# --- Rattachement de feuille + portée -------------------------------------------

@pytest.fixture(scope="module")
def comp_rattachement(tmp_path_factory) -> cq.Comparaison:
    d = tmp_path_factory.mktemp("classer_rattachement")
    p_ia = _grille(20, 120, 110, pas=110, colonnes=7)
    ia = ([("PRISE FOURNIE ET INSTALLEE", *p_ia[0])]
          + [("PRISE", *p) for p in p_ia[1:]])
    # raster humain portrait 1400×2000, contenu tourné d'un quart de tour
    humain = ([("PRISE EXISTANTE", 2 * (IA_H - p_ia[0][1]), 2 * p_ia[0][0])]
              + [("PRISE", 2 * (IA_H - y), 2 * x) for x, y in p_ia[1:]])
    return _charger(d, "S-7777", _qpl([("PLANS-TEST - 2", "PLANS-TEST - 2.png", humain)]),
                    _qpl([("E100", "E100.png", ia), ("E200", "E200.png", [])]),
                    ["S-7777 (fictif)|PLANS-TEST - 2.png|1400|2000"],
                    [("E100", 1), ("E200", 2)], "S-7777")


def test_rattachement_et_portee(comp_rattachement):
    ecarts = ce.classer(comp_rattachement)
    assert Counter(e.classe for e in ecarts) == {
        "mauvaise_portee": 1, "mauvais_rattachement_feuille": 1}
    r = [e for e in ecarts if e.classe == "mauvais_rattachement_feuille"][0]
    assert (r.feuille_humaine, r.feuille_ia) == ("PLANS-TEST - 2", "E100")
    assert r.libelle_humain == "" and r.libelle_ia == "" and r.position_ia == ""
    assert "E200" in r.detail and "E100" in r.detail and "1.00" in r.detail
    p = [e for e in ecarts if e.classe == "mauvaise_portee"][0]
    assert (p.libelle_humain, p.libelle_ia) == ("PRISE EXISTANTE", "PRISE FOURNIE ET INSTALLEE")
    assert p.position_humaine == p.position_ia == "120:110"   # p_ia[0] de la grille
    assert "existant" in p.detail and "neuf" in p.detail
    # la famille est la même des deux côtés (PRISE) : pas de mauvaise_famille
    assert not [e for e in ecarts if e.classe == "mauvaise_famille"]
    assert not [e for e in ecarts if e.classe in ("omission", "doublon", "en_trop")]


# --- Aucun désaccord / en_trop au-delà du seuil ----------------------------------

def test_aucun_desaccord_sorties_vides(tmp_path):
    d = tmp_path
    p = _grille(4, 300, 300)
    comp = _charger(d, "S-5555", _qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png",
                                        [("PRISE", 2 * x, 2 * y) for x, y in p])]),
                    _qpl([("E100", "E100.png", [("PRISE", x, y) for x, y in p])]),
                    ["S-5555 (fictif)|PLANS-TEST - 1.png|2000|1400"], [("E100", 1)], "S-5555")
    ecarts = ce.classer(comp)
    assert ecarts == []
    counts = ce.ecrire_sorties(ecarts, d / "sortie")
    assert counts == {}
    assert (d / "sortie" / "ecarts-classes.csv").read_text(encoding="utf-8").splitlines() == [ENTETE]
    rapport = (d / "sortie" / "ecarts-classes.md").read_text(encoding="utf-8")
    assert "Aucun désaccord classé" in rapport


def test_en_trop_au_dela_du_seuil_doublon(tmp_path):
    d = tmp_path
    seuil_px = ce.SEUIL_DOUBLON * math.hypot(IA_L, IA_H)
    assert 9 < seuil_px < 30           # (300,300)+9 px → doublon ; +30 px → en_trop
    comp = _charger(d, "S-4444", _qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png",
                                        [("PRISE", 2 * 300, 2 * 300)])]),
                    _qpl([("E100", "E100.png", [("PRISE", 300, 300), ("PRISE", 309, 300),
                                                ("PRISE", 330, 300)])]),
                    ["S-4444 (fictif)|PLANS-TEST - 1.png|2000|1400"], [("E100", 1)], "S-4444")
    ecarts = ce.classer(comp)
    assert Counter(e.classe for e in ecarts) == {"doublon": 1, "en_trop": 1}
    assert [e.position_ia for e in ecarts if e.classe == "doublon"] == ["309:300"]
    assert [e.position_ia for e in ecarts if e.classe == "en_trop"] == ["330:300"]


# --- Contrat CSV (en-tête exact, citation des virgules, UTF-8) --------------------

def test_csv_contrat_entete_et_citation(tmp_path):
    ecarts = [
        ce.EcartClasse(classe="omission", feuille_humaine="PAGE A, VIRGULE",
                       feuille_ia="E100", libelle_humain="PRISE « DOUBLE », 15 A",
                       libelle_ia="", position_humaine="12:34", position_ia=""),
        ce.EcartClasse(classe="mauvais_rattachement_feuille", feuille_humaine="P - 3",
                       feuille_ia="E200", detail="le nom désignait E300"),
    ]
    counts = ce.ecrire_sorties(ecarts, tmp_path / "s")
    assert counts == {"omission": 1, "mauvais_rattachement_feuille": 1}
    texte = (tmp_path / "s" / "ecarts-classes.csv").read_text(encoding="utf-8")
    lignes = texte.splitlines()
    assert lignes[0] == ENTETE
    assert '"PAGE A, VIRGULE"' in lignes[1]        # virgule citée
    assert '"PRISE « DOUBLE », 15 A"' in lignes[1]
    assert lignes[2] == "mauvais_rattachement_feuille,P - 3,E200,,,,,le nom désignait E300"
    rapport = (tmp_path / "s" / "ecarts-classes.md").read_text(encoding="utf-8")
    assert "| PAGE A, VIRGULE |" in rapport
    assert "## mauvais_rattachement_feuille (1)" in rapport


# --- Heuristique de portée --------------------------------------------------------

def test_portee_heuristique():
    assert ce.portee("PRISE EXISTANTE") == "existant"
    assert ce.portee("EXIT EXISTANT À CONSERVER") == "existant"
    assert ce.portee("EX") == "existant"
    assert ce.portee("EXIT") is None            # panneau de sortie ≠ existant
    assert ce.portee("PRISE NEUF") == "neuf"
    assert ce.portee("PRISE N.F") == "neuf"     # point du sigle → bigramme N F
    assert ce.portee("PRISE NF") == "neuf"
    assert ce.portee("LUMINAIRE FOURNI ET INSTALLÉ") == "neuf"
    assert ce.portee("TROFFER") is None
    assert ce.portee("") is None
    assert ce.portees_divergentes("PRISE EXISTANTE", "PRISE FOURNIE ET INSTALLEE")
    assert not ce.portees_divergentes("PRISE EXISTANTE", "PRISE")   # une seule portée affirmée
    assert not ce.portees_divergentes("PRISE", "PRISE")
    assert not ce.portees_divergentes("PRISE NEUF", "PRISE NEW")