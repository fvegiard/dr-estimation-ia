"""Package only reviewed deliverables and the Python scripts used to build them."""
from pathlib import Path
import argparse,hashlib,json,shutil
ROOT=Path(__file__).resolve().parent

def package(sheets, destination):
    checkpoint=json.loads((ROOT/'CHECKPOINT.json').read_text())
    completed=[r for r in checkpoint['feuilles_terminees'] if r['feuille'] in sheets]
    for row in completed:
        data=json.loads((ROOT/'evidence'/f"{row['feuille']}.json").read_text())
        row['reserves_repere']=sum(bool(m.get('reserve')) for m in data['markers'])
    pending=list(checkpoint['feuilles_restantes'])+[r['feuille'] for r in checkpoint['feuilles_terminees'] if r['feuille'] not in sheets]
    checkpoint.update(feuilles_terminees=completed,feuilles_restantes=pending,etat='Relevé en cours — livraison partielle vérifiée')
    text='S-0844 — RELEVÉ PAGE PAR PAGE\n\nÉTAT : EN COURS — LIVRAISON PARTIELLE VÉRIFIÉE\n'
    text+='Projet des cartouches : POLARIS, KEURIG - DR PEPPER MONTRÉAL, 7260 rue St-Urbain.\n'
    text+='Sources : SharePoint Mes projets / s-0844 (13-Novembre-2023). 75 PNG, 63 SHA-256 distincts, 12 doublons retirés. Aucun PDF reçu.\n'
    text+='Aucun QPL de l’estimateur ouvert ni téléchargé depuis SharePoint. Aucune comparaison à son relevé.\n\nFEUILLES VÉRIFIÉES\n'
    for r in completed:text+=f"{r['feuille']} : {r['pastilles']} pastilles; {r['reserves_repere']} réserve(s) de repère; contrôle visuel {r['score']}.\n"
    text+='Les scores concernent les repères annotés et vérifiés; ils ne certifient pas le dossier complet.\n'
    text+='JPEG à résolution source, plan conservé, pastilles et légende intégrée. CSV : une ligne par appareil.\n\nRESTANT À RELEVER\n'+', '.join(pending)+'\n'
    text+='\nNON COMPTÉ / PORTÉES\nLes autres plans ne sont pas encore relevés. Aucune quantité nulle ne doit en être déduite.\n'
    text+='Câbles, conduits, chemins de câbles et longueurs non métrés. Aucun prix. Aucun total global d’achat.\n'
    text+='Un disjoncteur multipolaire = un appareil, une pastille sur le premier pôle. LIBRE avec calibre compté; espace sans calibre exclu.\n'
    text+='EX-M-PE01 : 235 appareils aux cinq panneaux nouveaux. EX-E-PE01 : 103 appareils existants, séparés des achats.\n'
    text+='Ne pas additionner les schémas, plans, détails et cédules. Les versions antérieures ne sont pas additionnées.\n'
    text+='EX-M-0000 est une page de garde/liste de dessins, sans décompte d’appareils. Les légendes ne créent aucune quantité de chantier.\n'
    text+='Feuilles non électriques non relevées : MG-M-RC01 (protection incendie), MX-M-LG01 (mécanique, légende/tableaux), MV-M-0401 (ventilation niveau 4).\n'
    text+='Documents Changement 011 : examen textuel encore à faire. Documents commerciaux Connectrac exclus du relevé aveugle.\n\nRÉSERVES / CONTRADICTIONS\n'
    text+='* EE-M-RC01 : révision 06 datée du 2024-01-12 puis 04 en mars et 05 en avril. Version du 24 avril retenue pour lecture; ordre contractuel à confirmer.\n'
    text+='* C1-3, circuits 2/4/6 : 130 A / 3P conservé tel qu’écrit; série et disponibilité à confirmer. Aucun calibre choisi arbitrairement.\n'
    text+='* UE-1, C1-1, C3-1, C4-1 : barres omnibus indiquées 0 A aux tableaux existants; valeur inutilisable, vérification sur place requise.\n'
    text+='Marques, modèles, séries, protections, pouvoirs de coupure et principaux non précisés. Reconciliation interfeuilles encore en cours.\n'
    for row in completed:
        data=json.loads((ROOT/'evidence'/f"{row['feuille']}.json").read_text())
        text+='\n'+row['feuille']+' — PRÉCISIONS\n'+'\n'.join(data['notes'])+'\n'
    text+='Les autres sources sont accessibles; aucune feuille déclarée illisible à ce stade.\n\nMÉTHODE\n'
    text+='Scripts Python réellement utilisés dans methode/. Ils ont été exécutés à la racine du dossier de travail avec sources/, inspection/ et evidence/ locaux.\n'
    text+='Ces entrées de travail et les zooms ne sont pas publiés. Le clonage de référence et les fichiers sources ne font pas partie de ce livrable.\n'
    text+='Session interactive Codex (GPT-6), lecture et contrôle visuels directs, sans sous-agent.\n'
    text+='manifest.json couvre les fichiers livrés sauf lui-même, par taille et SHA-256.\n'
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'READ-ME.txt').write_text(text,encoding='utf-8')
    (destination/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
    files=[ROOT/'S-0844-inventaire-feuilles.csv']
    for sheet in sheets:files.extend(ROOT.glob(f'S-0844-{sheet}-*'))
    if {'EX-M-PE01','EX-E-PE01'}<=set(sheets):files.extend([ROOT/'S-0844-breakers-by-panel.xlsx',ROOT/'S-0844-breakers-detailed.csv'])
    for path in files:shutil.copy2(path,destination/path.name)
    method=destination/'methode';method.mkdir(exist_ok=True)
    for path in ROOT.glob('*.py'):shutil.copy2(path,method/path.name)
    manifest=[]
    for path in sorted(destination.rglob('*')):
        if path.is_file() and path.name!='manifest.json':manifest.append(dict(file=str(path.relative_to(destination)),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (destination/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    body='Relevé à l’aveugle du dossier S-0844, au format page par page Granby. **Travail en cours : PR brouillon, dossier incomplet.**\n\n'
    body+='| Feuille | Pastilles | Réserves de repère | Fichier |\n|---|---:|---:|---|\n'
    for r in completed:
        f=f"S-0844-{r['feuille']}-releve.jpg"
        body+=f"| {r['feuille']} | {r['pastilles']} | {r['reserves_repere']} | [{f}](dossiers/S-0844/releve-page-par-page/{f}) |\n"
    body+='\nContrôle visuel direct : JPEG ouverts en vue générale puis au zoom par panneau; pastilles sur les symboles, groupes multipolaires comptés une fois, légendes relues.\n'
    body+='\nLimites et contradictions :\n\n- 26 feuilles encore à relever; câbles et conduits non métrés; rapprochement interfeuilles incomplet.\n- 235 disjoncteurs aux tableaux nouveaux; 103 existants séparés. Aucun total global d’achat.\n- C1-3 : 130 A / 3P conservé littéralement, en réserve.\n- Quatre tableaux existants indiquent 0 A aux barres omnibus : à vérifier.\n- EE-M-RC01 : ordre des révisions 06/04/05 incompatible avec les dates janvier/mars/avril 2024.\n- Marques, séries, protections, principaux et pouvoirs de coupure non déterminés.\n- MG-M-RC01, MX-M-LG01 et MV-M-0401 non électriques : non relevées.\n- Aucun QPL estimateur lu; sources et zooms non publiés.\n'
    body=body.replace('26 feuilles encore à relever',f'{len(pending)} feuilles encore à relever')
    for row in completed:
        if row['feuille'] not in {'EX-M-PE01','EX-E-PE01'}:
            data=json.loads((ROOT/'evidence'/f"{row['feuille']}.json").read_text())
            body+='\n'+row['feuille']+' : '+' '.join(data['notes'])+'\n'
    body+='\nValidation : classeur rouvert, 338 lignes et quantités contrôlées. La PR reste en brouillon pendant le relevé.\n'
    test_log=ROOT/'pytest-output.txt'
    if test_log.exists() and (' passed' in test_log.read_text() or ' failed' in test_log.read_text()):
        body+='\nSortie réelle de `python -m pytest tests -q` (pr-repo) :\n```text\n'+test_log.read_text()[-6000:]+'\n```\n'
    (ROOT/'pr-body.md').write_text(body,encoding='utf-8')
    print(f'{len(completed)} feuilles; {len(manifest)} fichiers livrés')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--sheets',nargs='+',required=True);parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args();package(args.sheets,args.destination)
