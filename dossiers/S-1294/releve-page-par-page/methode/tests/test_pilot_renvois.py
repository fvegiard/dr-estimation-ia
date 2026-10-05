"""Delta graphique E203-0200/0201 : source externe explicitement requise.

S1294_TEST_SOURCE = PNG original page 16; S1294_TEST_JPEG = JPEG à contrôler;
S1294_TEST_REFERENCE = dossier pilote v1 gelé; S1294_TEST_DATA = données v2.
Ce test constate des pixels et des invariants, aucun taux d'exactitude métier.
"""
import hashlib, os, unittest
from pathlib import Path
from PIL import Image, ImageChops

D=Path(__file__).resolve().parents[2]
SOURCE=Path(os.environ.get('S1294_TEST_SOURCE',D/'sources/STAM23A - E - Pour construction - 2024-10-08 - 16.png'))
JPEG=Path(os.environ['S1294_TEST_JPEG'])
REFERENCE=Path(os.environ['S1294_TEST_REFERENCE'])
DATA=Path(os.environ.get('S1294_TEST_DATA',D))
SOURCE_SHA='98b9bedba7b38899b45d4da837b3893620f427685beb8099e9aff9e3d998005f'

class RenvoiDelta(unittest.TestCase):
    def test_11_both_source_notes_remain_without_colored_ink(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),SOURCE_SHA)
        with Image.open(SOURCE) as source, Image.open(JPEG) as output:
            scale=source.width/1920
            for ident,box in [('E203-0200',(295,145,414,162)),('E203-0201',(1302,144,1421,162))]:
                with self.subTest(id=ident):
                    native=tuple(round(v*scale) for v in box)
                    ink=source.crop(native).convert('L').point(lambda v:255 if v<128 else 0)
                    r,g,b=output.crop(native).convert('RGB').split()
                    color=ImageChops.lighter(ImageChops.difference(r,g),ImageChops.difference(g,b))
                    self.assertIsNone(ImageChops.multiply(color,ink).getbbox(),'Couleur sur les caractères noirs du renvoi source')

    def test_12_data_unchanged_from_v1(self):
        for name in ['E203-records.json','S-1294-E203-equipment.csv','S-1294-reprise-detail.csv','S-1294-reprise-par-panneau.xlsx']:
            with self.subTest(file=name):
                self.assertEqual((DATA/name).read_bytes(),(REFERENCE/name).read_bytes())

    def test_13_no_jpeg_change_outside_two_annotation_windows(self):
        with Image.open(REFERENCE/'S-1294-E203-pilote.jpg') as before,Image.open(JPEG) as after:
            self.assertEqual(before.size,after.size)
            difference=ImageChops.difference(before.convert('RGB'),after.convert('RGB'))
            scale=before.width/1920
            # Ces deux fenêtres englobent ancienne pastille, nouvelle pastille,
            # liaison et blocs JPEG touchés; aucune autre région ne peut varier.
            for box in [(347,122,361,159),(1360,122,1374,159)]:
                difference.paste((0,0,0),tuple(round(v*scale) for v in box))
            self.assertIsNone(difference.getbbox(),'Modification en dehors des deux renvois autorisés')

if __name__=='__main__':unittest.main(verbosity=2)
