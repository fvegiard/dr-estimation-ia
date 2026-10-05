"""Contrôles de fichiers bornés; aucun score visuel ni passage en page acceptée."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def report_is_current(report, root=ROOT):
    """Une preuve ou un livrable absent/modifié invalide le constat enregistré."""
    files = report.get('files', [])
    return bool(files) and all((root / f['path']).is_file() and
        sha(root / f['path']) == f['sha256'] for f in files)

def validate(key, review, root=ROOT, jpeg=None, evidence=()):
    if key == 'E201':
        raise ValueError('E201 réservée : hors périmètre de cette reprise.')
    records_path = root / 'audit' / f'{key}-records.json'
    data = json.loads(records_path.read_text('utf-8'))
    records = data['records']
    csv_path = root / f'S-1294-{key}-{data["type"]}.csv'
    image_path = Path(jpeg) if jpeg else root / f'S-1294-{key}-releve.jpg'
    source = root / 'sources' / f'STAM23A - E - Pour construction - 2024-10-08 - {data["page"]}.png'
    with csv_path.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    expected = [(r['id'], r['family'], str(r.get('quantity', 1)), str(r.get('circuits', ''))) for r in records]
    actual = [(r['Repère / source'], r['Matériel'], r['Qté'], r['Circuits']) for r in rows]
    errors = []
    if expected != actual:
        errors.append('CSV/JSON différents : ID, famille, quantité ou circuit.')
    if len({r['id'] for r in records}) != len(records):
        errors.append('ID dupliqué dans le relevé.')
    with Image.open(source) as src, Image.open(image_path) as output:
        dimensions = {'source': list(src.size), 'jpeg': list(output.size)}
    files = [records_path, csv_path, source, image_path, *map(Path, evidence)]
    return {
        'sheet': key, 'source_page': data['page'],
        'markers': sum(r.get('mark', True) for r in records),
        'review_note': review,
        'checks': {
            'csv_json_fields': {'status': 'FAIL' if errors else 'PASS', 'errors': errors,
                'scope': 'ID, famille, quantité et circuit transcrits; une omission commune reste possible.'},
            'sheet_dimensions': {'status': 'PASS' if dimensions['source'] == dimensions['jpeg'] else 'FAIL',
                **dimensions, 'scope': 'Dimensions seules; ne prouve ni absence de masquage ni lisibilité.'}},
        'visual_conformity': 'non démontrée',
        'business_accuracy': 'non démontrée',
        'qpl_comparison': 'non effectuée par ce script',
        'acceptance': 'non prononcée',
        'files': [{'path': str(p.resolve().relative_to(root.resolve())) if p.resolve().is_relative_to(root.resolve()) else str(p.resolve()),
                   'sha256': sha(p)} for p in files],
        'scope': 'Contrôles automatiques limités. Aucun taux métier. CHECKPOINT inchangé.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('review')
    parser.add_argument('--jpeg', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--evidence', type=Path, action='append', default=[])
    args = parser.parse_args()
    proof = validate(args.key, args.review, jpeg=args.jpeg, evidence=args.evidence)
    path = args.output or ROOT / 'audit' / args.key / 'verification.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        archive = path.with_name(f'{path.stem}-historique-{sha(path)[:12]}{path.suffix}')
        if not archive.exists():
            archive.write_bytes(path.read_bytes())
    path.write_text(json.dumps(proof, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'sheet': args.key, 'checks': proof['checks'], 'acceptance': proof['acceptance']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
