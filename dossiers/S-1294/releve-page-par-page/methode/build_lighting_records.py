"""Transcribe fixture/control schedule references and the sign-control detail."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
r=[]
def add(family,label,x,y,scope,model='',reserve=''):
    r.append(dict(family=family,label=label,x=x,y=y,quantity=1,scope=scope,parent=scope,model=model,reserve=reserve,radius=3))
fixtures=[('A — Rangement sous-sol',168,'STANPRO L2TRV-48-L-P40-Q-3C;120 V;30 W;3967 lm;3500 K;0-10 V'),('B — Local technique',230,'STANPRO L2TRV-48-L-P40-Q-3C;120 V;41 W;5457 lm;3500 K;0-10 V'),('C — Stationnement intérieur',287,'STANPRO L2TRV-48-L-S2-Q-3C;347 V;65/75/90 W;3500/4000/5000 K;0-10 V'),('E — Escalier',343,'STANPRO L2TRV-48-L-P40-Q-3C;120 V;35 W;4170 lm;0-10 V'),('Spot logement',400,'JUNO JPDZ4 DC 1000LM CWH;120 V;26 W;2000 lm;3000 K;TRIAC'),('H — Corridor commun',457,'JUNO TC20LED - MVOL EZ10;120 V;14 W;1129 lm;3500 K;0-10 V'),('K — Applique extérieure communs',511,'ACUITY LC6W13LM40K120BG 480CRIGZ1HMBDXX;120 V;12 W;1300 lm;4000 K;0-10 V'),('L — Applique extérieure logements',568,'ACUITY OLLWDLEDP140K 120DDB;120 V;14 W;947 lm;4000 K;0-10 V'),('W — Applique extérieure garage',625,'ACUITY ARC2LEDP440KMVOLT DMGDXXXX;120 V;30 W;3903 lm;4000 K;0-10 V'),('Q — Applique puits ascenseur',682,'ACUITY DMW2L242000ACLMD 120GZ1040K80CRI;120 V;18 W;2536 lm;4000 K;0-10 V'),('Plafonnier chambre',740,'ARTIKAPRO 12FLPR-SP3-WHJ-6PK;120 V;27 W;2000 lm;3000 K;TRIAC'),('Suspension salle à manger',797,'ARTIKA PRO PDT-DEC-BLJ;120 V;27 W;1300 lm;3000 K;TRIAC'),('Encastré extérieur',855,'JUNO WF4ADJSWW5 90CRIMWM6;120 V;10 W;729 lm;4000 K;TRIAC')]
for label,y,model in fixtures:
    reserve='Réglages multiples indiqués : puissance / température de couleur à préciser.' if label.startswith('C —') else ''
    if label.startswith('Spot'):reserve='Référence contient 1000LM, cédule indique 2000 lm; aucun arbitrage.'
    add('Type luminaire',label,894,round(38+y*820/2048,2),'RÉFÉRENCE CÉDULE — PAS UNE QUANTITÉ INSTALLÉE',model,reserve)
controls=[('MIN — Minuterie',235,''),('Interrupteur simple',323,''),('Interrupteur 3 voies',407,''),('Gradateur',488,''),('SW1 — Gradateur bas voltage',570,'NLIGHT NPDODMA WH ou équivalent approuvé'),('OS2 — Présence petit mouvement 360°',651,'NLIGHT NCM PDT 9RJB ou équivalent approuvé'),('OS3 — Présence grand mouvement 360°',732,'NLIGHT NCM PDT 10RJB ou équivalent approuvé'),('DP1 — Relais/contrôleur',823,'NLIGHT NPP16 D EFP 347 ou équivalent approuvé'),('DP2 — Relais/contrôleur',902,'NLIGHT NPP PCD EFP ou équivalent approuvé'),('Interrupteur contrôlé ventilateur',995,''),('DP — Présence petit mouvement 360°',1071,'Double technologie'),('Interrupteur avec présence',1153,'NLIGHT WSXA MWO PDT WH ou équivalent approuvé'),('SW9 — Interrupteur-gradateur',1235,'NLIGHT SPODMRA MWO WH ou équivalent approuvé'),('Contrôle sans fil présence/lumière',1307,'')]
for label,y,model in controls:add('Type contrôle',label,875,round(470+y*506/1804,2),'RÉFÉRENCE TABLEAU — PAS UNE QUANTITÉ INSTALLÉE',model)
for family,x,y in [('Disjoncteur contrôle',882,1062),('Minuterie',906,1083),('Photocellule',937,1105),('Sélecteur trois positions',997,1153),('Contacteur',1076,1162)]:
    add('Détail '+family,family,x,y,'PRINCIPE ENSEIGNE — RENVOI E101',reserve='Calibre non indiqué.' if family=='Disjoncteur contrôle' else '')
data=dict(page=12,title='TYPES ÉCLAIRAGE / CONTRÔLES ET PRINCIPE ENSEIGNE',type='details',scope='27 RÉFÉRENCES + 5 COMPOSANTS DE PRINCIPE',records=r,notes=[
'13 types de luminaires et 14 types de contrôles : références de cédule, aucun nombre installé déduit de ces lignes.',
'Principe enseigne : 5 composants représentés; répétition du détail E101 à ne pas additionner.',
'C : puissances et températures de couleur multiples sans sélection. Spot logement : 1000LM dans référence contre 2000 lm dans colonne.',
'A/B/E : même référence STANPRO et puissances différentes (30/41/35 W), conservées telles quelles. Calibre du disjoncteur non précisé.',
'Couleur au choix architecte/propriétaire. Localisation Q à coordonner. Équivalents approuvés permis pour contrôles nommés.',
'Matrice de séquences : exigences de fonctionnement, pas des quantités. Mise en marche et programmation à inclure; CAT6 de contrôle sous EMT selon note.' ])
(ROOT/'audit/E108-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
