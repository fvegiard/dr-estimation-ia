"""PDF pages -> grayscale working rasters, plus a mask of pre-existing coloured
mark-up.

Working resolution: every page is brought to WORK_WIDTH pixels wide (the
width of Plan Expert page exports), so symbol sizes are comparable across
PDFs. Image-only pages whose single image already has that width are used
as-is (no resampling); other pages are rendered by MuPDF.

Coloured mark-up (another takeoff's marks, highlighter, red-lines) is not
plan content. Pixels that are clearly coloured (HSV saturation and value
above thresholds), grown by a few pixels to swallow their dark outlines, form
the `overlay` mask. The detector never scores a window whose centre is
covered by that mask; such areas are reported as unreadable instead.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

WORK_WIDTH = 2997
SAT_MIN = 0.28        # HSV saturation of a coloured pixel
VAL_MIN = 0.20        # ... and minimum brightness (dark pixels have unreliable hue)
OVERLAY_GROW = 3      # px, swallows the dark outline drawn around coloured marks


@dataclass
class PageImage:
    index: int
    gray: np.ndarray            # uint8 HxW, 255 = paper; overlay pixels set to 255
    overlay: np.ndarray         # bool HxW
    width_pt: float
    height_pt: float
    scale: float                # working px per PDF pt
    words: list[tuple]          # PyMuPDF words (x0, y0, x1, y1, text, ...) in working px
    source: str                 # "embedded-image" | "rendered"
    original: np.ndarray | None = None   # uint8 HxW before overlay whitening (for export)

    @property
    def shape(self) -> tuple[int, int]:
        return self.gray.shape


def overlay_mask(rgb: np.ndarray) -> np.ndarray:
    f = rgb.astype(np.float32) / 255.0
    mx = f.max(axis=2)
    mn = f.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    m = (sat >= SAT_MIN) & (mx >= VAL_MIN)
    # drop isolated coloured specks (JPEG chroma noise around black ink)
    m = ndimage.binary_opening(m, structure=np.ones((2, 2), bool))
    if OVERLAY_GROW:
        m = ndimage.binary_dilation(m, iterations=OVERLAY_GROW)
    return m


def _page_rgb(doc: pymupdf.Document, page: pymupdf.Page) -> tuple[np.ndarray, str, float]:
    imgs = page.get_images(full=True)
    has_text = bool(page.get_text("text").strip())
    if len(imgs) == 1 and not has_text and not page.get_drawings():
        info = doc.extract_image(imgs[0][0])
        if info and info.get("width") == WORK_WIDTH:
            im = Image.open(io.BytesIO(info["image"])).convert("RGB")
            return np.asarray(im), "embedded-image", WORK_WIDTH / page.rect.width
    zoom = WORK_WIDTH / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), colorspace=pymupdf.csRGB, alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
    return arr.copy(), "rendered", zoom


def load_page(doc: pymupdf.Document, index: int) -> PageImage:
    page = doc[index]
    rgb, source, scale = _page_rgb(doc, page)
    ov = overlay_mask(rgb)
    original = np.asarray(Image.fromarray(rgb).convert("L"))
    gray = original.copy()
    gray[ov] = 255
    words = [(w[0] * scale, w[1] * scale, w[2] * scale, w[3] * scale, w[4]) for w in page.get_text("words")]
    return PageImage(index, gray, ov, float(page.rect.width), float(page.rect.height), scale, words, source,
                     original)


def iter_pages(pdf: Path, pages: list[int] | None = None):
    doc = pymupdf.open(pdf)
    for i in (pages if pages is not None else range(doc.page_count)):
        yield load_page(doc, i)
