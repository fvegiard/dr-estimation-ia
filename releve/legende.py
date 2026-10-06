"""Légende et devis : vocabulaire des codes de famille et extraction des articles de devis.

Deux besoins du relevé (correctif E08 du 2026-10-05) :

1. **Code de famille tiré de la légende.** Le code court d'une famille (`CT`, `CG`, `GF`, `CP`…) se déduit de la
   DESCRIPTION de la ligne de légende du plan (ou de la légende générale du lot), jamais d'une invention de
   l'agent. `code_attendu(description)` applique le vocabulaire de `apprentissage/hr26-14-exemplaire/
   STANDARD-RELEVE.md` §6 (codes seulement, aucune quantité) ; `""` = pas de code connu, l'agent en choisit
   un court et le justifie. Le contrôle `Q14` de `controle_qualite.py` bloque un code qui contredit ce vocabulaire.
2. **Modèle et prescription tirés du devis.** `articles_devis(page)` découpe une feuille de devis à couche texte
   en articles (section numérotée en gras, texte, ligne « MARQUE SPÉCIFIÉE : … ») ; `prepare.py` les écrit dans
   `devis/<feuille>-articles.csv` pour que l'agent remplisse `modele`/`prescription` avec la référence section.

Rien ici n'est propre à un dossier : règles de vocabulaire et de mise en page de devis seulement.
"""
from __future__ import annotations

import re
import unicodedata

# Ordre = priorité : le plus spécifique d'abord (une prise de comptoir DDFT est d'abord « comptoir DDFT »,
# pas « comptoir » ni « DDFT »). Motifs appliqués à la description normalisée (ASCII majuscules).
_DDFT = r"(DDFT|GFI|GFCI|DIFFERENTIEL)"
VOCABULAIRE: tuple[tuple[str, str], ...] = (
    ("CG", rf"PRISE.*COMPTOIR.*{_DDFT}|PRISE.*{_DDFT}.*COMPTOIR"),
    ("CT", r"PRISE.*COMPTOIR"),
    ("GF", rf"PRISE.*{_DDFT}"),
    ("CP", r"PRISE.*CUISINIERE"),
    ("SE", r"PRISE.*(SECHEUSE|SIMPLE 30 ?A)"),
    ("PC", r"PRISE.*DOUBLE 15 ?A(?!/)"),
    ("RA", r"RACCORD(EMENT)? DIRECT"),
    ("BJ", r"BOITE DE JONCTION"),
    ("EV", r"EVACUA(TEUR|TION)"),
    ("CU", r"COMMUTATEUR UNIPOLAIRE(?!.*3 VOIES)"),
    ("TE", r"(SORTIE|PLAQUE)( DE SERVICE)?.*TELEPHON"),
    ("TV", r"CABLO"),
    ("IC", r"INTERCOM"),
    ("AF", r"AVERTISSEUR (D.INCENDIE |DE )?FUMEE"),
    ("TH", r"THERMOSTAT"),
    ("PL", r"PLINTHE"),
    ("PN", r"PANNEAU.*LOGEMENT"),
)
_LUMINAIRE = re.compile(r"(LUMINAIRE|APPAREIL D.ECLAIRAGE|FIXT(URE)?)\b.*\bTYPE ([A-Z][0-9]?)\b")


def normaliser(texte: str) -> str:
    """ASCII majuscules, espaces simples, « 15 A » → « 15A » (la légende écrit les deux)."""
    t = unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode().upper()
    t = re.sub(r"[’'`]", "'", t)
    t = re.sub(r"(\d)\s+A\b", r"\1A", t)
    return re.sub(r"\s+", " ", t).strip()


# Vocabulaire des appareils EXISTANTS des feuilles agrégées de vues en plan (STANDARD-RELEVE.md §6 ; gold HR26-14
# E09 p.64 : CH 36, I 14, PC 20, T 28, M03 2, M05 3). Admis en plus du code de la légende quand la famille est un
# existant (portée REMPLACER ou CONSERVER) ; tout autre existant prend un numéro de la série M (M01, M02…).
VOCABULAIRE_EXISTANT: tuple[tuple[str, str], ...] = (
    ("CH", r"CHAUFF|PLINTHE|CONVECTEUR"),
    ("I", r"COMMUTATEUR"),
    ("PC", r"PRISE.*DOUBLE"),
    ("T", r"THERMOSTAT"),
)


def code_existant_admis(code: str, description: str) -> bool:
    """Vrai si `code` est un code d'appareil existant valable pour cette description (CH, I, PC, T, ou série M)."""
    if re.fullmatch(r"M\d{2}", code):
        return True
    t = normaliser(description)
    return any(code == c and re.search(motif, t) for c, motif in VOCABULAIRE_EXISTANT)


def code_attendu(description: str) -> str:
    """Code de famille du vocabulaire pour une description de légende, ou "" si aucun ne s'applique."""
    t = normaliser(description)
    if not t:
        return ""
    m = _LUMINAIRE.search(t)
    if m:
        return "L" + m.group(3)
    for code, motif in VOCABULAIRE:
        if re.search(motif, t):
            return code
    return ""


def variante_puissance(a: str, b: str) -> bool:
    """Vrai si deux libellés ne diffèrent que par une puissance (« PLINTHE 300W » / « PLINTHE 1500W »)."""
    pa = re.sub(r"\b\d+([.,]\d+)?\s*K?W\b", "#W", normaliser(a))
    pb = re.sub(r"\b\d+([.,]\d+)?\s*K?W\b", "#W", normaliser(b))
    return pa == pb and normaliser(a) != normaliser(b) and "#W" in pa


# --- devis -----------------------------------------------------------------------------------------------
_SECTION = re.compile(r"^(\d{1,2})\.(?!\d)\s*([^\W\d_].*)$")
_MARQUE = re.compile(r"^MARQUE SP[EÉ]CIFI[EÉ]E\s*:?\s*(.*)$", re.I)
_MODELE_MOT = re.compile(r"\b(MOD[EÈÉ]LE|S[EÉ]RIE|CATALOGUE)\s*:?\s*", re.I)


def _lignes(page) -> list[dict]:
    """Lignes de texte d'une page pymupdf : x0, y0, x1, y1, texte, gras."""
    out = []
    for b in page.get_text("dict").get("blocks", []):
        for ln in b.get("lines", []):
            spans = [s for s in ln.get("spans", []) if s.get("text", "").strip()]
            if not spans:
                continue
            gras = all("bold" in s.get("font", "").lower() or (s.get("flags", 0) & 16) for s in spans)
            out.append({"x0": ln["bbox"][0], "y0": ln["bbox"][1], "x1": ln["bbox"][2], "y1": ln["bbox"][3],
                        "texte": " ".join(s["text"].strip() for s in spans), "gras": gras})
    return out


def _colonnes(lignes: list[dict], ecart: float = 150.0) -> list[float]:
    """Débuts de colonnes : x0 des lignes regroupés (un saut > `ecart` pt ouvre une colonne)."""
    xs = sorted(l["x0"] for l in lignes)
    cols: list[float] = []
    for x in xs:
        if not cols or x - cols[-1] > ecart:
            cols.append(x)
    return cols


def articles_devis(page) -> list[dict]:
    """Découpe une feuille de devis en articles : une ligne par article fermé par « MARQUE SPÉCIFIÉE »
    (ou par la fin de section). Champs : section, titre, article, texte, marque, modele, x_pt, y_pt."""
    lignes = _lignes(page)
    if not lignes:
        return []
    cols = _colonnes(lignes)

    def col(l):
        return max(i for i, c in enumerate(cols) if c <= l["x0"] + 1)

    # titres de section en gras « 10. » + « THERMOSTATS » sur la même ligne : on les fusionne
    lignes.sort(key=lambda l: (col(l), round(l["y0"]), l["x0"]))
    fusion: list[dict] = []
    for l in lignes:
        p = fusion[-1] if fusion else None
        if p and p["gras"] and l["gras"] and col(p) == col(l) and abs(p["y0"] - l["y0"]) < 2 and re.fullmatch(r"\d{1,2}\.", p["texte"]):
            p["texte"] += " " + l["texte"]; p["x1"] = l["x1"]
            continue
        fusion.append(dict(l))
    arts, section, titre, buf, n, partie = [], "", "", [], 0, 1

    def fermer(marque=""):
        nonlocal buf, n
        if not section or not (buf or marque):
            buf = []
            return
        n += 1
        modele = _MODELE_MOT.sub("", re.sub(r"\s*,\s*", " ", marque)).strip(" .")
        arts.append({"partie": partie, "section": section, "titre": titre, "article": f"{section}.{n}",
                     "texte": " ".join(b["texte"] for b in buf), "marque": marque.strip(), "modele": modele,
                     "x_pt": f"{(buf or [{'x0': 0}])[0]['x0']:.1f}", "y_pt": f"{(buf or [{'y0': 0}])[0]['y0']:.1f}"})
        buf = []

    for l in fusion:
        m = _SECTION.match(l["texte"]) if l["gras"] else None
        if m:
            fermer()
            if section and int(m.group(1)) < int(section):     # la numérotation repart : nouvelle partie du devis
                partie += 1
            section, titre, n = m.group(1), m.group(2).strip(" :"), 0
            continue
        mm = _MARQUE.match(l["texte"])
        if mm and mm.group(1).strip():
            fermer(mm.group(1))
            continue
        if section:
            buf.append(l)
    fermer()
    return arts


MARQUE_RE = re.compile(r"MARQUE SP[EÉ]CIFI[EÉ]E\s*:", re.I)


def est_devis(titre: str, nb_mots: int) -> bool:
    """Feuille de devis : « DEVIS » au cartouche et beaucoup de texte (un plan qui porte quelques notes
    « MARQUE SPÉCIFIÉE » reste un plan à relever ; ses articles sont extraits quand même)."""
    return "DEVIS" in normaliser(titre) and nb_mots > 800


def est_legende(titre: str) -> bool:
    """Feuille de légende générale : « LÉGENDE(S) » au cartouche (le reste du texte peut être vectorisé)."""
    return "LEGENDE" in normaliser(titre)
