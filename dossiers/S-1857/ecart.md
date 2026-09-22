# Écart relevé automatique v2 et relevé Dupuis, S-1857 (Maison communautaire Saint-Michel)

Vérification indépendante faite le 2026-09-22.

**Relevé évalué** : `S-1857-Rapport-de-metre.md` et `travail/occurrences-*.csv`. Il compte 1 421 marques, dont 909 marques texte et 512 marques visuelles.

**Référence** : `reference/Releve-estimateur-Dupuis-S-1857.pdf`. C'est un export Plan Expert de 63 pages en images, à 2 997 × 2 116 px. Les pages 10 à 18 couvrent E400-E403 et E405-E409 en Rev0. Les pages 41 à 63 reprennent le relevé sur ADME-01.

**Échelle** : 1 pt du plan = 1,257 px sur la page Dupuis, et 2,388 px sur le raster IA.

**Outils** : `travail/ecart-preuves/` contient `sbs.py`, qui produit les images côte à côte (Dupuis à gauche, raster IA et marques v2 en vert à droite), ainsi que `det.py` et `red.py`. `det.py` détecte les pastilles Dupuis : couleur de légende × 0,75 + 64. `red.py` détecte les symboles rouges des prises sur le raster.

## 0. Transcription de la référence

- `reference-quantites.csv` (333 lignes) reprend la transcription vérifiée de v1 (`archives/S-1857-v1/dupuis-quantites.csv`).
- **J'ai relu deux feuilles sur le PDF** :
  - p. 15 (E406) : les 19 lignes de légende concordent. Je relève notamment PRISE 15/20A 86, PRISE 26, PRISE GFI 11, MONUMENT PLANCHER 11, TEL 18, MONUMENT TEL 7, 30A 250V 1, PRISE 50A250V 3, BORNE 3R 2 et TS 1.
  - p. 17 (E408) : les 14 lignes concordent. Je relève notamment PRISE 15/20A 39, PRISE 3, GFI 7, MONUMENT PLANCHER 4, TEL 6, MONUMENT TEL 4, COLONNETTE SERVICE 1 et KLAXON STROB 6.
  - Preuves : `dupuis-p15-legende-E406.png` et `dupuis-p17-legende-E408.png`.
- **Divergence trouvée : aucune.** Une remarque seulement : sur p. 17, le câble d'alarme porte « Échelle non configurée », sans longueur.
- **Pages retenues pour la comparaison** : p. 10 à 18 (Rev0). L'IA n'a reçu que les plans Rev0 et une seule page d'addenda, E600. La reprise ADME (p. 41 à 63) est traitée au §6.

## 1. Correspondance des nomenclatures

| Famille | Dupuis | IA v2 | Justification |
|---|---|---|---|
| Luminaires | FIXTURE TYPE DR2/DR5/DR51/DR52/DS0/DS1/DS2/DS4/DW4/DMWI | Luminaire DR2 … DW4 + DW42, Luminaire mural DMW1 | Correspondance 1 pour 1. Dupuis range DW42 dans DW4. |
| Luminaires (IA seule) | — | Luminaire ovale à classer ×2, Luminaire extérieur à classer ×1 | Dupuis Rev0 ne les compte pas (preuve `E401-ovales-accueil.png`). Sa reprise ADME porte DS3 ×2 sur E401. |
| Commandes | DO, DO PL, DO 3V / DI PL / B / BA / INT, INT PRE, GRADATEUR, GRADATEUR 3V | Do / Di / B / Ba / Interrupteur + Cercle barré fléché à classer | Dupuis pose une pastille sur chacun des 3 « cercles barrés » de l'E403, qui font partie de ses 5 INT/GRAD. |
| Secours | BATTERIE 36W + COMBO + COMBO 18W / EXIT / TETE SIMPLE + DOUBLE | Accumulateur 36W, 36W + enseigne, 18W + enseigne / Enseigne / Phare simple, double, sans étiquette | Les totaux par sous-groupe sont identiques. Le partage « + enseigne » (18) diffère de COMBO (8). |
| Alarme | KLAXON + KLAXON STROB (+WP), DÉTECTEUR FUMÉE / THERMIQUE, STATION MANUEL | Klaxon + Klaxon Ei, Détecteur fumée, thermique, Poste manuel | L'« Avertisseur visuel » (6) est un attribut du klaxon (combiné) et n'est pas ajouté au total. Il correspond au STROB de Dupuis (8). |
| Prises 15/20 A | PRISE 15/20A + PRISE (brun, y compris LV et REF) + PRISE GFI + MONUMENT PLANCHER | Prise duplex, DDFT, DDFT Ei, micro-onde, mobilier + Raccord lave-vaisselle | Dupuis ne distingue pas la pose. Ses pastilles brunes couvrent aussi les LV. |
| Prises spéciales | PRISE 50A250V, 30A 250V, COLONNETTE SERVICE | Prise cuisinière C | Les 3 « C » de l'E406 correspondent aux 3 PRISE 50A. |
| Services | SECHE MAIN, HOTTE | Raccord sèche-main, Raccord hotte Ht | 1 pour 1 |
| Télécom | TEL + MONUMENT TEL | Sortie data + Sortie data mobilier | 1 pour 1 (mur / mobilier) |
| Sectionneurs | NF 30A + 30A NF WP + BORNE 3R | Raccord CC équipement | BORNE 3R désigne le CC 3R des 2 bornes VE (E406). |
| Hors périmètre | COND ALARME 3/16 FT4 (60,6 + 162,8 + 161,0 m, E408 non métré) ; équipements mécaniques nommés (CH FR, CHAUFFE-EAU, CHE, SPP-1, xx-DCHT, VE-ELEC/MEC, HC-1/2, REF-DCHT, TS, THP-1, VRT-1 : 23) | Raccord pompe 10, chauffage 5, équipement cédule 17, évier électrique 6, borne VE 2 (cédules E600 addenda / E200), Panneau 6, Transfo 2, Sectionneur 2, MHQ 1, Sx 6, ID 5, Ls 6, TRA, PAI, PMI | Ces lignes ne se comparent pas 1 pour 1. Elles sont traitées à part. |

## 2. Écart par famille (objets communs, Rev0 p. 10 à 18)

| Famille | Dupuis | IA v2 | Écart | % | Explication (preuve au §4) |
|---|--:|--:|--:|--:|---|
| Luminaires typés | 504 | 509 | +5 | +1,0 % | Écart identique à v1. DS1 salle 124 et DS0 bureau 215 : Dupuis les a oubliés. DMW1 +3 : muraux sans étiquette (R-006). S'y ajoutent 3 « à classer » (§1). |
| Commandes | 205 | 203 | −2 | −1,0 % | Do +1 (oubli de Dupuis, toilette 105). E403 interrupteurs : 2 au lieu de 5, car 3 gradateurs sont passés en « à classer » (régression, signalée R-010). |
| Secours | 85 | 85 | 0 | 0 % | — |
| Alarme incendie | 121 | 121 | 0 | 0 % | Les klaxons concordent par feuille (13/31/38/20/1). Strobes : IA 6, Dupuis 8 (E408 : 4 contre 6). |
| Prises 15/20 A + LV | 332 | 324 | −8 | −2,4 % | E405 33 = 33. E406 134 = 134. E407 109 contre 112. E408 48 contre 53. |
| Prises spéciales | 5 | 3 | −2 | −40 % | Sécheuse 30 A comptée en duplex. Colonnette E408 non relevée. |
| Sèche-mains + hotte | 7 | 7 | 0 | 0 % | — |
| Télécom / data | 62 | 62 | 0 | 0 % | E407 +1 et E408 −1 (voir le détail par feuille). |
| Sectionneurs CC | 22 | 22 | 0 | 0 % | Le CC extérieur n'est plus compté deux fois (R-016). |
| **Total** | **1 343** | **1 336** | **−7** | **−0,5 %** | La somme des écarts absolus par famille est de 17 (1,3 %). |

### Écarts par feuille (familles dont l'écart n'est pas nul)

| Famille | Feuille | Dupuis | IA | Écart | Cause |
|---|---|--:|--:|--:|---|
| Luminaires | E401 | 153 | 157 | +4 | DS1 +1 (oubli de Dupuis) ; DMW1 +3 (R-006) |
| Luminaires | E402 | 197 | 198 | +1 | DS0 bureau 215 (oubli de Dupuis) |
| Commandes | E401 | 60 | 61 | +1 | Do toilette 105 (oubli de Dupuis) |
| Commandes | E403 | 37 | 34 | −3 | 3 gradateurs rangés en « Cercle barré fléché à classer » |
| Prises | E407 | 112 | 109 | −3 | 2 doublons MO restants (cuisinette 232) ; environ 5 prises accolées aux klaxons non relevées (bureaux est) |
| Prises | E408 | 53 | 48 | −5 | Bureau 315 : 3 prises non relevées ; autres zones : lecture visuelle déplacée (§4) |
| Prises spéciales | E406 | 4 | 3 | −1 | Sécheuse « S » 30 A (1 292 ; 1 277) comptée en duplex |
| Prises spéciales | E408 | 1 | 0 | −1 | Colonnette « C » (393 ; 1 028) sans aucune marque |
| Télécom | E407 | 25 | 26 | +1 | Non localisé : les coordonnées v2 sont trop imprécises sur E407 (§4) |
| Télécom | E408 | 10 | 9 | −1 | Salle 306 corrigée (+1), mais sortie du bureau 315 (414 ; 937) oubliée (−1) |

## 3. Totaux par feuille, Dupuis et IA (objets communs)

| Feuille | Page | Dupuis | IA v2 |
|---|--:|--:|--:|
| E400 | 10 | 77 | 77 |
| E401 | 11 | 240 | 245 (+3 à classer) |
| E402 | 12 | 316 | 317 |
| E403 | 13 | 161 | 158 (+3 à classer) |
| E405 | 14 | 63 (+14 équipements méc.) | 63 |
| E406 | 15 | 210 (+5 équipements méc.) | 209 |
| E407 | 16 | 181 | 179 |
| E408 | 17 | 92 | 85 |
| E409 | 18 | 3 (+2 équipements méc.) | 3 |

## 4. Vérification des écarts sur le plan

Les coordonnées sont en points du plan source (feuille de 2 383,92 pt). Les images sont dans `travail/ecart-preuves/`.

| # | Lieu | Constat | Qui a raison | Preuve |
|---|---|---|---|---|
| 1 | E406, cuisine 140 (1 298-1 314 ; 1 019) | Il y a une seule marque « Prise micro-onde » par prise MO. Les D voisins correspondent aux prises REF, qui portent une pastille brune chez Dupuis. **Le doublon MO est corrigé.** | Égalité | `E406-MO-cuisine140-corrige.png` |
| 2 | E407, cuisinette 232 (1 225 et 1 239 ; 1 150) | Deux marques « Prise duplex » sont posées sur 2 des 3 prises MO, qui portent déjà une marque MO. Il reste **2 doublons**. | Dupuis | `E407-MO-cuisinette232-2-doublons.png` |
| 3 | E407, bureaux est (x ≈ 1 395-1 400 ; y 897, 983, 1 051, 1 134) | Des prises rouges collées aux klaxons ont une pastille Dupuis, mais aucune marque IA. Les marques D de l'IA sont décalées vers x ≈ 1 445. Environ 4 à 5 prises manquent. | Dupuis | `E407-bureaux-est-prises-klaxon-oubliees.png` |
| 4 | E408, bureau 315 (405, 452, 498 ; 937) | 3 prises et 3 sorties data sont dessinées. L'IA a 0 prise et 2 T. v1 les avait. | Dupuis (régression) | `E408-bureau315-prises-data-colonnette-oubliees.png` |
| 5 | E408, bureau 315 (393 ; 1 028) | Carré « C » plein : c'est la colonnette de service chez Dupuis. L'IA n'a aucune marque et aucune réserve. v1 l'avait en « Prise spéciale ». | Dupuis (régression) | idem |
| 6 | E408, marques visuelles | Les marques ne tombent pas sur les objets : MO (730 ; 769) et DDFT Ei (707 ; 782) sont dans le vide ; DDFT (1 561 ; 797) est hors du bâtiment ; D (1 305 ; 1 031) est sur la terrasse. 21 des 48 marques de prises sont à plus de 15 pt d'un symbole (39 sur 109 sur E407, contre 2 sur 137 sur E406). | Dupuis ; défaut de positionnement de l'IA | `E408-vue-ouest-marques-deplacees.png`, `E408-est-marques-fantomes.png`, `E408-DDFT-1561-797-hors-batiment.png`, `E408-MO-Ei-marques-hors-objet.png` |
| 7 | E406, dépôt 137 (1 292 ; 1 277) | Le cercle « S » est la prise de sécheuse 30 A (teal 30A 250V chez Dupuis). L'IA la marque encore « Prise duplex ». Elle ajoute aussi « SÉCHEUSE 30A » depuis la cédule E600_ADD (899 ; 440) en affirmant qu'elle n'a pas de symbole au plan (R-004), ce qui est faux. On a donc **un mauvais classement et un double compte**. | Dupuis | `E406-secheuse-30A-en-duplex.png` |
| 8 | E406, débarcadère (1 264 ; 691 / 724) | Deux symboles de borne (éclair) avec un CC 3R. L'IA compte les 2 CC au plan, puis « Raccord borne VE ×2 » sur la cédule, en disant « aucun symbole au plan » (R-004), ce qui est faux. Les bornes sont maintenant comptées et signalées, mais elles sont mal localisées. | Dupuis sur la localisation ; compte OK | `E406-bornes-VE-symboles-au-plan.png` |
| 9 | E403 (620 ; 927), (1 071 ; 937), (1 046 ; 1 214) | Cercle barré avec une flèche. Dupuis y met sa pastille INT/GRAD. v1 les comptait « Interrupteur ». v2 les classe « à classer » (R-010). | Dupuis (régression de classement, signalée) | `E403-cercle-barre-620-927.png`, `E403-cercle-barre-1046-1214.png` |
| 10 | E401, accueil (557 et 715 ; 813) | Deux anneaux orange suspendus, sans étiquette. Dupuis Rev0 ne les compte pas ; sa reprise ADME ajoute DS3 ×2 sur E401. | Indécidable en Rev0 ; l'IA a raison de les signaler (R-005) | `E401-ovales-accueil.png` |
| 11 | E406, prises et data | Tous les symboles rouges ont une pastille Dupuis. Les 10 symboles que le script n'apparie pas sont masqués par des cotes ou par un klaxon. Vérifié à l'œil. | Égalité | `E406-postes-travail-OK.png`, `E406-bureau-OK.png` |
| 12 | E408, salle 306 (637 ; 904 / 943) | Les 2 sorties data sont maintenant marquées. **Corrigé.** | Égalité | `E408-vue-ouest-marques-deplacees.png` |
| 13 | E405 et E406, CC extérieur (404 ; 1 494) | Compté une seule fois (E406), et signalé R-016. **Corrigé.** | Égalité | diff v1/v2 |
| 14 | E402 (903,9 ; 1 394,1) et E407 (939,3 ; 1 321,5) | Les « B » de « ESC. B » sont supprimés (R-022). B = 31 sur E402 et 0 sur E407, soit Dupuis. **Corrigé.** | Égalité | diff v1/v2 |

Luminaires, Do et DS0/DS1 : les marques sont identiques à v1, à moins de 10 pt près. Le constat de v1 reste valable : Dupuis a oublié 3 objets.

### 10 marques tirées au hasard (`numpy.random.default_rng(1857)`, 1 421 marques)

| # | Feuille | Label | x ; y | Au raster |
|---|---|---|---|---|
| 1 | E402 | Luminaire DS0 | 1 148,9 ; 913,4 | Oui |
| 2 | E406 | Prise duplex | 1 176 ; 1 406 | Oui |
| 3 | E405 | Interrupteur fin de course Ls | 1 304,7 ; 312,6 | Oui (détail d'entrée d'eau) |
| 4 | E401 | Luminaire ovale à classer | 715 ; 813 | L'objet est présent ; son type n'est pas confirmé |
| 5 | E406 | Raccord CC équipement | 1 225,0 ; 785,3 | Oui (REF-DCHT) |
| 6 | E402 | Luminaire DS0 | 1 016,7 ; 916,5 | Oui |
| 7 | E405 | Poste manuel | 624,7 ; 706,4 | Oui |
| 8 | E407 | Prise duplex | 1 195 ; 1 150 | Oui (prise REF), à environ 6 pt |
| 9 | E402 | Luminaire DS1 | 1 214,4 ; 1 113,4 | Oui |
| 10 | E402 | Luminaire DS1 | 444,9 ; 1 405,4 | Oui |

Résultat : 10 sur 10 (`echantillon-seed1857.png`). Le tirage ne tombe sur aucune des zones E407/E408 où les marques sont déplacées.

## 5. Verdict

- **Écart net sur les objets communs : −7 sur 1 343 (−0,5 %).** La somme des écarts absolus par famille est de 17 (1,3 %).
- **Écart par poste majeur** (critère de Francis : 10 % au plus par poste) :

| Poste | Écart |
|---|--:|
| Luminaires | +1,0 % |
| Commandes | −1,0 % |
| Secours | 0 % |
| Alarme | 0 % |
| Prises (15/20 A + spéciales) | −3,0 % (327 contre 337) |
| Télécom | 0 % |
| Sectionneurs | 0 % |

  Tous les postes respectent le seuil, et le total respecte celui de 5 %. La sous-ligne des prises spéciales est à −40 % (2 objets).
- **Items manquants non signalés en réserve : le critère n'est pas respecté.**
  - la colonnette de service E408 ;
  - 3 prises et 1 sortie data du bureau 315 (E408) ;
  - environ 5 prises accolées aux klaxons (E407, bureaux est) ;
  - la sécheuse 30 A : elle n'est pas manquante, mais elle est mal classée et comptée deux fois, sous une réserve fausse.
- **Utilisable tel quel ?** Non. Les totaux sont bons, mais sur E407 et E408 la lecture visuelle des prises est moins fiable qu'en v1. Il y a des oublis, et 36 à 44 % des marques sont à plus de 15 pt de l'objet, donc le .qpl ne se contrôle pas dans Plan Expert.
- **Corrections avant soumission** :
  - relire E407 et E408 (prises et data) ;
  - ajouter la colonnette ;
  - reclasser la sécheuse en 30 A et retirer sa ligne de cédule ;
  - retirer les 2 doublons MO de l'E407 ;
  - reclasser les 3 gradateurs de l'E403 ;
  - rattacher les bornes VE à leurs symboles de l'E406.

## 6. Addenda ADME-01

L'entrée ne contient toujours qu'une page d'addenda (E600, cédules). La reprise Dupuis (p. 41 à 63) montre des plans d'étage ADME-01 réémis, avec les feuilles alarme-prises renumérotées de E404 à E408, et beaucoup d'ajouts : NF 30A 120 ×76, VC ×37, EFV, PREF, PC, CUISINIÈRE 70A, FOUR 250A, 200A/60A NF WP en toiture.

La v2 capte une partie de ces ajouts par les cédules : 36 raccordements, dont les bornes VE, PREF, PC, VC, la sécheuse et l'UAT-2. Mais elle ne peut pas les situer. **Le point bloquant de v1 subsiste** : il faut obtenir le jeu ADME-01 complet et refaire le relevé des plans alarme-prises.

## 7. v1 → v2

- **Totaux des objets communs** : v1 1 359 (+16, +1,2 %) ; v2 1 336 (−7, −0,5 %) ; Dupuis 1 343.
- **Erreurs systématiques de v1** :
  - MO en double : 10 → 2, corrigé en partie (restent E407, cuisinette 232) ;
  - « ESC. B » : corrigé ;
  - CC extérieur compté deux fois : corrigé.
- **Les 4 manquants de v1** :
  - bornes VE : comptées et signalées, mais depuis la cédule, avec une affirmation fausse « sans symbole au plan » ;
  - data de la salle 306 : corrigée, mais une sortie du bureau 315 est perdue, donc le compte net ne bouge pas ;
  - sécheuse : **non corrigée**, et désormais comptée deux fois (duplex + cédule) ;
  - TS : corrigé (signalé R-011).
- **Régressions** :
  - lecture visuelle des prises sur E407 et E408 (−8 prises, colonnette perdue, marques à 15 pt ou plus de l'objet, marques fantômes hors bâtiment) ;
  - 3 gradateurs de l'E403 déclassés en « à classer ».
- **Gains** :
  - nomenclature plus fine (DDFT, Ei, strobes, data mobilier) ;
  - cédules de l'addenda E600 exploitées (36 raccordements) ;
  - arbitrage E000/E600 corrigé (R-001).
