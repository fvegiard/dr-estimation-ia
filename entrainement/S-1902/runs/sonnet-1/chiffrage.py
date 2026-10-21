#!/usr/bin/env python3
"""Chiffrage « méthode Dupuis » — dossier S-1902 (Bibliothèque Georgette-Lepage, Brossard).

Script autonome et déterministe (stdlib + openpyxl). Lit le kit dans son propre dossier :
  - releve.xlsx + rapport-releve.md      quantités sur plan (famille x portée)
  - entree/reference-Estimation_2.xlsx   feuille Détail (quantités hors plan, heures « à valider »),
                                         feuille Matériel Lumen (familles absentes du catalogue)
  - entree/reference-Bordereau_de_prix.xlsx  (contrôle des articles)
  - catalogue-prix-temps-dupuis.csv      colonnes prix_a_utiliser / temps_a_utiliser (dernier Dupuis, jamais la médiane)
  - METHODE.md                           taux, facteur, lots confirmés
Écrit chiffrage.json. Toute anomalie (libellé introuvable/ambigu, quantité incohérente) lève une exception :
aucune erreur n'est masquée.
"""
import csv
import json
import math
import os
import re
import sys

import openpyxl

ICI = os.path.dirname(os.path.abspath(__file__))
M_VERS_PI = 1 / 0.3048


def chemin(*p):
    return os.path.join(ICI, *p)


# --------------------------------------------------------------------------- lecture des entrées
def lire_methode():
    txt = open(chemin("METHODE.md"), encoding="utf-8").read()
    m = re.search(r"\*\*taux\*\*\s*:\s*(\d+)\s*\$/h sur ses dossiers d'août–octobre 2026", txt)
    if not m:
        raise RuntimeError("taux introuvable dans METHODE.md")
    taux = float(m.group(1))
    m = re.search(r"total ACCEO \* ?× \*\*(\d+),(\d+)\*\*", txt) or re.search(r"× \*\*(\d+),(\d+)\*\*", txt)
    if not m:
        raise RuntimeError("facteur introuvable dans METHODE.md")
    facteur = float(m.group(1) + "." + m.group(2))
    return taux, facteur


def lire_catalogue():
    rows = list(csv.DictReader(open(chemin("catalogue-prix-temps-dupuis.csv"), encoding="utf-8-sig"), delimiter=";"))
    return rows


CAT = lire_catalogue()


def cat(label):
    """Ligne du catalogue par libellé EXACT (espaces compris). PRIX À UTILISER / TEMPS À UTILISER."""
    m = [r for r in CAT if r["description"] == label]
    if len(m) != 1:
        raise RuntimeError("libellé catalogue absent ou ambigu (%d) : %r" % (len(m), label))
    r = m[0]
    return float(r["prix_a_utiliser"]), float(r["temps_a_utiliser"]), r


def lire_releve():
    """Quantités sur plan : {famille: {portée: n}} (rapport-releve.md) contrôlées contre releve.xlsx."""
    fam = {}
    for ligne in open(chemin("rapport-releve.md"), encoding="utf-8"):
        m = re.match(r"\|\s*([A-Z0-9_ ]+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", ligne)
        if not m or m.group(1) == "famille":
            continue
        portees = {}
        for part in m.group(3).split(","):
            nom, n = part.strip().rsplit(" ", 1)
            portees[nom] = int(n)
        if sum(portees.values()) != int(m.group(2)):
            raise RuntimeError("portées incohérentes pour " + m.group(1))
        fam[m.group(1)] = portees
    wb = openpyxl.load_workbook(chemin("releve.xlsx"), data_only=True)
    par_lib = {r[0]: r[2] for r in wb["Par libellé"].iter_rows(min_row=2, values_only=True) if r[0]}
    marques = {}
    for r in wb["Marques"].iter_rows(min_row=2, values_only=True):
        if r[2]:
            marques[r[2]] = marques.get(r[2], 0) + 1
    for k, portees in fam.items():
        t = sum(portees.values())
        if par_lib.get(k) != t or marques.get(k) != t:
            raise RuntimeError("releve.xlsx incohérent pour %s : portées %d, libellé %s, marques %s" % (k, t, par_lib.get(k), marques.get(k)))
    if set(fam) != set(par_lib):
        raise RuntimeError("familles du relevé différentes de celles du rapport")
    return fam


def lire_detail():
    wb = openpyxl.load_workbook(chemin("entree", "reference-Estimation_2.xlsx"), data_only=True)
    det = {}
    for r in wb["Détail"].iter_rows(min_row=1, values_only=True):
        code = r[0]
        if code and re.match(r"^[A-H]-\d+$", str(code)):
            det[code] = {"desc": r[1], "q": r[3], "u": r[4], "h": r[7]}
    lumen = {}
    for r in wb["Matériel Lumen"].iter_rows(values_only=True):
        if r[0] and r[4] is not None and isinstance(r[4], (int, float)) and r[2] is not None:
            lumen[r[0]] = {"desc": r[1], "q": r[2], "u": r[3], "p": r[4]}
    return det, lumen


def verifier_bordereau(articles):
    wb = openpyxl.load_workbook(chemin("entree", "reference-Bordereau_de_prix.xlsx"), data_only=True)
    presents = {str(r[0]) for r in wb.active.iter_rows(values_only=True) if r[0] is not None}
    manquants = [a for a in articles if a not in presents]
    if manquants:
        raise RuntimeError("articles absents du bordereau : %s" % manquants)


TAUX, FACTEUR = lire_methode()
REL = lire_releve()
DET, LUMEN = lire_detail()


def rel(famille, portee):
    return REL[famille].get(portee, 0)


def det_q(code, attendu_u=None):
    d = DET[code]
    return d["q"]


def det_m_en_pi(code):
    d = DET[code]
    if d["u"] != "m":
        raise RuntimeError(code + " n'est pas en mètres")
    return round(d["q"] * M_VERS_PI, 1)


def det_h(code):
    return DET[code]["h"]


# --------------------------------------------------------------------------- lots confirmés (METHODE.md §2, 2026-10-20)
LOTS = {
    "eclairage": 11893.0,            # A1 x11, Axis SL1 4'/3'/1', trousses, E x3, Z6 x3 (prix confirmés par Francis)
    "distribution": 6200.0,          # NF 225 A 42 cct 3 400 + EDB 1P 95 x20 + EJB 3P 300 x3
    "JCI": 7400.0,
    "detecteurs_JCI": 600.0,         # 2 détecteurs
    "GPR": 1250.0,                   # scan dalle béton (GPR)
}
LOTS_ART = {                          # ventilation des lots par article du bordereau
    "eclairage": {"3.35": 11893.0},
    "distribution": {"3.24": 3400.0, "3.25": 2800.0},
    "JCI": {"3.38": 7400.0},
    "detecteurs_JCI": {"3.36": 600.0},
    "GPR": {"3.32": 1250.0},
}

LIGNES = []


def ligne(code, desc, q, u, p, h, art, src):
    if q is None or q <= 0:
        raise RuntimeError("quantité nulle/absente : " + code)
    LIGNES.append({"code": code, "desc": desc, "q": q, "u": u, "p": round(p, 4), "h": round(h, 4), "art": art, "src": src})


def L_cat(code, desc, q, u, label, art, p=None, extra=""):
    """Ligne dont prix et temps viennent du catalogue Dupuis (dernier). p= surcharge du prix (ex. 0 car couvert par un lot)."""
    pc, hc, r = cat(label)
    prix = pc if p is None else p
    src = "Catalogue Dupuis « %s » (%s, dernier %s, prix %s $ / temps %s h)" % (label.strip(), r["classe"], r["date_dernier"], pc, hc)
    if p is not None:
        src += " — prix ramené à %s $ : %s" % (p, extra)
    elif extra:
        src += " — " + extra
    ligne(code, desc, q, u, prix, hc, art, src)


def L_jug(code, desc, q, u, p, h, art, src):
    ligne(code, desc, q, u, p, h, art, src)


# =========================================================================== A. DÉMANTÈLEMENT / RELOCALISATION
a = "5.19"   # démolition (retrait définitif E.A.E)
b = "3.22"   # démontage / relocalisation / retrait temporaire
L_cat("A-01", "Démantèlement encastrés existants (E.A.E) — relevé ENCASTRE ENLEVER", rel("ENCASTRE", "ENLEVER"), "u", "ENLEVER FIXTURE ENCAST", a)
L_cat("A-02", "Démantèlement luminaires LED 2x2 existants (E.A.E) — relevé LED 2X2 ENLEVER", rel("LED 2X2", "ENLEVER"), "u", "ENLEVER FIXTURE 2X2", a)
L_cat("A-02b", "Démantèlement luminaires LED 1x4 existants (E.A.E) — relevé LED 1X4 ENLEVER", rel("LED 1X4", "ENLEVER"), "u", "ENLEVER FIXTURE 1X4", a)
L_cat("A-03", "Démantèlement prises doubles + DDFT (E.A.E) — relevé PRISE DOUBLE 15A + PRISE DDFT ENLEVER",
      rel("PRISE DOUBLE 15A", "ENLEVER") + rel("PRISE DDFT", "ENLEVER"), "u", "ENLEVER PRISE", a)
L_cat("A-03b", "Démantèlement sorties data (E.A.E) — relevé SORTIE DATA ENLEVER", rel("SORTIE DATA", "ENLEVER"), "u", "ENLEVER PRISE", a,
      extra="libellé « prise » retenu par analogie pour une sortie data")
L_cat("A-03c", "Démantèlement boîtes de jonction, boîtiers C et monuments de plancher (E.A.E)",
      rel("BOITE JONCTION", "ENLEVER") + rel("BOITIER C", "ENLEVER") + rel("MONUMENT PLANCHER", "ENLEVER"), "u", "ENLEVER PRISE", a,
      extra="libellé « prise » retenu par analogie (2 JB + 2 boîtiers C + 3 monuments)")
L_cat("A-04", "Démantèlement interrupteur simple (E.A.E)", rel("INT SIMPLE", "ENLEVER"), "u", "ENLEVER INTERRUPTEUR", a)
L_jug("A-04b", "Démantèlement détecteur de mouvement, détecteur de fumée et haut-parleur encastré (E.A.E)",
      rel("DETECTEUR MOUVEMENT", "ENLEVER") + rel("DETECTEUR FUMEE", "ENLEVER") + rel("HP ENCASTRE PLAFOND", "ENLEVER"), "u", 0.0, 0.35, a,
      "jugement (Estimation_2) : pas de libellé « enlever détecteur/HP » au catalogue Dupuis; 0,35 h = temps ENLEVER PRISE / ENLEVER INTERRUPTEUR (Dupuis)")
L_cat("A-05", "Relocalisation prises (9) et sorties data (3) (E.A.R)",
      rel("PRISE DOUBLE 15A", "RELOCALISER") + rel("PRISE DDFT", "RELOCALISER") + rel("SORTIE DATA", "RELOCALISER"), "u", "RELO PRISE", b,
      extra="RELO PRISE retenu aussi pour les 3 sorties data")
L_cat("A-06", "Relocalisation luminaires encastrés (E.A.R)", rel("ENCASTRE", "RELOCALISER"), "u", "RELO ENCASTRE", b)
L_cat("A-06b", "Relocalisation détecteur de fumée (E.A.R)", rel("DETECTEUR FUMEE", "RELOCALISER"), "u", "RELO DETECTEUR A FUME", b)
L_jug("A-07", "Relocalisation interrupteurs maîtres du hall (note spécifique 1 E-201)", det_q("A-07"), "lot", 0.0, det_h("A-07"), b,
      "jugement (Estimation_2) Détail A-07 : 6 h, hypothèse à valider (aucune quantité d'interrupteurs au plan; RELO INT Dupuis = 1,5 h/u)")
L_cat("A-08", "FabLab 210 : retrait temporaire + réinstallation luminaires linéaires existants (qté Détail, comptés sur plan)",
      det_q("A-08"), "u", "RELO FIXTURE TYPE S7", b, extra="libellé « RELO fixture » retenu pour un retrait + réinstallation")
L_cat("A-09", "FabLab 210 : retrait temporaire + réinstallation encastrés existants (qté Détail, comptés sur plan ±2)",
      det_q("A-09"), "u", "RELO ENCASTRE", b)
L_cat("A-10", "Toit : débrancher moteurs/équipements de ventilation (E.A.R) — relevé MOTEUR MONOPHASE RELOCALISER",
      rel("MOTEUR MONOPHASE", "RELOCALISER"), "u", "ENLEVER MOTEUR 1/2 HP 6", b)
L_cat("A-10b", "Toit : rebrancher moteurs/équipements de ventilation après travaux de toiture",
      rel("MOTEUR MONOPHASE", "RELOCALISER"), "u", "MOTEUR", b)
L_jug("A-11", "Maintien de continuité de service, traçage circuits existants, réalimentation circuits libérés", det_q("A-11"), "lot", 0.0, det_h("A-11"), a,
      "jugement (Estimation_2) Détail A-11 : 16 h, hypothèse")

# =========================================================================== B. DISTRIBUTION / PANNEAUX (matériel = lot distribution)
L_cat("B-01", "Panneau PP-3 NEUF 225 A 347/600 V 42 cct (NF Schneider) — pose (fourniture au lot distribution)", det_q("B-01"), "u", "PANN PS2 225A 120/208V 3F", "3.24")
L_cat("B-01b", "Démantèlement ancien panneau PP-3 + transfert de charges", det_q("B-01"), "u", "ENL PANN 42CCT 120/208V", "3.24")
for code in ("B-02", "B-06", "B-07", "B-08"):
    L_cat(code, DET[code]["desc"] + " — fourniture au lot distribution (EDB 1P)", det_q(code), "u", "DISJ15A1P", "3.25")
for code in ("B-03", "B-04", "B-05"):
    L_cat(code, DET[code]["desc"] + " — fourniture au lot distribution (EJB 3P)", det_q(code), "u", "DISJ 100A 3P 120/240V 22 K", "3.25", p=0.0,
          extra="temps 3P seulement (1,0 h); matériel déjà dans le lot distribution (EJB 3P 300 $ x3)")
L_jug("B-09", DET["B-09"]["desc"], det_q("B-09"), "u", 0.0, det_h("B-09"), "3.24", "jugement (Estimation_2) Détail B-09 : 1 h/u, à valider")

# =========================================================================== C. RACCORDEMENTS MÉCANIQUES
# contrôle : 1+1+2 = 4 moteurs triphasés INSTALLER, 3 humidificateurs = 3 moteurs monophasés INSTALLER (plans E-105/E-106)
if det_q("C-01") + det_q("C-02") + det_q("C-03") != rel("MOTEUR TRIPHASE", "INSTALLER") or det_q("C-04") != rel("MOTEUR MONOPHASE", "INSTALLER"):
    raise RuntimeError("raccordements mécaniques C-01..C-04 incohérents avec le relevé des moteurs")
L_cat("C-01", "Raccordement UTA-01 York 575 V/3Ø au toit (sectionneur d'usine)", det_q("C-01"), "u", "MOTEUR UAF-1", "3.23",
      extra="UTA = unité d'air (UAF) — 1,0 h comme le temps « UTA 1 h » de METHODE.md")
L_cat("C-02", "Raccordement VE-02N Plymovent 1,5 HP 575 V/3Ø au toit", det_q("C-02"), "u", "MOTEUR VE-2 120V", "3.23")
L_cat("C-03", "Chaudières CH-01 / CH-02 600 V/3Ø : vérifier/réutiliser tiroirs CCM-1 + câbles existants, raccord final", det_q("C-03"), "u", "MOTEUR", "3.26")
L_cat("C-04", "Humidificateurs HUM-1/2/3 Carel 120 V/1Ø — raccordement", det_q("C-04"), "u", "HUMIDIFICATEUR", "3.23")
L_cat("C-04b", "Sectionneur sans fusible 30 A 1Ø pour humidificateurs", det_q("C-04"), "u", "SECTIONNEUR POR ENTRETIEN HUBHBL13R22", "3.23",
      extra="Hubbell, plus proche équivalent du HBL1372 de la liste Lumen")
L_cat("C-05", "Conduit EMT 1\" + RW90 4 #8 (3 + MALT) alim. UTA-01 de PP-3 (35 m) — assemblage 04C08 (C-06 fondu ici)", det_m_en_pi("C-05"), "pi",
      "CONDUIT 1 04C08", "3.23")
L_cat("C-07", "Conduit EMT 3/4\" + RW90 4 #12 alim. VE-02N (35 m) — assemblage 04C12 (fils fondus ici)", det_m_en_pi("C-05"), "pi", "CONDUIT 3/4 04C12", "3.23",
      extra="longueur 35 m = Détail C-05/C-06 (hypothèse)")
L_cat("C-07b", "Conduit EMT 3/4\" + RW90 3 #12 alim. humidificateurs (3 x 15 m) — assemblage 03C12 (C-08 fondu ici)",
      round((det_q("C-07") - 35) * M_VERS_PI, 1), "pi", "CONDUIT 3/4 03C12", "3.23")
L_cat("C-09", "Conduit flexible étanche 3/4\" (LFMC) raccords mécaniques (UTA, VE-02N, HUM x3, CH x2) — base Lumen CONCONSEAL 14 m",
      round(LUMEN["CONCONSEAL3/4"]["q"] * M_VERS_PI, 1), "pi", "COND FLEX ETANCHE 3/4PO 30M ACIER", "3.23")
L_cat("C-10", "Raccords étanches isolés 3/4\" pour LFMC — base Lumen THO5333 x20", LUMEN["THO5333"]["q"], "u",
      "RACCORD ETANCHE DROIT ISOLE 3/4 FONTE MALLEABL", "3.23")

# =========================================================================== D/E. SERVICES (appareils du relevé + travaux hors plan du Détail)
a31 = "3.31"
L_cat("P-01", "Prises doubles 15 A 120 V neuves — relevé PRISE DOUBLE 15A INSTALLER", rel("PRISE DOUBLE 15A", "INSTALLER"), "u", "PRISE DUPLEX 15A 120V", "3.28")
L_cat("P-02", "Prises doubles USB neuves — relevé PRISE USB INSTALLER", rel("PRISE USB", "INSTALLER"), "u", "PRISE USB 125V 15 AMP", "3.27")
L_cat("P-03", "Prises doubles DDFT (GFI) neuves — relevé PRISE DDFT INSTALLER", rel("PRISE DDFT", "INSTALLER"), "u", "PRISE DUPLEX 20A 125V GFI", "3.30",
      extra="variante MALT isolée (art. 3.29) non distinguée au relevé : tout en 3.30")
L_cat("P-04", "Sorties informatique/réseau neuves (boîte + conduit 3/4\" vers entreplafond) — relevé SORTIE DATA INSTALLER", rel("SORTIE DATA", "INSTALLER"), "u",
      "TEL/DATA 3/4", "3.33", extra="assemblage avec conduit 3/4\" (Détail D-08) plutôt que TEL/DATA plaque seule 13,96 $ / 0,63 h")
L_cat("P-05", "Interrupteurs simples neufs — relevé INT SIMPLE INSTALLER", rel("INT SIMPLE", "INSTALLER"), "u", "INTERRUPTEUR 15A 120V", "3.35")
L_cat("P-06", "Thermostats neufs — relevé THERMOSTAT INSTALLER", rel("THERMOSTAT", "INSTALLER"), "u", "THERMOSTAT", "3.23")
L_cat("P-07", "Lecteurs de carte neufs — relevé LECTEUR CARTE INSTALLER", rel("LECTEUR CARTE", "INSTALLER"), "u", "LECTEUR DE CARTE", a31)
L_cat("P-08", "Boîtes de jonction neuves (boîte carrée 4\") — relevé BOITE JONCTION INSTALLER", rel("BOITE JONCTION", "INSTALLER"), "u", "BOITE CARRE 2-1/8PO KO 1", a31)
L_cat("P-08b", "Couvercles de boîtes de jonction", rel("BOITE JONCTION", "INSTALLER"), "u", "COUV CARRE 4PO VIERGE", a31)
L_cat("P-09", "Monuments de plancher neufs — relevé MONUMENT PLANCHER INSTALLER", rel("MONUMENT PLANCHER", "INSTALLER"), "u", "MONUMENT PLANCHER", "3.34")

L_jug("D-09", DET["D-09"]["desc"], det_q("D-09"), "lot", 0.0, det_h("D-09"), a31, "jugement (Estimation_2) Détail D-09 : 6 h")
L_jug("D-10", DET["D-10"]["desc"], det_q("D-10"), "u", 0.0, det_h("D-10"), a31, "jugement (Estimation_2) Détail D-10 : 2 h")
L_cat("D-11", "Bouton d'appel aide au lecteur 116 — boîte (système fourni par d'autres)", det_q("D-11"), "u", "BOUTON HANDICAPE", a31)
L_cat("D-12", "Percement de dalle carotté (RDC, 1 par course)", det_q("D-12"), "u", "PERCEMENT PLANCHER", a31)
L_cat("D-13", "Conduit EMT 1\" sous dalle vers panneaux P-2/P-3 (16 courses x 30 m, hyp. Détail)", det_m_en_pi("D-13"), "pi", "COND TME 1PO", a31)
L_cat("D-14", "Conduit vide 3/4\" data sous dalle (11 courses x 30 m, hyp. Détail)", det_m_en_pi("D-14"), "pi", "CONDUIT VIDE 3/4", a31)
L_cat("D-15", "Conducteur RW90 #12 Cu (5 cond./course) — conduits D-13", round(DET["D-15"]["q"] * M_VERS_PI, 1), "pi", "12AWG SOLIDE RW90 600V", a31)
u_box = LUMEN["IBE72171K"]["p"] + LUMEN["IBE72C1"]["p"]
L_jug("D-16", "Boîtes de tirage 4-11/16\" + couvercles — conduits sous dalle RDC (2 par course)", 2 * det_q("D-12"), "u", u_box, 0.25, a31,
      "Lumen IBE72171K (%s $) + IBE72C1 (%s $), famille absente du catalogue; temps par jugement 0,25 h/u (= Détail D-16 : 8 h / 32 boîtes)" % (LUMEN["IBE72171K"]["p"], LUMEN["IBE72C1"]["p"]))
L_cat("E-06", "Boutons d'appel (2) + bouton de panique (1) — boîte (étage)", det_q("E-06"), "u", "BOUTON HANDICAPE", a31)
L_cat("E-07", "Percement de dalle carotté (étage, 1 par course)", det_q("E-07"), "u", "PERCEMENT PLANCHER", a31)
L_cat("E-08", "Conduit EMT 1\" sous dalle vers P-4/P-6 (7 courses x 25 m, hyp. Détail)", det_m_en_pi("E-08"), "pi", "COND TME 1PO", a31)
L_cat("E-09", "Conduit vide 3/4\" data sous dalle étage (7 courses x 25 m, hyp. Détail)", det_m_en_pi("E-09"), "pi", "CONDUIT VIDE 3/4", a31)
L_cat("E-10", "Conducteur RW90 #12 Cu (5 cond./course) — conduits E-08", round(DET["E-10"]["q"] * M_VERS_PI, 1), "pi", "12AWG SOLIDE RW90 600V", a31)
L_jug("E-11", "Boîtes de tirage 4-11/16\" + couvercles — conduits sous dalle étage (2 par course)", 2 * det_q("E-07"), "u", u_box, 0.25, a31,
      "Lumen IBE72171K + IBE72C1, famille absente du catalogue; temps par jugement 0,25 h/u (Détail E-11 : 4 h)")
L_cat("D-17", "Scan dalle béton avant percements — prix = lot GPR 1 250 $ (compté dans les lots)", 1, "lot", "SCAN DALLE BETON", "3.32", p=0.0,
      extra="le prix 1 250 $ du catalogue = lot GPR confirmé de METHODE.md, compté une seule fois dans les lots")

# =========================================================================== F. ÉCLAIRAGE (matériel = lot éclairage; temps seulement)
L_cat("F-01", "Luminaire A1 Cooper 24CGTS 2'x4' encastré 347 V — relevé LUMINAIRE A1", rel("LUMINAIRE A1", "INSTALLER"), "u", "FIXTURE TYPE A1", "3.35")
L_cat("F-02", "Luminaire C1 Axis SL1 module 4' — relevé LUMINAIRE C1", rel("LUMINAIRE C1", "INSTALLER"), "u", "FIXTURE TYPE C1", "3.35")
L_cat("F-03", "Luminaire C1_1 Axis SL1 module 1' — relevé LUMINAIRE C1_1", rel("LUMINAIRE C1_1", "INSTALLER"), "u", "FIXTURE TYPE C1", "3.35",
      extra="pas de libellé C1_1 au catalogue : temps du type C1")
L_cat("F-04", "Luminaire C1_3 Axis SL1 module 3' — relevé LUMINAIRE C1_3", rel("LUMINAIRE C1_3", "INSTALLER"), "u", "FIXTURE TYPE C1", "3.35",
      extra="pas de libellé C1_3 au catalogue : temps du type C1")
L_jug("F-05", DET["F-05"]["desc"], det_q("F-05"), "rangée", 0.0, det_h("F-05"), "3.35",
      "jugement (Estimation_2) Détail F-05 : 1 h/rangée; trousses de suspension dans le lot éclairage (1 500 $)")
L_cat("F-06", "Luminaire E GreenCreative cylindre suspendu — relevé LUMINAIRE E (3; l'estimation en compte 4, le lot en compte 3)",
      rel("LUMINAIRE E", "INSTALLER"), "u", "FIXTURE TYPE E", "3.35")
L_cat("F-07", "Enseigne de sortie Z6 Stanpro (pictogramme) — relevé ENSEIGNE SORTIE Z6", rel("ENSEIGNE SORTIE Z6", "INSTALLER"), "u", "ENSEIGNE SORTIE Z6", "3.35")
L_cat("F-08", "Conduit EMT 3/4\" + RW90 3 #12 — raccordement luminaires sur circuits existants (8 m x 35 points, hyp. Détail; F-09 fondu ici)",
      det_m_en_pi("F-08"), "pi", "CONDUIT 3/4 03C12", "3.35")
L_cat("F-10", "Boîtes de jonction éclairage (octogonales 4\"), 1 par point", int(round(DET["F-08"]["q"] / 8)), "u", "BOITE OCTOG 1-1/2PO KO 1", "3.35",
      extra="35 points = Détail F-08 (280 m / 8 m); remplace le forfait 8 h")
L_cat("F-11", "Tige filetée 3/8\" suspension luminaires à la dalle (devis 16.5) — quantité Lumen VISTF3/8", LUMEN["VISTF3/8"]["q"], "pi", "TIGE FILETE 3/8PO", "3.35")
L_jug("F-12", "Ancrages drop-in 3/8-16 (paquets de 50) — suspension à la dalle", LUMEN["VISDIA3/816BX50"]["q"], "pk", LUMEN["VISDIA3/816BX50"]["p"], 0.0, "3.35",
      "Lumen VISDIA3/816BX50 (famille absente du catalogue); temps compris dans F-05")

# =========================================================================== G. ALARME INCENDIE (détecteurs : lot JCI 600 $ + temps)
L_cat("G-01", "Détecteurs de fumée neufs (fournis par JCI/Simplex, installés par DR) — relevé DETECTEUR FUMEE INSTALLER", rel("DETECTEUR FUMEE", "INSTALLER"), "u",
      "DETECTEUR FUMEE", "3.36")
L_cat("G-02", "Conduit vide 3/4\" boucle alarme incendie (30 m, hyp.)", det_m_en_pi("G-02"), "pi", "CONDUIT VIDE 3/4", "3.36")
L_cat("G-03", "Câble AI FT4 2c #16 (boucle adressable, 60 m, hyp.)", round(DET["G-03"]["q"] * M_VERS_PI, 1), "pi", "COND ALARME 3/16 FT4", "3.36")
L_cat("G-04", "Relocalisation panneau annonciateur Simplex — relevé PANNEAU ANNONCIATEUR", rel("PANNEAU ANNONCIATEUR", "INSTALLER"), "u", "RELO PANN ANNOCIATEUR", "3.37")
L_jug("G-05", DET["G-05"]["desc"], det_q("G-05"), "lot", 0.0, det_h("G-05"), "3.38", "jugement (Estimation_2) Détail G-05 : 12 h, allocation à valider")
L_jug("G-06", DET["G-06"]["desc"], det_q("G-06"), "lot", 0.0, det_h("G-06"), "3.38", "jugement (Estimation_2) Détail G-06 : 8 h")

# =========================================================================== H. FRAIS DE CHANTIER
L_cat("H-01", "Mobilisation / démobilisation, outillage, plateforme/nacelle", det_q("H-01"), "lot", "NACELLE", "6.1")
for code in ("H-02", "H-03", "H-04"):
    L_jug(code, DET[code]["desc"], det_q(code), "lot", 0.0, det_h(code), "6.1", "jugement (Estimation_2) Détail %s : %s h" % (code, det_h(code)))


# --------------------------------------------------------------------------- totaux
def arrondi_millier(x):
    return int(math.floor(x / 1000.0 + 0.5)) * 1000


def main():
    articles = sorted({l["art"] for l in LIGNES} | {a for v in LOTS_ART.values() for a in v})
    verifier_bordereau(articles)
    for nom, tot in LOTS.items():
        if abs(sum(LOTS_ART[nom].values()) - tot) > 0.005:
            raise RuntimeError("ventilation du lot " + nom)

    mat_lignes = sum(l["q"] * l["p"] for l in LIGNES)
    materiel = round(mat_lignes + sum(LOTS.values()), 2)
    heures_relevees = round(sum(l["q"] * l["h"] for l in LIGNES), 2)
    heures_chargees = int(math.ceil(heures_relevees / 10.0 - 1e-9)) * 10
    main_doeuvre = round(heures_chargees * TAUX, 2)
    total_acceo = round(materiel + main_doeuvre, 2)
    prix_vente = arrondi_millier(total_acceo * FACTEUR)

    # ventilation par article : heures relevées majorées au prorata pour retomber sur les heures chargées
    k = heures_chargees / heures_relevees
    par = {}
    for l in LIGNES:
        d = par.setdefault(l["art"], {"materiel": 0.0, "heures": 0.0})
        d["materiel"] += l["q"] * l["p"]
        d["heures"] += l["q"] * l["h"] * k
    for nom, rep in LOTS_ART.items():
        for art, m in rep.items():
            par.setdefault(art, {"materiel": 0.0, "heures": 0.0})["materiel"] += m
    par_article = {}
    for art in sorted(par, key=lambda s: [int(x) for x in s.split(".")]):
        par_article[art] = {"materiel": round(par[art]["materiel"], 2), "heures": round(par[art]["heures"], 2)}
    # corrections d'arrondi sur le plus gros article pour que les sommes soient exactes
    gros = max(par_article, key=lambda a: par_article[a]["materiel"] + par_article[a]["heures"])
    par_article[gros]["materiel"] = round(par_article[gros]["materiel"] + materiel - sum(v["materiel"] for v in par_article.values()), 2)
    par_article[gros]["heures"] = round(par_article[gros]["heures"] + heures_chargees - sum(v["heures"] for v in par_article.values()), 2)
    for v in par_article.values():
        v["total"] = round(v["materiel"] + v["heures"] * TAUX, 2)
    ecart = round(total_acceo - sum(v["total"] for v in par_article.values()), 2)
    par_article[gros]["total"] = round(par_article[gros]["total"] + ecart, 2)

    # contrôles de cohérence
    assert abs(materiel + heures_chargees * TAUX - total_acceo) < 0.005, "materiel + heures_chargees x taux != total_acceo"
    assert prix_vente == arrondi_millier(total_acceo * FACTEUR), "prix_vente"
    assert abs(sum(v["materiel"] for v in par_article.values()) - materiel) < 0.01
    assert abs(sum(v["total"] for v in par_article.values()) - total_acceo) < 0.01
    assert len({l["code"] for l in LIGNES}) == len(LIGNES), "codes de ligne dupliqués"

    sortie = {
        "taux": TAUX,
        "materiel": materiel,
        "heures_relevees": heures_relevees,
        "heures_chargees": heures_chargees,
        "main_doeuvre": main_doeuvre,
        "total_acceo": total_acceo,
        "facteur": FACTEUR,
        "prix_vente": prix_vente,
        "lignes": LIGNES,
        "par_article": par_article,
        "lots": LOTS,
    }
    with open(chemin("chiffrage.json"), "w", encoding="utf-8") as f:
        json.dump(sortie, f, ensure_ascii=False, indent=2)
    print("lignes: %d | materiel %.2f | h relevees %.2f | h chargees %d | MO %.2f | total ACCEO %.2f | x%s -> prix de vente %d"
          % (len(LIGNES), materiel, heures_relevees, heures_chargees, main_doeuvre, total_acceo, FACTEUR, prix_vente))
    return 0


if __name__ == "__main__":
    sys.exit(main())
