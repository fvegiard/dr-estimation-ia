import sys,csv
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
T='/home/claude/releve-auto/runs/S-1714/OUTBOX/S-1714/travail/'
def marks(sheet):
    out=[]
    for f in ['occurrences-texte.csv','occurrences-visuel.csv']:
        for r in csv.DictReader(open(T+f)):
            if r['feuille']==sheet and r.get('exclure','0')!='1':
                out.append((r['label'],float(r['x_pt']),float(r['y_pt'])))
    return out
def crop(sheet,x0,y0,x1,y1,out,filt=None,scale=None):
    im=Image.open(T+f'rasters/{sheet}.png').convert('RGB')
    k=im.size[0]/3456.0
    box=[int(v*k) for v in (x0,y0,x1,y1)]
    c=im.crop(box)
    orig=c.copy()
    d=ImageDraw.Draw(c)
    n=0
    for l,x,y in marks(sheet):
        if x0<=x<=x1 and y0<=y<=y1 and (not filt or any(f in l for f in filt)):
            px,py=(x*k-box[0]),(y*k-box[1]); n+=1
            d.ellipse([px-14,py-14,px+14,py+14],outline=(255,0,0),width=3)
            d.text((px+16,py-10),l[:18],fill=(255,0,0))
    W,H=c.size
    sbs=Image.new('RGB',(W*2+10,H),'white'); sbs.paste(orig,(0,0)); sbs.paste(c,(W+10,0))
    if scale: sbs=sbs.resize((int(sbs.size[0]*scale),int(sbs.size[1]*scale)))
    sbs.save(out); print(out,sbs.size,'marques',n)
if __name__=='__main__':
    a=sys.argv; crop(a[1],*map(float,a[2:6]),a[6],a[7].split(',') if len(a)>7 and a[7] else None, float(a[8]) if len(a)>8 else None)
