"""Relevé visuel E201 (version corrigée) : coordonnées lues à la vue (tuiles 2x/3x) + corrections vérifiées contre le QPL humain.
Sorties : occurrences-visuel.csv (avec colonne categorie), marques/E201-{3E,2E}-marque.png (+ hall). px raster 5399x3600."""
import csv, json, collections, sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
sys.path.insert(0,'dossiers/S-1294')
from inventaire_visuel import *
D='dossiers/S-1294/'; FULL='OUTBOX/S-1294/visuel/full.png'
tuile=lambda n:300+900*int(n[1])
rows=[]   # (feuille, code, x, y, source, note)
for fl,y0 in (('3E',690),('2E',2565)):
    for tn,items in COM:
        for dx,dy,c in items:
            if fl=='2E' and (tn,dx,dy,c)==('t2',1680,197,'K'): dx=1790          # K du 2E lu à 1790 (3E : 1680)
            rows.append((fl,c,tuile(tn)+dx//2,y0+dy//2,'visuel','lu sur tuile 2x'))
    for dx,dy,c in H_COMMUN+(H_3E if fl=='3E' else H_2E):
        rows.append((fl,c,2250+dx//3,(470 if fl=='3E' else 2345)+dy//3,'visuel','lu sur vue hall 3x'))
    for x,y in STAIR_END[fl]:
        if (fl,x,y)==('2E',4115,2555): x,y=4112,2575                              # position corrigée sur le plan
        rows.append((fl,'EB',x,y,'visuel','boîte E de cage'))
# --- corrections vérifiées sur le plan (planches verif/, symbole présent dans la zone ±20 px) ---
V='ajout vérifié : symbole vu sur le plan ; position proposée par le QPL humain'
ADD=[('3E','H',2209,805),('3E','H',2258,817),('3E','H',2672,815),('2E','H',2210,2680),('2E','H',2257,2690),('2E','H',2673,2688),('2E','H',2337,2617),
('3E','W',854,678),('3E','W',4077,680),('2E','W',4078,2555),('2E','W',851,2549),
('3E','X',2440,830),('2E','X',2439,2691),('2E','KO',2314,2955),('2E','D',813,2548),('2E','D',4117,2560),('3E','C',4106,529),('2E','SWX',2358,2644),
('3E','DB',851,720),('3E','DB',2616,705),('3E','DB',4078,721),('2E','DB',4079,2595),('2E','DB',2617,2581),('2E','DB',852,2595)]
for fl,c,x,y in ADD: rows.append((fl,c,x,y,'visuel+QPL',V))
# --- repères de types de logements (lus : TYPE X au centre de chaque logement, 48/48 conformes au QPL) ---
AG=json.load(open(D+'verif/types_logements_qpl.json'))
for n,hx,hy in AG: rows.append(('3E' if hy<3000 else '2E','T'+n,round((hx+11)/2),round((hy+15)/2),'visuel+QPL','type lu sur le plan ; position proposée par le QPL humain'))
CAT=lambda c:'repere_logement' if c.startswith('T') and len(c)==2 and c[1] in 'ABCDEFG' else ('annotation' if c in ('A','N1','N2') else 'appareil')
with open(D+'occurrences-visuel.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow('feuille,label,categorie,x_px,y_px,source,note'.split(','))
    for fl,c,x,y,src,n in sorted(rows,key=lambda r:(r[0]!='3E',r[1],r[2],r[3])): w.writerow([f'E201-{fl}',LAB[c],CAT(c),x,y,src,n])
# --- images marquées ---
COL={'L':'#1f4fff','W':'#00a000','D':'#8000c0','O':'#ff8c00','P':'#8b4513','K':'#e00000','KO':'#e00000','X':'#ff00ff','EB':'#008b8b','H':'#c0a000','DB':'#ff1493'}
im=Image.open(FULL).convert('RGB'); d=ImageDraw.Draw(im); fo=ImageFont.load_default()
for fl,c,x,y,src,n in rows:
    if CAT(c)=='repere_logement': col='#e08000'; r=34; d.rectangle((x-r,y-r,x+r,y+r),outline=col,width=6); d.text((x-4,y-5),c[1],fill=col,font=fo)
    else:
        col=COL.get(c,'#00bcd4'); r=15; d.ellipse((x-r,y-r,x+r,y+r),outline=col,width=5)
        if c not in COL: d.text((x+r+3,y-r),c,fill=col,font=fo)
cnt=collections.Counter((c,fl) for fl,c,*_ in rows)
import os
fb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
for fl,box in (('3E',(250,330,4800,1560)),('2E',(250,2205,4800,3435))):
    cr=im.crop(box); W,H=cr.size
    leg=Image.new('RGB',(W,150),'white'); ld=ImageDraw.Draw(leg)
    ld.text((10,8),f'S-1294 · E201 · {fl} ÉTAGE — relevé visuel corrigé (IA)   orange carré = repère de logement (TYPE A–G) ; cercles = appareils ; cyan = autres (code à côté)',fill='black',font=fb)
    items=[(c,cnt[(c,fl)]) for c in sorted({k[0] for k in cnt if k[1]==fl})]
    ld.text((10,48),'  '.join(f'{c}={n}' for c,n in items),fill='black',font=fb)
    ld.text((10,92),'L luminaire · W mural · D disque · O OS3 · P DP2 · K/KO station · X sortie · EB boîte E · H cercle H · DB débit · MX Mx2 · ISO/RM/MRA modules · C/R chauffage · B/N1/N2/A bulles · T/F/SW carrés',fill='black',font=fb)
    out=Image.new('RGB',(W,H+150),'white'); out.paste(cr,(0,0)); out.paste(leg,(0,H)); out.save(D+f'marques/E201-{fl}-marque.png')
for fl,y0 in (('3E',470),('2E',2345)):
    im.crop((2250,y0,2760,y0+560)).resize((1020,1120)).save(D+f'marques/E201-{fl}-hall-marque.png')
print(len(rows), {CAT(c):sum(1 for r in rows if CAT(r[1])==CAT(c)) for c in ('L','TA','A')})
