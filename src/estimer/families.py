"""Family taxonomy and label -> family mapping.

Families are the categories of the 2021-2026 Plan Expert dictionary
(`src.qpl.categorie.CATEGORIES`). A label is mapped by, in order:

1. the keyword categoriser (`src.qpl.categorie.categoriser`, built from the
   664-project corpus dictionary, not from any single dossier);
2. a `LabelFamilyMap` learnt from data: for labels the keyword rules cannot
   place (e.g. "KS", "AF1-5"), the family voted by co-located marks whose
   label *is* categorisable (position matches between the estimator's and
   another takeoff of the same sheet), kept only with a clear majority;
3. otherwise "indetermine".
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from src.qpl.categorie import CATEGORIES, INDETERMINE, categoriser, nettoyer

FAMILIES: tuple[str, ...] = CATEGORIES + (INDETERMINE,)

# Short, estimator-style Counter names used when the estimator writes a
# family-level count (Dupuis names counters in upper-case French).
FAMILY_COUNTER_NAME = {
    "dispositif": "DISPOSITIF",
    "luminaire": "LUMINAIRE",
    "securite_incendie": "ALARME INCENDIE",
    "telecom_donnees": "TELECOM",
    "chauffage": "CHAUFFAGE",
    "distribution": "DISTRIBUTION",
    "mecanique_moteur": "RACCORDEMENT MECANIQUE",
    "autre": "AUTRE",
    INDETERMINE: "A CLASSER",
}

MIN_VOTES = 3
MIN_SHARE = 0.6


def keyword_family(label: str) -> str:
    return categoriser(label).categorie


@dataclass
class LabelFamilyMap:
    """label (normalised) -> family, learnt from co-location votes."""
    votes: dict[str, Counter] = field(default_factory=lambda: defaultdict(Counter))

    def add_vote(self, label: str, family: str, n: int = 1) -> None:
        if family and family != INDETERMINE:
            self.votes[nettoyer(label)][family] += n

    def learnt(self, label: str) -> str | None:
        c = self.votes.get(nettoyer(label))
        if not c:
            return None
        fam, n = c.most_common(1)[0]
        total = sum(c.values())
        if n >= MIN_VOTES and n / total >= MIN_SHARE:
            return fam
        return None

    def family(self, label: str) -> str:
        fam = keyword_family(label)
        if fam != INDETERMINE:
            return fam
        return self.learnt(label) or INDETERMINE

    def merge(self, other: "LabelFamilyMap") -> None:
        for k, c in other.votes.items():
            self.votes[k].update(c)

    def to_json(self) -> dict:
        return {k: dict(v) for k, v in sorted(self.votes.items())}

    @classmethod
    def from_json(cls, data: dict) -> "LabelFamilyMap":
        m = cls()
        for k, v in data.items():
            m.votes[k] = Counter(v)
        return m

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), ensure_ascii=False, indent=1), encoding="utf-8")
