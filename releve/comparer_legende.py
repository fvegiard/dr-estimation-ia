# /// script
# requires-python = ">=3.12"
# dependencies = ["opencv-python-headless>=4.9", "numpy>=1.26"]
# ///
"""Contrôle de famille par la FORME : chaque occurrence est comparée (corrélation normalisée) au glyphe de SA ligne
de légende et à ceux des autres lignes de la même section. Si un autre glyphe ressemble davantage, la famille est
suspecte. Correctif du 2026-10-15 (TEST-E201) : 4 « avertisseurs 120 V » (A03, cercle 3/4 noir) étaient en fait des
« détecteurs de fumée » (A04, cercle coupé en diagonale) — tranché à tort sur un pourcentage de noir mesuré sur un
symbole de 4,6 pt traversé par un trait de mur. Une proportion de pixels ne distingue pas deux glyphes ; une
corrélation de forme, oui.

Entrées : `legende.csv` avec, pour les lignes à comparer, les colonnes `feuille_legende,x_pt,y_pt,taille_pt`
(centre et côté du glyphe sur la feuille de légende, lus sur les règles du zoom) ; `nomenclature.csv` (colonne
`legende` = numéro de ligne) ; `occurrences-visuel.csv` ; rasters de `prepare.py`.
Sortie : `comparaison-legende.json` + liste des occurrences dont un autre glyphe corrèle mieux (écart ≥ 0,08).

Usage : uv run releve/comparer_legende.py WORKDIR
"""
from __future__ import annotations
import csv, json, math, os, sys
import cv2
import numpy as np

SEUIL_ECART = 0.08     # un autre glyphe doit dépasser le glyphe attendu d'au moins cette marge pour être signalé
SEUIL_RECONNU = 0.45   # sous ce score, le glyphe attendu lui-même n'est pas reconnu : coordonnées de légende ou dessin différent, pas une confusion


def raster(work, feuille):
    img = cv2.imread(os.path.join(work, "rasters", feuille + ".png"), cv2.IMREAD_GRAYSCALE)
    rows = {r["feuille"]: r for r in csv.DictReader(open(os.path.join(work, "feuilles.csv"), encoding="utf-8"))}
    return img, img.shape[1] / float(rows[feuille]["largeur_pt"])


def crop(img, s, x, y, half):
    X, Y, h = int(round(x * s)), int(round(y * s)), int(round(half * s))
    return img[max(0, Y - h):Y + h, max(0, X - h):X + h]


def main():
    work = os.path.abspath(sys.argv[1])
    leg = [r for r in csv.DictReader(open(os.path.join(work, "legende.csv"), encoding="utf-8"))
           if (r.get("x_pt") or "").strip() and (r.get("y_pt") or "").strip()]
    if not leg:
        print("comparaison légende : aucune ligne de legende.csv n'a de coordonnées (feuille_legende,x_pt,y_pt,taille_pt) — rien à comparer")
        return
    nom = {r["label"]: r for r in csv.DictReader(open(os.path.join(work, "nomenclature.csv"), encoding="utf-8"))}
    occ = list(csv.DictReader(open(os.path.join(work, "occurrences-visuel.csv"), encoding="utf-8")))
    cache = {}
    glyphes = {}
    for r in leg:
        f = r.get("feuille_legende") or r["feuille"]
        if f not in cache:
            cache[f] = raster(work, f)
        img, s = cache[f]
        half = float(r.get("taille_pt") or 8) / 2 + 1.0
        glyphes[r["no"]] = (r.get("section", ""), r["description"], crop(img, s, float(r["x_pt"]), float(r["y_pt"]), half), half)
    rapport = {"occurrences": 0, "suspectes": [], "par_famille": {}, "sans_taille": 0}
    # Échelle par GÉOMÉTRIE, pas par corrélation (qui favorise toujours le gabarit le plus petit) : la taille du symbole
    # sur le plan vient de l'ancrage (`rayon_pt` → diamètre, ou boîte x0..y1) ; chaque glyphe de légende — l'attendu
    # comme ses concurrents — est redimensionné à CETTE taille, puis corrélé dans la fenêtre. Sans taille mesurée sur
    # l'occurrence, médiane de la famille ; sans rien, l'occurrence est sautée (comptée dans `sans_taille`).
    def taille_plan(o):
        r = (o.get("rayon_pt") or "").strip()
        if r:
            return 2 * float(r)
        bb = [(o.get(k) or "").strip() for k in ("x0_pt", "y0_pt", "x1_pt", "y1_pt")]
        if all(bb):
            return max(float(bb[2]) - float(bb[0]), float(bb[3]) - float(bb[1]))
        return None
    med = {}
    for o in occ:
        t = taille_plan(o)
        if t:
            med.setdefault(o["label"], []).append(t)
    med = {k: float(np.median(v)) for k, v in med.items()}
    for o in occ:
        no = (nom.get(o["label"], {}).get("legende") or "").strip()
        if no not in glyphes:
            continue
        t = taille_plan(o) or med.get(o["label"])
        if not t:
            rapport["sans_taille"] += 1
            continue
        f = o["feuille"]
        if f not in cache:
            cache[f] = raster(work, f)
        img, s = cache[f]
        section = glyphes[no][0]
        fen = crop(img, s, float(o["x_pt"]), float(o["y_pt"]), t / 2 + 6)
        scores = {}
        for n2, (sec2, _, g2, half2) in glyphes.items():
            if sec2 != section:
                continue
            e = (t + 2.0) / (2 * half2)           # glyphe (côté 2*half2 pt, marge comprise) → taille mesurée + trait
            gg = cv2.resize(g2, None, fx=e, fy=e, interpolation=cv2.INTER_AREA if e < 1 else cv2.INTER_CUBIC)
            if gg.shape[0] >= fen.shape[0] or gg.shape[1] >= fen.shape[1] or min(gg.shape) < 4:
                continue
            scores[n2] = float(cv2.matchTemplate(fen, gg, cv2.TM_CCOEFF_NORMED).max())
        if no not in scores:
            continue
        rapport["occurrences"] += 1
        meilleur = max(scores, key=scores.get)
        fam = rapport["par_famille"].setdefault(o["label"], {"n": 0, "score_moyen": 0.0, "suspectes": 0, "taille_plan_pt": round(t, 1)})
        fam["n"] += 1; fam["score_moyen"] += scores[no]
        if scores[no] < SEUIL_RECONNU:
            fam["non_reconnues"] = fam.get("non_reconnues", 0) + 1       # à vérifier au zoom, pas une confusion prouvée
        elif meilleur != no and scores[meilleur] - scores[no] >= SEUIL_ECART:
            fam["suspectes"] += 1
            rapport["suspectes"].append({"feuille": f, "label": o["label"], "x_pt": o["x_pt"], "y_pt": o["y_pt"],
                                         "attendu": no, "score_attendu": round(scores[no], 3),
                                         "meilleur": meilleur, "description": glyphes[meilleur][1], "score_meilleur": round(scores[meilleur], 3)})
    for fam in rapport["par_famille"].values():
        fam["score_moyen"] = round(fam["score_moyen"] / max(1, fam["n"]), 3)
    json.dump(rapport, open(os.path.join(work, "comparaison-legende.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    nr = {k: v["non_reconnues"] for k, v in rapport["par_famille"].items() if v.get("non_reconnues")}
    print(f"comparaison légende : {rapport['occurrences']} occurrences comparées, {len(rapport['suspectes'])} suspecte(s), "
          f"glyphe non reconnu : {nr or 'aucun'} → comparaison-legende.json")
    for s_ in rapport["suspectes"]:
        print(f"  {s_['label']} ({s_['x_pt']},{s_['y_pt']}) : attendu {s_['attendu']} {s_['score_attendu']} < {s_['meilleur']} « {s_['description'][:40]} » {s_['score_meilleur']}")


if __name__ == "__main__":
    main()
