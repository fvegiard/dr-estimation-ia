# `src.estimer` — plan PDF → compte par famille et par feuille, au format de M. Dupuis

## Commandes

```bash
pip install -r requirements.txt                      # pymupdf, numpy, scipy, scikit-learn, openpyxl…
python -m src.estimer.train                          # apprend models/estimer.joblib sur les références Dupuis
python -m src.estimer PLANS.pdf --out sortie/        # estimation d'un PDF quelconque
python -m src.estimer.evaluate --out eval            # validation « un dossier exclu » → eval/results.json + eval/REPORT.md
python -m src.estimer.evaluate --out eval --report-only   # régénère REPORT.md depuis results.json
python -m src.validation.ecart --reference ref.csv --ia sortie/estimate.json --sortie ecart.md
```

Options de `python -m src.estimer` : `--model`, `--pages 1-3,7`, `--name`, `--no-qpl`, et `--sheets feuilles.csv`
(colonnes `page,name,scale_ratio,paper_width_pt,skip`) pour donner le numéro de feuille, l'échelle (réel/papier :
96 = 1/8" = 1'-0") et la largeur papier d'un PDF image sans couche texte.

## Sorties

| Fichier | Contenu |
|---|---|
| `estimate.json` | lisible tel quel par `src.validation.ecart --ia` (liste `counters`, quantité = nombre d'éléments) ; comptes par famille et par feuille, chaque détection (x, y en px de page, score, probabilité de famille, drapeaux), conduits estimés, zones illisibles |
| `releve.xlsx` | gabarit DR (`src.releve.xlsx_export` : Relevé / Résumé) + feuille « Conduits » |
| `sheets.csv` | une ligne par page : comptes par famille, zones illisibles, conduit estimé, drapeaux |
| `planexpert/<nom>.qpl` + PNG | projet Plan Expert au format de Dupuis : `Plan Name="<pdf> - N"`, `FileName="<pdf> - N.png"`, un compteur par famille (forme / taille / couleur apprises de ses compteurs), échelle écrite comme lui (Type 1 = pouces par pied, virgule décimale ; Type 0 = 1:N), ligne « CONDUIT ESTIME » quand l'échelle est connue |

Drapeaux d'incertitude : `scale_unknown` (pas de conduit), `page_has_coloured_markup`, `unreadable_markup_zones`
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
   Un premier essai sans ce garde-fou (cœur couvert admis) retrouvait surtout les symboles cachés sous les marques
   (rappel 0,58 à 0,61 sur ceux-ci contre 0,06 à 0,08 sur les symboles visibles, R = 25 px, S-1714 pages 4, 6 et 9, modèle appris sur les 4 autres dossiers) : il relisait le relevé
   antérieur, pas le dessin. Il a été abandonné.
5. **Conduits** (`conduits.py`) : échelle lue dans la couche texte (« ÉCHELLE 1/8" = 1'-0" », « 1:100 ») ou donnée par
   `--sheets` ; longueur = ratio appris × arbre couvrant rectilinéaire des appareils détectés. Ratio = médiane, sur les
   feuilles où Dupuis a posé une échelle, de (longueur de ses lignes de conduit / arbre sur ses propres marques).
   C'est une estimation, toujours signalée comme telle.

## Limites connues (mesurées dans `eval/REPORT.md`)

- Les PDF de plans d'origine et les PNG de Dupuis ne sont pas dans l'environnement ; l'évaluation tourne sur
  `Plans-annotes.pdf`, où la plupart des symboles sont couverts. Les chiffres de bout en bout y sont bornés par la
  part lisible.
- S-1857 n'a pas de `.qpl` Dupuis ici (seulement `reference-quantites.csv`) : écarts de quantité seulement.
- Aucun prix : hors périmètre (les projets de Dupuis n'en contiennent pas).
