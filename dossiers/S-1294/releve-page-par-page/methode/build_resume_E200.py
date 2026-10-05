"""Relevé source E200. Sélections visuelles explicites, portée partielle tant que contrôle non achevé."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[3]
records=[]
def add(family,label,x,y,parent='',reserve='',**kw):
    records.append(dict(family=family,label=label,x=x,y=y,quantity=1,parent=parent,reserve=reserve,**kw))
candidates=json.loads((WORK/'evidence/E200-candidates/candidates.json').read_text('utf-8'))
for r in candidates:
    f=r['family']; x,y=r['x'],r['y']
    if f=='Ext_encastre' and r['candidate_id']!='Ext_encastre-028':
        add('Luminaire extérieur encastré','Symbole noir ovale à ouverture centrale; réf. cédule E108',x,y,'RDC extérieur')
    elif f=='Carre_diagonal':
        add('Carré diagonal à identifier','Symbole vu au commerce',x,y,'RDC commerces','Type absent de la cédule E108; éclairage temporaire prescrit dans ces zones. Ne pas choisir de modèle.')
    elif f=='Batterie':
        add('Batterie 2 phares','Ensemble dessiné, deux phares inclus',x,y-4.2,'RDC commerces','Capacité 144/320 W contradictoire dans la légende E100; ne pas arbitrer.')
    elif f=='Lum_C':
        pass # seconde planche contrôlée ci-dessous, sans cumul
    elif f=='Lum_A':
        add('Luminaire A','A — rangement sous-sol',x,y+6.3,'Sous-sol rangement')
    elif f=='Detect_fumee':
        add('Détecteur de fumée','B1-17',x,y,'Sous-sol vestibule')
more=json.loads((WORK/'evidence/E200-more/candidates.json').read_text('utf-8'))
for r in more:
    x,y=r['x'],r['y']
    if r['family']=='Lum_C' and r['candidate_id'] not in ['Lum_C-010','Lum_C-011','Lum_C-073']:
        floating=y<700 or y>1120
        add('Luminaire C hors emprise' if floating else 'Luminaire C','C — PPU1-'+('2' if y<930 else '4' if y<1000 else '6'),x-3,y,
            'Hors emprise dessinée' if floating else 'Sous-sol garage',
            'Symboles isolés hors emprise : localisation et doublon possible à clarifier; ne pas ajouter aux appareils implantés.' if floating else 'Réglages puissance/température non sélectionnés dans E108.')
    elif r['family']=='Batterie_bas':
        add('Batterie 2 phares','Ensemble dessiné, deux phares inclus',x,y+7.5,'RDC commerces','Capacité 144/320 W contradictoire dans E100.')
        add('Station manuelle','F',x+12.5,y+8.1,'RDC commerces',radius=2.1)
        add('Klaxon','K',x+12.5,y+3.8,'RDC commerces',radius=2.1)
for r in candidates:
    if r['family']=='Batterie':
        add('Station manuelle','F',r['x']+12.5,185.3,'RDC commerces',radius=2.1)
        add('Klaxon','K',r['x']+12.5,189.6,'RDC commerces',radius=2.1)
def many(family,label,points,parent,reserve='',radius=3.2):
    for x,y in points:add(family,label,x,y,parent,reserve,radius=radius)
# Appareils lus sur les zooms E200-centre-rdc-grid / ouest-ss-grid / centre-ss-grid / elec-*-grid.
many('Luminaire A','A',[(184,867),(228,867),(228,906),(228,945),(184,1060),(228,1060),(831.5,1011),(831.5,1038),(831.5,1069),(873,1073),(916,1073)],'Sous-sol')
many('Luminaire B','B',[(736,872),(764,874),(799,870),(737,911),(765,911),(799,910),(1511,857),(1537,858),(1538,885),(1538,906),(1574,859),(1574,887),(1574,913),(1574,940),(1574,968),(1574,991),(1574,1021),(1574,1042),(1574,1067)],'Sous-sol locaux techniques')
many('Luminaire C','C',[(280,938),(1513,933)],'Sous-sol','Réglages puissance/température à déterminer E108.')
many('Luminaire H','H',[(853.3,192.3),(853.3,220.8),(853.3,248.5),(871.5,195),(892.2,195),(871.5,223),(892.2,223),(871.5,251),(892.2,251),(831.5,263.5),(859.3,272),(890.5,272),(921.5,272),(828.3,293),(859.3,293),(890.5,293),(921.5,293),(828.3,320.5),(859.3,320.5),(890.5,320.5),(921.5,320.5),(831.5,346.5),(831.5,364.1),(831.5,381.3),(859.3,346.5),(890.5,346.5),(921.5,346.5),(859.3,364.1),(890.5,364.1),(921.5,364.1),(859.3,381.3),(890.5,381.3),(921.5,381.3)],'RDC espaces communs')
many('Luminaire E','E',[(297,191),(298,247),(918,191),(918,241),(1462,192),(1464,247),(267,895),(284,895),(303,883),(295,914),(267,930),(852,859),(852,886),(852,911),(1468,883),(1485,895),(1477,916),(1507,887),(1507,911)],'Cages escaliers et vestibules')
many('Luminaire K','K',[(277.5,179.5),(303,179.5),(862.7,175),(891.8,175),(821.5,397.5),(848,397.5),(1451,179.5),(1476,179.5)],'RDC accès')
many('Luminaire W','W',[(848,831.5),(865.5,824),(929,824)],'Sous-sol accès rampe')
many('Luminaire Q','Q',[(822,852),(822,879),(822,899)],'Sous-sol cage ascenseur')
many('Indicateur de sortie','Sortie',[(251,888),(271,892),(280,940),(280,969),(267,1051),(837,922),(838,967),(1509,922),(1503,968),(881,265.5),(832,328)],'E200 accès')
many('Détecteur de fumée','Photoélectrique adressable',[(853,212.5),(881.5,219.5),(914,236),(849,294),(912,295),(832.5,371),(864.5,368),(912,351),(267,906),(284,917),(751,881),(1503,894),(1485,912),(1514,861),(1578,881),(1572,956),(1571.5,1029)],'E200')
many('Détection en gaine','DNR dessiné',[(822,225),(826,237)],'RDC','Raccordement et module séparés; pas de quantité déduite des notes.')
many('Détecteur présence OS3','OS3',[(853,231),(882,213),(876,298.5),(830.5,1052)],'E200')
many('Contrôleur DP2','DP2',[(869,297)],'RDC')
many('Gradateur SW1','SW1',[(867,184.5),(822,322),(912,335.5),(844,388),(851,849.5),(1492,894)],'E200')
many('Interrupteur','Symbole interrupteur',[(832.5,270),(827,848),(1501,914),(1541,914),(1576,997),(1578,1005),(825,1003),(882,1069),(890,1069)],'E200','Nombre de mécanismes à confirmer lorsque les symboles se superposent.')
many('Minuterie MI','MI',[(267,1040),(805,927),(842,1001),(870,1069),(903,1069),(1520,866)],'Sous-sol')
many('Thermostat','T',[(159,911.5),(260,1040),(342,929),(866,907),(1500,927),(844,338.8),(844,254.5)],'E200')
many('Thermostat ligne','T carré',[(839,270),(898.5,257.5),(822,355),(1523,850.5),(1588,1025),(812.5,875)],'E200')
many('Thermostat inverse','TA',[(762,927),(1568,941),(1580,1004)],'Sous-sol')
many('Prise double','Prise — variante suivant symbole source',[(277,197),(1451,196),(861,190.5),(867,190.5),(861,256.5),(870,257.5),(906.5,237.5),(931,264.5),(931,325.8),(823,312.8),(844,335),(852,335),(932,336.5),(932,382.7),(821.5,384),(850,381.8),(210,850.5),(161,919),(161,1016.5),(248,958),(248,1036),(737,849.8),(784,881),(827,848),(851,900.5),(815,1009),(815,1057),(1487,899),(1507,900),(1558,847),(1562,847),(1518,866),(1541,915),(1590,923),(1558,995),(1558,1016),(1590,1069)],'E200','Calibre et variante à confirmer lorsqu’aucune étiquette locale ne tranche.')
many('Prise extérieure DDFT','Prise avec couvercle intempéries',[(351,929),(411,990),(531,929),(713,990),(852,934),(1095,933),(975,994),(1275,994),(1395,933),(1520,994),(308,994),(156,172)],'Sous-sol / extérieur','Calibre à valider au symbole et à la cédule; aucun disjoncteur déduit.')
many('Aéroconvecteur mural','Chauffage mural 2 kW',[(303,191),(1477,191)],'RDC cages escaliers')
many('Mini aéroconvecteur','Chauffage plafond 5 kW',[(879.5,191),(832,386)],'RDC vestibules')
many('Aéroconvecteur mural','Chauffage mural',[(861,855.5)],'Sous-sol','Puissance non indiquée près du symbole.')
many('Plinthe commune','750 W',[(847,183.5),(834,253),(919,182)],'RDC')
many('Plinthe commune','1750 W',[(873,390.5),(894,390.5)],'RDC')
many('Plinthe commune','1500 W',[(815,866.5),(1529,848.5),(1577,847),(1585,1032.5)],'Sous-sol')
many('Relais chauffage','R',[(846,186.5)],'RDC')
many('Station manuelle','F',[(277,188.5),(892,185.5),(1451,188.5),(280,930),(849,849.5),(1498,920)],'E200',radius=2.1)
many('Klaxon','K',[(892,190),(822.5,318),(250,1022),(284,930),(408,929),(843,914),(1214,929),(1519,902),(1498,924),(1560,940),(1590,1008.5)],'E200',radius=2.1)
many('Module surveillance double','Mx2',[(294,252.5),(938,247.8),(1458,255.5),(269,886),(283,931),(1486,885.5),(1498,921),(831,305)],'E200','Portée des entrées et capteurs mécaniques à réconcilier avec E105; ne pas additionner au schéma.',radius=2.5)
many('Module relais','MRA',[(882.5,185.5),(833.5,241),(839,260.5),(826,338),(696,299),(696,318),(712,326),(722,326)],'RDC')
many('Module surveillance double','Mx2',[(834,232),(834,237),(839,265.5),(697,323),(722,331),(1512,848.5),(1512,852.5),(1512,856.5),(1512,860.5),(1512,864.5),(1512,868.5),(1512,873.5),(1568,906),(1568,919)],'E200',radius=2.5)
many('Module isolateur','ISO',[(808,303),(827,303),(926,303),(944,303)],'RDC','Module à identifier précisément à la légende incendie.',radius=2.8)
many('Débit mécanique','Débit, fourniture mécanique',[(312,255),(931,251.5),(1451,252),(285,889),(1490,880)],'E200','Raccordement seulement; ne pas additionner aux schémas.')
many('Soupape mécanique','Soupape / contact à raccorder',[(312,252),(931,247.2),(1451,248),(285,885),(1485,879.5)],'E200','Fourniture mécanique; symbole raccordé via Mx2.')
many('Ventilateur','VE',[(249,1065),(779,921.5),(793,921.5),(817,1062),(880,1075),(894,1075),(1544,873.5),(1570,862.5),(1559,1009.5),(952,864)],'Sous-sol','Fourniture mécanique; repères et caractéristiques à contrôler avec mécanique. Pas de calibre supposé.')
many('Sectionneur','Sectionneur dessiné sans calibre local',[(213,862),(198,1057),(249,1072),(303,954),(770,921),(783,927),(788,904),(788,897),(788,891),(954,919),(811,1061),(875,1075),(889,1075),(1506,941),(1547,930),(1546,876),(1570,852),(1517,984),(1538,1009),(1512,1051),(1512,1060),(1512,1069),(1512,1076)],'Sous-sol','Calibre, fusibles et pôles non choisis; confronter aux cédules et schémas.')
many('Aérotherme','50 kW inscrit',[(284,951),(284,987),(214,1068),(206,856),(356,943),(946,915),(1457,934),(1550,934),(1547,988)],'Sous-sol','Repères A01 à A09; distinguer chauffage temporaire et permanent suivant prescriptions.')
many('Chauffe-eau','CE01 à CE04',[(1559,1049),(1559,1059),(1559,1068),(1559,1076)],'Sous-sol M05','Fourniture mécanique; ne pas additionner aux schémas.')
many('Pompe','Pompe 1/2 ou P07',[(899,863),(1541,851),(1550,851),(1559,1043)],'Sous-sol','Alimentation à raccorder; quantité de groupes représentés seulement.')
many('Panneau','Panneau temporaire',[(811,380),(942,374)],'RDC','Deux repères distincts PP-TEMPORAIRE 1/2. Ne pas assimiler aux panneaux permanents.')
many('Panneau','PSU1 / PSU1A / PS1A / PP1A',[(721,888),(721,897),(721,905),(721,914)],'Sous-sol M01','Instances au plan; renvoi aux appareils du schéma E102, non additionnables.')
many('Transformateur','TX6 / TX5 / TX4 / TX-PSU',[(729,856),(774,856),(774,864),(725,889)],'Sous-sol M01','Instances au plan, non additionnables aux schémas.')
many('Centre mesurage','CM06 / CM05 / CM04',[(722,872),(751,848),(783,882)],'Sous-sol M01','Ensembles représentés; emplacements de compteurs non comptés ici.')
many('Centre mesurage','CM03 / CM02 / CM01',[(1557,865),(1591,865),(1591,896)],'Sous-sol M04','Ensembles représentés; emplacements de compteurs non comptés ici.')
many('Panneau','PPU / PPU2 / PPU1 / PS1 / PP1',[(1556,894),(1556,913),(1556,926),(1556,937),(1556,955)],'Sous-sol M04','Instances au plan, non additionnables aux schémas.')
many('Inverseur','ATS2 / ATS1',[(1556,902),(1556,922)],'Sous-sol M04','Renvois E102; ne pas compter deux fois.')
many('Transformateur','TX3 / TX2 / TX1 / TX-PS1',[(1562,882),(1585,884),(1585,916),(1560,933)],'Sous-sol M04','Instances au plan; caractéristiques réservées aux schémas/cédules.')
many('Panneau incendie','PAI',[(844,373),(1558,966)],'E200','Deux représentations PAI, un renvoi probable entre niveaux; ne pas déduire deux appareils physiques.')
many('Bloc alimentation incendie','BA',[(769,895),(773,895),(778,895),(769,906),(773,906),(778,906),(1558,974),(1562,974),(1566,974),(1558,984),(1562,984),(1566,984)],'Sous-sol locaux électriques','Renvois aux 12 boîtiers du schéma, sans addition.',radius=2.2)
many('Panneau intercom','PIC',[(822,347)],'RDC')
many('Détection CO/NOx','Panneau de contrôle CO/NOx',[(725,922)],'Sous-sol M01','Sondes et raccordements à coordonner; seuls symboles identifiés comptés.')
# Bornes : une pastille par groupe, jamais une prise de courant ni une quantité de disjoncteurs.
many('Groupe borne double','Deux départs dessinés',[(351,924),(411,924),(471,924),(531,924),(592,924),(652,924),(310,1050),(351,1050),(411,1050),(471,1050),(531,1050),(652,1050),(713,1050),(773,1050),(975,924),(1035,924),(1095,924),(1155,924),(1215,924),(1276,924),(1336,924),(1396,924),(975,1050),(1035,1050),(1095,1050),(1155,1050),(1276,1050),(1336,1050),(1396,1050),(1456,1050),(891,1062)],'Sous-sol','Un groupe dessiné = une ligne. Deux bornes selon note type; contrôleurs DCC9 non déduits de ce nombre.')
many('Groupe borne simple','Un départ dessiné',[(308,922),(704,922),(587,1056),(594,1056),(1444,921),(1201,1056),(1208,1056)],'Sous-sol','Un groupe dessiné; contrôleur DCC9 non ajouté sans repère individuel.')
sys.path.insert(0,str(Path(__file__).parent))
from corrections_E200 import apply
apply(records)
data=dict(page=13,title='SOUS-SOL ET REZ-DE-CHAUSSÉE',type='equipment',
 scope='IMPLANTATIONS ET RENVOIS — REVUE INDÉPENDANTE ATTENDUE',records=records,
 notes=['Quantités de symboles inspectés; familles ambiguës et renvois réservés. Pas de certification exhaustive de soumission.',
 'Un ensemble batterie et deux phares = une unité; aucune addition avec les schémas E102 à E108.',
 'Carrés diagonaux commerces : identification réservée. Aucun modèle ni calibre supposé.',
 '31 groupes doubles et 7 simples de bornes repérés; pas de déduction automatique du nombre de contrôleurs DCC9.',
 'Luminaires C hors emprise : localisation/doublon à clarifier avant total. Renvoi pompes 1&2 : non additionnable.',
 'Câbles et conduits non métrés. Comparaison QPL non effectuée. E201 exclue de cette reprise.'])
(ROOT/'audit/E200-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
sys.path.insert(0,str(Path(__file__).parent))
import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'
render_sheet.render('E200')
