"""Chronomètre le vrai protocole stdio, depuis la création du processus Python.

Exemple : .venv/Scripts/python.exe outils/mesurer_demarrage_mcp.py --essais 5
Le premier essai n'est pas un démarrage à froid garanti : aucun cache OS n'est vidé.
Le code de sortie vaut 1 si un échange échoue ou si un essai dépasse la limite.
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import statistics
import subprocess
import sys
import threading
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def mesurer(python: str, *, delai: float = 15.0) -> dict:
    """Vérifie initialize, les trois catalogues et la fermeture propre du serveur."""
    messages: queue.Queue[str | None] = queue.Queue()
    erreurs: list[str] = []
    debut = time.perf_counter()
    processus = subprocess.Popen(
        [python, "-m", "serveur_mcp"],
        cwd=RACINE,
        env=dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8"),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    assert processus.stdin is not None
    assert processus.stdout is not None
    assert processus.stderr is not None

    def lire_sortie() -> None:
        assert processus.stdout is not None
        for ligne in processus.stdout:
            messages.put(ligne)
        messages.put(None)

    def lire_erreurs() -> None:
        assert processus.stderr is not None
        erreurs.extend(processus.stderr.readlines())

    sortie = threading.Thread(target=lire_sortie, daemon=True)
    diagnostic = threading.Thread(target=lire_erreurs, daemon=True)
    sortie.start()
    diagnostic.start()

    def envoyer(message: dict) -> None:
        assert processus.stdin is not None
        processus.stdin.write(json.dumps(message) + "\n")
        processus.stdin.flush()

    def demander(identifiant: int, methode: str, params: dict) -> dict:
        envoyer({"jsonrpc": "2.0", "id": identifiant, "method": methode, "params": params})
        echeance = time.perf_counter() + delai
        while True:
            restant = echeance - time.perf_counter()
            if restant <= 0:
                raise TimeoutError(f"Réponse {methode} absente après {delai:g} s")
            try:
                ligne = messages.get(timeout=restant)
            except queue.Empty as exc:
                raise TimeoutError(f"Réponse {methode} absente après {delai:g} s") from exc
            if ligne is None:
                raise RuntimeError(f"Serveur fermé avant la réponse {methode}")
            reponse = json.loads(ligne)
            if reponse.get("id") == identifiant:
                if "error" in reponse:
                    raise RuntimeError(f"{methode} : {reponse['error']}")
                return reponse["result"]

    try:
        initialisation = demander(1, "initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "mesure-demarrage", "version": "1.0"},
        })
        duree = time.perf_counter() - debut
        if initialisation.get("serverInfo", {}).get("name") != "expert-estimateur":
            raise RuntimeError(f"Identité MCP inattendue : {initialisation.get('serverInfo')}")
        envoyer({"jsonrpc": "2.0", "method": "notifications/initialized"})
        outils = demander(2, "tools/list", {})["tools"]
        noms = {outil["name"] for outil in outils}
        attendus = {"relever_automatique", "voir_image", "quantites", "produire_livrables"}
        if not attendus <= noms:
            raise RuntimeError(f"Outils manquants : {sorted(attendus - noms)}")
        ressources = demander(3, "resources/list", {})["resources"]
        if "estimateur://methode" not in {r["uri"] for r in ressources}:
            raise RuntimeError("Ressource estimateur://methode absente")
        prompts = demander(4, "prompts/list", {})["prompts"]
        if "releve_planexpert" not in {p["name"] for p in prompts}:
            raise RuntimeError("Prompt releve_planexpert absent")
        catalogues = time.perf_counter() - debut
        processus.stdin.close()
        code = processus.wait(timeout=delai)
        diagnostic.join(timeout=delai)
        if code != 0:
            raise RuntimeError(f"Serveur terminé avec le code {code} : {''.join(erreurs)}")
        return {
            "initialize_s": round(duree, 6),
            "catalogues_s": round(catalogues, 6),
            "outils": len(outils),
            "ressources": len(ressources),
            "prompts": len(prompts),
            "protocole": initialisation["protocolVersion"],
            "exit_code": code,
            "stderr": "".join(erreurs),
        }
    finally:
        if processus.poll() is None:
            processus.kill()
            processus.wait(timeout=delai)
        sortie.join(timeout=delai)
        diagnostic.join(timeout=delai)
        for flux in (processus.stdin, processus.stdout, processus.stderr):
            if flux is not None:
                flux.close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--essais", type=int, default=5)
    ap.add_argument("--limite", type=float, default=0.2, help="secondes, limite stricte par essai")
    ap.add_argument("--delai", type=float, default=15.0, help="secondes par réponse ou fermeture")
    ap.add_argument("--rapport", type=Path)
    args = ap.parse_args(argv)
    if args.essais < 1 or args.limite <= 0 or args.delai <= 0:
        ap.error("essais, limite et delai doivent être strictement positifs")
    rapport: dict = {
        "python": sys.executable,
        "commande": [sys.executable, "-m", "serveur_mcp"],
        "limite_s": args.limite,
        "mesure": "Création du processus jusqu'à réception de la réponse initialize complète.",
        "caches": "Non vidés : premier essai distinct, suivants à caches potentiellement chauds.",
        "essais": [],
    }
    try:
        for _ in range(args.essais):
            rapport["essais"].append(mesurer(sys.executable, delai=args.delai))
        temps = [essai["initialize_s"] for essai in rapport["essais"]]
        rapport.update({
            "premier_s": temps[0],
            "minimum_s": min(temps),
            "mediane_s": statistics.median(temps),
            "maximum_s": max(temps),
            "conforme": all(t < args.limite for t in temps),
        })
    except (OSError, ValueError, KeyError, RuntimeError, TimeoutError, subprocess.TimeoutExpired) as exc:
        rapport.update({"conforme": False, "erreur": str(exc)})
    texte = json.dumps(rapport, ensure_ascii=False, indent=2)
    if args.rapport:
        args.rapport.parent.mkdir(parents=True, exist_ok=True)
        args.rapport.write_text(texte + "\n", encoding="utf-8")
    print(texte)
    return 0 if rapport["conforme"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
