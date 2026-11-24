"""Rotation du bearer sur l'installation Podman locale, sans écrire ni afficher sa valeur.

Étapes: préflight, test sur un volume mémoire et un port local temporaire, puis
bascule du même digest d'image et du même volume. Ne modifie aucun autre client.
"""
from __future__ import annotations

import argparse
import http.client
import json
from pathlib import Path
import secrets
import subprocess
import time

NOM = "expert-estimateur-svc"
VARIABLE = "ESTIMATEUR_MCP_CLE"
PORT = 8765
PORT_TEST = 18765


def podman(*args, entree=None, capture=False):
    p = subprocess.run(["podman", *args], input=entree, check=False, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=45)
    if p.returncode:
        # L'erreur Podman peut citer les paramètres d'une requête; rien n'est relayé.
        raise RuntimeError(f"Podman {args[0]} a échoué (code {p.returncode})")
    return p.stdout if capture else None


def statut(port, cle=None):
    connexion = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
    try:
        entetes = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if cle:
            entetes["Authorization"] = "Bearer " + cle
        connexion.request("POST", "/mcp", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                       "clientInfo": {"name": "smoke-rotation", "version": "1"}}}), entetes)
        r = connexion.getresponse()
        return r.status, r.status == 200 and b'"protocolVersion"' in r.read(262144)
    finally:
        connexion.close()


def verifier(port, ancienne, nouvelle):
    for _ in range(35):
        try:
            if statut(port, nouvelle) == (200, True):
                break
        except (OSError, http.client.HTTPException):
            pass
        time.sleep(.3)
    else:
        raise RuntimeError(f"initialize authentifié indisponible sur {port}")
    if statut(port)[0] != 401 or statut(port, ancienne)[0] != 401:
        raise RuntimeError(f"refus sans bearer ou de l'ancien bearer non vérifié sur {port}")
    print(f"Port {port} : nouveau bearer 200 (MCP initialize), anonyme et ancien bearer 401.")


def rotation(appliquer):
    avant = json.loads(podman("inspect", NOM, capture=True))[0]
    config, hote = avant["Config"], avant["HostConfig"]
    vars_ = dict(v.split("=", 1) for v in config["Env"])
    ancienne = vars_.pop(VARIABLE, "")
    montages = avant["Mounts"]
    if not ancienne or not avant["State"]["Running"] or len(montages) != 1 or (
            montages[0].get("Name"), montages[0]["Destination"]) != ("estim", "/data"):
        raise RuntimeError("service actif et volume estim non reconnus; aucune bascule")
    if hote["PortBindings"] != {"8765/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8765"}]}:
        raise RuntimeError("publication inattendue; aucune bascule")
    nom_secret = f"expert-estimateur-bearer-{secrets.token_hex(6)}"
    nouvelle = secrets.token_urlsafe(40)
    essai = nom_secret + "-test"
    retour = nom_secret + "-retour"
    options = ["--secret", f"{nom_secret},type=env,target={VARIABLE}"]
    for k, v in sorted(vars_.items()):
        if k in {"ESTIMATEUR_BASE", "ESTIMATEUR_BIBLIOTHEQUE", "ESTIMATEUR_HOTE_PERMIS", "ESTIMATEUR_URL_PUBLIQUE"}:
            options.extend(["-e", f"{k}={v}"])
    preflight = Path.home() / "work/legion-knowledge/preflight.sh"
    if appliquer:
        subprocess.run([str(preflight), "backup", "expert-estimateur-mcp"], check=True)
    podman("secret", "create", nom_secret, "-", entree=nouvelle)
    actif = False
    try:
        try:
            podman("run", "-d", "--name", essai, "-p", f"127.0.0.1:{PORT_TEST}:{PORT}",
                   "--tmpfs", "/data", *options, avant["Image"])
            verifier(PORT_TEST, ancienne, nouvelle)
        finally:
            if subprocess.run(["podman", "container", "exists", essai], check=False).returncode == 0:
                podman("rm", "-f", essai)
        if not appliquer:
            return
        # Pendant la bascule le conteneur d'origine est conservé, arrêté. En
        # cas d'échec il est immédiatement remis en service avec sa config.
        podman("rename", NOM, retour)
        try:
            podman("stop", retour)
            podman("run", "-d", "--name", NOM, "-p", f"0.0.0.0:{PORT}:{PORT}", "-v", "estim:/data",
                   *options, avant["Image"])
            verifier(PORT, ancienne, nouvelle)
            subprocess.run([str(preflight), "verify", "expert-estimateur-mcp"], check=True)
        except Exception:
            if subprocess.run(["podman", "container", "exists", NOM], check=False).returncode == 0:
                podman("rm", "-f", NOM)
            podman("rename", retour, NOM)
            subprocess.run([str(preflight), "restore", "expert-estimateur-mcp"], check=True)
            subprocess.run([str(preflight), "verify", "expert-estimateur-mcp"], check=True)
            raise
        actif = True
        # Le retour applicatif est possible avec l'image sauvegardée et le NOUVEAU secret.
        podman("rm", retour)
        print(f"Rotation active; secret Podman : {nom_secret} (nom seulement).")
    finally:
        if not actif:
            podman("secret", "rm", nom_secret)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--appliquer", action="store_true", help="basculer après succès de l'instance d'essai")
    a = p.parse_args()
    try:
        rotation(a.appliquer)
    except (RuntimeError, subprocess.SubprocessError, OSError, KeyError) as e:
        # Ne pas imprimer d'exception qui pourrait contenir une valeur d'environnement.
        raise SystemExit(str(e) if isinstance(e, RuntimeError) else f"Échec rotation ({type(e).__name__})")