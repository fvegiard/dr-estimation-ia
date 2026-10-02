"""Render a source-preserving take-off sheet: plan + pastilles + legend strip under the plan + bordereau CSV.

Port of the render_sheet.py used for the S-1294 / S-0844 / S-0922 / Granby deliveries: same pastille
(r 4.2 units, pastel fill, family-coloured outline), same legend ("RELEVÉ <sheet> — <title>",
"N pastilles / M familles / RES R"), same bordereau columns, same proof boards. The plan is never covered:
the legend is appended below it.
"""
import colorsys
import csv
import io
import json
import os
import sys
from collections import Counter
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
OUT_W = 6854
UNITS = 1920
COLORS = ["#3C82BA", "#55A25E", "#A852A2", "#A37225", "#D45B6B", "#2B9B95", "#8B70AA", "#AC7860"]
HEADER = ["Repère / source", "Matériel", "Désignation", "Qté", "Portée", "Modèle", "Prescription / réserve", "Parent",
          "X pixels source", "Y pixels source", "Pastille", "Circuits", "Ampères", "Pôles", "Protection source"]


def _font(size):
    for path in (os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arial.ttf"),
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, max(1, round(size)))
    raise FileNotFoundError("no TrueType font found")


def _palette(families):
    colours = list(COLORS)
    hue = 0.07
    while len(colours) < len(families):  # more families than the reference palette: add distinct hues
        r, g, b = colorsys.hls_to_rgb(hue % 1, 0.42, 0.55)
        c = "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))
        if c not in colours:
            colours.append(c)
        hue += 0.61803
    return dict(zip(families, colours))


def render(data, project, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    key, records, prefix = data["key"], data["records"], project["prefix"]
    page = pymupdf.open(data["pdf"])[0]
    zoom = OUT_W / page.rect.width
    png = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False).tobytes("png")
    base = Image.open(io.BytesIO(png)).convert("RGB")
    scale = base.width / UNITS
    counts = Counter(r["family"] for r in records if r.get("mark", True))
    palette = _palette(list(counts))
    rows = (len(counts) + 2) // 3
    legend_height = round((140 + 27 * rows + 25 * len(data["notes"])) * scale)
    canvas = Image.new("RGB", (base.width, base.height + legend_height), "white")
    canvas.paste(base, (0, 0))
    overlay = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(overlay)
    for i, rec in enumerate(records, 1):
        rec["id"] = f"{key}-{i:04d}"
        if not rec.get("mark", True):
            continue
        x, y, radius = rec["x"] * scale, rec["y"] * scale, rec.get("radius", 4.2) * scale
        colour = palette[rec["family"]]
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour + "45", outline=colour,
                     width=max(2, round(.7 * scale)))
        if rec.get("reserve"):
            draw.text((x + radius, y - radius * 2), "*", font=_font(10 * scale), fill=colour)

    def text(x, y, value, size=13, colour="#222222"):
        draw.text((round(x * scale), base.height + round(y * scale)), value, font=_font(size * scale), fill=colour)

    draw.rectangle((25 * scale, base.height + 15 * scale, base.width - 25 * scale, canvas.height - 15 * scale),
                   outline="#909090", width=3)
    title = f"RELEVÉ {key} — {data['title']}"
    text(45, 27, title, 21)
    reserved = sum(bool(r.get("reserve")) for r in records)
    header = (f"{sum(counts.values())} pastilles / {len(counts)} familles / RES {reserved} — "
              f"source : {Path(data['pdf']).name} — {data['scope']}")
    text(45, 61, header, 13)
    for i, (family, count) in enumerate(counts.items()):
        x, y = 48 + (i % 3) * 620, 99 + (i // 3) * 27
        colour = palette[family]
        draw.ellipse(((x - 4.2) * scale, base.height + (y - 4.2) * scale, (x + 4.2) * scale, base.height + (y + 4.2) * scale),
                     fill=colour + "45", outline=colour, width=3)
        text(x + 14, y - 10, f"{family} : {count}", 14, colour)
    y = 114 + 27 * rows
    for note in data["notes"]:
        text(45, y, note, 12)
        y += 25
    final = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    jpg = out_dir / f"{prefix}-{key}-releve.jpg"
    final.save(jpg, quality=90, dpi=(300, 300))

    proof = out_dir / "audit" / key
    proof.mkdir(parents=True, exist_ok=True)
    overview = final.copy()
    overview.thumbnail((1920, 1600))
    overview.save(proof / "overview.jpg", quality=90)
    legend = final.crop((0, base.height, final.width, final.height))
    legend.thumbnail((2200, 1400))
    legend.save(proof / "legend.jpg", quality=92)
    marked = [r for r in records if r.get("mark", True)]
    boards = []
    for start in range(0, len(marked), 30):
        board = Image.new("RGB", (1800, 1350), "white")
        d = ImageDraw.Draw(board)
        for j, rec in enumerate(marked[start:start + 30]):
            x, y = round(rec["x"] * scale), round(rec["y"] * scale)
            col, row = j % 6, j // 6
            board.paste(final.crop((x - 150, y - 110, x + 150, y + 110)), (col * 300, row * 270 + 45))
            d.text((col * 300 + 4, row * 270 + 3), rec["id"], fill="black", font=_font(16))
            d.text((col * 300 + 4, row * 270 + 23), rec["family"][:34], fill="black", font=_font(13))
        boards.append(proof / f"marks-{start + 1:04d}.jpg")
        board.save(boards[-1], quality=90)

    csv_path = out_dir / f"{prefix}-{key}-{data['type']}.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        for rec in records:
            writer.writerow([rec["id"], rec["family"], rec.get("label", ""), rec.get("quantity", 1),
                             rec.get("scope", data["scope"]), rec.get("model", "MODELE NON PRECISE"),
                             rec.get("reserve", ""), rec.get("parent", ""),
                             round(rec.get("x", 0) * scale, 2), round(rec.get("y", 0) * scale, 2),
                             int(rec.get("mark", True)), rec.get("circuits", ""), rec.get("ampere", ""),
                             rec.get("poles", ""), rec.get("protection", "")])
    (out_dir / "audit" / f"{key}-records.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(key, "pastilles:", sum(counts.values()), "familles:", len(counts), "RES:", reserved)
    return {"jpg": jpg, "csv": csv_path, "base_size": base.size, "legend_top": base.height, "legend": dict(counts),
            "header": header, "title": title, "palette": palette, "boards": boards}


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    import tag_records
    project = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    wanted = set(sys.argv[3:])
    for sheet in project["sheets"]:
        if not wanted or sheet["sheet"] in wanted:
            render(tag_records.build(project, sheet), project, sys.argv[2])
