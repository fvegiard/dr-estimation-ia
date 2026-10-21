#!/usr/bin/env python3
"""Chiffrage « méthode Dupuis » à l'aveugle — S-1902 Bibliothèque Georgette-Lepage (Brossard).

Script autonome et déterministe (stdlib + openpyxl). Lit uniquement le kit du dossier courant :
  - releve.xlsx (Par libellé : totaux par famille) + rapport-releve.md (portées INSTALLER / ENLEVER / RELOCALISER / CONSERVER)
  - entree/reference-Estimation_2.xlsx (feuille Détail : hors plan + heures « à valider » ; feuille Matériel Lumen)
  - catalogue-prix-temps-dupuis.csv (colonnes prix_a_utiliser / temps_a_utiliser = dernier Dupuis, jamais la médiane)
Écrit chiffrage.json. Toute anomalie (libellé absent, total incohérent) lève une exception : code de sortie != 0.
"""
import csv
import json
import math
import os
import re
import sys

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------
# Paramètres de METHODE.md
# ----------------------------------------------------------------------------------------------
TAUX = 85.0          # $/h — dossiers août–octobre 2026 (S-1797, S-1835, S-1854, S-1881)
FACTEUR = 1.244      # prix de vente = total ACCEO × 1,244, arrondi au millier
PI_PAR_M = 3.28084   # pieds par mètre (conduits/filage : catalogue en $/pi)

# Lots fournisseur confirmés par Francis le 2026-10-20 (METHODE.md §2)
LOTS = {
    "Lot éclairage": 11893.0,
    "Lot distribution": 6200.0,       # NF 225 A 42 cct 3 400 + EDB 1P 95 x20 (1 900) + EJB 3P 300 x3 (900)
    "JCI alarme incendie": 7400.0,
    "JCI 2 détecteurs": 600.0,
    "GPR (scan dalle)": 1250.0,
}
LOT_DIST_PANNEAU = 3400.0
LOT_DIST_DISJ = 1900.0 + 900.0
assert LOT_DIST_PANNEAU + LOT_DIST_DISJ == LOTS["Lot distribution"]


# ----------------------------------------------------------------------------------------------
# Lecture du kit
# ----------------------------------------------------------------------------------------------
def lire_catalogue():
    cat = {}
    with open(os.path.join(HERE, "catalogue-prix-temps-dupuis.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            d = r["description"]
            if d in cat:
                cat[d] = None  # libellé ambigu (doublon) : refusé à l'usage
                continue
            # dernier Dupuis = colonnes « à utiliser » (== dernier_prix) ; jamais prix_unit_median
            cat[d] = {
                "um": r["um"],
                "prix": float(r["prix_a_utiliser"]),
                "temps": float(r["temps_a_utiliser"]),
                "date": r["date_dernier"],
                "classe": r["classe"],
            }
    return cat


def lire_releve():
    """Totaux par libellé (releve.xlsx) + portées (rapport-releve.md), recoupés."""
    wb = load_workbook(os.path.join(HERE, "releve.xlsx"), data_only=True)
    totaux = {}
    for lib, _fam, qte, *_ in list(wb["Par libellé"].iter_rows(values_only=True))[1:]:
        if lib:
            totaux[lib] = int(qte)
    marques = list(wb["Marques"].iter_rows(values_only=True))[1:]
    assert len(marques) == sum(totaux.values()), "Marques != Par libellé"

    portees = {}
    with open(os.path.join(HERE, "rapport-releve.md"), encoding="utf-8") as f:
        for ligne in f:
            m = re.match(r"\|\s*([A-Z0-9_ ]+?)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$", ligne)
            if not m or m.group(1) == "famille":
                continue
            fam, tot, txt = m.group(1), int(m.group(2)), m.group(3)
            p = {k: 0 for k in ("CONSERVER", "INSTALLER", "ENLEVER", "RELOCALISER")}
            for nom, n in re.findall(r"(CONSERVER|INSTALLER|ENLEVER|RELOCALISER)\s+(\d+)", txt):
                p[nom] += int(n)
            assert sum(p.values()) == tot, f"portées != total pour {fam}"
            assert totaux[fam] == tot, f"releve.xlsx != rapport pour {fam}"
            portees[fam] = p
    assert set(portees) == set(totaux), "familles rapport vs releve.xlsx"
    return portees


def lire_detail():
    wb = load_workbook(os.path.join(HERE, "entree", "reference-Estimation_2.xlsx"), data_only=True)
    det = {}
    for r in wb["Détail"].iter_rows(min_row=7, values_only=True):
        code = r[0]
        if code and re.match(r"^[A-H]-\d+$", str(code)):
            det[code] = {"desc": r[1], "q": r[3], "u": r[4], "h": r[7]}
    lumen = {}
    for r in wb["Matériel Lumen"].iter_rows(min_row=6, values_only=True):
        if r[0] and r[4] is not None:
            lumen[r[0]] = {"desc": r[1], "u": r[3], "prix": float(r[4])}
    return det, lumen


CAT = lire_catalogue()
PORT = lire_releve()
DET, LUMEN = lire_detail()


def P(fam, portee):
    return PORT[fam][portee]


def D(code):
    return DET[code]


def pi(m):
    return int(round(m * PI_PAR_M))


# ----------------------------------------------------------------------------------------------
# Construction des lignes
# ----------------------------------------------------------------------------------------------
LIGNES = []
CODES = set()


def ajoute(code, art, q, desc, u, p, h, src):
    assert code not in CODES, f"code en double {code}"
    CODES.add(code)
    LIGNES.append({"code": code, "desc": desc, "q": q, "u": u, "p": round(p, 4), "h": round(h, 4),
                   "art": art, "src": src})


def cat_ligne(code, art, q, lib, note, p=None, h=None, u=None, desc=None, motif_p=None):
    """Ligne issue du catalogue Dupuis (libellé exact). p/h = surcharge explicite et motivée."""
    row = CAT.get(lib)
    assert row is not None, f"libellé catalogue absent ou ambigu : {lib!r}"
    prix = row["prix"] if p is None else p
    temps = row["temps"] if h is None else h
    src = (f"catalogue Dupuis « {lib.strip()} » (dernier {row['date']} : {row['prix']} $ / {row['temps']} h par {row['um']}); {note}")
    if p is not None and p != row["prix"]:
        src += f"; prix en ligne forcé à {p} $ ({motif_p})"
    if h is not None and h != row["temps"]:
        src += f"; temps forcé à {h} h"
    ajoute(code, art, q, desc or lib.strip(), u or row["um"].lower().replace("p", "pi"), prix, temps, src)


def lumen_ligne(code, art, q, lcode, h, note, u=None, qdesc=None):
    row = LUMEN[lcode]
    src = (f"Lumen {lcode} « {row['desc']} » prix régulier 2026-10-07 : {row['prix']} $/{row['u']} (famille absente du catalogue Dupuis); "
           f"temps = jugement (Estimation_2) {h} h/u; {note}")
    ajoute(code, art, q, qdesc or row["desc"], u or row["u"], row["prix"], h, src)


def jugement_ligne(code, art, desc, q, u, p, h, note):
    d = DET[code.split(".")[0]]
    src = f"jugement (Estimation_2) {code.split('.')[0]} : {d['h']} h/{d['u']} « à valider »; {note}"
    ajoute(code, art, q, desc, u, p, h, src)


def lot_ligne(code, art, nom, montant, detail):
    ajoute(code, art, 1, nom, "lot", montant, 0.0,
           f"lot fournisseur confirmé par Francis le 2026-10-20 (METHODE.md) : {detail}")


# ============ 3.22 / 5.19 — Démontage, relocalisation, travaux temporaires ============
n_lum_enl = P("ENCASTRE", "ENLEVER") + P("LED 1X4", "ENLEVER") + P("LED 2X2", "ENLEVER")
cat_ligne("A-01", "3.22", n_lum_enl, "EQUIPEMENT A ENLEVER",
          "luminaires existants à enlever (relevé : ENCASTRE 26 + LED 1X4 6 + LED 2X2 8, portée ENLEVER) à 0,5 h (METHODE : luminaire enlevé 0,5 h); "
          "A-01/A-02 de l'Estimation_2 (39+7) fusionnés, répartition RDC/2e non récupérable du relevé",
          desc="EQUIPEMENT A ENLEVER — luminaires existants (E.A.E)")
n_prise_enl = P("PRISE DDFT", "ENLEVER") + P("PRISE DOUBLE 15A", "ENLEVER") + P("SORTIE DATA", "ENLEVER")
cat_ligne("A-03", "3.22", n_prise_enl, "ENLEVER PRISE",
          "prises DDFT 4 + doubles 7 + sorties data 17 (portée ENLEVER) ; A-03/A-04 fusionnés",
          desc="ENLEVER PRISE — prises et sorties data existantes (E.A.E)")
cat_ligne("R-01", "3.22", P("INT SIMPLE", "ENLEVER"), "ENLEVER INTERRUPTEUR",
          "interrupteur simple (portée ENLEVER)")
n_div = (P("MONUMENT PLANCHER", "ENLEVER") + P("BOITE JONCTION", "ENLEVER") + P("BOITIER C", "ENLEVER")
         + P("DETECTEUR FUMEE", "ENLEVER") + P("DETECTEUR MOUVEMENT", "ENLEVER") + P("HP ENCASTRE PLAFOND", "ENLEVER"))
cat_ligne("R-02", "3.22", n_div, "EQUIPEMENT A ENLEVER",
          "monuments 3 + boîtes de jonction 2 + boîtiers C 2 + détecteur fumée 1 + détecteur mouvement 1 + haut-parleur 1 (portée ENLEVER)",
          desc="EQUIPEMENT A ENLEVER — services et dispositifs divers (E.A.E)")
n_relo_prise = P("PRISE DOUBLE 15A", "RELOCALISER") + P("PRISE DDFT", "RELOCALISER") + P("SORTIE DATA", "RELOCALISER")
cat_ligne("A-05", "3.22", n_relo_prise, "RELO PRISE",
          "prises doubles 8 + DDFT 1 + sorties data 3 (portée RELOCALISER); Estimation_2 comptait 13")
cat_ligne("A-06", "3.22", P("ENCASTRE", "RELOCALISER"), "RELO ENCASTRE",
          "encastrés (portée RELOCALISER); Estimation_2 comptait 7 (dont 4 salle 227)")
jugement_ligne("A-07", "3.22", "Relocalisation interrupteurs maîtres du hall (note 1 E-201)", D("A-07")["q"], "lot", 0.0, D("A-07")["h"],
               "hors plan, famille « lot » absente du catalogue (RELO INT 1,5 h/u exige un nombre inconnu)")
jugement_ligne("G-05", "3.22", "Démontage/protection/réinstallation dispositifs AI existants dans zones touchées",
               D("G-05")["q"], "lot", 0.0, D("G-05")["h"], "allocation hors plan, famille absente du catalogue")

# FabLab 210 : retrait temporaire + réinstallation (hors plan, quantités Détail)
cat_ligne("A-08", "5.19", D("A-08")["q"], "EQUIPEMENT A ENLEVER",
          "FabLab 210 : retrait temporaire des luminaires linéaires existants (qté Estimation_2 A-08, comptée sur plan)",
          desc="EQUIPEMENT A ENLEVER — FabLab 210 linéaires existants (retrait temporaire)")
cat_ligne("A-08.2", "5.19", D("A-08")["q"], "FIXTURE 2X2 EXISTANT RE",
          "FabLab 210 : réinstallation des luminaires linéaires existants (qté Estimation_2 A-08)",
          desc="FIXTURE 2X2 EXISTANT RE — FabLab 210 linéaires (réinstallation)")
cat_ligne("A-09", "5.19", D("A-09")["q"], "EQUIPEMENT A ENLEVER",
          "FabLab 210 : retrait temporaire des encastrés existants (qté Estimation_2 A-09, ±2)",
          desc="EQUIPEMENT A ENLEVER — FabLab 210 encastrés existants (retrait temporaire)")
cat_ligne("A-09.2", "5.19", D("A-09")["q"], "FIXTURE 2X2 EXISTANT RE",
          "FabLab 210 : réinstallation des encastrés existants (qté Estimation_2 A-09)",
          desc="FIXTURE 2X2 EXISTANT RE — FabLab 210 encastrés (réinstallation)")
jugement_ligne("A-11", "5.19", "Maintien continuité de service, traçage circuits existants, réalimentation circuits libérés",
               D("A-11")["q"], "lot", 0.0, D("A-11")["h"], "hypothèse hors plan (catalogue : IDENTIFIER LES CIRCUITS EXISTANTS 3 h/u seulement, lot non chiffrable)")

# Toit : 6 moteurs monophasés à relocaliser (E-103) — débrancher / rebrancher
n_moteur_reloc = P("MOTEUR MONOPHASE", "RELOCALISER")
cat_ligne("A-10", "3.23", n_moteur_reloc, "DEBRANCHEMENT APPAREILAGE MECANIQUE",
          "toit E-103 : débrancher équipements de ventilation à relocaliser (relevé MOTEUR MONOPHASE RELOCALISER 6)")
cat_ligne("A-10.2", "3.23", n_moteur_reloc, "MOTEUR",
          "toit E-103 : rebrancher les moteurs relocalisés (0,75 h/moteur, METHODE)")

# ============ 3.24 / 3.25 — Distribution ============
cat_ligne("B-01", "3.24", D("B-01")["q"], "PANNEAU 100A 347/600V 3F",
          "panneau PP-3 neuf 225 A 347/600 V (METHODE : panneau 8 h); panneau fourni par le lot distribution",
          p=0.0, motif_p="panneaux 0 $ en ligne + lot distribution")
lot_ligne("LOT-DIST-1", "3.24", "Lot distribution — panneau NF 225 A 42 cct", LOT_DIST_PANNEAU, "NF 225 A 42 cct 3 400 $")
for code in ("B-02", "B-06", "B-07"):
    cat_ligne(code, "3.25", D(code)["q"], "DISJ15A1P", f"disjoncteurs 1P (qté Estimation_2 {code}); fournis par le lot distribution (EDB 1P)")
cat_ligne("B-08", "3.25", D("B-08")["q"], "DISJ 20A 1P 120V 10KA", "disjoncteurs 1P-20A machine de tri (qté Estimation_2 B-08)",
          p=0.0, motif_p="disjoncteurs fournis par le lot distribution (EDB 1P 95 $)")
for code in ("B-03", "B-04", "B-05"):
    cat_ligne(code, "3.25", D(code)["q"], "DISJ 100A 3P 120/240V 22 K",
              f"disjoncteur 3P 1 h (METHODE : disjoncteur 3P 1 h) (qté Estimation_2 {code}); fourni par le lot distribution (EJB 3P)",
              p=0.0, motif_p="disjoncteurs fournis par le lot distribution (EJB 3P 300 $)")
lot_ligne("LOT-DIST-2", "3.25", "Lot distribution — disjoncteurs EDB 1P x20 + EJB 3P x3", LOT_DIST_DISJ, "EDB 1P 95 $ x20 + EJB 3P 300 $ x3 = 2 800 $")
jugement_ligne("B-09", "3.24", "Mise à jour fiches dactylographiées + identification des panneaux", D("B-09")["q"], "u", 0.0, D("B-09")["h"],
               "famille absente du catalogue")

# ============ 3.23 / 3.26 — Raccordements mécaniques ============
cat_ligne("C-01", "3.23", D("C-01")["q"], "MOTEUR UAF-1",
          "UTA-01 au toit (METHODE : UTA 1 h); relevé MOTEUR TRIPHASE INSTALLER 4 = UTA + VE-02N + 2 chaudières")
cat_ligne("C-02", "3.23", D("C-02")["q"], "MOTEUR", "VE-02N Plymovent au toit (moteur 0,75 h)")
cat_ligne("C-03", "3.26", D("C-03")["q"], "MOTEUR", "chaudières CH-01/CH-02, tiroirs CCM-1 réutilisés (moteur 0,75 h)")
cat_ligne("C-04", "3.23", D("C-04")["q"], "MOTEUR", "humidificateurs HUM-1/2/3 (relevé MOTEUR MONOPHASE INSTALLER 3)")
lumen_ligne("C-04.2", "3.23", D("C-04")["q"], "HUBHBL1372", 2.0,
            "sectionneur 30 A sans fusible 1Ø des 3 humidificateurs; temps 2 h/u = catalogue « SECTIONNEURS SANS FUSIBLES 30A »")
cat_ligne("C-05", "3.23", pi(D("C-05")["q"]), "CONDUIT 1 04C08",
          "alimentation UTA-01 : EMT 1\" + 4 #8 (C-05+C-06 Estimation_2), 35 m converti en pi", u="pi")
cat_ligne("C-07", "3.23", pi(35), "CONDUIT 3/4 04C12",
          "alimentation VE-02N : EMT 3/4\" + 4 #12, 35 m (part de C-07/C-08 Estimation_2)", u="pi")
cat_ligne("C-08", "3.23", pi(3 * 15), "CONDUIT 3/4 03C12",
          "humidificateurs : EMT 3/4\" + 3 #12, 3 x 15 m (part de C-07/C-08 Estimation_2)", u="pi")
cat_ligne("R-03", "3.23", pi(14), "COND FLEX ETANCHE 3/4PO 30M ACIER",
          "raccords LFMC 3/4\" (14 m selon liste Lumen : UTA, VE-02N, HUM x3, CH x2)", u="pi")
lumen_ligne("R-03.2", "3.23", 20, "THO5333", 0.0, "connecteurs Conseal; pose comprise dans les lignes de raccordement")
cat_ligne("R-04", "3.23", P("THERMOSTAT", "INSTALLER"), "THERMOSTAT", "thermostats (portée INSTALLER)")

# ============ 3.27 à 3.34 — Services ============
cat_ligne("R-05", "3.27", P("PRISE USB", "INSTALLER"), "PRISE USB 125V 15 AMP", "prises USB Leviton Decora (portée INSTALLER)")
cat_ligne("R-06", "3.28", P("PRISE DOUBLE 15A", "INSTALLER"), "PRISE DUPLEX 15A 120V", "prises doubles 15 A (portée INSTALLER)")
cat_ligne("R-07", "3.30", P("PRISE DDFT", "INSTALLER"), "PRISE DUPLEX 20A 125V GFI",
          "prises DDFT (portée INSTALLER); variante MALT isolée (3.29) non distinguable au relevé, tout en 3.30")
n_data3_4 = D("D-08")["q"]
cat_ligne("D-08", "3.33", n_data3_4, "TEL/DATA 3/4",
          "sorties data murales/colonne avec conduit 3/4\" (qté Estimation_2 D-08), prélevées sur les 65 sorties INSTALLER")
cat_ligne("R-08", "3.33", P("SORTIE DATA", "INSTALLER") - n_data3_4, "TEL/DATA",
          "sorties data (relevé SORTIE DATA INSTALLER 65 moins les 10 de D-08)")
cat_ligne("E-02", "3.34", P("MONUMENT PLANCHER", "INSTALLER"), "MONUMENT PLANCHER",
          "monuments de plancher (portée INSTALLER 3; Estimation_2 : 2 + E-03 2 'à confirmer', fusionnés)")
cat_ligne("D-12", "3.31", D("D-12")["q"] + D("E-07")["q"], "PERCEMENT PLANCHER",
          "percements de dalle carottés : 16 (D-12) + 7 (E-07) courses (METHODE : percement 150 $ / 1 h)")
cat_ligne("D-12.2", "3.31", D("D-12")["q"] + D("E-07")["q"], "COUPE FEU TUBE 10.1 FL O",
          "coupe-feu CAN/ULC-S115 : 1 tube par percement")
cat_ligne("R-09", "3.32", 1, "SCAN DALLE BETON", "scan de la dalle (note 5 E-104)",
          p=0.0, motif_p="prix = lot GPR 1 250 $ ligne LOT-GPR")
lot_ligne("LOT-GPR", "3.32", "GPR — scan de dalle béton", LOTS["GPR (scan dalle)"], "GPR 1 250 $")
cat_ligne("D-13", "3.31", pi(D("D-13")["q"]), "CONDUIT VIDE 1",
          "EMT 1\" sous dalle vers P-2/P-3 (480 m en pi, hyp. Estimation_2 30 m/course)", u="pi")
cat_ligne("E-08", "3.31", pi(D("E-08")["q"]), "CONDUIT VIDE 1",
          "EMT 1\" sous dalle vers P-4/P-6 (175 m en pi, hyp. 25 m/course)", u="pi")
cat_ligne("D-15", "3.31", pi(D("D-15")["q"]), "12AWG SOLIDE RW90 600V",
          "RW90 #12 des courses RDC (5 cond./course, 2400 m en pi)", u="pi")
cat_ligne("E-10", "3.31", pi(D("E-10")["q"]), "12AWG SOLIDE RW90 600V",
          "RW90 #12 des courses étage (875 m en pi)", u="pi")
cat_ligne("D-14", "3.33", pi(D("D-14")["q"]), "CONDUIT VIDE 3/4",
          "EMT 3/4\" data sous dalle RDC (330 m en pi) (METHODE : conduit vide 3/4)", u="pi")
cat_ligne("E-09", "3.33", pi(D("E-09")["q"]), "CONDUIT VIDE 3/4",
          "EMT 3/4\" data sous dalle étage (175 m en pi)", u="pi")
n_boites_tirage = 46
ajoute("D-16", "3.31", 1, "Boîtes de tirage 4-11/16 + couvercles, connecteurs, supports (RDC + étage)", "lot",
       n_boites_tirage * (LUMEN["IBE72171K"]["prix"] + LUMEN["IBE72C1"]["prix"]), D("D-16")["h"] + D("E-11")["h"],
       f"Lumen IBE72171K {LUMEN['IBE72171K']['prix']} $ + IBE72C1 {LUMEN['IBE72C1']['prix']} $ x {n_boites_tirage} (23 courses x 2); "
       f"temps = jugement (Estimation_2) D-16 {D('D-16')['h']} h + E-11 {D('E-11')['h']} h « à valider » (famille absente du catalogue); E-11 fusionné")
lumen_ligne("R-10", "3.31", 1, "GRE430", 0.0, "corde de tirage des conduits vides; temps compris dans D-16")
jugement_ligne("D-09", "3.31", "Barrière anti-vol : 2 boîtes de jonction + raccord panneau de contrôle", D("D-09")["q"], "lot",
               2 * (CAT["BOITE CARRE 2-1/8PO KO 1"]["prix"] + CAT["COUV CARRE 4PO VIERGE"]["prix"]), D("D-09")["h"],
               "hors plan; prix = 2 x (BOITE CARRE 2-1/8PO KO 1 + COUV CARRE 4PO VIERGE) catalogue Dupuis")
jugement_ligne("D-10", "3.31", "Bornes de prêts / fontaine hall — JB dans mur adjacent", D("D-10")["q"], "u",
               CAT["BOITE CARRE 2-1/8PO KO 1"]["prix"] + CAT["COUV CARRE 4PO VIERGE"]["prix"], D("D-10")["h"],
               "hors plan; prix = BOITE CARRE 2-1/8PO KO 1 + COUV CARRE 4PO VIERGE catalogue Dupuis")
cat_ligne("D-11", "3.31", D("D-11")["q"], "BOUTON HANDICAPE", "bouton d'appel (système fourni par d'autres), qté Estimation_2 D-11")
cat_ligne("E-06", "3.31", D("E-06")["q"], "BOUTON HANDICAPE", "boutons d'appel (2) + panique (1), qté Estimation_2 E-06")
cat_ligne("R-11", "3.31", P("BOITE JONCTION", "INSTALLER"), "BOITE CARRE 2-1/8PO KO 1", "boîtes de jonction (portée INSTALLER)")
cat_ligne("R-11.2", "3.31", P("BOITE JONCTION", "INSTALLER"), "COUV CARRE 4PO VIERGE", "couvercles des boîtes de jonction")
cat_ligne("R-12", "3.31", P("LECTEUR CARTE", "INSTALLER"), "LECTEUR CARTE", "lecteurs de carte (portée INSTALLER)")

# ============ 3.35 — Éclairage et contrôle ============
cat_ligne("F-01", "3.35", P("LUMINAIRE A1", "INSTALLER"), "FIXTURE TYPE A1", "luminaires A1 (INSTALLER 11); fournis par le lot éclairage",
          p=0.0, motif_p="luminaires 0 $ en ligne + lot éclairage")
cat_ligne("F-02", "3.35", P("LUMINAIRE C1", "INSTALLER"), "FIXTURE TYPE C1", "luminaires C1 Axis 4' (INSTALLER 12); lot éclairage",
          p=0.0, motif_p="luminaires 0 $ en ligne + lot éclairage")
cat_ligne("F-03", "3.35", P("LUMINAIRE C1_1", "INSTALLER"), "FIXTURE TYPE C1", "luminaires C1_1 Axis 1' (INSTALLER 6); même temps que C1; lot éclairage",
          p=0.0, motif_p="luminaires 0 $ en ligne + lot éclairage")
cat_ligne("F-04", "3.35", P("LUMINAIRE C1_3", "INSTALLER"), "FIXTURE TYPE C1", "luminaires C1_3 Axis 3' (INSTALLER 15); même temps que C1; lot éclairage",
          p=0.0, motif_p="luminaires 0 $ en ligne + lot éclairage")
cat_ligne("F-06", "3.35", P("LUMINAIRE E", "INSTALLER"), "FIXTURE TYPE E",
          "luminaires E cylindre suspendu (relevé 3, lot confirmé x3; Estimation_2 en comptait 4); lot éclairage",
          p=0.0, motif_p="luminaires 0 $ en ligne + lot éclairage")
cat_ligne("F-07", "3.35", P("ENSEIGNE SORTIE Z6", "INSTALLER"), "ENSEIGNE SORTIE Z6", "enseignes de sortie Z6 (INSTALLER 3); lot éclairage",
          p=0.0, motif_p="enseignes 0 $ en ligne + lot éclairage")
jugement_ligne("F-05", "3.35", "Rangées linéaires Axis : suspension aux tiges/câbles et alimentation de rangée", D("F-05")["q"], "rangée",
               0.0, D("F-05")["h"], "trousses de suspension dans le lot éclairage (1 500 $); hors plan, famille absente du catalogue")
cat_ligne("F-05.2", "3.35", 200, "TIGE FILETE 3/8PO", "tiges de suspension des luminaires (devis 16.5; 200 pi selon liste Lumen)", u="pi")
lumen_ligne("F-05.3", "3.35", 2, "VISDIA3/816BX50", 0.0, "ancrages drop-in à la dalle; pose comprise dans F-05")
cat_ligne("F-08", "3.35", pi(D("F-08")["q"]), "CONDUIT 3/4 03C12",
          "raccordement luminaires sur circuits existants (280 m en pi); F-09 (RW90 #12 3 cond.) compris dans l'assemblage 03C12", u="pi")
lumen_ligne("F-08.2", "3.35", 63, "THOABRH03830", 0.0, "flexible 3/8\" des 35 points d'éclairage (63 m); pose comprise dans F-08")
lumen_ligne("F-08.3", "3.35", 70, "IBE2210", 0.0, "connecteurs BX 3/8\" 90D; pose comprise dans F-08")
cat_ligne("F-10", "3.35", 35, "BOITE OCTOG 1-1/2PO KO 1", "boîtes de jonction éclairage (35 points, liste Lumen); F-10 Estimation_2 : 8 h ~ 35 x 0,2 h")
cat_ligne("R-13", "3.35", P("INT SIMPLE", "INSTALLER"), "INTERRUPTEUR 15A 120V", "interrupteurs simples (portée INSTALLER)")
lot_ligne("LOT-ECL", "3.35", "Lot éclairage (luminaires, enseignes Z6, trousses de suspension)", LOTS["Lot éclairage"],
          "A1 x11 185 $, Axis SL1 4' x12 290 $, 3' x15 230 $, 1' x6 110 $, trousses 1 500 $, E x3 475 $, Z6 x3 161,60 $ — total confirmé 11 893 $")

# ============ 3.36 à 3.38 — Alarme incendie ============
cat_ligne("G-01", "3.36", P("DETECTEUR FUMEE", "INSTALLER"), "DETECTEUR FUMEE", "détecteurs de fumée neufs (INSTALLER 2); fournis par JCI (lot)",
          p=0.0, motif_p="détecteurs 0 $ en ligne + lot JCI")
cat_ligne("R-14", "3.36", P("DETECTEUR FUMEE", "RELOCALISER"), "RELO DETECTEUR A FUME", "détecteur de fumée à relocaliser (RELOCALISER 1)")
lot_ligne("LOT-JCI-DET", "3.36", "JCI — 2 détecteurs de fumée", LOTS["JCI 2 détecteurs"], "2 détecteurs 600 $")
cat_ligne("G-02", "3.36", pi(D("G-02")["q"]), "CONDUIT VIDE 3/4", "boucle AI : EMT 3/4\" (30 m en pi)", u="pi")
cat_ligne("G-03", "3.36", pi(D("G-03")["q"]), "16AWG 1PR PVC FT4 600V ", "boucle AI : câble FT4 2c #16 (60 m en pi)", u="pi")
cat_ligne("G-04", "3.37", P("PANNEAU ANNONCIATEUR", "INSTALLER"), "RELO PANN ANNOCIATEUR",
          "annonciateur Simplex relocalisé 8 h (METHODE); relevé PANNEAU ANNONCIATEUR 1 (libellé catalogue orthographié ANNOCIATEUR)")
jugement_ligne("G-06", "3.38", "Assistance électricien lors de la programmation / vérification ULC-S537", D("G-06")["q"], "lot", 0.0, D("G-06")["h"],
               "hors plan, famille absente du catalogue")
lot_ligne("LOT-JCI", "3.38", "JCI/Simplex — bypass, programmation 4007ES, vérification S537, certificat", LOTS["JCI alarme incendie"], "JCI 7 400 $")

# ============ 6.1 — Frais de chantier ============
cat_ligne("H-01", "6.1", D("H-01")["q"], "NACELLE", "mobilisation, plateforme/nacelle (METHODE : nacelle 1 250 $ / 16 h)")
for code, desc in (("H-02", "Coordination EG / multi-corps, dessins d'atelier, plans tel que construit"),
                   ("H-03", "Essais, mise en service, vérification des prises existantes, étiquetage"),
                   ("H-04", "Nettoyage, gestion des déchets")):
    jugement_ligne(code, "6.1", desc, D(code)["q"], "lot", 0.0, D(code)["h"], "hypothèse hors plan, famille absente du catalogue")

# ----------------------------------------------------------------------------------------------
# Totaux
# ----------------------------------------------------------------------------------------------
def r2(x):
    return round(x + 0.0, 2)


materiel = r2(sum(r2(l["q"] * l["p"]) for l in LIGNES))
heures_relevees = round(sum(l["q"] * l["h"] for l in LIGNES), 4)
heures_chargees = int(math.ceil(round(heures_relevees, 6) / 10.0) * 10)
main_doeuvre = r2(heures_chargees * TAUX)
total_acceo = r2(materiel + main_doeuvre)
prix_vente = int(round(total_acceo * FACTEUR / 1000.0)) * 1000

ARTICLES = [f"3.{n}" for n in range(22, 39)] + ["5.19", "6.1"]  # articles électricité du bordereau (3.29 : aucune ligne distincte)
par_article = {a: {"materiel": 0.0, "heures": 0.0, "total": 0.0} for a in ARTICLES}
for l in LIGNES:
    assert l["art"] in par_article, l["art"]
    l_art = l["art"]

    a = par_article[l_art]
    a["materiel"] += r2(l["q"] * l["p"])
    a["heures"] += l["q"] * l["h"]
for a in par_article.values():
    a["materiel"] = r2(a["materiel"])
    a["heures"] = round(a["heures"], 2)
    a["total"] = r2(a["materiel"] + a["heures"] * TAUX)
par_article = dict(sorted(par_article.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]))

lots = dict(LOTS)

# Cohérences exigées
assert abs(materiel + heures_chargees * TAUX - total_acceo) < 0.005, "materiel + heures_chargees x taux != total_acceo"
assert prix_vente == int(round(total_acceo * FACTEUR / 1000.0)) * 1000
assert heures_chargees % 10 == 0 and heures_chargees >= heures_relevees and heures_chargees - heures_relevees < 10
assert abs(sum(a["materiel"] for a in par_article.values()) - materiel) < 0.01, "par_article matériel"
assert abs(sum(a["heures"] for a in par_article.values()) - heures_relevees) < 0.05, "par_article heures"
lots_en_lignes = sum(l["q"] * l["p"] for l in LIGNES if l["code"].startswith("LOT-"))
assert abs(lots_en_lignes - sum(lots.values())) < 0.005, "lots != lignes LOT-"

sortie = {
    "taux": TAUX,
    "materiel": materiel,
    "heures_relevees": round(heures_relevees, 2),
    "heures_chargees": heures_chargees,
    "main_doeuvre": main_doeuvre,
    "total_acceo": total_acceo,
    "facteur": FACTEUR,
    "prix_vente": prix_vente,
    "lignes": LIGNES,
    "par_article": par_article,
    "lots": lots,
}
chemin = os.path.join(HERE, "chiffrage.json")
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(sortie, f, ensure_ascii=False, indent=2)

# Relecture de contrôle
with open(chemin, encoding="utf-8") as f:
    relu = json.load(f)
assert list(relu.keys()) == ["taux", "materiel", "heures_relevees", "heures_chargees", "main_doeuvre", "total_acceo",
                             "facteur", "prix_vente", "lignes", "par_article", "lots"]
assert abs(relu["materiel"] + relu["heures_chargees"] * relu["taux"] - relu["total_acceo"]) < 0.005
print(f"taux={TAUX} materiel={materiel} heures_relevees={sortie['heures_relevees']} heures_chargees={heures_chargees} "
      f"main_doeuvre={main_doeuvre} total_acceo={total_acceo} facteur={FACTEUR} prix_vente={prix_vente} lignes={len(LIGNES)}")
sys.exit(0)
