"""Visual constants of the EXEMPLE.pdf (HR26-14) relevé format.

Every value below was read from the content streams of the target EXEMPLE.pdf (produced with PyMuPDF),
not estimated from photos: plan page 1 (DSI01), 46 (E02), bordereau pages 2-7 (DSI01) and 30-32 (DSI06).
Units are PDF points on a 2594 x 1729 pt sheet; plan overlay sizes are absolute points (the EXEMPLE draws
them at a fixed size whatever the plan scale), table geometry is expressed relative to the page size.
"""
from __future__ import annotations

# Family colour cycle (stroke = fill colour; fill drawn at 28 % opacity -> pastel look).
# Palette A du gold (docs/FORMAT-EXEMPLE.md §2.3) : DSI01-08, E01, E02, E06, E07, E09, E10, E12, E13, EU01-04.
# Palette B (une couleur par famille) : PALETTE_B ci-dessous ; from_exemple recopie la couleur de chaque
# marqueur du gold, from_releve.build l'applique aux feuilles agrégées (écart E7 de la spec pour le choix A/B).
PALETTE = (
    (1.0, 0.6901961, 0.0),                     # orange   (I01, I07, ...)
    (0.0, 0.44705884, 0.80784317),             # blue     (I02, I08)
    (0.0, 0.6509804, 0.31764708),              # green    (I03)
    (0.5568628, 0.26666669, 0.6784314),        # purple   (I04)
    (0.17254903, 0.24313726, 0.3137255),       # slate    (I05)
    (0.90588238, 0.29803924, 0.23529412),      # red      (I06)
)
# Palette B du gold, par code de famille : (couleur, forme, diamètre ou côté en pt). Mesurée sur les 6 pages
# plan en palette B (p.50, 52, 54, 62, 70, 78 : même code = même couleur, même forme, même taille partout).
# Forme "plan" = rectangle aux dimensions graphiques du symbole sur le plan (plinthes PL, linéaires LC).
PALETTE_B = {
    "AF": ((0.207843, 0.6, 0.6), "circle", 10.88),
    "BJ": ((0.470588, 0.784314, 0.470588), "square", 10.88),
    "CG": ((0.870588, 0.870588, 0.207843), "circle", 10.05),
    "CP": ((0.6, 0.207843, 0.6), "circle", 11.72),
    "CT": ((0.870588, 0.870588, 0.207843), "circle", 10.05),
    "CU": ((0.866667, 0.529412, 0.741177), "circle", 9.21),
    "EV": ((0.588235, 0.784314, 0.980392), "square", 10.88),
    "GF": ((0.870588, 0.870588, 0.207843), "circle", 10.88),
    "IC": ((0.6, 0.207843, 0.6), "diamond", 11.72),
    "LA": ((0.133333, 0.545098, 0.133333), "circle", 10.88),
    "LB": ((0.145098, 0.388235, 0.921569), "circle", 10.88),
    "LBM": ((0.478431, 0.380392, 0.576471), "circle", 10.88),
    "LC": ((0.705882, 0.32549, 0.035294), "plan", 10.88),
    "LD": ((0.321569, 0.701961, 0.886274), "circle", 10.88),
    "LE": ((0.752941, 0.203922, 0.803922), "circle", 10.88),
    "LF": ((0.545098, 0.360784, 0.964706), "circle", 10.88),
    "LG": ((0.858824, 0.152941, 0.466667), "circle", 10.88),
    "PC": ((0.635294, 0.419608, 0.266667), "circle", 10.88),
    "PL": ((0.894118, 0.207843, 0.207843), "plan", 10.88),
    "PN": ((0.078431, 0.078431, 0.078431), "square", 12.56),
    "RA": ((0.207843, 0.207843, 0.207843), "circle", 10.88),
    "SE": ((0.207843, 0.6, 0.6), "circle", 11.72),
    "TE": ((0.207843, 0.207843, 0.619608), "diamond", 10.88),
    "TH": ((0.866667, 0.811765, 0.207843), "circle", 10.88),
    "TV": ((0.207843, 0.207843, 0.619608), "diamond", 10.05),
}
PALETTE_B_SIZE = 10.88                        # taille par défaut d'un code absent de la table (74 cercles sur 128, p.62)
# Équivalences de couleur seulement (codes du relevé -> code du gold), lues au tableau de contenu de
# l'essai E08 (rapport-test-E08.md §2). Sans effet dès que le relevé écrit les codes du gold.
PALETTE_B_ALIAS = {"PA": "PN", "VE": "EV", "PU": "CP", "PS": "SE", "RH": "RA", "PB": "TV", "PT": "TE",
                   "PG": "GF", "PD": "PC"}
LABEL_SIZE_B = {"PL": 5.2}                    # étiquettes des plinthes en 5,2 pt sur les feuilles en palette B
FILL_OPACITY = 0.28
STROKE_OPACITY = 0.9
MARK_LINE_W = 0.7
MARK_RADIUS = 4.1859                          # default circle radius when no symbol bbox is known
                                              # (rayon gold des DSI seulement ; E/EU : 4,6045 a 5,8603, spec §2.2)
MARK_RADIUS_MAX = 8.0                         # cap of the circle drawn around an anchored (larger) symbol

# Repère label next to each marker
LABEL_FONT = "helv"
LABEL_SIZE = 4.8
LABEL_COLOR = (0.1, 0.1, 0.1)
LABEL_BOX_H = 8.0
LABEL_LINE_H = 6.0                            # box grows 6 pt per detail line (EXEMPLE E11: 14 pt for 2)
LABEL_LINE_STEP = 5.42                        # baseline step between label lines
LABEL_PAD = 1.0                               # text inset inside the white label box
LABEL_BOX_OPACITY = 0.88
LEADER_W = 0.35
LEADER_GAP = 2.0                              # leader length beyond the marker edge

# "RELEVE <sheet> - MATERIEL" box
BOX_BORDER = (0.25, 0.3, 0.35)
BOX_BORDER_W = 0.7
BOX_PAD_X = 10.0
TITLE_FONT, TITLE_SIZE = "hebo", 12.0
COUNTER_SIZE = 8.2
HINT_SIZE = 8.2
WARN_SIZE, WARN_COLOR = 7.2, (0.55, 0.1, 0.1)
ROW_CODE_SIZE = 8.2                           # bold family code
ROW_LABEL_SIZE = 6.6
ROW_QTY_SIZE = 7.1
FOOTER_SIZE = 7.0
ROW_PITCH = 27.0
ROW_PITCHES = (27.0, 22.333, 18.0, 14.0)      # EXEMPLE: 27 (DSI01), 22.33 (E02), ~13-14 (E07)
LEGEND_MARK = 10.0                            # legend swatch diameter / side
COL_WIDTHS = (505.0, 390.0, 300.0, 250.0)     # tried in this order (EXEMPLE: 505 DSI01, 390 E02, 250 E07)
MAX_COLS = 4

WARN_TEXT = ("RES = reserve source, modele, position, portee ou reconciliation; "
             "* = identification a revalider")
HINT_TEXT = "Calques activables; modeles, prescriptions et reserves completes page {page}"
FOOTER_TEXT = "Quantites source et renvois; voir bordereau detaille."
LEGEND_LAYER = "RELEVE - Legende et avertissements"
REVALIDER = "revalider"                       # item flag: identification a revalider, label gets "*"
TRAVAUX_FOOTER_TEXT = ("Emplacements de travaux sur calques; achats, prescriptions et reserves detaillees "
                       "page {page}.")

# Encadré v6 sans RES (spec §3.3 ; mesuré p.62 E08, cadre 235 x 880) : offsets depuis le haut / la gauche du cadre.
# Règle de choix (plan.encadre_v6) : feuille agrégée, palette B, RES non partiel (aucun ou tous les repères).
V6_PAD_X = 12.0
V6_TITLE_Y, V6_TITLE_SIZE = 20.0, 14.0        # baselines
V6_COUNTER_Y, V6_COUNTER_SIZE = 38.0, 9.0
V6_IDENT_Y, V6_IDENT_SIZE = 53.0, 8.5
V6_RED_Y, V6_RED_SIZE, V6_RED_STEP = 66.0, 8.5, 13.0
V6_RED = (0.70, 0.10, 0.10)
V6_FIRST_ROW = 96.5                           # centre du 1er glyphe de légende (glyphe 90 -> 103)
V6_PITCHES = (32.045, 27.0, 22.0)             # E08 32,05 ; E04/E05 34,9 ; E03 36,6
V6_WIDTHS = (235.0, 295.0, 470.0)             # E08, E04/E05, E03
V6_GLYPH = 13.0
V6_CODE_X, V6_CODE_SIZE = 33.0, 10.0
V6_LABEL_X, V6_LABEL_SIZE, V6_LABEL_STEP, V6_LABEL_UP = 62.0, 8.7, 10.47, 2.65
V6_QTY_FROM_RIGHT, V6_QTY_SIZE = 27.0, 10.0
V6_FOOT_SIZE, V6_FOOT_STEP, V6_FOOT_GAP, V6_FOOT_BOTTOM = 8.0, 10.32, 36.65, 9.48
V6_FOOTER = (
    "PL : rectangles aux dimensions graphiques du plan.",
    "W et circuits affiches uniquement si verifies.",
    "* : identification heritee a revalider ; NI : materiel non identifie.",
    "Les quantites concernent cette feuille{type}.",
    "R-001 : designation conservee au registre des reserves.",
    "Modeles, prescriptions et sources : bordereau page {page}.",
)

# Bordereau (table) page
B_MARGIN = 55.0
B_TITLE_SIZE = 26.0
B_TITLE_Y = 60.0                              # baselines, from the page top
B_SUB1_SIZE, B_SUB1_Y = 12.0, 86.0
B_SUB2_SIZE, B_SUB2_Y = 11.0, 106.0
B_SUB1 = ("Quantites representees avec multiplicateurs; portees et composants de chaque ensemble "
          "conserves.")
B_SUB2 = ("Les renvois et composants de panneaux ne constituent pas des ensembles supplementaires "
          "a additionner.")
B_HEAD_TOP, B_HEAD_H = 135.0, 27.0
B_HEAD_FILL = (0.9, 0.94, 0.97)
B_HEAD_SIZE = 10.0
B_HEAD_BASELINE = 18.0                        # from header top
B_ROW_H = 65.0
B_ROW_SIZE = 9.0
B_ROW_BASELINE = 13.675                       # first text line, from row top
B_LINE_STEP = 10.6425                         # next text line inside a cell
B_SEP_COLOR, B_SEP_W = (0.75, 0.79, 0.82), 0.4
B_ROWS_BOTTOM = 202.0                         # free space kept under the last row (21 rows on 1729 pt)
B_CELL_PAD = 4.0
B_RES_GAP = 25.75                             # "RESERVES ET COMPLEMENTS" baseline below last separator
B_RES_SIZE, B_RES_STEP = 10.0, 12.3625
B_RES_TITLE = "RESERVES ET COMPLEMENTS"
B_MAX_CELL_LINES = 5

# Column start offsets as fractions of the table width (2484 pt in EXEMPLE: 55 -> 2539).
B_COLUMNS = (
    ("repere", "Repere / source", 0.0),
    ("materiel", "Materiel", 173.88 / 2484),
    ("designation", "Designation", 546.48 / 2484),
    ("qte", "Qte", 695.52 / 2484),
    ("portee", "Portee", 782.46 / 2484),
    ("modele", "Modele", 1006.02 / 2484),
    ("prescription", "Prescription / reserve", 1378.62 / 2484),
    ("parent", "Parent", 2334.96 / 2484),
)


def family_color(index: int) -> tuple[float, float, float]:
    return PALETTE[index % len(PALETTE)]


def palette_b(code: str):
    """(couleur, forme, taille) de la palette B pour un code de famille, sinon None.

    Recherche : le code, son équivalent (PALETTE_B_ALIAS), puis ses lettres seules (PL3 -> PL)."""
    import re
    letters = re.match(r"[A-Z]+", code or "")
    for c in (code, PALETTE_B_ALIAS.get(code), letters and letters.group(0),
              letters and PALETTE_B_ALIAS.get(letters.group(0))):
        if c and c in PALETTE_B:
            return PALETTE_B[c]
    return None


def is_palette_a(colors) -> bool:
    """Toutes les couleurs de familles sont dans le cycle de la palette A (tolérance 0,01)."""
    return all(any(max(abs(a - b) for a, b in zip(c, p)) < 0.01 for p in PALETTE) for c in colors)
