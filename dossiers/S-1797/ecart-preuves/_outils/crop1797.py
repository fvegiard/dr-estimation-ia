import sys,csv
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
T='/home/claude/releve-auto/runs/S-1797/OUTBOX/S-1797/travail/'
sheet,x0,y0,x1,y1,out=sys.argv[1],*map(float,sys.argv[2:6]),sys.argv[6]
filt=sys.argv[7].split('|') if len(sys.argv)>7 and sys.argv[7] else None
maxw=int(sys.argv[8]) if len(sys.argv)>8 else 1600
w={r['feuille']:float(r['largeur_pt']) for r in csv.DictReader(open(T+'feuilles.csv'))}[sheet]
s=5694/w
im=Image.open(T+'rasters/'+sheet+'.png').convert('RGB')
c=im.crop((int(x0*s),int(y0*s),int(x1*s),int(y1*s)))
d=ImageDraw.Draw(c)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except: f=None
n=0
for r in csv.DictReader(open(T+'occurrences-visuel.csv')):
  if r['feuille']!=sheet: continue
  if filt and not any(k in r['label'] for k in filt): continue
  x,y=float(r['x_pt']),float(r['y_pt'])
  if x0<=x<=x1 and y0<=y<=y1:
    n+=1;px,py=(x-x0)*s,(y-y0)*s
    d.ellipse((px-18,py-18,px+18,py+18),outline=(255,0,0),width=3)
    d.text((px+20,py-24),f"{n}",fill=(255,0,0),font=f)
    print(n,r['label'],x,y,r['note'])
if c.width>maxw: c=c.resize((maxw,int(c.height*maxw/c.width)))
c.save(out)
