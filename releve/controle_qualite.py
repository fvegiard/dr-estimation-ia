"""Contrôle qualité BLOQUANT d'un relevé (sorties de l'agent) avant de le déclarer conforme.

Usage : python releve/controle_qualite.py WORKDIR [--reference familles-par-feuille.csv --feuille-ref DSI01 --feuille F]
Écrit WORKDIR/qualite.json ; code 0 si aucune erreur bloquante, 2 sinon.

Un succès technique de l'agent (fichiers écrits) ne prouve pas un relevé exact (run1 Gemma DSI01 du 2026-09-29 :
« success » avec 31 marques contre 122 chez l'estimateur). Contrôles :
  Q1 sorties obligatoires présentes et non vides ; chaque feuille « plan » a au moins une occurrence ;
  Q2 chaque libellé d'occurrence existe dans nomenclature.csv ;
  Q3 un libellé = un appareil : même libellé pour deux jetons/descriptions différents = fusion interdite (R1/R3) ;
  Q4 classement : le préfixe du repère lu (note « [DT1.2] ») doit correspondre au jeton_regex du libellé choisi ;
  Q5 repère en double sur une même feuille ;
  Q6 trous dans une suite de repères (K1.1, K1.2, K1.6 → K1.3-K1.5 manquent) non expliqués dans reserves.md ;
  Q7 coordonnées hors de la feuille ;
  Q8 appareil jamais relevé sur les plans/schémas/tableaux et sans libellé complet dans reserves.md ;
  Q9 (si une référence est fournie) écart par famille > 5 % de la référence ;
  Q10 coordonnées fabriquées sur une grille mentale au lieu d'être lues sur le plan.

Q10 : un symbole réel tombe sur une coordonnée quelconque. Si presque toutes les marques sont des
multiples ronds (10 pt, 25 pt…), le modèle a inventé des positions au lieu de les lire — run2 Gemma
DSI01 du 2026-09-29 : 53/53 marques multiples de 10 en x ET en y, soit une chance sur 100^53, et
aucune ne tombait sur un symbole. Contrôle aveugle : il ne demande ni référence ni ancrage.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import os
import re
import sys

REPERE = re.compile(r"\[?\b([A-Z]{1,4}\d?)(\d+)\.(\d+)\]?")
TOLERANCE_REF = 0.05
PAS_GRILLE = (5, 10, 25, 50)  # pas ronds typiques d'une position inventée
MIN_GRILLE = 8                # en dessous, la coïncidence reste plausible
SEUIL_GRILLE = 0.80           # part de marques alignées à partir de laquelle on bloque
SEUIL_GRILLE_AVERT = 0.15     # au-dessus, le modèle arrondit trop (humains mesurés : 0,9 %)


def coordonnees(o):
    """(x, y) d'une occurrence, ou None si illisible."""
    try:
        return float(o.get("x_pt") or o.get("x")), float(o.get("y_pt") or o.get("y"))
    except (TypeError, ValueError):
        return None


def grille_suspecte(points, pas=PAS_GRILLE, minimum=MIN_GRILLE, seuil=SEUIL_GRILLE):
    """Plus grand pas sur lequel au moins `seuil` des points sont alignés en x ET en y.

    Renvoie (pas, nombre_aligné, total) ou None. Des positions lues sur un plan ne
    s'alignent pas : la probabilité que n marques tombent toutes sur un multiple de 10
    dans les deux axes est de 100^-n.

    Le pas 5 compte aussi : mesuré sur le dépôt, les relevés humains n'y tombent que
    dans 3,1 % des cas (319 marques) alors que kimi-k3 y tombe à 100 % sur 104 marques.
    Un modèle peut arrondir finement et paraître précis ; c'est la même invention.
    On renvoie le pas le plus grand qui tient, car c'est celui qui décrit vraiment la
    maille employée : gemma-4-31b est à 100 % sur 10 pt, kimi-k3 seulement sur 5 pt."""
    if len(points) < minimum:
        return None
    for p in sorted(pas, reverse=True):
        n = sum(1 for x, y in points if x % p == 0 and y % p == 0)
        if n >= seuil * len(points):
            return p, n, len(points)
    return None


def part_arrondie(points, pas=10):
    """Part des marques tombant sur un multiple de `pas` dans les deux axes.

    Repère mesuré sur les relevés humains du dépôt : 3 coordonnées rondes sur 319
    marques, soit 0,9 %. Un taux nettement supérieur sans atteindre SEUIL_GRILLE
    signale un modèle qui arrondit ses lectures — imprécis sans être inventé."""
    if not points:
        return 0.0
    return sum(1 for x, y in points if x % pas == 0 and y % pas == 0) / len(points)


def lire_csv(p, mal_formees=None):
    """Lit un CSV en normalisant les clés. Une ligne ayant plus de champs que d'en-têtes
    est signalée (csv.DictReader range le surplus dans une liste sous la clé None) : le
    contrôle doit la rapporter comme erreur, jamais planter dessus."""
    if not os.path.isfile(p):
        return []
    out = []
    with open(p, encoding="utf-8", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            surplus = r.pop(None, None)
            if surplus is not None and mal_formees is not None:
                mal_formees.append(f"{os.path.basename(p)} ligne {i} : {len(surplus)} champ(s) en trop "
                                   f"({', '.join(str(s) for s in surplus)[:80]}) — virgule non échappée ?")
            out.append({(k or "").strip(): (v if isinstance(v, str) else " ".join(map(str, v or []))).strip()
                        for k, v in r.items()})
    return out


def famille_de_repere(prefixe, nomenclature):
    """Libellés dont le jeton_regex reconnaît le préfixe du repère (ex. DT → DETECTEUR THERMIQUE)."""
    out = set()
    for n in nomenclature:
        rx = n.get("jeton_regex")
        if rx:
            try:
                if re.fullmatch(rx, prefixe):
                    out.add(n["label"])
            except re.error:
                pass
    return out


MOTS_VIDES = {"DE", "DU", "LA", "LE", "ET", "A", "D", "L", "UNITE", "TYPE"}


def piste_confusion(lab, comptes, fiche):
    """Nomme le libellé qui a probablement absorbé `lab`, ou '' si aucun candidat.

    Un libellé jamais employé est rarement un appareil absent : il est compté sous un voisin.
    On classe les libellés employés par mots significatifs partagés (DETECTEUR THERMIQUE 135F →
    DETECTEUR THERMIQUE), puis par nombre de marques. Sans mot commun, on accepte un voisin de
    même famille et même forme ; sinon on n'invente pas de piste."""
    mots = {m for m in re.split(r"[^A-Z0-9]+", (lab or "").upper()) if m and m not in MOTS_VIDES}
    meilleurs = []
    for autre, n in comptes.items():
        if not autre or autre == lab or not n:
            continue
        communs = len(mots & {m for m in re.split(r"[^A-Z0-9]+", autre.upper()) if m and m not in MOTS_VIDES})
        meme_type = fiche.get(autre) is not None and fiche.get(autre) == fiche.get(lab)
        if communs or meme_type:
            meilleurs.append((communs, n, autre, meme_type))
    if not meilleurs:
        return ""
    communs, n, autre, meme_type = max(meilleurs)
    motif = (f"{communs} mot(s) en commun" if communs else "même famille et même forme")
    return f" — confusion probable avec {autre!r} ({n} marques, {motif})"


def labels_justifies(reserves, labels):
    """Libellés complets cités en réserve, avec priorité au plus long libellé connu.

    « PRISE GFI » ne justifie pas aussi « PRISE »; une seconde mention distincte
    de « PRISE » le peut. La prose existante, sa casse et ses espaces sont conservés.
    """
    connus = {" ".join(lab.casefold().split()): lab for lab in labels if lab}
    if not connus:
        return set()
    motifs = [r"\s+".join(re.escape(mot) for mot in lab.split())
              for lab in sorted(connus, key=len, reverse=True)]
    rx = re.compile(r"(?<!\w)(?:" + "|".join(motifs) + r")(?!\w)", re.IGNORECASE)
    return {connus[" ".join(m.group().casefold().split())] for m in rx.finditer(reserves)}


def controler(work, reference=None, feuille_ref=None, feuille=None):
    err, avert, mal = [], [], []
    classement = lire_csv(os.path.join(work, "feuilles-classement.csv"), mal)
    nomen = lire_csv(os.path.join(work, "nomenclature.csv"), mal)
    occ = lire_csv(os.path.join(work, "occurrences-visuel.csv"), mal) + lire_csv(os.path.join(work, "occurrences-texte.csv"), mal)
    occ = [o for o in occ if (o.get("exclure") or "").strip().lower() not in ("1", "oui", "x", "true")]
    feuilles = lire_csv(os.path.join(work, "feuilles.csv"), mal)
    tailles = {}
    for r in feuilles:
        f = r.get("feuille", "")
        if not f or f in tailles:
            err.append(f"Q1 identifiant de feuille vide ou en double dans feuilles.csv : {f!r}")
        try:
            W, H = float(r.get("largeur_pt", "")), float(r.get("hauteur_pt", ""))
        except (TypeError, ValueError):
            W = H = 0
        if not (math.isfinite(W) and math.isfinite(H) and W > 0 and H > 0):
            err.append(f"Q7 dimensions de feuille invalides : {f!r} ({W}, {H})")
        tailles[f] = (W, H)
    reserves = open(os.path.join(work, "reserves.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(work, "reserves.md")) else ""

    # Q0 : lignes mal formées (champ en trop = virgule non échappée dans un libellé ou une note)
    for m in mal:
        err.append(f"Q0 ligne mal formée : {m}")
    # Q1
    for f in ("feuilles.csv", "feuilles-classement.csv", "nomenclature.csv", "reserves.md", "rapport-releve.md"):
        p = os.path.join(work, f)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            err.append(f"Q1 sortie manquante ou vide : {f}")
    if not feuilles:
        err.append("Q1 aucune feuille d'entrée dans feuilles.csv")
    classes = collections.Counter(r.get("feuille", "") for r in classement)
    for f in tailles:
        if classes[f] != 1:
            err.append(f"Q1 feuille à classer exactement une fois : {f!r} ({classes[f]} classements)")
    for r in classement:
        if r.get("feuille") not in tailles:
            err.append(f"Q1 classement d'une feuille inconnue : {r.get('feuille')!r}")
        if not r.get("type"):
            err.append(f"Q1 type de feuille manquant : {r.get('feuille')!r}")
    plans = [r.get("feuille") for r in classement if r.get("type") == "plan"]
    par_feuille = collections.Counter(o.get("feuille") for o in occ)
    for f in plans:
        if not par_feuille.get(f):
            err.append(f"Q1 feuille plan sans aucune occurrence : {f}")
    # Q2
    labels = {n.get("label") for n in nomen}
    for lab in sorted({o.get("label") for o in occ} - labels):
        err.append(f"Q2 libellé absent de nomenclature.csv : {lab!r}")
    # Q3
    defs = collections.defaultdict(set)
    for n in nomen:
        defs[n.get("label")].add((n.get("jeton_regex") or "", (n.get("description") or "").upper()))
    for lab, d in defs.items():
        jetons = {j for j, _ in d if j}
        if len(jetons) > 1:
            err.append(f"Q3 libellé {lab!r} fusionne des appareils distincts (jetons {sorted(jetons)}) : un libellé par appareil")
    # Q4 / Q5 / Q6
    vus = collections.defaultdict(list)
    for o in occ:
        m = REPERE.search((o.get("note") or "").upper())
        if not m:
            continue
        pref, niv, num = m.group(1), m.group(2), int(m.group(3))
        rep = f"{pref}{niv}.{num}"
        vus[(o.get("feuille"), rep)].append(o)
        attendus = famille_de_repere(pref, nomen)
        if attendus and o.get("label") not in attendus:
            err.append(f"Q4 classement : {rep} ({o.get('feuille')}) relevé comme {o.get('label')!r}, attendu {sorted(attendus)}")
    for (f, rep), l in vus.items():
        if len(l) > 1:
            err.append(f"Q5 repère {rep} relevé {len(l)} fois sur {f}")
    # Distinct repère names must not count the same physical symbol twice.
    # Match the MCP control: same sheet/label, within 4 pt on both axes.
    positions = collections.defaultdict(list)
    for o in occ:
        point = coordonnees(o)
        if point is not None and all(math.isfinite(c) for c in point):
            positions[(o.get("feuille"), o.get("label"))].append(point)
    for (f, label), points in positions.items():
        points.sort()
        for i, (x, y) in enumerate(points):
            for x2, y2 in points[i + 1:]:
                if x2 - x > 4:
                    break
                if abs(y2 - y) <= 4:
                    err.append(f"Q5 position en double sur {f} pour {label!r} : "
                               f"({x:g}, {y:g}) et ({x2:g}, {y2:g})")
    suites = collections.defaultdict(set)
    for (f, rep) in vus:
        m = REPERE.search(rep)
        suites[(f, m.group(1), m.group(2))].add(int(m.group(3)))
    for (f, pref, niv), nums in suites.items():
        trous = [f"{pref}{niv}.{i}" for i in range(1, max(nums)) if i not in nums]
        trous = [t for t in trous if t not in reserves]
        if trous:
            err.append(f"Q6 {f} : repères manquants dans la suite {pref}{niv}.x : {', '.join(trous[:15])}{' …' if len(trous) > 15 else ''}")
    n_reperes = len(vus)
    if occ and n_reperes == 0:
        avert.append("aucun repère lu dans les notes : Q4-Q6 non vérifiables (classement non contrôlé)")
    # Q7
    for o in occ:
        if o.get("feuille") not in tailles:
            err.append(f"Q7 occurrence sur une feuille inconnue : {o.get('feuille')!r} {o.get('label')}")
            continue
        W, H = tailles[o.get("feuille")]
        point = coordonnees(o)
        if point is None or not all(math.isfinite(c) for c in point):
            err.append(f"Q7 coordonnées invalides ou non finies : {o.get('feuille')} {o.get('label')}")
            continue
        x, y = point
        if not (0 <= x <= W and 0 <= y <= H):
            err.append(f"Q7 coordonnées hors feuille : {o.get('feuille')} {o.get('label')} ({x}, {y})")
    # Q8
    feuilles_releve = {r.get("feuille") for r in classement if r.get("type") in {"plan", "schema", "tableau"}}
    comptes = collections.Counter(o.get("label") for o in occ if o.get("feuille") in feuilles_releve)
    fiche = {n.get("label"): (n.get("famille", ""), n.get("forme", "")) for n in nomen}
    justifies = labels_justifies(reserves, labels)
    for lab in sorted(labels):
        if lab and not comptes.get(lab) and lab not in justifies:
            err.append(f"Q8 {lab!r} est dans la nomenclature mais n'est relevé sur aucun plan, schéma ou tableau "
                       f"(ni justifié en réserve){piste_confusion(lab, comptes, fiche)}")
    # Q9
    comparaison = None
    if reference and feuille_ref:
        ref = {r["designation"]: int(r["qte"]) for r in lire_csv(reference) if r.get("feuille") == feuille_ref}
        ia = collections.Counter()
        for o in occ:
            if feuille and o.get("feuille") != feuille:
                continue
            m = REPERE.search((o.get("note") or "").upper())
            fam = m.group(1) if m and m.group(1) in ref else None
            if fam is None:
                cand = [j for n in nomen if n.get("label") == o.get("label") for j in [n.get("jeton_regex") or ""] if j in ref]
                fam = cand[0] if len(set(cand)) == 1 else "?"
            ia[fam] += 1
        comparaison = {f: {"reference": ref.get(f, 0), "ia": ia.get(f, 0)} for f in sorted(set(ref) | set(ia))}
        for f, c in comparaison.items():
            if abs(c["ia"] - c["reference"]) > TOLERANCE_REF * max(c["reference"], 1):
                err.append(f"Q9 {feuille_ref} famille {f} : IA {c['ia']} / référence {c['reference']}")
    # Q10 : positions inventées sur une grille au lieu d'être lues sur le plan
    par_feuille = collections.defaultdict(list)
    for o in occ:
        c = coordonnees(o)
        if c:
            par_feuille[o.get("feuille")].append(c)
    grilles = {}
    for f, pts in sorted(par_feuille.items()):
        g = grille_suspecte(pts)
        if g:
            pas, n, tot = g
            grilles[f] = {"pas": pas, "alignees": n, "total": tot}
            err.append(f"Q10 {f} : {n}/{tot} marques sur une grille de {pas} pt (x et y) — positions "
                       f"inventées, pas lues sur le plan")
        elif len(pts) >= MIN_GRILLE and (part := part_arrondie(pts)) >= SEUIL_GRILLE_AVERT:
            avert.append(f"Q10 {f} : {part:.0%} des marques sur un multiple de 10 pt (relevés humains "
                         f"mesurés : 0,9 %) — lectures arrondies, positions à revalider")
    res = {"conforme": not err, "erreurs": err, "avertissements": avert, "occurrences": len(occ), "reperes_lus": n_reperes,
           "comparaison_reference": comparaison, "grilles_suspectes": grilles}
    json.dump(res, open(os.path.join(work, "qualite.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("work"); ap.add_argument("--reference"); ap.add_argument("--feuille-ref"); ap.add_argument("--feuille")
    a = ap.parse_args()
    r = controler(a.work, a.reference, a.feuille_ref, a.feuille)
    print(f"conforme={r['conforme']} erreurs={len(r['erreurs'])} occurrences={r['occurrences']} repères={r['reperes_lus']}")
    for e in r["erreurs"][:40]:
        print(" -", e)
    sys.exit(0 if r["conforme"] else 2)


if __name__ == "__main__":
    main()
