"""Visual constants of the EXEMPLE.pdf (HR26-14) relevé format.

Every value below was read from the content streams of the target EXEMPLE.pdf (produced with PyMuPDF),
not estimated from photos: plan page 1 (DSI01), 46 (E02), bordereau pages 2-7 (DSI01) and 30-32 (DSI06).
Units are PDF points on a 2594 x 1729 pt sheet; plan overlay sizes are absolute points (the EXEMPLE draws
them at a fixed size whatever the plan scale), table geometry is expressed relative to the page size.
"""
from __future__ import annotations

# Family colour cycle (stroke = fill colour; fill drawn at 28 % opacity -> pastel look).
PALETTE = (
    (1.0, 0.6901961, 0.0),                     # orange   (I01, I07, ...)
    (0.0, 0.44705884, 0.80784317),             # blue     (I02, I08)
    (0.0, 0.6509804, 0.31764708),              # green    (I03)
    (0.5568628, 0.26666669, 0.6784314),        # purple   (I04)
    (0.17254903, 0.24313726, 0.3137255),       # slate    (I05)
    (0.90588238, 0.29803924, 0.23529412),      # red      (I06)
)
FILL_OPACITY = 0.28
STROKE_OPACITY = 0.9
MARK_LINE_W = 0.7
HALO_W = 1.0                                  # white ring outside each plan marker
MARK_RADIUS = 4.1859                          # default circle radius when no symbol bbox is known
MARK_RADIUS_MAX = 8.0                         # cap of the circle drawn around an anchored (larger) symbol

# Repère label next to each marker
LABEL_FONT = "helv"
LABEL_SIZE = 4.8
LABEL_COLOR = (0.1, 0.1, 0.1)
LABEL_BOX_H = 8.0
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

# Aggregated-sheet legend box (EXEMPLE E03, page 50: 470 pt wide, one row per family with its model line)
AGG_PAD_X = 12.0
AGG_COL_W = 458.0
AGG_FIRST_ROW = 92.0                          # baseline of the first family code, from the box top
AGG_PITCHES = (36.57, 27.0, 20.0)
AGG_QTY_X = 431.0                             # quantity x inside a column (E03: 443 from the box edge)
AGG_ROWS_TO_FOOTER = 20.0
AGG_FOOTER_STEP = 10.32
AGG_FOOTER_BOTTOM = 19.8
AGG_HINT_TEXT = "Calques activables; modeles, prescriptions et sources : bordereau page {page}."
AGG_FOOTER = (
    "RES = reserve source, modele, position ou portee; * = identification a revalider.",
    "Quantites = reperes de cette feuille; les renvois ne s'additionnent pas.",
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
