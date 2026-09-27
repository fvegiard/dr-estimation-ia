"""Leave-one-out evaluation against the estimator's (M. Dupuis) references.

  python -m src.estimer.evaluate [--out eval] [--dossiers ...] [--resume]

For each dossier with a Dupuis Plan Expert project (position gold), a model is
trained on the OTHER such dossiers (`train.train`, with its own inner
calibration) and run on the held-out dossier's plan PDF through the same
pipeline as `python -m src.estimer`. Dossiers with count-only gold (S-1857:
transcribed quantities, no positions) are scored with the model trained on all
position dossiers — they are never part of any training set.

Metrics (every number is computed from the files, nothing typed in):
- detection, family-agnostic: optimal one-to-one matching of predicted and
  gold points within R px (R = 15, 25, 45 at 2997 px page width; 45 px is the
  1.2 %-of-diagonal threshold of compare_qpl), precision / recall / F1, on all
  pages and on the pages the estimator marked;
- per family: same matching restricted to one family, precision, recall, and
  count error (predicted - gold) / gold on all pages;
- recall split by whether the gold symbol lies under pre-existing coloured
  mark-up (another takeoff printed on the only available plan images);
- leakage check: share of predictions and of gold marks lying within 15 px of
  the other takeoff's marks (a detector that learnt "coloured mark here" would
  hit them far more often than the estimator does);
- conduit estimate vs the estimator's conduit lines on sheets where both exist;
- count-only dossiers: count error per family and per sheet.
Outputs: OUT/results.json, OUT/REPORT.md, OUT/runs/<dossier>/ (estimate.json, sheets.csv).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

from src.validation import compare_qpl as C

from . import conduits as K
from . import export as E
from . import gold as G
from . import model as M
from . import pipeline
from . import train as T
from .families import FAMILIES, INDETERMINE, LabelFamilyMap

RADII = (15.0, 25.0, 45.0)
PRIMARY_R = 25.0
LEAK_R = 15.0
ROOT = Path(__file__).resolve().parents[2]


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def _prf(tp: int, npred: int, ngold: int) -> dict:
    p = tp / npred if npred else None
    r = tp / ngold if ngold else None
    f1 = (2 * p * r / (p + r)) if p and r else (0.0 if p is not None and r is not None else None)
    return {"tp": tp, "predicted": npred, "gold": ngold, "precision": p, "recall": r, "f1": f1}


def sheets_csv_for(g: G.DossierGold, path: Path) -> Path:
    """Per-page metadata available to the pipeline for an image-only PDF: the sheet
    number / scale read by the earlier automatic pipeline (feuilles-classement.csv)
    and the paper width (feuilles-ia.csv). Nothing from the estimator."""
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["page", "name", "scale_ratio", "paper_width_pt"])
        for s in g.sheets:
            w.writerow([s.page + 1, s.display, s.scale_ratio or "", s.paper_width_pt or ""])
    return path


def ai_marks_page_xy(dossier_dir: Path, g: G.DossierGold) -> dict[int, np.ndarray]:
    """The other (automatic) takeoff's marks in page px, per page — for the leakage check."""
    out: dict[int, np.ndarray] = {}
    qpl = dossier_dir / "planexpert" / f"{dossier_dir.name}.qpl"
    fi = dossier_dir / "reference" / "feuilles-ia.csv"
    if not qpl.is_file():
        return out
    ias = C.lire_qpl(qpl, "ia")
    if fi.is_file():
        C.preparer_ia(ias, C.lire_feuilles(fi), None)
    by_name = {s.name: s for s in g.sheets}
    for p in ias:
        stem = Path(p.fichier).stem if p.fichier else p.nom
        sh = by_name.get(stem)
        if sh is None or not p.marques:
            continue
        if p.largeur:
            kx, ky = sh.page_width_px / p.largeur, sh.page_height_px / p.hauteur
        else:
            continue
        out[sh.page] = np.array([(m.x * kx, m.y * ky) for m in p.marques])
    return out


def score_position_dossier(g: G.DossierGold, sheets: list[E.SheetResult], ai_xy: dict[int, np.ndarray]) -> dict:
    pred_by_page = defaultdict(list)
    for s in sheets:
        for d in s.detections:
            pred_by_page[s.page].append(d)
    gold_by_page = defaultdict(list)
    for m in g.marks:
        gold_by_page[m.page].append(m)
    marked_pages = set(gold_by_page)
    pages = sorted(set(pred_by_page) | set(gold_by_page))

    def xy(items):
        return np.array([(i.x, i.y) for i in items], float).reshape(-1, 2)

    det = {}
    for scope in ("all_pages", "estimator_marked_pages"):
        det[scope] = {}
        for R in RADII:
            tp = npred = ngold = 0
            for pg in pages:
                if scope == "estimator_marked_pages" and pg not in marked_pages:
                    continue
                pr, gd = xy(pred_by_page[pg]), xy(gold_by_page[pg])
                tp += M.match(pr, gd, R); npred += len(pr); ngold += len(gd)
            det[scope][f"R{int(R)}"] = _prf(tp, npred, ngold)
    fam = {}
    for f in FAMILIES:
        tp = npred = ngold = 0
        for pg in pages:
            pr = xy([d for d in pred_by_page[pg] if d.family == f])
            gd = xy([m for m in gold_by_page[pg] if m.family == f])
            tp += M.match(pr, gd, PRIMARY_R); npred += len(pr); ngold += len(gd)
        if npred or ngold:
            e = _prf(tp, npred, ngold)
            e["unplaced_gold"] = int(g.unplaced.get(f, 0))
            e["count_error"] = (npred - ngold) / ngold if ngold else None
            fam[f] = e
    # occlusion split of recall (family-agnostic, primary radius)
    occ = {"visible": [0, 0], "occluded": [0, 0]}
    for pg in pages:
        prs = pred_by_page[pg]
        gds = gold_by_page[pg]
        flags = _gold_occlusion(g, pg, gds)
        for key, sel in (("visible", ~flags), ("occluded", flags)):
            gsub = xy([m for m, k in zip(gds, sel) if k])
            occ[key][0] += M.match(xy(prs), gsub, PRIMARY_R)
            occ[key][1] += len(gsub)
    occl = {k: {"gold": v[1], "matched": v[0], "recall": (v[0] / v[1]) if v[1] else None} for k, v in occ.items()}
    # leakage check
    near_pred = near_gold = n_pred = n_gold = 0
    for pg in pages:
        a = ai_xy.get(pg)
        prs, gds = xy(pred_by_page[pg]), xy(gold_by_page[pg])
        n_pred += len(prs); n_gold += len(gds)
        if a is None or not len(a):
            continue
        tree = cKDTree(a)
        if len(prs):
            near_pred += int((tree.query(prs)[0] <= LEAK_R).sum())
        if len(gds):
            near_gold += int((tree.query(gds)[0] <= LEAK_R).sum())
    leak = {"radius_px": LEAK_R, "predictions_near_other_takeoff": near_pred / n_pred if n_pred else None,
            "gold_near_other_takeoff": near_gold / n_gold if n_gold else None}
    # per sheet family counts
    per_sheet = []
    for s in sheets:
        gc = Counter(m.family for m in gold_by_page.get(s.page, []))
        pc = Counter(d.family for d in pred_by_page.get(s.page, []))
        per_sheet.append({"page": s.page + 1, "sheet": s.name, "gold_total": sum(gc.values()),
                          "predicted_total": sum(pc.values()), "gold": dict(gc), "predicted": dict(pc)})
    # conduits
    cond = []
    gold_ft = defaultdict(float)
    for ln in g.lines:
        if ln.length_ft and K.is_conduit_line(ln.name):
            gold_ft[ln.page] += ln.length_ft
    for s in sheets:
        if s.page in gold_ft and s.conduit_ft is not None:
            cond.append({"page": s.page + 1, "sheet": s.name, "estimator_ft": round(gold_ft[s.page], 1),
                         "estimated_ft": round(s.conduit_ft, 1),
                         "error": (s.conduit_ft - gold_ft[s.page]) / gold_ft[s.page]})
    totals = {"gold_placed": len(g.marks), "gold_unplaced": int(sum(g.unplaced.values())),
              "predicted": sum(len(v) for v in pred_by_page.values())}
    totals["count_error_vs_placed"] = (totals["predicted"] - totals["gold_placed"]) / totals["gold_placed"] if totals["gold_placed"] else None
    all_gold = totals["gold_placed"] + totals["gold_unplaced"]
    totals["count_error_vs_all_estimator_marks"] = (totals["predicted"] - all_gold) / all_gold if all_gold else None
    return {"detection": det, "families": fam, "occlusion": occl, "leakage": leak, "sheets": per_sheet,
            "conduits": cond, "totals": totals}


def _gold_occlusion(g: G.DossierGold, pg: int, gds) -> np.ndarray:
    from scipy import ndimage
    import pymupdf
    from . import features as F
    from . import pages as P
    key = (str(g.pdf), pg)
    if key not in _OCC_CACHE:
        page = P.load_page(pymupdf.open(g.pdf), pg)
        _OCC_CACHE[key] = M.readable_centre(page.overlay)
    ov = _OCC_CACHE[key]
    h, w = ov.shape
    return np.array([ov[min(h - 1, int(m.y)), min(w - 1, int(m.x))] > 0 for m in gds], bool)


_OCC_CACHE: dict = {}


def score_count_dossier(g: G.DossierGold, sheets: list[E.SheetResult], label_map: LabelFamilyMap) -> dict:
    G.finalize_count_families(g, label_map)
    gold_fam = Counter()
    gold_sheet_fam = defaultdict(Counter)
    for sh, _lab, f, q in g.counts:
        gold_fam[f] += q
        gold_sheet_fam[sh][f] += q
    pred_fam = Counter()
    pred_sheet_fam = defaultdict(Counter)
    for s in sheets:
        for d in s.detections:
            pred_fam[d.family] += 1
            pred_sheet_fam[s.name][d.family] += 1
    fam = {}
    for f in FAMILIES:
        if gold_fam[f] or pred_fam[f]:
            fam[f] = {"gold": gold_fam[f], "predicted": pred_fam[f],
                      "count_error": (pred_fam[f] - gold_fam[f]) / gold_fam[f] if gold_fam[f] else None}
    per_sheet = []
    for name in sorted(set(gold_sheet_fam) | set(pred_sheet_fam)):
        gt, pt = sum(gold_sheet_fam[name].values()), sum(pred_sheet_fam[name].values())
        per_sheet.append({"sheet": name, "gold_total": gt, "predicted_total": pt,
                          "gold": dict(gold_sheet_fam[name]), "predicted": dict(pred_sheet_fam[name])})
    gt, pt = sum(gold_fam.values()), sum(pred_fam.values())
    return {"families": fam, "sheets": per_sheet,
            "totals": {"gold": gt, "predicted": pt, "count_error": (pt - gt) / gt if gt else None}}


def run_fold(test: G.DossierGold, train_golds: list[G.DossierGold], out: Path, data_root: Path,
             model: M.Model | None = None) -> dict:
    t0 = time.time()
    if model is None:
        log(f"{test.dossier}: training on {[g.dossier for g in train_golds]}")
        model = T.train(train_golds, log=lambda m: log(m))
    run_dir = out / "runs" / test.dossier
    run_dir.mkdir(parents=True, exist_ok=True)
    sheets_csv = sheets_csv_for(test, run_dir / "sheets-input.csv")
    log(f"{test.dossier}: estimating {test.pdf.name} ({len(test.sheets)} pages)")
    sheets, _ = pipeline.run(test.pdf, model, sheets_csv, keep_gray=False, log=lambda m: log(m))
    E.write_json(run_dir / "estimate.json", test.pdf, sheets, model, {"evaluation_fold": test.dossier})
    E.write_sheets_csv(run_dir / "sheets.csv", sheets)
    res = {"dossier": test.dossier, "trained_on": model.trained_on, "threshold": model.threshold,
           "nms_radius": model.nms_radius, "conduit_ratio": model.conduit_ratio,
           "calibration_best": model.calibration.get("best") if model.calibration else None,
           "gold_type": "positions" if test.has_positions else "counts", "notes": test.notes}
    if test.has_positions:
        res.update(score_position_dossier(test, sheets, ai_marks_page_xy(data_root / test.dossier, test)))
    else:
        res.update(score_count_dossier(test, sheets, model.label_map))
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def pooled(results: list[dict]) -> dict:
    pos = [r for r in results if r["gold_type"] == "positions"]
    det = {}
    for scope in ("all_pages", "estimator_marked_pages"):
        det[scope] = {}
        for R in RADII:
            k = f"R{int(R)}"
            tp = sum(r["detection"][scope][k]["tp"] for r in pos)
            npred = sum(r["detection"][scope][k]["predicted"] for r in pos)
            ngold = sum(r["detection"][scope][k]["gold"] for r in pos)
            det[scope][k] = _prf(tp, npred, ngold)
    fam = {}
    for f in FAMILIES:
        tp = sum(r["families"].get(f, {}).get("tp", 0) for r in pos)
        npred = sum(r["families"].get(f, {}).get("predicted", 0) for r in pos)
        ngold = sum(r["families"].get(f, {}).get("gold", 0) for r in pos)
        if npred or ngold:
            e = _prf(tp, npred, ngold)
            e["count_error"] = (npred - ngold) / ngold if ngold else None
            errs = [abs(r["families"][f]["count_error"]) for r in pos
                    if f in r["families"] and r["families"][f]["count_error"] is not None]
            e["mean_abs_count_error_per_dossier"] = float(np.mean(errs)) if errs else None
            fam[f] = e
    occ = {}
    for k in ("visible", "occluded"):
        g = sum(r["occlusion"][k]["gold"] for r in pos)
        m = sum(r["occlusion"][k]["matched"] for r in pos)
        occ[k] = {"gold": g, "matched": m, "recall": m / g if g else None}
    cond = [c for r in pos for c in r["conduits"]]
    cond_s = {"sheets": len(cond),
              "median_abs_error": float(np.median([abs(c["error"]) for c in cond])) if cond else None}
    tot_err = [abs(r["totals"]["count_error_vs_placed"]) for r in pos if r["totals"]["count_error_vs_placed"] is not None]
    cnt = [r for r in results if r["gold_type"] == "counts"]
    return {"position_dossiers": [r["dossier"] for r in pos], "count_dossiers": [r["dossier"] for r in cnt],
            "detection": det, "families": fam, "occlusion": occ, "conduits": cond_s,
            "mean_abs_total_count_error_position_dossiers": float(np.mean(tot_err)) if tot_err else None}


def _pct(v) -> str:
    return "—" if v is None else f"{100 * v:.1f} %"


def _signed(v) -> str:
    return "—" if v is None else f"{100 * v:+.1f} %"


def write_report(path: Path, results: list[dict], pool: dict, meta: dict) -> None:
    L = ["# Estimator evaluation — leave-one-out vs M. Dupuis", "",
         f"Generated {meta['generated']} by `python -m src.estimer.evaluate` (commit {meta['commit']}). "
         "Every number below is computed from the files listed in `results.json`; nothing is typed in.", "",
         "## What was measured", "",
         "- **Input**: for each dossier, the only plan images available in this environment, `Plans-annotes.pdf` "
         "(one 2997 px raster page per sheet, no text layer, no vectors). These pages carry the coloured marks of an "
         "earlier automatic takeoff. The estimator never sees them as signal: coloured pixels are whitened, and during "
         "training the holes they leave are transplanted onto negative windows at the same rate as around the "
         "estimator's marks, so a hole alone carries no information. Detections whose window is under such mark-up are "
         "flagged `occluded_by_markup`.",
         "- **Gold**: M. Dupuis' own Plan Expert projects (`reference/*Dupuis*.qpl`) registered onto those pages "
         "(`src.validation.compare_qpl` page pairing + registration, duplicates removed). S-1857 has no Dupuis project "
         "in this environment; its gold is `reference-quantites.csv` (quantities per sheet, no positions), so only count "
         "errors are reported for it.",
         "- **Protocol**: leave-one-out. For each position dossier, the model (window classifier + calibrated threshold, "
         "label->family map, counter style, conduit ratio) is trained on the other position dossiers only. S-1857 is "
         "scored with the model trained on all five position dossiers.",
         f"- **Matching**: optimal one-to-one assignment within R px (page px at 2997 px width); primary R = {int(PRIMARY_R)} px, "
         "also 15 px and 45 px (45 px ≈ compare_qpl's 1.2 % of the diagonal). Families = `src.qpl.categorie` categories "
         "(keyword categoriser built from the 2021-2026 corpus, completed by co-location votes).", "",
         "## Pooled results (position dossiers)", "",
         "| Scope | R | Predicted | Gold | Matched | Precision | Recall | F1 |", "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for scope, lab in (("all_pages", "all pages"), ("estimator_marked_pages", "pages Dupuis marked")):
        for R in RADII:
            e = pool["detection"][scope][f"R{int(R)}"]
            L.append(f"| {lab} | {int(R)} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | "
                     f"{_pct(e['recall'])} | {_pct(e['f1'])} |")
    L += ["", f"### Per family (all pages, R = {int(PRIMARY_R)} px, same family required)", "",
          "| Family | Predicted | Gold | Matched | Precision | Recall | Total count error | Mean abs. count error per dossier |",
          "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for f, e in sorted(pool["families"].items(), key=lambda kv: -kv[1]["gold"]):
        L.append(f"| {f} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | {_pct(e['recall'])} | "
                 f"{_signed(e['count_error'])} | {_pct(e['mean_abs_count_error_per_dossier'])} |")
    o = pool["occlusion"]
    L += ["", "### Recall by visibility of the gold symbol (family-agnostic, R = 25 px)", "",
          "| Gold symbol | Gold | Matched | Recall |", "|---|--:|--:|--:|",
          f"| visible (no coloured mark-up at its centre) | {o['visible']['gold']} | {o['visible']['matched']} | {_pct(o['visible']['recall'])} |",
          f"| under coloured mark-up (drawing destroyed) | {o['occluded']['gold']} | {o['occluded']['matched']} | {_pct(o['occluded']['recall'])} |",
          "", f"Mean absolute total count error over position dossiers: {_pct(pool['mean_abs_total_count_error_position_dossiers'])}. "
          f"Conduit estimate: {pool['conduits']['sheets']} sheets comparable, median absolute error "
          f"{_pct(pool['conduits']['median_abs_error'])}.", "",
          "## Per dossier", "",
          "| Dossier | Gold | Trained on | Threshold | Predicted | Gold marks (placed / unplaced) | Total count error | P (R25) | R (R25) | F1 (R25) | Pred. near other takeoff | Gold near other takeoff |",
          "|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in results:
        if r["gold_type"] == "positions":
            e = r["detection"]["all_pages"]["R25"]
            t = r["totals"]
            L.append(f"| {r['dossier']} | Dupuis .qpl | {', '.join(r['trained_on'])} | {r['threshold']} | {t['predicted']} | "
                     f"{t['gold_placed']} / {t['gold_unplaced']} | {_signed(t['count_error_vs_placed'])} | {_pct(e['precision'])} | "
                     f"{_pct(e['recall'])} | {_pct(e['f1'])} | {_pct(r['leakage']['predictions_near_other_takeoff'])} | "
                     f"{_pct(r['leakage']['gold_near_other_takeoff'])} |")
        else:
            t = r["totals"]
            L.append(f"| {r['dossier']} | quantities only | {', '.join(r['trained_on'])} | {r['threshold']} | {t['predicted']} | "
                     f"{t['gold']} / — | {_signed(t['count_error'])} | — | — | — | — | — |")
    for r in results:
        L += ["", f"### {r['dossier']}", ""]
        L += ["| Family | Predicted | Gold | " + ("Matched | Precision | Recall | " if r["gold_type"] == "positions" else "")
              + "Count error |", "|---|--:|--:|" + ("--:|--:|--:|" if r["gold_type"] == "positions" else "") + "--:|"]
        for f, e in sorted(r["families"].items(), key=lambda kv: -kv[1]["gold"]):
            if r["gold_type"] == "positions":
                L.append(f"| {f} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | {_pct(e['recall'])} | {_signed(e['count_error'])} |")
            else:
                L.append(f"| {f} | {e['predicted']} | {e['gold']} | {_signed(e['count_error'])} |")
        L += ["", "| Sheet | Predicted | Gold |", "|---|--:|--:|"]
        for s in r["sheets"]:
            L.append(f"| {s['sheet']} | {s['predicted_total']} | {s['gold_total']} |")
        if r.get("conduits"):
            L += ["", "| Sheet | Dupuis conduit ft | Estimated ft | Error |", "|---|--:|--:|--:|"]
            for c in r["conduits"]:
                L.append(f"| {c['sheet']} | {c['estimator_ft']} | {c['estimated_ft']} | {_signed(c['error'])} |")
        if r.get("notes"):
            L += [""] + [f"- {n}" for n in r["notes"]]
    L += ["", "## Reading these numbers", "",
          "- The plan images used here are not the original drawings: an earlier takeoff's coloured marks cover most "
          "symbols (see the visibility table). Symbols under them can only be inferred from what remains around them "
          "(circuit tags, walls, leader lines). Results on clean original PDFs are expected to differ and must be "
          "measured once those PDFs (or Dupuis' PNGs) are in the environment.",
          "- The leakage columns compare how often predictions and the estimator's own marks fall within 15 px of the other "
          "takeoff's marks. Similar values mean the detector is not simply re-finding the coloured marks.",
          "- Conduit lengths are an estimate (learnt ratio × rectilinear tree over detected devices), not traced runs.",
          "- No price is involved anywhere (the estimator's projects carry none).", ""]
    path.write_text("\n".join(L), encoding="utf-8")


def git_commit() -> str:
    import subprocess
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.evaluate")
    ap.add_argument("--out", type=Path, default=ROOT / "eval")
    ap.add_argument("--data", type=Path, default=G.DATA_ROOT)
    ap.add_argument("--dossiers", default=",".join(G.ALL_DOSSIERS))
    ap.add_argument("--resume", action="store_true", help="reuse OUT/folds/<dossier>.json already computed")
    ap.add_argument("--save-full-model", type=Path, default=None,
                    help="also save the model trained on all position dossiers (used for count-only dossiers)")
    args = ap.parse_args(argv)
    wanted = [d.strip() for d in args.dossiers.split(",") if d.strip()]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "folds").mkdir(exist_ok=True)
    golds = {d: G.load(d, args.data) for d in G.ALL_DOSSIERS if (args.data / d).is_dir()}
    positions = [g for g in golds.values() if g.has_positions]
    results = []
    full_model = None
    for d in wanted:
        cache = args.out / "folds" / f"{d}.json"
        if args.resume and cache.is_file():
            log(f"{d}: reusing {cache}")
            results.append(json.loads(cache.read_text(encoding="utf-8")))
            continue
        test = golds[d]
        if test.has_positions:
            res = run_fold(test, [g for g in positions if g.dossier != d], args.out, args.data)
        else:
            if full_model is None:
                full_model = T.train(positions, log=lambda m: log(m))
                if args.save_full_model:
                    args.save_full_model.parent.mkdir(parents=True, exist_ok=True)
                    full_model.save(args.save_full_model)
            res = run_fold(test, positions, args.out, args.data, model=full_model)
        cache.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
        log(f"{d}: done in {res['elapsed_s']} s")
        results.append(res)
    pool = pooled(results)
    meta = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "commit": git_commit(),
            "data_root": str(args.data), "radii_px": list(RADII), "primary_radius_px": PRIMARY_R}
    out = {"meta": meta, "pooled": pool, "dossiers": results}
    (args.out / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    write_report(args.out / "REPORT.md", results, pool, meta)
    log(f"results -> {args.out / 'results.json'}, {args.out / 'REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
