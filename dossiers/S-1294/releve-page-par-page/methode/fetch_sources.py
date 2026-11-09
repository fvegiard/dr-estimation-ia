"""Fetch only PDF/PNG source candidates; never read estimator project files."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'reference-repo'))
from src.apprentissage.sharepoint import MesProjets

LINK = 'https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/IgANwhkY6XozQqRGlFYpejPCASNd72FSk0lM4uryKdA3kHM'
SITE = 'https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com'
BASE = '/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets'

def main():
    client = MesProjets(lien=LINK, site=SITE, racine=BASE)
    project = 'S-1294 (10-Décembre-2024)'
    pending = [(BASE + '/' + project, Path())]
    records, hashes = [], {}
    while pending:
        remote, relative = pending.pop()
        for item in client.fichiers(remote):
            name = item['Name']
            if Path(name).suffix.lower() not in {'.png', '.pdf'}:
                continue
            target = ROOT / 'sources' / relative / name
            print('Downloading:', str(relative / name), flush=True)
            client.telecharger(item['ServerRelativeUrl'], target, int(item['Length']))
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            record = {'remote': item['ServerRelativeUrl'], 'file': str(target.relative_to(ROOT)),
                      'bytes': target.stat().st_size, 'sha256': digest}
            if digest in hashes:
                record['duplicate_of'] = hashes[digest]
                target.unlink()
            else:
                hashes[digest] = record['file']
            records.append(record)
            (ROOT / 'audit/source-inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
        for folder in client.dossiers(remote):
            if folder['Name'].casefold() in {'prix', 'devis'}:
                continue
            pending.append((folder['ServerRelativeUrl'], relative / folder['Name']))
    print('Unique source files:', len(hashes), flush=True)

if __name__ == '__main__':
    main()
