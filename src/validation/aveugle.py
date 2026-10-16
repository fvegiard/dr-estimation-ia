"""
Contrôle du relevé « à l'aveugle » — étape 1 du critère d'acceptation (CLAUDE.md).
Preuve déterministe qu'un dossier de travail de relevé IA ne contient aucun
matériau de l'estimateur : l'identification doit venir des plans et addendas
SEULEMENT, jamais du .qpl ou du relevé de l'estimateur. Ce module constate
l'état du dossier ; il ne prouve pas davantage la discipline de l'agent.

CLI :
  python -m src.validation.aveugle WORKDIR

Code de sortie : 0 = aveugle (aucune référence détectée), 1 = référence
estimateur détectée, 2 = erreur d'entrée.

Détections (règles dans l'ordre ; la première qui s'applique nomme le motif) :
  1. `qpl-dupuis`          — .qpl dont le nom contient « dupuis » : le projet
                             Plan Expert de l'estimateur se nomme
                             <S>-Dupuis-PlanExpert.qpl ;
  2. `dossier-reference`   — tout fichier placé sous un dossier `reference/` :
                             c'est l'emplacement réservé au relevé humain de
                             l'estimateur (§Ajouter un dossier de CLAUDE.md),
                             jamais au travail du relevé aveugle — ce qui vaut
                             pour un .qpl vaut pour n'importe quel fichier du
                             même dossier (`feuilles-ia.csv`, PNG marqués…) ;
  2b. `dossier-estimateur` — tout fichier placé sous un dossier `estimateur/` :
                             `prepare.py` n'y écrit jamais autre chose qu'un
                             export de l'estimateur (`pNN.png`, `legendes/*.png`,
                             `pages.csv`), et les PNG binaires échapperaient
                             autrement au scan de contenu ;
  3. `nom-<mot>`           — tout fichier dont le NOM contient dupuis |
                              estimateur | reference | humain, insensible aux
                              accents et à la casse (relevés humains : releve
                              .xlsx dénommés de l'estimateur, CSV de décompte) ;
  4. `releve-humain`       — le relevé humain canonique `releve.xlsx` (NOM
                              exact, insensible à la casse) — « releve » seul
                              n'est PAS un marqueur (le relevé IA a ses propres
                              fichiers `rapport-releve.md`, `releve` n'est pas
                              dans les mots de la règle 3) : seul le nom exact
                              du relevé humain fait foi ;
  5. `contenu-<signature>` — tout fichier TEXTE (suffixe courant) de moins de
                              5 Mo dont le contenu signale « dupuis » ou
                              « estimateur » (noms trop neutres : `ecart.md`,
                              `resultats.json`) ; les signatures n'ont aucune
                              forme accentuée, une recherche insensible à la
                              casse suffit.

Le contrôle écrit `controle-aveugle.json` dans le dossier de travail :
  {date, fichiers_scannes, references_detectees: [{fichier, motif}], aveugle}

Fichiers méta du pipeline EXCLUS de la règle de contenu (gabarits et journaux
écrits par prepare.py / le lanceur, qui citent « estimateur » en texte fixe —
MANIFESTE.md : « Estimateur (si fourni) … » — sans jamais porter de données de
l'estimateur) : les scanner ferait échouer tout dossier honnête. À l'inverse,
`inventaire.json` et `feuilles.csv` restent scannés : si un export de
l'estimateur est déposé dans l'INBOX (règle « plans + addendas seulement »
enfreinte), c'est là qu'il se voit.

Le compte-rendu du contrôle (`controle-aveugle.json`) n'est jamais scanné :
il cite les fichiers détectés, une reprise le ferait détecter lui-même.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from src.qpl.charte import normaliser

NOM_RAPPORT = "controle-aveugle.json"

MOTS_NOM = ("dupuis", "estimateur", "reference", "humain")
SIGNATURES_CONTENU = ("dupuis", "estimateur")
NOM_RELEVE_HUMAIN = "releve.xlsx"   # relevé humain canonique (dossiers/<S>/releve.xlsx)

# 5 Mo : au-delà, un fichier texte n'est plus un livrable de relevé mais un
# export volumineux ; le scan de contenu refuserait de finir en temps utile.
TAILLE_MAX_TEXTE_OCTETS = 5 * 1024 * 1024

SUFFIXES_TEXTE = frozenset({
    ".csv", ".md", ".txt", ".json", ".xml", ".qpl", ".toml", ".yaml", ".yml",
    ".ini", ".cfg", ".log", ".py",
})

# Gabarits et journaux du pipeline (prepare.py, lanceurs d'agent) : texte fixe
# qui cite « estimateur » (MANIFESTE.md : « Estimateur (si fourni) … ») ou voix
# méta de l'agent (session, usage, journal d'outils) — jamais un matériau de
# l'estimateur. Le reste du dossier de travail, lui, est scanné sans exception.
FICHIERS_META_PIPELINE = frozenset({
    "MANIFESTE.md",
    "REPRISE.md",
    "agent-resultat.json",
    "agent-journal.log",
})


class AveugleErreur(ValueError):
    """Entrée illisible ou incomplète — refusée, jamais corrigée en silence."""


@dataclass(frozen=True)
class ReferenceDetectee:
    fichier: str   # chemin relatif au dossier de travail
    motif: str     # règle qui a tranché (qpl-dupuis, dossier-reference, nom-…, releve-humain, contenu-…)


@dataclass
class RapportAveugle:
    date: str
    fichiers_scannes: int = 0
    references_detectees: list[ReferenceDetectee] = field(default_factory=list)

    @property
    def aveugle(self) -> bool:
        return not self.references_detectees

    def vers_dict(self) -> dict:
        """Structure exacte du JSON livrable : {date, fichiers_scannes,
        references_detectees, aveugle}."""
        return {
            "date": self.date,
            "fichiers_scannes": self.fichiers_scannes,
            "references_detectees": [
                {"fichier": ref.fichier, "motif": ref.motif}
                for ref in self.references_detectees
            ],
            "aveugle": self.aveugle,
        }


# --------------------------------------------------------------------- #
# Règles de détection
# --------------------------------------------------------------------- #

def motif_par_chemin(relatif: Path) -> str | None:
    """Règles 1-4, appliquées au chemin relatif (nom + dossier parent)."""
    nom_norm = normaliser(relatif.name)
    if relatif.suffix.lower() == ".qpl" and "dupuis" in nom_norm:
        return "qpl-dupuis"
    if any(normaliser(part) == "reference" for part in relatif.parts[:-1]):
        return "dossier-reference"
    if any(normaliser(part) == "estimateur" for part in relatif.parts[:-1]):
        return "dossier-estimateur"
    for mot in MOTS_NOM:
        if mot in nom_norm:
            return f"nom-{mot}"
    if nom_norm == normaliser(NOM_RELEVE_HUMAIN):
        return "releve-humain"
    return None


def motif_par_contenu(path: Path) -> str | None:
    """Règle 5 : signatures « dupuis », « estimateur » dans un fichier texte
    de moins de 5 Mo. Les binaires (PNG, XLSX, PDF) sont ignorés."""
    if path.suffix.lower() not in SUFFIXES_TEXTE:
        return None
    if path.name in FICHIERS_META_PIPELINE:
        return None
    if path.stat().st_size > TAILLE_MAX_TEXTE_OCTETS:
        return None
    octets = path.read_bytes()
    try:
        texte = octets.decode("utf-8")
    except UnicodeDecodeError:
        if b"\x00" in octets:
            return None          # binaire déguisé en suffixe texte : ignoré
        texte = octets.decode("latin-1")
    bas = texte.casefold()
    for signature in SIGNATURES_CONTENU:
        if signature in bas:
            return f"contenu-{signature}"
    return None


# --------------------------------------------------------------------- #
# Contrôle et rapport
# --------------------------------------------------------------------- #

def controler(workdir) -> RapportAveugle:
    """Scan récursif du dossier de travail, détection de toute référence
    estimateur, écriture de `controle-aveugle.json` dans le dossier."""
    dossier = Path(workdir)
    if not dossier.is_dir():
        raise AveugleErreur(f"dossier de travail introuvable ou non répertoire : {dossier}")
    rapport = RapportAveugle(date=date.today().isoformat())
    for path in sorted(p for p in dossier.rglob("*") if p.is_file()):
        relatif = path.relative_to(dossier)
        if relatif.name == NOM_RAPPORT:
            continue
        rapport.fichiers_scannes += 1
        motif = motif_par_chemin(relatif) or motif_par_contenu(path)
        if motif:
            rapport.references_detectees.append(
                ReferenceDetectee(fichier=relatif.as_posix(), motif=motif)
            )
    ecrire_rapport(rapport, dossier)
    return rapport


def ecrire_rapport(rapport: RapportAveugle, workdir) -> Path:
    """Écrit `controle-aveugle.json` et retourne son chemin."""
    sortie = Path(workdir) / NOM_RAPPORT
    sortie.write_text(
        json.dumps(rapport.vers_dict(), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return sortie


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.validation.aveugle",
        description=(
            "Contrôle du relevé à l'aveugle : détecte toute référence estimateur "
            "(.qpl Dupuis, dossier reference/, noms dupuis|estimateur|reference|humain, "
            "signatures de contenu) dans un dossier de travail -> controle-aveugle.json"
        ),
    )
    parser.add_argument("workdir", type=Path,
                        help="Dossier de travail du relevé IA à contrôler")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rapport = controler(args.workdir)
    except (AveugleErreur, OSError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    sortie = Path(args.workdir) / NOM_RAPPORT
    if rapport.aveugle:
        print(
            f"AVEUGLE : {rapport.fichiers_scannes} fichier(s) scanné(s), "
            f"aucune référence estimateur détectée — rapport : {sortie}"
        )
        return 0
    print(
        f"NON AVEUGLE : {len(rapport.references_detectees)} référence(s) estimateur "
        f"détectée(s) — rapport : {sortie}"
    )
    for ref in rapport.references_detectees:
        print(f"  - {ref.fichier} ({ref.motif})")
    return 1


if __name__ == "__main__":
    from src.validation.console import forcer_utf8

    forcer_utf8()
    raise SystemExit(main())