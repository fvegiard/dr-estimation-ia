"""Crop source coordinates expressed on a 2000-pixel-wide overview."""
import json, sys
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = 200_000_000
root = Path(__file__).resolve().parent
idx = {r['id']:r for r in json.loads((root/'inspection/index.json').read_text())}
key, label = sys.argv[1:3]
row = idx[key]
im = Image.open(root/row['file']).convert('RGB')
scale = im.width/2000
box = tuple(round(float(v)*scale) for v in sys.argv[3:7])
crop = im.crop(box)
crop.thumbnail((2200, 1800))
dest = root/'inspection'/f'{key}-{label}.png'
crop.save(dest)
print(dest, box, crop.size)
