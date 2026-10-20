"""Extrait 25 pages originales distinctes sans modifier les dossiers de référence."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

import pymupdf

RACINE = Path(__file__).resolve().parents[1]
BASE = RACINE / "travail-mcp" / "campagne-25-plans"


def empreinte(chemin: Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> None:
    sources = [
        ("BOURASSA", Path("G:/Mon disque/D-claude-non-public-20260923/"
                         "dr-electrique-soumissions-2026/S-1645 ANNEXE-BOURASSA/"
                         "25084_Plans_Electrique.pdf"), range(3, 24)),
        ("MIL", RACINE / "travail-mcp/S-1842-MIL-25KV/entree/"
         "S-1842-MIL-25Kv-3pages.pdf", range(1, 4)),
        ("SUNLIFE", RACINE / "travail-mcp/S-1644-SUNLIFE/entree/"
         "S-1644-ELEC-page5.pdf", range(1, 2)),
    ]
    BASE.mkdir(parents=True, exist_ok=True)
    if (BASE / "manifest.json").exists():
        raise FileExistsError("Campagne existante : utiliser son manifeste, sans l'écraser.")
    (BASE / "sources").mkdir()
    (BASE / "apercus-sources").mkdir()
    (BASE / "preuves").mkdir()
    bibliotheque = RACINE / "releve/bibliotheque-blocs.csv"
    shutil.copy2(bibliotheque, BASE / "bibliotheque-blocs.csv")
    cas = []
    for projet, source, pages in sources:
        sha = empreinte(source)
        with pymupdf.open(source) as document:
            for numero in pages:
                page = document[numero - 1]
                texte = str(page.get_text())
                codes = re.findall(r"\bE-?\d{3}[A-Z]?\b", texte[-1800:])
                feuille = codes[-1] if codes else f"page-{numero}"
                identifiant = f"P{len(cas) + 1:02d}-{projet}-{feuille}"
                cible = BASE / "sources" / f"{identifiant}.pdf"
                with pymupdf.open() as extrait:
                    extrait.insert_pdf(document, from_page=numero - 1, to_page=numero - 1)
                    extrait.save(cible, deflate=True)
                page.get_pixmap(matrix=pymupdf.Matrix(1600 / page.rect.width,
                                                     1600 / page.rect.width)).save(
                    BASE / "apercus-sources" / f"{identifiant}.png")
                cas.append({
                    "id": identifiant, "projet": projet, "feuille": feuille,
                    "source": str(source.resolve()), "page_source": numero,
                    "source_sha256": sha, "extrait": str(cible),
                    "extrait_sha256": empreinte(cible), "caracteres_texte": len(texte),
                    "traces_vectoriels": len(page.get_drawings()),
                    "cartouche_texte": texte[-500:],
                    "source_statut": "Extrait original candidat; contrôle visuel requis",
                })
    if len(cas) != 25 or len({c["extrait_sha256"] for c in cas}) != 25:
        raise ValueError("Il faut exactement 25 extraits distincts.")
    manifeste = {"bibliotheque_sha256": empreinte(bibliotheque), "cas": cas}
    (BASE / "manifest.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps([{k: c[k] for k in ("id", "traces_vectoriels", "caracteres_texte")}
                      for c in cas], ensure_ascii=False))


if __name__ == "__main__":
    main()
