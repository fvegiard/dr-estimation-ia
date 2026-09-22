"""Aller-retour qpl → verifier → qpl, unicité des GroupID, injection de
lignes (bogue corrigé) et chaîne CLI inventaire → qpl → verifier."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import FIXTURES, run_cli
from src.releve import qpl_build, verifier
from src.cablage import compute_arteres, inject_lines


@pytest.fixture()
def qpl_genere(tmp_path) -> Path:
    plans = qpl_build.load_plans(FIXTURES / "plans.json")
    counters, lines = qpl_build.load_counters(FIXTURES / "counters.json")
    xml_text = qpl_build.build_qpl_text(plans, counters, lines)
    sortie = tmp_path / "fixture.qpl"
    qpl_build.write_qpl(sortie, xml_text)
    return sortie


def test_build_et_decompte(qpl_genere):
    root = verifier._parse(qpl_genere)
    counts = verifier.compute_counts(root)
    assert counts["n_plans"] == 2
    # chaque compteur n'a des marques que sur une seule feuille : 3 nœuds
    assert counts["n_counters"] == 3
    assert counts["n_counter_elements"] == 6
    assert counts["n_lines"] == 1
    assert counts["n_line_segments"] == 2
    assert counts["group_ids_partages_compteur_et_ligne"] == []
    assert counts["n_distinct_group_ids_total"] == 4


def test_aller_retour_qpl_verifier_qpl(qpl_genere, tmp_path):
    root = verifier._parse(qpl_genere)
    plans_model, counters_model = verifier.export_model(root)
    plans_json = tmp_path / "plans-export.json"
    counters_json = tmp_path / "counters-export.json"
    plans_json.write_text(json.dumps(plans_model, ensure_ascii=False), encoding="utf-8")
    counters_json.write_text(json.dumps(counters_model, ensure_ascii=False), encoding="utf-8")

    plans2 = qpl_build.load_plans(plans_json)
    counters2, lines2 = qpl_build.load_counters(counters_json)
    xml2 = qpl_build.build_qpl_text(plans2, counters2, lines2)
    regenere = tmp_path / "regenere.qpl"
    qpl_build.write_qpl(regenere, xml2)

    counts_avant = verifier.compute_counts(verifier._parse(qpl_genere))
    counts_apres = verifier.compute_counts(verifier._parse(regenere))
    assert counts_apres == counts_avant

    # GroupID uniques, compteurs et lignes confondus (même espace §2.6)
    gids = [int(n.get("GroupID")) for n in verifier._parse(regenere).iter() if n.get("GroupID")]
    assert len(gids) == len(set(gids))


def test_groupid_duplique_refuse(tmp_path):
    data = json.loads((FIXTURES / "counters.json").read_text(encoding="utf-8"))
    data["lines"][0]["group_id"] = 1  # collision avec le compteur GroupID 1
    chemin = tmp_path / "counters-dup.json"
    chemin.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(qpl_build.QplBuildError, match="dupliqué"):
        qpl_build.load_counters(chemin)


def test_feuille_inconnue_refusee(tmp_path):
    data = json.loads((FIXTURES / "counters.json").read_text(encoding="utf-8"))
    data["counters"][0]["elements"][0]["sheet"] = "E999_Rev0"
    chemin = tmp_path / "counters-feuille.json"
    chemin.write_text(json.dumps(data), encoding="utf-8")
    plans = qpl_build.load_plans(FIXTURES / "plans.json")
    counters, lines = qpl_build.load_counters(chemin)
    with pytest.raises(qpl_build.QplBuildError, match="absente"):
        qpl_build.build_qpl_text(plans, counters, lines)


def test_compute_et_inject_lines(qpl_genere, tmp_path):
    """Chaîne câblage : métré synthétique → injection → GroupID uniques
    (l'assertion corrigée de inject_lines doit tenir sur le résultat)."""
    donnees = json.loads((FIXTURES / "arteres-config.json").read_text(encoding="utf-8"))
    rows, qpl_lines = compute_arteres.calculer(donnees)
    # F04 est une réserve : longueur nulle et statut explicite, jamais inventé
    reserve = next(r for r in rows if r["id"] == "F04")
    assert reserve["L_total_m"] == 0
    assert reserve["statut"].startswith("RESERVE")
    # F01 même niveau : Manhattan (700-200)+(500-200) pt à 10 mm/pt = 8,0 m
    f01 = next(r for r in rows if r["id"] == "F01")
    assert f01["L_h_m"] == 8.0

    summary = tmp_path / "arteres-summary.json"
    summary.write_text(
        json.dumps({"params": donnees["params"], "frames": donnees["frames"],
                    "levels": donnees["levels"], "equipment": donnees["equipment"],
                    "riser": donnees["riser"], "lines": qpl_lines, "rows": rows},
                   ensure_ascii=False),
        encoding="utf-8",
    )
    sortie = tmp_path / "fixture-v2.qpl"
    audit = inject_lines.injecter(
        qpl_genere, summary, sortie,
        mm_par_px=10.0 / 2.0, feuilles_precision=["E100"],
    )
    assert audit["lines_before"] == 1
    # F01 (2 segments, même feuille) + F02 (2 tronçons via puits) = 3 lignes
    assert audit["lines_after"] == 1 + 3
    # GroupID uniques après injection — c'est exactement ce que l'assertion
    # corrigée vérifie (l'ancienne `... or True` passait même avec doublons)
    gids = [int(n.get("GroupID")) for n in verifier._parse(sortie).iter() if n.get("GroupID")]
    assert len(gids) == len(set(gids))
    # Précision d'affichage passée à 2 sur la feuille calibrée demandée
    texte = sortie.read_text(encoding="utf-8-sig")
    assert '<Scale Value="100" Type="0" Precision="2"' in texte


def test_chaine_cli_inventaire_qpl_verifier(pdf_synthetique, dossier_inbox, tmp_path):
    # 1. inventaire : dossier de PDF -> JSON
    inv_json = tmp_path / "inventaire.json"
    run_cli("-m", "src.releve", "inventaire", str(dossier_inbox), "--out", str(inv_json))
    inv = json.loads(inv_json.read_text(encoding="utf-8"))
    assert len(inv) == 1
    assert inv[0]["n_pages"] == 2
    assert inv[0]["discipline"] == "Électricité"
    assert "E100" in inv[0]["pages"][0]["text"]
    assert "E200" in inv[0]["pages"][1]["text"]

    # 2. qpl : JSON synthétiques -> .qpl
    qpl_path = tmp_path / "chaine.qpl"
    run_cli("-m", "src.releve", "qpl", str(FIXTURES / "plans.json"),
            str(FIXTURES / "counters.json"), str(qpl_path))
    assert qpl_path.exists()
    # le .qpl est en UTF-8 avec BOM, prologue sans déclaration d'encodage
    brut = qpl_path.read_bytes()
    assert brut.startswith(b"\xef\xbb\xbf<?xml version=\"1.0\"?>")

    # 3. verifier : .qpl -> décompte + exports pour l'aller-retour
    counts_json = tmp_path / "decompte.json"
    exp_plans = tmp_path / "exp-plans.json"
    exp_counters = tmp_path / "exp-counters.json"
    run_cli("-m", "src.releve", "verifier", str(qpl_path), "--json", str(counts_json),
            "--export-plans", str(exp_plans), "--export-counters", str(exp_counters))
    counts = json.loads(counts_json.read_text(encoding="utf-8"))
    assert counts["n_plans"] == 2
    assert counts["n_counter_elements"] == 6
    assert counts["group_ids_partages_compteur_et_ligne"] == []
    assert len(counts["sha256"]) == 64

    # 4. qpl (aller-retour) : les exports régénèrent un .qpl équivalent
    qpl_path2 = tmp_path / "chaine-2.qpl"
    run_cli("-m", "src.releve", "qpl", str(exp_plans), str(exp_counters), str(qpl_path2))
    counts2 = verifier.compute_counts(verifier._parse(qpl_path2))
    assert counts2["n_counter_elements"] == counts["n_counter_elements"]
    assert counts2["n_lines"] == counts["n_lines"]
