"""Download plan files only; never read estimator projects."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'reference-repo'))
from src.apprentissage.sharepoint import MesProjets

LINK = 'https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/IgANwhkY6XozQqRGlFYpejPCASNd72FSk0lM4uryKdA3kHM'
SITE = 'https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com'
BASE = '/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets'

def main():
    client = MesProjets(lien=LINK, site=SITE, racine=BASE)
    matches = [p for p in client.projets() if p.lower().startswith('s-0844 ')]
    print('Matching projects:', matches, flush=True)
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one project')
    project = matches[0]
    pending = [(f'{BASE}/{project}', Path())]
    inventory, hashes = [], {}
    while pending:
        remote, relative = pending.pop()
        for item in client.fichiers(remote):
            name = item['Name']
            if Path(name).suffix.lower() not in {'.png', '.pdf'}:
                continue
            destination = ROOT / 'sources' / relative / name
            client.telecharger(remote + '/' + name, destination, int(item['Length']))
            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
            row = dict(remote=remote + '/' + name, bytes=destination.stat().st_size, sha256=digest)
            if digest in hashes:
                row['duplicate_of'] = hashes[digest]
                destination.unlink()
            else:
                hashes[digest] = str(destination.relative_to(ROOT))
                row['file'] = hashes[digest]
            inventory.append(row)
            (ROOT / 'source-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
            print(row, flush=True)
        for folder in client.dossiers(remote):
            if folder['Name'].lower() in {'prix', 'devis'}:
                continue
            pending.append((remote + '/' + folder['Name'], relative / folder['Name']))

if __name__ == '__main__':
    main()
