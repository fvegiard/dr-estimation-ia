"""Vérifie la joignabilité HTTP et le refus d'une requête sans authentification."""

import http.client


def main() -> int:
    connexion = http.client.HTTPConnection("127.0.0.1", 8765, timeout=3)
    try:
        connexion.request("GET", "/mcp")
        reponse = connexion.getresponse()
        if reponse.status == 401 and reponse.getheader("WWW-Authenticate", "").lower() == "bearer":
            print("/mcp : HTTP 401 Bearer attendu, sans authentification")
            return 0
        print(f"/mcp : HTTP {reponse.status}, attendu 401 avec défi Bearer")
    except (OSError, http.client.HTTPException) as erreur:
        print(f"/mcp : connexion impossible ({erreur})")
    finally:
        connexion.close()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())