# Réserves — S-1693 (École primaire 16 classes, Beloeil — CSSP 9382-109)

Décisions prises sans pouvoir poser de question (règle 5). Coordonnées en points PDF.

## Outils et conditions d'exécution
- **R-001 — Politique d'outils.** Trois commandes ont été refusées pendant le relevé : `ls` du dossier INBOX (hors répertoires autorisés), un `sed -i` sur un fichier de travail temporaire, et un filtre `awk`. Aucun des trois ne touchait `zoom.py`, `extract_occurrences.py` ni `traits.py` : ces trois outils ont fonctionné normalement. Le travail a été repris avec des scripts Python du dossier temporaire. Effet sur le relevé : aucun direct. La procédure demande quand même de marquer le résumé « À VÉRIFIER ».
- **R-002 — Aucun export estimateur.** Le dossier `estimateur/` est vide. La comparaison n'a pas été faite et `comparaison-estimateur.md` n'est pas produit.

## Classement et feuilles
- **R-003 — Noms de feuilles provisoires trompeurs.** Dans le PDF « 0ADD-5-E01 », `prepare.py` a nommé des pages de l'addenda E-01 « E401 », « E602 », « E701 », « UL924 » et « RS232 ». Ce sont des pages de texte d'addenda ou de devis. Le vrai E401 est `E401_2`, le vrai E602 est `E602_3` et le vrai E701 est `E701_2`. Les noms de feuilles sont conservés, mais chaque correspondance est indiquée dans `feuilles-classement.csv`. Les marques E401, E602 et E701 se trouvent sur `E401_2`, `E602_3` et `E701_2`.
- **R-004 — E602_2 (extrait d'addenda, détail 12 révisé).** Classé `detail`. Il n'a pas de quantité propre : il remplace un détail de montage et n'ajoute aucun appareil.
- **R-005 — E901 (classe typique 1:50) non comptée.** C'est un agrandissement des feuilles E201 et E301. La compter aurait fait un double compte.
- **R-006 — E303 et E304 (cheminement des artères).** Ces feuilles sont classées `plan`, mais seules les étiquettes de légende (bulles de repère, lettres de chauffage) en sont sorties, et elles ont toutes été écartées. **Les conduits d'artères ne sont pas métrés : à métrer (échelle 1:100).**
- **R-007 — E751 (élévations des caméras extérieures).** Les caméras sont comptées sur E701 (étiquettes C). E751 n'est pas recompté.
- **R-008 — E604 (détails de portes) et E271 (diagrammes de contrôle d'éclairage niveau 2, typiques).** Ils ne sont pas comptés séparément : les appareils de ces feuilles sont relevés sur les plans E701 et E202. Les composantes propres aux diagrammes E271 (modules nLight, relais, blocs d'alimentation) **ne sont pas comptées** : à confirmer avec la nouvelle section 26 09 24 de l'addenda E-01.

## Relevé : ce qui manque ou reste incertain
- **R-009 — Interrupteurs et gradateurs (E201 et E202) non relevés.** Ce sont des symboles vectoriels « $ » et « Ø » sans étiquette texte. Le temps n'a pas permis de les compter visuellement sur les deux feuilles. **Quantité à relever.** Seuls les détecteurs de mouvement (texte « D ») sont comptés : 62 + 27.
- **R-010 — Éclairage d'urgence non typé.** Les 89 appareils ont été repérés par leur étiquette d'accumulateur (''A''…''H'') : 63 sur E201 et 26 sur E202. Ils sont sous le libellé « Appareil d'urgence à typer », sans distinguer les phares simples ou doubles et les indicateurs de sortie simple ou double face. **Les accumulateurs eux-mêmes (A à H, selon la liste E201) ne sont pas localisés.** À typer en plan.
- **R-011 — Services auxiliaires E701 et E702 relevés seulement par étiquettes.** Sont comptés : CP, LC, G, OP, BA, CL, H, C, HOR, WF, PA, PMI, DM-Zxx et SBT-Zxx. **Ne sont pas relevés :** les postes d'intercommunication de classe, les haut-parleurs et trompettes de communication (sauf les 2 ajoutés par l'addenda E-02) et les sirènes intrusion. Ces symboles n'ont pas d'étiquette texte. À relever visuellement.
- **R-012 — Multiplicateurs « 3x », « 6x », « 1x » à l'entrée d'eau 122.2 (E401).** Seules les étiquettes ID (2) et MS (2) sont comptées. Les mentions 3x ID, 6x ID ou MS et 1x MS laissent croire à **3 + 6 + 6 + 1 modules**. À confirmer sur le diagramme E471 révisé.
- **R-013 — Prises E301/E302 relevées visuellement (précision d'environ 5 pt).** Le relevé a été fait par zooms successifs. Quelques zones peu denses n'ont pas été revues à fort zoom : E301 autour de x 980–1200, y 590–700 (vestibule et direction), et E302 à l'ouest de x 400 sous y 1000. Une sortie informatique marquée « 2 » compte pour **une marque**, avec la mention « « 2 » inscrit » en note : il faut prévoir 2 prises de données à ces endroits. Les prises de la feuille E901 ne sont pas recomptées.
- **R-014 — Doublons possibles entre deux passes de zoom sur E301.** Les points à moins de 4 pt d'écart ont été fusionnés. Un contrôle visuel sur le PDF annoté est recommandé autour de x 1540–1990, y 600–900.
- **R-015 — Stèle, poteau client aéro-souterrain, massif de conduits et M.A.L.T. (E002).** Seul le raccordement de la stèle est compté. Le massif de conduits, le poteau client, les conduits de la borne de recharge **future** (conduit 53 mm seulement) et les 3 tiges de M.A.L.T. ne sont pas des appareils : **à métrer ou à chiffrer en forfait.**
- **R-016 — « C » sur E701 = caméras.** Les 16 marques « Caméra » viennent du texte « C » dans le symbole de caméra. Le compte n'a pas été recoupé avec les identifiants CAM-01-xx de E751.
- **R-017 — Lettres de légende relevées par erreur puis écartées.** Retirés : les lettres A, B, C, D, E, G, H et T des bulles d'axes, du cartouche et des tableaux T-01, T-03 et T-05 ; les « G » (gâche) dans E201 et E401, qui étaient la bulle d'axe G ou la mention « G » des trompettes ; les « MD » de E201, qui étaient du texte du tableau T-01 (D1 et MD). Le « D » de E301/E302 a été relu comme **plinthe D**, et non comme détecteur de mouvement : il est suivi d'une puissance en W et d'un circuit PA ou PB.

## Addendas appliqués (E-01 du 10 mars 2026, E-02 du 20 mars 2026)
- **R-018 — Addendas en texte seulement.** Aucune feuille de plan de base n'est remplacée. Les deux addendas n'ont que du texte et des extraits de détails. Les ajouts et retraits ont été appliqués en marques « position approx. » à partir de la description (axes, locaux). **La position de chacune est à valider.**
- **R-019 — E401 (E-01 .5).**
  - Retirés : klaxons aux axes J9 et G10.
  - Strobes annulés dans 135.1, 137.1, 138.1 et 139.1.
  - Ajoutés : 1 klaxon dans le corridor 100.9 près de la classe 137, 1 klaxon à K5, 1 KS à l'axe 10 entre G et H, et 1 KS en F10.
  - Axe 1 entre A et B : le KS et le strobe sont remplacés par un seul KS en B1.
  - Axe 9 entre A et B : le strobe devient un KS en B9.
  - Gymnase, axe G : les 2 strobes deviennent 2 KS.
  - Le klaxon J4 est déplacé à l'axe 6.
  - E-02 .3.1 : dans les locaux 113 et 115, le mini-klaxon et le strobe sont remplacés par un KS. Les 2 M/K ont été retirés.
- **R-020 — E402 (E-01 .6).**
  - Locaux 209 et 211 : le mini-klaxon et le strobe deviennent un KS dans chaque local. Seuls les strobes étaient visibles ; aucun M/K n'a été trouvé dans ces locaux.
  - Ajoutés pour REC-001 : 2 modules doubles, 1 relais (**quantité 1 ou 2 à confirmer**) et 2 détecteurs de conduit.
  - Ajouté dans le local 202 : le relais adressable (E-01 .5.15).
- **R-021 — Monte-personne (E-01 .3.1 et .4).** Ajoutés dans le puits : 1 sectionneur 30A/F15A sur E201 ; sur E301, 2 sectionneurs, le raccord du chargeur, le raccord du panneau PC, 1 prise double et 1 sortie téléphonique. **La position du puits a été déduite de la mention « rappel d'ascenseur » (axe 16, vers x 2665 et y 975) : à valider.**
- **R-022 — Camlock 400A (E-02 .1.4 et .4.1–.4.2).** Une marque sur E301 (salle électrique 136.1, axe 8). La marque couvre aussi le disjoncteur 400A du PP1(DIST), l'artère 2x(4#250AL+1#2V-C78) et la clé captive Kirk Key : **l'artère est à métrer.**
- **R-023 — Disjoncteurs ajoutés, pas de marque en plan.** Ils se chiffrent directement dans les cédules :
  - E-01 .9 : 4 × 15A-1P dans P2 ;
  - E-02 .5.1 : 5 × 15A-1P libres dans chacun des panneaux P1 à P6, soit 30 ;
  - E-02 .5.2 : 3 × 20A-1P dans P2 (circuits 67, 69 et 71) ;
  - E-01 .8 : disjoncteur principal du PP1 porté de 400A à 500A, PP2 porté à 600A, et nouvelle artère PP1–PP2 2X(4#350AL+1#1V-C91).
- **R-024 — Sectionneur par thermopompe (E-02 .6.1).** Une marque par thermopompe relevée : 18 sur E301 et 15 sur E302. Chacune est placée à 20 pt de l'étiquette TP-xxx. Les serpentins ont un sectionneur intégré fourni par la mécanique (E-02 .6.2) : rien n'est ajouté pour eux.
- **R-025 — Sondes basse température.** L'addenda E-02 fait passer le nombre de sondes de 2 à 3. On trouve 3 étiquettes SBT : 2 sur E701 et 1 sur E702. C'est cohérent.
- **R-026 — Haut-parleurs de communication (E-02 .8.1).** 2 ajoutés en position approximative dans les locaux 111.1 et 117.
- **R-027 — Carte de communication IP (E-01 .11.8).** Une marque au panneau d'intrusion du télécom 110. Contacts anti-sabotage retirés (E-01 .11.1 et .12.3) : ce retrait ne change aucune quantité relevée.
- **R-028 — Devis 26 09 24 (commandes d'éclairage basse tension, section ajoutée par E-01).** La section décrit un système de contrôle (écrans tactiles, gradateurs, blocs d'alimentation, capteurs) qui n'est pas entièrement représenté en plan. **À chiffrer à partir des diagrammes E271 et du devis.**

## Cédules et unifilaire (étape 5b) : ce qui n'a pas été fait
- **R-029 — Appariement cédules ↔ plan à faire.** Les raccordements mécaniques ont été comptés à partir des étiquettes du plan (TP, SE, PMP, VE, REC, CH, HU, CE, CON, EV), et non ligne par ligne dans les tableaux E581 (T-06 à T-15). Les départs de E502 (cédules P1 à P6, PA, PB) et de E501 (unifilaire) n'ont pas été recoupés un à un avec le plan : un équipement présent seulement en cédule a pu être oublié.
