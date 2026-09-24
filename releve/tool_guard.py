"""Garde-fou d'outils pour le relevé headless.

Actif seulement si RELEVE_TOOL_GUARD_ROOT est défini. Le hook PreToolUse :
- refuse Read/Write/Edit/Glob/Grep hors du dossier de travail ;
- refuse Bash hors d'une petite liste de commandes attendues.
"""
from __future__ import annotations

import json
import os
import pathlib
import shlex
import sys

FILE_TOOL_PATH_KEYS = {"file_path", "path", "paths"}
SAFE_SHELL_TOOLS = {"head", "cat", "sort", "cut"}
DENY = "deny"


def _real(path: str) -> str:
    return os.path.realpath(os.path.abspath(path))


def _resolve_arg_path(token: str, cwd: str) -> str:
    base = cwd if not os.path.isabs(token) else "/"
    return _real(os.path.join(base, token))


def _under(root: str, candidate: str) -> bool:
    try:
        return os.path.commonpath([root, candidate]) == root
    except ValueError:
        return False


def _deny(reason: str) -> int:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": DENY,
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


def _collect_paths(tool_input: object, cwd: str) -> list[str]:
    found: list[str] = []

    def walk(value: object, key: str | None = None) -> None:
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                walk(child_value, child_key)
            return
        if isinstance(value, list):
            for child in value:
                walk(child, key)
            return
        if not isinstance(value, str) or key not in FILE_TOOL_PATH_KEYS:
            return
        raw = value.strip()
        if not raw:
            return
        found.append(_resolve_arg_path(raw, cwd))

    walk(tool_input)
    return found


def _validate_file_tool(root: str, tool_input: dict, cwd: str) -> str | None:
    paths = _collect_paths(tool_input, cwd)
    if not paths:
        return None
    bad = [p for p in paths if not _under(root, p)]
    if bad:
        return f"Accès refusé hors du dossier de travail : {bad[0]}"
    return None


def _is_safe_shell_path(token: str, cwd: str, root: str) -> bool:
    if token.startswith("-"):
        return True
    if token in {".", ".."}:
        return False
    if "/" not in token and not token.startswith("."):
        return True
    resolved = _resolve_arg_path(token, cwd)
    return _under(root, resolved)


def _validate_bash(root: str, tool_input: dict, cwd: str) -> str | None:
    command = (tool_input.get("command") or "").strip()
    if not command:
        return "Commande Bash vide"
    if any(ch in command for ch in (";", "\n", "\r", "|", "&", "`", ">", "<")) or "$(" in command:
        return "Commande Bash chaînée ou redirigée refusée"
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return f"Commande Bash illisible : {exc}"
    if tuple(argv[:3]) == ("uv", "run", "releve/extract_occurrences.py"):
        if len(argv) != 4:
            return "extract_occurrences.py n'accepte qu'un seul argument : le workdir"
        return None if _resolve_arg_path(argv[3], cwd) == root else f"Argument Bash hors du dossier de travail : {argv[3]}"
    if tuple(argv[:3]) == ("uv", "run", "releve/traits.py"):
        if len(argv) not in (7, 8):
            return "traits.py attend WORKDIR FEUILLE x y [rayon]"
        return None if _resolve_arg_path(argv[3], cwd) == root else f"Argument Bash hors du dossier de travail : {argv[3]}"
    if tuple(argv[:3]) == ("uv", "run", "releve/zoom.py"):
        if len(argv) < 9:
            return "zoom.py attend WORKDIR FEUILLE X0 Y0 X1 Y1 [--px N] [--sans-marques]"
        if _resolve_arg_path(argv[3], cwd) != root:
            return f"Argument Bash hors du dossier de travail : {argv[3]}"
        extras = argv[9:]
        i = 0
        while i < len(extras):
            if extras[i] == "--sans-marques":
                i += 1
                continue
            if extras[i] == "--px" and i + 1 < len(extras):
                i += 2
                continue
            return f"Option zoom.py non autorisée : {' '.join(extras[i:])}"
        return None
    if argv and argv[0] in SAFE_SHELL_TOOLS:
        for token in argv[1:]:
            if not _is_safe_shell_path(token, cwd, root):
                return f"Argument Bash hors du dossier de travail : {token}"
        return None
    return f"Commande Bash non autorisée : {command}"


def validate(tool_name: str, tool_input: dict, cwd: str, root: str) -> str | None:
    if tool_name in {"Read", "Write", "Edit", "MultiEdit", "Glob", "Grep"}:
        return _validate_file_tool(root, tool_input, cwd)
    if tool_name == "Bash":
        return _validate_bash(root, tool_input, cwd)
    return None


def main() -> int:
    root = os.environ.get("RELEVE_TOOL_GUARD_ROOT")
    if not root:
        return 0
    payload = json.load(sys.stdin)
    cwd = _real(payload.get("cwd") or os.getcwd())
    root = _real(root)
    reason = validate(payload.get("tool_name") or "", payload.get("tool_input") or {}, cwd, root)
    if reason:
        return _deny(reason)
    return 0


if __name__ == "__main__":
    sys.exit(main())
