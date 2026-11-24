"""Tests de l'orchestrateur de la boucle d'acceptation
(`src.validation.boucle_acceptation`) : chaîne aveugle → gel → comparaison →
classification → justifications → ACCEPTATION.md, sur fixtures synthétiques
(mini relevé IA + mini référence estimateur, aucune donnée client).

Règles vérifiées :
- référence complète → ACCEPTATION.md écrit, désaccords classés (contrat gelé
  `ecarts-classes.csv`), dossier de justification généré ;
- référence absente → VÉRIFICATION INCOMPLÈTE, comparaison jamais lancée ;
- workdir non aveugle → INVALIDE, comparaison jamais lancée ;
- artefact modifié/supprimé après le gel → INVALIDE « gel violé », comparaison
  jamais relancée — y compris quand le .qpl IA vit hors du workdir ;
- dossier de justification entièrement tranché → relance = PRÊT POUR
  DÉCISION FRANCIS (le dossier rempli n'est jamais écrasé).
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

import pymupdf as pdf
import pytest
from PIL import Image

from src.validation import aveugle, boucle_acceptation as boucle, recalage_sources

from conftest import env_sans_encodage

ROOT = Path(__file__).resolve().parents[1]

EN_TETE_CONTRAT = [
    "classe", "feuille_humaine", "feuille_ia", "libelle_humain",
    "libelle_ia", "position_humaine", "position_ia", "detail",
]


def _qpl(plans: list[tuple[str, str, list[tuple[str, int, int]]]]) -> str:
    """plans : (Name, FileName, [(libellé, x, y)]) → XML Plan Expert minimal."""
    corps = []
    for nom, fichier, marques in plans:
        par: dict[str, list[tuple[int, int]]] = {}
        for lib, x, y in marques:
            par.setdefault(lib, []).append((x, y))
        compteurs = ""
        for gid, (lib, pts) in enumerate(par.items(), start=1):
            elements = "".join(
                f'<Element X="{x}" Y="{y}" Width="20" Height="20"/>' for x, y in pts)
            compteurs += f'<Counter Name="{lib}" GroupID="{gid}">{elements}</Counter>'
        corps.append(f'<Plan Name="{nom}" FileName="{fichier}"><Layers>'
                     f'<Layer Index="0" Name="Calque">{compteurs}</Layer></Layers></Plan>')
    return ('<?xml version="1.0"?><QuoterPlanSession><Project Name="synthetique"/>'
            f'<Plans>{"".join(corps)}</Plans></QuoterPlanSession>')


# 3 marques IA ; le relevé humain posé à l'échelle 2 (raster 2000×1400 vu dans
# un raster IA 1000×700, recalage identité 0,5) + 1 marque en plus → omission.
GRILLE_IA = [("PRISE", 150, 150), ("PRISE", 240, 150), ("PRISE", 330, 150)]
GRILLE_HU = [(lib, 2 * x, 2 * y) for lib, x, y in GRILLE_IA] + [("PRISE", 1600, 1200)]


def _fabriquer(d: Path, *, avec_reference: bool = True,
               qpl_ia_ou: str = "travail") -> dict[str, Path]:
    """Mini dossier S-TEST : workdir du relevé IA + référence de l'estimateur.
    `qpl_ia_ou` : « travail » (.qpl IA dans le workdir, gélé) ou « planexpert »
    (.qpl IA dans dossiers/S-TEST/planexpert/, hors workdir)."""
    workdir = d / "OUTBOX" / "S-TEST" / "travail"
    workdir.mkdir(parents=True)
    dossier = d / "dossiers" / "S-TEST"
    ref = dossier / "reference"
    ref.mkdir(parents=True)
    (workdir / "nomenclature.csv").write_text("libelle,quantite\nPRISE,3\n", encoding="utf-8")
    (workdir / "occurrences-texte.csv").write_text(
        "feuille,libelle,x,y\nE100,PRISE,150,150\n", encoding="utf-8")
    (workdir / "feuilles-classement.csv").write_text(
        "feuille,classement_fichier\nE100,plans\n", encoding="utf-8")
    (workdir / "reserves.md").write_text("Aucune reserve.\n", encoding="utf-8")
    if qpl_ia_ou == "travail":
        (workdir / "S-TEST.qpl").write_text(_qpl([("E100", "E100.png", GRILLE_IA)]),
                                            encoding="utf-8")
    else:
        pe = dossier / "planexpert"
        pe.mkdir()
        (pe / "S-TEST.qpl").write_text(_qpl([("E100", "E100.png", GRILLE_IA)]),
                                       encoding="utf-8")
    if avec_reference:
        (ref / "S-TEST-Dupuis-PlanExpert.qpl").write_text(
            _qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png", GRILLE_HU)]), encoding="utf-8")
        (ref / "dupuis-png-dimensions.txt").write_text(
            "S-TEST|PLANS-TEST - 1.png|2000|1400\n", encoding="utf-8")
        with (ref / "feuilles-ia.csv").open("w", encoding="utf-8", newline="") as flux:
            w = csv.writer(flux)
            w.writerow(["feuille", "fichier", "page", "largeur_pt", "hauteur_pt",
                        "raster_px", "classement_fichier"])
            w.writerow(["E100", "PLANS-TEST.pdf", "1", "1000", "700", "1000x700", "plans"])
    return {"workdir": workdir, "dossier": dossier, "ref": ref}


def _sans_comparer(monkeypatch) -> list[int]:
    """Neutralise `compare_qpl.comparer` : tout appel dans ces tests serait un
    bug (INVALIDE et VÉRIFICATION INCOMPLÈTE ne doivent jamais comparer)."""
    appels: list[int] = []

    def boom(*_a, **_k):
        appels.append(1)
        raise AssertionError("compare_qpl.comparer ne doit pas être appelé ici")

    monkeypatch.setattr(boucle.cq, "comparer", boom)
    return appels


@pytest.fixture()
def sans_comparaison(monkeypatch) -> list[int]:
    return _sans_comparer(monkeypatch)


def test_boucle_complete_avec_reference(tmp_path):
    """Fixtures complètes → ACCEPTATION.md écrit, désaccord classé selon le
    contrat gelé, dossier de justification généré, verdict JUSTIFICATIONS REQUISES."""
    f = _fabriquer(tmp_path)
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_JUSTIF
    assert rapport.compteurs == {"omission": 1}
    assert bool(rapport) is False   # JUSTIFICATIONS REQUISES : boucle bloquée avant la décision
    # ACCEPTATION.md présent, non vide, verdict en ligne machine-lisible
    md = f["dossier"] / "ACCEPTATION.md"
    assert md.is_file() and md.stat().st_size > 0
    texte = md.read_text(encoding="utf-8")
    assert "**Verdict : JUSTIFICATIONS REQUISES**" in texte
    # contrôle aveugle + gel dans le workdir
    av = json.loads((f["workdir"] / "controle-aveugle.json").read_text(encoding="utf-8"))
    assert av["aveugle"] is True
    gel_j = json.loads((f["workdir"] / "gel.json").read_text(encoding="utf-8"))
    artefacts = {a["fichier"] for a in gel_j["artefacts"]}
    assert "nomenclature.csv" in artefacts and "S-TEST.qpl" in artefacts
    # comparaison (relève humaine 4 marques, IA 3, appariées 3) + classification
    assert rapport.totaux_marques["humaines"] == 4 and rapport.totaux_marques["appariees"] == 3
    sortie = f["dossier"] / "comparaison-dupuis-qpl"
    with (sortie / "ecarts-classes.csv").open(encoding="utf-8", newline="") as flux:
        lignes = list(csv.reader(flux))
    assert lignes[0] == EN_TETE_CONTRAT          # contrat gelé : en-tête exact
    assert [l[0] for l in lignes[1:]] == ["omission"]
    assert lignes[1][1] == "PLANS-TEST - 1" and lignes[1][2] == "E100"
    # dossier de justification généré, l'écart y figure
    justif = (f["dossier"] / "justifications.md").read_text(encoding="utf-8")
    assert "omission" in justif and "PRISE" in justif


def test_reference_absente_verification_incomplete(tmp_path, sans_comparaison):
    """Pas de référence de l'estimateur → VÉRIFICATION INCOMPLÈTE (étape 8),
    comparaison jamais lancée, aucun classement ni dossier de justification."""
    f = _fabriquer(tmp_path, avec_reference=False)
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INCOMPLET
    assert bool(rapport) is True    # rien à corriger dans le relevé : boucle non bloquée… mais rien de prouvé
    assert not sans_comparaison
    assert not (f["dossier"] / "comparaison-dupuis-qpl").exists()
    assert not (f["dossier"] / "justifications.md").exists()
    texte = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : VÉRIFICATION INCOMPLÈTE**" in texte
    assert "pas pire que l'estimateur" in texte     # étape 8 : jamais certifié sans vérif
    assert "S-TEST-Dupuis-PlanExpert.qpl" in rapport.motif


def test_reference_partielle_verification_incomplete(tmp_path, sans_comparaison):
    """Une seule pièce de référence manquante (dimensions) suffit au verdict
    VÉRIFICATION INCOMPLÈTE, avec la pièce absente nommée."""
    f = _fabriquer(tmp_path)
    (f["ref"] / "dupuis-png-dimensions.txt").unlink()
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INCOMPLET
    assert "dupuis-png-dimensions.txt" in rapport.motif
    assert not sans_comparaison


def test_non_aveugle_par_nom_invalide_sans_compare(tmp_path, sans_comparaison):
    """Matériau de l'estimateur NOMMÉ comme le projet Dupuis dans le workdir →
    INVALIDE, comparaison jamais lancée."""
    f = _fabriquer(tmp_path)
    (f["workdir"] / "S-TEST-Dupuis-PlanExpert.qpl").write_text(
        "<QuoterPlanSession/>", encoding="utf-8")
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INVALIDE
    assert bool(rapport) is False
    assert not sans_comparaison
    assert not (f["dossier"] / "comparaison-dupuis-qpl").exists()
    assert not (f["dossier"] / "justifications.md").exists()
    texte = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : INVALIDE**" in texte
    assert "S-TEST-Dupuis-PlanExpert.qpl" in texte   # le fichier fautif est nommé


def test_non_aveugle_par_contenu_invalide_sans_compare(tmp_path, sans_comparaison):
    """La signature « estimateur » dans le TEXTE d'un artefact du workdir
    suffit : INVALIDE au premier étage, aucune comparaison, aucun classement."""
    f = _fabriquer(tmp_path)
    (f["workdir"] / "nomenclature.csv").write_text(
        "libelle,quantite\nPRISE (copie du relevé de l'estimateur),3\n", encoding="utf-8")
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INVALIDE
    assert not sans_comparaison
    assert "nomenclature.csv" in (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")


def test_gel_viole_invalide_gel_viole(tmp_path, monkeypatch):
    """Artefact gélé modifié après le gel → INVALIDE « gel violé », comparaison
    jamais relancée (le relevé n'est plus le résultat à l'aveugle d'origine)."""
    f = _fabriquer(tmp_path)
    premier = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert premier.verdict == boucle.VERDICT_JUSTIF      # première boucle : comparaison faite
    (f["workdir"] / "nomenclature.csv").write_text("libelle,quantite\nPRISE,99\n",
                                                   encoding="utf-8")
    _sans_comparer(monkeypatch)                          # neutralisée pour la relance
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INVALIDE
    assert boucle.MOTIF_GEL_VIOLE in rapport.motif
    comparaison = f["dossier"] / "comparaison-dupuis-qpl"
    assert comparaison.is_dir()          # reste de la première boucle (gelée)
    textes_avant = sorted(p.read_bytes() for p in comparaison.iterdir())
    boucle.executer("S-TEST", f["workdir"], f["dossier"])   # 3e relance : toujours INVALIDE
    assert sorted(p.read_bytes() for p in comparaison.iterdir()) == textes_avant
    texte = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "gel violé" in texte
    assert "nomenclature.csv" in texte                   # l'artefact fautif est nommé


def test_qpl_ia_disparu_gel_invalide(tmp_path, monkeypatch):
    """Le .qpl IA gélé supprimé après le gel → INVALIDE « gel violé »
    (disparu) : le gel couvre tout ce que la comparaison lit."""
    f = _fabriquer(tmp_path)
    assert boucle.executer("S-TEST", f["workdir"], f["dossier"]).verdict == boucle.VERDICT_JUSTIF
    (f["workdir"] / "S-TEST.qpl").unlink()
    _sans_comparer(monkeypatch)
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_INVALIDE
    assert boucle.MOTIF_GEL_VIOLE in rapport.motif


def test_qpl_ia_dans_dossier_agrandit_le_gel(tmp_path, monkeypatch):
    """Quand le .qpl IA vit hors du workdir (dossier assemblé : planexpert/),
    la comparaison l'utilise quand même — et une modification post-gel est
    détectée (le gel l'a couvert)."""
    f = _fabriquer(tmp_path, qpl_ia_ou="planexpert")
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_JUSTIF
    gel_j = json.loads((f["workdir"] / "gel.json").read_text(encoding="utf-8"))
    geles = [a["fichier"] for a in gel_j["artefacts"]]
    assert any("planexpert" in x and x.endswith("S-TEST.qpl") for x in geles)
    qpl = f["dossier"] / "planexpert" / "S-TEST.qpl"
    qpl.write_text("<QuoterPlanSession/>", encoding="utf-8")   # modifié après le gel
    _sans_comparer(monkeypatch)
    rapport2 = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport2.verdict == boucle.VERDICT_INVALIDE
    assert boucle.MOTIF_GEL_VIOLE in rapport2.motif


def test_dossier_rempli_relanche_pret(tmp_path):
    """Dossier de justification entièrement tranché → relance donne
    PRÊT POUR DÉCISION FRANCIS, et le dossier rempli n'est jamais écrasé."""
    f = _fabriquer(tmp_path)
    assert bool(boucle.executer("S-TEST", f["workdir"], f["dossier"])) is False
    justif = f["dossier"] / "justifications.md"
    rempli = justif.read_text(encoding="utf-8").replace(
        "|  |  |",
        "| plan PLANS-TEST - 1 (zoom ×8) : aucun appareil vu | IA correcte |")
    justif.write_text(rempli, encoding="utf-8")
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_PRET
    assert bool(rapport) is True
    assert justif.read_text(encoding="utf-8") == rempli    # jamais écrasé
    texte = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : PRÊT POUR DÉCISION FRANCIS**" in texte


@pytest.mark.parametrize("decision", ["estimateur correct", "ambigu → réserve"])
def test_justification_ne_corrige_pas_le_releve(tmp_path, decision):
    f = _fabriquer(tmp_path)
    boucle.executer("S-TEST", f["workdir"], f["dossier"])
    path = f["dossier"] / "justifications.md"
    path.write_text(path.read_text(encoding="utf-8").replace(
        "|  |  |", f"| Témoin sur le plan E101 p.1, (240, 420) | {decision} |"), encoding="utf-8")
    assert boucle.executer("S-TEST", f["workdir"], f["dossier"]).verdict == boucle.VERDICT_JUSTIF


def test_verdict_acceptation_lecture_seule(tmp_path):
    """verdict_acceptation : lit le verdict d'ACCEPTATION.md, None si absent —
    lecture seule (utilisé par le jeu de référence)."""
    f = _fabriquer(tmp_path)
    assert boucle.verdict_acceptation(f["dossier"]) is None
    boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert boucle.verdict_acceptation(f["dossier"]) == boucle.VERDICT_JUSTIF


def test_comparaison_dans_sortie_distincte_ne_modifie_pas_historique(tmp_path):
    f = _fabriquer(tmp_path)
    historique = f["dossier"] / "ACCEPTATION.md"
    historique.write_text("Historique à conserver.\n", encoding="utf-8")
    destination = tmp_path / "OUTBOX" / "acceptation"
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"], sortie=destination)
    assert historique.read_text(encoding="utf-8") == "Historique à conserver.\n"
    assert not (f["dossier"] / "comparaison-dupuis-qpl").exists()
    assert rapport.verdict == boucle.verdict_acceptation(destination) == boucle.VERDICT_JUSTIF
    assert (destination / "comparaison-dupuis-qpl" / "ecarts-classes.csv").is_file()
    assert (destination / "justifications.md").is_file()


def test_sortie_comparaison_interdite_dans_travail(tmp_path):
    f = _fabriquer(tmp_path)
    with pytest.raises(boucle.BoucleErreur, match="hors du dossier aveugle"):
        boucle.executer("S-TEST", f["workdir"], f["dossier"], sortie=f["workdir"] / "comparaison")


def test_cli_boucle(tmp_path):
    """CLI `python -m src.validation.boucle_acceptation S-TEST --workdir W
    --dossier D` : code 1 (désaccords non tranchés), dernière ligne VERDICT ;
    entrée introuvable → code 2 avec diagnostic."""
    f = _fabriquer(tmp_path)
    p = subprocess.run(
        [sys.executable, "-m", "src.validation.boucle_acceptation", "S-TEST",
         "--workdir", str(f["workdir"]), "--dossier", str(f["dossier"])],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage())
    assert p.returncode == 1, f"stdout={p.stdout}\nstderr={p.stderr}"
    lignes = [l for l in p.stdout.splitlines() if l.startswith("VERDICT : ")]
    assert lignes and lignes[-1] == f"VERDICT : {boucle.VERDICT_JUSTIF}"
    assert (f["dossier"] / "ACCEPTATION.md").is_file()

    p2 = subprocess.run(
        [sys.executable, "-m", "src.validation.boucle_acceptation", "S-TEST",
         "--workdir", str(tmp_path / "absent"), "--dossier", str(f["dossier"])],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage())
    assert p2.returncode == 2 and "ERREUR" in p2.stderr


def test_erreurs_entree(tmp_path):
    """Dossier ou workdir inexistant → erreur d'entrée refusée (exception
    typée), jamais corrigée en silence."""
    f = _fabriquer(tmp_path)
    with pytest.raises(boucle.BoucleErreur):
        boucle.executer("S-TEST", f["workdir"], tmp_path / "dossiers" / "Absent")
    with pytest.raises(aveugle.AveugleErreur):
        boucle.executer("S-TEST", tmp_path / "absent", f["dossier"])


def _plan_synthetique(chemin, feuille, *, revise=False):
    with pdf.open() as doc:
        p = doc.new_page(width=1000, height=700)
        p.draw_rect(pdf.Rect(100, 100, 620, 540), width=4)
        p.draw_line(pdf.Point(100, 440), pdf.Point(620, 100), width=3)
        p.draw_rect(pdf.Rect(750, 470, 960, 660), width=3)
        if revise:
            p.insert_text((760, 505), "1 POUR ADDENDA 2026-03-12", fontsize=10)
        p.insert_text((760, 530), "0 POUR SOUMISSIONS 2026-02-06", fontsize=10)
        p.insert_text((770, 635), feuille, fontsize=28)
        doc.save(chemin)


def _raster_synthetique(source, destination):
    with pdf.open(source) as doc:
        pix = doc[0].get_pixmap(matrix=pdf.Matrix(2, 2), colorspace=pdf.csGRAY)
        fond = Image.new("L", (2080, 1440), 255)
        fond.paste(Image.frombytes("L", (pix.width, pix.height), pix.samples), (80, 40))
        fond.save(destination)


@pytest.fixture
def strict(tmp_path):
    f = _fabriquer(tmp_path)
    inbox = tmp_path / "plans-seuls"
    inbox.mkdir()
    actif, ancien = inbox / "Addenda-plans.pdf", inbox / "Plans-ao.pdf"
    _plan_synthetique(actif, "E100", revise=True)
    _plan_synthetique(ancien, "E100")
    fichiers = [{"fichier": p.name, "sha256": sha256(p.read_bytes()).hexdigest(),
                 "classement": k, "pages": 1} for p, k in [(actif, "addenda"), (ancien, "plans")]]
    inv = {"inbox": str(inbox), "plans_seuls": True, "fichiers": fichiers,
           "revisions": {"actives": {actif.name: {"1": "E100"}},
                         "remplacees": {ancien.name: {"1": "E100 → Addenda-plans p.1"}}}}
    w, ref = f["workdir"], f["ref"]
    (w / "inventaire.json").write_text(json.dumps(inv), encoding="utf-8")
    (w / "feuilles.csv").write_text("feuille,fichier,page,raster_px\nE100,Addenda-plans.pdf,1,1000x700\n",
                                  encoding="utf-8")
    humain = ref / "S-TEST-Dupuis-PlanExpert.qpl"
    nom_actif, nom_ancien = "Tirage R1 - 1.png", "Tirage AO - 1.jpg"
    marques = [(lib, 2 * x + 80, 2 * y + 40) for lib, x, y in GRILLE_IA]
    humain.write_text(_qpl([("R1", nom_actif, marques), ("AO", nom_ancien, marques)]), encoding="utf-8")
    # Fichier de dimensions historique vide : les deux dimensions attestées
    # doivent être lues sur le vrai raster, et non extrapolées depuis les marques.
    (ref / "dupuis-png-dimensions.txt").write_text("", encoding="utf-8")
    (ref / "rasters").mkdir()
    pts = [(100, 100), (620, 100), (100, 540), (960, 660)]
    calages = {}
    for p, fichier, rev, nom in zip((actif, ancien), fichiers, ("2026-03-12", "2026-02-06"), (nom_actif, nom_ancien)):
        raster = ref / "rasters" / nom
        _raster_synthetique(p, raster)
        calages[nom] = {"pdf_sha256": fichier["sha256"], "page": 1, "feuille": "E100", "revision": rev,
                        "raster_sha256": sha256(raster.read_bytes()).hexdigest(),
                        "preuve": "Cartouche et coins du tracé synthétique contrôlés.",
                        "ancres": [[[(2 * x + 80) / 2080, (2 * y + 40) / 1440], [x / 1000, y / 700]]
                                   for x, y in pts]}
    donnees = {"version": 1, "qpl_sha256": sha256(humain.read_bytes()).hexdigest(),
               "documents": {"Tirage R1": fichiers[0]["sha256"], "Tirage AO": fichiers[1]["sha256"]}, "calages": calages}
    f.update(inbox=inbox, inv=inv, dest=tmp_path / "comparaison", actif=nom_actif, ancien=nom_ancien,
             humain=humain, donnees=donnees, attestation=ref / recalage_sources.NOM_ATTESTATION)
    return f


def _comparer_strict(f):
    f["attestation"].write_text(json.dumps(f["donnees"]), encoding="utf-8")
    return boucle.executer("S-TEST", f["workdir"], f["dossier"], sortie=f["dest"])


def _csv_strict(f, nom):
    with (f["dest"] / "comparaison-dupuis-qpl" / nom).open(encoding="utf-8", newline="") as flux:
        return list(csv.DictReader(flux))


def test_fonds_attestes_independants_des_positions(strict):
    r = _comparer_strict(strict)
    assert r.verdict == boucle.VERDICT_PRET
    assert r.totaux_marques["appariees"] == r.totaux_marques["humaines"] == 3
    assert [p["etat"] for p in _csv_strict(strict, "recalage-pages.csv")] == [
        recalage_sources.ATTESTEE, recalage_sources.REMPLACEE]
    hors = _csv_strict(strict, "marques-hors-comparaison.csv")
    assert len(hors) == 3 and all(p["raster"] == strict["ancien"] for p in hors)
    [page] = _csv_strict(strict, "pages.csv")
    assert page["methode"] == "fond attesté" and "translation (-40, -20)" in page["transformation"]
    assert not (strict["dossier"] / "ACCEPTATION.md").exists()


def test_fonds_absents_malgre_positions_identiques(strict):
    strict["donnees"]["calages"] = {}
    r = _comparer_strict(strict)
    assert r.verdict == boucle.VERDICT_INCOMPLET and not r.compteurs and not r.totaux_marques
    assert [p["etat"] for p in _csv_strict(strict, "recalage-pages.csv")] == [
        recalage_sources.A_VERIFIER, recalage_sources.REMPLACEMENT_PRESUME, "sans référence attestée"]
    assert len(_csv_strict(strict, "marques-hors-comparaison.csv")) == 9
    assert not _csv_strict(strict, "ecarts-classes.csv")
    md = (strict["dest"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "aucune paire de pages attestée" in md and "Comparaison non exécutée : aucun compteur." in md
    assert not (strict["dest"] / "justifications.md").exists()


@pytest.mark.parametrize("cas, message", [
    ("date", "révision courante"), ("fond", "fond ou cartouche différents"),
    ("ancien", "date du cartouche non confirmée"),
    ("ancre", "trop groupés ou alignés"), ("empreinte", "différent de l'attestation"),
    ("pagination", "contraire à l'identité PDF/page"),
])
def test_fausse_attestation_ne_permet_pas_de_comparer(strict, tmp_path, cas, message):
    a = strict["donnees"]["calages"][strict["actif"]]
    if cas == "date":
        a["revision"] = "2026-02-06"  # la date figure toujours au cartouche, mais n'est plus courante
    elif cas == "fond":
        faux = tmp_path / "fond.pdf"
        _plan_synthetique(faux, "T999", revise=True)
        with pdf.open(faux) as doc:
            doc[0].draw_rect(pdf.Rect(110, 120, 580, 510), color=(0, 0, 0), fill=(0, 0, 0))
            doc.saveIncr()
        raster = strict["ref"] / "rasters" / strict["actif"]
        _raster_synthetique(faux, raster)
        a["raster_sha256"] = sha256(raster.read_bytes()).hexdigest()  # exact, mais mauvais fond
    elif cas == "ancien":
        raster = strict["ref"] / "rasters" / strict["actif"]
        _raster_synthetique(strict["inbox"] / "Plans-ao.pdf", raster)
        a["raster_sha256"] = sha256(raster.read_bytes()).hexdigest()  # même dessin, révision différente
    elif cas == "ancre":
        a["ancres"] = [[[v, v], [v, v]] for v in [.1, .5, .9]]
    elif cas == "empreinte":
        a["raster_sha256"] = "0" * 64
    elif cas == "pagination":
        a["page"] = 2
    r = _comparer_strict(strict)
    assert r.verdict == boucle.VERDICT_INCOMPLET and not r.compteurs
    assert message in _csv_strict(strict, "recalage-pages.csv")[0]["note"]


def test_attestation_ne_reporte_pas_un_zero_non_verifie(strict):
    h = strict["humain"]
    h.write_text(_qpl([("R1", strict["actif"], [])]), encoding="utf-8")
    strict["donnees"]["qpl_sha256"] = sha256(h.read_bytes()).hexdigest()
    del strict["donnees"]["calages"][strict["ancien"]]
    assert _comparer_strict(strict).verdict == boucle.VERDICT_INCOMPLET
    assert "preuve_zero" in _csv_strict(strict, "recalage-pages.csv")[0]["note"]
    strict["donnees"]["calages"][strict["actif"]]["preuve_zero"] = "Aucun objet du périmètre dans le plan validé."
    r = _comparer_strict(strict)
    assert r.verdict == boucle.VERDICT_JUSTIF and r.compteurs == {"en_trop": 3}
    assert all("feuille IA sans page humaine" not in e["detail"] for e in _csv_strict(strict, "ecarts-classes.csv"))


def test_gel_strict_verifie_apres_lecture_de_la_reference(strict, monkeypatch):
    originale = recalage_sources.controler

    def mutation(*args, **kw):
        result = originale(*args, **kw)
        (strict["inbox"] / "Plans-ao.pdf").write_bytes(b"%PDF-1.4\nModifie pendant la comparaison")
        return result

    monkeypatch.setattr(recalage_sources, "controler", mutation)
    r = _comparer_strict(strict)
    assert r.verdict == boucle.VERDICT_INVALIDE and "pendant la comparaison" in r.motif
    assert not (strict["dest"] / "comparaison-dupuis-qpl").exists()


def test_plans_seuls_necrit_pas_dans_les_sources_ni_dans_la_reference(strict):
    for destination in (None, strict["dossier"], strict["inbox"] / "comparaison"):
        with pytest.raises(boucle.BoucleErreur, match="exige --sortie"):
            boucle.executer("S-TEST", strict["workdir"], strict["dossier"], sortie=destination)
    assert not (strict["workdir"] / "gel.json").exists()