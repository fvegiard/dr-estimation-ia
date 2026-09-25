# Vérification de l'extraction — HR26-14 (preuve chiffrée)

Source: `EXEMPLE.pdf` (87 pages). Extraction déterministe de la couche texte (pymupdf), aucune saisie manuelle.

## Bordereaux par repère (DSI + E-série M) — total extrait vs en-tête RELEVE

| Feuille | Extrait | En-tête | Statut |
|---|---|---|---|
| DSI01 | 122 | 122 | ✅ exact |
| DSI02 | 62 | 62 | ✅ exact |
| DSI03 | 94 | 94 | ✅ exact |
| DSI04 | 56 | 56 | ✅ exact |
| DSI05 | 122 | 122 | ✅ exact |
| DSI06 | 49 | 49 | ✅ exact |
| DSI07 | 121 | 121 | ✅ exact |
| DSI08 | 49 | 49 | ✅ exact |
| E02 | 52 | 52 | ✅ exact |
| E07 | 53 | 53 | ✅ exact |
| E10 | 53 | 53 | ✅ exact |
| E13 | 53 | 53 | ✅ exact |

## Électrique agrégé (E) — somme Qté vs en-tête / familles

| Feuille | Lignes | Σ Qté | En-tête repères | Familles | Statut |
|---|---|---|---|---|---|
| E01 | 4 | 80 | 80 | 4 | ✅ exact |
| E03 | 21 | 126 | — | — | grille de prix (\$ vide) — pas d'en-tête RES |
| E04 | 23 | 112 | — | — | grille de prix (\$ vide) — pas d'en-tête RES |
| E05 | 23 | 116 | — | — | grille de prix (\$ vide) — pas d'en-tête RES |
| E06 | 5 | 51 | 51 | 5 | ✅ exact |
| E08 | 22 | 128 | — | — | grille de prix (\$ vide) — pas d'en-tête RES |
| E09 | 4 | 98 | 103 | 6 | ⚠ divergence document (bordereau 4 fam/98 vs plan 6 fam/103) |
| E11 | 20 | 172 | 172 | 20 | ✅ exact |
| E12 | 4 | 107 | 110 | 6 | ⚠ divergence document (bordereau 4 fam/107 vs plan 6 fam/110) |
| E14 | 20 | 172 | 172 | 20 | ✅ exact |

## Éclairage d'urgence (EU) — bordereau travaux/achats

| Feuille | Lignes | Σ Lieux | Σ À fournir | En-tête (emplacements; appareils) | Statut |
|---|---|---|---|---|---|
| EU01 | 5 | 31 | 29 | (31, 29) | ✅ exact (lieux+à fournir) |
| EU02 | 5 | 28 | 24 | (28, 24) | ✅ exact (lieux+à fournir) |
| EU03 | 8 | 32 | 27 | (32, 27) | ✅ exact (lieux+à fournir) |
| EU04 | 8 | 30 | 24 | (30, 24) | ✅ exact (lieux+à fournir) |

## Constats (findings) — à traiter par l'estimateur
- **E09 / E12** : divergence interne de l'exemplaire — le bordereau matériel n'itemise que 4 familles (E09 Σ98, E12 Σ107) alors que le bloc RELEVE du plan annonce 6 familles / 103 (E09) et 6 / 110 (E12). À réconcilier (familles comptées ailleurs ou en réserve).
- **E03 / E04 / E05 / E08** : feuilles avec grille de prix (\$) **vide** — matériel relevé mais aucun prix. À alimenter depuis la base SQL des prix (Google Drive).
- **Prix** : aucun prix dans tout l'exemplaire (conforme au principe « relevé identification et quantités sans prix »).
