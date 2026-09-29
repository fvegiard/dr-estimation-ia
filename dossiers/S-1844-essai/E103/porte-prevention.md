# E103 — Porte de prévention (SAQ Varennes, « DÉTAILS CONTRÔLE D'ÉCLAIRAGE », éch. AUCUNE)

Source unique : `E103-page6.pdf` (3456 × 2592 pt). Coordonnées en points PDF (x, y), lues dans le texte vectoriel de la page.

## Ce qu'est la feuille
- Pas de légende classique. Les symboles sont définis par : (1) les 10 schémas « riser » nLight (Design 2) en haut/gauche,
  qui donnent pour chaque étiquette le modèle Acuity (ex. `DP1 = NPP16 D EFP 347`), et (2) les blocs d'étiquettes vectoriels
  posés sur le plan-clé central (x 942-2111, y 1157-2407), chacun = carré + code (DP1, DP2, PP1, SO3, SO4, SW1, SW6) + modèle + n° `#nn`.
  → `legende-zoom.png` = risers 2, 3, 4 + clé raster P4 (zone qui définit les symboles ; pas une légende au sens strict).
- Le plan-clé est une IMAGE raster (2 images, x 942-2111) = plan d'éclairage de l'ingénieur avec zones colorées, luminaires (D3-N,
  D4-N, S20-N, O8-N, T, B-B, P1/P2, J1, G3/G4…) et annotations de révision (« NPP20 », « SÉPARER CE RAIL », « RAIL SEUL »,
  « 3 luminaires (moins… », « POURQUOI NPP16? » en violet vectoriel). Les appareils nLight à relever sont la couche VECTORIELLE par-dessus.
- Existant vu (non relevé) : mentions « (EC) », « PLAFOND GYPSE EXISTANT », « AÉROTHERME (EC) », « EF (EC) », « GYPSE (EC) ».
  Hors contrat : « CHAUFFE-EAU SERA CHANGÉ DURANT CHANTIER PAR BAILLEUR (HORS-CONTRAT) » → « fourni par autres », non chiffré (§5b).
- Luminaires du fond raster : NON relevés sur E103 (feuille de contrôle ; ils relèvent de la feuille d'éclairage). §5d « plan d'abord,
  schéma en contrôle » : les appareils nLight sont marqués au plan-clé ; les risers servent seulement à typer (modèle) et ne s'additionnent pas
  (#27 figure dans riser 1 ET riser 10 → renvoi, pas une 2e unité).

## Familles que je compterais (neuf)
Quantités = nombre d'étiquettes `#nn` distinctes LUES au plan-clé (texte vectoriel), pas un relevé final validé.

| # | Famille (libellé = modèle, R7/§5d) | Ce qui la distingue | Où lu | Étiquettes vues au plan (x,y du code) | Règle |
|---|---|---|---|---|---|
| F1 | DP1 — NPP16 D EFP 347 (bloc d'alim. gradation 0-10 V 347 V) | carré « DP1 » + « NPP16 D EFP 347 » | riser 1,3,8,9,10 + plan | #27 (1703,2297), #28 (1957,2275), #29 (2053,1653), #30 (1345,2117), #31 (2049,1972), #32 (1706,1717), #33 (1653,1717), #35 (1182,1934) = 8 | R1/§5d un compteur par modèle ; le « Type » servi (O8-N, B-B, T, S20…) va en note, pas en famille |
| F2 | DP2 — NPP PCD EFP (bloc gradation à phase 120/277 V) | carré « DP2 » + « NPP PCD EFP » | riser 2,5,6,7 + plan | #16 (1704,2345) *ambigu*, #21 (1681,2178), #22 (1462,1784), #23 (1964,1823) = 4 | R1 (modèle ≠ DP1), R5 (lire le modèle, pas le préfixe) |
| F3 | PP1 — NPP20 PL BP (relais charge prise 20 A) | carré « PP1 » + « NPP20 PL BP », « Prise » | riser 4 + plan | #19 (1351,1745), #20 (2040,2055) = 2 | R2 : relais séparé de la prise qu'il commande ; R4 n/a (ce n'est pas une prise) |
| F4 | SO3 — WSXA MWO PDT D WH (détecteur mural double techno, gradation) | carré orange « SO3 », « WSXA-G », suffixe « D » | plan seulement | #17 (1423,2301), #24 (1080,2238) = 2 | R1 : « D » = caractéristique → séparé de SO4 ; R5 |
| F5 | SO4 — WSXA MWO PDT WH (détecteur mural double techno) | carré orange « SO4 », « WSXA » sans D | plan seulement | #18 (1160,2271), #25 (1264,2281), #26 (1218,2339) Type G3, #37 (1022,1253) = 4 | R1 : même modèle ; G3 vs G4 = luminaire servi, pas une caractéristique du détecteur → même famille (à confirmer) |
| F6 | SW1 — NPODMA WH (poste mural nLight) | carré « SW1 » + « NPODMA WH » ; riser 3 : symbole rectangle « 8 » | riser 3 + plan | #34 (1282,2000), #36 (1006,2033) = 2 | R5, §5d modèle |
| F7 | SW6 — NPOD TOUCH WH (écran tactile nLight) | carré « SW6 » + « NPOD TOUCH WH » ; riser 2 : double cadre + ampoule | riser 2 + plan | #13 (1427,2342) = 1 | R5, §5d modèle |
| F8 | PS 150 — bloc d'alimentation du NPOD TOUCH (à confirmer) | rectangle « PS 150 » | riser 2 seulement (≈ x1040, y190) | aucun symbole au plan → compteur par schéma, 1 vu au schéma | §5b (schéma de contrôle : compter ce qui n'a pas de symbole au plan) ; §5b « composante chiffrée séparément » ; réserve |
| F9 | CAT5e nLight (câble de contrôle) — linéaire | trait « CAT5e nLight » entre appareils | risers + arcs bleus au plan | pas de longueur : ÉCHELLE « AUCUNE » | §5b linéaire → réserve « à métrer » (sur la feuille d'éclairage à l'échelle) |
| F10 | Connecteur RJ45 / terminaison CAT5e (par règle) | détails « CAT5E/6 CABLE TERMINATION », « DIGITAL NETWORK CONNECTORS », note « ALL CABLES SUPPLIED BY CONTRACTOR » | coin droit (x ≈2180-3100, y ≈1700-2380) | pas de quantité : 2 par segment CAT5e | §5d « supports et accessoires par règle » → compteur créé + réserve « quantité par règle à fixer » |

Non comptés (décision) : luminaires du fond raster (autre feuille), existant (EC), chauffe-eau (bailleur), boîtes raster
« NPP16 / NSP5 / NPP20 / WSXA / WSXA-G / NPODMA / NPOD » de l'ingénieur (doublons des étiquettes vectorielles, voir ambigu 1 et 3).
R3 (thermostats) et R6 (RELO) : aucun cas vu sur la feuille. Aucun symbole de prise/luminaire neuf vectoriel à compter ici.

Manques / réserves à ouvrir :
- Numérotation des étiquettes : #13 à #37 seulement, et #14, #15 absents → #1-#12, #14, #15 sont probablement sur une autre feuille (non reçue). Réserve.
- Détecteurs SO3/SO4 et #37 ne figurent dans aucun riser → typés uniquement par l'étiquette du plan.
- Note bas du détail « SEE SYSTEM SPECIFIC NOTES ON SHEET LC0.1 » : feuille LC0.1 non reçue.

## Symboles ambigus (1 ligne par zoom)
- `ambigu-1.png` (x1400-1780, y2200-2380) : #16 est codé DP2 avec commande « NPP PCD EFP » mais son texte dit « NPP16, Type D3-N / D4-N »
  (plan et riser 2), alors que #21/#22/#23 disent « NPPPC » ; l'annotation violette « POURQUOI NPP16? » et la boîte raster « NPP16 » du
  bureau directeur montrent que le concepteur doute aussi. → Tranché par le code de commande (NPP PCD EFP, famille F2), réserve « modèle #16 à confirmer » ; la boîte raster NPP16 n'est pas comptée en plus.
- `ambigu-2.png` : le riser 10 « nLight - VESTIBULE » montre #27 « NPP16, Type O8-N [DP1 - CAISSE TYPE 0] » (copie du riser 1), alors
  qu'au plan le vestibule porte #28 « NPP16 Type B-B ». → Je compte au plan : #27 une seule fois (zone bleue O8-N) + #28 au vestibule ;
  riser 10 = erreur de dessin probable, réserve (ne jamais additionner le #27 du riser 10).
- `ambigu-3.png` (x1480-1560, y1560-1610) : symbole raster carré « S/N » (S dans un cercle + N) répété près des rails, environ 9 vus
  sur l'aperçu (non comptés au zoom), sans étiquette vectorielle ni définition sur E103 — peut être un capteur nLight de l'ingénieur ou
  un repère de structure. Idem clé raster P4 « NPP16 / NSP5 / NPP20 : se référer aux plans des ingénieurs pour la quantité de relais »
  (voir legende-zoom) : NSP5 n'a aucune étiquette vectorielle. → R5 : pas de légende = pas de nom ; libellé « SN — à classer » + réserve,
  quantité non posée tant que le superviseur n'a pas dit si la couche raster fait partie du périmètre de E103.
