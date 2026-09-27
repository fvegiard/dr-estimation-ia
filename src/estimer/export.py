"""Write the estimate: estimate.json (ecart-ready), releve.xlsx, <name>.qpl + page PNGs.

estimate.json is read directly by `python -m src.validation.ecart --ia` (its
top-level "counters" list is the `verifier --export-counters` shape: quantity
= number of elements) and carries per-sheet family counts, conduit estimates
and every uncertainty flag.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

from PIL import Image

from src.releve import qpl_build, xlsx_export

from .families import FAMILIES, FAMILY_COUNTER_NAME

FLAG_NEAR_MARKUP = "near_coloured_markup"
FLAG_UNREADABLE = "unreadable_markup_zones"
FLAG_LOW_FAMILY = "family_uncertain"
FLAG_SCALE_UNKNOWN = "scale_unknown"
FLAG_MARKUP_PAGE = "page_has_coloured_markup"
FLAG_NO_SYMBOL = "no_symbol_detected"
FAMILY_PROB_MIN = 0.5
FLAG_TEXT_TAG = "from_text_tag"              # counted from a legend code written on the plan
FLAG_FAMILY_FROM_TAG = "family_from_text_tag"  # visual symbol whose family comes from a nearby legend code


@dataclass
class SheetResult:
    page: int
    name: str
    width_px: int
    height_px: int
    source: str
    scale_ratio: float | None
    scale_source: str
    paper_width_pt: float | None
    overlay_fraction: float
    unreadable_zones: int = 0
    detections: list = field(default_factory=list)
    tree_ft: float | None = None
    conduit_ft: float | None = None
    tree_edges: list = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        c = Counter(d.family for d in self.detections)
        return {f: c[f] for f in FAMILIES if c[f]}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def detection_flags(d) -> list[str]:
    f = []
    if d.near_markup:
        f.append(FLAG_NEAR_MARKUP)
    if d.family_prob < FAMILY_PROB_MIN and d.source == "visual":
        f.append(FLAG_LOW_FAMILY)
    if d.source == "text_tag":
        f.append(FLAG_TEXT_TAG)
    elif d.source == "visual+text_tag":
        f.append(FLAG_FAMILY_FROM_TAG)
    return f


def counter_name(family: str, model) -> str:
    return FAMILY_COUNTER_NAME.get(family, family.upper())


def write_json(path: Path, pdf: Path, sheets: list[SheetResult], model, extra: dict) -> dict:
    counters = []
    by_fam: dict[str, list] = defaultdict(list)
    for s in sheets:
        for d in s.detections:
            by_fam[d.family].append((s, d))
    for gid, fam in enumerate([f for f in FAMILIES if f in by_fam], start=1):
        counters.append({
            "group_id": gid, "name": counter_name(fam, model), "family": fam,
            "quantity": len(by_fam[fam]),
            "elements": [{"sheet": s.name, "page": s.page + 1, "x": round(d.x, 1), "y": round(d.y, 1),
                          "score": round(d.score, 3), "family_prob": round(d.family_prob, 3),
                          **({"tag": d.tag} if d.tag else {}),
                          "flags": detection_flags(d)} for s, d in by_fam[fam]],
        })
    totals = Counter()
    for s in sheets:
        totals.update(s.counts())
    uncertainties = []
    for s in sheets:
        for fl in s.flags:
            uncertainties.append({"sheet": s.name, "page": s.page + 1, "flag": fl})
    n_occ = sum(1 for s in sheets for d in s.detections if d.near_markup)
    n_unread = sum(s.unreadable_zones for s in sheets)
    n_low = sum(1 for s in sheets for d in s.detections if d.family_prob < FAMILY_PROB_MIN)
    data = {
        "source_pdf": str(pdf), "source_sha256": sha256(pdf),
        "format": "dupuis-family-counts/1",
        "model": {"trained_on": model.trained_on, "threshold": model.threshold, "nms_radius_px": model.nms_radius,
                  "stride_px": model.stride, "conduit_ratio": model.conduit_ratio},
        "totals": {f: totals[f] for f in FAMILIES if totals[f]},
        "items": [{"libelle": c["name"], "quantite": c["quantity"]} for c in counters],
        "sheets": [{
            "page": s.page + 1, "sheet": s.name, "width_px": s.width_px, "height_px": s.height_px,
            "raster_source": s.source, "scale_ratio": s.scale_ratio, "scale_source": s.scale_source,
            "overlay_fraction": round(s.overlay_fraction, 4), "unreadable_markup_zones": s.unreadable_zones,
            "counts": s.counts(),
            "detections": len(s.detections),
            "conduit_tree_ft": None if s.tree_ft is None else round(s.tree_ft, 1),
            "conduit_estimate_ft": None if s.conduit_ft is None else round(s.conduit_ft, 1),
            "flags": s.flags,
        } for s in sheets],
        "counters": counters,
        "uncertainties": {"sheet_flags": uncertainties, "detections_near_markup": n_occ,
                          "unreadable_markup_zones": n_unread,
                          "detections_family_uncertain": n_low,
                          "family_prob_min": FAMILY_PROB_MIN},
        **extra,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def write_xlsx(path: Path, sheets: list[SheetResult], model) -> None:
    occ = []
    for s in sheets:
        for d in s.detections:
            fl = detection_flags(d)
            occ.append({"feuille": s.name, "label": counter_name(d.family, model), "page_pdf": str(s.page + 1),
                        "note": ("à vérifier : " + ", ".join(fl)) if fl else ""})
    lignes = xlsx_export.agreger(occ)
    nomenclature = {counter_name(f, model): f"Famille {f} (compte automatique)" for f in FAMILIES}
    xlsx_export.ecrire_xlsx(lignes, nomenclature, path)
    # conduit and sheet-flag sheets appended with openpyxl
    from openpyxl import load_workbook
    wb = load_workbook(path)
    ws = wb.create_sheet("Conduits")
    ws.append(["Feuille", "Page PDF", "Échelle (réel/papier)", "Source échelle", "Arbre des appareils (pi)",
               "Conduit estimé (pi)", "Zones illisibles (annotations de couleur)", "Notes"])
    for s in sheets:
        ws.append([s.name, s.page + 1, s.scale_ratio, s.scale_source,
                   None if s.tree_ft is None else round(s.tree_ft, 1),
                   None if s.conduit_ft is None else round(s.conduit_ft, 1),
                   s.unreadable_zones, ", ".join(s.flags)])
    wb.save(path)


def write_qpl(out_dir: Path, name: str, sheets: list[SheetResult], pages_gray: dict[int, "object"], model) -> Path:
    plans = []
    for s in sheets:
        file_name = f"{name} - {s.page + 1}.png"
        img = Image.fromarray(pages_gray[s.page])
        dpi = None
        if s.paper_width_pt:
            dpi = s.width_px / (s.paper_width_pt / 72.0)
        img.save(out_dir / file_name, dpi=(dpi, dpi) if dpi else None) if dpi else img.save(out_dir / file_name)
        plan = {"sheet": f"{name} - {s.page + 1}", "file_name": file_name,
                "raster_width_px": s.width_px, "raster_height_px": s.height_px,
                "bookmark": {"zoom": -1, "x": 0, "y": 0}, "layer_name": "Calque par défaut", "opacity": 150,
                "legend": {"x": 100, "y": 100, "font_size": 45, "max_rows": 25}}
        if s.scale_ratio:
            imperial = abs(12.0 / s.scale_ratio - round(12.0 / s.scale_ratio * 64) / 64) < 1e-6 and s.scale_ratio < 1000 \
                and s.scale_source.endswith("imperial")
            if imperial:
                plan["scale"] = {"value": f"{12.0 / s.scale_ratio:g}".replace(".", ","), "type": 1, "precision": 2}
            else:
                plan["scale"] = {"value": f"{s.scale_ratio:g}", "type": 0, "precision": 2}
        plans.append(plan)
    counters = []
    gid = 0
    for fam in FAMILIES:
        els = [(s, d) for s in sheets for d in s.detections if d.family == fam]
        if not els:
            continue
        gid += 1
        _label, shape, size, color = model.family_style.get(fam, (fam, 0, 20, -65536))
        counters.append({"group_id": gid, "name": counter_name(fam, model), "shape": shape, "default_size": size,
                         "color": color, "fill_color": color, "text": "1",
                         "elements": [{"sheet": f"{name} - {s.page + 1}", "x": round(d.x), "y": round(d.y),
                                       "width": size, "height": size} for s, d in els]})
    lines = []
    tree_segments = [(s, a, b) for s in sheets if s.conduit_ft is not None for a, b in s.tree_edges]
    if tree_segments:
        gid += 1
        segs = []
        for s, a, b in tree_segments:
            xa, ya = a
            xb, yb = b
            # rectilinear tree edge drawn as an L (horizontal then vertical)
            segs.append({"sheet": f"{name} - {s.page + 1}", "x1": xa, "y1": ya, "x2": xb, "y2": ya})
            segs.append({"sheet": f"{name} - {s.page + 1}", "x1": xb, "y1": ya, "x2": xb, "y2": yb})
        lines.append({"group_id": gid, "name": "CONDUIT ESTIME (arbre des appareils)", "color": -16776961,
                      "pen_width": 6, "segments": [x for x in segs if (x["x1"], x["y1"]) != (x["x2"], x["y2"])]})
    model_plans = {"project": {"name": name, "description": "Estimation automatique (src.estimer)"},
                   "plans": plans}
    text = qpl_build.build_qpl_text(model_plans, counters, lines)
    path = out_dir / f"{name}.qpl"
    qpl_build.write_qpl(path, text, force=True)
    return path


def write_sheets_csv(path: Path, sheets: list[SheetResult]) -> None:
    fams = [f for f in FAMILIES]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["page", "sheet", *fams, "total", "unreadable_markup_zones", "conduit_estimate_ft", "flags"])
        for s in sheets:
            c = s.counts()
            w.writerow([s.page + 1, s.name, *[c.get(f, 0) for f in fams], len(s.detections), s.unreadable_zones,
                        "" if s.conduit_ft is None else round(s.conduit_ft, 1), ";".join(s.flags)])
