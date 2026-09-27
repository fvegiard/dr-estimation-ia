"""Symbol detector learnt from the estimator's reference takeoffs.

Readable windows only. The only plan images available for the reference
dossiers carry another takeoff's coloured marks, which pages.py whitens; the
drawing under them is gone. A window whose symbol core touches
such mark-up is never scored and never used for training: the detector only
learns from, and only reports, symbols it can actually see (core = central
13x13 px, features.READABLE_HALF). Mark-up zones are
reported per sheet as unreadable instead (pipeline.py).

Training (`build_training_set` + `fit`):
  positives  = the estimator's marks whose central square is readable, plus
               jittered copies; class = the mark's family;
  negatives  = readable candidate windows (features.candidate_grid) farther
               than NEG_MIN_DIST px from any estimator mark, on pages he marked.
  Residual leakage guard: mark-up can still sit in the outer part of a window.
  Its masks around positives are transplanted onto negatives at the same rate
  and offset, so "mark-up nearby" carries no information either.
  Classifier: sklearn HistGradientBoostingClassifier (families + "none").
  Optional hard-negative refit (`fit_with_mining`, off by default): measured on
  the S-1844 fold it did not help (precision 13.1 % vs 13.9 %, recall on
  readable marks 17.6 % vs 20.0 %, R = 25 px).

Detection (`Model.detect`): score readable candidate windows on a stride grid,
p_symbol = 1 - p(none), keep local maxima above a threshold with non-maximum
suppression, family = most probable non-"none" class. Threshold and NMS radius
are calibrated on held-out dossiers (train.py).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import joblib
import numpy as np
import pymupdf
from scipy import ndimage
from scipy.optimize import linear_sum_assignment
from scipy.spatial import cKDTree
from sklearn.ensemble import HistGradientBoostingClassifier

from . import features as F
from . import pages as P
from .families import INDETERMINE, LabelFamilyMap
from .gold import DossierGold

NONE = "none"
STRIDE = 6
NEG_MIN_DIST = 24.0        # px: a negative window is at least this far from any estimator mark
NEG_PER_POS = 6
JITTER = 3
JITTER_COPIES = 3
NEAR_MARKUP_MIN = 1e-6     # any mark-up inside the 64 px window flags a detection "near_coloured_markup"


@dataclass
class Detection:
    page: int
    x: float
    y: float
    family: str
    score: float
    family_prob: float
    near_markup: bool
    source: str = "visual"          # "visual" | "text_tag" | "visual+text_tag"
    tag: str | None = None


@dataclass
class Model:
    clf: HistGradientBoostingClassifier
    classes: list[str]
    threshold: float = 0.5
    nms_radius: float = 18.0
    stride: int = STRIDE
    label_map: LabelFamilyMap = field(default_factory=LabelFamilyMap)
    # family -> (counter name, Shape, DefaultSize, Color) learnt from the estimator's counters
    family_style: dict[str, tuple[str, int, int, int]] = field(default_factory=dict)
    conduit_ratio: float | None = None       # estimator conduit ft / device-tree ft
    trained_on: list[str] = field(default_factory=list)
    calibration: dict = field(default_factory=dict)

    # ------------------------------------------------------------------ scoring
    def score_page(self, page: P.PageImage) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        xs, ys = F.candidate_grid(page.gray, page.overlay, self.stride)
        if len(xs) == 0:
            return xs, ys, np.zeros((0, len(self.classes)), np.float32), np.zeros(0, bool)
        dense = F.DenseFeatures(page.gray)
        proba = np.empty((len(xs), len(self.classes)), np.float32)
        for i in range(0, len(xs), 50000):
            proba[i:i + 50000] = self.clf.predict_proba(dense.at(xs[i:i + 50000], ys[i:i + 50000]))
        ov = ndimage.uniform_filter(page.overlay.astype(np.float32), F.PATCH, mode="constant")
        near = ov[ys, xs] >= NEAR_MARKUP_MIN
        return xs, ys, proba, near

    def peaks(self, page_index: int, shape: tuple[int, int], xs, ys, proba, near,
              threshold: float | None = None, nms_radius: float | None = None) -> list[Detection]:
        thr = self.threshold if threshold is None else threshold
        rad = self.nms_radius if nms_radius is None else nms_radius
        if len(xs) == 0:
            return []
        none_i = self.classes.index(NONE)
        psym = 1.0 - proba[:, none_i]
        h, w = shape
        gh, gw = (h + self.stride - 1) // self.stride, (w + self.stride - 1) // self.stride
        gx, gy = xs // self.stride, ys // self.stride
        grid = np.zeros((gh, gw), np.float32)
        grid[gy, gx] = psym
        k = max(1, int(round(rad / self.stride)))
        mx = ndimage.maximum_filter(grid, size=2 * k + 1, mode="constant")
        is_peak = (grid[gy, gx] >= mx[gy, gx]) & (psym >= thr)
        idx = np.nonzero(is_peak)[0]
        # plateau ties: keep one per NMS radius
        idx = idx[np.argsort(-psym[idx])]
        kept: list[int] = []
        if len(idx):
            tree = cKDTree(np.c_[xs[idx], ys[idx]])
            dead = np.zeros(len(idx), bool)
            for j in range(len(idx)):
                if dead[j]:
                    continue
                kept.append(idx[j])
                for q in tree.query_ball_point([xs[idx[j]], ys[idx[j]]], rad):
                    if q != j:
                        dead[q] = True
        fam_cols = [i for i, c in enumerate(self.classes) if c != NONE]
        out = []
        for i in kept:
            pf = proba[i, fam_cols]
            j = int(np.argmax(pf))
            out.append(Detection(page_index, float(xs[i]), float(ys[i]), self.classes[fam_cols[j]],
                                 float(psym[i]), float(pf[j] / max(psym[i], 1e-6)), bool(near[i])))
        return out

    def detect(self, page: P.PageImage) -> list[Detection]:
        xs, ys, proba, occ = self.score_page(page)
        return self.peaks(page.index, page.shape, xs, ys, proba, occ)

    def save(self, path: Path) -> None:
        joblib.dump(self, path, compress=3)

    @staticmethod
    def load(path: Path) -> "Model":
        return joblib.load(path)


# ---------------------------------------------------------------------- training
def readable_centre(overlay: np.ndarray) -> np.ndarray:
    """Float map: overlay fraction of the symbol core around each pixel (0 = readable)."""
    return ndimage.uniform_filter(overlay.astype(np.float32), 2 * F.READABLE_HALF + 1, mode="constant")


def _page_samples(page: P.PageImage, marks, rng: np.random.Generator, hole_pool: list[np.ndarray]):
    """Readable positives (+ jitter) and readable negative positions for one page."""
    h, w = page.shape
    centre = readable_centre(page.overlay)
    window = ndimage.uniform_filter(page.overlay.astype(np.float32), F.PATCH, mode="constant")
    pts_all = np.array([(m.x, m.y) for m in marks], float)
    ix = np.clip(np.round(pts_all[:, 0]).astype(int), 0, w - 1)
    iy = np.clip(np.round(pts_all[:, 1]).astype(int), 0, h - 1)
    visible = centre[iy, ix] <= 0
    fams = [m.family for m, v in zip(marks, visible) if v]
    ix, iy = ix[visible], iy[visible]
    px, py, yf = [ix], [iy], list(fams)
    for _ in range(JITTER_COPIES):
        jx = np.clip(ix + rng.integers(-JITTER, JITTER + 1, len(ix)), 0, w - 1)
        jy = np.clip(iy + rng.integers(-JITTER, JITTER + 1, len(iy)), 0, h - 1)
        ok = centre[jy, jx] <= 0
        px.append(jx[ok]); py.append(jy[ok]); yf.extend([f for f, k in zip(fams, ok) if k])
    px = np.concatenate(px); py = np.concatenate(py)
    # mark-up in the outer window around readable positives: rate + masks for transplant
    near = window[iy, ix] > 0
    ovp = np.pad(page.overlay, F.HALF, constant_values=False)
    for x, y in zip(ix[near], iy[near]):
        hole_pool.append(ovp[y:y + F.PATCH, x:x + F.PATCH].copy())
    # negatives: readable candidates far from every estimator mark (visible or not)
    cx, cy = F.candidate_grid(page.gray, page.overlay, STRIDE)
    d, _ = cKDTree(pts_all).query(np.c_[cx, cy], k=1)
    far = d >= NEG_MIN_DIST
    cx, cy = cx[far], cy[far]
    n_neg = min(len(cx), NEG_PER_POS * len(ix) + 50)
    sel = rng.choice(len(cx), n_neg, replace=False) if n_neg < len(cx) else np.arange(len(cx))
    cx, cy = cx[sel], cy[sel]
    natural = window[cy, cx] > 0
    return px, py, yf, cx, cy, natural, int(len(ix)), int(near.sum()), int(len(marks))


def build_training_set(golds: list[DossierGold], seed: int = 0, pages_filter=None, log=print):
    """X, y from the position golds. `pages_filter(dossier, page) -> bool` restricts pages.
    Pages are processed one at a time (dense maps are large)."""
    rng = np.random.default_rng(seed)
    X_parts, y_parts = [], []
    for g in golds:
        if not g.has_positions:
            continue
        by_page: dict[int, list] = defaultdict(list)
        for m in g.marks:
            by_page[m.page].append(m)
        doc = pymupdf.open(g.pdf)
        hole_pool: list[np.ndarray] = []
        n_vis = n_all = n_near = n_neg = n_pos = 0
        for pg in sorted(by_page):
            if pages_filter is not None and not pages_filter(g.dossier, pg):
                continue
            page = P.load_page(doc, pg)
            px, py, yf, cx, cy, natural, vis, near, allm = _page_samples(page, by_page[pg], rng, hole_pool)
            n_vis += vis; n_near += near; n_all += allm
            if not len(px):
                continue
            dense = F.DenseFeatures(page.gray)
            X_parts.append(dense.at(px, py)); y_parts.extend(yf); n_pos += len(yf)
            p_near = near / vis if vis else 0.0
            want = (~natural) & (rng.random(len(cx)) < p_near) if hole_pool else np.zeros(len(cx), bool)
            keep = ~want
            X_parts.append(dense.at(cx[keep], cy[keep])); y_parts.extend([NONE] * int(keep.sum()))
            del dense
            if want.any():
                g2 = np.pad(page.gray, F.HALF, constant_values=255)
                for x, y in zip(cx[want], cy[want]):
                    g2[y:y + F.PATCH, x:x + F.PATCH][hole_pool[rng.integers(len(hole_pool))]] = 255
                d2 = F.DenseFeatures(g2[F.HALF:-F.HALF, F.HALF:-F.HALF])
                X_parts.append(d2.at(cx[want], cy[want])); y_parts.extend([NONE] * int(want.sum()))
                del d2
            n_neg += len(cx)
        log(f"  train set {g.dossier}: readable estimator marks {n_vis}/{n_all}, positives {n_pos} "
            f"(with jitter), negatives {n_neg}, mark-up near readable marks {n_near}")
    X = np.concatenate(X_parts) if X_parts else np.zeros((0, F.N_FEATURES), np.float32)
    return X, np.array(y_parts)


def fit(X: np.ndarray, y: np.ndarray, seed: int = 0) -> tuple[HistGradientBoostingClassifier, list[str]]:
    clf = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.1, max_leaf_nodes=31,
                                         l2_regularization=1.0, early_stopping=True,
                                         validation_fraction=0.1, n_iter_no_change=15, random_state=seed)
    clf.fit(X, y)
    return clf, [str(c) for c in clf.classes_]


def mine_hard_negatives(model: "Model", golds: list[DossierGold], seed: int = 0, pages_per_dossier: int = 8,
                        per_readable_mark: float = 1.0, min_score: float = 0.5, log=print) -> np.ndarray:
    """Features of readable windows far from every estimator mark that the current
    model scores as symbols (p >= min_score), on up to `pages_per_dossier` marked pages
    per dossier, at most `per_readable_mark` x the page's readable estimator marks (so
    positives are not swamped). Standard hard-negative mining; labels are "none"."""
    rng = np.random.default_rng(seed + 1)
    parts = []
    none_i = model.classes.index(NONE)
    for g in golds:
        if not g.has_positions:
            continue
        marked = sorted({m.page for m in g.marks})
        if len(marked) > pages_per_dossier:
            marked = sorted(rng.choice(marked, pages_per_dossier, replace=False).tolist())
        doc = pymupdf.open(g.pdf)
        n = 0
        for pg in marked:
            page = P.load_page(doc, pg)
            pts = np.array([(m.x, m.y) for m in g.marks if m.page == pg], float)
            core = readable_centre(page.overlay)
            h, w = core.shape
            n_read = int(sum(core[min(h - 1, int(y)), min(w - 1, int(x))] <= 0 for x, y in pts))
            cap = int(per_readable_mark * n_read)
            if cap == 0:
                continue
            xs, ys = F.candidate_grid(page.gray, page.overlay, STRIDE)
            if not len(xs):
                continue
            far = cKDTree(pts).query(np.c_[xs, ys])[0] >= NEG_MIN_DIST
            xs, ys = xs[far], ys[far]
            dense = F.DenseFeatures(page.gray)
            X = dense.at(xs, ys)
            psym = 1.0 - model.clf.predict_proba(X)[:, none_i]
            order = np.argsort(-psym)
            order = order[psym[order] >= min_score][:cap]
            parts.append(X[order]); n += len(order)
            del dense
        log(f"  hard negatives {g.dossier}: {n} on {len(marked)} pages")
    return np.concatenate(parts) if parts else np.zeros((0, F.N_FEATURES), np.float32)


def fit_with_mining(golds: list[DossierGold], seed: int = 0, log=print,
                    hard_negatives: bool = False) -> tuple[HistGradientBoostingClassifier, list[str]]:
    """build_training_set -> fit [-> hard-negative mining -> refit]."""
    X, y = build_training_set(golds, seed=seed, log=log)
    clf, classes = fit(X, y, seed=seed)
    if not hard_negatives:
        return clf, classes
    Xh = mine_hard_negatives(Model(clf, classes), golds, seed=seed, log=log)
    if len(Xh):
        X = np.concatenate([X, Xh]); y = np.concatenate([y, np.array([NONE] * len(Xh))])
        clf, classes = fit(X, y, seed=seed)
    return clf, classes


def family_styles(golds: list[DossierGold]) -> dict[str, tuple[str, int, int, int]]:
    """Per family: the estimator's most used counter name, shape, size, colour."""
    names: dict[str, Counter] = defaultdict(Counter)
    for g in golds:
        for m in g.marks:
            names[m.family][m.label] += 1
    out = {}
    for fam, c in names.items():
        label = c.most_common(1)[0][0]
        style = next((g.styles[label] for g in golds if label in g.styles), (0, 20, -65536))
        out[fam] = (label, *style)
    return out


# ---------------------------------------------------------------------- matching / calibration
def match(pred_xy: np.ndarray, gold_xy: np.ndarray, radius: float) -> int:
    """Number of one-to-one matches within `radius` (optimal assignment)."""
    if len(pred_xy) == 0 or len(gold_xy) == 0:
        return 0
    d = np.hypot(pred_xy[:, None, 0] - gold_xy[None, :, 0], pred_xy[:, None, 1] - gold_xy[None, :, 1])
    big = 1e9
    cost = np.where(d <= radius, d, big)
    r, c = linear_sum_assignment(cost)
    return int((cost[r, c] < big).sum())


def calibrate(scored_pages: list[tuple], golds_by_page: dict, radius: float,
              thresholds=None, radii=(12.0, 18.0, 24.0)) -> dict:
    """Pick threshold / NMS radius maximising detection F1 (family-agnostic) on held-out pages.
    scored_pages: [(key, shape, xs, ys, proba, near, scoring model)];
    golds_by_page: key -> (all gold xy (N,2), readable gold xy (M,2)).
    Precision counts a prediction as right if it matches any estimator mark; recall is
    measured on the marks whose core is readable (the only ones a detector can see)."""
    thresholds = thresholds if thresholds is not None else np.round(np.arange(0.05, 0.96, 0.05), 2)
    best = None
    table = []
    for rad in radii:
        for t in thresholds:
            tp_p = tp_r = npred = nread = 0
            for key, shape, xs, ys, proba, near, scorer in scored_pages:
                det = scorer.peaks(0, shape, xs, ys, proba, near, threshold=float(t), nms_radius=rad)
                pxy = np.array([(d.x, d.y) for d in det]).reshape(-1, 2)
                g_all, g_read = golds_by_page.get(key, (np.zeros((0, 2)), np.zeros((0, 2))))
                tp_p += match(pxy, g_all, radius); tp_r += match(pxy, g_read, radius)
                npred += len(pxy); nread += len(g_read)
            p = tp_p / npred if npred else 0.0
            r = tp_r / nread if nread else 0.0
            f1 = 2 * p * r / (p + r) if p + r else 0.0
            table.append({"threshold": float(t), "nms_radius": rad, "precision": p, "recall_readable": r, "f1": f1,
                          "predicted": npred, "readable_gold": nread})
            if best is None or f1 > best["f1"]:
                best = table[-1]
    return {"best": best, "table": table}
