#!/usr/bin/env python3
"""Chiffrage « méthode Dupuis » à l'aveugle — dossier S-1902 (Bibliothèque Georgette-Lepage, Brossard).

Déterministe, stdlib + openpyxl. Lit uniquement le kit (dossier courant du script) et écrit chiffrage.json.
 - quantités sur plan      : rapport-releve.md (portées par famille) + releve.xlsx (totaux par libellé)
 - quantités hors plan     : entree/reference-Estimation_2.xlsx, feuille Détail (codes A-, B-, C-...)
 - prix / temps unitaires  : catalogue-prix-temps-dupuis.csv, colonnes prix_a_utiliser / temps_a_utiliser
 - familles absentes       : entree/reference-Estimation_2.xlsx, feuille Matériel Lumen (prix réguliers)
 - lots, taux, facteur     : METHODE.md (prix confirmés par Francis le 2026-10-20)
Aucune exception n'est avalée : toute valeur manquante fait échouer le script (code de sortie != 0).
"""
import csv
import json
import math
import os
import re
import sys

import openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))
P_CAT = os.path.join(BASE, "catalogue-prix-temps-dupuis.csv")
P_REL = os.path.join(BASE, "releve.xlsx")
P_RAP = os.path.join(BASE, "rapport-releve.md")
P_EST = os.path.join(BASE, "entree", "reference-Estimation_2.xlsx")
P_MET = os.path.join(BASE, "METHODE.md")
P_OUT = os.path.join(BASE, "chiffrage.json")

M_TO_PI = 3.28084

# ----------------------------------------------------------------------------------------------
# Paramètres METHODE.md
# ----------------------------------------------------------------------------------------------
TAUX = 85.0          # $/h — dossiers août-octobre 2026 (METHODE §5)
FACTEUR = 1.244      # METHODE §7
LOTS = {             # METHODE §2 (confirmés par Francis le 2026-10-20)
    "eclairage": 11893.0,
    "distribution": 3400.0 + 20 * 95.0 + 3 * 300.0,   # NF 225 A 42 cct + EDB 1P x20 + EJB 3P x3 = 6 200
    "JCI": 7400.0,
    "detecteurs_JCI": 600.0,
    "GPR": 1250.0,
}
# Ventilation des lots par article du bordereau
LOT_ART = {
    "eclairage": {"3.35": 11893.0},
    "distribution": {"3.24": 3400.0, "3.25": 2800.0},
    "JCI": {"3.38": 7400.0},
    "detecteurs_JCI": {"3.36": 600.0},
    "GPR": {"3.32": 1250.0},
}


def fail(msg):
    print("ERREUR: " + msg, file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------------------------
# Lecture du kit
# ----------------------------------------------------------------------------------------------
def lire_catalogue():
    cat = {}
    with open(P_CAT, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            d = r["description"].strip()
            if d in cat:
                cat[d] = None   # libellé ambigu (doublon): refusé s'il est utilisé
                continue
            cat[d] = {
                "um": r["um"],
                "prix": float(r["prix_a_utiliser"]),
                "temps": float(r["temps_a_utiliser"]),
                "date": r["date_dernier"],
                "projet": r["projet_dernier"],
            }
    return cat


def lire_portees():
    """rapport-releve.md : | famille | total | CONSERVER 5, INSTALLER 3, ... |"""
    out = {}
    with open(P_RAP, encoding="utf-8") as f:
        for ln in f:
            m = re.match(r"^\|\s*([A-Z0-9_ ]+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", ln)
            if not m:
                continue
            fam, tot, port = m.group(1), int(m.group(2)), m.group(3)
            d = {}
            for part in port.split(","):
                k, v = part.strip().rsplit(" ", 1)
                d[k] = int(v)
            if sum(d.values()) != tot:
                fail("portées incohérentes pour " + fam)
            out[fam] = d
    return out


def lire_totaux_releve():
    wb = openpyxl.load_workbook(P_REL, data_only=True)
    ws = wb["Par libellé"]
    out = {}
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[0]:
            out[r[0]] = int(r[2])
    return out


def lire_detail():
    wb = openpyxl.load_workbook(P_EST, data_only=True)
    ws = wb["Détail"]
    out = {}
    for r in ws.iter_rows(min_row=7, values_only=True):
        code = r[0]
        if code and re.match(r"^[A-H]-\d+$", str(code)):
            out[code] = {"desc": r[1], "q": r[3], "u": r[4], "h": r[7]}
    return out


def lire_lumen():
    wb = openpyxl.load_workbook(P_EST, data_only=True)
    ws = wb["Matériel Lumen"]
    out = {}
    for r in ws.iter_rows(min_row=6, values_only=True):
        if r[0] and r[4] is not None and r[2] is not None:
            out[r[0]] = {"desc": r[1], "prix": float(r[4]), "u": r[3]}
    return out


CAT = lire_catalogue()
POR = lire_portees()
TOT = lire_totaux_releve()
DET = lire_detail()
LUM = lire_lumen()

# vérifie que le releve.xlsx et le rapport concordent
for fam, d in POR.items():
    if TOT.get(fam) != sum(d.values()):
        fail("totaux releve.xlsx / rapport-releve.md différents pour " + fam)


def por(fam, *kinds):
    if fam not in POR:
        fail("famille inconnue du relevé: " + fam)
    return sum(POR[fam].get(k, 0) for k in kinds)


def pi(m):
    return int(math.ceil(m * M_TO_PI - 1e-9))


# ----------------------------------------------------------------------------------------------
# Construction des lignes
# ----------------------------------------------------------------------------------------------
LIGNES = []


def add(code, desc, q, u, art, src, p, h):
    LIGNES.append({"code": code, "desc": desc, "q": q, "u": u, "p": round(p, 4), "h": round(h, 4),
                   "art": art, "src": src})


def cat_line(code, desc, q, art, label, p=None, h=None, u=None, note=""):
    """Ligne chiffrée sur un libellé exact du catalogue Dupuis (prix_a_utiliser / temps_a_utiliser)."""
    if label not in CAT or CAT[label] is None:
        fail("libellé absent ou ambigu dans le catalogue: " + label)
    c = CAT[label]
    pp = c["prix"] if p is None else p
    hh = c["temps"] if h is None else h
    src = "catalogue Dupuis « %s » (PRIX/TEMPS À UTILISER, dernier %s)" % (label, c["date"])
    if p is not None:
        src += "; prix mis à 0 $ en ligne (inclus dans le lot fournisseur)" if p == 0 else "; prix ajusté"
    if h is not None:
        src += "; temps ajusté"
    if note:
        src += "; " + note
    add(code, desc, q, u or ("pi" if c["um"] == "P" else "u"), art, src, pp, hh)


def jug_line(code, desc, q, u, art, h, note="", det=None):
    """Heures de jugement lues dans la feuille Détail (Estimation_2), prix matériel 0 $."""
    d = DET[det or code]
    if h is None:
        h = float(d["h"])
    src = "jugement (Estimation_2) — Détail %s, %s h/u à valider" % (det or code, ("%g" % h))
    if note:
        src += "; " + note
    add(code, desc, q, u, art, src, 0.0, h)


def lumen_line(code, desc, q, art, lcode, h=0.0, note=""):
    if lcode not in LUM:
        fail("code Lumen absent: " + lcode)
    l = LUM[lcode]
    src = "prix Lumen %s « %s » (réguliers 2026-10-07), famille absente du catalogue Dupuis; temps par jugement" % (lcode, l["desc"])
    if note:
        src += "; " + note
    add(code, desc, q, "u", art, src, l["prix"], h)


# ---- A. Démantèlement / relocalisation (5.19 démolition, 3.22 démontage) ----------------------
n_lum_enl = por("ENCASTRE", "ENLEVER") + por("LED 1X4", "ENLEVER") + por("LED 2X2", "ENLEVER")
add("A-01", "Démantèlement luminaires existants (E.A.E) RDC + 2e — relevé: ENCASTRE + LED 1X4 + LED 2X2 enlevés (fusionne A-02)",
    n_lum_enl, "u", "5.19",
    "METHODE.md §3 « luminaire enlevé 0,5 h » (libellé absent du catalogue; voisins ENLEVER FIXTURE ENCAST/2X2/1X4 = 0,35 h); quantité releve.xlsx/rapport (portée ENLEVER)",
    0.0, 0.5)
n_prise_enl = por("PRISE DDFT", "ENLEVER") + por("PRISE DOUBLE 15A", "ENLEVER") + por("SORTIE DATA", "ENLEVER")
cat_line("A-03", "Démantèlement services (prises, DDFT, sorties data) E.A.E RDC + 2e — fusionne A-04",
         n_prise_enl, "5.19", "ENLEVER PRISE")
cat_line("A-12", "Interrupteur existant enlevé (E.A.E)", por("INT SIMPLE", "ENLEVER"), "5.19", "ENLEVER INTERRUPTEUR")
n_equip_enl = (por("MONUMENT PLANCHER", "ENLEVER") + por("BOITE JONCTION", "ENLEVER") + por("BOITIER C", "ENLEVER")
               + por("DETECTEUR FUMEE", "ENLEVER") + por("DETECTEUR MOUVEMENT", "ENLEVER") + por("HP ENCASTRE PLAFOND", "ENLEVER"))
cat_line("A-13", "Autres équipements enlevés (monuments plancher, boîtes de jonction, boîtier C, détecteurs, haut-parleur)",
         n_equip_enl, "5.19", "EQUIPEMENT A ENLEVER")
n_relo_prise = por("PRISE DDFT", "RELOCALISER") + por("PRISE DOUBLE 15A", "RELOCALISER") + por("SORTIE DATA", "RELOCALISER")
cat_line("A-05", "Relocalisation prises / sorties data (E.A.R) RDC + 2e", n_relo_prise, "3.22", "RELO PRISE")
cat_line("A-06", "Relocalisation luminaires encastrés (E.A.R)", por("ENCASTRE", "RELOCALISER"), "3.22", "RELO ENCASTRE")
jug_line("A-07", DET["A-07"]["desc"], DET["A-07"]["q"], "lot", "3.22", None)
cat_line("A-08", "FabLab 210 : retrait temporaire + réinstallation luminaires linéaires existants",
         DET["A-08"]["q"], "3.22", "RELO ENCASTRE", note="quantité Détail A-08 (comptée sur plan E-202); libellé voisin pour retrait + repose")
cat_line("A-09", "FabLab 210 : retrait temporaire + réinstallation encastrés existants",
         DET["A-09"]["q"], "3.22", "RELO ENCASTRE", note="quantité Détail A-09 (comptée sur plan E-202, ±2)")
jug_line("A-10", "Toit : débrancher, entreposer sectionneurs, couvrir câbles, rebrancher équipements de ventilation (E.A.R) — moteurs monophasés relocalisés",
         por("MOTEUR MONOPHASE", "RELOCALISER"), "u", "3.22", None, note="quantité releve (MOTEUR MONOPHASE RELOCALISER)")
jug_line("A-11", DET["A-11"]["desc"], DET["A-11"]["q"], "lot", "3.22", None)

# ---- B. Distribution (3.24 panneau, 3.25 disjoncteurs) -----------------------------------------
cat_line("B-01", "Panneau PP-3 neuf 225A 347/600V 42 cct (NF Schneider) — remplacement", DET["B-01"]["q"], "3.24",
         "PANNEAU 100A 347/600V 3F", p=0.0, h=None, note="panneau fourni par lot distribution; 8 h (METHODE §3)")
cat_line("B-02", "Disjoncteurs NF 1P-15A circuits existants transférés (PP-3)", DET["B-02"]["q"], "3.25", "DISJ15A1P",
         note="disjoncteur 1P fourni par lot distribution")
cat_line("B-03", "Disjoncteur 3P-20A (aérotherme) transféré", DET["B-03"]["q"], "3.25", "DISJ 100A 3P 120/240V 22 K", p=0.0,
         note="temps 3P = 1 h (METHODE §3), fourni par lot distribution")
cat_line("B-04", "Disjoncteur 3P-40A UTA-1 neuf", DET["B-04"]["q"], "3.25", "DISJ 100A 3P 120/240V 22 K", p=0.0,
         note="temps 3P = 1 h (METHODE §3), fourni par lot distribution")
cat_line("B-05", "Disjoncteur 3P-15A VE-2N neuf", DET["B-05"]["q"], "3.25", "DISJ 100A 3P 120/240V 22 K", p=0.0,
         note="temps 3P = 1 h (METHODE §3), fourni par lot distribution")
cat_line("B-06", "Disjoncteur 1P-15A DDFT fontaine P2-61", DET["B-06"]["q"], "3.25", "DISJ15A1P", note="fourni par lot distribution")
cat_line("B-07", "Disjoncteurs 1P-15A P2-63 / P2-64", DET["B-07"]["q"], "3.25", "DISJ15A1P", note="fourni par lot distribution")
cat_line("B-08", "Disjoncteurs 1P-20A P3-17/19 machine de tri", DET["B-08"]["q"], "3.25", "DISJ 20A 1P 120V 10KA", p=0.0,
         note="fourni par lot distribution")
jug_line("B-09", DET["B-09"]["desc"], DET["B-09"]["q"], "u", "3.24", None)

# ---- C. Raccordements mécaniques (3.23, 3.26 MCC) ----------------------------------------------
n_mot_tri_new = por("MOTEUR TRIPHASE", "INSTALLER")   # 4 = UTA-01 + VE-02N + 2 chaudières
n_mot_mono_new = por("MOTEUR MONOPHASE", "INSTALLER")  # 3 = humidificateurs
if n_mot_tri_new != 4 or n_mot_mono_new != 3:
    fail("moteurs à raccorder: répartition inattendue")
cat_line("C-01", "UTA-01 York 575V/3Ø au toit — raccordement (sectionneur d'usine)", DET["C-01"]["q"], "3.23",
         "UNITER UC AU TOIT", note="UTA 1 h (METHODE §3); libellé voisin « unité au toit »")
cat_line("C-02", "VE-02N Plymovent 1,5 HP 575V/3Ø c/a VFD au toit — raccordement", DET["C-02"]["q"], "3.23", "MOTEUR",
         note="releve MOTEUR TRIPHASE INSTALLER")
cat_line("C-03", "Chaudières CH-01 / CH-02 600V/3Ø — réutiliser tiroirs CCM-1 et câbles existants, raccord final",
         DET["C-03"]["q"], "3.26", "MOTEUR", note="releve MOTEUR TRIPHASE INSTALLER")
cat_line("C-04", "Humidificateurs HUM-1/2/3 120V/1Ø — raccordement", DET["C-04"]["q"], "3.23", "MOTEUR",
         note="releve MOTEUR MONOPHASE INSTALLER")
lumen_line("C-04b", "Sectionneur sans fusible 30A 1Ø des humidificateurs", DET["C-04"]["q"], "3.23", "HUBHBL1372", h=0.0,
           note="temps du sectionneur ajouté à la ligne suivante")
# le temps du sectionneur vient du catalogue (« SECTIONNEURS SANS FUSIBLES 30A », prix 0 $ au catalogue -> prix Lumen)
LIGNES[-1]["h"] = CAT["SECTIONNEURS SANS FUSIBLES 30A"]["temps"]
LIGNES[-1]["src"] = ("prix Lumen HUBHBL1372 « HUBBELL HBL1372 SECTIONNEUR 30A 2P » (réguliers 2026-10-07, prix catalogue = 0 $); "
                     "temps catalogue Dupuis « SECTIONNEURS SANS FUSIBLES 30A » (dernier %s)" % CAT["SECTIONNEURS SANS FUSIBLES 30A"]["date"])
cat_line("C-05", "Conduit EMT 1\" vide alim. UTA-01 (35 m)", pi(DET["C-05"]["q"]), "3.23", "CONDUIT VIDE 1",
         note="longueur Détail C-05 (hypothèse) convertie m→pi")
cat_line("C-06", "Conducteur RW90 #8 Cu UTA-01 (140 m)", pi(DET["C-06"]["q"]), "3.23", "8AWG 7 BRINS RW90 600V 90C NOIR",
         note="longueur Détail C-06")
cat_line("C-07", "Conduit EMT 3/4\" vide VE-02N + HUM (80 m)", pi(DET["C-07"]["q"]), "3.23", "CONDUIT VIDE 3/4",
         note="longueur Détail C-07")
cat_line("C-08", "Conducteur RW90 #12 Cu VE-02N + HUM (275 m)", pi(DET["C-08"]["q"]), "3.23", "12AWG SOLIDE RW90 600V",
         note="longueur Détail C-08")

# ---- D/E. Services RDC et étage (3.27 à 3.34) ---------------------------------------------------
cat_line("D-01", "Postes de travail mobilier : boîte de jonction + raccord câbles réutilisés", DET["D-01"]["q"], "3.31",
         "DROP DE PRISE", note="quantité Détail D-01 (18 postes, hors plan)")
cat_line("D-02", "Prise double 15A-120V USB (Leviton Decora USB) — relevé INSTALLER", por("PRISE USB", "INSTALLER"), "3.27",
         "PRISE USB 125V 15 AMP")
cat_line("D-03", "Cabines/isoloirs : JB mur + prise (hors plan)", DET["D-03"]["q"], "3.31", "DROP DE PRISE",
         note="quantité Détail D-03")
cat_line("E-01", "Poste aide au lecteur 227 : JB + prises (hors plan)", DET["E-01"]["q"], "3.31", "DROP DE PRISE",
         note="quantité Détail E-01")
cat_line("E-04", "Cabines/salles étage : JB + prise (hors plan)", DET["E-04"]["q"], "3.31", "DROP DE PRISE",
         note="quantité Détail E-04")
cat_line("D-06", "Prise double 15A-120V — relevé INSTALLER (incl. murales/colonnes/tables)", por("PRISE DOUBLE 15A", "INSTALLER"), "3.28",
         "PRISE DUPLEX 15A 120V")
cat_line("D-07", "Prise double DDFT / MALT isolée — relevé INSTALLER", por("PRISE DDFT", "INSTALLER"), "3.30",
         "PRISE DUPLEX 20A 125V GFI", note="DDFT 65,38 $ / 1,3 h (METHODE §1/§3)")
n_data_new = por("SORTIE DATA", "INSTALLER")
n_data_cond = DET["D-08"]["q"]
cat_line("D-08", "Sortie data murale/colonne avec conduit 3/4\" vers entreplafond (Détail D-08)", n_data_cond, "3.33", "TEL/DATA 3/4",
         note="quantité Détail D-08, comprise dans les %d sorties data INSTALLER du relevé" % n_data_new)
cat_line("D-17", "Sorties data neuves (boîte + plaque) — relevé INSTALLER moins D-08", n_data_new - n_data_cond, "3.33", "TEL/DATA")
jug_line("D-09", "Barrière anti-vol : raccord panneau de contrôle (PU-1 23)", DET["D-09"]["q"], "lot", "3.31", None,
         note="2 boîtes de jonction chiffrées en D-09b")
cat_line("D-09b", "Barrière anti-vol : 2 boîtes de jonction (relevé BOITE JONCTION INSTALLER)", 2, "3.31", "BOITE CARREES 4 PO")
jug_line("D-10", "Bornes de prêts / fontaine hall (P2-63)", DET["D-10"]["q"], "u", "3.31", None,
         note="1 boîte de jonction chiffrée en D-10b")
cat_line("D-10b", "Bornes de prêts : boîte de jonction (relevé BOITE JONCTION INSTALLER)", por("BOITE JONCTION", "INSTALLER") - 2, "3.31",
         "BOITE CARREES 4 PO")
cat_line("D-11", "Boutons d'appel / panique — boîte (système par d'autres) RDC + étage", DET["D-11"]["q"] + DET["E-06"]["q"], "3.31",
         "BOITE CARREES 4 PO", h=0.0, note="D-11 (1) + E-06 (3); temps en D-11b")
jug_line("D-11b", "Boutons d'appel / panique — conduit vide + raccord (D-11 + E-06)", DET["D-11"]["q"] + DET["E-06"]["q"], "u", "3.31", None,
         note="quantité Détail D-11 (1) + E-06 (3)", det="D-11")
cat_line("D-12", "Percement de dalle carotté + coupe-feu RDC (16 courses)", DET["D-12"]["q"], "3.31", "PERCEMENT PLANCHER",
         note="quantité Détail D-12")
cat_line("E-07", "Percement de dalle carotté + coupe-feu étage (7 courses)", DET["E-07"]["q"], "3.31", "PERCEMENT PLANCHER",
         note="quantité Détail E-07")
cat_line("D-13", "Conduit EMT 1\" vide sous dalle vers panneaux P-2/P-3 (16 courses, 480 m)", pi(DET["D-13"]["q"]), "3.31", "CONDUIT VIDE 1",
         note="longueur Détail D-13 (hypothèse 30 m/course)")
cat_line("D-14", "Conduit EMT 3/4\" data sous dalle (11 courses, 330 m)", pi(DET["D-14"]["q"]), "3.33", "CONDUIT VIDE 3/4",
         note="longueur Détail D-14 (hypothèse)")
cat_line("D-15", "Conducteur RW90 #12 Cu (5 cond./course, 2400 m)", pi(DET["D-15"]["q"]), "3.31", "12AWG SOLIDE RW90 600V",
         note="longueur Détail D-15")
jug_line("D-16", "Boîtes de tirage/jonction, connecteurs, supports, corde de tirage — conduits sous dalle (RDC)", DET["D-16"]["q"], "lot", "3.31", None)
lumen_line("D-16b", "Boîtes de tirage carrées 4-11/16\" (RDC, 2 par course x 16)", 32, "3.31", "IBE72171K",
           note="quantité = 2 x 16 courses (base Lumen: 23 courses x 2)")
lumen_line("D-16c", "Couvercles plats 4-11/16\" (RDC)", 32, "3.31", "IBE72C1")
lumen_line("D-16d", "Corde de tirage Poly Line 430 (conduits vides)", 1, "3.31", "GRE430")
cat_line("E-02", "Monument de plancher — relevé INSTALLER", por("MONUMENT PLANCHER", "INSTALLER"), "3.34", "MONUMENT PLANCHER",
         note="monument 250 $ (METHODE §1); remplace E-02 (2) + E-03 (2) du Détail")
cat_line("E-08", "Conduit EMT 1\" vide sous dalle étage (7 courses, 175 m)", pi(DET["E-08"]["q"]), "3.31", "CONDUIT VIDE 1",
         note="longueur Détail E-08")
cat_line("E-09", "Conduit EMT 3/4\" data sous dalle étage (7 courses, 175 m)", pi(DET["E-09"]["q"]), "3.33", "CONDUIT VIDE 3/4",
         note="longueur Détail E-09")
cat_line("E-10", "Conducteur RW90 #12 Cu étage (5 cond./course, 875 m)", pi(DET["E-10"]["q"]), "3.31", "12AWG SOLIDE RW90 600V",
         note="longueur Détail E-10")
jug_line("E-11", "Boîtes, connecteurs, supports — étage", DET["E-11"]["q"], "lot", "3.31", None)
lumen_line("E-11b", "Boîtes de tirage carrées 4-11/16\" (étage, 2 par course x 7)", 14, "3.31", "IBE72171K")
lumen_line("E-11c", "Couvercles plats 4-11/16\" (étage)", 14, "3.31", "IBE72C1")
cat_line("D-18", "Interrupteur simple 15A 120V — relevé INSTALLER", por("INT SIMPLE", "INSTALLER"), "3.35", "INTERRUPTEUR 15A 120V")
cat_line("D-19", "Thermostat — relevé INSTALLER", por("THERMOSTAT", "INSTALLER"), "3.23", "THERMOSTAT",
         note="thermostat 35 $ (METHODE §1)")
cat_line("D-20", "Lecteur de carte — relevé INSTALLER", por("LECTEUR CARTE", "INSTALLER"), "3.31", "LECTEUR DE CARTE",
         note="lecteur 15 $ (METHODE §1)")
cat_line("D-21", "Scan dalle béton (prix dans le lot GPR 1 250 $)", 1, "3.32", "SCAN DALLE BETON", p=0.0)

# ---- F. Éclairage (3.35) : luminaires 0 $ en ligne + lot --------------------------------------
cat_line("F-01", "Luminaire A1 Cooper 24CGTS 2'x4' encastré — relevé INSTALLER", por("LUMINAIRE A1", "INSTALLER"), "3.35", "FIXTURE TYPE A1",
         note="0 $ en ligne + lot éclairage")
cat_line("F-02", "Luminaire C1 Axis SL1 module 4'", por("LUMINAIRE C1", "INSTALLER"), "3.35", "FIXTURE TYPE C1",
         note="0 $ en ligne + lot éclairage")
cat_line("F-03", "Luminaire C1_1 Axis SL1 module 1'", por("LUMINAIRE C1_1", "INSTALLER"), "3.35", "FIXTURE TYPE C1",
         note="libellé C1_1 absent: FIXTURE TYPE C1 (0,75 h = luminaire METHODE §3); 0 $ en ligne + lot éclairage")
cat_line("F-04", "Luminaire C1_3 Axis SL1 module 3'", por("LUMINAIRE C1_3", "INSTALLER"), "3.35", "FIXTURE TYPE C1",
         note="libellé C1_3 absent: FIXTURE TYPE C1 (0,75 h = luminaire METHODE §3); 0 $ en ligne + lot éclairage")
jug_line("F-05", DET["F-05"]["desc"], DET["F-05"]["q"], "rangée", "3.35", None, note="trousses de suspension dans le lot éclairage")
cat_line("F-06", "Luminaire E GreenCreative cylindre suspendu — relevé INSTALLER (3, lot ×3)", por("LUMINAIRE E", "INSTALLER"), "3.35",
         "FIXTURE TYPE E", note="0 $ en ligne + lot éclairage; le Détail en compte 4 (hésitation)")
cat_line("F-07", "Enseigne de sortie Z6 Stanpro pictogramme", por("ENSEIGNE SORTIE Z6", "INSTALLER"), "3.35", "ENSEIGNE SORTIE Z6",
         note="0 $ en ligne + lot éclairage")
cat_line("F-08", "Conduit EMT 3/4\" + 3 #12 (raccordement luminaires sur circuits existants, 280 m) — inclut F-09",
         pi(DET["F-08"]["q"]), "3.35", "CONDUIT 3/4 03C12", note="longueur Détail F-08; assemblage 03C12 inclut les 3 conducteurs #12 (F-09)")
cat_line("F-10", "Boîtes de jonction octogonales éclairage (35 points)", 35, "3.35", "BOITE OCTOG 1-1/2PO KO 1",
         note="35 points = base Lumen/Détail F-08")

# ---- G. Alarme incendie (3.36 à 3.38) ------------------------------------------------------------
cat_line("G-01", "Détecteur de fumée neuf (fourni par JCI) — relevé INSTALLER", por("DETECTEUR FUMEE", "INSTALLER"), "3.36", "DETECTEUR FUMEE",
         note="0 $ en ligne + lot détecteurs 600 $; 0,5 h (METHODE §3)")
cat_line("G-01b", "Détecteur de fumée relocalisé — relevé RELOCALISER", por("DETECTEUR FUMEE", "RELOCALISER"), "3.36", "RELO DETECTEUR A FUME")
cat_line("G-02", "Conduit EMT 3/4\" vide boucle AI (30 m)", pi(DET["G-02"]["q"]), "3.36", "CONDUIT VIDE 3/4", note="longueur Détail G-02")
cat_line("G-03", "Câble AI FT4 2c #16 (boucle adressable, 60 m)", pi(DET["G-03"]["q"]), "3.36", "16AWG 1PR PVC FT4 600V",
         note="longueur Détail G-03")
cat_line("G-04", "Relocalisation panneau annonciateur Simplex", por("PANNEAU ANNONCIATEUR", "INSTALLER"), "3.37", "RELO PANN ANNOCIATEUR",
         note="annonciateur relocalisé 8 h (METHODE §3)")
jug_line("G-05", DET["G-05"]["desc"], DET["G-05"]["q"], "lot", "3.36", None)
jug_line("G-06", DET["G-06"]["desc"], DET["G-06"]["q"], "lot", "3.38", None)
jug_line("G-07", "Sous-traitance JCI/Simplex (bypass, programmation, vérification, certificat) — prix dans le lot JCI 7 400 $",
         DET["G-07"]["q"], "lot", "3.38", 0.0)

# ---- H. Frais de chantier (6.1) -------------------------------------------------------------------
cat_line("H-01", "Mobilisation / démobilisation, plateforme (nacelle)", DET["H-01"]["q"], "6.1", "NACELLE", u="lot",
         note="nacelle 1 250 $ / 16 h (METHODE §3)")
jug_line("H-02", DET["H-02"]["desc"], DET["H-02"]["q"], "lot", "6.1", None)
jug_line("H-03", DET["H-03"]["desc"], DET["H-03"]["q"], "lot", "6.1", None)
jug_line("H-04", DET["H-04"]["desc"], DET["H-04"]["q"], "lot", "6.1", None)

# ----------------------------------------------------------------------------------------------
# Totaux
# ----------------------------------------------------------------------------------------------
mat_lignes = sum(l["q"] * l["p"] for l in LIGNES)
mat_lots = sum(LOTS.values())
materiel = round(mat_lignes + mat_lots, 2)
heures_relevees = round(sum(l["q"] * l["h"] for l in LIGNES), 2)
heures_chargees = int(math.ceil(heures_relevees / 10.0 - 1e-12) * 10)
main_doeuvre = round(heures_chargees * TAUX, 2)
total_acceo = round(materiel + main_doeuvre, 2)
prix_vente = int(round(total_acceo * FACTEUR / 1000.0)) * 1000

# ventilation par article
par_article = {}
for l in LIGNES:
    a = par_article.setdefault(l["art"], {"materiel": 0.0, "heures": 0.0})
    a["materiel"] += l["q"] * l["p"]
    a["heures"] += l["q"] * l["h"]
for lot, rep in LOT_ART.items():
    if abs(sum(rep.values()) - LOTS[lot]) > 0.005:
        fail("ventilation du lot " + lot + " incohérente")
    for art, m in rep.items():
        a = par_article.setdefault(art, {"materiel": 0.0, "heures": 0.0})
        a["materiel"] += m


def cle_art(k):
    return tuple(int(x) for x in k.split("."))


par_article_out = {}
for k in sorted(par_article, key=cle_art):
    a = par_article[k]
    mat = round(a["materiel"], 2)
    hrs = round(a["heures"], 2)
    par_article_out[k] = {"materiel": mat, "heures": hrs, "total": round(mat + hrs * TAUX, 2)}

out = {
    "taux": TAUX,
    "materiel": materiel,
    "heures_relevees": heures_relevees,
    "heures_chargees": heures_chargees,
    "main_doeuvre": main_doeuvre,
    "total_acceo": total_acceo,
    "facteur": FACTEUR,
    "prix_vente": prix_vente,
    "lignes": LIGNES,
    "par_article": par_article_out,
    "lots": {k: round(v, 2) for k, v in LOTS.items()},
}

# contrôles de cohérence (échec = code de sortie != 0)
if abs(out["materiel"] + out["heures_chargees"] * out["taux"] - out["total_acceo"]) > 0.005:
    fail("total ACCEO incohérent")
if out["prix_vente"] != int(round(out["total_acceo"] * out["facteur"] / 1000.0)) * 1000:
    fail("prix de vente incohérent")
if abs(sum(v["materiel"] for v in par_article_out.values()) - out["materiel"]) > 0.05:
    fail("matériel par article incohérent")
if abs(sum(v["heures"] for v in par_article_out.values()) - out["heures_relevees"]) > 0.05:
    fail("heures par article incohérentes")
if out["heures_chargees"] < out["heures_relevees"] or out["heures_chargees"] % 10 != 0:
    fail("heures chargées incohérentes")

with open(P_OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("lignes=%d materiel=%.2f h_relevees=%.2f h_chargees=%d MO=%.2f total_acceo=%.2f prix_vente=%d" % (
    len(LIGNES), materiel, heures_relevees, heures_chargees, main_doeuvre, total_acceo, prix_vente))
