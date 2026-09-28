import sys,csv
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'.')
T='/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/travail/'
PAGE={'E400':10,'E401':11,'E402':12,'E403':13,'E405':14,'E406':15,'E407':16,'E408':17,'E409':18}
AB={'Prise duplex':'D','Prise duplex DDFT':'G','Prise DDFT Ei':'Ei','Prise micro-onde':'MO','Prise mobilier':'Mb','Raccord lave-vaisselle':'LV','Prise cuisinière C':'C','Sortie data':'T','Sortie data mobilier':'Tm'}
def sbs(sheet,x0,y0,w,h,out,z=4,labels=None):
    S=2997/2383.92; R=5694/2383.92
    d=Image.open(f'p{PAGE[sheet]:02d}.png').convert('RGB').crop((int(x0*S),int(y0*S),int((x0+w)*S),int((y0+h)*S))).resize((int(w*z),int(h*z)))
    r=Image.open(T+f'rasters/{sheet}.png').convert('RGB').crop((int(x0*R),int(y0*R),int((x0+w)*R),int((y0+h)*R))).resize((int(w*z),int(h*z)))
    dr=ImageDraw.Draw(r)
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
    except: f=None
    for fn in ['occurrences-texte.csv','occurrences-visuel.csv']:
        for row in csv.DictReader(open(T+fn)):
            if row['feuille']!=sheet: continue
            if labels and row['label'] not in labels: continue
            x=(float(row['x_pt'])-x0)*z; y=(float(row['y_pt'])-y0)*z
            if 0<=x<w*z and 0<=y<h*z:
                dr.ellipse((x-9,y-9,x+9,y+9),outline=(0,170,0),width=3)
                dr.text((x+10,y-8),AB.get(row['label'],row['label'][:10]),fill=(0,120,0),font=f)
    im=Image.new('RGB',(2*int(w*z)+10,int(h*z)),'white'); im.paste(d,(0,0)); im.paste(r,(int(w*z)+10,0))
    ImageDraw.Draw(im).text((5,5),f'Dupuis {sheet} p{PAGE[sheet]}  |  plan + marques IA v2  x0={x0} y0={y0}',fill=(0,0,200),font=f)
    im.save(out)
if __name__=='__main__':
    a=sys.argv; sbs(a[1],float(a[2]),float(a[3]),float(a[4]),float(a[5]),a[6],float(a[7]) if len(a)>7 else 4)
