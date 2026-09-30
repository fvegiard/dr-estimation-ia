"""Serveur MCP Expert estimateur : chaîne complète via un vrai client MCP en mémoire (plan synthétique)."""
from __future__ import annotations

import asyncio
import base64
import json

import pymupdf
import pytest

pytest.importorskip("mcp")
from mcp import Client  # noqa: E402

from serveur_mcp import serveur  # noqa: E402


def _plan_pdf() -> bytes:
    doc = pymupdf.open()
    p = doc.new_page(width=1224, height=792)
    p.insert_text((60, 60), "PLAN ELECTRIQUE REZ-DE-CHAUSSEE", fontsize=14)
    for i in range(6):
        x = 200 + 120 * i
        p.draw_circle((x, 300), 6, color=(0, 0, 0))
        p.insert_text((x + 8, 296), "SF", fontsize=6)
    for i in range(3):
        p.draw_rect(pymupdf.Rect(300 + 150 * i, 500, 312 + 150 * i, 512), color=(0, 0, 0))
    return doc.tobytes()


def _texte(res) -> dict:
    assert not res.is_error, res
    return json.loads(res.content[0].text)


async def _chaine(tmp_path):
    async with Client(serveur.mcp) as c:
        outils = {t.name for t in (await c.list_tools()).tools}
        assert {"preparer_dossier", "zoomer", "verifier_releve", "produire_livrables", "comparer_estimateur"} <= outils
        methode = await c.read_resource("estimateur://methode")
        assert "extraire_occurrences" in methode.contents[0].text and "uv run" not in methode.contents[0].text

        assert _texte(await c.call_tool("deposer_fichier", {
            "dossier": "ESSAI", "nom_fichier": "plans.pdf",
            "contenu_base64": base64.b64encode(_plan_pdf()).decode()}))["octets"] > 0
        prep = _texte(await c.call_tool("preparer_dossier", {"dossier": "ESSAI"}))
        f = prep["feuilles"][0]["feuille"]

        img = await c.call_tool("voir_image", {"dossier": "ESSAI", "chemin": f"travail/apercus/{f}.png", "largeur_max": 400})
        assert img.content[0].type == "image"

        refus = await c.call_tool("ecrire_fichier", {"dossier": "ESSAI", "nom": "../evil.csv", "contenu": "x"})
        assert refus.is_error
        hors = await c.call_tool("lire_fichier", {"dossier": "ESSAI", "chemin": "../../README.md"})
        assert hors.is_error

        ecrits = {
            "feuilles-classement.csv": f"feuille,type,echelle,note\n{f},plan,,essai\n",
            "nomenclature.csv": "label,famille,forme,rgb,jeton_regex,description,source\n"
                                "DETECTEUR DE FUMEE,alarme,cercle,255;0;0,SF,Detecteur de fumee,legende\n"
                                "BOITE DE JONCTION,distribution,carre,0;0;255,,Boite de jonction,legende\n",
            "occurrences-visuel.csv": "feuille,label,x_pt,y_pt,source,note\n" + "".join(
                f"{f},BOITE DE JONCTION,{306 + 150 * i},506,visuel,carre\n" for i in range(3)),
            "reserves.md": f"# Reserves\n\n1. R-001 {f} : modele du detecteur non precise.\n",
        }
        for nom, contenu in ecrits.items():
            await c.call_tool("ecrire_fichier", {"dossier": "ESSAI", "nom": nom, "contenu": contenu})
        ext = _texte(await c.call_tool("extraire_occurrences", {"dossier": "ESSAI"}))
        assert ext["occurrences"] == 6

        ctl = _texte(await c.call_tool("verifier_releve", {"dossier": "ESSAI"}))
        assert ctl["pret"], ctl
        assert ctl["occurrences"] == 9 and ctl["reserves"] == 1

        liv = _texte(await c.call_tool("produire_livrables", {"dossier": "ESSAI"}))
        assert liv["produit"], liv
        assert liv["reperes"] == 9
        assert {"ESSAI-RELEVE.pdf", "ESSAI.qpl"} <= set(liv["fichiers"])
        assert liv["a_verifier"] == [], "l'encadré doit tenir dans l'espace libre sur ce plan synthétique"
        page = await c.call_tool("voir_image", {"dossier": "ESSAI", "chemin": "sortie/ESSAI-RELEVE.pdf#1", "largeur_max": 800})
        assert page.content[0].type == "image"
    sortie = tmp_path / "ESSAI" / "sortie"
    # -RELEVE.pdf doit être une copie du rendu déjà produit par render_vectoriel.py (même build()+render()),
    # pas un second rendu indépendant dans un répertoire séparé (sortie/format-exemple/) : même contenu.
    assert (sortie / "ESSAI-RELEVE.pdf").read_bytes() == (sortie / "ESSAI-Plans-annotes.pdf").read_bytes()
    assert not (sortie / "format-exemple").exists()
    return sortie / "ESSAI-RELEVE.pdf"


def test_chaine_complete(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    pdf = asyncio.run(_chaine(tmp_path))
    with pymupdf.open(pdf) as doc:
        t0 = doc[0].get_text()
        assert "RELEVE" in t0 and "MATERIEL" in t0
        assert "9 reperes / 2 familles / RES 9" in t0
        assert "I01-01" in t0 and "M01-01" in t0
        tout = "".join(p.get_text() for p in doc)
        assert "BORDEREAU MATERIEL" in tout and "MODELE NON PRECISE" in tout
        assert "R-001" in tout


def test_doublon_bloque(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    t = tmp_path / "D" / "travail"
    t.mkdir(parents=True)
    (t / "feuilles.csv").write_text("feuille,fichier,page,largeur_pt,hauteur_pt\nE101,a.pdf,1,100,100\n", encoding="utf-8")
    (t / "feuilles-classement.csv").write_text("feuille,type\nE101,plan\n", encoding="utf-8")
    (t / "nomenclature.csv").write_text("label,famille\nX,alarme\n", encoding="utf-8")
    (t / "occurrences-visuel.csv").write_text("feuille,label,x_pt,y_pt\nE101,X,10,10\nE101,X,11,12\nE101,Y,500,5\n",
                                              encoding="utf-8")
    (t / "reserves.md").write_text("", encoding="utf-8")
    ctl = serveur.controler(t)
    assert not ctl["pret"]
    texte = " ".join(ctl["erreurs"])
    assert "doublon" in texte and "Y" in texte and "hors de la page" in texte


def test_http_exige_cle(monkeypatch):
    from starlette.testclient import TestClient

    with pytest.raises(SystemExit):
        serveur.application_http("0.0.0.0", cle="court")
    app = serveur.application_http("127.0.0.1", cle="k" * 32)
    with TestClient(app, base_url="http://127.0.0.1:8765") as cl:
        assert cl.post("/mcp", json={}).status_code == 401
        r = cl.post("/mcp", headers={"Authorization": "Bearer " + "k" * 32, "Accept": "application/json, text/event-stream"},
                    json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                        "protocolVersion": "2025-06-18", "capabilities": {},
                        "clientInfo": {"name": "essai", "version": "1"}}})
        assert r.status_code == 200


def test_parite_claude_e103(tmp_path):
    """Le relevé E103 (S-1844) de la chaîne Claude rendu par le serveur MCP : 23 repères, plan + bordereau materiel."""
    import shutil
    from pathlib import Path

    from serveur_mcp.exemple import rendre
    from serveur_mcp.serveur import controler

    src = Path(__file__).resolve().parents[1] / "dossiers" / "S-1844-essai" / "E103"
    t = tmp_path / "travail"
    (t / "feuilles").mkdir(parents=True)
    shutil.copy(src / "E103-page6.pdf", t / "feuilles" / "E103.pdf")
    with pymupdf.open(src / "E103-page6.pdf") as d:
        w, h = d[0].rect.width, d[0].rect.height
    (t / "feuilles.csv").write_text(f"feuille,fichier,page,largeur_pt,hauteur_pt\nE103,E103-page6.pdf,1,{w},{h}\n",
                                    encoding="utf-8")
    (t / "feuilles-classement.csv").write_text("feuille,type,echelle,bordereau,note\nE103,plan,AUCUNE,materiel,cartouche=E103\n",
                                               encoding="utf-8")
    for f in ("nomenclature.csv", "occurrences-visuel.csv", "reserves.md"):
        shutil.copy(src / f, t / f)
    (t / "occurrences-texte.csv").write_text("feuille,label,x_pt,y_pt,source,note\n", encoding="utf-8")
    ctl = controler(t)
    assert ctl["pret"], ctl
    r = rendre(t, tmp_path, "S-1844-E103")
    assert r["reperes"] == 23
    with pymupdf.open(tmp_path / "S-1844-E103-RELEVE.pdf") as d:
        assert len(d) == 2
        assert "RELEVE E103 - MATERIEL" in d[0].get_text()
        texte = d[1].get_text()
        assert "BORDEREAU MATERIEL - E103" in texte and "M01-08" in texte and "R-012" in texte

