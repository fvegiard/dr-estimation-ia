# STATUT — relevé automatique « S-1835 »

Date : 2026-09-23 16:50 · État : **TERMINÉ (partiel : addenda télécom T-01 non intégré)**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 49-366 (D) - ESBG - Addenda - E-01 - Plans.pdf | 4553010 | 81ee16087a961da4cceab42b5c8c7559a4ad165eaa05b419426e0f22104b0ada |
| 49-366 (D) - ESBG - Addenda - E-01.pdf | 185553 | e7712be8b86cfcaaf0f029b24af7098bd8d1bd3b48dcd32bd0b8143419c00a64 |
| 49-366 (D) - ESBG - Plans de télécommunications_12 pages.pdf | 4435312 | 7d9d333b682667b189a4577792ac55207c781e3943c9f9ec10c73c3a5205a125 |
| 49-366 (D) - ESBG - Plans électriques_10 pages.pdf | 5787167 | fc66fbe5caeb63c3d42a273123ffaac010877355a2092d447a46d3de08cdfe2e |

Note : l'addenda télécom T-01 (`...Addenda - T-01 (2).pdf` et `...Addenda - T-01 - Plans (2).pdf`) est présent dans l'inventaire Drive (`docs/inventaire-drive-2026-09-23/...`) mais n'a pas été ingéré dans ce relevé.

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1835-Dossier-complet.pdf | 14461998 | 6ab20f364199c6bdf08de4f522c8a350a693dd1bad626e0840fb957366cdcab3 |
| S-1835-Plans-annotes.pdf | 14292450 | 6d28ecf2e93e2fb12296257f96c50a298adcd101ccc662cc45f0989b753b8cb4 |
| S-1835-Rapport-de-metre.md | 16529 | 339cbc16f3e3705f7b52b57ba534a17b04e4ec4cd1c38757c9ba274e69472978 |
| S-1835-Rapport-de-metre.pdf | 169833 | 8c3e0841f90325b4e7963e0a6a848eebdc3d63fcd8fbf123c6874f815a2934ba |
| journal-etapes.log | 1347 | 73b499c34ffe052981a1c42c02c490d01bed500c2a3f7927f39b086b2f6ce89b |
| S-1835-planexpert/S-1835.qpl | 253184 | 1ae4d23735a9779f3a8f3fdd933dc369e7b83e55dab32296ca21203f463a2e55 |

Le projet Plan Expert `S-1835.qpl` est dans `S-1835-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| build_qpl | 0.0 min | ok |
| render_pdf | 0.2 min | ok |
| total | 0.2 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : None · sous-type : None
- coût estimé (client, `total_cost_usd`) : None $ US
- jetons : entrée None, cache créé None, cache lu None, sortie None
- session : `None` · dossier de travail : `/home/claude/releve-auto/runs/S-1835/OUTBOX/S-1835/travail`

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
11. **R-011 — Télécom.** Les haut-parleurs plafond (disque noir Ø 10,6 pt) ont été comptés par lecture vectorielle : 152 sur D410-D422 et **0 sur D400-D403 (sous-sol)**. Le 0 est à vérifier visuellement. Aucun autre symbole télécom n'a été compté (la note dit qu'aucun câble ne doit être démantelé). La note vise les blocs B, C et C1 : les haut-parleurs du bloc D (D413, D422) sont comptés quand même, à confirmer. **Ce résultat est provisoire tant que l'addenda T-01 télécom n'est pas ingéré et comparé feuille par feuille.**
12. **R-012 — Repères EAC (54).** Ils sont relevés par étiquette, en famille `autre`, comme « existant à conserver ». Ce sont des panneaux et des équipements muraux (R-3, CDP-1…), sans travaux.
13. **R-013 — Relevé non exhaustif hors calques.** Les symboles hors WIPEOUT et hors calque E-* ne sont pas captés. Aucun parcours tuile par tuile complet n'a été fait (volume : plus de 3 000 symboles).
