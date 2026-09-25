# HR26-14 — Analyse d'appel d'offres pour l'entrepreneur électricien

**Projet** : Réfection majeure de 4 bâtiments — 290 Montcalm, 291 Chaussé, 145 St-Georges,
155 Mercier, Saint-Jean-sur-Richelieu
**Donneur d'ouvrage** : Office municipal d'habitation Haut-Richelieu (OMHHR),
145 rue Latour bureau 100, Saint-Jean-sur-Richelieu, J3B 7T8
**Destinataire de l'analyse** : DR Électrique
**Analyse produite le** : 2026-09-15
**Source** : `C:\Users\fvegi\Downloads\Plans & Devis & Addendas` (lue en lecture seule, non modifiée)

> **Convention de citation.** Chaque affirmation est suivie de sa source sous la forme
> `fichier:page`, où le numéro est celui de la **page PDF**. Les citations entre guillemets sont
> reproduites telles quelles. Lorsqu'une information est absente des documents, c'est écrit
> explicitement plutôt que déduit.

---

## ⚠️ Les cinq points à retenir avant tout

1. **L'ouverture est le 14 octobre 2026 à 13 h 30**, pas le 29 septembre. La date du 29 septembre
   figure encore dans trois documents du dossier ; elle est périmée.
2. **Chiffrer sur les plans de l'Addenda-01 uniquement.** Ceux du dossier `Plans/` ne sont pas
   scellés par l'ingénieur, et le jeu Structure y est une émission de revue, pas d'appel d'offres.
3. **L'électricité se chiffre en 12 prix distincts** : 3 lignes (Services et éclairage / Urgence /
   Incendie) × 4 lots.
4. **L'amiante est invisible et généralisé** : le plâtre de base des murs et plafonds est positif
   sous une couche de finition propre. Tout perçage est concerné. Le désamiantage doit précéder
   les travaux, et son coût est à la charge du soumissionnaire — sans devis de référence au dossier.
5. **Le risque financier le plus lourd n'est pas la pénalité de 500 $/jour** (qui ne vise que les
   déficiences) mais les **frais de subsistance des locataires, non plafonnés**, si un logement
   n'est pas rendu à temps.

---

## 1. Inventaire des documents

24 fichiers PDF, 1 180 pages, 338 596 406 octets. `Thumbs.db` (3 fichiers) exclu de la copie de
travail. La source n'a subi aucune modification.

| Fichier | Octets | Pages | sha256 |
|---|---:|---:|---|
| `Addenda/Addenda-01/Addenda 01.pdf` | 190 420 | 2 | `62afaa380f6fe1a64b322a88fed373d5e3575fe8660e9e774a417ec61bfd0512` |
| `Addenda/Addenda-01/Devis_A_Pour soumission.pdf` | 1 051 849 | 270 | `bb37f0a4699bb71d827348ecc7e8d8b095710d5e00d76ea48af6e63092304266` |
| `Addenda/Addenda-01/Plan_Civ_Pour soumission.pdf` | 4 442 782 | 2 | `2ec4fdc187224f074e5c4b3daf277110d4cbf54a245ffe57148066bfd8f90e23` |
| `Addenda/Addenda-01/Plan_Lot A_A_Pour soumission.pdf` | 26 514 479 | 46 | `6be4c3019c6cab649957284582803ac3e74ec65b364a190a735e6593eed18139` |
| `Addenda/Addenda-01/Plan_Lot B_A_Pour soumission.pdf` | 22 483 924 | 41 | `dcaa7857e6fa6c213d484bedaa240e1a8f6b39acad089a87fd7e3608a8f4139e` |
| `Addenda/Addenda-01/Plan_Lot C_A_Pour soumission.pdf` | 34 342 306 | 43 | `6f4314f18f9668a2c8c1019e59f23a421a247aaf6091136a433e6965f6bf4df6` |
| `Addenda/Addenda-01/Plan_Lot D_A_Pour soumission.pdf` | 31 567 257 | 43 | `c453d192c2fa949d9da6756923c1d5b8fd9d7a17a7d606b0945148cd3aa776f5` |
| `Addenda/Addenda-01/Plan_ME_Pour soumission.pdf` | 38 983 414 | 60 | `3a591c05c1e0b7fa5e31eae096307b11176ae52f0cfa726b40aadf37cbe74745` |
| `Addenda/Addenda-01/Plan_Str_Pour soumission.pdf` | 7 338 982 | 23 | `cd17d6462fbb446eac322a3af19a03de22c7aef0d4257a368a579fbf7ac2efa2` |
| `Appeloffres.pdf` | 131 146 | 1 | `05102379d1b1a62071e9cdc77bfe4c7d0ce13159f5b10f8c52ae3ccda6d98793` |
| `Clauses et informations complémentaires.pdf` | 3 059 606 | 17 | `2c51a9ed63db44a8cce897529c8967d132d6dd99c3566a8d07a6ff0feb1c2676` |
| `Devis/Devis_A_Pour soumission.pdf` | 1 051 849 | 270 | `bb37f0a4699bb71d827348ecc7e8d8b095710d5e00d76ea48af6e63092304266` |
| `FORMULAIRE - AUTORISATION DE SIGNATURE.pdf` | 98 985 | 1 | `4a4ac502c445c7a80c0e1fd328c5ca6637cb833ee6f96c8b960fab35668b7599` |
| `Formulaire soumission.pdf` | 618 245 | 14 | `9c4de548fb778f5065f3e61f8689ad9c65595b6a9787d6bef3ce60e658a35712` |
| `LCV-contrats-Ao-Travaux-Construction HR26-14.pdf` | 868 138 | 49 | `3c090df250bf9f202772e1200738c5f38bee8962ca4421c8b3a975ea2fed136a` |
| `LISTE DOCUMENT CONTRATUEL.pdf` | 106 358 | 1 | `8d25334bfa4521bfdc35896045c18cd961fa7ab71b0373d1dd391097fde90e21` |
| `Plans/Plan_Civ_Pour soumission.pdf` | 4 442 782 | 2 | `2ec4fdc187224f074e5c4b3daf277110d4cbf54a245ffe57148066bfd8f90e23` |
| `Plans/Plans et Devis_ME_Pour Soumission.pdf` | 34 576 646 | 60 | `34c503420ec81b79ae06ad136325cdcb1d6257d4477ddc4587efad529bd8122a` |
| `Plans/Plans et Devis_Str_Pour Soumission.pdf` | 4 576 343 | 23 | `b20f4385ed7647bc76c9e1d75157dabb8fd2dced393a94e9706ee437f9ba8e2d` |
| `Plans/Plans_Lot A_A_Pour Soumission.pdf` | 27 038 715 | 46 | `4f73b46fec72aba18dd4c29287c8a254d539761182cfd0b71e70ccf43fb87f7d` |
| `Plans/Plans_Lot B_A_Pour Soumission.pdf` | 22 829 956 | 41 | `9c38dd4144b401a79d55dc204f138c996e8a3647ffa42662a3f5fd9f4a01d2e0` |
| `Plans/Plans_Lot C_A_Pour Soumission.pdf` | 34 816 236 | 43 | `0cdae0b583c8498c7829267dd9f6eb2c21c2ffea052055e38e53d25c4f2071f7` |
| `Plans/Plans_Lot D_A_Pour Soumission.pdf` | 32 038 620 | 43 | `8de4a0dd43c69947202130ed6e75c362ca586d06d84ee4a2444f4f7ac5cdf367` |
| `Rapport amiante.pdf` | 5 427 368 | 39 | `b6a856db46952be2585da77ada1b23bc8c6066607f0c908476423d20f24a11de` |

**Doublons exacts** (hash identique) entre le dossier de base et l'addenda :
`Plan_Civ` (`2ec4fdc1…`) et `Devis_A` (`bb37f0a4…`). L'addenda les re-livre **sans changement**.

**Extractibilité** : tous les PDF contiennent du texte extractible, sauf `Addenda 01.pdf`
(0 caractère/page — document scanné, lu par rendu d'image).

---

## 2. Cadre contractuel : dates, exigences, garanties, cautionnements, pénalités

### 2.1 Dates clés

| Élément | Valeur | Source |
|---|---|---|
| **Ouverture des soumissions** | **14 octobre 2026, 13 h 30** | `Addenda 01.pdf:1` |
| Date périmée (encore au dossier) | 29 septembre 2026, 10 h 00 | `Appeloffres.pdf:1`, `LCV…:5`, `LISTE DOCUMENT CONTRATUEL.pdf:1` |
| Lieu | 145 rue Latour, bureau 100 | `LCV…:5` |
| **Visite des lieux** | **Facultative, aucune date fixée**, sur rendez-vous | `Appeloffres.pdf:1` |
| **Questions / équivalences** | **72 h** avant l'heure limite | `LCV…:11` |
| Addenda influençant les prix | au moins 7 jours avant | `LCV…:11` |
| Validité de la soumission | **45 jours** | `LCV…:14` |
| Exécution des travaux | « entre octobre 2026 et le 15 décembre 2028 » | `Clauses…:1` |

> « La date d'ouverture des soumissions est reportée au 14 octobre 2026 à 13h30. »
> — `Addenda 01.pdf:1`

> « Les Entrepreneurs intéressés à soumissionner peuvent contacter l'Office Municipal
> d'Habitation Haut-Richelieu (Madame Myriame Dupuis – 514-717-1710) s'ils désirent voir les
> lieux. Aucune information particulière ne peut être obtenue autrement. » — `Appeloffres.pdf:1`

**Aucune visite obligatoire, aucune date de visite, aucune attestation de visite** n'existe dans
le dossier. En contrepartie la responsabilité de s'informer est intégralement transférée :
« il est de sa responsabilité de se renseigner sur l'état de l'emplacement et la nature des
travaux à accomplir » (`LCV…:11`).

> « Le soumissionnaire qui désire obtenir des renseignements complémentaires […] doit soumettre
> ses questions au représentant de l'Office au moins soixante-douze (72) heures avant la date et
> l'heure limites pour la réception des soumissions. » — `LCV…:11`

Interlocuteur **unique** : Myriame Dupuis, conseillère technique, 514-717-1710,
m.dupuis@omhhr.com (`LCV…:5`). Communiquer avec un autre employé est un motif de rejet (`LCV…:7`).

### 2.2 Exigences de soumission

**Dépôt papier en enveloppe scellée — il n'y a pas de dépôt électronique.** SEAO ne sert qu'à
obtenir les documents (`Appeloffres.pdf:1`).

> « Le soumissionnaire présente sa soumission sous emballage scellé portant les inscriptions
> suivantes : son nom et son adresse; le nom et l'adresse du destinataire; la mention
> « Soumission »; le titre et le numéro de l'appel d'offres. » — `LCV…:12`

Documents à joindre (`LCV…:12`, complété par `LISTE DOCUMENT CONTRATUEL.pdf:1`) :
formulaire de soumission et bordereau de prix signé · attestation de probité · déclaration de
lobbyisme · attestation d'intégrité · attestation de Revenu Québec · cautionnement ou garantie de
soumission · résolution d'autorisation de signature (`FORMULAIRE - AUTORISATION DE SIGNATURE.pdf:1`).
La liste du `LISTE DOCUMENT CONTRATUEL` ajoute explicitement « incluant la ventilation des coûts »
et traite la résolution comme obligatoire. **Joindre les deux listes réunies.**

Licence RBQ exigée **à la date limite de réception** (`LCV…:15`) et maintenue toute la durée du
contrat (`LCV…:36`). **Aucune sous-catégorie RBQ n'est nommée** dans le dossier.

Attestation de Revenu Québec : « ne doit pas avoir été délivrée après la date et l'heure limites
fixées pour la réception des soumissions » (`LCV…:14`).

**Motifs de rejet automatique** (`LCV…:15`) : retard · absence du formulaire signé avec le montant ·
soumission conditionnelle ou restrictive · **absence de garantie de soumission conforme** ·
plusieurs soumissions. Tout autre défaut est corrigible sans modifier le montant (`LCV…:16`).

### 2.3 Garanties et retenues

| Élément | Valeur | Source |
|---|---|---|
| Retenue sur chaque paiement | **10 %** | `LCV…:40` |
| Couverture des défauts après réception | jusqu'à la **fin de la 2ᵉ année** | `LCV…:44` |
| Garantie de fin de contrat | **1 %** (min. 500 $), levée après **1 an** | `LCV…:34` |
| Paiement des demandes | 30 jours ; solde final 45 jours | `LCV…:40` |

Le terme « garantie de parachèvement » **n'apparaît nulle part** ; le mécanisme équivalent est le
cautionnement d'exécution. Le paiement final exige l'attestation de conformité **CNESST**
(`LCV…:40`).

Le devis d'architecture impose par ailleurs des garanties techniques plus longues, notamment
« une garantie construction générale de un (1) an » (`Devis_A:70`) et, pour certains ouvrages,
« pour une période de 5 ans » (`Devis_A:109`).

### 2.4 Cautionnements

**Garantie de soumission** (`LCV…:13`) :
- **10 %** du montant si **cautionnement** d'une compagnie habilitée (formulaire Annexe 5) ;
- **5 %** si **chèque visé, mandat, traite ou lettre de garantie irrévocable** (Annexe 6).
- Validité **45 jours**. ⚠️ **À faire émettre contre le 14 octobre 2026**, non le 29 septembre :
  une garantie périmée tombe sous le rejet automatique.

**Avant signature du contrat** (`LCV…:34`) :
- Sous forme de **cautionnement** : exécution **50 %** + gages/matériaux/services **50 %** ;
- Sous forme monétaire ou LGI : **10 % au total**.
- Réémission obligatoire dès que les avenants cumulés atteignent **+10 %** du contrat.

**Assurances** (`LCV…:34`) : responsabilité civile « égale ou supérieure à la valeur du
bâtiment » ; **assurance chantier obligatoire** puisque les bâtiments restent occupés ; OMHHR et
SHQ ajoutés comme assurés additionnels.

### 2.5 Pénalités — attention au contresens

> « À défaut par l'Entrepreneur de corriger et de compléter les travaux (liste de déficiences)
> dans le délai fixé dans l'avis, celui-ci devra verser à l'Office une pénalité de cinq cents
> dollars (500 $) par jour de retard à titre de dommages liquidés, et ce, pour le seul retard
> dans l'exécution. » — `LCV…:41`

Cette pénalité **ne vise que la correction des déficiences**. **Il n'existe aucune pénalité
journalière pour le dépassement du 15 décembre 2028** dans le dossier.

**Le risque financier réel est ailleurs** — et il n'est pas plafonné :

> « Advenant le non-respect de l'échéancier, l'entrepreneur devra assumer les frais de
> subsistance des locataires touchés du vendredi soir jusqu'à ce que la cuisine et la salle de
> bain soit fonctionnelle. » — `Clauses…:3`

Avec la cadence imposée :

> « L'entrepreneur a dix (10) jours pour exécuter la totalité des travaux de cuisine. […]
> 5 premiers jours (Début le lundi matin et pour se terminer le vendredi après-midi). À
> l'intérieur de ces cinq (5) jours l'entrepreneur à l'obligation suivante : Démolition, nouvelle
> plomberie et électricité, relocalisation de la nouvelle sortie de hotte et nouvelle armoire de
> cuisine installée. » — `Clauses…:3`

**La démolition, la plomberie ET l'électricité d'une cuisine doivent tenir en 5 jours ouvrables.**
C'est la contrainte la plus lourde du dossier pour un électricien.

---

## 3. Addenda 01 — changements et impact électrique

**Émis le 2 septembre 2026** par Myriame Dupuis, conseillère technique (`Addenda 01.pdf:1-2`).
Document scanné, lu par rendu d'image ; preuves : `preuves/addenda01-p1.png`, `preuves/addenda01-p2.png`.

### 3.1 Les trois changements

| # | Changement | Impact électrique |
|---|---|---|
| 1 | « La date d'ouverture des soumissions est reportée au **14 octobre 2026 à 13h30**. » | Report de 15 jours. Faire émettre la garantie de soumission contre cette date. |
| 2 | Correction des heures de bureau dans `LCV-contrats-Ao-Travaux-Construction HR26-14` : mercredi à partir de **10 h 00** au lieu de 08 h 00 | Affecte le dépôt physique et le calcul des 72 h pour les questions. |
| 3 | « **Tous les plans d'architecture, de mécanique, de structure et de civil sont réémis pour appel d'offre.** » | Les plans à chiffrer sont **ceux de l'Addenda-01**. |

Force obligatoire : « Les soumissionnaires doivent indiquer dans leur soumission avoir pris
connaissance de cet addenda faute de quoi celle-ci pourrait être rejetée. » (`Addenda 01.pdf:1`)

### 3.2 Ce que l'addenda remplace réellement — mesuré par hash

L'addenda annonce une réémission globale. Les sha256 montrent que **2 des 8 documents sont
identiques octet pour octet** — donc re-livrés sans changement :

| Document | Base | Addenda-01 | Verdict |
|---|---|---|---|
| Plan_Civ | `2ec4fdc1…` | `2ec4fdc1…` | **identique** |
| Devis_A | `bb37f0a4…` | `bb37f0a4…` | **identique** |
| Lot A | `4f73b46f…` | `6be4c301…` | remplacé |
| Lot B | `9c38dd41…` | `dcaa7857…` | remplacé |
| Lot C | `0cdae0b5…` | `6f4314f1…` | remplacé |
| Lot D | `8de4a0dd…` | `c453d192…` | remplacé |
| **ME** | `34c50342…` | `3a591c05…` | **remplacé** |
| Str | `b20f4385…` | `cd17d646…` | remplacé |

Le nombre de pages est **inchangé** pour les 6 documents remplacés (Lot A 46, Lot B 41, Lot C 43,
Lot D 43, ME 60, Str 23) : **aucune feuille ajoutée ni retirée.**

> Note de nommage : la base écrit `Plans_Lot A_…Soumission.pdf`, l'addenda
> `Plan_Lot A_…soumission.pdf`. L'appariement est fait par lot, pas par nom de fichier.

### 3.3 Impact sur les plans ME (électricité) : les plans de base ne sont pas scellés

Comparaison page par page des 60 pages du PDF ME, base contre addenda.

**Dans le texte**, la seule différence est l'**indice de révision** :

```
PAGE 1 : -1 / +3   et   -B / +C
PAGE 2 : -2 / +3
PAGE 3 : -2 / +3
```

**Dans le dessin**, l'écart est faible et n'est pas un décalage de ré-export — dimensions
identiques (2162 × 1441 à 60 dpi) et aucun décalage testé sur ±2 px ne le réduit :

```
feuille E01 (page 33) : diff à décalage 0,0 = 0,20 %  ;  meilleur décalage dx=0 dy=0 → 0,20 %
volumes : E01 p33 = 2 793 px · E07 p39 = 8 694 px · E15 p47 = 17 563 px (sur ≈3,1 M px)
```

**La différence de fond est dans le cartouche.** Zone la plus dense en écarts de la feuille E15 :

- `preuves/me-e15-base.png` : case « sceau » **vide**
- `preuves/me-e15-add.png` : **sceau d'ingénieur et signature manuscrite, datés `2026-08-31`**

**Conclusion : l'Addenda-01 apporte aux plans ME leur scellement et leur signature par
l'ingénieur.** Aucune modification de contenu technique électrique n'est détectable entre les
deux versions. Le reste des écarts de pixels est du bruit de rendu (anti-crénelage).

**Cela ne dispense pas d'utiliser le jeu de l'addenda** : c'est le seul que l'addenda réémet et
le seul scellé — donc le seul contractuel.

### 3.4 Pour mémoire, le cas Structure est bien plus profond

Contrairement au ME, le jeu Structure de base n'est pas seulement non scellé : c'est une
**émission de revue**.

```
Str base    : statut = « COMMENTAIRES 100% »          date = 2026-06-03
Str addenda : statut = « ÉMIS POUR APPEL D'OFFRES »   date = 2026-08-26
Civ base et addenda : « ÉMIS POUR APPEL D'OFFRES » (déjà) → d'où l'identité des deux fichiers
```

Preuves : `preuves/str-p1-base.png`, `preuves/str-p1-addenda.png`.

### 3.5 Repérage des feuilles électriques

Dans le PDF ME (60 pages), l'index de la page 1 classe les feuilles en **P** (plomberie),
**V** (ventilation) et **E** (électricité — services et éclairage). Les feuilles **E01 à E15**
occupent les **pages 33 à 51** du PDF.

---

## 4. Devis et plans électriques — étendue, prescriptions, risques

### 4.1 CONSTAT CAPITAL : il n'existe aucune Division 26 dans cet appel d'offres

Le fichier `Devis_A_Pour soumission.pdf` est le **devis d'architecture seul**. Vérification faite
sur les 270 pages : les seuls préfixes de section présents sont **00 à 10**, et l'on compte
**zéro occurrence** d'un numéro de section 26, 27 ou 28. La dernière section est
`10 28 11 Trappes diverses` (page 269).

Le découpage officiel le confirme :

> « Devis d'architecture MA architecte : 00 01 10 à 10 28 11 »
> « Plans de mécanique par ARI Bureau d'Étude : 00 / P01 à P18 / V01 à V13 / **E01 à E15** /
> **EU01 à EU04** / **DSI01 à DSI09** » — `LCV…:10`

Le projet est d'ailleurs structuré selon l'**ancien MasterFormat à 16 divisions** pour ses
renvois — l'électricité y est la « Division 16 » (`Devis_A:64` et `:161`).

> **Conséquence pratique.** Les prescriptions électriques ne sont pas dans le devis : elles sont
> **imprimées sur deux feuilles de plans**, `E15` (page 47 du PDF ME, 31 979 caractères) et
> `DSI09` (page 60, 16 016 caractères). Dans toute question, demande de clarification ou
> réclamation, **citer la feuille et l'article**, jamais un numéro de section de devis.

### 4.2 Cartographie des feuilles électriques

| Feuille | Titre | Page PDF |
|---|---|---:|
| E01–E05 | Lot A — 145 St-Georges : vues en plan, unifilaire et cédules, logements types | 33–37 |
| E06–E08 | Lot B — 155 Mercier | 38–40 |
| E09–E11 | Lot C — 290 Montcalm (E11 couvre aussi 291 Chaussé) | 41–43 |
| E12–E14 | Lot D — 291 Chaussé | 44–46 |
| **E15** | **DEVIS — services et éclairage** | **47** |
| EU01–EU04 | Éclairage d'urgence, lots A à D | 48–51 |
| DSI01–DSI08 | Détection et signalisation incendie, lots A à D | 52–59 |
| **DSI09** | **DEVIS ET DÉTAILS — incendie** | **60** |

### 4.3 Étendue des travaux électriques

> « L'ENTREPRENEUR SPÉCIALISÉ EN ÉLECTRICITÉ DEVRA FOURNIR, INSTALLER, RACCORDER ET METTRE EN
> MARCHE TOUS LES ÉQUIPEMENTS ET COMPOSANTES ÉLECTRIQUES, LE TOUT TEL QUE MONTRÉ AUX PLANS ET
> DEVIS. IL DEVRA AUSSI ENLEVER, DÉMANTELER ET DÉBRANCHER TOUS LES ÉQUIPEMENTS ET COMPOSANTES
> ÉLECTRIQUES » — E15, art. 1, page 47

> « LES TRAVAUX DE DÉTECTION ET SIGNALISATION INCENDIE (DSI) […] **FONT PARTIE INTÉGRANTE DES
> TRAVAUX ÉLECTRIQUE**. » — E15, art. 1, page 47

L'ouvrage principal, pour **les quatre bâtiments** : « Réfection complète de l'entrée
électrique » (`LCV…:9`), en **bâtiments occupés** (`LCV…:9`).

**Séquence imposée** (E15, art. 24, page 47) : raccorder temporairement le groupe électrogène →
branchement temporaire entre le répartiteur existant et le nouveau panneau principal → remplacer
l'entrée (sectionneur principal et boîtier de compteur) → réalimenter via Hydro-Québec → mise en
marche → relocaliser un à un les services vers le nouveau panneau → démolition sélective. Avec
cet avertissement : « LA PRÉSENTE PLANIFICATION EST DONNÉE À TITRE INDICATIF SEULEMENT.
L'ENTREPRENEUR DEMEURE LE SEUL RESPONSABLE POUR LA PLANIFICATION DES TRAVAUX ».

**Éclairage d'urgence** : remplacement des appareils autonomes 120 V par des appareils bas voltage
à double tête, avec nouvelle alimentation indépendante et abandon du 120 V existant (EU01, p. 48).

**Incendie** : système neuf **entièrement adressable**, démolition des systèmes existants et
« **REMPLACER TOUT LE FILAGE NON CONFORME** » (DSI09, art. 1, p. 60).

### 4.4 Les cinq exigences qui coûtent cher

**a) Conducteurs d'aluminium existants — le risque non quantifié le plus lourd**

> « **TOUS LES CONDUCTEURS OBSERVÉS DANS LES INSTALLATIONS ÉLECTRIQUES EXISTANTES SONT AVEC
> CONDUCTEUR EN ALUMINIUM.** […] L'ENTREPRENEUR EST RESPONSABLE DE NE PAS CASSER LES EXTRÉMITÉS
> DES CONDUCTEURS D'ALUMINIUM EXISTANT. **L'ENTREPRENEUR SERA TENU DE REMPLACER, À SES FRAIS
> (INCLUANT LES TRAVAUX GÉNÉRAUX) TOUS LES CÂBLES AVEC CONDUCTEURS D'ALUMINIUM RENDUS TROP COURTS
> PAR SA MANIPULATION.** » — E15, art. 3, page 47

De l'aluminium vieilli de 1974, manipulé dans des centaines de boîtes, avec remplacement du
circuit **et** des travaux généraux (plâtre, peinture) à la charge de l'électricien.

**b) Fenêtre de coupure restreinte à l'été**

> « TRAVAUX ÉLECTRIQUES DE REMPLACEMENT DE LA DISTRIBUTION ÉLECTRIQUE DOIVENT ÊTRE EFFECTUER
> **EN DEHORS DE LA SAISON DE CHAUFFAGE, SOIT DU 1 MAI AU 15 SEPTEMBRE** » — E15, art. 22, page 47

Avec maintien **en tout temps** de l'éclairage d'urgence, de la détection incendie, du contrôle
d'accès et de l'éclairage des corridors (interruptions de **moins de 10 minutes** tolérées), et
maintien du service des logements « DE 17 H À 7 H ET À TOUT TEMPS POUR LES FINS DE SEMAINE ».
Préavis de coupure : 5 jours (E15, art. 23) — mais 4 semaines côté architecture (`Devis_A:76`).

> **Interaction critique, énoncée dans aucun document unique** : le contrat court de novembre 2026
> à décembre 2028, mais les coupures ne sont permises que du 1ᵉʳ mai au 15 septembre. Il ne reste
> donc que **deux fenêtres estivales (2027 et 2028)** pour remplacer les 4 entrées électriques.

**c) Groupe électrogène de location, 24/7**

> « FOURNIR UN GROUPE ÉLECTROGÈNE DE LOCATION D'UNE CAPACITÉ DE **150KW/125KVA, 120/208VOLTS
> TRIPHASÉ, 4 FILS** AVEC ENCEINTE ACOUSTIQUE (65DBA MAX) ET RÉSERVOIR DE CARBURANT INTÉGRÉ. […]
> **ASSURER LE FONCTIONNEMENT DU GROUPE ÉLECTROGÈNE ET L'APPROVISIONNEMENT DU CARBURANT EN TOUT
> TEMPS. FOURNIR UN CONTACT DE SERVICE 24HEURES, 7 JOURS** » — E15, art. 25, page 47

Câbles à passer « PAR LE SOFFITE DE L'IMMEUBLE (CORNICHE), LE GRENIER ET LA TRAPPE DU GRENIER ».
Location + carburant + astreinte, **× 4 bâtiments**, sur une durée que l'entrepreneur doit
lui-même estimer.

**d) Détection incendie : qualification, câblage et double vérification**

> « […] DOIVENT ÊTRE EFFECTUÉS PAR LE FABRICANT OU PAR UN ENTREPRENEUR SPÉCIALISÉ EN ALARME
> INCENDIE AUTORISÉ PAR LE FABRICANT ET DÉTENANT D'UNE **LICENCE DE SOUS-CATÉGORIE 13.2 DE LA
> RÉGIE DU BÂTIMENT DU QUÉBEC**. IL DOIT AUSSI ÊTRE MEMBRE DE L'**ASSOCIATION CANADIENNE D'ALARME
> INCENDIE (ACAI)**. DE PLUS, IL DOIT AVOIR DE L'EXPÉRIENCE ACQUISE SUR AU MOINS **TROIS PROJETS
> SIMILAIRES** » — DSI09, art. 4, page 60

Câblage **Classe A** pour détection et signalisation, « PROTECTION DES CONDUCTEURS D'AU MINIMUM
1 HEURE […] OU […] CÂBLAGE CSA, ULC APPROUVÉ 2 HEURES », boucles chargées à **80 % maximum**,
conduit EMT en espaces non aménagés et **Wiremold métallique laqué blanc** en espaces aménagés,
couvercles de boîtes **peints en rouge**, et « AUCUN CONDUIT NI CÂBLE APPARENTS […] DANS LES
LOGEMENTS » (DSI01, p. 52).

Et surtout, **deux firmes distinctes** :

> « **LA VÉRIFICATION DOIT ÊTRE EFFECTUÉE PAR UNE FIRME AUTRE QUE CELLE QUI A PROCÉDÉ À SON
> INSTALLATION.** » — DSI09, art. 12, page 60

Vérification ULC-S537 (avec sonomètre calibré ANSI S1.40 de moins d'un an) **plus** essais
dynamiques ULC-S1001 couvrant gicleurs, ventilation, portes, ascenseurs, génératrices —
« LES FRAIS RELATIFS À CES ESSAIS SONT À LA CHARGE ENTIÈRE ET EXCLUSIVE DU PRÉSENT ENTREPRENEUR ».
Le vérificateur doit fournir une assurance spécifique de **1 000 000 $** (dommages à la propriété)
et **300 000 $** (dommages aux personnes) (DSI09, art. 13).

**e) Équivalences : crédit obligatoire, et rien après la soumission**

> « SI L'ENTREPRENEUR DÉSIRE UTILISER DES APPAREILS […] DE MARQUE ALTERNATIVE, IL DEVRA SOUMETTRE
> UNE DEMANDE D'ÉQUIVALENCE **AVEC LA SOUMISSION** […] **LA DIFFÉRENCE DE PRIX DOIT FAIRE L'OBJET
> D'UN CRÉDIT.** » — E15, art. 8.2, page 47
> « .10 **Aucune équivalence ne sera acceptée après les soumissions.** » — `Devis_A:12`

Marques imposées à chiffrer telles quelles : câbles **Northern Cable** (AC90, FAS 105 Glo Wrap)
et **Noramco** (RW90, RWU90) ; prises et interrupteurs **Leviton** ; plinthes, thermostats et
convecteurs **Stelpro** ; appareillage de distribution **Schneider** (Powerpact + MGL, série DU) ;
luminaires **Canarm** série Omni ; scellant **Hilti Firestop** (E15, page 47).

### 4.5 Caractéristiques techniques imposées

| Exigence | Valeur | Source |
|---|---|---|
| Chute de tension maximale | **3 %** — choix du calibre à la charge de l'entrepreneur si non indiqué | E15 art. 21 |
| Conducteurs neufs | **cuivre obligatoire** ; MALT par l'armature interdite | E15 art. 3 |
| Calibres imposés | 15 A→14 AWG · 20 A→12 AWG · 30 A→10 AWG · 40 A→8 AWG | E15 art. 3 |
| Pouvoir de coupure | **22 kA** entrée→panneaux de service ; **10 kA** panneaux de logement ; **65 kA** interrupteur principal | E15 art. 12, 15 |
| Disjoncteurs anti-arc | obligatoires pour les prises des **chambres à coucher** | E15 art. 15 |
| Prises neuves | **toutes inviolables** | E15 art. 7 |
| Boîtier de compteur | conforme Hydro-Québec, **Livre bleu**, type B | E15 art. 14 |
| Installations | **dissimulées**, sauf salles mécaniques/électriques et espaces non aménagés | E15 art. 5 |

### 4.6 Provisions obligatoires « pour fin de soumission »

À inclure au prix, sans quoi la soumission est incomplète :

- « L'ENTREPRENEUR DOIT PRÉVOIR LA FOURNITURE ET L'INSTALLATION DE **5 DISPOSITIFS DE
  SIGNALISATION SUPPLÉMENTAIRE, NON MONTRÉS AUX PLANS** […] CÂBLAGE ET […] RACCORDEMENT ET LA
  PROGRAMMATION […] AINSI QUE LES ESSAIS, MESURES ET RAPPORT » — DSI09, art. 8, page 60
- « **PRÉVOIR LE RETRAIT D'UN PANNEAU D'ALARME INCENDIE ET DE 20 DISPOSITIFS** RÉPARTIS DANS LE
  BÂTIMENT À UNE DISTANCE MOYENNE DE 20 M DU PANNEAU. » — DSI01, page 52
- « PRÉVOIR AU MINIUM **2 CONTACTS DE PLUS** QUE CE QUI EST REQUIS SUR LE SITE » — E15, art. 17

### 4.7 Travaux non montrés aux plans, à chiffrer quand même

**Deux campagnes de traçage complet, × 4 bâtiments, avec rapport écrit** :

> « LES INFORMATIONS INDIQUÉES SUR LES CÉDULES EXISTANTES […] SONT DONNÉES **À TITRE INDICATIF
> SEULEMENT**. AVANT LE DÉBUT DES TRAVAUX, **TRACER TOUTES LES ALIMENTATIONS ÉLECTRIQUES DES
> CIRCUITS** […] **FAIRE UN RAPPORT ÉCRIT DE CE TRAÇAGE.** » — E15, art. 27, page 47

> « EFFECTUER UN **TRAÇAGE COMPLET** DES ALIMENTATIONS 120 VOLTS ET BAS VOLTAGES. » — EU01, p. 48

**Scellement coupe-feu des pénétrations existantes** — quantité non montrée, à relever sur place :

> « POUR TOUS CÂBLES ET CANALISATIONS ÉLECTRIQUES EXISTANTS **OU NOUVEAUX** TRAVERSANT […] UNE
> SÉPARATION COUPE-FEU, PRÉVOIR L'APPLICATION D'UN SCELLANT COUPE-FEU […] CECI EST
> PARTICULIÈREMENT APPLICABLE À **TOUS LES CÂBLES ET CANALISATIONS EXISTANTS DE LA SALLE
> ÉLECTRIQUE** » — E15, art. 28, page 47

**Frais Hydro-Québec** :

> « L'ENTREPRENEUR EST AUSSI TENU DE **PAYER TOUS LES FRAIS NÉCESSAIRES D'HYDRO-QUÉBEC POUR
> OBTENIR LES PERMIS, EFFECTUER LES COUPURES ET LES BRANCHEMENTS DE SERVICE**. » — E15, art. 29

**Éclairage temporaire** « POUR TOUTE LA PÉRIODE DES TRAVAUX » (E15, art. 20), à au moins
**162 lux** aux planchers et escaliers (`Devis_A:37`).

**Évacuation quotidienne** : « TOUT ÉQUIPEMENT ET COMPOSANT ÉLECTRIQUE EXISTANT ET RETIRÉ DOIT
ÊTRE **ÉVACUÉS QUOTIDIENNEMENT DU SITE** » (E15, art. 26) — et l'OMHHR décline toute
responsabilité pour les vols sur le site.

### 4.8 Sections de Division 01 qui obligent l'électricien

| Section | Obligation | Page |
|---|---|---:|
| 01 10 05 | **Inspection avant recouvrement** des conduits d'électricité dans les murs — à défaut, dégarnir aux frais de l'entrepreneur | 14 |
| 01 33 00 | Dessins d'atelier avant travaux ; un retard « ne saurait constituer une raison suffisante pour obtenir une prolongation » | 25 |
| 01 32 16 | Diagramme de Gantt dans les **15 jours ouvrables** suivant l'adjudication | 22 |
| 01 54 50 | Plan de santé-sécurité dans les 10 jours ; **maître d'œuvre CNESST** ; amendes remboursables | 44-46 |
| 01 74 00 | Évacuation **quotidienne** des débris | 60 |
| 01 47 00 | Preuve de disposition avec billet de transport ; conteneurs du propriétaire interdits | 33 |
| 01 52 00 | **Gardiennage hors heures aux frais de l'adjudicataire** | 41 |
| 01 79 00 | Formation du personnel 2 semaines avant l'inspection finale | 72-73 |
| 01 78 00 | Étiquette de garantie sur **chaque** élément électromécanique ; garanties notariées en double | 70-71 |
| 07 84 00 | Protection coupe-feu : dessins d'atelier par ensemble, échantillons, essais CAN/ULC-S101/S102/S115 | 161-170 |

Et la clause qui ferme toute réclamation de quantité :

> « L'Entrepreneur devra déterminer les quantités des éléments requis […] **en fonction de la
> situation existante du site. Il sera entièrement responsable des quantités sur lesquelles il
> aura soumissionnées.** » — `Devis_A:12`

**Hiérarchie des documents** en cas de contradiction : date la plus récente > devis sur dessins >
conditions générales du contrat sur les divisions 2 à 16 > contrat de construction (`Devis_A:13`).

### 4.9 Frontière des percements et ragréage — à faire trancher par écrit

Les notes de plans attribuent l'ouverture et le ragréage à **l'entrepreneur général** :

> « LES TRAVAUX D'OUVERTURE ET RAGRÉAGE REQUIS POUR LES TRAVAUX D'INSTALLATION SONT SOUS LA
> RESPONSABILITÉ DE **L'ENTREPRENEUR GÉNÉRALE**. » — DSI01, page 52

Mais le scellement pare-feu est attribué à l'électricien :

> « LE SOUS-TRAITANT EN ÉLECTRICITÉ EST RESPONSABLE DU SCELLEMENT PARE-FEU DE TOUS LES NOUVEAUX
> SERVICES ÉLECTRIQUES. » — EU01, note 1, page 48

Et l'architecture renvoie la décision à l'entrepreneur général : « L'Entrepreneur général sera
responsable de déterminer qui est responsable de l'ignifugation des percements » (`Devis_A:13`),
avec un seuil : les ouvertures « d'une surface équivalence à un cercle de **150 mm** de diamètre
ou plus sont à la charge de l'Adjudicataire » (`Devis_A:58`).

**Contradiction à clarifier avant de déposer le prix.**

### 4.10 Bordereau : 12 cellules électriques, aucune allocation électrique

> « PLOMBERIE / CHAUFFAGE, VENTILATION ET CONDITIONNEMENT D'AIR / **ÉLECTRICITÉ / SERVICES ET
> ÉCLAIRAGE** / **ÉLECTRICITÉ / URGENCE** / **ÉLECTRICITÉ / INCENDIE** / CIVIL — TRAVAUX
> EXTÉRIEURS ET RÉFECTIONS » × colonnes Lot A / Lot B / Lot C / Lot D
> — `Formulaire soumission.pdf:4`

**3 lignes × 4 lots = 12 prix électriques.** L'estimation doit être structurée ainsi dès le départ.

Les deux seules allocations du bordereau — « ALLOCATION 01 – LINTEAUX EXISTANTS » et
« ALLOCATION 02 – DÉFICIENCES DE MAÇONNERIE » — **ne concernent pas l'électricité**. Il n'existe
donc **aucune provision pour imprévus électriques**, alors que le dossier en accumule : aluminium
cassant, traçage, pénétrations coupe-feu existantes, amiante.

Les changements se règlent par forfait, prix unitaires convenus ou régie majorée, avec
« dix pour cent (10 %) […] à l'entrepreneur et quinze pour cent (15 %), aux sous-contractants »
(`LCV…:37`).

### 4.11 Anomalies documentaires à soulever

1. **Plinthe de portique, escalier et corridor : spécification incomplète** — « À REVOIR.
   CONSTRUCTION EN ALUMINIUM. EN ATTENTE DE / MARQUE SPÉCIFIÉE : STELPRO, À REVOIR » (E15,
   art. 9). **Impossible à chiffrer fermement.**
2. La section `01 10 05 Conditions générales` (pages 12-15) **n'apparaît pas dans la table des
   matières** du devis, alors qu'elle contient les clauses de coordination les plus contraignantes.
3. `Devis_A` page 11 comporte **deux articles numérotés « 1.5 »**.
4. L'index du PDF ME **duplique V10** et omet V13 : « V10 DEVIS, DÉTAILS » alors que V10 désigne
   déjà « LOT D - 291 CHAUSSÉ, VUES EN PLAN, 1 DE 2 ».
5. `LCV…:10` annonce des plans de structure « S001 à S504 », mais le PDF Structure ne compte que
   23 pages.
6. La date d'ouverture apparaît sous **trois valeurs** dans le dossier : 29 septembre
   (`LISTE DOCUMENT CONTRATUEL.pdf:1`), « Octobre 2026 » (`Devis_A:10`) et **14 octobre 13 h 30**
   (Addenda 01, qui prévaut).

---

## 5. Rapport d'amiante — ce que ça change pour l'électricien

**Document** : FNX-INNOV inc., « Caractérisation ciblée relative à la présence de matériaux
susceptibles de contenir de l'amiante », dossier F2100506-001, Mars 2021, Rapport final
révision 2 du 2021-03-26 (`Rapport amiante.pdf:3`). 39 pages.

### 5.1 Le fait déterminant : l'amiante est sous une couche propre

Dans tous les échantillons positifs multicouches, **la couche visible est négative et l'amiante
est en dessous**. Exemple type :

> « - Couche #1 Composition: Crépi de ciment gris blanc-beige peint en beige pâle — FIBRES
> D'AMIANTE: Non détectées »
> « - Couche #2 Composition: Plâtre beige jaune — FIBRES D'AMIANTE: Détectées (+) Type
> d'amiante: Chrysotile 1 à 5% » — `Rapport amiante.pdf:15`

Même structure aux pages 16, 18, 19 et 20.

**Conséquence directe** : aucune inspection visuelle ne permet de repérer le matériau. Le risque
se déclenche **au moment où la mèche ou la scie traverse le fini de surface** — c'est-à-dire
exactement lors du perçage d'une base de détecteur, de la découpe d'une boîte électrique, du
carottage pour un conduit, de l'ouverture d'une retombée de plafond pour tirer du filage, ou de
la démolition partielle pour encastrer un panneau.

### 5.2 Résultats — 10 positifs sur 16

> « Des fibres d'amiante de type Chrysotile ont été observées lors des analyses en concentration
> égale ou supérieure à 0,1 % (entre 1 et 5%) dans les matériaux suivants : » — `Rapport amiante.pdf:12`

| Station | Localisation | Concentration | État |
|---|---|---|---|
| A-2 | Enduit cimentaire, plafond de la conciergerie, sous-sol | 1 à 5 % | non friable |
| A-5 | Composé à joint, mur du rangement à vélo, sous-sol | 1 à 5 % | non friable |
| **A-7** | **Tuile de plancher jaune, entrée d'eau sous la cage d'escalier, sous-sol** | **17,6 %** | non friable |
| A-8 | Enduit cimentaire, plafond de la cage d'escalier, 1ᵉʳ étage (couches #2 et #4) | 1 à 5 % | non friable |
| A-9 | Composé à joint, mur de la cage d'escalier, 1ᵉʳ étage | 1 à 5 % | non friable |
| A-10 | Composé à joint et enduit, plafond du corridor, 3ᵉ étage | 1 à 5 % | non friable |
| A-11 | Composé à joint, mur du corridor 303, 3ᵉ étage | 1 à 5 % | non friable |
| A-12 | Composé à joint, plafond de la toilette, logement 201 | 1 à 5 % | non friable |
| A-13 | Composé à joint, mur de la chambre, logement 201 | 1 à 5 % | non friable |
| A-16 | Composé à joint, mur du corridor 102, 1ᵉʳ étage | 1 à 5 % | non friable |

Source : `Rapport amiante.pdf:9-12` et certificats `:15-21`. Bilan officiel au tableau 3
(`:11`) : 16 échantillons, 10 positifs, 6 négatifs, chrysotile.

**Le dénominateur commun de 9 positifs sur 10 est le « plâtre beige-jaune » du composé à joint** —
présent au sous-sol, au 1ᵉʳ, au 2ᵉ et au 3ᵉ étage. C'est un matériau **généralisé**, pas une poche.

**Cages d'escalier et corridors sont positifs aux trois niveaux testés** — précisément le
parcours des conduits, de l'éclairage d'issue et de la détection.

**Piège** : les deux seuls logements échantillonnés donnent des résultats **opposés** — logement
101 négatif (A-14, A-15), logement 201 positif (A-12, A-13). Aucun logement du 3ᵉ étage ni du
sous-sol n'a été testé. **Chaque logement est une inconnue.**

### 5.3 Un seul bâtiment sur quatre a été échantillonné

Les 16 certificats portent tous « Lieu du prélèvement : 155, rue Mercier » (`:15-21`).
Les trois autres bâtiments sont couverts par extrapolation :

> « Selon les informations fournies par le client, trois (3) autres bâtiments qui ont été
> construits durant la même année (en 1974) par le même entrepreneur, présenteraient des
> similitudes d'ouvrages (même matériaux de construction). Par conséquent, les résultats obtenus
> pour cette caractérisation d'amiante sont représentatifs pour les trois (3) bâtiments
> concernés. » — `Rapport amiante.pdf:5`

L'extrapolation repose sur une information **fournie par le client**, non vérifiée, et formulée
au **conditionnel**. **Zéro échantillon** au 290 Montcalm, au 291 Chaussé et au 145 St-Georges.

**Asymétrie à retenir** : les **positifs se transfèrent** aux trois autres bâtiments (le rapport
le dit), mais les **négatifs ne se transfèrent pas**.

### 5.4 Le rapport n'attribue aucun niveau de risque et ne prescrit aucune procédure

C'est le point le plus important à comprendre : **la détermination est renvoyée à l'entrepreneur.**

> « L'entrepreneur devra définir, avant le début des travaux de déconstruction, de réfection ou de
> toute autre opération, le type de travaux qu'il a à effectuer et le niveau de risque qui y est
> associé selon le type de matériaux rencontré et sa friabilité. Par la suite, il devra prendre
> les précautions nécessaires selon le niveau de risque déterminé. » — `Rapport amiante.pdf:12`

Les obligations ne sont que **référencées** :

> « l'employeur devra s'assurer de respecter, sans s'y limiter, les directives pour la protection
> des travailleurs, telles que décrites aux articles 3.23.14, 3.23.15 et 3.23.16 du Code de
> sécurité pour les travaux de construction. Les procédures de travaux en présence d'amiante
> doivent aussi être conformes aux exigences de la CNESST. » — `Rapport amiante.pdf:12`

Les mots *confinement*, *avis à la CNESST*, *formation*, *protection respiratoire* et
*décontamination* **n'apparaissent nulle part**. La table des mesures à budgéter n'est pas au
dossier : c'est à l'entrepreneur de la produire et de la payer.

### 5.5 Obligations et coûts créés

1. **Désamiantage avant tous travaux — jalon bloquant.**
   > « L'entrepreneur devra réaliser les travaux de désamiantage avant d'entreprendre tous travaux
   > de déconstruction et/ou de rénovation. » — `Rapport amiante.pdf:12`

   L'électricien ne peut ouvrir aucun mur ni plafond en zone positive avant libération.
   À concilier avec la cadence de 5 jours par cuisine (`Clauses…:3`).

2. **Séquence imposée** : « les matériaux contenant des fibres d'amiante nécessitant des mesures
   de protection les plus élevées devront être enlevés en premier lieu » (`:12`).

3. **Le coût est explicitement transféré au soumissionnaire** :
   > « Le soumissionnaire pourra prendre connaissance du contenu de ce rapport afin d'inclure,
   > dans son montant de soumission, tous les travaux et mesures de protection nécessaires afin
   > de se conformer à la réglementation en vigueur pour les travaux effectués en présence
   > d'amiante. » — `Clauses et informations complémentaires.pdf:2`

4. **L'obligation descend jusqu'au sous-traitant** :
   > « L'entrepreneur général doit prendre connaissance de l'annexe soumise dans le dossier SEAO
   > et prévoir les mesures de protection pour tous les occupants incluant lui-même, ses
   > sous-traitants ou ouvriers » — `Devis_A:76`

### 5.6 Ce que le rapport ne couvre pas — le risque d'estimation

**Le mandat est plus étroit que le projet.** Le rapport a été commandé « dans le cadre de la mise
à niveau du système incendie de l'édifice à logement » (`:5`), pas pour une réfection majeure.

**L'échantillonnage a été volontairement réduit :**
> « Cependant, dans le cadre de ce mandat, un nombre d'échantillons inférieur aux recommandations
> a été prélevé à la demande spécifique du client. » — `Rapport amiante.pdf:6`

**Périmètre échantillonné, phrase fermée :**
> « les prélèvements des échantillons ont été effectués sur le composé à joint des murs et
> plafonds en gypse, de l'enduit cimentaire des plafonds, du mortier de bloc de béton et des
> tuiles de vinyle des planchers. » — `Rapport amiante.pdf:6`

**Tout le reste est sans donnée** : calorifuge de tuyauterie, flocage, panneaux de faux plafonds,
colle sous les tuiles, et — directement pertinent — **les équipements et installations
électriques**, alors que le rapport reconnaît le gisement : « il est possible de trouver des
matériaux et des produits qui contiennent des fibres d'amiante dans les composantes de
construction, les installations et les équipements de tous les types de bâtiments » (`:6`).

**La clause de limitation vide la valeur des « non détecté »** :
> « Les résultats obtenus n'impliquent en aucune façon l'absence ou la présence de concentrations
> de contaminants à des endroits autres que ceux sondés. » — `Rapport amiante.pdf:13`

**Et l'électricien n'est pas couvert** :
> « Ce rapport a été préparé pour le seul bénéfice de notre client. Nous déclinons toutes
> responsabilités ou obligations associées à l'utilisation de ce rapport par une tierce
> personne » — `Rapport amiante.pdf:13`

### 5.7 Deux trous dans le dossier contractuel

1. **Le devis d'architecture exclut le désamiantage** — deux fois, texte identique :
   « La présente section exclut ce qui suit : .1 Enlèvement de matières dangereuses ou
   désamiantage. » (`Devis_A:77` et `Devis_A:82`).
2. **Le devis renvoie à un document absent du dossier** : « conformément aux prescriptions des
   documents émis par le Professionnel en travaux d'enlèvement d'amiante » (`Devis_A:74`).
   Aucun devis de désamiantage n'est fourni. **Le prix est exigé sans référence.**

Par ailleurs, **aucune occurrence du mot « amiante » dans le PDF ME** : l'électricien ne trouvera
aucune instruction amiante dans ses propres documents contractuels.

### 5.8 Incohérences relevées (matière à demande d'information)

- **A-2, mur ou plafond ?** Tableau 2 (`:9`) dit « mur du local de la conciergerie » ; la section 4
  (`:12`), le certificat (`:15`) et la photo n° 3 (`:24`) disent « plafond ». Cela change le
  scénario de perçage.
- **A-10, mur ou plafond ?** `:10` et `:12` disent plafond ; la photo n° 13 (`:29`) dit mur.
- **A-1 : « <1 % » (tableau `:9`) contre « <0.1 % » (certificat `:15`)** — facteur 10. Le
  certificat fait foi et classe A-1 négatif.
- Numéros de projet incohérents entre les annexes (`F1626553-016`) et le corps (`F2100506-001`).


## 6. Synthèse — ce qu'il faut faire avant de déposer un prix

### 6.1 Les dix points de risque, classés

| # | Risque | Ampleur | Où |
|---|---|---|---|
| 1 | **Conducteurs d'aluminium de 1974** : casse = remplacement du circuit **et** travaux généraux aux frais de l'électricien | non quantifiable sur plans | E15 art. 3 |
| 2 | **Amiante généralisé et invisible** sous les finis, désamiantage préalable obligatoire, sans devis ni allocation | non quantifiable | `Rapport amiante:12`, `Clauses…:2` |
| 3 | **Cycle de 5 jours** pour démolition + plomberie + électricité d'une cuisine, sanctionné par des frais de subsistance **non plafonnés** | élevée | `Clauses…:3` |
| 4 | **Coupures limitées au 1ᵉʳ mai – 15 septembre** → 2 fenêtres estivales pour 4 entrées électriques | élevée | E15 art. 22 |
| 5 | **Génératrice 150 kW** louée, carburant et astreinte 24/7, × 4 bâtiments, durée à estimer soi-même | élevée | E15 art. 25 |
| 6 | **Double vérification DSI** par une firme tierce (ULC-S537 + essais dynamiques ULC-S1001) avec assurance 1 M$ | moyenne | DSI09 art. 12-13 |
| 7 | **Deux campagnes de traçage** complet avec rapport écrit, × 4 bâtiments, sans article au bordereau | moyenne | E15 art. 27, EU01 |
| 8 | **Scellement coupe-feu des pénétrations existantes** de la salle électrique, quantité non montrée | moyenne | E15 art. 28 |
| 9 | **Aucune allocation électrique** au bordereau, et pas de prix unitaires au contrat | structurelle | `Formulaire soumission.pdf:4` |
| 10 | **Plinthe de corridor non spécifiée** (« À REVOIR ») — impossible à chiffrer fermement | à clarifier | E15 art. 9 |

### 6.2 Questions à poser — délai de 72 h avant le 14 octobre 2026 13 h 30

Le délai de 72 h (`LCV…:11`) tombe autour du **11 octobre 2026 à 13 h 30, un dimanche**. La
clause 4.11 sur le report des délais (`LCV…:35`) ne vise que « les délais prévus pour remplir une
obligation » et ne couvre peut-être pas celui-ci. **Ne pas viser cette date de justesse : poser
les questions au plus tard le vendredi 9 octobre.**

Questions à adresser à Myriame Dupuis (m.dupuis@omhhr.com, 514-717-1710), interlocuteur unique :

1. **Plinthe électrique** de portique, escalier et corridor commun : quelle marque et quel modèle ?
   La feuille E15 porte « À REVOIR / EN ATTENTE DE ».
2. **Scellement coupe-feu** : qui en est responsable pour les services électriques — l'entrepreneur
   général (`Devis_A:13`) ou le sous-traitant en électricité (EU01, note 1) ?
3. **Pénétrations coupe-feu existantes** de la salle électrique : quelle quantité prévoir, ou
   faut-il une allocation ?
4. **Désamiantage** : où est le devis du « Professionnel en travaux d'enlèvement d'amiante »
   mentionné à `Devis_A:74` ? Il n'est pas au dossier. Sur quelle base chiffrer ?
5. **Caractérisation d'amiante** : les 290 Montcalm, 291 Chaussé et 145 St-Georges n'ont fait
   l'objet d'**aucun échantillon**. L'extrapolation du rapport est au conditionnel. Une
   caractérisation complémentaire est-elle prévue, ou une allocation ?
6. **Numéro sur l'enveloppe** : `LISTE DOCUMENT CONTRATUEL.pdf:1` fait inscrire « Soumission
   HR25-03 » alors que l'appel d'offres est HR26-14. Lequel retenir ?
7. **Sous-catégorie RBQ** exigée pour le soumissionnaire principal : aucune n'est nommée.
8. **Fenêtre de coupure** : compte tenu de la restriction au 1ᵉʳ mai – 15 septembre, quel
   séquencement des 4 bâtiments est attendu sur les deux étés disponibles ?

### 6.3 Ce qu'il faut monter au dossier de soumission

- Formulaire de soumission signé **avec la ventilation des coûts** (12 cellules électriques)
- Résolution d'autorisation de signature, certifiée conforme
- Attestation de Revenu Québec **délivrée avant** le 14 octobre 2026 13 h 30
- Attestations de probité, d'intégrité, déclaration de lobbyisme
- **Garantie de soumission émise contre le 14 octobre 2026** — 10 % en cautionnement (Annexe 5)
  ou 5 % en chèque visé / mandat / traite / LGI (Annexe 6), valide 45 jours
- Mention explicite de la **prise de connaissance de l'Addenda 01**, sans quoi la soumission
  « pourrait être rejetée » (`Addenda 01.pdf:1`)
- Toute demande d'équivalence, **avec la soumission**, chiffrée **en crédit**

Rappel : le retard, l'absence du formulaire signé, une soumission conditionnelle et l'absence de
garantie conforme sont des motifs de **rejet automatique** (`LCV…:15`). Tout le reste est
corrigible après coup, sans modifier le montant (`LCV…:16`).

### 6.4 À vérifier avant de chiffrer

- Prendre rendez-vous pour la **visite des lieux** même si elle est facultative : « Aucune
  information particulière ne peut être obtenue autrement » (`Appeloffres.pdf:1`), et la
  responsabilité de connaître l'état des lieux est entièrement transférée (`LCV…:11`).
- Relever sur place les **pénétrations existantes** de chaque salle électrique.
- Évaluer l'**état des conducteurs d'aluminium** dans un échantillon de logements.
- Vérifier la **capacité de cautionnement** : 50 % + 50 % du montant du contrat avant signature,
  avec réémission à chaque tranche de +10 % d'avenants.
- Confronter la **cadence de 5 jours par cuisine** à la capacité réelle des équipes — c'est la
  seule clause dont le dépassement coûte sans plafond.

---

## Méthode et limites de cette analyse

**Ce qui a été fait** : les 24 PDF ont été copiés depuis `Downloads` puis hachés ; les 24 hashes
de la copie ont été comparés aux originaux et sont identiques. La source n'a jamais été modifiée.
Le texte a été extrait avec pymupdf ; `Addenda 01.pdf`, scanné, a été lu par rendu d'image. La
comparaison base/addenda a été faite par hash, par nombre de pages, par diff de texte page à page
et par comparaison de pixels avec recherche de décalage.

**Ce qui n'a pas été fait** :
- Aucun relevé de quantités (métré) n'a été produit. Cette analyse ne chiffre rien.
- Les feuilles de plans ont été lues par leur **texte** ; les symboles, les cédules de panneaux et
  les tracés n'ont pas été dépouillés graphiquement.
- Les plans d'architecture (lots A à D, 173 pages) et de structure n'ont pas été analysés au-delà
  de la comparaison base/addenda.
- Les divisions 02 à 10 du devis d'architecture n'ont été parcourues que pour ce qui touche
  l'électricien.

**Sur la fiabilité des citations** : chaque affirmation porte sa source. Les numéros de page sont
ceux du **PDF**, qui ne coïncident pas toujours avec la pagination imprimée — notamment dans
`Formulaire soumission.pdf` (pages imprimées 18 à 31 pour les pages PDF 1 à 14) et dans le devis,
repaginé à 1 à chaque section.
