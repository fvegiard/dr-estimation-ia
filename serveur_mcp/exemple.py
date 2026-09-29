"""Pont relevé → format EXEMPLE (HR26-14), par la chaîne commune `src.estimer.render.from_releve`.

Le relevé écrit par le LLM dans le dossier de travail (feuilles.csv, feuilles-classement.csv, nomenclature.csv,
occurrences-*.csv, reserves.md, feuilles/<F>.pdf) est converti par `from_releve.build` — le même pont que la chaîne
de Claude (ancrage des pastilles sur le symbole vectoriel, repères I/M, format materiel/agrege/travaux, réserves par
feuille) — puis rendu : page de plan avec pastilles + encadré « RELEVE <feuille> - MATERIEL », puis
« BORDEREAU MATERIEL - <feuille> » (8 colonnes) et « RESERVES ET COMPLEMENTS ».
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))


def rendre(travail: Path, sortie: Path, nom: str, ancrage: bool = True) -> dict:
    """Relevé → <nom>-RELEVE.pdf au format de l'exemplaire. Retourne le rapport du rendu."""
    from src.estimer.render import load_input, render
    from src.estimer.render.from_releve import build

    entree = sortie / "format-exemple"
    res = build(travail, entree, ancrage=ancrage)
    if not res.get("reperes"):
        raise ValueError("aucune occurrence valide à rendre")
    rapport = render(load_input(entree), entree / "plans.pdf", sortie / f"{nom}-RELEVE.pdf", log=lambda *_: None)
    rapport["reperes"] = res["reperes"]
    rapport["pont"] = {k: v for k, v in res.items() if isinstance(v, (int, float, str, list, dict))}
    (entree / "rapport-rendu.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=1, default=str),
                                               encoding="utf-8")
    return rapport
