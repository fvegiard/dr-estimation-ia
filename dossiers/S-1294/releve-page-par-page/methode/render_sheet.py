"""Render auditable source-preserving takeoffs from visually verified records."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
COLORS = ['#3C82BA', '#55A25E', '#A852A2', '#A37225', '#D45B6B', '#2B9B95', '#8B70AA', '#AC7860']

def render(key):
    data = json.loads((ROOT / 'audit' / f'{key}-records.json').read_text())
    page, records = data['page'], data['records']
    source = ROOT / 'sources' / f'STAM23A - E - Pour construction - 2024-10-08 - {page}.png'
    base = Image.open(source).convert('RGB')
    scale = base.width / 1920
    counts = Counter(r['family'] for r in records if r.get('mark', True))
    palette = {family: COLORS[i % len(COLORS)] for i, family in enumerate(counts)}
    legend_height = round((140 + 27 * ((len(counts)+2)//3) + 25*len(data['notes'])) * scale)
    canvas = Image.new('RGB', (base.width, base.height + legend_height), 'white')
    canvas.paste(base, (0, 0))
    overlay = Image.new('RGBA', canvas.size)
    draw = ImageDraw.Draw(overlay)
    for i, rec in enumerate(records, 1):
        rec.setdefault('id', f'{key}-{i:04d}')
        if not rec.get('mark', True):
            continue
        x, y = rec['x']*scale, rec['y']*scale
        radius = rec.get('radius', 4.2) * scale
        color = palette[rec['family']]
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color+'45', outline=color, width=max(2, round(.7*scale)))
        if rec.get('reserve'):
            star_size = 3.5 if rec.get('radius',4.2)<3 else 10
            draw.text((x+radius, y-radius*2), '*', font=ImageFont.truetype(FONT, round(star_size*scale)), fill=color)
    def text(x, y, value, size=13, color='#222222'):
        draw.text((round(x*scale), base.height+round(y*scale)), value, font=ImageFont.truetype(FONT, round(size*scale)), fill=color)
    draw.rectangle((25*scale, base.height+15*scale, base.width-25*scale, canvas.height-15*scale), outline='#909090', width=3)
    text(45, 27, f'RELEVÉ {key} — {data["title"]}', 21)
    reserved = sum(bool(r.get('reserve')) for r in records)
    text(45, 61, f'{sum(counts.values())} pastilles / {len(counts)} familles / RES {reserved} — source : page {page} — {data["scope"]}', 13)
    for i, (family, count) in enumerate(counts.items()):
        x, y = 48+(i%3)*620, 99+(i//3)*27
        color = palette[family]
        draw.ellipse(((x-4.2)*scale, base.height+(y-4.2)*scale, (x+4.2)*scale, base.height+(y+4.2)*scale), fill=color+'45', outline=color, width=3)
        if data.get('legend_by_parent'):
            parents=sorted(set(r.get('parent','') for r in records))
            values=' | '.join(f"{p.removeprefix('Logement type ')} : {sum(r.get('quantity',1) for r in records if r['family']==family and r.get('parent')==p)}" for p in parents)
            text(x+14,y-10,f'{family} — {values}',12,color)
        else:
            quantity=sum(r.get('quantity',1) for r in records if r['family']==family and r.get('mark',True))
            suffix=f'{quantity} ({count} repère)' if quantity!=count else str(count)
            text(x+14, y-10, f'{family} : {suffix}', 14, color)
    y = 114+27*((len(counts)+2)//3)
    for note in data['notes']:
        text(45, y, note, 12)
        y += 25
    final = Image.alpha_composite(canvas.convert('RGBA'), overlay).convert('RGB')
    output = ROOT / f'S-1294-{key}-releve.jpg'
    final.save(output, quality=96, subsampling=0)
    final = Image.open(output).convert('RGB')
    proof = ROOT / 'audit' / key
    proof.mkdir(exist_ok=True)
    overview = final.copy()
    overview.thumbnail((1920, 1600))
    overview.save(proof / 'overview.jpg', quality=95)
    legend = final.crop((0, base.height, final.width, final.height))
    legend.thumbnail((2200, 1400))
    legend.save(proof / 'legend.jpg', quality=96)
    marked = [r for r in records if r.get('mark', True)]
    for start in range(0, len(marked), 30):
        board = Image.new('RGB', (1800, 1350), 'white')
        d = ImageDraw.Draw(board)
        for j, rec in enumerate(marked[start:start+30]):
            x, y = round(rec['x']*scale), round(rec['y']*scale)
            tile = final.crop((x-150, y-110, x+150, y+110))
            col, row = j%6, j//6
            board.paste(tile, (col*300, row*270+45))
            d.text((col*300+4, row*270+3), rec['id'], fill='black', font=ImageFont.truetype(FONT, 16))
            d.text((col*300+4, row*270+23), rec['family'][:28], fill='black', font=ImageFont.truetype(FONT, 13))
        board.save(proof / f'marks-{start+1:04d}.jpg', quality=97)
    with (ROOT / f'S-1294-{key}-{data["type"]}.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Repère / source','Matériel','Désignation','Qté','Portée','Modèle','Prescription / réserve','Parent','X pixels source','Y pixels source','Pastille','Circuits','Ampères','Pôles','Protection source'])
        for rec in records:
            writer.writerow([rec['id'],rec['family'],rec.get('label',''),rec.get('quantity',1),rec.get('scope',data['scope']),rec.get('model','MODELE NON PRECISE'),rec.get('reserve',''),rec.get('parent',''),round(rec.get('x',0)*scale,2),round(rec.get('y',0)*scale,2),int(rec.get('mark',True)),rec.get('circuits',''),rec.get('ampere',''),rec.get('poles',''),rec.get('protection','')])
    (ROOT / 'audit' / f'{key}-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2), encoding='utf-8')
    print(key, 'pastilles:', sum(counts.values()), 'RES:', reserved)


def render_pilot(key, layout_path, output_dir):
    """Pilote Granby dans la feuille; aucune réécriture du relevé ou du JPEG livré.

    Les rectangles viennent d'une inspection de la source, par ID. La zone de
    légende doit être entièrement blanche dans le raster original. Les valeurs
    de la matrice viennent exclusivement des enregistrements existants.
    """
    if key == 'E201':
        raise ValueError('E201 réservée.')
    import hashlib
    data = json.loads((ROOT / 'audit' / f'{key}-records.json').read_text('utf-8'))
    layout = json.loads(Path(layout_path).read_text('utf-8'))
    if layout['sheet'] != key or layout['source_page'] != data['page']:
        raise ValueError('Mise en page associée à une autre feuille/source.')
    source = ROOT / 'sources' / f'STAM23A - E - Pour construction - 2024-10-08 - {data["page"]}.png'
    if hashlib.sha256(source.read_bytes()).hexdigest() != layout['source_sha256']:
        raise ValueError('Source modifiée depuis l’inspection de la zone libre.')
    output_dir = Path(output_dir)
    if output_dir.resolve() == ROOT.resolve():
        raise ValueError('Le pilote doit conserver une sortie distincte.')
    output_dir.mkdir(parents=True, exist_ok=True)
    base = Image.open(source).convert('RGB')
    scale = base.width / 1920
    records = [r for r in data['records'] if r.get('mark', True)]
    families = list(dict.fromkeys(r['family'] for r in records))
    palette = {family: COLORS[i % len(COLORS)] for i, family in enumerate(families)}
    box = tuple(round(v*scale) for v in layout['legend_box'])
    if not (0 <= box[0] < box[2] <= base.width and 0 <= box[1] < box[3] <= base.height):
        raise ValueError('Légende extérieure à la feuille.')
    if base.crop(box).getextrema() != ((255,255),)*3:
        raise ValueError('La zone de légende contient des pixels source : placement refusé.')
    overlay = Image.new('RGBA', base.size)
    draw = ImageDraw.Draw(overlay)
    frames = layout.get('frames', {})
    if not set(frames).issubset({r['id'] for r in records}):
        raise ValueError('ID de cadre absent du relevé.')
    leaders = layout.get('leaders', {})
    if not set(leaders).issubset({r['id'] for r in records}) or set(leaders) & set(frames):
        raise ValueError('ID de liaison absent ou également encadré.')
    for rec in records:
        color = palette[rec['family']]
        if rec['id'] in frames:
            bounds = tuple(round(v*scale) for v in frames[rec['id']])
            draw.rectangle(bounds, outline=color, width=max(2, round(.7*scale)))
        else:
            x, y, radius = rec['x']*scale, rec['y']*scale, rec.get('radius',4.2)*scale
            if rec['id'] in leaders:
                # Positions de présentation seulement; x/y métier restent intacts.
                placement = leaders[rec['id']]
                x, y = (v*scale for v in placement['marker'])
                ax, ay = (v*scale for v in placement['anchor'])
                safe_box = (int(min(x-radius,ax-2*scale))-2, int(min(y-radius,ay))-2,
                            int(max(x+radius,ax+2*scale))+3, int(max(y+radius,ay))+3)
                if not (0 <= safe_box[0] < safe_box[2] <= base.width and
                        0 <= safe_box[1] < safe_box[3] <= base.height):
                    raise ValueError('Liaison hors de la source.')
                if base.crop(safe_box).getextrema() != ((255,255),)*3:
                    raise ValueError(f'Liaison sur des pixels source : {rec["id"]}')
                draw.line((x,y+radius,ax,ay),fill=color,width=max(2,round(.7*scale)))
                draw.polygon([(ax,ay),(ax-1.4*scale,ay-2.5*scale),(ax+1.4*scale,ay-2.5*scale)],fill=color)
            draw.ellipse((x-radius,y-radius,x+radius,y+radius), fill=color+'45', outline=color, width=max(2,round(.7*scale)))
    x0,y0,x1,y1 = layout['legend_box']
    draw.rectangle(box,outline='#909090',width=3)
    font_path = FONT if Path(FONT).is_file() else 'C:/Windows/Fonts/arial.ttf'
    text_boxes=[]
    def label(x,y,value,size=11,anchor='la'):
        font=ImageFont.truetype(font_path,round(size*scale))
        xy=(round(x*scale),round(y*scale))
        bounds=draw.textbbox(xy,value,font=font,anchor=anchor)
        if bounds[0]<box[0] or bounds[1]<box[1] or bounds[2]>box[2] or bounds[3]>box[3]:
            raise ValueError(f'Texte hors légende : {value}')
        text_boxes.append(bounds)
        draw.text(xy,value,font=font,anchor=anchor,fill='#222222')
    label(x0+18,y0+13,f'RELEVÉ {key} — LOGEMENTS TYPES A / B — QUANTITÉS PAR DESSIN',17)
    label(x0+18,y0+42,f'{len(records)} repères / {len(families)} familles. Aucune multiplication par le nombre de logements. Indices 01–31 : légende uniquement.',11)
    split=(len(families)+1)//2
    for i,family in enumerate(families):
        col,row=divmod(i,split)
        x,y=x0+23+col*(x1-x0)/2,y0+74+row*15
        color=palette[family]
        if family.startswith('Plinthe'):
            draw.rectangle(((x-5)*scale,(y+4)*scale,(x+5)*scale,(y+8)*scale),outline=color,width=max(2,round(.7*scale)))
        else:
            radius=3*scale;cx,cy=x*scale,(y+6)*scale
            draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=color+'45',outline=color,width=max(2,round(.7*scale)))
        label(x+14,y,f'{i+1:02d}   {family}',11)
    matrix_y=y0+326
    label(x0+18,matrix_y,'TYPE',11)
    col_width=(x1-x0-150)/len(families)
    parents=sorted({r.get('parent','') for r in records})
    matrix=[]
    for i,family in enumerate(families):
        x=x0+135+(i+1)*col_width
        label(x,matrix_y,f'{i+1:02d}',11,'ra')
    draw.line(((x0+18)*scale,(matrix_y+18)*scale,(x1-18)*scale,(matrix_y+18)*scale),fill='#999999',width=2)
    for j,parent in enumerate(parents):
        y=matrix_y+24+j*20
        label(x0+18,y,parent.removeprefix('Logement type '),11)
        row=[]
        for i,family in enumerate(families):
            qty=sum(r.get('quantity',1) for r in records if r['family']==family and r.get('parent','')==parent)
            row.append(qty)
            label(x0+135+(i+1)*col_width,y,str(qty),11,'ra')
        matrix.append({'parent':parent,'quantities':row})
    notes_y=matrix_y+70
    for i,note in enumerate(data['notes']):
        label(x0+18,notes_y+i*13,note,9.5)
    final=Image.alpha_composite(base.convert('RGBA'),overlay).convert('RGB')
    path=output_dir/f'S-1294-{key}-pilote.jpg'
    final.save(path,quality=96,subsampling=0)
    final.crop(box).save(output_dir/'legende-pilote.png')
    overview=final.copy();overview.thumbnail((2200,1600));overview.save(output_dir/'ensemble-pilote.jpg',quality=96)
    report={'sheet':key,'source_page':data['page'],'source_size':list(base.size),'output_size':list(final.size),
        'source_sha256':layout['source_sha256'],'jpeg_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'legend_box_source_pixels':box,'legend_source_region':'entièrement blanche (255,255,255)',
        'markers':len(records),'circle_count':len(records)-len(frames),'frame_ids':list(frames),
        'leader_annotations':leaders,
        'families':families,'matrix':matrix,'text_boxes':text_boxes,
        'status':'Pilote pour revue visuelle; aucune acceptation globale, aucun taux métier.'}
    (output_dir/'rendu-pilote.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
    return path

if __name__ == '__main__':
    render(sys.argv[1])
