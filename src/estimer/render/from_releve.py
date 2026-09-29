"""Bridge: releve/ chain output -> EXEMPLE renderer input (estimate.json + bordereau.csv + reserves.md + plans.pdf).

    python -m src.estimer.render.from_releve WORKDIR OUT_DIR [--render OUT.pdf]

WORKDIR is a relevé working directory prepared by `releve/prepare.py` and filled by the `releveur` agent
(`feuilles.csv`, `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`,
`reserves.md`, `feuilles/<F>.pdf`). OUT_DIR receives:

  plans.pdf        the original vector page of every sheet that has occurrences, in sheet-name order
  estimate.json    one counter per nomenclature label; one element per occurrence (x/y in PDF points,
                   width_px/height_px = page size in points, so the renderer maps 1:1)
  bordereau.csv    one row per repère (gold `bordereau-materiel.csv` schema + `reserve`)
  reserves.md      `## <sheet>` sections for the "RESERVES ET COMPLEMENTS" block
  feuilles.json    per sheet: display name, source sheet id, page, bordereau format

Nothing is invented: every row is one occurrence written by the relevé; descriptive fields come from the
nomenclature/occurrence columns the relevé wrote, otherwise the neutral wording MODELE NON PRECISE / A PRECISER.

Optional columns read when present (written by the `releve-planexpert` skill since 2026-09-29):
  nomenclature.csv : code (symbol tag on the plan, e.g. DF, K, CE2), materiel (family name), portee, modele,
                     prescription, discipline (incendie | electricite | urgence)
  occurrences-*.csv: designation, portee, modele, prescription, parent, qte, reserve, x0_pt, y0_pt, x1_pt, y1_pt
  feuilles-classement.csv : bordereau (materiel | agrege | travaux)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "releve"))
from commun import load_feuilles, read_csv  # noqa: E402  (releve/ helpers are the single source of truth)

DEFAULT_MODEL = "MODELE NON PRECISE"
DEFAULT_PORTEE = "A PRECISER"
FORMATS = ("materiel", "agrege", "travaux")
# releve family -> EXEMPLE discipline (repère prefix): I = incendie, M = materiel electrique
INCENDIE = {"alarme", "securite_incendie", "incendie"}
URGENCE = {"secours", "urgence"}
# releve shape (Plan Expert enum or name) -> renderer marker; boxes with a bbox are drawn as rectangles
SHAPES = {"2": "diamond", "losange": "diamond"}
READING_BAND_PT = 40.0     # reading order of sources: top-to-bottom bands of 40 pt, then left-to-right


def ascii_upper(s: str) -> str:
    """EXEMPLE text is unaccented upper-case ASCII (REPERES, QUANTITES)."""
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def ascii_text(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip()


def natural_key(name: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def _cell(r: dict, key: str) -> str:
    return (r.get(key) or "").strip()


def _float(v, default=None):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return default


def read_nomenclature(work: Path) -> dict[str, dict]:
    out = {}
    for r in read_csv(str(work / "nomenclature.csv")):
        label = _cell(r, "label")
        if label:
            out[label] = r
    return out


def read_occurrences(work: Path) -> list[dict]:
    rows = []
    for name in ("occurrences-texte.csv", "occurrences-visuel.csv"):
        for r in read_csv(str(work / name)):
            if _cell(r, "exclure").lower() in ("1", "oui", "x", "true"):
                continue
            x, y = _float(r.get("x_pt")), _float(r.get("y_pt"))
            if x is None or y is None or not _cell(r, "feuille") or not _cell(r, "label"):
                continue
            rows.append(dict(r, x=x, y=y, feuille=_cell(r, "feuille"), label=_cell(r, "label")))
    return rows


def discipline(nom_row: dict) -> str:
    d = _cell(nom_row, "discipline").lower()
    if d in ("incendie", "electricite", "urgence"):
        return d
    fam = _cell(nom_row, "famille").lower()
    if fam in INCENDIE:
        return "incendie"
    if fam in URGENCE:
        return "urgence"
    return "electricite"


def sheet_format(classement: dict, items: list[dict]) -> str:
    """Bordereau format of a sheet: explicit `bordereau` column of feuilles-classement.csv, else
    incendie or schema -> materiel (one row per repère), all urgence -> travaux, other plans -> agrege."""
    f = _cell(classement, "bordereau").lower()
    if f in FORMATS:
        return f
    disc = {it["discipline"] for it in items}
    if (classement.get("type") or "").strip() == "schema" or "incendie" in disc:
        return "materiel"
    if disc == {"urgence"}:
        return "travaux"
    return "agrege"


def letter_code(nom_row: dict, label: str) -> str:
    """Aggregated/travaux family ID (CH, PC, IS): the `code` column, else the letters of the text token."""
    c = ascii_upper(_cell(nom_row, "code"))
    if c:
        return re.sub(r"[^A-Z0-9]", "", c) or "X"
    tok = _cell(nom_row, "jeton_regex")
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", tok):
        return tok.upper()
    return re.sub(r"[^A-Z]", "", ascii_upper(label))[:3] or "X"


def build(work: Path, out: Path) -> dict:
    work, out = Path(work), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    feuilles = load_feuilles(str(work))
    nom = read_nomenclature(work)
    occ = read_occurrences(work)
    unknown = sorted({o["label"] for o in occ if o["label"] not in nom})
    if unknown:
        raise SystemExit("labels absents de nomenclature.csv : " + ", ".join(unknown))
    missing = sorted({o["feuille"] for o in occ if o["feuille"] not in feuilles})
    if missing:
        raise SystemExit("feuilles absentes de feuilles.csv : " + ", ".join(missing))

    by_sheet: dict[str, list[dict]] = defaultdict(list)
    for o in occ:
        n = nom[o["label"]]
        it = dict(o, discipline=discipline(n))
        by_sheet[o["feuille"]].append(it)

    fids = sorted(by_sheet, key=lambda f: natural_key(feuilles[f]["nom"]))
    plans = pymupdf.open()
    sheets_json, counters, bord_rows, meta = [], defaultdict(list), [], []
    for page_no, fid in enumerate(fids, start=1):
        info = feuilles[fid]
        name = info["nom"]
        src = pymupdf.open(str(work / "feuilles" / f"{fid}.pdf"))
        plans.insert_pdf(src)
        W, H = src[0].rect.width, src[0].rect.height
        src.close()
        items = by_sheet[fid]
        fmt = sheet_format(info, items)
        sheets_json.append({"sheet": name, "page": page_no, "width_px": W, "height_px": H})
        meta.append({"sheet": name, "feuille": fid, "page": page_no, "format": fmt,
                     "type": info.get("type", ""), "note": info.get("note_classement", "")})

        # source ids: reading order over the whole sheet
        order = sorted(items, key=lambda o: (int(o["y"] // READING_BAND_PT), o["x"]))
        for k, o in enumerate(order, start=1):
            o["source_id"] = f"{name}-{k:03d}"

        # family codes: materiel sheets number families per discipline in alphabetical order of the
        # family name (EXEMPLE DSI01: I01 AVERTISSEUR DE FUMEE ... I08 RELAIS); other formats use the letter code
        def materiel_of(o):
            n = nom[o["label"]]
            return ascii_upper(_cell(n, "materiel") or _cell(n, "description") or o["label"])
        fam_code: dict[str, str] = {}
        if fmt == "materiel":
            for prefix, disc_set in (("I", {"incendie"}), ("M", {"electricite", "urgence"})):
                names = sorted({materiel_of(o) for o in items if o["discipline"] in disc_set})
                for i, m in enumerate(names, start=1):
                    fam_code[(prefix, m)] = f"{prefix}{i:02d}"
        seq: dict[str, int] = defaultdict(int)
        for o in sorted(items, key=lambda o: (materiel_of(o), int(o["y"] // READING_BAND_PT), o["x"])):
            n = nom[o["label"]]
            mat = materiel_of(o)
            if fmt == "materiel":
                code = fam_code[("I" if o["discipline"] == "incendie" else "M", mat)]
            else:
                code = letter_code(n, o["label"])
            seq[code] += 1
            repere = f"{code}-{seq[code]:02d}"
            designation = ascii_upper(_cell(o, "designation") or _cell(n, "code") or _jeton(o) or o["label"])
            portee = ascii_upper(_cell(o, "portee") or _cell(n, "portee")) or DEFAULT_PORTEE
            modele = ascii_text(_cell(o, "modele") or _cell(n, "modele")) or DEFAULT_MODEL
            prescription = ascii_text(_cell(o, "prescription") or _cell(n, "prescription") or _cell(n, "description"))
            parent = ascii_upper(_cell(o, "parent"))
            qte = _float(o.get("qte"), 1.0)
            reserve = _cell(o, "reserve")
            el = {"sheet": name, "page": page_no, "x": o["x"], "y": o["y"], "repere": repere, "code": code,
                  "source": o["source_id"], "shape": SHAPES.get(_cell(n, "forme").lower(), "circle")}
            bb = [_float(o.get(k)) for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")]
            if all(v is not None for v in bb):
                el["bbox"] = bb
                el["shape"] = "rect"
            counters[o["label"]].append(el)
            bord_rows.append({"feuille": name, "repere": repere, "source": o["source_id"], "materiel": mat,
                              "designation": designation, "qte": f"{qte:g}", "portee": portee, "modele": modele,
                              "prescription": prescription, "parent": parent, "reserve": reserve,
                              "code": code, "format": fmt, "note": ascii_text(_cell(o, "note"))})

    plans.save(str(out / "plans.pdf"), garbage=3, deflate=True)
    est = {"source": "releve", "workdir": str(work), "sheets": sheets_json,
           "counters": [{"family": label, "name": label, "elements": els} for label, els in sorted(counters.items())]}
    (out / "estimate.json").write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
    cols = ["feuille", "repere", "source", "materiel", "designation", "qte", "portee", "modele", "prescription",
            "parent", "reserve", "code", "format", "note"]
    bord_rows.sort(key=lambda r: (natural_key(r["feuille"]), natural_key(r["repere"])))
    with open(out / "bordereau.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(bord_rows)
    (out / "reserves.md").write_text(reserves_by_sheet(work, [m["sheet"] for m in meta], feuilles),
                                     encoding="utf-8")
    (out / "feuilles.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"sheets": len(meta), "reperes": len(bord_rows), "plans_pages": len(fids)}


def _jeton(o: dict) -> str:
    m = re.match(r"mot '(.+)'$", _cell(o, "note"))
    return m.group(1) if m else ""


def _sheet_tokens(line: str) -> set[str]:
    return {t.replace("-", "").upper() for t in re.findall(r"\b[A-Za-z]{1,4}-?\d{2,4}[A-Za-z]?\b", line)}


def reserves_by_sheet(work: Path, names: list[str], feuilles: dict) -> str:
    """Split the relevé `reserves.md` into `## <sheet>` sections: a reserve line goes to every sheet it names
    (E-201 matches E201); lines naming no relevé sheet are general and go to every sheet."""
    path = work / "reserves.md"
    lines = []
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            s = re.sub(r"^[-*]\s+", "", s).replace("**", "")
            lines.append(ascii_text(s))
    aliases = {n: {n.replace("-", "").upper()} for n in names}
    for fid, info in feuilles.items():
        if info.get("nom") in aliases:
            aliases[info["nom"]].add(fid.replace("-", "").upper())
    general = [l for l in lines if not (_sheet_tokens(l) & set().union(*aliases.values()))]
    out = []
    for n in names:
        own = [l for l in lines if _sheet_tokens(l) & aliases[n]]
        out.append(f"## {n}")
        out += own + general
        out.append("")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.estimer.render.from_releve", description=__doc__.splitlines()[0])
    ap.add_argument("workdir", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--render", type=Path, default=None, help="also render the EXEMPLE-format PDF here")
    ap.add_argument("--report", type=Path, default=None)
    a = ap.parse_args(argv)
    res = build(a.workdir, a.out_dir)
    print(f"{a.out_dir}: {res['sheets']} feuilles, {res['reperes']} reperes")
    if a.render:
        from . import load_input, render
        rep = render(load_input(a.out_dir), a.out_dir / "plans.pdf", a.render)
        print(f"{a.render}: {rep['pages']} pages")
        if a.report:
            a.report.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
