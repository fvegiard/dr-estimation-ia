"""Pont relevé → format EXEMPLE (HR26-14).

Convertit le relevé écrit par le LLM dans le dossier de travail (feuilles.csv de prepare.py, nomenclature.csv,
occurrences-*.csv, reserves.md) en entrée du rendu `src.estimer.render` : un PDF des plans d'origine (une page par
feuille relevée) + estimate.json + bordereau.csv + reserves.md. Le rendu produit alors, pour chaque feuille, la page
de plan avec une pastille par symbole et son repère (I01-07), l'encadré « RELEVE <feuille> - MATERIEL », puis les
pages « BORDEREAU MATERIEL - <feuille> » (8 colonnes) et le bloc des réserves — exactement la présentation de
l'exemplaire.

Colonnes facultatives reconnues (sinon valeurs par défaut de l'exemplaire, jamais inventées) :
  nomenclature.csv  : materiel, designation, portee, modele, prescription, code
  occurrences-*.csv : portee, modele, prescription, parent, reserve
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymupdf

FAMILLES_INCENDIE = {"alarme", "securite_incendie", "secours", "incendie"}
DEFAUT_MODELE = "MODELE NON PRECISE"
DEFAUT_PORTEE = "A PRECISER"
DEFAUT_PRESCRIPTION = "Identification a revalider sur le plan"


def _csv(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


def majuscules_sans_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().upper()


def _codes(nomenclature: list[dict], utilises: set[str]) -> dict[str, str]:
    """Un code famille stable par libellé : I01… pour l'incendie, M01… pour le reste (convention de l'exemplaire)."""
    compteurs = defaultdict(int)
    out = {}
    for r in nomenclature:
        lab = r["label"]
        if lab not in utilises or lab in out:
            continue
        if r.get("code"):
            out[lab] = r["code"]
            continue
        pref = "I" if (r.get("famille") or "").lower() in FAMILLES_INCENDIE else "M"
        compteurs[pref] += 1
        out[lab] = f"{pref}{compteurs[pref]:02d}"
    return out


def construire(travail: Path, dest: Path) -> tuple[Path, int]:
    """Écrit dest/estimate.json, bordereau.csv, reserves.md et dest/plans.pdf. Retourne (plans.pdf, nb de repères)."""
    dest.mkdir(parents=True, exist_ok=True)
    feuilles = {r["feuille"]: r for r in _csv(travail / "feuilles.csv")}
    nomen = [r for r in _csv(travail / "nomenclature.csv") if r.get("label")]
    par_label = {r["label"]: r for r in nomen}
    occ = [r for f in ("occurrences-texte.csv", "occurrences-visuel.csv") for r in _csv(travail / f)
           if r.get("exclure") != "1" and r.get("label") in par_label and r.get("feuille") in feuilles]
    if not occ:
        raise ValueError("aucune occurrence valide à rendre")
    codes = _codes(nomen, {o["label"] for o in occ})

    ordre = sorted({o["feuille"] for o in occ}, key=lambda f: (feuilles[f].get("fichier", ""), int(feuilles[f].get("page") or 0), f))
    plans = pymupdf.open()
    fiches, compteurs, lignes = [], defaultdict(list), []
    for i, f in enumerate(ordre, start=1):
        src = travail / "feuilles" / f"{f}.pdf"
        with pymupdf.open(src) as d:
            plans.insert_pdf(d, from_page=0, to_page=0)
        page = plans[i - 1]
        fiches.append({"sheet": f, "page": i, "width_px": page.rect.width, "height_px": page.rect.height})
        seq = defaultdict(int)
        items = sorted((o for o in occ if o["feuille"] == f), key=lambda o: (codes[o["label"]], float(o["y_pt"]), float(o["x_pt"])))
        for n, o in enumerate(items, start=1):
            lab = o["label"]
            nr = par_label[lab]
            code = codes[lab]
            seq[code] += 1
            repere = f"{code}-{seq[code]:02d}"
            source = f"{f}-{n:03d}"
            compteurs[lab].append({"sheet": f, "page": i, "x": float(o["x_pt"]), "y": float(o["y_pt"]),
                                   "repere": repere, "code": code, "source": source})
            lignes.append({
                "feuille": f, "repere": repere, "source": source,
                "materiel": majuscules_sans_accents(nr.get("materiel") or nr.get("description") or lab),
                "designation": nr.get("designation") or lab,
                "qte": "1",
                "portee": o.get("portee") or nr.get("portee") or DEFAUT_PORTEE,
                "modele": o.get("modele") or nr.get("modele") or DEFAUT_MODELE,
                "prescription": o.get("prescription") or nr.get("prescription") or DEFAUT_PRESCRIPTION,
                "parent": o.get("parent", ""),
                "reserve": o.get("reserve", ""),
            })
    plans_pdf = dest / "plans.pdf"
    plans.save(plans_pdf, garbage=3, deflate=True)

    estimate = {"sheets": fiches, "counters": [
        {"name": majuscules_sans_accents(par_label[lab].get("materiel") or par_label[lab].get("description") or lab),
         "family": par_label[lab].get("famille", ""), "elements": els} for lab, els in compteurs.items()]}
    (dest / "estimate.json").write_text(json.dumps(estimate, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(dest / "bordereau.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lignes[0]))
        w.writeheader()
        w.writerows(lignes)
    (dest / "reserves.md").write_text(_reserves_par_feuille(travail / "reserves.md", ordre), encoding="utf-8")
    return plans_pdf, len(lignes)


def _reserves_par_feuille(p: Path, feuilles: list[str]) -> str:
    """reserves.md du LLM (liste R-001…) → sections « ## <feuille> » : une réserve qui nomme une feuille va à cette
    feuille, une réserve générale va à toutes."""
    lignes = [l.strip() for l in (p.read_text(encoding="utf-8").splitlines() if p.exists() else [])
              if re.match(r"^\s*(?:[-*]\s*|\d+[.)]\s*)?\**R-\d{3}", l)]
    out = []
    for f in feuilles:
        motif = re.compile(rf"(?<![A-Za-z0-9]){re.escape(f)}(?![A-Za-z0-9])")
        propres = [l for l in lignes if motif.search(l)]
        generales = [l for l in lignes if not any(re.search(rf"(?<![A-Za-z0-9]){re.escape(g)}(?![A-Za-z0-9])", l) for g in feuilles)]
        out.append(f"## {f}")
        out += [majuscules_sans_accents(re.sub(r"[*`]", "", l)) for l in propres + generales] or ["AUCUNE RESERVE PROPRE A CETTE FEUILLE"]
        out.append("")
    return "\n".join(out)


def rendre(travail: Path, sortie: Path, nom: str) -> dict:
    """Relevé → <nom>-RELEVE.pdf au format de l'exemplaire. Retourne le rapport du rendu."""
    import sys

    racine = Path(__file__).resolve().parents[1]
    if str(racine) not in sys.path:
        sys.path.insert(0, str(racine))
    from src.estimer.render import load_input, render

    entree = sortie / "format-exemple"
    plans_pdf, n = construire(travail, entree)
    rapport = render(load_input(entree), plans_pdf, sortie / f"{nom}-RELEVE.pdf", log=lambda *_: None)
    rapport["reperes"] = n
    (entree / "rapport-rendu.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    return rapport
