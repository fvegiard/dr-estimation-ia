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
        rec['id'] = f'{key}-{i:04d}'
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
        text(x+14, y-10, f'{family} : {count}', 14, color)
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

if __name__ == '__main__':
    render(sys.argv[1])
