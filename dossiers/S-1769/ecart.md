# Écart entre le relevé automatique (v2) et le relevé de l'estimateur — S-1769

CPE Soleil Souriant St-Constant, agrandissement (LC-ING 25-0075). Vérification indépendante du 2026-09-22.

**Sources**
- **Relevé IA (v2, 3e exécution de la chaîne, terminée à 03:24).** `S-1769-Rapport-de-metre.md` et `travail/occurrences-{visuel,texte}.csv` contiennent 141 marques : 137 visuelles et 4 textes « S » ($).
  - La feuille nommée `E004` dans les CSV correspond au cartouche **E401**.
  - `250075EPER-p03/p04/p05/p06` correspondent à E003, E004, E101 et E201.
  - Le rapport de métré affiche maintenant les vrais numéros de feuille.
- **Référence.** `reference/relevé complet.pdf` a 5 pages. La page 1 est le sommaire de soumission ; les pages 2 à 5 sont l'export ACCEO « Relevé matériel ». Il est **complet** (éclairage, chauffage, service, alarme, distribution) mais **n'est pas ventilé par feuille**. Toutes les lignes sont lisibles et sont transcrites dans `reference-quantites.csv` (83 lignes). Les libellés tronqués par l'export portent la mention « [libellé tronqué] ». J'ai vérifié les sous-totaux de section par addition (11 537,94 $, 2 827,06 $, etc.).
- **Plans.** `INBOX/S-1769/25-0075_E_PERM_SOUM_20260507_Signed.pdf`, 7 pages, rotation 90°.
- **Preuves.** Elles sont dans `travail/ecart-preuves/`. Chaque image a deux côtés :
  - à gauche, le raster IA avec les marques du CSV (rouge = libellé visé, bleu = autres) ;
  - à droite, le rendu du PDF vectoriel à ×4.
  - Les coordonnées sont en points dans la page affichée (2592 × 1728).

---

## 1. Transcription (résumé ; détail dans `reference-quantites.csv`)

| Section (page du scan) | Objets comptés (quantité) | Hors périmètre (non relevable par l'IA) |
|---|---|---|
| Éclairage (p.2) | A 18 · A1 4 · B 8 · B1 3 · C 3 · D 1 · E 4 · F 1 · F1 1 · G 1 · enseigne sortie combo 1 · tête double 3 · tête simple 2 · gradateur 4 · interrupteur 15A 4 | prix de lot 7 887,77 $ · alim. 0-10 V 50 · drop de switch 4 · conduit 3/4 220 pi · antisismique 45 |
| Chauffage (p.2-3) | plinthe 1500W 7 · plinthe 900W 2 · plancher chauffant 2 · thermostat plancher 2 · sonde plancher 1 · thermostat 2 · triac 4 | prix de lot 5 675 $ · câble chauffant 1 |
| Service (p.3) | GFI 20A 4 · prise 15/20A 1 · prise 15A 11 · tél/data 2 · échangeur d'air 2 · condenseur 2 · évaporateur 1 · chauffe-eau 2 · serpentin 5 · interr. 30A 3P 2 | conduits 1¼ et 2 po, boîtes 8x8, couvercles, boîtes 2-1/8 |
| Alarme (p.4) | klaxon 3 · relocalisation station manuelle 1 · détecteur de fumée 5 · boîtier de protection 1 | prix de lot 3 750 $, boîtes, fil 16AWG, connecteurs, conduit |
| Distribution (p.4) | panneau 225A 1 · sectionneur 200A 1 (disj. maître 0 · disj. 0) | prix de lot 3 817,21 $, fusibles 200A 2, 250MCM 100 pi + 30 pi, 4AWG, accessoires |
| Totaux (p.1, p.5) | — | matériel 30 663,44 $ · M-O 202,27 h (210 h chargées, 99 $/h manuscrit) · total 51 453,44 $ |

## 2. Correspondance des nomenclatures

| Référence (ACCEO) | Libellé(s) IA | Justification |
|---|---|---|
| FIXTURE TYPE A, A1, B, B1, C, D, E, F, F1, G | Luminaire A / A1 / B / B1 / C / D / E / F / F1 / G | Même lettre au plan (tableau de la vraie E004) |
| ENSEIGNE SORTIE COMBO | Enseigne sortie mur tête double | Enseigne + 2 têtes (UA C,2) |
| TETE DOUBLE (3) | UA mur tête double (1) + UA plafond (2) | Les 2 UA au plafond ont deux têtes au vecteur (749,440) et (724,605) : `ecl_q2.png`, `ecl_q4.png` |
| TETE SIMPLE (2) | UA mur tête simple (2) | Correspondance directe |
| GRADATEUR / interrupteur 15A | Gradateur à glissière / Commande éclairage ($) | Symboles a/b et « $ » |
| KLAXON, RELO STATION, DÉTECTEUR, BOITIER PROTECTION | Klaxon, Station manuelle ER, Détecteur de fumée, Boîtier protection | Correspondance directe |
| PLINTHE 1500W / 900W | Chauffage type A 1500W / 900W | Repères A 1.5 / A 0.9 |
| PLANCHÉ CHAUFFANT (2) | Plancher chauffant zone (2) | Note 2 : deux zones |
| THERMOSTAT PLANCHÉ (2) | Thermostat maître (1) + esclave (1) | Note 6 |
| SONDE / THERMOSTAT / TRIAC | Sonde / Thermostat unipolaire / Relais RT | La légende E001 dit « relais bas voltage avec transformateur » ; l'article ACCEO est « triac » |
| prise duplex 20a GFI (4) | Prise 15-20A DDFT @48 (2) + Prise ext. DDFT EI (1) | Toutes les prises GFI de l'IA (voir l'écart E3) |
| prise duplex 15/20A (1) | Prise micro-onde 5-20R | Correspondance directe |
| prise duplex 15A (11) | Prise double 15A (1) + @48po (10) + réfrigérateur (1) | La hauteur ne change pas l'article |
| tel/data | Sortie data murale | Correspondance directe |
| ECHANGEUR AIR / CONDENSEUR / ÉVAPORATEUR / CHAUFFE-EAU / SERPENTIN | ECH / CD / Unité AC / CE-1 / SE | Étiquettes d'équipement |
| INTERR 30A 3P 600V (2) | Sectionneur 30A sans fusible (2) | « 30A/SF » au plan |
| PANNEAU 225A / SECTIONNEUR 200A | Panneau C 225A / Interrupteur 200A F200A | E101 : boîte « 200A 22kA F:200A » (`alea08_*`) |

**Hors périmètre** (compté par la référence, pas par l'IA) :
- prix de lot des 4 sections ;
- alimentation 0-10 V ×50, drops ×4, antisismiques ×45 ;
- câble chauffant ;
- conduits, boîtes, couvercles, connecteurs, fil 16AWG ;
- 250MCM, 4AWG, fusibles, embouts, mamelon, contre-écrous ;
- toute la main-d'œuvre.

Côté IA, la marque « Artère panneau C — à métrer » est un linéaire : je la classe hors périmètre (la référence a 100 pi de 250MCM).

**Hors comparaison** (IA seule, la référence n'a pas de ligne pour ces objets) : les 9 marques de démolition EE.

**IA sans correspondant** (11 objets). La référence ne les a pas ; ils sont peut-être compris dans un prix de lot.

| Objet IA | Nombre |
|---|--:|
| Détecteur de présence (à confirmer) | 2 |
| Minuterie astronomique | 1 |
| Relais adressable RA | 1 |
| Porte électrifiée (raccordement, BA, BJ) | 3 |
| Remplacement borniers | 1 |
| Raccordement circuit 22 | 1 |
| Aéroconvecteur ER | 1 |
| Cercle gras à classer | 1 |

Bilan des 141 marques : 120 correspondantes + 11 sans correspondant + 1 linéaire + 9 démolition.

## 3. Écart par famille

| Famille | Réf. | IA (objets correspondants) | Écart | Écart % | IA sans correspondant | Explication |
|---|--:|--:|--:|--:|--:|---|
| Luminaires | 44 | 45 | **+1** | +2,3 % | 0 | Un « D » compté sur E401 (402,541) est un symbole existant, pas une applique D (E1) |
| Commandes / interrupteurs / détecteurs | 8 | 8 | 0 | 0 % | 3 | Présence ×2 et minuterie ×1 viennent du devis E003 art. 2.22 et ne sont pas dessinées (E7). Famille brute : 11 contre 8, soit +37,5 % |
| Éclairage de secours | 6 | 6 | 0 | 0 % | 0 | Conforme |
| Alarme incendie | 10 | 9 | **−1** | −10,0 % | 1 (RA) | Klaxon « typique » de la note 4 manqué (E2) |
| Prises | 16 | 16 | 0 | 0 % | 0 | Total juste, mais un sous-type faux : C,4 est une GFI (E3) |
| Télécom / data | 2 | 1 | **−1** | −50 % | 0 | 2e sortie de la note 7 manquée (E4), signalée en R-023 |
| Distribution / panneaux / sectionneurs | 4 | 4 | 0 | 0 % | 1 (borniers) | Le sectionneur 200A est maintenant compté |
| Mécanique | 12 | 11 | **−1** | −8,3 % | 1 (circ. 22) | AC +1, CE −1, SE −1 ; l'IA suit le plan (E5) |
| Chauffage | 20 | 20 | 0 | 0 % | 1 (aéroconvecteur ER) | Conforme (2 zones, sonde, maître et esclave) |
| Autres | 0 | 0 | 0 | — | 4 | Porte électrifiée ×3 (détail B, circuit 25), cercle gras ×1 |
| **Total** | **122** | **120** | **−2** | **−1,6 %** | **11** | Écart brut (somme des valeurs absolues par article) : **8** |

Si l'on ajoute les 11 objets sans correspondant, l'IA compte 131 objets contre 122, soit +9 (+7,4 %).

### Par feuille (familles dont l'écart n'est pas nul ; la référence n'est pas ventilée, l'attribution se fait d'après le plan)

| Famille | Feuille | Réf. (déduite) | IA | Écart |
|---|---|--:|--:|--:|
| Luminaires | E401 | 36 (sans C, D, E) | 37 | +1 (D existant) |
| Luminaires | E201 | 8 (C 3, D 1, E 4) | 8 | 0 |
| Alarme | E401 | 10 | 9 | −1 (klaxon) |
| Télécom | E401 | 2 | 1 | −1 |
| Mécanique | E401 + E101 | 12 | 11 (+ circ. 22 sur E101) | −1 |

## 4. Analyse de chaque écart

| # | Écart | Qui a raison | Preuve |
|---|---|---|---|
| E1 | Luminaire D : réf. 1, IA 2 | **Référence** | L'IA marque E401 (402,541) « D ». Au vecteur, c'est un **cercle pointillé à moitié noir, sans potence**, dans le corridor existant hachuré, à côté d'une applique pointillée (existante). La vraie applique D (E201 (1260,629)) est un cercle plein avec potence (`ref_E201_luminaires_ext.png`). Le symbole demi-plein est celui des détecteurs (`ref_E001_legende_alarme.png`), et le pointillé indique l'existant. La réserve R-004 évoque un doublon, mais pour la mauvaise raison. Fichier : `ecart_D_E401_402_541.png`. |
| E2 | Klaxon : réf. 3, IA 2 | **Référence** | Klaxon à E401 (≈650,471), sous le « $ » (648.6,457.7), avec la flèche de la note 4 « (TYPIQUE) ». Aucune marque IA à cet endroit. L'IA a pris la note 4 pour celle du klaxon (569,657) (`alea03_*`). **Non signalé.** Fichier : `ecart_klaxon_manquant_648_468.png`. |
| E3 | GFI : réf. 4, IA 3 ; prise 15A : réf. 11, IA 12 | **Référence** | La prise E401 (1328,384) C,4 est un **cercle plein à croix**. La légende E001 le définit comme « GFI double 15A @ 48" PLF » (`ref_E001_legende_prises.png`). L'IA l'a classée en « Prise double 15A @48po ». **Non signalé.** Fichier : `ecart_prise_C4_GFI_1328_384.png`. |
| E4 | Tél./data : réf. 2, IA 1 | **Référence** (signalé) | Un triangle plein « data » se trouve à E401 (≈1305,597), désigné par la flèche de la note 7, à côté de la prise C,5 (1316,597). L'IA n'a relevé que (1336,460). La réserve R-023 évoque une « autre sortie possible à confirmer ». Fichier : `ecart_data_manquante_1305_597.png`. |
| E5a | Évaporateur : réf. 1, IA 2 (AC) | **IA conforme au plan** | AC-1 (1440,585) et AC-2 (1443,638) sont tous deux dessinés et raccordés (`srv_s4.png`). La référence en retient un seul, probablement par choix de l'estimateur. |
| E5b | Chauffe-eau : réf. 2, IA 1 | **IA conforme au plan** | Un seul CE-1 au plan (1437,604), et un seul circuit CE-1 (35/37) à la cédule (`ref_E101_cedule_panneau_C.png`). |
| E5c | Serpentin : réf. 5, IA 4 | **IA conforme au plan** | SE-1 à SE-4 au plan, circuits 39/41 et 36/38. Aucun SE-5. Le circuit 22 « MÉCANIQUE » 15 A, sans charge désignée, peut expliquer le 5e SE ou le 2e CE de la référence. L'IA le relève à part (R-016). **Indécidable** sur ce qu'il alimente. |
| E6 | Aéroconvecteur ER : réf. 0, IA 1 | **IA conforme au plan** | Le symbole « ER » (1249,344) figure au réaménagement services (`vue_E401_services.png`). La référence n'a pas de ligne pour cet objet ; il est probablement dans le lot chauffage. |
| E7 | Présence ×2 et minuterie ×1 : réf. 0 | **Indécidable** | Le devis E003, art. 2.22.3 a), exige une détection de présence (`ecart_E003_devis_2-22.png`). Rien n'est dessiné. L'IA pose 1+1 « à confirmer » (R-013) ; la référence les a probablement dans le « prix de lot éclairage » ou l'alimentation 0-10 V. Ils ne doivent pas être chiffrés deux fois. |
| E8 | Porte électrifiée ×3, RA ×1, borniers ×1 : réf. 0 | **IA conforme aux documents** | Ces objets figurent au détail B de E004 (`alea09_*`, `alea10_*`), au circuit 25 « CONTRÔLE D'ACCÈS » et à la note 1 de E101. La référence n'a aucune ligne pour eux : soit un oubli, soit un prix de lot. À signaler à l'estimateur. |
| E9 | Cercle gras : réf. 0, IA 1 | **Indécidable, penche pour « pas un appareil »** | Cercle noir épais à E401 (1244,719), au coin d'un mur existant, sans étiquette ni circuit et absent de la légende (`ecart_cercle_gras_1244_719.png`). Signalé en R-009. |

### Échantillon aléatoire : 10 marques IA (`random.seed(1769)`, `random.sample` sur les 141 lignes, visuel puis texte)

Liste : `travail/ecart-preuves/echantillon-seed1769.csv`. Images : `alea01..10_*.png`.

| # | Feuille | Libellé IA | (x,y) pt | Vu au raster et au vecteur | Verdict |
|--:|---|---|---|---|---|
| 1 | E401 | Luminaire A 2x2 30W | 788,459 | Carré barré « A » C,3 | Correct |
| 2 | E401 | Luminaire B 6po | 798,658 | ○ « B » C,3a | Correct |
| 3 | E401 | Klaxon | 569,657 | Symbole klaxon | Correct (note CSV « note 4 » fausse : la note vise l'autre klaxon, E2) |
| 4 | E401 | Gradateur | 795,598 | Gradateur « b » | Correct |
| 5 | E401 | Relais RT | 1275,447 | « RT d » | Correct |
| 6 | E401 | Panneau C 225A | 1252,500 | Panneau demi-plein pointé par « C » | Correct |
| 7 | E401 démant. | Démol. applique | 578,1134 | Applique « EE » | Correct |
| 8 | E101 | Interrupteur 200A F200A | 1942,1212 | Boîte « 200A 22kA F:200A » | Correct |
| 9 | E004 | Boîte de jonction BJ | 1170,800 | « BJ » (détail B) | Correct |
| 10 | E004 | Relais adressable RA | 1205,732 | « RA » (détail B) | Correct |

**10 marques sur 10 sont bien placées et bien typées**, à ±5 pt. Les défauts de la v2 sont des **omissions** (klaxon, data) et des **erreurs de sous-type ou de neuf/existant** (C,4, D). Il n'y a pas de marques fantômes aléatoires. L'éclairage E401 a été revu en entier (`ecl_q1..q4.png`, services `srv_s1..s5.png`) : aucune autre omission.

## 5. Verdict

**Écart net sur objets communs : −2 sur 122 (−1,6 %)**, avec un écart brut de 8. En comptant les 11 objets que l'IA ajoute sans correspondant dans la référence, l'écart est de +9 (+7,4 %).

| Poste | Écart % | Critère ≤ 10 % |
|---|--:|---|
| Luminaires | +2,3 % | OK |
| Commandes | 0 % (brut +37,5 % avec présence et minuterie) | OK sur les objets dessinés |
| Secours | 0 % | OK |
| Alarme incendie | −10,0 % | OK, à la limite (1 klaxon) |
| Prises | 0 % (1 sous-type faux) | OK |
| Télécom / data | −50 % | **Échec** (1 objet sur 2) |
| Distribution | 0 % | OK |
| Mécanique | −8,3 % | OK |
| Chauffage | 0 % | OK |
| **Total** | **−1,6 %** | **OK** (critère ≤ 5 %) |

**Items manquants NON signalés en réserve** (critère : aucun) :
- le klaxon de la note 4 à E401 (≈650,471) ;
- la GFI C,4 à E401 (1328,384), classée en prise ordinaire.

**Le critère n'est pas rempli.** La 2e sortie data est signalée (R-023). Le « D » en trop est signalé en R-004, mais pour une autre raison.

**Verdict** : le relevé n'est **pas utilisable tel quel**, mais il en est proche. Un estimateur peut s'en servir après **4 corrections ponctuelles** :

1. ajouter 1 klaxon ;
2. passer C,4 en GFI ;
3. ajouter la 2e sortie data ;
4. retirer le « D » de E401.

Il doit aussi **trancher 5 objets hors référence** :
- présence et minuterie : objets du devis, à inclure ou à laisser au lot ;
- porte électrifiée, RA et borniers : absents de la référence, à vérifier ;
- circuit 22 ;
- aéroconvecteur ER.

Après ces corrections, tous les postes seraient à 0 % sauf la mécanique (−1 net, l'IA suivant le plan).

## 6. v1 → v2

Deux versions précèdent celle-ci : v1-1re passe (`archives-v1-S-1769`) et v1-2e passe (`S-1769-v1`).

| Version | Marques | Écart net sur objets communs | Postes > 10 % | Non signalés |
|---|--:|---|---|---|
| v1-1re passe | 122 | −9/122 (−7,4 %) | 3 | 3 |
| v1-2e passe | 130 | −3/122 (−2,5 %) | 2 (commandes, distribution) | 0 |
| v2 | 141 | −2/122 (−1,6 %) | 1 (télécom) | 2 (klaxon, GFI C,4) |

**Corrigées**
- La réserve devient une quantité : sectionneur 200A, boîtier, 2 zones de plancher et sonde sont tous comptés.
- La sonde n'est plus fondue dans le thermostat : maître, esclave et sonde sont séparés.
- Le « $ » existant (555,554) n'est plus compté.
- Les numéros de feuille sont corrects dans le rapport. Les CSV et le .qpl gardent les noms provisoires.

**Régressions** par rapport à v1-2e passe, qui avait ces quatre objets justes :
- 3e klaxon perdu ;
- 2e sortie data perdue ;
- GFI C,4 retypée en prise ordinaire ;
- le symbole « D » existant, exclu en v1-2e passe, revient sous forme de **luminaire D**.

**Cause probable** : `zoom.py`, `extract_occurrences.py` et `traits.py` ont été refusés pendant cette exécution (R-003). La lecture s'est faite sur tuiles seulement, à ±5 pt. Sans l'attribut vectoriel, la distinction neuf/existant et la lecture des symboles denses se dégradent.

**Nouveau** : la v2 ajoute 11 objets hors référence (devis, détail B, note 1). Ils sont défendables, mais il faut les isoler pour éviter un double comptage avec les prix de lot.

## 7. Erreurs systématiques de l'IA : règles à corriger dans la méthode

1. **Neuf/existant et type lus à l'œil.** Le cas type est le cercle pointillé demi-plein classé en luminaire D. Règle : pour chaque marque, contrôler au vecteur (`traits.py` / `get_drawings`) le trait plein ou pointillé et l'épaisseur. Un symbole pointillé ou fin n'est jamais neuf. La lettre seule ne suffit pas : forme et lettre doivent correspondre à la légende.
2. **Une note « TYPIQUE » ou une flèche de note est rattachée à un seul symbole.** Conséquences : klaxon (note 4) et data (note 7) manqués. Règle : chaque flèche de note se suit jusqu'à sa cible et crée ou confirme une marque. Après le relevé, recompter chaque symbole de la légende par recherche de forme sur tout le plan (klaxon, triangle data).
3. **Sous-types de prises par ressemblance.** La prise C,4 (plein + croix) a été classée comme la prise ordinaire (vide + croix). Règle : pour les prises, le remplissage plein signifie GFI. Le sous-type est un attribut obligatoire, vérifié contre la légende E001.
4. **Pipeline dégradé sans blocage.** Les outils refusés n'ont pas arrêté la chaîne, et le .qpl a été produit quand même. Règle : si `zoom.py`, `extract_occurrences.py` ou `traits.py` ne peuvent pas tourner, le statut devient « À VÉRIFIER » et non « TERMINÉ ». La permission `uv run releve/*` est à corriger dans l'appel `claude -p`.
5. **Objets de devis, de détail ou de note sans position au plan.** Il faut les compter, mais dans une **section séparée « hors plan »** (famille `devis`), pour que l'estimateur voie ce qui peut faire double emploi avec ses prix de lot.
