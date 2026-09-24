# STATUT — relevé automatique « S-1835 »

Date : 2026-09-24 16:55 · État : **TERMINÉ** (addendas E-01 et T-01 intégrés ; reprise T-01 du 2026-09-24)

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 49-366 (D) - ESBG - Addenda - E-01 - Plans.pdf | 4553010 | 81ee16087a961da4cceab42b5c8c7559a4ad165eaa05b419426e0f22104b0ada |
| 49-366 (D) - ESBG - Addenda - E-01.pdf | 185553 | e7712be8b86cfcaaf0f029b24af7098bd8d1bd3b48dcd32bd0b8143419c00a64 |
| 49-366 (D) - ESBG - Addenda - T-01 - Plans.pdf | 2372905 | 6c24fcdfed44d107a81b0609aa08aa019e78ed8a6d7286879733a9a03069842b |
| 49-366 (D) - ESBG - Addenda - T-01.pdf | 888465 | c96423f9fb1f73745ba0cfe8dfeb5573ade30d958d8b37ad41f5bef394226fc9 |
| 49-366 (D) - ESBG - Plans de télécommunications_12 pages.pdf | 4435312 | 7d9d333b682667b189a4577792ac55207c781e3943c9f9ec10c73c3a5205a125 |
| 49-366 (D) - ESBG - Plans électriques_10 pages.pdf | 5787167 | fc66fbe5caeb63c3d42a273123ffaac010877355a2092d447a46d3de08cdfe2e |

## Addendas

| addenda | fichiers d'entrée | feuilles | traitement |
|---|---|---|---|
| E-01 (20 août 2024) | `…Addenda - E-01.pdf`, `…Addenda - E-01 - Plans.pdf` | E002_ADD, D210_ADD … D222_ADD ; texte D210_ADD_2 | remplacent E-002 et E-D210 à E-D222 (R-001) |
| T-01 (18 août 2026) | `…Addenda - T-01.pdf`, `…Addenda - T-01 - Plans.pdf` | D420_ADD, D421_ADD, D422_ADD ; texte D420_ADD_2 | remplacent T-D420 à T-D422 ; comparaison vectorielle et zooms dans `preuves-t01/` (R-014 à R-017) |

## Addendas non intégrés

- `49-366 (D) - ESBG - Addenda - ADM-01 (1).pdf` — absent de l'INBOX de ce relevé, non lu ; addenda administratif d'après son nom (ADM), à confirmer (R-018)
- `Addenda/` — sous-dossier non détaillé par l'inventaire Drive, contenu inconnu (R-018)

## Haut-parleurs : avant / après l'addenda T-01

Sous-sol D400–D403 : 0 haut-parleur, vérifié (aucun symbole télécom noir sur les 4 feuilles, `preuves-t01/zooms/sous-sol-*.jpg`).

| feuille | avant | après | écart |
|---|--:|--:|--:|
| D400 | 0 | 0 | +0 |
| D401 | 0 | 0 | +0 |
| D402 | 0 | 0 | +0 |
| D403 | 0 | 0 | +0 |
| D410 | 23 | 23 | +0 |
| D411 | 27 | 27 | +0 |
| D412 | 3 | 0 | -3 |
| D413 | 13 | 13 | +0 |
| D420 | 41 | 0 | -41 |
| D421 | 36 | 0 | -36 |
| D422 | 9 | 0 | -9 |
| D420_ADD | 0 | 38 | +38 |
| D421_ADD | 0 | 32 | +32 |
| D422_ADD | 0 | 9 | +9 |
| TOTAL | 152 | 142 | -10 |

## Libellés : avant / après

| libellé | avant | après | écart |
|---|--:|--:|--:|
| Alarme existante — à classer | 4 | 4 | +0 |
| Dém. chauffage — à classer | 3 | 3 | +0 |
| Dém. luminaire 1x4 / segment linéaire | 1888 | 1888 | +0 |
| Dém. luminaire 2x2 | 6 | 6 | +0 |
| Dém. luminaire 2x4 | 554 | 554 | +0 |
| Dém. luminaire rond encastré | 85 | 85 | +0 |
| Dém. prise plafond projecteur | 13 | 13 | +0 |
| Dém. éclairage — à classer | 27 | 27 | +0 |
| Détecteur fumée existant — dépose/repose temp. | 192 | 192 | +0 |
| Détecteur sécurité (M) — par autres | 13 | 13 | +0 |
| Haut-parleur classe — par autres | 3 | 3 | +0 |
| Haut-parleur existant — dépose/entreposage | 152 | 142 | -10 |
| Luminaire 24h existant — dépose/repose temp. | 218 | 218 | +0 |
| Prise existante — à classer | 4 | 4 | +0 |
| Repère EAC — existant à conserver | 54 | 54 | +0 |
| Station manuelle existante (F) — à confirmer | 32 | 32 | +0 |
| Éclairage existant carré — à classer | 55 | 55 | +0 |
| Éclairage existant — à classer | 5 | 5 | +0 |
| TOTAL | 3308 | 3298 | -10 |

Tables produites par `preuves-t01/analyse_t01.py` (fichiers `avant-apres-*.csv`).

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1835-Dossier-complet.pdf | 14574115 | c0c88b08331a9807f9b6c0033556af5f95776b9384ea5bae9e9f320f7486ac9f |
| S-1835-Plans-annotes.pdf | 14402388 | 1e75402659c0ec624a280d0251d012662795a098841cb4bd0e5ce3d0a555028f |
| S-1835-Rapport-de-metre.md | 19418 | 8401e4f781947dffb4a764530032bc4c9ea83a431adf59e1af3f3f45d300c399 |
| S-1835-Rapport-de-metre.pdf | 172015 | 5f3b3f82cce97dfc5a3479157faf8f1da0b0436c6dcafe4174ed1a8035ce4eed |
| S-1835-planexpert/S-1835.qpl | 254878 | 8e9d3a31a9e5ac2e8b1d30880654a66120b882ea403f8669cedaafd488a642e6 |

Le projet Plan Expert `S-1835.qpl` est dans `S-1835-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| build_qpl | 0.0 min | ok |
| render_pdf | 0.1 min | ok |
| total | 0.1 min |  |

## Reprise addenda T-01 (sans agent, 2026-09-24)

- `prepare.py` sur les 6 fichiers d'entrée ci-dessus → 35 feuilles ;
- `preuves-t01/analyse_t01.py` : détection vectorielle des haut-parleurs, recalage des feuilles d'un même étage, comparaison original/T-01, réécriture des occurrences (seul le libellé haut-parleur change) ;
- `preuves-t01/zooms_t01.py` : zooms `releve/zoom.py` côte à côte ;
- `preuves-t01/publier_t01.py` : `build_qpl.py`, `render_pdf.py` (RELEVE_NATIF=0), `releve.xlsx`, ce STATUT ;
- relevé de l'agent d'origine (claude -p headless, 2026-09-23) conservé pour tous les autres libellés.

## reserves.md

# Réserves — S-1835 École secondaire Bernard-Gariépy (démolition phase 1)

1. **R-001 — Addenda E-01 appliqué.** Les 8 feuilles d'addenda (E-002, E-D210 à E-D222 rév. 01) remplacent la version de base (classées `remplacee`, non relevées). Changement majeur : la note générale devient « tous les équipements montrés sont existants À ENLEVER » (la base disait « EAC » partout, ×101 sur D210 contre ×14 sur l'addenda) et 7 notes spécifiques sont ajoutées (24 h, DEL remise au propriétaire, détecteurs de fumée, enseignes de sortie, projecteurs, décontamination). L'addenda annonce aussi l'« ajout des travaux en alarme incendie » à E-002 (devis) : il n'y a aucun symbole à compter, voir le devis.
2. **R-002 — D210_ADD_2 n'est pas un doublon.** C'est le texte de l'addenda (1 page) ; il est classé `autre`.
3. **R-003 — Méthode vectorielle.** Il y a des milliers de symboles pointillés. Ils ont été comptés par lecture des calques CAO du PDF d'addenda : masque WIPEOUT + calque du symbole (E-D-* = démolition, E-E-* = existant). La classification se fait selon la taille du masque. Contrôle visuel fait par zoom sur D210_ADD seulement (luminaires 2x4, 24 h hachurés, détecteurs de fumée, drapeau F, M pointillés). **Échantillonnage à étendre aux autres feuilles.**
4. **R-004 — Rangées linéaires.** Le libellé « Dém. luminaire 1x4 / segment linéaire » compte chaque segment de 35 pt (≈ 1,2 m, soit 4 pi à 1:100) : une rangée continue est donc comptée en segments. Il faut confirmer si l'estimateur compte les rangées ou les luminaires 4 pi. Il faut aussi ajouter 2 hypothèses : les 9x35 isolés sont des 1x4, et les 17x35 sont des 2x4 (sans vérifier le type exact de chaque appareil).
5. **R-005 — Note 2 (luminaires DEL à remettre au propriétaire) et note 7 (décontamination).** Ces luminaires n'ont pas été séparés des autres démolitions. Les bulles de notes (calque E-000-GEN, 17x17) ne sont pas comptées comme appareils. Il faut les répartir par bulle si l'estimateur chiffre la remise au propriétaire à part.
6. **R-006 — « Luminaire 24h existant — dépose/repose temp. ».** Le calque E-E-200-ECL-EQP comprend les 24 h hachurés (note 1). Ce calque peut aussi contenir des luminaires EAC réellement conservés près des repères EAC : ils sont comptés quand même. À vérifier.
7. **R-007 — Symboles à classer.** 55 « carré mi-noir 11 pt » existants (unité d'urgence ? enseigne de sortie, note 4 ?), 27 éléments d'éclairage à enlever de forme non standard, 5 éléments d'éclairage existants, 4 éléments d'alarme, 4 prises existantes et 3 éléments de chauffage (symbole à croix, calque E-D-500-CHA). Tous sont à identifier avec la légende E-001.
8. **R-008 — Enseignes de sortie (note 4).** Aucun calque de démolition dédié n'a été trouvé. Elles sont possiblement dans « Éclairage existant carré — à classer ». Le compte séparé n'est pas fait.
9. **R-009 — Par autres.** Les caméras, bornes Wi-Fi, projecteurs et haut-parleurs de classe sont retirés par le CSSST (note générale 01). Les symboles M pointillés (calque E-D-400-SEC, 13) et les haut-parleurs du calque E-D-400-COM (3) sont relevés sous des libellés « par autres » : ils ne sont pas chiffrés par DR. L'interprétation « M » = détecteur de mouvement / caméra est à confirmer.
10. **R-010 — « Station manuelle existante (F) ».** Le symbole drapeau + F est existant et n'est pas explicitement visé par une note d'enlèvement. Il est compté à part, à confirmer (hors travaux ?).
11. **R-011 — Télécom (haut-parleurs).** Les haut-parleurs d'appel général (disque noir Ø 10,6 pt dans un carré pointillé ; légende T-001 « encastré plafond », la variante murale a le même disque) sont relevés par lecture vectorielle : **142** après l'addenda T-01 (D410 23, D411 27, D413 13, D420_ADD 38, D421_ADD 32, D422_ADD 9). Sous-sol D400–D403 : 0 disque noir et aucun tracé noir de symbole télécom, **le 0 est vérifié** (`preuves-t01/zooms/sous-sol-*.jpg`). Aucun cercle vide « en surface » ni « HP extérieur » sur les plans. Aucun autre symbole télécom n'est compté (note : aucun câble ne doit être démantelé). Bloc D : les notes de T-D403 et T-D413 disent « démantelés, ne doivent pas être entreposés », alors que le libellé dit dépose/entreposage ; les 13 haut-parleurs de D413 et les 9 de D422_ADD (sa note reprend la formule des blocs B, C et C1) restent sous ce libellé, à ventiler si l'estimateur chiffre le démantèlement à part.
12. **R-012 — Repères EAC (54).** Ils sont relevés par étiquette, en famille `autre`, comme « existant à conserver ». Ce sont des panneaux et des équipements muraux (R-3, CDP-1…), sans travaux.
13. **R-013 — Relevé non exhaustif hors calques.** Les symboles hors WIPEOUT et hors calque E-* ne sont pas captés. Aucun parcours tuile par tuile complet n'a été fait (volume : plus de 3 000 symboles).
14. **R-014 — Addenda T-01 appliqué.** Le texte (18 août 2026, 1 page, feuille `D420_ADD_2`) et les 3 plans T-D420, T-D421 et T-D422 rév. 1 remplacent les originaux (classés `remplacee`). Seul changement écrit : protéger le conduit de 63 mm de la fibre optique B-111.4 ↔ D-132.2 (note spécifique 1 de T-D420 : S-006 → B-111.4 par S-003 et B-116). Comparaison vectorielle des 3 feuilles (`preuves-t01/preuves-t01.md`) : T-D422 est le même dessin décalé de 239,7 pt (94,5 % de tracés communs) ; T-D420 et T-D421 recadrent les vues (81,9 % et 86,9 % de tracés communs). Haut-parleurs : 86 sur les originaux, 79 sur T-01, 0 nouveau.
15. **R-015 — Chevauchement D420/D421 et haut-parleur retiré par T-01.** Les vues originales D420 et D421 se recouvraient (6 haut-parleurs dessinés deux fois, donc comptés deux fois dans le relevé précédent). T-01 supprime ce recouvrement : 5 de ces haut-parleurs restent comptés une fois sur l'autre feuille T-01, et 1 (corridor, D420 (2083,6, 1860,9) = D421 (653,8, 1859,4)) n'est plus dessiné sur aucune feuille T-01. Le texte de l'addenda n'en parle pas : il n'est pas compté (la version d'addenda prime), à confirmer auprès de l'ingénieur.
16. **R-016 — Doublons RDC D411/D412.** D411 et D412 montrent la même bande de plan (recalage -519,0 / -903,5 pt, 22,3 % de tracés communs) : les 3 haut-parleurs de D412 sont ceux de D411 (locaux C-025, C-028…). Comptés une fois sur D411, retirés de D412 (`preuves-t01/marques-retirees.csv`). Aucune autre paire de feuilles d'un même étage ne se recouvre (meilleure part commune 3,1 %, `preuves-t01/recalage-feuilles.csv`).
17. **R-017 — Protection du conduit de fibre optique (T-01).** Sujétion sans symbole : pas de compteur. Tracé ajouté par T-01 (traits noirs de 0,42 pt des 3 feuilles, bande de raccord comprise) : 115,6 m à 1:100. À chiffrer en forfait ou à métrer.
18. **R-018 — Addendas non reçus.** L'inventaire Drive liste aussi « 49-366 (D) - ESBG - Addenda - ADM-01 (1).pdf » (456805 o) et « Addenda/ » (sous-dossier non détaillé). Ils ne sont pas dans l'INBOX de ce relevé et n'ont pas été lus.

