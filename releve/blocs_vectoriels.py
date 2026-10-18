# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "numpy>=1.26"]
# ///
"""Blocs vectoriels : sur un plan CAO exporté en PDF vectoriel, un même symbole (bloc) est dessiné partout avec la
même géométrie. On regroupe les tracés voisins en « blocs », on leur donne une signature invariante à la position et à
la rotation (périmètre, aire, nombre d'opérations de chaque partie, écartement des parties), et on compte les blocs de
même signature. La légende (feuille `legende`) est traitée pareil : le bloc dessiné devant chaque description donne le
nom de la famille → les mêmes signatures sur les plans sont étiquetées automatiquement.

Sorties (dans WORKDIR) :
- `blocs/<feuille>.csv`   : un bloc par ligne — feuille, signature, x_pt, y_pt, w_pt, h_pt, angle_deg, n_parties, famille_legende
- `blocs-signatures.json` : signature → {n_total, par_feuille, legende (description, section, feuille, x, y)}

Usage : uv run releve/blocs_vectoriels.py WORKDIR [PDF] [--feuilles E101 E201] [--max-cote 45]
(les feuilles viennent de feuilles.csv ; la légende est la feuille de rôle `legende`.)

Validation (2026-10-17, S-1902 E-201 contre les 121 repères du relevé vérifié TEST-E201) : voir `tests/test_blocs_vectoriels.py`.
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, sys
from collections import defaultdict
import numpy as np
import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import PagesFeuilles  # noqa: E402

MAX_COTE = 45.0          # pt — plus grand qu'un symbole d'électricité (2'x2' = 23 pt, 'x4 = 12x30 pt)
MIN_COTE = 1.2           # pt — en dessous : trame, pointillés, flèches de cotation
MARGE_FUSION = 0.6       # pt — deux tracés dont les boîtes se touchent à ≤ marge font partie du même bloc
Q_PERIM, Q_AIRE = 0.5, 1.0   # pas de quantification (pt, pt²) des signatures de parties


def _points(item):
    """Liste de points (pt) d'un item de tracé pymupdf (l, c, re, qu)."""
    op = item[0]
    if op == "l":
        return [item[1], item[2]]
    if op == "c":                                   # cubique : on échantillonne 4 points
        p0, p1, p2, p3 = item[1:5]
        return [pymupdf.Point(((1 - t) ** 3) * p0.x + 3 * ((1 - t) ** 2) * t * p1.x + 3 * (1 - t) * t * t * p2.x + t ** 3 * p3.x,
                              ((1 - t) ** 3) * p0.y + 3 * ((1 - t) ** 2) * t * p1.y + 3 * (1 - t) * t * t * p2.y + t ** 3 * p3.y)
                for t in (0, 1 / 3, 2 / 3, 1)]
    if op == "re":
        r = item[1]; return [r.tl, r.tr, r.br, r.bl, r.tl]
    if op == "qu":
        q = item[1]; return [q.ul, q.ur, q.lr, q.ll, q.ul]
    return []


def partie(d):
    """Mesures brutes d'un tracé : périmètre, aire du polygone (si fermé), nb d'ops, fermé, rempli, et ses points."""
    pts = []
    for it in d["items"]:
        pts += _points(it)
    if len(pts) < 2:
        return None, None
    per = sum(math.hypot(pts[i + 1].x - pts[i].x, pts[i + 1].y - pts[i].y) for i in range(len(pts) - 1))
    aire = abs(sum(pts[i].x * pts[(i + 1) % len(pts)].y - pts[(i + 1) % len(pts)].x * pts[i].y for i in range(len(pts)))) / 2
    ferme = bool(d.get("closePath")) or math.hypot(pts[-1].x - pts[0].x, pts[-1].y - pts[0].y) < 0.3
    return (per, aire if ferme else 0.0, len(d["items"]), ferme, bool(d.get("fill"))), pts


def signature(parties, centres, pts_tous):
    """Signature d'un bloc invariante à la POSITION, à la ROTATION et à l'ÉCHELLE : toutes les longueurs sont divisées
    par le diamètre D du nuage de points du bloc (distance max entre deux points), puis quantifiées. La légende dessine
    chaque symbole à son échelle propre, les plans au 1:100 et parfois tournés de 37° : seule une signature sans unité
    retrouve le même bloc partout. (per/D, sqrt(aire)/D, nb d'ops, fermé, rempli) par partie + écartement des parties / D."""
    P = np.array([(q.x, q.y) for q in pts_tous])
    if len(P) < 2:
        return None, 0.0
    # diamètre : max des distances aux 2 points extrêmes (approximation O(n), suffisante pour quantifier)
    c = P.mean(axis=0); i = int(np.argmax(((P - c) ** 2).sum(axis=1))); j = int(np.argmax(((P - P[i]) ** 2).sum(axis=1)))
    D = float(np.hypot(*(P[i] - P[j])))
    if D < 0.5:
        return None, D
    q = lambda v: round(v * 10) / 10          # pas 0,1 : un même bloc dessiné à 3,80 et 3,85 reste une signature
    parts = sorted((q(per / D), q(math.sqrt(aire) / D), nops, ferme, fill) for per, aire, nops, ferme, fill in parties)
    ecart = max((math.hypot(a[0] - b[0], a[1] - b[1]) for a in centres for b in centres), default=0.0)
    return (tuple(parts), q(ecart / D)), D


def _fusionnable(a, b):
    """Deux tracés font partie du même bloc seulement s'ils ont la même épaisseur de trait (un bloc CAO est homogène ;
    un mur à 0,4 pt ne colle pas à un symbole à 0,6 pt) et s'ils ne sont pas DEUX formes fermées de ≥ 10 pt (deux
    luminaires 2'x2' qui se touchent restent deux symboles)."""
    if abs(a[3] - b[3]) > 0.05:
        return False
    ga, gb = max(a[0].width, a[0].height), max(b[0].width, b[0].height)
    if a[1][3] and b[1][3] and ga >= 10 and gb >= 10:
        return False
    return True


def _spans(page):
    """(rect, couleur) de chaque span de texte de la page — calculé une fois par page, jamais mis en cache par numéro de
    page (les feuilles lues dans travail/feuilles/<F>.pdf sont toutes « page 0 » de leur document)."""
    return [(pymupdf.Rect(sp["bbox"]), sp["color"]) for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for sp in l["spans"]]


def _texte_de_fond(w, spans):
    """Mot écrit en gris clair (« PENTE STR », trames d'architecture : couleur ≥ 0x80 sur chaque canal) : jamais une
    lettre de symbole (celles-ci sont noires ou gris foncé 0x404040). Revue PR #27 : un mot de fond qui chevauche un
    moteur ne doit pas entrer dans sa signature."""
    cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
    for r, c in spans:
        if r.x0 - 0.5 <= cx <= r.x1 + 0.5 and r.y0 - 0.5 <= cy <= r.y1 + 0.5:
            return min((c >> 16) & 255, (c >> 8) & 255, c & 255) >= 0x80
    return False


def texte_dans(blocs, page):
    """Lettres dessinées DANS un bloc (F, K, RA, ANN, S, DM, +/−…) : elles font partie du symbole et de sa signature —
    sans elles, station manuelle, klaxon et module isolateur ont le même carré. Un mot compte s'il est à ≥ 60 % dans
    la boîte du bloc (marge 1 pt), pas plus grand que le bloc, pas en gris clair (texte de fond), centré dedans."""
    spans = _spans(page)
    mots = [w for w in page.get_text("words") if w[4].strip() and not _texte_de_fond(w, spans)]
    for b in blocs:
        x0, y0 = b["x_pt"] - b["w_pt"] / 2 - 1, b["y_pt"] - b["h_pt"] / 2 - 1
        x1, y1 = b["x_pt"] + b["w_pt"] / 2 + 1, b["y_pt"] + b["h_pt"] / 2 + 1
        dedans = []
        for w in mots:
            if w[2] - w[0] > b["w_pt"] + 2 or w[3] - w[1] > b["h_pt"] + 2:
                continue
            ix = max(0, min(w[2], x1) - max(w[0], x0)); iy = max(0, min(w[3], y1) - max(w[1], y0))
            if ix * iy >= 0.6 * max(1e-6, (w[2] - w[0]) * (w[3] - w[1])):
                dedans.append((w[1], w[0], w[4]))
        b["texte"] = " ".join(t for _, _, t in sorted(dedans))
        # lettre de symbole (F, K, C, DM, RA, ANN, PAI, S, T, +/−) : petit bloc, 1 à 4 lettres — une désignation
        # (« (j,k) », « PP-2 3 ») dans un luminaire 2'x2' n'est PAS le symbole, elle reste en colonne `texte`
        # critère RELATIF au bloc (la légende dessine ANN à 23 pt, le plan à 7 pt) : lettres seules (1-4), hauteur du mot
        # ≤ 0,8 × diamètre du bloc — les désignations de circuits (chiffres, tirets, parenthèses) sont exclues par le motif
        # — et centrée dans le bloc (centre du mot à ≤ 0,5 × diamètre du centre du bloc)
        D = b.get("diametre_pt", 0) or 1
        lettres = [w for w in mots if (w[1], w[0], w[4]) in dedans]
        h_mots = max((w[3] - w[1] for w in lettres), default=0)
        centres = all(math.hypot((w[0] + w[2]) / 2 - b["x_pt"], (w[1] + w[3]) / 2 - b["y_pt"]) <= 0.5 * D + 0.5 for w in lettres)
        if b["texte"] and lettres and centres and re.fullmatch(r"[A-Za-z+\-/]{1,4}", b["texte"].replace(" ", "")) and 0.2 * D <= h_mots <= 0.8 * D + 0.5:
            sig = json.loads(b["signature"]); b["signature"] = json.dumps([sig[0], sig[1], b["texte"].replace(" ", "").upper()])
    return blocs


def blocs_page(page, max_cote=MAX_COTE):
    """Regroupe les tracés d'une page en blocs (union-find sur les boîtes qui se touchent)."""
    dr = page.get_drawings()
    cand = []
    for d in dr:
        r = d["rect"]
        if max(r.width, r.height) < MIN_COTE or max(r.width, r.height) > max_cote:
            continue
        mes, pts = partie(d)
        if mes is None:
            continue
        cand.append((r, mes, pts, round(float(d.get("width") or 0), 2)))
    n = len(cand)
    parent = list(range(n))
    # nombre de « grandes formes fermées » (≥ 10 pt) par composante : deux composantes qui en ont chacune une ne
    # fusionnent jamais, même via un petit trait qui les touche toutes les deux (revue Codex PR #27)
    gros = [1 if (c[1][3] and max(c[0].width, c[0].height) >= 10) else 0 for c in cand]
    boite = [[c[0].x0, c[0].y0, c[0].x1, c[0].y1] for c in cand]     # boîte de la COMPOSANTE (racine), mise à jour à chaque union

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i

    # balayage par x pour limiter les paires
    order = sorted(range(n), key=lambda i: cand[i][0].x0)
    xs0 = [cand[i][0].x0 for i in order]
    for a_, i in enumerate(order):
        ri = cand[i][0]
        j_ = a_ + 1
        while j_ < n and xs0[j_] <= ri.x1 + MARGE_FUSION:
            j = order[j_]; rj = cand[j][0]
            if rj.y0 <= ri.y1 + MARGE_FUSION and rj.y1 >= ri.y0 - MARGE_FUSION and _fusionnable(cand[i], cand[j]):
                # contraintes vérifiées sur les COMPOSANTES déjà fusionnées (revues Codex/Copilot PR #27) : la boîte
                # résultante reste ≤ max_cote (jamais un mur entier par chaînage) et au plus une grande forme fermée
                pa, pb = find(i), find(j)
                if pa != pb and not (gros[pa] and gros[pb]):
                    ba, bb = boite[pa], boite[pb]
                    x0, y0 = min(ba[0], bb[0]), min(ba[1], bb[1]); x1, y1 = max(ba[2], bb[2]), max(ba[3], bb[3])
                    if max(x1 - x0, y1 - y0) <= max_cote:
                        parent[pa] = pb; gros[pb] += gros[pa]; boite[pb] = [x0, y0, x1, y1]
            j_ += 1
    groupes = defaultdict(list)
    for i in range(n):
        groupes[find(i)].append(i)
    blocs = []
    for idx in groupes.values():
        rs = [cand[i][0] for i in idx]
        x0, y0 = min(r.x0 for r in rs), min(r.y0 for r in rs); x1, y1 = max(r.x1 for r in rs), max(r.y1 for r in rs)
        if max(x1 - x0, y1 - y0) > max_cote:
            continue
        parties = [cand[i][1] for i in idx]
        # un bloc fait d'un seul trait ouvert n'est pas un symbole (mur, trame, cotation)
        if len(idx) == 1 and not parties[0][3] and parties[0][2] <= 2:
            continue
        # un bloc plat (traits colinéaires : h ou w ≈ 0, aucune forme fermée) n'est pas un symbole non plus — morceau de
        # mur ou de cadre qui partage la signature « deux segments » d'un luminaire 1'x4' (revue PR #27)
        if min(x1 - x0, y1 - y0) < 0.5 and not any(p_[3] for p_ in parties):
            continue
        cs = [((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2) for r in rs]
        pts_tous = [q for i in idx for q in cand[i][2]]
        sig, D = signature(parties, cs, pts_tous)
        if sig is None:
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        blocs.append({"signature": json.dumps(sig), "x_pt": round(cx, 1), "y_pt": round(cy, 1), "w_pt": round(x1 - x0, 1), "h_pt": round(y1 - y0, 1),
                      "diametre_pt": round(D, 1), "n_parties": len(idx), "angle_deg": 0.0, "trait_pt": cand[idx[0]][3]})
    return blocs


def legende_page(page, blocs):
    """Pour chaque bloc de la feuille de légende : description = texte le plus proche à droite sur la même ligne."""
    mots = page.get_text("words")       # x0,y0,x1,y1,text,block,line,word
    lignes = defaultdict(list)
    for w in mots:
        lignes[(w[5], w[6])].append(w)
    textes = []
    for k, ws in lignes.items():
        ws.sort(key=lambda w: w[0])
        textes.append((min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws), max(w[3] for w in ws), " ".join(w[4] for w in ws)))
    for b in blocs:
        cands = [t for t in textes if t[0] >= b["x_pt"] + b["w_pt"] / 2 - 2 and t[0] - b["x_pt"] < 160 and abs((t[1] + t[3]) / 2 - b["y_pt"]) < 7]
        b["description"] = min(cands, key=lambda t: t[0] - b["x_pt"])[4] if cands else ""
    return blocs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("pdf", nargs="?", default=None, help="repli seulement : chaque feuille est lue dans travail/feuilles/<F>.pdf ou dans son fichier source")
    ap.add_argument("--feuilles", nargs="+", default=None); ap.add_argument("--max-cote", type=float, default=MAX_COTE)
    a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    rows = list(csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8")))
    pages = PagesFeuilles(work, a.pdf)
    os.makedirs(os.path.join(work, "blocs"), exist_ok=True)
    sigs = defaultdict(lambda: {"n_total": 0, "par_feuille": {}, "legende": None})
    for r in rows:
        f = r["feuille"]
        if a.feuilles and f not in a.feuilles and r.get("role") != "legende":
            continue
        page = pages.page(r)
        blocs = texte_dans(blocs_page(page, a.max_cote), page)
        if r.get("role") == "legende":
            legende_page(page, blocs)
            for b in blocs:
                if b.get("description"):
                    s = sigs[b["signature"]]
                    if not s["legende"]:
                        s["legende"] = {"description": b["description"], "feuille": f, "x_pt": b["x_pt"], "y_pt": b["y_pt"]}
        for b in blocs:
            b["feuille"] = f
            s = sigs[b["signature"]]; s["n_total"] += 1; s["par_feuille"][f] = s["par_feuille"].get(f, 0) + 1
        with open(os.path.join(work, "blocs", f + ".csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["feuille", "signature", "x_pt", "y_pt", "w_pt", "h_pt", "diametre_pt", "angle_deg", "n_parties", "trait_pt", "texte", "description"])
            w.writeheader()
            for b in blocs:
                w.writerow({k: b.get(k, "") for k in w.fieldnames})
        print(f"{f}: {len(blocs)} blocs")
    json.dump(sigs, open(os.path.join(work, "blocs-signatures.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(sigs)} signatures → blocs-signatures.json")


if __name__ == "__main__":
    main()
