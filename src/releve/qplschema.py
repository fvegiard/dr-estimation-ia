"""
Schéma QPL (Plan Expert) — constantes et fonctions de bas niveau, communes
à `qpl_build.py` (écriture) et `verifier.py` (lecture).

Rien ici n'est inventé : chaque constante a été vérifiée en lisant de vrais
fichiers .qpl (voir docs/pipeline-qpl.md §2, section « Spécification du
format QPL — observée dans les fichiers réels ») :
  - planexpert/00-original-codex/maison st-michel test (8-Septembre-2026).qpl
    (projet nu, jamais modifié)
  - planexpert/04-v5-native/Saint-Michel-Codex-Releve-v5-20260909.qpl
    (218 compteurs, 1 575 éléments, resauvegardé par Plan Expert)
"""
from __future__ import annotations

import uuid
from xml.sax.saxutils import escape as _xml_escape

# --- Enveloppe (PIPELINE §2.1) -------------------------------------------
BOM = "﻿"
XML_DECL = '<?xml version="1.0"?>'
CRLF = "\r\n"
TAB = "\t"

# --- Fond de légende, vérifié en v5/v6 (PIPELINE §2.4 et §2.7) -----------
LEGEND_FILL_COLOR = -657931  # 0xFFF5F5F5, blanc cassé
LEGEND_FONT_SIZE = 45
LEGEND_MAX_ROWS = 25
LEGEND_PEN_WIDTH = 6

# --- Couleurs des artères, vérifiées en v6 (PIPELINE §2.6 et §2.7) -------
ARTERE_COLOR = -29696          # 0xFFFF8800, orange (27 artères en v6)
CTRL_ECHELLE_COLOR = -16776961  # 0xFF0000FF, bleu (objet de contrôle)

# --- Formes (PIPELINE §2.7, énumération lue par réflexion dans
#     PlanExpert.exe, QuoterPlan.DrawCounter+CounterShapeTypeEnum) --------
SHAPES = {
    0: "Circle",
    1: "Square",
    2: "Diamond",
    3: "Triangle",
    4: "TriangleReversed",
    5: "Trapeze",
    6: "TrapezeReversed",
    7: "CustomImage",
}

# --- Les 16 propriétés du rapport par défaut, recopiées telles quelles
#     depuis planexpert/04-v5-native/...-v5-20260909.qpl (PIPELINE §2.9) --
REPORT_PROPERTIES: list[tuple[str, str]] = [
    ("ShowProjectInfo", "True"),
    ("ShowComments", "True"),
    ("ShowInvisibleObjects", "True"),
    ("ApplyFilter", "True"),
    ("EstimatingShowProjectInfo", "True"),
    ("EstimatingShowComments", "True"),
    ("EstimatingShowInvisibleObjects", "True"),
    ("EstimatingApplyFilter", "True"),
    ("QuoteShowProjectInfo", "True"),
    ("QuoteShowComments", "True"),
    ("QuoteShowInvisibleObjects", "True"),
    ("QuoteApplyFilter", "True"),
    ("OrderByObjectsFilter", ""),
    ("OrderByPlansFilter", ""),
    ("ReportSortBy", "0"),
    ("QuoteReportSortBy", "0"),
]


def esc(value: object) -> str:
    """Échappe un attribut XML (gère notamment le '>' des noms d'artères,
    ex. « ART F10 P-P1>VRT-1 [puits->TOIT] », PIPELINE §2.6)."""
    return _xml_escape(str(value), {'"': "&quot;"})


def bool_str(value: object) -> str:
    """Plan Expert écrit les booléens 'True'/'False' (jamais 'true'/'1')."""
    return "True" if value else "False"


def new_thumbnail() -> str:
    """GUID de substitution pour <Thumbnail FileName="..."/>.

    Une vraie vignette est une image interne générée par Plan Expert à
    l'ouverture / sauvegarde (PIPELINE §3.4) : impossible à produire hors
    de Plan Expert sans inventer une image. On écrit un GUID neuf ; Plan
    Expert le remplace de toute façon à la prochaine sauvegarde native.
    """
    return str(uuid.uuid4())
