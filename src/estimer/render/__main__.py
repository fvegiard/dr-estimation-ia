"""python -m src.estimer.render <estimer-output-dir> <plans.pdf> <out.pdf> [--report report.json]

Renders the EXEMPLE-format relevé: annotated plan pages + bordereau pages (see src/estimer/render/__init__.py).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import load_input, render


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render",
                                 description="Estimer output -> annotated plans + bordereau PDF (EXEMPLE format).")
    ap.add_argument("in_dir", type=Path, help="estimer output directory (estimate.json [+ bordereau.csv, reserves.md])")
    ap.add_argument("plans", type=Path, help="the plans PDF the estimate was made on")
    ap.add_argument("out", type=Path, help="output PDF")
    ap.add_argument("--report", type=Path, default=None, help="write a JSON summary of what was rendered")
    args = ap.parse_args(argv)
    if not (args.in_dir / "estimate.json").is_file():
        print(f"error: {args.in_dir}/estimate.json not found", file=sys.stderr)
        return 2
    if not args.plans.is_file():
        print(f"error: {args.plans} not found", file=sys.stderr)
        return 2
    sheets = load_input(args.in_dir)
    if not sheets:
        print("error: no counted symbol in estimate.json", file=sys.stderr)
        return 1
    rep = render(sheets, args.plans, args.out)
    print(f"{args.out}: {rep['pages']} pages, {len(rep['sheets'])} sheets")
    if args.report:
        args.report.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
