"""
Classification des désaccords du comparateur `compare_qpl` en classes —
critère d'acceptation étape 4 (CLAUDE.md) : « Classer chaque désaccord :
omission, doublon, mauvaise famille, mauvaise portée, mauvais rattachement de
feuille. Un compte global ne suffit pas. »

CLI (mêmes arguments que `src.validation.compare_qpl`) :
  python -m src.validation.classer_ecarts --humain A.qpl --ia B.qpl \
      --dims png-dimensions.txt --feuilles feuilles.csv --sortie DIR

Sorties dans DIR — CONTRAT PARTAGÉ (producteur ici ; `justifier.py` est le
consommateur, le format est gelé) :
- `ecarts-classes.csv` : en-tête EXACT
  `classe,feuille_humaine,feuille_ia,libelle_humain,libelle_ia,position_humaine,position_ia,detail`
  `classe` ∈ {omission, en_trop, doublon, mauvaise_famille, mauvaise_portee,
  mauvais_rattachement_feuille} (snake_case, sans accents) ; positions au
  format `x:y` en pixels IA (position humaine = recalée dans le repère IA),
  vide si inconnue ; UTF-8 ; une valeur contenant une virgule est citée
  ( quoting CSV standard). La ligne de l'omission garde `feuille_ia` vide
  quand la page humaine elle-même n'a pas pu être appariée.
- `ecarts-classes.md` : compte par classe + liste individuelle de chaque écart,
  jamais le compte seul.

Classes et règles (tout est calculé depuis `compare_qpl.comparer()`, seuil
d'appariement des marques = `compare_qpl.SEUIL_MARQUE`, soit 1,2 % de la
diagonale du raster IA — rien n'est saisi à la main) :

- `omission` : marque humaine sans marque IA appariée (manquante sur une
  feuille appariée, ou marque d'une page humaine non appariée).
- `en_trop` : marque IA sans marque humaine appariée — SAUF si elle est à
  moins de 1,2 % de la diagonale d'une marque humaine déjà appariée à une
  autre marque IA : c'est alors un `doublon` (deux marques IA pour la même
  marque humaine = l'IA a compté deux fois le même appareil).
- `mauvaise_famille` : couple apparié dont les libellés sont classés dans deux
  catégories différentes par `src.qpl.categorie.categoriser`. Jamais tranché
  si une des deux catégories est `indetermine` : sans catégorie reconnaissable
  d'un côté, on ne peut pas affirmer que la famille diverge — l'écart resterait
  injustifiable sur le plan.
- `mauvaise_portee` : couple apparié dont les libellés divergent sur la portée
  des travaux — heuristique lexicalisée, documentée ici : côté « existant »,
  un mot EX / EXIST* / CONSERV* / REUTILIS* ; côté « neuf », NEUF / NEW / N F
  (« n.f » sans point) / NF / FOURNI* / INSTALL*. Flag seulement quand une
  portée est affirmée de chaque côté de manière opposée (existant vs neuf) ;
  une seule portée affirmée ou aucune → pas de flag (les préfixes d'addenda
  « ADD » ne sont pas traités comme « neuf » : ils marquent le document, pas
  la portée du poste).
- `mauvais_rattachement_feuille` : page humaine marquée que la géométrie a
  recalée sur une AUTRE feuille IA que celle que son nom désignait
  (`compare_qpl` a contredit l'appariement par nom). Les pages sans marques
  et les appariements par nom conservés malgré un recalage faible ne sont pas
  des rattachements fautifs.

Un même couple peut produire plusieurs écarts (mauvaise_famille ET
mauvaise_portee sont deux faits distincts à justifier séparément sur le plan).
La liste produite est triée de façon déterministe (classe, feuilles, libellés,
positions) pour que le fichier soit diff-able.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from src.qpl.categorie import INDETERMINE, categoriser, nettoyer
from src.validation import compare_qpl as cq

EN_TETE_CSV = [
    "classe", "feuille_humaine", "feuille_ia", "libelle_humain",
    "libelle_ia", "position_humaine", "position_ia", "detail",
]

CLASSES = (
    "omission", "en_trop", "doublon", "mauvaise_famille",
    "mauvaise_portee", "mauvais_rattachement_feuille",
)

# Seuil de doublon = seuil d'appariement des marques de compare_qpl (1,2 % de
# la diagonale du raster IA) — une seule source de vérité, jamais recopiée.
SEUIL_DOUBLON = cq.SEUIL_MARQUE

_PCT_FR = (f"{100 * cq.SEUIL_MARQUE:.1f}").replace(".", ",") + " %"


@dataclass
class EcartClasse:
    """Un désaccord classé. Champs nommés exactement selon le contrat CSV."""
    classe: str
    feuille_humaine: str = ""
    feuille_ia: str = ""
    libelle_humain: str = ""
    libelle_ia: str = ""
    position_humaine: str = ""
    position_ia: str = ""
    detail: str = ""


# --- Heuristique de portée ---------------------------------------------------

# Portée « existant » : EX seul, ou préfixes EXIST*/CONSERV*/REUTILIS*.
# « EX » ancré exactement pour ne pas capturer « EXIT » (panneau de sortie) ;
# inflexions par préfixe (EXISTANTE, CONSERVÉ, CONSERVATION, REUTILISÉ…).
RE_EXISTANT = re.compile(r"^EX$|^EXIST|^CONSERV|^REUTILIS")
# Portée « neuf » : NEUF/New, « N F » (« n.f ») ou NF, FOURNI*, INSTALL*.
RE_NEUF = re.compile(r"^NEUF|^NEW$|^NF$|^FOURN|^INSTALL")


def _tokens_portee(libelle: str) -> list[str]:
    return nettoyer(libelle).split()


def portee(libelle: str) -> str | None:
    """Portée d'un libellé : « existant », « neuf », ou None si rien n'est
    affirmé. « N.F » (point) devient le bigramme « N F » après nettoyage."""
    tokens = _tokens_portee(libelle)
    for mot in tokens:
        if RE_EXISTANT.match(mot):
            return "existant"
    for mot in tokens:
        if RE_NEUF.match(mot):
            return "neuf"
    for a, b in zip(tokens, tokens[1:]):
        if a == "N" and b == "F":
            return "neuf"
    return None


def portees_divergentes(libelle_humain: str, libelle_ia: str) -> bool:
    """Vrai si les deux libellés affirment des portées opposées."""
    return {portee(libelle_humain), portee(libelle_ia)} == {"existant", "neuf"}


# --- Classification ------------------------------------------------------------

def _pos(x: float | None, y: float | None) -> str:
    return "" if x is None or y is None else f"{x:.0f}:{y:.0f}"


def _couple_le_plus_proche(marque: cq.Marque, couples: list[cq.Couple]
                           ) -> tuple[cq.Couple | None, float]:
    meilleur, d_min = None, math.inf
    for c in couples:
        if c.humain.x_ia is None:
            continue
        d = math.hypot(marque.x - c.humain.x_ia, marque.y - c.humain.y_ia)
        if d < d_min:
            meilleur, d_min = c, d
    return meilleur, d_min


def classer(comp: cq.Comparaison) -> list[EcartClasse]:
    """Classe chaque désaccord de la comparaison en une des classes de
    CLAUDE.md (liste triée, déterministe — voir docstring du module)."""
    ecarts: list[EcartClasse] = []
    ia_par_feuille = comp.ia_par_feuille()
    res = comp.resultats[cq.SEUIL_MARQUE]

    for feuille, r in res.items():
        ia = ia_par_feuille[feuille]
        seuil_px = SEUIL_DOUBLON * ia.diagonale
        # Omissions : marques humaines sans paire IA.
        for h in r.manquantes:
            ecarts.append(EcartClasse(
                classe="omission", feuille_humaine=h.marque.plan, feuille_ia=feuille,
                libelle_humain=h.marque.libelle, libelle_ia="",
                position_humaine=_pos(h.x_ia, h.y_ia), position_ia="",
                detail=(f"marque humaine « {h.marque.libelle} » de la page "
                        f"« {h.marque.plan} » sans marque IA appariée "
                        f"(seuil {_PCT_FR} de la diagonale de {feuille})")))
        # IA seule : doublon si une autre marque IA est déjà appariée à la
        # même marque humaine à moins du seuil, sinon en trop.
        for m in r.en_trop:
            couple, d = _couple_le_plus_proche(m, r.couples)
            if couple is not None and d <= seuil_px:
                ecarts.append(EcartClasse(
                    classe="doublon", feuille_humaine=couple.humain.marque.plan,
                    feuille_ia=feuille, libelle_humain=couple.humain.marque.libelle,
                    libelle_ia=m.libelle,
                    position_humaine=_pos(couple.humain.x_ia, couple.humain.y_ia),
                    position_ia=_pos(m.x, m.y),
                    detail=(f"deux marques IA à moins de {_PCT_FR} de la diagonale "
                            f"de la même marque humaine « {couple.humain.marque.libelle} » : "
                            f"cette marque IA et « {couple.ia.libelle} » (appariée) — "
                            f"l'IA a compté deux fois le même appareil")))
            else:
                ecarts.append(EcartClasse(
                    classe="en_trop", feuille_humaine="", feuille_ia=feuille,
                    libelle_humain="", libelle_ia=m.libelle,
                    position_humaine="", position_ia=_pos(m.x, m.y),
                    detail=f"marque IA « {m.libelle} » sans marque humaine appariée "
                           f"(seuil {_PCT_FR} de la diagonale de {feuille})"))
        # Couples appariés : famille (categoriser) et portée (heuristique).
        for c in r.couples:
            cat_h = categoriser(c.humain.marque.libelle).categorie
            cat_i = categoriser(c.ia.libelle).categorie
            if INDETERMINE not in (cat_h, cat_i) and cat_h != cat_i:
                ecarts.append(EcartClasse(
                    classe="mauvaise_famille", feuille_humaine=c.humain.marque.plan,
                    feuille_ia=feuille, libelle_humain=c.humain.marque.libelle,
                    libelle_ia=c.ia.libelle,
                    position_humaine=_pos(c.humain.x_ia, c.humain.y_ia),
                    position_ia=_pos(c.ia.x, c.ia.y),
                    detail=(f"même position, famille divergente : « {c.humain.marque.libelle} » "
                            f"= {cat_h} (humain) ≠ {cat_i} (IA, « {c.ia.libelle} ») — "
                            "src.qpl.categorie.categoriser")))
            if portees_divergentes(c.humain.marque.libelle, c.ia.libelle):
                ecarts.append(EcartClasse(
                    classe="mauvaise_portee", feuille_humaine=c.humain.marque.plan,
                    feuille_ia=feuille, libelle_humain=c.humain.marque.libelle,
                    libelle_ia=c.ia.libelle,
                    position_humaine=_pos(c.humain.x_ia, c.humain.y_ia),
                    position_ia=_pos(c.ia.x, c.ia.y),
                    detail=(f"même position, portée divergente : "
                            f"« {c.humain.marque.libelle} » = {portee(c.humain.marque.libelle)} "
                            f"vs « {c.ia.libelle} » = {portee(c.ia.libelle)} "
                            "(heuristique existant|ex|conserv vs neuf|n.f|fourni|install)")))

    # Marques humaines sur des pages elles-mêmes non appariées : omissions
    # sans feuille IA connue (le rattachement de la page est en question).
    for m in comp.manquantes_hors_page:
        ecarts.append(EcartClasse(
            classe="omission", feuille_humaine=m.plan, feuille_ia="",
            libelle_humain=m.libelle, libelle_ia="",
            position_humaine="", position_ia="",
            detail=(f"marque humaine « {m.libelle} » sur la page « {m.plan} », "
                    "page non appariée à une feuille IA")))
    # Feuilles IA sans page humaine : marques en trop sans page du tout.
    for feuille, marques in comp.en_trop_hors_page.items():
        for m in marques:
            ecarts.append(EcartClasse(
                classe="en_trop", feuille_humaine="", feuille_ia=feuille,
                libelle_humain="", libelle_ia=m.libelle,
                position_humaine="", position_ia=_pos(m.x, m.y),
                detail=(f"marque IA « {m.libelle} » sur la feuille {feuille}, "
                        "feuille IA sans page humaine")))

    # Rattachement de feuille : la géométrie contredit le nom de la page.
    for paire in comp.pages.paires:
        if (paire.humain.marques and paire.methode == "géométrie"
                and paire.nom_candidat and paire.nom_candidat != paire.feuille):
            ecarts.append(EcartClasse(
                classe="mauvais_rattachement_feuille", feuille_humaine=paire.humain.nom,
                feuille_ia=paire.feuille, libelle_humain="", libelle_ia="",
                position_humaine="", position_ia="",
                detail=(f"page humaine « {paire.humain.nom} » : le nom désignait "
                        f"{paire.nom_candidat}, la géométrie la recale sur {paire.feuille} "
                        f"(score {paire.score:.2f})")))

    rang = {c: i for i, c in enumerate(CLASSES)}
    ecarts.sort(key=lambda e: (rang[e.classe], e.feuille_ia, e.feuille_humaine,
                               e.libelle_humain, e.libelle_ia,
                               e.position_humaine, e.position_ia))
    return ecarts


# --- Écriture -------------------------------------------------------------------

def _md(texte: str) -> str:
    return str(texte).replace("|", "\\|").replace("\n", " ")


def ecrire_sorties(ecarts: list[EcartClasse], sortie_dir: Path) -> dict[str, int]:
    """Écrit `ecarts-classes.csv` (contrat gelé) et `ecarts-classes.md`
    (compte par classe + liste individuelle, jamais le compte seul)."""
    sortie_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(e.classe for e in ecarts)

    with (sortie_dir / "ecarts-classes.csv").open("w", encoding="utf-8", newline="") as flux:
        w = csv.writer(flux)
        w.writerow(EN_TETE_CSV)
        for e in ecarts:
            w.writerow([e.classe, e.feuille_humaine, e.feuille_ia, e.libelle_humain,
                        e.libelle_ia, e.position_humaine, e.position_ia, e.detail])

    L: list[str] = []
    L.append("# Écarts classés — relevé humain vs relevé IA")
    L.append("")
    L.append(f"_Généré le {date.today().isoformat()} par `src.validation.classer_ecarts` — "
             "classification déterministe des désaccords de `compare_qpl` ;"
             " aucun chiffre saisi à la main._")
    L.append("")
    if not ecarts:
        L.append("Aucun désaccord classé : chaque marque humaine a une contrepartie IA, "
                 "chaque marque IA a une contrepartie humaine, familles, portées et "
                 "rattachements de feuille concordent.")
    else:
        L.append("## Compte par classe")
        L.append("")
        L.append("| Classe | Nombre |")
        L.append("|---|---:|")
        for classe in CLASSES:
            if counts.get(classe):
                L.append(f"| {classe} | {counts[classe]} |")
        L.append("")
        for classe in CLASSES:
            groupe = [e for e in ecarts if e.classe == classe]
            if not groupe:
                continue
            L.append(f"## {classe} ({len(groupe)})")
            L.append("")
            L.append("| feuille humaine | feuille IA | libellé humain | libellé IA | "
                     "position humaine | position IA | détail |")
            L.append("|---|---|---|---|---|---|---|")
            for e in groupe:
                L.append(f"| {_md(e.feuille_humaine)} | {_md(e.feuille_ia)} | "
                         f"{_md(e.libelle_humain)} | {_md(e.libelle_ia)} | "
                         f"{_md(e.position_humaine)} | {_md(e.position_ia)} | {_md(e.detail)} |")
            L.append("")
    L.append("Un compte global ne suffit pas : chaque écart ci-dessus doit être justifié "
             "sur le plan original (voir `justifier.py`, critère d'acceptation étape 5), "
             "y compris quand c'est l'estimateur qui s'est trompé.")
    (sortie_dir / "ecarts-classes.md").write_text("\n".join(L), encoding="utf-8")
    return dict(counts)


# --- CLI --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m src.validation.classer_ecarts",
                                description="Classe les désaccords de la comparaison humain/IA "
                                            "en 5 classes (critère d'acceptation étape 4).")
    p.add_argument("--humain", required=True, type=Path, help="projet Plan Expert de l'estimateur")
    p.add_argument("--ia", required=True, type=Path, help="projet Plan Expert produit par la chaîne")
    p.add_argument("--dims", required=True, type=Path, help="dimensions des rasters humains (dossier|nom|L|H)")
    p.add_argument("--feuilles", required=True, type=Path, help="feuilles.csv du dossier IA")
    p.add_argument("--sortie", required=True, type=Path, help="répertoire de sortie")
    p.add_argument("--dossier", default=None,
                   help="préfixe du dossier dans le fichier de dimensions (défaut : S-<n> tiré de --humain)")
    p.add_argument("--rasters-ia", type=Path, default=None,
                   help="répertoire des PNG IA (défaut : celui du .qpl IA)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        dossier = args.dossier
        if dossier is None:
            trouve = re.search(r"S-\d+", args.humain.name)
            dossier = trouve.group(0) if trouve else None
        dims = cq.lire_dimensions(args.dims, dossier)
        feuilles = cq.lire_feuilles(args.feuilles)
        humains = cq.lire_qpl(args.humain, "humain")
        ias = cq.lire_qpl(args.ia, "ia")
        cq.preparer_humain(humains, dims)
        anomalies = cq.preparer_ia(ias, feuilles, args.rasters_ia or args.ia.parent)
        comp = cq.comparer(humains, ias, anomalies)
    except (cq.CompareErreur, OSError) as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 2
    ecarts = classer(comp)
    counts = ecrire_sorties(ecarts, args.sortie)
    resume = ", ".join(f"{c} {counts.get(c, 0)}" for c in CLASSES if counts.get(c)) or "aucun désaccord"
    print(f"{dossier or ''} : {resume} → {args.sortie / 'ecarts-classes.csv'}")
    return 0


if __name__ == "__main__":
    from src.validation.console import forcer_utf8

    forcer_utf8()
    sys.exit(main())