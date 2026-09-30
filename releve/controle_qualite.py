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
  Q8 appareil de la nomenclature jamais relevé sur les plans et absent de reserves.md ;
  Q9 (si une référence est fournie) écart par famille > 5 % de la référence.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys

REPERE = re.compile(r"\[?\b([A-Z]{1,4}\d?)(\d+)\.(\d+)\]?")
TOLERANCE_REF = 0.05


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


def controler(work, reference=None, feuille_ref=None, feuille=None):
    err, avert, mal = [], [], []
    classement = lire_csv(os.path.join(work, "feuilles-classement.csv"), mal)
    nomen = lire_csv(os.path.join(work, "nomenclature.csv"), mal)
    occ = lire_csv(os.path.join(work, "occurrences-visuel.csv"), mal) + lire_csv(os.path.join(work, "occurrences-texte.csv"), mal)
    occ = [o for o in occ if o.get("exclure") not in ("1", "oui")]
    tailles = {r["feuille"]: (float(r["largeur_pt"] or 0), float(r["hauteur_pt"] or 0)) for r in lire_csv(os.path.join(work, "feuilles.csv"))}
    reserves = open(os.path.join(work, "reserves.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(work, "reserves.md")) else ""

    # Q0 : lignes mal formées (champ en trop = virgule non échappée dans un libellé ou une note)
    for m in mal:
        err.append(f"Q0 ligne mal formée : {m}")
    # Q1
    for f in ("feuilles-classement.csv", "nomenclature.csv", "reserves.md", "rapport-releve.md"):
        p = os.path.join(work, f)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            err.append(f"Q1 sortie manquante ou vide : {f}")
    plans = [r["feuille"] for r in classement if r.get("type") == "plan"]
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
        W, H = tailles.get(o.get("feuille"), (0, 0))
        try:
            x, y = float(o.get("x_pt") or o.get("x") or -1), float(o.get("y_pt") or o.get("y") or -1)
        except ValueError:
            x = y = -1
        if W and not (0 <= x <= W and 0 <= y <= H):
            err.append(f"Q7 coordonnées hors feuille : {o.get('feuille')} {o.get('label')} ({x}, {y})")
    # Q8
    comptes = collections.Counter(o.get("label") for o in occ if o.get("feuille") in plans)
    for lab in sorted(labels):
        if lab and not comptes.get(lab) and lab not in reserves:
            err.append(f"Q8 {lab!r} est dans la nomenclature mais n'est relevé sur aucun plan (ni justifié en réserve)")
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
    res = {"conforme": not err, "erreurs": err, "avertissements": avert, "occurrences": len(occ), "reperes_lus": n_reperes,
           "comparaison_reference": comparaison}
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
