"""Leave-one-out evaluation against the estimator's (M. Dupuis) references.

  python -m src.estimer.evaluate [--out eval] [--dossiers ...] [--resume] [--gold original|annotes]

Input plans: by default the ORIGINAL bid-package PDFs (`--gold original`,
gold_original.py through src/estimer/data/plan_index.json); `--gold annotes`
is the legacy run on the annotated renders `Plans-annotes.pdf`.
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
        sh = g.sheets[g.ia_sheet_page[stem]] if stem in g.ia_sheet_page else by_name.get(stem)
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
    """Count-only gold. Rows of sheets that are not pages of the evaluated PDF (e.g. an
    addendum version of a sheet) are kept aside as "outside the PDF", like unplaced
    marks of position gold; errors are computed on the sheets present in the PDF."""
    G.finalize_count_families(g, label_map)
    in_pdf = {s.name for s in sheets} | {s.display for s in g.sheets}
    gold_fam = Counter()
    outside_fam = Counter()
    gold_sheet_fam = defaultdict(Counter)
    for sh, _lab, f, q in g.counts:
        if sh in in_pdf:
            gold_fam[f] += q
            gold_sheet_fam[sh][f] += q
        else:
            outside_fam[f] += q
    pred_fam = Counter()
    pred_sheet_fam = defaultdict(Counter)
    for s in sheets:
        for d in s.detections:
            pred_fam[d.family] += 1
            pred_sheet_fam[s.name][d.family] += 1
    fam = {}
    for f in FAMILIES:
        if gold_fam[f] or pred_fam[f]:
            fam[f] = {"gold": gold_fam[f], "predicted": pred_fam[f], "gold_outside_pdf": outside_fam[f],
                      "count_error": (pred_fam[f] - gold_fam[f]) / gold_fam[f] if gold_fam[f] else None}
    per_sheet = []
    for name in sorted(set(gold_sheet_fam) | set(pred_sheet_fam)):
        gt, pt = sum(gold_sheet_fam[name].values()), sum(pred_sheet_fam[name].values())
        per_sheet.append({"sheet": name, "gold_total": gt, "predicted_total": pt,
                          "gold": dict(gold_sheet_fam[name]), "predicted": dict(pred_sheet_fam[name])})
    gt, pt, go = sum(gold_fam.values()), sum(pred_fam.values()), sum(outside_fam.values())
    return {"families": fam, "sheets": per_sheet,
            "totals": {"gold": gt, "gold_outside_pdf": go, "predicted": pt,
                       "count_error": (pt - gt) / gt if gt else None,
                       "count_error_vs_all_estimator_rows": (pt - gt - go) / (gt + go) if gt + go else None},
            "sheets_outside_pdf": sorted({sh for sh, *_ in g.counts if sh not in in_pdf})}


def run_fold(test: G.DossierGold, train_golds: list[G.DossierGold], out: Path, data_root: Path,
             model: M.Model | None = None, family_balance: bool = False) -> dict:
    t0 = time.time()
    if model is None:
        log(f"{test.dossier}: training on {[g.dossier for g in train_golds]}")
        model = T.train(train_golds, log=lambda m: log(m), family_balance=family_balance)
    run_dir = out / "runs" / test.dossier
    run_dir.mkdir(parents=True, exist_ok=True)
    sheets_csv = sheets_csv_for(test, run_dir / "sheets-input.csv")
    log(f"{test.dossier}: estimating {test.pdf.name} ({len(test.sheets)} pages)")
    sheets, _, _codes = pipeline.run(test.pdf, model, sheets_csv, keep_gray=False, log=lambda m: log(m))
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
    sum_pred = sum(r["totals"]["predicted"] for r in pos)
    sum_gold = sum(r["totals"]["gold_placed"] for r in pos)
    cnt = [r for r in results if r["gold_type"] == "counts"]
    return {"position_dossiers": [r["dossier"] for r in pos], "count_dossiers": [r["dossier"] for r in cnt],
            "detection": det, "families": fam, "occlusion": occ, "conduits": cond_s,
            "mean_abs_total_count_error_position_dossiers": float(np.mean(tot_err)) if tot_err else None,
            "total_count_error_pooled_position_dossiers": (sum_pred - sum_gold) / sum_gold if sum_gold else None,
            "predicted_total_position_dossiers": sum_pred, "gold_placed_total_position_dossiers": sum_gold}


def _pct(v) -> str:
    return "—" if v is None else f"{100 * v:.1f} %"


def _signed(v) -> str:
    return "—" if v is None else f"{100 * v:+.1f} %"


def _fam_fr(f: str) -> str:
    return f.replace("_", " ")


def write_report(path: Path, results: list[dict], pool: dict, meta: dict) -> None:
    """REPORT.md (in French: it is a deliverable for the estimating team)."""
    L = ["# Évaluation de l'estimateur automatique — validation croisée « un dossier exclu » contre M. Dupuis", "",
         f"Généré le {meta['generated']} par `python -m src.estimer.evaluate --gold {meta.get('gold_source', 'annotes')}` "
         f"(commit {meta['commit']}). "
         "Chaque nombre ci-dessous est calculé à partir des fichiers ; rien n'est saisi à la main. "
         "Détail complet : `eval/results.json` ; sorties de chaque dossier : `eval/runs/<dossier>/`.", "",
         "## Ce qui a été mesuré", ""]
    if meta.get("gold_source", "annotes") == "original":
        L += ["- **Entrée** : les PDF ORIGINAUX des appels d'offres (`entree/plans-originaux/*.pdf`, vectoriels avec couche "
              "texte ; indexés par `python -m src.estimer.plan_index`), jamais les rendus annotés `Plans-annotes.pdf`. "
              "Un dossier à plusieurs PDF (original + addendas) est évalué comme un seul PDF concaténé (pages dans "
              "l'ordre de l'index) ; les PDF sans aucun plan de l'estimateur (listes de feuilles scannées) sont exclus. "
              "Chaque page est rendue à 2997 px de large. Les pixels nettement colorés (nuages de révision, trames de "
              "couleur) sont toujours traités comme illisibles par le détecteur, comme avant ; leur part est faible ici.",
              "- **Référence (vérité)** : les marques des projets Plan Expert de M. Dupuis (`reference/*Dupuis*.qpl`), "
              "placées sur les pages par l'index : quand son plan est apparié à une page par son nom (`<pdf> - n`) et que "
              "la taille de son raster est connue, la marque est convertie directement (pixel de son raster → pixel de la "
              "page ; aucun autre relevé n'intervient). Pour le reste — rasters de taille inconnue (S-1811, 5 pages de "
              "l'addenda MEP01 exportées en JPG) ou plans d'un document absent de plans-originaux (S-1844, feuilles "
              "électriques du cahier global 23347) — c'est le recalage géométrique de `src.validation.compare_qpl` (une "
              "similitude par page, sur les rasters du relevé automatique, puis `feuilles-ia.csv` pour retrouver la "
              "page du PDF) qui les place ; ces cas sont comptés dans les notes de chaque dossier. Une page importée deux "
              "fois par l'estimateur (S-1714, E401–E408) est fusionnée : les doublons à moins de 1,2 % de la diagonale "
              "sont retirés. Une feuille marquée dans l'original ET dans son addenda garde ses deux jeux de marques : les "
              "deux pages sont dans l'entrée. S-1857 n'a pas de projet Dupuis dans cet environnement (voir sa section) ; "
              "sa vérité est `reference-quantites.csv` (quantités par feuille, sans position) : seuls des écarts de "
              "quantité y sont calculés.",
              "- **Protocole** : un dossier exclu à la fois. Pour chaque dossier à positions, le modèle (classifieur de "
              "fenêtres + seuil calibré, correspondance libellé → famille, style des compteurs, ratio de conduit) est "
              "appris sur les autres dossiers à positions seulement. S-1857 est évalué avec le modèle appris sur les cinq "
              "dossiers à positions. La lecture des légendes (`legend.py`, codes de la couche texte) est active : les "
              "PDF ont une couche texte (sauf les pages à polices vectorisées, cartouche lu par OCR dans l'index)."]
    else:
        L += [         "- **Entrée** : pour chaque dossier, les seules images de plans disponibles dans cet environnement, "
         "`Plans-annotes.pdf` (une page raster de 2997 px par feuille, sans couche texte ni vectoriel). Ces pages portent "
         "les marques de couleur opaques d'un relevé automatique antérieur, dessinées par-dessus les symboles. "
         "L'estimateur traite les pixels colorés comme illisibles : une fenêtre dont le cœur du symbole (13 × 13 px au "
         "centre) touche une marque de couleur n'est jamais évaluée ni utilisée à l'entraînement ; ces zones sont "
         "signalées par feuille (`unreadable_markup_zones`) au lieu d'être comptées. Les marques de couleur ailleurs dans "
         "la fenêtre sont rendues non informatives en les transplantant sur des fenêtres négatives au même taux.",
         "- **Référence (vérité)** : les projets Plan Expert de M. Dupuis (`reference/*Dupuis*.qpl`), recalés sur ces pages "
         "(appariement de pages et recalage de `src.validation.compare_qpl`, doublons retirés). S-1857 n'a pas de projet "
         "Dupuis dans cet environnement ; sa vérité est `reference-quantites.csv` (quantités par feuille, sans position) : "
         "seuls des écarts de quantité sont donc calculés pour ce dossier.",
         "- **Protocole** : un dossier exclu à la fois. Pour chaque dossier à positions, le modèle (classifieur de fenêtres + "
         "seuil calibré, correspondance libellé → famille, style des compteurs, ratio de conduit) est appris sur les autres "
         "dossiers à positions seulement. S-1857 est évalué avec le modèle appris sur les cinq dossiers à positions."]
    L += [         f"- **Appariement** : affectation optimale un-à-un à moins de R px (px de page, largeur 2997 px) ; R principal = "
         f"{int(PRIMARY_R)} px, aussi 15 px et 45 px (45 px ≈ le seuil de 1,2 % de la diagonale de compare_qpl). Familles = "
         "catégories de `src.qpl.categorie` (catégoriseur par mots-clés construit sur le corpus 2021-2026, complété par "
         "des votes de co-localisation).", "",
         "## Résultats groupés (dossiers à positions)", "",
         "| Portée | R (px) | Prédits | Dupuis | Appariés | Précision | Rappel | F1 |", "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for scope, lab in (("all_pages", "toutes les pages"), ("estimator_marked_pages", "pages marquées par Dupuis")):
        for R in RADII:
            e = pool["detection"][scope][f"R{int(R)}"]
            L.append(f"| {lab} | {int(R)} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | "
                     f"{_pct(e['recall'])} | {_pct(e['f1'])} |")
    o = pool["occlusion"]
    L += ["", f"### Rappel selon la lisibilité du symbole de Dupuis (toutes familles, R = {int(PRIMARY_R)} px)", "",
          "La première ligne est la qualité du détecteur sans fuite possible : symboles dont le cœur est visible sur la page.", "",
          "| Symbole de Dupuis | Nombre | Appariés | Rappel |", "|---|--:|--:|--:|",
          f"| lisible (aucune marque de couleur sur le cœur) | {o['visible']['gold']} | {o['visible']['matched']} | {_pct(o['visible']['recall'])} |",
          f"| cœur sous une marque de couleur (dessin détruit, non compté par conception) | {o['occluded']['gold']} | "
          f"{o['occluded']['matched']} | {_pct(o['occluded']['recall'])} |",
          "", f"### Par famille (toutes les pages, R = {int(PRIMARY_R)} px, même famille exigée)", "",
          "| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité total | Écart absolu moyen par dossier |",
          "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for f, e in sorted(pool["families"].items(), key=lambda kv: -kv[1]["gold"]):
        L.append(f"| {_fam_fr(f)} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | {_pct(e['recall'])} | "
                 f"{_signed(e['count_error'])} | {_pct(e['mean_abs_count_error_per_dossier'])} |")
    L += ["", f"Écart de quantité totale groupé (Σ prédits {pool.get('predicted_total_position_dossiers', '—')} contre "
          f"Σ marques Dupuis placées {pool.get('gold_placed_total_position_dossiers', '—')}) : "
          f"{_signed(pool.get('total_count_error_pooled_position_dossiers'))} ; écart absolu moyen par dossier : "
          f"{_pct(pool['mean_abs_total_count_error_position_dossiers'])}. Conduits : {pool['conduits']['sheets']} feuilles "
          f"comparables, écart absolu médian {_pct(pool['conduits']['median_abs_error'])}.", "",
          "## Par dossier", "",
          "| Dossier | Vérité | Appris sur | Seuil | Prédits | Marques Dupuis (placées / hors page) | Écart de quantité | "
          "P (R25) | R (R25) | F1 (R25) | Prédictions près du relevé antérieur | Dupuis près du relevé antérieur |",
          "|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in results:
        if r["gold_type"] == "positions":
            e = r["detection"]["all_pages"]["R25"]
            t = r["totals"]
            L.append(f"| {r['dossier']} | .qpl Dupuis | {', '.join(r['trained_on'])} | {r['threshold']} | {t['predicted']} | "
                     f"{t['gold_placed']} / {t['gold_unplaced']} | {_signed(t['count_error_vs_placed'])} | {_pct(e['precision'])} | "
                     f"{_pct(e['recall'])} | {_pct(e['f1'])} | {_pct(r['leakage']['predictions_near_other_takeoff'])} | "
                     f"{_pct(r['leakage']['gold_near_other_takeoff'])} |")
        else:
            t = r["totals"]
            L.append(f"| {r['dossier']} | quantités seulement | {', '.join(r['trained_on'])} | {r['threshold']} | {t['predicted']} | "
                     f"{t['gold']} / {t.get('gold_outside_pdf', '—')} | {_signed(t['count_error'])} | — | — | — | — | — |")
    for r in results:
        pos = r["gold_type"] == "positions"
        L += ["", f"### {r['dossier']}", ""]
        L += ["| Famille | Prédits | Dupuis | " + ("Appariés | Précision | Rappel | " if pos else "") + "Écart de quantité |",
              "|---|--:|--:|" + ("--:|--:|--:|" if pos else "") + "--:|"]
        for f, e in sorted(r["families"].items(), key=lambda kv: -kv[1]["gold"]):
            if pos:
                L.append(f"| {_fam_fr(f)} | {e['predicted']} | {e['gold']} | {e['tp']} | {_pct(e['precision'])} | "
                         f"{_pct(e['recall'])} | {_signed(e['count_error'])} |")
            else:
                L.append(f"| {_fam_fr(f)} | {e['predicted']} | {e['gold']} | {_signed(e['count_error'])} |")
        L += ["", "| Feuille | Prédits | Dupuis |", "|---|--:|--:|"]
        for sh in r["sheets"]:
            L.append(f"| {sh['sheet']} | {sh['predicted_total']} | {sh['gold_total']} |")
        if pos:
            oc = r["occlusion"]
            L += ["", f"Marques de Dupuis lisibles : {oc['visible']['gold']} sur {oc['visible']['gold'] + oc['occluded']['gold']} ; "
                  f"rappel sur celles-ci (R = 25 px) : {_pct(oc['visible']['recall'])}."]
            cb = r.get("calibration_best")
            if cb:
                L += [f"Calibration (dossiers d'entraînement mis de côté) : seuil {cb['threshold']}, rayon NMS "
                      f"{cb['nms_radius']} px, précision {_pct(cb['precision'])}, rappel sur marques lisibles "
                      f"{_pct(cb['recall_readable'])}."]
        if r.get("conduits"):
            L += ["", "| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |", "|---|--:|--:|--:|"]
            for c in r["conduits"]:
                L.append(f"| {c['sheet']} | {c['estimator_ft']} | {c['estimated_ft']} | {_signed(c['error'])} |")
        if r.get("sheets_outside_pdf"):
            L += ["", f"Feuilles du relevé de Dupuis absentes du PDF évalué (quantités mises à part, "
                  f"{r['totals'].get('gold_outside_pdf')} au total ; écart y compris ces feuilles : "
                  f"{_signed(r['totals'].get('count_error_vs_all_estimator_rows'))}) : {', '.join(r['sheets_outside_pdf'])}."]
        if r.get("notes"):
            L += [""] + [f"- {n}" for n in r["notes"]]
    L += ["", "## Lecture de ces chiffres", ""]
    if meta.get("gold_source", "annotes") == "original":
        L += ["- Les entrées sont les dessins d'origine : le détecteur voit tous les symboles, et les colonnes « près du "
              "relevé antérieur » n'ont plus de sens de fuite (aucune marque de couleur n'est dessinée sur ces pages) ; "
              "elles restent calculées à titre de contrôle (part des prédictions et des marques de Dupuis à moins de 15 px "
              "d'une marque du relevé automatique de la même feuille).",
              "- Précision et rappel sont mesurés contre les marques de l'estimateur telles qu'il les a posées (souvent au "
              "coin du symbole, pas au centre) ; R = 25 px absorbe cet écart pour les symboles courants, pas pour les "
              "grands appareils.",
              "- Les marques placées par recalage (S-1811 addenda MEP01, S-1844) dépendent de la similitude estimée par "
              "compare_qpl : une erreur globale de recalage sur une page déplace toutes ses marques ; vérifié visuellement "
              "sur S-1811 505B (addenda) et S-1844 E300 avant cette évaluation (marques sur les symboles).",
              "- Les longueurs de conduit sont une estimation (ratio appris × arbre rectilinéaire sur les appareils "
              "détectés), pas un tracé des parcours.",
              "- Aucun prix n'intervient (les projets de l'estimateur n'en contiennent pas).", ""]
    else:
        L += [          "- Les images de plans utilisées ici ne sont pas les dessins d'origine : les marques de couleur opaques d'un relevé "
          "antérieur couvrent le cœur de la plupart des symboles (voir le tableau de lisibilité). Ces symboles ne sont pas "
          "comptés, par conception : les compter reviendrait à retrouver les marques du relevé antérieur, pas à lire le "
          "dessin. Le rappel de bout en bout et les écarts de quantité sur ces entrées sont donc bornés par la part lisible ; "
          "la performance sur des PDF d'origine propres (ou sur les PNG de Dupuis) reste à mesurer dès que ces fichiers "
          "seront dans l'environnement.",
          "- Les colonnes « près du relevé antérieur » comparent la part des prédictions et celle des marques de Dupuis situées "
          "à moins de 15 px d'une marque du relevé antérieur. Des valeurs proches ou plus basses pour les prédictions "
          "montrent que le détecteur ne retrouve pas simplement les marques de couleur.",
          "- La lecture des légendes (codes de la couche texte, `legend.py`) ne s'active pas ici : les PDF évalués sont des "
          "images sans mots. Seul le détecteur visuel est mesuré.",
          "- Les longueurs de conduit sont une estimation (ratio appris × arbre rectilinéaire sur les appareils détectés), "
          "pas un tracé des parcours.",
          "- Aucun prix n'intervient (les projets de l'estimateur n'en contiennent pas).", ""]
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
    ap.add_argument("--report-only", action="store_true", help="rebuild REPORT.md from OUT/results.json")
    ap.add_argument("--full-model", type=Path, default=None,
                    help="reuse this model (trained on all position dossiers) for count-only dossiers instead of training")
    ap.add_argument("--save-full-model", type=Path, default=None,
                    help="also save the model trained on all position dossiers (used for count-only dossiers)")
    ap.add_argument("--family-balance", action="store_true",
                    help="train with family re-balancing sample weights (model.family_balance_weights)")
    ap.add_argument("--gold", choices=G.GOLD_SOURCES, default="original",
                    help="original = the original bid-package PDFs through plan_index.json (default); "
                         "annotes = legacy Plans-annotes.pdf renders")
    args = ap.parse_args(argv)
    wanted = [d.strip() for d in args.dossiers.split(",") if d.strip()]
    if args.report_only:
        data = json.loads((args.out / "results.json").read_text(encoding="utf-8"))
        write_report(args.out / "REPORT.md", data["dossiers"], data["pooled"], data["meta"])
        log(f"report -> {args.out / 'REPORT.md'}")
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "folds").mkdir(exist_ok=True)
    golds = {d: G.load(d, args.data, source=args.gold) for d in G.ALL_DOSSIERS if (args.data / d).is_dir()}
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
            res = run_fold(test, [g for g in positions if g.dossier != d], args.out, args.data,
                           family_balance=args.family_balance)
        else:
            if full_model is None and args.full_model:
                full_model = M.Model.load(args.full_model)
                if sorted(full_model.trained_on) != sorted(g.dossier for g in positions):
                    raise SystemExit(f"{args.full_model} was trained on {full_model.trained_on}, not on all position dossiers")
            if full_model is None:
                full_model = T.train(positions, log=lambda m: log(m), family_balance=args.family_balance)
                if args.save_full_model:
                    args.save_full_model.parent.mkdir(parents=True, exist_ok=True)
                    full_model.save(args.save_full_model)
                    T.write_summary(full_model, args.save_full_model.with_suffix(".json"))
            res = run_fold(test, positions, args.out, args.data, model=full_model)
        cache.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
        log(f"{d}: done in {res['elapsed_s']} s")
        results.append(res)
    pool = pooled(results)
    meta = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "commit": git_commit(),
            "data_root": str(args.data), "gold_source": args.gold, "family_balance": args.family_balance,
            "radii_px": list(RADII), "primary_radius_px": PRIMARY_R}
    out = {"meta": meta, "pooled": pool, "dossiers": results}
    (args.out / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    write_report(args.out / "REPORT.md", results, pool, meta)
    log(f"results -> {args.out / 'results.json'}, {args.out / 'REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
