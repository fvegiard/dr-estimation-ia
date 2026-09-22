#!/usr/bin/env python3
"""
vectoriel.py — repère les symboles répétés d'une feuille PDF vectorielle
(plans CAD) en regroupant les tracés par signature géométrique, et sort
leurs coordonnées.

Porté depuis `dr-releves-2026/outils/vectoriel/symboles_vectoriels.py`
(voir docs/consolidation.md).

Usage :
  python -m src.releve.vectoriel --pdf E.pdf --page 4 --out E4-clusters.json \
      --planches E4-planches [--dpi 300] [--min 2] [--max 60] [--top 40] [--zone x0,y0,x1,y1]

Sortie :
  - JSON : liste de clusters {id, n, w_pt, h_pt, items, signature,
    centres_pt:[[x,y],...], centres_px:[[x,y],...]}
    (px = pt * dpi / 72, origine en haut à gauche comme le raster de
    `src.releve raster`)
  - un PNG « planche » par cluster : 8 exemplaires découpés dans la page
    (pour identifier le symbole à l'œil ou avec un outil de vision et
    l'associer à la légende).
Règle : ce script ne décide rien. Il propose des groupes ; l'association
groupe → symbole de légende et la validation (recomptage visuel) restent
à faire et à prouver.
"""
import argparse, json, os, collections
import fitz  # pymupdf


def signature(dr, q=0.5):
    r = dr["rect"]
    w = round(r.width / q) * q
    h = round(r.height / q) * q
    kinds = "".join(it[0] for it in dr["items"])
    return (w, h, len(dr["items"]), kinds[:12])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--page", type=int, required=True, help="1-based")
    ap.add_argument("--out", required=True)
    ap.add_argument("--planches", default=None, help="dossier des planches PNG")
    ap.add_argument("--dpi", type=float, default=300)
    ap.add_argument("--min", type=float, default=2.0, help="taille min (pt) d'un tracé")
    ap.add_argument("--max", type=float, default=60.0, help="taille max (pt) d'un tracé")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--minn", type=int, default=3, help="occurrences min pour garder un cluster")
    ap.add_argument("--zone", default=None, help="x0,y0,x1,y1 en pt : ignorer hors zone (ex. exclure légende/cartouche)")
    a = ap.parse_args()

    doc = fitz.open(a.pdf)
    page = doc[a.page - 1]
    zone = fitz.Rect(*[float(v) for v in a.zone.split(",")]) if a.zone else None
    groups = collections.defaultdict(list)
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.width < a.min or r.height < a.min or r.width > a.max or r.height > a.max:
            continue
        if zone and not zone.contains(fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)):
            continue
        groups[signature(dr)].append(r)

    k = a.dpi / 72.0
    clusters = []
    for sig, rects in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(rects) < a.minn:
            continue
        centres = [[round((r.x0 + r.x1) / 2, 2), round((r.y0 + r.y1) / 2, 2)] for r in rects]
        clusters.append({
            "id": f"C{len(clusters)+1:03d}",
            "n": len(rects),
            "w_pt": sig[0], "h_pt": sig[1], "items": sig[2], "signature": sig[3],
            "centres_pt": centres,
            "centres_px": [[round(x * k, 1), round(y * k, 1)] for x, y in centres],
        })
        if len(clusters) >= a.top:
            break

    meta = {"pdf": os.path.basename(a.pdf), "page": a.page, "page_pt": [page.rect.width, page.rect.height],
            "dpi": a.dpi, "px_par_pt": k, "zone": a.zone, "nb_clusters": len(clusters)}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "clusters": clusters}, f, ensure_ascii=False, indent=1)

    if a.planches:
        from PIL import Image
        os.makedirs(a.planches, exist_ok=True)
        for c in clusters:
            tiles = []
            for (x, y) in c["centres_pt"][:8]:
                pad = max(c["w_pt"], c["h_pt"]) * 1.5 + 6
                clip = fitz.Rect(x - pad, y - pad, x + pad, y + pad) & page.rect
                pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False)
                tiles.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
            if not tiles:
                continue
            tw = max(t.width for t in tiles); th = max(t.height for t in tiles)
            sheet = Image.new("RGB", (tw * len(tiles) + 4 * (len(tiles) - 1), th), (255, 255, 255))
            for i, t in enumerate(tiles):
                sheet.paste(t, (i * (tw + 4), 0))
            sheet.save(os.path.join(a.planches, f"{c['id']}_n{c['n']}_{c['w_pt']}x{c['h_pt']}.png"))

    print(json.dumps(meta, ensure_ascii=False))
    for c in clusters[:15]:
        print(c["id"], c["n"], f"{c['w_pt']}x{c['h_pt']}pt", c["items"], c["signature"])


if __name__ == "__main__":
    main()
