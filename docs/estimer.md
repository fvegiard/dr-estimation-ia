# `src.estimer` — plan PDF → compte par famille et par feuille, au format de M. Dupuis

## Commandes

```bash
pip install -r requirements.txt                      # pymupdf, numpy, scipy, scikit-learn, openpyxl…
python -m src.estimer.train                          # apprend models/estimer.joblib sur les références Dupuis (plans originaux)
python -m src.estimer PLANS.pdf --out sortie/        # estimation d'un PDF quelconque
python -m src.estimer.evaluate --out eval            # validation « un dossier exclu » sur les PLANS ORIGINAUX → eval/results.json + eval/REPORT.md
python -m src.estimer.evaluate --out eval --report-only   # régénère REPORT.md depuis results.json
python -m src.estimer.evaluate --gold annotes --out eval/plans-annotes   # ancien protocole sur Plans-annotes.pdf (comparaison seulement)
python -m src.validation.ecart --reference ref.csv --ia sortie/estimate.json --sortie ecart.md
```

Options de `python -m src.estimer` : `--model`, `--pages 1-3,7`, `--name`, `--no-qpl`, et `--sheets feuilles.csv`
(colonnes `page,name,scale_ratio,paper_width_pt,skip`) pour donner le numéro de feuille, l'échelle (réel/papier :
96 = 1/8" = 1'-0") et la largeur papier d'un PDF image sans couche texte.

## Index des plans originaux (`src.estimer.plan_index`)

```bash
python -m src.estimer.plan_index                     # 6 dossiers → dossiers/<S>/entree/plans-originaux/INDEX.md + src/estimer/data/plan_index.json
python -m src.estimer.plan_index --dossiers S-1844 --no-ocr
```

Lit les PDF ORIGINAUX des appels d'offres (`/home/claude/data/dossiers/<S>/entree/plans-originaux/*.pdf`, jamais
`Plans-annotes.pdf`) et, pour chaque page : taille affichée (rotation appliquée), couche texte (oui / partielle / non),
nombre de dessins vectoriels et d'images, numéro de feuille lu dans le cartouche (texte ; à défaut OCR tesseract du
cartouche, marqué `ocr`), titre, échelle du cartouche, pages légende, listes de feuilles (page couverture, « liste des
plans » scannée). Puis apparie chaque `<Plan FileName=…>` du projet Plan Expert de M. Dupuis (`reference/*Dupuis*.qpl`)
à une page : règle de nom `<pdf> - N` / `<pdf>-page-000N` (comme `src.validation.compare_qpl`), contrôle du rapport
largeur/hauteur avec `dupuis-png-dimensions.txt`, et confrontation à l'appariement géométrique antérieur
(`comparaison-dupuis-qpl/pages.csv`). Les plans dont le document n'est pas dans `plans-originaux` sont listés avec leur
nombre de marques (S-1844 : 693/716 marques sur `23347_SELECTION_GLOBAL_SOUM…`, document absent). S-1857 n'a pas de
référence Dupuis : c'est `planexpert/S-1857.qpl` (projet de la chaîne) qui est indexé, et l'INDEX le dit.

## Vérité sur les plans originaux (`src.estimer.gold_original`, défaut de `train` et `evaluate`)

`gold.load(dossier, source="original")` place les marques de M. Dupuis sur les PDF originaux via `plan_index.json` :

- **Direct** (par défaut) : plan Dupuis apparié à une page par son nom (`<pdf> - n`, rapport L/H vérifié) et taille de son
  raster connue (`dupuis-png-dimensions.txt`) → `x · largeur_page / largeur_png`. Aucun autre relevé n'intervient.
- **Recalé** (reste, compté dans les notes du dossier) : raster de taille inconnue (S-1811 : 5 pages JPG de l'addenda
  MEP01, 681 marques) ou document absent de `plans-originaux` (S-1844 : feuilles électriques du cahier global 23347,
  685 marques) → recalage géométrique de `src.validation.compare_qpl` sur les rasters du relevé automatique
  (similitude par page), puis `feuilles-ia.csv` pour retrouver la page du PDF. Vérifié visuellement (S-1811 505B
  addenda, S-1844 E300) : marques sur les symboles.
- **Non plaçable** : compté dans `unplaced` (S-1844 : 23 marques de la page E103, raster inconnu et sans recalage).
- Page importée deux fois par Dupuis (S-1714 E401–E408) : doublons à moins de 1,2 % de la diagonale retirés (1001).
  Feuille marquée dans l'original ET l'addenda (S-1811 503B/505B/506B/507B/508B) : les deux jeux sont gardés, les deux
  pages étant dans l'entrée.
- Dossier à plusieurs PDF : concaténation dans `/home/claude/data/dossiers/_cache-plans-originaux/<S>-plans-originaux.pdf`
  (ordre de l'index, PDF sans plan Dupuis exclus — listes de feuilles scannées) ; le cache est régénéré si les SHA256 changent.
- S-1857 : aucun `.qpl` Dupuis → vérité de quantités `reference-quantites.csv` ; `planexpert/S-1857.qpl` (relevé
  automatique) n'est PAS utilisé comme vérité.

## Sorties

| Fichier | Contenu |
|---|---|
| `estimate.json` | lisible tel quel par `src.validation.ecart --ia` (liste `counters`, quantité = nombre d'éléments) ; comptes par famille et par feuille, chaque détection (x, y en px de page, score, probabilité de famille, drapeaux), conduits estimés, zones illisibles |
| `releve.xlsx` | gabarit DR (`src.releve.xlsx_export` : Relevé / Résumé) + feuille « Conduits » |
| `sheets.csv` | une ligne par page : comptes par famille, zones illisibles, conduit estimé, drapeaux |
| `planexpert/<nom>.qpl` + PNG | projet Plan Expert au format de Dupuis : `Plan Name="<pdf> - N"`, `FileName="<pdf> - N.png"`, un compteur par famille (forme / taille / couleur apprises de ses compteurs), échelle écrite comme lui (Type 1 = pouces par pied, virgule décimale ; Type 0 = 1:N), ligne « CONDUIT ESTIME » quand l'échelle est connue |

Drapeaux : `from_text_tag`, `family_from_text_tag` (famille lue dans une légende), `scale_unknown` (pas de conduit), `page_has_coloured_markup`, `unreadable_markup_zones`
(zones de marques de couleur de la taille d'un symbole — non comptées), `near_coloured_markup` (détection voisine d'une
marque), `family_uncertain` (probabilité de la famille < 0,5), `no_symbol_detected`.

## Méthode (tout est appris, rien n'est codé par dossier)

1. **Pages** (`pages.py`) : chaque page est ramenée à 2997 px de large (largeur des exports Plan Expert). Les pixels
   nettement colorés (saturation ≥ 0,28) forment un masque d'annotations, dilaté de 3 px, blanchi dans l'image.
2. **Vérité** (`gold.py`) : les marques des `.qpl` de Dupuis (pixels de ses PNG) sont recalées sur les pages par
   `src.validation.compare_qpl` (appariement de pages, échelle + translation), puis ramenées au raster de page.
   Famille = catégoriseur `src.qpl.categorie` ; pour les libellés qu'il ne sait pas classer (« KS », « AF1-5 »…), vote
   des marques co-localisées dont le libellé est classable (≥ 3 votes, ≥ 60 %).
3. **Détecteur** (`features.py`, `model.py`) : fenêtres de 64 px sur une grille de 6 px ; HOG fin (cellules de 8 px sur
   le symbole) + HOG grossier (contexte : murs, étiquettes de circuit) + densité d'encre + profil en anneaux ;
   `HistGradientBoostingClassifier` (familles + « aucun ») ; maxima locaux au-dessus d'un seuil, suppression des
   non-maxima ; seuil et rayon calibrés sur des dossiers d'entraînement mis de côté.
4. **Garde-fou contre la fuite** : les seules images de plans disponibles portent les marques opaques d'un relevé
   antérieur. Une fenêtre dont le cœur (13 × 13 px) touche une marque n'est ni apprise ni évaluée : le détecteur ne
   compte que ce qu'il voit, et les zones couvertes sont signalées. Les marques présentes ailleurs dans une fenêtre sont
   transplantées sur des négatifs au même taux, pour qu'elles ne portent aucune information.
   Un raffinement par négatifs difficiles (`python -m src.estimer.train --hard-negatives`) a été mesuré sur le pli
   S-1844 : précision 13,1 % contre 13,9 %, rappel sur marques lisibles 17,6 % contre 20,0 % (R = 25 px ; grille de seuils
   commençant à 0,05 pour l'essai, à 0,15 pour la référence) — pas de gain,
   désactivé par défaut.
   Un premier essai sans ce garde-fou (cœur couvert admis) retrouvait surtout les symboles cachés sous les marques
   (rappel 0,58 à 0,61 sur ceux-ci contre 0,06 à 0,08 sur les symboles visibles, R = 25 px, S-1714 pages 4, 6 et 9, modèle appris sur les 4 autres dossiers) : il relisait le relevé
   antérieur, pas le dessin. Il a été abandonné.
5. **Légendes** (`legend.py`, PDF avec couche texte seulement) : les lignes « CODE description » des légendes et
   cédules donnent code → famille (catégoriseur sur la description ; lignes contradictoires ou code jamais repris
   sur un plan = rejeté). Chaque occurrence isolée du code sur les plans devient une détection (`from_text_tag`), ou
   donne sa famille à la détection visuelle la plus proche à moins de 40 px (`family_from_text_tag`). Les PDF image
   (dont les anciens `Plans-annotes.pdf`) n'ont pas de mots : ce module ne s'y active pas ; sur les PDF originaux il est actif.
6. **Conduits** (`conduits.py`) : échelle lue dans la couche texte (« ÉCHELLE 1/8" = 1'-0" », « 1:100 ») ou donnée par
   `--sheets` ; longueur = ratio appris × arbre couvrant rectilinéaire des appareils détectés. Ratio = médiane, sur les
   feuilles où Dupuis a posé une échelle, de (longueur de ses lignes de conduit / arbre sur ses propres marques).
   C'est une estimation, toujours signalée comme telle.

## Limites connues (mesurées dans `eval/REPORT.md`)

- L'évaluation courante tourne sur les PDF originaux (`eval/REPORT.md`, `eval/results.json`) ; l'ancienne évaluation sur
  `Plans-annotes.pdf` (rendus portant les marques opaques d'un relevé antérieur) est conservée dans `eval/plans-annotes/`
  pour comparaison — elle ne doit plus servir d'entrée.
- Les marques de Dupuis sont posées à sa manière (souvent au coin du symbole) : R = 25 px absorbe l'écart pour les
  symboles courants, pas pour les grands appareils.
- 1366 marques (S-1811 addenda MEP01, S-1844) sont placées par recalage, pas directement : une erreur globale de
  recalage sur une page déplacerait toutes ses marques.
- S-1857 n'a pas de `.qpl` Dupuis ici (seulement `reference-quantites.csv`) : écarts de quantité seulement.
- Aucun prix : hors périmètre (les projets de Dupuis n'en contiennent pas).
