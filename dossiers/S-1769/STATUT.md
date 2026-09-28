# STATUT — relevé automatique « S-1769 »

Date : 2026-09-22 03:24 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 25-0075_E_PERM_SOUM_20260507_Signed.pdf | 3703388 | 801e057d9ddd0d09ac0c10a1b30f528f27fa7f97e087cb0c387104dc830c7b6c |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1769-Dossier-complet.pdf | 3720468 | fbc6f7bdb6f5e0f54ea213591fc95ffe97c4f9176dffa9673644d3e5ae3dca37 |
| S-1769-Plans-annotes.pdf | 3579991 | c0f2944fdf528f97bbd10dd2dee779cd54f811226084903b149b1af806fef617 |
| S-1769-Rapport-de-metre.md | 26031 | 453da53fe4813dba04f234cf1cf9994cdd4bbfb5fe120042cbf836449bfae36d |
| S-1769-Rapport-de-metre.pdf | 140820 | ed145adee0d188d09471eca6cd213e8ffa71e0c0a9e35479d4b0f4ec5c4ac15c |
| journal-etapes.log | 6409 | 896f8966378e7dcff7cd14c46b16f380ac06210f7b1711855a4181570fa270ab |
| S-1769-planexpert/S-1769.qpl | 33127 | 6ec907da6def58330c8bce312334d3c0c1d88c6f6771e535e0300ca5c5b4619d |

Le projet Plan Expert `S-1769.qpl` est dans `S-1769-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| prepare | 0.0 min | déjà à jour |
| agent Claude | 9.0 min | success / code 0 |
| build_qpl | 0.0 min | ok |
| render_pdf | 0.1 min | ok |
| total | 9.1 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : 50 · sous-type : success
- coût estimé (client, `total_cost_usd`) : 5.977594000000002 $ US
- jetons : entrée 80, cache créé 183803, cache lu 5510328, sortie 55360
- session : `ee0971be-0747-5d2f-962e-a9f568c158d0` · dossier de travail : `/home/claude/releve-auto/runs/S-1769/OUTBOX/S-1769/travail`

### Résumé de l'agent

I've written all the output files for S-1769 except `comparaison-estimateur.md`, because the `estimateur/` folder is empty. The session blocked `zoom.py`, `extract_occurrences.py`, `traits.py` and image cropping. That means none of the marks were checked with a zoom, and I read everything off the 3×4 tiles (about ±5 pt).

- **Sheets:** all 7 pages are classified. Two provisional names are swapped: `E004` is really E401 (the main plans), and `250075EPER-p04` is the real E004 (tables and details). The CSVs keep the provisional names; the real numbers are in `feuilles-classement.csv`.
- **Marks:** 141 in total: 4 from text (the $ symbols come out as the word « S ») and 137 read visually.
  - E401: 123
  - E201: 8 (exterior lights)
  - E101: 4 (200 A switch, terminal replacement, feeder to measure, circuit 22)
  - E004: 3 (electrified-door parts)
  - E003: 3 (astronomical timer and 2 occupancy sensors from spec section 2.22)
- **Legend:** 59 labels, and every label in both occurrence files exists in `nomenclature.csv`.
- **Reservations:** 28 in `reserves.md`. The main ones:
  - The corridor heater is labelled C,40,42 on the plan, but the panel schedule puts it on 28/30.
  - The D fixture may be counted twice (on both E401 and E201).
  - The occupancy sensors required by the spec aren't drawn; I counted 1 + 1 as "à confirmer".
- **Missing:** no linear lengths (panel C feeder, mini-split wiring, door cables, heated-floor area). There is no addendum and no estimator export.
- **Before building the .qpl:** run `extract_occurrences.py`, which should return the same 4 lines, and spot-check the dense areas with `zoom.py`.

## reserves.md

# Réserves — S-1769 CPE Soleil Souriant, agrandissement (26 montée Lasaline, St-Constant)

Noms de feuilles : `E004` (nom provisoire de prepare.py) = **cartouche E401** ; `250075EPER-p04` = **cartouche E004** ;
p02 = E002, p03 = E003, p05 = E101, p06 = E201. Les coordonnées sont en points PDF.

1. **R-001 — toutes feuilles — noms de feuilles.** prepare.py a nommé la page 7 « E004 » (bulle de détail) alors que le
   cartouche indique E401 ; la vraie E004 est la page 4 (`250075EPER-p04`). Les CSV gardent les noms provisoires
   (clés des fichiers) ; les vrais numéros sont dans `feuilles-classement.csv`. À corriger dans le .qpl si on affiche les numéros.
2. **R-002 — E401 (1256,480) — plinthe du corridor 140.** Étiquette lue « A 1.5 C,40,42d ». Or la cédule du panneau C
   met le MICRO-ONDE sur le circuit 40, rien sur le 42, et le CHAUFFAGE CORRIDOR 140 (1500 W) sur 28/30. Plinthe relevée
   (1500 W) ; circuit à confirmer par l'ingénieur.
3. **R-003 — méthode — outils non exécutables.** `uv run releve/zoom.py`, `extract_occurrences.py`, `traits.py` et toute
   commande de recadrage ont été refusés (pas d'approbation possible). Lecture faite sur les tuiles 3×4 et les aperçus
   seulement (≈ 5 pt de précision). `occurrences-texte.csv` a été écrit à la main selon la même règle que le script
   (fullmatch du `jeton_regex` `S` sur les mots des feuilles `plan`) : 4 mots « S » = symboles $ sur E401. À relancer
   `extract_occurrences.py` pour contrôle ; il doit redonner les mêmes 4 lignes.
4. **R-004 — E401 (402,541) / E201 (1260,629) — luminaire D.** Un D noir apparaît sur E401 hors de l'agrandissement
   (entre deux ailes existantes) et un D C,33 sur E201 au coin nord de l'agrandissement. Les deux sont relevés ; s'il s'agit
   du même appareil, retirer celui d'E401 (compter 1 D, sur E201).
5. **R-005 — E401 (640,405) et (640,552) — luminaires F et G.** Lus en bord de tuile r1c1, partiellement coupés (« F C, »
   et « G »). Types à confirmer.
6. **R-006 — E401 (543,537) et démantèlement (543,1171) — enseigne de sortie.** Noire, sans mention EE/ER, présente sur les
   deux plans : considérée comme existante à conserver, NON relevée. Idem pour les appareils gris de la zone existante
   (phares, $ à (554,554)) et le $ noir voisin de la station « F EE » (553,1188) du démantèlement : non relevés.
7. **R-007 — E401 — station manuelle.** « EAR » (546,1121) au démantèlement = « ER » (569,414) au réaménagement : comptée
   une fois (station existante relocalisée), avec le boîtier de protection de la note. La station « F EE » (545,1188) est
   comptée en démolition.
8. **R-008 — E401 — aéroconvecteur.** « EAR » (1225,1186) au démantèlement services = « ER » (1249,344) au réaménagement :
   compté une fois. Symbole (rectangle + flèche) rapproché de « aéroconvecteur mural encastré » de la légende : à confirmer.
9. **R-009 — E401 (1244,719) — cercle à trait gras hors légende** au coin sud-ouest du plan services : relevé sous
   « Cercle gras — à classer ».
10. **R-010 — E401 (1227,1121) — démantèlement services, « EE » avec flèche et boîte pointillée.** Relevé sous
    « Démol. chauffage — à confirmer » (même symbole que l'aéroconvecteur EAR voisin).
11. **R-011 — E401 — plancher chauffant, commandes.** Thermostat maître « T M » (1442,412) et sonde (1424,412) lus. Le
    thermostat esclave (1397,581) a été lu en bord de tuile (renvoi note 6) : à confirmer. La note 6 annonce deux zones
    mais une seule sonde est dessinée (note 5) : 2e sonde à confirmer.
12. **R-012 — E401 note 2 — plancher chauffant OWC-M.** Compté comme 2 zones (la note le demande, ≤ 3600 W par zone ;
    la cédule donne 4500 W sur 18/20). Surface (pi²) à métrer : non mesurée.
13. **R-013 — E003 art. 2.22 — détection de présence.** Le devis exige une détection de présence pour les corridors (a) et la
    toilette (d), sans symbole au plan. Relevé 1 + 1 « Détecteur de présence — à confirmer » ; quantité réelle à fixer.
    Minuterie astronomique (b) : 1 relevée. Dodos 136/138 (c) : gradateurs a/b relevés au plan (4).
14. **R-014 — E004 détail B / E401 — porte électrifiée (C,25 contrôle d'accès).** Relevés : raccordement porte (plan), BA,
    BJ, RA (détail). Clavier, gâche, bouton poussoir, ouvre-porte = « par d'autres » (légende), non relevés. Le fournisseur
    du verrou anti-panique B-P n'est pas précisé. Câbles C1/C2/C3 : à métrer.
15. **R-015 — E401 — échangeurs d'air ECH-1 (1309,462) et ECH-2 (1323,571).** Étiquettes seulement, sans symbole : le
    raccordement est posé sur l'étiquette.
16. **R-016 — E101 cédule circuit 22 « MÉCANIQUE » 15 A**, sans puissance ni équipement au plan : relevé
    « Raccordement mécanique circ. 22 — à confirmer ».
17. **R-017 — E101 / E004 — éléments linéaires à métrer.** Artère 3#250MCM-AL ACWU90 (+ 1#4 CU vert, C 2 po EMT) du
    panneau de répartition 600 A existant vers le panneau C : tracé absent, longueur non mesurée (1 marque « à métrer »).
    Alimentations mini-split 3#12 TECK90 (détail A notes 4-5) : à métrer.
18. **R-018 — E101 ↔ E401 — appariement cédule ↔ plan (pas de double comptage).** Circuits 1/3 éclairage, 2 batterie UA,
    4/6/8/5/7 prises, 9-16 et 10/12 chauffage, 17 frigo, 19/21 ECH-1, 23 prise extérieure, 25 contrôle d'accès,
    27/29 CD-1, 31 prise corridor, 33 éclairage extérieur (E201), 35/37 CE-1, 39/41 SE-1/SE-2, 18/20 plancher, 24/26 ECH-2,
    28/30 chauffage corridor, 32/34 CD-2, 36/38 SE-3/SE-4, 40 micro-onde : déjà relevés au plan, non recomptés sur E101.
    Seuls le circuit 22 (R-016), l'interrupteur 200 A, les borniers et l'artère sont posés sur E101.
19. **R-019 — E101 — panneau C** dessiné sur l'unifilaire modifié et au plan E401 : compté une fois (E401).
20. **R-020 — estimateur.** Le dossier `estimateur/` est vide : pas d'export Plan Expert de M. Dupuis, donc pas de
    `comparaison-estimateur.md`.
21. **R-021 — addendas.** Aucun fichier d'addenda reçu (1 seul PDF « PERM_SOUM » du 2026-05-07, révision 2).
22. **R-022 — existant hors travaux.** Le bâtiment hachuré gris d'E401 et le bâtiment gris d'E201 (panneau d'alarme FW106,
    interrupteur principal 600 A/F:600 A existants) ne sont pas relevés.
23. **R-023 — E401 note 7 (1290,637).** Renvoi « emplacement exact de la boîte de sortie » dont la cible n'a pas été
    identifiée sur la tuile ; une seule sortie data dessinée (1336,460). Autre sortie possible à confirmer.
24. **R-024 — E401 (724,605) — UA au plafond.** Nombre de têtes non lisible sur la tuile.
25. **R-025 — E401 (1370,534) C,8 et (1279,713) C,7 — prises.** Symbole noir à barre croisée, rapproché de « prise
    15-20 A GFI @ 48 po » (circuits P/D/T « comptoir » de la cédule). À confirmer.
26. **R-026 — démolition.** Aucune mention « par le bailleur / par autres / par HQ » : les 9 éléments EE sont en famille
    `demolition`, chiffrés par DR.
27. **R-027 — échelles.** Échelles impériales : 1/8 po = 1 pi (≈ 1:96) pour E401, 1/16 po = 1 pi (≈ 1:192) pour E201.
28. **R-028 — devis E002/E003.** Texte vectorisé (non extractible) ; seuls les articles 2.15 (raccordements de mécanique)
    et 2.22 (contrôle d'éclairage) ont été lus sur tuiles pour les articles sans symbole.

