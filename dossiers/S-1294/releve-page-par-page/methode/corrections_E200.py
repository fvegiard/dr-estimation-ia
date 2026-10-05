"""Corrections d’ancrage issues des planches source; IDs provisoires initiaux stables."""
def apply(rs):
 def shift(ids,dx=0,dy=0):
  for i in ids:rs[i-1]['x']+=dx;rs[i-1]['y']+=dy
 def put(i,x,y):rs[i-1].update(x=x,y=y)
 shift(range(1,56),-1.5);shift(range(76,90),-3,-5.5);shift(range(90,96),-4);shift([96],-7.1);shift(range(97,177),1)
 for i in range(177,222,3):shift([i],-2);shift([i+1,i+2],-4.2)
 shift(range(222,250),-2.7)
 for i,(x,y) in enumerate([(180,867),(224,867),(224,906),(224,945),(180,1060),(224,1060)],250):put(i,x,y)
 shift([259],5);shift([260],-3);shift([271],5,-4);shift([278],4);shift([279],3);put(280,268,938);shift([281],-2)
 shift([315,316],-6)
 for i,p in enumerate([(244,894),(262,894),(279,879),(272,914),(244,929)],321):put(i,*p)
 for i,p in enumerate([(823,853),(823,880),(823,907)],345):put(i,*p)
 for i,p in enumerate([(232,887),(252,891),(257,939),(257,969),(244,1052)],348):put(i,*p)
 deltas={353:(-3,2),354:(2,3),355:(6,1),356:(3,2),357:(2,0),358:(3,0),370:(1.4,-.9),371:(-3.9,0),372:(1.2,2.7),373:(2.3,2.1),374:(2.8,2.1),375:(2.8,2.1),383:(-1.4,.7),385:(-7.6,1.8),387:(-3.6,2),388:(-.9,2),389:(-6.8,-6.2),390:(18.3,2.3),391:(8.2,1.1),392:(-1.1,1.1),393:(1.2,-.4),394:(-.5,-1.8),396:(7.3,.5),399:(5.2,1.2),401:(1.8,1.4),403:(1.2,8),404:(0,2),406:(9.2,.9),408:(13.2,3.7),409:(8.4,1.8),410:(-4.1,4.6),413:(0,1.8),414:(0,2.7),415:(2.7,1.8),416:(.5,2),419:(.9,-.9),425:(9.2,.7),444:(9.6,1.6),445:(4.8,.9),446:(5,.9),447:(6.8,-.2),448:(4.6,-.2),452:(6.8,.2),456:(1.8,6),457:(6,6),458:(6,6),460:(6,6),461:(6,0),467:(-13,2)}
 for i,(dx,dy) in deltas.items():shift([i],dx,dy)
 put(367,244,904);put(368,262,915);put(398,245,1042);put(405,238,1042)
 put(487,256,930);put(493,260,930);put(504,257,886);put(505,257,930);put(538,264,888);put(543,266,884)
 shift(range(638,644),6);put(644,295,1050);shift(range(645,648),6);put(648,598,1050);shift(range(649,652),6)
 put(669,292,921);put(670,717,921);put(671,537,1058);put(672,544,1058);put(673,1461,921);put(674,1213,1058);put(675,1220,1058)
 # Seconde lecture des locaux électriques, cages et détails centraux.
 positions={425:(869.8,257.8),449:(1566,848.8),450:(1569.7,848.8),451:(1518,871.5),458:(477,994.5),
  477:(870,390.5),478:(891,390.5),494:(537,933.3),496:(1215.5,933.3),
  513:(669,302.5),514:(669,318),515:(685,327.3),516:(695,327.3),520:(669,322.5),521:(695,331.5),
  535:(303,255),540:(303,250.5),545:(244,1065.5),546:(772.5,921.5),547:(788.5,921.5),
  548:(822.5,1065),549:(876.3,1076),550:(899.5,1076),551:(1542,873.5),552:(1567.5,860.5),553:(1562,1009),554:(958,864.7),
  557:(244,1072),558:(297.5,956),559:(779.5,921.8),560:(794.2,928),
  565:(812.5,1065),566:(869.5,1076),567:(892.5,1076),568:(1498.7,940.7),570:(1544,875.8),571:(1568,854.5),
  578:(264.5,951),579:(263,985),580:(202,1075),582:(357,951.2),583:(929.5,915),
  591:(750,927.5),597:(721,887),598:(721,896),599:(721,905),600:(721,913),
  604:(726.5,889),606:(751,850),607:(777,882),614:(1556,935),623:(1558.5,965)}
 for i,p in positions.items():put(i,*p)
 for i,p in {397:(901.5,1066.5),549:(885,1076),566:(880.5,1076),567:(895.1,1076),564:(939,919),568:(1489.1,943),579:(268,994),580:(202,1071),592:(1541,853.3),593:(1550,853.3)}.items():put(i,*p)
 for i in range(522,529):rs[i-1]['x']=1505
 for i,label in {587:'CE01',588:'CE02',589:'CE03',590:'CE04',595:'PP-TEMPORAIRE 1',596:'PP-TEMPORAIRE 2',
  597:'PSU1',598:'PSU1A',599:'PS1A',600:'PP1A',601:'TX6',602:'TX5',603:'TX4',604:'TX-PSU1',605:'CM06',606:'CM05',607:'CM04',
  608:'CM03',609:'CM02',610:'CM01',611:'PPU',612:'PPU2',613:'PPU1',614:'PS1',615:'PP1',616:'ATS-2',617:'ATS-1',
  618:'TX3',619:'TX2',620:'TX1',621:'TX-PS1'}.items():rs[i-1]['label']=label
 rs[590].update(family='Renvoi alimentation pompes',label='POMPE 1&2 — circuits PPU2-1,3,5',x=792,y=942,quantity=1,scope='RENVOI DOCUMENTAIRE — NON ADDITIONNABLE',reserve='Une référence d’alimentation vers le sectionneur du local M01; pas une quantité de pompes implantées. Ne pas additionner au schéma.')
 for i,label in enumerate(['A05','A04','A08','A09','A06','A07','A03','A01','A02'],578):rs[i-1]['label']=label+' — 50 kW inscrit'
 # Le candidat initial 459 est un klaxon de colonne, pas une prise : suppression après examen.
 for i,r in enumerate(rs,1):r['initial_id']=f'E200-{i:04d}'
 rs[:]=[r for i,r in enumerate(rs,1) if i not in [441,459,468,505,507,508]]
 rs.append(dict(family='Batterie 2 phares',label='Ensemble batterie M01, deux phares inclus',x=749.5,y=926.5,quantity=1,parent='Sous-sol M01',radius=3.2,reserve='Capacité 144/320 W contradictoire dans E100; ne pas arbitrer. Aucun ajout des phares inclus.'))
 for f,l,x,y in [('Volet coupe-feu','VCF',677.5,304),('Volet coupe-feu','VCF',681.5,314),('Volet coupe-feu','VCF',686,321),('Volet coupe-feu','VCF',695,321),
  ('Volet coupe-feu','VCF',818.9,228),('Volet coupe-feu','VCF',818.9,237),('Volet coupe-feu','VCF',835.8,248.2),
  ('Détection en gaine','Photoélectrique associé VCF',675.3,298.5),('Détection en gaine','Photoélectrique associé VCF',675.3,318.3),
  ('Détection en gaine','Photoélectrique associé VCF',679.5,324),('Détection en gaine','Photoélectrique associé VCF',698.5,324)]:
  rs.append(dict(family=f,label=l,x=x,y=y,quantity=1,parent='RDC',radius=2.7,reserve='Renvoi de coordination mécanique/incendie; non additionnable au schéma.' if f!='Plinthe commune' else 'Puissance inscrite au plan; circuit PP1A-5.'))
