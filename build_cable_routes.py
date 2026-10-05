"""Record distinct drawn conduit routes; quantities are routes, never inferred metres."""
import json,sys
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
markers=[]
def marker(family,x,y,description,reserve='',scope='PARCOURS — pas une longueur'):
    markers.append(dict(family=family,x=x,y=y,description=description,reserve=reserve,scope=scope,radius=3.1))
sheet=sys.argv[1]
if sheet=='EC-M-RC01':
    source='008'
    marker('Parcours conduit 25 mm',753,381,'Parcours nord, libellé 1 x CONDUIT 25 mm')
    marker('Parcours conduit 63 mm',753,412.6,'Parcours ouest, libellé 1 x CONDUIT 63 mm')
    marker('Parcours conduit 25 mm',1080,438,'Parcours est, libellé 1 x CONDUIT 25 mm')
    marker('Parcours conduit 63 mm EH',875,580.37,'Premier des deux conduits 63 mm EH, représenté séparément',scope='RENVOI_EX-M-DG02')
    marker('Parcours conduit 63 mm EH',890,581.99,'Second des deux conduits 63 mm EH, représenté séparément',scope='RENVOI_EX-M-DG02')
    markers[-1]['radius']=1.3;markers[-2]['radius']=1.3
    marker('Parcours conduit — note B',904.5,578.8,'Conduit avec corde vers conduit existant intercepté DEMARC / niveau 03','* Diamètre non désigné par la note B; ne pas déduire 63 mm.')
    marker('Réseau chemin de câbles',955.5,510,'Un réseau continu en H dans MDF 1.34, bas à 3300 mm selon note A','* Largeur/hauteur du chemin et longueurs non établies.','RÉSEAU CONTINU — RENVOI_EX-M-DT03')
    notes=['6 parcours de conduits distingués : 2 × 25 mm, 3 × 63 mm et 1 selon note B.',
           'Les deux conduits 63 mm EH sont dessinés et repérés individuellement (petites pastilles).',
           '1 réseau continu de chemin de câbles en H : pas un nombre de pièces ou de mètres.',
           'Note A : bas du chemin à 3300 mm du sol. Section et longueurs non déterminées.',
           'Note B : corde de tirage, raccord au conduit existant DEMARC / mécanique niveau 03.',
           'Recouper avec EX-M-DG02 et EX-M-DT03 : aucune addition automatique des parcours.',
           'Coudes, tés, supports, manchons, raccords et métrés non quantifiés.']
    zones={'core':[700,310,1025,620],'eastline':[960,397,1250,468],'conduits-bas':[856,569,921,590]}
elif sheet=='EC-M-0301':
    source='009'
    def frame_point(frame,x,y):
        a,b,w,h,iw,ih={'ul':(260,260,640,340,2048,1088),'ur':(895,260,675,340,2048,1032),'ll':(260,830,640,350,2048,1120),'lr':(895,830,675,350,2048,1062),'r3':(840,410,180,170,725,684),'r4':(840,985,180,175,725,704)}[frame]
        return a+x*w/iw,b+y*h/ih
    def route(family,frame,x,y,description,quantity=1,reserve='',scope='PARCOURS / PORTION — pas un métré'):
        px,py=frame_point(frame,x,y);marker(family,px,py,description,reserve,scope);markers[-1]['quantity']=quantity
    route('Portion chemin 152 × 100 mm','ul',1284,498,'Niveau 03 ouest : indication environ 100 câbles')
    route('Portion chemin 152 × 100 mm','ur',653,401,'Niveau 03 est nord : indication environ 100 câbles')
    route('Portion chemin 152 × 100 mm','ur',1406,499,'Niveau 03 est : indication environ 40 câbles')
    route('Portion chemin 152 × 100 mm','ur',656,663,'Niveau 03 branche sud : indication environ 20 câbles')
    route('Portion chemin 152 × 100 mm','ll',1284,531,'Niveau 04 ouest : indication environ 100 câbles')
    route('Portion chemin 152 × 100 mm','lr',566,503,'Niveau 04 est : indication environ 100 câbles')
    for frame,level in [('r3','03'),('r4','04')]:
        route('Portion chemin IDF',frame,432,376 if level=='03' else 399,'Raccordement chemin dans IDF, niveau '+level,reserve='* Section de la portion IDF non inscrite localement; ne pas inventer sa longueur.')
        route('Groupe conduits 76 mm',frame,53,114 if level=='03' else 125,'Niveau '+level+' côté ouest, 2 x conduits 76 mm',quantity=2)
        route('Groupe conduits 76 mm',frame,621 if level=='03' else 594,114 if level=='03' else 110,'Niveau '+level+' côté est, 2 x conduits 76 mm',quantity=2)
        route('Groupe conduits 63 mm interétages',frame,480,394 if level=='03' else 416,'Niveau '+level+' : 2 conduits, '+('EH' if level=='03' else 'EB'),quantity=2,scope='RENVOI — même liaison niveaux 03/04, ne pas additionner')
        route('Groupe manchons 63 mm',frame,529,423 if level=='03' else 447,'Mention 2 x manchons, '+('EH' if level=='03' else 'EB'),quantity=2,scope='RENVOI — traversée niveaux 03/04, ne pas additionner')
    route('Groupe conduits 63 mm vers RDC','r3',301,361,'2 x conduits 63 mm vers mécanique/RDC',quantity=2,scope='RENVOI_EC-M-RC01 / EX-M-DG02')
    for x,y,room in [(258,475,'4.17'),(451,475,'4.17'),(715,434,'4.17'),(256,670,'4.12'),(449,670,'4.12'),(644,670,'4.12')]:
        route('Parcours conduit 41 mm','ll',x,y,'Data bureaux '+room+'; note C, passage plafond niveau 03')
    for x,y,room in [(1347,79,'4.29'),(1596,458,'4.29'),(1811,456,'4.29'),(1519,668,'4.34'),(1855,670,'4.34'),(1256,942,'4.34')]:
        route('Parcours conduit 42 mm (source)','lr',x,y,'Data bureaux '+room+'; inscription 42 mm conservée',reserve='* 42 mm inscrit ici, contre 41 mm dans la zone ouest : diamètre à confirmer.')
    for x,y,room in [(562,209,'4.26'),(646,711,'4.44'),(571,829,'4.41')]:
        route('Parcours conduit 21 mm','lr',x,y,'Salle '+room+'; notes A/B : sous dalle puis remontée niveau 04')
    notes=['Les pastilles de chemins désignent 8 portions repérées; elles ne sont pas des pièces commerciales.',
           'Sections inscrites 152 × 100 mm; environ 100/40/20 câbles = capacité/occupation, pas un achat de câbles.',
           'Groupes 2x : quantité CSV = 2, une pastille sur le symbole/renvoi commun.',
           'Liaisons 63 mm EH niveau 03 / EB niveau 04 et manchons : mêmes traversées, non additionnables.',
           '6 parcours 41 mm à l’ouest et 6 libellés 42 mm à l’est du niveau 04; conserver cette contradiction.',
           '3 parcours 21 mm aux salles 4.26 / 4.44 / 4.41, descente sous dalle et remontée (A/B).',
           'Note C : data des postes ouverts, passage plafond niveau 03; implantation à coordonner au mobilier.',
           'Aucune longueur de conduit/chemin ni quantité de supports, coudes ou accessoires déduite.']
    zones={'upperleft':[260,260,900,600],'upperright':[895,260,1570,600],'lowerleft':[260,830,900,1180],'lowerright':[895,830,1570,1180],'riser3':[840,410,1020,580],'riser4':[840,985,1020,1160]}
else:raise SystemExit('Unknown sheet')
data=dict(sheet=sheet,source=catalog[source]['file'],markers=markers,csv_type='details',scope='Parcours / réseau — métré non réalisé',legend_box=([260,810,1360,410] if sheet=='EC-M-RC01' else [45,30,1730,150]),legend_columns=(1 if sheet=='EC-M-RC01' else 4),notes=notes,review_zones=zones)
(ROOT/'evidence'/f'{sheet}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))

if sheet=='EC-M-0301':
    data['legend_box']=[50,1440,1900,340]
    data['legend_columns']=2
    (ROOT/'evidence'/f'{sheet}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
