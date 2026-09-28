# Réserves — S-1714 (Le Vallem – Riviera, Carignan · plans ÉQUIPE SP 2025-46, rév. 3 « émis pour construction 90 % » du 18.02.2026)

Outils : `extract_occurrences.py` et `zoom.py` ont fonctionné. **Refusés par la politique d'outils :** `sed` (lecture) et un script
pymupdf lancé par `uv run` en chemin absolu (classement vectoriel des symboles d'éclairage). Conséquence : le type des luminaires
de E300/E301/E308 n'a pas pu être lu automatiquement (voir R-010). Les filtrages ont été faits par petits scripts Python sans pymupdf.

| # | Feuille | Objet | Question / décision prise |
|---|---|---|---|
| R-001 | toutes | Addenda / export estimateur | Aucun addenda ni export Plan Expert de M. Dupuis dans le dossier : pas de `comparaison-estimateur.md`. |
| R-002 | E101 | Tableau des luminaires « À VENIR » | Aucun type de luminaire (A, B…) défini. Les luminaires sont relevés par forme de symbole ou « Luminaire — à classer ». |
| R-003 | E201–E208 | Prises du circuit 23 | L'étiquette « 23 » sert à la fois aux prises intérieures et aux prises extérieures de balcon/façade. Classement fait à l'œil : symbole encadré sur mur extérieur ou balcon = « Prise étanche », le reste = « Prise double ». À confirmer : DDFT ou non. |
| R-004 | E201–E208 | Prise salle de bain (circuit 15) | La légende ne dit pas si elle est DDFT intégrée ou protégée au panneau (devis 4.4/4.8 : pas de double protection). Relevée sous un label unique. |
| R-005 | E201–E208 | Chauffage : plinthe ou aéroconvecteur | Classement fait sur la forme du symbole (rectangle long = plinthe ; boîtier et flèche en zigzag = aéroconvecteur). Les puissances viennent de l'étiquette voisine. Les étiquettes « 1500W/2000W » seules ont été relevées en visuel, pas par le texte. |
| R-006 | E204 | Étiquettes « UNITÉ » absentes | Les panneaux de logement de E204 ont été placés aux positions de E203, qui est le même plan type. |
| R-007 | E201 | « 4000kW » aux vestibules (S-10, S-12) | Probablement 4000 W. Relevé sous « Aéroconvecteur commun » ; le type exact reste à confirmer. |
| R-008 | E201 | Serpentins de conduit « SERPENTIN X KW » et « SERPENTIN 6.25 » | Puissance du premier non donnée ; son circuit n'a pas été trouvé dans les cédules. |
| R-009 | E200 | CA-1/BC-1/AB-1, CA-2/BC-2/AB-2 | Lus comme des bancs de compteurs (rangées de boîtiers). Relevés sous « Équipement salle électrique — à classer ». À recouper avec E102. |
| R-010 | E300, E301, E308 (+ salle de toit de E307) | Luminaires | 325 luminaires relevés à raison d'une marque par étiquette de circuit (UE/S x.y-n), sous « Luminaire — à classer ». Types non lus (outil refusé, tableau des luminaires à venir). À classer par l'estimateur. Sur E300, des étiquettes à x < 1000 pt sont incluses : vérifier qu'aucune n'est dans la marge. |
| R-011 | E302–E307 | Enseignes de sortie | Le symbole cercle-X, avec tige ou flèches, est lu comme une enseigne « running man » (en applique ou directionnelle). La variante exacte (1 ou 2 faces, avec phare ou non) n'est pas déterminée. Les unités à batterie et les projecteurs ne sont pas visibles sur les zooms des étages types. |
| R-012 | E302–E308 | Interrupteurs et détecteurs de mouvement | Aucun vu sur les zooms des corridors et escaliers. Non relevés : à vérifier tuile par tuile. |
| R-013 | E400–E408 | Klaxons « K » | Retenus seulement quand une adresse d'appareil est voisine (x.y, 3.9K, WW…) : 52 retenus. Les « K » isolés présents à l'identique sur tous les étages (mobilier) sont écartés. |
| R-014 | E400–E408 | Alarme non relevée | Les symboles PAI, ANN, GSM, TÉLÉPHONE POMPIER, DG, DA, CO (détecteur CO), DN, NPE, S (gicleur), piézo-strobes et haut-parleurs ne sont pas relevés par le texte : ils sont absents de la nomenclature, faute d'avoir été repérés. À vérifier tuile par tuile. Les étiquettes AF/AF1/KS/DF sont relevées automatiquement et leurs faux positifs n'ont été contrôlés que par échantillon. |
| R-015 | E207, E209 | AF-1 / AF-2 | Ce sont des unités d'air frais (circuits UNE-7,9,11 et UNE-13,15,17), pas des avertisseurs de fumée. Mots exclus, et chaque unité relevée une fois sous « Raccordement équipement mécanique ». |
| R-016 | E200 | Ventilateurs | Les lettres « V » des symboles sont écartées. Un ventilateur est compté par bulle V-x (22 bulles), pour ne pas compter deux fois. |
| R-017 | E200 | Condenseurs CO-0.75 (S1.1-30,32 / 34,36 / S2.1-39,41) | Relevés par le mot CO-0.75. Les étiquettes de circuit voisines ne sont pas comptées une deuxième fois. |
| R-018 | E101 | Raccordements pris dans les cédules | Ascenseurs #1 et #2, consoles et cabines d'ascenseur, porte de garage, aérotherme AE-X 50 A (panneau S, introuvable en plan), génératrice, intercom, téléphonie, câblodistribution et transfos CO/TI sont posés sur E101. Le panneau piscine PC est « À CONFIRMER ». |
| R-019 | E102 | Unifilaire | Entrée 1200 A 347/600 V, disjoncteur principal, ATS et génératrice (« À VENIR ») : ces équipements ne sont pas comptés article par article. À chiffrer d'après E102/E104. |
| R-020 | toutes | Sectionneurs de condenseurs | Selon la note condenseur de E100, chaque condenseur a un sectionneur fourni et raccordé par l'électricien. 145 sectionneurs ont été ajoutés, un par condenseur. |
| R-021 | E500 | Plan d'implantation (branchement HQ, massif, transformateur sur socle) | Non compté : conduits et massif à métrer (1:200). Tous les mots-étiquettes de E500 ont été exclus : ce sont des numéros du plan de site. |
| R-022 | E309, E409 | Plans de toit vides | Rien à relever. Les mots « H », « I » et « R » sont des bulles d'axes et ont été exclus. |
| R-023 | E208 | Prise UE2.2-14 dans la cage grise | Probablement une prise de puits d'ascenseur. Relevée sous « Prise double ». |
| R-024 | E103 | Tableaux d'équipements mécaniques | Pompes, aérothermes, évaporateurs, condenseurs et bouilloire. Non recoupés ligne par ligne avec les relevés en plan : les puissances sont à reprendre de E103. |
| R-025 | E201 | Évaporateurs EVG (gym, lounge, résidentiel commun, hall 2) | Relevés en visuel. Ils sont alimentés par CD-1/CD-2 (S2.1-31/33 et 35/37), eux-mêmes relevés sur E202 (toit du RDC). |
