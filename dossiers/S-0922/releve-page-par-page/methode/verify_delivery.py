"""Verify delivery hashes, image dimensions, source-coordinate records and CSV parity."""
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS=None
root=Path(sys.argv[1]).resolve()
manifest=json.loads((root/'manifest.json').read_text())
for record in manifest:
    path=root/record['file']
    assert path.stat().st_size==record['bytes'],path
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],path
    assert path.suffix in {'.jpg','.csv','.xlsx','.txt','.json','.py'},path
    assert not any(part in {'sources','inspection','__pycache__'} for part in path.relative_to(root).parts),path
spec=importlib.util.spec_from_file_location('sheet_data',root/'methode/sheet_data.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for sheet,data in module.SHEETS.items():
    markers=data.get('markers',[])
    jpg=root/f'S-0922-{sheet}-releve.jpg'
    with Image.open(jpg) as im:
        assert im.width>=8000 and im.height>=6000
        width,height=im.size
    if markers:
        records=list(csv.DictReader((root/f'S-0922-{sheet}-equipment.csv').open(encoding='utf-8-sig')))
        assert len(records)==len(markers)
        assert len({r['Repère / source'] for r in records})==len(records)
        assert sum(int(r['Qté']) for r in records)==len(markers)
        for r in records:assert 0<=float(r['X source px'])<=width and 0<=float(r['Y source px'])<=height
    print(f'{sheet}: {len(markers)} pastilles; {sum(bool(m.get("reserve")) for m in markers)} réserves; JPEG {width}x{height}; CSV concordant')
breakers=root/'S-0922-breakers-detailed.csv'
if breakers.exists():
    rows=list(csv.DictReader(breakers.open(encoding='utf-8-sig')))
    assert Counter(r['panel'] for r in rows)=={'P1':49,'P2':42}
    assert sum(r['status']=='NEUF (*)' for r in rows)==8
    assert len([r for r in rows if r['reserve']])==3
    print('Disjoncteurs : 91 lignes; P1 49 / P2 42; 8 neufs; 3 lectures en réserve.')
print(f'Manifest : {len(manifest)}/{len(manifest)} tailles et SHA-256 conformes.')
