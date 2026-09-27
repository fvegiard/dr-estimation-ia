"""Train the estimator model on the Dupuis references.

  python -m src.estimer.train [--dossiers S-1714,S-1715,...] [--out models/estimer.joblib]

Steps (all learnt, nothing per-dossier hard-coded):
1. load each reference (gold.py) — marks placed on the plan pages, families;
2. calibration: split the training dossiers in two groups, train on one, score
   the other's marked pages (and vice versa), pick threshold / NMS radius by F1;
3. fit the final classifier on all training dossiers;
4. learn the label -> family map (co-location votes), the estimator's counter
   style per family and the conduit ratio.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pymupdf

from . import conduits as K
from . import gold as G
from . import model as M
from . import pages as P

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = ROOT / "models" / "estimer.joblib"
MATCH_RADIUS_PX = 25.0          # calibration matching radius (page px at 2997 px width)
CALIB_PAGES_PER_DOSSIER = 8


def _split_groups(golds: list[G.DossierGold]) -> tuple[list[G.DossierGold], list[G.DossierGold]]:
    """Two groups with balanced mark counts (greedy, largest first)."""
    a, b, na, nb = [], [], 0, 0
    for g in sorted(golds, key=lambda g: -len(g.marks)):
        if na <= nb:
            a.append(g); na += len(g.marks)
        else:
            b.append(g); nb += len(g.marks)
    return a, b


def _calib_pages(g: G.DossierGold, rng: np.random.Generator) -> list[int]:
    marked = sorted({m.page for m in g.marks})
    if len(marked) > CALIB_PAGES_PER_DOSSIER:
        marked = sorted(rng.choice(marked, CALIB_PAGES_PER_DOSSIER, replace=False).tolist())
    return marked


def readable_split(g: G.DossierGold, pg: int) -> tuple[np.ndarray, np.ndarray]:
    """(all estimator marks, marks whose symbol core is readable) on one page, page px."""
    xy = np.array([(m.x, m.y) for m in g.marks if m.page == pg], float).reshape(-1, 2)
    page = P.load_page(pymupdf.open(g.pdf), pg)
    core = M.readable_centre(page.overlay)
    h, w = core.shape
    ok = np.array([core[min(h - 1, int(y)), min(w - 1, int(x))] <= 0 for x, y in xy], bool)
    return xy, xy[ok] if len(xy) else xy


def score_pages(model: M.Model, g: G.DossierGold, pages: list[int]):
    doc = pymupdf.open(g.pdf)
    out = []
    for pg in pages:
        page = P.load_page(doc, pg)
        xs, ys, proba, occ = model.score_page(page)
        out.append(((g.dossier, pg), page.shape, xs, ys, proba, occ, model))
    return out


def conduit_pairs(golds: list[G.DossierGold]) -> list[tuple[float, float]]:
    """(estimator conduit-line length, rectilinear tree over his own marks), both in
    page px, per sheet where he set a scale (his lines there are measured runs).
    The scale cancels out of the ratio."""
    pairs = []
    for g in golds:
        by_page = defaultdict(list)
        for m in g.marks:
            by_page[m.page].append((m.x, m.y))
        px_by_page = defaultdict(float)
        for ln in g.lines:
            if ln.length_ft and K.is_conduit_line(ln.name):
                px_by_page[ln.page] += ln.length_px_page
        for pg, px in px_by_page.items():
            if len(by_page.get(pg, [])) < 2:
                continue
            tree_px, _ = K.tree_length_px(np.array(by_page[pg]))
            pairs.append((px, tree_px))
    return pairs


def train(golds: list[G.DossierGold], seed: int = 0, calibrate: bool = True, log=print) -> M.Model:
    golds = [g for g in golds if g.has_positions]
    rng = np.random.default_rng(seed)
    calib = {}
    if calibrate and len(golds) >= 2:
        ga, gb = _split_groups(golds)
        scored, gxy = [], {}
        for train_g, test_g in ((ga, gb), (gb, ga)):
            t = time.time()
            X, y = M.build_training_set(train_g, seed=seed, log=log)
            clf, classes = M.fit(X, y, seed=seed)
            inner = M.Model(clf, classes)
            log(f"  calibration model on {[g.dossier for g in train_g]}: {len(y)} samples, {time.time() - t:.0f}s")
            for g in test_g:
                pages = _calib_pages(g, rng)
                scored += score_pages(inner, g, pages)
                for pg in pages:
                    gxy[(g.dossier, pg)] = readable_split(g, pg)
        calib = M.calibrate(scored, gxy, MATCH_RADIUS_PX)
        log(f"  calibration best: {calib['best']}")
    t = time.time()
    X, y = M.build_training_set(golds, seed=seed, log=log)
    clf, classes = M.fit(X, y, seed=seed)
    log(f"  final model: {len(y)} samples, {clf.n_iter_} iterations, {time.time() - t:.0f}s")
    model = M.Model(clf, classes)
    if calib:
        model.threshold = calib["best"]["threshold"]
        model.nms_radius = calib["best"]["nms_radius"]
        model.calibration = calib
    for g in golds:
        model.label_map.merge(g.label_map)
    model.family_style = M.family_styles(golds)
    model.conduit_ratio = K.learn_ratio(conduit_pairs(golds))
    model.trained_on = [g.dossier for g in golds]
    return model


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.train")
    ap.add_argument("--dossiers", default=",".join(G.POSITION_DOSSIERS))
    ap.add_argument("--data", type=Path, default=G.DATA_ROOT)
    ap.add_argument("--out", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    golds = [G.load(d.strip(), args.data) for d in args.dossiers.split(",") if d.strip()]
    model = train(golds, seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.out)
    summary = {"trained_on": model.trained_on, "threshold": model.threshold, "nms_radius": model.nms_radius,
               "conduit_ratio": model.conduit_ratio, "classes": model.classes,
               "family_style": model.family_style}
    args.out.with_suffix(".json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"model -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
