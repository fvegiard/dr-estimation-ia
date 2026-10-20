# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Repères lus dans la boîte : relève les appareils dont le BLOC CAO est inconnu de la bibliothèque mais dont le plan
écrit le repère DANS la boîte (DP1, PP1, SO4, SW1…), avec le texte du matériel écrit juste dessous et le numéro
« #22 » de l'appareil. Aucun appel externe, aucune clé : tout vient du texte vectoriel du plan.

Pourquoi : la bibliothèque (`bibliotheque-blocs.csv`) ne reconnaît que les formes déjà vues. Un bureau d'ingénieurs
nouveau laissait donc tout en « signature inconnue » jusqu'à ce qu'une personne étiquette les planches. Ici, un bloc
fermé de 6 à 24 pt qui contient exactement un repère de la forme `AAA99` est un appareil : sa famille est le repère
lui-même (DP1 et DP2 sont deux familles : le plan les distingue), son matériel est le texte lu sous la boîte.

Prudence : une signature n'est « traitée » (retirée des inconnues à étiqueter) que si au moins 70 % de ses blocs
portent un repère ; les autres blocs de cette signature ne sont pas relevés. Rien n'est inventé : la famille de
l'appareil (commande, luminaire, prise…) n'est pas devinée, la portée suit la règle des autres blocs (CONSERVER sans
mention NOUVEAU) et chaque repère reste en réserve « à confirmer ».

Sorties (dans WORKDIR) :
- `blocs-etiquettes-auto.csv`      : un appareil par ligne (coordonnées dans le repère de la page source, converties
                                     par blocs_vers_releve.py pour les pages tournées)
- `blocs-etiquettes-traitees.json` : signatures dont l'étiquetage a été fait ici (lu par blocs_familles_auto.py)

Usage : uv run releve/blocs_etiquettes_texte.py WORKDIR PDF [--bibliotheque releve/bibliotheque-blocs.csv]
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import PagesFeuilles  # noqa: E402
from blocs_familles_auto import _trouver  # noqa: E402

TAG = re.compile(r"^[A-Z]{1,3}\d{1,2}$")     # DP1, PP1, SO4, SW6 — pas « E103 » (3 chiffres), pas « 12 », pas « N »
NUMERO = re.compile(r"^#\d{1,4}$")           # #22
COTE_MIN, COTE_MAX = 6.0, 24.0               # pt — une boîte d'appareil ; au-dessus : meuble, local, cartouche
BAS_MAX, X_MAX = 24.0, 48.0                  # pt — fenêtre du texte du matériel sous la boîte
SEUIL = 0.7                                  # part des blocs d'une signature qui doivent porter un repère
COLS = ["feuille", "label", "x_pt", "y_pt", "x0_pt", "y0_pt", "x1_pt", "y1_pt", "designation", "portee", "materiel",
        "reserve", "note"]
MOTIF = "famille et portee deduites du repere lu dans la boite, aucune legende sur la feuille - a confirmer"   # va dans la note : le rendu lit reserve comme un drapeau


def _centre(m):
    return (m[0] + m[2]) / 2, (m[1] + m[3]) / 2


def materiel_sous(mots, x0, y0, x1, y1, exclus):
    """(texte du matériel, numéro #NN) lus sous la boîte : la ligne de mots entre la boîte et le numéro."""
    cx = (x0 + x1) / 2
    bas = [m for m in mots if m[4] not in exclus and -1 <= m[1] - y1 <= BAS_MAX and abs(_centre(m)[0] - cx) <= X_MAX]
    numero = next((m for m in sorted(bas, key=lambda m: m[1]) if NUMERO.match(m[4])), None)
    lignes = defaultdict(list)
    for m in bas:
        if NUMERO.match(m[4]) or (numero and m[1] >= numero[1] - 1):
            continue
        lignes[round(m[1] / 3)].append(m)
    if not lignes:
        return "", numero[4] if numero else ""
    premiere = lignes[min(lignes)]
    return " ".join(m[4] for m in sorted(premiere, key=lambda m: m[0])), (numero[4] if numero else "")


def main():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("pdf", nargs="?")
    ap.add_argument("--bibliotheque", default=os.path.join(REPO, "releve", "bibliotheque-blocs.csv"))
    a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    biblio = {r["signature"]: r for r in csv.DictReader(open(a.bibliotheque, encoding="utf-8"))} if os.path.exists(a.bibliotheque) else {}
    feuilles = {r["feuille"]: r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8")) if r.get("role") == "plan"}
    # signatures déjà réglées : règle de bibliothèque, ou règle du dossier (blocs-familles.csv) posée à la main
    sig_de = {}
    p_idx = os.path.join(work, "blocs-index.csv")
    if os.path.exists(p_idx):
        sig_de.update({r["sig_id"]: r["signature"] for r in csv.DictReader(open(p_idx, encoding="utf-8"))})
    p_ids = os.path.join(work, "blocs-ids.json")
    if os.path.exists(p_ids):
        sig_de.update({v: k for k, v in json.load(open(p_ids, encoding="utf-8")).items()})
    reglees = set()
    p_fam = os.path.join(work, "blocs-familles.csv")
    if os.path.exists(p_fam):
        reglees = {sig_de[r["sig_id"]] for r in csv.DictReader(open(p_fam, encoding="utf-8")) if r.get("sig_id") in sig_de}
    pages = PagesFeuilles(work, a.pdf)
    candidats = []          # (feuille, bloc, repère, boîte)
    par_sig = Counter(); avec_repere = Counter()
    rangees = []
    for f, fr in feuilles.items():
        p_b = os.path.join(work, "blocs", f + ".csv")
        if not os.path.exists(p_b):
            continue
        page = pages.page(fr)
        mots = [(w[0], w[1], w[2], w[3], w[4].strip()) for w in page.get_text("words") if w[4].strip()]
        texte = page.get_text().upper()
        portee = "INSTALLER" if "NOUVEAU" in texte and "EXISTANT/DÉMOLITION" not in texte else "CONSERVER"
        for b in csv.DictReader(open(p_b, encoding="utf-8")):
            sg = b["signature"]
            if sg in reglees:
                continue
            e, ambigu = _trouver(biblio, sg)
            if e or ambigu:
                continue
            w, h = float(b["w_pt"]), float(b["h_pt"])
            if not (COTE_MIN <= w <= COTE_MAX and COTE_MIN <= h <= COTE_MAX):
                par_sig[sg] += 1
                continue
            x, y = float(b["x_pt"]), float(b["y_pt"])
            x0, y0, x1, y1 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
            dedans = [m for m in mots if x0 <= _centre(m)[0] <= x1 and y0 <= _centre(m)[1] <= y1]
            reperes = [m[4] for m in dedans if TAG.match(m[4]) and m[4] != f]
            par_sig[sg] += 1
            if len(reperes) != 1:
                continue
            avec_repere[sg] += 1
            mat, numero = materiel_sous(mots, x0, y0, x1, y1, {reperes[0]})
            rangees.append({"sg": sg, "feuille": f, "label": reperes[0], "x": x, "y": y, "box": (x0 - 0.5, y0 - 0.5, x1 + 0.5, y1 + 0.5),
                            "designation": numero, "portee": portee, "mat": mat})
    ok = {sg for sg, n in par_sig.items() if n and avec_repere[sg] / n >= SEUIL}
    gardees = [r for r in rangees if r["sg"] in ok]
    # un repère = une famille : le matériel est le texte le plus fréquent lu sous ce repère
    texte_de = {}
    for tag in {r["label"] for r in gardees}:
        c = Counter(r["mat"] for r in gardees if r["label"] == tag and r["mat"])
        texte_de[tag] = c.most_common(1)[0][0] if c else ""
    sorties, vus = [], []
    for r in sorted(gardees, key=lambda r: (r["feuille"], r["y"], r["x"])):
        if any(v[0] == r["feuille"] and v[1] == r["label"] and abs(v[2] - r["x"]) <= 2.5 and abs(v[3] - r["y"]) <= 2.5 for v in vus):
            continue
        vus.append((r["feuille"], r["label"], r["x"], r["y"]))
        sorties.append({"feuille": r["feuille"], "label": r["label"], "x_pt": f"{r['x']:.1f}", "y_pt": f"{r['y']:.1f}",
                        "x0_pt": f"{r['box'][0]:.1f}", "y0_pt": f"{r['box'][1]:.1f}", "x1_pt": f"{r['box'][2]:.1f}", "y1_pt": f"{r['box'][3]:.1f}",
                        "designation": r["designation"], "portee": r["portee"], "materiel": texte_de.get(r["label"], ""),
                        "reserve": "1", "note": f"repere {r['label']} lu dans la boite"
                        + (f" ; materiel lu sous la boite : {texte_de[r['label']]}" if texte_de.get(r["label"]) else " ; aucun texte de materiel sous la boite") + " ; " + MOTIF})
    with open(os.path.join(work, "blocs-etiquettes-auto.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(sorties)
    json.dump({"signatures": sorted(ok)}, open(os.path.join(work, "blocs-etiquettes-traitees.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    par_tag = Counter(s["label"] for s in sorties)
    print(f"{len(sorties)} appareils lus par repere dans la boite ({len(par_tag)} reperes : "
          + ", ".join(f"{t} x{n}" for t, n in sorted(par_tag.items())) + f") ; {len(ok)} signatures traitees")


if __name__ == "__main__":
    main()
