"""Comparaison relevé visuel E201 ↔ QPL humain (jamais modifié). Méthode explicite :
1. Repère : humain = 2 × mon raster − (11, 15) px (calé sur les 24 OS3, résidu ≤ 5 px).
2. Appareils : chaque compteur humain est relié à un ou plusieurs de mes libellés (table CORR, déduite de la géométrie, à confirmer).
   Toutes les paires (marque humaine, marque IA) de classes compatibles à ≤ 40 px humain sont triées par distance et appariées
   une à une (chaque marque sert une seule fois). Rappel = marques humaines appariées / marques humaines ; précision = idem côté IA.
3. Repères de logements A–G : séparés, appariés par type identique à ≤ 150 px humain ; non mélangés aux appareils.
4. Exclus de la comparaison : bulles A, 1, 2 (annotations) et les 36 avertisseurs (retirés, sans équivalent humain)."""
import xml.etree.ElementTree as ET, csv, collections, numpy as np
D='dossiers/S-1294/'
t=ET.parse(D+'reference/S-1294-E201-human-reference.qpl').getroot()
H={c.get('Name').strip():[(float(e.get('X')),float(e.get('Y'))) for e in c.findall('Element')] for c in t.iter('Counter')}
rows=list(csv.DictReader(open(D+'occurrences-visuel.csv')))
mine=[(r['label'],(2*float(r['x_px'])-11,2*float(r['y_px'])-15),r['categorie']) for r in rows]
CORR={'SERV  TYPE H':['Luminaire cercle+support','Cercle à point'],'SERV PRISE':['Appareil mural'],'SERV DECT GAINE':['Appareil mural'],
'SERV TYPE E':['Boîte à diagonale'],'SERV EXIT':['Enseigne de sortie'],'SERV OS3':['Capteur OS3'],'SERV STATION':['Carré F'],
'SERV KLAXON':['Carré K'],'SERV TYPE K':['Symbole K○'],'SERV DP2':['Boîtier DP2'],'SERV DECT':['Disque B1'],'SERV TH':['Carré T'],'SERV TH R':['Carré T'],
'SERV MX2':['Module Mx2'],'SW1':['SW1','Icône ≈'],'SERV ISO':['Module ISO'],'SERV RM':['Module RM'],'SERV MRA':['Module MRA'],
'SERV C 1250W':['Hexagone C'],'SERV C 750W':['Hexagone C'],'SERV C 1750W':['Hexagone C'],'SERV RELAIS':['Carré R'],
'SERV DIRECT':['Bulle B','Carré à croix'],'SERV VE-12':['Boîte VE-12'],'SERV DEBIT':['Icône sous Mx2']}
TOL=40
app=[m for m in mine if m[2]=='appareil']
pairs=[]
for hn,labs in CORR.items():
    tol=80 if 'VE' in hn else TOL
    for i,p in enumerate(H[hn]):
        for j,(l,q,_) in enumerate(app):
            if any(l.startswith(x) for x in labs):
                d=float(np.hypot(p[0]-q[0],p[1]-q[1]))
                if d<=tol: pairs.append((d,hn,i,j))
pairs.sort(); uh=set(); um=set(); res=collections.defaultdict(list)
for d,hn,i,j in pairs:
    if (hn,i) in uh or j in um: continue
    uh.add((hn,i)); um.add(j); res[hn].append((i,j,d))
nH=sum(len(H[k]) for k in CORR); nA=len(app); ok=len(uh)
with open(D+'appariement-E201.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow('compteur_humain,x_h,y_h,libelle_ia,x_ia,y_ia,distance_px_humain'.split(','))
    for hn,L in res.items():
        for i,j,d in L: w.writerow([hn,*map(round,H[hn][i]),app[j][0],*map(round,app[j][1]),round(d,1)])
out=[f'**Appareils** : rappel {ok}/{nH} = {100*ok/nH:.1f} % ; précision {len(um)}/{nA} = {100*len(um)/nA:.1f} % (tolérance {TOL} px humain, appariement un-à-un par distance croissante).','',
'| Compteur humain | Humain | Apparié | Mes libellés rattachés |','|---|--:|--:|---|']
for hn,labs in CORR.items(): out.append(f'| {hn} | {len(H[hn])} | {len(res[hn])} | {", ".join(labs)} |')
out+=['','Humain non apparié (px humain) : '+str([(hn,*map(round,p)) for hn in CORR for i,p in enumerate(H[hn]) if (hn,i) not in uh]),'',
'Mes appareils sans appariement : '+str(collections.Counter(app[j][0] for j in range(nA) if j not in um)),'']
# repères de logements
rl=[(r['label'][-1],(2*float(r['x_px'])-11,2*float(r['y_px'])-15)) for r in rows if r['categorie']=='repere_logement']
agp=[]
for ty in 'ABCDEFG':
    for i,p in enumerate(H[ty]):
        for j,(t2,q) in enumerate(rl):
            if t2==ty:
                d=float(np.hypot(p[0]-q[0],p[1]-q[1]))
                if d<=150: agp.append((d,ty,i,j))
agp.sort(); a=set(); b=set()
for d,ty,i,j in agp:
    if (ty,i) in a or j in b: continue
    a.add((ty,i)); b.add(j)
out+=[f'**Repères de logements A–G (séparés)** : {len(a)}/48 appariés par type identique à ≤ 150 px humain ; types par étage lus sur le plan : '+str(dict(sorted(collections.Counter(t2 for t2,_ in rl).items())))+'.']
open(D+'ecart-E201.md','w').write('# Écart E201 — relevé visuel corrigé vs QPL humain (S-1294)\n\n'+__doc__+'\n\n'+'\n'.join(out)+'\n')
print('\n'.join(out))
