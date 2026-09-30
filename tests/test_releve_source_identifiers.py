"""Source identifiers are distinct from contextual references and documented collisions."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

import pymupdf
import pytest

SPEC = importlib.util.spec_from_file_location('source_identifiers_qc', Path(__file__).resolve().parents[1] / 'releve/controle_qualite.py')
cq = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cq)


def write_rows(work, rows):
    fields = ['feuille', 'label', 'x_pt', 'y_pt', 'source', 'note']
    if any('repere' in row for row in rows):
        fields.append('repere')
    with (work / 'occurrences-visuel.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fixture(work):
    (work / 'feuilles.csv').write_text('feuille,largeur_pt,hauteur_pt\nP1,200,200\n', encoding='utf-8')
    (work / 'feuilles-classement.csv').write_text('feuille,type\nP1,plan\n', encoding='utf-8')
    (work / 'nomenclature.csv').write_text('label,famille,jeton_regex\nKLAXON,alarme,K\nG,autre,\n', encoding='utf-8')
    (work / 'reserves.md').write_text('G: aucun G dans cette fixture.\nSC-1: Identifiant imprime deux fois sur des appareils distincts.\n', encoding='utf-8')
    (work / 'rapport-releve.md').write_text('Synthetic source inspection fixture.', encoding='utf-8')
    rows = [dict(feuille='P1', label='KLAXON', x_pt=x, y_pt=y, source='visuel', note='[K1.1]')
            for x, y in [(20.5, 40.2), (100.5, 80.2)]]
    write_rows(work, rows)
    (work / 'feuilles').mkdir()
    (work / 'evidence').mkdir()
    with pymupdf.open() as doc:
        page = doc.new_page(width=200, height=200)
        for row in rows:
            x, y = row['x_pt'], row['y_pt']
            page.draw_rect(pymupdf.Rect(x - 3, y - 3, x + 3, y + 3))
            page.insert_text((x - 6, y - 6), 'K1.1', fontsize=6)
        doc.save(work / 'feuilles/P1.pdf')
        page.get_pixmap().save(work / 'evidence/pair.png')
    entry = dict(feuille='P1', repere='K1.1', source_sha256=hashlib.sha256((work / 'feuilles/P1.pdf').read_bytes()).hexdigest(),
        occurrences=[{key: row[key] for key in ('label', 'x_pt', 'y_pt')} for row in rows],
        reason='Two printed identifiers on separate source symbols', reserve_id='SC-1',
        reserve_text='Identifiant imprime deux fois sur des appareils distincts.',
        proof_images=[{'path': 'evidence/pair.png', 'sha256': hashlib.sha256((work / 'evidence/pair.png').read_bytes()).hexdigest()}])
    return rows, entry


def document(work, entry):
    (work / 'source-collisions.json').write_text(json.dumps({'collisions': [entry]}), encoding='utf-8')


@pytest.mark.parametrize('explicit', [False, True])
def test_contextual_reference_is_not_own_identifier(tmp_path, explicit):
    rows, _ = fixture(tmp_path)
    rows = [rows[0], dict(feuille='P1', label='G', x_pt=110.2, y_pt=120.7, source='visuel', note='carre G sous K1.1 hors legende')]
    if explicit:
        rows[0]['repere'] = 'K1.1'
        rows[1]['repere'] = ''
        rows[1]['note'] = '[K1.1] reference contextuelle, sans identifiant propre'
    write_rows(tmp_path, rows)
    result = cq.controler(str(tmp_path))
    assert result['conforme'], result['erreurs']
    assert 'K1.1' in (tmp_path / 'occurrences-visuel.csv').read_text()


def test_explicit_own_identifier_precedes_legacy_note(tmp_path):
    rows, _ = fixture(tmp_path)
    rows[0]['repere'], rows[1]['repere'] = 'K1.1', 'K1.2'
    write_rows(tmp_path, rows)
    assert cq.controler(str(tmp_path))['conforme']


@pytest.mark.parametrize('note,expected', [('[K1.1] appareil', True), ('K1.1 appareil', True),
    ('carre sous [K1.1]', False), ('voisin K1.1', False), ('K1.1autre', False)])
def test_only_own_leading_legacy_tag_is_used(note, expected):
    assert bool(cq.repere_propre({'note': note})) is expected


@pytest.mark.parametrize('value', ['[K1.1', 'K1.1]', 'sous K1.1', 'K1.1 autre'])
def test_malformed_explicit_identifier_fails_closed(tmp_path, value):
    rows, _ = fixture(tmp_path)
    rows = [rows[0]]
    rows[0]['repere'] = value
    write_rows(tmp_path, rows)
    assert any(error.startswith('Q4') for error in cq.controler(str(tmp_path))['erreurs'])


def test_complete_source_collision_is_visible_warning_and_reserve(tmp_path):
    _, entry = fixture(tmp_path)
    document(tmp_path, entry)
    result = cq.controler(str(tmp_path))
    assert result['conforme'], result['erreurs']
    assert any('SC-1' in warning and 'K1.1' in warning for warning in result['avertissements'])


@pytest.mark.parametrize('damage', ['no_proof', 'wrong_source_hash', 'wrong_image_hash', 'missing_image', 'outside_image',
    'third_row', 'wrong_label', 'wrong_position', 'no_reason', 'no_reserve', 'spatial_duplicate', 'duplicate_manifest'])
def test_incomplete_stale_or_spatial_collision_remains_blocking(tmp_path, damage):
    rows, entry = fixture(tmp_path)
    if damage == 'no_proof': entry['proof_images'] = []
    elif damage == 'wrong_source_hash': entry['source_sha256'] = '0' * 64
    elif damage == 'wrong_image_hash': entry['proof_images'][0]['sha256'] = '0' * 64
    elif damage == 'missing_image': (tmp_path / 'evidence/pair.png').unlink()
    elif damage == 'outside_image': entry['proof_images'][0]['path'] = '../pair.png'
    elif damage == 'third_row': rows.append({**rows[0], 'x_pt': 150.3, 'y_pt': 160.9})
    elif damage == 'wrong_label': entry['occurrences'][0]['label'] = 'G'
    elif damage == 'wrong_position': entry['occurrences'][0]['x_pt'] += .01
    elif damage == 'no_reason': entry['reason'] = ''
    elif damage == 'no_reserve': (tmp_path / 'reserves.md').write_text('G absent. No documented collision.')
    elif damage == 'spatial_duplicate':
        rows[1]['x_pt'], rows[1]['y_pt'] = rows[0]['x_pt'] + 1, rows[0]['y_pt'] + 1
        entry['occurrences'][1].update(x_pt=rows[1]['x_pt'], y_pt=rows[1]['y_pt'])
    write_rows(tmp_path, rows)
    document(tmp_path, entry)
    if damage == 'duplicate_manifest':
        (tmp_path / 'source-collisions.json').write_text(json.dumps({'collisions': [entry, entry]}))
    result = cq.controler(str(tmp_path))
    assert any(error.startswith('Q5') for error in result['erreurs']), result


def test_free_text_duplicate_claim_does_not_waive_q5(tmp_path):
    fixture(tmp_path)
    with (tmp_path / 'reserves.md').open('a') as stream:
        stream.write('K1.1 est en double au plan, donc accepter les deux.\n')
    assert any(error.startswith('Q5') for error in cq.controler(str(tmp_path))['erreurs'])


@pytest.mark.parametrize('manifest', ['null', '[]', '{broken', '{"collisions":[null]}',
                                   '{"collisions":[{"feuille":[],"repere":"K1.1"}]}'])
def test_malformed_proof_manifest_fails_closed(tmp_path, manifest):
    fixture(tmp_path)
    (tmp_path / 'source-collisions.json').write_text(manifest, encoding='utf-8')
    assert any(error.startswith('Q5') for error in cq.controler(str(tmp_path))['erreurs'])


def test_truncated_png_with_valid_header_and_matching_hash_is_rejected(tmp_path):
    _, entry = fixture(tmp_path)
    proof = tmp_path / 'evidence/pair.png'
    proof.write_bytes(proof.read_bytes()[:24])
    entry['proof_images'][0]['sha256'] = hashlib.sha256(proof.read_bytes()).hexdigest()
    document(tmp_path, entry)
    assert any(error.startswith('Q5') for error in cq.controler(str(tmp_path))['erreurs'])
