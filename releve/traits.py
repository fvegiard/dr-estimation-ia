# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Outil de l'agent : nature vectorielle d'une zone du plan (neuf vs existant, texte vs tracé).

    uv run releve/traits.py WORKDIR FEUILLE x_pt y_pt [rayon_pt=12]

Liste, dans le rayon donné autour du point (coordonnées PDF en points), les mots de texte (police, taille, couleur)
et les tracés vectoriels (épaisseur de trait, couleur, remplissage, pointillé, taille de la boîte). Un appareil NEUF est
en général du texte noir ou un tracé plein noir d'épaisseur normale ; un EXISTANT est gris, fin, hachuré ou pointillé
(audit S-1769 du 2026-09-22 : le « $ » existant était un tracé à 0,48 pt sans cercle, les neufs du texte ArialMT + barre 0,96 pt).
Rien n'est interprété ici : l'agent conclut.
"""
from __future__ import annotations
import csv, os, sys
import pymupdf

def gris(c):
    if c is None: return "sans"
    r, g, b = (int(round(v * 255)) for v in c)
    return f"#{r:02x}{g:02x}{b:02x}" + (" (gris)" if abs(r - g) < 12 and abs(g - b) < 12 and 40 < r < 215 else (" (noir)" if r < 40 and g < 40 and b < 40 else ""))

def main(work, feuille, x, y, rayon=12.0):
    row = next((r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8")) if r["feuille"] == feuille), None)
    if not row:
        sys.exit(f"feuille inconnue : {feuille}")
    src = None
    # le chemin source est dans inventaire : feuilles.csv donne fichier + page (relatifs à l'INBOX de run.py)
    for cand in (os.environ.get("RELEVE_INBOX"), os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(work))), "INBOX")):
        if not cand: continue
        for dp, _, fs in os.walk(cand):
            for f in fs:
                if os.path.join(dp, f).endswith(row["fichier"].replace("\\", "/")):
                    src = os.path.join(dp, f)
    if not src:
        sys.exit(f"PDF source introuvable pour {row['fichier']} (définir RELEVE_INBOX)")
    page = pymupdf.open(src)[int(row["page"]) - 1]
    z = pymupdf.Rect(x - rayon, y - rayon, x + rayon, y + rayon) * page.derotation_matrix   # repère tourné → repère natif
    z.normalize()
    print(f"# {feuille} = {row['fichier']} page {row['page']} ; zone {z}")
    print("## Texte")
    for b in page.get_text("dict", clip=z).get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                c = s["color"]; col = f"#{c:06x}"
                print(f"  « {s['text']} »  police={s['font']} taille={s['size']:.1f} couleur={col} bbox={[round(v, 1) for v in s['bbox']]}")
    print("## Tracés")
    n = 0
    for d in page.get_drawings():
        r = d["rect"]
        if not r.intersects(z): continue
        n += 1
        if n > 40:
            print("  … (plus de 40 tracés, zone trop large)"); break
        print(f"  type={d['type']} épaisseur={d.get('width')} trait={gris(d.get('color'))} remplissage={gris(d.get('fill'))} "
              f"pointillé={'oui' if d.get('dashes') and d['dashes'] not in ('[] 0', '', None) else 'non'} "
              f"boîte={r.width:.1f}×{r.height:.1f} pt à ({r.x0:.1f},{r.y0:.1f}) items={len(d.get('items', []))}")
    if n == 0:
        print("  aucun tracé dans la zone")

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4: sys.exit(__doc__)
    main(a[0], a[1], float(a[2]), float(a[3]), float(a[4]) if len(a) > 4 else 12.0)
