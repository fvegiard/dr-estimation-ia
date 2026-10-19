#!/bin/bash
# Hook SessionStart — session cloud Claude Code seulement : installe les dépendances Python du dépôt
# pour que `python -m pytest tests -q`, `python -m src.validation.jeu_reference`, le serveur MCP et la
# route « la session tient lieu d'agent » (CLAUDE.md §Agents) marchent dès le premier tour.
# Synchrone (pas de mode async) : la session ne démarre qu'une fois les paquets en place, pas de course.
# Idempotent : pip ne réinstalle rien de ce qui est déjà là ; l'état du conteneur est mis en cache après le hook.
# Poste Windows : ce hook ne fait rien (CLAUDE_CODE_REMOTE absent) — voir environment.yml (conda).
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

# requirements.txt = ce que la CI installe ; opencv-python-headless = route raster
# (releve/ancrage_raster.py, releve/comparer_legende.py le déclarent seulement en dépendance inline uv).
python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore \
  -r requirements.txt "opencv-python-headless>=4.9" >&2

# Variables de session : UTF-8 partout (accents des chemins et des rapports), dossiers du serveur MCP
# hors du dépôt suivi (travail-mcp/ est dans .gitignore).
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export PYTHONUTF8=1"
    echo "export PYTHONIOENCODING=utf-8"
    echo "export ESTIMATEUR_BASE=\"$PWD/travail-mcp\""
  } >> "$CLAUDE_ENV_FILE"
fi

# Contrôle : un import manquant fait échouer le hook au lieu de laisser croire que tout est prêt.
python3 - <<'EOF'
import importlib
for m in ("pymupdf", "PIL", "openpyxl", "pytest", "pydantic", "numpy", "scipy", "sklearn",
          "joblib", "markdown", "mcp", "uvicorn", "requests", "cv2"):
    importlib.import_module(m)
print("environnement dr-estimation-ia prêt : dépendances Python installées (requirements.txt + OpenCV)")
EOF
