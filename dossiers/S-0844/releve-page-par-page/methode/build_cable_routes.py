"""Record distinct drawn conduit routes; quantities are routes, never inferred metres."""
import json,sys
from pathlib import Path
from render_sheet import render
ROOT=Path(__file__).resolve().parent
catalog={r['id']:r for r in json.loads((ROOT/'sheet-catalog.json').read_text())}
markers=[]
def marker(family,x,y,description,reserve='',scope='PARCOURS — pas une longueur'):
    markers.append(dict(family=family,x=x,y=y,description=description,reserve=reserve,scope=scope,radius=3.1))
sheet=sys.argv[1]
if sheet=='EC-M-RC01':
    source='008'
    marker('Parcours conduit 25 mm',753,381,'Parcours nord, libellé 1 x CONDUIT 25 mm')
    marker('Parcours conduit 63 mm',753,412.6,'Parcours ouest, libellé 1 x CONDUIT 63 mm')
    marker('Parcours conduit 25 mm',1080,438,'Parcours est, libellé 1 x CONDUIT 25 mm')
    marker('Parcours conduit 63 mm EH',875,580.37,'Premier des deux conduits 63 mm EH, représenté séparément',scope='RENVOI_EX-M-DG02')
    marker('Parcours conduit 63 mm EH',890,581.99,'Second des deux conduits 63 mm EH, représenté séparément',scope='RENVOI_EX-M-DG02')
    markers[-1]['radius']=1.3;markers[-2]['radius']=1.3
    marker('Parcours conduit — note B',904.5,578.8,'Conduit avec corde vers conduit existant intercepté DEMARC / niveau 03','* Diamètre non désigné par la note B; ne pas déduire 63 mm.')
    marker('Réseau chemin de câbles',955.5,510,'Un réseau continu en H dans MDF 1.34, bas à 3300 mm selon note A','* Largeur/hauteur du chemin et longueurs non établies.','RÉSEAU CONTINU — RENVOI_EX-M-DT03')
    notes=['6 parcours de conduits distingués : 2 × 25 mm, 3 × 63 mm et 1 selon note B.',
           'Les deux conduits 63 mm EH sont dessinés et repérés individuellement (petites pastilles).',
           '1 réseau continu de chemin de câbles en H : pas un nombre de pièces ou de mètres.',
           'Note A : bas du chemin à 3300 mm du sol. Section et longueurs non déterminées.',
           'Note B : corde de tirage, raccord au conduit existant DEMARC / mécanique niveau 03.',
           'Recouper avec EX-M-DG02 et EX-M-DT03 : aucune addition automatique des parcours.',
           'Coudes, tés, supports, manchons, raccords et métrés non quantifiés.']
    zones={'core':[700,310,1025,620],'eastline':[960,397,1250,468],'conduits-bas':[856,569,921,590]}
else:raise SystemExit('Unknown sheet')
data=dict(sheet=sheet,source=catalog[source]['file'],markers=markers,csv_type='details',scope='Parcours / réseau — métré non réalisé',legend_box=[260,810,1360,410],notes=notes,review_zones=zones)
(ROOT/'evidence'/f'{sheet}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
render(data)
