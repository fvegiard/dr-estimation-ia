# Rapport de relevé — S-1797

**Projet :** CSR, École William-Latter, agrandissement et réaménagement, 1300 rue Barré à Chambly. Plans d'électricité de Stantec (n° 157103764).
**Entrées :** les plans pour AO (32 pages) et les addendas 1 (20 p.), 2 (11 p.) et 4 (5 p.), soit 68 pages. Pas d'addenda 3 ni d'export de l'estimateur.
**Date :** 2026-09-22.

## Méthode suivie

1. **Classement :** les 68 pages sont classées dans `feuilles-classement.csv`. Pour chaque feuille, on retient la version la plus récente (addenda). Les 35 versions antérieures sont classées `remplacee`. Les feuilles retenues se répartissent ainsi : 16 plans, 1 légende, 2 tableaux, 7 schémas, 2 détails et 3 pages couverture.
2. **Nomenclature :** elle vient de la légende EL001 (révision 2, addenda 4), qui comprend le tableau des luminaires A1…W, le tableau des contrôles nLight, les tableaux du chauffage et des appareils divers, ainsi que les légendes de l'urgence, des prises, de l'alarme et du contrôle d'accès. S'y ajoutent l'unifilaire EL201 et le tableau des raccordements mécaniques EL408. On obtient 175 libellés. Aucun `jeton_regex`, parce que les plans ne portent pas d'étiquettes texte d'appareils.
3. **Occurrences texte :** `extract_occurrences.py` a été lancé et renvoie 0 occurrence. Voir la réserve R-033.
4. **Occurrences visuelles :** chaque plan a été parcouru par zooms de 400 à 700 pt avec `zoom.py`. Les coordonnées sont lues sur les règles, avec une précision d'environ 5 pt. Le neuf (trait noir) est séparé de l'existant (gris) : seul le neuf est relevé. Les éléments temporaires et démolis ont leurs propres libellés.
5. **Addendas appliqués :**
   - Addenda 1 : EL102, les éclairages EL301/303/305, le toit EL407 et les schémas EL603 à EL606.
   - Addenda 2 : l'unifilaire EL201/202, les raccordements EL404/406/408, l'alarme EL502/503/504 et les nuages UR-01, VCFF, EV-01/02 et détecteurs du niveau 2.
   - Addenda 4 : EL001, EL403 (nouvelle note 5 sur l'adoucisseur), EL405 et EL501 (nouveau PAI et GSM).
6. **Sans symbole au plan :**
   - Raccordements mécaniques recoupés avec EL408.
   - Notes « fournir et installer » comptées : mini-onduleurs, sèche-mains, câble chauffant de gargouille, disjoncteurs ajoutés dans des panneaux existants, cellule photoélectrique, minuterie et contacteur de l'éclairage extérieur.
   - Détails du monte-personne : prises DDFT, minuteries, luminaires du puits et contacts vers l'ascenseur.
   - MALT de EL202 : barres, brides et tiges.

## Totaux par feuille (marques visuelles)

| feuille | alarme | autre | chauffage | commande | démolition | distribution | luminaire | mécanique | prise | secours | total |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| EL101 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | 4 |
| EL102_ADD | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 6 |
| EL104 | 0 | 0 | 0 | 0 | 0 | 10 | 7 | 0 | 0 | 0 | 17 |
| EL201_ADD_2 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 3 |
| EL202_ADD_2 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 9 |
| EL301_ADD | 0 | 0 | 0 | 2 | 0 | 1 | 2 | 0 | 0 | 3 | 8 |
| EL302 | 0 | 0 | 0 | 35 | 0 | 0 | 45 | 0 | 0 | 3 | 83 |
| EL303_ADD | 0 | 0 | 0 | 93 | 0 | 1 | 182 | 0 | 0 | 54 | 330 |
| EL304 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 2 |
| EL305_ADD | 0 | 0 | 0 | 68 | 0 | 0 | 169 | 0 | 0 | 38 | 275 |
| EL402 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 21 | 0 | 23 |
| EL403_ADD_3 | 0 | 26 | 1 | 0 | 0 | 14 | 0 | 5 | 76 | 1 | 123 |
| EL404_ADD_2 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 61 | 0 | 0 | 69 |
| EL405_ADD_2 | 0 | 4 | 0 | 0 | 0 | 3 | 0 | 3 | 77 | 1 | 88 |
| EL406_ADD_2 | 6 | 0 | 4 | 2 | 0 | 1 | 2 | 35 | 2 | 0 | 52 |
| EL407_ADD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 2 | 0 | 8 |
| EL501_ADD | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| EL502_ADD_2 | 69 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 72 |
| EL503_ADD_2 | 38 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 41 |
| EL504_ADD_2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| **Total** | 117 | 31 | 14 | 200 | 2 | 56 | 407 | 112 | 178 | 101 | **1218** |

Occurrences texte : 0. Réserves : 34 (R-001 à R-034).

## Ce qui n'a pas pu être relevé

- EL102 de l'addenda 4, qui n'a pas été reçue.
- Le contenu éventuel d'un addenda 3.
- Les équipements propres aux schémas nLight EL601 à EL606 (NECY, NIO…), non recomptés.
- Les métrés linéaires : profilés, lignes aériennes provisoires, massifs.
- Le nombre de projecteurs sur les rails de la scène.
- La vérification neuf/existant par `traits.py`.
- Aucune comparaison avec l'estimateur, faute d'export.

## Limites

- Le relevé est entièrement visuel. Les zones denses (hall 156, classes du niveau 2, corridors) sont à recompter au contrôle qualité.
- Les profilés sont comptés par segment d'environ 1,2 m.
- Les luminaires en urgence ont été identifiés à la teinte grise sur le rendu.
- Trois commandes auxiliaires ont été refusées par la politique d'outils (R-032).

## Vérification des libellés

Chaque `label` d'`occurrences-visuel.csv` existe dans `nomenclature.csv`, vérifié par script : 0 libellé absent. `occurrences-texte.csv` est vide.
