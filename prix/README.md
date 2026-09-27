# prix/ — barèmes de main-d'œuvre et de prix (livres de référence)

Dossier des données extraites des livres d'estimation, pour la chaîne d'estimation.
Règle : **aucun nombre inventé** — chaque ligne porte le livre, la page imprimée et la ligne source brute.

## National Electrical Estimator 2025 (matériel + main-d'œuvre, USD)

`parse_national_estimator.py` → `national-estimator-2025.csv` (13 370 lignes : `section, page, item, crew, manhours, unit,
material_usd, labor_usd, installed_usd, raw`) + `national-estimator-2025.report.md`. Voir ce rapport pour les contrôles.

## NECA Manual of Labor Units 2021-2022 (heures-personne seulement)

| Fichier | Rôle |
|---|---|
| `parse_neca.py` | Parseur déterministe du manuel complet (pymupdf, couche texte native du PDF). |
| `neca-2022.csv` | 14 398 lignes : `section, division, page, table_title, item, unit, normal_hours, difficult_hours, very_difficult_hours, raw`. |
| `neca-2022-report.md` | Rapport de contrôle : violations de monotonie (difficile ≥ normal ≥ …), pages à en-tête sans lignes, lignes à cellules vides, descriptions sur deux lignes, etc. |

Unités (p. 10 du manuel) : `E` = à l'unité, `C` = par 100 (unités ou pieds linéaires), `M` = par 1000, `LF` = pied linéaire,
`CY` = verge cube ; le livre emploie aussi `SF` (pied carré) et `FT` (pied) sur quelques pages.

```bash
python3 prix/parse_neca.py                 # relit le PDF, régénère neca-2022.csv + neca-2022-report.md
python3 prix/parse_neca.py --layer ocr --out /tmp/ocr.csv --report /tmp/ocr.md   # diagnostic sur la couche OCR
```

Source : `/home/claude/data/livres/Neca 2022 OCR.pdf` (531 pages, sha256 dans le rapport). `page` = folio imprimé
(= index PDF + 1, vérifié sur les 517 pages qui en portent un).
