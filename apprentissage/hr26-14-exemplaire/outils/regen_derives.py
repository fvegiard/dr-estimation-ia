#!/usr/bin/env python3
"""Régénère les fichiers dérivés depuis les CSV sources (sans le PDF).
Sorties : summary.json, familles-par-feuille.csv, VERIFICATION.md.
Utilisé par le workflow GitHub d'auto-commit pour garder les dérivés synchronisés.
Usage : python regen_derives.py <dossier>  (défaut : dossier courant)
"""
import sys, os, csv, json
from collections import defaultdict, Counter
D = sys.argv[1] if len(sys.argv) > 1 else "."
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n), encoding="utf-8")))
sheets = rd("feuilles.csv"); mat = rd("bordereau-materiel.csv")
agg = rd("bordereau-electrique-agrege.csv"); eu = rd("bordereau-travaux-eu.csv")
S = {s["feuille"]: s for s in sheets}

famf = defaultdict(Counter)
for r in mat: famf[r["feuille"]][r["designation"]] += 1
with open(os.path.join(D, "familles-par-feuille.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["feuille", "designation", "qte"])
    for sh in sorted(famf):
        for des, q in famf[sh].most_common(): w.writerow([sh, des, q])

tot_agg = sum(int(x["qte"]) for x in agg if x["qte"].isdigit())
tot_eu = sum(int(x["afournir"]) for x in eu if x["afournir"].isdigit())
summary = dict(
    dossier="HR26-14", projet="Réfection des cuisines et salles de bain et divers travaux",
    client="Office municipal d'habitation du Haut-Richelieu",
    adresse="145 rue Latour, Saint-Jean-sur-Richelieu (QC)", consultant="ARI Bureau d'études",
    emission="Pour appel d'offres (2026-08-31)",
    lots={"LOT A": "145 St-Georges", "LOT B": "155 Mercier", "LOT C": "290 Montcalm", "LOT D": "291 Chaussé"},
    nb_feuilles=len(sheets),
    totaux={"lignes_bordereau_materiel_par_repere": len(mat),
            "unites_electrique_agrege(sumQte)": tot_agg,
            "appareils_a_fournir_urgence(sumAfournir)": tot_eu},
    note_prix="Aucun prix dans l'exemplaire (grilles $ vides sur E03/E04/E05/E08). Prix à intégrer depuis la base SQL (Google Drive).")
json.dump(summary, open(os.path.join(D, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

L = ["# Vérification de l'extraction — HR26-14 (preuve chiffrée)", "",
     "Régénéré depuis les CSV sources par `outils/regen_derives.py`.", "",
     "## Bordereaux par repère (DSI + E-série M) — extrait vs en-tête RELEVE", "",
     "| Feuille | Extrait | En-tête | Statut |", "|---|---|---|---|"]
c = Counter(r["feuille"] for r in mat)
for s in sheets:
    sh = s["feuille"]
    if sh in c:
        L.append(f"| {sh} | {c[sh]} | {s['reperes']} | {'✅ exact' if str(c[sh])==s['reperes'] else '⚠ écart'} |")
L += ["", "## Électrique agrégé (E) — Σ Qté vs en-tête", "",
      "| Feuille | Lignes | Σ Qté | En-tête | Familles | Statut |", "|---|---|---|---|---|---|"]
by = defaultdict(list)
for r in agg: by[r["feuille"]].append(r)
for sh in sorted(by):
    q = sum(int(x["qte"]) for x in by[sh]); hr = S[sh]["reperes"]; fam = S[sh]["familles"]
    st = "grille de prix ($ vide)" if hr == "" else ("✅ exact" if str(q) == hr else "⚠ divergence document")
    L.append(f"| {sh} | {len(by[sh])} | {q} | {hr or '—'} | {fam or '—'} | {st} |")
L += ["", "## Éclairage d'urgence (EU) — bordereau travaux/achats", "",
      "| Feuille | Lignes | Σ Lieux | Σ À fournir | Emplacements (en-tête) | Statut |", "|---|---|---|---|---|---|"]
bye = defaultdict(list)
for r in eu: bye[r["feuille"]].append(r)
for sh in sorted(bye):
    li = sum(int(x["lieux"]) for x in bye[sh]); af = sum(int(x["afournir"]) for x in bye[sh])
    emp = S[sh]["reperes"]
    L.append(f"| {sh} | {len(bye[sh])} | {li} | {af} | {emp} | {'✅ exact' if str(li)==emp else '⚠'} |")
L += ["", "## Constats (findings)",
      "- **E09 / E12** : bordereau = 4 familles (E09 Σ98, E12 Σ107) vs plan RELEVE 6 familles / 103 (E09), 6 / 110 (E12). À réconcilier.",
      "- **E03 / E04 / E05 / E08** : grilles de prix vides — matériel relevé, prix à alimenter depuis la base SQL (Google Drive).",
      "- **Prix** : aucun prix dans l'exemplaire (relevé identification + quantités seulement).", ""]
open(os.path.join(D, "VERIFICATION.md"), "w", encoding="utf-8").write("\n".join(L))
print("dérivés régénérés :", D)
