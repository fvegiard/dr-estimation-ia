"""Record ground-floor fire alarm symbols with explicit grouped interface quantity."""
import json
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
markers=[]
frames={'west':(160,200,440,465,1536,1623),'core':(680,400,295,265,1664,1494),'east':(1210,365,280,275,1596,1568),'middle':(640,200,120,245,780,1594),'modules':(895,385,125,80,814,520)}
def add(family,points,frame,description,scope='INSTALLER',reserve='',quantity=1):
    a,b,w,h,iw,ih=frames[frame]
    for x,y in points:markers.append(dict(family=family,x=a+x*w/iw,y=b+y*h/ih,description=description,scope=scope,reserve=reserve,quantity=quantity,radius=3.1))
add('Klaxon',[(805,149),(1201,791),(676,1335),(1207,1335)],'west','Klaxons cafétéria, vestiaires (2), multifonctions')
add('Klaxon LO',[(1314,416)],'west','Rangement 1.04 — faible niveau sonore LO')
add('Déclencheur manuel ER',[(459,454)],'west','Note A : déplacer et recâbler à l’intérieur du mur de gypse','EXISTANT À RELOCALISER')
add('Klaxon',[(991,247)],'core','Au dégagement des WC 1.37/1.38')
add('Klaxon avec avertisseur visuel',[(1354,593)],'core','MDF 1.34 — 30 cd')
add('Module relais adressable MRA',[(365,433)],'modules','Contrôle porte ESC.2, note hexagonale 1')
add('Groupe interfaces MIA',[(501,433)],'modules','Mention 3x pour système préaction : trois interfaces; un symbole de groupe',quantity=3)
add('Panneau annonciateur TAI',[(391,515)],'middle','TAI représenté dans la zone hachurée','EXISTANT — RENVOI')
add('Déclencheur manuel existant',[(391,868)],'middle','Déclencheur à proximité TAI','EXISTANT — RENVOI')
add('Klaxon existant',[(475,1410)],'middle','Klaxon zone ESC.1','EXISTANT — RENVOI')
add('Déclencheur manuel existant',[(304,339),(126,1241),(1150,1241)],'east','Déclencheurs aux issues et ESC.2','EXISTANT — RENVOI')
add('Détecteur incendie existant',[(813,199)],'east','Détecteur près ESC.2, aucune lettre de type lisible','EXISTANT — RENVOI','* Sous-type du détecteur non inscrit à côté du symbole : ne pas choisir fumée/chaleur.')
data=dict(sheet='EA-M-RC01',source=catalog['045']['file'],markers=markers,csv_type='symbols',scope='RDC R3 — neuf et existant distingués',legend_box=[250,800,1250,470],notes=[
'MIA : une pastille sur le symbole 3x; quantité CSV = 3 modules pour préaction.',
'Déclencheur cafétéria ER : déplacement et recâblage selon note A; pas un achat neuf.',
'MRA : contrôle de porte ESC.2; coordination avec contrôle d’accès, pas de doublon au détail.',
'Les appareils des zones hachurées sont conservés séparément comme représentations existantes.',
'* Type du détecteur près ESC.2 non précisé; aucun modèle ni sous-type inventé.',
'Aucun ajout de quantité depuis le diagramme existant EX-E-DG01.',
'Marques/modèles et longueurs de câbles/conduits non déterminés.'],review_zones={'west':[265,230,575,590],'core':[780,403,1020,555],'middle':[640,200,760,445],'east':[1210,365,1490,640]})
(ROOT/'evidence/EA-M-RC01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
