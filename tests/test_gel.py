"""Gel sha256 des artefacts du relevé IA avant toute comparaison —
module `src.validation.gel` (étape 2 du critère d'acceptation).
Fixtures synthétiques tmp_path : aucune donnée client."""
from __future__ import annotations

import json
import pytest
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from conftest import ROOT, env_sans_encodage
from src.validation.gel import GelError, geler, verifier_gel


def _workdir(tmp_path: Path, *, complet: bool = True) -> Path:
    """Workdir synthétique : artefacts nommés + un `.qpl` produit."""
    w = tmp_path / "travail"
    w.mkdir()
    (w / "nomenclature.csv").write_text(
        "label,famille,forme,description\nDF,luminaires,cercle,Luminaire DS1\n",
        encoding="utf-8",
    )
    (w / "occurrences-texte.csv").write_text(
        "feuille,label,x_pt,y_pt,source,note\nE101,DF,100,200,texte,\n",
        encoding="utf-8",
    )
    if complet:
        (w / "occurrences-visuel.csv").write_text(
            "feuille,label,x_pt,y_pt,source,note\nE102,DF,300,400,visuel,\n",
            encoding="utf-8",
        )
        (w / "feuilles-classement.csv").write_text(
            "feuille,classement\nE101,plan\nE102,plan\n",
            encoding="utf-8",
        )
        (w / "reserves.md").write_text("- R-001 · E102 · symbole incertain *\n", encoding="utf-8")
    (w / "S-TEST.qpl").write_text("<projet/>", encoding="utf-8")
    return w


def test_gel_puis_verification_immediate(tmp_path):
    w = _workdir(tmp_path, complet=False)
    chemin = geler(w, soumission="S-TEST")
    assert chemin == w / "gel.json"
    assert chemin.is_file()
    # gel.json lui-même n'est jamais un artefact gelé
    assert "gel.json" not in [a["fichier"] for a in json.loads(chemin.read_text(encoding="utf-8"))["artefacts"]]
    rapport = verifier_gel(w)
    assert bool(rapport) is True
    assert rapport.ok is True
    assert rapport.modifies == []
    assert rapport.manquants == []
    assert rapport.ajoutes_apres_gel == []


def test_gel_json_structure(tmp_path):
    w = _workdir(tmp_path)
    chemin = geler(w)
    gel = json.loads(chemin.read_text(encoding="utf-8"))
    datetime.fromisoformat(gel["date"])                                  # ISO
    assert gel["soumission"] == tmp_path.name                            # parent du « travail »
    fichiers = {a["fichier"]: a for a in gel["artefacts"]}
    assert set(fichiers) == {
        "nomenclature.csv", "occurrences-texte.csv", "occurrences-visuel.csv",
        "feuilles-classement.csv", "reserves.md", "S-TEST.qpl",
    }
    for a in fichiers.values():
        assert set(a) == {"fichier", "sha256", "octets"}
        assert len(a["sha256"]) == 64
        assert a["octets"] == (w / a["fichier"]).stat().st_size


def test_soumission_deduite_du_parent_du_travail(tmp_path):
    outbox = tmp_path / "OUTBOX" / "S-123"
    (outbox / "travail").mkdir(parents=True)
    (outbox / "travail" / "nomenclature.csv").write_text("label,famille\nDF,luminaires\n", encoding="utf-8")
    w = outbox / "travail"
    gel = json.loads(geler(w).read_text(encoding="utf-8"))
    assert gel["soumission"] == "S-123"


def test_qpl_produit_geler_meme_dans_un_sous_dossier(tmp_path):
    w = _workdir(tmp_path)
    (w / "planexpert").mkdir()
    (w / "planexpert" / "S-TEST.qpl").write_text("<projet/>", encoding="utf-8")
    gel = json.loads(geler(w).read_text(encoding="utf-8"))
    rels = {a["fichier"] for a in gel["artefacts"]}
    assert "planexpert/S-TEST.qpl" in rels
    assert verifier_gel(w).ok is True


def test_csv_modifie_apres_gel_violation_listee(tmp_path):
    w = _workdir(tmp_path)
    geler(w)
    (w / "occurrences-texte.csv").write_text(
        "feuille,label,x_pt,y_pt,source,note\nE101,DF,999,999,texte,PIRATE\n",
        encoding="utf-8",
    )
    rapport = verifier_gel(w)
    assert rapport.ok is False
    assert not rapport
    assert rapport.modifies == ["occurrences-texte.csv"]
    assert rapport.manquants == []


def test_cet_artefact_supprime_apres_gel_violation_listee(tmp_path):
    w = _workdir(tmp_path)
    geler(w)
    (w / "reserves.md").unlink()
    rapport = verifier_gel(w)
    assert rapport.ok is False
    assert rapport.manquants == ["reserves.md"]
    assert rapport.modifies == []


def test_qpl_modifie_apres_gel_violation_listee(tmp_path):
    w = _workdir(tmp_path)
    geler(w)
    (w / "S-TEST.qpl").write_text("<projet modifie/>", encoding="utf-8")
    rapport = verifier_gel(w)
    assert rapport.ok is False
    assert rapport.modifies == ["S-TEST.qpl"]


def test_fichier_hors_perimetre_liste_pas_ajoute(tmp_path):
    # Produits de comparaison (ex. ecarts-classes.csv) : hors du domaine du gel
    # (le gel couvre les artefacts du relevé IA), ni gelés ni listés.
    w = _workdir(tmp_path)
    geler(w)
    (w / "ecarts-classes.csv").write_text(
        "classe,feuille_humaine,feuille_ia,libelle_humain,libelle_ia,"
        "position_humaine,position_ia,detail\n",
        encoding="utf-8",
    )
    rapport = verifier_gel(w)
    assert rapport.ok is True
    assert rapport.ajoutes_apres_gel == []


def test_qpl_ajoute_apres_gel_liste(tmp_path):
    w = _workdir(tmp_path)
    geler(w)
    (w / "S-TEST-v2.qpl").write_text("<projet tardif/>", encoding="utf-8")
    rapport = verifier_gel(w)
    assert rapport.ok is True
    assert rapport.ajoutes_apres_gel == ["S-TEST-v2.qpl"]


def test_workdir_vide_gel_error(tmp_path):
    w = tmp_path / "vide"
    w.mkdir()
    with pytest.raises(GelError):
        geler(w)


def test_workdir_inexistant_gel_error(tmp_path):
    with pytest.raises(GelError):
        geler(tmp_path / "inexistant")


def test_verifier_sans_gel_gel_error(tmp_path):
    w = _workdir(tmp_path, complet=False)
    with pytest.raises(GelError, match="aucun gel"):
        verifier_gel(w)


def test_cli_gele_et_verifie(tmp_path):
    w = _workdir(tmp_path)
    r_gel = subprocess.run(
        [sys.executable, "-m", "src.validation.gel", str(w), "--soumission", "S-CLI"],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage(),
    )
    assert r_gel.returncode == 0, r_gel.stderr
    assert json.loads((w / "gel.json").read_text(encoding="utf-8"))["soumission"] == "S-CLI"
    r_ok = subprocess.run(
        [sys.executable, "-m", "src.validation.gel", str(w), "--verifier"],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage(),
    )
    assert r_ok.returncode == 0, r_ok.stderr
    (w / "nomenclature.csv").write_text("label,famille\nX,viole\n", encoding="utf-8")
    r_viole = subprocess.run(
        [sys.executable, "-m", "src.validation.gel", str(w), "--verifier"],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage(),
    )
    assert r_viole.returncode == 1
    assert "GEL VIOLÉ" in r_viole.stderr
    assert "nomenclature.csv" in r_viole.stderr


def test_cli_sans_artefact_code_2(tmp_path):
    w = tmp_path / "vide"
    w.mkdir()
    r = subprocess.run(
        [sys.executable, "-m", "src.validation.gel", str(w)],
        cwd=ROOT, capture_output=True, encoding="utf-8", env=env_sans_encodage(),
    )
    assert r.returncode == 2
    assert "ERREUR" in r.stderr