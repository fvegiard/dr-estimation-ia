# Rapport de relevé — S-1714

**Projet :** Le Vallem – Riviera, rue de l'Aigle, Carignan (ÉQUIPE SP, dossier 2025-46). Fichier `01-PLANS.pdf`, 44 feuilles, rév. 3 « émis pour construction 90 % » (18.02.2026).
Deux tours : 140 logements du RDC au 8e, sous-sol de stationnement, salles électriques. **Aucun addenda ni export d'estimateur n'a été fourni.**

## Méthode
1. **Classement** (`feuilles-classement.csv`) : 31 plans, 1 légende (E100), 2 tableaux (E101, E103), 7 schémas (E102, E106 à E111), 1 détail (E501) et 2 devis (E104, E105). Le vrai numéro et le titre du cartouche sont inscrits dans `note`. Échelle : 3/32 po = 1 pi (≈ 1:128) ; E500 au 1:200.
2. **Nomenclature** (78 libellés), lue dans les légendes de E100 et les cédules de E101. Dans les logements, les prises portent le **numéro de circuit** du panneau type (1,3 = cuisinière, 2,4 = sécheuse, 7 = laveuse, 10/12 = comptoir, 11 = réfrigérateur, 13 = micro-onde, 15 = salle de bain, 17/19/21 = prises, lettre ajoutée = demi-commandée). Ces numéros servent de jetons.
3. **Occurrences texte** : `extract_occurrences.py`, suivi d'un contrôle par zooms. 78 faux positifs exclus (`exclure=1`) : marges et plan clé, numéros de E500, bulles d'axes des toits, AF-1/AF-2 (unités d'air frais), « 10 » dans une note DCC, lettres R sans adresse. Les klaxons « K » ne sont retenus que s'ils ont une adresse voisine.
4. **Occurrences visuelles** : prises du circuit 23 (intérieures ou étanches), chauffage (plinthe ou aéroconvecteur selon le symbole, puissance selon l'étiquette), sorties câblo/informatique, panneaux de logement, prises des communs, VCFFM, équipements du sous-sol (ventilateurs V-x, pompes, bouilloires, aérothermes, panneaux, transformateurs, sectionneurs), luminaires des communs (une marque par étiquette de circuit), raccordements tirés des cédules E101, et sectionneurs de condenseurs (note E100).
5. **Addenda** : aucun. **Estimateur** : aucun export, donc pas de comparaison.

## Totaux : 7 385 marques (texte 4 950 + visuel 2 435)
| Feuille | Marques | | Feuille | Marques |
|---|--:|---|---|--:|
| E101 (cédules) | 15 | | E300 | 187 |
| E200 | 114 | | E301 | 119 |
| E201 | 789 | | E302–E306 | 31 chacune |
| E202 | 810 | | E307 | 24 |
| E203 | 819 | | E308 | 15 |
| E204 | 821 | | E400 | 99 |
| E205 | 819 | | E401 | 161 |
| E206 | 820 | | E402–E406 | 144–146 |
| E207 | 427 | | E407 | 90 |
| E208 | 304 | | E408 | 69 |
| E209 | 2 | | | |

Principaux totaux : prises doubles 1 616, demi-commandées 586, comptoir 278, étanches 163 ; 140 prises chacune pour cuisinière, sécheuse, laveuse, réfrigérateur et micro-onde ; 179 prises salle de bain ; 398 thermostats ; plinthes 470 ; aéroconvecteurs 150 ; 145 condenseurs, 147 évaporateurs, 148 sectionneurs ; 140 panneaux de logement ; 195 sorties télécom ; 467 luminaires, dont 325 à classer ; 33 enseignes ; alarme : 388 avertisseurs, 414 klaxons et klaxons/strobes, 140 détecteurs.

## Non relevé ou limites
- Types des luminaires de E300, E301, E308 et de la salle de toit de E307 non lus (R-010). Interrupteurs, détecteurs de mouvement, unités à batterie et projecteurs non vus (R-011, R-012).
- Alarme : PAI, ANN, GSM, téléphones pompier, haut-parleurs et détecteurs CO/DN/DG/DA non relevés (R-014).
- Unifilaire (E102), génératrice (E104) et branchement HQ (E500) non comptés article par article (R-019, R-021).
- Tous les labels des deux fichiers d'occurrences existent dans `nomenclature.csv` (vérifié par script).
- Outil refusé : script pymupdf lancé par `uv run` en chemin absolu, et `sed`. D'où le relevé dégradé des types d'éclairage.

STATUT : À VÉRIFIER
