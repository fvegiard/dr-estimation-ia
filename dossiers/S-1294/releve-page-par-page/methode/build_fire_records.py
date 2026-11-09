"""Transcribe individually inspected symbols in the fire schematic."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=[]
models={'Fumée photoélectrique':'MIRCOM MIX-2251APA','Station manuelle':'MIRCOM MS-401AP','Module isolateur':'MIRCOM M500XA','Module double':'MIRCOM MIX-500DM','Module relais':'MIRCOM MIX-M500RAPA','Klaxon':'MIRCOM FH-400-RR','Klaxon stroboscope':'MIRCOM FHS-400-RR','Panneau incendie':'MIRCOM FX-2000','Annonciateur':'MIRCOM RAX-LCD','Résistance fin de ligne':'MIRCOM MP-300'}
def add(family,points,view,parent,reserve=''):
    x0,y0,scale={'upper':(45,30,2048/885),'lower':(45,380,2048/885),'signal':(965,120,1535/560)}[view]
    for x,y in points:
        records.append(dict(family=family,label=family,x=round(x0+x/scale,2),y=round(y0+y/scale,2),quantity=1,parent=parent,scope='REPRÉSENTATION SCHÉMATIQUE — NON ADDITIONNABLE',model=models.get(family,''),reserve=reserve,radius=2.9))
add('Fumée photoélectrique',[(126,175),(277,175),(424,175),(1530,175),(1834,175),(927,118),(736,188),(836,188),(736,269),(836,269),(576,317),(760,415),(860,415),(760,496),(860,496),(600,544),(424,605),(1834,605),(782,618),(882,618),(782,699),(882,699),(623,746)],'upper','Détection étages')
add('Station manuelle',[(632,188),(932,188),(632,269),(932,269),(656,415),(956,415),(656,496),(956,496),(678,618),(978,618),(678,699),(978,699)],'upper','Détection étages')
add('Module isolateur',[(576,y) for y in [169,209,249,289,338]]+[(600,y) for y in [396,436,476,516,565]]+[(622,y) for y in [598,638,678,718,769]],'upper','Détection étages')
add('Module double',[(455,311),(455,538),(455,738),(1800,283),(1800,542),(1800,750),(1512,544),(1512,744)],'upper','Escaliers')
add('Soupape supervisée',[(375,266),(375,492),(375,693),(1880,237),(1880,498),(1880,707),(1591,498),(1591,696)],'upper','Escaliers','Fourniture mécanique; raccordement électrique seulement.')
add('Détecteur de débit',[(385,309),(385,537),(385,738),(1583,543),(1583,744)],'upper','Escaliers','Fourniture mécanique; raccordement électrique seulement.')
add('Module relais',[(888,151)],'upper','UCA01')
add('Fumée photoélectrique',[(1534,807)],'upper','Escalier 3 — RDC')
add('Fumée photoélectrique',[(808,66),(908,66),(808,147),(908,147),(649,213),(424,298),(1834,298),(864,416),(442,512),(1800,510),(474,612),(1776,612)]+[(x,678) for x in [866,900,934,1071,1105,1139,1173]],'lower','Détection RDC / sous-sol')
add('Station manuelle',[(704,66),(1004,66),(704,147),(1004,147),(479,201),(1800,201),(815,416),(968,678),(1003,678),(1037,678)],'lower','Détection RDC / sous-sol')
add('Module isolateur',[(648,y) for y in [47,87,127,167,248]]+[(x,537) for x in [960,1018,1076,1134,1192,1250,1308]]+[(x,574) for x in [1018,1076,1134,1192]],'lower','Détection RDC / sous-sol')
add('Annonciateur',[(757,201)],'lower','RDC')
add('Panneau incendie',[(1375,575)],'lower','Salle électrique — détection')
add('Module double',[(455,460),(1800,460),(1512,234),(1219,678),(1278,678)],'lower','RDC / sous-sol')
add('Soupape supervisée',[(375,416),(1880,416),(1591,188)],'lower','Escaliers','Fourniture mécanique; raccordement électrique seulement.')
add('Détecteur de débit',[(385,459),(1871,459),(1583,234)],'lower','Escaliers','Fourniture mécanique; raccordement électrique seulement.')
add('Boîtier alimentation',[(x,722) for x in [865,925,985,1045,1105,1165,1225,1285,1345,1405,1465,1525]],'lower','Sous-sol — 12 représentations BA')
for ys,parent in [([110,223,307],'4e étage'),([408,520,604],'3e étage'),([706,818,902],'2e étage'),([999,1112,1197],'RDC')]:
    add('Klaxon stroboscope',[(x,y) for y in ys[:2] for x in [422,485,587,705,766,867]],'signal',parent+' — exemples logements')
    add('Klaxon',[(x,ys[2]) for x in [455,529,647]],'signal',parent+' — parties communes')
    add('Résistance fin de ligne',[(731,ys[2])],'signal',parent)
add('Klaxon',[(413,1521),(489,1521)],'signal','Sous-sol')
add('Klaxon stroboscope',[(616,1521)],'signal','Sous-sol')
add('Résistance fin de ligne',[(705,1521)],'signal','Sous-sol')
add('Panneau incendie',[(178,1290)],'signal','Signalisation — renvoi du même PAI')
add('Boîtier alimentation',[(x,1249) for x in [269,309,349,388]],'signal','Exemples de branches BA — non additionnables aux 12 BA détection','Schéma partiel : note 12 boîtiers; quatre représentations seulement.')
data=dict(page=10,title='ALARME INCENDIE — DIAGRAMME INDICATIF',type='symbols',scope='SCHÉMA — PLANS D’ÉTAGE PRIORITAIRES',records=records,notes=[
'Un symbole dessiné = une pastille. Les coupures de lignes et flèches ne sont pas extrapolées; légende et raccords de fil non comptés.',
'La note du plan donne priorité aux plans d’étage. Ces représentations ne sont pas des quantités globales de chantier.',
'PAI apparaît deux fois (détection / signalisation) : un renvoi, pas deux panneaux physiques. BA : 12 en détection, 4 exemples en signalisation.',
'Note BA : 12 boîtiers. Les adresses proposées ne constituent pas un nombre supplémentaire de boîtiers. Soupapes et débit : fourniture mécanique.',
'UCA01 : seuls le détecteur et le relais d’alarme sont comptés; organes internes de ventilation non comptés. Tableau de légende exclu des quantités.' ])
(ROOT/'audit/E105-page10-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(len(records))
