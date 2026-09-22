"""
Sous-commande `index` — PDF -> index des feuilles : numéro de feuille et
titre lus dans le cartouche **par position** (des zones en points PDF),
pas par une recherche de motif dans le texte brut de la page ; plus
échelle, révision et date quand ces champs sont configurés.

Chaque soumission a son propre gabarit de cartouche : la géométrie des
champs est donc un fichier de configuration (`--cartouche config.json`),
jamais codée en dur ici. `config/cartouche-s1857-electrique.json` est un
exemple RÉEL, mesuré sur `sources/plans/electrique/E405_Rev0.pdf` (mots
PyMuPDF de la bande x>=2050 pt déjà isolée par
`verification/crosscheck_text.py`) — pas inventé, mais propre à ce gabarit
de plans ; à re-mesurer pour toute autre soumission.

Schéma de la configuration :
{
  "page_width_pt": 2383.92, "page_height_pt": 1683.72,   # informatif
  "fields": [
    {"name": "numero", "type": "text", "bbox": [x0, y0, x1, y1]},
    {"name": "titre",  "type": "text", "bbox": [...]},
    {"name": "echelle","type": "text", "bbox": [...]}       # optionnel
    {"name": "revisions", "type": "table", "bbox": [...],
     "columns": [{"name": "indice", "x0":.., "x1":..},
                 {"name": "description", "x0":.., "x1":..},
                 {"name": "date", "x0":.., "x1":..}]}
  ]
}
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymupdf


def _overlaps(word_bbox: tuple[float, float, float, float], field_bbox: list[float]) -> bool:
    wx0, wy0, wx1, wy1 = word_bbox
    fx0, fy0, fx1, fy1 = field_bbox
    return wx0 < fx1 and wx1 > fx0 and wy0 < fy1 and wy1 > fy0


def extract_text_field(words: list, bbox: list[float]) -> str:
    """Mots dont la boîte croise `bbox`, triés haut-bas puis gauche-droite —
    lecture par position, jamais par expression régulière sur le texte."""
    hits = [w for w in words if _overlaps(w[:4], bbox)]
    hits.sort(key=lambda w: (round(w[1]), w[0]))
    return " ".join(w[4] for w in hits)


def extract_table_field(words: list, bbox: list[float], columns: list[dict], y_tol: float = 4.0) -> list[dict]:
    """Regroupe les mots de `bbox` en lignes (tolérance `y_tol` sur y0), puis
    répartit chaque ligne dans les colonnes par intervalle de x0 — la même
    logique de position que `extract_text_field`, appliquée par colonne."""
    hits = [w for w in words if _overlaps(w[:4], bbox)]
    rows: dict[float, list] = {}
    for w in hits:
        key = round(w[1] / y_tol)
        rows.setdefault(key, []).append(w)

    result = []
    for key in sorted(rows):
        row_words = sorted(rows[key], key=lambda w: w[0])
        row = {}
        for col in columns:
            texts = [w[4] for w in row_words if col["x0"] <= w[0] < col["x1"]]
            row[col["name"]] = " ".join(texts)
        result.append(row)
    return result


def index_page(page, config: dict) -> dict:
    words = page.get_text("words")
    out: dict = {}
    for field in config.get("fields", []):
        name = field["name"]
        if field["type"] == "text":
            out[name] = extract_text_field(words, field["bbox"]) or None
        elif field["type"] == "table":
            out[name] = extract_table_field(words, field["bbox"], field["columns"])
        else:
            raise ValueError(f"Type de champ inconnu : {field['type']!r}")

    # Confort : si un champ table nommé "revisions" existe, exposer aussi la
    # révision la plus récente à plat (première ligne du tableau, PIPELINE
    # §1 étape 1 : « indice 1 SOUMISSION 2026-08-17 » est bien la 1re ligne).
    revisions = out.get("revisions")
    if isinstance(revisions, list) and revisions:
        out["revision_indice"] = revisions[0].get("indice")
        out["revision_date"] = revisions[0].get("date")
    return out


def run_index(pdf_path: Path, config: dict, pages: list[int] | None) -> list[dict]:
    doc = pymupdf.open(pdf_path)
    indices = pages if pages is not None else list(range(doc.page_count))
    result = []
    for page_index in indices:
        page = doc[page_index]
        entry = {"pdf": str(pdf_path), "page_index": page_index}
        entry.update(index_page(page, config))
        result.append(entry)
    doc.close()
    return result


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("pdf", type=Path, help="Fichier PDF (une feuille par page)")
    sub.add_argument("--cartouche", type=Path, required=True, help="JSON de géométrie du cartouche")
    sub.add_argument("--out", type=Path, required=True, help="JSON de sortie")
    sub.add_argument("--pages", type=str, help="Pages à traiter, ex. '0,2-4' (défaut : toutes)")


def _parse_pages(spec: str) -> list[int]:
    result: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            result.extend(range(int(start), int(end) + 1))
        elif part:
            result.append(int(part))
    return result


def run(args: argparse.Namespace) -> int:
    config = json.loads(Path(args.cartouche).read_text(encoding="utf-8"))
    pages = _parse_pages(args.pages) if args.pages else None
    result = run_index(args.pdf, config, pages)
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK : {len(result)} feuille(s) indexée(s) -> {args.out}")
    return 0
