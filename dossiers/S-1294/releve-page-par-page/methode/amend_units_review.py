"""Corrections établies D1-D4 sur les checkpoints immuables; pas de changement de quantité/coordonnées."""
import json,zipfile,sys,re,copy,csv
from pathlib import Path
D=Path(__file__).resolve().parents[1];W=D.parents[3];sys.path.insert(0,str(Path(__file__).parent))
import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'
sources={'E203':'S-1294-E203-checkpoint.zip','E204':'S-1294-E204-checkpoint-v2.zip','E205':'S-1294-E205-checkpoint.zip','E206':'S-1294-E206-checkpoint.zip'}
simple={'E203':[127,128,141,143,147,148],'E204':[132,135,148,149],'E205':[102,109,119,120,121],'E206':[104,110,120,121,122]}
indices={'E203':{134:3,139:4,145:4,150:3},'E204':{131:4,134:4,141:3,143:4,151:3},'E205':{101:3,103:4,110:3,111:4,117:4},'E206':{103:3,105:4,106:3,111:3,114:4,117:4}}
commands={'E203':{130:'c',131:'b',132:'a',134:'a',137:'b',138:'d',139:'a',142:'d',144:'f',145:'a',146:'e',150:'a',168:'e',169:'c',170:'f'},'E204':{131:'a',133:'d',134:'a',137:'c',138:'b',139:'e',140:'f',143:'a',145:'b',146:'e',147:'d',151:'a',168:'c',169:'f'},'E205':{101:'a',103:'a',104:'d',105:'d',106:'e',107:'e',108:'b',110:'a',111:'a',113:'b',115:'b',117:'a',118:'g',134:'c',135:'c',136:'f'},'E206':{103:'a',105:'a',106:'d',107:'d',108:'f',109:'e',111:'a',112:'c',113:'b',114:'a',115:'g',117:'a',118:'b',135:'e',136:'f',137:'c'}}
ddft={'E203':[82,85,95,100],'E204':[68,77,93,101],'E205':[58,64,168,169],'E206':[53,54,56,65]}
models={'Spot logement':'JUNO JPDZ4 DC 1000LM CWH — E108','Plafonnier':'ARTIKAPRO 12FLPR-SP3-WHJ-6PK — E108','Suspension repas':'ARTIKA PRO PDT-DEC-BLJ — E108','Luminaire L':'ACUITY OLLWDLEDP140K 120DDB — E108','Relais chauffage':'STELPRO série RE306 — E100','Avertisseur fumée L':'KIDDE P12040CA — E100; CO conditionnel réservé','Thermostat ligne':'STELPRO (modèle non inscrit) / OUELLET série OTH/TH — E100','Convecteur 1000 W':'STELPRO série MIR / OUELLET série ONC — E100'}
deltas=[]
for k in sources:
 with zipfile.ZipFile(W/'checkpoints'/sources[k]) as z:d=json.loads(z.read(f'audit/{k}-records.json'))
 before=copy.deepcopy(d);d['legend_by_parent']=True;d['scope']='VENTILATION PAR DESSIN TYPE — NON MULTIPLIÉE'
 d['notes'][0]='Chaque famille est ventilée par logement type dans la légende. Total des pastilles = ensemble des dessins, pas un logement.'
 d['notes']+=['Références E100/E108 transcrites sans choix d’achat. Calibres/circuits : seulement les valeurs explicitement relevées.', 'Commandes : variante et indices lus sur chaque vignette source; réserve S/T et variantes ambiguës maintenues.']
 for r in d['records']:
  i=int(r['id'].rsplit('-',1)[1]);f=r['family']
  if f=='Interrupteur':
   if k=='E204' and i==170:
    r.update(family='Commande S/T à clarifier',label='S et T superposés; variante de commande réservée')
   else:
    r['family']='Interrupteur simple' if i in simple[k] else 'Gradateur'
    r['label']='Symbole S sans barre terminale' if i in simple[k] else 'Symbole S avec barre terminale — E108'
    if i in indices[k]:r['label']+=f", indice {indices[k][i]}";r['reserve']+=' Indice reproduit sans validation de compatibilité ni sélection de mécanisme.'
    if i in commands[k]:r['label']+=', commande '+commands[k][i]
    r['reserve']=r['reserve'].replace('Type simple/3/4 voies selon indice du dessin; calibre non déduit.','Variante lue selon E108; calibre non inscrit.').replace('Type simple/3/4 voies selon indice du dessin.','Variante lue selon E108; calibre non inscrit.')
  if i in ddft[k]:r['family']='Prise comptoir DDFT 20 A';r['label']+='; au-dessus du comptoir selon traverse du symbole E100'
  f=r['family']
  if f in models:r['model']=models[f]
  if f.startswith('Klaxon stroboscope'):r['model']='MIRCOM FHS-400-RR — E100'
  if f.startswith('Plinthe '):
   r['model']='STELPRO B / OUELLET OFM (logement); STELPRO SPDH / OUELLET OPPM (porte-patio) — E100'
   r['reserve']+=' Série selon variante de plinthe au dessin; alternatives conservées sans choix de marque.'
  if f=='Avertisseur fumée L' and k=='E204':r['reserve']+=' Si CO applicable : E204 prescrit BRK SC9120, E100 SC7010B; divergence non arbitrée.'
  if '20 A' in f and f.startswith('Prise'):r['ampere']=20
  if f=='Prise double 15 A':r['ampere']=15
  if f=='Prise sécheuse':r.update(ampere=30,circuits='11-13',model='Configuration 14-30R — E100')
  if f=='Prise cuisinière':r.update(ampere=50,circuits='1-3',model='Configuration 14-50R — E100')
  m=re.search(r'circuit (\d+(?:-\d+)?)',r.get('label',''),re.I)
  if m:r['circuits']=m.group(1)
  if 'DDFT' in f:r['protection']='DDFT selon symbole E100; ne vaut pas disjoncteur ajouté'
  old=before['records'][i-1]
  for field in sorted(set(old)|set(r)):
   if old.get(field)!=r.get(field):deltas.append([k,r['id'],field,str(old.get(field,'')),str(r.get(field,''))])
 assert [(r['id'],r['x'],r['y'],r['quantity']) for r in before['records']]==[(r['id'],r['x'],r['y'],r['quantity']) for r in d['records']]
 (D/'audit'/f'{k}-records.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8');render_sheet.render(k)
with (D/'S-1294-deltas-revue-E203-E206.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.writer(f);w.writerow(['Feuille','ID','Champ','Avant','Après']);w.writerows(deltas)
print('Delta champs',len(deltas),'; quantités, IDs et coordonnées inchangés.')
