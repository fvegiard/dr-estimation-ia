"""Transcribe ground-floor service symbols; enlarged views replace boxed areas."""
import json
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
markers=[]
frames={'floor':(150,180,338,370,1504,1646),'cafe':(130,818,337,347,1552,1600),'core':(662,775,253,390,1168,1800),'outside':(1100,408,120,175,781,1139)}
def add(family,points,room,frame='floor',scope='INSTALLER',reserve='',description=None,quantity=1):
    a,b,w,h,iw,ih=frames[frame]
    for x,y in points:markers.append(dict(family=family,x=a+x*w/iw,y=b+y*h/ih,description=description or family,parent=room,scope=scope,reserve=reserve,quantity=quantity,radius=2.5))
# The three dashed enlarged zones are counted on their large views only.
add('Prise double 15 A',[(160,107),(160,338),(743,59)],'Cafétéria 1.03')
add('Sortie télécom',[(132,107),(131,338),(740,94)],'Cafétéria 1.03',description='Note D : sortie 450 mm, conduit en colonne')
add('Prise double 15/20 A',[(777,668)],'Cafétéria 1.03',description='Symbole 5-20R circuit 22, N')
add('Sortie réseau Wi-Fi',[(629,293)],'Cafétéria 1.03',description='Sortie WIFI P; équipement actif non déduit')
add('Sortie data caméra',[(595,453)],'Cafétéria 1.03',description='Sortie CAM P; caméra non additionnée au plan sécurité')
add('Prise double 15 A',[(1359,439)],'Rangement 1.04')
add('Sortie télécom',[(1357,412)],'Rangement 1.04')
add('Raccordement serpentin',[(1319,254)],'Rangement 1.04',description='SE1-001-RC1 — 18 kW; point de raccordement mécanique')
add('Sortie réseau Wi-Fi',[(1310,792)],'Vestiaires 1.01')
add('Sortie data caméra',[(1245,874)],'Vestiaires 1.01')
add('Prise double 15/20 A',[(900,959),(973,1566)],'Vestiaires 1.01',description='Symbole 5-20R, circuit 22, N')
add('Prise double 15 A',[(160,1049),(793,1026),(160,1520),(744,1527)],'Multifonctions 1.02')
add('Sortie télécom',[(131,1049),(764,1026),(131,1518)],'Multifonctions 1.02',description='Note D : sortie 450 mm, conduit en colonne')
add('Sortie télécom double',[(741,1563)],'Multifonctions 1.02',description='Une plaque, indication (2) : deux sorties; note D')
add('Raccordement toile motorisée',[(125,y) for y in [932,1101,1243,1324,1401,1557]]+[(x,1570) for x in [236,318,401]],'Multifonctions 1.02',description='Note 3 : 118 W / 120 V; EQ11.2 architecture. Circuit 24',reserve='* Modèle de toile : plans architecture non fournis au dossier de plans reçu.')
add('Monument de plancher C',[(246,1215),(450,1215),(658,1215)],'Multifonctions 1.02',description='Type C : deux prises doubles 15 A, boîtier encastré poke thru résistant au feu 2 h; une pastille par ensemble')
add('Prise double 15 A',[(429,1318)],'Multifonctions 1.02',description='Prise P circuit 43')
add('Sortie réseau Wi-Fi',[(583,1190)],'Multifonctions 1.02')
add('Backbox téléviseur',[(855,1177),(855,1384)],'Multifonctions 1.02',description='CHIEF PAC525/526, note 4')
add('Prise double 15 A en hauteur',[(815,1190),(815,1367)],'Multifonctions 1.02',description='Circuit 34; note A intérieur backbox')
add('Sortie télécom',[(814,1157),(814,1397)],'Multifonctions 1.02',description='Note A intérieur backbox')
add('Prise double 15 A',[(819,1227)],'Multifonctions 1.02',description='Circuit 34; note H dans rack 2 gangs')
add('Boîte AV 2 gangs',[(820,1260)],'Multifonctions 1.02',description='Note K : HM 450 mm, conduit 53 mm à la boîte supérieure')
add('Boîte AV 1 gang',[(820,1287)],'Multifonctions 1.02',description='Note L : HM 1780 mm, conduit 53 mm vers entreplafond')
add('Sortie télécom double',[(816,1320)],'Multifonctions 1.02',description='Note H : plaque (2) dans rack; deux sorties indiquées')
add('Prise double 15 A en hauteur',[(553,1535)],'Multifonctions 1.02',description='Circuit 43, note J haut de toile de projection')
add('Prise double 15/20 A',[(457,1568)],'Multifonctions 1.02',description='Circuit 22, N, 5-20R')
add('Raccordement serpentin',[(757,1425)],'Multifonctions 1.02',description='SE2-001-RC1 — 13 kW; point de raccordement mécanique')
# Enlarged cafeteria equipment outlets, not appliance procurement.
add('Prise double 15 A en hauteur',[(235,145),(343,145)],'Cafétéria 1.03','cafe',description='M.-O. circuits 5 et 7')
add('Prise double 15/20 A en hauteur',[(632,145),(1017,1048)],'Cafétéria 1.03','cafe',description='Circuit 47, symbole 5-20R')
for y,circuit,item in [(266,9,'Machine à café'),(349,11,'Machine à café'),(443,15,'Machine à café'),(496,17,'Machine à café'),(617,19,'Machine à café'),(918,23,'Machine à café'),(1142,27,'Machine à eau'),(1299,29,'Distributeur boissons fontaine')]:
    add('Prise double 15/20 A en hauteur' if circuit==19 else 'Prise double 15 A en hauteur',[(1018,y)],'Cafétéria 1.03','cafe',description=f'{item}, circuit {circuit}; note E architecture pour spécification de charge',reserve='* Spécification de l’appareil de cuisine à confirmer aux plans architecte/designer non reçus.')
for y,circuit,item in [(408,13,'Réfrigérateur à lait'),(795,21,'Réfrigérateur présentation boissons deux portes'),(949,25,'Machine à glace sous comptoir')]:
    add('Prise double 15 A',[(1018,y)],'Cafétéria 1.03','cafe',description=f'{item}, circuit {circuit}; note E',reserve='* Spécification de la charge à confirmer aux plans architecte/designer non reçus.')
add('Prise double 15 A',[(477,574),(496,1038)],'Cafétéria 1.03','cafe',description='Lave-vaisselle, circuits 16/18; note G passage via sous-sol')
add('Prise double 15 A en hauteur',[(893,763)],'Cafétéria 1.03','cafe',description='Circuit 20, note F/A')
add('Sortie télécom',[(897,800)],'Cafétéria 1.03','cafe',description='Note A, intérieur backbox')
add('Backbox téléviseur',[(896,836)],'Cafétéria 1.03','cafe',description='Point/boîte TV au détail, note A; équipement exact à confirmer',reserve='* Type de boîte TV non désigné au détail cafétéria.')
add('Prise double 15 A',[(x,1451) for x in [233,328,424,520,616]],'Cafétéria 1.03','cafe',description='Réfrigérateurs R, circuits 14/12/10/8/6')
add('Prises 15 A — groupe M.-O.',[(719,1448)],'Cafétéria 1.03','cafe',description='Mention x2, circuits 33 et 35 : quantité 2, un symbole de groupe',quantity=2)
add('Prise double 15 A en hauteur',[(885,1448)],'Cafétéria 1.03','cafe',description='Distributeur boissons fontaine circuit 31')
# Enlarged toilets and mechanical room.
add('Prise double 15 A',[(260,345),(936,345)],'WC 1.37 / 1.38','core',description='Note 6 : sous lavabo pour robinet; circuit 40')
add('Raccordement miroir lumineux',[(294,345),(901,345)],'WC 1.37 / 1.38','core',description='Note 2 : 44 W / 120 V; circuit 40')
add('Prise 15 A avec DDFT',[(366,341),(840,341)],'WC 1.37 / 1.38','core',description='Circuit 40; point au-dessus du triangle = DDFT')
add('Sèche-mains encastré',[(413,358),(800,358)],'WC 1.37 / 1.38','core',description='ASI Turbo-Tuff, 320×400 mm, 1000 W / 120 V, circuits 36/38')
add('Prise double 15 A',[(892,409)],'Mécanique 1.36','core',description='Pour UB1, circuit 1, HM 2300 mm; batterie déjà à EE-M-RC01')
for pt,desc in [((716,409),'TP-RDC-2, 8/10/12 C1-1'),((947,409),'TP-RDC-3, 14/16/18 C1-1'),((454,1126),'TP-RDC-1, 13/15/17 C1-1'),((726,1643),'TP-RDC-3, 19/21/23 C1-1')]:
    add('Point de raccordement TP',[pt],'Mécanique 1.36','core',description=desc,reserve='* Deux points portent TP-RDC-3 avec des circuits différents : identité à confirmer.' if 'TP-RDC-3' in desc else '')
add('Plinthe / convecteur',[(440,416)],'Mécanique 1.36','core',description='Circuit 4 C1-1',reserve='* Puissance de la plinthe horizontale non inscrite.')
add('Plinthe / convecteur',[(1075,1498)],'Mécanique 1.36','core',description='Circuit 4 C1-1; 1000 W inscrits au plan')
add('Thermostat',[(356,656)],'Mécanique 1.36','core')
add('Raccordement pompe',[(447,598)],'Mécanique 1.36','core',description='PO-RDC-1, 41 C1-2; raccordement, pas fourniture mécanique')
add('Raccordement chauffe-eau',[(272,764)],'Mécanique 1.36','core',description='CE, 27/29 C1-1; raccordement, pas fourniture mécanique')
add('Prise existante',[(1079,790)],'Mécanique 1.36','core','EXISTANT',description='26(C2-1)')
add('Prise double 15/20 A',[(833,1340)],'Mécanique 1.36','core',description='Sous panneau, symbole 5-20R')
for pt,desc,scope in [((935,904),'PG-1','RENVOI_EE-M-RC01'),((931,1029),'C1-2','RENVOI_CÉDULE'),((933,1152),'C1-3','RENVOI_CÉDULE'),((928,1247),'SF1-1, alimenté par T2-1, F.150 A','EXISTANT / RENVOI_DISTRIBUTION'),((931,1348),'C1-1, alimenté par SF1-1','EXISTANT / RENVOI_CÉDULE')]:
    add('Panneau / équipement distribution',[pt],'Mécanique 1.36','core',scope,description=desc)
add('Interrupteur SW1-1',[(584,1366)],'Mécanique 1.36','core','RENVOI_DISTRIBUTION',description='SW1-1, F.250 A inscrits')
add('Transformateur T1-1',[(613,1526)],'Mécanique 1.36','core','RENVOI_DISTRIBUTION',description='75 kVA, alimenté par C1-3, EM')
add('Raccordement évaporateur',[(509,1471)],'Mécanique 1.36','core',description='14/16/18 C1-3; raccordement, pas fourniture mécanique')
add('Raccordement condenseur',[(197,935)],'Extérieur','outside',description='CS1-001-RC1, 8/10/12 C1-3; équipement mécanique')
add('Interrupteur de sûreté EI',[(139,936)],'Extérieur','outside',reserve='* Calibre EI non indiqué; ne pas le déduire du disjoncteur.')
add('Sortie data caméra',[(110,144)],'Zone est','outside',description='CAM P; caméra non additionnée au plan sécurité')
markers.append(dict(family='Sortie data caméra',x=698.65,y=320.5,description='CAM P, sortie plafond; caméra au plan sécurité',parent='Zone centrale',scope='INSTALLER',radius=2.5))
data=dict(sheet='ES-M-RC01',source=catalog['044']['file'],markers=markers,csv_type='equipment',legend_columns=2,scope='RDC R3 — vues agrandies substituées',legend_box=[1000,775,760,600],notes=[
'Une pastille par symbole; le groupe M.-O. x2 a une quantité CSV de 2.',
'Monuments C : 3 ensembles, chacun contient 2 prises; pas de second total.',
'Les zones 02/03 sont comptées uniquement sur leurs vues agrandies.',
'MDF 1.34 : renvoi EX-M-DT03, pas de décompte supplémentaire ici.',
'Les panneaux et équipements de distribution sont des renvois.',
'* TP-RDC-3 : deux raccordements, circuits différents; identité à confirmer.',
'* Charges de cuisine / toiles : renvois architecture non reçus.',
'* Sectionneur EI sans calibre; longueurs de câbles/conduits non métrées.'],review_zones={'floor-north':[175,183,483,390],'floor-south':[165,385,476,552],'cafe':[130,818,467,1165],'core':[662,775,915,1165],'outside':[1100,408,1220,583],'center-symbol':[670,290,725,345]})
(ROOT/'evidence/ES-M-RC01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
