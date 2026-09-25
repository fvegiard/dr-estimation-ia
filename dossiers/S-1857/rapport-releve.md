# Rapport de relevé — S-1857 Maison communautaire Saint-Michel (8615 boul. Saint-Michel)

Date : 2026-09-22. Dossier préparé par `prepare.py`, 22 pages. Aucun export d'estimateur n'était fourni (`estimateur/` vide), donc il n'y a pas de `comparaison-estimateur.md`.

## Méthode
1. **Classement** des 22 pages d'après le cartouche (`feuilles-classement.csv`) : 9 plans (E400-E409), 3 légendes (E102, E103, E104), 2 schémas (E200, E201), 1 tableau (E600_ADD), 1 page remplacée (E600_2), 1 détail vide (E500) et 4 pages « autre » (E000 page titre, E100/E101 devis, E150 implantation). Échelle 1:100 sur les plans.
2. **Nomenclature** construite à partir du tableau des luminaires et du tableau des spécifications (E102) et des légendes (E103/E104) : 63 libellés (`nomenclature.csv`).
3. **Étiquettes texte** : `extract_occurrences.py` a trouvé 964 occurrences. Nettoyage : bulles d'axes, « ESC. B », LV d'architecture, doublons, « SM » requalifié en sèche-main. Il en reste 909.
4. **Lecture visuelle** zone par zone (zooms 400×440 pt) des plans E400-E403 et E405-E409 : prises, sorties data, enseignes, phares, interrupteurs, distribution, alarme sans étiquette. Il y a 512 marques visuelles, dont 36 raccordements tirés des cédules de l'addenda et 1 de l'unifilaire E200.
5. **Addenda 02** : c'est une E600 complète (scan). Elle a été appliquée à la place d'E600 rév. 1, et ses ajouts (P-P1, BRVE-01/02) sont relevés.
6. **Recoupement cédules / plans** : un départ déjà dessiné au plan n'est pas recompté. Sont déjà au plan : HC-1, HC-2, CHE-1/2, CE-1/2, VRT-1, THP-1, SPP-1, SPP-ASC, EP-150, VE/VA/UV/UM/REF-DCHT, TRA, PAI, LV, hotte, cuisinières 110/140. Seuls les départs sans symbole au plan ont été ajoutés.

## Totaux par feuille (marques)
| feuille | contenu | marques |
|---|---|--:|
| E400 | Sous-sol éclairage | 77 |
| E401 | RDC éclairage | 248 |
| E402 | Niveau 1 éclairage | 317 |
| E403 | Niveau 2 éclairage | 161 |
| E404 | Toiture éclairage | 0 |
| E405 | Sous-sol alarme/prises/services + distribution | 91 |
| E406 | RDC alarme/prises/services | 216 |
| E407 | Niveau 1 alarme/prises/services | 180 |
| E408 | Niveau 2 alarme/prises/services | 90 |
| E409 | Toiture alarme/services | 4 |
| E600_ADD | Raccordements tirés des cédules (addenda 02) | 36 |
| E200 | Raccordement SE-1 (unifilaire) | 1 |
| **Total** | | **1 421** |

## Principaux totaux par article
- Luminaires : 201 DS1, 176 DS0, 50 DR5, 43 DR51, 11 DR52, 10 DMW1, 8 DW4, 4 DR2, 3 DS4, 2 DS2, 1 DW42, et 3 « à classer ».
- Commandes : 98 Do, 40 Di, 58 B, 2 Ba, 5 interrupteurs.
- Secours : 21 accumulateurs (dont 18 avec enseigne), 28 enseignes, 21 phares doubles, 12 phares simples.
- Prises : 262 duplex, 17 DDFT, 6 DDFT Ei, 11 micro-ondes, 21 mobilier, 3 cuisinières ; 62 sorties data.
- Alarme : 103 klaxons (dont 3 Ei), 6 avertisseurs visuels, 11 postes manuels, 6 détecteurs de fumée, 1 détecteur thermique, 6 Sx, 6 Ls, 5 ID, TRA, PAI.
- Raccordements : 22 CC, 7 LV, 6 sèche-mains, 10 pompes, 5 chauffage, 2 bornes VE, 6 éviers électriques, 17 équipements de cédule, 1 hotte.
- Distribution : 6 panneaux, 2 transformateurs, 2 sectionneurs, 1 MHQ.

## Ce qui n'a pas pu être relevé ou reste incertain
Voir `reserves.md` (25 réserves). Les points principaux :
- **Bornes VE BRVE-01/02** : présentes seulement dans la cédule de l'addenda, sans emplacement au plan (R-004).
- Symboles hors légende : luminaires ovales, cercles barrés, TS et symbole pointillé du SAS (R-005, R-010, R-011).
- Modules d'alarme Mi/Cx, batteries, résistances de fin de ligne : ils n'apparaissent que sur l'unifilaire E201 ou sur E102 et ne sont pas comptés (R-018, R-019).
- Doublons possibles : carrés pleins DDFT contre « évier électrique », et SPP-1 contre SPS-1 (R-013, R-015).
- Les cédules PS-2 à PS-4 de l'addenda n'ont pas été relues circuit par circuit, seulement pour les départs « Q » (R-004).

## Limites
- Coordonnées lues sur les règles des zooms, à environ 5 pt près.
- L'addenda est un scan sans texte : sa lecture est visuelle et ses coordonnées sont approximatives.
- Pas de comparaison avec l'estimateur (aucun export fourni).
- Contrôle final fait : chaque `label` des deux fichiers d'occurrences existe dans `nomenclature.csv` (0 absent).
