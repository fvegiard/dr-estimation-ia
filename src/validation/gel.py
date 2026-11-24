"""
Gel sha256 du relevé IA AVANT toute comparaison — étape 2 du critère
d'acceptation (CLAUDE.md §Critère d'acceptation : « Geler ce premier
résultat (commit) avant toute comparaison »).

`geler(workdir)` écrit `gel.json` dans le dossier de travail (workdir) :
empreinte sha256 de chaque artefact du relevé IA présent
(nomenclature.csv, occurrences-texte.csv, occurrences-visuel.csv,
feuilles-classement.csv, reserves.md, tout `.qpl` produit). Après le gel,
toute modification ou suppression d'un artefact gelé est détectée par
`verifier_gel(workdir)` — le relevé n'est plus le résultat « à l'aveugle »
d'origine et toute comparaison ultérieure est invalide pour l'étape 3.
Les fichiers ajoutés APRÈS le gel (résultats de comparaison, journaux…)
ne remettent pas le gel en cause : tolérés, mais toujours listés
(`ajoutes_apres_gel`) pour rester transparents.

CLI :
  python -m src.validation.gel WORKDIR              gèle les artefacts -> gel.json
  python -m src.validation.gel WORKDIR --verifier   revérifie le gel
                                                    (code 1 si violé, 2 erreur)

Le verrou du gel est le FICHIER gel.json, pas un rapport d'agent : la
comparaison (`src.validation.compare_qpl`) ne s'exécute que sur un gel
intact. Verdict FINAL reste à Francis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# Nom du livrable de gel — jamais gelé lui-même (artefact de contrôle).
NOM_GEL = "gel.json"

# Artefacts du relevé IA cherchés à la racine du workdir. Plus tout
# `.qpl` produit, quelque part dans le workdir (voir _candidats).
ARTEFACTS_NOMMES = (
    "nomenclature.csv",
    "occurrences-texte.csv",
    "occurrences-visuel.csv",
    "feuilles-classement.csv",
    "feuilles.csv",
    "inventaire.json",
    "legende.csv",
    "contexte-candidats.csv",
    "multiplicateurs.csv",
    "metre-longueurs.csv",
    "metre-longueurs.json",
    "qualite.json",
    "reserves.md",
)
ARTEFACTS_STRICTS = ("blocs-a-etiqueter.json", "blocs-non-relevees.json", "ancrage-raster.json",
                     "comparaison-legende.json", "rapport-releve.md")


class GelError(Exception):
    """Aucun artefact à geler, ou gel absent/illisible — refusé, jamais corrigé en silence."""


@dataclass
class Artefact:
    fichier: str   # chemin relatif au workdir (séparateurs /)
    sha256: str    # empreinte hexadécimale du contenu
    octets: int    # taille du fichier


@dataclass
class RapportGel:
    """Résultat de la vérification d'un gel. La vérité (« gel intact ? »)
    voyage avec ses listes : `__bool__` retourne `ok` — le rapport se
    teste exactement comme le booléen de la spécification."""

    ok: bool
    modifies: list[str] = field(default_factory=list)         # artefacts gelés changés
    manquants: list[str] = field(default_factory=list)        # artefacts gelés disparus
    ajoutes_apres_gel: list[str] = field(default_factory=list)  # tolérés, jamais silencieux
    chemin_gel: Path | None = None

    def __bool__(self) -> bool:
        return self.ok


# --------------------------------------------------------------------- #
# Empreintes
# --------------------------------------------------------------------- #

def _sha256(path: Path) -> str:
    """Empreinte sha256 hexadécimale du contenu d'un fichier."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _candidats(workdir: Path, *, strict: bool) -> dict[str, Path]:
    """Artefacts du relevé IA présents -> {chemin relatif POSIX : chemin}.
    Artefacts nommés à la racine + tout `.qpl` produit dans l'arbre."""
    actuels: dict[str, Path] = {}
    for nom in ARTEFACTS_NOMMES:
        p = workdir / nom
        if p.is_file():
            actuels[nom] = p
    if strict:
        for nom in ARTEFACTS_STRICTS:
            if (p := workdir / nom).is_file():
                actuels[nom] = p
    for p in sorted(workdir.rglob("*.qpl")):
        if p.is_file():
            actuels[p.relative_to(workdir).as_posix()] = p
    return actuels


def _deriver_soumission(workdir: Path) -> str:
    """Nom de Soumission dérivé du workdir : le parent si le workdir se
    nomme « travail » (OUTBOX/<S>/travail), sinon le workdir lui-même."""
    if workdir.name == "travail" and workdir.parent.name:
        return workdir.parent.name
    return workdir.name


def _sources(workdir):
    """Inventaire de la préparation stricte : contrôler également les PDF qu'il désigne."""
    p = workdir / "inventaire.json"
    if not p.is_file():
        return None, {}
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
        if not j.get("plans_seuls"):
            return None, {}
        racine = Path(j["inbox"])
        if not racine.is_absolute() or not j["fichiers"]:
            raise ValueError("racine absolue et PDF attendus")
        attendus = {}
        for e in j["fichiers"]:
            nom, h = e["fichier"], e["sha256"]
            rel = Path(nom)
            if (rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() != ".pdf" or nom in attendus or
                    not re.fullmatch(r"[0-9a-f]{64}", h) or e["classement"] not in {"plans", "addenda", "scan"}):
                raise ValueError("chemin, classement ou SHA-256 invalides")
            attendus[nom] = h
        return racine, attendus
    except (OSError, ValueError, AttributeError, KeyError, TypeError) as e:
        raise GelError(f"inventaire.json : sources invérifiables ({e})") from e


def verifier_sources(workdir, rapport):
    racine, attendus = _sources(workdir)
    if racine is None:
        return
    for nom, h in attendus.items():
        p = racine / nom
        trace = "INBOX/" + nom
        if not p.is_file():
            rapport.manquants.append(trace)
        elif p.is_symlink() or not p.resolve().is_relative_to(racine.resolve()) or _sha256(p) != h:
            rapport.modifies.append(trace)
    for p in sorted(q for q in racine.rglob("*") if q.is_file()):
        if p.relative_to(racine).as_posix() not in attendus:
            rapport.modifies.append(f"INBOX/{p.relative_to(racine).as_posix()} (nouvelle entrée)")


# --------------------------------------------------------------------- #
# Gel / vérification
# --------------------------------------------------------------------- #

def geler(workdir: Path | str, *, soumission: str | None = None) -> Path:
    """Gèle les artefacts du relevé IA présents dans `workdir` -> gel.json.
    Retourne le chemin du gel. `GelError` si aucun artefact (relevé vide)."""
    workdir = Path(workdir)
    if not workdir.is_dir():
        raise GelError(f"dossier de travail introuvable : {workdir}")
    actuels = _candidats(workdir, strict=_sources(workdir)[0] is not None)
    if not actuels:
        raise GelError(
            f"aucun artefact du relevé IA à geler dans {workdir} "
            f"(cherché : {', '.join(ARTEFACTS_NOMMES)}, *.qpl)"
        )
    controle = RapportGel(ok=True)
    verifier_sources(workdir, controle)
    if controle.modifies or controle.manquants:
        raise GelError("Les PDF ne correspondent plus à l'inventaire de la préparation")
    gel = {
        "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        "soumission": soumission or _deriver_soumission(workdir),
        "artefacts": [
            asdict(
                Artefact(
                    fichier=rel,
                    sha256=_sha256(p),
                    octets=p.stat().st_size,
                )
            )
            for rel, p in sorted(actuels.items())
        ],
    }
    chemin = workdir / NOM_GEL
    try:
        with chemin.open("x", encoding="utf-8") as flux:
            flux.write(json.dumps(gel, indent=1, ensure_ascii=False) + "\n")
    except FileExistsError as e:
        raise GelError("gel déjà présent : vérifiez-le ou utilisez un dossier de travail neuf") from e
    return chemin


def lire_gel(workdir: Path | str) -> dict:
    """Charge gel.json du workdir. `GelError` si absent, illisible ou mal formé."""
    chemin = Path(workdir) / NOM_GEL
    if not chemin.is_file():
        raise GelError(f"aucun gel à vérifier : {chemin} absent (relancer d'abord le gel)")
    try:
        gel = json.loads(chemin.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise GelError(f"{chemin} illisible : {exc}") from exc
    if not isinstance(gel, dict) or not isinstance(gel.get("artefacts"), list) or not gel["artefacts"]:
        raise GelError(f"{chemin} mal formé : « artefacts » (liste) introuvable")
    vus = set()
    for a in gel["artefacts"]:
        if (not isinstance(a, dict) or not isinstance(a.get("fichier"), str) or not a["fichier"]
                or Path(a["fichier"]).is_absolute() or a["fichier"] in vus
                or not isinstance(a.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", a["sha256"])
                or not isinstance(a.get("octets"), int) or a["octets"] < 0):
            raise GelError(f"{chemin} mal formé : artefact dupliqué ou invalide")
        vus.add(a["fichier"])
    return gel


def verifier_gel(workdir: Path | str) -> RapportGel:
    """Re-hache chaque artefact gelé : gel intact ? `RapportGel` à vérité
    booléenne (`__bool__` -> `ok`) :
      - artefact gelé changé   -> False + `modifies` rempli ;
      - artefact gelé disparu  -> False + `manquants` rempli ;
      - fichiers ajoutés après le gel -> tolérés, listés dans `ajoutes_apres_gel`
        (un fichier candidat présent aujourd'hui mais absent du gel).
    `GelError` si gel.json absent ou illisible."""
    workdir = Path(workdir)
    gel = lire_gel(workdir)
    rapport = RapportGel(ok=True, chemin_gel=workdir / NOM_GEL)
    gelés = {
        a["fichier"]: a
        for a in gel["artefacts"]
        if isinstance(a, dict) and "fichier" in a
    }
    for rel, info in sorted(gelés.items()):
        p = workdir / Path(*Path(rel).parts)
        if not p.is_file():
            rapport.manquants.append(rel)
            continue
        if _sha256(p) != info.get("sha256"):
            rapport.modifies.append(rel)
    inventaire_intact = "inventaire.json" not in rapport.modifies and "inventaire.json" not in rapport.manquants
    strict = inventaire_intact and _sources(workdir)[0] is not None
    for rel in sorted(_candidats(workdir, strict=strict)):
        if rel not in gelés:
            rapport.ajoutes_apres_gel.append(rel)
    if strict:
        verifier_sources(workdir, rapport)
    rapport.ok = not (rapport.modifies or rapport.manquants)
    return rapport


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.validation.gel",
        description="Gel sha256 des artefacts du relevé IA avant comparaison -> gel.json",
    )
    parser.add_argument("workdir", type=Path,
                        help="dossier de travail du relevé IA (les artefacts à la racine)")
    parser.add_argument("--verifier", action="store_true",
                        help="revérifie un gel existant (code 1 si violé)")
    parser.add_argument("--soumission", type=str, default=None,
                        help="nom de la soumission (dérivé du workdir si absent)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.verifier:
            rapport = verifier_gel(args.workdir)
        else:
            chemin = geler(args.workdir, soumission=args.soumission)
            gel = lire_gel(args.workdir)
            print(f"gelé : {chemin} — {len(gel['artefacts'])} artefact(s), "
                  f"soumission {gel['soumission']}, date {gel['date']}")
            return 0
    except (GelError, OSError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    for rel in rapport.modifies:
        print(f"modifié après le gel : {rel}", file=sys.stderr)
    for rel in rapport.manquants:
        print(f"disparu après le gel : {rel}", file=sys.stderr)
    for rel in rapport.ajoutes_apres_gel:
        print(f"ajouté après le gel (toléré) : {rel}")
    if rapport.ok:
        print(f"gel intact : {rapport.chemin_gel}")
        return 0
    print(
        f"GEL VIOLÉ : {len(rapport.modifies)} modifié(s), {len(rapport.manquants)} disparu(s) "
        f"— relevé IA plus le résultat à l'aveugle d'origine",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    from src.validation.console import forcer_utf8

    forcer_utf8()
    raise SystemExit(main())