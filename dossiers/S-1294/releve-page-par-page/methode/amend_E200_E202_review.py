"""Deltas localisés du rapport indépendant task-5; sources inspectées, anciens ZIP conservés."""
from pathlib import Path
import json,csv,zipfile,copy,sys,hashlib
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[1];W=D.parents[3]
sys.path.insert(0,str(Path(__file__).parent));import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'
Z={'E200':'S-1294-E200-checkpoint.zip','E202':'S-1294-E202-checkpoint-v2.zip'}
before={}
for k,n in Z.items():
 with zipfile.ZipFile(W/'checkpoints'/n) as z:before[k]=json.loads(z.read(f'audit/{k}-records.json'))
after=copy.deepcopy(before);changes={}
def move(k,i,x,y,radius=None,reason=''):
 r=next(r for r in after[k]['records'] if r['id']==f'{k}-{i:04d}')
 r['x']=x;r['y']=y
 if radius is not None:r['radius']=radius
 changes[r['id']]=reason
move('E202',177,1451.3,953.0,reason='D1 : H réel à gauche du OS3; OS3-0216 inchangé.')
move('E200',410,844.3,254.1,2.5,'D3 : T rond, distinct du MRA-0505 et du T carré-0411.')
move('E200',408,1498.5,934.7,2.5,'D4 : T rond à gauche du luminaire C.')
move('E200',391,1503.7,914.2,2.5,'D5 : groupe interrupteurs à gauche de E; multiplicité réservée.')
move('E200',392,1544.0,914.2,2.5,'D6 : groupe interrupteurs second vestibule; multiplicité réservée.')
move('E200',347,822.5,903.9,2.5,'Retouche rapport : recentrage du Q existant.')
for i,x in [(448,1567.4),(449,1571.7)]:move('E200',i,x,851.2,1.6,'Retouche rapport : deux prises distinctes, centrées; rayons réduits.')
for i,x,y in [(457,476.6,997.4),(461,973.3,997.1),(462,1276.4,997.1),(463,1397.6,934.8)]:move('E200',i,x,y,2.2,'Retouche rapport : recentrage de la prise extérieure existante.')
for i,y in enumerate([849.6,853.5,857.4,861.3,865.1,869.0,874.0],516):move('E200',i,1504.6,y,1.6,'Retouche rapport : module Mx2 distinct, rayon réduit pour séparer les pastilles.')
for i in range(618,624):move('E200',i,[768.6,772.8,777.0][(i-618)%3],896.6 if i<621 else 905.8,1.5,'Retouche rapport : BA ouest distinct, rayon réduit pour séparer les pastilles.')
for i in range(624,630):move('E200',i,[1559.8,1564.1,1568.4][(i-624)%3],975.8 if i<627 else 985.2,1.5,'Retouche rapport : BA est distinct, rayon réduit pour séparer les pastilles.')
removed=next(r for r in after['E202']['records'] if r['id']=='E202-0269')
after['E202']['records'].remove(removed)
after['E202']['notes'].append('Correction D2 : prise E202-0269 retirée (T rond déjà repéré 0285). 18 prises doubles; IDs conservés avec lacune 0269.')
out=W/'evidence/delta-E200-E202';out.mkdir(exist_ok=True)
delta=[]
for k,old in before.items():
 om={r['id']:r for r in old['records']};nm={r['id']:r for r in after[k]['records']}
 for rid,o in om.items():
  if rid not in nm:
   assert rid=='E202-0269'
   delta.append([k,rid,'SUPPRESSION INSTANCE','quantity',1,0,'D2 : aucun symbole prise à cet emplacement; T déjà 0285, prise réelle voisine déjà 0270. Pas de remplacement arbitraire.']);continue
  n=nm[rid]
  assert o['quantity']==n['quantity']
  for f in set(o)|set(n):
   if o.get(f)!=n.get(f):
    assert f in ('x','y','radius'),(rid,f)
    delta.append([k,rid,'RETOUCHE ANCRAGE',f,o.get(f),n.get(f),changes[rid]])
 assert len(nm)==len(after[k]['records']) and set(nm)<=set(om)
 (D/'audit'/f'{k}-records.json').write_text(json.dumps(after[k],ensure_ascii=False,indent=2),'utf-8')
 render_sheet.render(k)
with (D/'S-1294-deltas-revue-E200-E202.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Feuille','ID conservé','Action','Champ','Avant','Après','Motif source']);w.writerows(delta)
removed_info={'id_retire':'E202-0269','record_avant':removed,'delta_quantity':-1,'family_before':19,'family_after':18,'page_rows_before':357,'page_rows_after':356,'search_source_page':15,'search_normalized_box':[780,840,890,975],'proof':'E202-D2-local-grid.jpg','finding':'Ancien point sur T rond. Prise visible bas-gauche déjà 0270. Aucun autre symbole de prise non couvert constaté dans cette zone élargie. Ne conclut pas à un recomptage exhaustif de la feuille.','ids':'Tous les autres IDs sont conservés, sans réaffectation du numéro 0269.'}
(out/'D2-instance-retiree.json').write_text(json.dumps(removed_info,ensure_ascii=False,indent=2),'utf-8')
# Comparatifs source / ancien gel / rendu corrigé, sur régions identiques.
boxes={
 'D1-H':('E202',(1425,935,1475,975)),
 'D2-prise-retiree':('E202',(810,905,865,945)),
 'D3-T-rond':('E200',(820,230,860,280)),
 'D4-D6-vestibules':('E200',(1470,890,1575,955)),
 'retouche-Q':('E200',(805,885,850,925)),
 'retouches-0448-0449':('E200',(1545,835,1590,865)),
 'retouches-modules':('E200',(1485,835,1520,890)),
 'retouches-BA-ouest':('E200',(750,880,795,925)),
 'retouches-BA-est':('E200',(1530,955,1585,1000)),
 'retouche-0457':('E200',(465,985,490,1005)),
 'retouche-0461':('E200',(960,985,990,1005)),
 'retouche-0462':('E200',(1260,985,1290,1005)),
 'retouche-0463':('E200',(1385,930,1410,950))}
import io
font=ImageFont.truetype(render_sheet.FONT,18)
for k in Z:
 src=Image.open(D/'sources'/f'STAM23A - E - Pour construction - 2024-10-08 - {before[k]["page"]}.png').convert('RGB');scale=src.width/1920
 with zipfile.ZipFile(W/'checkpoints'/Z[k]) as z:oldim=Image.open(io.BytesIO(z.read(f'S-1294-{k}-releve.jpg'))).convert('RGB')
 newim=Image.open(D/f'S-1294-{k}-releve.jpg').convert('RGB')
 for name,(page,b) in boxes.items():
  if page!=k:continue
  box=tuple(round(v*scale) for v in b);ims=[im.crop(box) for im in [src,oldim,newim]]
  factor=2 if ims[0].width<350 else 1
  ims=[im.resize((im.width*factor,im.height*factor)) for im in ims]
  tw,th=ims[0].size;board=Image.new('RGB',(tw*3,th+65),'white');draw=ImageDraw.Draw(board)
  for j,(im,label) in enumerate(zip(ims,['SOURCE','AVANT FIGÉ','CORRIGÉ'])):
   board.paste(im,(j*tw,65));draw.text((j*tw+5,6),label,fill='black',font=font)
  draw.text((5,32),name+' — '+str(box),fill='black',font=font)
  board.save(out/(name+'.jpg'),quality=98)
verification={'changed_anchor_records':len(changes),'delta_field_rows':len(delta),'removed_ids':['E202-0269'],'rows':{k:len(d['records']) for k,d in after.items()},'all_other_ids_quantities_fields_preserved':True,'pixel_review':'Comparatifs générés; contrôle auteur des pixels requis avant gel.','source_sha256':{k:hashlib.sha256((D/'sources'/f'STAM23A - E - Pour construction - 2024-10-08 - {d["page"]}.png').read_bytes()).hexdigest() for k,d in after.items()}}
(out/'verification-delta.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(verification,ensure_ascii=False))
