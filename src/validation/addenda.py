"""Check that every addendum filed in a Drive folder was either ingested by the takeoff or explicitly declared.

    python -m src.validation.addenda <drive-inventory.json> <dossiers/<S>/STATUT.md>   # exit 1 if one is missing

Review finding 22 (PR #3, S-1835): the telecom addendum T-01 was in the Drive inventory but not in the takeoff
inputs, and nothing flagged it. Rule enforced here:
  - an addendum PDF of the inventory (file name contains "addend") counts as ingested when a row of the
    "## Entrées" table of STATUT.md has the same byte size (Drive adds " (2)" suffixes, sizes do not change);
  - otherwise it must be listed, with a reason, under a "## Addendas non intégrés" section of STATUT.md
    (one bullet per file, the file name in backticks);
  - an inventory sub-folder whose name contains "addend" was not listed file by file, so it must be declared too.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ADDENDUM_RE = re.compile(r"addend", re.IGNORECASE)
COPY_SUFFIX_RE = re.compile(r"\s*\(\d+\)(?=\.[^.]+$)")


def normalize(name: str) -> str:
    """Drop the ' (2)' copy suffix Drive adds before the extension, and surrounding blanks."""
    return COPY_SUFFIX_RE.sub("", name.strip()).strip()


def inventory_addenda(inventory: dict) -> list[dict]:
    """Addendum PDFs and addendum sub-folders of one Drive folder inventory."""
    out = []
    for f in inventory.get("fichiers", []):
        path = f.get("chemin", "")
        if not ADDENDUM_RE.search(path):
            continue
        if path.endswith("/") or "sous-dossier" in path:
            out.append({"name": path.split(" (sous-dossier")[0].strip(), "size": None, "folder": True})
        elif path.lower().endswith(".pdf"):
            out.append({"name": path, "size": int(f.get("octets") or 0), "folder": False})
    return out


def _section(text: str, title_re: str) -> list[str]:
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = re.match(title_re, line[3:].strip(), re.IGNORECASE) is not None
            continue
        if inside:
            lines.append(line)
    return lines


def status_input_sizes(status_md: str) -> set[int]:
    """Byte sizes of the rows of the '## Entrées' table (| file | bytes | sha256 |)."""
    sizes = set()
    for line in _section(status_md, r"entr[ée]es"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[1].isdigit():
            sizes.add(int(cells[1]))
    return sizes


def status_declared(status_md: str) -> set[str]:
    """Normalized names declared under '## Addendas non intégrés' (bullets with the name in backticks and a reason)."""
    out = set()
    for line in _section(status_md, r"addendas? non int[ée]gr[ée]s"):
        m = re.match(r"\s*[-*]\s*`([^`]+)`\s*[—:-]\s*\S", line)
        if m:
            out.add(normalize(m.group(1)))
    return out


def missing_addenda(inventory: dict, status_md: str) -> list[str]:
    sizes, declared = status_input_sizes(status_md), status_declared(status_md)
    missing = []
    for a in inventory_addenda(inventory):
        if not a["folder"] and a["size"] in sizes:
            continue
        if normalize(a["name"]) in declared:
            continue
        missing.append(a["name"])
    return missing


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("inventory", type=Path)
    p.add_argument("status", type=Path)
    a = p.parse_args(argv)
    miss = missing_addenda(json.loads(a.inventory.read_text(encoding="utf-8")), a.status.read_text(encoding="utf-8"))
    for m in miss:
        print(f"addendum neither ingested nor declared: {m}")
    if not miss:
        print("every addendum of the inventory is ingested or declared")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
