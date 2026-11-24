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
def _garde_aveugle(rapport, workdir, chemin_qpl):
    """Scanne et gèle sans ouvrir ni connaître l'emplacement de la référence."""
    # --- Étape 1 : aveugle -----------------------------------------------------
    # Revérification en mémoire après le gel : conserver le rapport initial
    # et son SHA-256 pour qu'il reste une preuve d'avant comparaison.
    rapport_av = aveugle.controler(workdir, ecrire=not (workdir / gel.NOM_GEL).is_file())
    if not rapport_av.aveugle:
        noms = ", ".join(r.fichier for r in rapport_av.references_detectees)
        rapport.verdict, rapport.motif = VERDICT_INVALIDE, (
            f"relevé non aveugle : {noms} référence(s) estimateur détectée(s) — "
            "l'identification n'est pas issue des plans seuls (voir controle-aveugle.json)")
        rapport.etapes.append(EtapeAcceptation(
            "controle_aveugle", "échec",
            f"{rapport.motif}; étape 1 violée : l'identification doit venir des plans "
            "et addendas SEULEMENT, la comparaison n'est pas lancée"))
        return False
    rapport.etapes.append(EtapeAcceptation(
        "controle_aveugle", "ok",
        f"{rapport_av.fichiers_scannes} fichier(s) scanné(s), aucune référence estimateur"))

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
            return False
        manifest = gel.lire_gel(workdir)
        rel = Path(os.path.relpath(chemin_qpl, start=workdir)).as_posix() if chemin_qpl else None
        if (manifest.get("soumission") != rapport.soumission or rapport_gel.ajoutes_apres_gel or
                (rel and rel not in {a['fichier'] for a in manifest['artefacts']})):
            rapport.verdict, rapport.motif = VERDICT_INVALIDE, (
                "gel violé : soumission différente, nouvel artefact ou .qpl absent du gel initial")
            rapport.etapes.append(EtapeAcceptation("gel", "échec", rapport.motif))
            return False
        detail_gel = f"gel existant vérifié et intact ({len(manifest['artefacts'])} artefact(s))"
        etat_gel = "intact"
    else:
        gel.geler(workdir, soumission=rapport.soumission)
        if chemin_qpl and not chemin_qpl.is_relative_to(workdir):
            _etendre_gel(workdir, chemin_qpl)
        gel_nouveau = gel.lire_gel(workdir)
        if not gel.verifier_gel(workdir):
            raise gel.GelError("gel nouvellement écrit non vérifiable")
        detail_gel = f"gel écrit et vérifié ({len(gel_nouveau['artefacts'])} artefact(s))"
        etat_gel = "gelé"
    rapport.etapes.append(EtapeAcceptation("gel", etat_gel, detail_gel))
    return True


def executer(soumission: str, workdir, dossier_dir=None, *, qpl_ia=None, gel_seul=False, sortie=None) -> RapportAcceptation:
    """Contrôle aveugle et gel, puis comparaison uniquement si demandée et possible."""
    workdir = Path(workdir).resolve()
    if not workdir.is_dir():
        raise aveugle.AveugleErreur(f"dossier de travail du relevé IA introuvable : {workdir}")
    dossier_dir = Path(dossier_dir).resolve() if dossier_dir else None
    if not gel_seul and (dossier_dir is None or not dossier_dir.is_dir()):
        raise BoucleErreur(f"dossier de la soumission introuvable : {dossier_dir}")
    destination = Path(sortie).resolve() if sortie is not None else dossier_dir
    if not gel_seul and (destination.is_relative_to(workdir) or destination.is_relative_to(dossier_dir / "reference")):
        raise BoucleErreur("La comparaison doit être écrite hors du dossier aveugle et de reference/")
    resolu = None
    if qpl_ia:
        qpl = Path(qpl_ia).resolve()
        if not qpl.is_file() or qpl.suffix.lower() != ".qpl" or any(
                x.casefold() in {"reference", "estimateur"} for x in qpl.parts):
            raise BoucleErreur("--qpl-ia doit désigner la sortie Plan Expert produite à l'aveugle")
        if aveugle.motif_par_chemin(Path(qpl.name)):
            raise BoucleErreur("--qpl-ia désigne un nom réservé à une référence")
        resolu = qpl, ".qpl IA explicite"
    elif dossier_dir and not gel_seul:
        resolu = trouver_qpl_ia(soumission, workdir, dossier_dir)
    elif gel_seul:
        raise BoucleErreur("--gel-seul exige --qpl-ia (aucune référence utilisée)")
    rapport = RapportAcceptation(soumission=soumission)
    if not _garde_aveugle(rapport, workdir, resolu[0] if resolu else None):
        if not gel_seul:
            ecrire_acceptation(rapport, destination, workdir)
        return rapport
    if gel_seul:
        rapport.verdict, rapport.motif = VERDICT_INCOMPLET, "gel seul — aucune comparaison exécutée"
        return rapport

    # --- Étape 3 : comparaison + classification + justifications ----------------
    ref_dir = dossier_dir / "reference"
    courant = workdir / "feuilles.csv"
    chemin_feuilles = courant if courant.is_file() else ref_dir / "feuilles-ia.csv"
    pieces_attendues: dict[str, Path] = {
        f"reference/{soumission}-Dupuis-PlanExpert.qpl": ref_dir / f"{soumission}-Dupuis-PlanExpert.qpl",
        "reference/dupuis-png-dimensions.txt": ref_dir / "dupuis-png-dimensions.txt",
        "inventaire des feuilles IA (feuilles.csv ou reference/feuilles-ia.csv)": chemin_feuilles,
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
        ecrire_acceptation(rapport, destination, workdir)
        return rapport
    chemin_qpl, provenance = resolu

    sortie_dir = destination / "comparaison-dupuis-qpl"
    try:
        dims = cq.lire_dimensions(ref_dir / "dupuis-png-dimensions.txt", soumission)
        feuilles = cq.lire_feuilles(chemin_feuilles)
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
        ecrire_acceptation(rapport, destination, workdir)
        return rapport
    rapport.etapes.append(EtapeAcceptation(
        "comparaison", "ok",
        f"marque par marque (compare_qpl) ; .qpl IA : {provenance} — {chemin_qpl}"))
    rapport.totaux_marques = cq.totaux(comp)
    cq.ecrire_sorties(comp, sortie_dir, {"dossier": soumission, "ia": str(chemin_qpl),
        "humain": str(ref_dir / f"{soumission}-Dupuis-PlanExpert.qpl"),
        "dims": str(ref_dir / "dupuis-png-dimensions.txt"), "feuilles": str(chemin_feuilles)})

    ecarts = classer_ecarts.classer(comp)
    rapport.compteurs = classer_ecarts.ecrire_sorties(ecarts, sortie_dir)
    total_ecarts = sum(rapport.compteurs.values())
    rapport.etapes.append(EtapeAcceptation(
        "classement", "ok",
        f"{total_ecarts} désaccord(s) classé(s) → {sortie_dir / 'ecarts-classes.csv'}"))

    # --- Étapes 5-7 : dossier de justification (généré si absent, jamais écrasé)
    chemin_justif = destination / "justifications.md"
    etat_justif, detail_justif = "", ""
    controle = None
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
                             f"{len(controle.lignes_csv_absentes)} ligne(s) du CSV absente(s), "
                             f"{controle.corrections_requises} correction(s) encore requise(s)")
    else:
        justifier.generer_dossier(sortie_dir / "ecarts-classes.csv", destination)
        etat_justif = "écrit"
        detail_justif = (f"{total_ecarts} désaccord(s) à trancher avec une preuve sur le "
                         "plan (justifications.md)" if total_ecarts
                         else "aucun désaccord à justifier (dossier trace déterministe)")
    rapport.etapes.append(EtapeAcceptation("justifications", etat_justif, detail_justif))

    incomplet = []
    qualite = workdir / "qualite.json"
    if qualite.is_file() and json.loads(qualite.read_text(encoding="utf-8")).get("conforme") is not True:
        incomplet.append("contrôle qualité non conforme")
    if comp.anomalies:
        incomplet.append(f"{len(comp.anomalies)} anomalie(s) de coordonnées ou de référence")
    for nom, cle in (("blocs-a-etiqueter.json", "inconnues"), ("blocs-a-etiqueter.json", "ambigues"),
                     ("blocs-non-relevees.json", "feuilles")):
        p = workdir / nom
        if p.is_file() and json.loads(p.read_text(encoding="utf-8")).get(cle):
            incomplet.append(f"{cle} non résolues ({nom})")
    if controle and (controle.ambigus or controle.corrections_requises):
        incomplet.append(f"{controle.ambigus} ambiguïté(s) ouverte(s), {controle.corrections_requises} erreur(s) IA à corriger")
    if incomplet:
        rapport.etapes.append(EtapeAcceptation("aptitude", "bloquée", "; ".join(incomplet)))
    if incomplet and (not total_ecarts or etat_justif == "COMPLET"):
        rapport.verdict, rapport.motif = VERDICT_JUSTIF, "; ".join(incomplet) + " — corriger et revérifier avant décision"
    elif etat_justif == "COMPLET":
        rapport.verdict, rapport.motif = VERDICT_PRET, (
            "vérification complète : relevé aveugle, gel intact, comparaison faite "
            "et chaque désaccord tranché avec une preuve sur le plan")
    elif total_ecarts:
        rapport.verdict, rapport.motif = VERDICT_JUSTIF, (
            f"{total_ecarts} désaccord(s) non tranché(s) : chaque désaccord exige une "
            "preuve sur la source originale (plan, cédule, addenda) — étapes 5 à 7")
    else:
        rapport.verdict, rapport.motif = VERDICT_PRET, (
            "vérification complète, aucun désaccord entre le relevé aveugle gélé et le "
            "relevé de l'estimateur — décision finale à Francis")

    ecrire_acceptation(rapport, destination, workdir)
    return rapport


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
    p.add_argument("--dossier", type=Path,
                   help="dossier de la soumission dans le dépôt (dossiers/<S>, référence + sorties)")
    p.add_argument("--sortie", type=Path, help="écrire la comparaison hors du dossier de référence")
    p.add_argument("--qpl-ia", type=Path, help="projet Plan Expert IA exact à geler/comparer")
    p.add_argument("--gel-seul", action="store_true", help="contrôler et geler sans accéder à une référence")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rapport = executer(args.soumission, args.workdir, args.dossier, qpl_ia=args.qpl_ia,
                           gel_seul=args.gel_seul, sortie=args.sortie)
    except (aveugle.AveugleErreur, gel.GelError, BoucleErreur, justifier.JustifierErreur, OSError) as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    for e in rapport.etapes:
        print(f"- {e.nom} : {e.etat} — {e.detail}")
    print(f"verdict : {rapport.verdict} — {rapport.motif}")
    print(f"VERDICT : {rapport.verdict}")     # ligne machine-lisible (run.py, outils)
    return 0 if rapport else 1


if __name__ == "__main__":
    from src.validation.console import forcer_utf8

    forcer_utf8()
    sys.exit(main())