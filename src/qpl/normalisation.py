"""Canonical Plan Expert labels, learnt from the 2021-2026 corpus (664 real .qpl).

Source: `apprentissage/qpl-2021-2026/normalisation.json`
  - `fusion`: variant -> canonical label (87 entries, may chain: A -> B -> C),
  - `rebut`:  noise labels (bare numbers, "COMPTEUR n") that carry no device.

`canonique(label)` -> uppercase, accents removed, whitespace collapsed, fusion applied
transitively; returns None for a noise label. Lossy by design (e.g. PRISE GFI -> PRISE):
use it to compare or group, never to overwrite what the estimator must price.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
NORMALISATION_JSON = RACINE / "apprentissage" / "qpl-2021-2026" / "normalisation.json"
DICTIONNAIRE_JSON = RACINE / "apprentissage" / "qpl-2021-2026" / "dictionnaire-symboles.json"


def nettoyer(label: str) -> str:
    """Uppercase, no accents, single spaces, trimmed."""
    texte = unicodedata.normalize("NFKD", label or "")
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texte).strip().upper()


class Normaliseur:
    def __init__(self, fusion: dict[str, str], rebut: list[str] | set[str]):
        self.fusion = {nettoyer(k): nettoyer(v) for k, v in fusion.items()}
        self.rebut = {nettoyer(r) for r in rebut}

    @classmethod
    def depuis_fichier(cls, path: Path = NORMALISATION_JSON) -> "Normaliseur":
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(d.get("fusion", {}), d.get("rebut", []))

    def canonique(self, label: str) -> str | None:
        """Canonical label, or None if the label is noise (or empty)."""
        t = nettoyer(label)
        vus: set[str] = set()
        while t in self.fusion and t not in vus:   # transitive, cycle-safe
            vus.add(t)
            t = self.fusion[t]
        if not t or t in self.rebut:
            return None
        return t

    def est_rebut(self, label: str) -> bool:
        return self.canonique(label) is None


@lru_cache(maxsize=1)
def normaliseur_defaut() -> Normaliseur:
    return Normaliseur.depuis_fichier()


def canonique(label: str) -> str | None:
    return normaliseur_defaut().canonique(label)
