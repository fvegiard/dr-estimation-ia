# HR26-14 — exemplaire gold de relevé (référence d'entraînement)

Relevé IA complet du dossier **HR26-14** (OMH Haut-Richelieu, 145 rue Latour, Saint-Jean-sur-Richelieu),
extrait de `EXEMPLE.pdf` (87 p., 4 lots, 26 feuilles) en données structurées et vérifiées. Sert de
**cible de forme et de contenu** pour l'expert estimateur.

## Fichiers
| Fichier | Contenu |
|---|---|
| `STANDARD-RELEVE.md` | **Le standard** : format cible, conventions, vocabulaire, règles d'or |
| `feuilles.csv` | 26 feuilles : discipline, lot, bâtiment, repères/familles/RES |
| `bordereau-materiel.csv` | 886 lignes par repère (DSI01-08, E02/E07/E10/E13) — **12/12 vérifiées exactes** |
| `bordereau-electrique-agrege.csv` | familles agrégées (E existants + grilles) |
| `bordereau-travaux-eu.csv` | éclairage d'urgence (EU01-04) — lieux + à fournir **exacts** |
| `familles-par-feuille.csv` | comptage par désignation et par feuille |
| `reserves.md` | blocs « RESERVES ET COMPLEMENTS » de chaque feuille |
| `summary.json` | totaux et métadonnées du dossier |
| `VERIFICATION.md` | **preuve chiffrée** (extrait vs en-têtes) + constats |
| `SOURCE.txt` | provenance + sha256 du PDF source |
| `outils/extract_exemple.py` | extraction reproductible depuis le PDF |
| `outils/regen_derives.py` | régénération des dérivés depuis les CSV (workflow auto-commit) |

## Reproduire
```bash
pip install pymupdf
python outils/extract_exemple.py EXEMPLE.pdf .   # depuis le PDF
python outils/regen_derives.py .                 # dérivés depuis les CSV
```

## Prix
Aucun prix dans l'exemplaire (grilles `$` vides). À compléter depuis les **QPL + SQL (Google Drive)** —
voir `STANDARD-RELEVE.md` §8 et `apprentissage/qpl-2021-2026/`.
