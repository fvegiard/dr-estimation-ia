"""Transcribe visually read schedules; preserve blank spaces and contradictory labels."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SCALE = 10799/1920
records = []
# Names below identify inspection crops, not inferred panel designations.
geometry = {
 'PP1':(70,27,288.5,25.22,765,957),
 'PP1A':(70,310,275.5,25.12,763,953),
 'PS1':(399,28,295.25,25.14,765,957),
 'PS1A':(399,215,273.5,25.1,765,957),
 'PPU':(854,32,285,24.85,762,951),
 'PPU1':(854,191,279.5,25.2,758,949),
 'PPU2':(854,373,278.5,25.2,758,949),
 'PSU1':(1181,191,280.5,25.15,770,960),
 'PSU1A':(1181,373,284.5,25.0,766,954),
}

def add(panel, circuit, amperes, poles, description, reserve='', protection='Non indiquée'):
    bx,by,first,step,left,right=geometry[panel]
    row=(circuit-1)//2
    y=first+step*row
    if panel=='PS1A':
        if row==4:y+=12
        elif row>4:y+=24
    records.append(dict(family=f'{amperes} A {poles}P',label=description,
        parent=panel,circuits='-'.join(str(circuit+2*i) for i in range(poles)),
        ampere=amperes,poles=poles,protection=protection,
        x=bx+(left if circuit%2 else right)/SCALE,y=by+y/SCALE,
        radius=1.8,reserve=reserve))

def singles(panel, start, values, descriptions=None):
    for i,a in enumerate(values):
        description=descriptions[i] if descriptions else 'LIBRE'
        reserve='* Ligne ESPACE avec calibre indiqué : présence du disjoncteur à confirmer.' if description=='ESPACE' else ''
        add(panel,start+2*i,a,1,description,reserve)

# PP1, 84 positions.
add('PP1',1,60,3,'TRANSFO PS1 (TX-PS1)')
for j in range(7):add('PP1',7+6*j,60,3,f'AÉROTHERME {j+1}')
add('PP1',49,20,3,'AÉROTHERMES 8 ET 9')
add('PP1',55,100,3,'ATS-1')
add('PP1',61,15,1,'CHAUFFAGE CAGE ESCALIER #02')
add('PP1',63,100,3,'ATS-2')
add('PP1',69,200,3,'PANNEAU PP-1A')
singles('PP1',75,[15,15],['ESPACE','ESPACE'])
for j in range(4):add('PP1',2+6*j,30,3,f'CHAUFFE-EAU {j+1}')
for c,a,d in [(26,15,'VENTILATEUR VE-10'),(32,60,'ASCENSEUR 1'),(38,60,'UCA-01'),(44,60,'ASCENSEUR 2')]:add('PP1',c,a,3,d)
singles('PP1',50,[20,20,15,15,20,20],['CHAUF. S.GICLEURS/MÉCANIQUE']+['LIBRE']*5)
# PP1A: first two descriptions share one explicitly marked 2P breaker.
add('PP1A',1,15,2,'CHAUFFAGE LOCAL EC-01 : lignes 1 et 3 (1500 W et 5000 W)', '* Deux puissances sur le même départ 15 A 2P; configuration à confirmer.')
singles('PP1A',5,[15,20,20,20,20,20,15,20,15],['CHAUFFAGE LOCAL EC-02','CHAUFFAGE LOCAL EC-04','CHAUFF. CORR. 4E (AILE GAUCHE)','CHAUFFAGE SAS ASC. 4E ÉTAGE 5000 W','CHAUFFAGE SAS ASC. 4E ÉTAGE 2500 W','CHAUFFAGE SAS ASC. 3E ÉTAGE 5000 W','CHAUFFAGE SAS ASC. 3E ÉTAGE 2500 W','CHAUFFAGE SAS ASC. 2E ÉTAGE 4000 W','CHAUFFAGE SAS ASC. 2E ÉTAGE 2500 W'])
singles('PP1A',23,[15,20,20])
singles('PP1A',2,[15,15,15],['CHAUFFAGE CAGE ESCALIER #01','CHAUFFAGE CAGE ESCALIER #03','CHAUFFAGE LOCAL V-05 (S.SOL)'])
add('PP1A',8,60,3,'ASCENSEUR')
singles('PP1A',14,[15,15,15,15])
# PS1 is transcribed literally: its 347/600 V header contradicts E102.
singles('PS1',1,[15,15],['POMPE P-7','PRISES TOIT (AILE DROITE)'])
add('PS1',5,100,3,'PANNEAU PS1A')
singles('PS1',11,[15]*6,['LIBRE']*5+['ESPACE'])
singles('PS1',2,[15]*7,['VENTILATEUR VE-01','VENTILATEUR VE-02','VENTILATEUR VE-03']+['LIBRE']*4)
singles('PS1A',1,[15,15,20,15,15,15],['VENTILATEURS VE11 & VE-12',"PANNEAU D’INTERCOM",'PRISES TOIT (AILE GAUCHE)','VOLET MOTORISÉ','PANNEAU CONTRÔLE VNT. GARAGE','VENTILATEUR VE-09'])
singles('PS1A',13,[20,20,20,15,15])
singles('PS1A',2,[15]*8,['VENTILATEUR VE-04','VENTILATEUR VE-05','VENTILATEUR VE-06','VENTILATEUR VE-07 &08']+['LIBRE']*4)
for c,a,d in [(1,100,'ATS-1 (PPU1)'),(7,100,'ATS-2 (PPU2)'),(13,175,'POMPE INCENDIE')]:add('PPU',c,a,3,d)
singles('PPU',2,[15]*4)
add('PPU1',1,40,3,'TRANSFO PSU1 (TX-PSU1)')
singles('PPU1',7,[20]*9)
singles('PPU1',2,[15]*7,['ÉCLAIRAGE GARAGE']*3+['LIBRE']*4)
for c,d in [(1,'POMPES 1&2'),(7,'POMPES 3&4'),(13,'POMPES 5&6')]:add('PPU2',c,15,3,d)
for c in [2,8]:add('PPU2',c,15,3,'LIBRE')
add('PSU1',1,30,3,'PANNEAU PSU1A')
singles('PSU1',7,[20,20,20,20,20,20,15,15,20,20],['PRISES ESCALIER #2','PRISE CORRIDOR 2E (AILE DROITE)','PRISE CORRIDOR 3E (AILE DROITE)','PRISE CORRIDOR 4E (AILE DROITE)','PRISE LOCAL M-03 (S.SOL)','PRISE LOCAL M-04 (S.SOL)','PRISE VIDÉOTRON','PRISE BELL','PRISE LOCAL M-05 (S.SOL)','PRISES GARAGE'])
singles('PSU1',27,[20]*5)
singles('PSU1',37,[20,15,15],['ESPACE']*3)
right=['PANNEAU ALARME INCENDIE','LIBRE','LIBRE','ÉCLAIRAGE ESCALIER #2','ÉCL. CORRIDOR 2E (AILE DROITE)','ÉCL. CORRIDOR 3E (AILE DROITE)','ÉCL. CORRIDOR 4E (AILE DROITE)','ÉCL. LOCAL M-03 (S.SOL)','ÉCL. LOCAL M-04 (S.SOL)','BATTERIE ÉCL. URG. LOCAL M-04','ÉCL. LOCAL M-05 (S.SOL)','INDICATEUR SORTIE GARAGE','LIBRE','LIBRE','LIBRE','LIBRE']
singles('PSU1',2,[15]*14+[20,20],right)
next(r for r in records if r['parent']=='PSU1' and r['circuits']=='2')['protection']='Cadenassable peint rouge (carré plein source)'
singles('PSU1A',1,[15]*10,['PRISES ESCALIER 1','PRISES ESCALIER 3','PRISE CORRIDOR 2E (AILE GAUCHE)','PRISE CORRIDOR 3E (AILE GAUCHE)','PRISE CORRIDOR 4E (AILE GAUCHE)']+['PRISE SAS ASCENSEUR 4E ÉTAGE (libellé source répété)']*3+['LOCAUX EC-01,C-03 & EC-04 (RDC)','LOCAL EC-02 (RDC)'])
add('PSU1A',21,15,2,'PORTE DE GARAGE')
add('PSU1A',25,40,2,'Ascenseur')
singles('PSU1A',29,[20]*10,['PRISES R-01 (SOUS-SOL)','PRISES M-06 (SOUS-SOL)','PRISES GARAGE','PRISE CAGE ASCENSEUR','POMPE JOCKEY','VOLETS COUPE-FUMÉE RDC','VOLETS COUPE-FUMÉE 2,3,4 ÉTAGE','LIBRE','LIBRE','LIBRE'])
singles('PSU1A',2,[15]*21+[20,20],['ÉCLAIRAGE ESCALIER 1','ÉCLAIRAGE ESCALIER 3','ÉCL. CORRIDOR 2E (AILE GAUCHE)','ÉCL. CORRIDOR 3E (AILE GAUCHE)','ÉCL. CORRIDOR 4E (AILE GAUCHE)','ÉCL. SAS ASCENSEUR 4E ÉTAGE','ÉCL. SAS ASCENSEUR 3E ÉTAGE','ÉCL. SAS ASCENSEUR 2E ÉTAGE','ÉCL. SAS ASCENSEUR S.SOL','ÉCL. LOCAUX M-01 & M-02','BATTERIE ÉCL. LOCAL M-01','ÉCL. LOCAUX M-06,R-52 & R-53','ÉCL. RDC ENTRÉE','INDICATEUR SORTIE GARAGE','ÉCLAIRAGE DESCENTE GARAGE','ÉCLAIRAGE ENTRÉE EXT. RDC','ÉCLAIRAGE CAGE ASCENSEUR','ÉCL. RDC ENTRÉE','ÉCL. RDC ENTRÉE','LIBRE','LIBRE','LIBRE','LIBRE'])
for panel,amp,bx,by,cx,cy in [('PP1',600,70,27,1290,48),('PP1A',200,70,310,1300,40),('PS1A',100,399,215,1300,38)]:
    records.append(dict(family='Principal',label=f'Disjoncteur principal {amp} A',parent=panel,circuits='PRINCIPAL',ampere=amp,poles='',x=bx+cx/SCALE,y=by+cy/SCALE,radius=2.0,reserve='* Nombre de pôles du principal non indiqué; quantité distincte des départs.'))
data=dict(page=9,title='CÉDULES — NEUF PANNEAUX',type='breakers',scope='CÉDULE — UN DISJONCTEUR MULTIPOLAIRE = UN APPAREIL',records=records,
    notes=['Pastilles sur cellules de calibre; une seule pastille par départ multipolaire. LIBRE avec calibre inclus; ESPACE sans calibre exclu.',
           '* ESPACE avec calibre : présence réservée. Principaux isolés des départs; N/A non compté. Un circuit simple occupe une seule position.',
           'Contradictions E102 / cédule : PS1 120/208 V / 347/600 V; PP1 Icc 35 / 14 kA; plusieurs valeurs de barres et Icc diffèrent. Aucun choix arbitraire.',
           'PSU1A : principal N/A mais « 100A » dans la colonne adjacente; PP1A départ 1-3 = 15 A 2P avec deux puissances. À clarifier.'])
(ROOT/'audit/E105-page09-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Schedule records:',len(records))
