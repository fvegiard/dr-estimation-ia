# S-1808 : écart entre le relevé automatique (v2) et le relevé de l'estimateur

Vérification indépendante faite le 2026-09-22.

**Sources comparées**
- **Relevé IA** : `S-1808-Rapport-de-metre.md`, 826 marques (passe v2 de 03:24).
- **Référence** : `reference/relevé final Daniel.pdf`, 7 pages. C'est un export ACCEO « Relevé matériel » avec prix et heures. `relevé matériaux.pdf` (4 pages) en est un sous-ensemble « demande de prix » aux quantités identiques.
- **Transcription** : `reference-quantites.csv`, 236 lignes, aucune illisible.

**Nature de la référence.** Elle est **globale** : aucune ventilation par feuille ni par zone. Les écarts par feuille ne peuvent donc être tranchés qu'en regardant le plan marque par marque.

**Méthode de preuve**
- Les coordonnées sont en points PDF de la feuille.
- Les images de `travail/ecart-preuves/` sont rendues depuis le PDF vectoriel (`travail/feuilles/<F>.pdf`), avec les marques IA en rouge.
- Pour les écarts de symboles sans étiquette texte, les objets ont été recherchés par **signature vectorielle** (calque et géométrie du chemin, avec pymupdf) puis confirmés à l'œil.

## 1. Transcription

Voir `reference-quantites.csv` (colonnes : fichier, page_pdf, section, objet, quantité, um, feuille_zone).

- Page 1 : sommaire. Matériel 184 933,73 $, service 126 720 $, grand total 311 653,75 $, 1 280 h chargées contre 1 272,6 h au relevé. Annotations manuscrites « $ 99.00 » et « TEMPORAIRE = ».
- Pages 2 à 7 : sections DISTRIBUTION, ÉCLAIRAGE, CHAUFFAGE, ALARME INCENDIE, SERVICE et CONTROL ÉCLAIRAGE.
- La section CONTROL ÉCLAIRAGE (0 $, 0 h) reprend les commandes déjà comptées dans ÉCLAIRAGE. On l'a prise comme quantité de référence (15 / 33 / 43 / 33 / 11) **une seule fois**.
- Point à signaler à Daniel : ÉCLAIRAGE contient à la fois « GRADATEUR DETECT PR… 11 » et « DÉTECTEUR-GRADATEUR… 11 ». La main-d'œuvre des détecteurs-gradateurs semble comptée deux fois (11 × 0,35 h + 11 × 0,5 h).

## 2. Correspondance des nomenclatures

| Référence (ACCEO) | Libellé(s) IA | Justification |
|---|---|---|
| FIXTURE TYPE A, B, C, D, E, F, EX1, EX2, EX3 | Luminaire A … EX3 | Même désignation que la cédule E-032 |
| ENSEIGNE Z6/Z2/Z4, TÊTE Z3/Z5, BATTERIE Z1 | Urgence Z1 … Z6 | Étiquettes Zx du plan |
| INT BV / INTERRUPTEUR 2 SCÈNES (15) | Interrupteur BV 2 scènes (10) + Interrupteur simple (2) | La référence n'a pas de ligne « simple » : elle a regroupé les $ non gradués |
| GRADATEUR B/V / 2 SCÈNES AVEC GRADATION (33) | Interrupteur BV 2 scènes grad. (30) + Gradateur (8) | La référence n'a pas de ligne « gradateur » sans B.V. |
| DÉTECTEUR MOUVEMENT RCMS PIR (43) | Détecteur mouvement BV | Légende E-001 |
| RELAIS RPP20 (33) | Relais nLight RE | Légende E-001 |
| DÉTECTEUR-GRADATEUR WSX PDT (11) | Détecteur-gradateur mural | Légende E-001 |
| PANNEAU ALARME / ANNONCIATEUR / STATION / FUMÉE / FUMÉE C/O / THERMIQUE / RELAI ADRESSABLE / ISOLATEUR / GAINE / GSM | PAI / Annonciateur / Station manuelle / Détecteur de fumée / Avertisseur fumée/CO / Détecteur thermique / Module RA / Module isolateur MI / Détecteur fumée de gaine / Transmetteur GSM | 1 pour 1 |
| KLAXON (14) + KLAXON WP EXTÉRIEUR (2) | Klaxon (16) | L'IA a regroupé intérieur et extérieur |
| KLAXON STROB (4) | Piézo-stroboscope (4) | Légende « piezo combiné à un strobe » |
| prise duplex 20 A GFI (27) + PRISE AU TOIT (1) | Prise double DDFT 3 + Prise comptoir DDFT 15 + Prise extérieure E.I 8 + Prise service toiture 1 + à confirmer 1 | Toutes DDFT |
| prise duplex 15 A (64) + 15/20 A (29) | Prise double 87 + Prise comptoir 6 | L'IA ne sépare pas les calibres (réserve R-008) |
| PRISE SÉCHEUSE (1) | Prise spéciale (2 : sécheuse + lave-vaisselle) | |
| PRISE POÊLE (1) | Raccordement cuisinière (1) | |
| tel/data (6) | Sortie informatique (6) | |
| SCR ×6 puissances (30), OFM ×4 (9), OAC (2), OWC-M (2), T1 INTÉGRÉ (8), RELAIS TRIAC (33) | Convecteur SCR, Plinthe OFM, Aéroconvecteur OAC, Câble chauffant OWC-M, Thermostat intégré TI, Relais triac RT | L'IA ne sépare pas les puissances (R-031) |
| THERMOSTAT FDP (10) | Thermostat AC fourni par autres (20) | Même objet : « T » + « FPD » au plan |
| A/C UNIT (21) | Raccordement AC 20 + AC à confirmer 1 | |
| VENTILATEUR (7) | Raccordement ventilateur VE 5 + VA-01 1 + EVP-01 1 | Hypothèse : 7 ventilateurs en cédule E-031 |
| SERPENTIN, CHAUFFE-EAU, ÉCHANGEUR, HUMIDIFICATEUR, POMPE, CONDENSEUR, MOTEUR ASCENSEUR | Raccordement SE / chauffe-eau / échangeur / humidificateur / pompe / condenseur / ascenseur | 1 pour 1 |
| SECTIONNEUR 400A, PANN PS, PSS1, PSS2, PANN 125A, TRANSFO, CONTACTEUR ×2, ABB BJT (embase) | Sectionneur principal 400 A, Panneau de distribution ×4, Transformateur TX1, Contacteur ×2, Embase HQ | Unifilaire E-010 |
| INTERR 30A 3P 600V CEMA3 (6) | Sectionneur E.I toiture 3 + Sectionneur à fusibles VA-01 1 + Sectionneur lumière ascenseur 1 = 5 | Correspondance **incertaine** : les 6 pourraient être SE ×4 + HUM ×2 (600 V) |
| ARMOIRE POUR APPAREILS (1) | — | Aucun équivalent IA : indécidable (objet hors plan ?) |

**Hors périmètre** : présent dans la référence, non relevable par l'IA.
- Prix de lot (distribution, transfo, D/M, étude, éclairage, contrôle, urgence, chauffage ×2).
- Tous les câbles (250MCM 1 120 pi, 3/0 400 pi, etc.) et les conduits (TME, CPV, flex, « conduit 3/4 03c12 »…).
- Les accessoires : boîtes, couvercles, connecteurs, Panduit, alimentation 0-10 V 270, drops de chauffage 53.
- Les lignes de panneau à 0, la NEMA 2 à 0 et la tige MALT.
- Plywood : 6 feuilles 4×8 contre « Contreplaqué télécom » compté 1 fois par l'IA. Unités différentes, non comparable.

**Relevé par l'IA seulement** : absent de la référence, exclu de l'écart.
- 12 marques d'alarme : MTA 1, RFL 3, Module I 2, Symbole puits 1, Hotte H-1 alarme 1, Volets coupe-feu 4.
- Mécanique : contrôleur d'ascenseur 1, four combi 1, boîte de dérivation VRF 2, démarreur de hotte fourni par autres 1.
- Distribution : boîte de tirage 1, MALT 2, barre de MALT 1, point de raccordement HQ 1, colonne de l'îlot 1, démarreur combiné 1.
- Commandes : minuterie 1, sélecteur 1, interrupteur de puits 1.
- Télécom : contrôle d'accès 8, conduits 2.
- Chauffage : thermostat plancher chauffant 2. La référence les inclut dans « OWC-M C/A TH ET SONDE ».

## 3. Écart par famille (objets communs seulement)

Signe : IA − référence.

| Famille | Réf. | IA | Écart | Écart % | Explication (détail en §4) |
|---|--:|--:|--:|--:|---|
| Luminaires | 224 | 224 | 0 | 0,0 % | Total juste. Mais C 33 contre 45 (−12) et D 16 contre 4 (+12) : 12 « TYPE D » d'E-101 reclassés en C par l'estimateur |
| Commandes (interr., détecteurs, relais) | 135 | 134 | −1 | −0,7 % | Détecteur-gradateur −3 (IA en tort) ; interrupteurs +2 (2 $ simples) ; 5 répartis autrement entre « 2 scènes » et « grad. » |
| Secours | 46 | 47 | +1 | +2,2 % | Z5 : 2 contre 1, l'IA a raison |
| Alarme incendie | 91 | 90 | −1 | −1,1 % | Thermique 29 contre 30, l'IA a tort ; klaxons 16 = 16 |
| Prises | 122 | 123 | +1 | +0,8 % | Prise spéciale 2 contre sécheuse 1 (lave-vaisselle) : indécidable. DDFT + toit : 28 = 28 |
| Télécom / data | 6 | 6 | 0 | 0,0 % | |
| Distribution / panneaux / sectionneurs | 16 | 14 | −2 | −12,5 % | Sectionneurs 30 A : 5 contre 6 (correspondance incertaine) ; armoire 0 contre 1 |
| Chauffage | 94 | 104 | +10 | +10,6 % | Tout est exact sauf « thermostat FDP » : 20 contre 10 |
| Mécanique (raccordements) | 43 | 44 | +1 | +2,3 % | Pompe 2 contre 1 : l'IA a raison (P-01 sur E200, P-02 sur E201) |
| **Total commun** | **777** | **786** | **+9** | **+1,2 %** | Somme des écarts absolus par famille : 17 (2,2 %). Par type : ≈ 55 (7 %) |

**Par feuille.** La référence n'est pas ventilée par feuille. Voici la répartition IA des familles dont l'écart n'est pas nul, pour localiser chaque écart.

| Famille / objet | E100 | E101 | E200 | E201 | E202 / autres | Écart localisé |
|---|--:|--:|--:|--:|--:|---|
| Luminaire C / D | 15 / 2 | 18 / 14 | — | — | — | E101 : 12 « TYPE D » hors salles méc. et élec. |
| Détecteur-gradateur | 4 | 4 | — | — | — | E100 : −2 ; E101 : −1 |
| Interrupteurs (tous) | 20 | 30 | — | — | E040 : 1 | E100 : 2 simples |
| Z5 | 1 | 1 | — | — | — | Réf. 1 |
| Thermique | 17 | 12 | — | — | — | E100 : −1 |
| Thermostat FPD | — | — | 11 | 9 | — | Réf. 10 |
| Pompe | — | — | 1 | 1 | — | Réf. 1 |
| Sectionneurs 30 A | — | — | — | 1 | E202 : 3 ; E041 : 1 | Réf. 6 |

## 4. Écarts tranchés un par un

| # | Écart | Qui a raison | Preuve |
|---|---|---|---|
| 1 | Luminaire C −12 / D +12 | **Indécidable sur plan ; en pratique, la référence.** L'IA a suivi l'étiquette, ce qui se défend, et l'a signalé (R-025) | E101, toilettes 209 et WC autour de (1100–1185, 415–613), (823–870, 268–719) : le texte dit « TYPE D » sous un **encastré rond** identique aux « TYPE C » de la toilette 207 (1096–1164, 947–1112). Or la cédule E-032 décrit D comme une réglette CLX L48 en surface. L'estimateur a pris le symbole, l'IA l'étiquette. Voir `ecart-preuves/E101-C-vs-D-cote-a-cote.png` |
| 2 | Détecteur-gradateur 8 contre 11 | **Référence** : 3 manques IA **non signalés** | Symbole « œil » trouvé par signature vectorielle (calque E-P-ECL, 2 courbes de 6,5 × 21,7 pt) : 10 occurrences + 1 oblique = 11. Non relevés : E100 (1027,875), E100 (857,906), E101 (820,519). La marque IA E100 (1008,1210) est juste. Voir `ecart-preuves/detecteur-gradateur-3-manques.png` |
| 3 | Thermostat FDP 20 contre 10 | **IA conforme au plan** : 20 couples « T » + « FPD » (11 sur E200, 9 sur E201, coordonnées dans occurrences-texte.csv). La référence en compte 10, sans explication visible : à demander à Daniel | Mots du PDF vectoriel E200 et E201. Le seul autre « T » isolé, sur E201 (543,973), est le TX1 112,5 kVA : `ecart-preuves/E201-T-est-TX1-verif.png` |
| 4 | Interrupteurs : « 2 scènes » 10 contre 15, « grad. » 38 (30 + 8) contre 33, simples +2 | **Mixte** | Les 2 $ simples existent bien (E100 (1010,1390) salle électrique et (1108,1112) dépôt 106) : `ecart-preuves/E100-int-simples.png`. La référence n'a pas de ligne « simple » et les a probablement mis dans ses 15. Les 8 « Gradateur » d'E101 sont bien des $ à barre sans B.V. (toilettes 207 : `E101-toilettes207-commandes.png`). Qui a la bonne répartition 2S / grad. pour les 5 restants : indécidable sans le relevé annoté de l'estimateur (R-004 le signale) |
| 5 | Détecteur thermique 29 contre 30 | **Référence** : 1 manque IA non signalé | E100 (853,1367), bureau DA 102 : cercle barré sur le calque E-P-ALA-EQP sans marque IA. Deux marques IA sont décalées de 30 à 40 pt de leur symbole (E100 (798,329) → (829,329) ; (1112,990) → (1113,1030)) mais sont justes. Voir `E100-thermiques.png` |
| 6 | Z5 2 contre 1 | **IA** | E100 (1271,372) et E101 (827,200) : deux doubles têtes E.I distinctes sur deux niveaux. Voir `Z5-deux-marques.png` |
| 7 | Pompe 2 contre 1 | **IA** | P-01 sur E200 (859,1060) (visible dans `echantillon-seed1808.png`, n° 4) et P-02 sur E201 (601,810) ; les deux sont à la cédule E-031 |
| 8 | Sectionneurs 30 A 5 contre 6 ; armoire 0 contre 1 | **Indécidable** | La correspondance entre objets est incertaine (voir §2) |
| 9 | Prise spéciale 2 contre 1 | **Indécidable** | La référence n'a qu'une prise de sécheuse ; l'IA compte aussi le lave-vaisselle |
| — | Klaxons (total égal) | Répartition IA fausse | E100 (1260,409) est un K avec E.I (extérieur, visible dans `echantillon-seed1808.png`, n° 1). L'IA n'en déclare qu'un extérieur (R-027) alors qu'il y en a 2, comme dans la référence. Le doublon apparent E101 (685,496)/(682,510) correspond à 2 klaxons dos à dos : `E101-klaxons-685-500.png` |

**Échantillon aléatoire** (`random.seed(1808)`, `random.sample` sur les 826 marques) : 10 marques sur 10 correspondent à un objet réel. Voir `ecart-preuves/echantillon-seed1808.png`.
- Objets vérifiés : EX2 E051, Klaxon E100, Prise comptoir DDFT E201, RFL E020, Pompe E200, C E100, BV grad. E101, A E101, D E101, MALT E010.
- Deux réserves de classement : le n° 1 est un klaxon **extérieur** non qualifié comme tel, et le n° 8 est un « TYPE D » contesté (écart 1).

## 5. Verdict

- **Écart net sur les objets communs : +9 sur 777 (+1,2 %).** Le critère Francis de ≤ 5 % au total est **respecté**.
- **Critère Francis de ≤ 10 % par poste**
  - Respecté : luminaires 0 % (mais 24 objets mal typés C/D), commandes −0,7 %, secours +2,2 %, alarme −1,1 %, prises +0,8 %, télécom 0 %, mécanique +2,3 %.
  - Non respecté :
    - **Chauffage +10,6 %**, entièrement dû aux 10 thermostats FDP en désaccord (IA conforme au plan).
    - **Distribution −12,5 %**, sur une petite base (16), avec une correspondance incertaine.
- **Items manquants non signalés en réserve** : critère « aucun », **non respecté**.
  - 3 détecteurs-gradateurs muraux WSX : E100 (1027,875), E100 (857,906), E101 (820,519).
  - 1 détecteur thermique : E100 (853,1367).
  - Les autres écarts sont couverts par une réserve (R-004, R-006, R-008, R-025, R-027).
- **Verdict** : l'estimateur peut **utiliser ce relevé comme base de travail, mais pas tel quel**. Corrections à faire avant de s'en servir :
  1. Reclasser les 12 « TYPE D » d'E101 en C.
  2. Ajouter 3 détecteurs-gradateurs et 1 détecteur thermique.
  3. Séparer les prises 15 A / 20 A et les puissances SCR / OFM à partir des cédules.
  4. Qualifier 2 klaxons comme extérieurs.
  5. Trancher le nombre de thermostats FDP (10 ou 20).
  6. Métrer tout le linéaire : câbles et conduits représentent la plus grande part des heures de la référence.

### Erreurs systématiques de l'IA (règles à corriger dans la méthode)

1. **Symboles sans étiquette texte relevés « à l'œil »** : c'est la source des 4 manques non signalés. Règle : pour chaque symbole de légende, faire une recherche par **signature vectorielle** (calque + géométrie du chemin, en tolérant la rotation), puis comparer au compte visuel. Tout écart doit aller en réserve.
2. **L'étiquette l'emporte sur le symbole même quand elle contredit la cédule** (TYPE D posé sur un encastré rond). Règle : si le symbole n'est pas cohérent avec la forme de la cédule, compter selon le symbole et mettre en réserve, ou au minimum marquer « à confirmer » dans le rapport de métré, pas seulement dans les réserves.
3. **Sous-types regroupés** : prises 15 / 20 A, puissances SCR / OFM, klaxons extérieurs. Or l'estimateur chiffre par sous-type. Règle : lire le calibre ou la puissance à la cédule ou au circuit, et créer un libellé par sous-type.
4. **Marques visuelles décalées de 30 à 40 pt de leur symbole** : cela gêne le contrôle dans Plan Expert. Règle : recaler chaque marque sur le centre du chemin vectoriel.

## v1 → v2

Aucune comparaison v1 n'existe (pas d'`ecart.md`). On compare donc les totaux du relevé v1 (`archives/S-1808-v1/S-1808-Rapport-de-metre.md`, 780 marques) avec la v2 et la référence, selon la même correspondance.

| Famille | v1 | v2 | Réf. |
|---|--:|--:|--:|
| Luminaires | 224 | 224 | 224 |
| Commandes | 139 | 134 | 135 |
| Alarme | 67 | 90 | 91 |
| Prises | 124 | 123 | 122 |
| **Total commun (approx.)** | **≈ 765** | **786** | **777** |

- **Corrigé en v2**
  - Le schéma d'alarme E-020 n'était pas relevé en v1 (MI 18, gaine 3, ANN, GSM absents : alarme −26 %).
  - Les libellés SCR / OFM étaient inversés en v1 (« Plinthe SCR », « Convecteur OFM »).
  - Les raccordements mécaniques étaient génériques en v1 (« Raccord équip. méca. » 16, « à confirmer » 3). Ils sont maintenant identifiés un à un et concordent à ±1.
- **Régressions**
  - Détecteur-gradateur : **11 en v1 (juste) → 8 en v2**.
  - La v1 séparait les prises 15 A (64, exactement la référence) et 20 A ; la v2 les fusionne en « Prise double » 87.
- **Non corrigé** : C/D (33/16 dans les deux passes) et thermique 29 dans les deux passes.
