import glob, re, json, collections, os
from xml.etree import ElementTree as ET

def readq(p):
    b=open(p,'rb').read()
    for enc in ('utf-8-sig','utf-16','utf-8','latin-1'):
        try: return b.decode(enc)
        except: pass
    return b.decode('utf-8','replace')

fs=sorted(glob.glob('**/*.qpl',recursive=True))
rows=[]
counter_totals=collections.Counter()      # label -> total elements across corpus
counter_projects=collections.Counter()    # label -> nb projects using it
price_samples=collections.defaultdict(list)  # label -> list of costEach
bad=0
for p in fs:
    try:
        s=readq(p)
        root=ET.fromstring(s.encode('utf-8')) if not s.startswith('﻿') else ET.fromstring(s[1:].encode('utf-8'))
    except Exception as e:
        bad+=1; continue
    proj=root.find('Project')
    name=proj.findtext('Name','') if proj is not None else ''
    desc=(proj.findtext('Description','') or '') if proj is not None else ''
    created=proj.findtext('CreationDate','') if proj is not None else ''
    # counters: label -> (groupID, shape, defaultsize, nb elements)
    counters={}
    for c in root.iter('Counter'):
        lab=c.get('Name',''); gid=c.get('GroupID',''); 
        nel=len(list(c.findall('Element')))
        if lab not in counters: counters[lab]={'gid':gid,'shape':c.get('Shape',''),'n':0}
        counters[lab]['n']+=nel
    # prices: Key "gid;;Counter;" -> costEach, markup
    prices={}
    for pr in root.iter('Price'):
        key=pr.get('Key',''); m=re.match(r'(\d+);',key)
        if m: prices[m.group(1)]={'cost':float(pr.get('CostEach','0') or 0),'markup':float(pr.get('MarkupEach','0') or 0),'sys':pr.get('SystemType','')}
    total_el=sum(v['n'] for v in counters.values())
    priced=0; extended=0.0
    gid2lab={v['gid']:k for k,v in counters.items()}
    for gid,pd in prices.items():
        lab=gid2lab.get(gid)
        if lab and pd['cost']>0:
            n=counters[lab]['n']
            priced+=1; extended+=n*pd['cost']
            price_samples[lab].append(pd['cost'])
    for lab,v in counters.items():
        counter_totals[lab]+=v['n']
        if v['n']>0: counter_projects[lab]+=1
    rows.append({'file':p,'name':name,'desc':desc,'created':created,
                 'n_counters':len(counters),'n_elements':total_el,
                 'n_priced':priced,'extended_cost':round(extended,2)})
json.dump(rows,open('parsed.json','w'),ensure_ascii=False)
# summary
withmarks=[r for r in rows if r['n_elements']>0]
withprice=[r for r in rows if r['extended_cost']>0]
print(f"qpl total={len(fs)} parsed={len(rows)} unparseable={bad}")
print(f"avec marques (Elements>0) = {len(withmarks)}")
print(f"avec prix chiffré (extended>0) = {len(withprice)}")
print(f"marques distinctes dans le corpus = {len(counter_totals)}")
print("--- top 25 marques par nb total d'occurrences:")
for lab,n in counter_totals.most_common(25):
    ps=price_samples.get(lab,[])
    import statistics
    med=round(statistics.median(ps),2) if ps else None
    print(f"  {n:>7}  {counter_projects[lab]:>4} proj  prix méd={med}  {lab[:60]}")
