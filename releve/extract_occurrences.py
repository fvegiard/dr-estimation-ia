# /// script
# requires-python = ">=3.12"
# ///
"""Étape 2a (déterministe) : étiquettes texte → occurrences.

Usage : uv run releve/extract_occurrences.py WORKDIR

Lit WORKDIR/nomenclature.csv (colonnes : label, famille, forme, rgb, jeton_regex, description, source)
et WORKDIR/feuilles-classement.csv (colonnes : feuille, type, echelle, note ; type = plan | legende | schema | tableau | detail | autre).
Pour chaque feuille de type `plan`, chaque mot vectoriel de texte/<feuille>-mots.csv dont le texte correspond
exactement (fullmatch, sensible à la casse) à un `jeton_regex` devient une occurrence, positionnée au centre du mot.
Écrit WORKDIR/occurrences-texte.csv (feuille, label, x_pt, y_pt, source, note) — l'agent peut ensuite l'éditer
(retirer les faux positifs : bulles d'axes, numéros de circuits…) et compléter occurrences-visuel.csv.
"""
import csv, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import read_csv

def main(work):
    nom = read_csv(os.path.join(work, "nomenclature.csv"))
    rules = []
    for r in nom:
        rx = (r.get("jeton_regex") or "").strip()
        if rx:
            try:
                rules.append((re.compile(rx), r["label"].strip()))
            except re.error as e:
                print(f"regex invalide pour {r['label']!r} : {rx!r} ({e})")
    plans = [r["feuille"] for r in read_csv(os.path.join(work, "feuilles-classement.csv")) if (r.get("type") or "").strip() == "plan"]
    out = []
    stats = collections.Counter()
    for f in plans:
        p = os.path.join(work, "texte", f"{f}-mots.csv")
        if not os.path.exists(p):
            print("feuille sans mots :", f); continue
        vus = []   # dédoublonnage : un même mot répété à moins de 4 pt (texte superposé, calques dupliqués — audit S-1844 v2) = 1 occurrence
        for w in read_csv(p):
            for rx, label in rules:
                if rx.fullmatch(w["mot"]):
                    cx, cy = float(w["cx"]), float(w["cy"])
                    if any(l == label and abs(cx - x) < 4 and abs(cy - y) < 4 for l, x, y in vus):
                        stats[(f, "(doublons ignorés)")] += 1
                        break
                    vus.append((label, cx, cy))
                    out.append({"feuille": f, "label": label, "x_pt": w["cx"], "y_pt": w["cy"], "source": "texte", "note": f"mot '{w['mot']}'"})
                    stats[(f, label)] += 1
                    break
    with open(os.path.join(work, "occurrences-texte.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=["feuille", "label", "x_pt", "y_pt", "source", "note"]); wr.writeheader(); wr.writerows(out)
    print(f"{len(out)} occurrences texte sur {len(plans)} feuilles → occurrences-texte.csv")
    for (f, l), n in sorted(stats.items()):
        print(f"  {f:10} {n:4}  {l}")

if __name__ == "__main__":
    main(sys.argv[1])
