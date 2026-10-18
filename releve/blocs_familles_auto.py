# /// script
# requires-python = ">=3.12"
# ///
"""Étiquetage AUTOMATIQUE des signatures de blocs depuis la bibliothèque `releve/bibliotheque-blocs.csv` : chaque
signature déjà vue dans un dossier précédent (même bureau d'ingénieurs = mêmes blocs CAO) reçoit sa famille sans
intervention. Écrit WORKDIR/blocs-familles.csv (format lu par blocs_vers_releve.py) et WORKDIR/blocs-a-etiqueter.md :
les signatures fréquentes (≥ --min instances sur les feuilles plan) ABSENTES de la bibliothèque — à étiqueter une fois
(planches signatures-NN.png) puis à ajouter à la bibliothèque. Jamais bloquant : le relevé sort avec ce qui est connu,
l'inconnu va en réserve.

Usage : uv run releve/blocs_familles_auto.py WORKDIR [--bibliotheque releve/bibliotheque-blocs.csv] [--min 3]
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["sig_id", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles", "portee", "note"]
TOL = 0.25      # tolérance par valeur numérique de la signature (pictogrammes : courbes quantifiées à ±0,1–0,2 d'un tracé à l'autre)


def _proche(a, b, tol=TOL):
    """Deux signatures « proches » : même structure (nombre de parties, nops, fermée, remplie, lettre) et chaque valeur
    numérique à ≤ TOL — les pictogrammes (détecteurs, enseignes, encastrés d'urgence) ne sont jamais identiques au 1/10."""
    try:
        sa, sb = json.loads(a), json.loads(b)
    except Exception:  # noqa
        return False
    if len(sa) != len(sb) or len(sa[0]) != len(sb[0]) or (len(sa) > 2 and sa[2] != sb[2]) or abs(sa[1] - sb[1]) > tol:
        return False
    for pa, pb in zip(sa[0], sb[0]):
        if pa[2:] != pb[2:] or abs(pa[0] - pb[0]) > tol or abs(pa[1] - pb[1]) > tol:
            return False
    return True


def _trouver(biblio, signature):
    if signature in biblio:
        return biblio[signature]
    # appariement tolérant SEULEMENT pour les entrées qui le déclarent (colonne `tolerance` > 0 : pictogrammes à courbes) —
    # un luminaire 1'x4' ou une prise se reconnaît à l'identique, sinon on attrape des morceaux de mur
    cands = [b for k, b in biblio.items() if b["label"] != "IGNORER" and float(b.get("tolerance") or 0) > 0 and _proche(k, signature, float(b["tolerance"]))]
    return cands[0] if len(cands) == 1 or (cands and len({c["label"] for c in cands}) == 1) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("--bibliotheque", default=os.path.join(REPO, "releve", "bibliotheque-blocs.csv"))
    ap.add_argument("--min", type=int, default=3)
    a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    p_idx = os.path.join(work, "blocs-index.csv")
    if not os.path.exists(p_idx):
        sys.exit("blocs-index.csv absent : lancer blocs_vectoriels.py puis blocs_vignettes.py d'abord")
    biblio = {r["signature"]: r for r in csv.DictReader(open(a.bibliotheque, encoding="utf-8"))} if os.path.exists(a.bibliotheque) else {}
    index = list(csv.DictReader(open(p_idx, encoding="utf-8")))
    feuilles = {r["feuille"] for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8")) if r.get("role") == "plan"}
    # un blocs-familles.csv déjà écrit à la main (dossier en cours de validation) a priorité : on n'écrase jamais un choix humain
    p_fam = os.path.join(work, "blocs-familles.csv")
    manuel = {r["sig_id"]: r for r in csv.DictReader(open(p_fam, encoding="utf-8"))} if os.path.exists(p_fam) else {}
    fam, inconnues = [], []
    for r in index:
        if r["sig_id"] in manuel:
            fam.append(manuel[r["sig_id"]]); continue
        b = _trouver(biblio, r["signature"])
        if b and b["label"] == "IGNORER":          # vu et jugé non-appareil dans un dossier précédent (mur, trame, cotation)
            continue
        if b:
            feuilles_ok = " ".join(sorted(f for f in feuilles if re.fullmatch(b["feuilles_regex"], f))) if b.get("feuilles_regex") else ""
            fam.append({"sig_id": r["sig_id"], "label": b["label"], "famille": b["famille"], "forme": b["forme"], "code": b["code"], "materiel": b["materiel"],
                        "legende_no": b["legende_no"], "diam_min": b["diam_min"], "diam_max": b["diam_max"], "feuilles": feuilles_ok,
                        "portee": b.get("portee", ""), "note": f"bibliothèque : {b['source']}" + (f" ; {b['note']}" if b.get("note") else "")})
        elif int(r["n_plans"] or 0) >= a.min:
            inconnues.append(r)
    # blocs RARES (sous le seuil de l'index) : un pictogramme (détecteur, enseigne) a une signature quasi unique ; s'il
    # est proche d'une entrée de la bibliothèque, il entre dans l'index (sig_id neuf, mémoire blocs-ids.json) et sa famille
    connus = {r["signature"] for r in index}
    p_ids = os.path.join(work, "blocs-ids.json")
    ids = json.load(open(p_ids, encoding="utf-8")) if os.path.exists(p_ids) else {}
    prochain = max([int(v[1:]) for v in ids.values()] + [int(r["sig_id"][1:]) for r in index] + [0]) + 1
    ajouts = []
    for f in sorted(feuilles):
        p_b = os.path.join(work, "blocs", f + ".csv")
        if not os.path.exists(p_b):
            continue
        for b_ in csv.DictReader(open(p_b, encoding="utf-8")):
            sg = b_["signature"]
            if sg in connus:
                continue
            e = _trouver(biblio, sg)
            if not e or e["label"] == "IGNORER":
                continue
            connus.add(sg)
            sid = ids.get(sg) or f"S{prochain:03d}"
            if sg not in ids:
                ids[sg] = sid; prochain += 1
            ajouts.append({"sig_id": sid, "signature": sg, "n_plans": 1, "par_feuille": f"{f}:1", "legende": "", "lettre": "", "exemple": f"{f} ({b_['x_pt']},{b_['y_pt']})", "diametre_pt": b_["diametre_pt"]})
            fam.append({"sig_id": sid, "label": e["label"], "famille": e["famille"], "forme": e["forme"], "code": e["code"], "materiel": e["materiel"],
                        "legende_no": e["legende_no"], "diam_min": e["diam_min"], "diam_max": e["diam_max"], "feuilles": "", "portee": e.get("portee", ""),
                        "note": f"bibliothèque (appariement tolérant) : {e['source']}"})
    if ajouts:
        with open(p_idx, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(index[0].keys())); w.writerows(ajouts)
        json.dump(ids, open(p_ids, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(p_fam, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(fam)
    p_inst = os.path.join(work, "blocs-instances.csv")
    if not os.path.exists(p_inst):
        open(p_inst, "w", encoding="utf-8").write("feuille,x_pt,y_pt,label,famille,forme,code,materiel,legende_no,portee,rayon_pt,note\n")
    lignes = ["# Signatures de blocs à étiqueter (absentes de la bibliothèque)", "",
              f"Bibliothèque : `{os.path.relpath(a.bibliotheque, REPO)}` ({len(biblio)} signatures). Étiquetées automatiquement : {len(fam)}. "
              f"Inconnues fréquentes (≥ {a.min} instances) : {len(inconnues)} — voir les planches `signatures-NN.png`, ajouter la ligne à "
              "`blocs-familles.csv` du dossier ET à la bibliothèque (signature, label, famille, forme, code, matériel).", ""]
    lignes += [f"- {r['sig_id']} : n={r['n_plans']} ({r['par_feuille']}) lettre « {r['lettre']} » légende « {r['legende'][:50]} » ex. {r['exemple']}" for r in inconnues]
    open(os.path.join(work, "blocs-a-etiqueter.md"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print(f"{len(fam)} signatures étiquetées depuis la bibliothèque ({len(manuel)} manuelles conservées, {len(ajouts)} pictogrammes rares appariés) ; {len(inconnues)} inconnues fréquentes → blocs-a-etiqueter.md")


if __name__ == "__main__":
    main()
