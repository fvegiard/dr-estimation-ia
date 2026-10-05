# S-0922 — pilote graphique E-3 pour revue indépendante

Une seule page est proposée : **E-3**. La v3 livrée reste disponible et inchangée. Ce pilote répond aux écarts E02/E04 de l'audit Granby, sans nouveau relevé métier ni généralisation aux autres feuilles. **L'acceptation graphique reste à prononcer par la revue indépendante. QPL global : BLOCKED. Aucun 95 % revendiqué; aucune validation de chantier.**

## Pièces à ouvrir

- `paquet/S-0922-E-3-releve.jpg` : JPEG exact du pilote, 12623 × 9467 pixels.
- `preuves/03-pages-entieres-reference-v3-pilote.jpg` : Granby E401, v3 et pilote, chaque feuille à 1000 pixels de largeur.
- `preuves/04-legendes-meme-largeur-feuille.png` : légendes prélevées après normalisation de chaque feuille à **6854 pixels**. Aucun ajustement séparé à un cadre commun ne fausse leur taille relative.
- `preuves/05-reperes-meme-largeur-feuille.jpg` : mêmes fenêtres de 1500 × 1000 pixels que l'audit, après normalisation à 6854 pixels; même réduction d'affichage pour les trois témoins.
- `preuves/06-quatorze-lineaires-source-v3-pilote.jpg` : les 14 G, source/v3/pilote, avec leurs limites complètes.
- `preuves/07-onze-familles-source-v3-pilote.jpg` : un témoin de chacune des 11 familles; les centres et symboles restent visibles.
- `travail/inspection/E-3/final-legend.jpg` et `layout-report.json` : légende réellement rendue et disposition contrôlée.

La même largeur de feuille ne rend pas identiques les échelles architecturales des projets. Les fenêtres et empreintes des références sont consignées dans `preuves/comparatifs-mesures.json`.

## Audit lu et choix du pilote

Le document exact `task-9/rapport/Rapport-Granby-S0922-S1294.html` a été lu, texte HTML extrait sans ses images encodées. Les comparatifs 02, 03 et 05 ont été ouverts, ainsi que la légende Granby E401. La page E401 a ensuite été relue depuis le ZIP Granby désigné par Francis. Son identité et celle du rapport sont consignées dans `baseline-v3.json` et `preuves/comparatifs-mesures.json`.

Constats pertinents : E-3 conserve déjà la feuille entière et sa légende intérieure, mais présente les familles en liste à une colonne, avec les quantités dans le texte. Le traitement des luminaires linéaires par des cercles ne reprend pas les contours allongés visibles dans Granby. L'audit ne démontre pas un décalage systématique des centres et n'impose aucun rayon, police ou RGB universel. Ces limites ont été respectées.

## Proposition graphique

1. **Légende intérieure maintenue.** Elle est déplacée dans l'espace vide en haut de la même feuille, à côté de la cédule source. Ses limites de travail sont x=540, y=25, largeur=910, hauteur=275 sur le référentiel existant de largeur 1800. La région source a été inspectée et ne contient aucun pixel de luminance inférieur à 200/255. Ce contrôle documente l'absence de texte ou trait foncé masqué dans cette région; il ne constitue pas une norme d'acceptation inventée. Les dimensions, orientation et cartouche de la feuille restent inchangés.
2. **Hiérarchie et alignement.** Titre de feuille, contexte de révision, résumé, puis deux groupes de familles; les quantités sont alignées à droite dans deux colonnes numériques distinctes. Libellés et chiffres restent foncés, les couleurs sont portées par les symboles. Les 11 familles, les six notes et toutes les réserves sont conservées. Le total de 185 luminaires codés provient des comptes A+B+C+G déjà présents.
3. **Linéaires G.** Les 14 cercles sont remplacés par des contours rectangulaires suivant les limites des symboles source : 13 verticaux et un horizontal. Les géométries ont été mesurées sur le PNG, puis vérifiées visuellement. Pour E-3-174, une composante sombre touchait le nuage de révision : le bord du luminaire a été délimité séparément et le cas est documenté dans `preuves/geometries-G-source.json`. Aucun métrage ou nombre de modules n'en est déduit.
4. **Autres repères.** Leurs centres, données, styles circulaires et palette existants sont conservés. Le rayon d'un témoin Granby n'a pas été transformé en règle universelle. La police reste celle du renderer existant configuré sous Windows; aucune équivalence exacte aux polices ou aux calques du JPEG Granby n'est prétendue.

Les dimensions de mise en page et les contours mesurés sont des choix de ce pilote, pas des exigences chiffrées attribuées à Francis. Le nouvel emplacement doit être apprécié dans le comparatif de page entière avant généralisation.

## Conservation et contrôles réalisés

- Le moteur existant a été réutilisé dans une copie située dans ce checkout : `travail/methode/render_sheet.py`. Aucun autre espace de production n'a été modifié.
- Commande réelle : `python -B travail/methode/render_sheet.py E-3 --pilot-granby` depuis ce dossier. Code 0 : 223 repères, dont 14 G; JPEG généré puis réellement ouvert.
- `--pilot-granby` refuse toute feuille autre qu'E-3. Sans cette option, le comportement antérieur du renderer est conservé. Aucun rendu E-1, E-2, E-4 ou E-5 n'a été régénéré.
- Le CSV E-3 généré est **identique octet par octet** à la v3 : toutes les identités, familles, quantités, coordonnées, modèles, parents et réserves sont conservés.
- Dans le paquet pilote, **15/16 fichiers métier sont identiques à v3**. Seul le JPEG E-3 change. Tous les CSV, le classeur, `sheet_data.py`, `CHECKPOINT.json` et les quatre autres JPEG restent identiques.
- Dans le dossier historique du checkout, les **16/16 fichiers métier restent identiques** au gel de début de pilote.
- **56 tests passent en 84,87 s** : les 48 tests v3 rejoués contre le paquet pilote, plus huit contrôles de conservation, coordonnées, placement intérieur, colonnes, limites de la proposition et E-5-072. Journal : `tests-pilote.txt`.
- Le vérificateur existant passe sous `python -O` sur le paquet réel : **27 fichiers physiques**, **26 empreintes indexées**, données concordantes. Journal : `verification-paquet.txt`. Ce succès est un contrôle d'intégrité, pas un verdict de conformité Granby/QPL.
- Inspection visuelle directe effectuée : page entière, légende entière, zone dense de l'audit, **14/14 contours G** et **11/11 familles témoins**. Les étoiles des sorties réservées et les symboles source demeurent visibles dans ces témoins. Ces comptes désignent la couverture de l'inspection, jamais un taux d'exhaustivité métier.

Les seuls fichiers différents entre le paquet pilote et v3 sont `S-0922-E-3-releve.jpg`, `methode/render_sheet.py`, `READ-ME.txt` et `manifest.json`. Le README identifie clairement le pilote; le checkpoint historique n'a pas été réinterprété comme une approbation du nouveau rendu. Le diff du renderer est `render-pilote-vs-v3.diff`.

## Limites et critères laissés à la revue

- Légende et contours G proposés pour **E-3 seulement**. Aucun avis global sur les cinq pages, leurs cédules, leurs détails ou la navigation du classeur ne découle de ce pilote.
- Les autres formes de repères restent celles de v3. La revue peut juger d'autres adaptations nécessaires; elles ne sont pas présentées ici comme déjà closes.
- Pas de comparaison QPL ouverte ou exécutée. Le dénominateur de 95 % demeure non établi.
- E-5 reste inchangée : **72 réserves, E-5-072 conservé, DO NOT USE FOR CONSTRUCTION**. Les 423 repères du dossier et les réserves métier ne sont pas recalculés.
- La généralisation est laissée en attente de la revue indépendante de ce pilote. Aucun push, merge, partage Library ou publication n'a été effectué.

Les versions antérieures restent dans `task-2/S-0922-package-v3/`, le ZIP v3 et ses trois ZIP de distribution déjà livrés. SHA256 du ZIP v3 conservé : `d550525df598584f01c89e78e3523ce0ec4aa96d88b12f70341ebdd5f78693c9`.
