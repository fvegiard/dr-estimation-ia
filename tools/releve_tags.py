"""Plan + BOM: mark every BOM device on a vector plan PDF and print the BOM list on the sheet.

Devices are found by their printed type tag ('FGG1') paired with the circuit label under it.
Output per sheet: <prefix>-<sheet>-releve.jpg (plan + coloured marks + BOM table),
<prefix>-<sheet>-bom.csv (Type,Description,Quantité,Source), <prefix>-<sheet>-releve-points.csv.
"""
import argparse, csv, io, json, math, os, re
import pymupdf
from PIL import Image, ImageDraw, ImageFont

TAG_RE = re.compile(r"^['\u2018\u2019]([A-Z]{1,4}\d{0,2})['\u2018\u2019]$")
CIR_RE = re.compile(r"^([A-Z]{2})-(\d+(?:\.\d+)?)$")
OUT_W = 6854
COLOURS = {"Normal": (31, 119, 180), "Secours": (214, 39, 40), "Autre": (255, 127, 14)}


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name), size)


def extract(page, types, max_dist):
    m = page.rotation_matrix
    tags, cirs = [], []
    for w in page.get_text("words"):
        r = pymupdf.Rect(w[:4]) * m
        r.normalize()
        c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        t = TAG_RE.match(w[4])
        if t:
            tags.append((t.group(1), c))
        elif CIR_RE.match(w[4]):
            cirs.append((w[4], c))
    # pair every tag (all types, so neighbours cannot steal a label), closest pairs first;
    # the circuit label sits level with or below its tag
    pairs = sorted((math.dist(tc, cc), ti, ci) for ti, (_, tc) in enumerate(tags)
                   for ci, (_, cc) in enumerate(cirs) if math.dist(tc, cc) <= max_dist and cc[1] >= tc[1] - 3)
    assigned, used = {}, set()
    for _, ti, ci in pairs:
        if ti not in assigned and ci not in used:
            assigned[ti] = ci
            used.add(ci)
    devices = []
    for ti, (typ, tc) in enumerate(tags):
        if typ not in types:
            continue
        if ti in assigned:
            cl, cc = cirs[assigned[ti]]
            devices.append({"type": typ, "circuit": cl, "x": (tc[0] + cc[0]) / 2, "y": (tc[1] + cc[1]) / 2})
        else:
            devices.append({"type": typ, "circuit": "", "x": tc[0], "y": tc[1] + 8})
    return devices


def klass(circuit):
    return {"N": "Normal", "S": "Secours"}.get(circuit[:1], "Autre")


def run(sheet_cfg, cfg):
    sheet = sheet_cfg["sheet"]
    page = pymupdf.open(sheet_cfg["pdf"])[0]
    devices = extract(page, set(cfg["types"]), cfg.get("max_dist", 60))
    scale = OUT_W / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    rad = int(13 * scale)
    n = {"Normal": 0, "Secours": 0, "Autre": 0}
    for d in devices:
        k = klass(d["circuit"])
        n[k] += 1
        x, y = d["x"] * scale, d["y"] * scale
        draw.ellipse((x - rad, y - rad, x + rad, y + rad), outline=COLOURS[k] + (255,), width=6, fill=COLOURS[k] + (45,))
    total = len(devices)

    # BOM rows: (colour key or None, type, description, quantity)
    lum = sheet_cfg["luminaire"]
    rows = [("Normal", "LUMINAIRE", f"{lum} — circuit normal", n["Normal"]),
            ("Secours", "LUMINAIRE", f"{lum} — circuit secours", n["Secours"])]
    if n["Autre"]:
        rows.append(("Autre", "LUMINAIRE", f"{lum} — circuit non indiqué au plan", n["Autre"]))
    rows.append((None, "FIXT ENL", cfg["removal"], total))
    rows += [(None, t, d, q) for t, d, q in sheet_cfg.get("extra_rows", [])]

    box = sheet_cfg.get("legend_box", cfg["legend_box"])
    lx0, ly0, lx1 = int(box[0] * W), int(box[1] * H), int(box[2] * W)
    pad, f_t, f_h, f_b, f_n, f_s = 28, font(38, True), font(26, True), font(26), font(30, True), font(24)
    qx = lx1 - pad - 70
    wrap_w = qx - (lx0 + pad + 56) - 20

    def wrap(text):
        out, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=f_b) <= wrap_w:
                cur = trial
            else:
                out.append(cur)
                cur = word
        return out + [cur]

    wrapped = [(k, t, wrap(d), q) for k, t, d, q in rows]
    foot = sheet_cfg.get("footer", []) + cfg.get("footer", [])
    height = pad + 54 + 40 + 44 + sum(34 + 32 * len(w[2]) + 14 for w in wrapped) + 50 + 32 * len(foot) + pad
    draw.rectangle((lx0, ly0, lx1, ly0 + height), fill=(255, 255, 255, 255), outline=(40, 40, 40, 255), width=5)
    y = ly0 + pad
    draw.text((lx0 + pad, y), "LISTE DE MATÉRIEL (BOM)", font=f_t, fill="black"); y += 54
    draw.text((lx0 + pad, y), f"Feuille {sheet}", font=f_b, fill="black"); y += 40
    draw.text((lx0 + pad + 56, y), "Type / Description", font=f_h, fill="black")
    draw.text((qx - 10, y), "Qté", font=f_h, fill="black"); y += 36
    draw.line((lx0 + pad, y, lx1 - pad, y), fill=(40, 40, 40, 255), width=3); y += 8
    for k, t, lines, q in wrapped:
        if k:
            draw.ellipse((lx0 + pad, y + 4, lx0 + pad + 36, y + 40), outline=COLOURS[k] + (255,), width=6, fill=COLOURS[k] + (45,))
        draw.text((lx0 + pad + 56, y), t, font=f_h, fill="black")
        draw.text((qx, y + 4), str(q), font=f_n, fill="black"); y += 34
        for line in lines:
            draw.text((lx0 + pad + 56, y), line, font=f_b, fill=(40, 40, 40)); y += 32
        y += 14
    draw.line((lx0 + pad, y, lx1 - pad, y), fill=(40, 40, 40, 255), width=3); y += 10
    draw.text((lx0 + pad + 56, y), "TOTAL luminaires à poser", font=f_h, fill="black")
    draw.text((qx, y), str(total), font=f_n, fill="black"); y += 40
    for line in foot:
        draw.text((lx0 + pad, y), line, font=f_s, fill=(70, 70, 70)); y += 32
    assert ly0 + height < H * 0.98, f"legend overflow on {sheet}"

    os.makedirs(cfg["outdir"], exist_ok=True)
    base = os.path.join(cfg["outdir"], f"{cfg['prefix']}-{sheet}")
    img.save(base + "-releve.jpg", quality=88, dpi=(300, 300))

    def write_csv(path, header, data):
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh, lineterminator="\r\n")
            w.writerow(header)
            w.writerows(data)

    write_csv(base + "-bom.csv", ["Type", "Description", "Quantité", "Source"],
              [[t, d, q, sheet] for _, t, d, q in rows])
    write_csv(base + "-releve-points.csv", ["Type", "Circuit", "Classe", "X points", "Y points"],
              [[d["type"], d["circuit"], klass(d["circuit"]), round(d["x"], 2), round(d["y"], 2)]
               for d in sorted(devices, key=lambda d: (d["circuit"], d["y"], d["x"]))])
    print(sheet, "normal", n["Normal"], "secours", n["Secours"], "autre", n["Autre"], "total", total)
    return [[sheet, t, d, q] for _, t, d, q in rows]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    cfg = json.load(open(ap.parse_args().config, encoding="utf-8"))
    allrows = []
    for s in cfg["sheets"]:
        allrows += run(s, cfg)
    with open(os.path.join(cfg["outdir"], f"{cfg['prefix']}-BOM-toutes-feuilles.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["Feuille", "Type", "Description", "Quantité"])
        w.writerows(allrows)
