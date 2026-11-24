# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Métré des parcours explicitement tracés (aucun trajet déduit entre appareils)."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pymupdf

from commun import load_feuilles, sha256

PROFIL_S1844 = Path(__file__).with_name("profils_revisions") / "s1844-e400.json"
CHAMPS = ("id", "feuille", "famille", "specification", "portee", "longueur_m", "source", "statut")


def calculer(profil: dict, page, feuille: dict):
    """Parcours de centre tracés en points PDF; contrôle sur le PDF avant le calcul."""
    if page.rotation or int(feuille["page"]) != profil["page"]:
        raise ValueError("rotation ou page de métré inattendue")
    if profil["texte_echelle"] not in page.get_text(clip=pymupdf.Rect(profil["zone_echelle"])):
        raise ValueError("échelle introuvable sur la source")
    facteur = float(profil["echelle"]) * .0254 / 72  # m/point pour le PDF à sa taille originale
    if not math.isfinite(facteur) or facteur <= 0:
        raise ValueError("échelle invalide")
    traces = {d["seqno"]: d for d in page.get_drawings() if d.get("fill") == (0, 0, 0)}
    lignes = []
    vus = set()
    for s in profil["traces"]:
        n, famille, pts = s
        d = traces.get(n)
        if n in vus or d is None or len(pts) < 2 or not (famille in profil["specifications"]):
            raise ValueError(f"tracé {n} non attesté ou dupliqué")
        vus.add(n)
        ext = pymupdf.Rect(d["rect"])
        if not all(pymupdf.Point(*xy) in ext for xy in pts):
            raise ValueError(f"tracé {n} : sommet en dehors de l'encre source")
        # Le centre (trait horizontal/vertical) doit être à l'intérieur des
        # triangles de remplissage et non seulement dans la boîte du tracé.
        triangles = [[it[1] for it in d["items"][i:i + 3]] for i in range(0, len(d["items"]), 3)]
        if any(len(t) != 3 for t in triangles) or any(it[0] != "l" for it in d["items"]):
            raise ValueError(f"tracé {n} : remplissage non reconnu")

        def sur_encre(x, y):
            for t in triangles:
                if len({(p.x, p.y) for p in t}) != 3:
                    continue
                produits = [(b.x - a.x) * (y - a.y) - (b.y - a.y) * (x - a.x)
                            for a, b in zip(t, t[1:] + t[:1])]
                if min(produits) >= -.01 or max(produits) <= .01:
                    return True
            return False

        longueur = 0.0
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            delta = math.hypot(x2 - x1, y2 - y1)
            if delta == 0 or x1 != x2 and y1 != y2:
                raise ValueError(f"tracé {n} : segment nul ou non orthogonal")
            divisions = max(1, math.ceil(delta / 2))
            if any(not sur_encre(x1 + (x2 - x1) * i / divisions, y1 + (y2 - y1) * i / divisions)
                   for i in range(divisions + 1)):
                raise ValueError(f"tracé {n} : centre hors de l'encre source")
            longueur += delta * facteur
        lignes.append({"id": f"{profil['feuille']}-{n}", "feuille": profil["feuille"], "famille": famille,
                       "specification": profil["specifications"][famille], "portee": "INSTALLER",
                       "longueur_m": round(longueur, 6), "points_pt": pts, "echelle": profil["echelle"],
                       "source": f"{feuille['fichier']} p.{profil['page']} ; pleine encre {n} ; légende {profil['feuille']}",
                       "statut": "horizontal tracé seulement"})
    return lignes


def produire(work, feuilles, out):
    """Écrit un métré même sans preuve: des réserves, pas une quantité zéro."""
    work, out = Path(work), Path(out)
    rapport = {"complet": False, "lignes": [], "reserves": ["Aucun parcours de câbles/conduits sourcé et calibré."]}
    p = work / "inventaire.json"
    if p.is_file():
        inv = json.loads(p.read_text(encoding="utf-8"))
        profil = json.loads(PROFIL_S1844.read_text(encoding="utf-8"))
        fichiers = inv.get("fichiers", [])
        if len(fichiers) == 1 and fichiers[0].get("sha256") == profil["sha256"]:
            source = Path(inv["inbox"]) / fichiers[0]["fichier"]
            f = feuilles.get(profil["feuille"])
            if not f or f.get("fichier") != fichiers[0]["fichier"] or sha256(source) != profil["sha256"]:
                raise ValueError("Métré E400 : source ou feuille incohérente")
            with pymupdf.open(source) as doc:
                rapport["lignes"] = calculer(profil, doc[profil["page"] - 1], f)
            rapport["reserves"] = profil["reserves"]
    (out / "metre-longueurs.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out / "metre-longueurs.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rapport["lignes"])
    return rapport


def lire(dossier):
    fichier = Path(dossier) / "metre-longueurs.json"
    return json.loads(fichier.read_text(encoding="utf-8")) if fichier.is_file() else None


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("work", type=Path)
    a = p.parse_args()
    r = produire(a.work, load_feuilles(a.work), a.work)
    print(f"{len(r['lignes'])} parcours sourcés, {len(r['reserves'])} réserve(s) de métrage")