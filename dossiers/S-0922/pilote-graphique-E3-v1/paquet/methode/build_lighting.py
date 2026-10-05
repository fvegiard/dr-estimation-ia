"""Record E-3 symbols individually from inspected source zones."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
if ROOT.name == 'methode':
    ROOT = ROOT.parent
(ROOT / 'data').mkdir(parents=True, exist_ok=True)

families={'A':'Cylindre 4 po Lithonia LDN4CYL','B':'Projecteur Juno R612L, 37 W','C':'Encastré orientable Gotham Incito 6 po','G':'Linéaire Signify Fluxstream','IS':'Indicateur de sortie','PD':'Paire de phares d’urgence','BAT':'Batterie avec deux phares','EU':'Phare d’urgence encastré','I':'Interrupteur unipolaire','MS':'Interrupteur maître (renvoi E-2)','AL':'Raccordement de rail'}
models={'A':'LITHONIA LIGHTING LDN4CYL CYLINDER 4"','B':'JUNO TRAC-LITES 37W LED CYLINDER R612L SERIES','C':'GOTHAM AIMABLE RECESSED CAN 6" INCITO ADJUSTABLE','G':'SIGNIFY LINEAR FLUXSTREAM LED STRIP','IS':'STANPRO RMEA0WHUDC','PD':'STANPRO N2-24V6WLJ','BAT':'STANPRO SLC24250-2N6WLJ','EU':'STANPRO SRC24V6LRWH','I':'LEVITON 1101 selon E-1','MS':'Selon E-1 §3.3 / E-2','AL':'MODÈLE NON PRÉCISÉ'}
markers=[]
def mark(family,x,y,parent='',reserve='',scope='INSTALLER'):
    markers.append(dict(id=f'E-3-{len(markers)+1:03}',family=family,x=x,y=y,parent=parent or 'E-3',model=models[family],reserve=reserve,scope=scope))

# Each row and each position was read on the source; no floor/type multiplier.
for y in [793.2,831.0,868.8,906.7,944.5,982.3,1020.1,1058.0,1095.8,1133.6,1171.4,1209.3]:
    for x in [216.7,254.5,292.3,330.1,595.5,633.3,671.1,708.9]:mark('B',x,y)
for x in [273.4,311.2,349.0,576.6,614.4,652.2]:mark('B',x,752.1)
for y in [752.0,827.9,903.7,979.5,1055.3,1131.1,1206.9]:
    for x in [405.7,443.5,481.3,519.1]:mark('B',x,y)
for x in [311.2,614.4]:mark('A',x,793.2)
for y in [831.0,906.7,982.3,1058.0,1133.6,1209.3]:
    for x in [235.6,311.2,614.4,690.0]:mark('A',x,y)
for x,y in [(782.1,722.2),(819.4,722.2),(867.0,722.2),(782.1,762.5),(819.4,762.5),(867.0,762.5),(780.8,819.1),
            (793.3,1189.0),(856.5,1189.0),(915.0,1184.0),(915.0,1217.0),(782.0,1243.6),(824.8,1243.6),(867.0,1243.6),(915.0,1250.0)]:mark('C',x,y)
for y in [409.0,507.8,616.6,715.5]:mark('G',921.0,y)
mark('G',878,819.1)
for y in [911.1,1006.5,1100.6]:
    for x in [794.9,851.7,908.5]:mark('G',x,y)
for x,y in [(916.8,363.8),(467.0,820.9),(804.4,826.2),(864.0,852.5),(482.1,1268.1),(765.8,1251.3)]:mark('IS',x,y,'EM#1','* Faces et flèches de sortie à confirmer selon orientation du dessin.')
for x,y in [(940,612.7),(402,878),(447.1,878),(705.5,839.8),(402,1143.1),(447.1,1143.1),(705.5,1162.8),(843.4,844)]:mark('PD',x,y,'EM#1')
mark('BAT',839.9,852.8,'EM#1')
for x,y in [(799.7,735),(867.7,735),(789.6,819.2),(811.0,1241.0)]:mark('EU',x,y,'EM#1')
for x,y in [(801.6,784.0),(853.3,784.0),(904.0,852.7)]:mark('I',x,y)
for x,y in [(899.0,852.7),(908.6,852.7)]:mark('MS',x,y,'E-2','',scope='RENVOI_E-2')
for x,y,circuit in [(257.7,745.0,'19'),(676.3,959.2,'15'),(211.2,1227.1,'5'),(259.2,1224.5,'5'),(297.5,1224.5,'7'),(335.3,1224.5,'7'),(410.9,1224.5,'9'),(448.7,1224.5,'11'),(486.5,1224.5,'11'),(524.3,1224.5,'13'),(601.0,1224.5,'15'),(638.8,1224.5,'15'),(676.6,1224.5,'17'),(714.4,1224.5,'17')]:mark('AL',x,y,'P1-'+circuit)

data=dict(title='Éclairage — construction / changement E-1, 22 avril 2024',legend_box=[1130,420,465,610],families=families,markers=markers,notes=[
    '185 luminaires codés : A 26 + B 130 + C 15 + G 14. Chaque symbole a été relevé, sans extrapolation.',
    'Urgence : 6 sorties, 8 paires de phares, 1 batterie à deux phares, 4 phares encastrés. La batterie compte pour un ensemble.',
    'Les raccordements de rails sont distincts des luminaires; aucune longueur de rail ni de câbles n’est déduite.',
    'MS-1 et MS-2 renvoient aux commandes du schéma E-2 : ne pas les additionner.',
    'Éclairage mobilier / bandes DEL : voir E-5, version antérieure en réserve. Aucun luminaire de présentation architecturale ajouté.',
    'RES / * : configuration des sorties à confirmer. Familles et modèles suivant cédules E-2 / E-3.'
],verify_zones={'nw':[160,700,535,985],'ne':[535,700,945,985],'sw':[160,985,535,1298],'se':[535,985,945,1298],'corridor':[890,345,960,748],'center':[360,730,562,1243]})
(ROOT/'data/E-3.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(markers))
