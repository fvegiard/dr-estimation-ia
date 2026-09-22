# Charte graphique Plan Expert : forme, couleur (RVB) et taille par famille d'objets.
#
# Porté depuis planexpert-s1857-saint-michel/verification/rules_dupuis.py
# (voir docs/consolidation.md). Palette et formes alignées sur le relevé de
# référence du projet S-1857 (couleurs échantillonnées dans les pastilles
# des légendes Plan Expert, pages E400-E409 ; formes lues sur les mêmes
# pastilles). Aucune valeur n'est inventée : c'est la charte mesurée sur le
# relevé de référence ; à rééchantillonner pour une autre charte.
#
# Enum Plan Expert : 0 Circle, 1 Square, 2 Diamond, 3 Triangle,
# 4 TriangleReversed, 5 Trapeze, 6 TrapezeReversed.
from __future__ import annotations

import re
import unicodedata

CIRCLE, SQUARE, DIAMOND, TRI, TRI_REV, TRAP, TRAP_REV = 0, 1, 2, 3, 4, 5, 6

RULES = [
    # --- luminaires (référence : FIXTURE TYPE ...)
    (r'^Luminaire DS0\b', CIRCLE, (108, 155, 190), 26),      # DS0 : rond bleu acier
    (r'^Luminaire DS1\b', SQUARE, (238, 182, 53), 24),       # DS1 : orange
    (r'^Luminaire DS2\b', CIRCLE, (202, 157, 102), 26),      # DS2 : rond brun clair
    (r'^Luminaire DS4', SQUARE, (215, 203, 53), 24),         # DS4 : jaune olive
    (r'^Luminaire DR2\b', SQUARE, (224, 219, 163), 24),      # DR2 : beige
    (r'^Luminaire DR5\b', SQUARE, (228, 53, 53), 24),        # DR5 : rouge
    (r'^Luminaire DR51\b', SQUARE, (103, 209, 197), 24),     # DR51 : cyan
    (r'^Luminaire DR52\b', SQUARE, (153, 216, 53), 24),      # DR52 : lime
    (r'^Luminaire DW4\b', SQUARE, (211, 155, 211), 24),      # DW4 : violet clair
    (r'^Luminaire DW42\b', SQUARE, (185, 115, 185), 24),     # DW42 : violet (référence fusionne dans DW4)
    (r'^Luminaire DMW1\b', CIRCLE, (53, 153, 53), 26),       # DMWI CME-01 : rond vert
    (r'^LUM - Mural ext', CIRCLE, (40, 110, 40), 26),        # (nous seulement) vert foncé
    # --- commandes
    (r'^CMD - Do inoccupation - mur', CIRCLE, (53, 53, 221), 26),       # DO : bleu
    (r'^CMD - Do inoccupation - plafond', CIRCLE, (221, 53, 221), 26),  # DO PL : magenta
    (r'^CMD - Di infrarouge', CIRCLE, (53, 53, 162), 26),               # DI PL : indigo
    (r'^CMD - B bouton', SQUARE, (162, 53, 53), 24),                    # B : carré rouge foncé
    (r'^CMD - Ba alimentation', SQUARE, (153, 53, 153), 26),            # BA : carré pourpre
    (r'^CMD - Interrupteur 1p', CIRCLE, (221, 135, 189), 26),           # INT : rose
    (r'^CMD - Interrupteur t', CIRCLE, (153, 222, 53), 26),             # INT PRE : lime
    (r'^CMD - Gradateur120V3voies', CIRCLE, (221, 53, 53), 26),         # GRADATEUR 3V : rouge
    (r'^CMD - Gradateur120V - mur', CIRCLE, (103, 214, 207), 26),       # GRADATEUR : cyan
    (r'^CMD - Photocellule', CIRCLE, (240, 160, 40), 28),               # (nous seulement) ambre
    # --- secours
    (r'^Accu36W avec phare double et enseigne', SQUARE, (184, 211, 211), 26),  # COMBO : cyan pâle
    (r'^Accu18W', SQUARE, (204, 204, 204), 26),                                # COMBO 18W : gris
    (r'^Accu36W avec phare double sans', SQUARE, (199, 188, 163), 26),         # BATTERIE UNIT 2T 36W : beige
    (r'^Enseigne separee|^Enseigne (double|simple) face', CIRCLE, (222, 177, 149), 26),  # EXIT : saumon
    (r'^Phare double', CIRCLE, (164, 164, 164), 26),                            # TETE DOUBLE : gris
    (r'^Phare simple', CIRCLE, (220, 220, 53), 26),                             # TETE SIMPLE : jaune
    # --- prises
    (r'^Prise duplex 20A 125V$', CIRCLE, (222, 180, 53), 26),                  # PRISE 15/20A : orange
    (r'^Prise duplex 20A 125V a 1070', CIRCLE, (200, 150, 40), 26),            # orange foncé (1070 mm)
    (r'^Prise duplex 20A 125V au plancher', SQUARE, (224, 53, 53), 26),        # MONUMENT PLANCHER : carré rouge
    (r'^Prise duplex 20A 125V integree', CIRCLE, (190, 140, 60), 26),          # mobilier (nous) : brun-orange
    (r'^Prise duplex 20A 125V micro', CIRCLE, (170, 120, 50), 26),             # micro-ondes (nous)
    (r'^Prise duplex 15A', CIRCLE, (162, 107, 68), 26),                        # PRISE : brun
    (r'^Prise duplex DDFT', CIRCLE, (222, 222, 53), 26),                       # PRISE GFI : jaune
    (r'^Prise cuisiniere', CIRCLE, (153, 53, 153), 28),                        # PRISE 50A250V : pourpre
    (r'^Prise secheuse', CIRCLE, (53, 153, 153), 28),                          # 30A 250V : sarcelle
    (r'^Colonnette', SQUARE, (209, 155, 209), 28),                             # COLONNETTE : carré rose
    # --- alarme incendie
    (r'^Alarme klaxon', CIRCLE, (53, 153, 153), 26),                 # KLAXON : sarcelle
    (r'^Alarme avertisseur combine', CIRCLE, (222, 107, 53), 26),    # KLAXON STROB : orange-rouge
    (r'^Alarme detecteur de fumee', CIRCLE, (108, 155, 190), 26),    # DETECTEUR FUMEE : bleu acier
    (r'^Alarme detecteur thermique', CIRCLE, (217, 213, 163), 26),   # DETECTEUR THERMIQUE : beige
    (r'^Alarme poste manuel', SQUARE, (216, 53, 216), 26),           # STATION MANUEL : carré magenta
    (r'^Alarme panneau', SQUARE, (53, 53, 53), 30),                  # PAI (nous) : noir
    (r'^Alarme module', SQUARE, (120, 120, 120), 28),                # TRA (nous) : gris
    # --- télécom
    (r'^DATA_MURAL', TRI, (53, 53, 158), 26),                         # TEL : triangle marine
    (r'^DATA_PLANCHER|^DATA_MOBILIER|^DATA_1070', SQUARE, (53, 153, 53), 26),  # MONUMENT TEL : carré vert
    (r'^PMI', TRI, (153, 53, 153), 30),                               # (nous) triangle pourpre
    # --- raccords mécaniques / équipements
    (r'^Sectionneur CC equipement', SQUARE, (224, 178, 149), 26),     # NF 30A : carré saumon
    (r'^Borne de recharge', TRI_REV, (196, 187, 53), 30),             # BORNE 3R : triangle inversé jaune-olive
    (r'^Hotte', SQUARE, (103, 222, 216), 28),                         # HOTTE : carré cyan
    (r'^Thermostat', CIRCLE, (221, 207, 53), 26),                     # TS : rond jaune-olive
    (r'^Lave-vaisselle', CIRCLE, (120, 200, 120), 26),                # (nous) vert clair
    (r'^Seche-main', CIRCLE, (150, 200, 250), 26),                    # (nous) bleu clair
    (r'^Enseigne lumineuse EN', CIRCLE, (255, 160, 80), 26),          # (nous) orange clair
    # --- distribution E200 / E600 (nous seulement)
    (r'^Coupe-circuit', SQUARE, (224, 178, 149), 24),                 # comme NF 30A
    (r'^Disjoncteur\S*1P', SQUARE, (60, 160, 60), 20),
    (r'^Disjoncteur\S*2P', SQUARE, (40, 150, 150), 20),
    (r'^Disjoncteur', SQUARE, (30, 60, 160), 20),
    (r'^Panneau', SQUARE, (20, 20, 20), 26),
    (r'^Transformateur', SQUARE, (130, 40, 160), 26),
    (r'^Coupure entree|^Sectionneur entree', SQUARE, (200, 40, 40), 24),
    (r'^Sectionneur fusible', SQUARE, (235, 53, 235), 24),            # 30A NF WP : magenta
    (r'^Ensemble mesurage', SQUARE, (200, 40, 40), 26),
    (r'^Electrode', SQUARE, (140, 90, 40), 22),
    (r'^Verrouillage', SQUARE, (250, 160, 40), 20),
]


def regle_pour_libelle(libelle: str):
    """(forme, rgb, taille) de la première règle qui correspond, sinon None.

    Même sémantique que l'application des RULES dans make_v6.py : premier
    motif (regex, ancré en début de libellé) qui « match » gagne."""
    for motif, forme, rgb, taille in RULES:
        if re.match(motif, libelle):
            return forme, rgb, taille
    return None


# --------------------------------------------------------------------- #
# Classification en postes (familles) — déduite des sections de la charte
# ci-dessus (commentaires « --- luminaires », « --- distribution »…), pas
# inventée. Sert au « Résumé par poste majeur » de releve.xlsx et au
# contrôle « écart par poste majeur ≤ 10 % » de la validation (ecart.md).
# --------------------------------------------------------------------- #

# Postes majeurs suivis par les critères d'acceptation (README, SPEC).
POSTES_MAJEURS = ("luminaires", "distribution", "filage", "conduits")

# (poste, regex) — appliquées au libellé NORMALISÉ (minuscules, sans
# accents). Les sept premières familles reprennent exactement les sections
# de RULES ; « filage » et « conduits » couvrent les métrés linéaires
# (artères, câbles, conduits) qui ne sont pas des compteurs de la charte.
_FAMILLES = [
    ("luminaires", r"^luminaire|^lum - "),
    ("commandes", r"^cmd - "),
    ("secours", r"^accu|^enseigne separee|^enseigne (double|simple)|^phare"),
    ("prises", r"^prise|^colonnette"),
    ("alarme", r"^alarme"),
    ("telecom", r"^data_|^pmi"),
    ("mecanique", r"^sectionneur cc|^borne de recharge|^hotte|^thermostat"
                  r"|^lave-vaisselle|^seche-main|^enseigne lumineuse"),
    ("distribution", r"^coupe-circuit|^disjoncteur|^panneau|^transformateur"
                     r"|^coupure entree|^sectionneur entree"
                     r"|^sectionneur fusible|^ensemble mesurage|^electrode"
                     r"|^verrouillage"),
    ("conduits", r"conduit"),
    ("filage", r"fil\b|cable|teck|acwu|ac90|nual|artere"),
]

_FAMILLES_RE = [(poste, re.compile(motif)) for poste, motif in _FAMILLES]


def normaliser(texte: str) -> str:
    """Minuscules, accents retirés, espaces compactées — la normalisation
    commune de tout le pipeline de comparaison (écarts, familles)."""
    txt = unicodedata.normalize("NFKD", str(texte))
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return " ".join(txt.casefold().split())


def famille_pour_libelle(libelle: str) -> str:
    """Poste (famille) d'un libellé, d'après les sections de la charte ;
    « autre » si aucune section ne correspond."""
    norm = normaliser(libelle)
    for poste, motif in _FAMILLES_RE:
        if motif.search(norm):
            return poste
    return "autre"
