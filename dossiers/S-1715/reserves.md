# Réserves — S-1715 (Parc Lionel-Groulx, chalet, patinoire et stationnement)

Relevé du 2026-09-22. Chaque réserve donne la feuille, l'objet et la question ou la décision prise.

## Addendas et périmètre documentaire

- **R-001** · E-001/E-002/E-101/E-201/E-301 · Addendas. Deux addendas reçus : ELE-001 (2026-03-02, 4 feuilles) et ELE-002 (2026-03-12, 6 feuilles). ELE-002 réémet toutes les feuilles d'ELE-001 (cartouches rév. 1 + rév. 2), donc **seules les feuilles ELE-002 sont relevées**. Les versions de base (E001, E002, E101, E201, E301) et ELE-001 (E002_ADD_2, E101_ADD_2, E201_ADD_2, E301_ADD_2) sont classées `remplacee`. Aucune comparaison tuile par tuile entre versions n'a été faite : on a relevé directement la dernière version. Les nuages de révision visibles sur ELE-002 : E-201 (conciergerie 103 : détecteurs de conduit (note 2), RA ; bureau 101 : panneau P1 (note 1) ; W.C. 105), E-301 (bureau 101 SE-01/02/03 et prises ; salle mécanique SE-05/06, CE-01/02), E-101 (tableau des luminaires : lignes A1, L1, P1, R1, R3 ; détails G et H), E-002 (cédules des deux panneaux), E-001 (ajout de la feuille E-003).
- **R-002** · Addendas · Seuls les **plans** des addendas ont été reçus. Les textes d'addenda (devis, questions/réponses) ne font pas partie du dossier : tout changement qu'ils apportent hors des plans n'est pas reporté.
- **R-003** · E-102 · Le plan d'implantation n'a été réémis par aucun addenda : c'est la version de soumission (rév. 0) qui est relevée.
- **R-004** · E-003 · Feuille nouvelle (ELE-002, rév. 0) : le schéma WaveLinx CAT est relevé sur E-003. Les composantes sans symbole au plan (contrôleurs RSP, terminaisons, concentrateurs, commutateur PoE, WAC2) y sont comptées. Les postes muraux (WST) et les détecteurs (OSC) sont comptés **sur E-201**, pas sur le schéma, pour ne pas les compter deux fois.
- **R-005** · Général · Aucun export Plan Expert de l'estimateur n'a été fourni (dossier `estimateur/` vide) : aucun fichier `comparaison-estimateur.md` n'a été produit.

## Éclairage et secours (E-201)

- **R-006** · E-201 · Indicateurs d'issue **Z1 (4) et Z2 (1)** : les types Z1/Z2 n'apparaissent pas dans le tableau des luminaires d'E-101. Ils sont relevés sous « à confirmer ». Z1 = symbole mural, Z2 = symbole au plafond (légende E-002).
- **R-007** · E-201 · Un seul accumulateur **AUBX (72 W)** pour 7 têtes doubles et 3 têtes simples. À vérifier : autonomie et capacité (devis). Une prise rouge « hauteur spéciale » accolée à l'AUBX (circuit sécurité) est relevée sur E-201 ; elle n'est pas dessinée sur E-301.
- **R-008** · E-201 · Détecteurs de fumée **de conduit** (note 2, volets coupe-feu), 2 unités : la fourniture relève peut-être de la division mécanique. Le raccordement est compté ; la fourniture est à confirmer.
- **R-009** · E-201 · Projecteurs **P1 (8)** RGBW sur colonnes, contrôle DMX : le symbole désigné par la note 1 (bureau 101) est compté comme « Panneau de contrôle P1 ». Les composantes DMX (décodeurs, câblage) ne sont pas détaillées aux plans.
- **R-010** · E-201 / E-003 · Commandes basse tension. Au plan : 3 paires d'interrupteurs étiquetées 3a/3b (×2) et c/d, soit une marque par paire (= un WST-C-3), plus 7 interrupteurs BT simples, 4 gradateurs BT et 1 panneau P1. Au schéma E-003 : 13 postes WST (3× WST-C-3, 5× WST-C-3D, 4× WST-C-1, 1× WST-C-5D). Le dépôt 107 et la salle d'entrée d'eau 110 ont un interrupteur au plan mais aucun poste au schéma. Le WST-C-5D (éclairage patinoire) n'a pas de symbole distinct au plan. Le type (WaveLinx ou 120 V) est à confirmer pour ces trois emplacements.
- **R-011** · E-201 / E-003 · Détecteurs de présence : 11 au plan (étiquette D, avec la salle 110) contre 10 OSC au schéma. Le plan fait foi. L'écart porte sur la salle 110.
- **R-012** · E-201 · Un interrupteur unipolaire 120 V (symbole sans cercle) est dessiné à côté du poste manuel de la sortie sud du vestiaire (1823, 807). Il n'est pas expliqué par une note : sa fonction est à confirmer.
- **R-013** · E-201 · Bulles d'axes « D » et « F » (597, 1196 / 597, 1570) : faux positifs retirés. Les deux « F » accompagnés d'un triangle sont relabellisés « Klaxon alarme incendie ». Les 5 autres « F » sont des postes manuels.

## Services (E-301) et cédules (E-002)

- **R-014** · E-301 · Équipements mécaniques : le symbole (moteur, C/E, serpentin) et l'étiquette (VE, VA, VC, ECH, PECR, COND, DEV, CE, SE) désignent le même appareil. **Une seule marque par étiquette.** Les boîtes « C/E » (3) sont reliées aux étiquettes CE-01/02/03 (36 kW, 60A-3P) et ne sont pas comptées séparément. La désignation « chauffe-eau » est tirée de la légende C/E et reste à confirmer avec la division mécanique.
- **R-015** · E-301 · Aucun sectionneur local n'est dessiné aux moteurs et serpentins (sauf 400A SF réfrigération et interrupteur manuel DEV-01). Sectionneurs requis par le code et non montrés : à confirmer au devis.
- **R-016** · E-002 · **Système de réfrigération de la glace** (350A-3P, cct 12-14-16 RC-PDNO-600) : le raccordement est compté sur la cédule E-002. Le sectionneur **400A SF** est compté sur E-301 (salle mécanique 111). C'est un appariement, pas un double compte.
- **R-017** · E-002 · Circuits **RÉGULATION** (cct 54) et **RTÉGULATION** (cct 56, coquille) : 2 raccordements sans emplacement au plan. Ils sont comptés sur la cédule.
- **R-018** · E-002 · Circuit **RCFFM** (cct 59, 15 A) : équipement non identifié. Relevé « à confirmer ».
- **R-019** · E-301 · Les symboles « prise DDFT » dessinés avec un trait horizontal (1662,529 / 2013,639 / 2014,741 / 2211,638 / 2211,747) sont classés **Prise DDFT**. La variante « au-dessus du comptoir » n'existe pas en DDFT dans la légende : à confirmer. Les prises « comptoir » tournées (⊕ avec trait) sont classées « Prise au-dessus du comptoir ».
- **R-020** · E-301 · Deux interrupteurs de sûreté 600 A (600A F:600A à l'entrée, 600A SF entre le mesurage HQ et RC-PDNO-600) sont relevés sous le même libellé. La barre de MALT est relevée sur E-301. La prise de terre (électrode) est traitée en R-024.
- **R-021** · E-301 · Boîtier Camlock 200 A (note + cédule cct 53-55-57) : 1 unité comptée.

## Site (E-102) et linéaires

- **R-022** · E-102 · **Poteau client** (liaison aérosouterraine) : relevé « fourni par autres ». Son emplacement est à coordonner au chantier.
- **R-023** · E-102 · Boîtier Synertech pour **borne de recharge future** : seul le boîtier est compté. Aucune borne n'est prévue.
- **R-024** · E-101 · Détail G « prise de terre artificielle » et détail H « base de béton pour lampadaire » : le nombre de tiges et les quantités de béton ne sont pas relevés. Les 2 bases des lampadaires D1 sont incluses dans les 2 D1 : **à métrer / à chiffrer par détail**.
- **R-025** · E-102 / T-201 · **Éléments linéaires non métrés** : conduits souterrains (2#10+1#12C C.53 mm vers D1, conduit vide 53 mm avec corde, conduits 35 mm notes 1-2, 21 mm note 3, massif pour fibre), câble CAT5e WaveLinx, conduits de vidéosurveillance 21/27 mm, réseau de crochets en J. Échelles connues (E-102 1:200, T-201 1:100) : **à métrer**.

## Télécommunications (T-201 / T-101)

- **R-026** · T-201 · Selon la note générale D, les équipements d'appel général, de contrôle d'accès et d'intrusion sont **fournis et installés par le client**. Le relevé compte les points (boîtes et conduits). Le PCA est « fourni et installé par l'entrepreneur » (note 2) : lequel, à confirmer. Le PDI est à confirmer. Le cabinet mural et les haut-parleurs sont relevés « fourni par autres ».
- **R-027** · T-201 / T-101 · **Portes contrôlées (11)** : une marque par étiquette de porte. Les composantes par porte (lecteur, gâche, contact, BS, etc.) sont données par les élévations 1 à 5 et le tableau des portes de T-101. Elles **ne sont pas dénombrées une à une** : à compter par groupe de portes si DR fournit les boîtes et conduits.
- **R-028** · T-201 · Les sorties télécom sont comptées par affectation (VS, WF, CB, D, CA), sans distinguer murale, plafond ou hauteur spéciale. Les sorties VS et WF extérieures (colonnes de la patinoire, note 6) comprennent un percement par le client.
- **R-029** · T-201 · Les numéros de note (bulles 1 à 8) et les étiquettes de conduits ne sont pas comptés. La barre MALT télécom (note 7) est comptée, car l'entrepreneur électricien la fournit.
- **R-030** · T-201 · Les faux positifs retirés : bulles d'axes D/F, et PCA/PDI du texte des notes générales (2552, 119/142).
