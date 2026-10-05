"""Correction unique de la lettre de commande après revue delta E205 v2."""
import json,zipfile,csv,copy,sys,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parents[1];W=D.parents[3]
sys.path.insert(0,str(Path(__file__).parent));import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'
with zipfile.ZipFile(W/'checkpoints/S-1294-E205-checkpoint-v2.zip') as z:
 old=json.loads(z.read('audit/E205-records.json'))
 before_hashes={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.jpg')}
new=copy.deepcopy(old);r=next(r for r in new['records'] if r['id']=='E205-0108')
original=r['label'];assert original.endswith('commande b');r['label']=original[:-1]+'f'
changes=[(a['id'],k,a.get(k),b.get(k)) for a,b in zip(old['records'],new['records']) for k in set(a)|set(b) if a.get(k)!=b.get(k)]
assert changes==[('E205-0108','label',original,r['label'])]
(D/'audit/E205-records.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),'utf-8');render_sheet.render('E205')
for n,h in before_hashes.items():assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h,n
with (D/'S-1294-delta-E205-v3.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','Champ','Avant','Après','Motif']);w.writerow(['E205-0108','Désignation',original,r['label'],'Source page 18 : f du mécanisme supérieur, e du mécanisme inférieur.'])
out=W/'evidence/delta-E205';out.mkdir(exist_ok=True)
src=Image.open(D/'sources/STAM23A - E - Pour construction - 2024-10-08 - 18.png').convert('RGB')
crop=src.crop((2280,1620,2540,1860)).resize((520,480))
proof=Image.new('RGB',(1100,580),'white');proof.paste(crop,(0,75));draw=ImageDraw.Draw(proof);font=ImageFont.truetype(render_sheet.FONT,21)
for x,y,t in [(10,8,'E205-0108 — source page 18'),(540,110,'Avant v2 : commande b'),(540,155,'Après v3 : commande f'),(540,220,'Mécanisme supérieur : f'),(540,255,'Mécanisme inférieur 0107 : e'),(540,320,'ID, position, quantité inchangés'),(540,365,'Tous les JPG identiques à v2')]:draw.text((x,y),t,fill='black',font=font)
proof.save(out/'E205-0108-correction.jpg',quality=98)
(out/'verification.json').write_text(json.dumps({'changes':changes,'all_jpg_sha256_unchanged':True,'records':169,'spot_counts_unchanged':'16 E / 18 F','source_sha256':hashlib.sha256((D/'sources/STAM23A - E - Pour construction - 2024-10-08 - 18.png').read_bytes()).hexdigest()},ensure_ascii=False,indent=2),'utf-8')
print('E205-0108 : b → f. Un champ changé; tous les JPG identiques à v2.')
