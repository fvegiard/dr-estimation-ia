"""Reprise E300/E301 : données transcrites des pixels, rendu existant conservé."""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).parent))
import render_sheet
render_sheet.FONT='C:/Windows/Fonts/arial.ttf'

def rec(family,label,x,y,quantity=1,scope='Instance au plan',reserve='',parent='',**kw):
    return dict(family=family,label=label,x=x,y=y,quantity=quantity,scope=scope,reserve=reserve,parent=parent,**kw)

r=[]
details=[
 ('Canalisation non armée','01-1110 rév. B — configurations générales; conduits bétonnés',250,478,'Diamètres intérieurs 50/75/100/115 mm; recouvrement 750 mm min. Tableau de variantes : aucune variante comptée comme installation.'),
 ('Canalisation armée','01-1120 rév. B — configurations générales; conduits bétonnés armés',554,478,'Armature 15M, acier 400 MPa; cales 3000 mm. Divergence : 6 conduits 100 mm (3 × 2) = 625 × 455 mm ici, contre 550 × 405 mm E300. Cette dernière dimension correspond à 75 mm dans ce tableau. Clarification technique requise, sans arbitrage.'),
 ('Arrêt de conduits','01-1310 rév. E — arrêt de conduits',858,478,'Barres : 2 pour 3 conduits ou moins, 4 pour 4 à 9, 6 pour 10 et plus. Plaque acier seulement pour arrêt remblayé futur; pas de quantité projet déduite.'),
 ('Nettoyage / mandrinage','01-1510 rév. D — nettoyage et vérification des conduits',1150,478,'Filin polypropylène 6 mm min.; mandrin et brosse suivant diamètre. Opération reprise au tableau E300, ne pas ajouter une installation.'),
 ('Socle — vue en plan','03-3120 rév. G — page 1/3',253,935,'Socle préfabriqué; 1900 × 1900 mm; cavité 1350 × 450 mm. Conduits selon projet, dessins génériques non cumulables.'),
 ('Socle — coupe B-B','03-3120 rév. G — page 2/3',555,935,'Même socle que la vue en plan. Coudes BT/MT illustratifs; drainage à coordonner, aucune longueur mesurée.'),
 ('Socle — ancrages','03-3120 rév. G — page 3/3',857,935,'Même socle. Détail : 8 boulons et chevilles pour fixation des barres; 4 barres 15M de 1580 mm; 4 ancrages de contreplaqué. Prescriptions par socle, pas de quantité supplémentaire de socles.'),
 ('Bollard — détail type','03-3425 rév. A — circulation lourde',1157,935,'Acier galvanisé diamètre 150 mm, paroi 6 mm min.; 1500 mm hors sol / 1500 mm enfoui, coffrage diamètre 400 mm. Quantité implantée relevée en E300.'),
 ('Mise à la terre — type','03-3610 rév. A — installation pour un socle',1462,935,'4 piquets acier cuivré 19 × 3000 mm reliés; ceinture à 1000 mm du socle et profondeur 300 mm. Même ensemble que E300, non additionnable.')]
for f,l,x,y,n in details:
    r.append(rec(f,l,x,y,scope='1 référence documentaire — NON ADDITIONNABLE',reserve=n,parent='Détail H.Q. — pas un appareil supplémentaire',radius=6))
data=dict(page=21,title='DÉTAILS H.Q. — NEUF RÉFÉRENCES CONTRÔLÉES',type='details',scope='DÉTAILS TYPES — AUCUN TOTAL D’APPAREILS',records=r,notes=[
 'Une pastille = une référence documentaire. Les trois vues 03-3120 décrivent le même socle.',
 'Les tableaux de variantes et vues en coupe ne créent aucune quantité d’installation.',
 'Les quantités du projet sont portées par E300; prescriptions détaillées dans le CSV.',
 'Lecture du dessin émis au dossier; actualité normative et approbation H.Q. non certifiées.'])
(ROOT/'audit/E301-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
render_sheet.render('E301')

r=[rec('Socle transformateur','Socle préfabriqué TSS, 1900 × 1900 mm',901,211,reserve='Une seule installation représentée aux vues 1, 2 et 3. Référence 03-3120 en E301, non additionnable.',parent='TSS'),
 rec('Groupe électrogène','Groupe sur dalle béton',603,554,reserve='Instance du groupe des schémas : ne pas additionner E102/E107. Dalle par entrepreneur général; puissance non indiquée sur E300.',parent='Génératrice',radius=3),
 rec('Poteau H.Q. neuf','NOUV. POTEAU H.Q.',1585.5,175,reserve='Ne pas compter les poteaux existants ni les renvois LAS comme poteaux neufs supplémentaires. Fourniture/portée à coordonner avec H.Q.',parent='Réseau'),
 rec('Conduits MT','4 conduits PVC DB2 75 mm — poteau vers TSS',1360,263,quantity=4,scope='4 conduits dans un massif, longueur source approximative 20 m',reserve='20 m lu au tableau de mandrinage; longueur réelle vide. Ne pas additionner la coupe 4 conduits.',parent='MT'),
 rec('Conduits BT','6 conduits PVC DB2 100 mm — TSS vers cabinet',1340,193,quantity=6,scope='6 conduits dans un massif, longueur source approximative 15 m',reserve='Conduits : environ 15 m au tableau, longueur réelle vide. Câbles BT : note de test pour plus de 15 m et dépassement 2 m du socle (N6); grandeurs distinctes, aucune incompatibilité démontrée. Massif : divergence E300/E301, voir coupe 6.',parent='BT'),
 rec('Conduits télécom','2 nouveaux conduits 75 mm',1439,103,quantity=2,scope='2 conduits — longueur non cotée',reserve='Longueur non déduite de l’échelle. Groupe ancré au symbole TC, couvre ensemble TC/TV; coupe non additionnable.',parent='Télécom'),
 rec('Ceinture équipotentielle','Ceinture continue, soudures aluminothermiques',817,255,reserve='Prescriptions N1/N2 : à 1 m du socle, profondeur 300 mm; longueur non métrée. Même ensemble que E301.',parent='TSS'),
 rec('Tige de terre H.Q.','Tige installée par H.Q., repère détaillé',1522,329,scope='Fourniture H.Q. — distinct des piquets du socle',reserve='Repère dans le détail de liaison aérienne; dimensions non indiquées localement.',parent='Poteau H.Q.')]
for x,y in [(903.4,124.8),(851.5,174.1),(800,222.5),(849.2,274.2),(898.1,325.8),(949.3,278.1),(1001.2,229.2)]:
    r.append(rec('Bollard TSS','Bollard de protection, renvoi A3',x,y,parent='TSS',reserve='Sept positions distinctes vues dans le détail 3; ne pas ajouter leurs reprises dans les autres vues. Détail E301 03-3425.'))
for x,y in [(3458*1920/10799,3139*1920/10799),(3433*1920/10799,3164*1920/10799),(605,567)]:
    r.append(rec('Bollard génératrice','Bollard pointé au plan d’implantation',x,y,parent='Génératrice',reserve='Trois cercles pointés visibles; détail de fondation et répartition contractuelle à coordonner.',radius=2.2))
for x,y in [(904.5,112.7),(787.5,223),(1014,229),(897.4,338.7)]:
    r.append(rec('Piquet de terre TSS','Point de la ceinture; 19 × 3000 mm suivant E301',x,y,parent='TSS',reserve='Quatre points de ceinture au détail 3, confirmés par 03-3610; une seule série, non cumulable avec E301.',radius=2.5))
for f,l,x,y in [('Coupe type 6 conduits','6 conduits de 100 mm, massif 550 × 405 mm',1080,850),('Coupe type 4 conduits','4 conduits de 75 mm, massif 415 × 405 mm',1066,1130),('Coupe type 2 conduits','2 conduits de 75 mm, massif 285 × 405 mm',1439,1130)]:
    r.append(rec(f,l,x,y,scope='Référence dimensionnelle — NON ADDITIONNABLE',reserve='Dimensions lues; recouvrement 750 mm min., ruban, sable et armature prescrits. Aucun volume ni longueur calculé.',parent='Renvoi aux conduits déjà relevés'))
    if f=='Coupe type 6 conduits':r[-1]['reserve']+=' Divergence : E300 indique 550 × 405 mm pour 6 × 100 mm; tableau armé 01-1120 B E301 indique 625 × 455 mm. 550 × 405 mm correspond à 6 × 75 mm dans ce tableau. Clarification technique requise.'
data=dict(page=20,title='IMPLANTATION TSS — PORTÉES ET DOUBLONS DISTINGUÉS',type='equipment',scope='QUANTITÉS SOURCÉES; RÉSERVES D’INTERFACE',records=r,notes=[
 'Les vues 1, 2 et 3 représentent la même installation; les coupes types ne sont pas des tronçons supplémentaires.',
 'TSS : 7 bollards et 4 piquets; génératrice : 3 bollards visibles. Pastilles = positions, CSV = quantités et portée.',
 'Conduits : 4 MT (20 m approx.), 6 BT (15 m approx.), 2 télécom (longueur non cotée). Longueurs réelles vides.',
 'BT : conduits environ 15 m; câbles >15 m visés par la note de test, dépassement 2 m (N6). Grandeurs distinctes.',
 'Massif 6 × 100 mm : 550 × 405 E300 contre 625 × 455 au tableau armé E301. Divergence à clarifier.',
 'Génératrice et socle repris aux schémas/détails : aucune addition entre feuilles. Câbles et volumes non métrés.'])
(ROOT/'audit/E300-records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
render_sheet.render('E300')
