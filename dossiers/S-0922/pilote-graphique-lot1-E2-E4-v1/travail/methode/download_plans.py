"""Download only PNG/PDF source candidates; never access estimator QPL files."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if ROOT.name == 'methode':
    ROOT = ROOT.parent
# Le module partagé appartient au dépôt, les sources au dossier livré.
REPO = next((p for p in ROOT.parents if (p / 'src/apprentissage/sharepoint.py').is_file()), None)
if REPO is None:
    raise FileNotFoundError('Exécuter ce script dans le dépôt dr-estimation-ia contenant src/apprentissage/sharepoint.py.')
spec = importlib.util.spec_from_file_location('sharepoint', REPO / 'src/apprentissage/sharepoint.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = module.MesProjets(
    lien='https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/IgANwhkY6XozQqRGlFYpejPCASNd72FSk0lM4uryKdA3kHM',
    site='https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com',
    racine='/personal/ddupuis_dreelectrique_com/Documents/Documents/DANIEL-FRANCIS-JO/Mes projets',
)
project = 'S-0922 (31-Janvier-2024)'
pending = [client.racine + '/' + project]
inventory = []
seen = {}
while pending:
    folder = pending.pop()
    print('Listing:', folder, flush=True)
    for item in client.fichiers(folder):
        name = item['Name']
        if any(word in name.casefold() for word in ('relevé', 'releve', 'proposition')):
            continue
        if Path(name).suffix.lower() not in {'.png', '.pdf'}:
            continue
        remote = folder + '/' + name
        relative = remote.split('/' + project + '/', 1)[1]
        target = ROOT / 'sources' / relative
        client.telecharger(remote, target, int(item['Length']))
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        record = {'source': remote, 'bytes': target.stat().st_size, 'sha256': digest}
        if digest in seen:
            record['duplicate_of'] = seen[digest]
            target.unlink()
        else:
            seen[digest] = str(target.relative_to(ROOT))
        record['file'] = seen[digest]
        inventory.append(record)
        (ROOT / 'source-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')
        print(record, flush=True)
    for item in client.dossiers(folder):
        if item['Name'].casefold() not in {'prix', 'devis'}:
            pending.append(folder + '/' + item['Name'])
print('Unique source candidates:', len(seen), flush=True)
