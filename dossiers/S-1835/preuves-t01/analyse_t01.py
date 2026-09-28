"""S-1835: integrate telecom addendum T-01 into the takeoff and prove every change.

    python dossiers/S-1835/preuves-t01/analyse_t01.py WORKDIR DOSSIER_DIR

WORKDIR     prepare.py output for the full input set (original telecom + electrical sets, E-01 and T-01).
DOSSIER_DIR dossiers/S-1835 (read: releve.xlsx marks of the previous takeoff; write: preuves-t01/*).

What it does (deterministic, no hand-typed figure):
1. detects the ceiling-speaker symbol (black disc, ~10.6 pt, drawn as horizontal filled slabs) on every
   telecom plan sheet, original (T-D400..T-D422) and T-01 (T-D420..T-D422 rev. 1);
2. checks every pair of sheets of the same floor for overlapping viewports: each speaker-to-speaker
   translation is a candidate registration, scored by the share of vector line endpoints that coincide;
   a true overlap aligns the whole background (share >= OVERLAP_SHARE), so its coinciding speakers are
   the same physical device drawn twice;
3. compares each original sheet with its T-01 revision (translation, vector diff, text diff, speakers);
4. rewrites the occurrence files of WORKDIR: original D420/D421/D422 replaced by the T-01 sheets,
   cross-sheet duplicates kept once (on the first sheet of the pair), every other mark unchanged;
5. writes the evidence tables (CSV + Markdown) and a JSON summary next to this script.
"""
from __future__ import annotations

import collections
import csv
import itertools
import json
import math
import os
import random
import sys

import numpy as np
import openpyxl
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SPEAKER = "Haut-parleur existant — dépose/entreposage"
SPEAKER_NOTE = "disque noir Ø10,6 pt (lecture vectorielle)"
ORIGINAL_TELECOM = ["D400", "D401", "D402", "D403", "D410", "D411", "D412", "D413", "D420", "D421", "D422"]
T01_REPLACES = {"D420_ADD": "D420", "D421_ADD": "D421", "D422_ADD": "D422"}
T01_TEXT = "D420_ADD_2"
FLOORS = {
    "RDC": ["D410", "D411", "D412", "D413"],
    "ÉTAGE (original)": ["D420", "D421", "D422"],
    "ÉTAGE (T-01)": ["D420_ADD", "D421_ADD", "D422_ADD"],
}
OVERLAP_SHARE = 0.10   # observed: true overlaps 0.21-0.22, thin T-01 match strip 0.03, noise <= 0.03
MATCH_PT = 2.0         # two speaker centres closer than this (after registration) are the same device
BASE_REV = "2875138"   # origin/releve-S-1835 before this fix
PLAN_XMAX = 2700       # right edge of the drawing area (title block and notes are to the right)
PT_TO_M_1_100 = 0.0254 / 72 * 100   # 1 pt on paper at 1:100 in metres


# ---------------------------------------------------------------- detection
_DRAWINGS = {}


def drawings(page):
    """page.get_drawings() is slow on 40k-path sheets: compute it once per page."""
    key = id(page)
    if key not in _DRAWINGS:
        _DRAWINGS[key] = page.get_drawings()
    return _DRAWINGS[key]


def black_discs(page, dmin=9.5, dmax=11.8):
    """Black discs built from thin horizontal filled slabs (how the CAD export draws a solid circle)."""
    slabs = []
    for d in drawings(page):
        f = d.get("fill")
        if f is None or d["type"] not in ("f", "fs") or max(f) > 0.05:
            continue
        r = d["rect"]
        if r.height < 1.3 and r.width < 12.5:
            slabs.append(r)
    by_x = collections.defaultdict(list)
    for i, r in enumerate(slabs):
        by_x[round((r.x0 + r.x1) / 2)].append(i)
    used = [False] * len(slabs)
    out = []
    for i, r in enumerate(slabs):
        if used[i]:
            continue
        g = pymupdf.Rect(r)
        used[i] = True
        grew = True
        while grew:
            grew = False
            cx = round((g.x0 + g.x1) / 2)
            for k in (cx - 1, cx, cx + 1):
                for j in by_x.get(k, []):
                    s = slabs[j]
                    if not used[j] and s.y0 <= g.y1 + 0.3 and s.y1 >= g.y0 - 0.3:
                        g |= s
                        used[j] = True
                        grew = True
        if dmin <= g.width <= dmax and dmin <= g.height <= dmax:
            out.append((round((g.x0 + g.x1) / 2, 1), round((g.y0 + g.y1) / 2, 1), round(g.width, 1)))
    return sorted(out, key=lambda p: (p[1], p[0]))


def endpoints(page):
    pts = []
    for d in drawings(page):
        for it in d["items"]:
            if it[0] == "l":
                for p in it[1:3]:
                    if p.x < PLAN_XMAX and 60 < p.y < 2330:
                        pts.append((p.x, p.y))
    return np.array(pts, dtype=float)


def _keys(pts, tol):
    q = np.round(pts / tol).astype(np.int64)
    return q[:, 0] * 1_000_003 + q[:, 1]


def share(a_pts, b_pts, dx, dy, tol=1.0):
    """Share of b's line endpoints that land on one of a's endpoints (grid tol) after translating b by (dx, dy)."""
    grid = np.unique(_keys(a_pts, tol))
    k = _keys(b_pts + np.array([dx, dy]), tol)
    i = np.clip(np.searchsorted(grid, k), 0, len(grid) - 1)
    return float(np.mean(grid[i] == k)) if len(k) else 0.0


def best_registration(ep_a, ep_b, disc_a, disc_b, extra=()):
    """Best translation b->a among speaker-pair offsets (and extra candidates), scored on a sample."""
    idx = random.Random(0).sample(range(len(ep_b)), min(5000, len(ep_b)))
    sample = ep_b[sorted(idx)]
    seen, best = set(), (0.0, None)
    cands = [(pa[0] - pb[0], pa[1] - pb[1]) for pa in disc_a for pb in disc_b] + list(extra)
    for dx, dy in cands:
        k = (round(dx), round(dy))
        if k in seen:
            continue
        seen.add(k)
        s = share(ep_a, sample, dx, dy, tol=1.0)
        if s > best[0]:
            best = (s, (dx, dy))
    return best, len(seen)


def pairs_at(disc_a, disc_b, off):
    dx, dy = off
    return [(pa, pb) for pa in disc_a for pb in disc_b if abs(pa[0] - pb[0] - dx) < MATCH_PT and abs(pa[1] - pb[1] - dy) < MATCH_PT]


# ---------------------------------------------------------------- vector / text diff
def draw_sig(d, dx=0.0, dy=0.0):
    r = d["rect"]
    col = tuple(round(c, 2) for c in d["color"]) if d.get("color") else None
    fill = tuple(round(c, 2) for c in d["fill"]) if d.get("fill") else None
    return (d["type"], round(r.x0 + dx), round(r.y0 + dy), round(r.x1 + dx), round(r.y1 + dy), col, fill, len(d["items"]))


def words(work, f):
    with open(os.path.join(work, "texte", f + "-mots.csv"), encoding="utf-8") as fh:
        return collections.Counter(r["mot"] for r in csv.DictReader(fh))


# ---------------------------------------------------------------- main
def main(work, dossier):
    out_dir = HERE
    pages = {f: pymupdf.open(os.path.join(work, "feuilles", f + ".pdf"))[0] for f in ORIGINAL_TELECOM + list(T01_REPLACES)}
    discs = {f: black_discs(p) for f, p in pages.items()}
    eps = {}

    def ep(f):
        if f not in eps:
            eps[f] = endpoints(pages[f])
        return eps[f]

    # 2. same-floor overlaps
    overlaps, dup_drop = [], {}      # dup_drop[(sheet, x, y)] = (kept_sheet, kx, ky)
    for floor, sheets in FLOORS.items():
        for a, b in itertools.combinations(sheets, 2):
            (s, off), n = best_registration(ep(a), ep(b), discs[a], discs[b])
            dups = pairs_at(discs[a], discs[b], off) if off and s >= OVERLAP_SHARE else []
            overlaps.append({"etage": floor, "feuille_a": a, "feuille_b": b, "candidats": n, "part_commune": round(s, 3),
                             "dx_pt": round(off[0], 1) if off else "", "dy_pt": round(off[1], 1) if off else "",
                             "recouvrement": "oui" if s >= OVERLAP_SHARE else "non", "doublons": len(dups)})
            for pa, pb in dups:
                dup_drop[(b, pb[0], pb[1])] = (a, pa[0], pa[1])

    # 3. original vs T-01 revision
    revisions = []
    for add, orig in T01_REPLACES.items():
        (s, off), _ = best_registration(ep(add), ep(orig), discs[add], discs[orig], extra=[(0.0, 0.0)])
        dx, dy = off
        full = share(ep(add), ep(orig), dx, dy, tol=0.25)
        same = pairs_at(discs[add], discs[orig], off)
        gone = [p for p in discs[orig] if not any(abs(p[0] + dx - q[0]) < MATCH_PT and abs(p[1] + dy - q[1]) < MATCH_PT for q in discs[add])]
        new = [q for q in discs[add] if not any(abs(p[0] + dx - q[0]) < MATCH_PT and abs(p[1] + dy - q[1]) < MATCH_PT for p in discs[orig])]
        do = [d for d in drawings(pages[orig]) if d["rect"].x1 < PLAN_XMAX]
        da = [d for d in drawings(pages[add]) if d["rect"].x1 < PLAN_XMAX]
        co = collections.Counter(draw_sig(d, dx, dy) for d in do)
        ca = collections.Counter(draw_sig(d) for d in da)
        wo, wa = words(work, orig), words(work, add)
        # fibre route drawn by T-01: new black 0.42 pt polylines
        only_t01 = ca - co
        new_black = [d for d in da if draw_sig(d) in only_t01 and d.get("color") and max(d["color"]) < 0.05
                     and d["type"] == "s" and all(it[0] == "l" for it in d["items"]) and abs((d.get("width") or 0) - 0.42) < 0.01]
        route_pt = sum(math.dist(it[1], it[2]) for d in new_black for it in d["items"])
        revisions.append({"feuille_originale": orig, "feuille_t01": add, "dx_pt": round(dx, 1), "dy_pt": round(dy, 1),
                          "part_commune": round(full, 3), "traces_original": len(do), "traces_t01": len(da),
                          "traces_seulement_original": sum((co - ca).values()), "traces_seulement_t01": sum((ca - co).values()),
                          "hp_original": len(discs[orig]), "hp_t01": len(discs[add]), "hp_identiques": len(same),
                          "hp_absents_t01": len(gone), "hp_nouveaux_t01": len(new),
                          "mots_ajoutes_t01": " ".join(sorted((wa - wo).elements())),
                          "mots_retires_t01": " ".join(sorted((wo - wa).elements())),
                          "trace_fibre_pt": round(route_pt, 1), "trace_fibre_m_1_100": round(route_pt * PT_TO_M_1_100, 1),
                          "_gone": gone, "_new": new})

    # where did each speaker missing from T-01 go? (the original D420/D421 overlap is the only registered one)
    for r in revisions:   # D420/D421 revisions keep the original frame, so the D420/D421 registration applies to T-01 too
        if r["feuille_originale"] in ("D420", "D421"):
            assert abs(r["dx_pt"]) < 0.5 and abs(r["dy_pt"]) < 0.5, r
    ov = {(o["feuille_a"], o["feuille_b"]): o for o in overlaps}
    reg_420_421 = ov[("D420", "D421")]
    off = (reg_420_421["dx_pt"], reg_420_421["dy_pt"])          # D421 -> D420 frame
    t01_disc = {orig: discs[add] for add, orig in T01_REPLACES.items()}
    fate = []
    for rev in revisions:
        orig = rev["feuille_originale"]
        for x, y, _ in rev["_gone"]:
            if orig == "D420":
                other, ox, oy = "D421", x - off[0], y - off[1]
            elif orig == "D421":
                other, ox, oy = "D420", x + off[0], y + off[1]
            else:
                other = None
            still = other and any(abs(ox - q[0]) < MATCH_PT and abs(oy - q[1]) < MATCH_PT for q in t01_disc[other])
            twin = other and any(abs(ox - q[0]) < MATCH_PT and abs(oy - q[1]) < MATCH_PT for q in discs[other])
            fate.append({"feuille_originale": orig, "x_pt": x, "y_pt": y, "vue_aussi_sur": other if twin else "",
                         "x_autre": round(ox, 1) if other else "", "y_autre": round(oy, 1) if other else "",
                         "present_sur_t01": f"{other}_ADD" if still else "non",
                         "conclusion": ("doublon du chevauchement original, conservé une fois sur " + other + "_ADD") if still
                         else "retiré du dessin par T-01 (absent des deux feuilles révisées)"})

    # T-01 viewports at the original D420/D421 registration: thin match strip only, no speaker drawn twice
    t01_strip = {"part_commune": round(share(ep("D420_ADD"), ep("D421_ADD"), off[0], off[1]), 3),
                 "doublons": len(pairs_at(discs["D420_ADD"], discs["D421_ADD"], off)), "dx_pt": off[0], "dy_pt": off[1]}
    removed_devices = {(round(f["x_pt"] if f["feuille_originale"] == "D420" else f["x_autre"]),
                        round(f["y_pt"] if f["feuille_originale"] == "D420" else f["y_autre"]))
                       for f in fate if f["present_sur_t01"] == "non"}

    # 4. occurrences
    # previous takeoff, as delivered before this fix (reading it from git keeps reruns idempotent)
    import io
    import subprocess
    xlsx = subprocess.run(["git", "show", f"{BASE_REV}:dossiers/S-1835/releve.xlsx"], cwd=dossier, check=True, capture_output=True).stdout
    wb = openpyxl.load_workbook(io.BytesIO(xlsx), read_only=True)
    rows = list(wb["Marques"].iter_rows(min_row=2, values_only=True))
    before = [dict(feuille=r[1], label=r[2], x_pt=r[3], y_pt=r[4], source=r[5] or "", note=r[6] or "") for r in rows]
    after, dropped = [], []
    for o in before:
        if o["label"] == SPEAKER and o["feuille"] in T01_REPLACES.values():
            dropped.append({**o, "raison": f"feuille remplacée par {o['feuille']}_ADD (addenda T-01)"})
            continue
        if o["label"] == SPEAKER:
            x, y = float(o["x_pt"]), float(o["y_pt"])
            hit = next((v for k, v in dup_drop.items() if k[0] == o["feuille"] and abs(k[1] - x) < MATCH_PT and abs(k[2] - y) < MATCH_PT), None)
            if hit:
                dropped.append({**o, "raison": f"doublon : même haut-parleur que {hit[0]} ({hit[1]}, {hit[2]}), vues superposées"})
                continue
        after.append(o)
    for add in T01_REPLACES:
        for x, y, _ in discs[add]:
            after.append(dict(feuille=add, label=SPEAKER, x_pt=f"{x:.1f}", y_pt=f"{y:.1f}", source="visuel",
                              note=f"{SPEAKER_NOTE} — T-{T01_REPLACES[add]} rév. 1 (addenda T-01)"))
    # sanity: the previous takeoff's speaker marks are exactly the detected discs of the original sheets
    prev = collections.Counter(o["feuille"] for o in before if o["label"] == SPEAKER)
    for f in ORIGINAL_TELECOM:
        assert prev.get(f, 0) == len(discs[f]), (f, prev.get(f, 0), len(discs[f]))
    fields = ["feuille", "label", "x_pt", "y_pt", "source", "note"]
    for name, pred in (("occurrences-texte.csv", lambda o: o["source"] == "texte"), ("occurrences-visuel.csv", lambda o: o["source"] != "texte")):
        with open(os.path.join(work, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows({k: o[k] for k in fields} for o in after if pred(o))

    # 5. evidence
    def write_csv(name, data, fields=None):
        fields = fields or [k for k in data[0] if not k.startswith("_")]
        with open(os.path.join(out_dir, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(data)

    det = []
    for f in ORIGINAL_TELECOM + list(T01_REPLACES):
        for x, y, dia in discs[f]:
            if f in T01_REPLACES.values():
                st = "remplacé (feuille révisée par T-01)"
            elif (f, x, y) in dup_drop:
                k = dup_drop[(f, x, y)]
                st = f"doublon de {k[0]} ({k[1]}, {k[2]}) — retiré"
            else:
                st = "relevé"
            det.append({"feuille": f, "x_pt": x, "y_pt": y, "diametre_pt": dia, "statut": st})
    write_csv("haut-parleurs-detection.csv", det)
    write_csv("recalage-feuilles.csv", overlaps)
    write_csv("comparaison-t01.csv", revisions)
    write_csv("haut-parleurs-absents-t01.csv", fate)
    write_csv("marques-retirees.csv", dropped, fields + ["raison"])

    tb, ta = collections.Counter(o["label"] for o in before), collections.Counter(o["label"] for o in after)
    sb = collections.Counter(o["feuille"] for o in before if o["label"] == SPEAKER)
    sa = collections.Counter(o["feuille"] for o in after if o["label"] == SPEAKER)
    table = [{"libelle": l, "avant": tb[l], "apres": ta[l], "ecart": ta[l] - tb[l]} for l in sorted(set(tb) | set(ta))]
    table.append({"libelle": "TOTAL", "avant": sum(tb.values()), "apres": sum(ta.values()), "ecart": sum(ta.values()) - sum(tb.values())})
    write_csv("avant-apres-libelles.csv", table)
    sheets = ORIGINAL_TELECOM + list(T01_REPLACES)
    per_sheet = [{"feuille": f, "avant": sb.get(f, 0), "apres": sa.get(f, 0), "ecart": sa.get(f, 0) - sb.get(f, 0)} for f in sheets]
    per_sheet.append({"feuille": "TOTAL", "avant": sum(sb.values()), "apres": sum(sa.values()), "ecart": sum(sa.values()) - sum(sb.values())})
    write_csv("avant-apres-haut-parleurs.csv", per_sheet)

    summary = {
        "haut_parleurs_avant": sum(sb.values()), "haut_parleurs_apres": sum(sa.values()),
        "marques_avant": sum(tb.values()), "marques_apres": sum(ta.values()),
        "marques_visuel_apres": sum(1 for o in after if o["source"] != "texte"),
        "marques_texte_apres": sum(1 for o in after if o["source"] == "texte"),
        "sous_sol_disques": {f: len(discs[f]) for f in ("D400", "D401", "D402", "D403")},
        "doublons_retires": sum(1 for d in dropped if d["raison"].startswith("doublon")),
        "doublons_par_paire": {f"{o['feuille_a']}|{o['feuille_b']}": o["doublons"] for o in overlaps if o["doublons"]},
        "t01_hp": {a: len(discs[a]) for a in T01_REPLACES},
        "original_hp": {o: len(discs[o]) for o in T01_REPLACES.values()},
        "t01_retires_du_dessin": [f for f in fate if f["present_sur_t01"] == "non"],
        "t01_appareils_retires": len(removed_devices), "t01_bande_raccord": t01_strip,
        "t01_doublons_resolus": sum(1 for f in fate if f["present_sur_t01"] != "non"),
        "t01_nouveaux": sum(r["hp_nouveaux_t01"] for r in revisions),
        "trace_fibre_m_1_100": round(sum(r["trace_fibre_m_1_100"] for r in revisions), 1),
        "revisions": [{k: v for k, v in r.items() if not k.startswith("_")} for r in revisions],
        "recalages": overlaps, "seuil_recouvrement": OVERLAP_SHARE, "tolerance_pt": MATCH_PT,
        "par_libelle": table, "par_feuille_hp": per_sheet,
    }
    json.dump(summary, open(os.path.join(out_dir, "resume-t01.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)

    md = ["# Addenda T-01 — preuves (généré par `analyse_t01.py`)", "",
          "## Haut-parleurs par feuille, avant / après", "", "| feuille | avant | après | écart |", "|---|--:|--:|--:|"]
    md += [f"| {r['feuille']} | {r['avant']} | {r['apres']} | {r['ecart']:+d} |" for r in per_sheet]
    md += ["", "## Tous les libellés, avant / après", "", "| libellé | avant | après | écart |", "|---|--:|--:|--:|"]
    md += [f"| {r['libelle']} | {r['avant']} | {r['apres']} | {r['ecart']:+d} |" for r in table]
    md += ["", "## Feuilles révisées par T-01 (comparaison vectorielle)", "",
           "| original → T-01 | décalage (pt) | tracés communs | tracés seulement orig. / T-01 | HP orig. | HP T-01 | identiques | absents de T-01 | nouveaux | tracé fibre (m à 1:100) |",
           "|---|---|--:|---|--:|--:|--:|--:|--:|--:|"]
    md += [f"| {r['feuille_originale']} → {r['feuille_t01']} | {r['dx_pt']}, {r['dy_pt']} | {r['part_commune']:.1%} | {r['traces_seulement_original']} / {r['traces_seulement_t01']} | "
           f"{r['hp_original']} | {r['hp_t01']} | {r['hp_identiques']} | {r['hp_absents_t01']} | {r['hp_nouveaux_t01']} | {r['trace_fibre_m_1_100']} |" for r in revisions]
    md += ["", "Mots ajoutés / retirés par T-01 : voir `comparaison-t01.csv`.", "",
           "## Haut-parleurs absents des feuilles T-01", "", "| feuille orig. | x | y | vu aussi sur | position sur l'autre feuille | présent sur T-01 | conclusion |", "|---|--:|--:|---|---|---|---|"]
    md += [f"| {f['feuille_originale']} | {f['x_pt']} | {f['y_pt']} | {f['vue_aussi_sur'] or '—'} | {f['x_autre']}, {f['y_autre']} | {f['present_sur_t01']} | {f['conclusion']} |" for f in fate]
    md += ["", f"Appareils distincts retirés du dessin par T-01 : {len(removed_devices)} (une ligne par feuille où il figurait). "
           f"Au recalage original D420/D421 ({off[0]}, {off[1]} pt), les vues T-01 ne partagent qu'une bande de raccord : "
           f"{t01_strip['part_commune']:.1%} de tracés communs, {t01_strip['doublons']} haut-parleur en double."]
    md += ["", f"## Recouvrement des vues d'un même étage (seuil {OVERLAP_SHARE:.0%} de tracés communs)", "",
           "| étage | feuilles | translations testées | meilleure part commune | décalage (pt) | recouvrement | doublons |", "|---|---|--:|--:|---|---|--:|"]
    md += [f"| {o['etage']} | {o['feuille_a']} / {o['feuille_b']} | {o['candidats']} | {o['part_commune']:.1%} | {o['dx_pt']}, {o['dy_pt']} | {o['recouvrement']} | {o['doublons']} |" for o in overlaps]
    md += ["", "## Sous-sol (T-D400 à T-D403)", "", "| feuille | disques noirs Ø 9,5–11,8 pt |", "|---|--:|"]
    md += [f"| {f} | {n} |" for f, n in summary["sous_sol_disques"].items()]
    open(os.path.join(out_dir, "preuves-t01.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(json.dumps({k: summary[k] for k in ("haut_parleurs_avant", "haut_parleurs_apres", "marques_avant", "marques_apres", "doublons_retires",
                                              "t01_doublons_resolus", "t01_appareils_retires", "t01_bande_raccord", "t01_nouveaux", "sous_sol_disques", "trace_fibre_m_1_100")}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
