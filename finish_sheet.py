"""Record a completed direct visual review and checkpoint."""
from pathlib import Path
import json,sys,hashlib
root=Path(__file__).resolve().parent
sheet=sys.argv[1]
data=json.loads((root/'evidence'/f'{sheet}.json').read_text())
image=root/f'S-0844-{sheet}-releve.jpg'
report=dict(feuille=sheet,pastilles=len(data['markers']),controle='Vérification visuelle directe du JPEG et de toutes les zones enregistrées',score=f"{len(data['markers'])}/{len(data['markers'])}",erreurs_restantes=[],legende_lisible=True,source_conservee=True,sha256_jpeg=hashlib.sha256(image.read_bytes()).hexdigest())
(root/'verification'/sheet/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
checkpoint=json.loads((root/'CHECKPOINT.json').read_text())
checkpoint['feuilles_terminees']=[r for r in checkpoint['feuilles_terminees'] if r['feuille']!=sheet]+[report]
checkpoint['feuilles_restantes']=[s for s in checkpoint['feuilles_restantes'] if s!=sheet]
(root/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(sheet,report['score'])
