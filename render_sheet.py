"""Render evidence-based markers over an unchanged source raster."""
from pathlib import Path
from collections import Counter
import json, csv, sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=200_000_000
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
COLORS=['#2C78BD','#489C60','#AA59AD','#18A6A2','#B77C38','#D14465','#7C77C4','#65705A']

def render(data):
    sheet=data['sheet']; source=ROOT/data['source']
    im=Image.open(source).convert('RGB'); scale=im.width/2000
    # Work in an image with a transparent drawing layer to retain source linework.
    layer=Image.new('RGBA',im.size);draw=ImageDraw.Draw(layer)
    counts=Counter(m['family'] for m in data['markers'])
    colors={f:COLORS[i%len(COLORS)] for i,f in enumerate(counts)}
    def text(x,y,s,size=12,color='#222222'):
        draw.text((round(x*scale),round(y*scale)),s,font=ImageFont.truetype(FONT,round(size*scale)),fill=color)
    for m in data['markers']:
        x,y=m['x'],m['y'];r=m.get('radius',3.2);c=colors[m['family']]
        draw.ellipse(tuple(round(v*scale) for v in (x-r,y-r,x+r,y+r)),fill=c+'35',outline=c,width=max(2,round(.65*scale)))
        if m.get('reserve'):text(x+r+1,y-5,'*',8,c)
    x,y,w,h=data['legend_box']
    draw.rectangle(tuple(round(v*scale) for v in (x,y,x+w,y+h)),fill='white',outline='#808080',width=max(2,round(scale*.5)))
    text(x+15,y+12,f'RELEVÉ {sheet} — MATÉRIEL',17)
    reserves=sum(bool(m.get('reserve')) for m in data['markers'])
    text(x+15,y+39,f'{len(data["markers"])} repères / {len(counts)} familles / RES {reserves} — '+data['scope'],11)
    cursor=y+65
    for family,count in counts.items():
        c=colors[family];draw.ellipse(tuple(round(v*scale) for v in (x+16,cursor+2,x+24,cursor+10)),fill=c+'35',outline=c,width=2)
        text(x+34,cursor,f'{family} : {count}',11);cursor+=20
    for note in data['notes']:text(x+15,cursor,note,10);cursor+=18
    assert cursor<y+h-4,(sheet,cursor,y+h)
    final=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
    destination=ROOT/f'S-0844-{sheet}-releve.jpg';final.save(destination,quality=96,subsampling=0)
    review=ROOT/'verification'/sheet;review.mkdir(parents=True,exist_ok=True)
    overview=final.copy();overview.thumbnail((2000,1600));overview.save(review/'overview.jpg',quality=96)
    final.crop(tuple(round(v*scale) for v in (x,y,x+w,y+h))).save(review/'legend.jpg',quality=96)
    for zone,box in data['review_zones'].items():
        crop=final.crop(tuple(round(v*scale) for v in box));crop.thumbnail((2100,1700));crop.save(review/f'{zone}.jpg',quality=96)
    fields=['Repère / source','Matériel','Désignation','Qté','Portée','Modèle','Prescription / réserve','Parent','X source px','Y source px']
    with (ROOT/f'S-0844-{sheet}-{data["csv_type"]}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(fields)
        for i,m in enumerate(data['markers'],1):
            writer.writerow([f'{sheet}-{i:03d}',m['family'],m.get('description',m['family']),1,m.get('scope',data['scope']),m.get('model','MODÈLE NON PRÉCISÉ'),m.get('reserve',''),m.get('parent',''),round(m['x']*scale,1),round(m['y']*scale,1)])
    print(sheet,len(data['markers']),dict(counts),flush=True)
    return destination

if __name__=='__main__':
    render(json.loads(Path(sys.argv[1]).read_text()))
