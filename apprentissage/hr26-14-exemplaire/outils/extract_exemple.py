#!/usr/bin/env python3
"""Extraction déterministe de l'exemplaire de relevé HR26-14 (EXEMPLE.pdf) en données structurées.

Reproductible : lit la couche texte du PDF (pymupdf), aucune saisie manuelle, aucun devinage.
Trois formats de bordereau reconnus (ancrage par géométrie de colonnes, en-tête du tableau) :
  - repère  (DSI01-08, E02/E07/E10/E13) : une ligne par symbole  -> bordereau-materiel.csv
  - agrégé  (E01/E03/.../E14)           : une ligne par famille   -> bordereau-electrique-agrege.csv
  - travaux (EU01-04)                    : une ligne par famille+portée -> bordereau-travaux-eu.csv
Écrit directement : feuilles.csv, bordereau-materiel.csv, bordereau-electrique-agrege.csv,
                    bordereau-travaux-eu.csv, reserves.md.
Puis appelle regen_derives.main() pour les dérivés : familles-par-feuille.csv, summary.json, VERIFICATION.md
(source unique de la logique des dérivés ; échoue si la validation de schéma du bordereau matériel échoue).
Usage : python extract_exemple.py EXEMPLE.pdf [dossier_sortie]
"""
import sys, os, re, csv
from collections import defaultdict
import pymupdf

SRC = sys.argv[1] if len(sys.argv) > 1 else "EXEMPLE.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "."
os.makedirs(OUT, exist_ok=True)
d = pymupdf.open(SRC)

REP   = re.compile(r"^[A-Z]\d{2}-\d+$")        # repère : 1 lettre + 2 chiffres + -seq  (I01-01, M03-12)
SRCID = re.compile(r"^[A-Z0-9]{2,7}-\d+$")     # source : DSI01-044, E02-007
PORT  = r"INSTALLER|ENLEVER|CONVERTIR|REMPLACER"
HEADER = {"Repere","source","Materiel","Designation","Qte","Portee","Modele","Prescription",
          "Parent","ID","Famille","Lieux","A","fournir","type","reserve","relation","devis","du","Source"}
REPERE_SHEETS = ("E02", "E07", "E10", "E13")   # feuilles E- au format repère (les autres E- sont agrégées)

# ---------- outils géométrie ----------
def find_header(words):
    """Ancre des colonnes du format repère (repère par la présence de Modele + Materiel)."""
    by_y = defaultdict(list)
    for w in words: by_y[round(w[1])].append(w)
    for y in sorted(by_y):
        near = [w for yy in by_y for w in by_y[yy] if abs(yy-y) < 10]
        ntoks = {w[4] for w in near}
        if "Modele" in ntoks and "Materiel" in ntoks:
            anchors = {}
            for w in near:
                if w[4] in HEADER: anchors.setdefault(w[4], w[0])
            return anchors, max(w[1] for w in near)
    return None, None

def header_anchors(words, markers):
    """x de chaque mot d'en-tête `markers` sur la première ligne qui les contient tous ; renvoie (dict, y_bas)."""
    by = defaultdict(list)
    for w in words: by[round(w[1])].append(w)
    for y in sorted(by):
        toks = {w[4]: w[0] for w in by[y]}
        if all(m in toks for m in markers):
            return {m: toks[m] for m in markers}, max(w[3] for w in by[y])
    return None, None

def find_footer_y(words, ytop, pred):
    """y de la première ligne sous l'en-tête qui satisfait `pred(texte_ligne)` (bloc de réserves / notes)."""
    by = defaultdict(list)
    for w in words:
        if w[1] > ytop: by[round(w[1])].append(w)
    for y in sorted(by):
        line = " ".join(w[4] for w in sorted(by[y], key=lambda z: z[0]))
        if pred(line): return y
    return None

def col_lines(words, ytop, ybot, cols):
    """Regroupe les mots en lignes visuelles (bande y de 2 px) et les répartit par colonne selon x.
    Les mots au-dessus de l'en-tête (ytop) et sous le pied (ybot) sont ignorés. `cols` = [(nom, x), ...]."""
    ws = [w for w in words if w[1] > ytop+2 and (ybot is None or w[1] < ybot-1)]
    by = defaultdict(list)
    for w in ws: by[round(w[1]/2)*2].append(w)
    out = []
    for y in sorted(by):
        cells = {n: [] for n, _ in cols}
        for w in sorted(by[y], key=lambda z: z[0]):
            name = cols[0][0]
            for n, x in cols:
                if w[0] >= x-6: name = n
                else: break
            cells[name].append(w[4])
        out.append({n: " ".join(cells[n]).strip() for n, _ in cols})
    return out

# ---------- format repère (géométrie) ----------
def cols_repere(a):
    order = [("repere",a.get("Repere",55)),("materiel",a.get("Materiel")),("designation",a.get("Designation")),
             ("qte",a.get("Qte")),("portee",a.get("Portee")),("modele",a.get("Modele")),
             ("prescription",a.get("Prescription")),("parent",a.get("Parent"))]
    order = [(n,x) for n,x in order if x is not None]; order.sort(key=lambda z:z[1]); return order

def visual_lines(words, ytop, cols, ybot=None):
    ws = [w for w in words if w[1] > ytop+2 and (ybot is None or w[1] < ybot-1)]
    by = defaultdict(list)
    for w in ws: by[round(w[1]/2)*2].append(w)
    out = []
    for y in sorted(by):
        cells = [[] for _ in cols]
        for w in sorted(by[y], key=lambda z:z[0]):
            xi = 0
            for i,(n,x) in enumerate(cols):
                if w[0] >= x-6: xi = i
                else: break
            cells[xi].append(w[4])
        out.append([" ".join(c).strip() for c in cells])
    return out

def parse_repere(lines, cols):
    names = [n for n,_ in cols]; rows = []; cur = None
    for cells in lines:
        c = dict(zip(names, cells)); first = cells[0]
        if REP.match(first) and len(cells) > 1 and cells[1]:
            if cur: rows.append(cur)
            cur = dict(c); cur["source"] = ""
        elif cur and SRCID.match(first) and not cells[1] and not cur.get("source"):
            cur["source"] = first
        elif cur:
            for n,v in c.items():
                if v and n != "repere": cur[n] = (cur.get(n,"")+" "+v).strip()
    if cur: rows.append(cur)
    return [r for r in rows if REP.match(r.get("repere",""))]

# ---------- format agrégé (géométrie) ----------
def parse_agg(page):
    words = page.get_text("words")
    anc, hy = header_anchors(words, ["ID","Qte","Famille","Modele","Prescription","Source"])
    if not anc: return []
    cols = [("id",anc["ID"]),("qte",anc["Qte"]),("famille",anc["Famille"]),
            ("modele",anc["Modele"]),("prescription",anc["Prescription"]),("source",anc["Source"])]
    ybot = find_footer_y(words, hy, lambda L: L.startswith("Notes de reserve source"))
    rows = []; cur = None
    for c in col_lines(words, hy, ybot, cols):
        if c["id"] and c["qte"].isdigit():
            if cur: rows.append(cur)
            cur = {k: c[k] for k in ("id","qte","famille","modele","prescription","source")}
        elif cur:
            for k in ("famille","modele","prescription","source"):
                if c[k]: cur[k] = (cur[k]+" "+c[k]).strip()
    if cur: rows.append(cur)
    return rows

# ---------- format travaux / achats EU (géométrie) ----------
def parse_eu(page):
    words = page.get_text("words")
    anc, hy = header_anchors(words, ["ID","Famille","Portee","Lieux","A","Modele","Prescription","Source"])
    if not anc: return []
    cols = [("id",anc["ID"]),("famille",anc["Famille"]),("portee",anc["Portee"]),("lieux",anc["Lieux"]),
            ("afournir",anc["A"]),("modele",anc["Modele"]),("prescription",anc["Prescription"]),("source",anc["Source"])]
    ybot = find_footer_y(words, hy, lambda L: L.startswith("Notes de reserve source"))
    rows = []; cur = None
    for c in col_lines(words, hy, ybot, cols):
        if c["id"] and c["lieux"].isdigit():
            if cur: rows.append(cur)
            cur = {k: c[k] for k in ("id","famille","portee","lieux","afournir","modele","prescription","source")}
        elif cur:
            for k in ("famille","portee","modele","prescription","source"):
                if c[k]: cur[k] = (cur[k]+" "+c[k]).strip()
    if cur: rows.append(cur)
    return rows

# ---------- passe principale ----------
mat=[]; agg=[]; eu=[]; sheets=[]; reserves=defaultdict(str); eu_af={}
for i in range(d.page_count):
    page=d[i]; t=page.get_text()
    mR=re.search(r"RELEVE (\w+) - MATERIEL", t)
    if mR:
        sh=mR.group(1); rel=re.search(r"([0-9]+) reperes / ([0-9]+) familles / RES ([0-9]+)", t)
        rep,fam,res=(rel.groups() if rel else ("","",""))
        lot=re.search(r"(LOT [A-D])\s*-\s*([^\n]+)", t)
        disc="INCENDIE" if sh.startswith("DSI") else ("URGENCE" if sh.startswith("EU") else "ELECTRICITE")
        sheets.append(dict(feuille=sh,discipline=disc,lot=(lot.group(1) if lot else ""),
              batiment=(lot.group(2).strip() if lot else ""),reperes=rep,familles=fam,res=res,page=i+1))
    # en-tête EU : "N emplacements de travaux;M appareils a fournir" -> retenir M (appareils a fournir)
    mEU=re.search(r"BORDEREAU TRAVAUX / ACHATS - (\w+)", t)
    if mEU:
        h=re.search(r"(\d+)\s*emplacements de travaux;\s*(\d+)\s*appareils a fournir", t)
        if h: eu_af[mEU.group(1)]=h.group(2)
    # bloc RESERVES ET COMPLEMENTS (repère) -> reserves.md
    rb=re.search(r"RESERVES ET COMPLEMENTS(.*?)$", t, re.S)
    mM=re.search(r"BORDEREAU MATERIEL - (\w+)", t)
    if rb and (mM or mEU): reserves[(mM or mEU).group(1)] += rb.group(1).strip()+"\n"
    if mM:
        sh=mM.group(1)
        if sh.startswith("DSI") or sh in REPERE_SHEETS:  # repère (géométrie)
            words=page.get_text("words"); a,hy=find_header(words)
            if a and "Materiel" in a:
                ybot=find_footer_y(words,hy, lambda L: "RESERVES" in L and "COMPLEMENTS" in L)
                cols=cols_repere(a); rows=parse_repere(visual_lines(words,hy,cols,ybot),cols)
                for r in rows: r["feuille"]=sh; mat.append(r)
        else:  # agrégé (géométrie)
            for r in parse_agg(page): r["feuille"]=sh; agg.append(r)
    if mEU:
        for r in parse_eu(page): r["feuille"]=mEU.group(1); eu.append(r)

# ---------- écriture des CSV sources ----------
def wcsv(name, rows, keys):
    with open(os.path.join(OUT,name),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in keys})
for s in sheets: s["af_entete"]=eu_af.get(s["feuille"],"")
wcsv("feuilles.csv",sheets,["feuille","discipline","lot","batiment","reperes","familles","res","page","af_entete"])
wcsv("bordereau-materiel.csv",mat,["feuille","repere","source","materiel","designation","qte","portee","modele","prescription","parent"])
wcsv("bordereau-electrique-agrege.csv",agg,["feuille","id","qte","famille","modele","prescription","source"])
wcsv("bordereau-travaux-eu.csv",eu,["feuille","id","famille","portee","lieux","afournir","modele","prescription","source"])
with open(os.path.join(OUT,"reserves.md"),"w",encoding="utf-8") as f:
    for sh in sorted(reserves): f.write(f"## {sh}\n{reserves[sh].strip()}\n\n")

# ---------- dérivés (source unique : regen_derives) ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regen_derives
regen_derives.main(OUT)

if __name__=="__main__":
    from collections import Counter
    c=Counter(r['feuille'] for r in mat)
    ok=sum(1 for s in sheets if s['feuille'] in c and str(c[s['feuille']])==s['reperes'])
    print(f"feuilles={len(sheets)} materiel={len(mat)} agrege={len(agg)} eu={len(eu)}  repere_exacts={ok}/{len(c)}")
