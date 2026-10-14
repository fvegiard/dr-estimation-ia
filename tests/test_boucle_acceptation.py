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
from pathlib import Path

import pytest

from src.validation import aveugle, boucle_acceptation as boucle

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
        "| plan PLANS-TEST - 1 (zoom ×8) : aucun appareil vu | estimateur correct |")
    justif.write_text(rempli, encoding="utf-8")
    rapport = boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert rapport.verdict == boucle.VERDICT_PRET
    assert bool(rapport) is True
    assert justif.read_text(encoding="utf-8") == rempli    # jamais écrasé
    texte = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : PRÊT POUR DÉCISION FRANCIS**" in texte


def test_verdict_acceptation_lecture_seule(tmp_path):
    """verdict_acceptation : lit le verdict d'ACCEPTATION.md, None si absent —
    lecture seule (utilisé par le jeu de référence)."""
    f = _fabriquer(tmp_path)
    assert boucle.verdict_acceptation(f["dossier"]) is None
    boucle.executer("S-TEST", f["workdir"], f["dossier"])
    assert boucle.verdict_acceptation(f["dossier"]) == boucle.VERDICT_JUSTIF


def test_cli_boucle(tmp_path):
    """CLI `python -m src.validation.boucle_acceptation S-TEST --workdir W
    --dossier D` : code 1 (désaccords non tranchés), dernière ligne VERDICT ;
    entrée introuvable → code 2 avec diagnostic."""
    f = _fabriquer(tmp_path)
    p = subprocess.run(
        [sys.executable, "-m", "src.validation.boucle_acceptation", "S-TEST",
         "--workdir", str(f["workdir"]), "--dossier", str(f["dossier"])],
        cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 1, f"stdout={p.stdout}\nstderr={p.stderr}"
    lignes = [l for l in p.stdout.splitlines() if l.startswith("VERDICT : ")]
    assert lignes and lignes[-1] == f"VERDICT : {boucle.VERDICT_JUSTIF}"
    assert (f["dossier"] / "ACCEPTATION.md").is_file()

    p2 = subprocess.run(
        [sys.executable, "-m", "src.validation.boucle_acceptation", "S-TEST",
         "--workdir", str(tmp_path / "absent"), "--dossier", str(f["dossier"])],
        cwd=ROOT, capture_output=True, text=True)
    assert p2.returncode == 2 and "ERREUR" in p2.stderr


def test_erreurs_entree(tmp_path):
    """Dossier ou workdir inexistant → erreur d'entrée refusée (exception
    typée), jamais corrigée en silence."""
    f = _fabriquer(tmp_path)
    with pytest.raises(boucle.BoucleErreur):
        boucle.executer("S-TEST", f["workdir"], tmp_path / "dossiers" / "Absent")
    with pytest.raises(aveugle.AveugleErreur):
        boucle.executer("S-TEST", tmp_path / "absent", f["dossier"])