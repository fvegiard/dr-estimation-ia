"""Build individually inspected sheets from explicit source symbol anchors."""
from pathlib import Path
import json,sys
from render_sheet import render
root=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((root/'sheet-catalog.json').read_text())}
def marker(family,x,y,description,scope,reserve='',parent=''):
    return dict(family=family,x=x,y=y,description=description,scope=scope,reserve=reserve,parent=parent,radius=4.2)
sheet=sys.argv[1]
if sheet=='ES-M-0T01':
    source='007';scope='Plan toiture — 31 octobre 2023, révision 0'
    markers=[]
    for tag,y,dy,panel in [('CS2-001-006',374.8,364.1,'C3-2'),('CS3-001-006',399.7,389.4,'C4-2')]:
        markers.append(marker('Raccordement mécanique',525.8,y,tag+' — circuits 75,77 ('+panel+')','RACCORDER — appareil mécanique distinct du sectionneur',parent=tag))
        markers.append(marker('Interrupteur de sûreté ≤ 240 V',525.8,dy,'Interrupteur EI de '+tag,'INSTALLER','* Calibre de l’interrupteur non indiqué au plan; ne pas déduire du disjoncteur 25 A.',tag))
    notes=['Deux appareils mécaniques et leurs deux interrupteurs EI représentés au toit.',
           'CS2-001-006 : C3-2 / 75,77. CS3-001-006 : C4-2 / 75,77.',
           '* Aucun calibre de sectionneur choisi. Les disjoncteurs sont déjà comptés à EX-M-PE01.',
           'Appareils mécaniques : points de raccordement, aucune fourniture mécanique déduite.',
           'Câbles, conduits et longueurs non métrés. Modèles non précisés.']
    box=[260,800,1370,240];zones={'appareils':[450,335,555,440],'toiture-ouest':[210,225,1000,650],'toiture-est':[1000,225,1620,650]}
elif sheet=='EX-M-DG02':
    source='016';scope='Diagramme télécommunication — symboles de renvoi'
    markers=[marker('Cabinet télécom représenté',401.0,361.9,'Cabinet 2 — salle MDF 1.34','RENVOI_EX-M-DT03'),marker('Cabinet télécom représenté',424.0,361.9,'Cabinet 1 — salle MDF 1.34','RENVOI_EX-M-DT03')]
    notes=['Deux cabinets dessinés; aucune quantité supplémentaire aux armoires du plan agrandi.',
           'RDC–niveau 3 : 1 conduit 63 mm / 2 fibres OM4 12 brins; 1 conduit 63 mm / corde DAS.',
           'Niveau 3–niveau 4 : 1 conduit 63 mm / fibre OM4 12 brins; 1 conduit 63 mm / corde DAS.',
           'Entre cabinets RDC : 2 fibres OM4 12 brins. Vers sous-sol : conduit 63 mm / corde.',
           'Note A : utiliser le conduit déjà présent indiqué. Longueurs non déterminables au diagramme.',
           'Les rectangles pointillés sont des locaux, pas des appareils. Aucune extrapolation.']
    box=[800,650,940,260];zones={'diagramme':[150,140,750,500],'note-A':[1540,35,1800,110]}
elif sheet=='EX-M-DT02':
    source='018';scope='Diagramme de mise à la terre — pas un achat global'
    markers=[]
    for level,y in [('Niveau 4',466.0),('Niveau 3',587.3),('RDC',831.0)]:
        for room,x in [('Salle électrique',576.2),('Salle MDF',769.2)]:markers.append(marker('Barre de mise à la terre',x,y,room+' — '+level,'RENVOI_PLANS_DE_NIVEAU'))
    markers.append(marker('Barre de mise à la terre existante',495.4,962.7,'Salle électrique principale — sous-sol','CONSERVER / RENVOI'))
    notes=['Six barres aux niveaux 4, 3 et RDC; une barre existante au sous-sol.',
           'Quantités de symboles au diagramme seulement : recouper avec les vues agrandies.',
           'Libellés source : 1#6V, C.21 mm et 1#1/0V, C.21 mm conservés sans choix de calibre.',
           'Longueurs des conducteurs et conduits non déterminées; aucun métré au diagramme.',
           'Modèles et dimensions des barres non précisés.']
    box=[1220,660,535,300];zones={'barres-haut':[470,420,870,650],'barres-bas':[340,760,920,1030]}
else:raise SystemExit('Unknown sheet')
data=dict(sheet=sheet,source=catalog[source]['file'],markers=markers,csv_type='equipment' if sheet=='ES-M-0T01' else 'details',scope=scope,legend_box=box,notes=notes,review_zones=zones)
(root/'evidence'/f'{sheet}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
render(data)
