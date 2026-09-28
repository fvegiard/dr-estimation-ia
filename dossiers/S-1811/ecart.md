# Écart relevé automatique (v2) ↔ relevé estimateur — S-1811

Vérification indépendante du 2026-09-22.

**Base de comparaison : 1 bâtiment type A + site.**
- L'IA compte 1 bâtiment (R-001).
- Le relevé ACCEO de Daniel liste les quantités par bâtiment, avec « Mult Bloc ×6 » sur DISTRIBUTION, ALARME, SERVICE, CHAUFFAGE et ÉCLAIRAGE, et ×1 sur RISER et LAMPADAIRE (site). Voir `reference-quantites.csv`, colonne `section`.

**Référence retenue.**
- On retient les sections non barrées de `relevé final Daniel.pdf` (11 pages de scan).
- Les sections « DEMANDE DE PRIX », barrées aux pages 2 à 4 du scan, sont transcrites mais non retenues (`retenu=non`). Idem pour `relevé alarme incendie.pdf`, une version antérieure : 36 fumée, 64 klaxons et 5 strobes, contre 44, 63 et 6 dans le final.
- **Seule exception : G2 = 21 et G3 = 11** (scan p. 3). Ces deux types n'ont pas de ligne de quantité dans le final, où ils sont inclus dans « PRIX DE LOT FIXTURE ». Faute d'autre source, on les prend dans la demande de prix barrée.

**Transcription.**
- `reference-quantites.csv` : 291 lignes, avec la page du scan et la page ACCEO. Tout est lisible.
- Libellés tronqués par l'export (colonne coupée) : notés « (...) ».
- Le type de la ligne « FIXTURE TYPE 60X6 » (scan p. 3) n'est pas écrit. C'est C1 par recoupement avec la p. 9.

**Preuves.** Dossier `travail/ecart-preuves/`.
- Rendu vectoriel des PDF d'origine par `crop.py`, avec les marques IA entourées : rouge = texte, bleu = visuel.
- Les montages côte à côte sont faits par `sbs.py`, l'échantillon aléatoire par `rnd.py`.

## 1. Correspondance des nomenclatures

| Référence (Daniel, final) | Libellés IA | Justification |
|---|---|---|
| FIXTURE TYPE A1 / B1 / C1 / C2 / C3 / D1 / E1 | « X » + « X urgence » | L'urgence (remplissage gris) est un branchement du même appareil. La référence ne la distingue pas. |
| G2 / G3 (demande de prix, p. 3) ; LAMPADAIRE L2 / L3 / L5 (p. 8) | G2, G3, L2, L3, L5 | Mêmes types, feuille 503B |
| ENSEIGNE SORTIE / ONDULATEUR | X1 Enseigne d'issue / Mini-onduleur 12V | Correspondance 1 pour 1 |
| INT DECT 34 / DETECTEUR 360 2 / GRADATEUR 6 / interrupteur 15A 7 | Interrupteur avec détecteur 37 / Détecteur de présence plafond 2 / Gradateur 6 / Interrupteur unipolaire 4 | Correspondance 1 pour 1 |
| PANNEAU ALARME, ANNONCIATEUR, PANN SP1 + PS2, STATION MANUEL, FL-R / FL-T, KLAXON STROB, STROB, RELAIS ADRESSABLE, INTERFACE ADRESSABLE | FAP, FAAP, Bloc d'alimentation PS (2), Déclencheur manuel, FL-RX / FL-TX, Klaxon/stroboscope, Stroboscope mural, ARM, AIM | Correspondance 1 pour 1 |
| DETECTEUR A FUMÉE 44 + DETECTEUR GAINE 6 | Détecteur de fumée photoélectrique 50 | L'IA n'a pas de libellé « gaine » (§3-B) |
| prise duplex 15A 101 | Prise double 5-15R 108 + triangle 2 + WP 1 | Toutes sont en configuration 5-15R (légende 501B) |
| prise duplex 15/20A 26 | Prise double 5-20R 25 | Correspondance 1 pour 1 |
| prise duplex 20a GFI 10 | DDFT cercle 8 + DDFT triangle 2 | Correspondance 1 pour 1 |
| tel/data | Sortie télécom | Correspondance 1 pour 1 |
| PANN P1-3PPN4N-1 400A, PANN 600A, PANN 225A | Panneau 347/600V 1 + Panneau 120/208V 2 | Correspondance 1 pour 1 |
| TRANSFO 112.5 kVA ; SECTIONNEUR 400A | Transformateur ; Interrupteur principal 400A | Correspondance 1 pour 1 |
| ARMOIRE POUR APPAREILS ; MESURAGE (0) | Armoire de mesurage HQ type B ; Dispositif de mesurage GTB | Armoire ↔ armoire HQ. MESURAGE est à 0 dans la référence : non retenu par Daniel. |
| BARRE MISE A TERRE 2 | Barre de mise à la terre 3 | Correspondance 1 pour 1 |
| Interrupteur de sécurité 30A 8 ; INTERR 30A 3P 600V CEMA3R 3 | Sectionneur ≤240V 8 ; Sectionneur ≤240V WP 3 | Le boîtier CEMA 3R correspond à l'extérieur (WP) |
| RACCORD DIRECT 43 | Points de raccordement : plomberie 32 + portes 4 + volets 6 | « PANN CONTROL » est une ligne à part |
| CHAUFFE-EAU, MOTEUR HUM, PUI-REC, TF1, EV, CSI, BRASSEUR CF, PANN CONTROL | WH, HU, PU1, TF, EV, CS, HVLS CF, panneau de contrôle | Correspondance 1 pour 1 |
| SERPENTIN 7 + SERPENTIN 3 | EHC1 3 + EHC2 3 + EHC3 1 ; EHC1-006 3 | Correspondance 1 pour 1. Le coût unitaire diffère (15 $ et 25 $). |
| MOTEUR EF 3 | Départ futur ventilateur EF 3 | Rapproché par le nom EF (511B). L'IA le range en « distribution » ; il est **reclassé ici en mécanique**. |
| — (aucune ligne) | Raccordement UTA toit RT 3 ; Raccordement unité HE toit 3 | Rien dans la référence (§3-E) |
| PLINTHE C1.1 500W 34, C1.1 1500W 1, C4.1 10, C6.1 4, CONVECTEUR C2.2 3, C3.2 1, C5.1 2, C5.2 1 | Mêmes libellés : C1.1 34, C4.1 11, C6.1 4, C2.2 3, C3.2 1, C5.1 2, C5.2 1 | La ligne « C1.1 1500W » de la référence correspond à la 11e plinthe 1500 W de l'IA (famille identique) |
| PUIT ACCESS 5 ; POTEAU DE BOIS 11 | Puits d'accès 5 ; Poteau de bois 8 + note D 5 | Famille « autres » (RISER, ×1) |
| — | Raccordement prise UTA toit (fournie par fabricant) 3 | **Exclu des deux côtés** : pas de matériel DR (R-027) |

**Hors périmètre.** Ce que la référence compte et que l'IA ne relève pas :
- conduits, fils et câbles : toutes les lignes en P, plus la section « DEMANDE PRIX COND ET FIL » ;
- boîtes, couvercles, connecteurs, « drop de switch » 40, « drop de chauffage » 56, alimentation 0-10 V 181, parasismique 180, rails, tiges, quincaillerie ;
- plywood, fusibles 350 A (3), tiges MALT, Cadwell, étagères à câbles (2) ;
- bases de lampadaire, porte-fusibles et fusibles ;
- tout le RISER sauf les puits et les poteaux : haubans, traverses, câble ASC 477, conduits TYPE II, supports HQ ;
- boom truck, pépine, nacelle ;
- prix de lot et main-d'œuvre : 16 796 h.

En dollars, ce hors-périmètre représente l'essentiel des 2,52 M$ de matériel.

## 2. Tableau d'écart par famille (1 bâtiment + site)

| Famille | Référence | IA | Écart | Écart % | Explication |
|---|--:|--:|--:|--:|---|
| Luminaires (A1…E1, G2/G3, L2/L3/L5) | 251 | 250 | −1 | −0,4 % | G2 : 21 → 20. Le total masque **C1 −32 / C2 +32** (§3-A). E1 = 16 = 16. |
| Commandes / interrupteurs / détecteurs | 49 | 49 | 0 | 0 % | Le total masque **unipolaire −3 / interrupteur avec détecteur +3** (§3-C) |
| Secours (X1 + onduleurs) | 20 | 20 | 0 | 0 % | — |
| Alarme incendie | 150 | 153 | +3 | +2,0 % | ARM +3 au toit (§3-D). Fumée + gaine : 50 = 50, mais 44/6 contre 50/0 (§3-B). |
| Prises | 137 | 146 | +9 | +6,6 % | 5-15R +10 (§3-F), 5-20R −1 |
| Télécom / data | 14 | 15 | +1 | +7,1 % | Moins de 2 objets, non tranché |
| Distribution / panneaux / sectionneurs | 19 | 21 | +2 | +10,5 % | Mesurage GTB +1 (la référence met 0) ; barres MALT 3 contre 2 |
| Mécanique (raccordements, moteurs, serpentins, CP) | 75 | 80 | +5 | +6,7 % | RT +3, HE +3 (§3-E) ; raccord direct 42 contre 43 |
| Chauffage | 56 | 56 | 0 | 0 % | Libellé : C4.1 11 contre C4.1 10 + C1.1-1500W 1 |
| Autres (puits, poteaux) | 16 | 18 | +2 | +12,5 % | Poteaux 13 contre 11 (§3-G) |
| **Total des objets communs** | **787** | **808** | **+21** | **+2,7 %** | Somme des écarts absolus par type : **107 (13,6 %)** |

### Par feuille, pour les familles en écart

La référence n'est pas ventilée par feuille. Chaque ligne de la référence est affectée à la seule feuille où l'objet est dessiné.

| Feuille | Objet | Réf. | IA | Écart |
|---|---|--:|--:|--:|
| 505B (S267_ADD_21) | C1 (+ urgence) | 60 | 28 | −32 |
| 505B | C2 | 4 | 36 | +32 |
| 505B | Interrupteur unipolaire / avec détecteur | 7 / 34 | 4 / 37 | −3 / +3 |
| 503B (S267_ADD_4) | G2 | 21 | 20 | −1 |
| 503B | Poteaux de bois | 11 | 13 | +2 |
| 508B (S267_ADD_24) | Fumée / gaine | 44 / 6 | 50 / 0 | +6 / −6 |
| 507B (S267_ADD_23) | ARM | 0 | 3 | +3 |
| 507B | Raccordement RT1 / HE1 | 0 / 0 | 3 / 3 | +3 / +3 |
| 506B (S267_ADD_22) | Prise 5-15R (tous symboles) | 101 | 111 | +10 |
| 506B | Prise 5-20R | 26 | 25 | −1 |
| 506B | Télécom | 14 | 15 | +1 |
| 506B | Raccord direct | 43 | 42 | −1 |
| 506B | Plinthes C4.1 / C1.1-1500W | 10 / 1 | 11 / 0 | +1 / −1 |
| 502B (S267_ADD_3) | Mesurage GTB / barres MALT | 0 / 2 | 1 / 3 | +1 / +1 |
| 511B (S267_ADD_25) | EF (futur) | 3 | 3 | 0 |

## 3. Vérification des écarts (qui a raison)

| # | Écart | Verdict | Preuve |
|---|---|---|---|
| A | C1 −32 / C2 +32 | **IA** | Le texte vectoriel donne, pour l'AO `S267_5` : C1 = 60, C2 = 4. Pour l'addenda MEP-01 `S267_ADD_21` : C1 = 28, C2 = 36 (`texte/*-mots.csv`). L'addenda change les 32 spots des cabines douche/WC en C2, sous un nuage de révision. La référence reprend les chiffres de l'AO. Preuve : `05-C1-C2-AO-vs-MEP01.png`, zone (960–1300, 1960–2190) pt. |
| B | Fumée +6 / gaine −6 | **Référence** (pour le classement ; le total est juste) | 508B, points (674, 1849), (912, 1849), (1556, 1849), (1875, 1849), (2489, 2097) et (2489, 2141). Chaque détecteur porte une **tige** et est collé à un ARM de volet coupe-feu. Le détecteur de fumée de la légende 501B n'a pas de tige, pas plus que ceux des dortoirs (1067..1154, 1701). La référence les compte en « DETECTEUR GAINE » (2,5 h/u contre 0,5 h). L'IA a vu la différence (R-030), mais les a laissés en fumée. Preuve : `02-detecteurs-gaine-6.png`. |
| C | Unipolaire −3 / détecteur +3 | **Référence** | 505B, points (267, 2022) entreposage B1-02, (1791, 2033) pièce technique B1-44 et (1791, 2122) salle des gicleurs B1-45. Les trois symboles sont un « $ » **tourné, sans l'éventail** du détecteur. Selon la légende 501B, ce sont des interrupteurs unipolaires. Les cabines et les WC accessibles portent l'éventail. L'IA a appliqué la règle « $ tourné = détecteur ». Preuve : `01-commandes-3-interrupteurs-simples.png`. |
| D | ARM +3 | **IA** | 507B, addenda : un ARM et une identification 1 sous un nuage de révision, près de RT1-001, -002 et -003, aux points (848, 1923), (1776, 1923) et (2817, 1923). Ces ARM sont absents de l'AO `S267_7`. La référence (10) ne compte que 508B. Preuve : `03-ARM-RT1-toit-AO-vs-MEP01.png`. |
| E | RT +3, HE +3 | **IA selon le plan**. Côté référence, probable prix de lot mécanique ou oubli | 507B : RT1-00x (circuits B, C, D) et HE1-00x (circuits E, F, G) sont alimentés depuis P1-3PPN4N-1, avec un symbole de moteur (image 03, à droite). Aucune ligne RT ou HE dans la référence. « MOTEUR EF 3 » correspond aux départs EF1, EF2 et EF3-007-101 (FUTUR) du 511B, que l'IA relève aussi (R-033). |
| F | 5-15R +10 | **IA selon le plan, et même −2 de trop peu** | (1) Buanderie : 9 prises 5-15R pour les laveuses, x = 561, circuits 16 à 32 ; le 511B dit « WASHING MACHINE LAUNDRY ROOM » ×9 (`08-prises-buanderie-9-laveuses.png`). L'écart de la référence vient probablement de là. (2) **Oubli de l'IA** : dans le module dortoir ouest, la 2e prise du circuit 7 n'est pas marquée, en haut vers (860, 1655) et en bas vers (860, 1859). Il y a donc 64 prises, soit exactement le tableau (`07-prises-dortoir-2-oubliees-circuit7.png`). L'IA avait noté l'écart en R-016 sans le résoudre. (3) WP 1 et triangles 2 : les symboles existent (R-019, R-020). Selon le plan, il y a donc 113 prises 5-15R contre 101 dans la référence. |
| G | Poteaux +2 | **Indécidable**. L'IA suit le plan à la lettre. | 503B : 6 poteaux en ligne (y ≈ 2073) + 2 dans l'encadré 6/510B (x = 2113) = 8 dessinés. La note D ajoute « cinq (5) poteaux supplémentaires à ceux déjà présents », soit 13. La référence en compte 11 ; les 2 de l'encadré 6 sont peut-être existants ou HQ. L'IA a signalé ce doute (R-035). Preuve : `04-poteaux-8-dessines-plus-5-noteD.png`. |
| H | Écarts de 1 : G2, 5-20R, télécom, raccord direct, mesurage GTB, barre MALT, C4.1 | Non tranchés (< 2) | G2 = 20 dans le texte vectoriel, dans l'AO comme dans l'addenda. MESURAGE est à 0 dans la référence : c'est un choix de Daniel, pas un oubli. |

**Échantillon aléatoire** : `random.seed(1811)` puis `random.sample` sur les 811 marques actives, dans l'ordre texte puis visuel (`rnd.py`). Image : `06-echantillon-10-marques-seed1811.png`. **Résultat : 10 sur 10 conformes.**

| # | Feuille | Libellé IA | (x, y) pt | Constat |
|---|---|---|---|---|
| 1 | 506B | 5-20R | (2434, 1874) | ✓ symbole 5-20R, circuit 14 |
| 2 | 508B | Klaxon/stroboscope | (1888, 1989) | ✓ boîtier F + 30cd |
| 3 | 508B | Fumée | (2145, 1701) | ✓ sans tige |
| 4 | 506B | 5-15R | (2596, 1745) | ✓ circuit 61 |
| 5 | 506B | 5-15R | (2909, 1821) | ✓ circuit 61 |
| 6 | 505B | C1 | (743, 2168) | ✓ normal (non rempli) |
| 7 | 503B | Poteau note D | (120, 2030) | ✓ conforme à la note ; aucun symbole (virtuel) |
| 8 | 505B | D1 urgence | (2546, 1912) | ✓ plein gris (R-010 confirmé) |
| 9 | 505B | C3 | (601, 2158) | ✓ normal |
| 10 | 506B | 5-15R | (838, 1859) | ✓ bon symbole. Mais sa **voisine du même circuit 7 n'est pas marquée** : c'est ce qui a révélé l'oubli du §3-F. |

## 4. Verdict

- **Écart net sur les objets communs : +21 (+2,7 %).** Le critère de Francis (≤ 5 % au total) est **respecté**.
- **Par poste majeur (critère ≤ 10 %)** : respecté partout sauf pour la distribution, à +10,5 %, soit 2 objets tous deux explicables (voir tableau ci-dessous).
- **Par type d'appareil**, le critère ne tient pas : C1 −53 %, C2 +800 %, gaine −100 %, unipolaire −43 %, ARM +30 %. Sur C1/C2 et ARM, c'est la **référence** qui n'a pas suivi l'addenda MEP-01.

| Poste | Écart |
|---|--:|
| Luminaires | −0,4 % |
| Commandes | 0 % |
| Secours | 0 % |
| Alarme | +2,0 % |
| Prises | +6,6 % |
| Télécom | +7,1 % |
| Distribution | **+10,5 %** : mesurage GTB mis à 0 par Daniel, 1 barre MALT de plus |
| Mécanique | +6,7 % |
| Chauffage | 0 % |

- **Items manquants non signalés en réserve (critère : aucun) : 1, critère non respecté.**
  - **3 interrupteurs unipolaires** relevés comme interrupteurs à détecteur (B1-02, B1-44, B1-45). Aucune réserve : R-015 ne parle que des cabines.
  - Les **6 détecteurs de gaine** sont à la limite. R-030 les signale bien (« pourrait s'agir de détecteurs dédiés… à confirmer »), mais ils restent comptés en fumée, sans libellé distinct.
  - Les 2 prises oubliées au dortoir sont couvertes par R-016.
- **Utilisable tel quel ?** Non, mais **après corrections légères**, oui. Sur les objets, le relevé est aussi juste que celui de Daniel et plus à jour : il applique C1→C2, l'ARM au toit et RT/HE. L'estimateur doit :
  1. appliquer le facteur ×6 ;
  2. reclasser 6 fumée en gaine et 3 interrupteurs à détecteur en unipolaires ;
  3. ajouter 2 prises au dortoir ;
  4. trancher le nombre de poteaux (11 ou 13), le mesurage GTB et les départs EF futurs.

  Conduits, fils, boîtes et main-d'œuvre restent entièrement à faire.

### Erreurs systématiques de l'IA (règles à corriger dans la méthode)

1. **Un symbole hors légende est rangé dans le libellé le plus proche** (détecteur à tige compté en fumée). Cette erreur était déjà relevée en v1 et n'est pas corrigée.
   - Règle : un symbole qui diffère de la légende reçoit un libellé « à classer : <description> ».
   - Un détecteur à tige accolé à un ARM de volet ou de gaine = « détecteur de gaine ».
2. **L'orientation d'un symbole sert à le classer** (« $ tourné = détecteur »).
   - Règle : on classe sur les attributs graphiques (éventail, remplissage, lettres), jamais sur la rotation.
   - Chaque libellé à variante est validé par un zoom sur au moins 3 occurrences hors série.
3. **Une réserve chiffrée plan / tableau reste sans suite** (R-016 : 62 contre 64). Quand le tableau 511B donne un nombre par circuit, il faut recompter le circuit sur le plan jusqu'à égalité, ou pointer la paire manquante. Dans les séries répétées, surveiller les paires de symboles collés (même circuit).
4. **Les tableaux et schémas sont intégrés sans filtre d'achat** (départs futurs EF, mesurage GTB). Règle : ajouter une colonne `achat_DR` (oui / non / à confirmer). Un départ « FUTUR » ou un appareil fourni par autres ne se compte pas comme un objet.

## 5. v1 → v2

Sur la grille de v1 (sans poteaux ni barres MALT, EF = HE) :

| | Total | Référence | Écart |
|---|--:|--:|--:|
| v1 | 792 | 773 | +2,5 % |
| v2 | 792 | 773 | +2,5 % |

Sur la grille complète de ce rapport, v2 = 808 contre 787 (+2,7 %). Le total net est identique, mais sa composition a changé.

**Corrigé depuis v1**
- Erreur systématique n° 2 de v1 (schémas et tableaux non exploités) : **corrigée**. Armoire HQ, barres MALT, poteaux 5 → 13 (note D), départs EF.
- E1 : 15 → 16 (réglette sans étiquette, R-009).
- Erreur n° 4 (achat par autres) : **en partie corrigée**. Les prises UTA sont bien isolées, mais le mesurage GTB et les départs futurs sont comptés.

**Non corrigé**
- Erreur n° 1 (symbole hors légende) : le **détecteur de gaine** est toujours compté en fumée, pour la 2e fois sur ce dossier.
- Erreur n° 3 (recoupement entre feuilles) : non vérifiable ici, faute d'écart ARM ou AIM nouveau.

**Régressions**
- **Commandes** : v1 avait 7 unipolaires et 34 à détecteur, comme la référence. v2 en a 4 et 37 : nouvelle règle fautive « $ tourné = détecteur ».
- **Dortoir** : 2 prises du circuit 7 oubliées. Les duplex passent de 110 à 108.
- La v2 fait donc **une erreur de classement de plus** que la v1, pour un total net inchangé.
