"""Fuzzy FR/EN product search over EEWin's abbreviated descriptions.

Descriptions look like "BOITE FS 1G 1/2PO METAL" or "SOCK ET" (split words), so matching
is done on a compact form (uppercase, no accents, no spaces) with synonym groups.
"""
from __future__ import annotations

import re
import unicodedata

SYNONYMS = [
    ["RECEPT", "PRISE", "RECEPTACLE", "OUTLET"],
    ["BOX", "BOITE", "BTE"],
    ["SWITCH", "INTERR", "INTERRUPTEUR", "INT"],
    ["BREAKER", "DISJ", "DISJONCTEUR", "BRKR", "CB"],
    ["PLATE", "PLAQUE", "COVER", "COUVERCLE"],
    ["EMT", "TMEC"],
    ["RIGID", "GRC", "RIGIDE"],
    ["WIRE", "FIL"],
    ["FIXTURE", "LUMIN", "LUMINAIRE", "LIGHT", "FIXT"],
    ["CONNECTOR", "CONNECTEUR", "CONN", "CONNECT"],
    ["COUPLING", "COUPLER", "COUPL", "MANCHON"],
    ["STRAP", "SANGLE", "COLLIER", "CLAMP"],
    ["ALUMINUM", "ALUM", "ALU"],
    ["COPPER", "CUIVRE", "CU"],
    ["GROUND", "MALT", "GRD", "GND"],
    ["PANEL", "PANNEAU", "PANELBOARD"],
    ["TRANSFORMER", "TRANSFO", "XFMR"],
    ["DISCONNECT", "SECTIONNEUR", "SECT"],
    ["THERMOSTAT", "THERMO"],
    ["HEATER", "PLINTHE", "CONVECTEUR", "CHAUFFERETTE"],
    ["DETECTOR", "DETECTEUR", "DETECT"],
    ["SMOKE", "FUMEE"],
    ["ARMORED", "ARMOURED", "ARME", "BX", "AC90", "ACWU"],
    ["WEATHERPROOF", "WP", "ETANCHE"],
    ["GANG", "G"],
    ["INCH", "PO", "IN"],
    ["FOOT", "PI", "FT"],
    ["STEEL", "ACIER", "STL"],
    ["STAINLESS", "SS", "INOX"],
    ["WHITE", "BLANC", "WH", "WHT"],
    ["IVORY", "IVOIRE", "IV"],
    ["BLACK", "NOIR", "BK", "BLK"],
    ["GREY", "GRAY", "GRIS", "GY"],
]
_SYN = {}
for group in SYNONYMS:
    for w in group:
        _SYN.setdefault(w, set()).update(group)


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def compact(s: str) -> str:
    """Uppercase, no accents, no spaces/punctuation except / . (keeps 1/2, 3.5)."""
    s = strip_accents(s or "").upper().replace("''", '"').replace('"', "PO")
    return re.sub(r"[^A-Z0-9/.]", "", s)


def words(s: str) -> str:
    """Space-delimited uppercase tokens with a leading/trailing space, for whole-token matching."""
    s = strip_accents(s or "").upper().replace("''", '"').replace('"', "PO")
    return " " + " ".join(re.sub(r"[^A-Z0-9/.]", " ", s).split()) + " "


def is_token_alt(alt: str) -> bool:
    """Short or numeric alternatives must match at a token start, not anywhere."""
    return len(alt) < 3 or any(ch.isdigit() for ch in alt)


def where_score(query: str, compact_col: str = "search_text", words_col: str = "search_words"):
    """SQL score expression (number of matched query terms) + params, SQLite/Postgres-compatible LIKE."""
    parts, params = [], []
    for alts in terms(query):
        conds = []
        for a in alts:
            if is_token_alt(a):
                conds.append(f"{words_col} LIKE ?"); params.append(f"% {a}%")
            else:
                conds.append(f"{compact_col} LIKE ?"); params.append(f"%{a}%")
        parts.append("(CASE WHEN " + " OR ".join(conds) + " THEN 1 ELSE 0 END)")
    return (" + ".join(parts) or "0"), params, len(parts)


def terms(query: str) -> list[list[str]]:
    """Each query word -> list of alternatives (synonyms), all compacted."""
    words = re.findall(r"[0-9]+/[0-9]+|[0-9]+(?:\.[0-9]+)?[A-Za-z\"']*|[A-Za-zÀ-ÿ]+", query)
    out = []
    for w in words:
        c = compact(w)
        if not c:
            continue
        alts = {c}
        m = re.fullmatch(r"([0-9/.]+)([A-Z]+)", c)
        if m:  # "30A", "1/2PO", "12AWG": keep number+unit, and swap unit synonyms
            num, unit = m.groups()
            alts |= {num + s for s in _SYN.get(unit, ())}
        alts |= _SYN.get(c, set())
        g = re.fullmatch(r"(18|16|14|12|10|8|6|4|3|2)/([2-4])", c)
        if g:  # cable "14/2" is written "14AWG 2C" in the catalog
            alts |= {g.group(1) + "AWG"}
        out.append(sorted(alts, key=len, reverse=True))
    return out
