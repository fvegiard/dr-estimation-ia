"""Package only deliverables and used Python methods for a given completed stage."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

METHOD=Path(__file__).resolve().parent
ROOT=METHOD.parent if METHOD.name=='methode' else METHOD
# Invalider le précédent reçu dès le début, y compris si une lecture/copie échoue.
(ROOT/'PR-BODY.md').unlink(missing_ok=True)
stage=int(sys.argv[1])
if stage not in range(1,6):
    raise ValueError('Étape attendue : 1 à 5.')
target=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else ROOT/'pr-repo/dossiers/S-0922/releve-page-par-page'
if target==ROOT or target in ROOT.parents:
    raise ValueError('La destination doit être distincte du dossier source et de ses parents.')
target.mkdir(parents=True,exist_ok=True)
checkpoint=json.loads((ROOT/'CHECKPOINT.json').read_text(encoding='utf-8'))
completed=[r for r in checkpoint['completed'] if int(r['sheet'].split('-')[1])<=stage]
checkpoint['completed']=completed
checkpoint['remaining']=[s for s in ['E-1','E-2','E-3','E-4','E-5'] if s not in {r['sheet'] for r in completed}]
# Refuser une ancienne livraison plus avancée, sans effacer ses fichiers.
for file in target.glob('S-0922-E-*-*'):
    if not any(file.name.startswith(f'S-0922-{r["sheet"]}-') for r in completed):
        raise ValueError(f'Destination contenant une autre étape : {file}. Choisir un dossier vide.')
checkpoint['status']='Relevé page par page terminé avec réserves; comparaison globale à l’estimateur non validée' if not checkpoint['remaining'] else 'Relevé en cours — PR brouillon'
lines=['S-0922 — RELEVÉ AVEC RÉSERVES','NIKE QUARTIER DIX30, UNITÉ S9D, BROSSARD',checkpoint['status'],'',
    'Identification initiale depuis les plans PNG; aucun QPL ouvert ni téléchargé par le producteur.',
    'V2 après revue indépendante : courbe F nord-ouest confirmée directement sur le plan E-5 et ajoutée en réserve.',
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
    'E-4 : 17 repères C/W/TC cerclés sans définition dans la légende disponible; aucune fonction supposée.',
    'E-4 / E-2 : 5 sectionneurs existants au plan contre 4 au schéma; calibres et correspondance non établis.',
    'E-4 : relais vers déclenchement shunt-trip sonore prescrit; circuit et calibre non précisés.',
    'E-4 : 4 serpentins et 2 boîtes terminales représentés; caractéristiques à coordonner avec mécanique.',
    'E-5 : 72 repères en réserve, dont 45 tronçons D. Aucun nombre de modules ou de longueurs déduit.',
    'E-5 : 5 sections F pour 4 alimentations dessinées; courbe nord-ouest entre deux jonctions ajoutée sous E-5-072, après vérification du plan source.',
    'E-5 : 2 sections N sans définition à la cédule; circuit 14 nommé TYPE N à E-2 mais inscrit aux sections J à E-5.',
    'E-5 : limites de segmentation aux jonctions courbe/droite D et aux sections F à confirmer avant achat.',
    'Les images de présentation architecturale ne donnent aucune quantité de luminaires.',
    'Comparaison métier globale à l’estimateur : BLOCKED dans la revue indépendante; aucune certification de supériorité ni de quantités de chantier.',
    '', 'DOCUMENTS NON RELEVÉS',
    'M-1 : 23-357-M-PE-2 - 1.png, légende et devis mécanique, non relevé.',
    'M-2 : 23-357-M-PE-2 - 2.png, ventilation mécanique, non relevé.',
    'NSP_DIX 30 - 1.png à - 16.png : présentation architecturale (vues et matériaux), non relevées.',
    'Nike - Gicleurs - Directive #1 - 2024-01-25.png : directive gicleurs, non relevée.',
    'Nike - Gicleurs - Directive #1 - Plan PI-04 2024-01-25.png : plan gicleurs PI-04, non relevé.',
    'Aucune feuille A- ou S- distincte identifiée dans les noms; vues architecturales sous NSP_DIX 30.',
    'relevé éclairage.png et propositions : exclus sans ouverture. Copies téléchargées par filtre initial PNG, retirées aussitôt identifiées.',
    'Révisions électriques PE-2 E-1 à E-4 et E-4 du 22 avril conservées seulement comme sources antérieures, non cumulées.',
    '', 'SOURCES ET MÉTHODE',
    'Accès anonyme SharePoint Mes projets / S-0922 (31-Janvier-2024), module MesProjets du dépôt.',
    'Déduplication par SHA-256; une copie conservée par empreinte. Sources exclues de la PR.',
    'Scripts dans methode/. Les coordonnées des CSV sont en pixels des sources originales.',
    'Les zooms de vérification restent dans le dossier de travail local et ne sont pas publiés.',
    'manifest.json : empreintes et tailles des fichiers publiés (hors manifest lui-même).',
    'CHECKPOINT.json : état par feuille et scores de vérification visuelle.',
    '', 'REPRODUIRE LOCALEMENT',
    'Depuis le dépôt : python dossiers/S-0922/releve-page-par-page/methode/download_plans.py',
    'Les sources sont restaurées sous releve-page-par-page/sources/. Le module src/apprentissage/sharepoint.py du dépôt est requis.',
    'Pour chaque feuille : python methode/render_sheet.py E-1 (puis E-2 à E-5). Les données revues de sheet_data.py sont incluses.',
    'Réassemblage : python methode/package_delivery.py 5 CHEMIN_DESTINATION. Choisir un dossier de livraison distinct.',
    'Contrôle : python methode/verify_delivery.py CHEMIN_DESTINATION. Le package exécute aussi ce contrôle avant de déclarer son succès.',
    'Inventaire strict : chaque fichier présent doit être attendu et indexé, sauf manifest.json lui-même.',
    'Checkout publié : ajouter --checkout tolère uniquement .gitattributes, PR-BODY.md et les caches CPython des scripts attendus sous methode/__pycache__/.',
    'Rendu Windows : Arial par défaut; S0922_FONT permet de fournir DejaVuSans.ttf pour retrouver la police Linux.',
    'Ces commandes ne publient rien. La revue du parent reste requise avant toute publication.',
]
readme='\n'.join(lines)+'\n'
(target/'READ-ME.txt').write_text(readme,encoding='utf-8',newline='\n')
(target/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for r in completed:
    for file in ROOT.glob(f'S-0922-{r["sheet"]}-*'):
        if file.suffix in {'.jpg','.csv'}:shutil.copy2(file,target/file.name)
if stage>=2:
    for name in ['S-0922-breakers-by-panel.xlsx','S-0922-breakers-detailed.csv']:shutil.copy2(ROOT/name,target/name)
method=target/'methode';method.mkdir(exist_ok=True)
scripts=['download_plans.py','prepare_images.py','render_sheet.py','package_delivery.py']
scripts.append('verify_delivery.py')
if stage>=2:scripts+=['build_panels.py']
if stage>=3:scripts+=['build_lighting.py']
for name in ['build_services.py','build_led.py']:
    if (METHOD/name).exists() and stage>=({'build_services.py':4,'build_led.py':5}[name]):scripts.append(name)
for name in scripts:shutil.copy2(METHOD/name,method/name)
# Keep hand-reviewed source records as Python data, without publishing sources or inspection images.
if (METHOD/'sheet_data.py').exists():
    from sheet_data import SHEETS
else:
    SHEETS={}  # Ancien dossier de travail : chaque JSON doit alors être présent.
sheets={}
for r in completed:
    data_path=ROOT/'data'/f'{r["sheet"]}.json'
    sheets[r['sheet']]=json.loads(data_path.read_text(encoding='utf-8')) if data_path.exists() else SHEETS[r['sheet']]
(method/'sheet_data.py').write_text('"""Reviewed source coordinates and sheet notes for the published stage."""\nSHEETS = '+repr(sheets)+'\n',encoding='utf-8',newline='\n')
manifest=[]
for file in sorted(target.rglob('*')):
    if file.is_file() and file.name!='manifest.json' and '__pycache__' not in file.parts:
        manifest.append(dict(file=file.relative_to(target).as_posix(),bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
(target/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
subprocess.run([sys.executable,'-B',str(method/'verify_delivery.py'),str(target)],check=True)
body=['Relevé S-0922 au format Granby, avec contrôles techniques du paquet et réserves explicites. Comparaison métier globale à l’estimateur non validée.','',
    '| Feuille | Pastilles | Réserves | Fichier |','|---|---:|---|---|']
for r in completed:
    d=sheets[r['sheet']];n=sum(bool(m.get('reserve')) for m in d.get('markers',[]))
    detail=f'{n} repères'+(' + 3 lectures de cédule' if r['sheet']=='E-2' else '')
    body.append(f'| {r["sheet"]} | {r["markers"]} | {detail} | [JPEG](dossiers/S-0922/releve-page-par-page/S-0922-{r["sheet"]}-releve.jpg) |')
body+=['','Feuilles restantes : '+(', '.join(checkpoint['remaining']) or 'aucune'),'',readme,
       '\nValidation automatisée : réussie pour les fichiers assemblés (inventaire, empreintes, dimensions, CSV/données revues, transcriptions des cédules et détails, cellules du classeur).',
       'Relevé encore partiel; feuilles restantes à traiter.' if checkpoint['remaining'] else
       'Les cinq feuilles sont assemblées avec leurs réserves. Revue du parent requise avant publication; aucune validation de chantier.']
(ROOT/'PR-BODY.md').write_text('\n'.join(body),encoding='utf-8')
print(target,len(manifest),'fichiers indexés')
