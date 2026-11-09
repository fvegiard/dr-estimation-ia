"""Record specification constraints without inventing installed equipment quantities."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
key=sys.argv[1]
settings={
'E001':(1,'CONDITIONS GÉNÉRALES',[
('Index des dessins','23 feuilles électriques; aucune M-, A- ou S- dans la liste.',''),
('Numérotation','Index : E003 page 3, E106 page 10 et E401 page 23; cartouches respectifs E002, E105 et E400.','Conserver les suffixes page, ne pas fusionner les feuilles.'),
('Coordination','Travaux à coordonner avec autres disciplines et fournisseurs de services. Percements et réfections selon portée du devis.',''),
('Mise en marche','Essais électriques, réglages, rapports, formation et documents de fin de chantier sont prescrits; aucun dénombrement par appareil déduit.',''),
('Discordances','Signaler erreurs et omissions à ingénieur; aucun arbitrage des contradictions dans le présent relevé.','')],
['Feuille textuelle : zéro symbole matériel à pastiller. CSV de prescriptions; aucune quantité de chantier ajoutée.',
'Liste E001 : 23 pages électriques. Index E003/E106/E401 différent des cartouches E002/E105/E400 pages 3/10/23.',
'Percements, parasismique, mise en marche, essais, formation et documents de fin de chantier : obligations, pas quantités inventées.']),
'E002-page02':(2,'CONDITIONS TECHNIQUES',[
('LIBRE / ESPACE','LIBRE = circuit non raccordé ou futur avec disjoncteur. ESPACE = circuit non raccordé sans disjoncteur. Sans indication = ESPACE.','Six ESPACE avec calibre sur E105 page 9 : présence de disjoncteur réservée.'),
('Pouvoir de coupure','Minimum 10 kA à 250 V; 22 kA à 600 V; armoire de commutation 35 kA, ou selon indications.','Comparer aux 14 kA des cédules et valeurs E102; aucune valeur choisie.'),
('Verrouillage','Disjoncteurs éclairage secours, sorties, extérieur, éclairage 24 h indépendant et panneau incendie à verrouiller.',''),
('Fabricants panneaux','Cutler-Hammer, Schneider Electric, Siemens; un seul fabricant.','Aucun fabricant unique choisi dans le relevé.'),
('Incendie','Description du système cite MIRCOM FX-2003; capacité minimale 198 points; caractéristiques et essais selon devis.','E100/E105 page10 indiquent FX-2000 : référence à confirmer.'),
('Travaux généraux','Mise à la terre, conduits, conducteurs, boîtes, supports, éclairage et raccordements selon notes; aucune longueur déduite.','')],
['Feuille textuelle : aucune pastille matériel. Les prescriptions sont au CSV; aucune quantité physique ajoutée.',
'LIBRE inclut le disjoncteur; ESPACE et absence d’indication l’excluent. ESPACE avec calibre en cédule demeure une contradiction.',
'Icc : 10 kA / 250 V, 22 kA / 600 V et commutation 35 kA dans le devis; ne pas remplacer arbitrairement les valeurs des cédules.',
'Panneau incendie FX-2003 dans le devis contre FX-2000 aux légendes : réserve de modèle.']),
'E002-page03':(3,'GROUPE ÉLECTROGÈNE ET INTERCOM',[
('Groupe électrogène','154 kW / 193 kVA;347/600 V;3PH;4F;60 Hz;diesel Tier3;réservoir sous-base2930 L;autonomie24 h pleine charge.','E102 indique150 kW; capacité de référence et dimensionnement à confirmer.'),
('Référence groupe','KOHLER150REOZJF ou équivalent Caterpillar/Generac/Cummins/MTU;chauffe-moteur2500 W120 V1PH.','Aucun choix de fabricant fait par le relevé.'),
('Inverseurs','Texte final : « 1-INVERSEUR »200 A et « 2-INVERSEUR »100 A;347/600 V3PH4F;KOHLER KBS-DNTC-0225S ou équivalent.','Préfixes1-/2- : ne pas supposer multiplicateur sans réconciliation avec les trois inverseurs E102.'),
('Capacité inverseur','Paragraphe inverseur cite100 A347/600 V3P4F60Hz;la liste finale cite aussi200 A.','Prescriptions internes divergentes : aucun calibre arbitré.'),
('Intercom','MIRCOM KS;KS-116;KM-P02;KSF-102;KB-102;MA-485;transformateurs PS-3B;stations IS-489F;16 boutons au panneau.','16 boutons n’est pas le nombre de logements; pas de multiplication des stations.'),
('Coordination protection','Étude de sélectivité par fabricant, signature ingénieur et transmission Hydro-Québec prescrites.',''),
('Coordination HQ','Inclure visites et coordination installation selon devis.','')],
['Feuille textuelle, sans symboles matériels : zéro pastille. Prescriptions et caractéristiques au CSV, pas de quantités supplémentaires.',
'Groupe : 154 kW / 193 kVA au devis contre 150 kW sur E102. Réservoir 2930 L; autonomie 24 h; aucun dimensionnement choisi.',
'Inverseurs : paragraphe 100 A, liste finale 200 A et 100 A. Préfixes 1-/2- à réconcilier avec les trois représentations E102.',
'Intercom : références MIRCOM; les 16 boutons mentionnés ne sont pas une quantité de logements ou de stations.',
'Index E001 nomme cette page E003; cartouche E002 conservé dans le nom avec suffixe page03.'])}
page,title,items,notes=settings[key]
records=[dict(family='Prescription',label=label,model=text,quantity='',mark=False,scope='DEVIS — SANS QUANTITÉ AJOUTÉE',parent=key,reserve=reserve) for label,text,reserve in items]
(ROOT/'audit'/f'{key}-records.json').write_text(json.dumps(dict(page=page,title=title,type='details',scope='DEVIS — ZÉRO QUANTITÉ AJOUTÉE',records=records,notes=notes),ensure_ascii=False,indent=2))
