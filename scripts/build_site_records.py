"""Trace site objects and keep repeated construction views separate."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=[]
def add(family,label,x,y,parent,reserve='',quantity=1):
 records.append(dict(family=family,label=label,x=x,y=y,parent=parent,quantity=quantity,scope='REPRÉSENTATION — NE PAS ADDITIONNER LES VUES',reserve=reserve,radius=3.2))
def detail(family,label,u,v,reserve=''):
 add(family,label,750+u/4.8485,30+v/4.8485,'Détail 1 du socle',reserve)
for i,(u,v) in enumerate([(772,794),(743,758),(738,826),(704,790),(700,856),(667,819)],1):
 detail('Conduit BT',f'Position {i} — Ø100 mm',u,v)
for name,u,v in [('A',879,982),('B',848,948),('C',814,911),('R',878,912)]:
 detail('Conduit MT',f'Position {name} — Ø75 mm',u,v)
for u,v in [(743,462),(492,699),(244,933),(480,1186),(718,1436),(967,1201),(1217,965)]:
 detail('Bollard','Protection mécanique du socle',u,v,'Sept symboles visibles dans cette vue; confronter au détail HQ et implantation définitive.')
detail('Socle','Socle préfabriqué 1900 × 1900',730,995)
detail('Mise à la terre','Ceinture MALT du socle',400,760,'Tracé de principe; aucune longueur déduite.')
add('Génératrice','Groupe sur dalle de béton',605.6,556.7,'Implantation générale','Même génératrice que E102; puissance contradictoire avec devis. Dalle par entrepreneur général.')
for u,v in [(426,207),(454,184),(486,164)]:
 add('Bollard','Protection de génératrice',530+u/5.624,530+v/5.624,'Implantation générale','Trois positions appelées par les leaders; implantation à confirmer.')
add('Socle','Socle transformateur',572.5,688.8,'Implantation générale','Même socle que détail 1 et extrait 2.')
add('Poteau HQ','Nouveau poteau H.Q.',1586,175,'Extrait 2','Fourniture et limites de travaux à coordonner avec HQ.')
add('Socle','Socle transformateur',1275,348,'Extrait 2','Même socle que vue générale et détail 1.')
for x in [1056,1077,1098]:
 for y in [843,864]:add('Coupe conduit BT','Ø100 mm PVC DB2',x,y,'Coupe 6 conduits')
for x in [1062,1083]:
 for y in [1117,1139]:add('Coupe conduit MT','Ø75 mm PVC DB2',x,y,'Coupe 4 conduits')
for y in [1115,1137]:add('Coupe télécom','Ø75 mm PVC DB2',1435,y,'Coupe 2 conduits')
for label,q,reserve in [('Poteau vers TSS : 4 conduits Ø75 mm; longueur approximative du parcours 20 m',4,'Longueur réelle laissée vide dans le tableau; ne pas assimiler 20 m au total des quatre conduits.'),('TSS vers cabinet : 6 conduits Ø100 mm; parcours approximatif 15 m',6,'Longueur réelle laissée vide; aucune mesure de tracé ajoutée.'),('Deux nouveaux conduits Ø75 mm télécom',2,'Longueur non indiquée; poteau LAS à coordonner.')]:
 records.append(dict(family='Prescription de canalisation',label=label,quantity=q,mark=False,scope='TABLEAU / APPEL — PAS UNE QUANTITÉ ADDITIONNELLE',reserve=reserve))
notes=['Les vues générale, agrandie et détail du socle représentent les mêmes ouvrages : les pastilles comptent des représentations, pas des ouvrages additionnels.', 'Conduits : 4 × Ø75 mm sur parcours approximatif 20 m; 6 × Ø100 mm sur parcours approximatif 15 m. Deux Ø75 mm télécom sans longueur. Aucune longueur réelle complétée.', 'Les coupes de tranchées sont des détails de construction. Poteaux existants, flèches, légende de canalisation, arbres et bâtiments ne sont pas comptés.', 'Les repères numériques et lettres des conduits de l’extrait sont des renvois au détail, pas des conduits supplémentaires. Les poteaux LAS électricité et télécom sont prescrits à coordonner, sans symbole d’ouvrage indépendant certain.', 'Bollards du socle : sept positions visibles dans ce détail; vérifier la disposition définitive et le détail HQ. Génératrice : trois positions appelées, à confirmer. Dalle béton par entrepreneur général.', 'Essai d’isolation BT par HQ au-delà de 15 m; cosses non installées avant essai. Calibres de câbles non déduits.']
(ROOT/'audit/E300-records.json').write_text(json.dumps(dict(page=20,title='IMPLANTATION — TRANSFORMATEUR SUR SOCLE',type='details',scope='OUVRAGES ET DÉTAILS — REPRÉSENTATIONS SÉPARÉES',records=records,notes=notes),ensure_ascii=False,indent=2))
