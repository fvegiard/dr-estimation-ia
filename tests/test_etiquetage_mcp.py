"""relever_automatique sur un plan d'un bureau d'ingénieurs inconnu de la bibliothèque : le LLM client étiquette les
signatures (etiqueter_signatures), la reprise livre le ZIP, la bibliothèque apprend → le dossier suivant sort seul."""
from __future__ import annotations

import asyncio
import base64
import csv

import pymupdf
import pytest

pytest.importorskip("mcp")
from mcp import Client  # noqa: E402

from serveur_mcp import serveur  # noqa: E402
from tests.test_serveur_mcp import _texte  # noqa: E402


def _plan_inconnu() -> bytes:
    """Plan vectoriel : 5 boîtiers « croix dans un carré » (bloc absent de la bibliothèque) + 4 losanges (non-appareils)."""
    doc = pymupdf.open()
    p = doc.new_page(width=1224, height=792)
    p.insert_text((60, 60), "PLAN ELECTRIQUE NIVEAU 1", fontsize=14)
    for i in range(5):
        x, y = 200 + 150 * i, 300
        p.draw_rect(pymupdf.Rect(x - 7, y - 7, x + 7, y + 7), color=(0, 0, 0), width=0.8)
        p.draw_line((x - 7, y - 7), (x + 7, y + 7), color=(0, 0, 0), width=0.8)
        p.draw_line((x - 7, y + 7), (x + 7, y - 7), color=(0, 0, 0), width=0.8)
    for i in range(4):
        x, y = 250 + 150 * i, 550
        p.draw_polyline([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y), (x, y - 9)], color=(0, 0, 0), width=0.5)
    return doc.tobytes()


def _sig_de(base, dossier: str, n: int) -> list[str]:
    idx = list(csv.DictReader(open(base / dossier / "travail" / "blocs-index.csv", encoding="utf-8")))
    return [r["sig_id"] for r in idx if int(r["n_plans"]) == n]


async def _parcours(tmp_path):
    async with Client(serveur.mcp) as c:
        b64 = base64.b64encode(_plan_inconnu()).decode()
        for d in ("NOUVEAU", "SUIVANT"):
            _texte(await c.call_tool("deposer_fichier", {"dossier": d, "nom_fichier": "plans.pdf", "contenu_base64": b64}))

        r = _texte(await c.call_tool("relever_automatique", {"dossier": "NOUVEAU", "verification_vision": False}))
        assert r["produit"] is False and r["a_etiqueter"]["planches"] and "etiqueter_signatures" in r["suite"]

        croix, losange = _sig_de(tmp_path, "NOUVEAU", 5), _sig_de(tmp_path, "NOUVEAU", 4)
        assert croix and losange
        e = _texte(await c.call_tool("etiqueter_signatures", {"dossier": "NOUVEAU", "etiquettes": [
            {"sig_id": croix[0], "label": "BOITE DE JONCTION", "famille": "commande", "forme": "carre",
             "materiel": "BOITE DE JONCTION 4x4"},
            {"sig_id": "S999", "label": "X"},
            {"sig_id": losange[0], "label": "IGNORER"}]}))
        assert e["ajoutees"] == 2 and e["refusees"][0]["sig_id"] == "S999"
        assert croix[0] in e["appris_bibliotheque"] and e["non_appris"] == []

        r = _texte(await c.call_tool("relever_automatique", {"dossier": "NOUVEAU", "reprendre": True,
                                                             "verification_vision": False}))
        assert r["produit"] is True and r["reperes"] == 5 and r["zip"].endswith("-LIVRABLES-PNG.zip")
        bom = list(csv.DictReader(open(tmp_path / "NOUVEAU" / "sortie" / "png" / "NOUVEAU-BOM.csv", encoding="utf-8")))
        assert {x["code"] for x in bom} == {"BJ"} and len(bom) == 5   # code du vocabulaire ; IGNORER jamais compté

        # même bureau d'ingénieurs : rien à étiqueter, la bibliothèque a appris
        r = _texte(await c.call_tool("relever_automatique", {"dossier": "SUIVANT", "verification_vision": False}))
        assert r["produit"] is True and r["reperes"] == 5 and r["a_etiqueter"]["inconnues"] == []


def test_etiquetage_llm_puis_bibliotheque(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    bib = tmp_path / "bibliotheque-blocs.csv"
    bib.write_bytes(serveur.BIBLIOTHEQUE.read_bytes())
    monkeypatch.setattr(serveur, "BIBLIOTHEQUE", bib)
    asyncio.run(_parcours(tmp_path))


def test_codes_uniques_par_materiel(tmp_path):
    (tmp_path / "blocs-index.csv").write_text("sig_id,signature,n_plans\nS001,a,3\nS002,b,3\nS003,c,3\n", encoding="utf-8")
    r = serveur._ajouter_etiquettes(tmp_path, [
        {"sig_id": "S001", "label": "BOITIER A", "materiel": "BOITIER A"},
        {"sig_id": "S002", "label": "BOITIER B", "materiel": "BOITIER B"},
        {"sig_id": "S003", "label": "BOITIER A BIS", "materiel": "BOITIER A"}], "llm-mcp", "")
    codes = {x["sig_id"]: x["code"] for x in r["regles"]}
    assert codes["S001"] == codes["S003"] != codes["S002"]   # même matériel = même code, sinon jamais partagé


def test_correction_garde_les_autres_plages_de_diametre(tmp_path):
    (tmp_path / "blocs-index.csv").write_text("sig_id,signature,n_plans\nS002,a,3\n", encoding="utf-8")
    with open(tmp_path / "blocs-familles.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=serveur.COLS_FAMILLES)
        w.writeheader()
        w.writerow({"sig_id": "S002", "label": "SORTIE DATA", "code": "DA", "materiel": "SORTIE DATA", "diam_min": "0",
                    "diam_max": "6.5", "origine": "auto"})
    serveur._ajouter_etiquettes(tmp_path, [{"sig_id": "S002", "label": "DP1", "materiel": "DP1", "diam_min": 12,
                                            "diam_max": 20}], "llm-mcp", "")
    rows = list(csv.DictReader(open(tmp_path / "blocs-familles.csv", encoding="utf-8")))
    assert [r["label"] for r in rows] == ["SORTIE DATA", "DP1"]
