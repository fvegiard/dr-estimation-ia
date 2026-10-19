#!/bin/bash
# Hook SessionStart — session cloud Claude Code seulement : installe les dépendances Python du dépôt
# pour que `python -m pytest tests -q`, `python -m src.validation.jeu_reference`, le serveur MCP et
# `uv run releve/run.py <NOM>` (route blocs par défaut) marchent dès le premier tour.
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

# Contrôle : un paquet de requirements.txt absent fait échouer le hook au lieu de laisser croire que tout
# est prêt. La liste est relue dans requirements.txt (seule liste maintenue), jamais recopiée ici ;
# pymupdf et cv2 sont en plus importés pour de vrai (bibliothèques natives).
python3 - <<'EOF'
import importlib, importlib.metadata as md, pathlib, re
for ligne in pathlib.Path("requirements.txt").read_text(encoding="utf-8").splitlines():
    nom = re.split(r"[<>=!~;\[ ]", ligne.split("#")[0].strip())[0]
    if nom:
        md.version(nom)  # PackageNotFoundError si absent
for m in ("pymupdf", "cv2"):
    importlib.import_module(m)
EOF

# Variables de session : UTF-8 partout (accents des chemins et des rapports) ; dossiers du serveur MCP et de
# run.py dans le dépôt, comme les chemins relatifs de CLAUDE.md (INBOX/<S>, OUTBOX/<S>) — sinon run.py vise
# /mnt/d/claude/releve-auto, chemin WSL du poste. travail-mcp/, INBOX/ et OUTBOX/ sont dans .gitignore.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export PYTHONUTF8=1"
    echo "export PYTHONIOENCODING=utf-8"
    echo "export ESTIMATEUR_BASE=\"$PWD/travail-mcp\""
    echo "export RELEVE_BASE=\"$PWD\""
  } >> "$CLAUDE_ENV_FILE"
fi

echo "environnement dr-estimation-ia prêt : requirements.txt + OpenCV installés, RELEVE_BASE=$PWD"
