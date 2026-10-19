"""Parcours d'un collègue depuis n'importe quel Claude : connecteur avec la clé dans l'URL, PDF par lien Google Drive,
livrables par lien signé (jamais la clé du serveur)."""
from __future__ import annotations

import pytest

pytest.importorskip("mcp")
from serveur_mcp import serveur  # noqa: E402

CLE = "k" * 32
INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "essai", "version": "1"}}}
ACCEPT = {"Accept": "application/json, text/event-stream"}


def test_cle_dans_url_et_livrables_signes(tmp_path, monkeypatch):
    from starlette.testclient import TestClient

    monkeypatch.setenv("ESTIMATEUR_BASE", str(tmp_path))
    monkeypatch.setenv("ESTIMATEUR_MCP_CLE", CLE)
    monkeypatch.setenv("ESTIMATEUR_URL_PUBLIQUE", "https://estim.exemple.ca/")
    (tmp_path / "S-1" / "sortie").mkdir(parents=True)
    (tmp_path / "S-1" / "sortie" / "S-1-LIVRABLES-PNG.zip").write_bytes(b"PK zip")
    liens = serveur._liens("S-1", {"zip": "sortie/S-1-LIVRABLES-PNG.zip"})
    assert liens["lien_zip"].startswith("https://estim.exemple.ca/livrables/S-1/S-1-LIVRABLES-PNG.zip?jeton=")
    assert CLE not in liens["lien_zip"]
    app = serveur.application_http("127.0.0.1", cle=CLE)
    with TestClient(app, base_url="http://127.0.0.1:8765") as cl:
        assert cl.post("/mcp?cle=faux", json=INIT, headers=ACCEPT).status_code == 401
        assert cl.post(f"/mcp?cle={CLE}", json=INIT, headers=ACCEPT).status_code == 200
        chemin = liens["lien_zip"].removeprefix("https://estim.exemple.ca")
        r = cl.get(chemin)
        assert r.status_code == 200 and r.content == b"PK zip"
        assert cl.get(chemin[:-4] + "0000").status_code == 403
        rel = "S-1/../../secret"
        assert cl.get(f"/livrables/S-1/%2E%2E/%2E%2E/secret?jeton={serveur._jeton(rel)}").status_code == 404


class _Rep:
    def __init__(self, contenu: bytes, entetes: dict | None = None):
        self.content, self.headers = contenu, entetes or {}

    def raise_for_status(self):
        pass


def test_lien_drive_fichier_et_dossier(tmp_path, monkeypatch):
    import requests

    from src.apprentissage import gdrive

    vus = []

    def get(self, url, **kw):
        vus.append(url)
        return _Rep(b"%PDF-1.7 plan", {"content-disposition": 'attachment; filename="E-101.pdf"'})

    monkeypatch.setattr(requests.Session, "get", get)
    assert serveur._telecharger_source("https://drive.google.com/file/d/1CpgOD3xxkjv3ge13-92eTb2xjFmggjBA/view?usp=sharing",
                                       tmp_path) == ["E-101.pdf"]
    assert "id=1CpgOD3xxkjv3ge13-92eTb2xjFmggjBA" in vus[-1] and "drive.usercontent.google.com" in vus[-1]

    monkeypatch.setattr(gdrive.DossierDrive, "fichiers", lambda self, i, prefixe="": [
        {"id": "a" * 25, "nom": "Electricite.pdf", "chemin": "Electricite.pdf"},
        {"id": "b" * 25, "nom": "Devis.pdf", "chemin": "Prix/Devis.pdf"},                       # prix : jamais
        {"id": "c" * 25, "nom": "Releve Daniel.pdf", "chemin": "take off/Releve Daniel.pdf"},   # estimateur : jamais
        {"id": "d" * 25, "nom": "notes.docx", "chemin": "notes.docx"}])
    vus.clear()
    serveur._telecharger_source("https://drive.google.com/drive/folders/13JWszeHOEIM41Gf6GnNO0o4sOtWZHOW7", tmp_path)
    assert len(vus) == 1 and "a" * 25 in vus[0]

    brut = 'attachment; filename="P-D Électricité.pdf"'.encode("utf-8").decode("latin-1")   # tel que lu par HTTP
    monkeypatch.setattr(requests.Session, "get", lambda self, url, **kw: _Rep(b"%PDF-1.7", {"content-disposition": brut}))
    assert serveur._telecharger_source("https://drive.google.com/file/d/1CpgOD3xxkjv3ge13-92eTb2xjFmggjBA/view",
                                       tmp_path) == ["P-D Électricité.pdf"]

    monkeypatch.setattr(requests.Session, "get", lambda self, url, **kw: _Rep(b"<html>connexion</html>"))
    with pytest.raises(serveur.ToolError, match="partager"):
        serveur._telecharger_source("https://drive.google.com/file/d/1CpgOD3xxkjv3ge13-92eTb2xjFmggjBA/view", tmp_path)
