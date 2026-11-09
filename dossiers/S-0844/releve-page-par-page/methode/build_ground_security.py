"""Read security infrastructure symbols and keep hatched-area scope conflicts explicit."""
import json
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
frames={'west':(250,235,340,350,1554,1600),'middle':(640,235,370,330,1664,1484),'east':(1190,305,370,280,1818,1376),'doorwest':(545,375,65,71,423,461),'doormdf':(980,485,50,59,326,384)}
markers=[]
def add(family,points,frame,room,scope='INFRASTRUCTURE',reserve='',description=None):
    a,b,w,h,iw,ih=frames[frame]
    for x,y in points:markers.append(dict(family=family,x=a+x*w/iw,y=b+y*h/ih,description=description or family,parent=room,scope=scope,reserve=reserve,radius=2.6))
conflict='* Symbole spécifique dessiné en zone hachurée HORS CONTRAT : portée à confirmer.'
add('Sortie caméra plafond',[(678,429),(1277,870)],'west','Cafétéria / vestiaires',description='Infrastructure; installation et patch cord de caméra par le client')
add('Sortie contact magnétique',[(164,534)],'west','Porte extérieure cafétéria')
for frame,room,points,reserve in [
    ('doorwest','Groupe 01 — corridor',{'contact':[(144,159),(144,319)],'strike':[(145,222)],'request':[(101,238)],'reader':[(273,363)]},''),
    ('middle','Groupe 01 — accès central',{'contact':[(287,694),(287,805)],'strike':[(287,737)],'request':[(315,750)],'reader':[(270,650)]},conflict),
    ('doormdf','Groupe 09 — MDF 1.34',{'contact':[(176,174)],'strike':[(176,248)],'request':[(150,210)],'reader':[(201,300)]},''),
    ('east','Groupe 13 — ESC.2',{'contact':[(263,565)],'strike':[(312,565)],'request':[(288,593)],'reader':[(252,450)]},conflict)]:
    for key,label in [('contact','Sortie contact magnétique'),('strike','Sortie gâche électrique'),('request','Sortie requête de sortie'),('reader','Sortie lecteur de cartes')]:
        add(label,points[key],frame,room,reserve=reserve)
add('Sortie caméra plafond',[(632,640)],'middle','Zone centrale',reserve=conflict,description='Infrastructure CAM au plafond; recoupement ES-M-RC01')
add('Sortie caméra plafond',[(180,741)],'east','ESC.2',reserve=conflict,description='Infrastructure CAM au plafond; recoupement ES-M-RC01')
add('Sortie caméra murale',[(1268,1255)],'middle','MDF 1.34',description='Infrastructure caméra murale; recoupement plan agrandi MDF')
add('Panneau de sécurité',[(1244,1390)],'middle','MDF 1.34',description='1200 mm × 250 mm inscrits; composants détaillés à EX-M-DT05',scope='RENVOI_DÉTAIL — enveloppe représentée')
data=dict(sheet='EA-M-RC02',source=catalog['046']['file'],markers=markers,csv_type='symbols',scope='RDC R2 — infrastructures sécurité',legend_box=[250,810,1310,400],notes=[
'5 sorties caméra : 4 au plafond, 1 murale; appareils/patch cords installés par le client.',
'4 groupes de porte représentés : deux groupes 01, un groupe 09 et un groupe 13.',
'1 contact isolé à la porte extérieure de la cafétéria, en plus des contacts des groupes.',
'* Groupes central 01 et ESC.2 / caméras centrales : symboles en zone HORS CONTRAT; portée à confirmer.',
'Les sorties CAM du plan ES-M-RC01 sont les mêmes infrastructures : ne pas additionner.',
'Panneau de sécurité 1200 × 250 mm : une enveloppe; composants au détail, sans doublon.',
'Les groupes décrivent des sorties, pas une fourniture arbitraire de quincaillerie.',
'Longueurs de câbles et conduits non métrées; aucun modèle choisi.'],review_zones={'west':[265,295,590,440],'doorwest':[545,375,610,446],'central':[690,345,800,425],'mdf':[905,482,1030,560],'east':[1200,370,1275,475]})
(ROOT/'evidence/EA-M-RC02.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
