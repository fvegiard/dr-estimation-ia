"""Render verified, manually anchored takeoff data onto the original raster."""
import csv
import json
import os
import sys
import textwrap
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from prepare_images import PAGES

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent
if ROOT.name == 'methode':
    ROOT = ROOT.parent
FONT = os.environ.get('S0922_FONT', 'arial.ttf' if sys.platform == 'win32' else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
COLORS = ['#2C78BD','#AA59AD','#489C60','#D14465','#18A6A2','#AB864B','#7C77C4','#45909F','#B36344','#597232','#AD4789','#4A71A8']

def render(sheet):
    data_path = ROOT/'data'/f'{sheet}.json'
    if data_path.exists():
        data = json.loads(data_path.read_text(encoding='utf-8'))
    else:
        from sheet_data import SHEETS
        data = SHEETS[sheet]
    im = Image.open(ROOT/'sources'/PAGES[sheet]).convert('RGB')
    scale = im.width/1800
    overlay = Image.new('RGBA',im.size)
    draw = ImageDraw.Draw(overlay)
    def text(x,y,value,size=9,color='#222222'):
        draw.text((round(x*scale),round(y*scale)),value,font=ImageFont.truetype(FONT,round(size*scale)),fill=color)
    families = data.get('families',{})
    colors = {key:COLORS[i%len(COLORS)] for i,key in enumerate(families)}
    markers = data.get('markers',[])
    assert len({m['id'] for m in markers})==len(markers)
    assert len({(m['x'],m['y']) for m in markers})==len(markers)
    for m in markers:
        x,y=m['x'],m['y'];r=m.get('radius',3.0);color=colors[m['family']]
        draw.ellipse(tuple(round(v*scale) for v in (x-r,y-r,x+r,y+r)),fill=color+'40',outline=color,width=max(2,round(.55*scale)))
        if m.get('reserve'):text(x+4,y-6,'*',7,color)
    x,y,w,h=data['legend_box']
    draw.rectangle(tuple(round(v*scale) for v in (x,y,x+w,y+h)),fill='white',outline='#999999',width=round(.5*scale))
    text(x+12,y+10,f'RELEVÉ {sheet} — MATÉRIEL',13)
    text(x+12,y+32,data['title'],9)
    reserves=sum(bool(m.get('reserve')) for m in markers)
    text(x+12,y+51,f'{len(markers)} pastilles / {len(set(m["family"] for m in markers))} familles / RES {reserves}',9)
    yy=y+74
    counts=Counter(m['family'] for m in markers)
    for key,description in families.items():
        if not counts[key]:continue
        color=colors[key]
        draw.ellipse(tuple(round(v*scale) for v in (x+12,yy+2,x+18,yy+8)),fill=color+'50',outline=color,width=round(.55*scale))
        for line in textwrap.wrap(f'{key}  {description} : {counts[key]}',width=int((w-40)/4.8)):
            text(x+25,yy,line,8.5);yy+=14
    yy+=8
    for note in data['notes']:
        for line in textwrap.wrap(note,width=int((w-28)/4.4)):
            text(x+12,yy,line,8);yy+=12
        yy+=6
    assert yy<y+h,(sheet,yy,y+h)
    result=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    dest=ROOT/f'S-0922-{sheet}-releve.jpg';result.save(dest,quality=96,subsampling=0)
    result = Image.open(dest).convert('RGB')
    folder=ROOT/'inspection'/sheet;folder.mkdir(parents=True,exist_ok=True)
    result.crop(tuple(round(v*scale) for v in (x,y,x+w,y+h))).resize((round(w*2),round(h*2))).save(folder/'final-legend.jpg',quality=96)
    overview=result.copy();overview.thumbnail((1800,1500));overview.save(folder/'final-overview.jpg',quality=96)
    for name,box in data.get('verify_zones',{}).items():
        result.crop(tuple(round(v*scale) for v in box)).resize((round((box[2]-box[0])*3),round((box[3]-box[1])*3))).save(folder/f'final-{name}.jpg',quality=96)
    if markers:
        with (ROOT/f'S-0922-{sheet}-{data.get("csv_type","equipment")}.csv').open('w',encoding='utf-8-sig',newline='') as stream:
            fields=['Repère / source','Matériel','Désignation','Qté','Portée','Modèle','Prescription / réserve','Parent','X source px','Y source px']
            writer=csv.writer(stream);writer.writerow(fields)
            for m in markers:
                writer.writerow([m['id'],m['family'],families[m['family']],1,m.get('scope','INSTALLER'),m.get('model','MODÈLE NON PRÉCISÉ'),m.get('reserve',''),m.get('parent',sheet),round(m['x']*scale,2),round(m['y']*scale,2)])
    print(sheet, len(markers),dict(counts),dest.stat().st_size)

if __name__=='__main__':render(sys.argv[1])
