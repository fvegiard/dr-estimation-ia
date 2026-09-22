import numpy as np, csv, sys
from PIL import Image
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
S=2997/2383.92
COL={'P1520':(253,182,53),'PRISE':(162,107,68),'GFI':(253,253,53),'MP':(253,53,53),'MT':(53,153,53),'TEL':(53,53,162),'50A':(153,53,153),'30A':(53,153,153),'COL':(240,155,240),'BORNE':(253,222,53),'NF':(253,178,149)}
def detect(page,keys,tol=30,minA=25):
    im=np.asarray(Image.open(f'p{page:02d}.png').convert('RGB')).astype(int)
    im[:, 2300:]=255
    out=[]
    for k in keys:
        c=np.array(COL[k])*0.75+64; m=(np.abs(im-c).max(axis=2)<tol)
        lab,n=ndimage.label(m)
        for i,sl in enumerate(ndimage.find_objects(lab)):
            a=(lab[sl]==i+1).sum()
            if a<minA: continue
            cy,cx=ndimage.center_of_mass(lab==i+1) if False else ((sl[0].start+sl[0].stop)/2,(sl[1].start+sl[1].stop)/2)
            out.append((k,cx/S,cy/S,a))
    return out
def v2(sheet,labels):
    r=[]
    for f in ['occurrences-texte.csv','occurrences-visuel.csv']:
        for row in csv.DictReader(open('/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/travail/'+f)):
            if row['feuille']==sheet and row['label'] in labels: r.append((row['label'],float(row['x_pt']),float(row['y_pt']),row['note']))
    return r
def match(D,A,R=30):
    if not D or not A: return [],list(range(len(D))),list(range(len(A)))
    C=np.array([[np.hypot(d[1]-a[1],d[2]-a[2]) for a in A] for d in D])
    C2=np.where(C<R,C,1e6); ri,ci=linear_sum_assignment(C2)
    pairs=[(i,j) for i,j in zip(ri,ci) if C2[i,j]<1e6]
    md={i for i,_ in pairs}; ma={j for _,j in pairs}
    return pairs,[i for i in range(len(D)) if i not in md],[j for j in range(len(A)) if j not in ma]
def dedup(D,r=7):
    out=[]
    for d in sorted(D,key=lambda d:-d[3]):
        if any(o[0]==d[0] and np.hypot(o[1]-d[1],o[2]-d[2])<r for o in out): continue
        out.append(d)
    return out
