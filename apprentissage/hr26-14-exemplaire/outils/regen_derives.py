#!/usr/bin/env python3
"""Régénère les fichiers dérivés depuis les CSV sources (sans le PDF).
Sorties : familles-par-feuille.csv, summary.json, VERIFICATION.md.
Utilisé par le workflow GitHub d'auto-commit pour garder les dérivés synchronisés,
et par extract_exemple.py après l'extraction.

Valide d'abord le schéma de bordereau-materiel.csv (repère/source valides, qté numérique,
portée non contaminée par du texte de réserve) et **échoue** (sortie 1) en cas d'erreur :
un CSV corrompu ne doit jamais être certifié « exact » silencieusement.

Usage : python regen_derives.py <dossier>  (défaut : dossier courant)
"""
import sys, os, csv, json, re
from collections import defaultdict, Counter

REP   = re.compile(r"^[A-Z]\d{2}-\d+$")
SRCID = re.compile(r"^[A-Z0-9]{2,7}-\d+$")
PORTEE = re.compile(r"^[A-Z0-9_ ]+$")         # INSTALLER, A PRECISER, RENVOI_DSI01, RENVOI_LOGEMENTS_LOT_A ...
REPERE_SHEETS = ("E02", "E07", "E10", "E13")  # feuilles E- au format repère

def is_repere_sheet(sh):
    return sh.startswith("DSI") or sh in REPERE_SHEETS

def validate_materiel(mat):
    """Retourne la liste des erreurs de schéma (vide = OK)."""
    errs = []
    for i, r in enumerate(mat, 2):  # ligne 1 = en-tête
        loc = f"L{i} ({r.get('feuille','?')} {r.get('repere','?')})"
        if not REP.match(r.get("repere", "")):
            errs.append(f"{loc} : repère invalide {r.get('repere','')!r}")
        src = r.get("source", "")
        if src and not SRCID.match(src):
            errs.append(f"{loc} : source invalide {src!r}")
        if not str(r.get("qte", "")).strip().isdigit():
            errs.append(f"{loc} : qté non numérique {r.get('qte','')!r}")
        por = r.get("portee", "")
        if por and not PORTEE.match(por):
            errs.append(f"{loc} : portée contaminée {por!r}")
    return errs

def main(D="."):
    rd = lambda n: list(csv.DictReader(open(os.path.join(D, n), encoding="utf-8")))
    sheets = rd("feuilles.csv"); mat = rd("bordereau-materiel.csv")
    agg = rd("bordereau-electrique-agrege.csv"); eu = rd("bordereau-travaux-eu.csv")
    S = {s["feuille"]: s for s in sheets}

    errs = validate_materiel(mat)
    if errs:
        print("ECHEC validation bordereau-materiel.csv (%d erreurs) :" % len(errs))
        for e in errs[:40]:
            print("  -", e)
        if len(errs) > 40:
            print("  ... (%d de plus)" % (len(errs) - 40))
        sys.exit(1)

    # familles-par-feuille : somme des quantités (une famille peut regrouper qté > 1)
    famf = defaultdict(Counter)
    for r in mat:
        q = int(r["qte"]) if str(r["qte"]).strip().isdigit() else 1
        famf[r["feuille"]][r["designation"]] += q
    with open(os.path.join(D, "familles-par-feuille.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["feuille", "designation", "qte"])
        for sh in sorted(famf):
            for des, q in famf[sh].most_common():
                w.writerow([sh, des, q])

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
        note_prix="Aucun prix dans l'exemplaire. Prix à intégrer depuis la base SQL (Google Drive).")
    json.dump(summary, open(os.path.join(D, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    L = ["# Vérification de l'extraction — HR26-14 (preuve chiffrée)", "",
         "Régénéré depuis les CSV sources par `outils/regen_derives.py`.", "",
         "## Bordereaux par repère (DSI + E-série M) — extrait vs en-tête RELEVE", "",
         "| Feuille | Extrait | En-tête | Statut |", "|---|---|---|---|"]
    c = Counter(r["feuille"] for r in mat)
    # une ligne pour CHAQUE feuille attendue au format repère (0 si aucune ligne extraite)
    for s in sheets:
        sh = s["feuille"]
        if not is_repere_sheet(sh):
            continue
        n = c.get(sh, 0)
        hdr = s["reperes"]
        st = "✅ exact" if str(n) == hdr else ("⚠ AUCUNE ligne" if n == 0 else "⚠ écart")
        L.append(f"| {sh} | {n} | {hdr or '—'} | {st} |")

    L += ["", "## Électrique agrégé (E) — Σ Qté vs en-tête", "",
          "| Feuille | Lignes | Σ Qté | En-tête | Familles | Statut |", "|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for r in agg: by[r["feuille"]].append(r)
    for sh in sorted(by):
        q = sum(int(x["qte"]) for x in by[sh] if x["qte"].isdigit()); hr = S[sh]["reperes"]; fam = S[sh]["familles"]
        st = "grille de prix ($ vide)" if hr == "" else ("✅ exact" if str(q) == hr else "⚠ divergence document")
        L.append(f"| {sh} | {len(by[sh])} | {q} | {hr or '—'} | {fam or '—'} | {st} |")

    L += ["", "## Éclairage d'urgence (EU) — bordereau travaux/achats", "",
          "| Feuille | Lignes | Σ Lieux | Empl. (en-tête) | Σ À fournir | À fournir (en-tête) | Statut |",
          "|---|---|---|---|---|---|---|"]
    bye = defaultdict(list)
    for r in eu: bye[r["feuille"]].append(r)
    for sh in sorted(bye):
        li = sum(int(x["lieux"]) for x in bye[sh] if x["lieux"].isdigit())
        af = sum(int(x["afournir"]) for x in bye[sh] if x["afournir"].isdigit())
        emp = S[sh]["reperes"]; afh = S[sh].get("af_entete", "")
        ok_li = str(li) == emp
        ok_af = (afh == "") or (str(af) == afh)
        st = "✅ exact" if (ok_li and ok_af) else "⚠ écart"
        L.append(f"| {sh} | {len(bye[sh])} | {li} | {emp or '—'} | {af} | {afh or '—'} | {st} |")

    # ---------- Constats dérivés des données (jamais codés en dur) ----------
    L += ["", "## Constats (findings)"]
    div = []
    for sh in sorted(by):
        hr = S[sh]["reperes"]
        if hr.strip():
            q = sum(int(x["qte"]) for x in by[sh] if x["qte"].isdigit())
            if str(q) != hr:
                div.append(f"- **{sh}** : bordereau Σ{q} ({len(by[sh])} familles) vs en-tête "
                            f"{hr} ({S[sh]['familles']} familles). À réconcilier.")
    grilles = sorted(sh for sh in by if not S[sh]["reperes"].strip())
    if div:
        L += div
    else:
        L.append("- Bordereaux agrégés : Σ Qté = en-tête sur toutes les feuilles chiffrées (aucune divergence).")
    if grilles:
        L.append(f"- **{' / '.join(grilles)}** : grilles de prix vides — matériel relevé, "
                 f"prix à alimenter depuis la base SQL (Google Drive).")
    for sh in sorted(bye):
        af = sum(int(x["afournir"]) for x in bye[sh] if x["afournir"].isdigit())
        afh = S[sh].get("af_entete", "")
        if afh and str(af) != afh:
            L.append(f"- **{sh}** : Σ à fournir {af} vs en-tête {afh}. À vérifier.")
    L += ["- **Prix** : aucun prix dans l'exemplaire (relevé identification + quantités seulement).", ""]

    open(os.path.join(D, "VERIFICATION.md"), "w", encoding="utf-8").write("\n".join(L))
    print("dérivés régénérés :", D)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
