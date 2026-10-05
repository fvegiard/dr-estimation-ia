"""Régressions bornées à S-1294, sans QPL humain ni taux métier synthétique.

Le témoin 0082 provient de la source E203 p16 inspectée : circuit 8 à
(3448.76, 2673.48). Il est indépendant du CSV et du classeur.
"""
import csv, json, os, shutil, subprocess, sys, tempfile, unittest
import importlib.util
from pathlib import Path
from openpyxl import load_workbook
from PIL import Image

D=Path(__file__).resolve().parents[2]
DATA=Path(os.environ.get('S1294_TEST_DATA',D))
PILOT=Path(os.environ.get('S1294_TEST_JPEG',D/'S-1294-E203-releve.jpg'))
SOURCE=Path(os.environ.get('S1294_TEST_SOURCE',D/'sources/STAM23A - E - Pour construction - 2024-10-08 - 16.png'))

def witness_errors(rows):
    matches=[r for r in rows if r.get('Repère / source')=='E203-0082']
    if len(matches)!=1:
        return ['Témoin source E203-0082 absent ou dupliqué']
    return [] if str(matches[0].get('Circuits',''))=='8' else ['Circuit 8 omis']

class SourceRegression(unittest.TestCase):
    def test_01_circuit_8_in_csv(self):
        with (DATA/'S-1294-E203-equipment.csv').open(encoding='utf-8-sig',newline='') as f:
            self.assertEqual(witness_errors(list(csv.DictReader(f))),[])

    def test_02_circuit_8_in_workbook(self):
        book=load_workbook(DATA/'S-1294-reprise-par-panneau.xlsx',read_only=True)
        sheet=book['Relevés huit feuilles']
        self.assertEqual(sheet['B1120'].value,'E203-0082')
        self.assertEqual(str(sheet['M1120'].value),'8')
        book.close()

    def test_03_common_omission_is_not_evidence(self):
        csv_rows=[{'Repère / source':'E203-0082','Circuits':''}]
        book_rows=[{'Repère / source':'E203-0082','Circuits':''}]
        self.assertEqual(csv_rows,book_rows)
        self.assertEqual(witness_errors(csv_rows),['Circuit 8 omis'])
        self.assertEqual(witness_errors(book_rows),['Circuit 8 omis'])

    def test_04_missing_expected_object_is_detected(self):
        self.assertEqual(witness_errors([]),['Témoin source E203-0082 absent ou dupliqué'])

    def test_05_full_sheet_has_no_external_band(self):
        with Image.open(SOURCE) as source, Image.open(PILOT) as output:
            self.assertEqual(output.size,source.size,'Bande externe / feuille redimensionnée')

class ValidatorRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        for name in ['methode','audit/E203','sources']:
            (cls.root/name).mkdir(parents=True,exist_ok=True)
        shutil.copy2(D/'methode/validate_sheet.py',cls.root/'methode/validate_sheet.py')
        cls.initial={'completed':[],'remaining':['E203','E201'],'status':'Relevé en cours'}
        (cls.root/'CHECKPOINT.json').write_text(json.dumps(cls.initial),'utf-8')
        data={'page':16,'type':'equipment','records':[{'id':'E203-0082','family':'Témoin synthétique','quantity':1,'circuits':'8'}]}
        (cls.root/'audit/E203-records.json').write_text(json.dumps(data),'utf-8')
        with (cls.root/'S-1294-E203-equipment.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f);w.writerow(['Repère / source','Matériel','Qté','Circuits']);w.writerow(['E203-0082','Témoin synthétique',1,'8'])
        Image.new('RGB',(40,30),'white').save(cls.root/'sources/STAM23A - E - Pour construction - 2024-10-08 - 16.png')
        Image.new('RGB',(40,50),'white').save(cls.root/'S-1294-E203-releve.jpg')
        result=subprocess.run([sys.executable,str(cls.root/'methode/validate_sheet.py'),'E203','Essai sans preuve visuelle indépendante'],capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        cls.report=json.loads((cls.root/'audit/E203/verification.json').read_text('utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_06_count_over_itself_is_not_a_visual_score(self):
        self.assertNotIn('visual_score',self.report)

    def test_07_partial_automatic_check_cannot_complete_page(self):
        self.assertEqual(json.loads((self.root/'CHECKPOINT.json').read_text('utf-8')),self.initial)

    def validator_module(self):
        spec=importlib.util.spec_from_file_location('validator',D/'methode/validate_sheet.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_08_modified_jpeg_invalidates_prior_report(self):
        module=self.validator_module()
        image=self.root/'S-1294-E203-releve.jpg';before=image.read_bytes()
        self.assertTrue(module.report_is_current(self.report,self.root))
        try:
            image.write_bytes(before+b'changed')
            self.assertFalse(module.report_is_current(self.report,self.root))
        finally:
            image.write_bytes(before)

    def test_09_missing_proof_invalidates_prior_report(self):
        module=self.validator_module()
        report=json.loads(json.dumps(self.report))
        report['files'].append({'path':'proof-missing.png','sha256':'0'*64})
        self.assertFalse(module.report_is_current(report,self.root))

    def test_10_geometric_defect_is_reported_without_business_pass(self):
        self.assertEqual(self.report['checks']['sheet_dimensions']['status'],'FAIL')
        self.assertEqual(self.report['business_accuracy'],'non démontrée')
        self.assertEqual(self.report['acceptance'],'non prononcée')

if __name__=='__main__':
    unittest.main(verbosity=2)
