# /// script
# requires-python = ">=3.12"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Assemble le livrable d'un dossier dans dossiers/<S>/ à partir d'un run releve/ (OUTBOX) et de sa comparaison.

    uv run outils/assembler_dossier.py <S> <OUTBOX/S> <dossier reference>

Produit : releve.xlsx (Résumé, Par feuille, Marques, Nomenclature, Réserves), ecart.md, reference-quantites.csv,
Plans-annotes.pdf, Rapport-de-metre.pdf, Dossier-complet.pdf, STATUT.md, projet Plan Expert (.qpl + PNG) dans planexpert/.
Rien n'est inventé : tout est copié ou tabulé depuis les fichiers du run.
"""
import csv, os, shutil, sys, hashlib
from collections import Counter, defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def rows(p):
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []

def main(S, out, ref):
    dst = os.path.join("dossiers", S); os.makedirs(dst, exist_ok=True); os.makedirs(os.path.join(dst, "entree"), exist_ok=True)
    W = os.path.join(out, "travail")
    nom = {r["label"]: r for r in rows(os.path.join(W, "nomenclature.csv"))}
    feuilles = {r["feuille"]: r for r in rows(os.path.join(W, "feuilles.csv"))}
    for r in rows(os.path.join(W, "feuilles-classement.csv")):
        if r["feuille"] in feuilles: feuilles[r["feuille"]].update(r)
    occ = [r for r in rows(os.path.join(W, "occurrences-texte.csv")) + rows(os.path.join(W, "occurrences-visuel.csv"))
           if (r.get("exclure") or "").strip().lower() not in ("1", "oui", "x", "true")]
    import re
    def nomf(f):
        m = re.search(r"cartouche\s*=\s*([A-Za-z]{1,3}-?\d{2,4}[A-Za-z]?)", feuilles.get(f, {}).get("note") or "")
        return m.group(1).upper().replace("-", "") if m else f
    wb = Workbook(); H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="1F4E79")
    def sheet(title, header, data, widths=None):
        ws = wb.create_sheet(title); ws.append(header)
        for c in ws[1]: c.font = H; c.fill = F; c.alignment = Alignment(vertical="center", wrap_text=True)
        for r in data: ws.append(r)
        for i, w in enumerate(widths or [18] * len(header), 1): ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A2"
        return ws
    tot = Counter(o["label"] for o in occ); fam = Counter((nom.get(o["label"], {}).get("famille") or "?") for o in occ)
    sheet("Résumé", ["Soumission", "Marques", "Libellés", "Feuilles de plan", "Familles"],
          [[S, len(occ), len(tot), sum(1 for f in feuilles.values() if f.get("type") == "plan"), len(fam)]], [16, 12, 12, 16, 12])
    sheet("Par famille", ["Famille", "Quantité"], sorted(fam.items()), [22, 12])
    sheet("Par libellé", ["Libellé", "Famille", "Quantité", "Description", "Source (légende)"],
          [[l, nom.get(l, {}).get("famille", ""), n, nom.get(l, {}).get("description", ""), nom.get(l, {}).get("source", "")] for l, n in sorted(tot.items())], [34, 14, 10, 40, 30])
    pf = defaultdict(Counter)
    for o in occ: pf[o["feuille"]][o["label"]] += 1
    sheet("Par feuille", ["Feuille (cartouche)", "Feuille (fichier)", "Libellé", "Quantité"],
          [[nomf(f), f, l, n] for f in sorted(pf) for l, n in sorted(pf[f].items())], [18, 22, 34, 10])
    sheet("Marques", ["Feuille (cartouche)", "Feuille (fichier)", "Libellé", "x (pt)", "y (pt)", "Source", "Note"],
          [[nomf(o["feuille"]), o["feuille"], o["label"], o.get("x_pt"), o.get("y_pt"), o.get("source", ""), o.get("note", "")] for o in occ], [16, 20, 34, 9, 9, 10, 50])
    sheet("Feuilles", ["Feuille (fichier)", "Cartouche / note", "Type", "Échelle", "Fichier source", "Page", "Mots"],
          [[f, r.get("note", ""), r.get("type", ""), r.get("echelle", ""), r.get("fichier", ""), r.get("page", ""), r.get("nb_mots", "")] for f, r in sorted(feuilles.items())], [20, 50, 10, 8, 40, 6, 8])
    res = open(os.path.join(W, "reserves.md"), encoding="utf-8").read().splitlines() if os.path.exists(os.path.join(W, "reserves.md")) else []
    sheet("Réserves", ["Ligne"], [[l] for l in res if l.strip()], [140])
    del wb["Sheet"]; wb.save(os.path.join(dst, "releve.xlsx"))
    for src, name in ((os.path.join(out, "ecart.md"), "ecart.md"), (os.path.join(out, "reference-quantites.csv"), "reference-quantites.csv"),
                      (os.path.join(out, "dupuis-quantites.csv"), "reference-quantites.csv"), (os.path.join(out, "STATUT.md"), "STATUT.md"),
                      (os.path.join(out, f"{S}-Plans-annotes.pdf"), "Plans-annotes.pdf"), (os.path.join(out, f"{S}-Rapport-de-metre.pdf"), "Rapport-de-metre.pdf"),
                      (os.path.join(out, f"{S}-Rapport-de-metre.md"), "Rapport-de-metre.md"), (os.path.join(out, f"{S}-Dossier-complet.pdf"), "Dossier-complet.pdf")):
        if os.path.exists(src): shutil.copy2(src, os.path.join(dst, name))
    for extra in ("rapport-releve.md", "reserves.md", "nomenclature.csv", "feuilles-classement.csv"):
        if os.path.exists(os.path.join(W, extra)): shutil.copy2(os.path.join(W, extra), os.path.join(dst, extra))
    pe = os.path.join(out, f"{S}-planexpert")
    if os.path.isdir(pe):
        shutil.copytree(pe, os.path.join(dst, "planexpert"), dirs_exist_ok=True)
    pr = os.path.join(out, "travail", "ecart-preuves")
    if os.path.isdir(pr): shutil.copytree(pr, os.path.join(dst, "ecart-preuves"), dirs_exist_ok=True)
    if os.path.isdir(ref):
        for f in os.listdir(ref): shutil.copy2(os.path.join(ref, f), os.path.join(dst, "entree", "reference-" + f))
    with open(os.path.join(dst, "SHA256SUMS.txt"), "w") as fh:
        for dp, _, fs in os.walk(dst):
            for f in sorted(fs):
                if f != "SHA256SUMS.txt": p = os.path.join(dp, f); fh.write(f"{sha(p)}  {os.path.relpath(p, dst)}\n")
    print(f"{S} : {len(occ)} marques, {len(tot)} libellés → {dst}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
