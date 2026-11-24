#!/bin/sh
# Ne démarre ni ne modifie les conteneurs. Le test stdio lance seulement un sous-processus de test.
set -eu

racine=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

verifier_travail() (
    conteneur=$1
    printf '\n=== %s ===\n' "$conteneur"
    echec=0
    timeout 15s podman exec --workdir /workspace "$conteneur" \
        python -B -m serveur_mcp --help >/dev/null || echec=1
    # Le test vérifie aussi les imports; pytest est lui-même une dépendance déclarée.
    timeout 60s podman exec --env PYTHONDONTWRITEBYTECODE=1 --workdir /workspace "$conteneur" \
        python -B -m pytest -q -p no:cacheprovider tests/test_demarrage_mcp.py || echec=1
    timeout 10s podman exec "$conteneur" git --version || echec=1
    exit "$echec"
)

verifier_serveur() {
    printf '\n=== HTTP MCP local ===\n'
    python3 -B "$racine/probe_http.py"
}

case "${1:-all}" in
    dev) verifier_travail dr-estimation-ai-dev ;;
    work) verifier_travail dr-estimation-ai-work ;;
    server) verifier_serveur ;;
    all)
        echec=0
        verifier_travail dr-estimation-ai-dev || echec=1
        verifier_travail dr-estimation-ai-work || echec=1
        verifier_serveur || echec=1
        exit "$echec"
        ;;
    *) printf 'Usage : sh %s [dev|work|server|all]\n' "$0" >&2; exit 2 ;;
esac