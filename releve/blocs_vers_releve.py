# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "numpy>=1.26"]
# ///
"""Blocs vectoriels étiquetés → fichiers du relevé (`nomenclature.csv`, `occurrences-visuel.csv`, `feuilles-classement.csv`).

Entrées (WORKDIR) : `blocs/<feuille>.csv` + `blocs-index.csv` (blocs_vectoriels.py / blocs_vignettes.py), et
`blocs-familles.csv` écrit par l'agent après lecture des planches de signatures :
    sig_id,label,famille,forme,code,materiel,legende_no,diam_min,diam_max,feuilles,note
(diam_min/max en pt : une même signature invariante à l'échelle peut être une sortie data à 4 pt ET une flèche de
circuit à 12 pt ; `feuilles` : liste blanche de feuilles, vide = toutes).

Pour chaque bloc étiqueté : centre exact, boîte tournée (rectangle minimal du bloc : x0..y1 + angle_deg, familles
`carre`), rayon (cercles), portée lue sur l'étiquette voisine (E.A.E → ENLEVER, E.A.R → RELOCALISER, E.A.C → CONSERVER,
sinon défaut de la feuille : existant/démolition → CONSERVER, nouveau → INSTALLER), désignation = circuits et zones
voisins, type de luminaire (A1, C1, C1_1, C1_3, E, Z6…) lu à côté des luminaires → `modele` et label « LUMINAIRE <type> ».

Usage : uv run releve/blocs_vers_releve.py WORKDIR PDF
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, sys
from collections import Counter, defaultdict
import numpy as np
import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocs_vectoriels import MAX_COTE, MIN_COTE, MARGE_FUSION, _points  # noqa: E402
from legende import code_attendu  # noqa: E402

PORTEE_TAGS = {"E.A.E": "ENLEVER", "E.A.R": "RELOCALISER", "E.A.C": "CONSERVER", "E.A.D": "ENLEVER"}
TYPES_LUM = re.compile(r"^(A\d|B\d|C\d(_\d)?|D\d|E|G\d|Z\d)$")   # pas « F » seul : lettre de la station manuelle
CIRCUIT = re.compile(r"^(P{1,2}-?U?\d+|PR-\d+|\(?[A-Za-z]{1,2}(,[A-Za-z]{1,2})?\)?|\(M[a-z]\)|\d{1,2})$")


def rect_minimal(pts):
    """Rectangle minimal (centre, w, h, angle°) d'un nuage de points : rotation par les arêtes de l'enveloppe convexe."""
    P = np.unique(np.round(np.array(pts, dtype=float), 3), axis=0)
    if len(P) < 3:
        x0, y0 = P.min(axis=0); x1, y1 = P.max(axis=0)
        return (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, 0.0
    # enveloppe convexe (monotone chain)
    P = P[np.lexsort((P[:, 1], P[:, 0]))]
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(tuple(p))
    for p in P[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(tuple(p))
    H = np.array(lower[:-1] + upper[:-1])
    best = None
    for i in range(len(H)):
        e = H[(i + 1) % len(H)] - H[i]
        a = math.atan2(e[1], e[0]); ca, sa = math.cos(a), math.sin(a)
        u = H @ np.array([ca, sa]); v = H @ np.array([-sa, ca])
        w, h = u.max() - u.min(), v.max() - v.min()
        if best is None or w * h < best[0]:
            cu, cv = (u.max() + u.min()) / 2, (v.max() + v.min()) / 2
            best = (w * h, cu * ca - cv * sa, cu * sa + cv * ca, w, h, math.degrees(a))
    _, cx, cy, w, h, ang = best
    if w < h:
        w, h, ang = h, w, ang + 90
    ang = ((ang + 90) % 180) - 90
    if abs(w - h) < 0.5:
        ang = ((ang + 45) % 90) - 45
    return cx, cy, w, h, ang


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workdir"); ap.add_argument("pdf"); a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    feuilles = {r["feuille"]: r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8"))}
    index = {r["sig_id"]: r["signature"] for r in csv.DictReader(open(os.path.join(work, "blocs-index.csv"), encoding="utf-8"))}
    fam_rows = list(csv.DictReader(open(os.path.join(work, "blocs-familles.csv"), encoding="utf-8")))
    par_sig = defaultdict(list)
    for r in fam_rows:
        if r["sig_id"] in index:
            par_sig[index[r["sig_id"]]].append(r)
    doc = pymupdf.open(a.pdf)
    occ, nom, portees = [], {}, defaultdict(Counter)
    for f, fr in feuilles.items():
        if fr.get("role") != "plan":
            continue
        p = os.path.join(work, "blocs", f + ".csv")
        if not os.path.exists(p):
            continue
        blocs = [b for b in csv.DictReader(open(p, encoding="utf-8")) if b["signature"] in par_sig]
        if not blocs:
            continue
        page = doc[int(fr["page"]) - 1]
        mots = [w for w in page.get_text("words") if w[4].strip()]
        texte_page = page.get_text().upper()
        nouveau = "NOUVEAU" in texte_page and "EXISTANT/DÉMOLITION" not in texte_page
        defaut = "INSTALLER" if nouveau else "CONSERVER"       # feuille EXISTANT/DÉMOLITION : tout est existant sauf étiquette
        # tracés de la page, pour la boîte tournée exacte du bloc
        dr = [(d["rect"], d) for d in page.get_drawings() if MIN_COTE <= max(d["rect"].width, d["rect"].height) <= MAX_COTE]
        for b in blocs:
            x, y, w, h, D = float(b["x_pt"]), float(b["y_pt"]), float(b["w_pt"]), float(b["h_pt"]), float(b["diametre_pt"])
            regle = None
            for r in par_sig[b["signature"]]:
                if float(r["diam_min"] or 0) <= D <= float(r["diam_max"] or 99) and (not r["feuilles"].strip() or f in r["feuilles"].split()):
                    regle = r; break
            if not regle:
                continue
            label, forme = regle["label"], regle["forme"]
            bx0, by0, bx1, by1 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
            # mots voisins (≤ 14 pt de la boîte)
            vois_all = []
            for m in mots:
                dx = max(bx0 - m[2], m[0] - bx1, 0); dy = max(by0 - m[3], m[1] - by1, 0)
                d = math.hypot(dx, dy)
                if d <= 14:
                    vois_all.append((d, m[4], m))
            vois_all.sort(key=lambda v: v[0])
            vois = [(d, t) for d, t, _ in vois_all]; vois_m = [m for _, _, m in vois_all]
            portee = defaut
            for d, t in vois:
                if t.upper() in PORTEE_TAGS:
                    portee = PORTEE_TAGS[t.upper()]; break
            # type de luminaire : étiquette dont le centre tombe dans l'emprise x du bloc (barres linéaires : C1 et C1_1
            # sont écrits côte à côte au-dessus de deux barres), sinon la plus proche à ≤ 10 pt
            cand_t = [(d, t, m) for (d, t), m in zip(vois, vois_m) if TYPES_LUM.match(t) and d <= 10]
            dans_x = [c for c in cand_t if bx0 - 1 <= (c[2][0] + c[2][2]) / 2 <= bx1 + 1]
            typ = (dans_x or cand_t or [(0, "", None)])[0][1]
            if regle["famille"] == "eclairage" and typ and typ not in ("E",) or (regle["famille"] == "eclairage" and typ == "E" and label == "ENCASTRE"):
                label = f"LUMINAIRE {typ}"
            if label == "INT 3 VOIES" and not any(t == "3" and d <= 9 for d, t in vois):
                label = "INT SIMPLE"
            # feuille NOUVEAU : un luminaire sans lettre de type est un existant dessiné pour contexte → CONSERVER
            if nouveau and regle["famille"] == "eclairage" and not typ and portee == "INSTALLER":
                portee = "CONSERVER"
            designation = " ".join(t for d, t in vois if CIRCUIT.match(t) and t.upper() not in PORTEE_TAGS and not TYPES_LUM.match(t))[:60]
            o = {"feuille": f, "label": label, "x_pt": f"{x:.1f}", "y_pt": f"{y:.1f}", "source": "visuel",
                 "note": f"bloc {regle['sig_id']}" + (f" ; type {typ}" if typ else ""), "designation": designation, "portee": portee,
                 "modele": typ, "x0_pt": "", "y0_pt": "", "x1_pt": "", "y1_pt": "", "angle_deg": "", "rayon_pt": ""}
            if forme in ("carre", "triangle"):
                pts = []
                for r_, d_ in dr:
                    if r_.x0 >= bx0 - MARGE_FUSION and r_.x1 <= bx1 + MARGE_FUSION and r_.y0 >= by0 - MARGE_FUSION and r_.y1 <= by1 + MARGE_FUSION:
                        for it in d_["items"]:
                            pts += [(q.x, q.y) for q in _points(it)]
                if len(pts) >= 3:
                    cx, cy, rw, rh, ang = rect_minimal(pts)
                    o.update({"x_pt": f"{cx:.1f}", "y_pt": f"{cy:.1f}", "x0_pt": f"{cx - rw / 2 - 0.5:.1f}", "y0_pt": f"{cy - rh / 2 - 0.5:.1f}",
                              "x1_pt": f"{cx + rw / 2 + 0.5:.1f}", "y1_pt": f"{cy + rh / 2 + 0.5:.1f}", "angle_deg": f"{ang:.1f}"})
            else:
                o["rayon_pt"] = f"{max(w, h) / 2 + 0.6:.1f}"
            occ.append(o)
            portees[label][portee] += 1
            if label not in nom:
                nom[label] = {"label": label, "famille": regle["famille"], "forme": forme, "rgb": "", "jeton_regex": "",
                              "description": regle["materiel"] + (f" — type {typ}" if typ else ""), "source": f"E-001 légende ; bloc {regle['sig_id']}",
                              "code": (typ.replace("_", "") if typ else regle["code"]), "materiel": regle["materiel"] + (f" TYPE {typ}" if typ else ""),
                              "portee": "", "modele": typ, "prescription": "", "discipline": "electricite", "legende": regle["legende_no"]}
    # 1) dédoublonnage : deux blocs superposés (barre + son contour, deux signatures) = un seul appareil
    occ.sort(key=lambda o: -(float(o["x1_pt"] or 0) - float(o["x0_pt"] or 0) + float(o["rayon_pt"] or 0)))
    gardes = []
    for o in occ:
        x, y = float(o["x_pt"]), float(o["y_pt"])
        if any(g["feuille"] == o["feuille"] and g["label"] == o["label"] and math.hypot(float(g["x_pt"]) - x, float(g["y_pt"]) - y) <= 2.5 for g in gardes):
            continue
        gardes.append(o)
    occ = gardes
    # 1b) prises : cercles fermés de 3,3 à 5 pt (4 courbes, trait ≥ 0,35 pt) NON couverts par une occurrence — sur les
    #     feuilles de services, deux prises côte à côte ou une prise collée à une sortie data fusionnent en un bloc à
    #     signature unique (même épaisseur de trait) ; le CERCLE, lui, reste une partie identifiable. Classement par
    #     ce que le cercle contient : partie remplie → PRISE DDFT (demi-cercle plein), ≥ 1 trait → PRISE DOUBLE 15A.
    for f, fr in feuilles.items():
        if fr.get("role") != "plan" or not re.match(r"E1\d\d", f):
            continue
        page = doc[int(fr["page"]) - 1]
        texte_page = page.get_text().upper()
        nouveau = "NOUVEAU" in texte_page and "EXISTANT/DÉMOLITION" not in texte_page
        dr = page.get_drawings()
        mots = [w for w in page.get_text("words") if w[4].strip()]
        deja = [(float(o["x_pt"]), float(o["y_pt"])) for o in occ if o["feuille"] == f]
        petits = [d for d in dr if max(d["rect"].width, d["rect"].height) <= 12]
        for d in dr:
            its = d["items"]; r = d["rect"]
            if len(its) != 4 or any(it[0] != "c" for it in its) or not (3.3 <= max(r.width, r.height) <= 5.0) or abs(r.width - r.height) > 0.6 or (d.get("width") or 0) < 0.35:
                continue
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if any(math.hypot(cx - x, cy - y) <= 3.5 for x, y in deja):
                continue
            dedans = [e for e in petits if e is not d and e["rect"].x0 >= r.x0 - 0.4 and e["rect"].x1 <= r.x1 + 0.4 and e["rect"].y0 >= r.y0 - 0.4 and e["rect"].y1 <= r.y1 + 0.4]
            traversent = [e for e in petits if e is not d and e["rect"].intersects(r) and max(e["rect"].width, e["rect"].height) <= 2.5 * max(r.width, r.height)]
            plein = any(e.get("fill") for e in dedans) or any(e.get("fill") for e in traversent)
            lignes = sum(1 for e in traversent if all(it[0] == "l" for it in e["items"]))
            if plein:
                label, code, mat, leg = "PRISE DDFT", "GF", "PRISE DOUBLE DDFT (moitié pleine)", "S06"
            elif lignes >= 1:
                label, code, mat, leg = "PRISE DOUBLE 15A", "PC", "PRISE DE COURANT DOUBLE 15A- 120V", "S01"
            else:
                continue
            vois_all = []
            for m in mots:
                dx = max(r.x0 - m[2], m[0] - r.x1, 0); dy = max(r.y0 - m[3], m[1] - r.y1, 0); dd = math.hypot(dx, dy)
                if dd <= 14:
                    vois_all.append((dd, m[4]))
            vois_all.sort()
            portee = "INSTALLER" if nouveau else "CONSERVER"
            for dd, t in vois_all:
                if t.upper() in PORTEE_TAGS:
                    portee = PORTEE_TAGS[t.upper()]; break
            designation = " ".join(t for dd, t in vois_all if CIRCUIT.match(t) and t.upper() not in PORTEE_TAGS)[:60]
            occ.append({"feuille": f, "label": label, "x_pt": f"{cx:.1f}", "y_pt": f"{cy:.1f}", "source": "visuel",
                        "note": f"cercle ø{max(r.width, r.height):.1f} pt ({lignes} trait(s){', plein' if plein else ''})", "designation": designation,
                        "portee": portee, "modele": "", "x0_pt": "", "y0_pt": "", "x1_pt": "", "y1_pt": "", "angle_deg": "", "rayon_pt": f"{max(r.width, r.height) / 2 + 0.8:.1f}"})
            deja.append((cx, cy))
            if label not in nom:
                nom[label] = {"label": label, "famille": "prise", "forme": "cercle", "rgb": "", "jeton_regex": "", "description": mat, "source": "E-001 légende ; cercles vectoriels",
                              "code": code, "materiel": mat, "portee": portee, "modele": "", "prescription": "", "discipline": "electricite", "legende": leg}
    sans_bloc = []
    # 2) luminaires typés sur feuille NOUVEAU : l'ÉTIQUETTE est l'unité (une rangée linéaire « C1 + C1_1 » = 2 modules ;
    #    E-203 : mots C1 x12, C1_1 x6, C1_3 x15 = tableau E-008). On remplace les occurrences de blocs typés par une
    #    occurrence par étiquette, posée sur le bloc le plus proche (boîte du bloc si ce bloc n'a qu'une étiquette).
    for f, fr in feuilles.items():
        if fr.get("role") != "plan":
            continue
        page = doc[int(fr["page"]) - 1]
        texte_page = page.get_text().upper()
        if not ("NOUVEAU" in texte_page and "EXISTANT/DÉMOLITION" not in texte_page):
            continue
        blocs_typ = [o for o in occ if o["feuille"] == f and o["label"].startswith("LUMINAIRE ")]
        if not blocs_typ:
            continue
        occ = [o for o in occ if not (o["feuille"] == f and o["label"].startswith("LUMINAIRE "))]
        mots = [w for w in page.get_text("words") if TYPES_LUM.match(w[4].strip())]
        bruts = [b for b in csv.DictReader(open(os.path.join(work, "blocs", f + ".csv"), encoding="utf-8"))
                 if 12 <= float(b["diametre_pt"]) <= 60 and max(float(b["w_pt"]), float(b["h_pt"])) >= 3 * max(0.1, min(float(b["w_pt"]), float(b["h_pt"])))]
        par_bloc = defaultdict(list)
        for w in mots:
            cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
            b = min(blocs_typ, key=lambda o: max(float(o["x0_pt"] or o["x_pt"]) - cx, cx - float(o["x1_pt"] or o["x_pt"]), 0) ** 2
                    + max(float(o["y0_pt"] or o["y_pt"]) - cy, cy - float(o["y1_pt"] or o["y_pt"]), 0) ** 2)
            d = math.sqrt(max(float(b["x0_pt"] or b["x_pt"]) - cx, cx - float(b["x1_pt"] or b["x_pt"]), 0) ** 2
                          + max(float(b["y0_pt"] or b["y_pt"]) - cy, cy - float(b["y1_pt"] or b["y_pt"]), 0) ** 2)
            par_bloc[id(b)].append((w, b if d <= 12 else None))
        for k, lst in par_bloc.items():
            for w, b in lst:
                typ = w[4].strip(); cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
                o = {"feuille": f, "label": f"LUMINAIRE {typ}", "source": "visuel", "designation": "", "portee": "INSTALLER", "modele": typ,
                     "x0_pt": "", "y0_pt": "", "x1_pt": "", "y1_pt": "", "angle_deg": "", "rayon_pt": ""}
                if b is not None and len(lst) == 1:
                    o.update({k2: b[k2] for k2 in ("x_pt", "y_pt", "x0_pt", "y0_pt", "x1_pt", "y1_pt", "angle_deg", "designation")})
                    o["note"] = f"étiquette {typ} sur {b['note']}"
                elif b is not None:
                    o.update({"x_pt": f"{cx:.1f}", "y_pt": f"{float(b['y_pt']):.1f}", "note": f"étiquette {typ} ({len(lst)} modules sur la rangée {b['note']})",
                              "designation": b["designation"]})
                    o["rayon_pt"] = "4.0"
                else:
                    # pas de bloc étiqueté : une barre brute (bloc allongé non étiqueté) à ≤ 12 pt, sinon le mot lui-même
                    # s'il est au milieu d'autres appareils (≤ 60 pt) — jamais une lettre du cartouche ou des notes
                    brut = min(bruts, key=lambda b: math.hypot(float(b["x_pt"]) - cx, float(b["y_pt"]) - cy), default=None)
                    if brut and math.hypot(float(brut["x_pt"]) - cx, float(brut["y_pt"]) - cy) <= 12:
                        o.update({"x_pt": brut["x_pt"], "y_pt": brut["y_pt"], "rayon_pt": "4.0", "note": f"étiquette {typ} sur barre non étiquetée ø{brut['diametre_pt']} pt"})
                    elif any(math.hypot(float(q["x_pt"]) - cx, float(q["y_pt"]) - cy) <= 60 for q in occ if q["feuille"] == f):
                        o.update({"x_pt": f"{cx:.1f}", "y_pt": f"{cy:.1f}", "rayon_pt": "4.0", "note": f"étiquette {typ} sans bloc à ≤ 12 pt — position = mot, à vérifier"})
                    else:
                        sans_bloc.append((f, typ, round(cx), round(cy)))
                        continue
                occ.append(o)
                if o["label"] not in nom:
                    nom[o["label"]] = {"label": o["label"], "famille": "eclairage", "forme": "cercle" if not o["x0_pt"] else "carre", "rgb": "", "jeton_regex": "",
                                       "description": f"Luminaire type {typ} (tableau E-008)", "source": f"{f} étiquettes", "code": typ.replace("_", ""),
                                       "materiel": f"APPAREIL D'ÉCLAIRAGE TYPE {typ}", "portee": "INSTALLER", "modele": typ, "prescription": "", "discipline": "electricite", "legende": "E-008"}
    # 3) instances posées à la main (pictogrammes aux signatures uniques : enseignes, détecteurs, encastrés d'urgence)
    p_inst = os.path.join(work, "blocs-instances.csv")
    if os.path.exists(p_inst):
        for r in csv.DictReader(open(p_inst, encoding="utf-8")):
            occ.append({"feuille": r["feuille"], "label": r["label"], "x_pt": r["x_pt"], "y_pt": r["y_pt"], "source": "visuel",
                        "note": "instance manuelle : " + r["note"], "designation": "", "portee": r["portee"], "modele": "",
                        "x0_pt": "", "y0_pt": "", "x1_pt": "", "y1_pt": "", "angle_deg": "", "rayon_pt": r["rayon_pt"]})
            if r["label"] not in nom:
                nom[r["label"]] = {"label": r["label"], "famille": r["famille"], "forme": r["forme"], "rgb": "", "jeton_regex": "",
                                   "description": r["materiel"], "source": "E-001 légende ; instances manuelles", "code": r["code"],
                                   "materiel": r["materiel"], "portee": r["portee"], "modele": "", "prescription": "", "discipline": "electricite", "legende": r["legende_no"]}
    # dédoublonnage final (instances manuelles comprises) : même feuille, même famille, ≤ 2,5 pt
    gardes = []
    for o in occ:
        x, y = float(o["x_pt"]), float(o["y_pt"])
        if any(g["feuille"] == o["feuille"] and g["label"] == o["label"] and math.hypot(float(g["x_pt"]) - x, float(g["y_pt"]) - y) <= 2.5 for g in gardes):
            continue
        gardes.append(o)
    occ = gardes
    portees = defaultdict(Counter)
    for o in occ:
        portees[o["label"]][o["portee"]] += 1
    nom = {k: v for k, v in nom.items() if k in portees}
    for label, n in nom.items():
        n["portee"] = portees[label].most_common(1)[0][0]
    # 4) legende.csv depuis les blocs de la feuille de légende (description lue à droite du glyphe), sections par zone
    leg_rows = []
    f_leg = next((f for f, fr in feuilles.items() if fr.get("role") == "legende"), None)
    if f_leg and os.path.exists(os.path.join(work, "blocs", f_leg + ".csv")):
        page_l = doc[int(feuilles[f_leg]["page"]) - 1]
        heads = [(b[0], b[1], b[4].strip().split("\n")[0].upper()) for b in page_l.get_text("blocks")
                 if re.match(r"^(DISTRIBUTION|ÉCLAIRAGE|ECLAIRAGE|ALARME|SERVICES|CHAUFFAGE|TÉLÉ|COMMUNICATION|SÉCURITÉ|MÉCANIQUE)", b[4].strip().upper())
                 and len(b[4].strip().split("\n")[0]) < 40]

        def section(x, y):
            cands = [h for h in heads if h[0] - 30 <= x <= h[0] + 400 and h[1] <= y]
            return max(cands, key=lambda h: h[1])[2] if cands else ""
        vus = set(); comp = Counter()
        for b in csv.DictReader(open(os.path.join(work, "blocs", f_leg + ".csv"), encoding="utf-8")):
            d = (b.get("description") or "").strip()
            if not d or (float(b["x_pt"]), d) in vus:
                continue
            vus.add((float(b["x_pt"]), d))
            sec = section(float(b["x_pt"]), float(b["y_pt"]))
            pref = {"DISTRIBUTION": "D", "ALARME INCENDIE": "A", "ALARME INTRUSION": "I", "ÉCLAIRAGE D'URGENCE": "U", "SERVICES": "S", "ÉCLAIRAGE": "L", "CHAUFFAGE": "C"}.get(sec, "X")
            comp[pref] += 1
            leg_rows.append({"feuille": f_leg, "section": sec, "no": f"{pref}{comp[pref]:02d}", "symbole": f"bloc ø{b['diametre_pt']} pt" + (f" [{b.get('texte')}]" if b.get("texte") else ""),
                             "description": d, "code": code_attendu(d), "statut": "absent", "qte": 0,
                             "preuve": "signature de bloc vectoriel absente des feuilles plan (blocs-signatures.json)",
                             "feuille_legende": f_leg, "x_pt": b["x_pt"], "y_pt": b["y_pt"], "taille_pt": b["diametre_pt"]})
        leg_rows.sort(key=lambda r: (r["section"], float(r["y_pt"])))
        # rattacher chaque famille à sa ligne (description de la famille = début de la description de légende)
        def norm(t): return re.sub(r"[^A-Z0-9]", "", t.upper().replace("É", "E").replace("È", "E").replace("Â", "A"))
        for label, n in nom.items():
            cible = norm(n["materiel"].split(" TYPE ")[0].split(" (")[0].split(" — ")[0])
            cands = [r for r in leg_rows if len(norm(r["description"])) >= 6 and (cible.startswith(norm(r["description"])) or norm(r["description"]).startswith(cible))]
            hit = max(cands, key=lambda r: len(norm(r["description"]))) if cands and n["legende"] != "E-008" else None
            if hit:
                n["legende"] = hit["no"]; hit["statut"] = "compte"; hit["qte"] = int(hit["qte"]) + sum(portees[label].values())
                hit["preuve"] = f"famille {label} : {sum(portees[label].values())} occurrences (blocs vectoriels)"
            elif n["legende"] == "E-008":
                pass
            else:
                n["legende"] = "HORS LEGENDE"
            attendu = code_attendu(n["materiel"])
            if attendu:
                n["code"] = attendu
        # luminaires typés : leur « légende » est le tableau des appareils E-008 (une ligne par type)
        for label, n in nom.items():
            if n["legende"] == "E-008":
                no = f"E008-{n['modele'].replace('_', '')}"
                leg_rows.append({"feuille": f_leg, "section": "TABLEAU E-008", "no": no, "symbole": f"étiquette {n['modele']}", "description": n["materiel"],
                                 "code": n["code"], "statut": "compte", "qte": sum(portees[label].values()), "preuve": f"étiquettes {n['modele']} sur les feuilles NOUVEAU",
                                 "feuille_legende": "", "x_pt": "", "y_pt": "", "taille_pt": ""})
                n["legende"] = no
        with open(os.path.join(work, "legende.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["feuille", "section", "no", "symbole", "description", "code", "statut", "qte", "preuve", "feuille_legende", "x_pt", "y_pt", "taille_pt"])
            w.writeheader(); w.writerows(leg_rows)
    # 5) réserves et rapport
    R = ["# Réserves — relevé par blocs vectoriels (blocs_vectoriels.py → blocs_vers_releve.py)", "",
         "## R-001 — Méthode", "Chaque symbole est un bloc CAO ; les blocs de même signature (invariante à la position, la rotation et l'échelle, "
         "lettre contenue incluse) sont étiquetés une fois (`blocs-familles.csv`, planches `signatures-NN.png`), puis chaque instance devient une "
         "occurrence au centre exact du bloc, avec sa boîte tournée. Validé sur E-201 contre le relevé vérifié TEST-E201 : 116/121 repères "
         "retrouvés à ≤ 5 pt, précision par signature 34/34, 17/17, 11/11.", "",
         "## R-002 — Portée", "E.A.E → ENLEVER, E.A.R → RELOCALISER, E.A.C → CONSERVER lus à ≤ 14 pt du bloc ; sans étiquette : CONSERVER sur une feuille "
         "EXISTANT/DÉMOLITION, INSTALLER sur une feuille NOUVEAU — sauf luminaire sans lettre de type sur feuille NOUVEAU (existant dessiné pour contexte → CONSERVER). "
         "À confirmer famille par famille sur les planches de contrôle.", "",
         "## R-003 — Luminaires typés (E-203/E-204)", "L'unité est l'ÉTIQUETTE (A1, C1, C1_1, C1_3, E) : une rangée linéaire « C1 + C1_1 » = 2 modules. "
         "E-203 : A1 11, C1 12, C1_1 6, C1_3 15 = tableau E-008 et relevé d'éclairage du 2026-10-07. LUMINAIRE E : 3 étiquettes sur bloc (l'estimation en compte 4) — à trancher au zoom.", ""]
    if sans_bloc:
        R += ["## R-004 — Étiquettes de type sans bloc à ≤ 12 pt (écartées, cartouche/notes probables)", ""] + [f"- {f} : « {t} » à ({x}, {y})" for f, t, x, y in sans_bloc] + [""]
    R += ["## R-005 — Pictogrammes (instances manuelles, `blocs-instances.csv`)", "Enseignes Z6 (3, tracé pointillé : confirmer neuf — E-008 en liste 3), détecteurs de fumée (3 existants pointillés + neufs pleins), "
          "encastrés sur circuit d'urgence PP-U1 (quart noir). Les pictogrammes ont des signatures uniques (courbes, remplissages), ils ne se regroupent pas automatiquement.", "",
          "## Q12 — familles par type sur une même ligne de légende (justification)",
          "L05 (encastré) → ENCASTRE (existant), ENCASTRE URGENCE (quart noir, circuit PP-U1) et LUMINAIRE E (type E du tableau E-008) ; "
          "L07 ('x4) → LED 1X4 (existant) et LUMINAIRE A1 (type A1 neuf) ; S16 (prise double 15 A) → PRISE DOUBLE 15A et PRISE USB (symbole « USB » distinct). "
          "Une famille par type de luminaire est voulue : le chiffrage est par type (E-008), pas par symbole (règle R7 : nommer comme la légende/le tableau).", "",
          "## R-007 — Prises (cercles vectoriels, feuilles E-10x)", "Détectées au niveau de la partie (cercle fermé 3,3–5 pt, trait ≥ 0,35 pt) parce que deux prises côte à côte ou une prise collée "
          "à une sortie data fusionnent en un seul bloc. PRISE DDFT = cercle contenant une partie remplie (légende : demi-cercle plein = DDFT ; barre pleine = M.A.L.T. isolée — "
          "les deux variantes tombent ici dans PRISE DDFT, à départager au zoom) ; PRISE DOUBLE 15A = cercle traversé d'au moins un trait (15 A et 20 A non distingués : "
          "le crochet 20 A est un petit trait à côté du cercle, à vérifier sur les planches). Comptoir/standard non distingués (même cercle, trait de comptoir à côté).", "",
          "## R-006 — Hors relevé", "Sorties data : triangle plein ≤ 6,5 pt seulement (les grandes flèches sont des renvois de circuit). Cercles nus, bulles d'axes, numéros de locaux, mobilier : ignorés. "
          "Longueurs de conduits/filage : hors relevé (estimation du 2026-10-08). Panneaux E-501/E-502, schémas E-006/E-007 : non relevés (tableaux).", ""]
    open(os.path.join(work, "reserves.md"), "w", encoding="utf-8").write("\n".join(R))
    T = ["# Rapport de relevé — S-1902 Bibliothèque Georgette-Lepage (SP-GTER-26-0080, HF experts-conseils 26-29)", "",
         f"Entrée : P-D Électricité_2026-09-22.pdf, 21 feuilles A1 vectorielles. Méthode : blocs vectoriels (R-001). {len(occ)} occurrences, {len(nom)} familles.", "",
         "| feuille | occurrences |", "|---|--:|"] + [f"| {f} | {n} |" for f, n in sorted(Counter(o["feuille"] for o in occ).items())] + ["", "| famille | total | portées |", "|---|--:|---|"] \
        + [f"| {label} | {sum(c.values())} | {', '.join(f'{k} {v}' for k, v in c.most_common())} |" for label, c in sorted(portees.items())] \
        + ["", "Modèle : Claude Fable 5.1 (session interactive, route « session = agent »). Outils : prepare.py, blocs_vectoriels.py, blocs_vignettes.py, blocs_vers_releve.py, controle_qualite.py.", "",
           "**STATUT : relevé automatique à VÉRIFIER sur les planches de contrôle avant chiffrage.**"]
    open(os.path.join(work, "rapport-releve.md"), "w", encoding="utf-8").write("\n".join(T))
    with open(os.path.join(work, "nomenclature.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["label", "famille", "forme", "rgb", "jeton_regex", "description", "source", "code", "materiel", "portee", "modele", "prescription", "discipline", "legende"])
        w.writeheader(); w.writerows(sorted(nom.values(), key=lambda r: (r["famille"], r["label"])))
    cols = ["feuille", "label", "x_pt", "y_pt", "source", "note", "designation", "portee", "modele", "x0_pt", "y0_pt", "x1_pt", "y1_pt", "angle_deg", "rayon_pt"]
    with open(os.path.join(work, "occurrences-visuel.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(occ)
    with open(os.path.join(work, "occurrences-texte.csv"), "w", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=["feuille", "label", "x_pt", "y_pt", "source", "note"]).writeheader()
    # classement : plan / legende / devis / schema / tableau
    with open(os.path.join(work, "feuilles-classement.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["feuille", "type", "echelle", "note", "bordereau"]); w.writeheader()
        for f, fr in feuilles.items():
            t = (fr.get("titre") or "")
            role = fr.get("role")
            typ = "plan" if role == "plan" and re.match(r"E[12]0\d", f) else ("legende" if role == "legende" else "devis" if role == "devis" else
                  "schema" if "SCHÉMA" in t.upper() else "tableau" if "TABLEAU" in t.upper() or "PANNEAUX" in t.upper() else "detail")
            ech = "100" if "1:100" in t else ""
            w.writerow({"feuille": f, "type": typ, "echelle": ech, "note": f"cartouche={f[:1]}-{f[1:]} · {t[:70]}", "bordereau": ""})
    par_f = Counter(o["feuille"] for o in occ)
    print(f"{len(occ)} occurrences, {len(nom)} familles → nomenclature.csv / occurrences-visuel.csv ; par feuille : {dict(sorted(par_f.items()))}")
    for label, c in sorted(portees.items()):
        print(f"  {label:26s} {sum(c.values()):4d}  {dict(c)}")


if __name__ == "__main__":
    main()
