"""Étiquetage par vision (releve/vision_signatures.py) : choix du fournisseur par clé, toutes les planches, requêtes conformes
à la doc (Gemini : schéma JSON, réflexion LOW, pas de temperature ; NVIDIA : data URI, réflexion coupée, Retry-After),
rejet des identifiants inventés, réponse tronquée ou illisible journalisée. Aucun appel réseau : le transport est simulé."""
import csv, json, os, sys
from pathlib import Path

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "releve"))
sys.path.insert(0, REPO)
import vision_signatures as vs  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32


def _ok(*ids, label="BOITIER", famille="commande"):
    return json.dumps([{"sig_id": i, "label": label, "famille": famille, "forme": "carre", "code": "DP1", "materiel": "NPP16"} for i in ids])


def test_fournisseur_selon_les_cles():
    assert vs.fournisseur({}) is None
    assert vs.fournisseur({"NVIDIA_API_KEY": "nvapi-x"}) == "nvidia"
    assert vs.fournisseur({"GEMINI_API_KEY": "g"}) == "gemini"
    assert vs.fournisseur({"GOOGLE_API_KEY": "g", "NVIDIA_API_KEY": "n"}) == "gemini"           # Gemini d'abord
    assert vs.fournisseur({"GEMINI_API_KEY": "g", "NVIDIA_API_KEY": "n", "ESTIMATEUR_VISION": "nvidia"}) == "nvidia"
    assert vs.fournisseur({"GEMINI_API_KEY": "g", "ESTIMATEUR_VISION": "off"}) is None
    assert vs.fournisseur({"NVIDIA_API_KEY": "n", "ESTIMATEUR_VISION": "gemini"}) is None         # forcé sans sa clé : rien


def test_planche_de_chaque_signature(tmp_path):
    idx = tmp_path / "blocs-index.csv"
    with open(idx, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["sig_id", "signature"])
        for i in range(1, 36):
            w.writerow([f"S{i:03d}", f"sig{i}"])
    par = vs.signatures_par_planche(idx, ["S002", "S030", "S031", "S035"], nb_planches=2)
    assert par == {1: ["S002", "S030"], 2: ["S031", "S035"]}                                      # 30 vignettes par planche
    assert vs.signatures_par_planche(idx, ["S035"], nb_planches=1) == {}                          # pas de vignette = ignoré


def test_etiqueter_lit_toutes_les_planches_et_rejette_ce_qui_n_est_pas_demande(tmp_path, monkeypatch):
    p1, p2 = tmp_path / "signatures-01.png", tmp_path / "signatures-02.png"
    p1.write_bytes(PNG); p2.write_bytes(PNG)
    appels = []

    def faux(png, texte, modele):
        appels.append(texte)
        if "S001" in texte:
            return _ok("S001", "S099"), {"finish_reason": "STOP"}                                 # S099 : inventé, pas sur la planche
        return json.dumps([{"sig_id": "S031", "label": "x", "famille": "IGNORER"}]), {"finish_reason": "STOP"}
    monkeypatch.setattr(vs, "_appel_nvidia", faux)
    journal = []
    items = vs.etiqueter({p1: ["S001"], p2: ["S031"]}, "nvidia", journal)
    assert len(appels) == 2                                                                        # une requête par planche
    assert [i["sig_id"] for i in items] == ["S001", "S031"]
    assert items[0]["label"] == "BOITIER" and items[0]["code"] == "DP1"
    assert items[1]["label"] == "IGNORER"
    assert journal[0]["rejetees_hors_planche"] == 1 and journal[0]["gardees"] == 1
    assert "S099" not in appels[0] and "S001" in appels[0]                                         # consigne = ses identifiants seulement
    assert "RECTANGLE ROUGE" in appels[0] and "IGNORER" in appels[0]


@pytest.mark.parametrize("reponse,fin,motif", [
    (_ok("S001"), "MAX_TOKENS", "tronquée"),
    (_ok("S001"), "length", "tronquée"),
    ("pas du json", "STOP", "JSONDecodeError"),
    (json.dumps([{"sig_id": "S001", "label": "X", "famille": "inconnue"}]), "STOP", "ValidationError"),
])
def test_reponse_tronquee_ou_illisible_est_journalisee_jamais_crue(tmp_path, monkeypatch, reponse, fin, motif):
    p = tmp_path / "signatures-01.png"; p.write_bytes(PNG)
    monkeypatch.setattr(vs, "_appel_gemini", lambda png, texte, modele: (reponse, {"finish_reason": fin}))
    journal = []
    assert vs.etiqueter({p: ["S001"]}, "gemini", journal) == []
    assert motif in journal[0]["erreur"]


def test_echec_reseau_est_journalise_sans_bloquer(tmp_path, monkeypatch):
    p = tmp_path / "signatures-01.png"; p.write_bytes(PNG)

    def casse(png, texte, modele):
        raise ConnectionError("CONNECT tunnel failed, response 403")
    monkeypatch.setattr(vs, "_appel_nvidia", casse)
    journal = []
    assert vs.etiqueter({p: ["S001"]}, "nvidia", journal) == []
    assert "403" in journal[0]["erreur"]


def test_requete_nvidia_conforme_et_retry_after_respecte(monkeypatch):
    import requests
    envoyees, pauses = [], []

    class Rep:
        def __init__(self, code, corps=None, entetes=None):
            self.status_code, self._c, self.headers = code, corps or {}, entetes or {}
        def json(self): return self._c
        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(str(self.status_code))
    suite = [Rep(429, entetes={"Retry-After": "7"}), Rep(200, {"choices": [{"message": {"content": "[]"}, "finish_reason": "stop"}]})]

    def faux_post(url, headers, json, timeout):
        envoyees.append((url, headers, json, timeout)); return suite.pop(0)
    monkeypatch.setattr(requests, "post", faux_post)
    monkeypatch.setattr(vs.time, "sleep", lambda s: pauses.append(s))
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-secret")
    texte, meta = vs._appel_nvidia(PNG, "consigne", vs.MODELE_NVIDIA)
    assert (texte, meta["finish_reason"]) == ("[]", "stop")
    assert len(envoyees) == 2 and pauses == [7.0]                                                  # attend le Retry-After du serveur
    url, entetes, corps, delai = envoyees[0]
    assert url == "https://integrate.api.nvidia.com/v1/chat/completions"
    assert entetes["Authorization"] == "Bearer nvapi-secret"
    assert corps["model"] == vs.MODELE_NVIDIA and corps["temperature"] == 0
    assert corps["chat_template_kwargs"] == {"enable_thinking": False}                             # réflexion coupée
    image = corps["messages"][0]["content"][1]["image_url"]["url"]
    assert image.startswith("data:image/png;base64,")


def test_requete_gemini_conforme(monkeypatch):
    genai = pytest.importorskip("google.genai")
    saisi = {}

    class FauxModeles:
        def generate_content(self, model, config, contents):
            saisi.update(model=model, config=config, contents=contents)
            class C: finish_reason = type("F", (), {"name": "STOP"})()
            class R: text = "[]"; candidates = [C()]
            return R()

    class FauxClient:
        models = FauxModeles()
    monkeypatch.setattr(genai, "Client", lambda *a, **k: FauxClient())
    texte, meta = vs._appel_gemini(PNG, "consigne", vs.MODELE_GEMINI)
    cfg = saisi["config"]
    assert saisi["model"] == "gemini-3.8-flash" and meta["finish_reason"] == "STOP"
    assert cfg.response_mime_type == "application/json" and cfg.response_json_schema    # schéma JSON, pas de regex
    assert cfg.thinking_config.thinking_level.name == "LOW"
    assert cfg.temperature is None                                                         # ignorée depuis Gemini 3.6 : jamais posée
    assert saisi["contents"][0].inline_data.mime_type == "image/png"


def test_serveur_sans_cle_journalise_le_motif_et_ne_bloque_pas(tmp_path, monkeypatch):
    from serveur_mcp import serveur
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "NVIDIA_API_KEY", "ESTIMATEUR_VISION"):
        monkeypatch.delenv(k, raising=False)
    travail, sigs = _dossier_vision(tmp_path)
    assert serveur._etiqueter_signatures_vision(travail, sigs) == 0
    assert "aucune clé" in (travail / "vision.log").read_text(encoding="utf-8")


def test_serveur_avec_cle_ecrit_les_regles_du_dossier(tmp_path, monkeypatch):
    from serveur_mcp import serveur
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "ESTIMATEUR_VISION"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-x")
    monkeypatch.setattr(vs, "_appel_nvidia", lambda png, texte, modele: (_ok("S001", label="DETECTEUR", famille="alarme") , {"finish_reason": "stop"}))
    travail, sigs = _dossier_vision(tmp_path)
    assert serveur._etiqueter_signatures_vision(travail, sigs) == 1
    regles = list(csv.DictReader(open(travail / "blocs-familles.csv", encoding="utf-8")))
    assert regles[0]["sig_id"] == "S001" and regles[0]["label"] == "DETECTEUR" and regles[0]["origine"] == "vision-nvidia"
    assert json.loads((travail / "vision.log").read_text(encoding="utf-8").splitlines()[0])["fournisseur"] == "nvidia"


def _dossier_vision(tmp_path: Path):
    travail = tmp_path / "travail"; travail.mkdir()
    sigs = tmp_path / "signatures"; sigs.mkdir()
    (sigs / "signatures-01.png").write_bytes(PNG)
    with open(travail / "blocs-index.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["sig_id", "signature"]); w.writerow(["S001", "sig1"])
    (travail / "blocs-a-etiqueter.json").write_text(json.dumps({"inconnues": [{"sig_id": "S001", "n_plans": 5}]}), encoding="utf-8")
    return travail, sigs
