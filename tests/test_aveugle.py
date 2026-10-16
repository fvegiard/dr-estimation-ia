"""Contrôle d'aveugle `src.validation.aveugle` — preuve déterministe de
l'étape 1 du critère d'acceptation : le dossier de travail est aveugle
(workdir propre code 0) ou cite le matériel de l'estimateur (code 1).
Fixtures 100 % synthétiques via tmp_path, aucune donnée client."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from conftest import ROOT, env_sans_encodage
from src.validation import aveugle

NOM_RAPPORT = "controle-aveugle.json"


def _ecrire(workdir: Path, nom: str, contenu: str = "contenu synthetique de test\n") -> Path:
    """Crée un fichier (parents au besoin) et retourne son chemin."""
    p = workdir / nom
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenu, encoding="utf-8")
    return p


def _cli(workdir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "src.validation.aveugle", str(workdir)],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage(),
    )


def _rapport_json(workdir: Path) -> dict:
    return json.loads((workdir / NOM_RAPPORT).read_text(encoding="utf-8"))


def _creer_travail_ia_propre(workdir: Path) -> None:
    """Artefacts du relevé IA uniquement — l'état aveugle attendu."""
    _ecrire(workdir, "nomenclature.csv", "feuille,label,famille\nE100,Luminaire DS1,luminaire\n")
    _ecrire(workdir, "occurrences-texte.csv", "feuille,label,x_pt,y_pt\nE100,DS1,120.0,480.0\n")
    _ecrire(workdir, "occurrences-visuel.csv", "feuille,label,x_px,y_px\nE100,DS1,700,2100\n")
    _ecrire(workdir, "feuilles-classement.csv", "feuille,role\nE100,plan\n")
    _ecrire(workdir, "reserves.md", "# Reserves\n- famille indeterminee sur E100 (symbole sans legende)\n")
    _ecrire(workdir, "planexpert/S-TEST.qpl", '<?xml version="1.0"?><projet version="1"></projet>\n')
    (workdir / "rasters").mkdir(parents=True, exist_ok=True)
    (workdir / "rasters" / "E100.png").write_bytes(b"\x89PNG\x0d\x0a\x1a\x0a")


def test_travail_ia_propre_est_aveugle_code_0(tmp_path):
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    r = _cli(workdir)
    assert r.returncode == 0, r.stderr
    j = _rapport_json(workdir)
    scannes = {p.relative_to(workdir).as_posix() for p in workdir.rglob("*")
               if p.is_file() and p.name != NOM_RAPPORT}
    assert j["aveugle"] is True
    assert j["references_detectees"] == []
    assert j["fichiers_scannes"] == len(scannes)
    assert set(j) == {"date", "fichiers_scannes", "references_detectees", "aveugle"}
    assert j["date"] == date.today().isoformat()
    # appel direct : même verdict, même compte
    rapport = aveugle.controler(workdir)
    assert rapport.aveugle is True
    assert rapport.fichiers_scannes == j["fichiers_scannes"]


def test_qpl_dupuis_detecte_code_1(tmp_path):
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "planexpert/S-1294-Dupuis-PlanExpert.qpl", '<?xml version="1.0"?><projet></projet>\n')
    r = _cli(workdir)
    assert r.returncode == 1
    j = _rapport_json(workdir)
    assert j["aveugle"] is False
    assert len(j["references_detectees"]) == 1
    ref = j["references_detectees"][0]
    assert ref["fichier"] == "planexpert/S-1294-Dupuis-PlanExpert.qpl"
    assert ref["motif"] == "qpl-dupuis"


def test_nom_dupuis_sans_contenu(tmp_path):
    # la détection par le NOM ne dépend pas du contenu (dimensions de PNG)
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "dupuis-png-dimensions.txt", "E100.png 5694x4002\nE200.png 5694x4002\n")
    r = _cli(workdir)
    assert r.returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "dupuis-png-dimensions.txt", "motif": "nom-dupuis"}


def test_dossier_reference_bannis(tmp_path):
    # tout fichier sous reference/ est banni ; le .qpl y est vu des deux règles
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "reference/S-1294-Dupuis-PlanExpert.qpl", '<?xml version="1.0"?>\n')
    _ecrire(workdir, "reference/feuilles-ia.csv", "feuille_ia,feuille_humaine\nE100,DSI01\n")
    r = _cli(workdir)
    assert r.returncode == 1
    refs = {(x["fichier"], x["motif"]) for x in _rapport_json(workdir)["references_detectees"]}
    assert ("reference/S-1294-Dupuis-PlanExpert.qpl", "qpl-dupuis") in refs
    assert ("reference/feuilles-ia.csv", "dossier-reference") in refs


def test_dossier_estimateur_bannis(tmp_path):
    # tout fichier sous estimateur/ est du matériau de l'estimateur (prepare.py
    # n'y écrit jamais rien d'autre) : y compris un PNG binaire au nom neutre
    # (p01.png) qui échapperait au scan de contenu et aux règles de nom.
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    (workdir / "estimateur" / "legendes").mkdir(parents=True, exist_ok=True)
    (workdir / "estimateur" / "p01.png").write_bytes(b"\x89PNG\x0d\x0a\x1a\x0a")
    (workdir / "estimateur" / "legendes" / "p01-legende.png").write_bytes(b"\x89PNG\x0d\x0a\x1a\x0a")
    _ecrire(workdir, "estimateur/pages.csv", "page,largeur_pt,hauteur_pt,fichier\n1,2383,1683,\n")
    r = _cli(workdir)
    assert r.returncode == 1
    refs = {(x["fichier"], x["motif"]) for x in _rapport_json(workdir)["references_detectees"]}
    assert ("estimateur/p01.png", "dossier-estimateur") in refs
    assert ("estimateur/legendes/p01-legende.png", "dossier-estimateur") in refs
    assert ("estimateur/pages.csv", "dossier-estimateur") in refs


def test_signature_dans_contenu(tmp_path):
    # noms neutres, contenu citant la référence ou l'estimateur
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "resultats.md", "# Resultats\n- Humain : reference/S-1294-Dupuis-PlanExpert.qpl\n")
    _ecrire(workdir, "compte.csv", "libelle,quantite\nPrise duplex,12\n")
    r = _cli(workdir)
    assert r.returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "resultats.md", "motif": "contenu-dupuis"}


def test_signature_estimateur_dans_contenu(tmp_path):
    workdir = tmp_path / "travail"
    _ecrire(workdir, "nomenclature.csv", "label\nLuminaire\n")
    _ecrire(workdir, "ecart.md", "Comparaison effectuée avec le relevé de l'estimateur (122 marques)\n")
    assert _cli(workdir).returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "ecart.md", "motif": "contenu-estimateur"}


def test_releve_humain_canonique(tmp_path):
    # nom exact du relevé humain — sans aucun marqueur dupuis/estimateur/humain
    workdir = tmp_path / "travail"
    _ecrire(workdir, "releve.xlsx", "feuille,description,quantite\nE100,Luminaire,10\n")
    r = _cli(workdir)
    assert r.returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "releve.xlsx", "motif": "releve-humain"}


def test_rapport_releve_ia_n_est_pas_banni(tmp_path):
    # le relevé IA a ses propres fichiers « releve » : aucun faux positif
    workdir = tmp_path / "travail"
    _ecrire(workdir, "rapport-releve.md", "# Methode et constats de l'agent\n")
    assert _cli(workdir).returncode == 0


def test_mots_insensibles_accents_et_casse(tmp_path):
    workdir = tmp_path / "travail"
    _ecrire(workdir, "RÉFÉRENCE-quantites.CSV", "description,quantite\nConduit EMT,40\n")
    r = _cli(workdir)
    assert r.returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "RÉFÉRENCE-quantites.CSV", "motif": "nom-reference"}


def test_meta_pipeline_exclues_du_contenu(tmp_path):
    # MANIFESTE.md cite « Estimateur (si fourni) » en gabarit fixe (prepare.py) :
    # il ne prouve pas un accès au relevé de l'estimateur ; inventaire.json et
    # estimateur/pages.csv restent scannés (présence réelle détectée là).
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "MANIFESTE.md",
            "# MANIFESTE du dossier préparé\n\nEstimateur (si fourni) : `estimateur/pNN.png` et "
            "`estimateur/legendes/pNN-legende.png`.\n")
    _ecrire(workdir, "agent-resultat.json", '{"result": "releve termine", "usage": {}}\n')
    _ecrire(workdir, "agent-journal.log", "$ python -m ...\nok\n")
    assert _cli(workdir).returncode == 0


def test_inventaire_revele_export_estimateur_depose(tmp_path):
    # un export de l'estimateur dans l'INBOX (règle « plans + addendas
    # seulement » enfreinte) se voit dans inventaire.json et estimateur/pages.csv
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "inventaire.json",
            '{"inbox": "/INBOX/S-TEST", "fichiers": [{"fichier": "Releve-Dupuis.pdf", '
            '"octets": 100, "sha256": "abc", "classement": "estimateur", "pages": 2}], "notes": []}\n')
    r = _cli(workdir)
    assert r.returncode == 1
    ref = _rapport_json(workdir)["references_detectees"][0]
    assert ref == {"fichier": "inventaire.json", "motif": "contenu-dupuis"}


def test_texte_au_dela_de_5_mo_pas_scanne(tmp_path):
    # au-delà de la limite de taille, le balayage du contenu est sauté (spec)
    workdir = tmp_path / "travail"
    remplissage = "x" * 4096 + "\ndupuis\n"        # la signature est bien dans le gros fichier
    blocs = aveugle.TAILLE_MAX_TEXTE_OCTETS // len(remplissage) + 1
    _ecrire(workdir, "gros-dump.log", remplissage * blocs)
    assert (workdir / "gros-dump.log").stat().st_size > aveugle.TAILLE_MAX_TEXTE_OCTETS
    assert _cli(workdir).returncode == 0


def test_binaire_ignore_meme_avec_suffixe_texte(tmp_path):
    # un suffixe texte portant des octets illisibles (binaire déguisé : PK,
    # NULs, 0xFF) n'est pas balayé — jamais de signature inventée dedans
    workdir = tmp_path / "travail"
    p = workdir / "export-dump.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"PK\x00\x03\xff\xe9dupuis\x00" + b"\x00" * 24)
    assert _cli(workdir).returncode == 0


def test_relance_stable_le_rapport_ne_se_detecte_pas_lui_meme(tmp_path):
    # deux contrôles successifs sur le même dossier : le compte ne double pas
    # (le rapport cite des noms « dupuis » que la relance ne doit pas balayer)
    workdir = tmp_path / "travail"
    _creer_travail_ia_propre(workdir)
    _ecrire(workdir, "reference/S-1294-Dupuis-PlanExpert.qpl", '<?xml version="1.0"?>\n')
    rapport1 = aveugle.controler(workdir)
    rapport2 = aveugle.controler(workdir)
    assert rapport1.fichiers_scannes == rapport2.fichiers_scannes
    assert [r.fichier for r in rapport2.references_detectees] == ["reference/S-1294-Dupuis-PlanExpert.qpl"]


def test_erreur_dossier_absent_code_2(tmp_path):
    r = _cli(tmp_path / "introuvable")
    assert r.returncode == 2
    assert "ERREUR" in r.stderr
    with pytest.raises(aveugle.AveugleErreur):
        aveugle.controler(tmp_path / "introuvable")


def test_erreur_chemin_fichier_code_2(tmp_path):
    fichier = tmp_path / "pas-un-dossier.txt"
    fichier.write_text("x", encoding="utf-8")
    assert _cli(fichier).returncode == 2


def test_motif_chemin_regles_en_direct(tmp_path):
    # le verdict « aveugle » est un booléen calculé, pas une chaîne saisie
    rapport = aveugle.RapportAveugle(date=date.today().isoformat(), fichiers_scannes=3)
    assert rapport.aveugle is True
    assert aveugle.motif_par_chemin(Path("reference/x.qpl")) == "dossier-reference"
    assert aveugle.motif_par_chemin(Path("estimateur/p01.png")) == "dossier-estimateur"
    assert aveugle.motif_par_chemin(Path("S-1294-Dupuis-PlanExpert.qpl")) == "qpl-dupuis"
    assert aveugle.motif_par_chemin(Path("note-humain.txt")) == "nom-humain"
    assert aveugle.motif_par_chemin(Path("nomenclature.csv")) is None