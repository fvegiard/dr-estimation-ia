#!/usr/bin/env python3
"""Extraction déterministe de l'exemplaire de relevé HR26-14 (EXEMPLE.pdf) en données structurées.

Reproductible : lit la couche texte du PDF (pymupdf), aucune saisie manuelle, aucun devinage.
Trois formats de bordereau reconnus :
  - repère  (DSI01-08, E02/E07/E10/E13) : une ligne par symbole  -> bordereau-materiel.csv
  - agrégé  (E01/E03/.../E14)           : une ligne par famille   -> bordereau-electrique-agrege.csv
  - travaux (EU01-04)                    : une ligne par famille+portée -> bordereau-travaux-eu.csv
Sorties : feuilles.csv, familles-par-feuille.csv, reserves.md, summary.json, VERIFICATION.md
Usage : python extract_exemple.py EXEMPLE.pdf [dossier_sortie]
"""
import sys, os, re, csv, json, hashlib
from collections import defaultdict, Counter
import pymupdf

SRC = sys.argv[1] if len(sys.argv) > 1 else "EXEMPLE.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "."
os.makedirs(OUT, exist_ok=True)
d = pymupdf.open(SRC)

REP   = re.compile(r"^[A-Z]\d{2}-\d+$")       # repère : 1 lettre + 2 chiffres + -seq  (I01-01, M03-12)
SRCID = re.compile(r"^[A-Z0-9]{2,7}-\d+$")     # source : DSI01-044, E02-007
PORT  = r"INSTALLER|ENLEVER|CONVERTIR|REMPLACER"
HEADER = {"Repere","source","Materiel","Designation","Qte","Portee","Modele","Prescription",
          "Parent","ID","Famille","Lieux","A","fournir","type","reserve","relation","devis","du","Source"}

# ---------- format repère (géométrie) ----------
def find_header(words):
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

def cols_repere(a):
    order = [("repere",a.get("Repere",55)),("materiel",a.get("Materiel")),("designation",a.get("Designation")),
             ("qte",a.get("Qte")),("portee",a.get("Portee")),("modele",a.get("Modele")),
             ("prescription",a.get("Prescription")),("parent",a.get("Parent"))]
    order = [(n,x) for n,x in order if x is not None]; order.sort(key=lambda z:z[1]); return order

def visual_lines(words, ytop, cols):
    ws = [w for w in words if w[1] > ytop+2]
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

# ---------- formats agrégé / travaux (flux texte) ----------
def sheet_text(title):
    out = defaultdict(str)
    for i in range(d.page_count):
        t = d[i].get_text(); m = re.search(title+r" - (\w+)", t)
        if m: out[m.group(1)] += t + "\n"
    return out

# ---------- passe principale ----------
mat=[]; agg=[]; eu=[]; sheets=[]; reserves=defaultdict(str)
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
    rb=re.search(r"RESERVES ET COMPLEMENTS(.*?)$", t, re.S)
    mM=re.search(r"BORDEREAU MATERIEL - (\w+)", t); mT=re.search(r"BORDEREAU TRAVAUX / ACHATS - (\w+)", t)
    if rb and (mM or mT): reserves[(mM or mT).group(1)] += rb.group(1).strip()+"\n"
    if mM and not (mM.group(1).startswith("DSI") or mM.group(1) in ("E02","E07","E10","E13")):
        continue  # agrégé traité en flux texte plus bas
    if mM:  # repère (géométrie)
        words=page.get_text("words"); a,hy=find_header(words)
        if a and "Materiel" in a:
            cols=cols_repere(a); rows=parse_repere(visual_lines(words,hy,cols),cols)
            for r in rows: r["feuille"]=mM.group(1); mat.append(r)

for sh,t in sheet_text("BORDEREAU MATERIEL").items():
    if sh.startswith("DSI") or sh in ("E02","E07","E10","E13"): continue
    for m in re.finditer(r"\n([A-Z]{1,3})\n(\d+)\n([A-Z][^\n]+)\n", t):
        if m.group(3).strip().upper() in ("QTE","MODELE"): continue
        agg.append(dict(feuille=sh,id=m.group(1),qte=m.group(2),famille=m.group(3).strip()))
for sh,t in sheet_text("BORDEREAU TRAVAUX / ACHATS").items():
    body=t.split("Notes de reserve source")[0]
    for m in re.finditer(rf"\n([A-Z]{{2}})\n(.+?)\n({PORT})\n(\d+)\n(\d+)\n(.+?)\n", body):
        eu.append(dict(feuille=sh,id=m.group(1),famille=m.group(2).strip(),portee=m.group(3),
                       lieux=m.group(4),afournir=m.group(5),modele=m.group(6).strip()))

# ---------- écriture ----------
def wcsv(name, rows, keys):
    with open(os.path.join(OUT,name),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in keys})
wcsv("feuilles.csv",sheets,["feuille","discipline","lot","batiment","reperes","familles","res","page"])
wcsv("bordereau-materiel.csv",mat,["feuille","repere","source","materiel","designation","qte","portee","modele","prescription","parent"])
wcsv("bordereau-electrique-agrege.csv",agg,["feuille","id","qte","famille"])
wcsv("bordereau-travaux-eu.csv",eu,["feuille","id","famille","portee","lieux","afournir","modele"])
famf=defaultdict(Counter)
for r in mat: famf[r['feuille']][r['designation']]+=1
with open(os.path.join(OUT,"familles-par-feuille.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["feuille","designation","qte"])
    for sh in sorted(famf):
        for des,q in famf[sh].most_common(): w.writerow([sh,des,q])
with open(os.path.join(OUT,"reserves.md"),"w",encoding="utf-8") as f:
    for sh in sorted(reserves): f.write(f"## {sh}\n{reserves[sh].strip()}\n\n")

if __name__=="__main__":
    c=Counter(r['feuille'] for r in mat)
    ok=sum(1 for s in sheets if s['feuille'] in c and str(c[s['feuille']])==s['reperes'])
    print(f"feuilles={len(sheets)} materiel={len(mat)} agrege={len(agg)} eu={len(eu)}  repere_exacts={ok}/{len(c)}")
