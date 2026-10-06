# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "numpy", "scipy"]
# ///
"""Note un relevé contre le gold, feuille par feuille (encadré, légende, positions des repères).

    python -m outils.score_gold <OUTBOX/S> <EXEMPLE.pdf> [--json score.json] [--tol 8]

Lit dans le dossier de sortie : `*-Plans-annotes.pdf`, `*-rendu-rapport.json` (page du plan de chaque feuille) et
`vecteur/estimate.json` (repères en pixels du raster). Lit dans le gold la page de chaque feuille via le tableau de
`docs/FORMAT-EXEMPLE.md` (colonne « page plan »). Rien n'est inventé : une feuille du gold absente du relevé vaut 0.

Par feuille : repères et familles de l'encadré (gold / IA), familles exactes (code + quantité de la légende),
rappel et précision des repères à `tol` pt, et rappel « même famille » (bon code au bon endroit).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import numpy as np
import pymupdf
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.estimer.render import from_exemple as FX  # noqa: E402

LIGNE_SPEC = re.compile(r"^\|\s*(DSI\d{2}|E\d{2}|EU\d{2})\s*\|[^|]*\|\s*(\d+)\s*\|")


def pages_gold(spec_md: str) -> dict[str, int]:
    out = {}
    for ligne in open(spec_md, encoding="utf-8"):
        m = LIGNE_SPEC.match(ligne.strip())
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def famille(code: str) -> str:
    return (code or "").split("-")[0].strip().upper()


def noter_feuille(gold: list[tuple[str, float, float]], ia: list[tuple[str, float, float]],
                  legende_gold: dict[str, float], legende_ia: dict[str, float], tol: float = 8.0) -> dict:
    res = {"reperes_gold": len(gold), "reperes_ia": len(ia),
           "familles_gold": len(legende_gold), "familles_ia": len(legende_ia),
           "familles_exactes": sum(1 for k, q in legende_gold.items() if k in legende_ia and float(legende_ia[k]) == float(q)),
           "ecarts_legende": {k: [legende_gold.get(k), legende_ia.get(k)]
                              for k in sorted(set(legende_gold) | set(legende_ia))
                              if legende_gold.get(k) is None or legende_ia.get(k) is None
                              or float(legende_gold[k]) != float(legende_ia[k])}}
    if not gold or not ia:
        res.update(apparies=0, meme_famille=0, rappel=0.0, precision=0.0, rappel_meme_famille=0.0)
        return res
    apparies = apparier([(x, y) for _, x, y in gold], [(x, y) for _, x, y in ia], tol)
    meme = 0
    for code in {c for c, _, _ in gold}:
        g = [(x, y) for c, x, y in gold if c == code]
        a = [(x, y) for c, x, y in ia if c == code]
        meme += apparier(g, a, tol) if a else 0
    res.update(apparies=apparies, meme_famille=meme,
               rappel=round(100 * apparies / len(gold), 1), precision=round(100 * apparies / len(ia), 1),
               rappel_meme_famille=round(100 * meme / len(gold), 1))
    return res


def apparier(gold: list[tuple[float, float]], ia: list[tuple[float, float]], tol: float) -> int:
    d = cdist(np.array(gold), np.array(ia))
    lignes, colonnes = linear_sum_assignment(np.where(d <= tol, d, 1e9))
    return int((d[lignes, colonnes] <= tol).sum())


def legende(page: pymupdf.Page) -> dict[str, float]:
    return {k: float(v[0] if isinstance(v, list) else v) for k, v in FX.read_legend(page).items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m outils.score_gold")
    ap.add_argument("outbox")
    ap.add_argument("exemple")
    ap.add_argument("--json", default=None)
    ap.add_argument("--tol", type=float, default=8.0)
    a = ap.parse_args(argv)
    annotes = glob.glob(os.path.join(a.outbox, "*-Plans-annotes.pdf"))
    rapport = glob.glob(os.path.join(a.outbox, "*-rendu-rapport.json"))
    if not annotes or not rapport:
        sys.exit(f"Plans-annotes.pdf ou rendu-rapport.json absent de {a.outbox}")
    ai_doc = pymupdf.open(annotes[0])
    feuilles_ia = {s["sheet"]: s for s in json.load(open(rapport[0], encoding="utf-8"))["sheets"]}
    est = json.load(open(os.path.join(a.outbox, "vecteur", "estimate.json"), encoding="utf-8"))
    ex = pymupdf.open(a.exemple)
    gold_pages = pages_gold(os.path.join(ROOT, "docs", "FORMAT-EXEMPLE.md"))
    lignes = []
    for f in sorted(set(gold_pages) | set(feuilles_ia)):
        gp = gold_pages.get(f)
        gold = [(famille(m["repere"]), m["x"], m["y"]) for m in FX.read_markers(ex, gp - 1)] if gp else []
        lg = legende(ex[gp - 1]) if gp else {}
        ia, li = [], {}
        if f in feuilles_ia:
            page = ai_doc[feuilles_ia[f]["plan_page"] - 1]
            li = legende(page)
            s_est = next((s for s in est["sheets"] if s["sheet"] == f), None)
            if s_est:
                k = page.rect.width / s_est["width_px"]
                ia = [(famille(e.get("code") or e.get("repere")), e["x"] * k, e["y"] * k)
                      for c in est["counters"] for e in c["elements"] if e.get("sheet") == f]
        r = noter_feuille(gold, ia, lg, li, a.tol)
        r.update(feuille=f, page_gold=gp, releve="oui" if f in feuilles_ia else "non")
        lignes.append(r)
    print(f"| Feuille | Page gold | Relevée | Repères gold / IA | Familles exactes | Rappel | Précision | Même famille |")
    print("|---|--:|---|--:|--:|--:|--:|--:|")
    for r in lignes:
        print(f"| {r['feuille']} | {r['page_gold'] or '-'} | {r['releve']} | {r['reperes_gold']} / {r['reperes_ia']} | "
              f"{r['familles_exactes']}/{r['familles_gold']} | {r['rappel']} % | {r['precision']} % | {r['rappel_meme_famille']} % |")
    tg = sum(r["reperes_gold"] for r in lignes); tm = sum(r.get("meme_famille", 0) for r in lignes)
    print(f"\nTotal : {tg} repères au gold ; même famille au bon endroit : {tm} ({100 * tm / max(1, tg):.1f} %).")
    if a.json:
        json.dump(lignes, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
