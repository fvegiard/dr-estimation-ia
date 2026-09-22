"""Seuils 5 % / 10 %, postes majeurs, item manquant signalé — comparateur
déterministe `src.validation.ecart`."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from conftest import FIXTURES, ROOT, run_cli
from src.validation import ecart


def _ecrire_csv(path: Path, texte: str) -> Path:
    path.write_text(texte, encoding="utf-8")
    return path


def test_pass_fixture_cli(tmp_path):
    sortie = tmp_path / "ecart.md"
    run_cli("-m", "src.validation.ecart",
            "--reference", str(FIXTURES / "reference.csv"),
            "--ia", str(FIXTURES / "compteurs.csv"),
            "--sortie", str(sortie))
    contenu = sortie.read_text(encoding="utf-8")
    assert "**PASS**" in contenu
    assert "Verdict FINAL réservé à Francis" in contenu
    assert "## Items manquants" in contenu
    assert "Aucun : chaque item de la référence a une contrepartie IA." in contenu


def _comparer(reference_csv: str, ia_csv: str, tmp_path) -> ecart.Resultat:
    ref = _ecrire_csv(tmp_path / "ref.csv", reference_csv)
    ia = _ecrire_csv(tmp_path / "ia.csv", ia_csv)
    return ecart.comparer(ecart.lire_reference(ref), ecart.lire_ia(ia))


def test_ecart_total_au_dela_5_pour_cent(tmp_path):
    res = _comparer(
        "poste,description,quantite\nluminaires,Luminaire DS1,100\n",
        "libelle,quantite\nLuminaire DS1,110\n",
        tmp_path,
    )
    assert res.verdict == "FAIL"
    assert any("écart total" in c for c in res.causes)
    assert res.ecart_total_pct == pytest.approx(10.0)


def test_poste_majeur_au_dela_10_pour_cent_meme_si_total_ok(tmp_path):
    # Total : 110 -> 108 (-1,8 % ≤ 5 %) mais luminaires : 10 -> 7 (-30 %)
    res = _comparer(
        "poste,description,quantite\n"
        "luminaires,Luminaire DS1,10\n"
        "conduits,Conduit EMT 21 mm,100\n",
        "libelle,quantite\n"
        "Luminaire DS1,7\n"
        "Conduit EMT 21 mm,101\n",
        tmp_path,
    )
    assert res.verdict == "FAIL"
    assert abs(res.ecart_total_pct) <= 5.0
    assert any("luminaires" in c for c in res.causes)
    # un poste non majeur au-delà de 10 % ne fait PAS échouer à lui seul
    res2 = _comparer(
        "poste,description,quantite\n"
        "prises,Prise duplex 15A,10\n"
        "conduits,Conduit EMT 21 mm,100\n",
        "libelle,quantite\n"
        "Prise duplex 15A,7\n"
        "Conduit EMT 21 mm,101\n",
        tmp_path,
    )
    assert res2.verdict == "PASS"


def test_item_manquant_signale_et_fail(tmp_path):
    res = _comparer(
        "poste,description,quantite\n"
        "luminaires,Luminaire DS1,10\n"
        "prises,Prise duplex DDFT,4\n",
        "libelle,quantite\n"
        "Luminaire DS1,10\n",
        tmp_path,
    )
    assert res.verdict == "FAIL"
    assert len(res.manquants) == 1
    assert res.manquants[0].description == "Prise duplex DDFT"
    # la section « Items manquants » du livrable n'est jamais silencieuse
    sortie = tmp_path / "ecart.md"
    ecart.ecrire_ecart_md(res, Path("ref.csv"), Path("ia.csv"), sortie)
    contenu = sortie.read_text(encoding="utf-8")
    assert "Prise duplex DDFT" in contenu.split("## Items manquants")[1]


def test_item_en_trop_liste_sans_fail(tmp_path):
    res = _comparer(
        "poste,description,quantite\nluminaires,Luminaire DS1,10\n",
        "libelle,quantite\nLuminaire DS1,10\nPhotocellule,1\n",
        tmp_path,
    )
    assert len(res.en_trop) == 1
    # l'item en trop entre dans le total : +10 % ici -> FAIL par le total,
    # pas par la seule présence de l'item en trop
    assert res.verdict == "FAIL"
    assert any("écart total" in c for c in res.causes)


def test_appariement_normalise_accents_et_casse(tmp_path):
    res = _comparer(
        "poste,description,quantite\nprises,Prise sécheuse 30A,5\n",
        "libelle,quantite\nPRISE SECHEUSE 30A,5\n",
        tmp_path,
    )
    assert not res.manquants
    assert not res.en_trop
    assert res.verdict == "PASS"


def test_reference_xlsx(tmp_path):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append(["poste", "description", "quantité"])
    ws.append(["luminaires", "Luminaire DS1", 10])
    ws.append(["conduits", "Conduit EMT 21 mm", 60])
    ref_xlsx = tmp_path / "ref.xlsx"
    wb.save(ref_xlsx)
    ia = _ecrire_csv(tmp_path / "ia.csv", "libelle,quantite\nLuminaire DS1,10\nConduit EMT 21 mm,61\n")
    res = ecart.comparer(ecart.lire_reference(ref_xlsx), ecart.lire_ia(ia))
    assert res.verdict == "PASS"
    assert res.total_reference == 70


def test_ia_json_export_verifier(tmp_path):
    # format JSON produit par `src.releve verifier --export-counters`
    data = {
        "counters": [
            {"group_id": 1, "name": "Luminaire DS1",
             "elements": [{"sheet": "E100_Rev0", "x": 1, "y": 2}] * 10},
        ],
        "lines": [],
    }
    ia_json = _ecrire_csv(tmp_path / "ia.json", "")
    ia_json.write_text(__import__("json").dumps(data), encoding="utf-8")
    ref = _ecrire_csv(tmp_path / "ref.csv",
                      "poste,description,quantite\nluminaires,Luminaire DS1,10\n")
    res = ecart.comparer(ecart.lire_reference(ref), ecart.lire_ia(ia_json))
    assert res.verdict == "PASS"


def test_code_sortie_fail(tmp_path):
    ref = _ecrire_csv(tmp_path / "ref.csv",
                      "poste,description,quantite\nluminaires,Luminaire DS1,100\n")
    ia = _ecrire_csv(tmp_path / "ia.csv", "libelle,quantite\nLuminaire DS1,90\n")
    result = subprocess.run(
        [sys.executable, "-m", "src.validation.ecart",
         "--reference", str(ref), "--ia", str(ia), "--sortie", str(tmp_path / "ecart.md")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 1  # FAIL : verdict calculé, pas une erreur
    assert "FAIL" in result.stdout
