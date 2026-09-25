# Rapport de relevé — S-1693

**Projet** : Construction d'une école primaire de 16 classes à Beloeil (CSS des Patriotes, projet 9382-109). Ingénierie : Tetra Tech / Ponton Guillot.
**Documents reçus** :
- PLA-E (25 feuilles E000 à E901) ;
- addenda E-01 du 2026-03-10 (22 pages : texte, devis 26 09 24 et extraits) ;
- addenda E-02 du 2026-03-20 (3 pages de texte).

Aucun export d'estimateur n'a été fourni.

**STATUT : À VÉRIFIER.** Trois commandes shell accessoires ont été refusées (R-001). Le relevé visuel est partiel : interrupteurs, typage de l'urgence et communication E701 (R-009 à R-011).

## Méthode
1. **Classement des 50 pages** dans `feuilles-classement.csv`. Les vrais numéros ont été relus dans les cartouches : les noms provisoires E401, E602 et E701 étaient des pages d'addenda (R-003). Plans comptés : E002, E101, E201, E202, E301, E302, E401, E402, E701 et E702. E303 et E304 (artères) sont des feuilles « plan » sans appareil compté.
2. **Nomenclature** dans `nomenclature.csv`, avec 102 libellés utilisés. Sources :
   - luminaires : tableau T-01 de E201 ;
   - chauffage : tableau T-03 de E301 ;
   - raccordements mécaniques : E581 (T-06 à T-15) ;
   - légende E001 : prises, communication, alarme incendie, sécurité, distribution ;
   - addendas : mini-klaxon, sectionneurs, camlock, carte IP.
3. **Occurrences par étiquettes** avec `extract_occurrences.py`, puis filtrage :
   - mots admis par famille et par feuille ;
   - bulles d'axes et cartouche exclus ;
   - tableaux T-01, T-03 et T-05 exclus ;
   - doublons de texte écartés.

   Au total, 1 482 occurrences brutes ont été ramenées à 1 275.
4. **Occurrences visuelles**, relevées sur des zooms de 420 × 290 pt au plus pour les prises et de 700 × 470 pt pour l'alarme incendie :
   - prises, télécom et raccordements divers sur E301 et E302 ;
   - stations, klaxons, KS, strobes et détecteurs de fumée sur E401 et E402 ;
   - prise sur potelet et sectionneur sur E101.

   Au total : 490 marques.
5. **Addendas E-01 et E-02 appliqués** en marques datées « add. » (R-018 à R-028).

## Totaux par feuille (marques)
| feuille | texte | visuel | total | contenu principal |
|---|--:|--:|--:|---|
| E002 implantation | 11 | 1 | 12 | 9 bollards B1, 2 lampadaires L1, stèle |
| E101 toiture | 1 | 2 | 3 | CON-001, prise sur potelet, sectionneur |
| E201 éclairage N1 | 459 | 1 | 460 | 334 luminaires, 62 détecteurs de mouvement, 63 appareils d'urgence |
| E202 éclairage N2 | 234 | 0 | 234 | 181 luminaires, 27 détecteurs, 26 appareils d'urgence |
| E301 services N1 | 185 | 251 | 436 | chauffage, 18 TP, 14 SE, 160 prises, 56 sorties télécom |
| E302 services N2 | 123 | 162 | 285 | chauffage, 15 TP, 84 prises, 40 sorties télécom, salle mécanique |
| E401 alarme N1 | 41 | 42 | 83 | 18 M/K, 9 klaxons, 8 KS, 4 strobes, 8 stations, 11 détecteurs |
| E402 alarme N2 | 39 | 28 | 67 | 16 détecteurs de conduit, 11 M/K, 4 klaxons, 2 KS, 6 strobes |
| E701 services auxiliaires N1 | 152 | 3 | 155 | 24 CP, 9 LC, 12 G, 16 caméras, 21 horloges, 17 WiFi, 12 DM |
| E702 services auxiliaires N2 | 30 | 0 | 30 | 13 horloges, 12 WiFi, 2 DM, 1 SBT |
| **Total** | **1 275** | **490** | **1 765** | |

**Par famille** :

| famille | marques |
|---|--:|
| luminaire | 526 |
| alarme (incendie et intrusion) | 269 |
| prise | 251 |
| telecom | 207 |
| chauffage | 194 |
| mecanique | 117 |
| commande | 89 |
| secours | 89 |
| distribution | 23 |

## Ce qui n'a pas pu être relevé (voir `reserves.md`)
- interrupteurs et gradateurs sur E201 et E202 (R-009) ;
- type exact des appareils d'urgence et position des accumulateurs (R-010) ;
- postes de classe, haut-parleurs, trompettes et sirènes sur E701 et E702 (R-011) ;
- métrage des artères E303 et E304, du massif E002 et de l'artère du camlock (R-006, R-015, R-022) ;
- système de commande d'éclairage basse tension 26 09 24 et E271 (R-008, R-028) ;
- appariement ligne à ligne des cédules E502 et E581 et de l'unifilaire E501 avec le plan (R-029) ;
- disjoncteurs ajoutés par les addendas : à chiffrer en cédule (R-023).

## Contrôle final
Tous les libellés de `occurrences-texte.csv` et de `occurrences-visuel.csv` existent dans `nomenclature.csv` : 0 manquant, vérifié par script. Les libellés sans occurrence (enseignes, phares et accumulateurs typés) ont été retirés de la nomenclature pour éviter des compteurs vides.

## Limites
Le relevé visuel repose sur des zooms, avec une précision d'environ 5 pt. Les ajouts d'addenda sont placés approximativement d'après les axes cités. Les positions de marques n'ont été contrôlées ni avec `traits.py` (neuf ou existant) ni sur le PDF annoté. Le projet étant une construction neuve, il n'y a pas d'existant ni de démolition.
