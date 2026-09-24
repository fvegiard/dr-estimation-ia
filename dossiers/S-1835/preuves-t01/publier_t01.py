"""S-1835 / T-01: rebuild the deliverables from the corrected occurrences and update the dossier.

    python dossiers/S-1835/preuves-t01/publier_t01.py INBOX_DIR OUTBOX_DIR DOSSIER_DIR

Run after analyse_t01.py (which rewrote WORKDIR/occurrences-*.csv). OUTBOX_DIR = <OUTBOX>/S-1835, WORKDIR = OUTBOX_DIR/travail.
Steps: classement + nomenclature + reserves (+ the proposed rapport-releve.md, embedded in the report) in WORKDIR,
build_qpl.py and render_pdf.py (no agent, no native Plan Expert export: RELEVE_NATIF=0), releve.xlsx through
outils/assembler_dossier.py run in a scratch directory (so it cannot overwrite files owned by others), STATUT.md through
releve/run.py::statut plus the addendum sections, then copies the files this fix owns into DOSSIER_DIR and rewrites
SHA256SUMS.txt. Every figure written here comes from resume-t01.json, the CSV next to it or the Drive inventory.
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
S = "S-1835"
SPEAKER = "Haut-parleur existant — dépose/entreposage"
INVENTORY = os.path.join(REPO, "docs", "inventaire-drive-2026-09-23", "dossiers", "s-1835 esbg  rehabilitation inbterieur.json")
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "releve"))


def fr(v, d=1):
    """French decimal formatting."""
    return f"{v:.{d}f}".replace(".", ",")


def pct(v):
    return fr(100 * v) + " %"


BASE_REV = "2875138"   # takeoff as delivered before this fix (origin/releve-S-1835): inputs are read from it, so reruns are idempotent


def read(p):
    return open(p, encoding="utf-8").read()


def base(rel):
    """Content of dossiers/S-1835/<rel> at BASE_REV."""
    return subprocess.run(["git", "show", f"{BASE_REV}:dossiers/{S}/{rel}"], cwd=REPO, check=True, capture_output=True, text=True).stdout


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def rows(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def classement(work):
    buf = io.StringIO()
    rd = list(csv.DictReader(io.StringIO(base("feuilles-classement.csv"))))
    titles = {"D420": "ÉTAGE BLOC B", "D421": "ÉTAGE BLOC C", "D422": "ÉTAGE BLOC D"}
    out = []
    for r in rd:
        if r["feuille"] in titles:
            r = dict(r, type="remplacee", note=f"cartouche=T-{r['feuille']} · TÉLÉCOM DÉMOLITION PHASE 1 {titles[r['feuille']]} — remplacée par {r['feuille']}_ADD (addenda T-01)")
        out.append(r)
        if r["feuille"] == "D210_ADD_2":
            for f, t in titles.items():
                out.append({"feuille": f + "_ADD", "type": "plan", "echelle": "100",
                            "note": f"cartouche=T-{f} rév.1 · TÉLÉCOM DÉMOLITION PHASE 1 {t} EXISTANT/DÉMOLITION (addenda T-01)"})
            out.append({"feuille": "D420_ADD_2", "type": "autre", "echelle": "",
                        "note": "texte de l'addenda T-01 (18 août 2026) — pas un doublon de D420_ADD"})
    w = csv.DictWriter(buf, fieldnames=["feuille", "type", "echelle", "note"], lineterminator="\n")
    w.writeheader(); w.writerows(out)
    write(os.path.join(work, "feuilles-classement.csv"), buf.getvalue())


def nomenclature(work):
    t = base("nomenclature.csv")
    t = replace_once(t, ",T-D4xx note générale 1\n", ",T-D4xx note générale 1; T-D420 à T-D422 rév. 1 (addenda T-01)\n")
    write(os.path.join(work, "nomenclature.csv"), t)


def reserves(work, R, inv_extra):
    t = base("reserves.md")
    ps = {r["feuille"]: int(r["apres"]) for r in rows("avant-apres-haut-parleurs.csv")}
    detail = ", ".join(f"{f} {n}" for f, n in ps.items() if n and f != "TOTAL")
    basement = sum(R["sous_sol_disques"].values())
    old = [l for l in t.splitlines() if l.startswith("11. **R-011")][0]
    t = t.replace(old, (
        f"11. **R-011 — Télécom (haut-parleurs).** Les haut-parleurs d'appel général (disque noir Ø 10,6 pt dans un carré pointillé ; "
        f"légende T-001 « encastré plafond », la variante murale a le même disque) sont relevés par lecture vectorielle : "
        f"**{R['haut_parleurs_apres']}** après l'addenda T-01 ({detail}). Sous-sol D400–D403 : {basement} disque noir et aucun tracé noir de symbole "
        f"télécom, **le 0 est vérifié** (`preuves-t01/zooms/sous-sol-*.jpg`). Aucun cercle vide « en surface » ni « HP extérieur » sur les plans. "
        f"Aucun autre symbole télécom n'est compté (note : aucun câble ne doit être démantelé). Bloc D : les notes de T-D403 et T-D413 disent "
        f"« démantelés, ne doivent pas être entreposés », alors que le libellé dit dépose/entreposage ; les {ps.get('D413', 0)} haut-parleurs de D413 "
        f"et les {ps.get('D422_ADD', 0)} de D422_ADD (sa note reprend la formule des blocs B, C et C1) restent sous ce libellé, à ventiler si "
        f"l'estimateur chiffre le démantèlement à part."))
    rev = {r["feuille_originale"]: r for r in R["revisions"]}
    gone = R["t01_retires_du_dessin"]
    g420 = next(g for g in gone if g["feuille_originale"] == "D420")
    rdc = next(o for o in R["recalages"] if o["recouvrement"] == "oui" and o["feuille_a"] == "D411")
    noise = max(o["part_commune"] for o in R["recalages"] if o["recouvrement"] == "non")
    t = t.rstrip("\n") + "\n" + "\n".join([
        f"14. **R-014 — Addenda T-01 appliqué.** Le texte (18 août 2026, 1 page, feuille `D420_ADD_2`) et les 3 plans T-D420, T-D421 et T-D422 "
        f"rév. 1 remplacent les originaux (classés `remplacee`). Seul changement écrit : protéger le conduit de 63 mm de la fibre optique "
        f"B-111.4 ↔ D-132.2 (note spécifique 1 de T-D420 : S-006 → B-111.4 par S-003 et B-116). Comparaison vectorielle des 3 feuilles "
        f"(`preuves-t01/preuves-t01.md`) : T-D422 est le même dessin décalé de {fr(rev['D422']['dx_pt'])} pt ({pct(rev['D422']['part_commune'])} de tracés "
        f"communs) ; T-D420 et T-D421 recadrent les vues ({pct(rev['D420']['part_commune'])} et {pct(rev['D421']['part_commune'])} de tracés communs). "
        f"Haut-parleurs : {sum(R['original_hp'].values())} sur les originaux, {sum(R['t01_hp'].values())} sur T-01, {R['t01_nouveaux']} nouveau.",
        f"15. **R-015 — Chevauchement D420/D421 et haut-parleur retiré par T-01.** Les vues originales D420 et D421 se recouvraient "
        f"({R['doublons_par_paire'].get('D420|D421', 0)} haut-parleurs dessinés deux fois, donc comptés deux fois dans le relevé précédent). "
        f"T-01 supprime ce recouvrement : {R['t01_doublons_resolus']} de ces haut-parleurs restent comptés une fois sur l'autre feuille T-01, et "
        f"{R['t01_appareils_retires']} (corridor, D420 ({fr(g420['x_pt'])}, {fr(g420['y_pt'])}) = D421 ({fr(g420['x_autre'])}, {fr(g420['y_autre'])})) "
        f"n'est plus dessiné sur aucune feuille T-01. Le texte de l'addenda n'en parle pas : il n'est pas compté (la version d'addenda prime), "
        f"à confirmer auprès de l'ingénieur.",
        f"16. **R-016 — Doublons RDC D411/D412.** D411 et D412 montrent la même bande de plan (recalage {fr(rdc['dx_pt'])} / {fr(rdc['dy_pt'])} pt, "
        f"{pct(rdc['part_commune'])} de tracés communs) : les {rdc['doublons']} haut-parleurs de D412 sont ceux de D411 (locaux C-025, C-028…). "
        f"Comptés une fois sur D411, retirés de D412 (`preuves-t01/marques-retirees.csv`). Aucune autre paire de feuilles d'un même étage ne se "
        f"recouvre (meilleure part commune {pct(noise)}, `preuves-t01/recalage-feuilles.csv`).",
        f"17. **R-017 — Protection du conduit de fibre optique (T-01).** Sujétion sans symbole : pas de compteur. Tracé ajouté par T-01 "
        f"(traits noirs de 0,42 pt des 3 feuilles, bande de raccord comprise) : {fr(R['trace_fibre_m_1_100'])} m à 1:100. À chiffrer en forfait ou à métrer.",
        f"18. **R-018 — Addendas non reçus.** L'inventaire Drive liste aussi {inv_extra}. Ils ne sont pas dans l'INBOX de ce relevé et n'ont pas été lus.",
    ]) + "\n"
    write(os.path.join(work, "reserves.md"), t)


def proposals(dossier, R):
    """Exact replacements for files owned by other agents (ecart.md, rapport-releve.md); applied to WORKDIR copies only."""
    ref = {r["libellé humain"]: r for r in csv.DictReader(open(os.path.join(dossier, "reference-quantites.csv"), encoding="utf-8"))}
    hp_h = int(ref["HAUT PARLEUR"]["quantité"])
    n_sheets = sum(1 for _ in csv.DictReader(open(os.path.join(os.environ["T01_WORK"], "feuilles.csv"), encoding="utf-8")))
    rap = [
        ("1. J'ai classé les 31 feuilles (`feuilles-classement.csv`) et lu le texte de l'addenda E-01 (D210_ADD_2). Les 8 feuilles d'addenda remplacent E-002 et E-D210 à E-D222.",
         f"1. J'ai classé les 31 feuilles (`feuilles-classement.csv`) et lu le texte de l'addenda E-01 (D210_ADD_2). Les 8 feuilles d'addenda remplacent E-002 et E-D210 à E-D222. "
         f"Reprise du 2026-09-24 : l'addenda télécom T-01 (texte D420_ADD_2 + 3 plans) remplace T-D420 à T-D422 ({n_sheets} feuilles au total, voir `preuves-t01/`)."),
        ("- Occurrences visuelles : 3254.", f"- Occurrences visuelles : {R['marques_visuel_apres']}."),
        ("| Haut-parleur existant — dépose/entreposage | 152 |", f"| Haut-parleur existant — dépose/entreposage | {R['haut_parleurs_apres']} |"),
        ("- Le sous-sol télécom (D400-D403) compte 0 haut-parleur, à vérifier.",
         f"- Le sous-sol télécom (D400-D403) compte {sum(R['sous_sol_disques'].values())} haut-parleur : vérifié (aucun symbole télécom noir, `preuves-t01/zooms/sous-sol-*.jpg`)."),
    ]
    ec = [
        ("Relevé IA : `runs/S-1835/OUTBOX/S-1835/travail/occurrences-visuel.csv` (3254 marques).",
         f"Relevé IA : `runs/S-1835/OUTBOX/S-1835/travail/occurrences-visuel.csv` ({R['marques_visuel_apres']} marques, addenda T-01 intégré)."),
        ("| Haut-parleurs (dépose + réinstallation) | 153 | 152 (+3 « classe — par autres ») | 99,3 % | — |",
         f"| Haut-parleurs (dépose + réinstallation) | {hp_h} | {R['haut_parleurs_apres']} (+3 « classe — par autres ») | "
         f"{pct(min(hp_h, R['haut_parleurs_apres']) / hp_h)} | — |"),
    ]
    L = ["# Changements proposés aux fichiers tenus par d'autres (générés par `publier_t01.py`)", "",
         "Chaque ligne « avant » existe une seule fois dans le fichier ; remplacer par « après ».", ""]
    for name, pairs in (("rapport-releve.md", rap), ("ecart.md", ec)):
        L += [f"## {name}", ""]
        for a, b in pairs:
            L += ["avant :", "", "```", a, "```", "", "après :", "", "```", b, "```", ""]
    write(os.path.join(HERE, "changements-proposes.md"), "\n".join(L))
    t = base("rapport-releve.md")
    for a, b in rap:
        t = replace_once(t, a, b)
    return t


def sha(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(inbox, outbox, dossier):
    work = os.path.join(outbox, "travail")
    os.environ["T01_WORK"] = work
    R = json.load(open(os.path.join(HERE, "resume-t01.json"), encoding="utf-8"))
    from src.validation import addenda
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    in_sizes = {os.path.getsize(os.path.join(inbox, f)) for f in os.listdir(inbox)}
    not_received = [a for a in addenda.inventory_addenda(inv) if a["folder"] or a["size"] not in in_sizes]
    inv_extra = " et ".join(f"« {a['name']} » (sous-dossier non détaillé)" if a["folder"] else f"« {a['name']} » ({a['size']} o)" for a in not_received)

    classement(work)
    nomenclature(work)
    reserves(work, R, inv_extra)
    write(os.path.join(work, "rapport-releve.md"), proposals(dossier, R))

    steps, pe = [], os.path.join(outbox, f"{S}-planexpert")
    for name, cmd in (("build_qpl", ["releve/build_qpl.py", work, S, pe]), ("render_pdf", ["releve/render_pdf.py", work, S, outbox])):
        t = time.time()
        subprocess.run([sys.executable] + cmd, cwd=REPO, check=True, env=dict(os.environ, RELEVE_NATIF="0"))
        steps.append((name, time.time() - t, "ok"))
    steps.append(("total", sum(s[1] for s in steps), ""))
    with tempfile.TemporaryDirectory() as tmp:     # assembler writes ./dossiers/<S>: keep it away from files owned by others
        subprocess.run([sys.executable, os.path.join(REPO, "outils", "assembler_dossier.py"), S, outbox, os.path.join(tmp, "pas-de-reference")],
                       cwd=tmp, check=True)
        shutil.copy2(os.path.join(tmp, "dossiers", S, "releve.xlsx"), os.path.join(dossier, "releve.xlsx"))

    import run as runmod
    runmod.statut(S, inbox, outbox, work, steps, None, True)
    st = read(os.path.join(outbox, "STATUT.md"))
    st = re.sub(r"État : \*\*TERMINÉ\*\*", "État : **TERMINÉ** (addendas E-01 et T-01 intégrés ; reprise T-01 du 2026-09-24)", st)
    per_sheet = rows("avant-apres-haut-parleurs.csv")
    labels = rows("avant-apres-libelles.csv")
    add = ["## Addendas", "",
           "| addenda | fichiers d'entrée | feuilles | traitement |", "|---|---|---|---|",
           "| E-01 (20 août 2024) | `…Addenda - E-01.pdf`, `…Addenda - E-01 - Plans.pdf` | E002_ADD, D210_ADD … D222_ADD ; texte D210_ADD_2 | remplacent E-002 et E-D210 à E-D222 (R-001) |",
           "| T-01 (18 août 2026) | `…Addenda - T-01.pdf`, `…Addenda - T-01 - Plans.pdf` | D420_ADD, D421_ADD, D422_ADD ; texte D420_ADD_2 | remplacent T-D420 à T-D422 ; comparaison vectorielle et zooms dans `preuves-t01/` (R-014 à R-017) |",
           "", "## Addendas non intégrés", ""]
    for a in not_received:
        why = "sous-dossier non détaillé par l'inventaire Drive, contenu inconnu" if a["folder"] else "absent de l'INBOX de ce relevé, non lu ; addenda administratif d'après son nom (ADM), à confirmer"
        add.append(f"- `{a['name']}` — {why} (R-018)")
    add += ["", "## Haut-parleurs : avant / après l'addenda T-01", "",
            f"Sous-sol D400–D403 : {sum(R['sous_sol_disques'].values())} haut-parleur, vérifié (aucun symbole télécom noir sur les 4 feuilles, "
            "`preuves-t01/zooms/sous-sol-*.jpg`).", "", "| feuille | avant | après | écart |", "|---|--:|--:|--:|"]
    add += [f"| {r['feuille']} | {r['avant']} | {r['apres']} | {int(r['ecart']):+d} |" for r in per_sheet]
    add += ["", "## Libellés : avant / après", "", "| libellé | avant | après | écart |", "|---|--:|--:|--:|"]
    add += [f"| {r['libelle']} | {r['avant']} | {r['apres']} | {int(r['ecart']):+d} |" for r in labels]
    add += ["", "Tables produites par `preuves-t01/analyse_t01.py` (fichiers `avant-apres-*.csv`).", ""]
    st = st.replace("## Sorties", "\n".join(add) + "\n## Sorties", 1)
    agent = st.index("## Agent de relevé")
    end = st.index("## reserves.md")
    st = st[:agent] + "\n".join([
        "## Reprise addenda T-01 (sans agent, 2026-09-24)", "",
        "- `prepare.py` sur les 6 fichiers d'entrée ci-dessus → 35 feuilles ;",
        "- `preuves-t01/analyse_t01.py` : détection vectorielle des haut-parleurs, recalage des feuilles d'un même étage, comparaison original/T-01, "
        "réécriture des occurrences (seul le libellé haut-parleur change) ;",
        "- `preuves-t01/zooms_t01.py` : zooms `releve/zoom.py` côte à côte ;",
        "- `preuves-t01/publier_t01.py` : `build_qpl.py`, `render_pdf.py` (RELEVE_NATIF=0), `releve.xlsx`, ce STATUT ;",
        "- relevé de l'agent d'origine (claude -p headless, 2026-09-23) conservé pour tous les autres libellés.", "", ""]) + st[end:]
    write(os.path.join(dossier, "STATUT.md"), st)

    for src, dst in ((f"{S}-Plans-annotes.pdf", "Plans-annotes.pdf"), (f"{S}-Rapport-de-metre.pdf", "Rapport-de-metre.pdf"),
                     (f"{S}-Rapport-de-metre.md", "Rapport-de-metre.md"), (f"{S}-Dossier-complet.pdf", "Dossier-complet.pdf")):
        shutil.copy2(os.path.join(outbox, src), os.path.join(dossier, dst))
    for f in os.listdir(pe):
        shutil.copy2(os.path.join(pe, f), os.path.join(dossier, "planexpert", f))
    for f in ("reserves.md", "nomenclature.csv", "feuilles-classement.csv"):
        shutil.copy2(os.path.join(work, f), os.path.join(dossier, f))
    with open(os.path.join(dossier, "SHA256SUMS.txt"), "w") as fh:     # same layout as outils/assembler_dossier.py
        for dp, _, fs in os.walk(dossier):
            for f in sorted(fs):
                if f != "SHA256SUMS.txt" and "__pycache__" not in dp:
                    p = os.path.join(dp, f)
                    fh.write(f"{sha(p)}  {os.path.relpath(p, dossier)}\n")
    print("ok", R["haut_parleurs_avant"], "->", R["haut_parleurs_apres"])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
