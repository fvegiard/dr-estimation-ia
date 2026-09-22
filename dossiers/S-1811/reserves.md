# Réserves — S-1811 (STJ-Construire 6 nouveaux bâtiments d'hébergement, Garnison Saint-Jean)

Relevé du 2026-09-22. Chaque réserve donne la feuille, l'objet, la question ou la décision prise.

## Périmètre et documents

- **R-001 · 502B (S267_ADD_3), note A · multiplicateur de bâtiments.** Les plans électriques (505B à 508B, 502B, 511B) ne dessinent que le bâtiment #1 (type A). La note A du 502B dit : « for tender, include the distribution for the six buildings ». Les bâtiments de type B sont en miroir du type A. **Le relevé compte UN bâtiment.** Il faut multiplier par 6 les feuilles 505B, 506B, 507B, 508B, 502B et 511B. Le plan de site 503B couvre déjà tout le site et ne se multiplie pas. Cette décision revient à l'estimateur.
- **R-002 · Addendas · pas de texte d'addenda.** On a reçu les plans des addendas MEP-01 (20 p.) et MEP-02 (5 p.), mais aucun document texte qui décrit les changements. Rien ne permet donc de vérifier que MEP-02 est complet. Versions retenues, d'après le bloc de révision du cartouche : 501B, 502B, 503B et 510B en MEP-02 (rév. 2) ; 505B, 506B, 507B, 508B et 511B en MEP-01 (rév. 1) ; 504B et 509B dans la version de soumission (non réémises). Les feuilles de base et les versions MEP-01 remplacées sont classées `remplacee`.
- **R-003 · Addendas · comparaison base / addenda non faite tuile par tuile.** Le relevé porte seulement sur la version en vigueur. On n'affirme pas qu'aucun appareil n'a été ajouté ou retiré. Zones ennuagées (changements) vues dans les versions retenues :
  - 505B : bloc des douches (C2) ;
  - 506B : plinthes des sas, C3.2, C6.1 de l'entreposage, EV1/CS1-007, C5.1, détail 2 de la salle des gicleurs, EHC1-006, HU1-003/EV1-006, classe entière, CS extérieurs ;
  - 507B : modules ARM des UTA ;
  - 508B : détecteurs et ARM des modules dortoirs ;
  - 503B : ligne aérienne et poteaux, conduits de 103 mm ;
  - 502B : interrupteur principal, mesurage HQ et client ;
  - 501B : liste C2/C3/D1 et liste de chauffage ;
  - 511B : tableau P1-2PDPN4N-1.

  Pour garantir le différentiel, il faut comparer 505B à 508B avec les feuilles S267_5 à S267_8.
- **R-004 · 402B–416B (feuilles mécaniques reçues dans les addendas) · hors électricité.** Classées `autre`, non relevées. Les équipements mécaniques à raccorder sont pris sur 506B, 507B, 502B et 511B. Les capteurs et thermostats de régulation (plan 415B, Div. 25) ne sont pas comptés.
- **R-005 · Outils non exécutés.** Les commandes `uv run releve/extract_occurrences.py`, `zoom.py` et `traits.py` ont été refusées (permission indisponible dans la session). Conséquences :
  - `occurrences-texte.csv` a été construit à la main à partir de `texte/<F>-mots.csv`, avec les colonnes du script et une colonne `exclure` ;
  - **il ne faut pas le régénérer** par `extract_occurrences.py`, sinon les libellés « urgence » et les exclusions seraient perdus ;
  - la lecture visuelle s'est faite sur les tuiles 3×4 seulement, sans zoom.
- **R-006 · Neuf / existant.** Aucune mention « EX. », « existant » ou « à démolir » sur les feuilles électriques. Tout est relevé comme neuf.
- **R-007 · Estimateur.** Aucun dossier `estimateur/` (export Plan Expert de M. Dupuis) n'a été fourni. `comparaison-estimateur.md` n'est donc pas produit.

## Éclairage (505B, S267_ADD_21)

- **R-008 · A1 à (123,1908), sas B1-01.** Le mot « A1 » est isolé près d'une enseigne X1, sans appareil dessiné. Exclu (`exclure=1`). À confirmer s'il manque un appareil.
- **R-009 · E1 sans étiquette à (149,2019), entreposage B1-02.** 6 réglettes sont dessinées pour 5 étiquettes. La 6e est ajoutée visuellement.
- **R-010 · D1 à (2546,1911), corridor B1-52.** Le symbole est coupé par la limite de tuile ; il a été lu plein gris et classé urgence. À confirmer.
- **R-011 · C3 à (2535,2159), sas B1-51.** Le remplissage n'est pas visible (bord de tuile). Classé urgence par symétrie avec le sas B1-50.
- **R-012 · Luminaires d'urgence.** Distingués par le remplissage gris (légende « linéaire / ponctuel sur l'urgence »), alimentés par les mini-onduleurs M1/M2 (note générale 3). Résultat : 6 A1, 4 C1, 7 C3, 14 D1 et 4 E1 en urgence. Le plan montre un boîtier de mini-onduleur en salle électrique, et le détail 2 en montre deux (M1, M2). **On compte 2, sur le détail seulement.**
- **R-013 · X1.** Les variantes de légende (plafond, mural, une face ou deux faces, avec flèche) ne sont pas lisibles de façon fiable sur les tuiles. Les 18 enseignes sont sous un seul libellé et restent à ventiler par variante.
- **R-014 · Gradateurs.** Le symbole « Ø + flèche » a été relevé comme gradateur (6). On ne peut pas le distinguer du « gradateur avec détecteur de présence ». Les deux symboles « Ø a / Ø b » de la classe pourraient être des postes de contrôle de zone. À confirmer.
- **R-015 · Commandes.** Les 32 cabines douche/WC ont chacune un interrupteur avec détecteur (symbole tourné). Aucun panneau de commande d'éclairage n'est dessiné (note 2 : système de contrôle selon le devis).

## Services (506B, S267_ADD_22)

- **R-016 · Prises des modules dortoirs.** 62 relevées au plan. Les tableaux indiquent environ 64 (circuits 1 à 9 « OUTLETS (6) », circuit 11 « (6) » à 200 VA, sur deux panneaux). Écart de 2 à vérifier.
- **R-017 · Circuit 16, P1-2PDPN4N-1 « OUTLETS (3) CIRCULATION ».** Seulement 2 prises trouvées.
- **R-018 · Classe.** Le tableau indique « OUTLETS (4) CLASSROOM » sur 3 circuits (61, 63, 65), soit 12. Le plan en montre 10 (4 + 4 + 2).
- **R-019 · Boîte au plafond du projecteur, classe (2706–2717,2152).** On y voit Φ + ▽. Le Φ est compté en prise 5-15R, le ▽ en « prise double 5-15R (triangle) ». Le ▽ pourrait être une sortie A/V ou data.
- **R-020 · Symbole ▽ à tiges.** C'est une ligne distincte de la légende (« DOUBLE 15A 5-15R » sans qualificatif), avec son propre compteur (micro-ondes circuit 38 et boîte du projecteur). La nature exacte est à confirmer.
- **R-021 · Salle des gicleurs B1-45.** Les appareils sont relevés sur le détail 2 (1:50) : WH×3, TF1, TF2, PU1, HU1-002, 6 sectionneurs et le panneau de contrôle. Au plan 1, les équipements en gris sont du fond mécanique. Seule la prise circuit 22, dessinée au plan 1 et absente du détail, y est comptée. Pas de double compte.
- **R-022 · Serpentins EHC1-006-101.** 506B indique 3 × 500 W ; 502B indique « ECH1-006-101 (3X) 1.5kW ». Le total est cohérent ; l'orthographe ECH/EHC diffère. Les trois mots « 500W » de ces serpentins sont exclus des plinthes C1.1 et relevés visuellement.
- **R-023 · Interrupteur principal.** 506B indique « 400A / F.400A » ; 502B indique « 400A-3P F.350A ». Calibre des fusibles à confirmer.
- **R-024 · Plinthes.** Une plinthe = un mot de puissance (500W, 1000W…). L'étiquette C1.1 regroupe 2 plinthes. Les suffixes .1 et .2 correspondent aux accessoires X.1 (relais triac Div. 25) et X.2 (thermostat intégré) et sont comptés comme libellés distincts. Aucun thermostat n'est dessiné, aucun n'est compté.
- **R-025 · C5.2 à (1698,2175).** Convecteur 2000 W lu par son mot de puissance près de l'étiquette C5.2 (zone ennuagée). Local exact à confirmer.

## Toit (507B, S267_ADD_23)

- **R-026 · UTA RT1 et unités HE1.** Aucun sectionneur n'est dessiné près des unités. Fourni avec l'unité ? Non compté.
- **R-027 · Prises des UTA.** Elles sont fournies par le fabricant et alimentées par l'électricité. Relevées sous « Raccordement prise UTA toit (fournie par fabricant) » : seule l'alimentation est au prix de DR.

## Alarme incendie (508B, S267_ADD_24 ; 509B, S267_9)

- **R-028 · 509B.** Le schéma est indicatif (note 1) et n'est pas compté ; tous les comptes viennent de 508B. Les étiquettes « D1-x » sont des numéros de dispositifs, pas des appareils. Le « S » sous certains « 115cd » n'est pas expliqué dans la légende ; ces appareils sont comptés comme klaxons/stroboscopes.
- **R-029 · Stroboscopes seuls.** Distingués des klaxons/stroboscopes par l'absence du boîtier « F » ou par la potence murale : 4 × 115 cd en circulation et 2 × 30 cd.
- **R-030 · Détecteurs dessinés avec potence près des volets coupe-feu et de la salle calme.** Comptés comme détecteurs de fumée photoélectriques (6), accompagnés de modules ARM. Il pourrait s'agir de détecteurs dédiés à la retenue des volets. À confirmer.
- **R-031 · PS1.** Le plan 508B indique 32(P1-2PDPN4F-1) ; le tableau 511B met « POWER SUPPLY PS1 » au circuit 34.

## Distribution (502B, S267_ADD_3 ; 511B, S267_ADD_25)

- **R-032 · Appariement schéma / plan.**
  - Comptés au plan 506B seulement : panneaux, transformateur, interrupteur principal et armoire HQ.
  - Comptés sur le 502B, faute de symbole au plan : le dispositif de mesurage client pour la GTB (note B) et les 3 barres de mise à la terre.
  - Tous les départs de P1-3PPN4N-1 (RT1, HE1, EHC1, EHC2, HU1, groupes de chauffage) et des tableaux 120/208 V sont appariés à des symboles des plans 506B et 507B.
- **R-033 · Départs EF1, EF2 et EF3-007-101 (FUTUR) au tableau P1-2PDPN4F-1.** Aucun équipement au plan. Comptés comme « Départ futur ventilateur EF » sur 511B (disjoncteur et réserve seulement).
- **R-034 · Câblage et canalisations.** Artères (2X(4#4/0…), 4#500-103, etc.), conduits et chemins de câbles : **à métrer**. Non relevés.

## Site (503B, S267_ADD_4 ; 504B ; 510B)

- **R-035 · Poteaux de bois.** 8 poteaux sont dessinés, dont 1 dans l'encadré 7/510B et 2 dans l'encadré 6/510B. S'y ajoutent **5 poteaux additionnels (note D)**, marqués près de la flèche « vers autre poteau ». Le statut des 8 poteaux dessinés (neufs, existants, poteau client HQ) n'est pas précisé. La longueur de la ligne aérienne est **à métrer** (détail 8/510B, environ 30 m entre poteaux).
- **R-036 · Puits d'accès.** 5 relevés (identification 1). La note A parle de « futur puits » (voir plans civils) : à vérifier. Massifs et conduits souterrains (2 × 103 mm, 4 × 78 mm, 1 × 78 mm…) : **à métrer** à l'échelle 1:250. La note C (descente aérosouterraine) et la note B (5 m de câble additionnel par bâtiment) ne sont pas comptées comme articles.
- **R-037 · Appliques G2/G3 et lampadaires L2/L3/L5.** Comptés une seule fois pour le site entier, 6 bâtiments inclus (voir R-001).
- **R-038 · Détails 504B (Hydro-Québec) et 510B.** Détails typiques, non comptés.
