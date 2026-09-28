# Écart relevé automatique ↔ relevé de Daniel — S-1695 Playground Hotel

Vérificateur indépendant · 2026-09-22 · relevé IA évalué : run v2 (`OUTBOX/S-1695`, 1 719 marques, terminé 03:48) · référence : `reference/relevé de Daniel.pdf` (export ACCEO Estimation, 7 pages scannées, transcrit intégralement dans `reference-quantites.csv`, 213 lignes, aucune ligne illisible).

## 0. Nature de la référence (à lire avant les chiffres)

- La référence est un **export ACCEO complet du bâtiment**, sans ventilation par feuille ni par zone : sections Éclairage (p.2-3), Alarme incendie (p.3-4), Distribution (p.4-5), Chauffage (p.5-6), Service (p.6-7), Caméra/HP (p.7). Totaux : 379 414,59 $ coûtant matériel, 8 106,286 h.
- Contrôle de transcription : la somme des luminaires transcrits (A1…E2 + D1 + D5 par longueur) = **2 053**, identique à la ligne « alimentation éclairage 2053 » de la p.3. La transcription des luminaires est donc exacte.
- La référence inclut **toutes les chambres** (A1 = 823). Le relevé IA ne compte **qu'un exemplaire de chaque chambre type** (E400/E401) et le déclare en réserve R-002. Tout ce qui est dans les chambres n'est donc **pas comparable** tel quel. Le verdict chiffré ci-dessous se limite aux **objets communs** : aires communes, alarme, mécanique, chauffage, distribution dessinée sur les plans d'étage.
- Page 2 : bloc « Sommaire Général / CH11 » à 0 $ × 14 (bloc vide), sans effet sur les quantités.

## 1. Correspondance des nomenclatures

| Référence (ACCEO) | Labels IA | Justification |
|---|---|---|
| FIXTURE TYPE A1…E2 (hors D1/D5) | Luminaire A1…E2 | même code de la légende E001 |
| FIXTURE TYPE D1 xx pi (18 lignes, 78 u) / D5 xx pi (6 lignes, 10 u) | Luminaire D1 (86) / D5 (8) | l'IA compte 1 par étiquette. Daniel compte 1 par tronçon de longueur. Unités différentes (R-005). |
| — (aucune ligne B5, B6, B7, B8) | Luminaire B5, B6, B7, B8 (1+1+1+2, E400 par type) | codes absents de la référence (fusionnés par Daniel ou absents de sa liste) |
| ENSEIGNE SORTIE 29 | Enseigne sortie murale 11 + plafond 18 | même objet |
| interrupteur 15A / 3 way / 4 way / GRADATEUR / drop de switch | Interrupteur simple 39 | l'IA ne distingue pas les types et n'a pas relevé les chambres (R-003) |
| DETECTEUR MOUVEMENT 2 + INT DETEC PR 3 | Détecteur présence plafond DP 2 + Interrupteur détecteur présence 5 | même fonction |
| DÉTECTEUR A FUMÉE 65 + DÉTECTEUR DE GAINE 4 + STATION MANUEL 6 = 75 | AI dispositif adressé D 75 | l'IA compte les adresses D sans distinguer le type (R-017) |
| HAUT PARLEUR (alarme) 78 | AI signal adressé S 80 | adresses S = HP ou HP+strobe |
| MODULE ADRESSABLE 14 / MAT 7 | AI module relais MRA 14 / AI module MAT 7 | même objet |
| HAUT PARLEUR 94 (section CAMERA/HP) | AI haut-parleur + stroboscope 11 (E400, par chambre type) | **indécidable** : section « caméra/HP », sans doute les HP des chambres ou la sonorisation. Sans le nombre de chambres, pas de comparaison possible. |
| CAMERA 66 | Caméra (conduit vide) 68 | même objet |
| prise duplex GFI 184 / duplex 707 / usb 246 / RECEPT 30A 6 / PRISE AU TOIT 2 | Prise double 105, DDFT 8, USB 27, 30A 6-30R 3 + chambres (CCT-PRISES 78, CCT-DDFT 20, frigo 10, café 10, par type) | chambres non multipliées |
| tel/data 311, SORTIE TV 86, WIFI 79, RG11 13 | Sortie informatique murale 35, plafond/WiFi 9, Sortie TV câblodistribution 13 | chambres non relevées (R-004). RG11 13 ↔ Sortie TV 13 : égalité probable mais non prouvée. |
| N4A…N6D PANN 225A (12) + PANN 100A 120/240V (3) | Panneau de distribution 11 | 100A sur l'unifilaire E300, non relevé (R-020) |
| DISJ 125A 3P ×3, DISJ 40A 2P ×1 | — | E300, réservé (R-020) |
| INTERR 30A 3P 600V CEMA3 93 | Sectionneur E.I. 15 (E213 seulement) | **manque non signalé** (voir §5) |
| RACCORD DIRECT 20 | Raccord direct 9 | même libellé |
| MOTEUR EV 83 / BC 6 / SERPENTIN 8 / UAF 2 | Raccordement EV 83 / BC 6 / serpentin SE 8 / UAF toit 2 | même objet |
| MOTEUR HU 2 | (Élément H — à classer 5 ?) | le symbole « carré H » n'est pas dans la légende. **Indécidable** (R-012). |
| — | Raccordement VT 11, VE 6, CD 6, VM 5 | pas de ligne dans la référence (probablement dans INTERR 30A ou dans le lot) |
| PLINTHE B 500…2250W 347V (85) | Plinthe électrique 85 | même objet |
| TRIAC 347/24V 85, RADIANT 1, CHAUFFAGE RADIANT 9 | — | réservé (R-011) |
| SÉCHOIRE A MAIN 3 | Sèche-mains 2 | même objet |
| — | Boîte de jonction 6 (E202 éclairage ext.), Boîtes de jonction chambre ×5 78 marques, Boîte de répartition télécom 3 | la référence compte des boîtes en vrac (matériel), hors périmètre |

**Hors périmètre** (compté par la référence mais jamais relevé par l'IA, sans que ce soit un défaut) : alimentation éclairage 2053, tous les conduits (3/4, 1, 1-1/4, TME, conduit vide), fils (14AWG, 4/0, 3/0, 1/0, 3, 4, 6 AWG), boîtes octogonales ou carrées et couvercles, connecteurs, coudes, accouplements, LB, courroies, rail, crochets Caddy, clips, câble chauffant nVent (550 pi + 3), drops (switch 22, prise 55, chauffage 85), quincaillerie, parasismique, prix de lot, main-d'œuvre et $.

## 2. Écart par famille

### 2a. Totaux bruts (tout le bâtiment ; les écarts sont dominés par le multiplicateur de chambres non appliqué)

| Famille | Référence | IA v2 | écart | écart % | explication |
|---|--:|--:|--:|--:|---|
| Luminaires | 2 053 | 730 | −1 323 | −64 % | chambres × 1 au lieu de × n (R-002) |
| Commandes / interrupteurs / détecteurs | 997 | 46 | −951 | −95 % | chambres et corridors (Lutron) non relevés (R-003, R-006, R-025) |
| Secours (enseignes) | 29 | 29 | 0 | 0 % | — |
| Alarme incendie (hors HP 94 caméra/HP) | 174 | 176 (+11 HP chambre type) | +2 | +1,1 % | voir §3 |
| Prises | 1 145 | 261 | −884 | −77 % | chambres × 1 (R-002, R-004) |
| Télécom / data / caméra | 555 | 125 (+3 boîtes) | −430 | −77 % | télécom des chambres non relevé (R-004) |
| Distribution / panneaux / sectionneurs | 132 | 41 | −91 | −69 % | INTERR 30A (93) quasi absent, N4B manqué, E300 non relevé |
| Mécanique / chauffage | 199 | 219 | +20 | +10 % | VT/VE/CD/VM (28) sans ligne dans la référence ; radiant et HU absents de l'IA |

### 2b. Objets communs (comparables directement)

| Poste | Référence | IA | écart | écart % | qui a raison | preuve |
|---|--:|--:|--:|--:|---|---|
| Luminaires aires communes (A3-A9, B3, B9, C4, D3, D4, D5, E1, E2) | 354 | 360 | +6 | +1,7 % | IA pour A5, E2 et B9 ; D5 indécidable | §3 |
| dont A3/A4/A6/A7/A8/A9/B3/C4/D3/D4/E1 | 327 | 327 | 0 | 0 % | — | égalité ligne à ligne |
| Enseignes de sortie | 29 | 29 | 0 | 0 % | — | — |
| Détecteurs de présence (plafond + interrupteur) | 5 | 7 | +2 | +40 % | IA | `ecart-preuves/E200-intdet-*.png` |
| Alarme D + S + MRA + MAT | 174 | 176 | +2 | +1,1 % | indécidable (S) | §3 |
| Plinthes | 85 | 85 | 0 | 0 % | — | — |
| Raccordements EV/BC/SE/UAF | 99 | 99 | 0 | 0 % | — | — |
| Sèche-mains | 3 | 2 | −1 | −33 % | référence | `E210-SM-414.png` |
| Panneaux 225A | 12 | 11 | −1 | −8 % | référence (N4B manqué) | `E210-N4B-manquant.png` |
| Raccord direct | 20 | 9 | −11 | −55 % | indécidable, référence probable | §3 |
| Caméras | 66 | 68 | +2 | +3 % | IA probable | `E210-CAM-paires.png` |
| Prise 30A | 6 | 3 | −3 | −50 % | indécidable | `E210-prise30A.png` |
| **Total objets communs** | **853** | **849** | **−4** | **−0,5 %** | écart brut absolu 32 (3,8 %) | |

### 2c. Par feuille (familles à écart ≠ 0 ; la référence n'est pas ventilée par feuille, seule l'IA l'est)

| Label IA | E200 | E201 | E202 | E210 | E211 | E212 | E400 (type) | Réf. (bâtiment) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Luminaire A5 | 9 | – | – | – | – | – | – | 5 |
| Luminaire E2 | 12 | – | – | – | – | – | – | 9 |
| Luminaire B9 | 4 | – | – | – | – | – | – | 3 |
| Luminaire D5 | 8 | – | – | – | – | – | – | 10 tronçons |
| Luminaire D1 | 18 | 22 | 22 | – | – | – | 24 | 78 tronçons |
| Int. détecteur + DP | 7 | – | – | – | – | – | – | 5 |
| Panneau de distribution | – | – | – | 3 | 4 | 4 | – | 12 (+3 × 100A) |
| Raccord direct | – | – | – | 3 | 3 | 3 | – | 20 |
| Caméra | – | – | – | 28 | 21 | 19 | – | 66 |
| Sèche-mains | – | – | – | 2 | – | – | – | 3 |
| Prise 30A | – | – | – | 1 | 1 | 1 | – | 6 |
| AI signal S (E800/E801/E802) | 40 / 21 / 19 | | | | | | | 78 |

Chambres types : ratio implicite référence ÷ IA (par type) : A1 (823−57)/113 = 6,8 ; A2 6,5 ; B1 7,6 ; B2 7,6 ; B4 7,8 ; C1 9,0. Le ratio est cohérent, autour de 7, ce qui correspond à une soixantaine de chambres pour 11 types (plans clés E400). Le décompte par type de l'IA est donc plausible, mais la multiplication est à faire. C2, C3 et D2 (ratio 3 à 3,5) sont à vérifier.

## 3. Vérification des écarts sur le raster ou le PDF vectoriel

Chaque image `travail/ecart-preuves/*.png` montre à gauche le PDF vectoriel (`travail/feuilles/<f>.pdf`) et à droite le raster (`travail/rasters/<f>.png`) avec les marques IA cerclées en rouge.

| Écart | Feuille, zone (pt) | Constat | Verdict |
|---|---|---|---|
| A5 +4 | E200, x 1820-2130, y 580-870 (manucure/pédicure 411) | 9 cercles « A5 » dessinés : 5 en rangée à y≈714 et 4 en colonne à x≈1857. Les 9 marques IA sont sur ces 9 symboles. `E200-A5.png` | **IA** |
| E2 +3 | E200, x 2180-2420, y 580-900 (salles de massage/faciale) | 4 groupes de 3 appliques E2, soit 12. `E200-E2-B9.png` | **IA** (Daniel a manqué un groupe) |
| B9 +1 | E200 (2127,845), (2211,597), (2303,717), (2303,819) | 4 profilés B9 dessinés. `E200-E2-B9.png`, `E200-B9-4e.png` | **IA** |
| D5 −2 | E200, x 1840-2440, y 880-1120 (atrium/jardin 427) | 8 étiquettes D5 sur 8 profilés linéaires. Daniel en fait 10 tronçons par longueur (5, 6, 10, 18, 22, 22′6″). `E200-D5.png` | **indécidable** (unité : étiquette ou tronçon) |
| D1 (86 contre 78) | E200-E202, E400 | même problème d'unité, et 24 D1 sont par chambre type | **indécidable** |
| Détecteurs de présence +2 | E200 (1941,660), (2012,622), (2141,627), (1777,1230), (1877,1260) + DP (1808,1168), (2002,1168) | 5 interrupteurs « $ à ondes » et 2 DP dessinés. `E200-intdet-nord.png`, `E200-intdet-sud.png` | **IA** |
| Alarme S +2 | E800-E802 | 80 adresses S uniques (S4-001…042 sans 041, S5-002…021, S6-002…021), aucun doublon | **indécidable** (Daniel exclut peut-être 2 strobes seuls) ; < 3 % |
| Caméras +2 | E210 (2015/2035,550) et (2583/2604,1396) | caméras dos à dos : 2 boîtiers distincts à chaque endroit. `E210-CAM-paires.png` | **IA probable** (Daniel en a peut-être compté 1 par paire) |
| Panneaux −1 | E210 (2391,676), élec. 435 | l'octogone « N4B » est dessiné et le mot N4B figure dans le texte vectoriel, mais il n'y a **aucune marque IA** (la v1 l'avait). `E210-N4B-manquant.png` | **Référence** |
| PANN 100A ×3 | E300 (1597,2336 « 100A, ») | unifilaire non relevé | réservé (R-020) |
| Sèche-mains −1 | E210 toilette 413 (≈2004,662) | « SM » dessiné en 413 et en 414, marque IA sur 414 seulement (la v1 avait les 3). `E210-SM-414.png` | **Référence** |
| Raccord direct −11 | E210-E212 | l'IA ne marque que les carrés pleins des chambres universelles (415/424/425 par étage, R-010). Les 11 autres ne sont pas localisés. | **indécidable** (référence probable, non signalé par l'IA) |
| Prise 30A −3 | E210 (1495,631) salle serveurs | un seul symbole « (6-30R) » par salle serveurs, soit 3 dessinés. La référence parle de « RECEPT 30A 125V 2P 3F ×6 », un autre calibre. `E210-prise30A.png` | **indécidable** |
| Élément H (5) contre MOTEUR HU (2) | E210 x 1730-2210, y 680-880 | 6 « carrés H » visibles dans la zone, 5 marqués : l'un d'eux, près du distributeur d'eau, est manqué (la v1 en avait 6). Rien ne prouve que ce soient des HU. `E210-elementH.png` | IA incomplète, correspondance indécidable |

### Échantillon aléatoire (seed 1695, `random.sample` sur les 1 719 marques) — `ecart-preuves/echantillon-seed1695.png`

| # | Feuille | Label | x, y (pt) | Constat |
|---|---|---|---|---|
| 1 | E200 | Luminaire A8 | 1755, 1247 | A8 au vestiaire 426B ✔ |
| 2 | E801 | AI signal S | 2254, 545 | S5-012 sur un appareil de signalisation ✔ |
| 3 | E400 | Luminaire A1 | 949, 2011 | A1 ✔ |
| 4 | E200 | Luminaire A1 | 1943, 825 | A1 N4B-51e ✔ |
| 5 | E200 | Luminaire B3 | 2168, 1315 | B3 corridor ✔ |
| 6 | E200 | Luminaire B3 | 1724, 558 | B3 ✔ |
| 7 | E211 | Raccordement EV | 2293, 517 | EV-506 208V 1Ø ✔ |
| 8 | E210 | Boîtes JB chambre ×5 | 2467, 438 | cadre de boîtes N4B-21…29 ✔ (1 marque = 5 boîtes, selon la convention R-010) |
| 9 | E211 | Plinthe | 2943, 1059 | 750W UN3H-5-A-9 ✔ |
| 10 | E400 | Luminaire A1 | 1704, 1051 | A1 ✔ |

**10 sur 10 conformes.** Aucun faux positif trouvé dans l'échantillon.

## 4. Verdict

- **Écart net sur les objets communs : −4 sur 853 (−0,5 %) ; écart brut 32 (3,8 %).** Critère total ≤ 5 % : ✔ sur ce périmètre.
- **Par poste (critère ≤ 10 %)** : luminaires communs +1,7 % ✔ · secours 0 % ✔ · alarme +1,1 % ✔ · plinthes 0 % ✔ · raccordements mécaniques 0 % ✔ · caméras +3 % ✔ · panneaux −8 % ✔ · détecteurs de présence +40 % ✗ (l'IA a raison) · sèche-mains −33 % ✗ · raccord direct −55 % ✗ · prise 30A −50 % ✗ (indécidable). Sur 5 des 9 écarts par code de luminaire, c'est **l'IA qui a raison** contre la référence : A5, E2, B9, détecteurs, caméras probables.
- **Sur le bâtiment entier, le critère n'est pas atteint** : luminaires −64 %, commandes −95 %, prises −77 %, télécom −77 %. Ces écarts sont dus au multiplicateur de chambres non appliqué et aux dispositifs de chambre non relevés, mais tout cela est **déclaré en réserve** (R-002, R-003, R-004, R-006).
- **Items manquants NON signalés en réserve (critère : aucun) : ✗**
  1. Sectionneurs des équipements mécaniques : référence INTERR 30A 3P 600V = 93, IA 15 (E213 seulement). La v1 le signalait (R-005 v1), la v2 non.
  2. Panneau N4B (E210, élec. 435).
  3. Sèche-mains de la toilette 413 (E210).
  4. Raccords directs hors chambres universelles (−11, non localisés).
  5. 1 « carré H » sur E210.
- **Utilisable tel quel ? Non.** Sur les aires communes, l'alarme, le chauffage et la mécanique, le relevé est fiable, souvent plus juste que la référence. Mais un estimateur doit encore : (a) appliquer le nombre de chambres de chaque type (E400/E401) ; (b) relever les interrupteurs, gradateurs, 3-way/4-way et le télécom des chambres ; (c) ajouter 1 sectionneur par raccordement mécanique ; (d) métrer D1/D5 par tronçon ; (e) relever E300 (panneaux 100A, disjoncteurs) ; (f) ajouter N4B et SM 413.

**3 pires écarts** : interrupteurs 39 contre 973 (−934, chambres et types) ; prises 261 contre 1 145 (−884, chambres × 1) ; luminaires A1 170 contre 823 (−653, chambres × 1). Sur les objets communs : raccord direct −11, A5 +4 (IA juste), panneaux −4 (N4B + 3 × 100A sur E300).

**Erreurs systématiques (règles à corriger dans la méthode)**
1. Chambres types : appliquer le multiplicateur (compter les chambres de chaque type sur les plans clés E400 ou sur les numéros de chambre de E200-E202). Pour l'instant, c'est seulement réservé.
2. Symboles porteurs d'un mot vectoriel (N4B, SM, H, 6-30R) : extraire par le texte, pas par balayage visuel. Les oublis de la v2 (N4B, SM 413, un H) sont tous des symboles étiquetés.
3. Un raccordement mécanique (EV, VT, BC, SE, CD, VE, UAF) doit générer un sectionneur, ou au minimum une réserve.
4. Luminaires linéaires : 1 marque par tronçon avec sa longueur, et non 1 par étiquette.
5. Commandes : distinguer simple, 3-way, 4-way et gradateur, et relever les chambres types.

## 5. v1 → v2

Aucun `ecart.md` n'existe pour la v1 (`archives/S-1695-v1/`). La comparaison porte sur les totaux par famille de ses rapports de métré.

| Famille | v1 | v2 | Référence (commun / brut) |
|---|--:|--:|--:|
| Total des marques | 1 707 | 1 719 | 853 communs / 5 286 brut |
| Luminaires | 730 | 730 | 354 communs / 2 053 |
| Alarme D / S / MRA / MAT | 96 « détection » (D + MRA + MAT confondus) / 80 | 75 / 80 / 14 / 7 | 75 / 78 / 14 / 7 |
| Plinthes | 82 | 85 | 85 |
| Panneaux | 12 | 11 | 12 (+3) |
| Sèche-mains | 3 | 2 | 3 |
| Raccord CD / VM | 7 / 13 | 6 / 5 | – |
| « À confirmer » (symbole, télécom, prise) | 18 + 17 + 2 | 5 | – |

- **Corrigé dans la v2** : alarme séparée en D/MRA/MAT, et D = 75 correspond exactement à la référence (65 + 4 + 6). Plinthes 82 → 85 (exact). Doublons VM/CD retirés. Beaucoup moins de labels « à confirmer ». Sectionneurs E.I. ajoutés (15).
- **Régressions** : N4B perdu (12 → 11) et SM 413 perdu (3 → 2) alors que la v1 avait les deux. Un « carré H » perdu (6 → 5). La réserve sur les sectionneurs non comptés (v1 R-005) a disparu.
- **Non corrigé** : multiplicateur de chambres, commandes et télécom des chambres, longueurs des linéaires.
