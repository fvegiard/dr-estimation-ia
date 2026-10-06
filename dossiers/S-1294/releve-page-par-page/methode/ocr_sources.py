"""Produce searchable reading aids; OCR is not a quantity proof."""
import subprocess
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit' / 'ocr'
OUT.mkdir(exist_ok=True)
for source in sorted((ROOT / 'sources').glob('*.png')):
    target = OUT / source.stem
    if target.with_suffix('.txt').exists():
        continue
    im = Image.open(source)
    im.thumbnail((6500, 6500))
    scratch = OUT / 'ocr-input.png'
    im.save(scratch)
    subprocess.run(['tesseract', str(scratch), str(target), '-l', 'eng', '--psm', '3'], check=True, capture_output=True)
    print(source.name, flush=True)
(OUT / 'ocr-input.png').unlink(missing_ok=True)
