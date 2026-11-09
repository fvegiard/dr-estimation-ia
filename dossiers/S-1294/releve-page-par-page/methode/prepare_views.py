"""Create inspection overviews and title-block crops from unmodified sources."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit' / 'source-views'
OUT.mkdir(exist_ok=True)
paths = sorted((ROOT / 'sources').glob('STAM*.png'), key=lambda p: int(p.stem.rsplit(' - ', 1)[1]))
for index, path in enumerate(paths, 1):
    im = Image.open(path).convert('RGB')
    im.crop((9400, 5800, 10799, 7199)).save(OUT / f'p{index:02d}-title.jpg', quality=95)
    im.thumbnail((2160, 1440))
    im.save(OUT / f'p{index:02d}-overview.jpg', quality=95)
    print(index, flush=True)
for start in range(0, len(paths), 6):
    page = Image.new('RGB', (2100, 1400), 'white')
    draw = ImageDraw.Draw(page)
    for j in range(start, min(start + 6, len(paths))):
        im = Image.open(OUT / f'p{j+1:02d}-title.jpg')
        im.thumbnail((700, 650))
        x, y = ((j-start) % 3)*700, ((j-start)//3)*700
        page.paste(im, (x, y+30))
        draw.text((x+10, y+10), f'PAGE {j+1}', fill='black')
    page.save(OUT / f'titles-{start+1:02d}.jpg', quality=95)
