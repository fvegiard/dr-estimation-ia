"""Chiffrage interne : correspondances explicites, pièces sourcées, aucun forfait par défaut.

Le catalogue historique fournit des prix d'assemblage et des heures unitaires.
Le résultat n'est pas une soumission client et ne déduit ni taux ni marge.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from src.releve.quantites import calculer as quantites, ecrire as ecrire_quantites, lire_csv

RACINE = Path(__file__).resolve().parents[2]
CATALOGUE = RACINE / "prix/dupuis/catalogue-prix-temps-dupuis.csv"
S1844 = "456eecd92a05beef45ae214d65cff804ac410d916c9891caeb9fddf94716b334"
M_PAR_PI = Decimal("0.3048")
CENT = Decimal("0.01")


def decimal(brut) -> Decimal | None:
    if brut in ("", None):
        return None
    try:
        d = Decimal(str(brut))
    except InvalidOperation as e:
        raise ValueError(f"quantité, prix ou heures illisibles : {brut!r}") from e
    if not d.is_finite() or d < 0:
        raise ValueError("quantité, prix et heures doivent être finis et non négatifs")
    return d


def formater(d, quantum=None):
    if d is None:
        return None
    return format(d.quantize(quantum, rounding=ROUND_HALF_UP) if quantum else d.normalize(), "f")


def _correspondances(p: Path):
    out = {}
    for r in lire_csv(p):
        cle = (r["label"].strip(), r["portee"].strip(), r["unite"].strip())
        if not all(cle) or cle in out or not (r.get("source_equivalence") or "").strip():
            raise ValueError("correspondance catalogue ambiguë ou sans source d'équivalence")
        out[cle] = r
    return out


def calculer(travail: Path, lignes_quantites, catalogue=CATALOGUE, correspondances=None):
    catalogue = Path(catalogue)
    p = travail / "inventaire.json"
    inv = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    if correspondances is None and [f.get("sha256") for f in inv.get("fichiers", [])] == [S1844]:
        correspondances = RACINE / "prix/dupuis/correspondances-s1844.csv"
    mapping = _correspondances(Path(correspondances)) if correspondances else {}
    articles = defaultdict(list)
    with catalogue.open(encoding="utf-8-sig", newline="") as f:
        for i, r in enumerate(csv.DictReader(f, delimiter=";"), 2):
            articles[(r["description"], r["um"])].append((i, r))
    empreinte = hashlib.sha256(catalogue.read_bytes()).hexdigest()
    postes = list(lignes_quantites["lignes"])
    longueurs = travail / "metre-longueurs.json"
    metrage = json.loads(longueurs.read_text(encoding="utf-8")) if longueurs.is_file() else {"lignes": [], "complet": False}
    longueurs_par_famille = defaultdict(list)
    for r in metrage["lignes"]:
        longueurs_par_famille[(r["feuille"], r["famille"], r["portee"])].append(r)
    for (f, lab, portee), regs in sorted(longueurs_par_famille.items()):
        postes.append({"feuille": f, "label": lab, "portee": portee, "unite": "m", "represente": len(regs),
                       "quantite": formater(sum(decimal(r["longueur_m"]) for r in regs), Decimal("0.000001")),
                       "source": [r["source"] for r in regs], "reserve": [] if metrage["complet"] else
                       ["Portion horizontale seulement; parcours complet non établi"]})
    resultat = []
    mat_sous_total, heures_sous_total = Decimal(0), Decimal(0)
    for p in postes:
        ligne = dict(p, prix_unitaire=None, heures_unitaires=None, materiel_cad=None, heures=None,
                     unite_catalogue=None, qte_catalogue=None, source_catalogue=None, source_equivalence=None)
        motif = "; ".join(p["reserve"])
        if p["portee"] == "CONSERVER" and not motif:
            ligne.update(statut="Hors achat — équipement conservé", reserve="Ne constitue pas une pose neuve")
        else:
            cle = (p["label"], p["portee"], p["unite"])
            correspondance = mapping.get(cle)
            qte = decimal(p["quantite"])
            if qte is None or qte == 0:
                motif = motif or "Quantité de travaux non établie"
            if not correspondance:
                motif = motif or "Aucune équivalence catalogue sourcée (famille, portée, unité)"
            if not motif:
                description, um = correspondance["description"], correspondance["um"]
                lignes = articles[(description, um)]
                if len(lignes) != 1:
                    motif = "Entrée catalogue absente ou non unique"
                elif (p["unite"], um) not in {("u", "U"), ("m", "P")}:
                    motif = "Unités plan/catalogue incompatibles"
                else:
                    numero, tarif = lignes[0]
                    qcat = qte / M_PAR_PI if um == "P" else qte
                    pu, hu = (decimal(tarif[c]) for c in ("prix_a_utiliser", "temps_a_utiliser"))
                    date, projet = tarif.get("date_dernier", ""), tarif.get("projet_dernier", "")
                    if not pu or not hu or not date or not projet:
                        motif = "Prix, heures positifs ou provenance du catalogue manquants; zéro non accepté par défaut"
                    else:
                        montant = (qcat * pu).quantize(CENT, rounding=ROUND_HALF_UP)
                        heures = qcat * hu
                        mat_sous_total += montant
                        heures_sous_total += heures
                        ligne.update(prix_unitaire=formater(pu), heures_unitaires=formater(hu),
                            materiel_cad=formater(montant, CENT), heures=formater(heures, Decimal("0.0001")),
                            qte_catalogue=formater(qcat, Decimal("0.000001")), unite_catalogue=um,
                            source_catalogue=f"{catalogue.name}:{numero} — {description}; {date}; {projet}",
                            source_equivalence=correspondance["source_equivalence"])
            ligne.update(statut="Non chiffrable" if motif else "Barème historique sourcé", reserve=motif)
        resultat.append(ligne)

    comptes = Counter(r["statut"] for r in resultat)
    reserves = [*lignes_quantites["reserves"], *metrage.get("reserves", []),
                "Le barème historique n'est pas une offre fournisseur courante.",
                "Taux, marge, lots fournisseurs, couverture du relevé et décision Francis non attestés."]
    return {"document": "ESTIMATION INTERNE — NE PAS SOUMETTRE", "complet": False, "devise": "CAD",
            "rendu_client_autorise": False, "prix_forfaitaire": None, "catalogue_sha256": empreinte,
            "couverture_postes": dict(comptes), "materiel_sous_total_sourcé": formater(mat_sous_total, CENT)
            if comptes["Barème historique sourcé"] else None, "heures_sous_total_sourcées":
            formater(heures_sous_total, Decimal("0.0001")) if comptes["Barème historique sourcé"] else None,
            "postes": resultat, "reserves": reserves}


def ecrire(rapport, destination: Path, nom: str):
    p = destination / f"{nom}-CHIFFRAGE-INTERNE"
    p.with_suffix(".json").write_text(json.dumps(rapport, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    champs = ("feuille", "label", "portee", "quantite", "unite", "prix_unitaire", "heures_unitaires", "materiel_cad",
              "heures", "statut", "source_catalogue", "source_equivalence", "reserve", "source")
    with p.with_suffix(".csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        w.writerows({**r, "source": " | ".join(r["source"])} for r in rapport["postes"])
    def md(s):
        return "—" if s is None else str(s).replace("|", "/").replace("\n", " ")
    texte = [f"# {nom} — {rapport['document']}", "", "Aucun prix de soumission émis.", "",
             "| Feuille | Poste | Portée | Quantité | Matériel CAD | Heures | État / source |",
             "|---|---|---|---:|---:|---:|---|"]
    for r in rapport["postes"]:
        preuve = r["source_catalogue"] or r["reserve"]
        texte.append("| " + " | ".join(map(md, (r["feuille"], r["label"], r["portee"],
            (str(r["quantite"]) + " " + r["unite"]) if r["quantite"] is not None else None, r["materiel_cad"],
            r["heures"], r["statut"] + " : " + preuve))) + " |")
    texte += ["", "Sous-totaux partiels seulement : " + md(rapport["materiel_sous_total_sourcé"]) + " $ CAD; "
              + md(rapport["heures_sous_total_sourcées"]) + " h.", "", "## Réserves",
              *[f"- {r}" for r in rapport["reserves"]]]
    p.with_suffix(".md").write_text("\n".join(texte) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("travail", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("nom")
    p.add_argument("--correspondances", type=Path)
    a = p.parse_args()
    q = quantites(a.travail)
    ecrire_quantites(q, a.destination, a.nom)
    rapport = calculer(a.travail, q, correspondances=a.correspondances)
    ecrire(rapport, a.destination, a.nom)
    print("Chiffrage interne exporté; aucune soumission client. " + str(rapport["couverture_postes"]))


if __name__ == "__main__":
    main()