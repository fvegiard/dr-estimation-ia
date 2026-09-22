# Rapport de relevé — S-1689

**Projet :** réaménagement de la mezzanine et de la cour arrière de l'usine de pultrusion, 1830 rue Marie-Victorin, Saint-Bruno-de-Montarville (Direktion 360, dossier 21-0291-01, émis pour construction rév. 1, 2025-12-18).

**Source :** `Pultrusion Plan Électrique.pdf`, 6 pages. Aucun addenda. Aucun export d'estimateur.

## Méthode
1. **Classement des 6 pages.** Chaque aperçu a été ouvert et le cartouche lu (voir `feuilles-classement.csv`). Les pages 3 et 4 ne sont pas des doublons : ce sont la légende (E003) et le plan E004, dont les cartouches sont mal numérotés (R-001).
2. **Nomenclature.** Elle a été tirée des tableaux de légende de E001_2 : alarme, interrupteurs, BlueEcosystem, CVC, distribution, télécom, prises, éclairage, urgence. Des libellés « à confirmer / à classer » ont été ajoutés pour chaque symbole hors légende. Au total, 66 libellés.
3. **Étiquettes texte** (`extract_occurrences.py`). Seules DP (RooM-PIR), Z1 (BBR-HV) et B (luminaires de l'abri, E005) existent en texte vectoriel. Six faux positifs ont été exclus avec `exclure=1` : cinq bulles d'axe « B » sur E002_2 et le « B » du plan clé de E005.
4. **Relevé visuel.** Il couvre les 3 plans de E002_2 (services mezzanine, éclairage mezzanine et incendie, services et éclairage RDC), zone par zone, avec `zoom.py` (fenêtres d'environ 155 × 200 pt). S'y ajoutent l'unifilaire, les cédules PP-MEZZANINE et PS-MEZZANINE, les notes, et le schéma de principe et les détails de E006.
5. **Cédules et unifilaire.** Chaque départ vers un équipement a été apparié aux symboles du plan :
   - PP-1/3/5/7 (serpentins) : 4 raccordements ;
   - PP-2/4/6 (transformateur) ;
   - PP-8/10 (aérothermes des escaliers) ;
   - PP-12 (éclairage de l'abri, E005) ;
   - PS-20 (ventilateurs des salles de bain) ;
   - PS-42 (boîtes à volume variable) ;
   - PS-52 (VE-2) ;
   - PS-54/56 (CO-1).

   Tout élément déjà présent au plan n'est compté qu'une fois (R-023). Le départ PP-23/25 (chauffage 2100 W) n'a aucun appareil au plan et n'est pas relevé (R-014).
6. **Notes « fournir et installer ».** Elles ont été converties en articles : barre de MALT, contreplaqué ignifuge, protections ignifuges, trappes d'accès, raccordement à l'auget, services du technicien en alarme, programmation des contrôles, fixation du transformateur.

## Feuilles traitées
| feuille | cartouche réel | type | marques relevées |
|---|---|---|--:|
| E001 | E-001 Devis – conditions générales | autre | 0 |
| E002 | E-002 Devis – conditions techniques | autre | 0 |
| E001_2 | E-001 (= E003) Légende | legende | 0 |
| E002_2 | E-002 (= E004) Services, éclairage, diagramme et panneaux | plan | 236 (23 texte + 213 visuel) |
| E005 | E-005 Éclairage abri extérieur | plan | 14 (texte) |
| E006 | E-006 Contrôle d'éclairage et détails | detail | 6 (visuel) |
| **Total** | | | **256** |

## Totaux par famille (toutes feuilles)
- **Luminaires : 70**
  - D1 2x2 : 35
  - B : 18 (14 à l'abri E005, 2 en salle des serveurs, 2 aux toilettes)
  - C : 7
  - A : 2
  - E réglette : 4
  - F en surface : 4
- **Secours : 18**
  - indicateurs de sortie : 2 muraux et 1 au plafond
  - phares doubles : 7
  - phares simples : 3
  - batteries 2 phares c/a sortie 144 W : 4
  - batterie 144 W à confirmer : 1
- **Commandes : 47**
  - interrupteurs (type à confirmer) : 18
  - interrupteur avec détecteur de présence : 1
  - détecteurs RooM-PIR (DP) : 13
  - contrôleurs BBR-HV (Z1) : 10
  - schéma de l'éclairage extérieur : minuterie 1, cellule PE 1, sélecteur 1, contacteur 1
  - programmation (forfait) : 1
- **Alarme : 13**
  - détecteurs de fumée : 2
  - stations manuelles : 4
  - klaxons : 3
  - klaxons miniatures : 3
  - services du technicien : 1
- **Prises : 46**
  - doubles : 26
  - USB : 1
  - comptoir 20 A : 10
  - comptoir DDFT (à confirmer) : 3
  - micro-onde : 2
  - lave-vaisselle : 2
  - extérieures DDFT : 2
- **Télécom : 10**
  - téléphone/données : 5
  - triangles ouverts (à confirmer) : 3
  - TV : 1
  - conduit de 2" à métrer : 1
- **Chauffage : 29**
  - plinthes : 11 (2 × 500 W, 1 × 750 W, 1 × 1500 W, 4 × 2000 W, 3 × 2500 W)
  - aéroconvecteurs muraux 4 kW : 2
  - aéroconvecteurs 2 kW (à confirmer) : 2
  - raccordements de serpentins : 4
  - thermostats de ligne : 2
  - thermostat BT STE241 : 1
  - thermostats BT fournis par la mécanique : 3
  - carrés « R » à classer : 4
- **Mécanique : 9**
  - moteurs de ventilateurs : 3
  - boîtes à volume variable : 3
  - condenseur CO-1 : 1
  - évaporateur EV-01 (à confirmer) : 1
  - volet « M » à classer : 1
- **Distribution et divers : 14**
  - panneaux : 2 (PP-MEZZ, PS-MEZZ)
  - transformateur 30 kVA : 1
  - interrupteur de sécurité 30 A E.I. : 1
  - barre de MALT : 1
  - raccordement à l'auget : 1
  - contreplaqué ignifuge : 1
  - fixation du transformateur : 1
  - protections ignifuges (par note) : 3
  - trappes d'accès : 2
  - « TA » à classer : 1

## Ce qui n'a pas pu être relevé
- **Longueurs non métrées :** conduits et conducteurs (artères de l'unifilaire, 0-10 V, conduit télécom de 2"). L'échelle est connue (≈1:128), mais aucun tracé de parcours n'est dessiné (R-018).
- **Circuit PP-23/25** (chauffage 2100 W) : introuvable au plan (R-014).
- **Écart de wattage sur PS-4** : environ 230 W de moins que la cédule. Un groupe de luminaires a peut-être été manqué (R-026).
- **Modules d'alarme adressables** : aucun n'est dessiné. Le système existant est à confirmer (R-021).
- **Comparaison avec l'estimateur** : non faite, faute d'export (R-002).

## Limites
- Les étiquettes d'appareils de E002_2 sont en vectoriel dessiné, et non en texte : presque tout le plan a été relevé visuellement, à environ 5 pt près.
- Les symboles de E002_2 sont denses et se chevauchent (étiquettes de circuit par-dessus les symboles). Les cas douteux sont en réserve.
- 33 réserves au total (`reserves.md`).
- Le contrôle final des libellés a été fait à la main : l'exécution de scripts de vérification a été refusée dans cette session (R-033).
