# Écart relevé automatique ↔ relevé de Daniel — S-1714 (Le Vallem – Riviera, Carignan, 2 tours, 140 logements)

Vérificateur indépendant, 2026-09-22. Référence : `reference/relevé de Daniel.pdf` (12 pages, export ACCEO « Relevé matériel RAPPORT 2026 » + 1 feuille manuscrite Wesco + sommaire). Tout est lisible, rien d'illisible. Transcription complète : `reference-quantites.csv` (307 lignes, avec la page du scan).
Relevé IA : `S-1714-Rapport-de-metre.md` + `travail/occurrences-*.csv` (7 385 marques). Preuves : `travail/ecart-preuves/`.

**La référence est complète** (toutes les sections : distribution, éclairage, chauffage, alarme, génératrice, urgence, logement, service, télécom, caméra, lecteur de carte). En revanche, **elle est par section, pas par feuille** : une comparaison par feuille n'est donc possible que contre un recomptage indépendant (vectoriel), pas contre Daniel.

## 0. Unités types et multiplicateurs : contrôle

- Chaque étage est dessiné sur sa propre feuille (cartouches « PLAN DU 2E » … « PLAN DU 8E » sur E202–E208 et E302–E308). Il n'y a pas de plan type avec multiplicateur, donc **aucun multiplicateur à appliquer**.
- Logements par feuille selon l'IA (panneaux = cuisinières = sécheuses sur chaque feuille) : E201 18, E202–E206 21 chacune, E207 11, E208 6, **total 140**. La référence a elle aussi 140 panneaux de logement (types 1.1 : 55, 2.1 : 8, 2.3 : 1, 3.1 : 5, 4 : 2, 1.2 : 11, 2.2 : 53, 3.2 : 4, 2.4 : 1 ; p. 4). Les totaux concordent.
- **Incohérence dans la référence** : plusieurs lignes « par logement » valent 142 (poêle, sécheuse, TV, hotte, évaporateur, condenseur, boîtier 3000, boîtier interr. 30 A ; p. 9), alors que la même référence compte 140 panneaux. L'IA trouve 140 au plan, feuille par feuille. Ces écarts de −2 sont classés « IA probable » plus bas.
- Doublons internes de la référence, **neutralisés** : les plinthes, les aéroconvecteurs et les 398 thermostats apparaissent deux fois, en CHAUFFAGE (fourniture, p. 7) et en LOGEMENT (main-d'œuvre, p. 9–10). Ils ne sont comptés qu'une fois. Contrôle : « drop de chauffage 984 » = 586 appareils de logement + 398 thermostats.

## 1. Correspondance des nomenclatures

| Référence (ligne, page) | Libellé(s) IA | Justification |
|---|---|---|
| STRIP 214 + PLAFONNIER 207 + APPLIQUE MURAL EXT 10 (p. 6) | Luminaire — à classer 325 + Luminaire encastré urgence 94 + Luminaire linéaire applique urgence 48 | Luminaires des communs. Le tableau des luminaires de E101 est « À VENIR », donc les types ne sont pas comparables un à un. |
| APPLIQUE MURAL BALCON 140 (p. 6) | — | Non dessinée (voir § hors plan). |
| ENSEIGNE SORTIE 72 (p. 9) | Enseigne sortie 33 | Même objet. |
| STATION MANUEL 37 / DÉTECTEUR FUMÉ 105 / GAINE 34 / FUMÉ ET MON 1 / KLAXON 50 / KLAXON STROB 362 / PANN INX 14 / RELAIS 31 / MODULE 28 / DÉBIT 17 / VANNE 22 (p. 7–8) | DM 36 / DF 106 / DF2 33 / DF3 1 / Klaxon 52 / Klaxon-strobe 362 / INX 14 / R 31 / MA 27 / DD 17 / DV 22 | Correspondance directe, légende E100. |
| DETECTEUR FUMÉ/MONOX 387 (logement, p. 9) | Avertisseur de fumée 336 + Avertisseur fumée/CO 52 | AF + AF1, dans les logements. |
| PANNEAU ALARME 1, ANNONCIATEUR 1, COMMUNICATEUR 1 | — | Non relevés par l'IA (réserve R-014). |
| PRISE 15A 125V 2166 + GFI 344 + prise duplex service 35 | Prise double 1616 + comptoir 278 + salle de bain 179 + laveuse 140 + réfrigérateur 140 + micro-ondes 140 | Le partage 15A/GFI de Daniel est inconnu : comparaison au niveau du groupe « prises 120 V standard ». Les 35 prises de service correspondent aux 35 « Prise double » de E200. |
| PRISE CONTROLE 588 | Prise demi-commandée 586 | Direct. |
| PRISE GFI WP 156 | Prise étanche 163 | Direct. |
| PRISE POELE 142 / SÉCHEUSE 142 | Prise cuisinière 140 / sécheuse 140 | Direct. |
| SORTIE TEL 196 / SORTIE TV 142 | Sortie informatique 55 + Sortie câblo/informatique 140 (= 195 « tel ») / câblo 140 (= « TV ») | Le boîtier câblo/info porte une sortie TV et une sortie tel. |
| Panneaux communs PP1, S, S1-1, S2-1, UE, UE1-1, UE2-1, UNE, UNE1, UNE2, UE1.2, UE2.2, PP2, PP3, S1.2, S2.2, PC = 17 (p. 3–5) | Panneau de distribution 17 | Liste identique (notes des marques E200/E207/E208). |
| PANN TYPE x.x = 140 | Panneau de logement 140 | Même total, mais l'IA ne type pas les panneaux (9 types chez Daniel). |
| TRANSFO 250/200/45/30 kVA = 9 | Transformateur 11 | T1–T9 sur E200, plus 2 marques E101 (voir écart). |
| SECTIONNEUR 400A 1 + 100A 2 | Sectionneur SN1–SN3 (E200) | Direct. |
| BOITIER INTERR 30A 142 + 7 (p. 9, 11) | Sectionneur de condenseur 145 | Sectionneurs d'équipement. |
| CENTRE DE COMPTEUR 1+2+1+2 = 6 ; TRANSFERT SWITCH 2 ; GÉNÉRATRICE 1 | Équipement salle électrique — à classer 11 (6 bancs de compteurs CA/BC/AB, ST1, ST2, génératrice, embase HQ, panneau PC) | Regroupement par note de marque. |
| BOITE DE RACCORD 1200A 6 | — | Non relevée (réserve R-019, unifilaire). |
| Plinthes B300 157+2 (347 V), B500 26, B1000 203+30 (347 V), B1250 46, B1500 6 | Plinthe 300W 159, 500W 26, 1000W 232, 1250W 47, 1500W 6 | Tensions confondues. |
| RWF 1000/1250/1500/2000 = 14/25/71/38 ; WFA4000W 347V 2 | Aéroconvecteur 1000/1250/1500/2000W = 14/25/71/38 ; Aéroconvecteur commun 2 | Exact. |
| CHAUFFAGE 120V GAS 2 (service) | Aérotherme 2 (AG-1a/b) | Aérothermes au gaz 120 V. Hypothèse raisonnable. |
| THERMOSTAT 398 | Thermostat 398 | Exact. |
| VENTILATEUR 35 (logement) + VENTILATEUR 120V 22 (service) | Raccordement ventilateur 40 (E201–E208) + 22 (E200, bulles V-x) | Direct. |
| EVAPORATEUR 142 ; CONDENSEUR 142 + CODENSEUR 3 ; HOTTE 142 | Évaporateur 147 ; Condenseur 145 ; Raccordement hotte 140 | Direct (la hotte est rangée en mécanique pour la comparaison). |
| POMPE 3PH 6 ; PANN POMPE 2 | Équip. mécanique : pompes P-1a, P-1b, P-2a, P-2b, P-3, P-4 = 6 ; panneaux de contrôle de pompe 4 | Selon les notes des marques. |

**IA seulement, pas de ligne chez Daniel** (hors comparaison) : Raccordement lave-vaisselle 140, Résistance fin de ligne 56, Volet motorisé 14, bouilloires B-1a/b 2, AF-1/AF-2/serpentins/EA-1 5, lignes de cédule E101 11 (ascenseurs, cabines, consoles, porte de garage, AE-X, intercom, téléphonie, câblo), embase HQ 1.
**Hors périmètre** (Daniel les compte, l'IA ne relève pas ce type d'item) : câbles et conduits (tout ARTERE PANN, conduits TME/HQ/vides, 12AWG 35 000 pi, 16AWG alarme…), boîtes et couvercles, quincaillerie, plywood, socle TSS, prix de lot (distribution 177 330,80 $, transfo 46 538,05 $, fixtures 19 813 $, chauffage 59 920,77 $, alarme 81 000 $), drop de chauffage 984, « alimentation éclairage » 72, feuille Wesco (branchement HQ/Bell, 95 986,43 $), caméra (50 boîtes) et lecteur de carte (7 portes) « si requis au plan » (seulement en légende E100, rien au plan), conduits vides des 20 bornes (note DCC de E200).
**Allocations de Daniel sans objet dessiné** (voir § 5) : SORTIE ECL 3000, INT 1 VOIE 2000, INT 3 VOIE 600, APPLIQUE MURAL BALCON 140, BOITIER 3000 142.

## 2. Tableau d'écart par famille (objets dessinés et communs)

| Famille | Référence | IA | Écart | Écart % | Explication |
|---|--:|--:|--:|--:|---|
| Luminaires (communs) | 431 | 467 | +36 | +8,4 % | 39 enseignes comptées à tort comme « Luminaire — à classer » (E300, E301, E308). Sans elles : 428, soit −3 (−0,7 %). |
| Commandes / interrupteurs / détecteurs | 0 dessiné | 0 | 0 | — | Aucun interrupteur au plan. Les 2 600 de Daniel sont une allocation (§ 5). |
| Secours (enseignes) | 72 | 33 | **−39** | **−54,2 %** | Enseignes de E300 (19), E301 (17) et E308 (3) non relevées comme telles. Recomptage vectoriel : 72. |
| Alarme incendie | 1 091 | 1 089 | −2 | −0,2 % | Panneau, annonciateur et communicateur (3) non relevés (R-014). Klaxon +2, DM −1, DF +1, DF2 −1, MA −1, avertisseurs +1. |
| Prises | 3 573 | 3 522 | −51 | −1,4 % | Prises standard −52 (regroupement de Daniel inconnu), étanches +7, commandées −2, poêle −2, sécheuse −2. |
| Télécom / data | 338 | 335 | −3 | −0,9 % | Tel 195 contre 196, TV 140 contre 142. |
| Distribution / panneaux / sectionneurs | 333 | 327 | −6 | −1,8 % | Boîtes de raccord 1200 A −6 (R-019), sectionneurs 30 A −4, transfos +2 (erreur IA), embase HQ et panneau PC en double (+2). |
| Mécanique | 494 | 504 | +10 | +2,0 % | Évaporateurs +5, ventilateurs +5, panneaux de pompe +2, hottes −2. |
| Chauffage | 1 020 | 1 020 | 0 | 0 % | Plinthes 1000W −1 et 1250W +1 ; tout le reste est exact. |
| **Total objets communs** | **7 352** | **7 297** | **−55** | **−0,75 %** | Somme des écarts absolus par famille : 147 (2,0 %). |

### 2b. Par feuille, familles avec écart ≠ 0

Daniel ne ventile pas par feuille. La colonne « contrôle » est un recomptage vectoriel indépendant dans `01-PLANS.pdf` : symbole cercle de 7 à 11 pt contenant un X, script `travail/ecart-preuves/ens.py`, positions dans `ens.json`. Ce recomptage **donne exactement 72, comme Daniel**.

| Feuille | Enseignes IA | Enseignes contrôle | Luminaires IA | dont enseignes absorbées |
|---|--:|--:|--:|--:|
| E300 sous-sol | 0 | 19 | 187 | 19 |
| E301 RDC | 0 | 17 | 119 | 17 |
| E302–E306 (chacune) | 6 | 6 | 25 | 0 |
| E307 | 3 | 3 | 21 | 0 |
| E308 | 0 | 3 | 15 | 3 |
| **Total** | **33** | **72** | **467** | **39** |

Autres familles avec écart (IA par feuille ; la référence n'a qu'un total) :

| Libellé IA | E200 | E201 | E202 | E203–E206 | E207 | E208 | E101 | E400 | E401–E408 | Total IA | Réf |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Transformateur | 9 | | | | | | 2 | | | 11 | 9 |
| Évaporateur | | 25 | 21 | 21 ×4 | 11 | 6 | | | | 147 | 142 |
| Ventilateur | 22 | 8 | 4 | 5 ×4 | 2 | 6 | | | | 62 | 57 |
| Prise étanche | | 25 | 23 | 23,23,23,22 | 15 | 8 | | | (E209 : 1) | 163 | 156 |
| Klaxon | | | | | | | | 29 | 7,3,2,2,2,2,3,2 | 52 | 50 |

## 3. Écarts ≥ 2 objets : qui a raison

| # | Écart | Verdict | Preuve |
|---|---|---|---|
| 1 | Enseignes 33 contre 72 (−39) | **Référence** | Recomptage vectoriel E300 19 / E301 17 / E302–E306 6 chacune / E307 3 / E308 3 = 72. Sur E302–E307, les 33 de l'IA tombent exactement aux mêmes positions. `ecart-preuves/E300-enseigne-garage.png` (enseigne à pt 1228,914 marquée « Luminaire — à classer » via l'étiquette UE2.1-7), `E301-enseigne-classee-luminaire.png` (pt ≈2241,917, UE2.1-17), `E308-enseignes-non-relevees.png` (pt 2060–2204, 913–922). |
| 2 | Luminaires 467 contre 431 (+36) | **Référence** (le surplus, ce sont les 39 enseignes) ; −3 résiduel : indécidable | Chacune des 39 enseignes a une marque « à classer » à moins de 25 pt (19/19, 17/17, 3/3). Règle de l'IA : « une marque par étiquette de circuit » (R-010). |
| 3 | Prises standard −52 | Indécidable | Le regroupement 15A/GFI de Daniel est inconnu. S'il a inclus les 140 prises d'échangeur d'air (note E201–E208) ou les 140 lave-vaisselle dans « 15A », l'écart réel est de ±90 dans un sens ou dans l'autre. Échantillon : les prises 15, 21 et 21j vérifiées sont correctes (§ 4). |
| 4 | Prise étanche +7 | Indécidable | Classement visuel intérieur/étanche des prises du circuit 23 « à l'œil » (R-003). Pas de recomptage fait. |
| 5 | Poêle, sécheuse, hotte, TV : 140 contre 142 (−2 chacun) | **IA probable** | 140 par feuille cumulées = 140 panneaux, et la référence compte elle-même 140 panneaux (p. 4). Les 142 ne s'expliquent pas. |
| 6 | Prise commandée −2 | Indécidable | < 0,5 %. |
| 7 | Transformateurs 11 contre 9 (+2) | **Référence** | Les 2 marques E101 sont des « TRANSFO 120V/24V (CO/TI) » de contrôle, lus dans la cédule UNE1-8 et UNE2-2. Ce ne sont pas des transformateurs de puissance. `E101-transfo-CO-TI.png` (pt 3175, 861 et 1020). |
| 8 | Distribution : panneau PC compté 2 fois, embase HQ | **Référence** | Le panneau PC est marqué sur E200 (pt 2075,784) **et** sur E101 (pt 1113,874, « À CONFIRMER »). C'est le même panneau. |
| 9 | Boîtes de raccord 1200 A −6 | Référence (manque de l'IA, **signalé** R-019) | Unifilaire E102 non compté article par article. |
| 10 | Sectionneurs 30 A 145 contre 149 (−4) | Indécidable | L'IA en met un par condenseur (145 = total des condenseurs de la référence). Daniel en compte 142 + 7. |
| 11 | Évaporateurs 147 contre 142 (+5) | **IA probable** | Étiquettes vectorielles « EV-x » (21 sur E201 pour 18 logements) et 4 « EVG » dans les communs. `E201-EVG-communs.png` (EVG-1.5 gym, EVG-2.5 lounge/résidentiel). La note climatisation exige le raccordement de chaque évaporateur. |
| 12 | Ventilateurs de logement 40 contre 35 (+5) | Indécidable (penche IA) | Sur E208, 6 marques sur 6 correspondent à une boîte « V » réelle : `E208-ventilateurs-V.png`. Pas de recomptage des autres feuilles. |
| 13 | Klaxons 52 contre 50 (+2) | Indécidable | E400 pt 1950/1962,749 : 2 « K » encadrés réels (3.1 et 3.2), `E400-klaxon-doublon.png`. 59 « K » bruts, 7 exclus comme mobilier. |
| 14 | Panneaux de pompe 4 contre 2 (+2) | Indécidable | Notes IA « raccordé par électricien — à confirmer » (E200, 3 simplex et 1 duplex). |
| 15 | Panneau d'alarme, annonciateur, communicateur (−3) | Référence (manque de l'IA, **signalé** R-014) | — |

## 4. Échantillon aléatoire (seed 1714, 10 marques sur 7 385) : 10 correctes sur 10

Montage : `ecart-preuves/echantillon-seed1714.png` (raster 5694 px, ±110 px autour de chaque marque).

| # | Feuille | Libellé IA | pt | Vu au raster | OK |
|--:|---|---|---|---|---|
| 1 | E200 | Transformateur | 1600.9,1921.2 | boîte « T9 » en salle électrique | oui |
| 2 | E207 | Raccordement lave-vaisselle | 2426.3,1037.9 | boîte « LV » circuit 9 | oui |
| 3 | E200 | Prise double | 2176.3,1304.4 | prise S2.1-15 sur colonne | oui |
| 4 | E201 | Prise salle de bain | 1691.8,1832.1 | prise « 15 » près du lavabo | oui |
| 5 | E404 | Module adressable | 2151.5,907.8 | « MA » encadré 22.6 | oui |
| 6 | E205 | Raccordement lave-vaisselle | 2126.5,990.8 | boîte « LV » | oui |
| 7 | E206 | Prise double | 2359.3,1062.4 | prise « 21 » | oui |
| 8 | E201 | Sortie câblo/informatique | 2312,1102 | boîtier cercle+triangle | oui |
| 9 | E206 | Thermostat | 2626.5,1075.3 | « T » cerclé | oui |
| 10 | E208 | Prise demi-commandée | 2681.3,754.6 | prise « 21j » | oui |

Aucune fausse marque dans l'échantillon. Les erreurs de l'IA sont des erreurs de **classement** (enseigne → luminaire, transfo de contrôle → transfo) et d'**omission** (notes), pas des marques inventées.

## 5. Items manquants NON signalés en réserve par l'IA (critère : aucun) : 4, critère échoué

| Item | Qté attendue | Source | Réserve IA ? |
|---|--:|---|---|
| Enseignes de sortie E300/E301/E308 | 39 | plans E300, E301, E308 (vectoriel) | Non. R-010 les noie dans « luminaires à classer » ; R-011 ne parle que de E302–E307. |
| Prise 5-15R dédiée à l'échangeur d'air, une par logement | 140 | note « ÉCHANGEUR D'AIR » sur E201–E208 | Non. Note ignorée. |
| Éclairage et interrupteurs des logements, appliques de balcon : non dessinés (Daniel alloue 3 000 sorties, 2 000 interrupteurs 1 voie, 600 interrupteurs 3 voies, 140 appliques de balcon) | allocation | E302–E308 : rien dans les logements (`E303-logement-sans-eclairage.png`) | Non. R-012 ne parle que des corridors. L'absence n'est pas déclarée. |
| 20 conduits vides pour les bornes (DCC) | 20 | note E200 « PRÉVOIR 10 CONDUITS VIDES POUR LES DCC BOX » ×2 | Non. Le « 10 » a été exclu comme faux positif, sans réserve (hors périmètre comptage, mais l'item existe). |

Signalés, donc acceptables : panneau d'alarme, annonciateur et GSM (R-014) ; unifilaire, boîtes de raccord et génératrice (R-019) ; branchement HQ (R-021) ; types de luminaires (R-010).

## 6. Verdict

- **Écart net sur les objets communs dessinés : −55 sur 7 352 (−0,75 %)**. Somme des écarts absolus : 147 (2,0 %). **Critère total ≤ 5 % : OK.**
- **Par poste (≤ 10 %)** : chauffage 0 %, alarme −0,2 %, télécom −0,9 %, prises −1,4 %, distribution −1,8 %, mécanique +2,0 %, luminaires +8,4 % (OK en apparence, mais seulement parce que les enseignes sont comptées dedans), **secours −54,2 % : ÉCHEC**.
- **Items manquants non signalés : 4 : ÉCHEC** (critère : aucun).
- **Utilisable tel quel ? Non, mais proche.** Les comptes des logements (prises, chauffage, alarme, télécom, panneaux, mécanique) sont à ±2 % de Daniel, sans marque fausse dans l'échantillon. Un estimateur peut les reprendre directement. Avant de soumettre, il faut 4 corrections :
  1. Reclasser les 39 enseignes de E300, E301 et E308 (et les retirer des luminaires).
  2. Retirer les 2 transfos 120/24 V et le panneau PC compté en double.
  3. Ajouter les 140 prises d'échangeur d'air.
  4. Ajouter les allocations de l'éclairage et des interrupteurs de logement et des appliques de balcon, que le plan ne montre pas.
  Il faut aussi taper les 140 panneaux de logement par type (1.1 à 4).

### Erreurs systématiques de la méthode (règles à corriger)

1. **« Une marque par étiquette de circuit » sur les plans d'éclairage** : tout symbole qui porte une étiquette UE/S devient un luminaire, y compris les enseignes. Règle : détecter d'abord les symboles d'enseigne (cercle-X vectoriel, identique à la légende E100), puis appliquer l'étiquette. Rapprocher le total d'enseignes du tableau des enseignes (E101).
2. **Cédules E101 converties en objets** sans vérifier qu'elles ne sont ni déjà au plan ni de nature différente (transfo de contrôle compté comme transformateur de puissance, panneau PC en double). Règle : une ligne de cédule ne crée un objet que si l'objet est absent du plan, et avec son libellé exact.
3. **Notes générales non transformées en quantités** (« prévoir … dans chacun des logements », « prévoir N conduits vides »). Règle : chaque note « prévoir/fournir » donne N objets ou une réserve.
4. **Rien n'est déclaré pour ce qui n'est pas dessiné** : éclairage, interrupteurs et balcons des logements. Règle : pour tout projet résidentiel, fournir une liste de contrôle des items habituels par logement, et produire une réserve explicite pour chaque item absent.
5. Granularité : panneaux de logement non typés alors que les cédules donnent les types.

## 7. v1 → v2

Aucune v1 comparable. La 1re passe de ce dossier a été interrompue par le bogue des pages tournées (34 pages sur 44 perdues) et n'a produit ni `ecart.md` ni rapport complet. Aucune comparaison v1/v2 n'est donc possible. À noter seulement : toutes les pages de `01-PLANS.pdf` (et de la référence) portent `/Rotate 270`. La v2 les traite correctement : les coordonnées des marques retombent sur les bons symboles dans les 10 marques tirées au hasard et dans les 33 enseignes recoupées.
