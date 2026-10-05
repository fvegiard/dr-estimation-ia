# Architecture cible — proposition de consolidation

**Statut : proposition documentée. Aucun code n'est supprimé ni déplacé dans
cette PR — Francis tranche.**

## Constat

Le dépôt (branche `main`) contient deux chaînes de relevé parallèles :

- **`releve/`** (racine) — la « chaîne qui marche » selon CLAUDE.md :
  `prepare.py` → agent (compétence `releve-planexpert`) →
  `extract_occurrences.py` → `build_qpl.py` → `render_pdf.py`, orchestrés par
  `run.py`. C'est elle qui a produit le livrable Granby approuvé.
- **`src/pipeline/`** — le port prévu par SPEC.md depuis
  `planexpert-core/releve/` : `prepare.py`, `extract_occurrences.py`,
  `build_qpl.py`, `render_pdf.py`, `zoom.py`, `commun.py`. Ces six fichiers
  sont des **versions parallèles** de ceux de `releve/` (pas des copies
  octet pour octet : ex. `prepare.py` y est une version réduite, 211 lignes
  contre 248). Ils ne s'importent qu'entre eux — rien hors de `src/pipeline/`
  ne les utilise.
- **`src/releve/`** — le port SPEC depuis `dr-releves-2026/_socle/releve/` :
  `inventaire`, `index`, `raster`, `qpl_build`, `qplschema`, `verifier`,
  `xlsx_export`, `vectoriel`. Celui-ci **est utilisé** : par `src/estimer/`,
  `src/validation/ecart.py` et plusieurs tests.

## Principe directeur

**`releve/` (racine) est la base canonique.** C'est la chaîne qui marche, qui
a produit les bons résultats Granby, et CLAUDE.md impose que toute
modification de `releve/` passe le jeu de référence. On consolide autour
d'elle ; on ne la réécrit pas.

## Table de consolidation proposée

| Fichier / module | Proposition | Justification |
|---|---|---|
| `releve/prepare.py`, `extract_occurrences.py`, `build_qpl.py`, `render_pdf.py`, `zoom.py`, `commun.py`, `run.py`, `traits.py`, `controle_qualite.py` | **Garder — base canonique** | La chaîne qui marche (CLAUDE.md) |
| `src/pipeline/prepare.py`, `extract_occurrences.py`, `build_qpl.py`, `render_pdf.py`, `zoom.py`, `commun.py` | **Retirer** (après vérification d'imports) ou **fusionner** les éventuels correctifs dans `releve/` | Doublons de `releve/` ; rien hors de `src/pipeline/` ne les importe |
| `src/releve/` (`inventaire`, `index`, `raster`, `qpl_build`, `qplschema`, `verifier`, `xlsx_export`, `vectoriel`) | **Garder comme bibliothèque** importée par `releve/` et `src/validation/` | Utilisé par `src/estimer/`, `src/validation/ecart.py`, les tests ; complémentaire (schéma QPL, export xlsx) plutôt que doublon |
| `src/validation/` (`compare_qpl.py`, `ecart.py`, `jeu_reference.py`, `addenda.py`) | **Garder tel quel** | Exigé par CLAUDE.md (jeu de référence) et SPEC.md |
| `src/cablage/`, `src/qpl/`, `src/estimer/`, `src/apprentissage/` | **Garder tel quel** | Hors du chevauchement |
| `releve/agent_sdk.py`, `releve/agent_nvidia.py` | **Question pour Francis** | SPEC.md dit de ne pas porter `agent_sdk.py` (dépend de l'agent local de Francis) ; à clarifier : garder dans `releve/` ou sortir |
| `releve/docs/` (documentation agent-sdk) | **Question pour Francis** : déplacer vers `docs/` ou laisser | Documentation de référence, pas du code |

## Intégration de la méthode page par page

La méthode Granby (voir `docs/methode-page-par-page.md`) devient le **mode de
relevé standard** de la chaîne canonique :

1. `releve/prepare.py` produit les rasters haute résolution **par feuille**
   (c'est déjà son rôle : rasters, tuiles, mots).
2. L'agent relève **feuille par feuille** : un JPEG annoté + un CSV par
   feuille, selon les règles du livrable Granby (pas d'agrégation implicite,
   contradictions consignées, rien d'inventé).
3. `releve/extract_occurrences.py` lit les CSV par feuille ; l'**agrégation
   est une étape explicite avec contrôle des doublons** (schémas vs plans
   d'étage vs chambres types).
4. `releve/build_qpl.py` et `src/releve/xlsx_export.py` se construisent **à
   partir** des CSV par feuille validés.
5. Chaque dossier produit un `manifest.json` (sha256) et un `READ-ME.txt`
   (portée, réserves, contradictions) comme à Granby.

## Questions laissées à Francis

1. Garder `releve/` à la racine ou le déplacer sous `src/` une fois
   `src/pipeline/` retiré ? (SPEC.md visait `src/`, CLAUDE.md documente la
   racine.)
2. Retirer `src/pipeline/` entièrement, ou fusionner d'abord des correctifs
   vers `releve/` ?
3. Sort de `releve/agent_sdk.py` et `releve/agent_nvidia.py` ?
4. Faut-il faire de la sortie page par page (JPEG + CSV par feuille) une
   étape obligatoire du jeu de référence ?

## Hors de cette PR

- Aucune suppression ni déplacement de code.
- Aucune modification du dossier Granby (référence approuvée, lecture seule).
- `docs/consolidation.md` (sur `main`) devra renvoyer vers ce document lors
  de la fusion.
