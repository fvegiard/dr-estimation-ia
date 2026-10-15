# /// script
# requires-python = ">=3.12"
# dependencies = ["opencv-python-headless>=4.9", "numpy>=1.26", "pymupdf>=1.24"]
# ///
"""Ancrage des pastilles sur le symbole, pour les feuilles RASTER (plan scanné / PNG : aucun tracé vectoriel,
donc `src/estimer/render/ancrage.py` ne peut rien ancrer). Correctif du 2026-10-15 (TEST-E201, vérificateur
indépendant) : 8 pastilles décalées de 3 à 10 pt et des cercles 2 fois trop gros, parce que les coordonnées
étaient lues sur les règles d'un zoom (± 1 pt) ou prises au centroïde des pixels sombres — qu'un remplissage
mi-noir attire vers lui.

Pour chaque occurrence de `occurrences-visuel.csv` dont la famille a une forme `cercle` ou `carre` :
- cercle : ajustement de cercle (Hough) autour du point ; on garde le cercle le plus proche (≤ 6 pt) → x, y, rayon_pt ;
- carre / rectangle : composante connexe sombre la plus proche, puis RECTANGLE MINIMAL ENGLOBANT de ses pixels
  (`minAreaRect`, qui dépend du contour et jamais du remplissage) → x, y, x0..y1 (boîte axée centrée) et angle_deg.
Un symbole non retrouvé garde ses coordonnées d'origine et est listé dans `ancrage-raster.json` (à vérifier au zoom).
Le rendu (`render_vectoriel.py` → `from_releve`) lit ces colonnes : `rayon_pt` (rayon de la pastille, plancher
`style.MARK_RADIUS_MIN`), `x0_pt..y1_pt` + `angle_deg` (boîte tournée).

Usage : uv run releve/ancrage_raster.py WORKDIR [--feuille F] [--max-deplacement 8]
Idempotent : relancer ne bouge plus rien (le symbole est déjà sous la pastille).
"""
from __future__ import annotations
import argparse, csv, json, math, os, sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import load_nomenclature, CIRCLE, SQUARE  # noqa: E402

RAYON_MIN, RAYON_MAX = 1.5, 9.0        # pt — plage des symboles circulaires d'un plan d'électricité (4,6 à 18 pt de diamètre)
COTE_MIN, COTE_MAX = 3.0, 45.0         # pt — carrés 2'x2' (18 pt), rectangles 'x4 (35 pt), petits boîtiers (6 pt)
SEUIL_NOIR = 100                       # niveau de gris sous lequel un pixel est « encre »


def _raster(work: str, feuille: str):
    path = os.path.join(work, "rasters", feuille + ".png")
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, 0.0
    rows = {r["feuille"]: r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8"))}
    largeur_pt = float(rows[feuille]["largeur_pt"]) if feuille in rows else 2383.94
    return img, img.shape[1] / largeur_pt          # px par pt


def ajuster_cercle(img, s, x, y, max_dep):
    """Centre et rayon (pt) du cercle le plus proche de (x, y), ou None."""
    X, Y, h = int(x * s), int(y * s), int((RAYON_MAX + max_dep) * s)
    c = img[max(0, Y - h):Y + h, max(0, X - h):X + h]
    if c.size == 0:
        return None
    cir = cv2.HoughCircles(cv2.GaussianBlur(c, (3, 3), 0), cv2.HOUGH_GRADIENT, dp=1, minDist=int(RAYON_MIN * s),
                           param1=120, param2=14, minRadius=int(RAYON_MIN * s), maxRadius=int(RAYON_MAX * s))
    if cir is None:
        return None
    ox, oy = X - max(0, X - h), Y - max(0, Y - h)
    best = None
    for cx, cy, r in cir[0]:
        d = math.hypot(cx - ox, cy - oy) / s
        if d <= max_dep and (best is None or d < best[0]):
            best = (d, cx, cy, r)
    if best is None:
        return None
    _, cx, cy, r = best
    return (max(0, X - h) + cx) / s, (max(0, Y - h) + cy) / s, r / s + 0.4


def ajuster_boite(img, s, x, y, max_dep):
    """Centre, largeur, hauteur (pt) et angle (°) du rectangle minimal englobant la composante sombre la plus proche."""
    X, Y, h = int(x * s), int(y * s), int((COTE_MAX / 2 + max_dep) * s)
    x0, y0 = max(0, X - h), max(0, Y - h)
    c = img[y0:Y + h, x0:X + h]
    if c.size == 0:
        return None
    m = (c < SEUIL_NOIR).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    ox, oy = X - x0, Y - y0
    cands = []
    for j in range(1, n):
        w, hh, area = st[j][cv2.CC_STAT_WIDTH] / s, st[j][cv2.CC_STAT_HEIGHT] / s, st[j][cv2.CC_STAT_AREA]
        if area < 40 or max(w, hh) < COTE_MIN or max(w, hh) > COTE_MAX * 1.5:
            continue
        d = math.hypot(cen[j][0] - ox, cen[j][1] - oy) / s
        if d <= max_dep + max(w, hh) / 2:
            cands.append((d, j))
    # du plus proche au plus loin : la première boîte qui CONTIENT le point d'origine (marge 3 pt) gagne —
    # sinon un texte voisin (« E.A.R », « PP-2 ») ou le trait de mur attire la pastille (TEST-E201 : ANN, F, ⊠)
    for _, j in sorted(cands):
        pts = np.column_stack(np.where(lab == j))[:, ::-1].astype(np.float32)
        (rx, ry), (rw, rh), ang = cv2.minAreaRect(pts)
        if rw < rh:
            rw, rh, ang = rh, rw, ang + 90
        a_ = math.radians(ang); dx, dy = ox - rx, oy - ry
        u, v = dx * math.cos(a_) + dy * math.sin(a_), -dx * math.sin(a_) + dy * math.cos(a_)
        if abs(u) <= rw / 2 + 3 * s and abs(v) <= rh / 2 + 3 * s:
            ang = ((ang + 45) % 90) - 45 if abs(rw - rh) < 2 * s else ((ang + 90) % 180) - 90
            return (x0 + rx) / s, (y0 + ry) / s, rw / s, rh / s, ang
    return None


def ajuster_par_trou(img, s, x, y, max_dep):
    """Boîtier soudé à un trait de mur (composante sombre = tout le mur) : on cherche l'intérieur BLANC du boîtier
    (région claire fermée, 3 à 40 pt, qui contient le point ou en est à ≤ max_dep), puis sa boîte + 1 pt de trait."""
    X, Y, h = int(x * s), int(y * s), int((COTE_MAX / 2 + max_dep) * s)
    x0, y0 = max(0, X - h), max(0, Y - h)
    c = img[y0:Y + h, x0:X + h]
    if c.size == 0:
        return None
    blanc = (c >= SEUIL_NOIR).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(blanc)
    ox, oy = X - x0, Y - y0
    H, W = blanc.shape
    best = None
    for j in range(1, n):
        l, t, w, hh = st[j][cv2.CC_STAT_LEFT], st[j][cv2.CC_STAT_TOP], st[j][cv2.CC_STAT_WIDTH], st[j][cv2.CC_STAT_HEIGHT]
        if l == 0 or t == 0 or l + w >= W or t + hh >= H:
            continue                                  # touche le bord du crop : ce n'est pas un intérieur fermé
        if not (3 * s <= max(w, hh) <= 40 * s):
            continue
        d = 0.0 if (l <= ox <= l + w and t <= oy <= t + hh) else math.hypot(cen[j][0] - ox, cen[j][1] - oy) / s
        if d <= max_dep and (best is None or d < best[0]):
            best = (d, l, t, w, hh)
    if best is None:
        return None
    _, l, t, w, hh = best
    marge = 1.0 * s
    cx, cy = x0 + l + w / 2, y0 + t + hh / 2
    return cx / s, cy / s, (w + 2 * marge) / s, (hh + 2 * marge) / s, 0.0


SEUIL_GABARIT = 0.32                   # corrélation minimale d'un contour de rectangle synthétique pour l'accepter


def _gabarit(w_px, h_px, ang, trait):
    """Contour de rectangle w×h tourné de `ang`, dessiné blanc sur noir (comme l'encre sur `255 - img`)."""
    diag = int(math.hypot(w_px, h_px)) + 2 * trait + 4
    g = np.zeros((diag, diag), np.uint8)
    box = cv2.boxPoints(((diag / 2, diag / 2), (w_px, h_px), ang)).astype(np.int32)
    cv2.polylines(g, [box], True, 255, trait)
    return g


def ajuster_gabarit(img, s, x, y, max_dep, tailles):
    """Boîtier soudé à un trait de mur (TEST-E201 : F, C, ANN, ⊠, accumulateur) : la composante connexe est tout le
    mur, mais le CONTOUR du boîtier reste un rectangle. On corrèle (TM_CCOEFF_NORMED) un contour synthétique
    w×h tourné de 0 à 175° (pas de 5°, puis ±4° au degré) dans une fenêtre ±max_dep autour du point, pour chaque
    taille candidate ; le meilleur score ≥ SEUIL_GABARIT, dont le centre reste à ≤ max_dep du point, gagne."""
    lim = max(hh for hh in (max(t) for t in tailles)) / 2 + max_dep + 3
    X, Y, h = int(x * s), int(y * s), int(lim * s)
    x0, y0 = max(0, X - h), max(0, Y - h)
    inv = 255 - img[y0:Y + h, x0:X + h]
    if inv.size == 0:
        return None
    trait = max(1, int(round(0.9 * s)))
    ox, oy = X - x0, Y - y0
    best = None            # (score, cx, cy, w, h, ang)

    def essai(w, hh, ang):
        nonlocal best
        g = _gabarit(w * s, hh * s, ang, trait)
        if g.shape[0] >= inv.shape[0] or g.shape[1] >= inv.shape[1]:
            return
        r = cv2.matchTemplate(inv, g, cv2.TM_CCOEFF_NORMED)
        # masque : centre du gabarit à ≤ max_dep du point d'origine
        yy, xx = np.mgrid[0:r.shape[0], 0:r.shape[1]]
        cx, cy = xx + g.shape[1] / 2, yy + g.shape[0] / 2
        r[np.hypot(cx - ox, cy - oy) > max_dep * s] = -1
        j = int(r.argmax()); py, px = divmod(j, r.shape[1])
        sc = float(r[py, px])
        if sc >= SEUIL_GABARIT and (best is None or sc > best[0]):
            best = (sc, px + g.shape[1] / 2, py + g.shape[0] / 2, w, hh, ang)

    for w, hh in tailles:
        pas_max = 90 if abs(w - hh) < 1 else 180
        for ang in range(0, pas_max, 5):
            essai(w, hh, ang)
    if best is None:
        return None
    sc, _, _, w, hh, a0 = best
    for ang in range(a0 - 4, a0 + 5):
        essai(w, hh, ang % (90 if abs(w - hh) < 1 else 180))
    sc, cx, cy, w, hh, ang = best
    ang = ((ang + 45) % 90) - 45 if abs(w - hh) < 1 else ((ang + 90) % 180) - 90
    return (x0 + cx) / s, (y0 + cy) / s, w + 1.0, hh + 1.0, float(ang), sc


def tailles_candidates(rows, label, legende_taille):
    """Tailles (w, h) en pt à essayer pour une famille : boîtes déjà ancrées de la même famille, taille du glyphe de
    légende, puis une gamme générique (carrés 5-12 pt, rectangles 2:1 de 10 à 24 pt)."""
    t = []
    for r in rows:
        if r.get("label") == label and all((r.get(k) or "").strip() for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")):
            w = float(r["x1_pt"]) - float(r["x0_pt"]); hh = float(r["y1_pt"]) - float(r["y0_pt"])
            t.append((round(max(w, hh) - 1, 1), round(min(w, hh) - 1, 1)))
    if legende_taille:
        t.append((legende_taille, legende_taille))
    t += [(c, c) for c in range(5, 13)] + [(w, w / 2) for w in range(10, 26, 2)] \
        + [(w, w / 3) for w in range(15, 33, 3)] + [(w, w / 4) for w in range(20, 37, 4)]   # accumulateur « + | − » 26×7
    out = []
    for v in t:
        if v not in out:
            out.append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("--feuille", default=None); ap.add_argument("--max-deplacement", type=float, default=8.0)
    a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    nom = load_nomenclature(work)
    path = os.path.join(work, "occurrences-visuel.csv")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    cols = list(rows[0].keys()) if rows else []
    for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt", "angle_deg", "rayon_pt"):
        if k not in cols:
            cols.append(k)
    rapport = {"ancres": 0, "deplacement_max_pt": 0.0, "non_ancres": [], "par_feuille": {}, "par_gabarit": []}
    cache = {}
    leg_taille = {}
    pleg = os.path.join(work, "legende.csv")
    if os.path.exists(pleg):
        for lr in csv.DictReader(open(pleg, encoding="utf-8")):
            if (lr.get("taille_pt") or "").strip():
                leg_taille[lr["no"]] = float(lr["taille_pt"])
    # 1er passage : cercles et composantes connexes isolées (boîtes franches) ; 2e passage : gabarit tourné pour les
    # carrés restants, qui profite des tailles des boîtes trouvées au 1er passage dans la même famille.
    restants = []
    for r in rows:
        f = r.get("feuille", "")
        if a.feuille and f != a.feuille:
            continue
        if f not in cache:
            cache[f] = _raster(work, f)
        img, s = cache[f]
        if img is None or not s:
            continue
        forme = nom.get(r["label"], {}).get("forme", CIRCLE)
        desc = (nom.get(r["label"], {}).get("description") or "").lower()
        if "rail" in desc or "lineaire" in desc or "linéaire" in desc:
            continue                                     # élément linéaire : pas de boîte, marqué par son point (R-008)
        x, y = float(r["x_pt"]), float(r["y_pt"])
        res = None
        if forme == CIRCLE:
            res = ajuster_cercle(img, s, x, y, a.max_deplacement)
            if res:
                r["x_pt"], r["y_pt"], r["rayon_pt"] = f"{res[0]:.1f}", f"{res[1]:.1f}", f"{res[2]:.1f}"
        elif forme == SQUARE:
            res = ajuster_boite(img, s, x, y, a.max_deplacement) or ajuster_par_trou(img, s, x, y, a.max_deplacement)
            if res:
                cx, cy, w, h, ang = res
                r["x_pt"], r["y_pt"] = f"{cx:.1f}", f"{cy:.1f}"
                r["x0_pt"], r["y0_pt"], r["x1_pt"], r["y1_pt"] = f"{cx - w / 2:.1f}", f"{cy - h / 2:.1f}", f"{cx + w / 2:.1f}", f"{cy + h / 2:.1f}"
                r["angle_deg"] = f"{ang:.1f}"
        if res:
            d = math.hypot(float(r["x_pt"]) - x, float(r["y_pt"]) - y)
            rapport["ancres"] += 1; rapport["deplacement_max_pt"] = max(rapport["deplacement_max_pt"], round(d, 1))
            rapport["par_feuille"].setdefault(f, 0); rapport["par_feuille"][f] += 1
        elif forme == SQUARE:
            restants.append((r, f, x, y))
        else:
            rapport["non_ancres"].append({"feuille": f, "label": r["label"], "x_pt": x, "y_pt": y})
    for r, f, x, y in restants:
        img, s = cache[f]
        leg = (nom.get(r["label"], {}).get("legende") or "").strip()
        res = ajuster_gabarit(img, s, x, y, a.max_deplacement, tailles_candidates(rows, r["label"], leg_taille.get(leg)))
        if res:
            cx, cy, w, h, ang, sc = res
            r["x_pt"], r["y_pt"] = f"{cx:.1f}", f"{cy:.1f}"
            r["x0_pt"], r["y0_pt"], r["x1_pt"], r["y1_pt"] = f"{cx - w / 2:.1f}", f"{cy - h / 2:.1f}", f"{cx + w / 2:.1f}", f"{cy + h / 2:.1f}"
            r["angle_deg"] = f"{ang:.1f}"
            d = math.hypot(cx - x, cy - y)
            rapport["ancres"] += 1; rapport["deplacement_max_pt"] = max(rapport["deplacement_max_pt"], round(d, 1))
            rapport["par_feuille"].setdefault(f, 0); rapport["par_feuille"][f] += 1
            rapport["par_gabarit"].append({"feuille": f, "label": r["label"], "x_pt": round(cx, 1), "y_pt": round(cy, 1),
                                           "w_pt": round(w, 1), "h_pt": round(h, 1), "angle_deg": round(ang, 1), "score": round(sc, 2)})
        else:
            rapport["non_ancres"].append({"feuille": f, "label": r["label"], "x_pt": x, "y_pt": y})
    for r in rows:
        for k in cols:
            r.setdefault(k, "")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    json.dump(rapport, open(os.path.join(work, "ancrage-raster.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"ancrage raster : {rapport['ancres']} pastilles ajustées (déplacement max {rapport['deplacement_max_pt']} pt, "
          f"dont {len(rapport['par_gabarit'])} par gabarit tourné), {len(rapport['non_ancres'])} non retrouvées → ancrage-raster.json")


if __name__ == "__main__":
    main()
