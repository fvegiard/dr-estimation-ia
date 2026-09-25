# Écart relevé automatique ↔ relevé humain — S-1797 (École William-Latter, Chambly)

Vérificateur indépendant, 2026-09-22. Relevé IA évalué : `travail/occurrences-visuel.csv` (1218 marques, 175 libellés), rendu le 2026-09-22 à 04:19.
Référence : « Relevé de Daniel.pdf » (export ACCEO, 6 p.) et « relevé alarme incendie ecole chambly.pdf » (1 p.). Transcription complète : `reference-quantites.csv`. Preuves : `travail/ecart-preuves/`.

## 0. Portée de la référence (à lire d'abord)

- La page « alarme » est **un doublon exact** de la page 5 de Daniel (mêmes 13 lignes, mêmes quantités, pied de page « Page 5 »). Elle n'est comptée qu'une fois.
- La référence est une **demande de prix de matériel**, pas un relevé complet. Elle couvre la distribution (panneaux, sectionneurs 600 V, transformateurs), l'éclairage, l'urgence, les contrôles nLight, l'alarme et le chauffage.
- Elle **ne contient pas** : les prises (178 marques IA), les raccordements mécaniques (112), le télécom, le contrôle d'accès (31 « autre »), le branchement et la MALT, ni les démolitions. Ces familles sont **non comparables**, et le verdict ne porte pas sur elles.
- Elle n'est ventilée **ni par feuille, ni par zone**. Les tableaux « par feuille » ci-dessous donnent donc la répartition IA, et pour l'alarme un recomptage manuel des deux versions du plan.

## 1. Correspondance des nomenclatures

| Référence (page) | Libellés IA regroupés | Justification |
|---|---|---|
| FIXTURE TYPE X (p.2) | « Luminaire X » + « Luminaire X urgence » | Daniel ne sépare pas l'urgence (ex. G 50 = IA 38 + 12). |
| FIXTURE TYPE T | « Luminaire T temporaire » + « Luminaire T urgence » | 2 + 3 = 5 = référence. |
| FIXTURE TYPE R | « Rail éclairage R » | Même objet (2 rails). |
| — (pas de ligne) | « Luminaire L3S » (+ urgence) = 23, « Luminaire mural puits » = 2 | Pas d'équivalent dans la référence (L3 : 75 = 68 + 7, sans L3S). **IA seule.** |
| ENSEIGNE SORTIE 17 + DOUBLE FACE 3 (p.2-3) | « Enseigne sortie applique » 7 + « plafond » 13 | 20 = 20. Les enseignes « temporaire » et « existante relocalisée » sont exclues (IA seule). |
| TETE DOUBLE | « Phare double temporaire » | Seule tête double au plan (EL301_ADD). |
| BATTERIE UNIT 72W | « Batterie urgence UA » | Même objet. |
| ONDULATEUR 1440W | « Mini-onduleur 1440W » | Même objet. |
| S01…SC2 (p.4) | « Poste mural SO1… », « Détecteur plafond OS2/OS3 », « Pont nLight BG1 », « Module gradation DE2 », « Bloc relais DP1/DP3 », « Module nLight NI1/SC2 », « Kit partition OS8 », « Boîte PS1 — à confirmer » | Codes nLight identiques. PS1 = 4 = 4 : la boîte « hors légende » de l'IA est bien comptée par Daniel. |
| PANNEAU ALARME | « Panneau principal alarme » | Nouveau PAI FX-4003. |
| DÉTECTEUR FUMÉE | « Détecteur fumée » | « Détecteur fumée conduit » (6) est **exclu** (pas de ligne chez Daniel). |
| DÉTECTEUR THERMIQUE | « Détecteur thermique — à confirmer » | Puits d'ascenseur. |
| KLAXON / KLAXON STROB / CLOCHE / STATION MANUEL | « Klaxon alarme » / « Klaxon-stroboscope » / « Cloche alarme extérieure » / « Poste manuel » | Symboles de la légende EL001. |
| RELAIS ADRESSABLE / MODULE INTERFACE / ISOLATEUR | « Relais adressable RA » / « Module adressable MA » / « Isolateur de ligne » | Mêmes symboles RA / MA / IL. |
| GSM | « Communicateur GSM fourni par autres » | Même objet (famille « autre » chez l'IA). |
| PANNEAU A CHANGER | — | Aucun libellé IA. |
| — | Témoin visuel 5, interrupteurs de gicleurs 9, boîte contact ascenseur 5 | **IA seule** (addenda 2). Exclus de la comparaison. |
| PANN CDP-1 / PD1 / PS1 / PS2 / PS3 (p.1) | « Armoire distribution CDP-1 » / « Panneau distribution » | L'IA compte aussi PS4. |
| SECTIONNEUR 30A 600V 3PH F / NF / NF WP (9) | « Sectionneur 30A » 36 + « fusible » 2 | Voir §4 : l'IA ne distingue ni la tension ni les pôles. |
| TRANSFO 150/75 kVA | « Transformateur sec » | 2 = 2. |
| AC1/AC2, CBF1000/1500 (p.6) | « Chauffage AC1/AC2 xkW », « Chauffage P3 1kW / 1.5kW » | Mêmes puissances. |
| RE253C 24V (5) | — | **Absent chez l'IA** (tableau du chauffage d'EL001 : relais électronique 24 V au plafond). |
| SECHE MAIN | « Sèche-mains » | 4 = 4. |

**Hors périmètre (référence) :**
- Les lignes de composition des panneaux (cellules, disjoncteurs) ont une quantité 0 chez Daniel : ce sont des descriptions.
- L'IA ne détaille pas les disjoncteurs, sauf 3 « disjoncteurs ajoutés ».
- **Non comparable (IA seule, famille absente de la référence) :** prises, mécanique, télécom, contrôle d'accès, branchement, MALT, bornes VE, démolition.

## 2. Tableau d'écart par famille (objets communs)

| Famille | Référence | IA | Écart | Écart % | Explication |
|---|--:|--:|--:|--:|---|
| Luminaires (A1…W, R, T) | 459 | 456 | −3 | −0,7 % | 36 types sur 42 identiques. Écarts : D36 −3, F +2, N −1, S2 −1, S3 +1, W −1 (brut 9 = 2,0 %). Voir §4. |
| Secours (enseignes, tête, batterie, onduleur) | 24 | 25 | +1 | +4,2 % | Batterie UA : 2 contre 1. Les enseignes concordent (20 = 20). |
| Commandes nLight | 192 | 193 | +1 | +0,5 % | DP1 : 43 contre 42. Les 16 autres codes sont exacts. |
| Alarme incendie | 75 | 93 | +18 | +24 % | Fumée +11, klaxons +11, RA +6, isolateurs −9, panneau à changer −1. **La référence suit la version AO** (voir §4). |
| Chauffage | 22 | 17 | −5 | −23 % | RE253C ×5 absents chez l'IA. Le reste est exact. |
| Distribution | 16 | 46 | +30 | +188 % | Sectionneurs 38 contre 9 (dont 24 sectionneurs 208 V 1 ph de thermopompes, absents de la demande de prix de Daniel). Panneaux 5 contre 4 (PS4). |
| Prises, télécom, mécanique, autres | — | 352 | n/c | n/c | Absents de la référence. |
| **Total commun** | **788** | **830** | **+42** | **+5,3 %** | Écart brut (somme des \|écarts\|) : 84 = 10,7 %. |

### Par feuille (familles où l'écart ≠ 0)

| Famille / objet | EL302 | EL303_ADD | EL305_ADD | EL404_ADD_2 | EL406_ADD_2 | EL407_ADD | EL403_ADD_3 | EL405_ADD_2 | EL502_ADD_2 | EL503_ADD_2 | EL504_ADD_2 | IA total | Réf. |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| D36 | – | 3 | 3 | | | | | | | | | 6 | 9 |
| F (+urg.) | 6 | 6 | 2 | | | | | | | | | 14 | 12 |
| N (+urg.) | – | 17 | 8 | | | | | | | | | 25 | 26 |
| S2 / S3 / W | | 0/0/1 | 1/1/0 | | | | | | | | | 1/1/1 | 2/0/2 |
| Batterie UA | | 2 | | | | | | | | | | 2 | 1 |
| DP1 | 12 | 17 | 14 | | | | | | | | | 43 | 42 |
| Sectionneurs | | | | 21 | 14 | 3 | | | | | | 38 | 9 |
| Panneaux | | | | | | | 3 | 2 | | | | 5 | 4 |
| Détecteur fumée | | | | | | | | | 12 | 10 | | 22 | 11 |
| Klaxon | | | | | | | | | 20 | 17 | | 37 | 26 |
| RA | | | | | | | | | 5 | 3 | | 8 | 2 |
| Isolateur | | | | | | | | | | | 3 | 3 | 12 |

Recomptage manuel des **versions AO** EL502 et EL503 (preuves `alarme-EL502-AO-vs-ADD2.png` et `alarme-EL503-AO-vs-ADD2.png`, panneau de gauche) :

| Objet | AO RDC | AO niv. 2 | Total AO | Réf. |
|---|--:|--:|--:|--:|
| Détecteur de fumée | 7 | 5 | 12 | 11 |
| Klaxon | 11 | 14 | 25 | 26 |
| Poste manuel | 5 | 2 | 7 | 7 |
| Klaxon-stroboscope | 2 | 0 | 2 | 2 |
| RA | 2 | 0 | 2 | 2 |

## 3. Qui a raison, écart par écart (≥ 2 objets, plus les écarts de 1 visibles)

| Écart | Verdict | Preuve |
|---|---|---|
| Fumée +11, klaxons +11, RA +6 | **IA** (pour la soumission) | L'addenda 2 a réaménagé le RDC et ajouté des dispositifs au niveau 2 (nuages Δ2). Sur EL502_ADD_2 et EL503_ADD_2, chaque marque IA tombe sur un symbole noir de la légende EL001 (klaxon = F + sablier, fumée = ⊘ grisé) : `alarme-EL502-AO-vs-ADD2.png` et `alarme-EL503-AO-vs-ADD2.png` (droite). Le recomptage de la version AO (gauche) donne 12 / 25 / 7 / 2 / 2, soit les chiffres de Daniel à ±1. **La référence alarme a été faite sur les plans AO, sans l'addenda 2.** Les 6 RA en plus (UR-01, VCFF) et les 6 détecteurs de conduit sont des ajouts de l'addenda 2 (notes « addenda 2 » dans le CSV, nuages visibles). |
| Isolateurs −9 (3 contre 12) | **Indécidable** (signalé : R-029) | `EL504-isolateurs-plein-vs-pointille.png` : 3 [IL] en trait plein (nouveau, marques 1-3) et environ 16 [IL] en pointillé sur les boucles existantes, qui seront raccordées au nouveau PAI (note 1 : « réutiliser le circuit de l'ancien panneau »). Daniel en compte 12 : il en remplace donc une partie. C'est un choix d'estimateur, pas une lecture du plan. L'IA a signalé l'exclusion, mais **sans en donner le nombre**. |
| Panneau à changer −1 | **Référence** (partiellement signalé, R-030) | L'ancien panneau d'alarme est remplacé par le FX-4003 (EL501_ADD, EL504 note 1). L'IA n'a pas de ligne pour son démantèlement ou son remplacement. |
| Sectionneurs +29 | **IA sur le fond, périmètre différent** | Tableau EL408_ADD_2 (`EL408-sectionneurs-div26.png`) : les colonnes « Sectionneur » et « Fourni par Div.26 » portent un X pour TP-01…TP-22 et TP-101/102. Ce sont 24 sectionneurs 208 V 1 ph à fournir, que Daniel ne met pas dans sa demande de prix « 600 V 3PH ». Hors TP, l'IA en a 14 contre 9 : il reste un surplus de 5, indécidable faute de qualification. L'IA ne distingue ni la tension, ni les pôles, ni F/NF, ni l'étanchéité (WP) : **erreur de méthode**. |
| RE253C −5 | **Référence** | Tableau des appareils de chauffage d'EL001_ADD_2 : ligne « RE253C ou RC580C, relais électronique 24 V, entreplafond ». Aucun libellé dans `nomenclature.csv` (grep RE253 = 0) et aucune réserve. **Oubli non signalé.** |
| D36 −3 | **Indécidable** (zone dense signalée, R-017) | `EL303-hall156-D36-N.png` : les 3 D36 du hall 156 sont bien marqués (14, 25, 28), et EL305_ADD en a 3 dans la salle 251. On ne retrouve pas de 9e D36 sans recomptage complet. Daniel a 9 pour D18, D24 et D36 : une saisie en série est possible. |
| F +2 | **IA probable** | `EL302-type-F-tableaux.png` : 6 F réels au-dessus des tableaux d'E-114 et E-110 (réaménagement dans l'existant, R-018). Daniel a peut-être exclu une partie de l'existant réaménagé. |
| Panneaux +1 (PS4) | **IA probable** | Marque PS4 sur EL405_ADD_2 (847, 873), note 4 « local giclé ». Daniel liste PD1, PS1, PS2 et PS3 seulement. |
| N −1, S2 −1 / S3 +1, W −1, DP1 +1, batterie +1 | Non vérifiés individuellement (< 2) | S2 et S3 se compensent : il s'agit probablement d'un classement S2/S3 dans la salle 258 (EL305_ADD, 956, 412). |
| L3S +23 (IA seule) | **Indécidable, à demander à Daniel** | Type présent au tableau d'EL001 (nomenclature IA). Daniel a L3 = 75, égal au L3 de l'IA **sans** L3S. Soit Daniel l'a oublié, soit il l'inclut ailleurs. |

**Échantillon aléatoire (seed 1797, 10 marques)** : `echantillon-seed1797.png`. Les marques sont OS2 (EL305, 1135/786), G (EL305, 959/1055), S1 (EL303, 769/323), L2S (EL303, 954/1082), A2 (EL302, 1788/479), prise de comptoir (EL403, 978/529), L2 (EL303, 886/972), N (EL303, 1106/1228), M (EL104, 1256/1081) et G (EL305, 1094/1039). **10 sur 10 sont correctes** : bon symbole, bon type, position à ±5 pt.

## 4. Verdict

- **Écart net sur les objets communs** : +42, soit +5,3 % (830 contre 788). L'écart brut est de 84 (10,7 %). Si l'on retire les 24 sectionneurs de thermopompes, hors périmètre de la demande de prix, l'écart net tombe à +18 (+2,3 %).
- **Critère de Francis (≤ 10 % par poste)** :
  - réussi : luminaires (−0,7 %), commandes (+0,5 %), secours (+4,2 %) ;
  - échoué : alarme (+24 %), chauffage (−23 %), distribution (+188 %).
- **Total ≤ 5 %** : échec de peu (5,3 %). Mais l'écart d'alarme vient d'une **référence périmée** (plans AO) : sur ce poste, c'est l'IA qui suit le dossier en vigueur.
- **Items manquants non signalés** (critère : aucun) :
  1. RE253C ×5 ;
  2. le remplacement de l'ancien panneau d'alarme, seulement effleuré en R-030.

  Les isolateurs existants sont signalés (R-029), mais sans nombre. **Le critère n'est pas atteint.**
- **Utilisable tel quel ?** Oui pour l'éclairage, l'urgence et les commandes nLight : 99 % de concordance, sans erreur dans l'échantillon. **Non tel quel** pour la distribution et le chauffage. L'estimateur doit :
  - qualifier les sectionneurs (tension, pôles, F/NF, WP) ;
  - ajouter les RE253C ;
  - décider des isolateurs et du panneau à remplacer ;
  - confirmer le L3S.
- **À faire du côté de DR** : la référence alarme doit être refaite sur l'addenda 2 (+11 détecteurs, +11 klaxons, +6 RA, +6 détecteurs de conduit, +5 témoins).

### Erreurs systématiques de l'IA (règles à corriger dans la méthode)

1. **Tableaux d'appareils sans symbole en plan** : chaque ligne des tableaux d'EL001 (chauffage, divers) doit produire un libellé ou une réserve (ici RE253C).
2. **Qualification des sectionneurs** : lire tension, phases, F/NF et WP dans EL408 et l'unifilaire, et en faire des libellés distincts (« Sectionneur 30A 208V 2P NF », « 30A 600V 3P F WP »…).
3. **Existant en pointillé sur les schémas de colonne** : compter et publier la quantité pointillée (isolateurs, dispositifs réutilisés) dans la réserve, au lieu de l'exclure sans chiffre.
4. **Remplacement d'équipement existant** (panneau d'alarme) : prévoir un libellé « démantèlement / remplacement » quand une note dit « nouveau panneau remplaçant l'existant ».

## 5. v1 → v2

- **v1** (`archives/S-1797-v1/`) : passe interrompue (marqueur `.en-cours`). Il n'y a ni `occurrences-visuel.csv`, ni rapport, ni `ecart.md`.
  - Les feuilles ont été mal identifiées à cause du bogue des pages tournées : `E114`, `E208`, `TP101` et `00lectrici-pNN` au lieu de `EL…`, dans `travail/texte/`.
  - **Total v1 : 0 marque. Aucune comparaison v1 n'existe.**
- **v2** : 1218 marques, 68 pages correctement classées (EL001…EL701, versions d'addenda retenues). Total commun v2 : 830, contre 788 pour la référence.
- **Correction constatée** : le bogue des pages tournées est corrigé (les noms de feuilles et l'orientation des rasters sont bons, 10/10 dans l'échantillon).
- **Régression** : impossible à évaluer, faute de sortie v1.
