"""Multiplicateurs d'unités types (cause S-1695 : chambres types non multipliées) + images JPEG du serveur MCP."""
from __future__ import annotations

import asyncio
import base64
import csv
import json

import pytest

pytest.importorskip("mcp")
from mcp import Client  # noqa: E402

from serveur_mcp import serveur  # noqa: E402
from tests.test_serveur_mcp import _plan_pdf, _texte  # noqa: E402


def test_facteur_de_zone_la_plus_petite_puis_feuille():
    regles = [
        {"feuille": "F1", "facteur": 4.0, "zone": None},
        {"feuille": "F1", "facteur": 6.0, "zone": (0, 0, 500, 500)},
        {"feuille": "F1", "facteur": 2.0, "zone": (100, 100, 200, 200)},
    ]
    assert serveur.facteur_de(regles, "F1", 150, 150) == 2.0   # plus petite zone
    assert serveur.facteur_de(regles, "F1", 300, 300) == 6.0   # zone englobante
    assert serveur.facteur_de(regles, "F1", 900, 900) == 4.0   # hors zones -> toute la feuille
    assert serveur.facteur_de(regles, "F2", 150, 150) == 1.0   # autre feuille -> 1


@pytest.mark.parametrize(("note", "bloquant"), [
    ("cartouche=E101 · APPAREIL TYPE D3-N", False),
    ("feuille=E101 · APPAREIL TYPE D3-N", False),
    ("LOGEMENT TYPE A (RDC ET 2E ETAGE)", True),
])
def test_controle_multiplicateurs_titre_automatique_ou_note_confirmee(tmp_path, note, bloquant):
    classement = [{"feuille": "E101", "type": "plan", "note": note}]
    erreurs, alertes = serveur.controle_multiplicateurs(tmp_path, classement)
    assert len(erreurs) == int(bloquant)
    assert len(alertes) == int(not bloquant)
    assert "sans multiplicateur" in (erreurs or alertes)[0]
    (tmp_path / "multiplicateurs.csv").write_text(
        "feuille,facteur,source\nE101,1,Une unité confirmée sur le plan\n", encoding="utf-8")
    assert serveur.controle_multiplicateurs(tmp_path, classement) == ([], [])


async def _chaine(tmp_path):
    async with Client(serveur.mcp) as c:
        assert "quantites" in {t.name for t in (await c.list_tools()).tools}
        _texte(await c.call_tool("deposer_fichier", {
            "dossier": "TYPES", "nom_fichier": "plans.pdf",
            "contenu_base64": base64.b64encode(_plan_pdf()).decode()}))
        f = _texte(await c.call_tool("preparer_dossier", {"dossier": "TYPES"}))["feuilles"][0]["feuille"]

        img = await c.call_tool("voir_image", {"dossier": "TYPES", "chemin": f"travail/apercus/{f}.png", "largeur_max": 400})
        assert img.content[0].type == "image" and img.content[0].mime_type == "image/jpeg"

        ecrits = {
            "feuilles-classement.csv": f"feuille,type,echelle,note\n{f},plan,,LOGEMENT TYPE A (RDC ET 2E ETAGE)\n",
            "nomenclature.csv": "label,famille,forme,rgb,jeton_regex,description,source\n"
                                "DETECTEUR DE FUMEE,alarme,cercle,255;0;0,SF,Detecteur de fumee,legende\n"
                                "BOITE DE JONCTION,distribution,carre,0;0;255,,Boite de jonction,legende\n",
            "occurrences-visuel.csv": "feuille,label,x_pt,y_pt,source,note\n" + "".join(
                f"{f},BOITE DE JONCTION,{306 + 150 * i},506,visuel,carre\n" for i in range(3)),
            "reserves.md": f"# Reserves\n\n1. R-001 {f} : modele du detecteur non precise.\n",
        }
        for nom, contenu in ecrits.items():
            await c.call_tool("ecrire_fichier", {"dossier": "TYPES", "nom": nom, "contenu": contenu})
        _texte(await c.call_tool("extraire_occurrences", {"dossier": "TYPES"}))

        # 1. Feuille d'unités types sans multiplicateur : bloquant.
        ctl = _texte(await c.call_tool("verifier_releve", {"dossier": "TYPES"}))
        assert not ctl["pret"]
        assert any("multiplicateur" in e for e in ctl["erreurs"]), ctl["erreurs"]

        # 2. Multiplicateur sans source : bloquant.
        await c.call_tool("ecrire_fichier", {"dossier": "TYPES", "nom": "multiplicateurs.csv",
                                             "contenu": f"feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source\n{f},6,,,,,\n"})
        ctl = _texte(await c.call_tool("verifier_releve", {"dossier": "TYPES"}))
        assert any("sans source" in e for e in ctl["erreurs"]), ctl["erreurs"]

        # 3. Feuille x6 + zone des boîtes x2 : détecteurs 6 x 6 = 36, boîtes 3 x 2 = 6.
        await c.call_tool("ecrire_fichier", {"dossier": "TYPES", "nom": "multiplicateurs.csv", "contenu":
            "feuille,facteur,x0_pt,y0_pt,x1_pt,y1_pt,source\n"
            f"{f},6,,,,,6 logements type A (RDC 3 + 2e 3) - cartouche\n"
            f"{f},2,280,480,640,530,2 salles identiques - note 3\n"})
        ctl = _texte(await c.call_tool("verifier_releve", {"dossier": "TYPES"}))
        assert ctl["pret"], ctl
        q = _texte(await c.call_tool("quantites", {"dossier": "TYPES"}))
        par = {l["label"]: l for l in q["lignes"]}
        assert par["DETECTEUR DE FUMEE"]["represente"] == 6 and par["DETECTEUR DE FUMEE"]["total"] == 36
        assert par["BOITE DE JONCTION"]["represente"] == 3 and par["BOITE DE JONCTION"]["total"] == 6
        assert q["represente"] == 9 and q["total"] == 42
        sortie = serveur.dossier_de("TYPES") / "sortie" / "quantites.csv"
        rangs = {r["label"]: r for r in csv.DictReader(sortie.open(encoding="utf-8"))}
        assert rangs["DETECTEUR DE FUMEE"]["total"] == "36"


def test_multiplicateurs_bout_en_bout(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    asyncio.run(_chaine(tmp_path))
