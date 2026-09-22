# S-1693 — Écart relevé automatique (v2) ↔ relevé de Daniel (ACCEO)

Vérificateur indépendant · 2026-09-22 · preuves dans `travail/ecart-preuves/` (PNG recadrés du raster : chaque marque de l'IA est cerclée en rouge, avec son libellé).

## 0. Nature de la référence
- Il s'agit d'un **export ACCEO complet** : 13 pages, 397 lignes transcrites dans `reference-quantites.csv`. On y trouve 13 sections : vidéo, distribution, éclairage, chauffage, alarme incendie, intrusion, lecteur de carte, communication, urgence, contrôle d'éclairage, service, horloge, intercom et câblage structuré.
- Les quantités sont **globales**. Aucune n'est donnée par feuille : le détail par feuille ci-dessous ne vient donc que de l'IA.
- La page 1 (sommaire) porte des notes manuscrites sans valeur (« TEMPORAIRE = … »). Aucune ligne n'est illisible.
- La référence a été montée sur les plans **avant addendas**. C'est démontré au § 4 (alarme incendie) : les écarts s'annulent exactement quand on retire les modifications E-01 et E-02.
- La référence a des doublons de section. « DETECTEUR MOUVEMENT 14 » paraît deux fois, et les caméras sont reprises dans la section intrusion (14 + 14). Ces doublons sont comptés une seule fois.

## 1. Hors périmètre (compté par la référence, non relevé par l'IA)
Tout ce qui se mesure en pieds ou relève de l'accessoire est hors périmètre : conduits, câbles, boîtes carrées ou octogonales, couvercles, raccords, supports, plywood, boom truck, pépine, poteau 30 pi, tiges de M.A.L.T., prix de lot, quincaillerie, coupe-feu, drops, blocs d'alimentation de commandes, Panduit, alimentations 0-10 V (450), RIZE et bases de lampadaire ou de bollard. Au total, 397 lignes transcrites, dont 239 hors périmètre (en « P » ou en accessoire).

## 2. Correspondance des nomenclatures
| Référence (ACCEO) | Libellé(s) IA | Justification |
|---|---|---|
| FIXTURE TYPE xx | Luminaire xx | Même code du tableau T-01 |
| DETECTEUR MOUVEMENT… (contrôle éclairage) 83 | Détecteur de mouvement (« D ») | Légende E001 : « D » = détecteur de mouvement |
| INTERRUPTEUR B/V, GRADATEUR, INTERRUPTEUR A DÉTECTEUR, interrupteur 15A | — | Non relevé (R-009) |
| LUMACELL LS1WU/LS2WU/MQM1/MDML (81) + RG12S (8 accus) | Appareil d'urgence à typer (89) | Chaque « A »…« H » marque un appareil **ou un accumulateur** : `urgence-E201-accuE.png` (le « E » du local 106 est un accumulateur) |
| STATION MANUEL 10 | Station manuelle 8 + Station manuelle c/a garde 2 | |
| KLAXON/STROB 31 | Mini-klaxon M/K | 29 marques + 2 M/K retirés par l'addenda E-02 .3.1 = 31 (`alarme-E401-MK-*.png`) |
| KAXON 13 / STROB 23 | Klaxon 13 / Strobe 10 + Klaxon-strobe 10 | Voir § 4 |
| DÉTECTEUR DE GAINE | Détecteur de conduit RCFF/RCFU | |
| RELAIS ADRESSABLE 16 + MODULE ADRESSABLE 7 | Module RA 17 + MD 2 + MS 2 | |
| CAMERA 12 + CAMERA DOME 14 (vidéo) | Caméra (« C ») | |
| BOITIER ALIMENTATION (intrusion) 6 | « Bouton anti-agression » (BA) 6 | Le bouton anti-agression est un « B » dans un carré (légende E001, `legende-gache-BA.png`). « BA » n'est pas dans la légende : erreur de type, pas de quantité |
| GACHE 1 | Gâche électrique 12 | 11 des 12 sont des « G » noirs = GRILLAGE DE PROTECTION (§ 4) |
| tel/data 96 (câblage structuré) | Sortie informatique 74 + 1070mm 17 + tél+info 3 + tél 2 = 96 | |
| WIFI / HDMI / HORLOGE + 2 FACE | Borne WiFi / Boîte HDMI / Horloge numérique | |
| INTERCOM 29, HAUT PARLEUR 38 | PMI 1, HP plafond 2, trompette 2 | Non relevé (R-011) |
| prise duplex 15A 178 + usb 12 + 15/20A 31 + GFI 36 + GFI WP 3 + poêle, sécheuse, toit | Toutes les « Prise … » | Regroupées en famille (voir § 3) |
| SCAS / SHU / WFA / ALUX3 / THERMARAY | Convecteur B / Aérotherme C / Aérotherme A / Plinthe D / Panneau radiant E | Tableau T-03 |
| RELAIS TRANSFO 347/24V 42 | Relais triac chauffage (RT) 42 | |
| PP1, PP1, CDP1, PP2, CDP2, P1–P6, PA, PB (13) ; T1/T2 (2) | Panneau de distribution 8 | |
| 30A 600V 58 | Sectionneur thermopompe 33 + Sectionneur 30A 5 + 30A F15A 3 | |
| THERMOPOMPE, SERPENTIN, RACCORD DIRECT, moteurs, CE, chaudière… | Raccordement … | |

## 3. Tableau d'écart par famille (objets communs)
| Famille | Réf. | IA | Écart | % | Explication (preuve au § 4) |
|---|--:|--:|--:|--:|---|
| Luminaires | 525 | 526 | +1 | +0,2 % | E3 : 73 contre 72. Indécidable, écart < 2. La paire douteuse du local 125 correspond bien à 2 luminaires (`lum-E3-E201-775.png`) |
| Commandes : détecteurs de mouvement | 83 | 89 | +6 | +7,2 % | Échantillon : chaque « D » est bien un symbole de détecteur (`det-E201-*.png`). Indécidable, IA probablement juste |
| Commandes : interrupteurs et gradateurs | 101 | 0 | −101 | −100 % | **Réserve R-009** |
| Secours (appareils + accumulateurs) | 89 | 89 | 0 | 0 % | Compte juste, mais non typé. Les 8 accumulateurs sont rangés comme « appareils » (R-010 dit à tort qu'ils ne sont pas localisés) |
| Alarme incendie (panneau, stations, fumée, gaine, signalisation, retenues, modules, isolateurs) | 158 | 148 | −10 | −6,3 % | Addendas (−5 en signalisation, +2 en gaine) ; 6 isolateurs absents du plan (aucun « ISO » sur E401/E402) |
| Sécurité, intrusion, contrôle d'accès, caméras | 133 | 116 | −17 | −12,8 % | Caméras −10 (le plan en montre 16) ; gâches +11 (faux positifs) ; panneaux d'accès 4, boîtiers d'alimentation 13, sirène et coffret à clé : aucune marque |
| Télécom (sorties, WiFi, HDMI, horloges, TV) | 201 | 201 | 0 | 0 % | Horloges +1, TV −1 |
| Intercom (postes, haut-parleurs) | 67 | 5 | −62 | −93 % | **Réserve R-011** |
| Prises (y compris poêle, sécheuse, toit, WP) | 263 | 245 | −18 | −6,8 % | Au moins 5 prises oubliées, prouvées, hors des zones de R-013 |
| Distribution (panneaux, transformateurs, camlock, sectionneurs, démarreurs) | 79 | 50 | −29 | −36,7 % | Salle électrique 136.1 oubliée ; T1 et T2 relevés comme thermostats ; 58 contre 41 sectionneurs |
| Mécanique (raccordements) | 88 | 84 | −4 | −4,5 % | Catégories différentes (le « RACCORD DIRECT 12 » de la référence est générique). Indécidable |
| Chauffage (appareils + relais) | 175 | 178 | +3 | +1,7 % | 4 faux positifs C/E sur des chauffe-eau (+2 C, +2 E) ; B −2, D +1 |
| **Total, hors R-009 et R-011** | **1 794** | **1 726** | **−68** | **−3,8 %** | Somme des écarts absolus : 88 (4,9 %) |
| **Total, toutes familles** | **1 962** | **1 731** | **−231** | **−11,8 %** | |

Hors catégorie (sans équivalent ACCEO) : 16 « Thermostat BT T », dont 2 sont en réalité les transformateurs T1 et T2 ; 2 interrupteurs de débit ID ; 3 sondes basse température ; 4 boîtes de jonction ; 1 boîtier de communication.

### Détail par feuille (IA) pour les familles dont l'écart n'est pas nul
| Famille | E101 | E201 | E202 | E301 | E302 | E401_2 | E402 | E701_2 | E702 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Luminaire E3 | | 55 | 18 | | | | | | |
| Détecteurs de mouvement | | 62 | 27 | | | | | | |
| Alarme incendie (hors ID) | | | | | | 81 | 67 | | |
| Sécurité et caméras | | | | | | | | 112 | 4 |
| Prises | 1 | | | 160 | 84 | | | | |
| Distribution + sectionneurs | 1 | 1 | | 24 | 24 | | | | |
| Mécanique (+1 sur E002) | 1 | | | 41 | 41 | | | | |
| Chauffage + relais | | | | 111 | 67 | | | | |

Ce tableau ne donne que la répartition de l'IA ; la référence n'a pas de répartition par feuille.

## 4. Vérification des écarts de 2 objets ou plus
| # | Écart | Qui a raison | Preuve |
|---|---|---|---|
| 1 | Gâches : IA 12, réf. 1 | **Référence** | E701_2 : un seul « G » violet (0x9900cc, x 765, y 970, dans un carré à côté du REX) = gâche selon la légende. Les 11 autres « G » sont noirs (x 209 à 849, y 462 à 952), à côté de HOR ou WF. Légende E001 (x 1831, y 1224) : « G = GRILLAGE DE PROTECTION ». Fichiers `gache-E701-rangee.png`, `legende-G-noir.png` |
| 2 | Panneaux : IA 8, réf. 13 ; transformateurs : IA 0, réf. 2 | **Référence** | E301, salle électrique (x 1070 à 1180, y 1560 à 1650) : CDP1, P1, PA, PP1 et T1 n'ont aucune marque de panneau, et T1 est relevé comme « Thermostat BT T ». E302 (x 1075, y 988) : T2, idem. Fichiers `distrib-E301-salle-elec-136.png`, `distrib-E302-T2.png` |
| 3 | Prises : −18 | **Référence** (au moins 5 prouvées) | E301 (x 630 à 727, y 934) : 3 prises P1,16 / P1,16 / P1,12 et 1 sortie de données sans marque. E301 (x 1276, y 854), secrétariat 101.5 : 2 prises P2,21 et 1 sortie de données sans marque. Ni l'une ni l'autre zone n'est citée dans R-013. Fichiers `prises-E301-630-934.png`, `prises-E301-1276-854.png`. Les multiplicateurs « 3x M.O. » et « 2x M.O. » sont bien traités (`prises-E301-1742-798.png`, `prises-E301-2072-720.png`) |
| 4 | Caméras : IA 16, réf. 26 | **IA** au regard du plan | E701_2 : 16 symboles « C » violets, soit 14 extérieurs CAM-01-01 à 14 et 2 intérieurs (vestibule). Aucune caméra sur E702. Les 26 de la référence ne sont pas sur les plans (devis ou vidéo au lot ?). Fichiers `cam-E701-170.png`, `cam-E701-890.png` |
| 5 | Signalisation d'alarme incendie : IA 62, réf. 67 | **IA** (addendas) | Retour à l'état avant addendas à partir des notes IA : M/K 29 + 2 = **31** (réf. 31) ; strobes 10 + 4 annulés + B1 + B9 + 2 au gymnase + 113/115 + 209/211 = **22** (réf. 23) ; klaxons 13 + 2 retirés − 2 ajoutés = **13** (réf. 13). La référence ignore E-01 et E-02 |
| 6 | Détecteurs de gaine : IA 25, réf. 23 | **IA** (addenda) | E-01 .6 ajoute 2 détecteurs de conduit pour REC-001 (E402) ; 25 − 2 = 23 |
| 7 | Sectionneurs 30A : IA 41, réf. 58 | Indécidable (IA probable) | Chaque TP a un « 30A » dessiné au plan, et l'IA en compte un par TP (`sect-E301-corridor.png`, `sect-E301-540-1400.png`). 58 = 33 TP + 22 serpentins + 3, alors que E-02 .6.2 rend le sectionneur des serpentins intégré (fourni par la mécanique) |
| 8 | Aérotherme C +2 et panneau radiant E +2 | **Référence** | E302 (x 598 et 624, y 988) : les cercles « C/E » sont les symboles des chauffe-eau CE-001 et CE-002. L'IA a lu C comme aérotherme et E comme panneau radiant. Corrigés : C = 4 et E = 68, comme la référence. Fichier `chauff-E302-C-600.png` ; les C réels sont dans `chauff-E301-C-150.png` et `chauff-E301-C-1011.png` |
| 9 | Convecteur B −2 | Indécidable | Les 29 étiquettes « B » de E301 et E302 sont toutes relevées. Les seuls « B » écartés sont la bulle d'axe (x 108, y 589) et le tableau T-03 (x 1397, y 1472) (`chauff-E301-BD-1397.png`). L'écart vient probablement d'une révision ou de la cédule |
| 10 | Détecteurs de mouvement +6 | Indécidable | Les « D » échantillonnés sont tous de vrais détecteurs (`det-E201-1905.png`, `det-E201-436.png`) |
| 11 | Modules −2 ; isolateurs −6 | Réf. (devis) / IA (plan) | Aucun « ISO » sur E401 ni E402. Les multiplicateurs « 6x MS » et « 3x ID » à l'entrée d'eau sont comptés 1 fois (R-012 les signale) |
| 12 | Grillages (strobes 6, horloges 2, haut-parleurs 4) : IA 0 | **Référence** | Les 6 « G » de E401_2 (x 206 à 864) ont été écartés comme « trompettes » (R-017) : ce sont des grillages de protection |
| 13 | Intercom −62 ; interrupteurs et gradateurs −101 | **Référence** | Signalé : R-011 et R-009 |
| 14 | Boîtier d'alimentation 6 = « Bouton anti-agression » 6 | Quantité juste, type faux | `ba-E701-1214.png` et `legende-gache-BA.png` |

### 10 marques IA tirées au hasard (`random.seed(1693)`, `random.sample` sur texte + visuel) — `hasard-montage.png`
| # | Feuille | Libellé | x, y (pt) | Verdict |
|---|---|---|---|---|
| 1 | E301 | Prise DDFT 5-15R 1070mm | 610, 1778 | OK |
| 2 | E201 | Luminaire E6 | 1752, 1203 | OK |
| 3 | E201 | Luminaire M1 | 162, 922 | OK |
| 4 | E401_2 | Module MS | 1075, 719 | Objet OK. Le symbole voisin « 6x MS » ne compte que pour 1 (R-012) |
| 5 | E201 | Luminaire E1A | 1575, 998 | OK |
| 6 | E701_2 | Bouton handicapé (H) | 2747, 885 | OK |
| 7 | E302 | Prise double 5-15R | 1696, 631 | OK |
| 8 | E401_2 | Module RA | 2693, 950 | OK |
| 9 | E301 | Prise micro-onde (3x M.O.) | 891, 815 | OK |
| 10 | E701_2 | Borne WiFi | 668, 1288 | OK |
Résultat : 10 marques sur 10 sont posées sur le bon objet. Une seule a une quantité sous-estimée (multiplicateur).

## 5. Verdict
- **Écart net sur les objets communs** : −68 sur 1 794 (−3,8 %) hors R-009 et R-011. Avec les familles réservées, l'écart est de −231 sur 1 962 (−11,8 %).
- **Critère Francis** (≤ 10 % par poste) :
  - respecté : luminaires (+0,2 %), secours (0 %), télécom (0 %), chauffage (+1,7 %), mécanique (−4,5 %), prises (−6,8 %), alarme incendie (−6,3 %) ;
  - non respecté : **distribution (−36,7 %)**, **sécurité et caméras (−12,8 %)**, et les postes réservés interrupteurs (−100 %) et intercom (−93 %) ;
  - total : ≤ 5 % seulement si l'on exclut les réserves.
- **Items manquants non signalés en réserve** (le critère exige aucun) :
  1. les panneaux PP1, CDP1, P1 et PA et les transformateurs T1 et T2 ;
  2. les grillages de protection (≥ 17 « G ») ;
  3. au moins 5 prises et 2 sorties de données hors des zones citées dans R-013 ;
  4. les panneaux de contrôle d'accès (4), les boîtiers d'alimentation de sécurité (13), la sirène et le coffret à clé ;
  5. les démarreurs combinés et les variateurs (5 + 4).

  **Le critère n'est pas respecté.**
- **Phrase honnête** : le relevé n'est **pas utilisable tel quel**. Il est fiable pour les luminaires, les sorties télécom, le WiFi, le HDMI, les horloges, les relais, les thermopompes et les serpentins, et il applique correctement les addendas, ce que la référence ne fait pas. Un estimateur doit encore :
  - relever les interrupteurs, les gradateurs et l'intercom ;
  - ajouter la salle électrique et les transformateurs ;
  - retirer les 11 fausses gâches et les 4 faux C/E ;
  - retyper les BA en boîtiers d'alimentation, les T1 et T2 en transformateurs, et l'urgence (appareils et accumulateurs) ;
  - reprendre les multiplicateurs « Nx ».

## 6. Erreurs systématiques de l'IA (règles à corriger)
1. **Une lettre seule est interprétée hors contexte** :
   - « G » (grillage) pris pour une gâche ;
   - « T1 »/« T2 » (transformateurs) pris pour des thermostats ;
   - « C/E » (chauffe-eau) pris pour un aérotherme C et un panneau radiant E ;
   - « BA » pris pour un bouton anti-agression ;
   - « G » de E401 écarté comme « trompette ».

   Règle à ajouter : vérifier la **couleur de discipline** (le violet 0x9900cc = sécurité) et la **forme d'encadré** de la légende, et rejeter toute lettre qui n'a pas la même forme.
2. **Les salles électriques et les équipements de distribution sans étiquette de circuit ne sont pas relevés.** Règle : apparier le plan avec E501 et E502 (liste des panneaux et transformateurs) avant de conclure.
3. **Un multiplicateur « Nx » est compté pour 1** (6x MS, 3x ID).
4. **Prises visuelles : il reste des trous hors des zones déclarées.** Règle : contrôle par script de chaque étiquette de circuit « Pn, xx » sans marque à moins de 40 pt. Ce contrôle trouve 10 étiquettes orphelines sur E301.
5. **Les accumulateurs sont confondus avec les appareils d'urgence** (même étiquette « A »…« H »). Règle : typer selon le symbole de la légende E001.

## 7. v1 → v2
La v1 est `archives/S-1693-v1/` : une passe interrompue (`.en-cours`), avec `occurrences-texte.csv` seul, 1 384 marques, sans relevé visuel, sans rapport et **sans ecart.md**. La comparaison porte donc sur les totaux des deux relevés.

| Famille | v1 | v2 | Réf. |
|---|--:|--:|--:|
| Luminaires | 526 | 526 | 525 |
| Détecteurs de mouvement | 89 | 89 | 83 |
| Secours | 0 | 89 | 89 |
| Alarme incendie | 84 (M/K, RCF, RA, RM, ID, MS, PAI) | 148 | 158 |
| Sécurité et caméras | 84 (caméras 14 par CAM-id) | 116 | 133 |
| Télécom (hors intercom) | 105 (sans sorties de données) | 201 | 201 |
| Prises | 251 (« Prise 120V (circuit) », non typées) | 245 | 263 |
| Chauffage (+ RT) | 132 + 40 | 178 | 175 |
| Mécanique | 73 | 84 | 88 |
| Distribution | 0 | 50 | 79 |
| **Total** | **1 384** | **1 765** | — |

Ce que la v2 a corrigé :
- les stations, détecteurs de fumée, klaxons et strobes (absents de la v1) ;
- les sorties de données (0 → 96) ;
- l'urgence ;
- les addendas ;
- le typage des prises et du chauffage ;
- la distribution, partiellement.

Ce qui a **régressé** :
- les 11 fausses gâches (aucune en v1) ;
- les 4 faux C/E et les T1/T2 lus comme thermostats (le chauffage passe de 132 à 136 appareils) ;
- les prises : 251 → 245 au total, alors que la référence en compte 263.

Ce qui n'est pas corrigé : les interrupteurs, l'intercom et le « BA ».
