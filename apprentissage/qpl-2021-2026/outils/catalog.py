import json, re, unicodedata, collections, glob, statistics
from xml.etree import ElementTree as ET
rows=json.load(open('parsed.json'))
def readq(p):
    b=open(p,'rb').read()
    for enc in ('utf-8-sig','utf-16','utf-8','latin-1'):
        try: return b.decode(enc)
        except: pass
    return b.decode('utf-8','replace')
def canon(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()
    s=re.sub(r'\s+',' ',s).strip()
    return s
# re-walk to get per-project canonical label counts + year
raw=collections.Counter(); proj=collections.Counter(); byyear=collections.defaultdict(collections.Counter)
projlabels=[]  # (name, year, {canon:count})
for r in rows:
    p=r['file']
    try: s=readq(p); root=ET.fromstring((s[1:] if s.startswith('﻿') else s).encode('utf-8'))
    except: continue
    yr=(r['created'] or '')[:4]
    lc=collections.Counter()
    for c in root.iter('Counter'):
        lab=canon(c.get('Name','')); n=len(c.findall('Element'))
        if not lab: continue
        lc[lab]+=n
    for lab,n in lc.items():
        raw[lab]+=n; proj[lab]+=1; 
        if yr.isdigit(): byyear[yr][lab]+=n
    projlabels.append({'name':r['name'],'desc':r['desc'],'year':yr,'labels':dict(lc),'total':sum(lc.values())})
json.dump(projlabels,open('projects.json','w'),ensure_ascii=False)
cat=[{'label':lab,'occ':raw[lab],'projets':proj[lab]} for lab in raw]
cat.sort(key=lambda x:-x['occ'])
json.dump(cat,open('catalog.json','w'),ensure_ascii=False)
print('canonical labels:',len(cat),' projets avec marques:',len([p for p in projlabels if p['total']>0]))
print('occurrences totales:',sum(raw.values()))
print('années présentes:',sorted(byyear))
# labels appearing in >=8 projects = "real" recurring symbols
recur=[c for c in cat if c['projets']>=8]
print('marques récurrentes (>=8 projets):',len(recur),'  couvrent',sum(c['occ'] for c in recur),'occ (',round(100*sum(c['occ'] for c in recur)/sum(raw.values())),'%)')
open('recurrents.json','w').write(json.dumps(recur,ensure_ascii=False))
for c in recur[:40]: print(f"  {c['occ']:>7} {c['projets']:>4}p  {c['label'][:55]}")
