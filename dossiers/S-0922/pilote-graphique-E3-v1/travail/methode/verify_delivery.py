"""Verify delivery hashes, image dimensions, source-coordinate records and CSV parity."""
import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from PIL import Image
import openpyxl

Image.MAX_IMAGE_PIXELS=None

def require(condition, detail):
    """Un contrôle de livraison doit rester actif avec Python -O."""
    if not condition:
        raise ValueError(detail)

def table_digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()

# Transcriptions revues gelées au commit 0085374ee0eb971b2700b91a986f4935c89f8887.
# Empreintes du contenu tabulaire, indépendantes du manifeste régénérable, des
# fins de ligne CSV et des métadonnées ZIP du classeur. Aucun chiffre n'est déduit.
REVIEWED_TABLES={
    'S-0922-E-1-details.csv':('E-1',';','4ec8a5610a01ac8409d7275ab3c139a67236a4d78c2979b162ab4a2246c99a11'),
    'S-0922-E-2-details.csv':('E-2',',','a9db14f77cd8fb1c9c9e4d15a9df9d80e42502ffc801a8cad539a748b4a3e97e'),
    'S-0922-breakers-detailed.csv':('E-2',',','9527eed4446b51849a120190fb02800b028c2566ee7247e80ed5919332e58742'),
    'S-0922-E-2-breakers.csv':('E-2',',','9527eed4446b51849a120190fb02800b028c2566ee7247e80ed5919332e58742'),
}
REVIEWED_WORKBOOK='e229a5164a8360572602ca22d283afec532fddbce43e2e7784246b2b1cd1a751'

require(len(sys.argv) in {2,3} and (len(sys.argv)==2 or sys.argv[2]=='--checkout'),
        'Usage : verify_delivery.py DOSSIER [--checkout]')
checkout=len(sys.argv)==3
root=Path(sys.argv[1]).resolve()
# Le contrôle normal doit laisser intact le paquet, même sans option Python -B.
sys.dont_write_bytecode=True
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
require(isinstance(manifest,list) and bool(manifest),'Manifeste vide ou invalide')
indexed=[]
for record in manifest:
    path=root/record['file']
    require(path.resolve().is_relative_to(root),f'Chemin hors livraison : {path}')
    require(path.stat().st_size==record['bytes'],f'Taille divergente : {path}')
    require(hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],f'Empreinte divergente : {path}')
    require(path.suffix in {'.jpg','.csv','.xlsx','.txt','.json','.py'},f'Type exclu : {path}')
    require(not any(part in {'sources','inspection','__pycache__'} for part in path.relative_to(root).parts),f'Fichier exclu : {path}')
    indexed.append(path.relative_to(root).as_posix())
require(len(indexed)==len(set(indexed)),'Entrées du manifeste dupliquées')
spec=importlib.util.spec_from_file_location('sheet_data',root/'methode/sheet_data.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
checkpoint=json.loads((root/'CHECKPOINT.json').read_text(encoding='utf-8'))
completed=[r['sheet'] for r in checkpoint['completed']]
require(bool(completed) and len(completed)==len(set(completed)),'Feuilles du checkpoint invalides')
require(set(completed)==set(module.SHEETS),'Feuilles checkpoint/données revues divergentes')
require(set(completed)<= {'E-1','E-2','E-3','E-4','E-5'},'Feuille inconnue')
require(checkpoint['remaining']==[s for s in ['E-1','E-2','E-3','E-4','E-5'] if s not in completed],
        'Feuilles restantes divergentes du checkpoint')
for record in checkpoint['completed']:
    require(record['markers']==len(module.SHEETS[record['sheet']].get('markers',[])),
            (record['sheet'],'nombre de repères divergent du checkpoint'))
required={'READ-ME.txt','CHECKPOINT.json'} | {f'methode/{name}.py' for name in
          ['download_plans','prepare_images','render_sheet','package_delivery','verify_delivery','sheet_data']}
for sheet,data in module.SHEETS.items():
    required.add(f'S-0922-{sheet}-releve.jpg')
    if data.get('markers'):
        required.add(f'S-0922-{sheet}-{data.get("csv_type","equipment")}.csv')
    method={'E-2':'build_panels','E-3':'build_lighting','E-4':'build_services','E-5':'build_led'}.get(sheet)
    if method:
        required.add(f'methode/{method}.py')
required.update(name for name,(sheet,_,_) in REVIEWED_TABLES.items() if sheet in completed)
if 'E-2' in completed:
    required.add('S-0922-breakers-by-panel.xlsx')
require(set(indexed)==required,('Inventaire incomplet ou inattendu',sorted(required-set(indexed)),sorted(set(indexed)-required)))
physical={path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file()}
metadata=set()
if checkout:
    # Exceptions explicites du checkout publié, jamais des livrables supplémentaires.
    metadata={'.gitattributes','PR-BODY.md'}
    stems='|'.join(re.escape(Path(name).stem) for name in required if name.startswith('methode/'))
    cache_pattern=rf'methode/__pycache__/(?:{stems})\.cpython-\d+(?:\.opt-[12])?\.pyc'
    metadata.update(name for name in physical if re.fullmatch(cache_pattern,name))
expected=required|{'manifest.json'}
require(physical-metadata==expected,
        ('Inventaire physique incomplet ou inattendu',sorted(expected-physical),sorted(physical-expected-metadata)))
print(f'Inventaire physique : {len(expected)} fichiers de livraison; {len(physical & metadata)} métadonnées de checkout tolérées.')
for sheet,data in module.SHEETS.items():
    markers=data.get('markers',[])
    jpg=root/f'S-0922-{sheet}-releve.jpg'
    with Image.open(jpg) as im:
        require(im.width>=8000 and im.height>=6000,(sheet,'dimensions JPEG insuffisantes'))
        width,height=im.size
    if markers:
        with (root/f'S-0922-{sheet}-{data.get("csv_type","equipment")}.csv').open(encoding='utf-8-sig',newline='') as stream:
            reader=csv.DictReader(stream)
            fields=['Repère / source','Matériel','Désignation','Qté','Portée','Modèle','Prescription / réserve','Parent','X source px','Y source px']
            require(reader.fieldnames==fields,(sheet,'colonnes CSV'))
            records=list(reader)
        require(len(records)==len(markers),(sheet,'nombre de lignes CSV'))
        require(len({r['Repère / source'] for r in records})==len(records),(sheet,'identifiants CSV dupliqués'))
        reviewed={m['id']:m for m in markers}
        require(len(reviewed)==len(markers),(sheet,'identifiants revus non uniques'))
        require({r['Repère / source'] for r in records}==set(reviewed),(sheet,'identifiants CSV divergents'))
        scale=width/1800
        for r in records:
            m=reviewed[r['Repère / source']]
            expected=[m['id'],m['family'],data['families'][m['family']],'1',m.get('scope','INSTALLER'),
                      m.get('model','MODÈLE NON PRÉCISÉ'),m.get('reserve',''),m.get('parent',sheet),
                      round(m['x']*scale,2),round(m['y']*scale,2)]
            require(set(r)==set(fields),(sheet,m['id'],'colonnes supplémentaires'))
            for field,value in zip(fields,expected):
                actual=float(r[field]) if field in {'X source px','Y source px'} else r[field]
                require(actual==value,(sheet,m['id'],field,actual,value))
            require(0<=float(r['X source px'])<=width and 0<=float(r['Y source px'])<=height,(sheet,m['id'],'coordonnées hors image'))
    print(f'{sheet}: {len(markers)} pastilles; {sum(bool(m.get("reserve")) for m in markers)} réserves; JPEG {width}x{height}; CSV concordant')
for name,(sheet,delimiter,expected) in REVIEWED_TABLES.items():
    if sheet in completed:
        with (root/name).open(encoding='utf-8-sig',newline='') as stream:
            rows=list(csv.reader(stream,delimiter=delimiter))
        require(bool(rows) and table_digest([rows[0],sorted(rows[1:])])==expected,
                f'{name} : transcription divergente de la référence revue 0085374')
if 'E-2' in completed:
    workbook=openpyxl.load_workbook(root/'S-0922-breakers-by-panel.xlsx',read_only=True,data_only=False)
    try:
        tables=[[sheet.title,list(sheet.values)] for sheet in workbook]
        require(table_digest(tables)==REVIEWED_WORKBOOK,'Classeur : onglets ou cellules divergents de la référence revue 0085374')
    finally:
        workbook.close()
    print('Disjoncteurs : 91 lignes revues; deux CSV et cinq onglets du classeur concordants; réserves conservées.')
print(f'Manifest : {len(manifest)}/{len(manifest)} tailles et SHA-256 conformes.')
