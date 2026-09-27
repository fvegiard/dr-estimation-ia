"""python -m src.estimer <any.pdf> [--out DIR] [--model models/estimer.joblib] [--sheets sheets.csv]

Outputs in DIR (default: ./estimation-<pdf stem>/):
  estimate.json   ecart-ready (python -m src.validation.ecart --ia estimate.json),
                  per-sheet family counts, detections, conduit estimates, flags
  releve.xlsx     DR template (Relevé / Résumé) + Conduits sheet
  sheets.csv      one row per page: counts per family, conduit estimate, flags
  planexpert/<name>.qpl + one PNG per page (Plan Expert project, estimator layout)

--sheets (optional CSV, columns page,name,scale_ratio,paper_width_pt,skip) supplies
sheet names / scales for image-only PDFs that carry no text layer.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from . import export as E
from . import pipeline
from .model import Model
from .train import DEFAULT_MODEL


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m src.estimer",
                                 description="Plan PDF -> symbol counts per family per sheet (estimator format).")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("--sheets", type=Path, default=None, help="per-page metadata CSV (page,name,scale_ratio,paper_width_pt,skip)")
    ap.add_argument("--pages", default=None, help="1-based pages, e.g. 1-3,7 (default: all)")
    ap.add_argument("--name", default=None, help="project / plan name (default: PDF stem)")
    ap.add_argument("--no-qpl", action="store_true", help="skip the Plan Expert project and its PNGs")
    return ap


def parse_pages(spec: str | None) -> list[int] | None:
    if not spec:
        return None
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a) - 1, int(b)))
        elif part:
            out.append(int(part) - 1)
    return out


def estimate(pdf: Path, out: Path, model: Model, sheets_csv: Path | None = None, pages=None,
             name: str | None = None, qpl: bool = True, log=print) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    name = name or pdf.stem
    t = time.time()
    sheets, grays, codes = pipeline.run(pdf, model, sheets_csv, pages, keep_gray=qpl, log=log)
    data = E.write_json(out / "estimate.json", pdf, sheets, model,
                        {"elapsed_s": round(time.time() - t, 1),
                         "legend_codes": codes})
    E.write_xlsx(out / "releve.xlsx", sheets, model)
    E.write_sheets_csv(out / "sheets.csv", sheets)
    if qpl:
        qdir = out / "planexpert"
        qdir.mkdir(exist_ok=True)
        E.write_qpl(qdir, name, sheets, grays, model)
    return data


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.pdf.is_file():
        print(f"error: {args.pdf} not found", file=sys.stderr)
        return 2
    if not args.model.is_file():
        print(f"error: model {args.model} not found — train it with: python -m src.estimer.train", file=sys.stderr)
        return 2
    out = args.out or Path(f"estimation-{args.pdf.stem}")
    model = Model.load(args.model)
    data = estimate(args.pdf, out, model, args.sheets, parse_pages(args.pages), args.name, not args.no_qpl)
    tot = data["totals"]
    print(f"{sum(tot.values())} symbols on {len(data['sheets'])} pages -> {out}")
    for fam, n in sorted(tot.items(), key=lambda kv: -kv[1]):
        print(f"  {fam}: {n}")
    u = data["uncertainties"]
    print(f"  flagged: {u['unreadable_markup_zones']} unreadable zones under coloured mark-up (not counted), "
          f"{u['detections_near_markup']} detections next to mark-up, "
          f"{u['detections_family_uncertain']} with uncertain family")
    return 0


if __name__ == "__main__":
    sys.exit(main())
