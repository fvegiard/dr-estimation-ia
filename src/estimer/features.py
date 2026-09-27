"""Window features for symbol detection (no learning here).

A window is a 64x64 px neighbourhood of the working-resolution grayscale page
centred on a candidate point. Features are computed densely for a whole page
(box filters over gradient-orientation channels), then sampled at candidate
points, so scoring a page costs a few seconds:

- fine HOG: gradient orientation histograms (8 unsigned bins) on a 4x4 grid
  of 8 px cells over the central 32x32 px (the symbol itself);
- coarse HOG: same on a 4x4 grid of 16 px cells over the whole 64x64 px
  window (walls, leader lines, circuit tags next to the symbol);
- ink density on an 8x8 grid of 8 px cells over the window;
- square-ring ink profile around the centre (half-sizes 3..15 px), which
  separates filled dots, circles and squares; ink density of the central
  8x8 px.

Overlay (pre-existing coloured mark-up) pixels arrive already whitened by
`pages.load_page`; no feature reads the overlay mask itself.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage

PATCH = 64
HALF = PATCH // 2
N_BINS = 8
CANDIDATE_INNER = 12      # half-size of the central square tested for ink
CANDIDATE_MIN_INK = 0.02  # fraction of dark pixels in that square
READABLE_HALF = 6         # a window is readable if the central 13x13 px carry no coloured mark-up
INK_LEVEL = 160           # gray < INK_LEVEL is ink
RING_HALF = (3, 6, 9, 12, 15)

N_FEATURES = 16 * N_BINS * 2 + 64 + len(RING_HALF) + 1


def _cell_offsets(cell: int, grid: int, span: int) -> list[tuple[int, int]]:
    """Centre offsets (dy, dx) of a grid x grid array of cells spanning `span` px."""
    start = -span // 2 + cell // 2
    return [(start + i * cell, start + j * cell) for i in range(grid) for j in range(grid)]


FINE = _cell_offsets(8, 4, 32)
COARSE = _cell_offsets(16, 4, 64)
DENS = _cell_offsets(8, 8, 64)


class DenseFeatures:
    """Per-page dense maps; `at(xs, ys)` returns (N, N_FEATURES)."""

    def __init__(self, gray: np.ndarray):
        self.h, self.w = gray.shape
        ink = (255.0 - gray.astype(np.float32)) / 255.0
        gy = ndimage.convolve1d(ink, [1, 0, -1], axis=0, mode="nearest")
        gx = ndimage.convolve1d(ink, [1, 0, -1], axis=1, mode="nearest")
        mag = np.hypot(gx, gy)
        ang = np.mod(np.arctan2(gy, gx), np.pi)
        b = np.minimum((ang / np.pi * N_BINS).astype(np.int8), N_BINS - 1)
        self.fine = []
        self.coarse = []
        for k in range(N_BINS):
            ch = np.where(b == k, mag, 0.0).astype(np.float32)
            # uniform_filter of even size: window [i-s/2, i+s/2-1]; offsets absorb the half-pixel shift
            self.fine.append(ndimage.uniform_filter(ch, 8, mode="constant"))
            self.coarse.append(ndimage.uniform_filter(ch, 16, mode="constant"))
        dark = (gray < INK_LEVEL).astype(np.float32)
        self.dens = ndimage.uniform_filter(dark, 8, mode="constant")
        self.rings = [ndimage.uniform_filter(dark, 2 * r + 1, mode="constant") for r in RING_HALF]

    def _sample(self, m: np.ndarray, ys: np.ndarray, xs: np.ndarray, dy: int, dx: int) -> np.ndarray:
        yy = np.clip(ys + dy, 0, self.h - 1)
        xx = np.clip(xs + dx, 0, self.w - 1)
        v = m[yy, xx]
        outside = (ys + dy < 0) | (ys + dy >= self.h) | (xs + dx < 0) | (xs + dx >= self.w)
        return np.where(outside, 0.0, v)

    def _hog(self, maps: list[np.ndarray], offsets, ys, xs) -> np.ndarray:
        n = len(xs)
        out = np.empty((n, len(offsets), N_BINS), np.float32)
        for c, (dy, dx) in enumerate(offsets):
            for k in range(N_BINS):
                out[:, c, k] = self._sample(maps[k], ys, xs, dy, dx)
        out = np.sqrt(np.maximum(out.reshape(n, -1), 0.0))
        out /= np.linalg.norm(out, axis=1, keepdims=True) + 1e-3
        return out

    def at(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        xs = np.asarray(xs, np.int64)
        ys = np.asarray(ys, np.int64)
        fine = self._hog(self.fine, FINE, ys, xs)
        coarse = self._hog(self.coarse, COARSE, ys, xs)
        dens = np.stack([self._sample(self.dens, ys, xs, dy, dx) for dy, dx in DENS], axis=1)
        boxes = [self._sample(m, ys, xs, 0, 0) for m in self.rings]
        areas = [(2 * r + 1) ** 2 for r in RING_HALF]
        rings = [boxes[0]]
        for i in range(1, len(boxes)):
            s = boxes[i] * areas[i] - boxes[i - 1] * areas[i - 1]
            rings.append(s / (areas[i] - areas[i - 1]))
        centre = self._sample(self.dens, ys, xs, 0, 0)
        return np.concatenate([fine, coarse, dens, np.stack(rings, 1), centre[:, None]], axis=1).astype(np.float32)


def candidate_grid(gray: np.ndarray, overlay: np.ndarray, stride: int) -> tuple[np.ndarray, np.ndarray]:
    """Grid points worth scoring: some ink in the central square and no
    coloured mark-up on the symbol core (central 13x13 px) — a window whose core
    is covered is unreadable."""
    h, w = gray.shape
    size = 2 * CANDIDATE_INNER + 1
    ink = ndimage.uniform_filter((gray < INK_LEVEL).astype(np.float32), size, mode="constant")
    ov = ndimage.uniform_filter(overlay.astype(np.float32), 2 * READABLE_HALF + 1, mode="constant")
    ys = np.arange(stride // 2, h, stride)
    xs = np.arange(stride // 2, w, stride)
    keep = (ink[np.ix_(ys, xs)] >= CANDIDATE_MIN_INK) & (ov[np.ix_(ys, xs)] <= 0)
    gy, gx = np.nonzero(keep)
    return xs[gx], ys[gy]
