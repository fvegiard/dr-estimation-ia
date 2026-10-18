"""Fonctions partagées du pipeline de relevé (lecture des CSV de travail, palette, dessin des formes)."""
from __future__ import annotations
import csv, os, re, hashlib

# Enum Plan Expert (lu dans PlanExpert.exe, QuoterPlan.DrawCounter+CounterShapeTypeEnum) :
CIRCLE, SQUARE, DIAMOND, TRI, TRI_REV, TRAP, TRAP_REV = 0, 1, 2, 3, 4, 5, 6
FORMES = {"cercle": CIRCLE, "carre": SQUARE, "carré": SQUARE, "losange": DIAMOND, "triangle": TRI,
          "triangle_inverse": TRI_REV, "trapeze": TRAP, "trapeze_inverse": TRAP_REV}

# Palette par défaut par famille (alignée sur les pastilles de légende de M. Dupuis, verification/rules_dupuis.py)
PALETTE_FAMILLE = {
    "luminaire": (SQUARE, (238, 182, 53)), "commande": (CIRCLE, (53, 53, 221)), "secours": (CIRCLE, (164, 164, 164)),
    "prise": (CIRCLE, (222, 180, 53)), "alarme": (CIRCLE, (53, 153, 153)), "telecom": (TRI, (53, 53, 158)),
    "distribution": (SQUARE, (228, 53, 53)), "mecanique": (SQUARE, (162, 53, 53)), "chauffage": (SQUARE, (224, 53, 53)),
    "autre": (DIAMOND, (120, 120, 120)),
}
# écarts de teinte pour différencier les libellés d'une même famille
VARIANTES = [(0, 0, 0), (30, -40, 60), (-50, 30, -30), (60, 20, -60), (-30, -60, 40), (40, 60, 20), (-60, 0, 0), (0, -50, -50), (50, 50, 50), (-40, 40, 40)]

def argb(rgb):
    v = (0xFF << 24) | (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]
    return v - (1 << 32)

def parse_rgb(s: str):
    m = re.findall(r"\d+", s or "")
    return (int(m[0]), int(m[1]), int(m[2])) if len(m) >= 3 else None

def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh) if any((v or "").strip() for v in r.values() if v is not None)]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def load_nomenclature(work):
    """Retourne {label: dict(famille, forme:int, rgb:(r,g,b), taille:int, description)} avec palette complétée."""
    rows = read_csv(os.path.join(work, "nomenclature.csv"))
    out, used = {}, {}
    for r in rows:
        label = (r.get("label") or "").strip()
        if not label:
            continue
        fam = (r.get("famille") or "autre").strip().lower()
        base_shape, base_rgb = PALETTE_FAMILLE.get(fam, PALETTE_FAMILLE["autre"])
        f = (r.get("forme") or "").strip().lower()
        shape = int(f) if f.isdigit() else FORMES.get(f, base_shape)
        rgb = parse_rgb(r.get("rgb", ""))
        if rgb is None:
            k = used.get(fam, 0); used[fam] = k + 1
            d = VARIANTES[k % len(VARIANTES)]
            rgb = tuple(max(0, min(255, base_rgb[i] + d[i])) for i in range(3))
        out[label] = {"famille": fam, "forme": shape, "rgb": rgb, "taille": 26, "description": r.get("description") or "", "source": r.get("source") or "",
                      "legende": (r.get("legende") or "").strip()}     # no de ligne de légende (ancrage_raster : glyphe ou cercle, taille)
    return out

def load_occurrences(work):
    occ = read_csv(os.path.join(work, "occurrences-texte.csv")) + read_csv(os.path.join(work, "occurrences-visuel.csv"))
    out = []
    for r in occ:
        if (r.get("exclure") or "").strip().lower() in ("1", "oui", "x", "true"):
            continue
        try:
            out.append({"feuille": r["feuille"].strip(), "label": r["label"].strip(), "x": float(r["x_pt"]), "y": float(r["y_pt"]),
                        "source": r.get("source") or "", "note": r.get("note") or ""})
        except (KeyError, ValueError, AttributeError):
            continue
    return out

def load_feuilles(work):
    feuilles = {r["feuille"]: r for r in read_csv(os.path.join(work, "feuilles.csv"))}
    for r in read_csv(os.path.join(work, "feuilles-classement.csv")):
        if r.get("feuille") in feuilles:
            feuilles[r["feuille"]].update({"type": (r.get("type") or "").strip(), "echelle": (r.get("echelle") or "").strip(), "note_classement": r.get("note") or ""})
    # Nom d'affichage = numéro lu par l'agent dans le cartouche (« cartouche=E401 · TITRE » dans la note), sinon le nom provisoire.
    # Audit S-1769 (2026-09-22) : E401 publiée « E004 », E201 publiée « 250075EPER-p06 ».
    vus = {}
    for f, r in feuilles.items():
        m = re.search(r"cartouche\s*=\s*([A-Za-z]{1,3}-?\d{2,4}[A-Za-z]?)", r.get("note_classement") or "")
        nom = m.group(1).upper().replace("-", "") if m else f
        vus[nom] = vus.get(nom, 0) + 1
        r["nom"] = nom if vus[nom] == 1 else f"{nom}_{vus[nom]}"
    return feuilles

class PagesFeuilles:
    """La page de chaque feuille dans SON document source — jamais « page n du plus gros PDF » (revue Codex PR #28 :
    une INBOX peut contenir plusieurs PDF de plans ou un addenda ; `feuilles.csv` porte `fichier` + `page` relative à
    ce fichier). Ordre de résolution : `travail/feuilles/<F>.pdf` (la page seule écrite par prepare.py) →
    `<inbox>/<fichier>` (inbox lue dans inventaire.json) → le PDF passé en argument si son nom est celui de `fichier`."""

    def __init__(self, work, pdf=None):
        import json
        self.work, self.pdf, self._docs = work, (os.path.abspath(pdf) if pdf else None), {}
        self.inbox = None
        p = os.path.join(work, "inventaire.json")
        if os.path.exists(p):
            try:
                self.inbox = json.load(open(p, encoding="utf-8")).get("inbox")
            except Exception:  # noqa
                self.inbox = None

    def _open(self, path):
        import pymupdf
        if path not in self._docs:
            self._docs[path] = pymupdf.open(path)
        return self._docs[path]

    def page(self, row):
        """`row` = une ligne de feuilles.csv (feuille, fichier, page)."""
        seule = os.path.join(self.work, "feuilles", f"{row['feuille']}.pdf")
        if os.path.exists(seule):
            return self._open(seule)[0]
        fichier = row.get("fichier") or ""
        if self.inbox and fichier and os.path.exists(os.path.join(self.inbox, fichier)):
            return self._open(os.path.join(self.inbox, fichier))[int(row["page"]) - 1]
        if self.pdf and (not fichier or os.path.basename(self.pdf) == os.path.basename(fichier)):
            return self._open(self.pdf)[int(row["page"]) - 1]
        raise FileNotFoundError(f"feuille {row['feuille']} : ni {seule}, ni {fichier} dans l'INBOX, ni un PDF du même nom en argument")


def vers_repere_affiche(page, pts):
    """Points du repère NON tourné (get_drawings / get_text) → repère AFFICHÉ (page.rect, celui des rasters de prepare.py,
    des occurrences du relevé et du rendu) : `page.rotation_matrix`. Identité quand la page n'est pas tournée. Revue
    Codex PR #28 : pages Rotate 90/270 (S-1714, S-1769…) — sans ça, les pastilles sortent de la page."""
    if not page.rotation:
        return [(float(x), float(y)) for x, y in pts]
    import pymupdf
    M = page.rotation_matrix
    return [((q := pymupdf.Point(x, y) * M).x, q.y) for x, y in pts]


def shape_points(shape, cx, cy, rx, ry):
    if shape == DIAMOND: return [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
    if shape == TRI: return [(cx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]
    if shape == TRI_REV: return [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx, cy + ry)]
    if shape == TRAP: return [(cx - rx * 0.6, cy - ry), (cx + rx * 0.6, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]
    if shape == TRAP_REV: return [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx + rx * 0.6, cy + ry), (cx - rx * 0.6, cy + ry)]
    return None

def draw_mark(dr, shape, cx, cy, r, rgb, outline=(40, 40, 40), width=2):
    """Dessine une marque Plan Expert (PIL ImageDraw)."""
    fill = tuple(rgb) + (235,)
    if shape == CIRCLE:
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)
    elif shape == SQUARE:
        dr.rectangle([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)
    else:
        dr.polygon(shape_points(shape, cx, cy, r, r), fill=fill, outline=outline, width=width)
