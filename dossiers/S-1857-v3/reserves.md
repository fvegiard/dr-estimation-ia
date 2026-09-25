# Réserves — S-1857 Maison communautaire Saint-Michel (relevé à l'aveugle, v3, 2026-09-22)

Le relevé a été fait à l'aveugle. Aucun relevé humain ni export de l'estimateur n'était fourni (`estimateur/` vide), donc il n'y a pas de `comparaison-estimateur.md`.

## Classement et addenda
- **R-001 · E600 (fichier E000_Rev0) · classement** : `prepare.py` a nommé « E600 » la page titre (fichier `E000_Rev0.pdf`). Elle est classée `autre` avec cartouche=E000. La vraie feuille E600 PANNEAUX rév. 1 est `E600_2`.
- **R-002 · E600_2 → E600_ADD · addenda appliqué** : l'addenda 02 / ADME-01 (rév. 2 du 2026-09-11, scellée F. Ouerghemi, ing.) réémet E600 PANNEAUX. `E600_2` (rév. 1 SOUMISSION) est classée `remplacee` et n'est pas relevée. Seule la version d'addenda est relevée. J'ai comparé les deux versions cédule par cédule (textes d'E600_2 et zooms d'E600_ADD). Les écarts sont importants :
  - totaux : PS-1 104 051 → 171 408 W ; PS-2 46 887 → 59 875 W ; PS-3 27 867 → 61 260 W ; PS-4 20 430 → 33 796 W ; PS-5 32 880 → 168 600 W ;
  - ajout de la cédule **P-P1** 347/600V 600A (939 708 W) : THP-1 150A, CHE-1 et CHE-2 150A, CE-1 et CE-2 50A, VRT-1, SE-2, PC-1 à PC-6, PREF-1 à PREF-4, UAT-1, SPS-1, HC-1, SPP-1, chauffage ESC.A, S-07, ESC.B, S-03 et SAS00 ;
  - lave-vaisselle passés de 15A à 50A 2P (LV 100, 110, 122, 150, 232, 270, 273 et 140) ;
  - bornes BRVE-01 et BRVE-02 50A sur PS-5 ;
  - cuisine 140 : cuisinière 4 feux 50A, cuisinière 6 feux 70A et four combiné 250A (en rév. 1 : cuisinières « 4 ronds » et « 6 ronds » du local 150) ;
  - UAT-2 60A sur PS-4 ; PECD-1 sur PS-1.
  
  Les départs d'équipement sans symbole au plan sont relevés sur E600_ADD (famille `mecanique`).
- **R-003 · Addenda 02 · complétude** : je n'ai reçu qu'une seule page (E600, scan sans texte). Le document d'addenda lui-même (liste des modifications ADME-01) n'est pas fourni. Si ADME-01 modifie d'autres feuilles (plans E405 à E408, unifilaire E200), ces feuilles ne sont pas reçues et ne sont pas relevées. Les plans restent en rév. 1 SOUMISSION du 2026-08-17. À vérifier : il est possible qu'E200 (sans P-P1 à 939 kW) ne reflète plus la cédule d'addenda.
- **R-004 · E500 DÉTAILS COMMUNS** : la feuille est vide (cartouche seul). Aucun détail n'est émis et rien n'est relevé.
- **R-005 · E404 ACCÈS TOITURE - ÉCLAIRAGE** : la feuille ne porte aucun appareil électrique. Elle est classée `plan`, avec 0 occurrence (les étiquettes B, F, CE du texte sont des bulles d'axes grises, exclues).

## Doublons entre feuilles (comptés une fois)
- **R-006 · E150 IMPLANTATION** : les 5 DMW1 sont les appareils muraux extérieurs du RDC. Ils sont comptés sur E401 : 2 étiquettes DMW1, plus 3 muraux sans étiquette dont le type a été lu sur E150. Les lignes d'E150 sont exclues (`exclure=1`). E150 est donc écartée pour ces appareils.
- **R-007 · Raccord extérieur ▲CC (≈400,1494)** : il est dessiné à la fois sur E405 et sur E406. Il est compté une fois, sur E406 (niveau du sol extérieur). E405 est écartée.
- **R-008 · Équipements vus en plan et en cédule** : j'ai apparié ces équipements et ne les ai pas recomptés sur E600_ADD. Il s'agit de THP-1 et VRT-1 (E409), CHE-1, CHE-2, CE-1 et CE-2, SPP-1, SPP-ASC, EP-150, VE-MEC, VE-ELEC, UV-DCHT, VA-DCHT, REF-DCHT (E405 et E406), HC-1 et HC-2 (E406), SAS00 (aéroconvecteur E406), BRVE-01/02 (E406) et les 6 sèche-mains (SM E406, E407 et E408 = 6 départs sèche-main PS-2, PS-3 et PS-4). Les cuisinières 4 et 6 feux (140) sont appariées aux 2 prises « C » d'E406.

## Symboles hors légende ou type incertain (relevés sous « à classer » / « à confirmer »)
- **R-009 · E401 accueil 100** : 2 anneaux ovales orange (≈557,813 et 715,813) n'ont pas d'étiquette de type et ne figurent pas au tableau E102. Ils sont relevés en « Luminaire ovale suspendu — à classer ». Il faut confirmer le type, la longueur (profilé linéaire ? périmètre ≈ 32×15 pt de boîte, soit environ 3,2 m × 1,5 m à 1:100) et s'ils sont en service continu (couleur orange).
- **R-010 · E405 pompes** : 3 cercles violets avec un triangle plein pointe en bas (SPP-1 ×2, SPP-ASC) sont absents de la légende E103/E104. Ils sont relevés en « Raccord pompe (▼) — à classer ».
- **R-011 · E408 (648,995) et (745,822)** : 2 cercles rouges avec traits de fixation, sans marque interne (ni ∥, ni ⊣, ni capuchon). Ils sont relevés en « Prise — cercle vide à classer ». Il faut confirmer s'il s'agit de prises 15A ou 20A ou d'une autre sortie.
- **R-012 · E408 (393,1028)** : un carré rouge plein avec un octogone « C » est absent des légendes. Il est relevé en « Carré plein « C » — à classer » (commande de cuisinière ? prise cuisinière en mobilier ?).
- **R-013 · E405 (665,1051) et E406 (1260,1277)** : 2 raccords ▲CC sans étiquette d'équipement. Ils sont relevés en « Raccord direct équipement (▲CC) ». L'équipement est à identifier (celui d'E406 est voisin de la prise sécheuse, peut-être VE-SECH).
- **R-014 · PECD-1 et PREF-1 à PREF-4 (E600_ADD)** : ces équipements ne sont définis ni en légende ni sur les plans reçus (plans de mécanique non fournis). Ils sont relevés en « … — à confirmer ».
- **R-015 · CME-01 (E401 et E403)** : le contacteur d'éclairage CME-01 est seulement renvoyé (« VERS CME-01 »). Son emplacement n'est pas dessiné. Il est relevé une fois sur E401, au renvoi.

## Lecture des symboles (décisions prises sans personne pour répondre)
- **R-016 · Prises 15A / 20A** : selon la légende E103, la duplex 15A est un cercle avec 2 traits parallèles et la duplex 20A un cercle avec une marque en T (⊣). Le classement a été fait sur la géométrie vectorielle de chaque symbole et contrôlé sur des zooms d'E406 et d'E408. Les 26 prises 15A sont surtout des prises dédiées réfrigérateur/congélateur (REF. et CONG.). Leur cohérence avec les cédules (réfrigérateurs 15A) est bonne, mais l'écart de lecture reste possible sur quelques symboles.
- **R-017 · « à 1070mm »** : je les ai identifiées par la barre extérieure perpendiculaire. Les prises au comptoir (« 150mm du comptoir ») portent le même symbole et sont comptées dans les mêmes libellés.
- **R-018 · Qualificatifs MO, Ei, C, S, LV** : le qualificatif écrit à côté d'une prise la requalifie (une seule marque). Les mentions grises d'architecture (REF., CONG., LV, MO en gris) n'ont pas créé de marque. Les LV violets sont des raccords lave-vaisselle, distincts de la prise voisine.
- **R-019 · Détecteurs Do/Di plafond ou mur** : je les ai distingués par la présence des arcs latéraux (symbole plafond) autour de l'étiquette. 25 Do sont lus « mural » (forme en D). Aucun Di mural n'a été trouvé.
- **R-020 · Luminaires en service continu** : une étiquette dont le symbole le plus proche est orange (avec point) est relevée « … service continu ». 12 étiquettes sont dans ce cas (DR52, DS1, DW42). Les étiquettes « ? » près de l'éclairage d'urgence sont des numéros de circuit non encore attribués : aucun appareil n'est compté pour elles.
- **R-021 · Éclairage d'urgence** : les accumulateurs, phares et enseignes (sans étiquette sauf PH1 et X1) ont été classés un par un sur des planches de zooms. Les puissances d'accumulateur lues sont 18W et 36W (en note). La direction des enseignes (flèches) est une lecture visuelle, et la frontière entre montage mural et plafond (barre en T présente ou non) est à confirmer. Les étiquettes « X1 » sont notées, mais le type X1 n'est pas au tableau E102.
- **R-022 · Bulles d'axes et texte d'architecture** : j'ai exclu 81 mots par couleur (gris 153/170 = bulles d'axes A à F, texte d'architecture), par position (cartouche et notes, x > 2050) ou pour doublon (E150). Ils restent dans `occurrences-texte.csv` avec `exclure=1` et un motif.

## Non relevé / à métrer
- **R-023 · Conduits, câblage, chemins de câbles, mises à la terre** : rien n'est métré (la consigne porte sur les appareils). Les échelles sont connues (1:100 sur E150, E400 à E409).
- **R-024 · E201 unifilaire alarme incendie et E200 unifilaire distribution** : ils sont utilisés pour les appariements. Les dispositifs d'alarme sont comptés en plan, pas sur l'unifilaire. Sur E200, seuls les départs sans symbole en plan sont relevés (SPS-1 ×2, ASC, SE-1). SE-1 figure sur E200 mais pas dans la cédule P-P1 d'addenda (SE-2 seulement) : à confirmer.
- **R-025 · Éviers électriques** : PS-3 c2 (205, 227) et PS-4 c1 (302, 304) desservent 2 éviers par circuit. J'ai compté 2 raccordements par circuit, soit 7 en tout. À confirmer.
- **R-026 · Cuisinières** : la cédule PS-5 compte 3 cuisinières en prise (110, 150 ×2) plus 2 en raccord direct (140). Le plan E406 ne montre que 3 prises « C ». Il manque potentiellement 1 ou 2 prises cuisinière, ou des raccords directs. À vérifier.
- **R-027 · Lave-vaisselle** : la cédule donne 5 départs LV au RDC (100, 110, 122, 150, 140) pour 4 symboles LV sur E406, et 3 au niveau 1 (232, 270, 273) pour 2 symboles sur E407. J'ai ajouté 1 « Raccordement lave-vaisselle (cédule) » par niveau.

## Outils
- **R-028 · Politique d'outils** : aucun outil n'a été refusé. Les appels à `uv run releve/zoom.py` et `uv run releve/extract_occurrences.py` ont été lancés depuis la racine du dépôt, en chemin relatif, précédés d'un `cd` vers la racine : le shell de l'agent revient au dossier de travail à chaque appel, d'où cet enchaînement `cd … &&`. L'analyse vectorielle complémentaire (couleurs, formes) a été faite par des scripts de lecture seule, dans le dossier temporaire de session. Aucun fichier de `prepare.py` n'a été modifié. `build_qpl.py` et `render_pdf.py` n'ont pas été exécutés.
