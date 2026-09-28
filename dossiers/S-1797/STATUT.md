# STATUT — relevé automatique « S-1797 »

Date : 2026-09-22 04:19 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 00 Addenda MEP-01_Plans_ELectricité.pdf | 18675493 | dc0c7228781c26f30fa84e21ab3f08c2606c14c00b87cdafbce6aa67de7f814a |
| 00 Addenda MEP-02_Plans_Électricité.pdf | 8176488 | 6d1d540e3ed68db7e4fbbe2f7f333cba51e418202519a065397c0e8ce36e1db0 |
| 00 Addenda MEP-04_Plans_Électricité.pdf | 3712605 | 576db28af7e54bc48183e19257e0b7b27b3e5d12c524eb9b076d225d985f0cb6 |
| 00 Électricité_Plans_pour AO.pdf | 42190400 | 64e37eca9699988aff598d1c083c572542d1fc276d1f142efe2b1c9e13a1f345 |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1797-Dossier-complet.pdf | 16506360 | daab9998cbb761be2c6bab1ed1841662d38405255bd7a0636df14a43b521a4b1 |
| S-1797-Plans-annotes.pdf | 16318115 | fd8a3c20e575e242ac4d9fbf04967609e5fd7ebaf1096e4c9c1df0cc230bbf98 |
| S-1797-Rapport-de-metre.md | 50052 | ce5730de746da3f4399b4f4285a867ae646c0907c286b0b99b7031c45da4ec7b |
| S-1797-Rapport-de-metre.pdf | 188469 | c66b33a4b098108fb92362ac382d0ede8bb0333b64b9ec8a06f11e67e4a5dda5 |
| journal-etapes.log | 9938 | afee4cb1fb6127b2aa5333331031fbb497931a27fd65f26f3cd67288567f1587 |
| S-1797-planexpert/S-1797.qpl | 190794 | f93772a8a07ee5cbcc0692dc931b26c62c473a08566758b273217f188539ad93 |

Le projet Plan Expert `S-1797.qpl` est dans `S-1797-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| prepare | 0.0 min | déjà à jour |
| agent Claude | 32.8 min | success / code 0 |
| build_qpl | 0.0 min | ok |
| render_pdf | 0.2 min | ok |
| total | 33.1 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : 436 · sous-type : success
- coût estimé (client, `total_cost_usd`) : 57.336306000000015 $ US
- jetons : entrée 598, cache créé 1769211, cache lu 71805412, sortie 149540
- session : `ee0971be-0747-5d2f-962e-a9f568c158d0` · dossier de travail : `/home/claude/releve-auto/runs/S-1797/OUTBOX/S-1797/travail`

### Résumé de l'agent

Le relevé S-1797 est écrit, mais il est à vérifier. Tout est visuel, trois commandes ont été refusées par la politique d'outils, et plusieurs zones denses sont à recompter.

- **Feuilles :** les 68 pages sont classées, dont 35 versions remplacées par un addenda. Les marques sont posées sur les 20 feuilles relevées (plans, schémas, tableaux) : RDC et niveau 2 (éclairage, services, mécanique, alarme), toit, extérieur, branchement, unifilaire et MALT.
- **Total : 1218 marques visuelles.** Les plus grosses familles sont les luminaires (407), les commandes (200), les prises (178), l'alarme (117), la mécanique (112) et l'urgence (101). La nomenclature compte 175 libellés, tous présents dans `nomenclature.csv`.
- **Aucune occurrence texte :** les plans Stantec n'ont pas d'étiquettes d'appareils, donc tout est lu sur les zooms, à environ 5 pt près.
- **34 réserves (R-001 à R-034).** Les principales :
  - l'addenda 3 n'a pas été reçu ;
  - EL102 est annoncée à l'addenda 4 mais absente du PDF ;
  - les profilés sont comptés par segment et restent à métrer ;
  - les schémas nLight EL601 à EL606 ne sont pas recomptés ;
  - 3 symboles hors légende sont relevés « à confirmer » ou « à classer ».
- **Ce qui manque :** les métrés linéaires, les projecteurs sur les rails de la scène, la vérification neuf/existant par `traits.py` (pas utilisé), et la comparaison avec l'estimateur, car le dossier `estimateur/` était vide.
- **Commandes refusées (R-032) :** mon script de carte des tracés neufs/existants, une commande `sed` et un script Python en ligne. J'ai fait autrement avec des scripts autorisés ; `zoom.py` et `extract_occurrences.py` ont fonctionné.
- **Fichiers :** `feuilles-classement.csv`, `nomenclature.csv`, `occurrences-texte.csv` (vide), `occurrences-visuel.csv`, `reserves.md`, `rapport-releve.md`.

STATUT : À VÉRIFIER

## reserves.md

# Réserves — S-1797 (École William-Latter, agrandissement et réaménagement)

Relevé du 2026-09-22. Chaque réserve donne la feuille, l'objet et la question ou la décision prise sans réponse.

## Addendas et périmètre

- **R-001** · tous · Addenda n° 3 : aucun fichier « MEP-03 » reçu. Si l'addenda 3 touchait l'électricité, il n'est pas reporté.
- **R-002** · EL102 · La page couverture de l'addenda 4 (EL701_ADD_3) annonce une révision d'EL102, mais le PDF MEP-04 ne contient pas EL102. Le relevé est fait sur EL102 de l'addenda 1. La feuille non reçue n'est pas relevée.
- **R-003** · doublons · Quand une feuille existe en plusieurs versions, on relève la plus récente : EL001_ADD_2, EL201/202_ADD_2, EL403_ADD_3, EL404/406/408_ADD_2, EL405_ADD_2, EL502/503/504_ADD_2, EL501_ADD, EL301/303/305/407_ADD. Les versions antérieures sont classées `remplacee`. Le contenu des nuages de révision a été lu (UR-01, VCFF, EV-01/02, CD-01/02/TR-01 au toit, détecteurs ajoutés au niveau 2). En revanche, les versions n'ont pas été comparées tuile par tuile hors des nuages.
- **R-004** · EL601-EL606 (schémas nLight) · Les relais, ponts, blocs et modules sont relevés sur les plans d'éclairage. Ils ne sont pas recomptés sur les schémas, pour éviter un double compte. Le NECY Eclypse (contrôleur), le NIO-1S et les éventuels équipements propres aux schémas **n'ont pas été relevés**. Il faut vérifier les schémas.
- **R-005** · EL103, EL701_ADD_2 (détails) · Pas de relevé : massifs HQ et détail 25 des évaporateurs. Les raccordements EV-01/EV-02 sont comptés sur EL406.

## Distribution / branchement

- **R-006** · EL101 · Les lignes aériennes provisoires (P5 → PP1 → PP2 → bâtiment) et le câble sur supports au toit (note 2) sont à métrer. L'échelle 1:300 est à confirmer.
- **R-007** · EL102_ADD · Les massifs MT 4×75 mm, télécom 3×78 mm et BT 4×100 mm sont linéaires, donc à métrer. Tronçons cotés lus : 13 300 mm et 19 750 mm.
- **R-008** · EL102_ADD / EL201 · Le poteau P6, le transformateur sur socle et le cabinet de mesurage HQ sont relevés. Qui les fournit (HQ ou entrepreneur) est à confirmer.
- **R-009** · EL102_ADD vs EL403_ADD_3 · L'armoire CDP-1 est comptée une seule fois, sur EL403 (salle électrique 162-1). La marque sur EL102 est écartée.
- **R-010** · EL201_ADD_2 · Aucune ligne de départ n'est posée sur l'unifilaire : tous les départs (PD1, PS1-PS4, TX1/TX2) sont relevés en plan (EL403). Le vérificateur doit contrôler les calibres et artères sur l'unifilaire.
- **R-011** · EL202_ADD_2 · Les cédules PS1 à PS4 n'ont été lues que partiellement (PS1). Les circuits de réserve ne sont pas comptés.

## Éclairage

- **R-012** · EL303/EL305 · Les profilés linéaires L1S, L2, L2S, L3, L3S, L4, L5 et L8 sont comptés **par segment dessiné** (≈ 1,2 m). La longueur totale est à métrer au 1:100.
- **R-013** · EL303/EL305 · Les luminaires grisés sont relevés sous « … urgence » (alimentés par PS1U/PS4U). La lecture du gris sur tuile est à confirmer, car `traits.py` n'a pas été utilisé.
- **R-014** · EL303_ADD · Une boîte carrée « PS1 » se trouve dans 162, le vestibule, 164 et ESC.01. Elle est hors légende et relevée sous « Boîte PS1 — à confirmer ». Il s'agit probablement d'un bloc d'alimentation nLight NPS-80.
- **R-015** · EL303_ADD · Un « M » carré se trouve près de la fosse d'ascenseur. Il est hors légende et relevé sous « Symbole M carré — à classer ».
- **R-016** · EL303_ADD · La scène de 171 comporte 2 rails R avec 4 projecteurs chacun (note 1). Chaque rail compte pour 1 : il faut ajouter 8 projecteurs.
- **R-017** · EL303_ADD · Les suspendus D12/D18/D24/D36 et les N du hall 156 ont été lus par zoom dans une zone dense. Il faut recompter.
- **R-018** · EL302 · Le réaménagement dans l'existant (E-105, E-110, E-114, E-118, E-124, E-103-1) est relevé comme neuf. Le reste de la feuille est existant et n'est pas relevé.
- **R-019** · EL301_ADD · L'issue temporaire (luminaires T, interrupteurs, phare, enseigne) est relevée. Elle est à retirer en fin de travaux (note 5).
- **R-020** · EL304 · Il y a 1 enseigne à enlever (démolition) et 1 nouvelle enseigne double face.

## Prises / mécanique

- **R-021** · EL403_ADD_3 · Il faut confirmer le nombre de raccordements directs de fontaines d'eau (détails 11/12). Nous en comptons 4 au RDC.
- **R-022** · EL404_ADD_2 · Le circuit de P-03 n'est pas indiqué en plan (le tableau EL408 le donne sur PS1). La pompe PGL-01 est branchée sur une prise PS1(9), qui est déjà comptée comme prise.
- **R-023** · EL404/EL406 · Les sectionneurs « SF » sont relevés sous « Sectionneur 30A ». Il n'a pas été vérifié s'ils sont fusibles ou non fusibles.
- **R-024** · EL406_ADD_2 · Les deux sectionneurs cadenassables 30A F:15 et F:20 du monte-personne (notes 1/2) sont relevés sous « Sectionneur 30A fusible ».
- **R-025** · EL406_ADD_2 · Un « détecteur thermique dans le puits » figure au détail 16. On ne sait pas s'il est fourni par l'alarme ou par l'ascensoriste : il est relevé « à confirmer ».
- **R-026** · EL408_ADD_2 · Recoupement du tableau avec les plans : les thermopompes TP-01 à TP-22 et TP-101/102, les SE-1-1 à 1-6 et SE-2-1 à 2-8, les ventilateurs VA-01/02, VH-01, H-01, UR-01, HU-01, CH-01, CE-01, les pompes P-01/02/03, PP-01/02, PER-01, PGL-01, EV-01/02, CD-01/02 et TR-01 se retrouvent en plan. Aucun raccordement n'est posé sur EL408. TP-22 (EL404) se trouve sur une ligne « RDC » : à confirmer.
- **R-027** · EL104 · Les bornes VE sont fournies par DR (note 1). Il y a 3 socles doubles, soit 6 bornes : la quantité par socle est à confirmer.

## Alarme incendie

- **R-028** · EL502/EL503 · Les klaxons (symbole F + triangle) et les klaxons-stroboscopes « 30cd » sont relevés séparément. On ne peut pas distinguer les klaxons simples des combinés sans lire la légende au zoom : à confirmer.
- **R-029** · EL504_ADD_2 · Seuls les 3 isolateurs de ligne neufs (trait plein) sont relevés. Les isolateurs en pointillé sont existants et ne sont pas relevés. Les résistances de fin de ligne et les modules MA/RA des schémas ne sont pas recomptés : ils sont déjà en plan.
- **R-030** · EL501_ADD · Le nouveau PAI Mircom FX-4003-12N et ses cartes (note 1) sont comptés comme 1 panneau. Le raccordement des circuits existants et l'inspection sont à chiffrer au forfait.
- **R-031** · EL501_ADD · Le communicateur GSM est **fourni par d'autres** (note 2). Seul le raccordement est à la charge de DR.

## Outils et méthode

- **R-032** · outils · Trois commandes ont été refusées par la politique d'outils : un script maison de carte des tracés noirs (`noir.py`, pour détecter le neuf et l'existant), une commande `sed` d'édition et un script Python en ligne. Elles ont été remplacées par des scripts Python autorisés et par la lecture de zooms. `zoom.py` et `extract_occurrences.py` ont fonctionné. `traits.py` n'a pas été utilisé.
- **R-033** · occurrences-texte · Les plans de Stantec n'ont pas d'étiquettes texte d'appareils : les symboles sont vectoriels et sans jeton. `extract_occurrences.py` renvoie donc 0 occurrence. Tout le relevé est visuel, avec une précision d'environ 5 pt, et doit être contrôlé par l'estimateur.
- **R-034** · estimateur · Aucun export de l'estimateur n'a été fourni (le dossier `estimateur/` est vide). Il n'y a donc pas de `comparaison-estimateur.md`.

