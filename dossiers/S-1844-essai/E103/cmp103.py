import sys
import csv
import re
sys.path.insert(0,'.')
import numpy as np
from pathlib import Path
from scipy.optimize import linear_sum_assignment
from src.validation.compare_qpl import lire_qpl
plans=lire_qpl(Path(sys.argv[1]),'humain')
p=[q for q in plans if 'POUR SOUMISSION-page-00006' in q.nom][0]
H=np.array([[m.x,m.y] for m in p.marques]);Hl=[m.libelle for m in p.marques]
rows=list(csv.DictReader(open('dossiers/S-1844-essai/E103/occurrences-visuel.csv')))
I=np.array([[float(r['x_pt']),float(r['y_pt'])] for r in rows]);Il=[r['label'].split(' - ')[0] for r in rows]
nn=[re.search(r'#(\d+)',r['note']).group(1) for r in rows]
# fit scale+translation via least squares after coarse s
s=np.median(H[:,1].max()/I[:,1].max())
def fit(s,t=(0,0)):
    D=np.linalg.norm(H[:,None]-(I*s+t)[None],axis=2);r,c=linear_sum_assignment(D);return r,c,D
s=4777/2299.2
for it in range(3):
    r,c,D=fit(s)
    A=np.c_[I[c].ravel()]
    # global scale/translation LSQ
    X=np.c_[I[c,0],np.ones(len(c))];sx,tx=np.linalg.lstsq(X,H[r,0],rcond=None)[0]
    Y=np.c_[I[c,1],np.ones(len(c))];sy,ty=np.linalg.lstsq(Y,H[r,1],rcond=None)[0]
    I2=np.c_[I[:,0]*sx+tx,I[:,1]*sy+ty]
    D=np.linalg.norm(H[:,None]-I2[None],axis=2);r,c=linear_sum_assignment(D)
    s=sy
print('scale',sx,sy,tx,ty)
diag=np.hypot(sx*3456,sy*2592)
print('seuil 1.2% diag px',0.012*diag)
for a,b in sorted(zip(r,c),key=lambda z:z[1]):
    print(nn[b],Il[b],'<->',Hl[a],round(D[a,b]/diag*100,2),'%')
print('non appariés H',[Hl[i] for i in range(len(H)) if i not in r])
print('non appariés IA',[nn[i] for i in range(len(I)) if i not in c])
