"""Sélections des logements types; quantités par type sans multiplicateur projet."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];W=ROOT.parents[3]
sys.path.insert(0,str(Path(__file__).parent))
import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'

rules={16:dict(types=['A','B'],reject={'Plafonnier':[5]},keep={'Téléphone':[1,3,4,5,11,13,20]}),
       17:dict(types=['C','D'],reject={'Plafonnier':[1,7],'TV':[8]},keep={'Thermostat':list(range(1,10)),'Téléphone':[1,5,8,9,14,16,17]}),18:dict(types=['E','F'],reject={},keep={}),19:dict(types=['F inversé','G'],reject={},keep={})}
manual={16:[
 ('Suspension repas','Suspension salle à manger',[(506,425),(1026,470)],''),
 ('Prise sécheuse','30 A, 125/250 V, circuit 11-13',[(463,568),(1166,572)],''),
 ('Prise cuisinière','50 A, 125/250 V, circuit 1-3',[(702,428),(1009,649)],''),
 ('Moteur hotte','Symbole moteur monophasé, circuit 14',[(683,428),(1010,632)],'Fourniture mécanique; raccordement seulement. Ne pas assimiler à un plafonnier.'),
 ('Interrupteur','Mécanisme supplémentaire dans groupe dessiné',[(567,550.5),(1144,459.5),(1294,543.8)],'Type simple/3/4 voies selon indice du dessin; calibre non déduit.'),
 ('Plinthe 1500 W','Plinthe logement, puissance inscrite',[(348,234),(273,454),(275,615),(1224,291),(1349,291)],''),
 ('Plinthe 1000 W','Plinthe porte-patio',[(497,234)],''),
 ('Plinthe 1750 W','Plinthe logement, puissance inscrite',[(648,234)],''),
 ('Plinthe 2000 W','Plinthe porte-patio',[(1048,291)],''),
 ('Convecteur 1000 W','Chauffage salle de bain, 1 kW inscrit',[(480,620),(1322,607)],''),
 ('Évaporateur','Évaporateur, renvoi condenseur au toit',[(451,305),(958,379)],'Fourniture mécanique; ne pas ajouter un condenseur à celui de la toiture E202.'),
 ('Relais chauffage','R',[(451,327),(1142,443)],''),
 ('Klaxon stroboscope 185 cd','185 CD inscrit',[(439,314),(355,394),(441,560),(1268,397),(1281,397)],'Un ensemble klaxon/stroboscope par symbole; ne pas compter ses composantes une seconde fois.'),
 ('Klaxon stroboscope 15 cd','15 CD inscrit',[(461,338),(1144,417)],'Un ensemble; renvoi au réseau incendie, non additionnable au schéma.'),
 ('Boîte de jonction vanité','Carré à diagonales, circuit 12 f',[(614,574),(1317.6,503)],'Symbole de boîte E100. Appareil de vanité non précisé dans E108; aucun modèle inventé.'),
 ('Panneau logement','PL',[(714,626),(1149,596)],'Une instance par logement type; non cumulable avec E104/E400 et les plans d’implantation.'),
 ('Poste intercom','IC',[(708.2,543.8),(1277,655)],''),
 ('Boîtier télécom BELL','BELL',[(639,538),(1206,644)],'Désignation littérale du plan; équipements internes non déduits.'),
 ('Renvoi condenseur','1 — CONDENSEUR NIVEAU TOIT',[(354,152),(1367,152)],'Référence de note uniquement; aucune quantité physique ajoutée à E202.')
]}
manual[17]=[
 ('Suspension repas','Suspension salle à manger',[(644,444),(1176,336)],''),
 ('Prise sécheuse','30 A, 125/250 V, circuit 11-13',[(427,554),(1318,184)],''),
 ('Prise cuisinière','50 A, 125/250 V, circuit 1-3',[(658,623),(1212,152)],''),
 ('Moteur hotte','Symbole moteur monophasé, circuit 14',[(657.67,607.33),(1212.67,168.33)],'Fourniture mécanique; raccordement seulement.'),
 ('Interrupteur','Mécanisme supplémentaire dans groupe dessiné',[(457,434),(319,512)],'Type simple/3/4 voies selon indice du dessin.'),
 ('Interrupteur','S superposé au thermostat',[(381,406)],'Symboles S et T superposés au plan; implantation à clarifier, deux fonctions visibles.'),
 ('Plinthe 1500 W','Puissance inscrite',[(250,263),(379,263),(663,263),(940,236),(978,515),(1276,601),(1407,601)],''),
 ('Plinthe 1000 W','Puissance inscrite',[(486,263)],''),
 ('Plinthe 500 W','Puissance inscrite',[(1134,515),(941,391)],''),
 ('Convecteur 1000 W','Salle de bain, 1 kW inscrit',[(239,629),(1377,263)],''),
 ('Évaporateur','Renvoi au condenseur au toit',[(712,375),(1266,327)],'Fourniture mécanique; non additionnable au condenseur E202.'),
 ('Relais chauffage','R',[(468,427),(1061,328)],''),
 ('Klaxon stroboscope 185 cd','185 CD inscrit',[(319,372),(332,372),(1074,243),(1338,486),(1351,486)],'Un ensemble par symbole; non additionnable au schéma incendie.'),
 ('Klaxon stroboscope 15 cd','15 CD inscrit',[(457,411),(1230,416)],'Un ensemble par symbole.'),
 ('Boîte de jonction vanité','Carré à diagonales, circuit 12 f',[(295,477),(1403,303)],'Symbole E100; modèle appareil vanité non précisé E108.'),
 ('Panneau logement','PL',[(481,550),(1391,213)],'Instance par logement type; non cumulable avec E104/E400.'),
 ('Poste intercom','IC',[(339,628),(1398,148)],''),
 ('Boîtier télécom BELL','BELL',[(408,619),(1394,274)],'Équipements internes non déduits.'),
 ('Luminaire L','Applique extérieure logement L — E108',[(1058,539)],''),
 ('Renvoi condenseur','1 — CONDENSEUR NIVEAU TOIT',[(254,152),(1008,132)],'Référence de note; aucune quantité physique ajoutée à E202.')
]
rules[18].update(reject={'Plafonnier':[1],'Commande':[5]},keep={'Téléphone':[3,11,12,13]})
manual[18]=[
 ('Suspension repas','Suspension salle à manger',[(563,353),(1192.5,363)],''),
 ('Prise sécheuse','30 A, 125/250 V, circuit 11-13',[(319,285),(1014,280)],''),
 ('Prise cuisinière','50 A, 125/250 V, circuit 1-3',[(588,175),(1155,181)],''),
 ('Moteur hotte','Symbole moteur monophasé, circuit 14',[(588,192),(1155,198)],'Fourniture mécanique; raccordement seulement.'),
 ('Interrupteur','Mécanisme supplémentaire dans groupe dessiné',[(482,401),(1123,403),(1322,272)],'Type simple/3/4 voies selon indice du dessin.'),
 ('Plinthe 750 W','Puissance inscrite',[(327,538),(423,538)],''),
 ('Plinthe 1500 W','Puissance inscrite',[(1055,546),(1340,633)],''),
 ('Plinthe 1000 W','Puissance inscrite',[(507,538),(627,514),(1120,513),(1237,545)],''),
 ('Convecteur 1000 W','Salle de bain, 1 kW inscrit',[(378,364),(1403,260)],''),
 ('Évaporateur','Renvoi au condenseur au toit',[(626,421),(1265,438)],'Fourniture mécanique; non additionnable au condenseur E202.'),
 ('Relais chauffage','R',[(494,403.5),(1133,408)],''),
 ('Klaxon stroboscope 185 cd','185 CD inscrit',[(406,404),(1107,451),(1276,485)],'Un ensemble par symbole; non additionnable au schéma incendie.'),
 ('Klaxon stroboscope 15 cd','15 CD inscrit',[(482,425),(1123,420)],'Un ensemble par symbole.'),
 ('Boîte de jonction vanité','Carré à diagonales, circuit 12 f',[(401,270),(1358,295)],'Symbole E100; modèle appareil vanité non précisé E108.'),
 ('Panneau logement','PL',[(367,177),(1045,366)],'Instance par logement type; non cumulable avec E104/E400.'),
 ('Poste intercom','IC',[(412,173),(1035,211)],''),
 ('Boîtier télécom BELL','BELL',[(425,251),(1011,366)],'Équipements internes non déduits.'),
 ('Luminaire L','Applique extérieure logement L — E108',[(471,565),(1239,571)],''),
 ('Renvoi condenseur','1 — CONDENSEUR NIVEAU TOIT',[(315,121),(1030,120)],'Référence de note; aucune quantité physique ajoutée à E202.'),
 ('Prise DDFT 20 A','Symbole E100, circuit 8',[(626,260),(1227,266)],'Protection selon symbole et prescriptions E100.')
]

def build(page):
    key=f'E{page+187}';rule=rules[page];types=rule['types'];rs=[]
    def add(f,label,x,y,reserve='',**kw):
        typ=types[0 if x<850 else 1]
        rs.append(dict(family=f,label=label,x=x,y=y,quantity=1,parent=f'Logement type {typ}',scope=f'PAR LOGEMENT TYPE {typ} — NON MULTIPLIÉ',reserve=reserve,radius=3,**kw))
    cand=json.loads((W/f'evidence/unit-candidates/{page}.json').read_text('utf-8'))
    for c in cand:
        f=c['family'];i=int(c['candidate_id'].rsplit('-',1)[1]);x,y=c['x'],c['y']
        if i in rule['reject'].get(f,[]) or (f in rule['keep'] and i not in rule['keep'][f]):continue
        label=f;res=''
        if f=='Encastré':
            f='Spot logement';label='Cercle à croix débordante — réf. E108';x-=1
            res='JUNO JPDZ4 DC 1000LM CWH : colonne cédule 2000 lm; incohérence de référence conservée.'
        elif f=='Plafonnier':label='Plafonnier chambre — réf. E108'
        elif f=='Avertisseur L':
            f='Avertisseur fumée L';label='L, 120 V, circuit 16'
            res='Note générale : appareil combiné CO/fumée selon adjacence au garage ou gaz; vérifier applicabilité sans ajouter de symbole absent.'
        elif f=='Prise':
            f='Prise selon symbole';label='Point de prise dessiné; variante visible dans la vignette'
            res='Variantes 15/20 A, comptoir/DDFT : conserver le symbole source et les exigences E100. Les circuits numérotés ne sont pas des calibres.'
            if page in [16,17,18,19]:
                sockets={16:([1,5],[16,44],[21,30,55,56],[32,35,45,50]),17:([10,47],[11,44],[5,6,58,59],[13,22,38,46]),18:([43,44],[10,12],[4,5,6,7],[15,21]),19:([46,48],[10,13],[1,2,7,8],[11,12,14,23])}[page]
                if i in sockets[0]:
                    f='Prise balcon';label='Prise extérieure, circuit 22';res='Note E100 : DDFT et couvercle intempéries. Symbole au plan simplifié; confirmer variante 15/20 A au devis.'
                elif i in sockets[1]:
                    f='Prise comptoir DDFT 20 A';label='Symbole E100 5-20R, au-dessus du comptoir';res='Protection DDFT selon symbole et prescriptions E100.'
                elif i in sockets[2]:
                    f='Prise comptoir 20 A';label='Symbole E100 5-20R, au-dessus du comptoir';res='DDFT selon proximité de l’évier et prescriptions E100.'
                elif i in sockets[3]:
                    f='Prise DDFT 20 A';label='Symbole E100 5-20R avec DDFT';res='Protection suivant E100; circuit numéroté distinct du calibre.'
                else:
                    f='Prise double 15 A';label='Symbole E100 5-15R';res='Protection AFCI/DDFT selon prescriptions E100; aucun disjoncteur supplémentaire compté au plan type.'
        elif f=='Commande':
            f='Interrupteur';label='Un mécanisme dessiné';res='Type simple/3/4 voies selon indice du dessin; calibre non déduit.'
        elif f=='Thermostat':f='Thermostat ligne';label='T carré';y-=1.8
        elif f=='Téléphone':f='Sortie téléphone';label='Triangle plein';res='CAT 5e suivant E100; longueur non métrée.'
        elif f=='TV':f='Sortie TV';label='TV';res='RG58/U suivant E100; longueur non métrée.'
        elif f=='Luminaire L':label='Applique extérieure logement L — E108'
        add(f,label,x,y,res)
        rs[-1]['source_candidate']=c['candidate_id']
    for f,l,pts,res in manual[page]:
        for x,y in pts:add(f,l,x,y,res)
    data=dict(page=page,title=f'LOGEMENTS TYPES {types[0].upper()} / {types[1].upper()}',type='equipment',scope='QUANTITÉS PAR TYPE — NON MULTIPLIÉES',records=rs,notes=[
      'Chaque ligne correspond à un symbole inspecté. Parent = logement type; aucun multiplicateur de logements appliqué.',
      'Les plans d’étage, schémas et cédules représentent les mêmes équipements : ne pas additionner leurs quantités.',
      'Les renvois de condenseur ne sont pas des appareils supplémentaires. Toiture et plan type à réconcilier.',
      'Prises : variantes et calibres réservés au symbole/aux prescriptions E100; pas aux numéros de circuits.',
      'Boîtes de vanité et boîtiers BELL : désignation source conservée. Câbles et conduits non métrés.'])
    (ROOT/'audit'/f'{key}-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
    render_sheet.render(key)
rules[19].update(reject={'Plafonnier':[1,2]},keep={'Thermostat':list(range(1,7)),'Téléphone':[3,12,13,14]})
manual[19]=[
 ('Suspension repas','Suspension salle à manger',[(523,360),(1168,327)],''),
 ('Prise sécheuse','30 A, 125/250 V, circuit 11-13',[(710,278),(1348,253)],''),
 ('Prise cuisinière','50 A, 125/250 V, circuit 1-3',[(561,181),(1145,158)],''),
 ('Moteur hotte','Symbole moteur monophasé, circuit 14',[(562.33,196.67),(1146.33,175)],'Fourniture mécanique; raccordement seulement.'),
 ('Interrupteur','Mécanisme supplémentaire dans groupe dessiné',[(395,270),(1263,275),(451,403)],'Type simple/3/4 voies selon indice du dessin.'),
 ('Plinthe 750 W','Puissance inscrite',[(1103,367)],''),
 ('Plinthe 1500 W','Puissance inscrite',[(379,630),(662,542),(1330,520)],''),
 ('Plinthe 1000 W','Puissance inscrite',[(477,541),(594,515),(1153,519)],''),
 ('Convecteur 1000 W','Salle de bain, 1 kW inscrit',[(312,254),(1297,328)],''),
 ('Évaporateur','Renvoi au condenseur au toit',[(450,437),(1373,440)],'Fourniture mécanique; non additionnable au condenseur E202.'),
 ('Relais chauffage','R',[(461,411),(1237,479)],''),
 ('Klaxon stroboscope 185 cd','185 CD inscrit',[(606,448),(1250,418)],'Un ensemble par symbole; non additionnable au schéma incendie.'),
 ('Klaxon stroboscope 15 cd','15 CD inscrit',[(594,407),(1250,347)],'Un ensemble par symbole.'),
 ('Boîte de jonction vanité','Carré à diagonales, circuit 12 f',[(354,292),(1312,230)],'Symbole E100; modèle appareil vanité non précisé E108.'),
 ('Panneau logement','PL',[(668,364),(1341,153)],'Instance par logement type; non cumulable avec E104/E400.'),
 ('Symbole P à clarifier','P dans carré avec triangle plein, mur chambre principale',[(440,460)],'Fonction non identifiée dans la légende E100 consultée. Ne pas assimiler au panneau PL représenté à l’entrée, ni au klaxon K. Symbole source conservé sans modèle ni affectation inventés.'),
 ('Poste intercom','IC',[(678,212),(1293,154)],''),
 ('Boîtier télécom BELL','BELL',[(707,363),(1314,170)],'Équipements internes non déduits.'),
 ('Luminaire L','Applique extérieure logement L — E108',[(693,573),(1347,546)],''),
 ('Renvoi condenseur','1 — CONDENSEUR NIVEAU TOIT',[(355,122),(1120,124)],'Référence de note; aucune quantité physique ajoutée à E202.')
]
for p in map(int,sys.argv[1:] or [16]):build(p)
