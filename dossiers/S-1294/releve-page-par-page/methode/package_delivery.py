"""Package only reviewed deliverables and generate the French PR description."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'pr-repo' / 'dossiers' / 'S-1294' / 'releve-page-par-page'

def main():
    checkpoint = json.loads((ROOT / 'CHECKPOINT.json').read_text())
    limit = int(sys.argv[1]) if len(sys.argv)>1 else len(checkpoint['completed'])
    completed = checkpoint['completed'][:limit]
    omitted = checkpoint['completed'][limit:]
    checkpoint['completed'] = completed
    checkpoint['remaining'] = [r['sheet'] for r in omitted] + checkpoint['remaining']
    DEST.mkdir(parents=True, exist_ok=True)
    methods = DEST / 'methode'
    methods.mkdir(exist_ok=True)
    for source in (ROOT / 'scripts').glob('*.py'):
        shutil.copy2(source, methods / source.name)
    lines = ['S-1294 — RELEVÉ PAGE PAR PAGE', '',
             'ÉTAT : EN COURS — PR BROUILLON. Ce dossier ne constitue pas un relevé exhaustif.',
             'Source : série STAM23A, pour construction du 8 octobre 2024, dossier SharePoint S-1294 (10-Décembre-2024).',
             '34 PNG uniques conservés après dédoublonnage SHA-256; un doublon supprimé. Aucun .qpl SharePoint téléchargé ou ouvert.',
             'Référence de présentation : livrable Granby du 30 septembre 2026.', '', 'FEUILLES VÉRIFIÉES :']
    table = ['| Feuille | Pastilles | Réserves | Fichier |','|---|---:|---:|---|']
    for entry in completed:
        key = entry['sheet']
        data = json.loads((ROOT/'audit'/f'{key}-records.json').read_text())
        reserved = sum(bool(r.get('reserve')) for r in data['records'])
        entry['reserves'] = reserved
        for source in ROOT.glob(f'S-1294-{key}-*'):
            if source.suffix.lower() in {'.csv','.jpg'}:
                shutil.copy2(source, DEST / source.name)
        filename=f'S-1294-{key}-releve.jpg'
        lines.append(f'{key} : {entry["markers"]} pastilles; {reserved} réserves; contrôle visuel {entry["visual_score"]}.')
        lines += ['  '+note for note in data['notes']]
        table.append(f'| {key} | {entry["markers"]} | {reserved} | [{filename}](dossiers/S-1294/releve-page-par-page/{filename}) |')
    limits = [
        'Feuilles restant à traiter : '+', '.join(checkpoint['remaining'])+'.',
        'Numéros de cartouche répétés : E002 pages 2–3, E105 pages 9–10, E400 pages 22–23. Les suffixes page distinguent les fichiers.',
        'Aucune feuille M-, A- ou S- dans la série principale de 23 pages. Les 11 scans complémentaires restent à classer et à contrôler.',
        'Les détails types et diagrammes ne constituent pas une quantité globale de chantier. Ne pas additionner schémas, plans de niveau et logements types.',
        'Câbles, conduits, longueurs, fixations et accessoires non représentés ne sont pas métrés. Familles non marquées non réputées comptées.',
        'Aucun calibre ni nombre de pôles choisi arbitrairement. Les incertitudes explicites portent un astérisque et une réserve dans le CSV.',
        'Modèle non précisé ne signifie pas choix de fabricant. Équipements fournis par autres et renvois conservent leur portée.',
        'Vérification à l’aveugle : aucune comparaison au relevé de l’estimateur. Aucune certification de résultat équivalent à l’estimateur.',
        'La légende est ajoutée dans une bande blanche intégrée sous le plan, afin de préserver intégralement le dessin source.',
        'Le manifest couvre les livrables et les scripts livrés, hors manifest lui-même. Sources et preuves de zoom conservées uniquement dans le dossier de travail.'
    ]
    if any(e['sheet']=='E103' for e in completed):
        limits.append('E103 : repères PL incompatibles avec les numéros d’unités aux centres CM-01 à CM-03; correspondance réservée. Disjoncteurs 100 A : pôles non indiqués.')
    if any(e['sheet']=='E104' for e in completed):
        limits.append('E104 : repères PL206 et PL208 répétés; correspondance logements / centres réservée. Les 36 représentations PL ne prouvent pas 36 panneaux distincts.')
    if any(e['sheet']=='E105-page09' for e in completed):
        for filename in ['S-1294-breakers-by-panel.xlsx','S-1294-breakers-detailed.csv']:
            shutil.copy2(ROOT/filename, DEST/filename)
        limits.append('E105 page 9 : 194 départs et 3 principaux; six ESPACE avec calibre réservés. PS1 : tension 347/600 V en cédule contre 120/208 V sur E102. PP1 : Icc 14 kA contre 35 kA. Autres divergences de barres, principaux et Icc consignées au classeur; aucun arbitrage. Les 86 disjoncteurs de centres CM restent dans un onglet séparé, non additionné.')
    lines += ['', 'LIMITES ET RÉSERVES :'] + limits
    (DEST/'READ-ME.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (DEST/'CHECKPOINT.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    inventory=[]
    for path in sorted(DEST.rglob('*')):
        if path.is_file() and path.name!='manifest.json':
            inventory.append({'file':path.relative_to(DEST).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (DEST/'manifest.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    body = ['Relevé à l’aveugle S-1294 en cours, depuis les plans sources. Chaque feuille publiée comporte un JPEG annoté vérifié au zoom et un CSV traçable.', '', *table, '', 'Limites et contradictions :', '']
    body += ['- '+s for s in limits]
    body += ['', 'Validation : contrôles visuels individuels consignés dans CHECKPOINT.json. Tests pytest et CI à exécuter avant toute sortie du brouillon. Aucun merge demandé.']
    (ROOT/'audit'/'pr-body.md').write_text('\n'.join(body)+'\n',encoding='utf-8')
    print('Packaged:', ', '.join(e['sheet'] for e in completed))

if __name__=='__main__':
    main()
