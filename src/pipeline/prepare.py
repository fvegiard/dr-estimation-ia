"""Étape 1 (déterministe) : inventaire d'un dossier de soumission et préparation du travail.

Porté depuis planexpert-core/releve/prepare.py (imports relatifs de package).

Usage : python -m src.pipeline.prepare INBOX_DIR WORKDIR

Entrée  : INBOX_DIR = dossier déposé par Francis (PDF de plans, addendas, relevé de l'estimateur…).
Sortie  : WORKDIR/
  inventaire.json         chaque fichier d'entrée : taille, sha256, pages, classement (plans / estimateur / addenda / autre)
  feuilles.csv            une ligne par page de plan : feuille, fichier source, page, taille pt, nb de mots, jetons fréquents
  feuilles/<F>.pdf        la page seule (vectorielle, telle quelle)
  rasters/<F>.png         raster 5694 px de large (convention Plan Expert : px = pt × 5694 / largeur_pt)
  apercus/<F>.png         aperçu 1600 px pour lecture rapide
  tuiles/<F>/rXcY.png     tuiles 3 × 4 avec règles graduées en points PDF (pour la lecture visuelle)
  texte/<F>-mots.csv      tous les mots vectoriels avec leur boîte (points PDF, origine haut-gauche)
  texte/<F>-jetons.csv    fréquence des jetons (pour repérer les étiquettes d'appareils)
  estimateur/             si un export Plan Expert de l'estimateur est fourni : aperçus + légendes découpées
  MANIFESTE.md            résumé lisible pour l'agent

Aucune valeur n'est inventée : tout vient des PDF. Les rasters et les mots sont la base du relevé.
"""
from __future__ import annotations
import csv, hashlib, json, os, re, sys, collections
import pymupdf
from PIL import Image, ImageDraw, ImageFont

RASTER_W = 5694          # largeur raster Plan Expert (px) pour une feuille 2383,92 pt
TILE_ROWS, TILE_COLS = 3, 4
SHEET_RE = re.compile(r"\b([A-Z]{1,2}-?\d{3}[A-Z]?)\b")   # E401, E-401, A101, ME-101…

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def font(size: int):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def sheet_id(page: pymupdf.Page) -> str | None:
    """Identifiant de feuille lu dans le cartouche (quart bas-droit), sinon dans toute la page."""
    r = page.rect
    zones = [pymupdf.Rect(r.width * 0.70, r.height * 0.70, r.width, r.height), r]
    for z in zones:
        best = None
        d = page.get_text("dict", clip=z)
        for b in d.get("blocks", []):
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    for m in SHEET_RE.findall(s["text"]):
                        k = m.replace("-", "")
                        key = (round(s["size"], 1), s["bbox"][3])   # le numéro de feuille du cartouche est en gros caractères (puis le plus bas)
                        if best is None or key > best[0]:
                            best = (key, k)
        if best:
            return best[1]
    return None

def classify(path: str, doc: pymupdf.Document) -> str:
    name = os.path.basename(path).lower()
    p0 = doc[0]
    text_pages = sum(1 for p in doc if p.get_text().strip())
    if re.search(r"addenda|adme|addendum", name):
        return "addenda"
    if re.search(r"estimateur|releve|relevé|plan ?expert", name) or (text_pages == 0 and abs(p0.rect.width - 2997) < 40 and len(doc) > 1):
        return "estimateur"          # export Plan Expert (rasterisé, page 2997 × 2116 pt)
    if text_pages == 0:
        return "scan"
    full = " ".join(doc[i].get_text() for i in range(min(3, len(doc)))).lower()
    if "addenda" in full[:4000] and len(doc) <= 6 and not sheet_id(p0):
        return "addenda"
    return "plans"

def draw_rulers(im: Image.Image, x0: float, y0: float, x1: float, y1: float, step: float):
    """Règles graduées en points PDF sur les bords de la tuile."""
    W, H = im.size
    dr = ImageDraw.Draw(im, "RGBA")
    f = font(22)
    sx, sy = W / (x1 - x0), H / (y1 - y0)
    dr.rectangle([0, 0, W, 30], fill=(255, 255, 255, 220)); dr.rectangle([0, 0, 40, H], fill=(255, 255, 255, 220))
    x = int(x0 // step + 1) * step
    while x < x1:
        px = (x - x0) * sx
        dr.line([(px, 0), (px, H)], fill=(0, 120, 255, 70), width=1)
        dr.text((px + 3, 4), str(int(x)), fill=(0, 60, 200, 255), font=f)
        x += step
    y = int(y0 // step + 1) * step
    while y < y1:
        py = (y - y0) * sy
        dr.line([(0, py), (W, py)], fill=(0, 120, 255, 70), width=1)
        dr.text((3, py + 2), str(int(y)), fill=(0, 60, 200, 255), font=f)
        y += step

def main(inbox: str, work: str):
    os.makedirs(work, exist_ok=True)
    for d in ("feuilles", "rasters", "apercus", "tuiles", "texte", "estimateur"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    inv, feuilles, notes = [], [], []
    files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(inbox) for f in fs)
    seen_sheets = collections.Counter()
    for path in files:
        rel = os.path.relpath(path, inbox)
        entry = {"fichier": rel, "octets": os.path.getsize(path), "sha256": sha256(path)}
        if not path.lower().endswith(".pdf"):
            entry["classement"] = "autre"; inv.append(entry); continue
        try:
            doc = pymupdf.open(path)
        except Exception as e:  # noqa
            entry["classement"] = "illisible"; entry["erreur"] = str(e); inv.append(entry); continue
        kind = classify(path, doc)
        entry.update({"classement": kind, "pages": len(doc)})
        inv.append(entry)
        if kind == "estimateur":
            prepare_estimateur(doc, work, rel)
            continue
        if kind in ("plans", "addenda"):
            for i, page in enumerate(doc):
                sid = sheet_id(page)
                if sid is None and kind == "addenda":
                    m = SHEET_RE.findall(os.path.basename(rel).replace("_", " ").upper())
                    sid = m[0].replace("-", "") if len(m) == 1 else f"ADD{i + 1:02d}"
                    notes.append(f"{rel} page {i + 1} : page sans texte (scan) — feuille nommée {sid} d'après le nom du fichier")
                if sid is None:
                    if kind == "plans":
                        notes.append(f"{rel} page {i + 1} : aucun numéro de feuille lu dans le cartouche (page ignorée)")
                    continue
                if kind == "addenda":
                    sid = f"{sid}_ADD"
                seen_sheets[sid] += 1
                fid = sid if seen_sheets[sid] == 1 else f"{sid}_{seen_sheets[sid]}"
                if seen_sheets[sid] > 1:
                    notes.append(f"{rel} page {i + 1} : feuille {sid} déjà vue (renommée {fid}) — doublon, à arbitrer")
                feuilles.append(prepare_sheet(doc, i, fid, rel, kind, work))
        doc.close()
    with open(os.path.join(work, "inventaire.json"), "w", encoding="utf-8") as fh:
        json.dump({"inbox": os.path.abspath(inbox), "fichiers": inv, "notes": notes}, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(work, "feuilles.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["feuille", "fichier", "page", "largeur_pt", "hauteur_pt", "raster_px", "classement_fichier", "nb_mots", "jetons_frequents", "titre"])
        w.writeheader(); w.writerows(feuilles)
    write_manifest(work, inv, feuilles, notes)
    print(f"{len(inv)} fichiers, {len(feuilles)} feuilles préparées dans {work}")
    for n in notes:
        print("NOTE:", n)

def prepare_sheet(doc, i, fid, rel, kind, work):
    page = doc[i]
    W, H = page.rect.width, page.rect.height
    one = pymupdf.open(); one.insert_pdf(doc, from_page=i, to_page=i)
    one.save(os.path.join(work, "feuilles", f"{fid}.pdf")); one.close()
    zoom = RASTER_W / W
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
    pix.save(os.path.join(work, "rasters", f"{fid}.png"))
    rw, rh = pix.width, pix.height
    z2 = 1600 / W
    page.get_pixmap(matrix=pymupdf.Matrix(z2, z2), alpha=False).save(os.path.join(work, "apercus", f"{fid}.png"))
    td = os.path.join(work, "tuiles", fid); os.makedirs(td, exist_ok=True)
    tw, th = W / TILE_COLS, H / TILE_ROWS
    zt = 1800 / tw
    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            x0, y0 = c * tw, r * th
            clip = pymupdf.Rect(x0, y0, x0 + tw, y0 + th)
            px = page.get_pixmap(matrix=pymupdf.Matrix(zt, zt), clip=clip, alpha=False)
            im = Image.frombytes("RGB", (px.width, px.height), px.samples)
            draw_rulers(im, x0, y0, x0 + tw, y0 + th, 50)
            im.save(os.path.join(td, f"r{r + 1}c{c + 1}.png"))
    words = page.get_text("words")
    with open(os.path.join(work, "texte", f"{fid}-mots.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["x0", "y0", "x1", "y1", "cx", "cy", "mot"])
        for x0, y0, x1, y1, t, *_ in words:
            w.writerow([f"{x0:.1f}", f"{y0:.1f}", f"{x1:.1f}", f"{y1:.1f}", f"{(x0 + x1) / 2:.1f}", f"{(y0 + y1) / 2:.1f}", t])
    tokens = collections.Counter(w[4] for w in words if len(w[4]) <= 12)
    with open(os.path.join(work, "texte", f"{fid}-jetons.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["jeton", "n"])
        for t, n in tokens.most_common():
            w.writerow([t, n])
    with open(os.path.join(work, "texte", f"{fid}.txt"), "w", encoding="utf-8") as fh:
        fh.write(page.get_text())
    freq = " ".join(f"{t}×{n}" for t, n in tokens.most_common(25))
    title = ""
    r = page.rect
    tb = page.get_text("words", clip=pymupdf.Rect(r.width * 0.70, r.height * 0.80, r.width, r.height))
    if tb:
        title = " ".join(w[4] for w in sorted(tb, key=lambda w: (round(w[1] / 8), w[0])))[:160]
    return {"feuille": fid, "fichier": rel, "page": i + 1, "largeur_pt": f"{W:.2f}", "hauteur_pt": f"{H:.2f}",
            "raster_px": f"{rw}x{rh}", "classement_fichier": kind, "nb_mots": len(words), "jetons_frequents": freq, "titre": title}

def prepare_estimateur(doc, work, rel):
    """Export Plan Expert de l'estimateur (rasterisé) : aperçu de chaque page + découpe de la légende (bloc à droite)."""
    base = os.path.join(work, "estimateur"); os.makedirs(os.path.join(base, "legendes"), exist_ok=True)
    rows = []
    for i, p in enumerate(doc):
        r = p.rect
        p.get_pixmap(matrix=pymupdf.Matrix(0.5, 0.5), alpha=False).save(os.path.join(base, f"p{i + 1:02d}.png"))
        # zone de légende Plan Expert : à droite du dessin, hors cartouche (mesuré sur S-1857 : x ≥ 0,66 W, 0,30 H ≤ y ≤ 0,62 H)
        clip = pymupdf.Rect(r.width * 0.66, r.height * 0.30, r.width * 0.93, r.height * 0.62)
        p.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip, alpha=False).save(os.path.join(base, "legendes", f"p{i + 1:02d}-legende.png"))
        clip2 = pymupdf.Rect(r.width * 0.76, r.height * 0.80, r.width, r.height)
        p.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip2, alpha=False).save(os.path.join(base, "legendes", f"p{i + 1:02d}-cartouche.png"))
        rows.append({"page": i + 1, "largeur_pt": f"{r.width:.0f}", "hauteur_pt": f"{r.height:.0f}", "fichier": rel})
    with open(os.path.join(base, "pages.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["page", "largeur_pt", "hauteur_pt", "fichier"]); w.writeheader(); w.writerows(rows)

def write_manifest(work, inv, feuilles, notes):
    L = ["# MANIFESTE du dossier préparé", "", "## Fichiers d'entrée", "", "| fichier | classement | pages | octets | sha256 |", "|---|---|--:|--:|---|"]
    for e in inv:
        L.append(f"| {e['fichier']} | {e['classement']} | {e.get('pages', '')} | {e['octets']} | {e['sha256'][:16]}… |")
    L += ["", "## Feuilles de plans (une page = une feuille)", "", "| feuille | fichier | page | pt | mots | titre (cartouche) |", "|---|---|--:|---|--:|---|"]
    for f in feuilles:
        L.append(f"| {f['feuille']} | {f['fichier']} | {f['page']} | {f['largeur_pt']}×{f['hauteur_pt']} | {f['nb_mots']} | {f['titre'][:90]} |")
    if notes:
        L += ["", "## Notes de préparation", ""] + [f"- {n}" for n in notes]
    L += ["", "Jetons fréquents par feuille : `texte/<feuille>-jetons.csv` ; mots avec coordonnées : `texte/<feuille>-mots.csv` ;",
          "tuiles graduées (points PDF) : `tuiles/<feuille>/r1c1.png` … `r3c4.png` ; aperçus : `apercus/<feuille>.png`.",
          "Estimateur (si fourni) : `estimateur/pNN.png` et `estimateur/legendes/pNN-legende.png`."]
    with open(os.path.join(work, "MANIFESTE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
