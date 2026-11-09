"""Record sheet identities read directly from source title blocks."""
import csv, json
from pathlib import Path
root = Path(__file__).resolve().parent
index = json.loads((root/'inspection/index.json').read_text())
base = {
1:('EX-M-0000','Page frontispice — liste des dessins'),2:('EX-M-LG01','Légende électrique'),
3:('EX-M-LG02','Liste des appareils d’éclairage, panneaux de contrôle et détails'),
4:('EX-E-DE01','Distribution électrique — existant'),5:('EX-M-DE01','Distribution électrique — modifié'),
6:('EM-D-SS01','Multidisciplinaire — sous-sol et RDC — démolition'),7:('EM-D-0301','Multidisciplinaire — niveaux 03 et 04 — démolition'),
8:('EE-M-RC01','Éclairage — RDC'),9:('EE-M-0301','Éclairage — niveaux 03 et 04'),
10:('ES-D-SS01','Services — sous-sol et RDC — démolition'),11:('ES-M-RC01','Services — RDC'),
12:('ES-D-0301','Services — niveaux 03 et 04 — démolition'),13:('ES-M-0301','Services et télécommunication — niveaux 03 et 04'),
14:('ES-M-0T01','Services — toit'),15:('EC-M-RC01','Chemins de câbles et conduits vides — RDC'),16:('EC-M-0301','Chemins de câbles et conduits vides — niveaux 03 et 04'),
17:('EA-M-RC01','Alarme incendie — RDC'),18:('EA-M-RC02','Sécurité et caméra — RDC'),19:('EA-M-0301','Alarme incendie — niveaux 03 et 04'),20:('EA-M-0302','Sécurité et caméra — niveaux 03 et 04'),
21:('EX-E-DG01','Diagramme alarme incendie — signalisation et détection'),22:('EX-M-DG02','Diagramme télécommunication'),
23:('EX-M-DT01','Vues agrandies — éclairage et services'),24:('EX-M-DT02','Détails électriques'),25:('EX-M-DT03','Vues agrandies — télécommunication et services'),26:('EX-M-DT04','Détails télécommunication'),27:('EX-M-DT05','Détails et diagramme télécommunication et sécurité'),28:('EX-E-PE01','Panneaux électriques — existants'),29:('EX-M-PE01','Panneaux électriques — nouveaux')}
changes={1:(8,'06','2024-01-12'),31:(2,'02','2024-03-13'),32:(2,'02','2024-03-13'),33:(3,'05','2024-03-13'),34:(3,'05','2024-03-13'),35:(8,'04','2024-03-13'),36:(8,'04','2024-03-13'),37:(9,'04','2024-03-13'),38:(13,'05','2024-03-13'),39:(25,'02','2024-03-13'),40:(29,'05','2024-03-13'),41:(3,'06','2024-04-24'),42:(8,'05','2024-04-24'),43:(9,'05','2024-04-24'),44:(11,'3','2024-04-24'),45:(17,'3','2024-04-24'),46:(18,'2','2024-04-24'),47:(29,'06','2024-04-24'),59:(5,'2','2024-11-14'),60:(13,'7','2024-11-14')}
selected = {2:31,3:41,5:59,8:42,9:43,11:44,13:60,17:45,18:46,25:39,29:47}
rows=[]
for row in index:
    n=int(row['id']); name=Path(row['file']).name
    row.update(sheet='', title='', revision='', date='', status='', reserve='')
    if name.startswith('169 - '):
        p=int(name.rsplit(' - ',1)[1].split('.')[0]); row['sheet'],row['title']=base[p]
        row.update(revision='0',date='2023-10-31',status='À relever' if p not in selected else 'Version antérieure — non additionnable')
        if p==1:row['status']='Document de référence — aucun appareil à compter'
    elif n in changes:
        p,revision,date=changes[n];row['sheet'],row['title']=base[p]
        row.update(revision=revision,date=date,status='À relever' if selected.get(p)==n else 'Version antérieure ou variante — non additionnable')
    elif n in {58,61,62}:
        row['sheet'],row['title']={58:('MG-M-RC01','Protection incendie — RDC'),61:('MX-M-LG01','Mécanique — légende et tableaux'),62:('MV-M-0401','Ventilation — niveau 4')}[n]
        row['status']='Non électrique — non relevée'
    elif 50<=n<=57:
        row.update(title='Changement 011 — document textuel',status='Document à examiner — aucune quantité automatique')
    else:row.update(title='Document Connectrac',status='Hors plans — exclu du relevé aveugle')
    if row['sheet']=='EE-M-RC01':row['reserve']='* Révision 06 datée du 2024-01-12, puis 04 et 05 en mars/avril : ordre contradictoire. Version du 2024-04-24 retenue pour lecture, validation contractuelle requise.'
    rows.append(row)
(root/'sheet-catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (root/'S-0844-inventaire-feuilles.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID source','Fichier','Feuille','Titre','Révision','Date','État','Réserve'])
    for r in rows:w.writerow([r[k] for k in ['id','file','sheet','title','revision','date','status','reserve']])
checkpoint=json.loads((root/'CHECKPOINT.json').read_text())
checkpoint.update(etat='Inspection des plans et relevé en cours',sources_distinctes=63,doublons_sha256=12,feuilles_restantes=[r['sheet'] for r in rows if r['status']=='À relever'])
(root/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
