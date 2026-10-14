"""Test bout en bout (e2e) de la boucle d'acceptation — TOUT passe par le CLI
`python -m src.validation.boucle_acceptation S-TEST --workdir W --dossier D`
(subprocess, cwd = racine du dépôt, aucune donnée client, aucun fichier hors
dépôt). Le module `src.validation.boucle_acceptation` n'est jamais importé
ici : on vérifie le comportement observable d'un vrai processus.

Fixtures synthétiques : mini-dossier S-TEST d'après « Ajouter un dossier » de
CLAUDE.md —

- workdir du relevé IA : `nomenclature.csv`, `occurrences-texte.csv`,
  `feuilles-classement.csv`, `reserves.md` + un petit `.qpl` IA ;
- `dossiers/S-TEST/reference/` : mini `.qpl` Dupuis
  (`S-TEST-Dupuis-PlanExpert.qpl`), `dupuis-png-dimensions.txt`,
  `feuilles-ia.csv` ;
- 3 marques IA appariées, 1 marque humaine en plus → 1 omission classée →
  verdict JUSTIFICATIONS REQUISES (exit 1).

Propriétés vérifiées sur disque :
1. boucle complète → chaque artefact présent et non vide :
   `controle-aveugle.json`, `gel.json`, `comparaison-dupuis-qpl/`
   (`ecarts-classes.csv` au contrat gelé, `ecarts-classes.md`),
   `justifications.md`, `ACCEPTATION.md` ;
2. propriété clé : modifier le `.qpl` IA APRÈS le gel puis relancer →
   INVALIDE « gel violé », exit 1, et la comparaison n'est PAS relancée
   (`comparaison-dupuis-qpl/` byte-identique, justifications.md intact) ;
3. référence absente → VÉRIFICATION INCOMPLÈTE, exit 0, comparaison jamais
   créée ;
4. dossier de justification tranché → relance PRÊT POUR DÉCISION FRANCIS,
   exit 0.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

EN_TETE_CONTRAT = [
    "classe", "feuille_humaine", "feuille_ia", "libelle_humain",
    "libelle_ia", "position_humaine", "position_ia", "detail",
]

# Artefacts attendus, relatifs au dossier de la soumission (acceptation) et au
# workdir du relevé IA (contrôle aveugle et gel — contrat des modules aveugle/gel).
ARTÉFACTS_DOSSIER = (
    "comparaison-dupuis-qpl/ecarts-classes.csv",
    "comparaison-dupuis-qpl/ecarts-classes.md",
    "justifications.md",
    "ACCEPTATION.md",
)
ARTÉFACTS_WORKDIR = ("controle-aveugle.json", "gel.json")


def _qpl(plans: list[tuple[str, str, list[tuple[str, int, int]]]]) -> str:
    """plans : (Name, FileName, [(libellé, x, y)]) → XML Plan Expert minimal."""
    corps = []
    for nom, fichier, marques in plans:
        par: dict[str, list[tuple[int, int]]] = {}
        for lib, x, y in marques:
            par.setdefault(lib, []).append((x, y))
        compteurs = ""
        for gid, (lib, pts) in enumerate(par.items(), start=1):
            elements = "".join(
                f'<Element X="{x}" Y="{y}" Width="20" Height="20"/>' for x, y in pts)
            compteurs += f'<Counter Name="{lib}" GroupID="{gid}">{elements}</Counter>'
        corps.append(f'<Plan Name="{nom}" FileName="{fichier}"><Layers>'
                     f'<Layer Index="0" Name="Calque">{compteurs}</Layer></Layers></Plan>')
    return ('<?xml version="1.0"?><QuoterPlanSession><Project Name="synthetique"/>'
            f'<Plans>{"".join(corps)}</Plans></QuoterPlanSession>')


# 3 marques IA ; le relevé humain posé à l'échelle 2 (raster 2000×1400 vu dans
# un raster IA 1000×700, recalage identité 0,5) + 1 marque en plus → omission.
GRILLE_IA = [("PRISE", 150, 150), ("PRISE", 240, 150), ("PRISE", 330, 150)]
GRILLE_HU = [(lib, 2 * x, 2 * y) for lib, x, y in GRILLE_IA] + [("PRISE", 1600, 1200)]


def _fabriquer(d: Path, *, avec_reference: bool = True) -> dict[str, Path]:
    """Mini-dossier S-TEST : workdir du relevé IA + référence de l'estimateur
    (qpl Dupuis, dimensions des PNG humains, feuilles-ia.csv)."""
    workdir = d / "OUTBOX" / "S-TEST" / "travail"
    workdir.mkdir(parents=True)
    dossier = d / "dossiers" / "S-TEST"
    ref = dossier / "reference"
    ref.mkdir(parents=True)
    (workdir / "nomenclature.csv").write_text("libelle,quantite\nPRISE,3\n", encoding="utf-8")
    (workdir / "occurrences-texte.csv").write_text(
        "feuille,libelle,x,y\nE100,PRISE,150,150\n", encoding="utf-8")
    (workdir / "feuilles-classement.csv").write_text(
        "feuille,classement_fichier\nE100,plans\n", encoding="utf-8")
    (workdir / "reserves.md").write_text("Aucune reserve.\n", encoding="utf-8")
    (workdir / "S-TEST.qpl").write_text(_qpl([("E100", "E100.png", GRILLE_IA)]),
                                        encoding="utf-8")
    if avec_reference:
        (ref / "S-TEST-Dupuis-PlanExpert.qpl").write_text(
            _qpl([("PLANS-TEST - 1", "PLANS-TEST - 1.png", GRILLE_HU)]), encoding="utf-8")
        (ref / "dupuis-png-dimensions.txt").write_text(
            "S-TEST|PLANS-TEST - 1.png|2000|1400\n", encoding="utf-8")
        with (ref / "feuilles-ia.csv").open("w", encoding="utf-8", newline="") as flux:
            w = csv.writer(flux)
            w.writerow(["feuille", "fichier", "page", "largeur_pt", "hauteur_pt",
                        "raster_px", "classement_fichier"])
            w.writerow(["E100", "PLANS-TEST.pdf", "1", "1000", "700", "1000x700", "plans"])
    return {"workdir": workdir, "dossier": dossier, "ref": ref}


def _lancer_boucle(workdir: Path, dossier: Path) -> subprocess.CompletedProcess:
    """Une exécution complète de la boucle par son CLI officiel (subprocess)."""
    return subprocess.run(
        [sys.executable, "-m", "src.validation.boucle_acceptation", "S-TEST",
         "--workdir", str(workdir), "--dossier", str(dossier)],
        cwd=ROOT, capture_output=True, text=True)


def _verdict(p: subprocess.CompletedProcess) -> str:
    """Dernière ligne de sortie = verdict machine-lisible `VERDICT : …`."""
    lignes = p.stdout.splitlines()
    assert lignes, f"sortie vide — stderr={p.stderr}"
    assert lignes[-1].startswith("VERDICT : "), f"dernière ligne sans verdict : {lignes[-1]}"
    return lignes[-1].removeprefix("VERDICT : ").strip()


def _exiger(p: subprocess.CompletedProcess, code: int, verdict: str) -> None:
    assert p.returncode == code, f"exit {p.returncode} ≠ {code}\nstdout={p.stdout}\nstderr={p.stderr}"
    assert _verdict(p) == verdict


def _exiger_non_vide(chemin: Path) -> None:
    assert chemin.is_file(), f"artefact absent : {chemin}"
    assert chemin.stat().st_size > 0, f"artefact vide : {chemin}"


def test_e2e_boucle_complete_artefacts_sur_disque(tmp_path):
    """Boucle complète via CLI : chacun des six artefacts présent et non vide,
    verdict JUSTIFICATIONS REQUISES (exit 1), désaccord classé au contrat gelé."""
    f = _fabriquer(tmp_path)
    p = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p, 1, "JUSTIFICATIONS REQUISES")
    for rel in ARTÉFACTS_DOSSIER:
        _exiger_non_vide(f["dossier"] / rel)
    for rel in ARTÉFACTS_WORKDIR:
        _exiger_non_vide(f["workdir"] / rel)
    av = json.loads((f["workdir"] / "controle-aveugle.json").read_text(encoding="utf-8"))
    assert av["aveugle"] is True and av["fichiers_scannes"] > 0
    gel = json.loads((f["workdir"] / "gel.json").read_text(encoding="utf-8"))
    gelés = {a["fichier"] for a in gel["artefacts"]}
    assert {"nomenclature.csv", "occurrences-texte.csv", "feuilles-classement.csv",
            "reserves.md", "S-TEST.qpl"} <= gelés
    with (f["dossier"] / "comparaison-dupuis-qpl" / "ecarts-classes.csv").open(
            encoding="utf-8", newline="") as flux:
        lignes = list(csv.reader(flux))
    assert lignes[0] == EN_TETE_CONTRAT
    assert [l[0] for l in lignes[1:]] == ["omission"]
    assert lignes[1][2] == "E100" and "PRISE" in lignes[1]
    md = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : JUSTIFICATIONS REQUISES**" in md
    justif = (f["dossier"] / "justifications.md").read_text(encoding="utf-8")
    assert "omission" in justif and "PRISE" in justif


def test_e2e_qpl_ia_modifie_apres_gel_invalide(tmp_path):
    """PROPRIÉTÉ CLÉ : modifier le .qpl IA APRÈS le gel puis relancer →
    INVALIDE « gel violé » (exit 1), et la comparaison n'est pas relancée
    (comparaison-dupuis-qpl/ byte-identique, justifications.md intact)."""
    f = _fabriquer(tmp_path)
    p1 = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p1, 1, "JUSTIFICATIONS REQUISES")
    sortie = f["dossier"] / "comparaison-dupuis-qpl"
    avant = {q.name: q.read_bytes() for q in sorted(sortie.iterdir())}
    justif_avant = (f["dossier"] / "justifications.md").read_bytes()

    qpl_ia = f["workdir"] / "S-TEST.qpl"
    qpl_ia.write_text(
        _qpl([("E100", "E100.png", GRILLE_IA + [("PRISE", 420, 150)])]),
        encoding="utf-8")   # retouche post-gel du relevé IA
    p2 = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p2, 1, "INVALIDE")
    assert "gel violé" in p2.stdout
    assert "S-TEST.qpl" in p2.stdout        # l'artefact fautif est nommé
    md = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : INVALIDE**" in md and "gel violé" in md
    apres = {q.name: q.read_bytes() for q in sorted(sortie.iterdir())}
    assert apres == avant
    assert (f["dossier"] / "justifications.md").read_bytes() == justif_avant
    # Une 3e relance sans retouche reste INVALIDE : le gel ne se répare pas seul.
    p3 = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p3, 1, "INVALIDE")
    assert "gel violé" in p3.stdout


def test_e2e_reference_absente_verification_incomplete(tmp_path):
    """Référence absente → VÉRIFICATION INCOMPLÈTE (exit 0), ACCEPTATION.md
    écrit avec l'avertissement de l'étape 8, comparaison jamais créée."""
    f = _fabriquer(tmp_path, avec_reference=False)
    p = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p, 0, "VÉRIFICATION INCOMPLÈTE")
    assert "S-TEST-Dupuis-PlanExpert.qpl" in p.stdout    # la pièce absente est nommée
    _exiger_non_vide(f["dossier"] / "ACCEPTATION.md")
    md = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : VÉRIFICATION INCOMPLÈTE**" in md
    assert "pas pire que l'estimateur" in md
    _exiger_non_vide(f["workdir"] / "controle-aveugle.json")
    _exiger_non_vide(f["workdir"] / "gel.json")
    assert not (f["dossier"] / "comparaison-dupuis-qpl").exists()
    assert not (f["dossier"] / "justifications.md").exists()


def test_e2e_justifications_tranchees_relance_pret(tmp_path):
    """Dossier de justification tranché à la sortie du CLI (preuve + verdict)
    → relance PRÊT POUR DÉCISION FRANCIS (exit 0), dossier jamais écrasé."""
    f = _fabriquer(tmp_path)
    p1 = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p1, 1, "JUSTIFICATIONS REQUISES")
    justif = f["dossier"] / "justifications.md"
    rempli = justif.read_text(encoding="utf-8").replace(
        "|  |  |",
        "| plan PLANS-TEST - 1 (zoom ×8) : le 4e compteur est absent du raster | "
        "estimateur correct |")
    assert rempli != justif.read_text(encoding="utf-8")
    justif.write_text(rempli, encoding="utf-8")
    p2 = _lancer_boucle(f["workdir"], f["dossier"])
    _exiger(p2, 0, "PRÊT POUR DÉCISION FRANCIS")
    assert justif.read_text(encoding="utf-8") == rempli
    md = (f["dossier"] / "ACCEPTATION.md").read_text(encoding="utf-8")
    assert "**Verdict : PRÊT POUR DÉCISION FRANCIS**" in md


def test_e2e_erreur_entree_exit_2(tmp_path):
    """Workdir inexistant → diagnostic ERREUR sur stderr, exit 2, rien d'écrit."""
    f = _fabriquer(tmp_path)
    p = _lancer_boucle(tmp_path / "absent", f["dossier"])
    assert p.returncode == 2
    assert "ERREUR" in p.stderr
    assert not (f["dossier"] / "ACCEPTATION.md").exists()