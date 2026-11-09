"""Inspect a source rectangle in a 1920 by 1280 coordinate system."""
import sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
page = int(sys.argv[1])
box = tuple(float(v) for v in sys.argv[2:6])
label = sys.argv[6]
source = ROOT / 'sources' / f'STAM23A - E - Pour construction - 2024-10-08 - {page}.png'
im = Image.open(source).convert('RGB')
im = im.crop(tuple(round(v * im.width / 1920) for v in box))
im.thumbnail((2400, 2000))
im.save(ROOT / 'audit' / f'{label}.jpg', quality=97)
