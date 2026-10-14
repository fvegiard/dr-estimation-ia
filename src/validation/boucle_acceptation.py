"""
Orchestrateur de la boucle d'acceptation — chaîne complète « relevé IA accepté
ou rejeté » du critère d'acceptation (CLAUDE.md, étapes 1 à 8). Le module
assemble les quatre étapes déterministes déjà écrites, sans en modifier une
seule : chaque verdict est calculé, jamais récitée par un agent.

Chaîne (s'arrête au premier refus ; l'étape de comparaison n'appelle JAMAIS
`compare_qpl` si le relevé n'est pas aveugle ou si le gel est violé) :

1. `aveugle.controler(workdir)` — relevé IA sans aucune trace du matériau de
   l'estimateur. Non aveugle → arrêt, verdict INVALIDE (étape 1).
2. gel : `gel.json` absent → `gel.geler(workdir)` ; présent →
   `gel.verifier_gel(workdir)`. Violé → INVALIDE « gel violé » (étape 2).
   Si le .qpl IA retenu pour la comparaison vit HORS du dossier de travail
   (dossier assemblé : `dossiers/<S>/planexpert/<S>.qpl`), son empreinte
   sha256 est ajoutée au gel — comparer un fichier non gélé n'est pas
   possible, qu'importe son emplacement.
3. comparaison — si `dossier_dir/reference/` contient les trois pièces de
   l'estimateur (`<S>-Dupuis-PlanExpert.qpl`, `dupuis-png-dimensions.txt`,
   `feuilles-ia.csv`) ET que le `.qpl` IA existe (`.qpl` du dossier de
   travail, sinon `dossiers/<S>/planexpert/<S>.qpl`) :
   `compare_qpl.comparer` → `classer_ecarts.classer` →
   `classer_ecarts.ecrire_sorties` → `justifier.generer_dossier`.
   Une pièce manquante, illisible ou une comparaison en échec →
   VÉRIFICATION INCOMPLÈTE (étape 8 : jamais « pas pire que l'estimateur »
   sans vérification complète).
4. `ACCEPTATION.md` écrit dans `dossier_dir` : étapes ok/échec, compteurs
   par classe, verdict final ∈ {INVALIDE, VÉRIFICATION INCOMPLÈTE,
   JUSTIFICATIONS REQUISES, PRÊT POUR DÉCISION FRANCIS}.

Verdicts :
- INVALIDE — relevé non aveugle, ou gel violé (les désaccords ne seraient
  plus ceux du relevé d'origine) ;
- VÉRIFICATION INCOMPLÈTE — référence de l'estimateur absente, incomplète ou
  illisible, ou comparaison en échec : rien n'est prouvé dans un sens ni dans
  l'autre ;
- JUSTIFICATIONS REQUISES — la comparaison a produit des désaccords et le
  dossier `justifications.md` n'est pas entièrement tranché (ou n'existe pas
  encore) : chaque désaccord exige une preuve sur le plan (étapes 5-7) ;
- PRÊT POUR DÉCISION FRANCIS — vérification complète : relevé aveugle, gel
  intact, comparaison faite, aucun désaccord à trancher (soit aucun écart,
  soit un dossier de justification entièrement rempli). Le verdict FINAL
  reste à Francis : ce verdict ouvre la décision, il ne la remplace pas.

Sorties écrites :
- workdir : `controle-aveugle.json`, `gel.json` (modules aveugle/gel) ;
- dossier_dir : `comparaison-dupuis-qpl/` (sorties de compare_qpl et de
  classer_ecarts, dont `ecarts-classes.csv` — contrat gelé), `justifications.md`,
  `ACCEPTATION.md`.

Le dossier_dir n'est JAMAIS le dossier de travail : il contient les pièces du
relevé humain (reference/) et les rapports citant l'estimateur ; le scan
« à l'aveugle » ne porte que sur le workdir du relevé IA.

CLI :
  python -m src.validation.boucle_acceptation S-1844 --workdir W --dossier D

Codes de sortie : 0 = PRÊT POUR DÉCISION FRANCIS ou VÉRIFICATION INCOMPLÈTE
(la boucle n'a rien à redire), 1 = INVALIDE ou JUSTIFICATIONS REQUISES
(désaccord non tranché), 2 = erreur d'entrée (workdir/dossier introuvable,
gel illisible). La dernière ligne de la sortie est « VERDICT : … ».
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from src.validation import aveugle, classer_ecarts, gel, justifier
from src.validation import compare_qpl as cq

NOM_RAPPORT = "ACCEPTATION.md"

VERDICT_INVALIDE = "INVALIDE"
VERDICT_INCOMPLET = "VÉRIFICATION INCOMPLÈTE"
VERDICT_JUSTIF = "JUSTIFICATIONS REQUISES"
VERDICT_PRET = "PRÊT POUR DÉCISION FRANCIS"

# Sorte de INVALIDE portée par son motif : le gel violé doit rester lisible
# tel quel dans ACCEPTATION.md et sur la console.
MOTIF_GEL_VIOLE = "gel violé"

PIECES_REFERENCE = "référence de l'estimateur (reference/)"

# Le verdict final d'ACCEPTATION.md — ligne unique, machine-lisible
# (lu par releve/run.py et src.validation.jeu_reference).
RE_VERDICT = re.compile(r"\*\*Verdict : (.+?)\*\*")


class BoucleErreur(Exception):
    """Entrée illisible pour la boucle (workdir/dossier indus, gel illisible)."""


@dataclass
class EtapeAcceptation:
    """Une étape de la boucle : nom, état (« ok », « échec », « non exécutée »), détail."""
    nom: str
    etat: str = "ok"
    detail: str = ""


@dataclass
class RapportAcceptation:
    """Résultat de la boucle : verdict, motif, étapes, compteurs. Le statut
    booléen (`__bool__`) suit le critère d'acceptation : vrai seulement si
    rien n'oppose à poursuivre (PRÊT ou VÉRIFICATION INCOMPLÈTE — rien à
    corriger dans le relevé) ; INVALIDE et JUSTIFICATIONS REQUISES sont faux."""
    soumission: str
    verdict: str = ""
    motif: str = ""                                  # raison exacte du verdict (ex. : gel violé)
    etapes: list[EtapeAcceptation] = field(default_factory=list)
    compteurs: dict[str, int] = field(default_factory=dict)   # désaccords par classe
    totaux_marques: dict[str, int] = field(default_factory=dict)
    date: str = date.today().isoformat()

    def __bool__(self) -> bool:
        return self.verdict in (VERDICT_PRET, VERDICT_INCOMPLET)

    def vers_md(self, workdir: Path | None = None) -> str:
        """ACCEPTATION.md — étapes ok/échec, compteurs par classe, verdict."""
        L: list[str] = [f"# Acceptation — relevé IA « {self.soumission} »", ""]
        L.append(f"_Généré le {self.date} par `src.validation.boucle_acceptation` "
                 "(critère d'acceptation de CLAUDE.md, étapes 1 à 8). "
                 "Toutes les étapes sont calculées, aucune n'est rapportée sur foi d'un agent._")
        L.append("")
        L.append(f"**Verdict : {self.verdict}**")
        if self.motif:
            L.append(f"Motif : {self.motif}")
        L.append("")
        L.append("| étape | état | détail |")
        L.append("|---|---|---|")
        for e in self.etapes:
            L.append(f"| {e.nom} | {e.etat} | {e.detail.replace('|', chr(92) + '|')} |")
        L.append("")
        L.append("## Compteurs par classe")
        L.append("")
        if self.compteurs:
            L.append("| classe | nombre |")
            L.append("|---|--:|")
            total = 0
            for classe in classer_ecarts.CLASSES:
                n = self.compteurs.get(classe, 0)
                total += n
                if n:
                    L.append(f"| {classe} | {n} |")
            L.append(f"| **total** | **{total}** |")
        elif any(e.nom == "classement" for e in self.etapes):
            L.append("Comparaison exécutée : aucun désaccord classé.")
        else:
            L.append("Comparaison non exécutée : aucun compteur.")
        if self.totaux_marques:
            t = self.totaux_marques
            L.append("")
            L.append(f"Marques humaines uniques {t.get('humaines', 0)} · marques IA "
                     f"{t.get('ia', 0)} · appariées {t.get('appariees', 0)} · "
                     f"manquantes IA {t.get('manquantes', 0)} · en trop IA {t.get('en_trop', 0)}.")
        L.append("")
        if self.verdict == VERDICT_INCOMPLET:
            L.append("Vérification incomplète (étape 8) : tant que la référence de "
                     "l'estimateur est absente, incomplète ou illisible — ou que la "
                     "comparaison est en échec — il est impossible de certifier « pas "
                     "pire que l'estimateur ». L'absence de preuve n'est pas une preuve "
                     "d'absence de régression : ne pas déclarer ce relevé acceptable.")
            L.append("")
        if self.verdict == VERDICT_JUSTIF:
            L.append("Chaque désaccord ci-dessus doit être tranché dans `justifications.md` "
                     "avec une preuve sur la source originale (plan, cédule, addenda), "
                     "y compris quand c'est l'estimateur qui s'est trompé (étape 5). "
                     "Une quantité plus élevée seule n'est jamais une amélioration (étape 7).")
            L.append("")
        if self.verdict == VERDICT_PRET:
            L.append("Vérification complète : contrôle aveugle passé, gel intact, "
                     "comparaison faite, aucun désaccord non tranché. La décision finale "
                     "reste à Francis — ce verdict ouvre la décision, il ne la remplace pas.")
            L.append("")
        if workdir is not None:
            L.append(f"Dossier de travail du relevé IA (controlé à l'aveugle, gelé) : `{workdir}`.")
            L.append("")
        return "\n".join(L)


def ecrire_acceptation(rapport: RapportAcceptation, dossier_dir: Path,
                       workdir: Path | None = None) -> Path:
    """Écrit `ACCEPTATION.md` dans `dossier_dir` et retourne son chemin."""
    chemin = Path(dossier_dir) / NOM_RAPPORT
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(rapport.vers_md(workdir), encoding="utf-8")
    return chemin


# --------------------------------------------------------------------- #
# Résolution du .qpl IA
# --------------------------------------------------------------------- #

def trouver_qpl_ia(soumission: str, workdir: Path, dossier_dir: Path) -> tuple[Path, str] | None:
    """`.qpl` IA à comparer : d'abord tout `.qpl` produit dans le dossier de
    travail (il sera gélé par `gel.geler`/`gel.verifier_gel`), à défaut le
    projet assemblé `dossiers/<S>/planexpert/<S>.qpl`. Retourne (chemin,
    provenance) ou None. Un `.qpl` placé sous un dossier `reference/` est
    ignoré — c'est du matériau de l'estimateur, jamais la sortie IA."""
    candidats = [
        p for p in sorted(workdir.rglob("*.qpl"))
        if "reference" not in {part.lower() for part in p.relative_to(workdir).parts[:-1]}
    ]
    if candidats:
        return candidats[0], "dossier de travail"
    assemblé = dossier_dir / "planexpert" / f"{soumission}.qpl"
    if assemblé.is_file():
        return assemblé, "dossier assemblé (planexpert/)"
    return None


def _etendre_gel(workdir: Path, qpl_ia: Path) -> str:
    """Agrandit le gel au .qpl IA quand il vit hors du dossier de travail
    (dossier assemblé) : son empreinte sha256 rejoint les artefacts de
    gel.json — `gel.verifier_gel` la revérifie à chaque relance. Le .qpl
    déjà couvert (dans le workdir) est signalé sans réécriture."""
    relatif = Path(os.path.relpath(qpl_ia, start=workdir)).as_posix()
    chemin_gel = workdir / gel.NOM_GEL
    try:
        contenu = json.loads(chemin_gel.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise gel.GelError(f"{chemin_gel} illisible : {exc}") from exc
    if not isinstance(contenu, dict) or not isinstance(contenu.get("artefacts"), list):
        raise gel.GelError(f"{chemin_gel} mal formé : « artefacts » (liste) introuvable")
    if any(isinstance(a, dict) and a.get("fichier") == relatif for a in contenu["artefacts"]):
        return "déjà couvert par le gel"
    from src.validation.gel import _sha256 as sha256_gel   # empreinte identique au gel lui-même
    contenu["artefacts"].append({
        "fichier": relatif,
        "sha256": sha256_gel(qpl_ia),
        "octets": qpl_ia.stat().st_size,
    })
    chemin_gel.write_text(json.dumps(contenu, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return "ajouté au gel"


# --------------------------------------------------------------------- #
# Boucle
# --------------------------------------------------------------------- #

def executer(soumission: str, workdir, dossier_dir) -> RapportAcceptation:
    """Enchaîne aveugle → gel → comparaison → classification → justifications,
    écrit `ACCEPTATION.md` (dossier_dir) et retourne le rapport. La comparaison
    n'est lancée que sur un relevé à l'aveugle au gel intact ; une référence
    manquante/incomplète/illisible donne VÉRIFICATION INCOMPLÈTE, jamais un
    « pas pire que l'estimateur » tacite."""
    workdir = Path(workdir)
    dossier_dir = Path(dossier_dir)
    if not workdir.is_dir():
        raise aveugle.AveugleErreur(
            f"dossier de travail du relevé IA introuvable : {workdir} (le scan à "
            "l'aveugle n'a rien à scanner)")
    if not dossier_dir.is_dir():
        raise BoucleErreur(
            f"dossier de la soumission introuvable : {dossier_dir} (les rapports "
            "d'acceptation s'écrivent à côté de reference/)")

    rapport = RapportAcceptation(soumission=soumission)

    # --- Étape 1 : aveugle -----------------------------------------------------
    rapport_av = aveugle.controler(workdir)      # écrit controle-aveugle.json
    if not rapport_av.aveugle:
        noms = ", ".join(r.fichier for r in rapport_av.references_detectees)
        rapport.verdict, rapport.motif = VERDICT_INVALIDE, (
            f"relevé non aveugle : {noms} référence(s) estimateur détectée(s) — "
            "l'identification n'est pas issue des plans seuls (voir controle-aveugle.json)")
        rapport.etapes.append(EtapeAcceptation(
            "controle_aveugle", "échec",
            f"{rapport.motif}; étape 1 violée : l'identification doit venir des plans "
            "et addendas SEULEMENT, la comparaison n'est pas lancée"))
        ecrire_acceptation(rapport, dossier_dir, workdir)
        return rapport
    rapport.etapes.append(EtapeAcceptation(
        "controle_aveugle", "ok",
        f"{rapport_av.fichiers_scannes} fichier(s) scanné(s), aucune référence estimateur"))

    # --- Résolution du .qpl IA (AVANT le gel : le gel doit le couvrir) ---------
    resolu = trouver_qpl_ia(soumission, workdir, dossier_dir)

    # --- Étape 2 : gel (« geler ce premier résultat avant toute comparaison ») --
    chemin_gel = workdir / gel.NOM_GEL
    if chemin_gel.is_file():
        rapport_gel = gel.verifier_gel(workdir)          # relance : gel revérifié
        if not rapport_gel:
            detail = "; ".join(
                [f"{len(rapport_gel.modifies)} modifié(s): {', '.join(rapport_gel.modifies)}",
                 f"{len(rapport_gel.manquants)} disparu(s): {', '.join(rapport_gel.manquants)}"])
            rapport.verdict, rapport.motif = VERDICT_INVALIDE, (
                "gel violé : le relevé IA n'est plus le résultat « à l'aveugle » "
                f"gelé d'origine ({detail}) — annuler les retouches post-gel ou faire "
                "un nouveau relevé, puis regeler AVANT toute comparaison")
            rapport.etapes.append(EtapeAcceptation("gel", "échec", f"gel violé — {detail}"))
            ecrire_acceptation(rapport, dossier_dir, workdir)
            return rapport
        detail_gel = f"gel existant vérifié et intact ({len(gel.lire_gel(workdir)['artefacts'])} artefact(s))"
        etat_gel = "intact"
    else:
        gel.geler(workdir, soumission=soumission)        # première exécution : gel écrit
        gel_nouveau = gel.lire_gel(workdir)
        detail_gel = f"gel écrit ({len(gel_nouveau['artefacts'])} artefact(s))"
        etat_gel = "gelé"
    if resolu is not None:
        chemin_qpl, provenance = resolu
        if not chemin_qpl.is_relative_to(workdir):
            detail_gel += f" ; {chemin_qpl.name} {_etendre_gel(workdir, chemin_qpl)}"
    rapport.etapes.append(EtapeAcceptation("gel", etat_gel, detail_gel))

    # --- Étape 3 : comparaison + classification + justifications ----------------
    ref_dir = dossier_dir / "reference"
    pieces_attendues: dict[str, Path] = {
        f"reference/{soumission}-Dupuis-PlanExpert.qpl": ref_dir / f"{soumission}-Dupuis-PlanExpert.qpl",
        "reference/dupuis-png-dimensions.txt": ref_dir / "dupuis-png-dimensions.txt",
        "reference/feuilles-ia.csv": ref_dir / "feuilles-ia.csv",
    }
    if resolu is None:
        pieces_attendues[".qpl IA (dossier de travail ou planexpert/)"] = Path("")
    manquantes = [rel for rel, p in pieces_attendues.items() if not str(p) or not p.is_file()]
    if manquantes:
        rapport.verdict, rapport.motif = VERDICT_INCOMPLET, (
            f"pièce(s) de la comparaison absente(s) : {', '.join(manquantes)} — "
            "VÉRIFICATION INCOMPLÈTE, jamais « pas pire que l'estimateur » sans "
            "vérification complète (étape 8)")
        rapport.etapes.append(EtapeAcceptation(
            "comparaison", "non exécutée",
            f"pièce(s) absente(s) : {', '.join(manquantes)}"))
        ecrire_acceptation(rapport, dossier_dir, workdir)
        return rapport
    chemin_qpl, provenance = resolu

    sortie_dir = dossier_dir / "comparaison-dupuis-qpl"
    try:
        dims = cq.lire_dimensions(ref_dir / "dupuis-png-dimensions.txt", soumission)
        feuilles = cq.lire_feuilles(ref_dir / "feuilles-ia.csv")
        humains = cq.lire_qpl(ref_dir / f"{soumission}-Dupuis-PlanExpert.qpl", "humain")
        ias = cq.lire_qpl(chemin_qpl, "ia")
        cq.preparer_humain(humains, dims)
        anomalies = cq.preparer_ia(ias, feuilles, chemin_qpl.parent)
        comp = cq.comparer(humains, ias, anomalies)
    except (cq.CompareErreur, OSError, ValueError) as exc:
        rapport.verdict, rapport.motif = VERDICT_INCOMPLET, (
            f"comparaison en échec : {exc} — les pièces existent mais la comparaison "
            "marque par marque n'a pas pu être produite (VÉRIFICATION INCOMPLÈTE, "
            "jamais « pas pire que l'estimateur »)")
        rapport.etapes.append(EtapeAcceptation(
            "comparaison", "échec", f"{provenance} : {chemin_qpl} — {exc}"))
        ecrire_acceptation(rapport, dossier_dir, workdir)
        return rapport
    rapport.etapes.append(EtapeAcceptation(
        "comparaison", "ok",
        f"marque par marque (compare_qpl) ; .qpl IA : {provenance} — {chemin_qpl}"))
    rapport.totaux_marques = cq.totaux(comp)

    ecarts = classer_ecarts.classer(comp)
    rapport.compteurs = classer_ecarts.ecrire_sorties(ecarts, sortie_dir)
    total_ecarts = sum(rapport.compteurs.values())
    rapport.etapes.append(EtapeAcceptation(
        "classement", "ok",
        f"{total_ecarts} désaccord(s) classé(s) → {sortie_dir / 'ecarts-classes.csv'}"))

    # --- Étapes 5-7 : dossier de justification (généré si absent, jamais écrasé)
    chemin_justif = dossier_dir / "justifications.md"
    etat_justif, detail_justif = "", ""
    if chemin_justif.is_file():
        try:
            controle = justifier.controler_justifications(chemin_justif,
                                                          sortie_dir / "ecarts-classes.csv")
        except (justifier.JustifierErreur, OSError) as exc:
            etat_justif = "échec"
            detail_justif = f"dossier existant illisible ou hors contrat : {exc} — à reprendre"
        else:
            etat_justif = controle.etat
            detail_justif = (f"{controle.tranches} tranché(s), {controle.non_tranches} non "
                             f"tranché(s), {controle.ambigus} ambigu(s) → réserve ; "
                             f"{len(controle.lignes_csv_absentes)} ligne(s) du CSV absente(s)")
    else:
        justifier.generer_dossier(sortie_dir / "ecarts-classes.csv", dossier_dir)
        etat_justif = "écrit"
        detail_justif = (f"{total_ecarts} désaccord(s) à trancher avec une preuve sur le "
                         "plan (justifications.md)" if total_ecarts
                         else "aucun désaccord à justifier (dossier trace déterministe)")
    rapport.etapes.append(EtapeAcceptation("justifications", etat_justif, detail_justif))

    n_ambigus = _ambigus(dossier_dir)
    if chemin_justif.is_file() and etat_justif == "COMPLET":
        rapport.verdict, rapport.motif = VERDICT_PRET, (
            "vérification complète : relevé aveugle, gel intact, comparaison faite "
            "et chaque désaccord tranché avec une preuve sur le plan"
            + (f", dont {n_ambigus} ambigu(s) → réserve" if n_ambigus else ""))
    elif total_ecarts:
        rapport.verdict, rapport.motif = VERDICT_JUSTIF, (
            f"{total_ecarts} désaccord(s) non tranché(s) : chaque désaccord exige une "
            "preuve sur la source originale (plan, cédule, addenda) — étapes 5 à 7")
    else:
        rapport.verdict, rapport.motif = VERDICT_PRET, (
            "vérification complète, aucun désaccord entre le relevé aveugle gélé et le "
            "relevé de l'estimateur — décision finale à Francis")

    ecrire_acceptation(rapport, dossier_dir, workdir)
    return rapport


def _ambigus(dossier_dir: Path) -> int:
    """Nombre de désaccords « ambigu » d'un dossier rempli — d'après le
    dossier lui-même (lecture du contrôle), 0 en cas de lecture impossible."""
    try:
        return justifier.controler_justifications(
            dossier_dir / "justifications.md").ambigus
    except (justifier.JustifierErreur, OSError):
        return 0


def verdict_acceptation(dossier_dir) -> str | None:
    """Verdict d'un `ACCEPTATION.md` existant (regex `**Verdict : …**`),
    None si le fichier est absent — lecture seule, pour `jeu_reference`."""
    p = Path(dossier_dir) / NOM_RAPPORT
    if not p.is_file():
        return None
    m = RE_VERDICT.search(p.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else None


# --------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.validation.boucle_acceptation",
        description=("Boucle d'acceptation : aveugle → gel → comparaison → "
                     "classification → justifications → ACCEPTATION.md "
                     "(critère d'acceptation de CLAUDE.md, étapes 1 à 8)."),
    )
    p.add_argument("soumission", type=str, help="nom de la soumission (ex. S-1844)")
    p.add_argument("--workdir", required=True, type=Path,
                   help="dossier de travail du relevé IA (nomenclature.csv, occurrences…)")
    p.add_argument("--dossier", required=True, type=Path,
                   help="dossier de la soumission dans le dépôt (dossiers/<S>, référence + sorties)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rapport = executer(args.soumission, args.workdir, args.dossier)
    except (aveugle.AveugleErreur, gel.GelError, BoucleErreur, justifier.JustifierErreur, OSError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    for e in rapport.etapes:
        print(f"- {e.nom} : {e.etat} — {e.detail}")
    print(f"verdict : {rapport.verdict} — {rapport.motif}")
    print(f"VERDICT : {rapport.verdict}")     # ligne machine-lisible (run.py, outils)
    return 0 if rapport else 1


if __name__ == "__main__":
    sys.exit(main())