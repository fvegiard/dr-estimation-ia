"""Delta local de l'étoile, contrôlé sur les pixels réellement rendus."""
import hashlib
import json
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT.parent / 'pilote-graphique-E3-v1'


def test_v1_frozen_files_remain_identical():
    frozen = json.loads((V1 / 'CHECKPOINT-PILOTE-E3.json').read_text(encoding='utf-8'))
    for record in frozen['frozen_files']:
        assert hashlib.sha256((V1 / record['file']).read_bytes()).hexdigest() == record['sha256']
    assert hashlib.sha256(Path(frozen['archive']).read_bytes()).hexdigest() == frozen['sha256']


def test_only_the_star_neighbourhood_changes_on_the_page():
    proof = json.loads((ROOT / 'preuves/delta-pixels-E3-188.json').read_text(encoding='utf-8'))
    with Image.open(V1 / 'paquet/S-0922-E-3-releve.jpg') as before, \
         Image.open(ROOT / 'paquet/S-0922-E-3-releve.jpg') as after:
        assert before.size == after.size == (12623, 9467)
        difference = ImageChops.difference(before, after)
        assert difference.getbbox() is not None
        ImageDraw.Draw(difference).rectangle(proof['local_comparison_mask_px'], fill=(0, 0, 0))
        assert difference.getbbox() is None


def test_star_moves_from_circuit_text_to_white_source_region():
    proof = json.loads((ROOT / 'preuves/delta-pixels-E3-188.json').read_text(encoding='utf-8'))
    with Image.open(ROOT / 'travail/sources/23-357-E-CO-CH-E1 (1) - 3.png') as source, \
         Image.open(ROOT / 'paquet/S-0922-E-3-releve.jpg') as output:
        assert sum(source.crop(proof['new_star_bbox_px']).convert('L').histogram()[:200]) == 0
        new_star = output.crop(proof['new_star_bbox_px']).convert('RGB')
        assert any(g - r > 40 and b - r > 40 for r, g, b in new_star.get_flattened_data())
        # Le texte source possède déjà des franges colorées. Comparer les pixels
        # source réencodés, dans une fenêtre alignée sur les blocs JPEG 8 x 8.
        old_region = (5664, 5760, 5696, 5808)
        encoded = BytesIO()
        source.crop(old_region).convert('RGB').save(encoded, format='JPEG', quality=96, subsampling=0)
        encoded.seek(0)
        with Image.open(encoded) as expected:
            assert ImageChops.difference(expected, output.crop(old_region)).getbbox() is None
