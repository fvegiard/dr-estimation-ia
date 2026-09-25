import pymupdf,sys,json
doc=pymupdf.open('01-PLANS.pdf')
res={}
for pg in range(22,32):
    p=doc[pg]; name='E3%02d'%(pg-22)
    ds=p.get_drawings()
    circ=[d for d in ds if d['type']=='s' and len(d['items'])==4 and all(i[0]=='c' for i in d['items']) and 7<d['rect'].width<11 and 7<d['rect'].height<11]
    lines=[d for d in ds if d['type']=='s' and len(d['items'])==1 and d['items'][0][0]=='l' and 5<d['rect'].width<8 and 5<d['rect'].height<8]
    found=[]
    for c in circ:
        inner=[l for l in lines if c['rect'].contains(l['rect'])]
        if len(inner)>=2:
            ctr=(c['rect'].tl+c['rect'].br)/2*p.rotation_matrix
            found.append((round(ctr.x,1),round(ctr.y,1)))
    # dedupe
    ded=[]
    for f in found:
        if all(abs(f[0]-g[0])>2 or abs(f[1]-g[1])>2 for g in ded): ded.append(f)
    res[name]=ded
    print(name,len(circ),len(ded))
json.dump(res,open(sys.argv[1],'w'))
