# DR Estimation IA

Estimations électriques de DR Électrique produites par IA, prêtes pour soumission.
Les dossiers (plans, devis, addendas) sont publics — appels d'offres publiés.

## Définition de « 100 % prêt » (mesurable)

- 10 dossiers déjà soumissionnés refaits par l'IA de bout en bout
- Écart sur le total ≤ 5 % vs l'estimation de référence de Francis (seuil proposé, à confirmer par Francis)
- Écart par poste majeur (luminaires, distribution, filage, conduits) ≤ 10 %
- Aucun item manquant non signalé
- Verdict final : Francis, pas l'IA

Tant que ces chiffres ne sont pas atteints et prouvés dans `dossiers/`, le projet n'est PAS prêt.

## Pipeline

1. **Entrée** — `dossiers/<no>/entree/` : plans PDF, devis, addendas
2. **Relevé** — `dossiers/<no>/releve.xlsx` : quantités par item, référence de page/plan pour chaque ligne
3. **Validation** — `dossiers/<no>/ecart.md` : comparaison ligne par ligne vs estimation de référence
4. **Saisie Plan Expert** — VM Windows sur `mxlinux`, pilotée par Claude Code (mxlinux) + Windows-MCP
5. **Chemins de câblage** — `dossiers/<no>/cablage.pdf` : tracé sur les plans

## Outillage livré (voir `SPEC.md` et `docs/consolidation.md`)

- `src/releve/` — chaîne `python -m src.releve` : `inventaire`, `index`, `raster`, `qpl`, `verifier`,
  `xlsx` (export `releve.xlsx` au gabarit DR)
- `src/pipeline/` — préparation d'un dossier de soumission (feuilles, tuiles, occurrences, `.qpl`, PDF)
- `src/validation/ecart.py` — comparateur déterministe référence vs décompte IA → `ecart.md`
  (verdict PASS/FAIL **calculé** ; le verdict FINAL reste à Francis)
- `src/cablage/` — métré des artères (`compute_arteres`) et injection de lignes dans le `.qpl`
  (`inject_lines`, assertion d'unicité des GroupID corrigée)
- `src/qpl/` — import de compteurs dans un `.qpl` existant (`import_counters`) + charte graphique (`charte`)
- `docs/` — format QPL et pipeline complet (`pipeline-qpl.md`), gabarits de livrables
  (`format-livrable.md`), table de consolidation (`consolidation.md`)
- `infra/` — VM Plan Expert sur mxlinux (`infra/mxlinux/`) et traitement en série (`infra/pe-batch.ps1`)
- `tests/` — pytest, fixtures **synthétiques uniquement** (aucune donnée client)

```bash
pip install -r requirements.txt
python -m compileall src        # propre
python -m pytest tests -q       # vert
```

## État réel

| Étape | État |
|---|---|
| Estimations produites | **0** |
| 1. Entrée | outillée (gabarit `dossiers/_gabarit/`, `src.releve inventaire` testé) |
| 2. Relevé | outillé et testé (`src.releve` + `xlsx_export`, chaîne CLI de bout en bout verte) |
| 3. Validation | outillée et testée (`src.validation.ecart`, seuils 5 % / 10 % / items manquants) |
| 4. Saisie Plan Expert | non prouvé (S-1857 rejeté) — infra et scripts portés, saisie VM hors scope |
| 5. Chemins de câblage | outillé (`src.cablage`, bogue d'assertion corrigé, tests sur fixture synthétique) |

## Repos existants (à consolider ici)

planexpert-core, planexpert-atelier, planexpert-s1857-saint-michel, planexpert-hr26-14,
planexpert-s1787-bioscript, planexpert-infra-mxlinux, dr-releves-2026,
dashboard-soumissions-dr, electrical-estimation-mcp (tous privés)

## Ce qui ne va jamais dans ce repo

Image de la VM, installateurs ou licences Windows/Plan Expert, clés/tokens, données client
(plans, devis, compteurs réels) — les tests n'utilisent que des fixtures synthétiques.
