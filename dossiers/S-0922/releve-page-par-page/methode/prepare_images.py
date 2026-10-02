"""Prepare source overviews and coordinate-based inspection crops."""
import json
import sys
from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent
PAGES = {
    'E-1': '23-357-E-CO-CH-E1 (1) - 1.png',
    'E-2': '23-357-E-CO-CH-E1 (1) - 2 (1).png',
    'E-3': '23-357-E-CO-CH-E1 (1) - 3.png',
    'E-4': '23-357-E-CH-E2.png',
    'E-5': '23-357-E-PE-2 - 5.png',
}

def crop(page, name, box, scale=2):
    source = Image.open(ROOT / 'sources' / PAGES.get(page, page)).convert('RGB')
    factor = source.width / 1800
    result = source.crop(tuple(round(v*factor) for v in box))
    result = result.resize((round((box[2]-box[0])*scale), round((box[3]-box[1])*scale)))
    dest = ROOT / 'inspection' / (name + '.jpg')
    result.save(dest, quality=96)
    print(dest)

if __name__ == '__main__':
    crop(sys.argv[1], sys.argv[2], [float(v) for v in sys.argv[3:7]], float(sys.argv[7]) if len(sys.argv)>7 else 2)
