# SPEC — dr-estimation-ia (consolidation + pipeline)

## Objectif
Transformer le dépôt `fvegiard/dr-estimation-ia` (aujourd'hui : README seul) en un pipeline
fonctionnel et testé : plans PDF → relevé (releve.xlsx) → validation (ecart.md) → projet
Plan Expert (.qpl) → chemins de câblage. Consolidation des 9 dépôts existants.
Langue du repo : français. Python ≥ 3.12. Aucune donnée client, aucun secret.

## Arborescence cible
```
README.md                 (existant — mettre à jour la table « État réel »)
.gitignore                (VM images, installateurs, licences, clés/tokens, données client, __pycache__)
SPEC.md                   (ce fichier)
dossiers/
  _gabarit/
    entree/.gitkeep       (plans PDF, devis, addendas — déposés par Francis)
    LISEZMOI.md           (comment structurer un dossier de soumission)
src/
  releve/                 (PORTÉ depuis dr-releves-2026/_socle/releve/ — voir § Ports)
  pipeline/               (PORTÉ depuis planexpert-core/releve/)
  validation/ecart.py     (NOUVEAU — comparateur déterministe)
  cablage/                (PORTÉ depuis planexpert-s1857-saint-michel/arteres/, bug corrigé)
  qpl/import_counters.py  (PORTÉ depuis planexpert-s1857-saint-michel/tools/import/)
docs/
  pipeline-qpl.md         (PORTÉ depuis dr-releves-2026/_socle/PIPELINE.md)
  format-livrable.md      (PORTÉ depuis dr-releves-2026/_socle/FORMAT-LIVRABLE.md)
  consolidation.md        (NOUVEAU — table origine → destination, ce qui reste à faire)
infra/
  mxlinux/                (PORTÉ depuis planexpert-core/infra/mxlinux/)
  pe-batch.ps1            (PORTÉ depuis dr-releves-2026/outils/)
tests/
  test_qpl_roundtrip.py   (aller-retour qpl → verifier → qpl, GroupID uniques)
  test_ecart.py           (seuils 5 %/10 %, postes majeurs, item manquant signalé)
  test_xlsx_export.py     (releve.xlsx conforme au gabarit)
  fixtures/               (données synthétiques UNIQUEMENT)
```

## Ports (récupérer via MCP GitHub get_file_contents, owner fvegiard)
| Origine | Destination |
|---|---|
| dr-releves-2026: `_socle/releve/{__init__,__main__,inventaire,index,raster,qpl_build,qplschema,verifier}.py` + `_socle/releve/config/` | `src/releve/` |
| dr-releves-2026: `_socle/PIPELINE.md` | `docs/pipeline-qpl.md` |
| dr-releves-2026: `_socle/FORMAT-LIVRABLE.md` | `docs/format-livrable.md` |
| dr-releves-2026: `outils/vectoriel/symboles_vectoriels.py` | `src/releve/vectoriel.py` |
| dr-releves-2026: `outils/pe-batch.ps1` | `infra/pe-batch.ps1` |
| planexpert-core: `releve/{prepare,extract_occurrences,zoom,commun,build_qpl,render_pdf}.py` | `src/pipeline/` |
| planexpert-core: `infra/mxlinux/` (compose.yml, .env.example, planexpert.initd, README…) | `infra/mxlinux/` |
| planexpert-s1857-saint-michel: `arteries/` = `arteres/{compute_arteres,inject_lines}.py` | `src/cablage/` |
| planexpert-s1857-saint-michel: `tools/import/planexpert_counter_import.py` | `src/qpl/import_counters.py` |
| planexpert-s1857-saint-michel: `verification/rules_dupuis.py` | `src/qpl/charte.py` |

## Corrections obligatoires lors du portage
1. `inject_lines.py` : assertion toujours vraie `assert len(gids2) == len(set(gids2)) - 0 or True`
   → remplacer par `assert len(gids2) == len(set(gids2))`.
2. Chemins machine codés en dur (D:\claude…, /mnt/d/…, /home/francis/…) → paramètres/env.
3. NE PAS porter : agent_sdk.py/run.py (dépendent de l'agent Claude local de Francis),
   dashboard-soumissions-dr, planexpert-s1787-bioscript/tools, données client EP2026-*,
   QPL client de planexpert-atelier. Le noter dans docs/consolidation.md.

## Nouveau module 1 — src/validation/ecart.py
Comparateur déterministe (PAS un texte narratif) :
- Entrées : (a) décompte IA = CSV/JSON de compteurs par libellé (sortie de `src/releve/verifier.py`
  ou occurrences), (b) estimation de référence = CSV/XLSX (colonnes : poste, description, quantité).
- Postes majeurs : luminaires, distribution, filage, conduits (familles de charte.py).
- Sortie : `ecart.md` — tableau ligne par ligne (référence vs IA, écart absolu et %),
  écart total ≤ 5 %, écart par poste majeur ≤ 10 %, section « Items manquants » (référence
  sans contrepartie IA — jamais silencieux), verdict PASS/FAIL calculé (le verdict FINAL
  reste à Francis : le mentionner en en-tête).
- CLI : `python -m src.validation.ecart --reference ref.csv --ia compteurs.csv --sortie ecart.md`

## Nouveau module 2 — src/releve/xlsx_export.py
- Génère `releve.xlsx` (openpyxl) depuis les occurrences/compteurs :
  colonnes : Description | Type/Identification | Quantité | Feuille/Plan | Page PDF | Notes.
- Une ligne par (libellé, feuille) + feuille « Résumé » par poste majeur.
- CLI : `python -m src.releve.xlsx_export --occurrences occurrences.csv --sortie releve.xlsx`

## Tests (tout doit passer dans le sandbox)
- Générer en fixture un PDF synthétique (pymupdf) : 2 pages avec cartouche E100/E200 et texte.
- Chaîne CLI : inventaire → qpl (plans+counters JSON synthétiques) → verifier → xlsx → ecart.
- `python -m compileall src` sans erreur ; `python -m pytest tests -q` vert.
- Installer les deps nécessaires (pymupdf, pillow, openpyxl, pytest, pydantic) via pip.

## Push final
Vers `fvegiard/dr-estimation-ia`, branche main, via MCP GitHub push_files (par lots).
Commit en français. README « État réel » : outillage = fait ; estimations produites = 0
(en attente de dossiers client), étapes 2/3 outillées et testées, 4/5 documentées.
