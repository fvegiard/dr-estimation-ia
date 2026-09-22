"""
Sous-commande `inventaire` — dossier de PDF -> JSON (pages, format pt,
texte, disciplines détectées). Première étape du pipeline
(docs/pipeline-qpl.md §1 étape 1-2) : c'est l'empreinte de ce qu'on a
réellement reçu, et la matière première de tout le reste (« les étiquettes
sont lues comme mots avec leurs coordonnées »).

La détection de discipline se fait par un tableau **préfixe de nom de
fichier -> discipline**, explicite et modifiable (`--disciplines`), jamais
par un mot-clé cherché dans le texte du plan : un plan peut mentionner
« électricité » sans être un plan électrique.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pymupdf  # PyMuPDF — déjà utilisé dans tout le dépôt de référence

# Convention de préfixe de feuille couramment utilisée sur les jeux de plans
# québécois (ex. E4xx = Électricité). Ce n'est PAS une donnée de S-1857 :
# c'est une convention générique, à ajuster par --disciplines si le jeu de
# plans d'une autre soumission en utilise une autre.
DEFAULT_DISCIPLINES = {
    "E": "Électricité",
    "A": "Architecture",
    "M": "Mécanique",
    "S": "Structure",
    "C": "Civil",
    "P": "Plomberie",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_discipline(filename: str, table: dict[str, str]) -> str | None:
    """Discipline déduite du préfixe du nom de fichier, par position (les
    premières lettres), pas par recherche dans le texte du plan."""
    stem = Path(filename).stem
    prefix = "".join(ch for ch in stem if ch.isalpha())
    for code in sorted(table, key=len, reverse=True):
        if prefix.upper().startswith(code.upper()):
            return table[code]
    return None


def inventory_pdf(path: Path, disciplines: dict[str, str]) -> dict:
    doc = pymupdf.open(path)
    pages = []
    for index in range(doc.page_count):
        page = doc[index]
        rect = page.rect
        pages.append(
            {
                "page_index": index,
                "page_width_pt": rect.width,
                "page_height_pt": rect.height,
                "text": page.get_text(),
            }
        )
    doc.close()
    return {
        "fichier": path.name,
        "chemin": str(path),
        "sha256": _sha256(path),
        "taille_octets": path.stat().st_size,
        "n_pages": len(pages),
        "discipline": detect_discipline(path.name, disciplines),
        "pages": pages,
    }


def run_inventaire(folder: Path, disciplines: dict[str, str]) -> list[dict]:
    pdfs = sorted(folder.glob("*.pdf")) + sorted(folder.glob("**/*.pdf"))
    seen: set[Path] = set()
    result = []
    for pdf in pdfs:
        if pdf in seen:
            continue
        seen.add(pdf)
        result.append(inventory_pdf(pdf, disciplines))
    return result


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("dossier", type=Path, help="Dossier contenant les PDF à inventorier")
    sub.add_argument("--out", type=Path, required=True, help="JSON de sortie")
    sub.add_argument(
        "--disciplines",
        type=Path,
        help="JSON {préfixe: discipline} pour remplacer la convention par défaut",
    )
    sub.add_argument(
        "--sans-texte",
        action="store_true",
        help="N'écrit pas le texte des pages (fichier de sortie plus léger)",
    )


def run(args: argparse.Namespace) -> int:
    disciplines = DEFAULT_DISCIPLINES
    if args.disciplines:
        disciplines = json.loads(Path(args.disciplines).read_text(encoding="utf-8"))

    result = run_inventaire(args.dossier, disciplines)
    if args.sans_texte:
        for entry in result:
            for page in entry["pages"]:
                page.pop("text", None)

    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_pages = sum(e["n_pages"] for e in result)
    print(f"OK : {len(result)} PDF, {n_pages} pages -> {args.out}")
    return 0
