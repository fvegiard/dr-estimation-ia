"""Record visually read ground-floor lighting anchors, without area extrapolation."""
import json
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
markers=[]
def add(family,points,room,scope='INSTALLER',reserve='',description=None,frame='west'):
    x0,y0,w,h,iw,ih=(250,230,350,395,1502,1696) if frame=='west' else (785,403,225,197,1464,1281)
    for x,y in points:
        markers.append(dict(family=family,x=x0+x*w/iw,y=y0+y*h/ih,description=description or family,parent=room,scope=scope,reserve=reserve,radius=2.5))
add('Luminaire L05f',[(x,120) for x in [151,284,417,548,680,812,944,1075]]+[(151,220),(151,320)]+[(1075,y) for y in [259,356,465,563]]+[(812,563),(944,563)],'Cafétéria 1.03')
add('Luminaire L05f',[(1269,y) for y in [117,283,429,594]],'Rangement 1.04')
add('Luminaire L05f',[(x,y) for x in [174,316,457,599,718] for y in [1030,1182,1285,1437]],'Multifonctions 1.02')
add('Luminaire L05f',[(x,y) for x in [899,1091,1284] for y in [954,1086,1220,1360,1495]],'Vestiaires 1.01')
add('Luminaire L05i',[(296,260),(519,286),(450,365),(245,539),(526,560)],'Cafétéria 1.03')
add('Luminaire L05h',[(253,350),(369,320),(373,562),(604,489)],'Cafétéria 1.03')
add('Luminaire L05k',[(326,475),(617,293),(448,502)],'Cafétéria 1.03')
add('Luminaire L04e',[(864,259),(864,465)],'Cafétéria 1.03')
add('Luminaire L08d',[(x,732) for x in [250,340,431,522,613,696,777,861,959,1040,1121,1205,1285]]+[(x,825) for x in [163,249,341,431,522,614,698,778,861,960,1041,1122,1207,1284]],'Corridor')
add('Luminaire L03a',[(x,917) for x in [174,316,457,599,718]],'Multifonctions 1.02')
for family,pts in [('L05m',[(1156,1020),(1040,1094),(1077,1279),(1178,1352)]),('L05n',[(999,984),(976,1233),(1207,1214)]),('L05o',[(1132,1128),(1018,1395)])]:
    add('Panneau acoustique '+family,pts,'Vestiaires 1.01','ACCESSOIRE ACOUSTIQUE — distinct des luminaires')
add('Détecteur de présence',[(1269,199),(1269,512)],'Rangement 1.04')
add('Détecteur de présence',[(899,1026),(1284,1026),(899,1294),(1284,1294)],'Vestiaires 1.01')
add('Clavier numérique CL',[(755,637)],'Cafétéria 1.03')
add('Clavier numérique CL',[(784,1003)],'Multifonctions 1.02')
add('Commande graduée M',[(1341,696)],'Corridor',reserve='* Symbole gradateur avec suffixe M; fonction exacte à confirmer.')
add('Point de raccordement',[(1158,352)],'Cafétéria 1.03',description='Point de raccordement 1mm; renvoi hexagonal 1, charge non désignée.',reserve='* Charge du raccordement 1mm non désignée sur cette feuille.')
add('Phare double Y2',[(700,586)],'Cafétéria 1.03',description='Y2 alimenté par UB1')
add('Phare double Y2',[(1178,850)],'Corridor',description='Y2 alimenté par UB1')
add('Issue existante ER',[(188,524),(1336,770)],'Cafétéria / corridor','EXISTANT À RELOCALISER')
add('Luminaire existant EX3',[(138,438),(138,554),(138,669)],'Cafétéria 1.03','EXISTANT',description='EX3-18(S1), trois symboles muraux conservés distincts')
for pt,n in [((1199,952),3),((918,1435),4),((1271,1435),4)]:
    add('Groupe ruban DEL L06f',[pt],'Vestiaires 1.01','NOTE — groupe de segments',description=f'L06f : {n}x selon la flèche du plan; longueurs non indiquées.',reserve='* Longueur des segments non indiquée; ne pas assimiler une flèche à un mètre.')
add('Luminaire L03d',[(261,200),(435,201),(705,201)],'WC 1.37 / 1.38 / accès',frame='core')
add('Phare simple Y1',[(154,256),(811,256)],'WC 1.37 / 1.38',description='Y1 alimenté par UB1',frame='core')
add('Unité accumulateurs UB1',[(692,318)],'Mécanique 1.36',description='UB1 — 72 W inscrits au plan',frame='core')
add('Interrupteur avec présence',[(367,252),(602,252)],'WC 1.37 / 1.38',frame='core')
add('Luminaire existant EX1',[(647,537),(647,997)],'Mécanique 1.36','EXISTANT À RELOCALISER',frame='core')
add('Luminaire urgence existant EX1',[(647,766)],'Mécanique 1.36','EXISTANT À RELOCALISER',description='EX1-5(UE1) 24H ER',frame='core')
add('Luminaire existant EX7',[(991,558),(1290,558),(991,944),(1290,944)],'MDF 1.34','EXISTANT À RELOCALISER',frame='core')
add('Interrupteur minuterie',[(260,478)],'Mécanique 1.36',frame='core')
add('Interrupteur unipolaire',[(1431,850)],'MDF 1.34',frame='core')
add('Panneau PG-1',[(732,697)],'Mécanique 1.36',description='Panneau de contrôle éclairage PG-1; un appareil, rectangle de désignation exclu',frame='core')
add('Interface IC',[(301,775)],'Mécanique 1.36',reserve='* Désignation IC au plan; spécification détaillée non établie.',frame='core')
data=dict(sheet='EE-M-RC01',source=catalog['042']['file'],markers=markers,csv_type='equipment',legend_columns=2,scope='RDC R05 — symboles et notes séparés',legend_box=[245,780,1300,615],notes=[
'* Ordre des révisions contradictoire : R06 du 12 janvier / R05 du 24 avril 2024. R05 utilisée ici.',
'L05m/n/o : 9 panneaux acoustiques, pas des luminaires (cédule EX-M-LG02).',
'L06f : 3 flèches, mentions 3x + 4x + 4x = 11 segments; longueurs inconnues, pas de métré.',
'EX1/EX7 et issues ER séparés : existants à relocaliser. EX3 existants distingués.',
'* Commande M, charge du point 1mm et interface IC : spécifications à confirmer.',
'Les traits de liaison et extrémités noires des commandes ne sont pas des détecteurs.',
'Ne pas additionner les mêmes appareils aux vues agrandies EX-M-DT01.'],review_zones={'cafeteria':[265,235,550,386],'corridor':[270,380,565,435],'multifonctions':[275,436,445,585],'vestiaires':[450,436,560,585],'noyau':[785,403,1010,600],'mur-ouest':[222,295,320,458],'rangement':[523,238,568,386]})
(ROOT/'evidence/EE-M-RC01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
