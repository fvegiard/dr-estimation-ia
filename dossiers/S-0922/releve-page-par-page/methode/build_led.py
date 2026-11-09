"""Record E-5 LED drawing segments, without inferring purchase lengths or modules."""
import json
from pathlib import Path

families={'D':'Tronçon DEL D repéré','F':'Section linéaire F dessinée','J':'Section linéaire J dessinée','M':'Section linéaire M dessinée','N*':'Section N sans définition à la cédule','AL':'Point d’alimentation dessiné'}
models={'D':'COLORKINETICS PURESTYLE INTELLIHUE POWERCORE; 4 pi et 1 pi à la cédule',
    'F':'COLORKINETICS VAYA LINEAR LP G2-RGBW 4 pi WALL GRAZING',
    'J':'MARK SLOT 1 RECESSED WALL TUNABLE WHITE',
    'M':'MARK SLOT 2 LED RECESSED LINEAR','N*':'MODÈLE NON PRÉCISÉ','AL':'MODÈLE NON PRÉCISÉ'}
markers=[]
def mark(family,x,y,parent='',extra=''):
    reserve='* Version du 26 janvier 2024 « DO NOT USE FOR CONSTRUCTION »; portée actuelle à confirmer.'
    if family in {'D','F','J','M','N*'}:reserve+=' Tronçon/section au dessin, pas une quantité de modules à acheter; longueurs non métrées.'
    if family=='N*':reserve+=' Repère N absent de la cédule E-5; ne pas remplacer par M.'
    if extra:reserve+=' '+extra
    markers.append(dict(id=f'E-5-{len(markers)+1:03}',family=family,x=x,y=y,parent=parent or 'E-5',model=models[family],scope='À PRÉCISER',reserve=reserve,radius=2.8))

for y in [793.5,831.5,869.25,907,945,982.75,1020.5,1058.5,1096.25,1134,1172,1209.75,1247.5]:mark('D',170,y,'P1-10')
for y in [869.25,907,945,982.75,1020.5,1058.5,1096.25,1134,1172,1209.75]:mark('D',757.5,y,'P1-12')
for x,y in [(273.5,688.5),(311,688.5),(349,688.5),(248,689.5),(231.5,692.25),(216,698.5),(202,707.5),(190,719.25),(180.5,733),(174,748.5),(170.75,764.75)]:mark('D',x,y,'P1-10')
for x,y in [(578.25,688.5),(616,688.5),(653.75,688.5),(679,689.5),(695.75,692.25),(711.25,698.5),(725,707.5),(737.25,719.25),(746.5,733),(753.25,748.5),(756.75,764.75)]:mark('D',x,y,'P1-12')
for x,y in [(198.5,820),(400,717.5),(597,717.5),(726.8,762)]:mark('F',x,y,'P1-25','Sections suivant les joints dessinés et les quatre alimentations; découpage final à confirmer.')
for x,y,parent in [(793,1166.3,'P1-14'),(856.5,1166.3,'P1-14'),(938,1210,'P1-14'),(850,1267.3,'P1-16')]:mark('J',x,y,parent)
for x in [300,620]:mark('M',x,1284.5,'P1-18')
for x,y in [(464,777.5),(464,1231.3)]:mark('N*',x,y,'P1-14 TYPE N à E-2','Réconciliation du circuit 14 : cédule TYPE N, mais alimentations J portent aussi 14(P1) sur E-5.')
for x,y,circuit in [(373.5,690,'10'),(553,690,'12'),(184.3,1261.3,'10'),(742.5,1223.5,'12'),(203,847.5,'25'),(269,712.5,'25'),(572,712.5,'25'),(734.5,765.5,'25'),(199,1296.5,'18'),(545,1296.5,'18'),(767.5,1171.3,'14'),(831.4,1171.3,'14'),(933,1168.7,'14'),(772.2,1261.3,'16')]:mark('AL',x,y,'P1-'+circuit)

data=dict(title='DEL — version antérieure du 26 janvier 2024, en réserve',legend_box=[1120,410,480,625],families=families,markers=markers,notes=[
    'ATTENTION : source estampillée DO NOT USE FOR CONSTRUCTION. Chaque repère demeure en réserve de portée.',
    '45 tronçons D repérés : 13 verticaux ouest, 10 verticaux est, 22 sur la partie supérieure et ses courbes.',
    'Les deux jonctions courbe/droite D sont distinguées selon leur direction et leurs repères; assemblage des modules à confirmer.',
    'F : 4 sections / 4 alimentations dessinées. J : 4 sections. M : 2 sections. N : 2 sections sans modèle défini.',
    'Ces sections ne sont pas des quantités de modules à acheter. Aucun métré ni longueur totale extrapolée.',
    '14 points d’alimentation distincts. Ne pas les ajouter aux disjoncteurs de E-2 ni aux luminaires de E-3.',
    'Contradiction : N absent de la cédule E-5; circuit 14 décrit TYPE N dans E-2 mais marqué sur J dans E-5.',
    'G est hachuré à la cédule E-5 : aucun G ajouté ici; les G sont relevés à E-3. Unistrut non métré.',
    'RES / * : version, modèle, segmentation ou portée à confirmer. Aucun calibre choisi arbitrairement.'
],verify_zones={'nw':[160,700,535,985],'ne':[535,700,945,985],'sw':[160,985,535,1305],'se':[535,985,945,1305],'arc-west':[160,677,410,780],'arc-east':[520,677,770,780],'west':[160,770,205,1290],'east':[737,840,776,1250],'fitting':[755,1155,945,1275]})
Path('data/E-5.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(len(markers))
