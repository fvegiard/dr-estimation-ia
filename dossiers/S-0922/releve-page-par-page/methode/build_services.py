"""Record E-4 power, auxiliary and existing equipment from inspected symbols."""
import json
from pathlib import Path

families={'PC':'Prise double murale','PQ':'Prise quadruple au plancher','PQC':'Prise quadruple au plafond','PCC':'Prise double au plafond','DATA':'Sortie DATA, implantation dessinée','CDV':'Sortie combinée DATA/voix au plancher','DM':'Déclencheur manuel incendie','AV':'Avertisseur incendie','DG':'Détecteur de fumée en gaine','RA':'Relais incendie','HC':'Aérotherme plafond C75, 7 500 W','HE':'Aérotherme mural E40, 4 000 W','DH':'Serpentin électrique en gaine','TB':'Boîte terminale','PN':'Panneau existant P1 / P2','TR':'Transformateur existant à suspendre','SEC':'Sectionneur existant au plan','BJ':'Boîte de jonction','AC':'Unité de toiture existante','SENS':'Portique dessiné, système Sensormatic','C*':'Repère cerclé C non défini','W*':'Repère cerclé W non défini','TC*':'Repère cerclé TC non défini'}
models={'PC':'15 A / 125 V, 5-15R selon légende E-2','PQ':'15 A / 125 V, 5-15R quadruple selon E-2','PQC':'15 A / 125 V, 5-15R quadruple selon E-2','PCC':'15 A / 125 V, 5-15R selon E-2','HC':'STELPRO / OUELLET DRI/ODS; thermostat intégré','HE':'STELPRO / OUELLET WF/OAC; thermostat intégré'}
markers=[]
def mark(family,x,y,parent='',reserve='',scope='INSTALLER',model=None):
    markers.append(dict(id=f'E-4-{len(markers)+1:03}',family=family,x=x,y=y,parent=parent or 'E-4',model=model or models.get(family,'MODÈLE NON PRÉCISÉ'),reserve=reserve,scope=scope,radius=2.8))

for x,y,circuit in [
    (177,793,'7'),(177,944.7,'7'),(177,1096,'7'),(177,1246,'7'),
    (273.3,712.7,'7'),(388.3,710,'37'),(538,711.3,'35'),(652.3,711.3,'9'),
    (401.3,878,'17'),(432.7,878,'17'),(666.3,878,'13'),(698,878,'13'),
    (401.3,1143.3,'19'),(671.3,1143.3,'15'),(692.7,1143.3,'15'),
    (750,784,'9'),(750,869,'9'),(750,982.3,'11'),(750,1096,'11'),(750,1209.7,'11'),
    (781.3,711.3,'41'),(825,711.3,'41'),(787.9,780,'43'),(850,780,'45'),
    (904,726.3,'47'),(935,784,'47'),(845.7,802.5,'49'),(904,859.3,'2')]:mark('PC',x,y,'P2-'+circuit)
for x in [813.3,876.3,898.7]:mark('PC',x,1189,'P1-47')
for x,y,circuit in [(423,765.3,'1'),(502.3,765.3,'3'),(340.7,935.5,'21'),(564,904.7,'23'),(311.3,1093.7,'27'),(505.3,1162.7,'29'),(307.3,1193.7,'33'),(676,1025,'10'),(573,1085.3,'25'),(611,1170,'31')]:mark('PQ',x,y,'P2-'+circuit)
for x,y,panel,circuit in [(467,789,'P2','5'),(457.7,1153.7,'P2','39'),(467,1223,'P1','23')]:mark('PQC',x,y,panel+'-'+circuit)
mark('PCC',191.7,1284.7,'P1-49')
for x in [771,815]:
    for y in [706,714,722,730]:mark('DATA',x,y)
for x,y in [(458,789),(448.3,1153.7),(458,1223),(392,878),(894.7,855),(894.7,863)]:mark('DATA',x,y)
for x in [414,512]:mark('CDV',x,765.3)
mark('DM',898,367.7)
mark('DM',529.7,1287.9,scope='CONSERVER',model='EXISTANT (EX)')
for x,y in [(417,890),(682,1131),(841.3,843.4),(837.3,1158)]:mark('AV',x,y)
mark('DG',688.7,643)
mark('RA',937.6,871,'Note 1','* Déclenchement shunt-trip du circuit sonore prescrit; circuit et calibre non précisés.')
mark('HE',939.7,387,'P2-30/32')
mark('HC',488.3,1252,'P2-42/44/46')
for x,y,parent in [(811.7,809.5,'DH-01 / P2-14'),(830.3,872.7,'DH-03 / P2-24/26/28'),(809.3,1117.7,'DH-02 / P2-16'),(865,1149,'DH-04 / schéma E-2')]:mark('DH',x,y,parent,'* Puissance et caractéristiques finales à coordonner avec mécanique; aucun calibre déduit de la puissance.')
for x,y,parent in [(823,811.7,'TB-01 / DH-01'),(823,1118.3,'TB-02 / DH-02')]:mark('TB',x,y,parent,'* Alimentée par transformateur du serpentin (note 7); pas un départ supplémentaire supposé.')
for x,y,parent in [(937.4,883.5,'P1'),(937.4,904,'P2')]:mark('PN',x,y,parent,scope='CONSERVER',model='EXISTANT 225 A, 120/208 V selon E-2')
mark('TR',912.4,893.8,'E-2','* Existant à suspendre; position finale à coordonner selon note 10.',scope='MODIFIER',model='112,5 kVA; 600/120/208 V selon E-2')
for x,y in [(937,857.5),(936.7,927.7),(936.7,943.9),(937.7,959.2),(937.7,971.6)]:mark('SEC',x,y,'Distribution existante','* RE : existant à conserver. Calibre absent au plan; correspondance avec les 4 sectionneurs E-2 non établie.',scope='CONSERVER',model='EXISTANT, CALIBRE NON INDIQUÉ')
for x,y in [(835.3,787.3),(888.7,787.3)]:mark('BJ',x,y,'P2-12 / note 11')
mark('BJ',416.7,1273.8,'P2-4 / note 13','* Alimentation Sensormatic à coordonner avec le fournisseur.')
mark('AC',269.5,644,'AC-01 / note 5','* Existant non utilisé; localisation et orientation exactes à déterminer sur place.',scope='À PRÉCISER',model='EX-UC-S9D-1')
mark('AC',766,644,'AC-02 / note 6',scope='CONSERVER',model='EX-UC-S9D-2')
for x in [449,524.7]:mark('SENS',x,1268,'Note 13','* Portique représenté; fourniture et exigences électriques à confirmer avec fournisseur.',scope='À PRÉCISER')
for x,y in [(209,744.3),(409,755),(516.3,755),(703.7,744),(886,707),(938.3,775.3),(805.7,797.3),(458,1082.3),(458,1117.3),(196.3,1265.7),(850,1151.7),(709,1265.7),(719.3,1265.7)]:mark('C*',x,y,reserve='* C cerclé : symbole sans définition dans la légende électrique disponible; fonction et portée à confirmer.',scope='À PRÉCISER')
for x,y in [(462.7,834),(458,1100),(891.3,799.7)]:mark('W*',x,y,reserve='* W cerclé : symbole sans définition dans la légende électrique disponible; fonction et portée à confirmer.',scope='À PRÉCISER')
mark('TC*',487.5,1278,reserve='* TC cerclé : différent de la minuterie TC carrée de E-2; identification à confirmer.',scope='À PRÉCISER')

data=dict(title='Services et incendie — changement E-2 du 29 avril 2024',legend_box=[1120,415,480,845],families=families,markers=markers,notes=[
    'Quantités des symboles dessinés, avec distinction existant / neuf / portée à préciser dans le CSV.',
    'Prises : 31 doubles murales, 10 quadruples plancher, 3 quadruples plafond, 1 double plafond. Une quadruple = un symbole.',
    'DATA : 14 sorties et 2 combinées au plancher. Modèles et terminaison à confirmer; aucune longueur de câble.',
    'P1, P2 et transformateur renvoient au schéma E-2. Ne pas additionner les représentations.',
    'Écart : 5 sectionneurs existants dessinés ici contre 4 au schéma E-2; correspondance et calibres à confirmer.',
    '17 repères C/W/TC cerclés non définis dans la légende électrique : réservés, aucune fonction inventée.',
    'Note 1 : relais incendie vers shunt-trip sonore. Circuit/calibre non identifié à la cédule.',
    'AC-01 : existant non utilisé; AC-02 : existant. Les conduits et supports ne sont pas métrés.',
    'RES / * : source, modèle, position, portée ou réconciliation à confirmer. Aucun calibre choisi arbitrairement.'
],verify_zones={'nw':[160,700,535,985],'ne':[535,700,945,985],'sw':[160,985,535,1298],'se':[535,985,945,1298],'upper':[200,350,960,680],'entrance':[400,1230,550,1320],'panel-room':[876,840,945,985]})
Path('data/E-4.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(len(markers),sum(bool(m['reserve']) for m in markers))
