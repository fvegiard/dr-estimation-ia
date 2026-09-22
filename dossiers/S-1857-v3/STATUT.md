# STATUT — relevé automatique « S-1857-v3 »

Date : 2026-09-22 13:16 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| Addenda02-ADME-01-plans-electrique-E600.pdf | 1208763 | c5076cb555858c9eb4882a06b6ab653115700f555af013b353a0dc913d40f1c6 |
| plans-electriques/E000_Rev0.pdf | 369102 | d0f3f414999c47434a17e56a7a14122ce4a67a330d39760fa9739157f6e7597c |
| plans-electriques/E100_Rev0.pdf | 1794636 | 93b3e225fbfde0d9f94f9fb9f63184c52e1090eb4f58c80306172239077fb361 |
| plans-electriques/E101_Rev0.pdf | 1555199 | 8a490459526a44109b479a24fa0515522cdb9968f4d385d7a8a2ab73f6ecbf6a |
| plans-electriques/E102_Rev0.pdf | 321490 | 1265774c70a5ba64eeae08e010c2b6358582adf6b0d3dac2a35cf90e5b7ec3d5 |
| plans-electriques/E103_Rev0.pdf | 373306 | 21dc791866215b9ecc2bfa1bf5fadb352efe4c858f84bcd89e17662efbfe0d2e |
| plans-electriques/E104_Rev0.pdf | 347932 | e5318ce6ed1d38292ae02cf8a70b08a3f4e7e029534af2a4636ff33346499cc7 |
| plans-electriques/E150_Rev0.pdf | 661011 | c328c77d4067beb33081bcfd1ba9b296a36d166f57a6e77d26aef135decdfe4f |
| plans-electriques/E200_Rev0.pdf | 315646 | 5834a9d1544fcf191963d65b464fbb66c08d51899ff74919ee2e869598a5c1e2 |
| plans-electriques/E201_Rev0.pdf | 502855 | e9717efe9effa1d68dff17d2e23656f9c2d48bf8e096c3c3fc71a8493728eb9e |
| plans-electriques/E400_Rev0.pdf | 432678 | 3206a6650ce3664679451c9d751def9d64d336f67e86aa4a5eb3fe77bff79a9a |
| plans-electriques/E401_Rev0.pdf | 853974 | c3d6ee467463dbb706d83214064acc67bbcb0362fd3a7f8adba2ddc92f093e5b |
| plans-electriques/E402_Rev0.pdf | 678123 | bf7807eb7e15a80d5eb6ad58ba361c1800f2f6e53bbc8f3505932416f81a390e |
| plans-electriques/E403_Rev0.pdf | 766823 | 20120659537cf04e23cdc86c89015f6463666e09919917feae88c7c55ba2db50 |
| plans-electriques/E404_Rev0.pdf | 346749 | 5577c85f5233553eb72b1ce0669e55fa908263a91ce7f85890f905c9b3f3d41c |
| plans-electriques/E405_Rev0.pdf | 498070 | 2b4445455e11af25e64395d760642ced2adc737832578df1864372ca5b99416d |
| plans-electriques/E406_Rev0.pdf | 820017 | a95b7b77b44d0f2b35b5a659fdf38fb378dba6da2a6051191085af67294ab191 |
| plans-electriques/E407_Rev0.pdf | 632240 | 84a93d28628fdf2f0c47ab6488bc882fc5338603d3bc17a8c142bf6c4e41c6bf |
| plans-electriques/E408_Rev0.pdf | 740552 | c6e997b45036bef95b77c537a1f4a67a1f4eeca8ada563b7e53baba9f3e6a789 |
| plans-electriques/E409_Rev0.pdf | 371422 | f26ba98f07436995dc143bafab4dbd8216ccc1282026fb2302c7af79ad122626 |
| plans-electriques/E500_Rev0.pdf | 269322 | e7b02b7fcbcede394fe94e94d8425f05700412b9b1238e5828c4d11591b67707 |
| plans-electriques/E600_Rev0.pdf | 333881 | 450fcc5688ef97924799391fd450005d6f36f5ca29367109393af771cf51c891 |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1857-v3-Dossier-complet.pdf | 8060771 | 4949a45b587492963f29d05dce54092c573e23d148b89fab73c7abf6d3ebbb06 |
| S-1857-v3-Plans-annotes.pdf | 7357388 | 239c5c68924836f2ff78c97762605212f1798a352da142cbd0a26917c06d5dad |
| S-1857-v3-Rapport-de-metre.md | 44242 | cb11a02e07a3901b5b8e2a82bb5ca7871ef166ad7460bfe1dd4bb82d26c31098 |
| S-1857-v3-Rapport-de-metre.pdf | 703651 | 686c879df7df9666aea61bacc5538eb9d2b0ec42c28b4915186ac626740e74b2 |
| journal-etapes.log | 1758 | a3f1162e9cad227be6bb90b04b88994e21708b3cceede2c80beacecfd5d0ecdd |
| S-1857-v3-planexpert/S-1857-v3.qpl | 155421 | 52bf7909d1709b1678e718a242de09015109029d779b242bdd58c319c920ffb6 |

Le projet Plan Expert `S-1857-v3.qpl` est dans `S-1857-v3-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| build_qpl | 0.1 min | ok |
| render_pdf | 0.2 min | ok |
| total | 0.3 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : None · sous-type : None
- coût estimé (client, `total_cost_usd`) : None $ US
- jetons : entrée None, cache créé None, cache lu None, sortie None
- session : `None` · dossier de travail : `/home/claude/releve-auto/runs/S-1857-v3/OUTBOX/S-1857-v3/travail`

## reserves.md

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

