"""Quantités par portée : un repère physique reste distinct du facteur documenté."""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ZONES = ("x0_pt", "y0_pt", "x1_pt", "y1_pt")
COLONNES = ("feuille", "label", "portee", "unite", "represente", "quantite", "source", "reserve")
TYPIQUE = re.compile(r"\b(?:LOGEMENTS?|CHAMBRES?|UNITÉS?|SALLES?)\s+TYP(?:E|ES|IQUE|IQUES)\b", re.I)
PORTEE_INCONNUE = "À PRÉCISER"


def lire_csv(p: Path):
    if not p.is_file():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def lire_regles(travail: Path):
    regles = []
    for i, r in enumerate(lire_csv(travail / "multiplicateurs.csv"), 2):
        prefixe = f"multiplicateurs.csv:{i}"
        try:
            f = float(r.get("facteur") or "")
            valeurs = [(r.get(k) or "").strip() for k in ZONES]
            if any(valeurs) and not all(valeurs):
                raise ValueError("zone partielle")
            zone = tuple(float(x) for x in valeurs) if all(valeurs) else None
        except ValueError as e:
            raise ValueError(f"{prefixe} facteur ou zone illisible ({e})") from e
        if not math.isfinite(f) or f < 1 or not f.is_integer():
            raise ValueError(f"{prefixe} facteur non entier ou inférieur à 1")
        if zone and (not all(math.isfinite(x) for x in zone) or zone[0] == zone[2] or zone[1] == zone[3]):
            raise ValueError(f"{prefixe} zone vide ou non finie")
        feuille, source = (r.get(k, "").strip() for k in ("feuille", "source"))
        regles.append({"feuille": feuille, "facteur": f, "zone": zone, "source": source, "_ligne": i})
    return regles


def regle_de(regles, feuille, x, y):
    applicables = []
    for r in regles:
        if r["feuille"] != feuille:
            continue
        if r["zone"] is None:
            applicables.append((float("inf"), r))
            continue
        x0, y0, x1, y1 = r["zone"]
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            applicables.append((abs((x1 - x0) * (y1 - y0)), r))
    if not applicables:
        return None
    plus_petite = min(aire for aire, _ in applicables)
    resultats = [r for aire, r in applicables if aire == plus_petite]
    if any(r["facteur"] != resultats[0]["facteur"] for r in resultats):
        raise ValueError(f"{feuille} ({x:g}, {y:g}) : multiplicateurs concurrents de même priorité")
    return resultats[0]


def facteur_de(regles, feuille, x, y):
    r = regle_de(regles, feuille, x, y)
    return r["facteur"] if r else 1.0


def calculer(travail: Path):
    fe = {r["feuille"]: r for r in lire_csv(travail / "feuilles.csv")}
    cl = {r["feuille"]: r for r in lire_csv(travail / "feuilles-classement.csv") if r.get("type") == "plan"}
    nomenclature = {r["label"]: r for r in lire_csv(travail / "nomenclature.csv")}
    regles = lire_regles(travail)
    for r in regles:
        if not r["source"] or r["feuille"] not in cl:
            raise ValueError(f"multiplicateurs.csv:{r['_ligne']} source ou feuille plan non renseignée")
    reserves = [f"{f} : unité type détectée sans multiplicateur sourcé; total non établi" for f, r in cl.items()
                if TYPIQUE.search(r.get("note") or fe.get(f, {}).get("titre") or "") and
                not any(a["feuille"] == f for a in regles)]
    types_non_traites = {r.split(" :", 1)[0] for r in reserves}
    postes = {}
    vus = {}
    for nom in ("occurrences-texte.csv", "occurrences-visuel.csv"):
        for o in lire_csv(travail / nom):
            f, lab = o.get("feuille", ""), o.get("label", "")
            if f not in cl or (o.get("exclure") or "").strip().lower() in {"1", "oui", "x", "true"}:
                continue
            n = nomenclature.get(lab)
            if not n:
                raise ValueError(f"{f} : libellé {lab!r} absent de la nomenclature")
            x, y = float(o["x_pt"]), float(o["y_pt"])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError(f"{f} : coordonnées de {lab!r} non finies")
            portee = ((o.get("portee") or "").strip() or (n.get("portee") or "").strip() or PORTEE_INCONNUE).upper()
            if portee == "A PRECISER":
                portee = PORTEE_INCONNUE
            r = regle_de(regles, f, x, y)
            qte = float(o.get("qte") or "1")
            if not math.isfinite(qte) or qte < 1 or not qte.is_integer():
                raise ValueError(f"{f} ({x:g}, {y:g}) : quantité unitaire invalide")
            qte_source = (o.get("source_qte") or "").strip()
            if qte != 1 and not qte_source:
                raise ValueError(f"{f} ({x:g}, {y:g}) : quantité supérieure à 1 sans source_qte")
            source = fe.get(f, {})
            loc = f"{source.get('fichier', '')} p.{source.get('page', '?')}, {f} ({x:g}, {y:g})".strip()
            signature = (f, lab, round(x, 1), round(y, 1))
            unique = (portee, qte)
            if signature in vus:
                if vus[signature] != unique:
                    raise ValueError(f"{loc} : repère dupliqué avec portée ou quantité contradictoire")
                continue
            vus[signature] = unique
            reserve = (o.get("reserve") or "").strip()
            p = postes.setdefault((f, lab, portee), {"feuille": f, "label": lab, "portee": portee,
                   "unite": "u", "represente": 0, "quantite": 0, "source": [], "reserve": []})
            p["represente"] += 1
            if f in types_non_traites or portee == PORTEE_INCONNUE:
                p["quantite"] = None
            elif p["quantite"] is not None:
                p["quantite"] += int(qte * (r["facteur"] if r else 1))
            p["source"].append(loc + (f" ; ×{r['facteur']:g} ({r['source']})" if r else "") +
                               (f" ; {qte_source}" if qte_source else ""))
            if reserve and reserve not in p["reserve"]:
                p["reserve"].append(reserve)
            if portee == PORTEE_INCONNUE and "Portée de travaux non établie" not in p["reserve"]:
                p["reserve"].append("Portée de travaux non établie")
            if f in types_non_traites and "multiplicateur inconnu" not in p["reserve"]:
                p["reserve"].append("multiplicateur inconnu")
    return {"lignes": [postes[k] for k in sorted(postes)], "reserves": reserves}


def ecrire(resultat, destination: Path, nom: str):
    destination.mkdir(parents=True, exist_ok=True)
    p = destination / f"{nom}-QUANTITES.json"
    p.write_text(json.dumps(resultat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (destination / f"{nom}-QUANTITES.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES)
        w.writeheader()
        for r in resultat["lignes"]:
            w.writerow({**r, "source": " | ".join(r["source"]), "reserve": "; ".join(r["reserve"])})
    return p


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("travail", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("nom")
    a = p.parse_args()
    ecrire(calculer(a.travail), a.destination, a.nom)


if __name__ == "__main__":
    main()