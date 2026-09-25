import numpy as np
from PIL import Image
from scipy import ndimage
R=5694/2383.92
def reds(sheet):
    im=np.asarray(Image.open(f'/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/travail/rasters/{sheet}.png').convert('RGB')).astype(int)
    m=(im[:,:,0]>230)&(im[:,:,1]<140)&(im[:,:,2]<100)
    m[:, int(2000*R):]=False
    m=ndimage.binary_closing(m,iterations=1)
    lab,n=ndimage.label(m)
    out=[]
    for i,sl in enumerate(ndimage.find_objects(lab)):
        h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
        a=(lab[sl]==i+1).sum()
        out.append(((sl[1].start+sl[1].stop)/2/R,(sl[0].start+sl[0].stop)/2/R,w,h,a/(w*h)))
    return out
