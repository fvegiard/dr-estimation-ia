# /// script
# requires-python = ">=3.12"
# dependencies = ["opencv-python-headless>=4.9", "numpy>=1.26", "pymupdf>=1.24", "scipy>=1.12"]
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

Usage : uv run releve/ancrage_raster.py WORKDIR [--feuilles F1 F2 …] [--max-deplacement 8]
(`--feuilles` : seulement les feuilles raster — dans un dossier mixte, les occurrences des feuilles vectorielles ne
sont pas touchées ; sans option, toutes les feuilles.)
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


def ajuster_glyphe(img, s, x, y, max_dep):
    """Famille à GLYPHE (S, $, DM, lettre : aucun contour circulaire) : Hough s'accroche aux arcs et coins de mur et
    éloigne la pastille du symbole (E-201 : 4 interrupteurs décalés de 2-3 pt). Ici : encre de la fenêtre moins les
    traits longs (murs), composante la plus proche du point de l'agent (2 à 14 pt), fusionnée avec ses morceaux
    contigus (≤ 1 pt) ; centre = centre de sa boîte, rayon = demi-diagonale + 0,6 pt."""
    X, Y, h = int(x * s), int(y * s), int((max_dep + 8) * s)
    x0, y0 = max(0, X - h), max(0, Y - h)
    c = img[y0:Y + h, x0:X + h]
    if c.size == 0:
        return None
    encre = (c < SEUIL_NOIR).astype(np.uint8)
    lignes = cv2.HoughLinesP(encre * 255, 1, np.pi / 180, threshold=int(8 * s), minLineLength=int(10 * s), maxLineGap=3)
    if lignes is not None:
        for l in lignes.reshape(-1, 4):
            cv2.line(encre, (int(l[0]), int(l[1])), (int(l[2]), int(l[3])), 0, max(2, int(1.2 * s)))
    n, lab, st, cen = cv2.connectedComponentsWithStats(encre)
    ox, oy = X - x0, Y - y0
    cands = []
    for j in range(1, n):
        w, hh = st[j][cv2.CC_STAT_WIDTH] / s, st[j][cv2.CC_STAT_HEIGHT] / s
        if st[j][cv2.CC_STAT_AREA] < 6 or max(w, hh) < 2 or max(w, hh) > 14:
            continue
        d = math.hypot(cen[j][0] - ox, cen[j][1] - oy) / s
        if d <= max_dep:
            cands.append((d, j))
    if not cands:
        return None
    _, j0 = min(cands)
    l, t, w, hh = st[j0][cv2.CC_STAT_LEFT], st[j0][cv2.CC_STAT_TOP], st[j0][cv2.CC_STAT_WIDTH], st[j0][cv2.CC_STAT_HEIGHT]
    bx0, by0, bx1, by1 = l, t, l + w, t + hh
    for _, j in cands:                                   # morceaux contigus du même glyphe (trait interrompu)
        if j == j0:
            continue
        L, T, W, H = st[j][cv2.CC_STAT_LEFT], st[j][cv2.CC_STAT_TOP], st[j][cv2.CC_STAT_WIDTH], st[j][cv2.CC_STAT_HEIGHT]
        m = 1.0 * s
        if L < bx1 + m and L + W > bx0 - m and T < by1 + m and T + H > by0 - m and max(W, H) / s <= 6:
            bx0, by0, bx1, by1 = min(bx0, L), min(by0, T), max(bx1, L + W), max(by1, T + H)
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    ray = max(math.hypot(bx1 - bx0, by1 - by0) / 2 / s + 0.6, 2.0)
    # mesure sur la tache du glyphe SEULEMENT (un « S » voisin ou un « 3 » d'étiquette ne compte pas) : décalage
    # centre de pastille ↔ centroïde de l'encre du glyphe, et part de cette encre dans le cercle
    sel = np.zeros_like(encre)
    for _, j in cands:
        L, T, W, H = st[j][cv2.CC_STAT_LEFT], st[j][cv2.CC_STAT_TOP], st[j][cv2.CC_STAT_WIDTH], st[j][cv2.CC_STAT_HEIGHT]
        if L >= bx0 and T >= by0 and L + W <= bx1 and T + H <= by1:
            sel[lab == j] = 1
    ys, xs = np.where(sel > 0)
    d = np.hypot(xs - cx, ys - cy) / s
    dec = math.hypot(xs.mean() - cx, ys.mean() - cy) / s if len(xs) else 2.0
    part = float((d <= ray).mean()) if len(xs) else 0.0
    return (x0 + cx) / s, (y0 + cy) / s, ray, float(min(dec, 2.0)), part


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
        # garde-fou de forme : le BORD du rectangle minimal doit être couvert d'encre (≥ 75 % de son périmètre à
        # ≤ 1,5 pt d'un pixel de la composante). Vrai pour un boîtier (même avec diagonale ou remplissage), faux pour
        # un rail courbe ou un bout de mur soudé au boîtier (E-201 : ⊠ en tête de rail → saut de 14 pt)
        dcomp = cv2.distanceTransform((lab != j).astype(np.uint8), cv2.DIST_L2, 3)
        k = 32; uu = np.linspace(-0.5, 0.5, k, endpoint=False)
        loc = np.concatenate([np.column_stack((uu * rw, np.full(k, -rh / 2))), np.column_stack((np.full(k, rw / 2), uu * rh)),
                              np.column_stack((-uu * rw, np.full(k, rh / 2))), np.column_stack((np.full(k, -rw / 2), -uu * rh))])
        ca_, sa_ = math.cos(a_), math.sin(a_)
        px_ = np.clip((rx + loc[:, 0] * ca_ - loc[:, 1] * sa_).astype(int), 0, dcomp.shape[1] - 1)
        py_ = np.clip((ry + loc[:, 0] * sa_ + loc[:, 1] * ca_).astype(int), 0, dcomp.shape[0] - 1)
        if (dcomp[py_, px_] <= 1.5 * s).mean() < 0.75:
            continue
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


SEUIL_GABARIT = 0.32
SEUIL_ECART_PT, SEUIL_COUVERTURE = 0.5, 0.75   # une pastille est « alignée » si son contour est en moyenne à ≤ 0,5 pt de l'encre
                                               # du symbole et qu'au moins 75 % du contour touche un trait (≤ 0,6 pt)                   # corrélation minimale d'un contour de rectangle synthétique pour l'accepter


def _gabarit(w_px, h_px, ang, trait):
    """Contour de rectangle w×h tourné de `ang`, dessiné blanc sur noir (comme l'encre sur `255 - img`)."""
    diag = int(math.hypot(w_px, h_px)) + 2 * trait + 4
    g = np.zeros((diag, diag), np.uint8)
    box = cv2.boxPoints(((diag / 2, diag / 2), (w_px, h_px), ang)).astype(np.int32)
    cv2.polylines(g, [box], True, 255, trait)
    return g


def ajuster_gabarit(img, s, x, y, max_dep, tailles, dist=None):
    """Boîtier soudé à un trait de mur (TEST-E201 : F, C, ANN, ⊠, accumulateur) : la composante connexe est tout le
    mur, mais le CONTOUR du boîtier reste un rectangle. On corrèle (TM_CCOEFF_NORMED) un contour synthétique
    w×h tourné de 0 à 175° (pas de 5°) dans une fenêtre ±max_dep autour du point, pour chaque taille candidate.
    Les 5 meilleures corrélations (≥ SEUIL_GABARIT, centre ≤ max_dep du point) sont ensuite AFFINÉES sur l'encre
    (`affiner`) et départagées par la MESURE (couverture − écart), jamais par la corrélation seule : une boîte 2 fois
    trop grande corrèle parfois mieux (ANN 13×7 au lieu de 7×4,5 sur E-201) mais son contour ne touche pas l'encre."""
    lim = max(hh for hh in (max(t) for t in tailles)) / 2 + max_dep + 3
    X, Y, h = int(x * s), int(y * s), int(lim * s)
    x0, y0 = max(0, X - h), max(0, Y - h)
    inv = 255 - img[y0:Y + h, x0:X + h]
    if inv.size == 0:
        return None
    trait = max(1, int(round(0.9 * s)))
    ox, oy = X - x0, Y - y0
    cands = []            # (score, cx, cy, w, h, ang)
    for w, hh in tailles:
        pas_max = 90 if abs(w - hh) < 1 else 180
        for ang in range(0, pas_max, 5):
            g = _gabarit(w * s, hh * s, ang, trait)
            if g.shape[0] >= inv.shape[0] or g.shape[1] >= inv.shape[1]:
                continue
            r = cv2.matchTemplate(inv, g, cv2.TM_CCOEFF_NORMED)
            yy, xx = np.mgrid[0:r.shape[0], 0:r.shape[1]]
            r[np.hypot(xx + g.shape[1] / 2 - ox, yy + g.shape[0] / 2 - oy) > max_dep * s] = -1
            j = int(r.argmax()); py, px = divmod(j, r.shape[1])
            sc = float(r[py, px])
            if sc >= SEUIL_GABARIT:
                cands.append((sc, px + g.shape[1] / 2, py + g.shape[0] / 2, w, hh, ang))
    if not cands:
        return None
    cands.sort(reverse=True)
    if dist is None:
        dist = _dist(img)
    best = None           # (qualité, cx, cy, w, h, ang, score)
    for sc, cx, cy, w, hh, ang in cands[:5]:
        ang = ((ang + 45) % 90) - 45 if abs(w - hh) < 1 else ((ang + 90) % 180) - 90
        p = affiner(dist, s, "boite", ((x0 + cx) / s, (y0 + cy) / s, w, hh, float(ang)))
        e_, c_ = mesurer(dist, s, "boite", p)
        q = c_ - e_
        if best is None or q > best[0]:
            best = (q, *p, sc)
    _, cx, cy, w, hh, ang, sc = best
    return cx, cy, w, hh, float(ang), sc


def _dist(img, seuil=128):
    """Carte de distance (px) à l'encre : 0 sur un trait, croissante en s'en éloignant."""
    encre = (img < seuil).astype(np.uint8)
    return cv2.distanceTransform(1 - encre, cv2.DIST_L2, 3)


def _contour(kind, p, n=96):
    """Points (pt) du contour de la pastille : cercle (cx, cy, r) ou rectangle (cx, cy, w, h, ang)."""
    if kind == "cercle":
        cx, cy, r = p; t = np.linspace(0, 2 * math.pi, n, endpoint=False)
        return np.column_stack((cx + r * np.cos(t), cy + r * np.sin(t)))
    cx, cy, w, h, ang = p; a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    k = n // 4; u = np.linspace(-0.5, 0.5, k, endpoint=False)
    loc = np.concatenate([np.column_stack((u * w, np.full(k, -h / 2))), np.column_stack((np.full(k, w / 2), u * h)),
                          np.column_stack((-u * w, np.full(k, h / 2))), np.column_stack((np.full(k, -w / 2), -u * h))])
    return np.column_stack((cx + loc[:, 0] * ca - loc[:, 1] * sa, cy + loc[:, 0] * sa + loc[:, 1] * ca))


def mesurer(dist, s, kind, p, tol=0.6):
    """Écart moyen contour → encre (pt, tronqué à 2 pt) et couverture = part du contour à ≤ tol pt d'un trait."""
    pts = _contour(kind, p) * s
    H, W = dist.shape
    xs = np.clip(pts[:, 0], 0, W - 1).astype(int); ys = np.clip(pts[:, 1], 0, H - 1).astype(int)
    d = dist[ys, xs] / s
    return float(np.minimum(d, 2.0).mean()), float((d <= tol).mean())


def mesurer_englobant(img, s, cx, cy, r, seuil=128):
    """Glyphe (S, $, DM, lettre) : la pastille ne suit pas un contour, elle ENGLOBE un dessin. Mesure : décalage (pt)
    entre le centre de la pastille et le centre de l'encre qu'elle contient (fenêtre r + 1,5 pt), et part de cette
    encre à l'intérieur du cercle. Aligné si décalage ≤ 1 pt et ≥ 90 % de l'encre dedans."""
    X, Y, h = int(cx * s), int(cy * s), int((r + 1.5) * s)
    c = img[max(0, Y - h):Y + h, max(0, X - h):X + h]
    encre = (c < seuil).astype(np.uint8)
    # un interrupteur est posé sur un mur : on retire les traits LONGS (≥ 2 r) qui traversent la fenêtre, pour ne
    # mesurer que le glyphe lui-même (HoughLinesP, lignes effacées sur 1,5 pt d'épaisseur)
    lignes = cv2.HoughLinesP(encre * 255, 1, np.pi / 180, threshold=int(1.5 * r * s), minLineLength=int(2 * r * s), maxLineGap=3)
    if lignes is not None:
        for l in lignes.reshape(-1, 4):
            cv2.line(encre, (int(l[0]), int(l[1])), (int(l[2]), int(l[3])), 0, max(2, int(1.5 * s)))
    ys, xs = np.where(encre > 0)
    if len(xs) < 5:
        return None
    ox, oy = X - max(0, X - h), Y - max(0, Y - h)
    d = np.hypot(xs - ox, ys - oy) / s
    dedans = d <= r
    if dedans.sum() < 5:
        return 2.0, 0.0
    dec = math.hypot(xs[dedans].mean() - ox, ys[dedans].mean() - oy) / s
    return float(min(dec, 2.0)), float(dedans.mean())


def affiner(dist, s, kind, p0):
    """Optimisation continue (Nelder-Mead) de la pastille sur l'encre : position ±2 pt, angle ±8°, taille ±20 %.
    Ce n'est plus un pas de 5° ni une taille de catalogue : c'est le contour qui épouse le symbole, mesuré."""
    from scipy.optimize import minimize
    p0 = np.array(p0, dtype=float)
    lo = p0.copy(); hi = p0.copy()
    lo[:2] -= 2.0; hi[:2] += 2.0
    if kind == "cercle":
        lo[2] *= 0.8; hi[2] *= 1.2
    else:
        lo[2:4] *= 0.8; hi[2:4] *= 1.2; lo[4] -= 8; hi[4] += 8

    def f(p):
        pen = float(np.sum(np.maximum(0, lo - p) ** 2 + np.maximum(0, p - hi) ** 2))
        return mesurer(dist, s, kind, p)[0] + pen
    r = minimize(f, p0, method="Nelder-Mead", options={"xatol": 0.05, "fatol": 1e-3, "maxiter": 400})
    p = np.clip(r.x, lo, hi)
    return p if f(p) <= f(p0) else p0


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


def poser_boite(r, dist, s, res):
    """Affine (cx, cy, w, h, ang) sur l'encre, mesure l'écart, écrit la boîte (+1 pt de marge) dans la ligne."""
    cx, cy, w, h, ang = affiner(dist, s, "boite", res)
    e_, c_ = mesurer(dist, s, "boite", (cx, cy, w, h, ang))
    w, h = w + 1.0, h + 1.0
    r["x_pt"], r["y_pt"] = f"{cx:.1f}", f"{cy:.1f}"
    r["x0_pt"], r["y0_pt"], r["x1_pt"], r["y1_pt"] = f"{cx - w / 2:.1f}", f"{cy - h / 2:.1f}", f"{cx + w / 2:.1f}", f"{cy + h / 2:.1f}"
    r["angle_deg"] = f"{ang:.1f}"; r["ecart_pt"], r["couverture"], r["mesure"] = f"{e_:.2f}", f"{c_:.2f}", "contour"
    return cx, cy, w, h, ang


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("--feuille", default=None, help="une seule feuille")
    ap.add_argument("--feuilles", nargs="+", default=None, help="feuilles RASTER à traiter (run.py : `feuilles_raster()`) — les autres lignes sont laissées intactes")
    ap.add_argument("--max-deplacement", type=float, default=8.0)
    a = ap.parse_args()
    work = os.path.abspath(a.workdir)
    nom = load_nomenclature(work)
    path = os.path.join(work, "occurrences-visuel.csv")
    with open(path, encoding="utf-8") as fh:
        lecteur = csv.DictReader(fh)
        rows = list(lecteur)
        cols = list(lecteur.fieldnames or [])        # schéma conservé même sans occurrence (revue Codex PR #25)
    feuilles = set(a.feuilles or ([a.feuille] if a.feuille else []))
    for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt", "angle_deg", "rayon_pt", "x_agent_pt", "y_agent_pt", "ecart_pt", "couverture", "mesure"):
        if k not in cols:
            cols.append(k)
    # Idempotence : le point de départ est TOUJOURS celui de l'agent (`x_agent_pt`, copié au 1er passage), jamais le
    # centre déjà recalé — sinon un 2e passage re-cherche autour du résultat et peut sauter sur un voisin (E-201 : ANN
    # réduit à une boîte de 4 pt au 2e passage).
    for r in rows:
        if not (r.get("x_agent_pt") or "").strip():
            r["x_agent_pt"], r["y_agent_pt"] = r["x_pt"], r["y_pt"]
    rapport = {"ancres": 0, "deplacement_max_pt": 0.0, "non_ancres": [], "par_feuille": {}, "par_gabarit": []}
    cache = {}
    leg_taille, leg_symbole = {}, {}
    pleg = os.path.join(work, "legende.csv")
    if os.path.exists(pleg):
        for lr in csv.DictReader(open(pleg, encoding="utf-8")):
            if (lr.get("taille_pt") or "").strip():
                leg_taille[lr["no"]] = float(lr["taille_pt"])
            leg_symbole[lr["no"]] = (lr.get("symbole") or "").strip().lower()

    def est_glyphe(label):
        """Cercle ou glyphe ? Le dessin de la ligne de légende tranche (« cercle … » = contour ; « $ », « ovale DM »,
        « S » = glyphe) ; hors légende, la description de la nomenclature."""
        n_ = nom.get(label, {})
        sym = leg_symbole.get((n_.get("legende") or "").strip()) or (n_.get("description") or "").lower()
        return not sym.startswith("cercle")
    # 1er passage : cercles et composantes connexes isolées (boîtes franches) ; 2e passage : gabarit tourné pour les
    # carrés restants, qui profite des tailles des boîtes trouvées au 1er passage dans la même famille.
    restants = []
    dists, dists_gris = {}, {}
    for r in rows:
        f = r.get("feuille", "")
        if feuilles and f not in feuilles:
            continue                                     # feuille vectorielle : ancrage.py (vectoriel) s'en charge, pas ici
        if f not in cache:
            cache[f] = _raster(work, f)
        img, s = cache[f]
        if img is None or not s:
            continue
        forme = nom.get(r["label"], {}).get("forme", CIRCLE)
        desc = (nom.get(r["label"], {}).get("description") or "").lower()
        if desc.lstrip().startswith("rail") or "lineaire" in desc or "linéaire" in desc:
            continue                                     # élément linéaire : pas de boîte, marqué par son point (R-008)
            # (« carré X en tête de rail » n'est PAS un rail : seul un libellé qui COMMENCE par « rail » est linéaire)
        x, y = float(r["x_agent_pt"]), float(r["y_agent_pt"])
        r["x_pt"], r["y_pt"] = r["x_agent_pt"], r["y_agent_pt"]
        for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt", "angle_deg", "rayon_pt", "ecart_pt", "couverture", "mesure"):
            r[k] = ""
        res = None
        if f not in dists:
            dists[f] = _dist(img)
        if forme == CIRCLE and est_glyphe(r["label"]):
            res = ajuster_glyphe(img, s, x, y, a.max_deplacement)
            if res:
                cx, cy, ray, e_, c_ = res
                r["x_pt"], r["y_pt"], r["rayon_pt"] = f"{cx:.1f}", f"{cy:.1f}", f"{ray:.1f}"
                r["ecart_pt"], r["couverture"], r["mesure"] = f"{e_:.2f}", f"{c_:.2f}", "englobant"
        elif forme == CIRCLE:
            res = ajuster_cercle(img, s, x, y, a.max_deplacement)
            if res:
                e0, c0 = mesurer(dists[f], s, "cercle", (res[0], res[1], res[2] - 0.4))
                if c0 < 0.5:                                 # trait gris pâle (existant) : Hough sur l'image seuillée à 200
                    if f not in dists_gris:
                        dists_gris[f] = _dist(img, 200)
                    gris = np.where(img < 200, 0, 255).astype(np.uint8)
                    res2 = ajuster_cercle(gris, s, x, y, a.max_deplacement)
                    if res2:
                        cx, cy, ray = affiner(dists_gris[f], s, "cercle", (res2[0], res2[1], res2[2] - 0.4))
                        r["x_pt"], r["y_pt"], r["rayon_pt"] = f"{cx:.1f}", f"{cy:.1f}", f"{ray + 0.4:.1f}"
                        e_, c_ = mesurer(dists_gris[f], s, "cercle", (cx, cy, ray))
                        r["ecart_pt"], r["couverture"], r["mesure"] = f"{e_:.2f}", f"{c_:.2f}", "contour gris"
                        continue_ = True
                    else:
                        continue_ = False
                else:
                    continue_ = False
            if res and not continue_:
                cx, cy, ray = affiner(dists[f], s, "cercle", (res[0], res[1], res[2] - 0.4))
                r["x_pt"], r["y_pt"], r["rayon_pt"] = f"{cx:.1f}", f"{cy:.1f}", f"{ray + 0.4:.1f}"
                e_, c_ = mesurer(dists[f], s, "cercle", (cx, cy, ray)); r["mesure"] = "contour"
                if c_ < 0.5:                                   # pas un contour : glyphe (S, $, DM) ou trait gris pâle
                    if f not in dists_gris:
                        dists_gris[f] = _dist(img, 200)
                    e2, c2 = mesurer(dists_gris[f], s, "cercle", (cx, cy, ray))
                    if c2 >= 0.75:
                        e_, c_, r["mesure"] = e2, c2, "contour gris"
                    else:
                        m = mesurer_englobant(img, s, cx, cy, ray + 0.4)
                        if m:
                            e_, c_, r["mesure"] = m[0], m[1], "englobant"
                r["ecart_pt"], r["couverture"] = f"{e_:.2f}", f"{c_:.2f}"
        elif forme == SQUARE:
            res = ajuster_boite(img, s, x, y, a.max_deplacement) or ajuster_par_trou(img, s, x, y, a.max_deplacement)
            if res:
                poser_boite(r, dists[f], s, res)
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
        res = ajuster_gabarit(img, s, x, y, a.max_deplacement, tailles_candidates(rows, r["label"], leg_taille.get(leg)), dists[f])
        if res:
            cx, cy, w, h, ang, sc = res
            cx, cy, w, h, ang = poser_boite(r, dists[f], s, (cx, cy, w, h, ang))
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
    al = [r for r in rows if (r.get("ecart_pt") or "").strip()]
    def hors(r):
        if r.get("mesure") == "englobant":
            return float(r["ecart_pt"]) > 1.0 or float(r["couverture"]) < 0.9
        return float(r["ecart_pt"]) > SEUIL_ECART_PT or float(r["couverture"]) < SEUIL_COUVERTURE
    mal = [r for r in al if hors(r)]
    rapport["alignement"] = {"mesures": len(al), "seuil_ecart_pt": SEUIL_ECART_PT, "seuil_couverture": SEUIL_COUVERTURE,
                             "ecart_moyen_pt": round(float(np.mean([float(r["ecart_pt"]) for r in al])), 2) if al else None,
                             "par_mesure": {m: sum(1 for r in al if r.get("mesure") == m) for m in ("contour", "contour gris", "englobant")},
                             "hors_seuil": [{"feuille": r["feuille"], "label": r["label"], "x_pt": r["x_pt"], "y_pt": r["y_pt"],
                                             "mesure": r.get("mesure"), "ecart_pt": r["ecart_pt"], "couverture": r["couverture"]} for r in mal]}
    json.dump(rapport, open(os.path.join(work, "ancrage-raster.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"alignement empirique : {len(al)} pastilles mesurées, écart moyen {rapport['alignement']['ecart_moyen_pt']} pt, "
          f"{len(mal)} hors seuil (écart > {SEUIL_ECART_PT} pt ou couverture < {SEUIL_COUVERTURE})")
    print(f"ancrage raster : {rapport['ancres']} pastilles ajustées (déplacement max {rapport['deplacement_max_pt']} pt, "
          f"dont {len(rapport['par_gabarit'])} par gabarit tourné), {len(rapport['non_ancres'])} non retrouvées → ancrage-raster.json")


if __name__ == "__main__":
    main()
