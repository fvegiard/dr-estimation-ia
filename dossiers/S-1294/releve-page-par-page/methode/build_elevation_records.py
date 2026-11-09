"""Separate architectural elevation tags from actual electrical callouts."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
key=sys.argv[1]
if key=='E400-page22':
 page=22;title='ÉLÉVATIONS AVANT ET ARRIÈRE';records=[]
 notes=['Aucun symbole électrique ni appel de note électrique identifié sur cette page après inspection des quatre zones de façade.',
 'Les cercles F2, F16, P20, P24 et similaires sont des repères de fenêtres/portes du fond architectural; ils ne sont pas des luminaires.',
 'Zéro pastille ne signifie pas absence d’éclairage extérieur au projet. Les plans et logements types portent les autres prescriptions.',
 'Aucune quantité d’appareil déduite des fenêtres, portes, enseignes ou garde-corps. Plan original intégralement conservé.']
 records=[dict(family='Contrôle de portée',label=notes[0],quantity='',mark=False,scope='FOND ARCHITECTURAL — AUCUN APPAREIL DÉDUIT')]
else:
 page=23;title='ÉLÉVATIONS GAUCHE ET DROITE'
 records=[dict(family='Luminaire sécurité',label='Note A — alimentation PSU1-A',x=x,y=y,quantity=1,parent=side,scope='ÉLÉVATION — RÉCONCILIER AVEC PLANS',reserve='Emplacement exact et modèle à coordonner avec architecture; puissance non indiquée.',radius=4.2) for x,y,side in [(507,331,'Gauche'),(416,684,'Droite')]]
 notes=['Deux symboles noirs, chacun avec note A : fournir, installer et raccorder un luminaire de sécurité au panneau PSU1-A.',
 'Modèle, puissance et emplacement exact à coordonner avec architecture. Aucune référence choisie arbitrairement.',
 'Ne pas additionner aux plans de niveau sans identifier les mêmes appareils. Fond architectural et repères fenêtres/portes exclus.',
 'Index E001 nomme cette page E401; le cartouche porte E400. Suffixe page23 conservé pour éviter une fusion avec la page22.']
(ROOT/'audit'/f'{key}-records.json').write_text(json.dumps(dict(page=page,title=title,type='equipment',scope='RELEVÉ DES APPELS ÉLECTRIQUES UNIQUEMENT',records=records,notes=notes),ensure_ascii=False,indent=2))
