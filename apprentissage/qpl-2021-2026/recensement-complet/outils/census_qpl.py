"""Full census of a Plan Expert (.qpl) corpus.

Covers every structure found in QuoterPlanSession files, not only Counters:
Counters (count takeoff), Lines (linear takeoff: conduit/cable runs), Areas,
Perimeters, Drops, Plans (sheets + scale), Groups/EEExchangeData (link to the
EE estimating database: ENSEMBLE ids) and Prices.

Usage: python census_qpl.py <corpus_dir> <out_dir> [<soumission_dir>]
Pure standard library. Writes CSV/JSON + SUMMARY.md into out_dir.
"""
import collections
import csv
import hashlib
import json
import math
import os
import re
import statistics
import sys
import xml.etree.ElementTree as ET

CORPUS, OUT = sys.argv[1], sys.argv[2]
SOUM = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(OUT, exist_ok=True)

S_RE = re.compile(r"\bS[- ]?(?:SIP|BR)?[- ]?0*(\d{3,4})", re.I)
COND_RE = re.compile(
    r"(?P<diam>\d+(?:''|\")?(?:\s*\d/\d)?|\d/\d|1''1/4|1''1/2)\s*(?P<nc>\d{1,2})\s*c\s*(?P<ga>\d{1,2})", re.I)


def s_number(text):
    m = S_RE.search(text or "")
    return int(m.group(1)) if m else None


def seg_len(e):
    try:
        return math.hypot(float(e.get("X2")) - float(e.get("X1")), float(e.get("Y2")) - float(e.get("Y1")))
    except (TypeError, ValueError):
        return 0.0


files = []
for root_dir, _dirs, names in os.walk(CORPUS):
    for n in names:
        if n.lower().endswith(".qpl"):
            files.append(os.path.join(root_dir, n))
files.sort()

# de-duplicate identical files (" - Copie", _gsdata_ saves) by sha256
seen = {}
proj_rows, bad = [], []
lab_tot = collections.Counter()
lab_proj = collections.Counter()
lab_ee = collections.defaultdict(collections.Counter)
ee_info = {}
ee_marks = collections.Counter()
ee_proj = collections.Counter()
ee_labels = collections.defaultdict(collections.Counter)
line_tot = collections.Counter()
line_len = collections.defaultdict(float)
line_proj = collections.Counter()
cond_spec = collections.Counter()
cond_len = collections.defaultdict(float)
scale_vals = collections.Counter()
price_nonzero = 0
per_sheet_rows = []

for p in files:
    raw = open(p, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    rel = os.path.relpath(p, CORPUS)
    if h in seen:
        continue
    seen[h] = rel
    try:
        r = ET.fromstring(raw)
    except ET.ParseError as ex:
        bad.append((rel, str(ex)))
        continue
    pj = r.find("Project")
    name = pj.findtext("Description", "") if pj is not None else ""
    created = pj.findtext("CreationDate", "") if pj is not None else ""
    modified = pj.findtext("LastModified", "") if pj is not None else ""
    sn = s_number(rel) or s_number(name)

    # Groups -> EE ensemble link
    gid2ee = {}
    for g in r.iter("Group"):
        x = g.find("EEExchangeData")
        if x is not None and x.get("ItemID"):
            gid2ee[g.get("GroupID")] = x.get("ItemID")
            ee_info.setdefault(x.get("ItemID"), {
                "item_type": x.get("ItemType", ""), "key": x.get("Key", ""),
                "name": x.get("Name", ""), "description": x.get("Description", "")})
    for pr in r.iter("Price"):
        try:
            if float(pr.get("CostEach", "0") or 0) > 0:
                price_nonzero += 1
        except ValueError:
            pass

    n_plans = n_cnt = n_el = n_lines = n_areas = n_perim = n_drops = 0
    tot_line_px = 0.0
    labs_here, ee_here, lines_here = set(), set(), set()
    for plan in r.iter("Plan"):
        layers = plan.find("Layers")
        if layers is None:
            continue
        n_plans += 1
        sc = plan.find("Scale")
        sv = sc.get("Value", "") if sc is not None else ""
        scale_vals[sv] += 1
        sheet_marks = 0
        sheet_len = 0.0
        for c in layers.iter("Counter"):
            n_cnt += 1
            k = len(c.findall("Element"))
            lab = (c.get("Name") or "").strip()
            n_el += k
            sheet_marks += k
            lab_tot[lab] += k
            if k:
                labs_here.add(lab)
            ee = gid2ee.get(c.get("GroupID"))
            if ee:
                lab_ee[lab][ee] += k
                ee_marks[ee] += k
                ee_labels[ee][lab] += k
                if k:
                    ee_here.add(ee)
        for ln in layers.iter("Line"):
            n_lines += 1
            nm = (ln.get("Name") or "").strip()
            L = sum(seg_len(e) for e in ln.findall("Element"))
            tot_line_px += L
            sheet_len += L
            line_tot[nm] += 1
            line_len[nm] += L
            lines_here.add(nm)
            m = COND_RE.search(nm)
            if m:
                spec = f"{m.group('diam').replace(' ', '')} {int(m.group('nc'))}c{int(m.group('ga'))}"
                cond_spec[spec] += 1
                cond_len[spec] += L
        n_areas += len(list(layers.iter("Area")))
        n_perim += len(list(layers.iter("Perimeter")))
        n_drops += len(list(layers.iter("Drop")))
        per_sheet_rows.append([rel, plan.get("Name", ""), sv, sheet_marks, round(sheet_len, 1)])
    for lab in labs_here:
        lab_proj[lab] += 1
    for ee in ee_here:
        ee_proj[ee] += 1
    for nm in lines_here:
        line_proj[nm] += 1
    proj_rows.append({
        "file": rel, "sha256": h[:16], "s_number": sn, "description": name,
        "created": created, "modified": modified, "n_plans": n_plans,
        "n_counters": n_cnt, "n_marks": n_el, "n_labels_used": len(labs_here),
        "n_lines": n_lines, "line_len_px": round(tot_line_px, 1),
        "n_areas": n_areas, "n_perimeters": n_perim, "n_drops": n_drops,
        "n_ee_groups": len(gid2ee), "n_ee_used": len(ee_here)})


def wcsv(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


keys = list(proj_rows[0].keys()) if proj_rows else []
wcsv("projets.csv", keys, [[r[k] for k in keys] for r in proj_rows])
wcsv("feuilles.csv", ["file", "plan", "scale_value", "marks", "line_len_px"], per_sheet_rows)
wcsv("etiquettes.csv", ["label", "marks_total", "n_projects", "top_ee_ensemble", "ee_key"],
     [[lab, n, lab_proj[lab],
       (lab_ee[lab].most_common(1)[0][0] if lab_ee[lab] else ""),
       (ee_info.get(lab_ee[lab].most_common(1)[0][0], {}).get("key", "") if lab_ee[lab] else "")]
      for lab, n in lab_tot.most_common()])
wcsv("ensembles-ee.csv", ["item_id", "item_type", "key", "name", "description", "marks_total", "n_projects", "labels"],
     [[i, d["item_type"], d["key"], d["name"], d["description"], ee_marks[i], ee_proj[i],
       " | ".join(f"{l}({n})" for l, n in ee_labels[i].most_common(5))]
      for i, d in sorted(ee_info.items(), key=lambda kv: -ee_marks[kv[0]])])
wcsv("lignes.csv", ["line_name", "occurrences", "n_projects", "len_px_total"],
     [[n, c, line_proj[n], round(line_len[n], 1)] for n, c in line_tot.most_common()])
wcsv("conduits-spec.csv", ["spec (diametre nb_cond calibre)", "occurrences", "len_px_total"],
     [[s, c, round(cond_len[s], 1)] for s, c in cond_spec.most_common()])

pairing = []
if SOUM and os.path.isdir(SOUM):
    folders = {}
    for d in os.listdir(SOUM):
        n = s_number(d)
        if n:
            folders.setdefault(n, []).append(d)
    by_s = collections.defaultdict(list)
    for r in proj_rows:
        if r["s_number"]:
            by_s[r["s_number"]].append(r)
    for n in sorted(set(folders) | set(by_s)):
        qs = by_s.get(n, [])
        pairing.append([n, " ; ".join(folders.get(n, [])), len(qs),
                        sum(q["n_marks"] for q in qs), " ; ".join(q["file"] for q in qs)[:500]])
    wcsv("appariement-plans-qpl.csv", ["s_number", "dossier_plans_drive", "n_qpl", "marks", "qpl_files"], pairing)

marks = [r["n_marks"] for r in proj_rows]
summary = {
    "qpl_files_found": len(files), "unique_after_sha256": len(seen), "parsed": len(proj_rows),
    "unparseable": bad, "with_marks": sum(1 for m in marks if m),
    "marks_total": sum(marks), "marks_median_per_project": statistics.median(marks) if marks else 0,
    "labels_distinct": len(lab_tot), "sheets": sum(r["n_plans"] for r in proj_rows),
    "lines_total": sum(r["n_lines"] for r in proj_rows),
    "projects_with_lines": sum(1 for r in proj_rows if r["n_lines"]),
    "areas_total": sum(r["n_areas"] for r in proj_rows),
    "ee_ensembles_distinct": len(ee_info),
    "projects_with_ee_link": sum(1 for r in proj_rows if r["n_ee_used"]),
    "marks_linked_to_ee": sum(ee_marks.values()),
    "prices_nonzero": price_nonzero,
    "scale_values_top": scale_vals.most_common(8),
    "conduit_specs_distinct": len(cond_spec),
}
if pairing:
    summary["pairing_s_with_plans_and_qpl"] = sum(1 for p in pairing if p[1] and p[2])
    summary["pairing_s_plans_only"] = sum(1 for p in pairing if p[1] and not p[2])
    summary["pairing_s_qpl_only"] = sum(1 for p in pairing if p[2] and not p[1])
json.dump(summary, open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
print("TOP EE:", [(ee_info[i]["key"], ee_marks[i], ee_proj[i]) for i, _ in ee_marks.most_common(15)])
print("TOP CONDUITS:", cond_spec.most_common(15))
