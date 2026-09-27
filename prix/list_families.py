#!/usr/bin/env python3
"""List the Dupuis symbol families to price.

Sources (read-only):
  apprentissage/qpl-2021-2026/dictionnaire-symboles.json  (337 canonical symbols + variants)
  apprentissage/qpl-2021-2026/categories.json             (439 recurring labels classified)
  apprentissage/qpl-2021-2026/normalisation.json          (fusion map + noise labels)
  recensement-complet/etiquettes.csv                      (11 807 raw labels, dedup mark counts)
  recensement-complet/ensembles-ee.csv                    (132 EE ensembles linked from QPLs)
  recensement-complet/conduits-spec.csv                   (98 conduit+wire specs from Line traces)

Output: prix/families.json — array of {family, category, examples_labels, ee_codes, marks_total}
sorted by marks_total desc. marks_total = dedup mark count from etiquettes.csv summed over the
canonical label and its variants (case-insensitive); for conduit specs it is the number of traced
lines (occurrences column). No number is invented: every count comes from those CSV/JSON files.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path("/home/claude/data/apprentissage/qpl-2021-2026")
REC = BASE / "recensement-complet"
OUT = Path(__file__).resolve().parent / "families.json"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().upper())


def main() -> None:
    dico = json.load(open(BASE / "dictionnaire-symboles.json", encoding="utf-8"))["symboles"]
    cats = {c["label"]: c for c in json.load(open(BASE / "categories.json", encoding="utf-8"))}
    normalisation = json.load(open(BASE / "normalisation.json", encoding="utf-8"))
    noise = {norm(x) for x in normalisation.get("rebut", [])}

    # canonical label -> family record ; variant (normalized) -> canonical
    fam = {}
    alias = {}
    for s in dico:
        lab = s["label"]
        fam[lab] = {
            "family": lab,
            "category": s.get("categorie") or cats.get(lab, {}).get("categorie", ""),
            "sous_type": s.get("sous_type", ""),
            "examples_labels": [],
            "ee_codes": [],
            "marks_total": 0,
        }
        alias[norm(lab)] = lab
        for v in s.get("variantes", []):
            alias.setdefault(norm(v), lab)
    for src, dst in normalisation.get("fusion", {}).items():
        if dst in fam:
            alias.setdefault(norm(src), dst)

    # dedup mark counts per raw label
    with open(REC / "etiquettes.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = norm(r["label"])
            if key in noise:
                continue
            canon = alias.get(key)
            if canon is None:
                continue
            fam[canon]["marks_total"] += int(r["marks_total"])
            fam[canon]["examples_labels"].append((int(r["marks_total"]), r["label"]))
            if r["ee_key"] and r["top_ee_ensemble"] not in fam[canon]["ee_codes"]:
                fam[canon]["ee_codes"].append(r["top_ee_ensemble"])

    # EE ensembles: attach by keyword to a family (only these deterministic rules)
    ens_rules = [
        (re.compile(r"^prise", re.I), "PRISE"),
        (re.compile(r"^interrupteur", re.I), "INT"),
        (re.compile(r"^tel/data", re.I), "TEL/DATA"),
        (re.compile(r"^BOITE ", re.I), "BOITE"),
        (re.compile(r"^RECEPT", re.I), "PRISE"),
    ]
    conduit_ens = defaultdict(list)  # (diam, nb, gauge) -> [codes]
    with open(REC / "ensembles-ee.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name = r["name"].strip()
            m = re.match(r"conduit\s+([\d/''\.]+)\s+0*(\d+)c(\d+)", name, re.I)
            if m:
                conduit_ens[(m.group(1), int(m.group(2)), int(m.group(3)))].append(r["item_id"])
                continue
            direct = alias.get(norm(name))
            for rx, target in ens_rules:
                if direct:
                    target = direct  # ensemble name is itself a canonical label/variant
                if rx.search(name) and target in fam:
                    if r["item_id"] not in fam[target]["ee_codes"]:
                        fam[target]["ee_codes"].append(r["item_id"])
                    if int(r["marks_total"]) and name not in [x[1] for x in fam[target]["examples_labels"]]:
                        # marks already counted via etiquettes.csv; only keep the label as example
                        fam[target]["examples_labels"].append((int(r["marks_total"]), name))
                    break

    out = []
    for rec in fam.values():
        if rec["marks_total"] == 0 and not rec["ee_codes"]:
            continue
        ex = sorted(set(rec["examples_labels"]), key=lambda t: -t[0])
        rec["examples_labels"] = [lab for _, lab in ex[:8]]
        out.append(rec)

    # conduit + wire specs as families
    with open(REC / "conduits-spec.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            spec = r["spec (diametre nb_cond calibre)"]
            m = re.match(r"^(\S+)\s+(\d+)c(\d+)$", spec)
            if not m:
                continue
            diam, nb, gauge = m.group(1), int(m.group(2)), int(m.group(3))
            diam_txt = diam.replace("''", " ")  # 1''1/4 -> 1 1/4
            out.append({
                "family": f"{diam_txt} EMT {nb}#{gauge}",
                "category": "conduit_filage",
                "sous_type": f"conduit {diam_txt} po, {nb} conducteurs #{gauge} (Line traces; source spec '{spec}')",
                "examples_labels": [spec],
                "ee_codes": conduit_ens.get((diam, nb, gauge), []),
                "marks_total": int(r["occurrences"]),
            })

    out.sort(key=lambda r: -r["marks_total"])
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} families -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
