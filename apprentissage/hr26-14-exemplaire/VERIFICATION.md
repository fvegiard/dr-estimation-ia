# Vérification de l'extraction — HR26-14 (preuve chiffrée)

Régénéré depuis les CSV sources par `outils/regen_derives.py`.

## Bordereaux par repère (DSI + E-série M) — extrait vs en-tête RELEVE

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

## Électrique agrégé (E) — Σ Qté vs en-tête

| Feuille | Lignes | Σ Qté | En-tête | Familles | Statut |
|---|---|---|---|---|---|
| E01 | 4 | 80 | 80 | 4 | ✅ exact |
| E03 | 21 | 126 | — | — | grille de prix ($ vide) |
| E04 | 23 | 112 | — | — | grille de prix ($ vide) |
| E05 | 23 | 116 | — | — | grille de prix ($ vide) |
| E06 | 5 | 51 | 51 | 5 | ✅ exact |
| E08 | 22 | 128 | — | — | grille de prix ($ vide) |
| E09 | 6 | 103 | 103 | 6 | ✅ exact |
| E11 | 20 | 172 | 172 | 20 | ✅ exact |
| E12 | 6 | 110 | 110 | 6 | ✅ exact |
| E14 | 20 | 172 | 172 | 20 | ✅ exact |

## Éclairage d'urgence (EU) — bordereau travaux/achats

| Feuille | Lignes | Σ Lieux | Empl. (en-tête) | Σ À fournir | À fournir (en-tête) | Statut |
|---|---|---|---|---|---|---|
| EU01 | 5 | 31 | 31 | 29 | 29 | ✅ exact |
| EU02 | 5 | 28 | 28 | 24 | 24 | ✅ exact |
| EU03 | 8 | 32 | 32 | 27 | 27 | ✅ exact |
| EU04 | 8 | 30 | 30 | 24 | 24 | ✅ exact |

## Constats (findings)
- Bordereaux agrégés : Σ Qté = en-tête sur toutes les feuilles chiffrées (aucune divergence).
- **E03 / E04 / E05 / E08** : grilles de prix vides — matériel relevé, prix à alimenter depuis la base SQL (Google Drive).
- **Prix** : aucun prix dans l'exemplaire (relevé identification + quantités seulement).
