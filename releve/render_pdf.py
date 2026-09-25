# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "pillow>=10", "markdown>=3.6"]
# ///
"""Étape 4 (déterministe) : PDF « Plans annotés » (même présentation que l'export Plan Expert : fond du plan,
marques colorées par famille, légende à droite) + « Rapport de métré (par plans) » + dossier complet.

Usage : uv run releve/render_pdf.py WORKDIR NOM_PROJET SORTIE_DIR
Sorties : SORTIE_DIR/<NOM>-Plans-annotes.pdf, <NOM>-Rapport-de-metre.pdf (+ .md), <NOM>-Dossier-complet.pdf
"""
import os, sys, io, collections, datetime, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf, markdown
from PIL import Image, ImageDraw
from commun import load_nomenclature, load_occurrences, load_feuilles, draw_mark, sha256
from prepare import font
Image.MAX_IMAGE_PIXELS = None
PAGE_W = 2997          # largeur de page de l'export Plan Expert (pt)
MARK_R = 9             # rayon des marques (px à 2997 de large)

def annotate_sheet(work, f, info, occ_f, nom):
    im = Image.open(os.path.join(work, "rasters", f + ".png")).convert("RGB")
    W = float(info["largeur_pt"]); H = float(info["hauteur_pt"])
    k = PAGE_W / W
    im = im.resize((PAGE_W, int(round(H * k))), Image.LANCZOS)
    dr = ImageDraw.Draw(im, "RGBA")
    counts = collections.Counter()
    for o in occ_f:
        n = nom[o["label"]]
        draw_mark(dr, n["forme"], o["x"] * k, o["y"] * k, MARK_R, n["rgb"], outline=(30, 30, 30), width=2)
        counts[o["label"]] += 1
    if counts:
        rows = sorted(counts)
        fnt = font(22)
        lh = 30
        tw = max(dr.textlength(f"{l}  ({counts[l]})", font=fnt) for l in rows) + 70
        x0, y0 = int(im.width * 0.746), int(im.height * 0.336)
        x0 = min(x0, im.width - int(tw) - 20)
        bh = lh * len(rows) + 60
        dr.rectangle([x0, y0, x0 + tw, y0 + bh], fill=(255, 255, 255, 235), outline=(0, 0, 0, 255), width=3)
        dr.text((x0 + 15, y0 + 10), f"Légende — {info.get('nom', f)} ({sum(counts.values())} marques)", fill=(0, 0, 0, 255), font=font(22))
        for i, l in enumerate(rows):
            n = nom[l]; y = y0 + 50 + i * lh
            draw_mark(dr, n["forme"], x0 + 25, y + 10, 10, n["rgb"], outline=(30, 30, 30), width=2)
            dr.text((x0 + 45, y - 2), f"{l}  ({counts[l]})", fill=(0, 0, 0, 255), font=fnt)
    return im, counts

def md_to_pdf(md_text):
    body = markdown.markdown(md_text, extensions=["tables"])
    css = ("body{font-family:sans-serif;font-size:9.5pt;line-height:1.35} h1{font-size:18pt;border-bottom:2px solid #222} h2{font-size:13pt;color:#B4532A;margin-top:14pt}"
           "h3{font-size:11pt} table{border-collapse:collapse;width:100%;font-size:8.5pt} th,td{border:1px solid #999;padding:2px 5px;vertical-align:top} th{background:#eef1f4;text-align:left} code{font-size:8.5pt}")
    story = pymupdf.Story(html=f"<html><body>{body}</body></html>", user_css=css)
    buf = io.BytesIO()
    writer = pymupdf.DocumentWriter(buf)   # API Story : DocumentWriter.begin_page → Story.place/draw → end_page
    rect = pymupdf.Rect(36, 36, 559, 806)   # A4 portrait
    more = True
    while more:
        dev = writer.begin_page(pymupdf.Rect(0, 0, 595, 842))
        more, _ = story.place(rect)
        story.draw(dev)
        writer.end_page()
    writer.close()
    return pymupdf.open("pdf", buf.getvalue())

def main(work, name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    nom = load_nomenclature(work); occ = load_occurrences(work); feuilles = load_feuilles(work)
    by_sheet = collections.defaultdict(list)
    for o in occ:
        by_sheet[o["feuille"]].append(o)
    sheets = sorted(f for f in feuilles if feuilles[f].get("type") == "plan" or by_sheet.get(f))
    plans = pymupdf.open(); per_sheet = {}; grand = collections.Counter()
    for f in sheets:
        im, counts = annotate_sheet(work, f, feuilles[f], by_sheet.get(f, []), nom)
        per_sheet[f] = counts; grand.update(counts)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=85, subsampling=0)
        pg = plans.new_page(width=im.width, height=im.height); pg.insert_image(pg.rect, stream=buf.getvalue())
        print(f"  {f}: {sum(counts.values())} marques", flush=True)
    p_plans = os.path.join(out_dir, f"{name}-Plans-annotes.pdf")
    plans.save(p_plans, garbage=3, deflate=True)
    # --- rapport de métré
    today = datetime.date.today().strftime("%Y-%m-%d")
    L = [f"# Rapport de métré (par plans) — {name}", "", f"Généré le {today} par le pipeline `releve/` (relevé automatique Claude + scripts déterministes). "
         "Chaque marque est une occurrence relevée sur le plan (étiquette texte vectorielle ou lecture visuelle) ; les quantités sont des comptes d'objets, sans métrage de câble.", ""]
    L += ["## Résumé", "", "| Feuille | Marques | Libellés |", "|---|--:|--:|"]
    for f in sheets:
        L.append(f"| {feuilles[f].get('nom', f)} | {sum(per_sheet[f].values())} | {len(per_sheet[f])} |")
    L.append(f"| **Total** | **{sum(grand.values())}** | **{len(grand)}** |")
    L += ["", "## Tous les plans", "", "| Libellé | Famille | Quantité |", "|---|---|--:|"]
    for l in sorted(grand):
        L.append(f"| {html.escape(l)} | {nom[l]['famille']} | {grand[l]} |")
    for f in sheets:
        if not per_sheet[f]:
            continue
        L += ["", f"## {feuilles[f].get('nom', f)}", "", "| Libellé | Ce plan | Tous les plans |", "|---|--:|--:|"]
        for l in sorted(per_sheet[f]):
            L.append(f"| {html.escape(l)} | {per_sheet[f][l]} | {grand[l]} |")
    L += ["", "## Nomenclature (libellé → source de la lecture)", "", "| Libellé | Famille | Description | Source |", "|---|---|---|---|"]
    for l in sorted(nom):
        n = nom[l]; L.append(f"| {html.escape(l)} | {n['famille']} | {html.escape(n['description'])} | {html.escape(n['source'])} |")
    for extra, title in (("rapport-releve.md", "Méthode et constats de l'agent"), ("reserves.md", "Réserves"), ("comparaison-estimateur.md", "Comparaison avec le relevé de l'estimateur")):
        p = os.path.join(work, extra)
        if os.path.exists(p):
            L += ["", f"# {title}", "", open(p, encoding="utf-8").read()]
    md = "\n".join(L)
    open(os.path.join(out_dir, f"{name}-Rapport-de-metre.md"), "w", encoding="utf-8").write(md)
    rap = md_to_pdf(md)
    p_rap = os.path.join(out_dir, f"{name}-Rapport-de-metre.pdf"); rap.save(p_rap, garbage=3, deflate=True)
    # --- dossier complet
    full = pymupdf.open(); full.insert_pdf(rap); full.insert_pdf(pymupdf.open(p_plans))
    p_full = os.path.join(out_dir, f"{name}-Dossier-complet.pdf"); full.save(p_full, garbage=3, deflate=True)
    for p in (p_plans, p_rap, p_full):
        print(f"{os.path.basename(p)}  {os.path.getsize(p)} o  {len(pymupdf.open(p))} p  sha256 {sha256(p)}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
