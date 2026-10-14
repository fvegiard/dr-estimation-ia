"""
Dossier de justification des désaccords — étapes 5 à 7 du critère
d'acceptation (CLAUDE.md). Le module est le **consommateur** du contrat gelé
`ecarts-classes.csv` (produit parallèle par `classer_ecarts` — en-tête exact,
classes énumérées, positions `x:y` pixels IA, UTF-8) : toute entrée hors
contrat est refusée, jamais corrigée en silence. Il n'importe aucun des
autres modules du convoy.

1. `generer_dossier` écrit `justifications.md` : une ligne à trancher par
   désaccord, preuve et verdict à remplir sur la source originale
   (plan / cédule / addenda).
2. `controler_justifications` relit le dossier rempli : verdicts reconnus
   (« IA correcte », « estimateur correct », « ambigu → réserve »), mais
   aucune ligne n'est tranchée sans preuve non vide — « estimateur correct »
   compris ; toute ligne du CSV absente du dossier est signalée.
   Un désaccord sans preuve = non tranché : la boucle d'acceptation ne
   poursuit jamais sur des désaccords non tranchés.
3. Rappels en en-tête du dossier : symétrie IA/estimateur (étape 5 —
   une erreur constatée chez l'estimateur exige elle aussi une preuve sur
   le plan) et « une quantité plus élevée seule n'est jamais une
   amélioration » (étape 7).

CLI :
  python -m src.validation.justifier generer --ecarts ecarts-classes.csv \
      --dossier DIR [--sortie F]
  python -m src.validation.justifier controler justifications.md [--ecarts E]

Codes de sortie : generer 0 = OK, 2 = erreur d'entrée ;
controler 0 = complet, 1 = au moins un désaccord non tranché (ou une ligne
du CSV absente du dossier), 2 = erreur.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from src.qpl.charte import normaliser

# Contrat gelé (NON NÉGOCIABLE) — en-tête exact de `ecarts-classes.csv`.
EN_TETE_CONTRAT = (
    "classe", "feuille_humaine", "feuille_ia", "libelle_humain",
    "libelle_ia", "position_humaine", "position_ia", "detail",
)
CLASSES_CONTRAT = (
    "omission", "en_trop", "doublon", "mauvaise_famille",
    "mauvaise_portee", "mauvais_rattachement_feuille",
)

VERDICT_IA = "IA correcte"
VERDICT_ESTIMATEUR = "estimateur correct"
VERDICT_AMBIGU = "ambigu → réserve"

_RE_RASTER = re.compile(r"[\w./\\-]+\.(?:png|jpe?g|tiff?)\b", re.IGNORECASE)
_RE_POSITION = re.compile(r"\d+(?:\.\d+)?\s*:\s*\d+(?:\.\d+)?")
# Couples `x, y` (ou `x:y`) numériques d'une cellule de position remplie.
_RE_COUPLES = re.compile(r"(\d+(?:\.\d+)?)\s*[:,]\s*(\d+(?:\.\d+)?)")


class JustifierErreur(ValueError):
    """Entrée illisible ou hors contrat — refusée, jamais corrigée en silence."""


# --------------------------------------------------------------------- #
# Lecture du contrat gelé
# --------------------------------------------------------------------- #

@dataclass
class Desaccord:
    """Un désaccord du CSV gelé, tel quel (aucune valeur calculée)."""
    classe: str
    feuille_humaine: str
    feuille_ia: str
    libelle_humain: str
    libelle_ia: str
    position_humaine: str
    position_ia: str
    detail: str
    ligne: int   # n° de ligne dans le CSV (2 = première ligne de données)

    @property
    def cle(self) -> tuple:
        """Identité d'appariement CSV ↔ dossier (indépendante de l'affiche)."""
        return _cle_ligne(self.classe, self.libelle_humain, self.libelle_ia,
                          self.position_humaine, self.position_ia)


def _paire_position(brut: str) -> tuple[float, float] | None:
    brut = (brut or "").strip()
    if not brut:
        return None
    x, y = brut.split(":")
    return (float(x), float(y))


def _cle_ligne(classe: str, libelle_humain: str, libelle_ia: str,
               position_humaine: str, position_ia: str) -> tuple:
    positions = sorted(p for p in (_paire_position(position_humaine),
                                   _paire_position(position_ia)) if p)
    return (normaliser(classe), normaliser(libelle_humain),
            normaliser(libelle_ia), tuple(positions))


def lire_ecarts(ecarts_csv: Path) -> list[Desaccord]:
    """Lit `ecarts-classes.csv` — refuse toute entorse au contrat gelé."""
    path = Path(ecarts_csv)
    try:
        with path.open(encoding="utf-8-sig", newline="") as flux:
            lignes = list(csv.reader(flux))
    except OSError as exc:
        raise JustifierErreur(f"CSV illisible : {path} ({exc})") from exc
    except csv.Error as exc:
        raise JustifierErreur(f"CSV illisible : {path} ({exc})") from exc
    if not lignes or not any(c.strip() for c in lignes[0]):
        raise JustifierErreur(f"{path} : CSV vide")
    entete = [c.strip() for c in lignes[0]]
    if entete != list(EN_TETE_CONTRAT):
        raise JustifierErreur(
            f"{path} : en-tête hors contrat\n"
            f"  attendu : {','.join(EN_TETE_CONTRAT)}\n"
            f"  obtenu  : {','.join(entete)}"
        )
    desaccords: list[Desaccord] = []
    for i, champs in enumerate(lignes[1:], start=2):
        if not any(c.strip() for c in champs):
            continue
        if len(champs) != len(EN_TETE_CONTRAT):
            raise JustifierErreur(
                f"{path} ligne {i} : {len(champs)} colonnes, le contrat en exige "
                f"{len(EN_TETE_CONTRAT)}")
        classe, feuille_h, feuille_i, lib_h, lib_i, pos_h, pos_i, detail = (
            c.strip() for c in champs)
        if classe not in CLASSES_CONTRAT:
            raise JustifierErreur(
                f"{path} ligne {i} : classe « {classe} » hors contrat "
                f"({', '.join(CLASSES_CONTRAT)})")
        for pos, nom in ((pos_h, "position_humaine"), (pos_i, "position_ia")):
            if pos and not _RE_POSITION.fullmatch(pos):
                raise JustifierErreur(
                    f"{path} ligne {i} : {nom} = « {pos} » — positions "
                    "`x:y` pixels attendues")
        desaccords.append(Desaccord(classe, feuille_h, feuille_i, lib_h, lib_i,
                                    pos_h, pos_i, detail, i))
    return desaccords


# --------------------------------------------------------------------- #
# Rendu des cellules (affichage exact, lisible, repréable au plan)
# --------------------------------------------------------------------- #

def _echapper(texte: str) -> str:
    return str(texte).replace("|", "\\|")


def _xy_affiche(pos: str) -> str:
    x, y = (p.strip() for p in pos.split(":"))
    return f"{x}, {y}"


def cellule_position(position_humaine: str, position_ia: str) -> str:
    """Position(s) exacte(s) en pixels IA — l'IA d'abord, puis l'humain recalé."""
    parts = []
    if position_ia:
        parts.append(f"IA {_xy_affiche(position_ia)}")
    if position_humaine:
        parts.append(f"humain {_xy_affiche(position_humaine)}")
    return " ; ".join(parts) if parts else "—"


def cellule_feuille(feuille_humaine: str, feuille_ia: str, raster: str = "") -> str:
    """Feuille du désaccord ; le raster lu dans `detail` (contrat) est ajouté."""
    if feuille_ia and feuille_humaine and feuille_ia != feuille_humaine:
        base = f"humain {feuille_humaine} / IA {feuille_ia}"
    else:
        base = feuille_ia or feuille_humaine
    if raster:
        return f"{base} (raster {raster})" if base else f"raster {raster}"
    return base or "—"


def _raster_de_detail(detail: str) -> str:
    m = _RE_RASTER.search(detail or "")
    return m.group(0) if m else ""


# --------------------------------------------------------------------- #
# Génération du dossier à remplir
# --------------------------------------------------------------------- #

def generer_dossier(ecarts_csv: Path, dossier_dir: Path,
                    sortie: Path | None = None) -> Path:
    """Écrit `justifications.md` — une ligne à trancher par désaccord du CSV.

    `--sortie` remplace la destination par défaut
    (`dossier_dir/justifications.md`). Le fichier reste volontairement
    incomplet : preuve et verdict se saisissent sur la source originale,
    au plan. Renvoie le chemin écrit.
    """
    desaccords = lire_ecarts(ecarts_csv)
    sortie = Path(sortie) if sortie is not None else Path(dossier_dir) / "justifications.md"
    L: list[str] = []
    L.append("# Dossier de justification des désaccords")
    L.append("")
    L.append(f"Généré le {date.today().isoformat()} par `src.validation.justifier` "
             f"depuis `{Path(ecarts_csv).name}` — {len(desaccords)} désaccord(s). "
             "Aucune case remplie d'avance : la preuve et le verdict se prennent "
             "sur la source originale (plan, cédule, addenda).")
    L.append("")
    L.append("**Rappels avant de trancher** (étapes 5 et 7 du critère d'acceptation) :")
    L.append("")
    L.append("- **Symétrie IA/estimateur** : chaque désaccord se tranche sur la source "
             "originale, y compris quand c'est l'estimateur qui s'est trompé — une "
             "erreur constatée chez l'estimateur exige elle aussi une preuve sur le "
             "plan, jamais un simple aveu.")
    L.append("- **Une quantité plus élevée seule n'est jamais une amélioration** : "
             "compter plus n'est pas compter mieux ; seul le plan décide.")
    L.append(f"- **Un désaccord sans preuve = non tranché** ; tout verdict exige une "
             f"preuve non vide (« {VERDICT_ESTIMATEUR} » compris).")
    L.append(f"- **Verdicts acceptés** (dernière colonne) : `{VERDICT_IA}`, "
             f"`{VERDICT_ESTIMATEUR}` ou `{VERDICT_AMBIGU}`.")
    compte = Counter(d.classe for d in desaccords)
    L.append("")
    L.append("**Désaccords par classe** : "
             + (", ".join(f"{c} = {n}" for c, n in sorted(compte.items())) or "aucun") + ".")
    if not desaccords:
        L.append("")
        L.append("**Aucun désaccord à justifier** : dossier laissé vide à titre de "
                 "trace déterministe (aucun classement, aucune justification).")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text("\n".join(L), encoding="utf-8")
        return sortie
    L.append("")
    L.append("## Désaccords à justifier")
    L.append("")
    L.append("| classe | libellé humain | libellé IA | feuille | position (x, y) "
             "| preuve sur le plan (à remplir) | verdict (à remplir) |")
    L.append("|---|---|---|---|---|---|---|")
    for d in desaccords:
        raster = _raster_de_detail(d.detail)
        L.append(
            f"| {_echapper(d.classe)} | {_echapper(d.libelle_humain)} "
            f"| {_echapper(d.libelle_ia)} "
            f"| {_echapper(cellule_feuille(d.feuille_humaine, d.feuille_ia, raster))} "
            f"| {_echapper(cellule_position(d.position_humaine, d.position_ia))} "
            f"|  |  |"
        )
    if any(d.detail for d in desaccords):
        L.append("")
        L.append("## Détails fournis par le classement")
        L.append("")
        for d in desaccords:
            if d.detail:
                L.append(f"- {d.classe} · {_echapper(d.detail)}")
    L.append("")
    L.append("## Réserves")
    L.append("")
    L.append("Un désaccord classé « ambigu → réserve » reste un point signalé : "
             "il exige une réserve dans `reserves.md` du relevé, jamais un "
             "silence.")
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text("\n".join(L), encoding="utf-8")
    return sortie


# --------------------------------------------------------------------- #
# Contrôle du dossier rempli
# --------------------------------------------------------------------- #

@dataclass
class RapportJustification:
    """Résultat du contrôle : totaux, lignes fautes listées, état global."""
    lignes: int = 0                       # désaccords du dossier
    tranches: int = 0
    non_tranches: int = 0
    ambigus: int = 0
    sans_preuve: list[str] = field(default_factory=list)
    verdicts_non_reconnus: list[str] = field(default_factory=list)
    lignes_csv_absentes: list[str] = field(default_factory=list)
    details: list[str] = field(default_factory=list)
    cles: list[tuple] = field(default_factory=list)
    etat: str = "INCOMPLET"


def _verdict_canonique(texte: str) -> str:
    v = normaliser(texte)
    v = v.replace("->", " ").replace("=>", " ").replace("→", " ")
    return " ".join(v.split())


_VERDICTS_ACCEPTES = {
    "ia correcte": VERDICT_IA,
    "estimateur correct": VERDICT_ESTIMATEUR,
    "ambigu reserve": VERDICT_AMBIGU,
}


def _cellules(ligne: str) -> list[str]:
    corps = ligne.strip()
    if corps.startswith("|"):
        corps = corps[1:]
    if corps.endswith("|"):
        corps = corps[:-1]
    corps = corps.replace("\\|", "\x00")
    return [c.strip().replace("\x00", "\\|") for c in corps.split("|")]


def _est_separateur(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-+:?", c) or not c for c in cells)


def _lire_tableau_dossier(texte: str, source: Path) -> tuple[dict[str, int], list[list[str]]]:
    """(colonnes par rôle, lignes de données) du tableau des désaccords du dossier."""
    lignes_md = texte.splitlines()
    idx = None
    for i, l in enumerate(lignes_md):
        if not l.lstrip().startswith("|"):
            continue
        if any(normaliser(c) == "classe" for c in _cellules(l)):
            idx = i
            break
    if idx is None:
        raise JustifierErreur(
            f"{source} : tableau des désaccords introuvable (en-tête « classe … »)")
    en_tete = _cellules(lignes_md[idx])
    roles: dict[str, int] = {}
    for j, c in enumerate(en_tete):
        n = normaliser(c)
        if n == "classe":
            roles["classe"] = j
        elif "libelle humain" in n:
            roles["libelle_humain"] = j
        elif "libelle ia" in n:
            roles["libelle_ia"] = j
        elif "feuille" in n:
            roles["feuille"] = j
        elif "position" in n:
            roles["position"] = j
        elif "preuve" in n:
            roles["preuve"] = j
        elif "verdict" in n:
            roles.setdefault("verdict", j)
    manquants = [r for r in ("classe", "libelle_humain", "libelle_ia", "feuille",
                             "position", "preuve", "verdict") if r not in roles]
    if manquants:
        raise JustifierErreur(
            f"{source} : colonnes du tableau introuvables : {', '.join(manquants)}")
    i = idx + 1
    while i < len(lignes_md) and lignes_md[i].lstrip().startswith("|") \
            and _est_separateur(_cellules(lignes_md[i])):
        i += 1
    rangees: list[list[str]] = []
    while i < len(lignes_md) and lignes_md[i].lstrip().startswith("|"):
        cells = _cellules(lignes_md[i])
        i += 1
        if _est_separateur(cells):
            continue
        if not any(cells):
            continue
        rangees.append(cells)
    return roles, rangees


def _cle_dossier(classe: str, libelle_h: str, libelle_ia: str, cellule_pos: str) -> tuple:
    """Clé d'appariement d'une ligne du dossier (sensibilité aux accents)."""
    positions = sorted((float(a), float(b)) for a, b in _RE_COUPLES.findall(cellule_pos))
    return (normaliser(classe), normaliser(libelle_h), normaliser(libelle_ia),
            tuple(positions))


def controler_justifications(path: Path,
                             ecarts_csv: Path | None = None) -> RapportJustification:
    """Contrôle du dossier rempli : totaux, non tranchés, lignes CSV absentes.

    `ecarts_csv` (optionnel) permet la contre-vérification : toute ligne du
    CSV absent du dossier est signalée dans `lignes_csv_absentes`.
    """
    path = Path(path)
    if not path.is_file():
        raise JustifierErreur(f"fichier introuvable : {path}")
    texte = path.read_text(encoding="utf-8-sig")
    rapport = RapportJustification()
    if "aucun desaccord a justifier" in normaliser(texte):
        if ecarts_csv is not None and lire_ecarts(ecarts_csv):
            rap_absent = ("toutes les lignes du CSV sont absentes du dossier "
                          "(dossier « aucun désaccord »)")
            rapport.lignes_csv_absentes.append(rap_absent)
            rapport.details.append(rap_absent)
            rapport.etat = "INCOMPLET"
        else:
            rapport.etat = "COMPLET"
        return rapport
    roles, rangees = _lire_tableau_dossier(texte, path)
    n_cols = 1 + max(roles.values())
    for cells in rangees:
        cells = cells + [""] * (n_cols - len(cells))

        def c(name: str) -> str:
            j = roles.get(name)
            return cells[j] if j is not None and j < len(cells) else ""

        classe = c("classe")
        libelle_h = c("libelle_humain")
        libelle_i = c("libelle_ia")
        cellule_pos = c("position")
        preuve = c("preuve")
        verdict_brut = c("verdict")
        ident = (f"{classe or '?'} · {(libelle_h or libelle_i or '?')}"
                 + (f" ({cellule_pos})" if cellule_pos and cellule_pos != "—" else ""))
        rapport.lignes += 1
        canon = _verdict_canonique(verdict_brut)
        if not verdict_brut or verdict_brut == "—":
            rapport.non_tranches += 1
            rapport.details.append(f"{ident} : verdict vide — désaccord non tranché")
        elif canon not in _VERDICTS_ACCEPTES:
            rapport.non_tranches += 1
            msg = (f"{ident} : verdict « {verdict_brut} » non reconnu (attendus : "
                   f"{VERDICT_IA}, {VERDICT_ESTIMATEUR}, {VERDICT_AMBIGU})")
            rapport.verdicts_non_reconnus.append(msg)
            rapport.details.append(msg)
        elif not preuve or preuve == "—":
            rapport.non_tranches += 1
            msg = f"{ident} : verdict « {verdict_brut} » sans preuve sur le plan — non tranché"
            rapport.sans_preuve.append(msg)
            rapport.details.append(msg)
        else:
            rapport.tranches += 1
            if canon == "ambigu reserve":
                rapport.ambigus += 1
        rapport.cles.append(_cle_dossier(classe, libelle_h, libelle_i, cellule_pos))
    if ecarts_csv is not None:
        desaccords = lire_ecarts(ecarts_csv)
        attendus = Counter(d.cle for d in desaccords)
        couverts = Counter(rapport.cles)
        premiers: dict[tuple, Desaccord] = {}
        for d in desaccords:
            premiers.setdefault(d.cle, d)
        for cle, n in sorted(attendus.items()):
            manque = n - couverts.get(cle, 0)
            if manque > 0:
                desc = _decrire(premiers[cle])
                msg = f"ligne du CSV absente du dossier (×{manque}) : {desc}"
                rapport.lignes_csv_absentes.append(msg)
                rapport.details.append(msg)
    rapport.etat = ("COMPLET" if rapport.non_tranches == 0
                    and not rapport.lignes_csv_absentes else "INCOMPLET")
    return rapport


def _decrire(d: Desaccord) -> str:
    pos = d.position_ia or d.position_humaine or "sans position"
    feuille = d.feuille_ia or d.feuille_humaine or "?"
    return (f"{d.classe} · feuille {feuille} · "
            f"« {d.libelle_humain or d.libelle_ia or '?'} » à {pos}")


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.validation.justifier",
        description="Dossier de justification des désaccords (étapes 5 à 7 du "
                    "critère d'acceptation).",
    )
    sous = p.add_subparsers(dest="commande", required=True)
    g = sous.add_parser("generer", help="écrit justifications.md à remplir")
    g.add_argument("--ecarts", type=Path, required=True,
                   help="ecarts-classes.csv (contrat gelé de classer_ecarts)")
    g.add_argument("--dossier", type=Path, required=True,
                   help="dossier où écrire justifications.md")
    g.add_argument("--sortie", type=Path, default=None,
                   help="remplace la destination (défaut : <dossier>/justifications.md)")
    c = sous.add_parser("controler", help="contrôle un justifications.md rempli")
    c.add_argument("fichier", type=Path, help="justifications.md rempli")
    c.add_argument("--ecarts", type=Path, default=None,
                   help="CSV gelé : signale toute ligne absente du dossier")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.commande == "generer":
            sortie = generer_dossier(args.ecarts, args.dossier, args.sortie)
            print(f"OK : {sortie} — preuve et verdict à remplir par désaccord "
                  "(un désaccord sans preuve = non tranché)")
            return 0
        rapport = controler_justifications(args.fichier, args.ecarts)
    except (JustifierErreur, OSError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    print(f"État : {rapport.etat} — {rapport.lignes} désaccord(s) : "
          f"{rapport.tranches} tranché(s) ({rapport.ambigus} ambigu(s) → réserve), "
          f"{rapport.non_tranches} non tranché(s).")
    for msg in rapport.details:
        print(f"- {msg}")
    return 0 if rapport.etat == "COMPLET" else 1


if __name__ == "__main__":
    raise SystemExit(main())