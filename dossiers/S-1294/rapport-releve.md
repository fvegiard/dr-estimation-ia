# Rapport — S-1294, feuille E201 (2E et 3E étage), rév. 4, 2024-10-08 — version corrigée

PDF reçu = image pure (5399×3600, sans texte ni vecteur) : relevé 100 % visuel, coordonnées en px du raster (pas en points PDF).
Référence humaine : `reference/S-1294-E201-human-reference.qpl` (téléchargé de GitHub, **jamais modifié**).
Légende et cédule : **absentes** du fichier (seulement 2 notes spécifiques, 1 note de câbles 2 h, encadrés de circuits) → types provisoires.
Le ZIP « Granby-page-by-page » (chemin Windows) n'est pas accessible depuis cette session : le format des images est le mien.

## Corrections faites (avant → après : `avant-apres/`)
1. **Retrait des 36 avertisseurs** (18 + 18) : aucun compteur humain ne leur correspond.
2. **Ajout de 48 repères de logements TYPE A–G** (A 4, B 8, C 8, D 4, E 18, F 4, G 2 ; 24 par étage) : le type est lu sur le plan
   (« TYPE X » dans chaque logement, 48/48 conformes au QPL, planches `verif/types_logements_*.png`). Catégorie séparée : `repere_logement`.
3. **Ajouts vérifiés sur planche** (`verif/planche_*.png`, symbole visible dans la zone ±20 px) : 7 cercles à point (TYPE H), 4 appareils muraux de cages,
   6 icônes DEBIT, 2 sorties (2e pictogramme du bloc double), 3 K○ + 1 K○ du sas 2E (4e), 2 disques de cage, 1 hexagone C 750 W, 1 icône ≈ (SW1 du 2E).
4. **Corrections d'étiquette/position** : « T » sous K du hall = « F » ; K du 2E lu à 1790 (3E : 1680) ; boîte E du 2E déplacée de 20 px ; carrés PSU1A-41 rattachés à DIRECT.
5. **Non ajoutés (non vérifiés sur le plan)** : C 1250 W à (4872,1694) et C 750 W à (1596,1046) en px humains — aucun hexagone visible dans la zone.

## Comparaison (méthode explicite : `comparer_reference_E201.py`, `appariement-E201.csv`)
 : rappel 295/297 = 99.3 % ; précision 295/298 = 99.0 % (tolérance 40 px humain, appariement un-à-un par distance croissante).
Repères de logements A–G, comparés à part : 48/48 (type identique, ≤ 150 px humain).
**Seuil 95 % atteint (99,3 % de rappel), mais à lire avec prudence** : 24 des appareils ajoutés ont leur **position** proposée par le QPL humain
(symbole confirmé à la vue, position non mesurée indépendamment) et 3 positions/étiquettes ont été corrigées d'après lui. Sans ces 24 ajouts,
le rappel indépendant serait 271/297 = 91,2 %. Les correspondances compteur↔libellé sont déduites de la géométrie, pas d'une légende.

## Comptes par catégorie, symbole et étage
| Catégorie | Symbole (libellé provisoire) | 3E | 2E |
|---|---|--:|--:|
| annotation | Bulle 1 (renvoi) | 1 | 1 |
| annotation | Bulle 2 (renvoi) | 1 | 1 |
| annotation | Bulle A | 3 | 3 |
| appareil | Appareil mural de porte (cercle à tige) — à classer | 19 | 19 |
| appareil | Boîte VE-12 (étiquetée) | 0 | 1 |
| appareil | Boîte à diagonale + E (escalier) — à classer | 6 | 6 |
| appareil | Boîtier DP2 avec batterie — à classer | 3 | 3 |
| appareil | Bulle B (boîtiers quincaillerie) | 2 | 2 |
| appareil | Capteur OS3 (étiqueté) | 12 | 12 |
| appareil | Carré F | 5 | 5 |
| appareil | Carré K (station/module) — à classer | 5 | 5 |
| appareil | Carré R — à classer | 3 | 3 |
| appareil | Carré T (étiqueté) | 4 | 5 |
| appareil | Carré à croix PSU1A-41 (étiqueté) | 1 | 1 |
| appareil | Cercle à point (près de H) — à classer | 3 | 4 |
| appareil | Disque B1-xxx (secours ou détecteur) — à classer | 12 | 14 |
| appareil | Enseigne de sortie | 5 | 5 |
| appareil | Hexagone C (chauffage 1250 W ?) — à classer | 8 | 8 |
| appareil | Icône sous Mx2/T (débit) — à classer | 3 | 3 |
| appareil | Icône ≈ sous T (compté SW1 par l'estimateur) — à classer | 0 | 1 |
| appareil | Luminaire cercle+support (corridor/hall) — à classer | 36 | 36 |
| appareil | Module ISO | 4 | 4 |
| appareil | Module MRA | 3 | 3 |
| appareil | Module Mx2 | 4 | 4 |
| appareil | Module RM | 4 | 4 |
| appareil | SW1 (étiqueté) | 2 | 2 |
| appareil | Symbole K○ (sas ascenseur) — à classer | 0 | 4 |
| repere_logement | Repère logement TYPE A | 2 | 2 |
| repere_logement | Repère logement TYPE B | 4 | 4 |
| repere_logement | Repère logement TYPE C | 4 | 4 |
| repere_logement | Repère logement TYPE D | 2 | 2 |
| repere_logement | Repère logement TYPE E | 9 | 9 |
| repere_logement | Repère logement TYPE F | 2 | 2 |
| repere_logement | Repère logement TYPE G | 1 | 1 |
| | **Total** | **173** | **183** |

## Réserves
- R-001 : types non lus faute de légende (tous les libellés « à classer ») ; hypothèses seulement.
- R-002 : « 1250 W / 750 W / 1750 W » = puissances probables de convecteurs ; les traits ne sont pas comptés, seulement les hexagones C/R.
- R-003 : aucune prise ni interrupteur sur cette feuille (le QPL humain non plus) ; carrés gris à 4 points = fond architectural.
- R-004 : 3 appareils de mon relevé sans équivalent humain (2 « T », 1 disque) et 2 repères humains non vérifiés (point 5) : écart résiduel.
- R-005 : bulles A, 1, 2 = renvois, catégorie `annotation`, exclus de la comparaison.
- R-006 : circuits (PSU1A-…, PP1A-…) et boucles BA… = texte de rattachement, non comptés. RDC et 4E absents du fichier.
- R-007 : jeu de référence global non rejoué (aucune modification de `releve/` ni de la compétence) ; ce relevé n'entre pas dans `build_qpl.py` (px raster).

## Fichiers
`occurrences-visuel.csv` (356 lignes, colonne `categorie`), `marques/E201-3E-marque.png`, `marques/E201-2E-marque.png`, `marques/E201-*-hall-marque.png`,
`verif/` (planches), `avant-apres/`, `ecart-E201.md`, `appariement-E201.csv`, scripts `inventaire_visuel.py`, `dessiner.py`, `comparer_reference_E201.py`.
