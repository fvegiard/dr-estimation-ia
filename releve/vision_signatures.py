# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2", "requests", "google-genai>=2.31"]
# ///
"""Étiquetage des signatures de blocs par VISION (API Gemini ou NVIDIA) : le modèle regarde les planches
`signatures-NN.png` écrites par blocs_vignettes.py et dit, pour chaque signature inconnue, si c'est un appareil
électrique (et lequel) ou du bruit (mur, fil, trame, numéro de détail, cartouche, schéma de câblage).

Choix du fournisseur (variables d'environnement, jamais de clé dans le dépôt) :
- `ESTIMATEUR_VISION` = gemini | nvidia | off ; sinon le premier dont la clé est présente (Gemini d'abord)
- Gemini : `GEMINI_API_KEY` (ou `GOOGLE_API_KEY`) ; modèle `ESTIMATEUR_VISION_MODELE_GEMINI` (défaut gemini-3.8-flash)
- NVIDIA : `NVIDIA_API_KEY` (nvapi-…) ; modèle `ESTIMATEUR_VISION_MODELE_NVIDIA` (défaut
  nvidia/nemotron-3.5-super-vl-120b-a12b) ; hôte integrate.api.nvidia.com à autoriser dans le réseau de l'environnement

Règles tirées de la documentation (rapports de recherche du 2026-10-20, voir tests/test_vision_signatures.py) :
- TOUTES les planches sont envoyées, une par appel, avec les seuls identifiants qu'elle contient (l'ancien appel ne lisait
  que la planche 1 et citait en dur des repères d'un autre dossier — il invitait à inventer) ;
- Gemini : `generate_content`, JSON Schema (`response_json_schema`), réflexion `LOW`, aucune `temperature`
  (ignorée depuis Gemini 3.6) ; `max_output_tokens` inclut la réflexion → on refuse une réponse tronquée ;
- NVIDIA : compatible OpenAI, image en data URI, réflexion coupée (`enable_thinking: false`), `Retry-After` respecté
  sur 429/5xx, une requête à la fois (le dépôt a vu des HTTP 500 dès 2 simultanées) ;
- une réponse n'est jamais crue sur parole : identifiants hors planche rejetés, familles hors liste rejetées,
  réponse tronquée ou illisible journalisée dans `travail/vision.log` (jamais silencieux).
"""
from __future__ import annotations
import base64, csv, json, os, re, sys, time
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, TypeAdapter, ValidationError

FAMILLES = ("luminaire", "commande", "secours", "prise", "alarme", "telecom", "distribution", "mecanique", "chauffage", "autre")
FORMES = ("carre", "cercle", "triangle", "losange")
PAR_PLANCHE = 30                       # = blocs_vignettes.py --par-planche (défaut)
MODELE_GEMINI = "gemini-3.8-flash"
MODELE_NVIDIA = "nvidia/nemotron-3.5-super-vl-120b-a12b"
URL_NVIDIA = "https://integrate.api.nvidia.com/v1/chat/completions"
MAX_JETONS = 8192                      # inclut la réflexion côté Gemini
ESSAIS = 4


class Etiquette(BaseModel):
    sig_id: str
    label: str                                     # « IGNORER » ou le nom de l'appareil, en majuscules sans accents
    famille: Literal["luminaire", "commande", "secours", "prise", "alarme", "telecom", "distribution", "mecanique", "chauffage", "autre", "IGNORER"]
    forme: Literal["carre", "cercle", "triangle", "losange"] = "carre"
    code: str = ""                                 # repère lu dans ou contre le symbole (DP1, SO4…), sinon vide
    materiel: str = ""                             # texte lu sur le plan, sinon vide — jamais inventé


LISTE = TypeAdapter(list[Etiquette])


def consigne(sig_ids: list[str]) -> str:
    return (
        "Cette image est une planche de vignettes extraites d'un plan électrique de construction (PDF de CAO). "
        "Chaque vignette porte en haut son identifiant (de la forme Sxxx), son nombre d'instances et son diamètre ; le symbole "
        "à identifier est dans le RECTANGLE ROUGE ; le plan autour n'est que du contexte (texte, repères, murs).\n"
        f"Identifiants à traiter, et seulement ceux-là : {', '.join(sig_ids)}.\n"
        "Pour chacun, décide si le symbole encadré en rouge est un VRAI APPAREIL électrique posé sur le plan "
        "(luminaire, prise, interrupteur, boîtier de contrôle, détecteur, panneau, sortie…). Si oui : label = nom de "
        "l'appareil en MAJUSCULES sans accents, famille parmi " + ", ".join(FAMILLES) + ", forme = carre, cercle, triangle "
        "ou losange selon la silhouette, code = repère lisible dans ou contre le symbole (sinon vide), materiel = texte lu "
        "sur le plan (sinon vide). Sinon (mur, fil, trame de remplissage, flèche, cote, numéro de détail dans un cercle, "
        "lettre de renvoi, symbole de légende, cartouche, texte seul, schéma de câblage) : label = IGNORER et famille = IGNORER.\n"
        "Dans le doute : IGNORER. N'invente aucun texte : ce qui n'est pas lisible reste vide. "
        "Réponds uniquement par le tableau JSON, un objet par identifiant demandé."
    )


def fournisseur(env=None) -> str | None:
    env = os.environ if env is None else env
    choix = (env.get("ESTIMATEUR_VISION") or "").strip().lower()
    if choix == "off":
        return None
    if choix == "gemini":
        return "gemini" if (env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY")) else None
    if choix == "nvidia":
        return "nvidia" if env.get("NVIDIA_API_KEY") else None
    if env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY"):
        return "gemini"
    if env.get("NVIDIA_API_KEY"):
        return "nvidia"
    return None


def signatures_par_planche(index_csv: Path, inconnues: list[str], nb_planches: int, par_planche: int = PAR_PLANCHE) -> dict[int, list[str]]:
    """planche (1…) → identifiants INCONNUS qu'elle contient. blocs_vignettes.py écrit blocs-index.csv dans l'ordre des
    vignettes : la ligne i est sur la planche i // par_planche + 1 ; les lignes ajoutées après coup (blocs rares) n'ont
    pas de vignette et sont ignorées."""
    a_faire = set(inconnues)
    out: dict[int, list[str]] = {}
    with open(index_csv, encoding="utf-8", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh)):
            k = i // par_planche + 1
            if k > nb_planches:
                break
            if r["sig_id"] in a_faire:
                out.setdefault(k, []).append(r["sig_id"])
    return out


# ---------------------------------------------------------------------------------------------- fournisseurs
def _appel_gemini(png: bytes, texte: str, modele: str) -> tuple[str, dict]:
    from google import genai
    from google.genai import types
    cfg = types.GenerateContentConfig(
        response_mime_type="application/json", response_json_schema=LISTE.json_schema(),
        thinking_config=types.ThinkingConfig(thinking_level="LOW"), max_output_tokens=MAX_JETONS)
    r = genai.Client().models.generate_content(
        model=modele, config=cfg,
        contents=[types.Part.from_bytes(data=png, mime_type="image/png", media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH), texte])
    cand = (r.candidates or [None])[0]
    fin = getattr(getattr(cand, "finish_reason", None), "name", str(getattr(cand, "finish_reason", "")))
    return (r.text or ""), {"finish_reason": fin}


def _appel_nvidia(png: bytes, texte: str, modele: str) -> tuple[str, dict]:
    import requests
    corps = {"model": modele, "temperature": 0, "max_tokens": MAX_JETONS,
             "messages": [{"role": "user", "content": [
                 {"type": "text", "text": texte},
                 {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode("ascii")}}]}],
             "chat_template_kwargs": {"enable_thinking": False}}
    en_tete = {"Authorization": "Bearer " + os.environ["NVIDIA_API_KEY"], "Content-Type": "application/json"}
    for essai in range(1, ESSAIS + 1):
        r = requests.post(URL_NVIDIA, headers=en_tete, json=corps, timeout=300)
        if r.status_code in (429, 500, 502, 503, 504) and essai < ESSAIS:
            try:
                attente = float(r.headers.get("Retry-After") or 0)
            except ValueError:
                attente = 0.0
            time.sleep(min(max(attente, 2.0 ** essai), 60.0))
            continue
        r.raise_for_status()
        break
    ch = r.json()["choices"][0]
    return (ch["message"].get("content") or ""), {"finish_reason": ch.get("finish_reason")}


def _json_tableau(texte: str):
    """Tableau JSON d'une réponse : tel quel, sinon le premier tableau [...] ; jamais d'invention si illisible."""
    try:
        return json.loads(texte)
    except ValueError:
        m = re.search(r"\[.*\]", texte, re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def etiqueter(planches: dict[Path, list[str]], fournisseur_: str, journal: list[dict], modele: str = "") -> list[dict]:
    """planches : fichier PNG → identifiants à traiter sur cette planche. Rend les règles à écrire (format de
    `_ajouter_etiquettes`) ; `journal` reçoit une ligne par planche : succès, jetons, motif d'échec."""
    appel, modele = (_appel_gemini, modele or MODELE_GEMINI) if fournisseur_ == "gemini" else (_appel_nvidia, modele or MODELE_NVIDIA)
    items: list[dict] = []
    for png, sigs in planches.items():
        ligne = {"planche": png.name, "fournisseur": fournisseur_, "modele": modele, "demandees": len(sigs)}
        try:
            texte, meta = appel(png.read_bytes(), consigne(sigs), modele)
            ligne.update(meta)
            if str(meta.get("finish_reason") or "").upper() in ("MAX_TOKENS", "LENGTH"):
                raise ValueError("réponse tronquée (finish_reason=%s) : monter MAX_JETONS ou réduire la planche" % meta["finish_reason"])
            lues = LISTE.validate_python(_json_tableau(texte))
            permises = set(sigs)
            gardees = [e for e in lues if e.sig_id.strip().upper() in permises]
            ligne.update({"recues": len(lues), "gardees": len(gardees), "rejetees_hors_planche": len(lues) - len(gardees)})
            for e in gardees:
                d = e.model_dump()
                d["sig_id"] = e.sig_id.strip().upper()
                d["label"] = "IGNORER" if e.famille == "IGNORER" else e.label.strip().upper()
                if d["label"] == "IGNORER":
                    d["famille"] = "commande"      # colonne ignorée pour IGNORER ; valeur de la liste du dossier
                items.append(d)
        except (ValidationError, ValueError, KeyError) as e:
            ligne["erreur"] = type(e).__name__ + ": " + str(e)[:400]
        except Exception as e:  # noqa : réseau, quota, clé refusée… jamais avalé, jamais bloquant
            ligne["erreur"] = type(e).__name__ + ": " + str(e)[:400]
        journal.append(ligne)
    return items


def ecrire_journal(travail: Path, journal: list[dict]) -> None:
    (travail / "vision.log").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in journal) + "\n", encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit("module de bibliothèque : voir serveur_mcp/serveur.py::_etiqueter_signatures_vision")


if __name__ == "__main__":
    main()
