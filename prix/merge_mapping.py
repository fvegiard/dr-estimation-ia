#!/usr/bin/env python3
"""Merge prix/mapping/chunk-*.csv into prix/mapping-familles.csv and print coverage stats (JSON).

Rules:
- Rows are concatenated in chunk order; a `chunk` column is added for provenance.
- No number is invented or recomputed; cells are copied verbatim (whitespace-stripped only; a literal
  "none" in a page/number/unit cell is normalised to empty; a printed thousands separator "2,250.00" is
  written 2250.00). A side whose item is `none` may still carry a page as a pointer to the book table consulted.
- Every priced side (NE and/or NECA) must carry book + page + raw source line. The raw line is taken from
  the `|| raw:` marker in the item; when absent, it is looked up in the parsed book tables
  (prix/national-estimator-2025.csv, prix/neca-2022.csv) on the same page with the same numbers.
  Columns ne_raw / neca_raw hold the raw line; ne_raw_src / neca_raw_src say where it came from
  (`item` = written by the mapping agent and confirmed in the parsed book table, `item-unconfirmed` =
  written by the agent, no identical line found in the parsed table, `note` = quoted in the note by the agent (with -unconfirmed likewise), `book` = recovered from the table).
- A row is REJECTED (prix/mapping-rejets.csv, not merged) when: the family is unknown, a priced side has
  no page, no raw line can be found, a number is not numeric, or the numbers in the row contradict the
  raw line (NE: material and manhours; NECA: normal hours).
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.join(HERE, "mapping")
OUT = os.path.join(HERE, "mapping-familles.csv")
OUT_REJ = os.path.join(HERE, "mapping-rejets.csv")
FAM = os.path.join(HERE, "families.json")
NE_CSV = os.path.join(HERE, "national-estimator-2025.csv")
NECA_CSV = os.path.join(HERE, "neca-2022.csv")

COLS = ["family", "ee_codes", "ne_page", "ne_item", "ne_material_usd", "ne_manhours", "ne_unit",
        "neca_page", "neca_item", "neca_normal_hours", "neca_unit", "confidence", "note"]
OUT_COLS = ["chunk"] + COLS + ["ne_raw", "ne_raw_src", "neca_raw", "neca_raw_src"]
NUM = re.compile(r"^\d+(\.\d+)?$")
CONF = ["high", "medium", "low", "none"]


def chunk_key(p):
    return int(re.search(r"chunk-(\d+)\.csv$", p).group(1))


def fnum(s):
    return float(s) if NUM.match(s) else None


def load_books():
    ne, neca = {}, {}
    with open(NE_CSV, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            ne.setdefault(int(r["page"]), []).append(r)
    with open(NECA_CSV, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["page"].isdigit():
                neca.setdefault(int(r["page"]), []).append(r)
    return ne, neca


def split_raw(item):
    if "|| raw:" in item:
        a, b = item.split("|| raw:", 1)
        return a.strip(), b.strip()
    return item, ""


NOTE_RAW = re.compile(r'\b(NE|NECA)\s+raw\s+p\.?\s*(\d+)\s*:?\s*"([^"]+)"', re.I)
TOK = re.compile(r"[a-z0-9#/\-]+")


def tokens(s):
    return set(TOK.findall(s.lower().replace("-inch", "").replace("inch", "")))


def resolve(side, row, page_rows, reasons):
    """Fill row[side+'_raw'] / row[side+'_raw_src']; append reasons on failure."""
    desc, raw = split_raw(row[side + "_item"])
    page = row[side + "_page"]
    if side == "ne":
        want = (fnum(row["ne_material_usd"]), fnum(row["ne_manhours"]))
        cand = [r for r in page_rows if (fnum(r["material_usd"]), fnum(r["manhours"])) == want and r["unit"] == row["ne_unit"]]
    else:
        want = fnum(row["neca_normal_hours"])
        cand = [r for r in page_rows if fnum(r["normal_hours"]) == want and r["unit"] == row["neca_unit"]]
    src = "item"
    norm = lambda t: re.sub(r"\s+", " ", t.replace(",", "").replace('""', '"')).strip().lower()
    if not raw:
        # raw quoted in the note by the agent, e.g. NE raw p240: "Ivory L1@0.20 Ea 1.05 9.32 10.37"
        n = norm(row["note"])
        quoted = [r for r in cand if norm(r["raw"]) in n]
        tail = norm(desc.split(">")[-1].split(":")[-1])
        exact = [r for r in quoted if norm(r["item"]) == tail]
        if len(exact) > 1:  # same printed line under several tables: the item text names the table
            exact = [r for r in exact if r.get("table_title") and norm(r["table_title"]) in norm(desc)]
        if len(quoted) == 1 or len(exact) == 1:
            raw, src = (exact or quoted)[0]["raw"].strip(), "note"
    if raw:
        same = [r for r in cand if norm(r["raw"]) == norm(raw)]
        row[side + "_raw"] = raw
        row[side + "_raw_src"] = src if same else src + "-unconfirmed"
        return
    # no raw anywhere: recover from the parsed book table on that page (same numbers + best text overlap)
    if not cand:
        reasons.append(f"{side}: raw line missing and no line with these numbers on page {page}")
        return
    tail = norm(desc.split(">")[-1].split(":")[-1])
    exact = [r for r in cand if norm(r["item"]) == tail]
    if len(exact) > 1:
        exact = [r for r in exact if r.get("table_title") and norm(r["table_title"]) in norm(desc)]
    if len(exact) == 1:
        row[side + "_raw"] = exact[0]["raw"].strip()
        row[side + "_raw_src"] = "book"
        return
    d = tokens(desc)
    scored = []
    for r in cand:
        t = tokens(r["item"] + " " + r.get("table_title", "") + " " + r.get("section", "") + " " + r["raw"])
        scored.append((len(d & t), r))
    scored.sort(key=lambda x: -x[0])
    if len(scored) == 1 or scored[0][0] > scored[1][0]:
        row[side + "_raw"] = scored[0][1]["raw"].strip()
        row[side + "_raw_src"] = "book"
    else:
        reasons.append(f"{side}: raw line missing and {len(cand)} indistinguishable lines on page {page}")


def check(row, ne_book, neca_book):
    r = []
    for c in ("ne_page", "ne_material_usd", "ne_manhours", "ne_unit", "neca_page", "neca_normal_hours", "neca_unit"):
        if row[c].lower() == "none":
            row[c] = ""
    for side in ("ne", "neca"):
        row[side + "_raw"] = row[side + "_raw_src"] = ""
        it = row[side + "_item"]
        is_none = it.lower() in ("none", "")
        nums = ("ne_material_usd", "ne_manhours") if side == "ne" else ("neca_normal_hours",)
        if is_none:
            row[side + "_item"] = "none"
            for c in nums + (side + "_unit",):
                if row[c]:
                    r.append(f"{c} set although {side}_item is none")
            continue
        if not row[side + "_page"].isdigit():
            r.append(f"{side}_page missing")
        for c in nums:
            if re.match(r"^\d{1,3}(,\d{3})+(\.\d+)?$", row[c]):
                row[c] = row[c].replace(",", "")  # thousands separator as printed in the book (e.g. 2,250.00)
            if not NUM.match(row[c]):
                r.append(f"{c} not numeric: {row[c]!r}")
        if not row[side + "_unit"]:
            r.append(f"{side}_unit missing")
        if r:
            continue
        book = ne_book if side == "ne" else neca_book
        resolve(side, row, book.get(int(row[side + "_page"]), []), r)
    if row["confidence"] not in CONF:
        r.append(f"confidence invalid: {row['confidence']!r}")
    if row["ne_item"] == "none" and row["neca_item"] == "none" and row["confidence"] != "none":
        r.append("both sides none but confidence != none")
    return r


def main():
    fams = json.load(open(FAM, encoding="utf-8"))
    weight = {f["family"]: int(f["marks_total"]) for f in fams}
    cat = {f["family"]: f["category"] for f in fams}
    ne_book, neca_book = load_books()
    kept, rejected = [], []
    paths = sorted(glob.glob(os.path.join(MAP_DIR, "chunk-*.csv")), key=chunk_key)
    for path in paths:
        ck = chunk_key(path)
        with open(path, encoding="utf-8-sig", newline="") as fh:
            rd = csv.DictReader(fh)
            if [h.strip() for h in rd.fieldnames] != COLS:
                sys.exit(f"{path}: unexpected header {rd.fieldnames}")
            for i, raw in enumerate(rd, start=2):
                if None in raw or any(v is None for v in raw.values()):
                    rejected.append({"chunk": str(ck), "source_line": str(i), "family": (raw.get("family") or "").strip(),
                                     "reject_reason": "malformed CSV row (column count)"})
                    continue
                row = {k.strip(): v.strip() for k, v in raw.items()}
                row["chunk"] = str(ck)
                reasons = check(row, ne_book, neca_book)
                if row["family"] not in weight:
                    reasons.append("family not in families.json")
                if reasons:
                    row["reject_reason"] = "; ".join(reasons)
                    row["source_line"] = str(i)
                    rejected.append(row)
                else:
                    kept.append(row)

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLS)
        w.writeheader()
        w.writerows(kept)
    with open(OUT_REJ, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["chunk", "source_line", "reject_reason"] + COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rejected)

    by_fam = {}
    for r in kept:
        by_fam.setdefault(r["family"], []).append(r)
    priced, none_fams, ne_only, neca_only, both = [], [], [], [], []
    conf_count = {c: 0 for c in CONF}
    conf_w = {c: 0 for c in CONF}
    by_cat = {}
    for f in fams:
        name = f["family"]
        rows = by_fam.get(name)
        c = by_cat.setdefault(f["category"], {"families": 0, "priced": 0, "marks": 0, "marks_priced": 0})
        c["families"] += 1
        c["marks"] += weight[name]
        if not rows:
            continue
        has_ne = any(r["ne_item"] != "none" for r in rows)
        has_neca = any(r["neca_item"] != "none" for r in rows)
        best = min((r["confidence"] for r in rows), key=CONF.index)
        conf_count[best] += 1
        conf_w[best] += weight[name]
        if has_ne or has_neca:
            priced.append(name)
            c["priced"] += 1
            c["marks_priced"] += weight[name]
            (both if has_ne and has_neca else ne_only if has_ne else neca_only).append(name)
        else:
            none_fams.append(name)
    missing = [f["family"] for f in fams if f["family"] not in by_fam]
    w_of = lambda names: sum(weight[n] for n in names)
    src = {}
    for r in kept:
        for s in ("ne", "neca"):
            if r[s + "_raw_src"]:
                src[s + ":" + r[s + "_raw_src"]] = src.get(s + ":" + r[s + "_raw_src"], 0) + 1
    stats = {
        "chunks": len(paths), "rows_read": len(kept) + len(rejected),
        "rows_kept": len(kept), "rows_rejected": len(rejected),
        "raw_source": src,
        "families_total": len(fams), "families_mapped": len(by_fam),
        "families_priced": len(priced), "families_none": len(none_fams), "families_missing": len(missing),
        "families_both_books": len(both), "families_ne_only": len(ne_only), "families_neca_only": len(neca_only),
        "marks_total": sum(weight.values()), "marks_priced": w_of(priced), "marks_none": w_of(none_fams),
        "marks_missing": w_of(missing), "marks_both": w_of(both), "marks_ne_only": w_of(ne_only),
        "marks_neca_only": w_of(neca_only),
        "confidence_families": conf_count, "confidence_marks": conf_w,
        "by_category": by_cat,
        "none_families": [{"family": n, "marks_total": weight[n], "category": cat[n], "chunk": by_fam[n][0]["chunk"],
                           "note": by_fam[n][0]["note"]} for n in sorted(none_fams, key=lambda n: -weight[n])],
        "missing_families": [{"family": n, "marks_total": weight[n], "category": cat[n]} for n in missing],
        "rejected": [{"chunk": r["chunk"], "line": r["source_line"], "family": r["family"], "reason": r["reject_reason"]} for r in rejected],
        "units_ne": sorted({r["ne_unit"] for r in kept if r["ne_unit"]}),
        "units_neca": sorted({r["neca_unit"] for r in kept if r["neca_unit"]}),
    }
    json.dump(stats, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
