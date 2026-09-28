"""S-1835 / T-01: build the visual proofs (side-by-side zooms made with releve/zoom.py).

    python dossiers/S-1835/preuves-t01/zooms_t01.py WORKDIR

Reads the CSV written by analyse_t01.py next to this script; writes PNG/JPEG proofs in zooms/.
Original sheets are zoomed without marks (they are no longer part of the takeoff); kept sheets show the
current marks, so a panel without a mark on a symbol is a symbol that is not counted there.
"""
from __future__ import annotations

import csv
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "zooms")
HALF = 60      # pt around the symbol
PX = 520       # pixel width of one panel
Image.MAX_IMAGE_PIXELS = None


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def zoom(work, sheet, x, y, marks):
    x0, y0, x1, y1 = x - HALF, y - HALF, x + HALF, y + HALF
    cmd = [sys.executable, "releve/zoom.py", work, sheet, f"{x0:.1f}", f"{y0:.1f}", f"{x1:.1f}", f"{y1:.1f}", "--px", str(PX)]
    if not marks:
        cmd.append("--sans-marques")
    path = subprocess.run(cmd, cwd=REPO, check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    return Image.open(path).convert("RGB")


def compose(panels, name, title):
    """panels: list of (caption, image)."""
    cap_h, gap = 64, 12
    w = sum(im.width for _, im in panels) + gap * (len(panels) - 1)
    h = max(im.height for _, im in panels) + cap_h + 40
    out = Image.new("RGB", (w, h), "white")
    dr = ImageDraw.Draw(out)
    dr.text((8, 6), title, fill=(0, 0, 0), font=font(20))
    x = 0
    for cap, im in panels:
        dr.text((x + 6, 40), cap, fill=(160, 30, 30), font=font(17))
        out.paste(im, (x, cap_h + 36))
        x += im.width + gap
    out = out.convert("P", palette=Image.ADAPTIVE, colors=64)
    out.save(os.path.join(OUT, name), optimize=True)
    return name


def rows(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(work):
    os.makedirs(OUT, exist_ok=True)
    made = []
    # 1. speakers present on the original D420/D421 but absent from one T-01 sheet
    seen = set()
    for r in rows("haut-parleurs-absents-t01.csv"):
        a, b = r["feuille_originale"], r["vue_aussi_sur"]
        xa, ya, xb, yb = float(r["x_pt"]), float(r["y_pt"]), float(r["x_autre"]), float(r["y_autre"])
        key = (round(xa if a == "D420" else xb), round(ya if a == "D420" else yb))
        if key in seen:
            continue
        seen.add(key)
        (s420, x420, y420), (s421, x421, y421) = ((a, xa, ya), (b, xb, yb)) if a == "D420" else ((b, xb, yb), (a, xa, ya))
        verdict = "retiré du dessin par T-01" if r["present_sur_t01"] == "non" else "doublon du chevauchement original, compté une fois"
        made.append(compose([
            (f"{s420} original ({x420:.0f}, {y420:.0f})", zoom(work, s420, x420, y420, False)),
            (f"{s421} original ({x421:.0f}, {y421:.0f})", zoom(work, s421, x421, y421, False)),
            (f"{s420}_ADD (T-01), marques actuelles", zoom(work, s420 + "_ADD", x420, y420, True)),
            (f"{s421}_ADD (T-01), marques actuelles", zoom(work, s421 + "_ADD", x421, y421, True)),
        ], f"etage-{s420}-{int(x420)}-{int(y420)}.png", f"Haut-parleur étage, recalage D420/D421 : {verdict}"))
    # 2. RDC duplicates (D411 / D412 overlapping views)
    for r in rows("marques-retirees.csv"):
        if not r["raison"].startswith("doublon"):
            continue
        keep = r["raison"].split("que ")[1]
        ks, kxy = keep.split(" (")[0], keep.split(" (")[1].split(")")[0]
        kx, ky = map(float, kxy.split(", "))
        x, y = float(r["x_pt"]), float(r["y_pt"])
        made.append(compose([
            (f"{ks} ({kx:.0f}, {ky:.0f}) : marque conservée", zoom(work, ks, kx, ky, True)),
            (f"{r['feuille']} ({x:.0f}, {y:.0f}) : marque retirée", zoom(work, r["feuille"], x, y, True)),
        ], f"rdc-doublon-{r['feuille']}-{int(x)}-{int(y)}.png", "Même haut-parleur dessiné sur deux feuilles (vues superposées) : compté une fois"))
    # 3. D422: T-01 moved the viewport, same 9 speakers
    comp = {r["feuille_originale"]: r for r in rows("comparaison-t01.csv")}
    det = [r for r in rows("haut-parleurs-detection.csv") if r["feuille"] == "D422"]
    dx, dy = float(comp["D422"]["dx_pt"]), float(comp["D422"]["dy_pt"])
    x, y = float(det[0]["x_pt"]), float(det[0]["y_pt"])
    made.append(compose([
        (f"D422 original ({x:.0f}, {y:.0f})", zoom(work, "D422", x, y, False)),
        (f"D422_ADD ({x + dx:.0f}, {y + dy:.0f}), marques actuelles", zoom(work, "D422_ADD", x + dx, y + dy, True)),
    ], "d422-decalage.png", f"T-D422 rév. 1 : même dessin décalé de {dx} pt en x ; les 9 haut-parleurs sont identiques"))
    # 4. basement: whole-sheet previews (no speaker symbol at all)
    for f in ("D400", "D401", "D402", "D403"):
        im = Image.open(os.path.join(work, "apercus", f + ".png")).convert("RGB")
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        name = f"sous-sol-{f}.jpg"
        im.save(os.path.join(OUT, name), quality=80, optimize=True)
        made.append(name)
    print("\n".join(made))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
