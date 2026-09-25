# sbs.py out.png titre img1 [img2 ...] : assemble côte à côte (ou en grille si >2) avec légendes
import sys
from PIL import Image, ImageDraw
out,title,*ims=sys.argv[1:]
imgs=[Image.open(i).convert('RGB') for i in ims]
cols=2 if len(imgs)>2 else len(imgs)
rows=(len(imgs)+cols-1)//cols
cw=max(i.width for i in imgs); ch=max(i.height for i in imgs)
W=cw*cols; H=ch*rows+40
c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c); d.text((10,10),title,fill=(0,0,0))
for k,i in enumerate(imgs):
    c.paste(i,((k%cols)*cw,40+(k//cols)*ch)); d.rectangle([(k%cols)*cw,40+(k//cols)*ch,(k%cols)*cw+i.width-1,40+(k//cols)*ch+i.height-1],outline=(150,150,150))
c.save(out); print(out,c.size)
