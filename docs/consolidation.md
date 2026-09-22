# Consolidation — origine → destination

Table de portage exigée par `SPEC.md`. Chaque fichier du dépôt indique sa
source ; rien n'a été inventé. Dépôts sources : `dr-releves-2026`,
`planexpert-core`, `planexpert-s1857-saint-michel` (fvegiard, privés).

## Code porté

| Origine | Destination | Adaptations |
|---|---|---|
| `dr-releves-2026/_socle/releve/__init__.py` | `src/releve/__init__.py` | docstring mentionne `xlsx_export` |
| `…/_socle/releve/__main__.py` | `src/releve/__main__.py` | imports relatifs de package ; sous-commande `xlsx` ajoutée |
| `…/_socle/releve/inventaire.py` | `src/releve/inventaire.py` | imports relatifs |
| `…/_socle/releve/index.py` | `src/releve/index.py` | imports relatifs |
| `…/_socle/releve/raster.py` | `src/releve/raster.py` | imports relatifs |
| `…/_socle/releve/qpl_build.py` | `src/releve/qpl_build.py` | imports relatifs |
| `…/_socle/releve/qplschema.py` | `src/releve/qplschema.py` | identique (BOM, constantes QPL vérifiées §2) |
| `…/_socle/releve/verifier.py` | `src/releve/verifier.py` | imports relatifs |
| `…/_socle/releve/config/cartouche-s1857-electrique.json` | `src/releve/config/cartouche-s1857-electrique.json` | identique |
| `dr-releves-2026/outils/vectoriel/symboles_vectoriels.py` | `src/releve/vectoriel.py` | en-tête d'usage ajusté |
| `dr-releves-2026/_socle/PIPELINE.md` | `docs/pipeline-qpl.md` | identique (+ note de portage) |
| `dr-releves-2026/_socle/FORMAT-LIVRABLE.md` | `docs/format-livrable.md` | identique (+ note de portage) |
| `planexpert-core/releve/prepare.py` | `src/pipeline/prepare.py` | imports relatifs ; motif `dupuis` retiré du classement (`estimateur` suffit) |
| `planexpert-core/releve/extract_occurrences.py` | `src/pipeline/extract_occurrences.py` | imports relatifs |
| `planexpert-core/releve/zoom.py` | `src/pipeline/zoom.py` | imports relatifs |
| `planexpert-core/releve/commun.py` | `src/pipeline/commun.py` | commentaire palette pointe vers `src/qpl/charte.py` |
| `planexpert-core/releve/build_qpl.py` | `src/pipeline/build_qpl.py` | imports relatifs ; renvoie vers `src.releve qpl` pour les projets riches |
| `planexpert-core/releve/render_pdf.py` | `src/pipeline/render_pdf.py` | imports relatifs ; `markdown` importé paresseusement (dépendance optionnelle) |
| `planexpert-core/infra/mxlinux/*` | `infra/mxlinux/*` | identique, **sauf** `oem/authorized_keys` (clés publiques SSH : exclues, voir plus bas) |
| `planexpert-s1857-saint-michel/tools/import/planexpert_counter_import.py` | `src/qpl/import_counters.py` | CLI `typer` → `argparse` (une dépendance en moins) ; logique et garde-fous inchangés |
| `planexpert-s1857-saint-michel/verification/rules_dupuis.py` | `src/qpl/charte.py` | règles **identiques** ; ajout de `POSTES_MAJEURS`, `normaliser()` et `famille_pour_libelle()` (familles déduites des sections du fichier) |
| `planexpert-s1857-saint-michel/arteres/compute_arteres.py` | `src/cablage/compute_arteres.py` | **généralisé** (pipeline-qpl.md §4.2) : `FRAME`, `LEVEL`, `STOREY`, `SHEET_LEVEL`, `EQ`, `RISER`, `FEEDERS`, `PARAMS` chargés depuis `--config JSON` ; seule la géométrie reste dans le code |
| `planexpert-s1857-saint-michel/arteres/inject_lines.py` | `src/cablage/inject_lines.py` | **bogue corrigé** + chemins paramétrés (voir ci-dessous) |
| `dr-releves-2026/outils/pe-batch.ps1` | `infra/pe-batch.ps1` | identique |

## Modules créés (SPEC)

| Fichier | Rôle |
|---|---|
| `src/validation/ecart.py` | comparateur déterministe référence (CSV/XLSX) vs décompte IA (CSV/JSON) → `ecart.md` ; écart total ≤ 5 %, postes majeurs ≤ 10 %, items manquants jamais silencieux, verdict PASS/FAIL **calculé** (FINAL = Francis) |
| `src/releve/xlsx_export.py` | occurrences CSV → `releve.xlsx` au gabarit DR : `Description \| Type/Identification \| Quantité \| Feuille/Plan \| Page PDF \| Notes`, une ligne par libellé/feuille, feuille « Résumé » par poste majeur |

## Corrections obligatoires (SPEC)

1. **Bogue `inject_lines.py`** — l'assertion d'unicité des GroupID était
   `assert len(gids2) == len(set(gids2)) - 0 or True` (toujours vraie à cause
   du `or True`). Corrigée en `assert len(gids2) == len(set(gids2))` et couverte
   par `tests/test_qpl_roundtrip.py::test_compute_et_inject_lines`.
2. **Chemins machine codés en dur paramétrés** — `inject_lines.py` lisait
   `../v3-roundtrip/incoming-project.zip` en dur : source/résumé/sortie sont
   désormais des arguments CLI ; couleur, épaisseur, feuilles à passer en
   `Precision=2` et rapport mm/px sont des options. `compute_arteres.py`
   n'écrit plus à côté du script : `--out`. Les données S-1857 (positions,
   départs) sont sorties du code vers un JSON de configuration par soumission.

## Non porté, volontairement

| Source | Raison |
|---|---|
| `planexpert-core/releve/agent_sdk.py`, `releve/run.py` | dépendent de l'agent local de Francis (SDK Claude Code, chemins machine) — hors scope pipeline déterministe |
| `planexpert-core/infra/mxlinux/oem/authorized_keys` | clés publiques SSH : aucune clé dans ce dépôt (règle absolue) ; à déposer à la main dans la VM |
| `planexpert-s1857-saint-michel/arteres/` données S-1857 (FEEDERS, EQ, niveaux) | données du projet S-1857 : sorties du code, non commitées ici ; une config JSON par soumission les remplace (fixture synthétique dans `tests/fixtures/arteres-config.json`) |
| gabarits Excel binaires (`_socle/gabarits/*.xlsx`) | binaires maîtres DR, hors périmètre du pipeline de test ; le format est documenté dans `docs/format-livrable.md` |
| scripts `tools/host/_*.ps1` / `_*.py` du dépôt S-1857 | classés « jetables » par pipeline-qpl.md §4.3 |
| tout dossier client (`dossiers/<no>/…`) | jamais dans le dépôt (`.gitignore`) ; gabarit dans `dossiers/_gabarit/` |

## Travail restant (hors scope de cette consolidation)

- Saisie dans Plan Expert (VM mxlinux) : ouverture du `.qpl`, échelle,
  sauvegarde, exports natifs — pilotage VM documenté dans
  `docs/pipeline-qpl.md` §1 étape 11 et `infra/pe-batch.ps1`.
- Refaire les 10 dossiers de référence et faire passer les seuils de
  « 100 % prêt » (README) — nécessite les dossiers client, absents du dépôt.
- Configuration cartouche par gabarit de plans (`src/releve/config/` n'a que
  celle de S-1857, mesurée réellement).
