"""Package only deliverables and used Python methods for a given completed stage."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
stage=int(sys.argv[1])
target=ROOT/'pr-repo/dossiers/S-0922/releve-page-par-page'
target.mkdir(parents=True,exist_ok=True)
checkpoint=json.loads((ROOT/'CHECKPOINT.json').read_text())
completed=[r for r in checkpoint['completed'] if int(r['sheet'].split('-')[1])<=stage]
checkpoint['completed']=completed
checkpoint['remaining']=[s for s in ['E-1','E-2','E-3','E-4','E-5'] if s not in {r['sheet'] for r in completed}]
checkpoint['status']='Relevé page par page terminé avec réserves; vérification à l’aveugle' if not checkpoint['remaining'] else 'Relevé en cours — PR brouillon'
lines=['S-0922 — NIKE QUARTIER DIX30, UNITÉ S9D, BROSSARD',checkpoint['status'],'',
    'Identification depuis les plans PNG seulement; aucun QPL ouvert ni téléchargé.',
    'Référence de présentation : Granby du 30 septembre 2026. Plans originaux conservés et légendes intégrées.',
    'Les révisions antérieures ne sont pas additionnées. Pas de prix, de métré de câbles, conduits ou rails.',
    'Les symboles au schéma et les renvois ne constituent pas des appareils supplémentaires.',
    'Une pastille par symbole retenu; cédules de disjoncteurs transcrites séparément.',
    'Aucun calibre choisi arbitrairement. * dans le relevé = réserve; * dans la cédule source = disjoncteur neuf.','',
    'FEUILLES COUVERTES']
for r in completed:lines.append(f"{r['sheet']} : {r['markers']} pastilles. {r['visual_check']}")
if checkpoint['remaining']:lines.append('À terminer : '+', '.join(checkpoint['remaining']))
lines+=['','RÉVISIONS ET RÉSERVES',
    'E-1 / E-2 / E-3 : construction et changement E-1 du 22 avril 2024.',
    'E-4 : changement E-2 du 29 avril 2024; remplace la version du 22 avril.',
    'E-5 : seule version disponible du 26 janvier 2024, DO NOT USE FOR CONSTRUCTION. Portée actuelle à confirmer.',
    'E-2 : P1 49 + P2 42 = 91 disjoncteurs, dont 8 marqués neufs et 83 existants à réutiliser.',
    'SPARE avec calibre inclus; SPACE sans calibre exclu. Un multipolaire = un appareil, pôles selon cellules regroupées.',
    'P2-6 et P2-10 : calibres traversés par les nuages de révision, laissés vides. P2-14 : 20* lu, à confirmer.',
    'Panneaux existants 225 A, 120/208 V, 3 phases, 4 fils. Marque, série, protections et ICC non déterminés.',
    'Contradiction E-2 : répartiteur secondaire noté 600 V après transformateur 600/120/208 V; aucune tension corrigée arbitrairement.',
    'E-2 : transformateur existant 112,5 kVA à suspendre; détail de suspension et représentation E-4 non additionnés.',
    'E-2 : détail incendie = 3 symboles de principe, aucun multiplicateur déduit.',
    'E-3 : faces et flèches des 6 indicateurs de sortie à confirmer.',
    'Les images de présentation architecturale ne donnent aucune quantité de luminaires.',
    'Comparaison à l’estimateur volontairement absente : relevé à l’aveugle, aucune certification de supériorité.',
    '', 'DOCUMENTS NON RELEVÉS',
    '23-357-M-PE-2 - 1.png et - 2.png : mécanique (devis/légendes et implantation), non relevés.',
    'NSP_DIX 30 - 1.png à - 16.png : présentation architecturale (vues et matériaux), non relevées.',
    'Nike - Gicleurs - Directive #1 - 2024-01-25.png : directive gicleurs, non relevée.',
    'Nike - Gicleurs - Directive #1 - Plan PI-04 2024-01-25.png : plan gicleurs PI-04, non relevé.',
    'Aucune feuille A- ou S- distincte identifiée dans les noms; vues architecturales sous NSP_DIX 30.',
    'relevé éclairage.png et propositions : exclus sans ouverture. Copies téléchargées par filtre initial PNG, retirées aussitôt identifiées.',
    'Révisions électriques PE-2 E-1 à E-4 et E-4 du 22 avril conservées seulement comme sources antérieures, non cumulées.',
    '', 'SOURCES ET MÉTHODE',
    'Accès anonyme SharePoint Mes projets / S-0922 (31-Janvier-2024), module MesProjets du dépôt.',
    'Déduplication par SHA-256; une copie conservée par empreinte. Sources exclues de la PR.',
    'Scripts en anglais dans methode/. Les coordonnées des CSV sont en pixels des sources originales.',
    'Les zooms de vérification restent dans le dossier de travail local et ne sont pas publiés.',
    'manifest.json : empreintes et tailles des fichiers publiés (hors manifest lui-même).',
    'CHECKPOINT.json : état par feuille et scores de vérification visuelle.',
]
readme='\n'.join(lines)+'\n'
(ROOT/'READ-ME.txt').write_text(readme,encoding='utf-8')
(target/'READ-ME.txt').write_text(readme,encoding='utf-8')
(target/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in completed:
    for file in ROOT.glob(f'S-0922-{r["sheet"]}-*'):
        if file.suffix in {'.jpg','.csv'}:shutil.copy2(file,target/file.name)
if stage>=2:
    for name in ['S-0922-breakers-by-panel.xlsx','S-0922-breakers-detailed.csv']:shutil.copy2(ROOT/name,target/name)
method=target/'methode';method.mkdir(exist_ok=True)
scripts=['download_plans.py','prepare_images.py','render_sheet.py','package_delivery.py']
if stage>=2:scripts+=['build_panels.py']
if stage>=3:scripts+=['build_lighting.py']
for name in ['build_services.py','build_led.py']:
    if (ROOT/name).exists() and stage>=({'build_services.py':4,'build_led.py':5}[name]):scripts.append(name)
for name in scripts:shutil.copy2(ROOT/name,method/name)
# Keep hand-reviewed source records as Python data, without publishing sources or inspection images.
sheets={r['sheet']:json.loads((ROOT/'data'/f'{r["sheet"]}.json').read_text()) for r in completed}
(method/'sheet_data.py').write_text('"""Reviewed source coordinates and sheet notes for the published stage."""\nSHEETS = '+repr(sheets)+'\n',encoding='utf-8')
manifest=[]
for file in sorted(target.rglob('*')):
    if file.is_file() and file.name!='manifest.json':manifest.append(dict(file=str(file.relative_to(target)),bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
(target/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body=['Relevé à l’aveugle de S-0922 depuis les plans PNG, au format Granby. Aucune réponse de l’estimateur utilisée.','',
    '| Feuille | Pastilles | Réserves | Fichier |','|---|---:|---|---|']
for r in completed:
    d=sheets[r['sheet']];n=sum(bool(m.get('reserve')) for m in d.get('markers',[]))
    detail=f'{n} repères'+(' + 3 lectures de cédule' if r['sheet']=='E-2' else '')
    body.append(f'| {r["sheet"]} | {r["markers"]} | {detail} | [JPEG](dossiers/S-0922/releve-page-par-page/S-0922-{r["sheet"]}-releve.jpg) |')
body+=['','Feuilles restantes : '+(', '.join(checkpoint['remaining']) or 'aucune'),'',readme,
       '\nValidation automatisée : en attente de fin du relevé; PR maintenue en brouillon.']
(ROOT/'PR-BODY.md').write_text('\n'.join(body),encoding='utf-8')
print(target,len(manifest),'fichiers indexés')
