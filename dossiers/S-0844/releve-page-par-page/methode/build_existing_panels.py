"""Transcribe existing panel breakers; keep them separate from new purchases."""
from pathlib import Path
import json
from render_sheet import render
root=Path(__file__).resolve().parent
catalog=json.loads((root/'sheet-catalog.json').read_text())
markers=[]
def add(panel,c,amp,poles,x,y):
    circuits=list(range(c,c+2*poles,2))
    markers.append(dict(family=f'Existant {amp} A / {poles}P',description=f'{panel} — circuits '+','.join(map(str,circuits)),parent=panel,circuits=circuits,amps=amp,poles=poles,x=x,y=y,radius=2.7,scope='CONSERVER / RÉFÉRENCE EXISTANTE — aucun achat déduit',reserve=''))
s1={1:(20,1),2:(20,1),5:(20,1),7:(15,1),8:(15,1),9:(15,1),10:(40,2),11:(20,1),16:(20,1),17:(15,1),18:(20,1),19:(15,1),20:(20,1),21:(15,1),23:(15,1),24:(20,2),25:(20,1),27:(15,1),32:(15,1),34:(15,1),35:(15,1),40:(20,2),43:(15,1),45:(15,1),47:(15,1),49:(15,1)}
for c,(amp,p) in s1.items():add('S1',c,amp,p,197.6 if c%2 else 226.2,110.5+((c-1)//2)*10.63)
for c in range(1,22):
    amp=40 if c==20 else 15 if c in {1,6,8,12,14} else 20
    add('UE-1',c,amp,2 if c==20 else 1,486.7 if c%2 else 516.5,124.65+((c-1)//2)*11.18)
common={1:(20,1),2:(20,1),3:(20,1),4:(15,2),5:(20,1),7:(25,2),8:(50,3),11:(15,1),13:(50,3),14:(50,3),19:(50,3),20:(15,1),22:(20,2),25:(15,1),26:(15,2),27:(20,2),30:(20,1),31:(20,1)}
for panel,xs in [('C1-1',(774.8,805.0)),('C3-1',(1063.3,1093.3)),('C4-1',(1351.8,1381.5))]:
    entries=dict(common)
    if panel=='C1-1':
        del entries[1]
        entries.update({5:(15,1),8:(20,3),13:(80,3),32:(30,2),36:(15,1),38:(15,1)})
    if panel=='C4-1':entries[2]=(15,1)
    for c,(amp,p) in sorted(entries.items()):add(panel,c,amp,p,xs[0 if c%2 else 1],124.65+((c-1)//2)*11.18)
data=dict(sheet='EX-E-PE01',source=next(r['file'] for r in catalog if r['id']=='022'),markers=markers,csv_type='breakers',scope='Panneaux existants — référence du 31 octobre 2023',legend_box=[150,600,1500,440],notes=[
    'Un appareil multipolaire = un repère au premier pôle. Espaces sans calibre exclus.',
    'S1 : 26; UE-1 : 21; C1-1 : 20; C3-1 : 18; C4-1 : 18 appareils existants.',
    'Aucun achat déduit de cette feuille. Modifications à recouper aux plans modifiés.',
    '* Les barres omnibus indiquées 0 A sur quatre tableaux ne constituent pas un calibre utilisable.',
    'Marques, séries, protections et pouvoirs de coupure non précisés. Vérification sur place requise.'
],review_zones={'S1':[80,65,335,530],'UE-1':[365,65,625,435],'C1-1':[660,65,920,435],'C3-1':[945,65,1205,435],'C4-1':[1230,65,1490,435]})
(root/'evidence/EX-E-PE01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
render(data)
