"""Démarrage rapide du transport stdio : « initialize » répondu avant d'avoir importé le SDK.

La mission impose un démarrage en moins de 0,2 s (PROMPT_MISSION.md ; mesure :
`.venv/bin/python outils/mesurer_demarrage_mcp.py --essais 5 --limite 0.2`). Le SDK n'est
pas la cible : le chargement seul de `mcp` (client, mcp_types, transports HTTP) prend
~0,4 s. Ici la première ligne du canal est reconnue et répondue avec la seule bibliothèque
standard (protocole JSON-RPC 2.0, versions de prise de contact du SDK), puis le serveur
complet se charge et la boucle délègue chaque requête au noyau officiel du SDK
(`mcp.server.runner.serve_one` + `Connection.from_envelope`) — gestion des erreurs,
validation des paramètres et contenu des résultats identiques au serveur officiel.

Toute première ligne dont ce n'est pas un « initialize » d'une version supportée rend la
main au serveur officiel, intégralement (`serveur_officiel`, ligne non consommée : repli
gratuit) — erreurs de prise de contact incluses. Dans la boucle, une ligne illisible ou
une réponse inattendue est ignorée comme le font les transports du SDK (journal de
débogage), jamais un message inventé.
"""
from __future__ import annotations

import json
import sys
import time
from typing import Any

from .instructions import INSTRUCTIONS

# Versions de prise de contact acceptées par le SDK installé (mcp_types.version.HANDSHAKE_PROTOCOL_VERSIONS),
# figées ici pour répondre sans l'importer : l'écart éventuel est contrôlé par tests/test_demarrage_mcp.py.
VERSIONS_POISE = ("2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25")
# Capacités au format filaire du noyau (InitializeResult — PAS le dump des opérations
# d'initialisation, qui ajoute « extensions ») : parité contrôlée par
# tests/test_demarrage_mcp.py::test_reponse_initialize_pareille_au_serveur_officiel.
CAPACITES = {
    "prompts": {"listChanged": False},
    "resources": {"subscribe": False, "listChanged": False},
    "tools": {"listChanged": False},
}
INFO_SERVEUR = {"name": "expert-estimateur", "version": "0.1.0"}


def reponse_initialize(ligne: bytes) -> tuple[bytes, dict[str, Any]] | None:
    """Réponse « initialize » immédiate, ou None quand le SDK doit servir la requête.

    Renvoie la ligne de réponse (JSON-RPC, un « \\n » final) et les paramètres de prise
    de contact (protocolVersion, clientInfo, capabilities) dont la boucle a besoin pour
    construire l'état de connexion au noyau. Une ligne non initialize, sans identifiant
    de requête ou à version inconnue rend la main au serveur officiel (repli gratuit :
    la ligne n'a pas été consommée par l'appelant).
    """
    try:
        message = json.loads(ligne)
    except ValueError:
        return None
    if not isinstance(message, dict):
        return None
    if message.get("jsonrpc") != "2.0" or message.get("method") != "initialize":
        return None
    identifiant = message.get("id")
    if identifiant is None:
        return None   # initialize sans identifiant de requête : le tranchant reste au SDK
    params = message.get("params")
    if not isinstance(params, dict) or params.get("protocolVersion") not in VERSIONS_POISE:
        return None   # le refus exact (code, versions servies) reste celui du SDK
    version = params.get("protocolVersion")
    reponse = json.dumps({
        "jsonrpc": "2.0",
        "id": identifiant,
        "result": {
            "protocolVersion": version,
            "capabilities": CAPACITES,
            "serverInfo": INFO_SERVEUR,
            "instructions": INSTRUCTIONS,
        },
    }, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    return reponse, {
        "version": version,
        "client_info": params.get("clientInfo"),
        "capacites_client": params.get("capabilities"),
    }


def stdio(delai_lecture: float = 2.0) -> int:
    """Serveur stdio : réponse initialize immédiate, puis boucle d'échanges officielle."""
    tampon = sys.stdin.buffer
    sortie = sys.stdout.buffer
    premier = tampon.peek(1)   # bloque jusqu'aux premiers octets (ou EOF) ; rien n'est consommé
    echeance = time.monotonic() + delai_lecture
    while premier and b"\n" not in premier and time.monotonic() < echeance:
        time.sleep(0.005)
        premier = tampon.peek(1)
    rapide = reponse_initialize(premier.split(b"\n", 1)[0]) if b"\n" in premier else None
    if rapide is None:
        return serveur_officiel()   # ligne intacte dans le tampon : le SDK voit le flux d'origine
    reponse, poise = rapide
    tampon.read(premier.index(b"\n") + 1)   # retire exactement la première ligne du tampon
    sortie.write(reponse)
    sortie.flush()
    return boucle_echanges(poise["version"], poise["client_info"], poise["capacites_client"])


def serveur_officiel() -> int:
    """Le serveur complet, tel quel : la boucle du SDK gère initialize et tous les échanges.

    Les streams sont passés EXPLICITEMENT au transport du SDK : en les laissant le
    prendre lui-même, il réclamerait les descripteurs 0/1 en ouvrant un flux neuf sur leur
    duplicata noyau — et les octets déjà tamponnés côté utilisateur (notre peek de la
    première ligne) seraient invisibles à ce flux neuf : le serveur attendrait des octets
    déjà en sa possession. En passant les mêmes tampons, la boucle du SDK voit exactement
    le flux d'origine, tampon compris.
    """
    import io

    from .serveur import mcp as application

    import anyio

    async def service() -> None:
        from mcp.server.stdio import stdio_server

        lecture = anyio.wrap_file(io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace"))
        ecriture = anyio.wrap_file(io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8"))
        async with stdio_server(lecture, ecriture) as (read_stream, write_stream):
            await application._lowlevel_server.run(
                read_stream, write_stream, application._lowlevel_server.create_initialization_options())

    anyio.run(service)
    return 0


class CtxEchange:
    """Contexte du dispatch pour un échange : pas de canal serveur→client (stdio sans état ici).

    Ne porte que du code paresseux : importer ce module doit rester léger.
    """

    def __init__(self, identifiant: Any) -> None:
        self._id = identifiant

    @property
    def transport(self) -> Any:
        from mcp.shared.transport_context import TransportContext
        return TransportContext(kind="stdio", can_send_request=False)

    @property
    def can_send_request(self) -> bool:
        return False

    @property
    def request_id(self) -> Any:
        return self._id

    @property
    def message_metadata(self) -> None:
        return None

    async def send_raw_request(self, _requete: Any, _options: Any = None) -> Any:
        from mcp.shared.exceptions import NoBackChannelError
        raise NoBackChannelError("pas de canal retour sur un stdio sans état")

    async def send_notification(self, _methode: str, _params: Any = None, _options: Any = None) -> None:
        return None   # notification serveur→client abandonnée : ce serveur n'en publie aucune



def boucle_echanges(version: str, client_info: Any, capacites_client: Any) -> int:
    """Charge le serveur complet et délègue chaque requête au noyau du SDK, un échange à la fois.

    L'état de connexion est reconstruit par requête (`Connection.from_envelope`, né prêt) :
    le serveur ne publie rien d'asynchrone (aucun listChanged, aucune souscription), donc
    ce service sans état est équivalent au service en boucle du SDK pour son usage.
    """
    import anyio
    anyio.run(_boucle, version, client_info, capacites_client)
    return 0


async def _boucle(version: str, client_info: Any, capacites_client: Any) -> int:
    from mcp.server.connection import Connection
    from mcp.server.runner import serve_one
    from mcp.shared.exceptions import MCPError
    from mcp.shared.jsonrpc_dispatcher import handler_exception_to_error_data
    from mcp_types import ErrorData, INTERNAL_ERROR
    from pydantic import ValidationError

    tampon = sys.stdin.buffer
    sortie = sys.stdout.buffer

    def enveloppe(identifiant: Any, corps: dict) -> bytes:
        message = {"jsonrpc": "2.0", "id": identifiant}
        message.update(corps)
        return json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"

    async def echange(identifiant: Any, methode: str, params: Any) -> bytes:
        from .serveur import mcp as application

        connexion = Connection.from_envelope(version, client_info, capacites_client)
        try:
            resultat = await serve_one(application._lowlevel_server, CtxEchange(identifiant),
                                       methode, params, connection=connexion, lifespan_state={})
        except MCPError as erreur:
            return enveloppe(identifiant, {"error": erreur.error.model_dump(by_alias=True, exclude_none=True)})
        except ValidationError as erreur:
            donnee = handler_exception_to_error_data(erreur)
            return enveloppe(identifiant, {"error": (donnee if donnee is not None else ErrorData(
                code=INTERNAL_ERROR, message=str(erreur))).model_dump(by_alias=True, exclude_none=True)})
        except Exception as exception:
            return enveloppe(identifiant, {"error": ErrorData(
                code=INTERNAL_ERROR, message=f"Erreur interne : {exception}").model_dump(
                by_alias=True, exclude_none=True)})
        return enveloppe(identifiant, {"result": resultat})

    while True:
        ligne = tampon.readline()
        if not ligne:
            break
        try:
            message = json.loads(ligne)
        except ValueError:
            continue   # trame illisible : ignorée comme par les transports du SDK (journal), pas de réponse inventée
        if isinstance(message, list):
            reponses = [await echange(element.get("id"), element.get("method", ""), element.get("params"))
                        for element in message
                        if isinstance(element, dict) and "method" in element
                        and element.get("id") is not None]
            if reponses:
                sortie.write(json.dumps(reponses, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n")
                sortie.flush()
            continue
        if not isinstance(message, dict) or "method" not in message:
            continue   # réponse renvoyée au serveur ou trame non conforme : ignorée, comme les transports du SDK
        identifiant = message.get("id")
        if identifiant is None:
            continue   # notification (notifications/initialized…) : rien à répondre
        sortie.write(await echange(identifiant, message.get("method", ""), message.get("params")))
        sortie.flush()
    return 0
