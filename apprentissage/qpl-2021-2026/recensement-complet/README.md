# Recensement complet — corpus Plan Expert (.qpl) + base SQL EE + EXEMPLE HR26-14

Date : 2026-09-25 (heure de l'Est). Exécuté sur fv_legion, sortie réelle (`summary.json`).
Script : `outils/census_qpl.py` (stdlib seulement, sha256 `e9e48f63…d42fa`).

Reproduire :

```
python3 outils/census_qpl.py "D:\claude\releve-auto\qpl-corpus\files" <sortie> "G:\My Drive\AI\Soumission 2026"
```

## 1. Où sont réellement les QPL et le SQL (vérifié)

Source de vérité : base de métadonnées Google Drive pour ordinateur (`DriveFS\metadata_sqlite_db`,
159 555 éléments, y compris les partages « plan expert qpl »).

| Emplacement | .qpl | Nature |
|---|---|---|
| Google Drive (tout le compte fvegiard@gmail.com) | 18 | 10 dans `AI\Soumission 2026` : 8 relevés IA (Claude/Codex S-1787, S-1857), 1 projet **vide** HR26-14 (11 Ko), 1 original Dupuis 2024 (S-1272) ; 5 copies `cloud-transfert\corrections` ; reste = doublons |
| `D:\claude\releve-auto\qpl-corpus\files` (robocopy de `Z:\Soumission\mes projets`, 2026-09-24) | 856 | **Le corpus complet de M. Dupuis 2021-2026** |
| SQL dans Drive | 0 | aucun .sql/.bak/.mdf métier (seul `dispatch_gobby.sql`, sans rapport) |
| SQL dans le dépôt (branche `lena/planexpert-sql`) | 1 | `EE_BaseDeDonnees_Complet_V0_V45.sql` (package V14 de M. Dupuis) |

## 2. Corpus QPL — chiffres complets (toutes les structures, pas seulement les compteurs)

| Mesure | Valeur |
|---|---|
| Fichiers .qpl | 856 |
| Uniques (sha256) | **511** (345 doublons « - Copie » / `_gsdata_`) |
| Analysables | 510 (1 corrompu : `s-1582`, fichier vide) |
| Projets avec marques | 394 |
| Marques (comptage) | **386 005** (le chiffre 596 502 du 24/09 comptait les doublons) |
| Médiane marques / projet | 157 |
| Étiquettes brutes distinctes | 11 807 |
| Feuilles (Plan) | 16 905 |
| **Tracés linéaires (Line = conduits/câbles)** | **8 955 dans 372 projets** — jamais analysés avant |
| Spécifications conduit+filage distinctes | 98 (ex. `1/2 3c12` ×160, `3/4 3c12` ×118, `3/4 3c10` ×104) |
| Surfaces (Area) | 375 |
| Liens vers la base EE (`EEExchangeData` → ENSEMBLE) | **30 projets, 132 ensembles, 3 767 marques** |
| Prix dans les .qpl | 0 (CostEach = 0 partout) |
| Échelle renseignée | 14 % des feuilles (86 % à `0` → longueurs en pixels seulement) |

## 3. Appariement plans (Drive `Soumission 2026`) ↔ relevés QPL de l'estimateur

- **54 numéros S** ont à la fois les plans dans Drive **et** un QPL de M. Dupuis → jeu d'entraînement
  plans → relevé expert (`appariement-plans-qpl.csv`). Les plus riches : S-1714 (8 503 marques),
  S-1741 (5 758), S-1767 (4 334), S-1692 (3 656), S-1695 (3 306), S-1775 (3 231), S-1706 (2 722).
- 191 dossiers 2026 avec plans mais sans QPL ; 371 QPL (2021-2025) sans plans dans Drive.

## 4. Base SQL EE (`EE_BaseDeDonnees_Complet_V0_V45.sql`)

- 12,9 Mo, CP1252, 2 029 lots `GO`. 60 tables : `PRODUITS` (COUBRUTUNI = coût brut, TEMPUNI = temps
  unitaire, MULCOM), `ENSEMBLE`/`ENSCOMPO` (assemblages), `SOUMIS`/`SOUPRO`/`SOUENS` (soumissions),
  `FACTURES`, `COMMANDE`, `TAUX`, `PriceUpdate_Products`…
- **Données : aucune** sauf `PROCORRESP` (90 573 lignes de correspondance ancienne→nouvelle clé
  manufacturier). **Zéro prix, zéro soumission historique.** C'est le schéma, pas la base d'un an.
- Pont confirmé : chaque `EEExchangeData ItemID="ENS…"` d'un QPL = clé `ENSEMBLE` de cette base.
  Avec un export de la base **vivante** (EEWin, serveur DR), chaque marque liée obtient prix + main-d'œuvre.

## 5. EXEMPLE HR26-14 (87 images = 87 pages de EXEMPLE.pdf)

- Images vérifiées visuellement (p. 1, 2, 12, 30, 60, 87) : plans annotés (pastilles couleur par
  famille + encadré « RELEVE <feuille> - MATERIEL » : repères, familles, RES), chacun suivi de ses
  pages « BORDEREAU MATERIEL » ; « BORDEREAU TRAVAUX / ACHATS » pour EU01-04. Même contenu que la
  couche texte déjà extraite (`apprentissage/hr26-14-exemplaire`, 12/12 + 10/10 + 4/4 exacts).
- C'est le **format de livrable cible** (`STANDARD-RELEVE.md`).
- Le QPL « HR26-14 (15-Septembre-2026) » du Drive est un **projet vide** : pas de relevé humain
  HR26-14 à recouper.

## 6. Ce qui manque pour chiffrer (bloquant, hors Drive)

1. Export de la base EE/EEWin **vivante** (tables PRODUITS, ENSEMBLE, ENSCOMPO, TAUX) — le script
   V0→V45 n'en contient pas les données.
2. L'échelle des feuilles (86 % à 0) pour convertir les 8 955 tracés en pieds.
