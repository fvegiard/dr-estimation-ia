"""Build source overviews and title crops without changing source files."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

root = Path(__file__).resolve().parent
out = root / 'inspection'
out.mkdir(exist_ok=True)
files = sorted((root / 'sources').glob('*.png'))
index = []
for n, path in enumerate(files, 1):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    key = f'{n:03d}'
    title = im.crop((int(w*.88), int(h*.79), w, h))
    title.thumbnail((700, 1000))
    title.save(out / f'{key}-title.png')
    preview = im.copy()
    preview.thumbnail((2000, 1500))
    preview.save(out / f'{key}-overview.jpg', quality=94)
    index.append(dict(id=key, file=str(path.relative_to(root)), width=w, height=h))
(out / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
for start in range(0, len(index), 12):
    canvas = Image.new('RGB', (1600, 1680), 'white')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    for i, row in enumerate(index[start:start+12]):
        x, y = (i % 4)*400, (i // 4)*560
        crop = Image.open(out / f"{row['id']}-title.png")
        crop.thumbnail((390, 490))
        canvas.paste(crop, (x, y+60))
        draw.text((x+5, y+5), row['id']+' '+Path(row['file']).name[:36], fill='black', font=font)
    canvas.save(out / f'titles-{start//12+1}.jpg', quality=95)
print(f'{len(index)} sources prepared')
