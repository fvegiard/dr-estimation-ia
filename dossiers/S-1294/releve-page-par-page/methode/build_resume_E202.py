import json,sys
from pathlib import Path
D=Path(__file__).resolve().parents[1];W=D.parents[3];sys.path.insert(0,str(Path(__file__).parent))
import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'
rs=[]
def add(f,l,x,y,p='',r='',**kw):rs.append(dict(family=f,label=l,x=x,y=y,quantity=1,parent=p,scope='INSTANCE AU PLAN — NON CUMULABLE AVEC SCHÉMAS/TYPES',reserve=r,radius=2.7,**kw))
cs=json.loads((W/'evidence/E202-candidates/candidates.json').read_text('utf-8'))
H=[4,5,6,9,10,11,12]+list(range(17,32))+[33,34,35,36,37,39,41,42,44,45,48]
F=[1,2,5,6,10,11,12,13,16,20,34,39]
for c in cs:
 f=c['family'];i=int(c['candidate_id'].rsplit('-',1)[1]);x,y=c['x'],c['y']
 if f=='Condenseur':add('Condenseur logement','Condenseur condo (typ.)',x-1.3,y,'Toiture','Fourniture mécanique; même appareil que les renvois des logements types. Tension et puissance non inscrites localement.')
 elif f=='Sectionneur30':add('Sectionneur 30 A 2P','30A-2P, E.I.',x-.4,y,'Toiture','Calibre du sectionneur, pas du disjoncteur; fusibles non indiqués.',ampere=30,poles=2)
 elif f=='LuminaireH' and i in H:add('Luminaire H','H, réf. E108',x,y,'4e étage','Choix fabricant et variation selon cédule; aucun cumul avec schémas.')
 elif f=='Fumee' and i in F:add('Détecteur fumée','Photoélectrique, adresse sur source',x,y,'4e étage','Même boucle incendie que schéma; non additionnable.')
 elif f=='OS3':add('Présence OS3','OS3',x,y,'4e étage')
 else:continue
 rs[-1]['source_candidate']=c['candidate_id']
def many(f,l,pts,p='4e étage',r=''):
 for x,y in pts:add(f,l,x,y,p,r)
many('Luminaire H','H, réf. E108',[(852.3,870.3),(852.3,925.7),(780,954),(825,954)])
many('Détecteur fumée','Photoélectrique, adresse sur source',[(285,906),(914,901),(1460,906),(803,959),(949,958)],r='Non additionnable au schéma incendie.')
many('Luminaire E','E, réf. E108',[(290,860),(290,910),(917,857),(917,906),(1460,861),(1460,910)],'Cages escaliers')
many('Présence OS3','OS3',[(871,877),(872,942),(961,958),(1060,954),(1206,954),(1338,954),(1478,954)])
many('Contrôleur DP2','DP2',[(424,950),(874,881),(1053,957)])
many('Prise toiture DDFT','E.I., circuit PS1A-5',[(207,257),(415,257),(685,257),(887,270),(300,339),(477,335),(722,354)],'PS1A','Protection DDFT selon symbole E100; calibre non assimilé au numéro de circuit.')
many('Prise toiture DDFT','E.I., circuit PS1-3',[(1071,257),(1321,257),(1541,257),(1031,357),(1125,352),(1293,318),(1455,328)],'PS1','Protection DDFT selon symbole E100; tension PS1 contradictoire entre E102 et E105, à clarifier.')
many('Unité apport air frais','UAC01, PP1-38,40,42',[(902,287)],'PP1','Fourniture mécanique; caractéristiques aux cédules, aucune puissance déduite de l’image.')
many('Sectionneur UAC01','E.I., PP1-38,40,42',[(873,289)],'PP1','Calibre non inscrit localement; ne pas déduire 30A des condenseurs voisins.')
many('Détection gaine','B1-139',[(882,289)],'UAC01','Détecteur en gaine distinct du module relais; non additionnable au schéma.')
many('Module relais MRA','B1-140',[(911,289)],'UAC01','Une instance source; caractéristiques suivant E100.')
many('Évaporateur logement','Évaporateur représenté à l’étage',[(203,869),(423,867),(434,867),(674,877),(685,877),(240,1008),(349,1029),(445,1029),(559,1031),(570,1031),(629,1031),(779,1031),(1062,867),(1073,867),(1327,867),(1338,867),(1543,869),(1029,1031),(1080,1031),(1169,1031),(1278,1026),(1289,1026),(1400,1031),(1502,1008)],'Logements 4e étage','Même appareil que sur plans types; fourniture mécanique. Aucun multiplicateur des quantités des types appliqué.')
many('Prise double','Prise, circuit selon cartouche de zone',[(311,949),(411,949),(511,949),(611,949),(713,949),(798,949),(892,853),(843,919),(820,930),(930,935),(949,949),(1046,949),(1146,949),(1246,949),(1346,949),(1443,949),(303,906),(921,918),(1451,907)],r='Variante selon symbole; circuit de zone et tension à réconcilier avec les cédules.')
many('Thermostat ligne','T carré',[(290,922),(916,918),(1460,916)])
many('Thermostat','T rond',[(294,931),(844,914),(778,961),(972,961),(1450,949)])
many('Gradateur SW1','SW1',[(300,931),(1453,931)])
many('Plinthe commune 750 W','750W inscrit',[(291,853),(852,850),(917,850),(1460,853)])
many('Plinthe commune 1750 W','1750W inscrit',[(875,850)])
many('Plinthe commune 1250 W','1250W inscrit',[(835,970),(858,970),(882,970),(906,970),(931,970)])
many('Plinthe commune 2000 W','2000W inscrit',[(327,945),(473,945),(618,945),(763,945),(1010,945),(1110,945),(1228,945),(1380,945)])
many('Relais chauffage','R',[(325,947),(755,947),(998,947),(1363,947),(859,853),(865,964),(908,964)])
many('Indicateur de sortie','Sortie',[(277,952),(872,963),(881,963),(908,927),(1490,954)],r='Sens et faces éclairées conservés dans le plan; deux symboles centraux contigus, ne pas fusionner sans clarification.')
many('Station manuelle','F',[(289,931),(822,970),(915,925),(929,940),(1460,930)],r='Portée incendie non additionnable au schéma.')
many('Klaxon','K',[(289,935),(651,949),(822,966),(1030,949),(1460,934)],r='BA10-2/BA12-2 suivant source; ne pas ajouter des strobes non dessinés.')
many('Module surveillance double','Mx2',[(294,917),(921,913),(1459,922),(833,934)],r='Note A et note2 : raccordements mécaniques; capteurs séparés, sans doublon schéma.')
many('Débit mécanique','Symbole débit, raccordement',[(303,922),(931,918),(1451,924)],r='Fourniture mécanique; raccordement seulement.')
many('Soupape mécanique','Contact soupape',[(303,918),(931,914),(1451,920)],r='Fourniture mécanique; raccordement seulement.')
many('Module isolateur','ISO',[(812,949),(822,953),(939,949),(939,954),(927,954)],r='Désignation ISO lue; modèle non précisé localement.')
many('Module RM','RM',[(813,955),(821,961),(934,955),(927,963)],r='Désignation RM conservée; rôle précis à confirmer avec système incendie/quincaillerie.')
many('Module relais MRA','MRA',[(807,959),(941,959),(833,939)],r='Renvois de fermeture incendie et coordination mécanique; non cumulable au schéma.')
many('Boîtier quincaillerie','B',[(810,966),(935,966)],r='Note B : alimentation quincaillerie électrifiée; référence de groupe, ne pas ajouter aux appareils du détail.')
many('Détection gaine','Détecteur dessiné près VCF',[(838,920)],r='Renvoi note1; non additionnable à MRA/Mx2.')
many('Volet coupe-feu','VCF',[(833,916)],r='Fourniture mécanique; raccordement, fermeture incendie et coordination prescrits.')
many('Boîte jonction','PSU1A-41, carré X',[(833,927)],r='Symbole source; aucun circuit supplémentaire créé.')
from corrections_E202 import apply
apply(rs,W)
data=dict(page=15,title='QUATRIÈME ÉTAGE ET TOITURE',type='equipment',scope='IMPLANTATIONS ET RENVOIS — SANS DOUBLE COMPTAGE',records=rs,notes=[
'Toiture : 72 condenseurs et 72 sectionneurs 30 A 2P inspectés individuellement. Calibre sectionneur ≠ disjoncteur.',
'Les 24 évaporateurs de l’étage sont repris aux types E203 à E206 : quantités non additionnables entre feuilles.',
'Les câbles résistants au feu 2h des montées sont prescrits par la note; aucune longueur ni quantité non dessinée déduite.',
'Appareils incendie, boucles BA et boîtiers de quincaillerie : renvois au système commun, sans addition aux schémas.',
'Tension PS1 et Icc PP1 : réserves interfeuilles à clarifier. Équipements mécaniques : raccordement selon portée.',
'Câbles/conduits non métrés; aucun QPL consulté. E201 exclue de cette reprise.'])
(D/'audit/E202-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8');render_sheet.render('E202')
