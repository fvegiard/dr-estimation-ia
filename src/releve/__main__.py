"""
Point d'entrée `python -m src.releve <sous-commande> ...`.

Sous-commandes, une par étape du pipeline (voir docs/pipeline-qpl.md) :
  inventaire  dossier de PDF -> JSON (pages, format pt, texte, disciplines)
  index       PDF -> index des feuilles (numéro, titre, échelle, révision,
              date lus dans le cartouche par position)
  raster      page PDF -> PNG au DPI voulu + JSON du rapport px<->pt
  qpl         JSON de compteurs + JSON de plans -> .qpl Plan Expert valide
  verifier    .qpl -> décompte (compteurs, éléments, lignes, GroupID) + sha256
  xlsx        occurrences CSV -> releve.xlsx au gabarit DR (xlsx_export)
"""
from __future__ import annotations

import argparse
import sys

from . import index as mod_index
from . import inventaire as mod_inventaire
from . import qpl_build as mod_qpl
from . import raster as mod_raster
from . import verifier as mod_verifier
from . import xlsx_export as mod_xlsx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.releve",
        description="Outillage de relevé de quantités Plan Expert (socle réutilisable).",
    )
    sub = parser.add_subparsers(dest="commande", required=True)

    p = sub.add_parser("inventaire", help="Dossier de PDF -> JSON (pages, format, texte, discipline)")
    mod_inventaire.add_arguments(p)
    p.set_defaults(func=mod_inventaire.run)

    p = sub.add_parser("index", help="PDF -> index des feuilles (cartouche par position)")
    mod_index.add_arguments(p)
    p.set_defaults(func=mod_index.run)

    p = sub.add_parser("raster", help="Page PDF -> PNG + JSON du rapport px<->pt")
    mod_raster.add_arguments(p)
    p.set_defaults(func=mod_raster.run)

    p = sub.add_parser("qpl", help="JSON de compteurs + JSON de plans -> .qpl Plan Expert")
    mod_qpl.add_arguments(p)
    p.set_defaults(func=mod_qpl.run)

    p = sub.add_parser("verifier", help=".qpl -> décompte (compteurs, éléments, lignes, GroupID) + sha256")
    mod_verifier.add_arguments(p)
    p.set_defaults(func=mod_verifier.run)

    p = sub.add_parser("xlsx", help="Occurrences CSV -> releve.xlsx au gabarit DR")
    mod_xlsx.add_arguments(p)
    p.set_defaults(func=mod_xlsx.run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
