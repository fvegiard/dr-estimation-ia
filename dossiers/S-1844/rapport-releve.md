# Rapport de relevé — S-1844 SAQ Varennes (électricité, 12 pages)

## Méthode
1. Classement des 12 pages d'après les aperçus et les cartouches (`feuilles-classement.csv`) :
   - 6 plans : E200D, E200, E201, E300D, E300, E400 ;
   - 2 légendes : E100, E101 ;
   - 1 schéma : E102 ;
   - 1 détail : E103 ;
   - 2 pages de devis : E001, E002.
   L'échelle des plans est 1/4" = 1'-0" (≈ 1:48).
2. Nomenclature lue sur les légendes :
   - E101 : tableau d'éclairage et contrôles nLight ;
   - E100 : légende électrique, CVC, sorties et abréviations (E.C., E.D., N., R.).

   Le fichier compte 94 libellés, dont 35 reconnus par étiquette texte.
3. Occurrences par étiquettes : `extract_occurrences.py` a produit 480 lignes. J'ai retiré 1 doublon du PDF (U2). J'ai ajouté à la main 144 lettres seules, qu'une regex globale ne peut pas cibler sans faux positifs (bulles d'axes C/E, thermostats T et relais R de E200) : 15 « T » sur E300, et R, H, C, J, W, M, E sur E300D.
4. Occurrences visuelles : j'ai parcouru E200 zone par zone (N. = neuf). J'ai aussi relevé E201, les boîtes de jonction et l'enseigne sans étiquette de E300, les boîtes de E400, et une partie des symboles sans étiquette de E300D.
5. J'ai recoupé les cédules PA (M) et PP (EC) de E102 avec les raccordements relevés au plan (voir R-023) : aucun double compte, aucun départ neuf oublié.
6. Aucun addenda ni export d'estimateur n'a été reçu.

## Totaux par feuille

| feuille | texte | visuel | total |
|---|--:|--:|--:|
| E200D (démolition prises) | 82 | 0 | 82 |
| E200 (prises & services) | 0 | 79 | 79 |
| E201 (toiture) | 0 | 1 | 1 |
| E300D (démolition éclairage) | 180 | 46 | 226 |
| E300 (éclairage) | 361 | 7 | 368 |
| E400 (conduits sécurité) | 0 | 16 | 16 |
| E101 (forfait mise en route) | 0 | 1 | 1 |
| **Total** | **623** | **150** | **773** |

Principaux postes :

- **E300 (éclairage)**
  - Projecteurs : D3-N 102, D3-NT1 21, D4-N 27, D4-NT1 22.
  - Rails : R12-NS 23, R8-NS 8, R6-NS 4, R4-NS 5.
  - Linéaires et luminaires : S20-N 5, O8-N 2, P2 31, P1 4, J1 8, G4 6, G3 2, K3 3, B-B 2, profilé T 20 (+ 5 boîtes de jonction).
  - Sorties : U1 3, U2 7, U3 6, U6 1, U9 1, + 1 enseigne à confirmer.
  - Contrôles : NPP16 10, NPP PCD 3, NPP20 2, NPOD 2, NPODMA 3, WSXA 6, WSXA-G 4.
  - Autres : SN 9, AA 9 (bailleur).
- **E200 (prises & services)**
  - Prises : duplex 16, circuit indépendant 4, BX caisse 11, 30 A UPS 1, affleurement 1, relocalisées 4.
  - Télécom : sorties télécom 6, sorties conduit dalle 5, haut-parleur 1, contrôle de volume 1.
  - Chauffage : plinthes 5, relais BT 4, thermostats 3 (électricien) + 2 (CVAC) + 1 relocalisé.
  - Raccordements : SE 2, BV-01, CE-1, PR-1 + démarreur, volet, sèche-mains 2, minuterie, thermostat à action inversée ; à confirmer : VE-01 et BX 4 pi.
- **E201 (toiture)** : raccordement du ventilateur VE-02.
- **E400 (conduits sécurité)** : 5 boîtes de tirage, 10 descentes avec boîte 4x4, 1 boîte 2x2.

## Ce qui n'a pas pu être relevé ou reste à compléter
- **Longueurs** à métrer : conduits sous dalle (E200), conduits EMT (E400, tronc 1-1/2 estimé à ≈ 150 pi) et profilés T.
- **Démolition E200D** : 82 E.D. sous un seul libellé, sans ventilation par type (R-025).
- **Démolition E300D** : le relevé visuel des symboles sans étiquette est partiel (entrepôt, bureaux et toilettes non parcourus en détail) (R-026).
- **Symboles à classer** : « à confirmer » ou hors légende, listés dans `reserves.md` (R-007, R-009, R-016 à R-019).
- **Annotations rouges sur E103** (révision probable) non reportées (R-014).

## Contrôle final
Chaque libellé des deux fichiers d'occurrences a été vérifié à la main contre `nomenclature.csv`. La commande `cut | sort -u` n'a pas pu être lancée : les commandes composées étaient refusées dans cette session. Les marques ont été contrôlées par zoom (`zoom.py`) sur E200 sud et E300 nord-est : elles tombent sur les symboles.

## Limites
Le relevé visuel repose sur des zooms d'environ 500 pt. Les symboles de prises (plein, demi-plein) ont été distingués à l'œil (R-021). Les scripts d'analyse ad hoc (python, awk) étaient bloqués. Le tri des mots s'est donc fait par recherche d'étiquettes et par lecture des zooms.
