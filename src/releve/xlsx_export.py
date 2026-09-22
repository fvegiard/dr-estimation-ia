"""
Export `releve.xlsx` au gabarit DR — NOUVEAU module (voir SPEC.md).

Génère un classeur Excel (openpyxl) depuis les occurrences relevées :
  python -m src.releve.xlsx_export --occurrences occurrences.csv --sortie releve.xlsx
  (aussi : python -m src.releve xlsx occurrences.csv --sortie releve.xlsx)

Colonnes de la feuille « Relevé » (une ligne par couple libellé/feuille,
chaque ligne restant rattachée à sa feuille et sa page — exigence du
pipeline : « quantités par item, référence de page/plan pour chaque
ligne ») :

    Description | Type/Identification | Quantité | Feuille/Plan | Page PDF | Notes

Plus une feuille « Résumé » agrégée par poste (familles de
`src/qpl/charte.py`, postes majeurs en tête).

Entrées :
  --occurrences  CSV des occurrences. Colonnes acceptées :
                 feuille|sheet, label|libelle|libellé, x_pt, y_pt,
                 et en option page_pdf|page, note|notes.
  --nomenclature CSV optionnel (label, description, ...) : fournit la
                 colonne « Description » ; sinon la description reprend
                 le libellé. Aucune description n'est inventée.

Format de sortie aligné sur le gabarit « Take-off et demande de prix »
(documenté dans docs/format-livrable.md) ; les colonnes que le relevé ne
peut pas remplir (Fabricant, Modèle, prix…) restent hors de ce fichier,
comme le prescrit le gabarit.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from src.qpl.charte import POSTES_MAJEURS, famille_pour_libelle, normaliser

COLONNES_RELEVE = [
    "Description",
    "Type/Identification",
    "Quantité",
    "Feuille/Plan",
    "Page PDF",
    "Notes",
]

_COL_FEUILLE = ("feuille", "sheet", "plan")
_COL_LABEL = ("label", "libelle", "libellé", "description")
_COL_PAGE = ("page_pdf", "page", "pagepdf")
_COL_NOTE = ("note", "notes", "commentaire")

_ENTETE = Font(bold=True, color="FFFFFF")
_REMPLISSAGE_ENTETE = PatternFill("solid", fgColor="1F4E79")
_REMPLISSAGE_MAJEUR = PatternFill("solid", fgColor="FFF2CC")


def _colonne(fieldnames: list[str], candidats: tuple[str, ...]) -> str | None:
    norm = {normaliser(f): f for f in fieldnames}
    for c in candidats:
        if normaliser(c) in norm:
            return norm[normaliser(c)]
    return None


def lire_occurrences(path: Path) -> list[dict]:
    """Lit le CSV d'occurrences et retourne des dicts normalisés
    {feuille, label, page_pdf, note}. Les colonnes x_pt/y_pt, si
    présentes, ne servent pas à l'agrégat mais valident la ligne."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError(f"{path} : CSV sans en-tête")
        c_feuille = _colonne(reader.fieldnames, _COL_FEUILLE)
        c_label = _colonne(reader.fieldnames, _COL_LABEL)
        if not c_feuille or not c_label:
            raise ValueError(
                f"{path} : colonnes obligatoires introuvables "
                f"(feuille parmi {_COL_FEUILLE}, label parmi {_COL_LABEL})"
            )
        c_page = _colonne(reader.fieldnames, _COL_PAGE)
        c_note = _colonne(reader.fieldnames, _COL_NOTE)
        out = []
        for row in reader:
            feuille = (row.get(c_feuille) or "").strip()
            label = (row.get(c_label) or "").strip()
            if not feuille or not label:
                continue
            out.append(
                {
                    "feuille": feuille,
                    "label": label,
                    "page_pdf": (row.get(c_page) or "").strip() if c_page else "",
                    "note": (row.get(c_note) or "").strip() if c_note else "",
                }
            )
    return out


def lire_nomenclature(path: Path | None) -> dict[str, str]:
    """{label: description} depuis un CSV de nomenclature (colonnes
    label + description ; les autres colonnes sont ignorées)."""
    if path is None:
        return {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return {}
        c_label = _colonne(reader.fieldnames, _COL_LABEL)
        c_desc = _colonne(reader.fieldnames, ("description", "desc"))
        if not c_label or not c_desc:
            return {}
        return {
            (row[c_label] or "").strip(): (row[c_desc] or "").strip()
            for row in reader
            if (row.get(c_label) or "").strip()
        }


def agreger(occurrences: list[dict]) -> list[dict]:
    """Une ligne par (libellé, feuille) : quantité = nombre d'occurrences,
    pages = pages PDF distinctes (triées), notes = notes distinctes."""
    groupes: dict[tuple[str, str], dict] = {}
    for occ in occurrences:
        cle = (occ["label"], occ["feuille"])
        g = groupes.setdefault(
            cle, {"label": occ["label"], "feuille": occ["feuille"],
                  "quantite": 0, "pages": [], "notes": []}
        )
        g["quantite"] += 1
        if occ["page_pdf"] and occ["page_pdf"] not in g["pages"]:
            g["pages"].append(occ["page_pdf"])
        if occ["note"] and occ["note"] not in g["notes"]:
            g["notes"].append(occ["note"])

    def _tri_page(valeur: str):
        return (0, int(valeur)) if valeur.isdigit() else (1, valeur)

    lignes = []
    for (label, feuille), g in sorted(groupes.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        lignes.append(
            {
                "label": label,
                "feuille": feuille,
                "quantite": g["quantite"],
                "page_pdf": ", ".join(sorted(g["pages"], key=_tri_page)),
                "notes": " ; ".join(g["notes"]),
            }
        )
    return lignes


def ecrire_xlsx(lignes: list[dict], nomenclature: dict[str, str], sortie: Path) -> None:
    wb = Workbook()

    # --- Feuille « Relevé » : une ligne par (libellé, feuille)
    ws = wb.active
    ws.title = "Relevé"
    ws.append(COLONNES_RELEVE)
    for cell in ws[1]:
        cell.font = _ENTETE
        cell.fill = _REMPLISSAGE_ENTETE
    for ligne in lignes:
        ws.append(
            [
                nomenclature.get(ligne["label"]) or ligne["label"],
                ligne["label"],
                ligne["quantite"],
                ligne["feuille"],
                ligne["page_pdf"],
                ligne["notes"],
            ]
        )
    for col, largeur in zip("ABCDEF", (46, 30, 10, 14, 10, 40)):
        ws.column_dimensions[col].width = largeur
    ws.freeze_panes = "A2"

    # --- Feuille « Résumé » : agrégat par poste (familles de la charte),
    #     postes majeurs en tête.
    ws2 = wb.create_sheet("Résumé")
    ws2.append(["Poste", "Poste majeur", "Quantité", "Détail par feuille"])
    for cell in ws2[1]:
        cell.font = _ENTETE
        cell.fill = _REMPLISSAGE_ENTETE
    par_poste: dict[str, dict] = {}
    for ligne in lignes:
        poste = famille_pour_libelle(ligne["label"])
        p = par_poste.setdefault(poste, {"quantite": 0, "feuilles": {}})
        p["quantite"] += ligne["quantite"]
        p["feuilles"][ligne["feuille"]] = p["feuilles"].get(ligne["feuille"], 0) + ligne["quantite"]

    def _tri_poste(item):
        poste = item[0]
        return (POSTES_MAJEURS.index(poste) if poste in POSTES_MAJEURS else len(POSTES_MAJEURS), poste)

    for poste, p in sorted(par_poste.items(), key=_tri_poste):
        detail = ", ".join(f"{f} : {n}" for f, n in sorted(p["feuilles"].items()))
        ws2.append([poste, "oui" if poste in POSTES_MAJEURS else "non", p["quantite"], detail])
        if poste in POSTES_MAJEURS:
            for cell in ws2[ws2.max_row]:
                cell.fill = _REMPLISSAGE_MAJEUR
    for col, largeur in zip("ABCD", (16, 13, 10, 60)):
        ws2.column_dimensions[col].width = largeur
    ws2.freeze_panes = "A2"

    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    wb.save(sortie)


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def add_arguments(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("occurrences", type=Path, nargs="?", default=None,
                     help="CSV des occurrences (positionnel, ou --occurrences)")
    sub.add_argument("--occurrences", dest="occurrences_opt", type=Path,
                     help="CSV des occurrences (équivalent en option)")
    sub.add_argument("--sortie", type=Path, required=True, help="releve.xlsx à écrire")
    sub.add_argument("--nomenclature", type=Path,
                     help="CSV optionnel (label, description) pour la colonne Description")


def run(args: argparse.Namespace) -> int:
    occurrences_csv = args.occurrences_opt or args.occurrences
    if occurrences_csv is None:
        raise SystemExit("CSV d'occurrences requis (positionnel ou --occurrences)")
    occurrences = lire_occurrences(occurrences_csv)
    if not occurrences:
        raise SystemExit(f"{occurrences_csv} : aucune occurrence exploitable")
    lignes = agreger(occurrences)
    nomenclature = lire_nomenclature(args.nomenclature)
    ecrire_xlsx(lignes, nomenclature, args.sortie)
    total = sum(l["quantite"] for l in lignes)
    print(
        f"OK : {args.sortie} — {total} occurrences agrégées en {len(lignes)} lignes "
        f"({len({l['label'] for l in lignes})} libellés, {len({l['feuille'] for l in lignes})} feuilles)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m src.releve.xlsx_export",
        description="Occurrences CSV -> releve.xlsx au gabarit DR.",
    )
    add_arguments(parser)
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
