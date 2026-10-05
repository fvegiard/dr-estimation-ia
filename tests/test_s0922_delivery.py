"""Régressions des chemins publiés et mutations des données revues de S-0922."""
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


DELIVERY = Path(__file__).resolve().parents[1] / 'dossiers/S-0922/releve-page-par-page'


def run(script, *args, cwd=None, optimize=False):
    return subprocess.run([sys.executable, '-B', str(script), *map(str, args)],
                          cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding='utf-8',
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONOPTIMIZE': '1' if optimize else '0'})


def manifest(root):
    records = [dict(file=p.relative_to(root).as_posix(), bytes=p.stat().st_size,
                    sha256=hashlib.sha256(p.read_bytes()).hexdigest())
               for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'manifest.json'
               and '__pycache__' not in p.parts]
    (root / 'manifest.json').write_text(json.dumps(records), encoding='utf-8')


@pytest.fixture
def published(tmp_path):
    root = tmp_path / 'repo/dossiers/S-0922/releve-page-par-page'
    root.mkdir(parents=True)
    shutil.copytree(DELIVERY / 'methode', root / 'methode',
                    ignore=shutil.ignore_patterns('__pycache__', 'pr-repo'))
    for source in DELIVERY.iterdir():
        if source.suffix in {'.csv', '.xlsx', '.txt', '.json'}:
            shutil.copyfile(source, root / source.name)
        elif source.suffix == '.jpg':
            with Image.open(source) as im:
                # Les dimensions sont réelles, le fond synthétique évite de dupliquer les plans.
                Image.new('RGB', im.size, 'white').save(root / source.name)
    manifest(root)
    return root


def test_downloader_resolves_repository_and_delivery_roots(published, tmp_path):
    shared = published.parents[2] / 'src/apprentissage/sharepoint.py'
    shared.parent.mkdir(parents=True)
    shared.write_text('''class MesProjets:
    def __init__(self, **kw): self.racine = kw['racine']
    def fichiers(self, folder):
        return [{'Name': 'plan.png', 'Length': 3}, {'Name': 'relevé.png', 'Length': 3},
                {'Name': 'réponse.qpl', 'Length': 3}]
    def dossiers(self, folder): return []
    def telecharger(self, remote, target, size):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'PNG')
''', encoding='utf-8')
    result = run(published / 'methode/download_plans.py', cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (published / 'sources/plan.png').read_bytes() == b'PNG'
    assert not (published / 'methode/sources').exists()
    assert len(json.loads((published / 'source-inventory.json').read_text())) == 1


def test_prepare_creates_inspection_parent(published, tmp_path):
    sources = published / 'sources'
    sources.mkdir()
    Image.new('RGB', (1800, 1400), 'white').save(sources / '23-357-E-PE-2 - 5.png')
    result = run(published / 'methode/prepare_images.py', 'E-5', 'detail', 100, 100, 200, 200,
                 cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (published / 'inspection/detail.jpg').exists()


def test_render_creates_inspection_parent_and_csv(published, tmp_path):
    sources = published / 'sources'
    sources.mkdir()
    Image.new('RGB', (1800, 1400), 'white').save(sources / '23-357-E-PE-2 - 5.png')
    code = ('import sys; sys.path.insert(0, sys.argv[1]); import render_sheet; '
            "render_sheet.FONT = 'arial.ttf' if sys.platform == 'win32' else render_sheet.FONT; "
            "render_sheet.render('E-5')")
    result = subprocess.run([sys.executable, '-B', '-c', code, str(published / 'methode')],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (published / 'inspection/E-5/final-legend.jpg').exists()
    with (published / 'S-0922-E-5-equipment.csv').open(encoding='utf-8-sig') as f:
        assert len(list(csv.DictReader(f))) == 72


@pytest.mark.parametrize('stage', [2, 5])
def test_package_replays_published_layout(published, tmp_path, stage):
    target = tmp_path / f'livraison-{stage}'
    result = run(published / 'methode/package_delivery.py', stage, target, cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (target / 'methode/sheet_data.py').exists()
    assert (target / 'methode/verify_delivery.py').exists()
    assert not (target / 'sources').exists()
    result = run(target / 'methode/verify_delivery.py', target, cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert len(list(target.glob('*-releve.jpg'))) == stage
    body = (published / 'PR-BODY.md').read_text(encoding='utf-8')
    assert 'Validation automatisée : réussie' in body
    assert 'en attente de fin du relevé' not in body
    if stage == 5:
        assert 'PR maintenue en brouillon' not in body
        assert 'DO NOT USE FOR CONSTRUCTION' in body
        # Le paquet autonome doit à son tour se réassembler sans data/*.json.
        again = tmp_path / 'reassemblage'
        result = run(target / 'methode/package_delivery.py', 5, again, cwd=tmp_path)
        assert result.returncode == 0, result.stderr


MUTATIONS = [
    ('Repère / source', 'E-5-999'), ('Matériel', 'N*'), ('Désignation', 'AUTRE'),
    ('Qté', '2'), ('Portée', 'INSTALLER'), ('Modèle', 'MODÈLE INCORRECT'),
    ('Prescription / réserve', ''), ('Parent', 'P1-99'),
    ('X source px', '1.0'), ('Y source px', '1.0'),
]


def mutate(root, field, value, filename='S-0922-E-5-equipment.csv'):
    path = root / filename
    delimiter = ';' if filename == 'S-0922-E-1-details.csv' else ','
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fields = reader.fieldnames
        rows = list(reader)
    rows[0][field] = value
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)
    manifest(root)  # Une empreinte régénérée ne doit pas masquer un CSV faux.


@pytest.mark.parametrize(('field', 'value'), MUTATIONS)
def test_verifier_rejects_rehashed_field_mutations(published, tmp_path, field, value):
    mutate(published, field, value)
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path)
    assert result.returncode != 0, f'Mutation acceptée : {field}'


def test_package_does_not_claim_success_after_failed_verification(published, tmp_path):
    (published / 'PR-BODY.md').write_text('Validation automatisée : réussie', encoding='utf-8')
    mutate(published, 'Portée', 'INSTALLER')
    result = run(published / 'methode/package_delivery.py', 5, tmp_path / 'incorrect', cwd=tmp_path)
    assert result.returncode != 0
    body = published / 'PR-BODY.md'
    assert not body.exists() or 'Validation automatisée : réussie' not in body.read_text(encoding='utf-8')


def test_verifier_accepts_reordered_rows(published, tmp_path):
    path = published / 'S-0922-E-5-equipment.csv'
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reversed(rows))
    manifest(published)
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('extra', ['extra.csv', 'methode/extra.xlsx', 'extra/releve.jpg',
                                 'extra/manifest.json', 'methode/__pycache__/extra.csv'])
@pytest.mark.parametrize('checkout', [False, True])
def test_verifier_rejects_unindexed_files(published, tmp_path, extra, checkout):
    path = published / extra
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('unreviewed,data', encoding='utf-8')
    args = [published, '--checkout'] if checkout else [published]
    result = run(published / 'methode/verify_delivery.py', *args, cwd=tmp_path, optimize=True)
    assert result.returncode != 0, f'Fichier hors manifeste accepté : {extra}'
    assert 'Inventaire physique' in result.stderr


def test_verifier_accepts_normal_package_without_creating_cache(published, tmp_path):
    # Exécution usuelle sans -B : le contrôle ne doit pas ajouter son propre fichier.
    result = subprocess.run([sys.executable, str(published / 'methode/verify_delivery.py'), str(published)],
                            cwd=tmp_path, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stderr
    assert not list(published.rglob('*.pyc'))


def test_verifier_checkout_metadata_requires_explicit_mode(published, tmp_path):
    (published / '.gitattributes').write_text('*.csv -text\n', encoding='utf-8')
    (published / 'PR-BODY.md').write_text('Relevé avec réserves\n', encoding='utf-8')
    cache = published / 'methode/__pycache__/render_sheet.cpython-314.opt-1.pyc'
    cache.parent.mkdir()
    cache.write_bytes(b'cache de travail non importe')
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path)
    assert result.returncode != 0
    assert 'Inventaire physique' in result.stderr
    result = run(published / 'methode/verify_delivery.py', published, '--checkout', cwd=tmp_path)
    assert result.returncode == 0, result.stderr


def test_package_refuses_stale_later_sheets(published, tmp_path):
    target = tmp_path / 'ancienne-livraison'
    target.mkdir()
    stale = target / 'S-0922-E-5-equipment.csv'
    stale.write_text('conserver', encoding='utf-8')
    result = run(published / 'methode/package_delivery.py', 2, target, cwd=tmp_path)
    assert result.returncode != 0
    assert stale.read_text(encoding='utf-8') == 'conserver'


def test_builders_replay_from_arbitrary_working_directory(published, tmp_path):
    for name in ['build_panels.py', 'build_lighting.py', 'build_services.py', 'build_led.py']:
        result = run(published / 'methode' / name, cwd=tmp_path)
        assert result.returncode == 0, result.stderr
    spec = importlib.util.spec_from_file_location('reviewed_sheets', published / 'methode/sheet_data.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for sheet in ['E-2', 'E-3', 'E-4', 'E-5']:
        generated = json.loads((published / 'data' / f'{sheet}.json').read_text(encoding='utf-8'))
        assert generated == module.SHEETS[sheet], sheet
    for name in ['S-0922-breakers-detailed.csv', 'S-0922-E-2-breakers.csv']:
        assert (published / name).read_bytes() == (DELIVERY / name).read_bytes()


@pytest.mark.parametrize(('filename', 'field', 'value'), [
    ('S-0922-breakers-detailed.csv', 'ampere', '999'),
    ('S-0922-breakers-detailed.csv', 'quantity', '999'),
    ('S-0922-breakers-detailed.csv', 'circuits', '999'),
    ('S-0922-E-2-breakers.csv', 'ampere', '999'),
    ('S-0922-E-1-details.csv', 'Quantité', '999'),
    ('S-0922-E-2-details.csv', 'Portée / réserve', 'RESERVE INVENTEE'),
])
def test_independent_csv_counterexamples(published, tmp_path, filename, field, value):
    mutate(published, field, value, filename)
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path)
    assert result.returncode != 0, f'Mutation acceptée : {filename}, {field}'


@pytest.mark.parametrize('case', ['empty_manifest', 'missing_workbook', 'corrupt_workbook',
                                 'workbook_value', 'workbook_missing_sheet', 'optimized_equipment'])
def test_independent_structural_counterexamples(published, tmp_path, case):
    workbook = published / 'S-0922-breakers-by-panel.xlsx'
    if case == 'missing_workbook':
        workbook.unlink()
    elif case == 'corrupt_workbook':
        workbook.write_bytes(b'NOT AN XLSX')
    elif case in {'workbook_value', 'workbook_missing_sheet'}:
        import openpyxl
        wb = openpyxl.load_workbook(workbook)
        if case == 'workbook_value':
            wb['P1']['C2'] = 999
        else:
            del wb['P1']
        wb.save(workbook)
    elif case == 'optimized_equipment':
        mutate(published, 'Portée', 'INSTALLER')
    manifest(published)
    if case == 'empty_manifest':
        (published / 'manifest.json').write_text('[]', encoding='utf-8')
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path,
                 optimize=case == 'optimized_equipment')
    assert result.returncode != 0, f'Contre-exemple accepté : {case}'


@pytest.mark.parametrize('case', ['wrong_breaker', 'missing_workbook', 'missing_checkpoint'])
def test_independent_package_counterexamples(published, tmp_path, case):
    if case == 'wrong_breaker':
        mutate(published, 'ampere', '999', 'S-0922-breakers-detailed.csv')
    elif case == 'missing_workbook':
        (published / 'S-0922-breakers-by-panel.xlsx').unlink()
    else:
        (published / 'CHECKPOINT.json').unlink()
    body = published / 'PR-BODY.md'
    body.write_text('Validation automatisée : réussie', encoding='utf-8')
    result = run(published / 'methode/package_delivery.py', 5, tmp_path / 'incorrect', cwd=tmp_path)
    assert result.returncode != 0
    assert not body.exists() or 'Validation automatisée : réussie' not in body.read_text(encoding='utf-8')


def test_reviewed_workbook_accepts_resave(published, tmp_path):
    import openpyxl
    path = published / 'S-0922-breakers-by-panel.xlsx'
    wb = openpyxl.load_workbook(path)
    wb.properties.creator = 'Test de conservation des cellules'
    wb.save(path)
    manifest(published)
    result = run(published / 'methode/verify_delivery.py', published, cwd=tmp_path)
    assert result.returncode == 0, result.stderr


def test_e5_corrected_curve_keeps_reservations_and_identifiers(published):
    spec = importlib.util.spec_from_file_location('reviewed_led', published / 'methode/sheet_data.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    markers = module.SHEETS['E-5']['markers']
    assert [m['id'] for m in markers] == [f'E-5-{i:03}' for i in range(1, 73)]
    assert sum(m['family'] == 'F' for m in markers) == 5
    assert sum(m['family'] == 'AL' for m in markers) == 14
    assert all('DO NOT USE FOR CONSTRUCTION' in m['reserve'] and m['scope'] == 'À PRÉCISER' for m in markers)
    curve = markers[-1]
    assert curve['family'] == 'F' and curve['parent'] == 'P1-25'
    assert 907 < curve['x'] * 8255 / 1800 < 1173
    assert 3291 < curve['y'] * 8255 / 1800 < 3550
