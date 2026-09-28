# Écart relevé automatique (v2) ↔ relevé estimateur — S-1715

Vérification indépendante, 2026-09-22. Chalet, patinoire et stationnement, parc Lionel-Groulx (118 rue Mathias, Salaberry-de-Valleyfield).

**Sources**
- Relevé IA v2 : `S-1715-Rapport-de-metre.md` (359 marques, 96 libellés) et `travail/occurrences-texte.csv` + `occurrences-visuel.csv`, `reserves.md` (R-001 à R-030).
- Référence : `reference/RELEVÉ ESTIMATION.pdf`, 8 pages scannées = export ACCEO « Relevé matériel RAPPORT 2026 » (p. 1 sommaire manuscrit, p. 2-8 détail). Transcription intégrale ligne par ligne : `reference-quantites.csv` (258 lignes, page du scan sur chaque ligne). Aucune ligne illisible ; quelques libellés tronqués par l'export (complétés entre parenthèses).
- Plans : `INBOX/S-1715/*.pdf`, rendus en vecteur (PyMuPDF). Coordonnées en points PDF (feuille 3370,44 × 2383,92 pt ; raster px = pt × 1,6894).
- Preuves : `travail/ecart-preuves/` (01 à 07 + tirage aléatoire).

**Nature de la référence.** Complète (alarme, distribution, éclairage, chauffage, service, sécurité, vidéosurveillance, 1 916 h, 555 060 $), mais **non ventilée par feuille** (tout est « Général ») et **sans aucune sortie télécom** (« tel/data » = 0 ; « TÉLÉPHONIE » ajouté à la main p. 1). Le télécom T-201 n'est donc comparable que pour les portes. La ventilation par feuille ci-dessous se déduit de la feuille où chaque objet est dessiné.

## 1. Correspondance des nomenclatures

| Référence (page scan) | Qté réf. | Libellé(s) IA v2 | Qté IA | Justification |
|---|--:|---|--:|---|
| FIXTURE TYPE A1, D1, L1, L2, L3, L3A, L4, L4A, M1, P1, R1, R2, R3 (p. 4) | 94 | Luminaire A1…R3, Lampadaire D1, Luminaire mural M1, Projecteur P1, Luminaire suspendu R1 | 94 | Même code de type (tableau E-101) ; 13 types identiques un à un |
| ENSEIGNE SORTIE (p. 4) | 5 | Indicateur d'issue Z1 (mur) 4 + Z2 (plafond) 1 | 5 | Deux variantes du même indicateur (légende E-002) |
| TETE DOUBLE / TETE SIMPLE / BATTERIE UNIT 2T (p. 4) | 7 / 3 / 1 | Tête double / Tête simple / Accumulateur AUBX | 7 / 3 / 1 | Légende E-002 |
| WST-C-3D 5, WST-0-5D 1, WST-C-3 3, WST-C-1 4 (p. 4-5) + INT B/V 8 (p. 5) | 13 + 8 | Interrupteur BT 7 + Gradateur BT 4 + Poste BT double (a/b) 3 + Panneau de contrôle P1 1 | 15 | Postes muraux basse tension ; voir §4-A |
| INT (p. 5) | 1 | Interrupteur unipolaire (E-201 1 + E-301 1) | 2 | Symbole « $ » sans cercle ; voir §4-A |
| DÉTECTEUR MOUV 360 OSC (p. 5) | 11 | Détecteur de présence 360° | 11 | |
| RELAIS RSP-C-347-Z1 / ACC-C-TP / WAC2-POE / WAH-C-POE-ID / GS308PP (p. 5) | 19 / 11 / 1 / 2 / 1 | Contrôleur RSP / Terminaison ACC-C-TP / WAC2 / WAH / GS308PP | 19 / 12 / 1 / 2 / 1 | Schéma E-003 ; voir §4-E |
| PANNEAU RELAIS (p. 5) | 1 | Armoire de relais BT (P.R.) | 1 | |
| PANNEAU ALARME, STATION MANUEL, KLAXON, DETECTEUR A FUMER (p. 2) | 1 / 5 / 2 / 10 | PAI, Poste manuel, Klaxon, Détecteur de fumée | 1 / 5 / 2 / 10 | |
| STROB (p. 2) | 2 | Klaxon + stroboscope | 1 | §4-C |
| DETECTEUR DE GAINE REL(ais) (p. 2), 2 h/u | 2 | Détecteur de conduit 2 + Relais adressable RA 2 | 4 | La ligne ACCEO inclut le relais (libellé « …REL », 2 h). Écart de nomenclature, pas d'objet manquant |
| prise duplex 15A 120V (p. 6) | 18 | Prise double 15A 8 + comptoir 6 + plafond 4 | 18 | Toutes 5-15R (légende E-002) ; répartition interne fausse, §4-G |
| prise usb (p. 6) | 2 | Prise double USB | 2 | |
| prise duplex 20a 125v GFI (p. 6) | 9 | Prise DDFT 5 + intempéries 3 + fontaine FR 1 | 9 | Trois variantes DDFT classe A |
| prise duplex 15/20A (p. 6) | 3 | Prise 15/20A (5-20R) | 3 | |
| CR2510 (p. 6), 145 $ | 1 | Prise hauteur spéciale (E-201, rouge, près de l'AUBX) | 1 | Appariement présumé : seul objet « prise » restant des deux côtés ; §4-G |
| PLINTHE B500W / B1000W / B1250W / B1500W / B2500W (p. 5-6) | 5/1/2/1/1 | Plinthe B5 / B10 / B12 / B15 / B25 | 5/1/2/1/1 | Tableau chauffage E-101 |
| WAF1503C24W (p. 6) | 5 | Aérotherme mural A15 | 3 | §4-B |
| SHU0431CCHAR / SHU1531CCAR (p. 6) | 1 / 1 | Aérotherme T4 / T15 | 1 / 1 | |
| RELAIS TRIAC (p. 6) | 9 | Relais triac RT | 9 | |
| SERPENTIN (p. 6) | 7 | Raccordement serpentin SE | 7 | SE-01…07 |
| MOTEUR VE, ECH, VC, PERC, VA, DEV + CONDENSEUR (p. 6) | 4+1+1+1+2+1+1 | Raccordement VE, ECH, VC, PECR, VA, DEV, COND | 11 | Un à un |
| CHAUFFE-EAU (p. 6) | 3 | Raccordement chauffe-eau CE (36 kW) | 3 | C/E ↔ CE-01…03, une marque par appareil (R-014) |
| SYTEME REF (p. 6) | 1 | Raccordement réfrigération de la glace (cédule E-002) | 1 | |
| — | 0 | Raccordement régulation 2 + RCFFM 1 (cédule RC-PSNO-200) | 3 | §4-F |
| SECHOIRE A MAIN (p. 6) | 3 | Sèche-mains | 3 | |
| PANN 600A 347/600V, PANN 400A 120/208V, TRANSFO 75KVA (p. 2) | 1/1/1 | Panneau RC-PDNO-600, RC-PSNO-200, Transformateur RC-TRNO-600 | 1/1/1 | |
| SECTIONNEUR 600A ×2 + 400A (p. 2) | 3 | Interrupteur de sûreté 600A 2 + 400A SF 1 | 3 | |
| ARMOIRE POUR APPAREILS (p. 3) | 1 | Cabinet de mesurage HQ | 1 | |
| BOITIER CAMLOCK STA-205 (p. 3) | 1 | Boîtier Camlock 200A | 1 | |
| PUIT TIRAGE (p. 3) | 2 | Puits de tirage | 2 | |
| BARRE MISE A TERRE 1/4X2 (p. 3) | 2 | Barre de MALT (E-301) 1 + Barre MALT télécom note 7 (T-201) 1 | 2 | |
| POTEAU 30pi (+ KIT HAUBAN, TERRIÈRE, BOOM TRUCK) (p. 3) | 1 | Poteau client — **fourni par autres** | 1 | Compte juste, qualification fausse : §4-H |
| — | 0 | Boîtier borne de recharge future | 1 | Absent de la référence ; en réserve R-023 |
| PORTE SIMPLE 2 + PORTE DOUBLE 3 (p. 7) | 5 | Porte contrôlée | 11 | §4-D |
| tel/data 0 | 0 | 61 marques télécom/sécurité T-201 (BG 11, CLI 5, mouvement 5, VS 8, WF 3, CB 3, D 2, CA 1, notes 2, HP 6, volume 2, micro 1, PCA, PDI, cabinet) | 61 | **Non comparable** |

**Hors périmètre** (compté par la référence, pas relevé par l'IA, par méthode) : conduits, câbles, boîtes, raccords, colle, courroies, supports (≈ 200 lignes) ; prix de lot (distribution 20 067 $, Camlock, transfo, éclairage 98 294 $, chauffage) ; MALT (tiges 3, figure 6 ×3) ; fusibles 600A ×3, plywood ×10, support transfo, protège-butoir, terrière, boom truck, kit hauban ; base lampadaire ×2 (incluse dans D1 par l'IA, R-024) ; alimentations d'éclairage 0-10 V (57) et 15 ; câble CAT5e 1 500 pi ; drops de chauffage 17 ; Oldcastle, Panduit ; boîtes 8×8×4 sécurité ×5 ; mentions manuscrites TEMPORAIRE / TÉLÉPHONIE / TRANSPORT. L'IA les renvoie explicitement en R-024/R-025 (linéaires, détails G/H).

## 2. Écart par famille (objets communs)

| Famille | Réf. | IA v2 | Écart | Écart % | Explication |
|---|--:|--:|--:|--:|---|
| Luminaires | 94 | 94 | 0 | 0 % | 13 types identiques |
| Commandes, interrupteurs, détecteurs, WaveLinx | 68 | 64 | −4 | −5,9 % | Postes muraux 22 réf. / 17 IA (indécidable, §4-A) ; ACC-C-TP +1 (IA juste, §4-E) |
| Secours | 16 | 16 | 0 | 0 % | |
| Alarme incendie | 22 | 23 | +1 | +4,5 % | Strobe −1 (IA conforme au plan, §4-C) ; RA +2 (nomenclature) |
| Prises | 33 | 33 | 0 | 0 % | CR2510 ↔ prise hauteur spéciale (présumé) ; 3 prises mal typées à l'intérieur du poste (§4-G) |
| Télécom : portes seulement | 5 | 11 | +6 | +120 % | Référence compte des types de porte, pas des portes (§4-D) |
| Distribution, panneaux, sectionneurs | 13 | 14 | +1 | +7,7 % | Boîtier borne recharge (réservé) ; poteau compté mais « fourni par autres » (§4-H) |
| Chauffage | 33 | 31 | −2 | −6,1 % | A15 : réf. 5, plan 3 (IA juste, §4-B) |
| Mécanique (raccordements) | 15 | 18 | +3 | +20 % | Régulation ×2 + RCFFM : circuits de cédule absents de la référence (§4-F) |
| Autres (sèche-mains) | 3 | 3 | 0 | 0 % | |
| **Total commun** | **302** | **307** | **+5** | **+1,7 %** | Écart brut (Σ valeurs absolues) : 21 objets, 7,0 % |
| Total commun hors portes | 297 | 296 | −1 | −0,3 % | |

**Par feuille** (familles avec écart ≠ 0) :

| Feuille | Objet | Réf. | IA | Écart | Qui a raison |
|---|---|--:|--:|--:|---|
| E-201 | Postes muraux BT + INT | 22 | 16 | −6 | Indécidable (§4-A) |
| E-301 | Interrupteur unipolaire (DEV-01) | 0 | 1 | +1 | IA (symbole au plan) ; la réf. l'inclut sans doute dans MOTEUR DEV |
| E-003 | ACC-C-TP | 11 | 12 | +1 | IA |
| E-201 | Stroboscope | 2 | 1 | −1 | IA (plan) |
| E-201 | Relais adressables | 0 | 2 | +2 | Nomenclature |
| E-301 | A15 | 5 | 3 | −2 | IA |
| E-002 (cédule) | Régulation ×2, RCFFM | 0 | 3 | +3 | IA défendable, à confirmer (réservé R-017/R-018) |
| E-102 | Boîtier borne recharge | 0 | 1 | +1 | Réservé R-023 |
| T-201 / T-101 | Portes | 5 | 11 | +6 | IA |

## 3. Dix marques IA tirées au hasard (seed 1715)

`random.seed(1715)`, `random.sample` sur les 359 lignes (occurrences-texte puis occurrences-visuel, ordre des fichiers). Recadrage ±45 pt sur `rasters/<feuille>.png`. Image : `ecart-preuves/10-marques-aleatoires-seed1715.png`.

| # | Feuille | x, y (pt) | Libellé IA | Vu sur le raster | Verdict |
|--:|---|---|---|---|---|
| 1 | E301_ADD | 2211, 638 | Prise DDFT | Prise avec trait DDFT, 41(200), salle d'entrée d'eau | OK |
| 2 | E301_ADD | 1715, 805 | Prise double 15A | Prise double (queue double), 12(200), bureau | OK |
| 3 | E201_ADD | 1851, 857 | Luminaire R3 | Étiquette R3 + cercle, 62(200) | OK |
| 4 | E003_ADD | 1083, 1290 | Contrôleur RSP-C-347-Z1 | RSP du segment éclairage extérieur M1 | OK |
| 5 | E201_ADD | 2138, 470 | Luminaire mural M1 | M1 6(200) sur le mur | OK |
| 6 | E201_ADD | 2361, 775 | Luminaire L3 | L3 3d(200) | OK |
| 7 | E201_ADD | 1749, 857 | Luminaire R3 | R3 62(200) | OK |
| 8 | T201 | 2027, 629 | Sortie télécom CA | Triangle CA près du PCA | OK |
| 9 | E003_ADD | 1984, 1739 | Terminaison ACC-C-TP | ACC-C-TP du segment W.C. 106 | OK |
| 10 | E201_ADD | 2361, 648 | Luminaire L3 | L3 3d(200) | OK |

**10/10 exactes en position et en type.**

## 4. Écarts de compte : qui a raison

**A. Postes muraux BT. Réf. 13 WST + 8 INT B/V + 1 INT = 22 ; IA 17 → indécidable, IA cohérente avec plan et schéma.**
- E-201 porte 18 symboles de commande BT (légende E-002 : cercle-$ = interrupteur BT, cercle-$ + carré plein = gradateur BT) : 7 interrupteurs simples (103, 104, 105, 106, 107, 109, 110), 5 avec carré (entrepôt 102, bureau 101, vestiaire N et S, + celui de la note 1 = P1), 3 paires 3a/3b, 3a/3b, c/d (6 symboles). L'IA en fait 15 postes : une paire = un WST-C-3.
- E-003 montre 13 WST : WST-C-3 ×3 (garage ×2, salle méca 111 ×1 = les 3 paires), WST-C-3D ×5 (103, 102, 101, vestiaire ×2), WST-C-1 ×4 (104, 105, 106, 109), WST-C-5D ×1 (patinoire). 14 postes au plan − 107 − 110 (absents du schéma) + 5D (sans symbole au plan) = 13. L'IA le dit exactement en R-010.
- La référence reprend les 13 WST du schéma **et** 8 « INT B/V » dont aucun groupe de 8 symboles n'existe au plan (ni 7 simples, ni 5 carrés, ni 6 symboles de paires). Soit l'estimateur double-compte une partie des postes, soit il prévoit 8 boîtiers/plaques par ailleurs. À lui demander.
- L'IA a en plus 1 unipolaire E-201 (1823, 807, réservé R-012) et 1 unipolaire E-301 (2208, 778, interrupteur manuel DEV-01) ; la référence a 1 INT.
- Preuve : `01-commandes-plan-vs-schema.png`.

**B. Aérothermes A15. Réf. 5, IA 3 → IA juste.** E-301 rév. 2 porte 3 hexagones A15 : (1819, 455) 3(600), (2149, 455) 5(600), (1817, 868) 7(600). Tableau E-101 : A15 = WFA1503C24W. Les 17 « drops de chauffage » de la référence (10 plinthes + 5 A15 + 2 T) héritent de l'erreur (15). Preuve : `02-A15-IA3-ref5.png`.

**C. Stroboscope. Réf. 2, IA 1 → plan = 1.** Un seul « S » avec avertisseur (klaxon + stroboscope, légende E-002) en (2231, 662), salle mécanique 111 ; deux « F » triangle = klaxons en (1815, 555) et (2144, 562). Le 2ᵉ STROB de la référence n'est pas au plan (ajout volontaire de l'estimateur ?). Preuve : `03-strobe-IA1-ref2.png`.

**D. Portes contrôlées. Réf. 5, IA 11 → IA juste sur le nombre de portes.** T-201 porte 11 ovales de porte ; le tableau « groupe de porte » de T-101 liste 11 portes en 8 groupes (P-EXT-01, 02, 03, 05, 06, P-101, 103, 106, 107, 109, 110). La référence compte 5 élévations types (2 simples + 3 doubles) et donc 5 boîtes 8×8×4 au lieu de 11. Preuve : `04-portes-IA11-ref5.png`.

**E. ACC-C-TP. Réf. 11, IA 12 → IA juste.** E-003 a 13 jetons « ACC-C-TP » : 12 bouts de segment (garage, salle méca, extérieur M1, patinoire, 103, 102, 101, vestiaire, 104, 105, 106, 109) + 1 dans la note générale (2076, 523), correctement écartée par l'IA. RSP 19 = 19 (21 jetons dont le titre du détail typique et sa légende). Preuve : `01-commandes-plan-vs-schema.png` (panneau de droite).

**F. Raccordements de cédule. Réf. 0, IA 3 → IA défendable, référence silencieuse.** RC-PSNO-200 cct 54 « RÉGULATION », cct 56 « RTÉGULATION » (coquille), cct 59 « RCFFM » (texte E002_ADD). Ce sont des départs réels, sans emplacement au plan ; l'IA les compte et les réserve (R-017, R-018). La référence n'a pas de ligne (peut-être dans le prix de lot). À confirmer ; ce n'est pas une erreur de lecture.

**G. Prises.**
- *CR2510 ↔ prise hauteur spéciale.* Le symbole rouge (2068, 590) E-201 est exactement « prise double 15A hauteur spéciale » de la légende E-002 (cercle, double queue, barre oblique). C'est le seul objet non apparié de part et d'autre ; appariement présumé, à confirmer avec l'estimateur. Preuve : `06-prise-hauteur-speciale-CR2510.png`.
- *Typage interne faux (IA).* 3 des 4 « Prise au plafond » — (1715, 575), (1730, 681), (1730, 754) — sont des prises doubles pivotées : la double ligne sort d'un seul côté du cercle, alors que le symbole « au plafond » la fait dépasser des deux côtés. Seule (2128, 713) garage est au plafond. Correct : double 11, plafond 1 (ce que v1 avait). Sans effet sur le total 5-15R, mais faux pour la main-d'œuvre. Preuve : `07-prise-plafond-vs-double.png` (4 symboles du plan puis la légende).

**H. Poteau. Compte 1 = 1, mais IA fausse sur la fourniture.** E-102 (619, 486) : « POTEAU CLIENT POUR LA LIAISON AÉROSOUTERRAINE. EMPLACEMENT EXACT À COORDONNER AU CHANTIER. » « Poteau client » = poteau privé (par opposition au réseau HQ) ; aucune note ne dit « par autres ». La référence le fournit : POTEAU 30 pi 2 500 $ + KIT HAUBAN 250 $ + TERRIÈRE 2 500 $ + BOOM TRUCK 1 500 $ ≈ 6 750 $ et 20 h. L'IA le marque « fourni par autres » (R-022) : un estimateur qui suit le relevé l'oublie. Preuve : `05-poteau-client.png`.

## 5. Verdict

- **Écart net sur objets communs : +5, soit +1,7 %** (302 réf., 307 IA) ; brut 21 objets (7,0 %). Hors portes : −1 (−0,3 %). Critère total ≤ 5 % : **respecté**.
- **Par poste (≤ 10 %)** : luminaires 0 %, commandes −5,9 %, secours 0 %, alarme +4,5 %, prises 0 %, distribution +7,7 %, chauffage −6,1 %, autres 0 % → respecté. **Hors critère** : mécanique +20 % (3 circuits de cédule que la référence n'a pas, IA défendable) et portes +120 % (erreur de la référence).
- **Items manquants non signalés en réserve (critère : aucun)** : aucun objet du plan absent du relevé. **Mais 1 item est de fait retiré du prix sans être signalé comme tel** : le poteau 30 pi, marqué « fourni par autres » (≈ 6 750 $ + 20 h dans la référence). Critère **non respecté** pour ce seul point. Le 2ᵉ stroboscope et le CR2510 ne sont pas des omissions de lecture (absent du plan / apparié).
- **Phrase honnête.** Pour les appareils comptables au plan, ce relevé est **utilisable par un estimateur** comme base de comptage (luminaires, secours, alarme, prises, chauffage, WaveLinx à ±1), après 3 corrections : (1) repasser le poteau en fourniture DR ; (2) retyper 3 « prises au plafond » en prises doubles ; (3) faire trancher par l'estimateur le nombre de postes BT (13 WST + 8 INT B/V ?) et les 3 départs régulation/RCFFM. Il ne remplace pas le métré des conduits et câbles, qui fait l'essentiel des heures (≈ 1 400 h sur 1 916). Sur ce projet, l'IA a trouvé 3 erreurs dans la référence : 2 A15 (et 2 drops) en trop, portes comptées par type (5 au lieu de 11, et 5 boîtes au lieu de 11), 1 ACC-C-TP manquant.

**Erreurs systématiques de l'IA (règles à corriger dans la méthode)**
1. **Qualificatif de fourniture inféré sans texte** : « client » (poteau client, et déjà « existant » en v1) interprété comme « fourni par autres ». Règle : ne marquer « par autres » que sur une mention explicite (« fourni par le client / par autres / existant ») ; « poteau client » = fourniture de l'électricien.
2. **Variantes de symbole jugées sur l'orientation** : un symbole pivoté (double queue d'un seul côté) pris pour une autre variante (« au plafond », queue des deux côtés). Règle : comparer au gabarit de légende après rotation, en regardant la symétrie de la queue.
3. **Nomenclature plus fine que l'ACCEO** (RA séparés des détecteurs de gaine, Z1/Z2, comptoir/plafond/double, régulation) sans table de regroupement vers les articles ACCEO : génère des écarts apparents. Prévoir une colonne « article ACCEO ».

## 6. v1 → v2

| | v1 | v2 | Réf. |
|---|--:|--:|--:|
| Périmètre v1 (hors WaveLinx E-003 et barres MALT) | 270 | 270 | 266 |
| Périmètre v2 complet | — | 307 | 302 |

- **Corrigé** : cédules et unifilaire lus (système de réfrigération 350 A compté, + régulation/RCFFM) ; schéma E-003 relevé et réconcilié avec le plan (RSP 19/19, WAH, WAC2, GS308PP justes, ACC 12 meilleur que la référence ; table plan ↔ schéma en R-010/R-011) ; double compte C/E + CE de v1 supprimé (v1 avait 6 raccordements pour 3 chauffe-eau, erreur que le contrôle v1 n'avait pas vue) ; paires 3a/3b ramenées à un WST-C-3.
- **Non corrigé** : le qualificatif du poteau (v1 « existant », v2 « fourni par autres ») — même effet, le poteau sort du prix ; la nomenclature reste plus fine que l'ACCEO. La « note 8 T-201 » reprochée à v1 était un faux grief : c'est la sortie 2CB (2367, 877), comptée dans les deux versions.
- **Régression** : 3 prises doubles pivotées retypées « au plafond » (v1 : double 11 / plafond 1, juste ; v2 : 8 / 4). Total des prises inchangé.
