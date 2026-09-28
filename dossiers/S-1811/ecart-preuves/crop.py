# Usage: crop.py FEUILLE x0 y0 x1 y1 out.png [zoom] [labels-regex]
# Rend la zone (pt, repère des CSV) depuis le PDF vectoriel de la feuille et entoure les marques IA.
import sys, csv, re, pymupdf
from PIL import Image, ImageDraw
T='/home/claude/releve-auto/runs/S-1811/OUTBOX/S-1811/travail/'
f,x0,y0,x1,y1,out=sys.argv[1],*map(float,sys.argv[2:6]),sys.argv[6]
z=float(sys.argv[7]) if len(sys.argv)>7 else 4
rx=re.compile(sys.argv[8]) if len(sys.argv)>8 else None
doc=pymupdf.open(T+'feuilles/'+f+'.pdf'); p=doc[0]
# repère CSV = repère page affiché (après rotation)
r=pymupdf.Rect(x0,y0,x1,y1)
if p.rotation:
    pix=p.get_pixmap(matrix=pymupdf.Matrix(z,z))
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples).crop((int(x0*z),int(y0*z),int(x1*z),int(y1*z)))
else:
    pix=p.get_pixmap(matrix=pymupdf.Matrix(z,z),clip=r)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
d=ImageDraw.Draw(im)
n=0
for fn in ['occurrences-texte.csv','occurrences-visuel.csv']:
    for row in csv.DictReader(open(T+fn)):
        if row['feuille']!=f or row.get('exclure','') in ('1',): continue
        if rx and not rx.search(row['label']): continue
        x,y=float(row['x_pt']),float(row['y_pt'])
        if x0<=x<=x1 and y0<=y<=y1:
            X,Y=(x-x0)*z,(y-y0)*z; n+=1
            col=(220,0,0) if row['source']=='texte' else (0,90,220)
            d.ellipse([X-6*z,Y-6*z,X+6*z,Y+6*z],outline=col,width=3)
            d.text((X+6*z,Y-6*z),row['label'][:22],fill=col)
im.save(out); print(out,im.size,'marques',n,'rotation',p.rotation)
