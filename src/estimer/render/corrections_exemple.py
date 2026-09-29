"""Corrections apportées au texte du relevé EXEMPLE (HR26-14) avant le rendu.

L'EXEMPLE sert de cible de format, mais il contient des erreurs qu'on ne veut pas reproduire. Chaque
correction est une règle nommée, appliquée de façon déterministe et journalisée (feuille, ligne, champ,
avant, après) pour que l'écart entre l'EXEMPLE et notre sortie soit entièrement expliqué :

  ESPACE-MOT-CHIFFRE    mot collé à un nombre : "note7" -> "note 7", "circuit15A" -> "circuit 15A"
  ESPACE-MOT-SIGLE      mot collé à un sigle : "lotA" -> "lot A", "panneauPS" -> "panneau PS"
  ESPACE-VIRGULE        virgule sans espace entre un mot et un nombre : "chauffages,24" -> "chauffages, 24"
  ESPACE-NORME          "NEMA5-20R" -> "NEMA 5-20R", "DEL5.5" -> "DEL 5.5"
  ESPACE-UNITES         "120V15A" -> "120V 15A"
  TRONCATURE            cellule coupée par "..." dans l'EXEMPLE : on termine le mot évident ("a confirme..."
                        -> "a confirmer") sinon on revient à la dernière proposition complète et on renvoie
                        aux notes de réserve (le texte perdu n'est pas inventé)
  PHRASE-DOUBLEE        phrase répétée à l'identique dans la même cellule : gardée une fois
  MODELE-VIDE           "Non renseigne" -> "MODELE NON INDIQUE" (même libellé que les autres lignes)
  SOURCE-FICTIVE        "Preuve du releve (voir audit)" renvoie à un audit absent : remplacé par la preuve
                        réelle (plan de la feuille, plage de repères)
  LEGENDE-R001          encadré "PLINTHE DE CHAUFFAGE [R-001]" vs bordereau "(hors legende - R-001)" : le
                        libellé du bordereau fait foi partout
"""
from __future__ import annotations

import re

MOT_CHIFFRE = re.compile(r"\b([A-Za-z][a-z]{2,})(\d)")
MOT_SIGLE = re.compile(r"\b([a-z]{3,})([A-Z](?:\d|[A-Z]?\b))")
VIRGULE = re.compile(r"([A-Za-z]),(\d)")
NORME = re.compile(r"\b(NEMA|DEL)(\d)")
UNITES = re.compile(r"(\d+V)(\d+A)\b")

TEXTE_RULES = (
    ("ESPACE-MOT-CHIFFRE", MOT_CHIFFRE, r"\1 \2"),
    ("ESPACE-MOT-SIGLE", MOT_SIGLE, r"\1 \2"),
    ("ESPACE-VIRGULE", VIRGULE, r"\1, \2"),
    ("ESPACE-NORME", NORME, r"\1 \2"),
    ("ESPACE-UNITES", UNITES, r"\1 \2"),
)

PLACEHOLDER_MODELE = "Non renseigne"
PLACEHOLDER_SOURCE = "Preuve du releve (voir audit)"
MODELE_NON_INDIQUE = "MODELE NON INDIQUE"
# fins de mot évidentes pour les coupures "..." (seulement quand le mot est certain)
FINS_EVIDENTES = {"a confirme": "a confirmer", "a confi": "a confirmer"}
RENVOI_NOTES = "(suite: notes de reserve source)"


def corriger_espaces(text: str) -> tuple[str, list[str]]:
    """Règles typographiques ; renvoie (texte corrigé, règles appliquées)."""
    rules = []
    for name, rx, rep in TEXTE_RULES:
        new = rx.sub(rep, text)
        if new != text:
            rules.append(name)
            text = new
    return text, rules


def _phrases(text: str) -> list[str]:
    return [p for p in re.split(r"(?<=[.;])\s+", text) if p]


def dedoubler(text: str) -> str:
    """Retire les phrases répétées à l'identique (même paragraphe), en gardant la première."""
    out = []
    for para in text.split("\n"):
        seen, keep = set(), []
        for p in _phrases(para):
            key = p.strip()
            if key in seen:
                continue
            seen.add(key)
            keep.append(p)
        out.append(" ".join(keep))
    return "\n".join(out)


def reparer_troncature(text: str) -> str:
    """Cellule finissant par '...' : mot évident complété, sinon retour à la dernière proposition complète."""
    lines = text.split("\n")
    last = lines[-1].rstrip()
    if not last.endswith("..."):
        return text
    body = last[:-3].rstrip()
    for cut, full in FINS_EVIDENTES.items():
        if body.endswith(cut):
            lines[-1] = body[: -len(cut)] + full + "."
            return "\n".join(lines)
    k = max(body.rfind("; "), body.rfind(". "), body.rfind(": "))
    head = body[:k + 1].rstrip(" ;:") if k > 0 else ""
    if head and not head.endswith("."):
        head += "."
    lines[-1] = (head + " " if head else "") + RENVOI_NOTES
    return "\n".join(lines)


def corriger_cellule(sheet: str, ident: str, champ: str, text: str, contexte: dict, journal: list) -> str:
    """Applique toutes les règles à une cellule et journalise chaque changement."""
    avant = text
    regles = []
    if champ == "modele" and text.strip() == PLACEHOLDER_MODELE:
        text = MODELE_NON_INDIQUE
        regles.append("MODELE-VIDE")
    if champ == "source" and text.strip() == PLACEHOLDER_SOURCE:
        n = contexte.get("n", 0)
        code = contexte.get("code", ident)
        plage = f"{code}-01 a {code}-{n:02d}" if n > 1 else f"{code}-01"
        text = f"Plan {sheet}: reperes {plage} (symboles de la legende du plan)"
        regles.append("SOURCE-FICTIVE")
    if "[R-001]" in text:
        text = text.replace("[R-001]", "(hors legende - R-001)")
        regles.append("LEGENDE-R001")
    if text.rstrip().endswith("..."):
        text = reparer_troncature(text)
        regles.append("TRONCATURE")
    d = dedoubler(text)
    if d != text:
        text = d
        regles.append("PHRASE-DOUBLEE")
    text, r = corriger_espaces(text)
    regles += r
    if regles:
        journal.append({"feuille": sheet, "ligne": ident, "champ": champ, "regles": regles,
                        "avant": avant, "apres": text})
    return text


def corriger_ligne(sheet: str, row: dict, champs, contexte: dict, journal: list) -> dict:
    ident = row.get("repere") or row.get("id", "")
    if row.get("portee") and "repere" not in row:
        ident = f"{ident}/{row['portee']}"
    out = dict(row)
    for k in champs:
        if out.get(k):
            out[k] = corriger_cellule(sheet, ident, k, out[k], contexte, journal)
    return out


def resume(journal: list) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in journal:
        for r in e["regles"]:
            out[r] = out.get(r, 0) + 1
    return dict(sorted(out.items()))
