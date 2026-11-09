"""Transcribe breaker symbols from the visually inspected panel schedules."""
from pathlib import Path
import json,csv
from collections import Counter
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog=json.loads((ROOT/'sheet-catalog.json').read_text())
source=next(r['file'] for r in catalog if r['id']=='047')
markers=[]
def breaker(panel,circuit,amps,poles,x,y,reserve='',description=''):
    markers.append(dict(family=f'Disjoncteur {amps} A / {poles}P',description=description or f'{panel} — circuits '+','.join(map(str,circuit)),parent=panel,circuits=circuit,amps=amps,poles=poles,x=x,y=y,radius=2.7,reserve=reserve,scope='CÉDULE NOUVEAU — non additionnable aux plans'))
for c in range(1,54):
    amp=20 if c in {1,2,3,4,16,18,19,22,47,53} else 15
    breaker('C1-2',[c],amp,1,222.0 if c%2 else 250.6,137.7+((c-1)//2)*10.62)
for panel,xs,twenties,excluded in [
    ('C3-2',[590.2,614.4,787.0,811.5],{1,2,3,4,5,6,8,27,44,45,46,47,48,53,55,58},{77,80,82,84}),
    ('C4-2',[1126.2,1150.5,1323.0,1347.4],set(range(1,9))|{45,46,47,48,53,55,58,68,70,74},{77,78,80,82,84})]:
    for c in range(1,85):
        if c in excluded:continue
        column=0 if c<=42 else 2
        row=((c-1)%42)//2
        amp=25 if c==75 else 20 if c in twenties else 15
        breaker(panel,[75,77] if c==75 else [c],amp,2 if c==75 else 1,xs[column+(0 if c%2 else 1)],137.5+row*8.96)
for c,amp in [(1,90),(2,130),(7,20),(8,15),(13,30),(14,25),(19,15),(21,15)]:
    poles=3 if c<19 else 1
    note='* Calibre 130 A conservé littéralement; série et disponibilité à confirmer.' if c==2 else ''
    breaker('C1-3',list(range(c,c+2*poles,2)),amp,poles,222.7 if c%2 else 252.7,729.0+((c-1)//2)*11.13,note)
for c in [1,2,5,6,9,10,13,14,17,21,25,29,33,35,37]:
    poles=2 if c<=29 else 1; amp=30 if c<=21 else 20 if c<=33 else 15
    breaker('CA1-1',list(range(c,c+2*poles,2)),amp,poles,602.0 if c%2 else 631.7,729.0+((c-1)//2)*11.13)
data=dict(sheet='EX-M-PE01',source=source,markers=markers,csv_type='breakers',scope='Cédule du 24 avril 2024 — révision 06',legend_box=[790,660,945,445],notes=[
    'Un appareil multipolaire = une pastille sur son premier pôle; pôles liés exclus du total.',
    'LIBRE avec calibre : disjoncteur compté. Tiret sans calibre : espace exclu.',
    'C1-2 : 53; C3-2 : 80; C4-2 : 79; C1-3 : 8; CA1-1 : 15 appareils.',
    '* 130 A C1-3 conservé tel qu’indiqué. Aucun calibre choisi arbitrairement.',
    'Marque, série, protections, pouvoir de coupure et principaux non déterminés.',
    'La cédule ne donne pas une quantité supplémentaire de prises ou de luminaires.'
],review_zones={'C1-2':[85,75,365,560],'C3-2':[470,80,920,365],'C4-2':[1010,80,1460,365],'C1-3-CA1-1':[90,660,750,1050]})
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/EX-M-PE01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
render(data)
