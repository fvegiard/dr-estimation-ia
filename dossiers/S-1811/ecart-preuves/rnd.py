import csv,random,subprocess
T='/home/claude/releve-auto/runs/S-1811/OUTBOX/S-1811/travail/'
rows=[r for f in ['occurrences-texte.csv','occurrences-visuel.csv'] for r in csv.DictReader(open(T+f)) if r.get('exclure','')!='1']
random.seed(1811); s=random.sample(rows,10)
outs=[]
for i,r in enumerate(s,1):
    x,y=float(r['x_pt']),float(r['y_pt'])
    o=f'/tmp/claude-0/-home-claude/ee0971be-0747-5d2f-962e-a9f568c158d0/scratchpad/s{i}.png'
    subprocess.run(['python3',T+'ecart-preuves/crop.py',r['feuille'],str(x-45),str(y-35),str(x+45),str(y+35),o,'4','^'+r['label'].replace('(','\\(').replace(')','\\)')+'$'],check=True,capture_output=True)
    print(i,r['feuille'],r['label'],x,y,r['source'],r['note'][:50]); outs.append(o)
subprocess.run(['python3',T+'ecart-preuves/sbs.py',T+'ecart-preuves/06-echantillon-10-marques-seed1811.png','Echantillon seed 1811 (random.sample sur 811 marques actives), 1 a 10 de gauche a droite, haut en bas']+outs,check=True)
