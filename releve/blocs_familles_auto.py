# /// script
# requires-python = ">=3.12"
# ///
"""Étiquetage AUTOMATIQUE des signatures de blocs depuis la bibliothèque `releve/bibliotheque-blocs.csv` : chaque
signature déjà vue dans un dossier précédent (même bureau d'ingénieurs = mêmes blocs CAO) reçoit sa famille sans
intervention. Écrit WORKDIR/blocs-familles.csv (format lu par blocs_vers_releve.py ; colonne origine=auto pour les règles de la
bibliothèque — une ligne modifiée à la main, ou sans origine=auto, est une correction humaine : jamais écrasée) et
WORKDIR/blocs-a-etiqueter.md :
les signatures fréquentes (≥ --min instances sur les feuilles plan) ABSENTES de la bibliothèque — à étiqueter une fois
(planches signatures-NN.png) puis à ajouter à la bibliothèque. Jamais bloquant : le relevé sort avec ce qui est connu,
l'inconnu va en réserve.

Usage : uv run releve/blocs_familles_auto.py WORKDIR [--bibliotheque releve/bibliotheque-blocs.csv] [--min 3]
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["sig_id", "label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles", "portee", "reserve", "origine", "note"]
CLES_REGLE = ("label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "portee", "reserve")   # ce qu'une règle dit (hors feuilles)
COLS_INDEX = ["sig_id", "signature", "n_plans", "par_feuille", "legende", "lettre", "exemple", "diametre_pt"]   # = blocs_vignettes.py
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


CLES_RELEVE = ("label", "famille", "forme", "code", "materiel", "legende_no", "diam_min", "diam_max", "feuilles_regex")


def _trouver(biblio, signature):
    """Entrée de bibliothèque pour une signature : exacte, sinon tolérante (pictogrammes). Retourne (entrée, ambigu).
    Plusieurs candidats tolérants : ils doivent s'accorder sur TOUTES les propriétés du relevé (label, famille, forme,
    code, matériel, légende, diamètres, feuilles) — sinon `ambigu`, jamais « le premier » (revue Codex PR #28). S'ils ne
    diffèrent que par la PORTÉE (détecteur existant pointillé / neuf plein aux signatures voisines), l'appareil est bien
    là : il est relevé avec la portée par défaut de la feuille et une réserve * « portée à confirmer » — un appareil
    non compté est pire qu'un appareil compté à vérifier."""
    if signature in biblio:
        return biblio[signature], False
    # appariement tolérant SEULEMENT pour les entrées qui le déclarent (colonne `tolerance` > 0 : pictogrammes à courbes) —
    # un luminaire 1'x4' ou une prise se reconnaît à l'identique, sinon on attrape des morceaux de mur
    cands = [b for k, b in biblio.items() if b["label"] != "IGNORER" and float(b.get("tolerance") or 0) > 0 and _proche(k, signature, float(b["tolerance"]))]
    if not cands:
        return None, False
    if len({tuple((c.get(k) or "").strip() for k in CLES_RELEVE) for c in cands}) != 1:
        return None, True
    portees = {(c.get("portee") or "").strip() for c in cands}
    if len(portees) == 1:
        return cands[0], False
    e = dict(cands[0]); e["portee"] = ""
    e["reserve"] = "portée à confirmer : la bibliothèque connaît ce pictogramme en " + " et en ".join(sorted(p or "défaut feuille" for p in portees))
    return e, False


def _feuilles_admises(entree, feuilles):
    """(liste de feuilles admises, applicable) : sans `feuilles_regex` → toutes (chaîne vide = toutes pour
    blocs_vers_releve.py) ; avec regex → les feuilles du dossier qui y répondent, et « non applicable » s'il n'y en a
    aucune — une restriction sans correspondance ne devient jamais un accès global (revue Codex PR #28)."""
    rx = (entree.get("feuilles_regex") or "").strip()
    if not rx:
        return "", True
    ok = sorted(f for f in feuilles if re.fullmatch(rx, f))
    return " ".join(ok), bool(ok)


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
    # PLUSIEURS règles par sig_id possibles (blocs_vers_releve.py choisit par diamètre et feuille) : liste, jamais « la
    # dernière ligne » (revue Codex PR #28)
    manuel = {}
    if os.path.exists(p_fam):
        for r in csv.DictReader(open(p_fam, encoding="utf-8")):
            manuel.setdefault(r["sig_id"], []).append(r)
    p_ids = os.path.join(work, "blocs-ids.json")
    ids = json.load(open(p_ids, encoding="utf-8")) if os.path.exists(p_ids) else {}
    # règles AUTOMATIQUES inchangées (colonne origine=auto, écrite ici, et contenu identique à ce que la bibliothèque
    # donnerait aujourd'hui) : régénérées — leurs feuilles admises sont recalculées sur les feuilles ACTUELLES du
    # dossier (relance après ajout d'E204 : E203 → E203 E204). Toute ligne modifiée par une personne, sans colonne
    # origine ou avec origine≠auto, est une correction humaine : conservée telle quelle (revue Codex PR #28).
    sig_de = {r["sig_id"]: r["signature"] for r in index}
    sig_de.update({v: k for k, v in ids.items()})
    regenerees = 0
    for sid, rows in list(manuel.items()):
        if not all((r.get("origine") or "").strip() == "auto" for r in rows):
            continue
        sg = sig_de.get(sid)
        e = _trouver(biblio, sg)[0] if sg else None
        if e and e["label"] != "IGNORER" and all(all((r.get(k) or "").strip() == (e.get(k) or "").strip() for k in CLES_REGLE) for r in rows):
            del manuel[sid]; regenerees += 1
    fam, inconnues, ambigus = [], [], []
    vus_manuel = set()

    def regle(sid, b, note):
        return {"sig_id": sid, "label": b["label"], "famille": b["famille"], "forme": b["forme"], "code": b["code"], "materiel": b["materiel"],
                "legende_no": b["legende_no"], "diam_min": b["diam_min"], "diam_max": b["diam_max"], "feuilles": "", "portee": b.get("portee", ""),
                "reserve": b.get("reserve", ""), "origine": "auto", "note": note + (f" ; {b['note']}" if b.get("note") else "")}

    for r in index:
        if r["sig_id"] in manuel:
            fam.extend(manuel[r["sig_id"]]); vus_manuel.add(r["sig_id"]); continue
        b, ambigu = _trouver(biblio, r["signature"])
        if ambigu:
            ambigus.append(r); continue
        if b and b["label"] == "IGNORER":          # vu et jugé non-appareil dans un dossier précédent (mur, trame, cotation)
            continue
        if b:
            feuilles_ok, applicable = _feuilles_admises(b, feuilles)
            if not applicable:                     # restreinte à des feuilles absentes de ce dossier : connue, mais pas ici
                continue
            rg = regle(r["sig_id"], b, f"bibliothèque : {b['source']}"); rg["feuilles"] = feuilles_ok; fam.append(rg)
        elif int(r["n_plans"] or 0) >= a.min:
            inconnues.append(r)
    # blocs RARES (sous le seuil de l'index) : un pictogramme (détecteur, enseigne) a une signature quasi unique ; s'il
    # est proche d'une entrée de la bibliothèque — ou s'il porte déjà une règle MANUELLE (sig_id connu de blocs-ids.json,
    # écrit à la passe précédente) — il entre dans l'index (sig_id stable) et sa famille suit. La règle manuelle gagne
    # toujours sur la bibliothèque (revue Codex PR #28 : relancer ne doit jamais écraser une correction humaine).
    connus = {r["signature"] for r in index}
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
            sid_connu = ids.get(sg)
            if sid_connu and sid_connu in manuel:
                e, note = manuel[sid_connu][0], "règle manuelle conservée"
                if not any(not (m.get("feuilles") or "").strip() or f in m["feuilles"].split() for m in manuel[sid_connu]):
                    continue                       # toutes les règles manuelles limitent leurs feuilles et celle-ci n'en est pas
            else:
                e, ambigu = _trouver(biblio, sg)
                if ambigu:
                    ambigus.append({"sig_id": "", "n_plans": 1, "par_feuille": f"{f}:1", "lettre": "", "legende": "", "exemple": f"{f} ({b_['x_pt']},{b_['y_pt']})"}); continue
                if not e or e["label"] == "IGNORER":
                    continue
                _, applicable = _feuilles_admises(e, feuilles)
                rx = (e.get("feuilles_regex") or "").strip()
                if not applicable or (rx and not re.fullmatch(rx, f)):
                    continue                       # même restriction de feuilles que pour les signatures de l'index
                note = f"bibliothèque (appariement tolérant) : {e['source']}"
            connus.add(sg)
            sid = sid_connu or f"S{prochain:03d}"
            if sg not in ids:
                ids[sg] = sid; prochain += 1
            ajouts.append({"sig_id": sid, "signature": sg, "n_plans": 1, "par_feuille": f"{f}:1", "legende": "", "lettre": "", "exemple": f"{f} ({b_['x_pt']},{b_['y_pt']})", "diametre_pt": b_["diametre_pt"]})
            if sid in manuel:
                if sid not in vus_manuel:
                    fam.extend(manuel[sid]); vus_manuel.add(sid)
            else:
                rg = regle(sid, e, note); rg["feuilles"] = _feuilles_admises(e, feuilles)[0]; fam.append(rg)
    # règles manuelles dont la signature n'est plus dans l'index ni dans les blocs : conservées telles quelles (jamais effacées)
    for sid, rs in manuel.items():
        if sid not in vus_manuel:
            fam.extend(rs); vus_manuel.add(sid)
    if ajouts:
        with open(p_idx, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS_INDEX); w.writerows(ajouts)     # un index vide (en-tête seul) s'écrit aussi
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
    if ambigus:
        lignes += ["", "## Appariements AMBIGUS (plusieurs entrées tolérantes de la bibliothèque, propriétés contradictoires — non relevés)", ""]
        lignes += [f"- {r.get('sig_id') or '(bloc rare)'} : n={r['n_plans']} ({r['par_feuille']}) ex. {r['exemple']}" for r in ambigus]
    open(os.path.join(work, "blocs-a-etiqueter.md"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    # version structurée, reprise par blocs_vers_releve.py (reserves.md → PDF) et run.py (STATUT « À VÉRIFIER ») :
    # l'inconnu ne reste jamais confiné à un fichier de travail (revue Copilot PR #28)
    json.dump({"bibliotheque": os.path.relpath(a.bibliotheque, REPO), "etiquetees": len(fam),
               "inconnues": [{"sig_id": r["sig_id"], "n_plans": int(r["n_plans"] or 0), "par_feuille": r["par_feuille"], "exemple": r["exemple"]} for r in inconnues],
               "ambigues": [{"sig_id": r.get("sig_id") or "", "n_plans": int(r["n_plans"] or 0), "par_feuille": r["par_feuille"], "exemple": r["exemple"]} for r in ambigus]},
              open(os.path.join(work, "blocs-a-etiqueter.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(fam)} signatures étiquetées depuis la bibliothèque ({sum(len(v) for v in manuel.values())} manuelles conservées, {regenerees} automatiques régénérées, {len(ajouts)} pictogrammes rares appariés) ; "
          f"{len(inconnues)} inconnues fréquentes, {len(ambigus)} ambiguës → blocs-a-etiqueter.md")


if __name__ == "__main__":
    main()
