"""Rule-based categoriser for Plan Expert labels — no LLM, deterministic.

`compare_qpl` matches marks by position, not by label; the learnt dictionary
(`apprentissage/qpl-2021-2026/dictionnaire-symboles.json`, 664 real .qpl) shows the
AI writes descriptive labels ("Prise double 5-15R", "A1 Troffer 2x4") while the
estimator writes short French codes with prefixes ("ADD PRISE", "FIXTURE ENLEVER").
Raw label agreement between the two is therefore near 0 %, even on well-matched marks.

`categoriser(label)` maps ANY label — AI or human, French or English, with prefixes
like ADD/NEW/DEMO/ENLEVER/RELO — to one of the dictionary's categories (dispositif,
luminaire, securite_incendie, telecom_donnees, chauffage, distribution,
mecanique_moteur, autre, or "indetermine" when nothing matches), plus demolition and
relocation flags. It never changes the position-based matching or the default
recall/precision metric; it is a secondary, informative signal (label-agreement by
category instead of by exact label).

Method: keyword rules built from the dictionary's `label`/`sous_type`/`variantes`
(weighted by `occurrences`, so a frequent meaning wins a keyword shared by two
categories, e.g. EXIT), plus a small hand-written table of English/domain synonyms
the AI uses that the French corpus does not (troffer, receptacle, breaker, …).
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DICTIONNAIRE_JSON = RACINE / "apprentissage" / "qpl-2021-2026" / "dictionnaire-symboles.json"

CATEGORIES = (
    "dispositif", "luminaire", "securite_incendie", "telecom_donnees",
    "chauffage", "distribution", "mecanique_moteur", "autre",
)
INDETERMINE = "indetermine"

# Filler words found in the dictionary's `sous_type` free-text descriptions —
# never category-indicative, dropped before building keywords from that field.
_MOTS_VIDES = {
    "DE", "DU", "DES", "LA", "LE", "LES", "UN", "UNE", "ET", "OU", "A", "AU", "EN",
    "AVEC", "SANS", "SELON", "NON", "PRECISE", "PRECISEE", "PROBABLE", "INCERTAIN",
    "INCERTAINE", "AMBIGUE", "AMBIGU", "ABREVIATION", "ABREGE", "ABREGEE", "RESOLUE",
    "RESOLU", "LETTRE", "SEULE", "SEUL", "ISOLEE", "ISOLE", "GENERIQUE", "GENERALE",
    "GENERAL", "TYPE", "VARIANTE", "SIGNIFICATION", "INCONNUE", "SENS", "REPERE",
    "FONCTION", "CODE", "CHIFFRES", "CATALOGUE", "FORME", "NUMEROTATION", "FAMILLE",
    "SIGLE", "SIGNIFICATIONS", "AMBIGUS", "PROBABLEMENT", "NUMERO", "NUMERIQUE",
    "IDENTIFIEE", "INCERTAINS", "ELECTRIQUE", "ELECTRIQUES", "VOIR", "PEUT", "ETRE",
    "NOTE", "NOTES", "REFERENCE", "VARIANTES", "APPAREIL", "APPAREILS", "NON_PRECISE",
    # generic qualifiers: real, but not category-indicative on their own —
    # dropping them keeps the head word ("PRISE" in "PRISE DOUBLE") decisive.
    "DOUBLE", "SIMPLE", "UNIT", "UNITE", "COMBO", "STANDARD", "GENERIC", "POINT",
    "TETE", "TETES",
}

# Modifiers/tags that appear in real labels (AI or human) but are never
# category-indicative on their own — a demolition/revision/relocation marker,
# or a bare letter used as a revision tag (A/B/C/D…). Excluded from the
# keyword table built from the dictionary so they cannot mis-categorise.
_MODIFICATEURS = {
    "ADD", "NEW", "EXIST", "EXISTANT", "EXISTANTE", "DEMO", "DEMOLI", "ENL",
    "ENLEVER", "ENLEVE", "ENLEVEE", "RELO", "RELOC", "RELOCALISE", "RELOCALISEE",
    "RELOCATE", "RELOCATED", "REMOVE", "REMOVED", "TO", "WP",
}

# Hand-written synonyms — mostly the English/descriptive vocabulary an AI
# vision agent uses that the (mostly French, code-style) 2021-2026 corpus
# does not contain in `label`/`sous_type`/`variantes`. Small weight: a
# dictionary-derived keyword with real `occurrences` always outranks these
# on conflict (e.g. EXIT, resolved from the corpus below).
_SYNONYMES: dict[str, tuple[str, int]] = {
    # dispositif
    "RECEPTACLE": ("dispositif", 50), "OUTLET": ("dispositif", 50),
    "DUPLEX": ("dispositif", 30), "SWITCH": ("dispositif", 30),
    "DIMMER": ("dispositif", 30), "OCCUPANCY": ("dispositif", 20),
    "SENSOR": ("dispositif", 10),
    # luminaire
    "LIGHT": ("luminaire", 30), "LIGHTING": ("luminaire", 30),
    "LAMP": ("luminaire", 20), "TROFFER": ("luminaire", 50),
    "FIXTURE": ("luminaire", 50), "DOWNLIGHT": ("luminaire", 30),
    "POTLIGHT": ("luminaire", 30), "SCONCE": ("luminaire", 30),
    "CANOPY": ("luminaire", 20), "WALLPACK": ("luminaire", 30),
    "HIGHBAY": ("luminaire", 30), "FLOODLIGHT": ("luminaire", 30),
    "POLE": ("luminaire", 15),
    # securite_incendie
    "SMOKE": ("securite_incendie", 40), "DETECTOR": ("securite_incendie", 30),
    "ALARM": ("securite_incendie", 30), "STROBE": ("securite_incendie", 30),
    "SPRINKLER": ("securite_incendie", 30), "FIRE": ("securite_incendie", 20),
    "EMERGENCY": ("securite_incendie", 15), "PULLSTATION": ("securite_incendie", 30),
    "ACCESS": ("securite_incendie", 10),
    # telecom_donnees
    "PHONE": ("telecom_donnees", 30), "DATA": ("telecom_donnees", 30),
    "SPEAKER": ("telecom_donnees", 30), "NETWORK": ("telecom_donnees", 20),
    "ETHERNET": ("telecom_donnees", 20), "COAX": ("telecom_donnees", 20),
    # chauffage
    "HEATER": ("chauffage", 30), "BASEBOARD": ("chauffage", 30),
    "HEATING": ("chauffage", 20), "RADIANT": ("chauffage", 20),
    # distribution
    "PANEL": ("distribution", 30), "BREAKER": ("distribution", 30),
    "JUNCTION": ("distribution", 20), "TRANSFORMER": ("distribution", 30),
    "GROUND": ("distribution", 15), "GROUNDING": ("distribution", 15),
    "SUBPANEL": ("distribution", 30),
    # mecanique_moteur
    "MOTOR": ("mecanique_moteur", 30), "FAN": ("mecanique_moteur", 20),
    "PUMP": ("mecanique_moteur", 30), "DISCONNECT": ("mecanique_moteur", 30),
    "CONTACTOR": ("mecanique_moteur", 20), "STARTER": ("mecanique_moteur", 20),
    "COMPRESSOR": ("mecanique_moteur", 20),
    # autre
    "RELAY": ("autre", 15), "CHARGER": ("autre", 15), "HUMIDIFIER": ("autre", 20),
}


def nettoyer(texte: str) -> str:
    """Uppercase, accents removed, non-alphanumerics collapsed to single spaces."""
    texte = unicodedata.normalize("NFKD", texte or "")
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = re.sub(r"[^A-Za-z0-9]+", " ", texte)
    return re.sub(r"\s+", " ", texte).strip().upper()


def _tokens(texte_nettoye: str) -> list[str]:
    return texte_nettoye.split()


def _utile(mot: str) -> bool:
    return len(mot) >= 2 and mot not in _MOTS_VIDES and mot not in _MODIFICATEURS and not mot.isdigit()


@lru_cache(maxsize=1)
def _table_mots_cles(path: Path = DICTIONNAIRE_JSON) -> dict[str, str]:
    """keyword -> category, resolved by summed `occurrences` when a keyword is
    shared by several categories (e.g. EXIT: securite_incendie and luminaire
    both use it — the more frequent meaning wins)."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    poids: dict[str, Counter] = {}

    def ajouter(mot: str, categorie: str, poids_mot: int) -> None:
        if _utile(mot):
            poids.setdefault(mot, Counter())[categorie] += poids_mot

    for entree in d["symboles"]:
        categorie = entree["categorie"]
        occ = max(1, int(entree.get("occurrences", 1)))
        if categorie == INDETERMINE:
            continue  # ambiguous by construction — no keyword derived from it
        for mot in _tokens(nettoyer(entree["label"])):
            ajouter(mot, categorie, occ)
        for variante in entree.get("variantes", []):
            for mot in _tokens(nettoyer(variante)):
                ajouter(mot, categorie, occ)
        # sous_type is free-text prose: weight it lightly, it is a description
        # of the label, not a label itself.
        for mot in _tokens(nettoyer(entree.get("sous_type", ""))):
            ajouter(mot, categorie, max(1, occ // 20))

    for mot, (categorie, poids_mot) in _SYNONYMES.items():
        poids.setdefault(mot, Counter())[categorie] += poids_mot

    return {mot: compte.most_common(1)[0][0] for mot, compte in poids.items()}


_DEMOLITION = re.compile(
    r"\b(DEMO|DEMOLI|ENLEVER|ENLEVE|ENLEVEE|ENL|REMOVE|REMOVED|A ENLEVER|TO REMOVE|"
    r"EXISTANT A ENLEVER)\b"
)
_RELOCATION = re.compile(r"\b(RELO|RELOC|RELOCALISE|RELOCALISEE|RELOCATE|RELOCATED|DEPLACE|DEPLACEE)\b")


@dataclass(frozen=True)
class Categorisation:
    categorie: str              # one of CATEGORIES, or "indetermine"
    demolition: bool
    relocation: bool
    mot_cle: str | None = None  # keyword that decided the category, for debugging


def categoriser(label: str) -> Categorisation:
    """Category + demolition/relocation flags for ANY label (AI or human,
    French or English, with ADD/DEMO/ENLEVER/RELO-style prefixes). Deterministic,
    keyword-based — no LLM, no dependency on how the two sides happened to word
    the same device."""
    nettoye = nettoyer(label)
    demolition = bool(_DEMOLITION.search(nettoye))
    relocation = bool(_RELOCATION.search(nettoye))
    table = _table_mots_cles()
    tokens = [t for t in _tokens(nettoye) if t not in _MODIFICATEURS]
    # 1) longest-token-first: prefer a specific match ("TROFFER") over a
    #    shorter one that might also appear ("A" in "A1").
    for mot in sorted(tokens, key=len, reverse=True):
        if mot in table:
            return Categorisation(table[mot], demolition, relocation, mot)
    return Categorisation(INDETERMINE, demolition, relocation, None)
