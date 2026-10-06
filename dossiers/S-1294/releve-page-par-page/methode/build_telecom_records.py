"""Transcribe telecom and door-detail symbols from inspected crops."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=[]
def add(family,x,y,parent,reserve='',view=None):
    if view:
        x0,y0,scale={'single':(1230,550,1722/395),'double':(1120,910,2004/530)}[view]
        x,y=x0+x/scale,y0+y/scale
    records.append(dict(family=family,label=family,x=round(x,2),y=round(y,2),quantity=1,parent=parent,scope='DÉTAIL / SCHÉMA — NON ADDITIONNABLE',reserve=reserve,radius=2.7))
for y,parent in [(134,'Logement type — 4e'),(231,'Logement type — 3e'),(328,'Logement type — 2e'),(427,'Commerce type — RDC')]:
    for x in [307,324]:add('Prise téléphone P',x,y,parent)
    for x in [341,358]:add('Sortie combinée C',x,y-6,parent,'Désignation C à réconcilier avec légende générale; aucune multiplication par logement.')
    add('Prise courant',410,y+4,parent)
    add('Cabinet BELL',428,y+4,parent)
for y in [133,230,327,425]:add('Boîte répartition Vidéotron',915,y,'Étages / RDC','V2 correspond au câble dans les notes; boîte V figurée sans quantité définitive.')
for fam,x,y in [('Système téléphonique BELL',624,516),('Système câblodistribution',967,516),('Panneau alarme incendie',731,397),('Panneau intercom principal',1085,398),('Gâche électrique',1167,400),('Transformateur T',1105,425),('Prise courant',677,558),('Prise courant',1020,558)]:
    add(fam,x,y,'Schéma général', '2 PU / 4 PU : une représentation de groupe; nombre physique à confirmer.' if fam=='Prise courant' else ('Caractéristiques non indiquées.' if fam=='Transformateur T' else ''))
legend={'RA':'Relais adressable incendie','R':'Retenue magnétique','OP':'Opérateur porte','DR':'Détecteur relâche','P':'Détecteur présence','E':'Contact magnétique / électroaimant','G':'Gâche électrique','LC':'Lecteur carte','BS':'Bouton sortie','BH':'Bouton handicapé','SB':'SB non défini','K':'K non défini','INT':'Intercommunication','F':'Poste manuel incendie'}
def device(code,x,y,view):
    reserve='Symbole absent de la légende de cette feuille.' if code in ['SB','K'] else ('Fourniture architecture; raccordement électrique.' if code in ['OP','P','G','BH'] else '')
    add(legend[code],x,y,'Porte '+('simple' if view=='single' else 'double'),reserve,view)
for x in [367,494]:add('Boîte jonction',x,307,'Porte simple',view='single')
for x in [103,166,389,668,747]:device('RA',x,592,'single')
for code,x,y in [('R',103,683),('OP',461,592),('DR',526,592),('P',598,683),('E',668,683)]:device(code,x,y,'single')
for code,x in zip(['G','LC','BS','BH','SB','K','INT','F'],[747,814,881,948,1015,1082,1149,1217]):device(code,x,1018,'single')
add('Barre panique',470,1018,'Porte simple','Quincaillerie de porte : portée fourniture à confirmer.',view='single')
for x in [767,878]:add('Boîte jonction',x,250,'Porte double',view='double')
for x in [150,785,1028,1109,1166,1224]:device('RA',x,497,'double')
for code,x,y in [('R',150,576),('R',1224,576),('OP',850,497),('DR',905,497),('E',319,576),('P',379,576),('P',968,576),('E',1028,576),('G',692,933)]:device(code,x,y,'double')
for code,x in zip(['LC','BS','BH','SB','K','INT','F'],[1283,1341,1399,1457,1515,1574,1632]):device(code,x,867,'double')
add('Barre panique',860,867,'Porte double','Quincaillerie de porte : portée fourniture à confirmer.',view='double')
add('Transfert courant',1053,934,'Porte double','Fourniture architecture; raccordement électrique.',view='double')
data=dict(page=11,title='TÉLÉCOM ET DISPOSITIFS TYPES DE PORTE',type='details',scope='SCHÉMAS TYPES — AUCUNE MULTIPLICATION',records=records,notes=[
'Quantités : représentations uniquement; voir plans de niveau et logements types pour la quantité physique. Aucun câble ou conduit métré.',
'Portes simple et double : composants dessinés comptés séparément. Légende, charnières et renvois ascenseurs exclus.',
'Quincaillerie fournie par architecture identifiée en réserve; SB et K non définis dans la légende de cette feuille.',
'BELL : installation filerie par spécialiste; conduits par électricien. Vidéotron : point de raccordement, ramifications locales et portée selon notes.',
'Prises des systèmes BELL / Vidéotron marquées une fois par groupe dessiné « 2 PU » / « 4 PU »; pas de quantité physique déduite.',
'Le panneau incendie et les renvois intercom ne doivent pas être additionnés aux représentations des autres feuilles.' ])
(ROOT/'audit/E107-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(len(records))
