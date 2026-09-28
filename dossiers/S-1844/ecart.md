# Écart relevé automatique (v2) ↔ relevé estimateur — S-1844 SAQ Varennes

Vérificateur indépendant, 2026-09-22.

**Sources**
- Relevé IA v2 : `S-1844-Rapport-de-metre.md`, `travail/occurrences-texte.csv` (623 lignes) et `travail/occurrences-visuel.csv` (150 lignes), soit 773 marques.
- Référence DR : `reference/take off.pdf`, 4 pages scannées, export ACCEO « Relevé matériel RAPPORT 2026 ». Transcription : `reference-quantites.csv`.
- Plans : `INBOX/S-1844/26-0108-02_ELECTRICITE_POUR SOUMISSION.pdf`. J'ai lu la couche texte et les vecteurs avec PyMuPDF. Correspondance feuille → page : E103 = p6, E200D = p7, E200 = p8, E300D = p10, E300 = p11.

**Preuves** (`travail/ecart-preuves/`) : chaque image met côte à côte deux vues.
- À gauche : le raster du pipeline avec les marques IA. Rouge = 1 marque ; magenta = une 2e marque au même point. Un carré bleu = objet dessiné sans marque IA.
- À droite : le rendu vectoriel du PDF.

**Nature de la référence**
- Export d'estimateur **sans aucune ventilation par feuille ni par zone**, en 3 blocs : ÉCLAIRAGE, DÉMOLITION, SERVICE.
- Pas d'alarme incendie.
- Environ la moitié des lignes sont du matériel au pied ou des accessoires.
- La comparaison « par feuille » n'est donc possible que du côté IA et plan.

## 1. Transcription de la référence

- **109 lignes** transcrites dans `reference-quantites.csv` : page du scan, section, objet, quantité, UM, prix, heures, feuille/zone (toujours « non indiquée ») et note. **Aucune ligne illisible.**
- **Page 1** : sommaire et notes manuscrites.
  - Totaux : 191 909,19 $ ; 1 050 h chargées / 1 044,005 h au relevé.
  - Notes : « $185.00 », « TRANCHER PAR AUTRE », « LIFT = », « TEMPORAIRE = », « TRAVAUX PAR PHASE ».
- **Deux lignes en double, et les deux comptent** :
  - « tel/data 10 » est en p.3 **et** en p.4.
  - « BOITE D 12X12X4 2 » est deux fois en p.4.
  - Preuve : j'ai refait la somme du bloc SERVICE et j'obtiens exactement 17 098,52 $ / 307,725 h, les deux lignes incluses. La référence charge donc **20 tel/data** (la v1 n'en avait compté que 10).
- **Anomalie d'impression** : « COND TME 1-1/2PO » affiche un temps unitaire de 6,500 h, alors que le total est de 9,750 h. Le temps unitaire réel est donc 0,065 h.

## 2. Correspondance des nomenclatures

| Référence (ACCEO) | Libellés IA v2 | Justification |
|---|---|---|
| FIXT TYPE D3-N / D3-NT1 / D4-N / D4-NTI | Projecteur D3-N / D3-NT1 / D4-N / D4-NT1 | Même code E101 (« D4-NTI » = D4-NT1, faute de frappe) |
| G3, G4, J1, K3, O8-N, P1, P2, S20-N | Réglette G3/G4, Troffer J1, Réglette K3, Linéaire O8-N/S20-N, Panneau P1/P2 | Même code |
| R4-NS, R6-NS, R8-NS, R12-N | Rail R4/R6/R8/R12-NS | « R12-N » = R12-NS (le texte E300 ne contient aucun « R12-N » seul) |
| FIXT TYPE T | Profilé T | Même code E101 |
| ENSEIGNE SORTIE | Enseigne U1 + U9 + « type à confirmer » | Toutes des enseignes |
| TETE DOUBLE + TETE SIMPLE | Phare double U2 + Phare simple U3 + Batterie U6 | Unités de secours. Comparées au total de la famille (U6 = batterie à 2 phares) |
| NPP20, NPP16, NPP-PCD, WSXA, WSXA-G, NPOD, NPODMA | Relais NPP20 / NPP16 / NPP PCD, Détecteur WSXA / WSXA-G, Contrôleur NPOD, Interrupteur NPODMA | Même code. NPP-PCD = « NPPPC » du plan |
| prise duplex 15/20A + GFI + MONUMENT PLANCHER DOU/SIM | Prise duplex 15A, circuit indépendant, BX caisse, 30A L5-30R, affleurement plancher, existante relocalisée, BX 4 pi | Tous des points de prise. Les monuments sont la façon d'installer les prises de caisse |
| tel/data (10 + 10) | Sortie télécom 6 + Sortie conduit dalle télécom 5 | Points tél./données |
| HAUT PARLEUR | Haut-parleur suspendu SN | |
| SÉCHOIREA MAIN | Sèche-mains SM | |
| RELO PLINTHE CHAUFFANT / RELO SONDE | Plinthe électrique 5 / Thermostat existant relocalisé 1 | Même objet (la référence dit « relo », le plan dit « N. ») |
| ENLEVEMENT FIXTURE | Démo luminaire A1…W + sans type + projecteurs sur rail + phares + enseigne (E300D) | Luminaires et secours à démonter |
| ENLEVER PRISE | Démo appareil prises/services (E.D.) E200D | L'IA ne ventile pas par type (R-025) |

**Hors périmètre** : la référence compte ces postes, mais l'IA ne relève pas ce genre d'objet.
- Prix de lot éclairage (62 303 $).
- Accessoires de rail : coupling 23, connecteur 6, 90° 2.
- Suspension P2 33, drop de switch 10.
- Unistrut 620 pi, tiges, noix et rondelles, crochets 140.
- Alimentation 0-10 V 125, PARASIMIC 125, Panduit / patch cords.
- Boîtes octogonales, carrées et couvercles, boîtes D 8x8 et 12x12.
- Tous les conduits (EMT, CPV, TME, vides) et le câble 18AWG.
- TRANCHER BÉTON 250.
- Main-d'œuvre et notes manuscrites (levage, temporaire, phasage).

**IA seulement** (aucune ligne dans la référence) :
- AA 9 : bailleur, que l'IA a elle-même marqué « non chiffré ».
- B-B 2, et 1 linéaire sans étiquette.
- Mise en route nLight 1.
- Mécanique et raccordements : 15 (BV-01, CE-1, PR-1, SE ×2, VE-01, VE-02, volet, démarreur, minuterie, thermostat inversé, relais BT 4).
- Thermostats : 3 à l'électricien + 2 par CVAC.
- E400 : 16 (5 boîtes 8x8, 10 descentes, 1 boîte 2x2).
- Télécom : sortie haut-parleur 1, contrôle de volume 1.
- 2 symboles « à classer ».

## 3. Écarts par famille (objets communs)

| Famille | Réf. | IA v2 | Écart | Écart % | Explication (détail au §4) |
|---|--:|--:|--:|--:|---|
| Luminaires (17 types communs) | 282 | 293 | +11 | +3,9 % | Total proche, mais par compensation : D3-N −20, D3-NT1 +15, T +8, D4-NT1 +3, G4 +3 (doublons), P2 +2 (doublons), G3 +1 (doublon), rails ±1. Il manque aussi 12 têtes sans étiquette au plan |
| Commandes / détecteurs nLight | 16 | 30 | +14 | +87,5 % | 8 marques en double dans l'IA : le vrai compte au plan E300 est de 22 (+6 = +37,5 %) |
| Secours (enseignes + têtes) | 19 | 19 | 0 | 0 % | Enseignes 5 = 5. Têtes 14 = 14 (répartition double / simple différente) |
| Alarme incendie | — | — | — | — | Aucune au dossier. E400 = conduits de sécurité, non comparables poste à poste |
| Prises | 56 | 38 | −18 | −32 % | L'IA couvre 100 % des prises neuves dessinées. La référence ajoute des « points » qui ne sont pas au plan |
| Télécom tel/data | 20 | 11 | −9 | −45 % | 2 lignes tel/data de 10 dans la référence ; le plan montre 11 sorties |
| Haut-parleurs | 9 | 9 | 0 | 0 % | |
| Chauffage (plinthes + sonde) | 6 | 6 | 0 | 0 % | |
| Sèche-mains (autres) | 2 | 2 | 0 | 0 % | |
| Distribution / panneaux / sectionneurs | 0 | 0 (+16 E400) | — | — | Aucun panneau ni sectionneur neuf (R-023, R-024) |
| Mécanique | 0 | 15 | — | — | La référence ne détaille pas les raccordements. Voir la note sur les prises |
| **Sous-total objets communs** | **410** | **408** | **−2** | **−0,5 %** | Somme des écarts absolus : 52 (12,7 %) |
| Démolition luminaires | 204 | 196 | −8 | −3,9 % | E300D : 7 « carrés-cercles à classer » (R-026) → 203 s'ils sont comptés |
| Démolition prises / services | 65 | 82 | +17 | +26 % | Les 82 E.D. mélangent prises, BX, télécom et thermostats |

**Par feuille**. La référence n'étant pas ventilée, les emplacements viennent de l'IA et du plan :

| Famille avec écart ≠ 0 | Feuille où se trouvent tous les objets | Écart |
|---|---|--:|
| Luminaires, commandes | E300 (sauf la mise en route nLight, sur E101) | +11 / +14 |
| Prises, télécom | E200 | −18 / −9 |
| Démolition luminaires | E300D | −8 |
| Démolition prises | E200D | +17 |

Détail des luminaires :

| Type | Réf. | IA v2 | Plan (dédoublonné) | Écart IA−réf. |
|---|--:|--:|--:|--:|
| D3-N | 122 | 102 | 102 (+12 têtes sans étiquette) | −20 |
| D3-NT1 | 6 | 21 | 21 | +15 |
| D4-N | 27 | 27 | 27 | 0 |
| D4-NT1 | 19 | 22 | 22 | +3 |
| G3 | 1 | 2 | **1** | +1 |
| G4 | 3 | 6 | **3** | +3 |
| P2 | 29 | 31 | **29** | +2 |
| J1 / K3 / O8-N / P1 / S20-N | 8/3/2/4/5 | 8/3/2/4/5 | idem | 0 |
| R4 / R6 / R8 / R12 | 5/5/9/22 | 5/4/8/23 | 5/4/8/23 | 0/−1/−1/+1 |
| T | 12 | 20 | 15 « T » + 5 « Tx » | +8 |

## 4. Vérification de chaque écart ≥ 2

| # | Écart | Preuve (feuille, coordonnées pt, fichier) | Qui a raison |
|---|---|---|---|
| 1 | **Marques en double (14)** : G4 +3, P2 +2, G3 +1, NPP16 +1, NPP20 +1, NPOD +1, NPODMA +1, WSXA +2, WSXA-G +2 | La couche texte E300 contient le même mot deux fois aux mêmes coordonnées : G4 (455,440), (602,1923), (868,1881) ; G3 (722,2052) ; WSXA (462,392), (722,1981) ; WSXA-G (528,1830), (1053,1986) ; NPOD (1058,1998) ; NPODMA (850,1496) ; NPP16 (631,1411) ; NPP20 (958,1170) ; P2 et « P2. » à (706,1023) et (707,1563). Un seul symbole est dessiné à chaque fois. Fichiers `ecart-02-E300-doublons-G4-WSXA.png`, `ecart-03-E300-doublon-NPP16.png`, `ecart-04-E300-NPP20-NPPPC.png`, `ecart-05-E300-doublons-NPOD-WSXAG.png` | **Référence** (G3 1, G4 3, P2 29 = plan). **IA fausse** : elle a dédoublonné U2 et H (R-013), mais pas ces 14 marques |
| 2 | **Projecteurs : 12 têtes sans étiquette oubliées** | E300 : 184 triangles verts (0.22/0.87/0, 4,6×5,3 pt) dans les vecteurs. 172 portent une étiquette D3 ou D4. Les 12 autres, à y 2019–2026 et x 1212–1698 (rail R12/R6 du bas, zone caisses), sont sans étiquette et sans marque IA, et ne sont dans aucune réserve. `ecart-01-E300-12-tetes-sans-etiquette.png` (carrés bleus) | **Plan** : 184 têtes. L'IA en a 172, la référence 174. Tous les deux sont incomplets ; l'IA l'est **sans le signaler** |
| 3 | D3-NT1 +15 / D3-N −20 / D4-NT1 +3 | E300, colonne ouest x≈1014, y 708–1382 : une série d'étiquettes « D3-NT1 », chacune à côté d'un triangle, plus des étiquettes D4-NT1 à (1024,676), (1060,663), (1098,664). `ecart-06-E300-D3NT1-colonne-ouest.png` | **IA** sur les types (étiquettes explicites). La référence a reclassé environ 15 D3-NT1 en D3-N ; ses 122 D3-N = 102 + 15 + ≈ 5 des 12 têtes sans étiquette. Indécidable au-delà |
| 4 | Profilé T +8 | E300 : 16 mots « T » (15 dans le plan, 1 dans une note) + « Tx5 » ×4 + « Tx2 » ×1. Mur nord y≈639 : `ecart-07-E300-profiles-T-nord.png`. E101 : « DIM : au pied » | **Indécidable** : l'unité est le pied, pas le segment. La référence (12 × 1 h) et l'IA (20) comptent tous deux des segments. Signalé par l'IA (R-005) |
| 5 | Commandes +6 (après dédoublonnage : 22 contre 16) | Plan E300, uniques : NPP16 9, NPP20 1, NPPPC 3, NPOD 1, NPODMA 2, WSXA 4, WSXA-G 2 = 22. E103 : annotations rouges « NPP20 » (PP1 #19, #20), « POURQUOI NPP16? », « SÉPARER CE RAIL » (`zooms/E103_960_1180_2110_2400.png`). Référence : NPP20 4, NPP16 2 | **Indécidable** par type : l'estimateur a visiblement appliqué une révision (NPP16 → NPP20) qui n'est pas au plan. L'IA suit le plan émis (après dédoublonnage) et signale les annotations (R-014) |
| 6 | Têtes doubles 9/7, simples 5/6 | E300 : U2 = 7 symboles (« U2 » doublé à (938,1481)), U3 = 6, U6 = 1 batterie à 2 phares | **Indécidable** par type. La famille est égale (14 = 14) |
| 7 | Prises −18 | E200 : 36 cercles bleus de prise dans les vecteurs. Les 32 marqués N. ont tous une marque IA à ≤ 10 pt. Les 4 E.C. (607,329), (412,988), (670,1861), (1725,2052) sont exclus avec raison (`E.C.` vu à (670,1861)). Il faut ajouter 4 « R. », la boîte au plancher et la 30 A | **IA** pour ce qui est dessiné. Les 18 points de plus de la référence ne se situent pas sur le plan. Il est probable que l'estimateur chiffre les raccordements méca (15) et thermostats (5) de l'IA et les monuments en « prise » : **indécidable** sans lui |
| 8 | GFI 2 (réf.) / 0 DDFT (IA) | Les 4 symboles en demi-cercle plein (932,1072), (489,1722), (926,1882), (1059,1882) sont des « circuit indépendant » selon E100 : moitié pleine. Le symbole DDFT, lui, est plein avec une bande blanche. `ecart-10-E200-prises-circuit-independant-vs-DDFT.png` + `zooms/E100_80_60_500_900.png` | **IA** selon le plan (aucun DDFT dessiné). La référence ajoute 2 GFI, probablement par règle de code |
| 9 | Monuments plancher 7 | E200 : caisses y≈1950 (8 prises BX + 4 sorties dalle), caisse nord (1102–1116,769), îlot (1456,766), affleurement (1844,1499). L'IA relève les prises mais pas le dispositif de plancher | **Référence**. Non signalé comme article, seulement comme conduit à métrer (R-022) |
| 10 | Tel/data −9 | E200 : 6 sorties télécom + 5 sorties conduit dalle = 11 au plan | **Indécidable**. La référence facture 2 × 10, peut-être tél. et données séparés |
| 11 | Démolition prises +17 | E200D : 82 mots E.D. (text layer : 82, aucun en double). Les E.D. marquent des prises, des BX, des triangles télécom et des thermostats. `ecart-09-E200D-ED-types-melanges.png` | **Référence** sur le poste « prise » (65). L'IA ne ventile pas (**signalé**, R-025) |
| 12 | Démolition luminaires −8 | Texte E300D : R 32, H 34 uniques, C 34, W 18, J 10… Zone entrepôt nord : toutes les marques tombent sur un symbole rouge (`ecart-08-E300D-entrepot-nord.png`). Relevé visuel déclaré partiel (R-026) | **Référence** probablement, écart faible (−3,9 %) et **signalé** |

Écarts de 1 (sous le seuil) : rails R6, R8 et R12. La couche texte donne l'avantage à l'IA (R6 : 2 « R6-NS » + 2 « R6NS » = 4).

### Tirage aléatoire de 10 marques IA

Tirage fait avec `random.seed(1844)` et `random.sample(…, 10)` sur les 772 marques des plans (E101 exclu). Montage : `ecart-preuves/tirage-montage.png`.

| # | Feuille | Libellé | x,y (pt) | Constat raster + vecteur | Fichier |
|---|---|---|---|---|---|
| 1 | E300D | Démo luminaire H | 1639,2018 | Symbole rouge H : OK | tirage-01-E300D.png |
| 2 | E300D | Démo luminaire S2 | 1516,710 | Luminaire S2 rouge : OK | tirage-02-E300D.png |
| 3 | E300 | Projecteur D3-N | 1486,691 | Triangle et D3-N : OK | tirage-03-E300.png |
| 4 | E200 | Raccordement serpentin SE | 518,1800 | SE-02 1 kW N. PA(82,84) : OK | tirage-04-E200.png |
| 5 | E300 | Rail R4-NS | 1089,1828 | Rail R4-NS : OK | tirage-05-E300.png |
| 6 | E300D | Démo luminaire R | 1148,1849 | Symbole R rouge sur rail : OK | tirage-06-E300D.png |
| 7 | E300D | Démo luminaire H | 1943,938 | Symbole H rouge : OK | tirage-07-E300D.png |
| 8 | E300 | Relais NPP16 | 1863,1892 | Encadré NPP16 : OK | tirage-08-E300.png |
| 9 | E300 | Réglette K3 | 433,1707 | K3 sous armoire : OK | tirage-09-E300.png |
| 10 | E300 | Rail R12-NS | 1239,698 | Rail R12-NS : OK | tirage-10-E300.png |

**Résultat : 10 sur 10 bien placées.** Le tirage n'est pas tombé sur une des 14 marques en double (1,8 % des marques). C'est le recoupement par coordonnées (§4 #1) qui les a trouvées.

## 5. Verdict

**Écart net sur les objets communs** : référence 410, IA 408, soit **−2 (−0,5 %)**.
- Démolition incluse : 679 contre 686, soit +7 (+1,0 %).
- Le total est bon **par compensation**. La somme des écarts absolus fait 52 (12,7 %).

**Critère Francis, ≤ 10 % par poste :**

| Poste | Écart | Conforme ? | Remarque |
|---|--:|:-:|---|
| Luminaires | +3,9 % | Oui | Mais les types D3 sont décalés |
| Secours | 0 % | Oui | |
| Commandes | +87,5 % | Non | +37,5 % même après dédoublonnage |
| Prises | −32 % | Non | Articles ACCEO de l'estimateur |
| Tel/data | −45 % | Non | |
| Haut-parleurs / chauffage / sèche-mains | 0 % | Oui | |
| Démolition luminaires | −3,9 % | Oui | |
| Démolition prises | +26 % | Non | |

**Total ≤ 5 % : conforme (−0,5 %)**, mais seulement parce que les écarts se compensent.

**Items manquants NON signalés en réserve** (critère : aucun) → **critère non respecté**.
1. 12 têtes de projecteur sans étiquette sur E300 (y≈2019–2026). La v1 les avait.
2. Les 14 marques en double ne sont pas signalées : c'est un surcompte non réservé, R-013 ne couvre que U2 et H.
3. Les monuments / boîtes de plancher des caisses ne sont pas signalés comme article : seul le conduit l'est (R-022).

**Utilisable tel quel ?** Non.
- **Fiable pour** : le repérage (10/10 au tirage), l'inventaire des types, la couverture E200 (100 % des prises neuves) et la démolition E300D (−3,9 %).
- **Corrections à faire avant de s'en servir** :
  - (a) retirer les 14 doublons ;
  - (b) ajouter les 12 têtes de projecteur, à typer ;
  - (c) appliquer les révisions de E103 aux commandes ;
  - (d) métrer les profilés T au pied ;
  - (e) ventiler les E.D. de E200D par type ;
  - (f) faire correspondre prises, raccordements et monuments aux articles ACCEO de DR.

### Erreurs systématiques de l'IA (règles à corriger dans la méthode)

1. **Pas de dédoublonnage automatique des mots superposés.** Le PDF AutoCAD répète certaines étiquettes aux mêmes coordonnées, et 14 marques fantômes en sortent. Règle : même mot à ±1 pt = une seule occurrence, appliquée par script dans `extract_occurrences.py` et non à la main (python était bloqué dans la session v2 : R-013, rapport §Limites).
2. **Pas de recoupement symbole ↔ étiquette.** Les symboles dessinés sans étiquette sont perdus. Règle : compter la géométrie de chaque famille (couleur et gabarit du symbole) et produire « N symboles − M étiquettes = K sans type ».
3. **Démolition par étiquette sans type** (E.D. de E200D) : l'écart sur ENLEVER PRISE en vient.
4. **Produits vendus au pied comptés par segment** : profilé T, et rails comptés en unités.
5. **Aucune table de correspondance vers les articles ACCEO de DR** : points de prise génériques, monuments, tel/data, raccordements méca.
6. **Les révisions de E103 (en rouge) sont notées mais pas intégrées** : c'est la source probable de l'écart NPP16 / NPP20.

## 6. v1 → v2

J'ai recalculé la v1 (`archives/S-1844-v1/`) sur la même base que la v2, avec tel/data = 20 dans la référence.

| | v1 | v2 | Référence |
|---|--:|--:|--:|
| Marques | 551 | 773 | — |
| Objets communs | 405 (−1,2 %) | 408 (−0,5 %) | 410 |
| Démolition (luminaires + prises) | 84 | 278 | 269 |

**Corrigé depuis la v1 :**
- E300D (démolition éclairage) est maintenant relevé : 196 contre 204 à la référence.
- La confusion DDFT de la v1 est réglée : 3 prises « DDFT » redevenues « circuit indépendant », ce qui est juste selon E100.
- E200D passe à 82 E.D., conforme au texte du plan (la v1 en avait 84).

**Pas corrigé :**
- La ventilation par type de la démolition E200D.
- Le T au pied.
- La table de correspondance ACCEO.
- L'utilisation de E103 (révisions rouges).

**A régressé :**
- **Le dédoublonnage est perdu.** La v1 avait P2 29, G4 3, G3 1 et 22 commandes ; la v2 a 31, 6, 2 et 30. Le « correctif » des relais E103 a été obtenu en comptant des doublons, pas des relais.
- **Les 12 têtes de projecteur sans étiquette, que la v1 relevait « à confirmer », ont disparu** sans réserve.
- Au bilan, le total est meilleur par hasard, et la justesse par type est moins bonne.
