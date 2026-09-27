# Évaluation de l'estimateur automatique — validation croisée « un dossier exclu » contre M. Dupuis

Généré le 2026-09-27 14:00 par `python -m src.estimer.evaluate` (commit e240619). Chaque nombre ci-dessous est calculé à partir des fichiers ; rien n'est saisi à la main. Détail complet : `eval/results.json` ; sorties de chaque dossier : `eval/runs/<dossier>/`.

## Ce qui a été mesuré

- **Entrée** : pour chaque dossier, les seules images de plans disponibles dans cet environnement, `Plans-annotes.pdf` (une page raster de 2997 px par feuille, sans couche texte ni vectoriel). Ces pages portent les marques de couleur opaques d'un relevé automatique antérieur, dessinées par-dessus les symboles. L'estimateur traite les pixels colorés comme illisibles : une fenêtre dont le cœur du symbole (13 × 13 px au centre) touche une marque de couleur n'est jamais évaluée ni utilisée à l'entraînement ; ces zones sont signalées par feuille (`unreadable_markup_zones`) au lieu d'être comptées. Les marques de couleur ailleurs dans la fenêtre sont rendues non informatives en les transplantant sur des fenêtres négatives au même taux.
- **Référence (vérité)** : les projets Plan Expert de M. Dupuis (`reference/*Dupuis*.qpl`), recalés sur ces pages (appariement de pages et recalage de `src.validation.compare_qpl`, doublons retirés). S-1857 n'a pas de projet Dupuis dans cet environnement ; sa vérité est `reference-quantites.csv` (quantités par feuille, sans position) : seuls des écarts de quantité sont donc calculés pour ce dossier.
- **Protocole** : un dossier exclu à la fois. Pour chaque dossier à positions, le modèle (classifieur de fenêtres + seuil calibré, correspondance libellé → famille, style des compteurs, ratio de conduit) est appris sur les autres dossiers à positions seulement. S-1857 est évalué avec le modèle appris sur les cinq dossiers à positions.
- **Appariement** : affectation optimale un-à-un à moins de R px (px de page, largeur 2997 px) ; R principal = 25 px, aussi 15 px et 45 px (45 px ≈ le seuil de 1,2 % de la diagonale de compare_qpl). Familles = catégories de `src.qpl.categorie` (catégoriseur par mots-clés construit sur le corpus 2021-2026, complété par des votes de co-localisation).

## Résultats groupés (dossiers à positions)

| Portée | R (px) | Prédits | Dupuis | Appariés | Précision | Rappel | F1 |
|---|--:|--:|--:|--:|--:|--:|--:|
| toutes les pages | 15 | 8526 | 9383 | 824 | 9.7 % | 8.8 % | 9.2 % |
| toutes les pages | 25 | 8526 | 9383 | 1765 | 20.7 % | 18.8 % | 19.7 % |
| toutes les pages | 45 | 8526 | 9383 | 2683 | 31.5 % | 28.6 % | 30.0 % |
| pages marquées par Dupuis | 15 | 7362 | 9383 | 824 | 11.2 % | 8.8 % | 9.8 % |
| pages marquées par Dupuis | 25 | 7362 | 9383 | 1765 | 24.0 % | 18.8 % | 21.1 % |
| pages marquées par Dupuis | 45 | 7362 | 9383 | 2683 | 36.4 % | 28.6 % | 32.0 % |

### Rappel selon la lisibilité du symbole de Dupuis (toutes familles, R = 25 px)

La première ligne est la qualité du détecteur sans fuite possible : symboles dont le cœur est visible sur la page.

| Symbole de Dupuis | Nombre | Appariés | Rappel |
|---|--:|--:|--:|
| lisible (aucune marque de couleur sur le cœur) | 1134 | 414 | 36.5 % |
| cœur sous une marque de couleur (dessin détruit, non compté par conception) | 8249 | 1459 | 17.7 % |

### Par famille (toutes les pages, R = 25 px, même famille exigée)

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité total | Écart absolu moyen par dossier |
|---|--:|--:|--:|--:|--:|--:|--:|
| dispositif | 2380 | 5043 | 101 | 4.2 % | 2.0 % | -52.8 % | 526.3 % |
| luminaire | 4015 | 1351 | 296 | 7.4 % | 21.9 % | +197.2 % | 251.5 % |
| securite incendie | 1048 | 1233 | 65 | 6.2 % | 5.3 % | -15.0 % | 259.5 % |
| chauffage | 178 | 1021 | 6 | 3.4 % | 0.6 % | -82.6 % | 68.7 % |
| telecom donnees | 31 | 361 | 0 | 0.0 % | 0.0 % | -91.4 % | 76.7 % |
| indetermine | 851 | 215 | 2 | 0.2 % | 0.9 % | +295.8 % | 568.1 % |
| mecanique moteur | 8 | 77 | 0 | 0.0 % | 0.0 % | -89.6 % | 78.0 % |
| autre | 0 | 45 | 0 | — | 0.0 % | -100.0 % | 100.0 % |
| distribution | 15 | 37 | 0 | 0.0 % | 0.0 % | -59.5 % | 77.9 % |

Écart absolu moyen de la quantité totale sur les dossiers à positions : 174.4 %. Conduits : 23 feuilles comparables, écart absolu médian 164.5 %.

## Par dossier

| Dossier | Vérité | Appris sur | Seuil | Prédits | Marques Dupuis (placées / hors page) | Écart de quantité | P (R25) | R (R25) | F1 (R25) | Prédictions près du relevé antérieur | Dupuis près du relevé antérieur |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| S-1714 | .qpl Dupuis | S-1715, S-1769, S-1811, S-1844 | 0.25 | 4305 | 7502 / 0 | -42.6 % | 28.6 % | 16.4 % | 20.9 % | 9.1 % | 95.6 % |
| S-1715 | .qpl Dupuis | S-1714, S-1769, S-1811, S-1844 | 0.25 | 843 | 399 / 0 | +111.3 % | 10.3 % | 21.8 % | 14.0 % | 2.0 % | 75.7 % |
| S-1769 | .qpl Dupuis | S-1714, S-1715, S-1811, S-1844 | 0.1 | 731 | 116 / 0 | +530.2 % | 6.0 % | 37.9 % | 10.4 % | 2.1 % | 90.5 % |
| S-1811 | .qpl Dupuis | S-1714, S-1715, S-1769, S-1844 | 0.05 | 1633 | 681 / 0 | +139.8 % | 16.9 % | 40.5 % | 23.9 % | 4.7 % | 88.8 % |
| S-1844 | .qpl Dupuis | S-1714, S-1715, S-1769, S-1811 | 0.1 | 1014 | 685 / 23 | +48.0 % | 12.4 % | 18.4 % | 14.8 % | 6.9 % | 53.4 % |
| S-1857 | quantités seulement | S-1714, S-1715, S-1769, S-1811, S-1844 | 0.1 | 1042 | 1364 / 1584 | -23.6 % | — | — | — | — | — |

### S-1714

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité |
|---|--:|--:|--:|--:|--:|--:|
| dispositif | 188 | 4676 | 42 | 22.3 % | 0.9 % | -96.0 % |
| securite incendie | 924 | 1020 | 65 | 7.0 % | 6.4 % | -9.4 % |
| chauffage | 102 | 941 | 5 | 4.9 % | 0.5 % | -89.2 % |
| luminaire | 2590 | 386 | 186 | 7.2 % | 48.2 % | +571.0 % |
| telecom donnees | 0 | 335 | 0 | — | 0.0 % | -100.0 % |
| indetermine | 486 | 58 | 0 | 0.0 % | 0.0 % | +737.9 % |
| mecanique moteur | 0 | 38 | 0 | — | 0.0 % | -100.0 % |
| autre | 0 | 31 | 0 | — | 0.0 % | -100.0 % |
| distribution | 15 | 17 | 0 | 0.0 % | 0.0 % | -11.8 % |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| E101 | 40 | 0 |
| E200 | 264 | 74 |
| E201 | 166 | 792 |
| E202 | 125 | 800 |
| E203 | 112 | 818 |
| E204 | 111 | 818 |
| E205 | 98 | 817 |
| E206 | 99 | 819 |
| E207 | 66 | 422 |
| E208 | 71 | 300 |
| E209 | 24 | 2 |
| E300 | 369 | 187 |
| E301 | 209 | 123 |
| E302 | 158 | 30 |
| E303 | 142 | 31 |
| E304 | 143 | 31 |
| E305 | 146 | 31 |
| E306 | 135 | 31 |
| E307 | 86 | 24 |
| E308 | 81 | 15 |
| E309 | 39 | 0 |
| E400 | 257 | 88 |
| E401 | 204 | 227 |
| E402 | 164 | 314 |
| E403 | 156 | 139 |
| E404 | 159 | 138 |
| E405 | 154 | 140 |
| E406 | 163 | 141 |
| E407 | 94 | 84 |
| E408 | 80 | 66 |
| E409 | 41 | 0 |
| E500 | 149 | 0 |

Marques de Dupuis lisibles : 762 sur 7502 ; rappel sur celles-ci (R = 25 px) : 35.0 %.
Calibration (dossiers d'entraînement mis de côté) : seuil 0.25, rayon NMS 18.0 px, précision 21.6 %, rappel sur marques lisibles 32.3 %.

| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |
|---|--:|--:|--:|
| E200 | 4730.2 | 7137.2 | +50.9 % |
| E201 | 791.6 | 4480.0 | +465.9 % |
| E300 | 2424.0 | 9328.1 | +284.8 % |
| E400 | 2548.1 | 6739.3 | +164.5 % |
| E401 | 4703.4 | 4932.2 | +4.9 % |
| E402 | 4584.3 | 3934.9 | -14.2 % |
| E403 | 149.6 | 4012.0 | +2581.7 % |
| E407 | 2381.5 | 2786.9 | +17.0 % |
| E408 | 1747.5 | 2643.1 | +51.3 % |

### S-1715

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité |
|---|--:|--:|--:|--:|--:|--:|
| luminaire | 411 | 117 | 16 | 3.9 % | 13.7 % | +251.3 % |
| indetermine | 32 | 102 | 0 | 0.0 % | 0.0 % | -68.6 % |
| dispositif | 348 | 74 | 8 | 2.3 % | 10.8 % | +370.3 % |
| securite incendie | 31 | 48 | 0 | 0.0 % | 0.0 % | -35.4 % |
| mecanique moteur | 1 | 22 | 0 | 0.0 % | 0.0 % | -95.5 % |
| telecom donnees | 8 | 16 | 0 | 0.0 % | 0.0 % | -50.0 % |
| chauffage | 12 | 10 | 0 | 0.0 % | 0.0 % | +20.0 % |
| autre | 0 | 9 | 0 | — | 0.0 % | -100.0 % |
| distribution | 0 | 1 | 0 | — | 0.0 % | -100.0 % |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| E002 | 160 | 0 |
| E003 | 129 | 42 |
| E102 | 134 | 9 |
| E201 | 176 | 160 |
| E301 | 136 | 82 |
| T201 | 108 | 106 |

Marques de Dupuis lisibles : 79 sur 399 ; rappel sur celles-ci (R = 25 px) : 27.8 %.
Calibration (dossiers d'entraînement mis de côté) : seuil 0.25, rayon NMS 24.0 px, précision 23.1 %, rappel sur marques lisibles 40.0 %.

| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |
|---|--:|--:|--:|
| E102 | 2453.2 | 7341.2 | +199.3 % |
| E201 | 1643.3 | 4337.0 | +163.9 % |
| E301 | 1182.5 | 2954.9 | +149.9 % |
| T201 | 149.6 | 2865.7 | +1815.6 % |

- 2 Dupuis marks with junk labels removed (normalisation.json rebut list)

### S-1769

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité |
|---|--:|--:|--:|--:|--:|--:|
| luminaire | 207 | 47 | 9 | 4.3 % | 19.1 % | +340.4 % |
| dispositif | 451 | 32 | 5 | 1.1 % | 15.6 % | +1309.4 % |
| chauffage | 5 | 14 | 0 | 0.0 % | 0.0 % | -64.3 % |
| securite incendie | 26 | 12 | 0 | 0.0 % | 0.0 % | +116.7 % |
| mecanique moteur | 7 | 6 | 0 | 0.0 % | 0.0 % | +16.7 % |
| indetermine | 20 | 3 | 0 | 0.0 % | 0.0 % | +566.7 % |
| autre | 0 | 2 | 0 | — | 0.0 % | -100.0 % |
| telecom donnees | 15 | 0 | 0 | 0.0 % | — | — |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| E003 | 246 | 0 |
| E004 | 83 | 0 |
| E101 | 101 | 0 |
| E201 | 43 | 8 |
| E401 | 258 | 108 |

Marques de Dupuis lisibles : 10 sur 116 ; rappel sur celles-ci (R = 25 px) : 70.0 %.
Calibration (dossiers d'entraînement mis de côté) : seuil 0.1, rayon NMS 24.0 px, précision 20.5 %, rappel sur marques lisibles 40.6 %.

| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |
|---|--:|--:|--:|
| E201 | 187.0 | 2688.5 | +1338.1 % |
| E401 | 428.3 | 4633.9 | +982.0 % |

### S-1811

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité |
|---|--:|--:|--:|--:|--:|--:|
| luminaire | 461 | 285 | 42 | 9.1 % | 14.7 % | +61.8 % |
| dispositif | 912 | 166 | 30 | 3.3 % | 18.1 % | +449.4 % |
| securite incendie | 21 | 149 | 0 | 0.0 % | 0.0 % | -85.9 % |
| chauffage | 46 | 51 | 1 | 2.2 % | 2.0 % | -9.8 % |
| indetermine | 187 | 14 | 0 | 0.0 % | 0.0 % | +1235.7 % |
| mecanique moteur | 0 | 11 | 0 | — | 0.0 % | -100.0 % |
| autre | 0 | 3 | 0 | — | 0.0 % | -100.0 % |
| distribution | 0 | 2 | 0 | — | 0.0 % | -100.0 % |
| telecom donnees | 6 | 0 | 0 | 0.0 % | — | — |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| S267_ADD_21 | 269 | 271 |
| S267_ADD_22 | 380 | 199 |
| S267_ADD_23 | 101 | 6 |
| S267_ADD_24 | 234 | 150 |
| S267_ADD_25 | 121 | 0 |
| S267_ADD_3 | 142 | 0 |
| S267_ADD_4 | 386 | 55 |

Marques de Dupuis lisibles : 113 sur 681 ; rappel sur celles-ci (R = 25 px) : 73.5 %.
Calibration (dossiers d'entraînement mis de côté) : seuil 0.05, rayon NMS 24.0 px, précision 18.9 %, rappel sur marques lisibles 31.5 %.

| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |
|---|--:|--:|--:|
| S267_ADD_21 | 2329.5 | 4616.1 | +98.2 % |
| S267_ADD_22 | 3557.8 | 5923.4 | +66.5 % |
| S267_ADD_23 | 882.8 | 2561.1 | +190.1 % |
| S267_ADD_24 | 5521.1 | 4104.7 | -25.7 % |
| S267_ADD_4 | 20130.4 | 16981.7 | -15.6 % |

- 14 Dupuis marks with junk labels removed (normalisation.json rebut list)

### S-1844

| Famille | Prédits | Dupuis | Appariés | Précision | Rappel | Écart de quantité |
|---|--:|--:|--:|--:|--:|--:|
| luminaire | 346 | 516 | 43 | 12.4 % | 8.3 % | -32.9 % |
| dispositif | 481 | 95 | 16 | 3.3 % | 16.8 % | +406.3 % |
| indetermine | 126 | 38 | 2 | 1.6 % | 5.3 % | +231.6 % |
| distribution | 0 | 17 | 0 | — | 0.0 % | -100.0 % |
| telecom donnees | 2 | 10 | 0 | 0.0 % | 0.0 % | -80.0 % |
| chauffage | 13 | 5 | 0 | 0.0 % | 0.0 % | +160.0 % |
| securite incendie | 46 | 4 | 0 | 0.0 % | 0.0 % | +1050.0 % |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| E101 | 31 | 0 |
| E200 | 216 | 57 |
| E200D | 169 | 53 |
| E201 | 11 | 0 |
| E300 | 220 | 354 |
| E300D | 215 | 204 |
| E400 | 152 | 17 |

Marques de Dupuis lisibles : 170 sur 685 ; rappel sur celles-ci (R = 25 px) : 20.6 %.
Calibration (dossiers d'entraînement mis de côté) : seuil 0.1, rayon NMS 24.0 px, précision 21.6 %, rappel sur marques lisibles 51.7 %.

| Feuille | Conduit Dupuis (pi) | Conduit estimé (pi) | Écart |
|---|--:|--:|--:|
| E200 | 670.0 | 3067.9 | +357.9 % |
| E300 | 206.4 | 3512.6 | +1601.7 % |
| E400 | 365.8 | 2966.0 | +710.9 % |

### S-1857

| Famille | Prédits | Dupuis | Écart de quantité |
|---|--:|--:|--:|
| luminaire | 429 | 532 | -19.4 % |
| dispositif | 497 | 388 | +28.1 % |
| indetermine | 49 | 234 | -79.1 % |
| securite incendie | 48 | 137 | -65.0 % |
| telecom donnees | 14 | 46 | -69.6 % |
| mecanique moteur | 0 | 23 | -100.0 % |
| chauffage | 4 | 2 | +100.0 % |
| autre | 0 | 2 | -100.0 % |
| distribution | 1 | 0 | — |

| Feuille | Prédits | Dupuis |
|---|--:|--:|
| E200 | 80 | 0 |
| E400 | 72 | 77 |
| E401 | 94 | 240 |
| E402 | 84 | 316 |
| E403 | 88 | 161 |
| E404 | 49 | 0 |
| E405 | 97 | 77 |
| E406 | 82 | 215 |
| E407 | 63 | 181 |
| E408 | 72 | 92 |
| E409 | 43 | 5 |
| E600 | 218 | 0 |

Feuilles du relevé de Dupuis absentes du PDF évalué (quantités mises à part, 1584 au total ; écart y compris ces feuilles : -64.7 %) : E15 (ADME-01 implantation HQ), E400 (ADME-01), E401 (ADME-01), E402 (ADME-01), E403 (ADME-01), E405 (ADME-01 numerotee E404), E406 (ADME-01 numerotee E405), E407 (ADME-01 numerotee E406), E408 (ADME-01 numerotee E407), E409 (ADME-01 numerotee E408).

- count-only gold: reference-quantites.csv (transcription of the estimator's printed takeoff)

## Lecture de ces chiffres

- Les images de plans utilisées ici ne sont pas les dessins d'origine : les marques de couleur opaques d'un relevé antérieur couvrent le cœur de la plupart des symboles (voir le tableau de lisibilité). Ces symboles ne sont pas comptés, par conception : les compter reviendrait à retrouver les marques du relevé antérieur, pas à lire le dessin. Le rappel de bout en bout et les écarts de quantité sur ces entrées sont donc bornés par la part lisible ; la performance sur des PDF d'origine propres (ou sur les PNG de Dupuis) reste à mesurer dès que ces fichiers seront dans l'environnement.
- Les colonnes « près du relevé antérieur » comparent la part des prédictions et celle des marques de Dupuis situées à moins de 15 px d'une marque du relevé antérieur. Des valeurs proches ou plus basses pour les prédictions montrent que le détecteur ne retrouve pas simplement les marques de couleur.
- La lecture des légendes (codes de la couche texte, `legend.py`) ne s'active pas ici : les PDF évalués sont des images sans mots. Seul le détecteur visuel est mesuré.
- Les longueurs de conduit sont une estimation (ratio appris × arbre rectilinéaire sur les appareils détectés), pas un tracé des parcours.
- Aucun prix n'intervient (les projets de l'estimateur n'en contiennent pas).
