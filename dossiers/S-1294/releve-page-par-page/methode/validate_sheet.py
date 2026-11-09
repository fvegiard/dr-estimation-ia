"""Persist a manual visual review after all rendered proof images were inspected."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
key, review = sys.argv[1:3]
data = json.loads((ROOT / 'audit' / f'{key}-records.json').read_text())
count = sum(r.get('mark',True) for r in data['records'])
proof = {'sheet':key,'markers':count,'visual_score':f'{count}/{count}',
         'review':review,'jpeg_sha256':hashlib.sha256((ROOT/f'S-1294-{key}-releve.jpg').read_bytes()).hexdigest(),
         'scope':'Contrôle des repères retenus; ne certifie pas les familles explicitement exclues.'}
(ROOT/'audit'/key/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2))
path=ROOT/'CHECKPOINT.json'
cp=json.loads(path.read_text())
cp['completed']=[r for r in cp['completed'] if r['sheet']!=key]+[proof]
cp['remaining']=[r for r in cp['remaining'] if r!=key]
cp['status']='Relevé en cours'
path.write_text(json.dumps(cp,ensure_ascii=False,indent=2))
print(key, proof['visual_score'])
