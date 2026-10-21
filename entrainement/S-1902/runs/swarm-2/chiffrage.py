#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chiffrage.py — consolidation finale du chef (essaim 2, S-1902, méthode Dupuis, à l'aveugle).

Déterministe, stdlib + openpyxl. Lit UNIQUEMENT, dans ce dossier :
  - lots/directeur-A.json  (quantités : code, desc, q, u, art proposé, src)
  - lots/directeur-B.json  (prix/temps unitaires : code, p, h, art final, src ; lots ; codes hors A)
  - catalogue-prix-temps-dupuis.csv (contrôle : p == prix_a_utiliser, h == temps_a_utiliser du libellé cité ;
    valeurs des décisions du chef)
  - METHODE.md (taux et facteur lus dans le texte)
  - entree/reference-Bordereau_de_prix.xlsx (libellés des articles, openpyxl)
Écrit chiffrage.json. Code de sortie 0 seulement si toutes les cohérences passent.

Règles de jointure (ARCHITECTURE.md §4) : le plan (directeur A) gagne sur Détail pour q ; Dupuis dernier gagne
sur Lumen pour p/h ; Lumen gagne sur le jugement ; les décisions du chef sont dans DECISIONS ci-dessous, chacune
avec sa raison, et sont réappliquées à chaque exécution (rien n'est modifié dans lots/).
"""
import csv
import json
import math
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)

PI_PAR_M = 3.2808


def lire_json(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def lire_catalogue():
    """Catalogue Dupuis : {(description strippée, um): (prix_a_utiliser, temps_a_utiliser, date, projet)}."""
    cat = {}
    with open("catalogue-prix-temps-dupuis.csv", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            cle = (r["description"].strip(), r["um"].strip())
            cat[cle] = (float(r["prix_a_utiliser"]), float(r["temps_a_utiliser"]), r["date_dernier"], r["projet_dernier"])
    if len(cat) < 2000:
        raise SystemExit("catalogue incomplet : %d lignes" % len(cat))
    return cat


def valeur_catalogue(cat, libelle, um):
    cle = (libelle, um)
    if cle not in cat:
        raise SystemExit("libellé introuvable au catalogue : %r um=%s" % (libelle, um))
    return cat[cle]


def lire_parametres_methode():
    """Taux et facteur lus dans METHODE.md (85 $/h sur les dossiers d'août–octobre 2026 ; × 1,244)."""
    with open("METHODE.md", encoding="utf-8") as f:
        texte = f.read()
    m_taux = re.search(r"\*\*taux\*\*\s*:\s*(\d+)\s*\$/h sur ses dossiers d.ao[uû]t", texte)
    m_fact = re.search(r"total ACCEO × \*\*([\d,]+)\*\*", texte)
    if not m_taux or not m_fact:
        raise SystemExit("taux ou facteur introuvable dans METHODE.md")
    return float(m_taux.group(1)), float(m_fact.group(1).replace(",", "."))


def lire_articles_bordereau():
    import openpyxl
    wb = openpyxl.load_workbook("entree/reference-Bordereau_de_prix.xlsx", data_only=True)
    ws = wb["Bordereau de prix"]
    art = {}
    for row in ws.iter_rows(values_only=True):
        if row[0] is not None and isinstance(row[0], str) and re.fullmatch(r"\d+\.\d+", row[0]):
            art[row[0]] = row[1]
    return art


def libelle_cite(src):
    """Premier libellé « … » cité dans un src 'catalogue Dupuis « X » um=U (...)' ; None si composé/forcé/jugement."""
    if not src.startswith("catalogue Dupuis «"):
        return None
    if " + catalogue Dupuis" in src or "opération" in src or "forcé" in src or "composé" in src:
        return None
    m = re.match(r"catalogue Dupuis « (.+?) » um=(\w)", src)
    return (m.group(1).strip(), m.group(2)) if m else None


def arrondi_dizaine_sup(h):
    return int(math.ceil(round(h, 6) / 10.0) * 10)


def arrondi_millier(x):
    return int(round(x / 1000.0) * 1000)


# ----------------------------------------------------------------------------------------------------------
# Décisions du chef (Claude Fable 5.1). Chaque entrée : code → {champs remplacés} + raison. Réappliquées à chaque
# exécution ; les valeurs numériques viennent du catalogue (lues ici, jamais recopiées à la main).
# ----------------------------------------------------------------------------------------------------------
def decisions_du_chef(cat):
    vide1 = valeur_catalogue(cat, "CONDUIT VIDE 1", "P")
    fil12 = valeur_catalogue(cat, "12AWG SOLIDE RW90 600V", "P")
    scan = valeur_catalogue(cat, "SCAN DALLE BETON", "U")
    p_1po_5c12 = round(vide1[0] + 5 * fil12[0], 4)
    h_1po_5c12 = round(vide1[1] + 5 * fil12[1], 4)
    src_1po = ("catalogue Dupuis « CONDUIT VIDE 1 » um=P (dernier %s, %s) + 5 × catalogue Dupuis « 12AWG SOLIDE RW90 600V » "
               "um=P (dernier %s, %s) ; composé du chef : %.4f $/pi, %.3f h/pi" % (vide1[2], vide1[3], fil12[2], fil12[3],
                                                                                   p_1po_5c12, h_1po_5c12))
    return [
        {"code": "D-13", "p": p_1po_5c12, "h": h_1po_5c12, "src": src_1po,
         "raison": "Détail D-13 = conduit EMT 1 po + 5 #12 ; aucun « CONDUIT 1 05C12 » au catalogue. Le directeur B avait pris "
                   "« CONDUIT 3/4 05C12 » (3,4197 $/0,081 h) : même nombre de conducteurs mais diamètre 3/4 au lieu de 1 po. "
                   "Le chef garde le diamètre du plan et compose conduit vide 1 po + 5 fils #12 (dernières valeurs Dupuis), "
                   "option que B avait calculée et écartée (4,3787 $/0,095 h)."},
        {"code": "E-08", "p": p_1po_5c12, "h": h_1po_5c12, "src": src_1po,
         "raison": "même objet que D-13 (EMT 1 po + 5 #12 sous dalle, étage) : même composé."},
        {"code": "X-01", "ajout": True, "desc": "Scan de dalle béton (temps de l'électricien ; le 1 250 $ est porté par LOT-GPR)",
         "q": 1, "u": "U", "p": 0.0, "h": scan[1], "art": "3.32",
         "src": "catalogue Dupuis « SCAN DALLE BETON » um=U (dernier %s, %s) : p = 0 forcé (1 250 $ déjà dans LOT-GPR), "
                "h = %.1f ; q = 1 (bordereau 3.32, 23 percements D-12 + E-07)" % (scan[2], scan[3], scan[1]),
         "raison": "le directeur A avait exclu X-01 comme doublon de LOT-GPR (même 1 250 $) ; le directeur B signalait que le "
                   "temps Dupuis du scan (2 h) disparaissait avec lui. Le chef garde le lot pour le prix et rétablit la ligne "
                   "à 0 $ + 2 h : un objet payé une fois, le temps d'accompagnement compté une fois."},
    ]


DECISIONS_SANS_CHANGEMENT = [
    "LOT-ECL gardé à 11 893 $ (prix confirmé par Francis, METHODE.md §2) malgré la décomposition qui donne 13 034,80 $ : le "
    "montant confirmé fait foi, écart signalé dans incoherences.",
    "LE-I = 3 (3 étiquettes sur plan, lot éclairage E ×3) contre Détail F-06 = 4 : le plan gagne.",
    "MM-R (6 moteurs du toit) au composé Dupuis de B (débranchement 0,4 h + sectionneur enlevé 0,5 h + moteur 0,75 h = 1,65 h, "
    "25 $) plutôt qu'aux 4 h/u de Détail A-10 : le catalogue gagne sur le jugement.",
    "X-02 nacelle (1 250 $ / 16 h, pratique Dupuis) ET H-01 mobilisation (16 h, jugement) gardés tous deux : objets distincts "
    "(moyen d'accès vs mobilisation/outillage) ; le recouvrement « plateforme » de H-01 est signalé, pas chiffré deux fois.",
    "SD-I à « TEL/DATA 3/4 » 22,32 $ / 0,89 h (assemblage avec le bout de conduit 3/4 vers l'entreplafond, Détail D-08) plutôt "
    "qu'à « TEL/DATA » 13,96 $ / 0,63 h : l'objet du plan a un conduit ; les deux repères sont dans METHODE.md.",
    "Enlèvements de luminaires (ENC-E, L14-E, L22-E) à « EQUIPEMENT A ENLEVER » 0,5 h (= repère METHODE « luminaire enlevé "
    "0,5 h ») plutôt qu'à « ENLEVER FIXTURE ENCAST » 0,35 h : le repère METHODE décrit la pratique Dupuis récente.",
    "B-09 à 9 × « IDENTIFIER LES CIRCUITS EXISTANTS A » 3 h (27 h) et A-11 réduit à 12 h (NOTE 5 + NOTE 6 RETRACER) pour ne "
    "pas payer l'identification deux fois : arbitrage B conservé.",
    "Articles : la table du chef de lot B3 (règles R0–R13) fait foi sur les propositions de A (18 désaccords, tous tranchés "
    "pour B : -R et dépose → 3.22, conduits/fils → 3.31, boutons → 3.33, LC-I → 3.33). LOT-DIST ventilé 3 400 $ → 3.24 et "
    "2 800 $ → 3.25 dans par_article (règle R6 de B3).",
    "Les 61 codes chiffrés par B hors des lignes A (portées absentes du relevé, lignes Détail exclues par A) restent à "
    "quantité 0 : le plan gagne sur Détail pour les quantités.",
    "Lots fournisseur : présents une seule fois dans les lignes (q = 1, p = montant, h = 0) et repris tels quels dans `lots` ; "
    "le matériel les compte une fois.",
]


def main():
    A = lire_json("lots/directeur-A.json")
    B = lire_json("lots/directeur-B.json")
    cat = lire_catalogue()
    taux, facteur = lire_parametres_methode()
    articles = lire_articles_bordereau()

    b_par_code = {l["code"]: l for l in B["lignes"]}
    incoherences = []
    decisions = []

    # 1. Jointure A (q) × B (p, h, art)
    lignes = []
    codes_vus = set()
    for a in A["lignes"]:
        code = a["code"]
        if code in codes_vus:
            raise SystemExit("code en double dans directeur-A : " + code)
        codes_vus.add(code)
        if code not in b_par_code:
            raise SystemExit("code A sans prix/temps chez B : " + code)
        b = b_par_code[code]
        if a["u"] != b["u"]:
            incoherences.append("unité différente A/B pour %s : %s vs %s (unité A gardée)" % (code, a["u"], b["u"]))
        if a.get("art") != b.get("art"):
            decisions.append("article %s : A proposait %s, B (chef de lot B3) tranche %s — B retenu" % (code, a.get("art"), b.get("art")))
        lignes.append({
            "code": code, "desc": a["desc"], "q": a["q"], "u": a["u"],
            "p": float(b["p"]), "h": float(b["h"]), "art": b["art"],
            "src": "q : " + a["src"] + " || p/h : " + b["src"],
        })

    # 2. Contrôle du chef : p/h == catalogue pour chaque ligne à libellé unique cité par B
    verifies = 0
    for l in lignes:
        src_b = l["src"].split(" || p/h : ", 1)[1]
        lib = libelle_cite(src_b)
        if lib is None:
            continue
        if lib not in cat:
            incoherences.append("%s : libellé cité par B introuvable au catalogue : %r" % (l["code"], lib))
            continue
        p_cat, h_cat = cat[lib][0], cat[lib][1]
        if abs(l["h"] - h_cat) > 1e-9:
            incoherences.append("%s : h %s != temps_a_utiliser %s de %r" % (l["code"], l["h"], h_cat, lib))
        if abs(l["p"] - p_cat) > 1e-9 and "p = 0" not in src_b:
            incoherences.append("%s : p %s != prix_a_utiliser %s de %r" % (l["code"], l["p"], p_cat, lib))
        verifies += 1

    # 3. Décisions du chef
    par_code = {l["code"]: l for l in lignes}
    for d in decisions_du_chef(cat):
        if d.get("ajout"):
            if d["code"] in par_code:
                raise SystemExit("décision d'ajout sur un code déjà présent : " + d["code"])
            l = {"code": d["code"], "desc": d["desc"], "q": d["q"], "u": d["u"], "p": d["p"], "h": d["h"],
                 "art": d["art"], "src": "q : décision du chef || p/h : " + d["src"]}
            lignes.append(l)
            par_code[d["code"]] = l
            decisions.append("AJOUT %s : %s" % (d["code"], d["raison"]))
        else:
            l = par_code[d["code"]]
            avant = (l["p"], l["h"])
            l["p"], l["h"] = d["p"], d["h"]
            l["src"] = l["src"].split(" || p/h : ")[0] + " || p/h : " + d["src"]
            decisions.append("MODIF %s : p/h %s/%s → %s/%s — %s" % (d["code"], avant[0], avant[1], d["p"], d["h"], d["raison"]))
    decisions.extend(DECISIONS_SANS_CHANGEMENT)

    # 4. Lots (une seule fois : les lignes LOT-* portent le montant ; `lots` le répète pour le schéma)
    lots = dict(B["lots"])
    for nom, montant in lots.items():
        if nom not in par_code or abs(par_code[nom]["p"] * par_code[nom]["q"] - montant) > 0.005:
            raise SystemExit("lot %s absent des lignes ou montant différent" % nom)
    if abs(A["lots"]["LOT-ECL"] - lots["LOT-ECL"]) > 0.005:
        raise SystemExit("lot éclairage différent entre A et B")
    incoherences.append("LOT-ECL : décomposition de METHODE.md (11×185 + 12×290 + 15×230 + 6×110 + 1 500 + 3×475 + 3×161,60) = "
                        "13 034,80 $ contre 11 893 $ confirmé ; le confirmé est gardé (écart 1 141,80 $).")

    # 5. Totaux
    for l in lignes:
        l["montant"] = round(l["q"] * l["p"], 4)
        l["heures"] = round(l["q"] * l["h"], 4)
    materiel = round(sum(l["montant"] for l in lignes), 2)
    heures = round(sum(l["heures"] for l in lignes), 3)
    heures_chargees = arrondi_dizaine_sup(heures)
    main_doeuvre = round(heures_chargees * taux, 2)
    total_acceo = round(materiel + main_doeuvre, 2)
    prix_vente = arrondi_millier(total_acceo * facteur)

    # 6. Ventilation par article (LOT-DIST : 3 400 $ panneau → 3.24, 2 800 $ disjoncteurs → 3.25, règle R6 de B3)
    par_article = {}

    def ajoute(art, m, h):
        d = par_article.setdefault(art, {"materiel": 0.0, "heures": 0.0, "total": 0.0})
        d["materiel"] += m
        d["heures"] += h

    for l in lignes:
        if l["code"] == "LOT-DIST":
            ajoute("3.24", 3400.0, 0.0)
            ajoute("3.25", 2800.0, 0.0)
            continue
        ajoute(l["art"], l["montant"], l["heures"])
    for art, d in par_article.items():
        d["materiel"] = round(d["materiel"], 2)
        d["heures"] = round(d["heures"], 3)
        d["total"] = round(d["materiel"] + d["heures"] * taux, 2)
        d["libelle"] = articles.get(art, "?")
        if art not in articles:
            incoherences.append("article %s absent du bordereau" % art)
    par_article = dict(sorted(par_article.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]))

    # 7. Cohérences obligatoires
    assert abs(materiel + heures_chargees * taux - total_acceo) < 0.01, "materiel + heures_chargees×taux != total_acceo"
    assert prix_vente == arrondi_millier(total_acceo * facteur), "prix_vente != arrondi millier(total×facteur)"
    assert heures_chargees >= heures and heures_chargees % 10 == 0 and heures_chargees - heures < 10
    assert abs(sum(d["materiel"] for d in par_article.values()) - materiel) < 0.01, "par_article matériel != matériel"
    assert abs(sum(d["heures"] for d in par_article.values()) - heures) < 0.01, "par_article heures != heures"
    assert len({l["code"] for l in lignes}) == len(lignes), "code en double"
    part_mo = main_doeuvre / total_acceo
    h_par_100k = heures_chargees / (prix_vente / 100000.0)
    if not (0.30 <= part_mo <= 0.69):
        incoherences.append("part main-d'œuvre %.1f %% hors plage 30–69 %%" % (100 * part_mo))
    if not (450 <= h_par_100k <= 520):
        incoherences.append("%.0f h par 100 k$ de prix de vente, hors plage 450–520 (METHODE.md §6) — longueurs de conduits "
                            "de Détail (hypothèses 30/25 m par course) : non forcé" % h_par_100k)

    # 8. Écarts signalés par les directeurs (contradictions plan / Détail / kit), repris tels quels
    incoherences.extend([
        "Quantités sur plan issues d'un relevé automatique « à VÉRIFIER sur les planches de contrôle » (rapport-releve.md).",
        "Luminaires E.A.E : Détail A-01 + A-02 = 46 vs plan ENC-E 26 + L14-E 6 + L22-E 8 = 40 (plan retenu).",
        "Services E.A.E : Détail A-03 + A-04 = 44 vs plan 35 (PC-E 7, PG-E 4, SD-E 17, BJ-E 2, MP-E 3, BC-E 2) (plan retenu).",
        "Relocalisations : Détail A-05 13 vs plan 12 (PC-R 8, PG-R 1, SD-R 3) ; A-06 7 vs ENC-R 4 (plan retenu).",
        "USB : Détail D-02 10 vs plan PU-I 20 (plan retenu).",
        "Boîtes de jonction de l'étage (Détail E-01 2 + E-04 3) sans symbole BJ sur E105 : non chiffrées (plan retenu).",
        "DDFT et M.A.L.T. isolée confondues au relevé (R-007) : tout PG en 3.30, 3.29 à 0 $.",
        "B-04 disjoncteur UTA-1 40 A (E-502) vs MOCP 35 A (E-009) : à clarifier par l'ingénieur.",
        "Disjoncteurs 1P posés 19 (B-02 14 + B-06 1 + B-07 2 + B-08 2) vs 20 EDB dans LOT-DIST.",
        "Toutes les longueurs de conduits (C-05, C-07, D-13, D-14, E-08, E-09, F-08, G-02, G-03) sont des hypothèses de Détail "
        "(30 m / 25 m par course, 8 m × 35 points) ; relevé : « longueurs hors relevé ».",
        "A-11, G-05, G-06, H-01…H-04 : heures « jugement (Estimation_2) », aucun libellé Dupuis.",
        "Z6 sur E204 (1 des 3) vs relevé éclairage « aucun appareil neuf à l'étage » : 3 gardés (tableau E-008, lot ×3).",
        "Détecteurs de fumée : 3 des 10 marques sont le même objet dessiné sur E201 et E203 (CONSERVER seulement, sans effet).",
        "Schéma E-007 : 2 détecteurs neufs à l'étage vs plans : 2 au RDC (plans retenus).",
    ])

    sortie = {
        "dossier": "S-1902", "methode": "Dupuis (METHODE.md)", "essaim": "swarm-2 (chef Claude Fable 5.1)",
        "taux": taux, "facteur": facteur,
        "materiel": materiel,
        "heures": heures, "heures_relevees": heures,
        "heures_chargees": heures_chargees,
        "main_doeuvre": main_doeuvre,
        "total_acceo": total_acceo,
        "prix_vente": prix_vente,
        "controles": {"part_main_doeuvre_pct": round(100 * part_mo, 1), "h_par_100k_prix_vente": round(h_par_100k, 0),
                      "lignes_verifiees_au_catalogue": verifies, "nb_lignes": len(lignes)},
        "lots": lots,
        "lignes": lignes,
        "par_article": par_article,
        "decisions": decisions,
        "incoherences": incoherences,
    }
    with open("chiffrage.json", "w", encoding="utf-8") as f:
        json.dump(sortie, f, ensure_ascii=False, indent=1)
    # relecture
    relu = lire_json("chiffrage.json")
    for k in ("taux", "materiel", "heures_relevees", "heures_chargees", "main_doeuvre", "total_acceo", "facteur",
              "prix_vente", "lignes", "par_article", "lots", "heures", "decisions", "incoherences"):
        assert k in relu, "clé manquante : " + k
    print("lignes=%d  materiel=%.2f  heures=%.3f  heures_chargees=%d  taux=%.0f  MO=%.2f  total_acceo=%.2f  "
          "facteur=%.3f  prix_vente=%d  partMO=%.1f%%  h/100k=%.0f  verifiees=%d  incoherences=%d" % (
              len(lignes), materiel, heures, heures_chargees, taux, main_doeuvre, total_acceo, facteur, prix_vente,
              100 * part_mo, h_par_100k, verifies, len(incoherences)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
