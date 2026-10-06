"""Garde anti-dérive : docs/FORMAT-EXEMPLE.md est la SEULE spec du format du PDF de relevé.

Échoue si un fichier .md du dépôt (hors spec, apprentissage/, dossiers/, releve/docs/) réintroduit une
affirmation de format concurrente déjà corrigée (audit docs vs gold HR26-14, contradictions C1-C25),
ou si un fichier retiré pour cause de spec concurrente réapparaît.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SPEC = RACINE / "docs" / "FORMAT-EXEMPLE.md"
EXCLUS = {".git", "dossiers", "apprentissage", "node_modules", ".venv", "venv"}
EXCLUS_CHEMINS = {Path("releve") / "docs"}

# Motifs précis tirés des contradictions corrigées (le gold a 3 formats de bordereau, pas un seul).
MOTIFS = {
    "bordereau 8 colonnes comme règle générale (C1, C2, C4, C5, C16, C21)": r"\bbordereau\s+8\s+colonnes\b",
    "« BORDEREAU MATERIEL » 8 colonnes comme règle générale": r"BORDEREAU\s+MAT[EÉ]RIEL\W{0,4}8\s+colonnes",
    "rayon unique de pastille r≈4,2 / r=4,186 (C3, C6, C8)": r"\br\s*[≈~=]\s*4[,.]\d|≈\s*4[,.]2\s*pt|4[,.]2\s*pt\s+de\s+rayon",
    "nom de feuille DS01 au lieu de DSI01 (C13)": r"\bDS0[1-8]\b",
    "« chaque feuille produit deux pages » (C19)": r"chaque\s+feuille\s+produit\W+(\*\*)?deux\s+pages",
    "encadré v6 « harmonisé » présenté comme la cible (C12)": r"encadr[ée]\s+v6[^\n]{0,80}harmonis",
}
RETIRES = ("SPEC.md", "docs/format-sortie-exemple.md", "src/pipeline")


def _fichiers_md():
    for dossier, sous, fichiers in os.walk(RACINE):
        rel = Path(dossier).relative_to(RACINE)
        sous[:] = [d for d in sous if d not in EXCLUS and rel / d not in EXCLUS_CHEMINS]
        for f in fichiers:
            p = Path(dossier) / f
            if f.lower().endswith(".md") and p != SPEC:
                yield p


def test_aucune_affirmation_de_format_concurrente():
    fautes = []
    for p in _fichiers_md():
        texte = p.read_text(encoding="utf-8", errors="replace")
        for nom, motif in MOTIFS.items():
            for m in re.finditer(motif, texte, flags=re.IGNORECASE):
                ligne = texte.count("\n", 0, m.start()) + 1
                fautes.append(f"{p.relative_to(RACINE)}:{ligne} — {nom} : « {m.group(0)} »")
    assert not fautes, ("Affirmation de format concurrente de docs/FORMAT-EXEMPLE.md (renvoyer à la spec) :\n"
                        + "\n".join(fautes))


def test_spec_unique_presente_et_couvre_les_trois_formats():
    texte = SPEC.read_text(encoding="utf-8")
    for attendu in ("matériel 8 col.", "agrégé 6 col.", "travaux / achats 8 col.", "v6 sans RES", "Palette B"):
        assert attendu in texte, f"docs/FORMAT-EXEMPLE.md ne mentionne plus « {attendu} »"


def test_specs_concurrentes_retirees():
    revenus = [r for r in RETIRES if (RACINE / r).exists()]
    assert not revenus, f"spec ou moteur concurrent réapparu : {revenus}"
