"""Annotated take-off from vector plan PDFs whose devices carry quoted type tags.

For each sheet: locate every quoted type tag ('FGG1'), pair it with the nearest
circuit label (NA-3, SA-10...), draw a coloured ring on the device, add an
integrated legend with counts, and write a JPG + per-device CSV + count CSV.
Nothing is inferred: only tags physically printed on the sheet are counted.
"""
import argparse, csv, io, json, math, os, re, sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont

TAG_RE = re.compile(r"^['\u2018\u2019]([A-Z]{1,4}\d{0,2})['\u2018\u2019]$")
CIR_RE = re.compile(r"^([A-Z]{2})-(\d+(?:\.\d+)?)$")
OUT_W = 6854
PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf",
           "#e377c2", "#8c564b", "#bcbd22", "#393b79", "#ad494a", "#637939"]


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name), size)


def extract(page, max_dist):
    m = page.rotation_matrix
    tags, cirs = [], []
    for w in page.get_text("words"):
        r = pymupdf.Rect(w[:4]) * m
        r.normalize()
        c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        t = TAG_RE.match(w[4])
        if t:
            tags.append((t.group(1), c))
            continue
        k = CIR_RE.match(w[4])
        if k:
            cirs.append((w[4], c))
    devices = []
    used = set()
    # greedy nearest pairing, closest pairs first, one circuit label per tag
    pairs = sorted(
        ((math.dist(tc, cc), ti, ci) for ti, (_, tc) in enumerate(tags) for ci, (_, cc) in enumerate(cirs)
         if math.dist(tc, cc) <= max_dist and cc[1] >= tc[1] - 3))
    assigned = {}
    for d, ti, ci in pairs:
        if ti in assigned or ci in used:
            continue
        assigned[ti] = ci
        used.add(ci)
    for ti, (typ, tc) in enumerate(tags):
        if ti in assigned:
            cl, cc = cirs[assigned[ti]]
            pos = ((tc[0] + cc[0]) / 2, (tc[1] + cc[1]) / 2)
            devices.append({"type": typ, "circuit": cl, "x": pos[0], "y": pos[1]})
        else:
            devices.append({"type": typ, "circuit": "", "x": tc[0], "y": tc[1]})
    return devices


def klass(circuit):
    if not circuit:
        return "sans circuit"
    return {"N": "Normal", "S": "Secours", "U": "UPS"}.get(circuit[0], circuit[:1]) + " (" + circuit[:2] + ")"


def run(pdf, sheet, outdir, prefix, legend_box, title, notes, max_dist, descriptions, compare=None):
    doc = pymupdf.open(pdf)
    page = doc[0]
    devices = extract(page, max_dist)
    scale = OUT_W / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    groups = {}
    for d in devices:
        groups.setdefault((d["type"], klass(d["circuit"])), []).append(d)
    keys = sorted(groups, key=lambda k: (-sum(len(v) for kk, v in groups.items() if kk[0] == k[0]), k[0], k[1]))
    colour = {k: PALETTE[i % len(PALETTE)] for i, k in enumerate(keys)}

    rad = int(13 * scale)
    for k in keys:
        col = colour[k]
        rgb = tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))
        for d in groups[k]:
            x, y = d["x"] * scale, d["y"] * scale
            if d["circuit"]:
                draw.ellipse((x - rad, y - rad, x + rad, y + rad), outline=rgb + (255,), width=6, fill=rgb + (45,))
            else:
                draw.rectangle((x - rad, y - rad, x + rad, y + rad), outline=rgb + (255,), width=5)

    # integrated legend (auto height, anchored at legend_box x0,y0,x1)
    if compare:
        n_plan = sum(len(v) for k, v in groups.items() if k[0] == compare["type"])
        n_free = len(groups.get((compare["type"], "sans circuit"), []))
        notes = notes + [
            f"BOM corrigé — luminaires à remplacer : {compare['bom']}",
            f"Repères '{compare['type']}' au plan : {n_plan}" + (f" (dont {n_free} sans circuit)" if n_free else ""),
            ("Concordance plan = BOM" if n_plan == compare["bom"]
             else f"ÉCART plan − BOM : {n_plan - compare['bom']:+d} — À VALIDER")] + compare.get("extra", [])
    big = len(keys) > 14
    row = 40 if big else 50
    f_t, f_b, f_s = font(36, True), font(28 if big else 32), font(25)
    f_n = font(28 if big else 32, True)
    pad = 28
    lx0, ly0, lx1 = int(legend_box[0] * W), int(legend_box[1] * H), int(legend_box[2] * W)
    head = [f"{sum(1 for d in devices if d['circuit'])} appareils repérés avec circuit sur cette feuille"]
    expl = ["Cercle = appareil compté (repère + circuit).", "Carré = repère sans circuit, NON compté."]
    height = pad + 52 + 44 + 34 * len(expl) + 14 + row * len(keys) + 14 + 36 * len(notes) + pad
    ly1 = ly0 + height
    if ly1 > H * 0.975:
        print(f"WARNING legend overflow on {sheet}", file=sys.stdout)
    draw.rectangle((lx0, ly0, lx1, ly1), fill=(255, 255, 255, 255), outline=(60, 60, 60, 255), width=4)
    y = ly0 + pad
    draw.text((lx0 + pad, y), title, font=f_t, fill="black"); y += 52
    draw.text((lx0 + pad, y), head[0], font=f_b, fill="black"); y += 44
    for line in expl:
        draw.text((lx0 + pad, y), line, font=f_s, fill=(70, 70, 70)); y += 34
    y += 14
    for k in keys:
        col = colour[k]
        box = (lx0 + pad, y + 4, lx0 + pad + row - 18, y + row - 14)
        if k[1] == "sans circuit":
            draw.rectangle(box, outline=col, width=5)
        else:
            draw.ellipse(box, outline=col, width=6)
        draw.text((lx0 + pad + row, y), f"'{k[0]}'  {k[1]}", font=f_b, fill="black")
        draw.text((lx1 - pad - 70, y), str(len(groups[k])), font=f_n, fill="black")
        y += row
    y += 14
    for line in notes:
        draw.text((lx0 + pad, y), line, font=f_s, fill=(160, 0, 0) if "ÉCART" in line else (40, 40, 40)); y += 36

    os.makedirs(outdir, exist_ok=True)
    base = os.path.join(outdir, f"{prefix}-{sheet}")
    img.save(base + "-releve.jpg", quality=88, dpi=(300, 300))

    def write_csv(path, header, rows):
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh, lineterminator="\r\n")
            w.writerow(header)
            w.writerows(rows)

    write_csv(base + "-releve-points.csv", ["Type", "Circuit", "Classe", "X points", "Y points"],
              [[d["type"], d["circuit"], klass(d["circuit"]), round(d["x"], 2), round(d["y"], 2)]
               for d in sorted(devices, key=lambda d: (d["type"], d["circuit"], d["y"], d["x"]))])
    write_csv(base + "-releve-count.csv", ["Type", "Description", "Quantité", "Source"],
              [[k[0], (descriptions.get(k[0], "Repère au plan; description selon légende du projet") + " — " + k[1]),
                len(groups[k]), sheet + (" (repère sans circuit, non compté)" if k[1] == "sans circuit" else "")]
               for k in keys])
    summary = {"sheet": sheet, "size": [W, H], "counts": {f"{k[0]}|{k[1]}": len(groups[k]) for k in keys if k[0] in ("FGG1", "FS", "FF")}}
    print(json.dumps(summary, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    cfg = json.load(open(ap.parse_args().config, encoding="utf-8"))
    for s in cfg["sheets"]:
        run(s["pdf"], s["sheet"], cfg["outdir"], cfg["prefix"], s.get("legend_box", cfg["legend_box"]),
            s["title"], s.get("notes", []) + cfg.get("notes", []), cfg.get("max_dist", 60), cfg.get("descriptions", {}), s.get("compare"))
