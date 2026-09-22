# PIPELINE — relevé de quantités électrique dans Plan Expert (socle généralisé)

> Porté tel quel depuis `dr-releves-2026/_socle/PIPELINE.md` (voir
> `consolidation.md`). `<REPO>` désigne le dépôt de référence S-1857, en
> lecture seule.

Extrait du relevé **S-1857 Maison communautaire Saint-Michel**, réussi les 8 et 9 septembre 2026.
Objectif : pouvoir refaire le même travail sur n'importe quelle soumission.

**Règle de rédaction** : rien n'est inventé. Chaque affirmation vient d'un fichier lu dans le dépôt de
référence, cité par son chemin. Le format QPL a été **vérifié en lisant les vrais `.qpl`**, pas recopié de la
documentation ; les écarts entre la doc et le fichier réel sont signalés (§2.8).

Dépôt de référence, **lecture seule** (aucun fichier n'y a été modifié) :
`C:\Users\fvegi\.codex\workspaces\2026-09-08-install-planexpert\gitlab\saint-michel-takeoff`
noté `<REPO>` ci-dessous (vu de WSL : `/mnt/c/Users/fvegi/.codex/workspaces/2026-09-08-install-planexpert/gitlab/saint-michel-takeoff`).

Documents-sources : `<REPO>/REPRODUCTION.md`, `<REPO>/HANDOFF-SAINT-MICHEL.md`, `<REPO>/README.md`,
`<REPO>/manifest.json`, `<REPO>/INDEX.md`, `<REPO>/SHA256SUMS.txt`, plus les scripts cités un par un.

---

## 0. Vue d'ensemble : la chaîne de versions

Le relevé n'est pas un fichier, c'est une **suite de versions numérotées**. Chacune est produite par un
script hors de Plan Expert, puis **rouverte et resauvegardée par Plan Expert** avant de servir de base à la
suivante (`<REPO>/REPRODUCTION.md` §2–§6 ; `<REPO>/HANDOFF-SAINT-MICHEL.md` §2).

| Version | Contenu ajouté | Produite par | Fichier |
|---|---|---|---|
| v0 | projet nu : 21 plans, rasters importés, 0 marque | Plan Expert (Francis) | `planexpert/00-original-codex/maison st-michel test (8-Septembre-2026).qpl` (9 174 o) |
| v1 / agrégé | marques par lot, puis agrégées | `tools/import/planexpert_counter_import.py` | `planexpert/00-original-codex/Saint-Michel-Codex-Releve-20260908.qpl` et `…-agrege-…` |
| v2 | 1 536 marques consolidées, 120 groupes | idem, avec `--share-groups-by-label` | `project/saint-michel-releve.qpl` (131 859 o) |
| v3 | échelle 1:100 saisie dans Plan Expert | Plan Expert (UI) | `project/saint-michel-releve-v3-scaled.qpl` (159 863 o) |
| v4 | 32 artères injectées comme `<Line>` | `arteres/inject_lines.py` | `planexpert/03-v4-native/…-v4-20260909.qpl` (169 252 o) |
| v5 | 39 ajouts de la contre-vérification → 1 575 marques | `verification/additions.py` + import | `planexpert/04-v5-native/…-v5-20260909.qpl` (176 272 o) |
| v6 | formes/couleurs alignées sur le concurrent, légende déplacée, corrections | `verification/make_v6.py` + `verification/rules_dupuis.py` | `planexpert/05-v6/…-v6-20260909.qpl` (177 559 o) |

Principe structurant : **on ne clique pas 1 500 fois dans Plan Expert**. Le `.qpl` est du XML ; on le lit et on
l'écrit par script, et Plan Expert ne sert qu'à ouvrir / vérifier / mettre à l'échelle / sauvegarder / exporter
(`<REPO>/HANDOFF-SAINT-MICHEL.md` §4 point 6).

---

## 1. Les étapes exactes, de la réception des PDF au dossier livré

Notation : `<WS>` = espace de travail de la soumission (pour S-1857 :
`C:\Users\fvegi\.codex\workspaces\2026-09-08-install-planexpert\takeoff`, `<REPO>/HANDOFF-SAINT-MICHEL.md` §3).
Les scripts `.py` marqués « PEP 723 » déclarent leurs dépendances en en-tête et se lancent par `uv run`.
Les `.ps1` s'exécutent avec **Windows PowerShell 5.1 `-File`** (jamais `-Command`, voir §6).

### Étape 1 — Réception et empreinte des plans sources

| | |
|---|---|
| Entrée | PDF fournis par le client : 21 feuilles électriques `E000–E600` (indice 1 SOUMISSION 2026-08-17) et 50 feuilles d'architecture `A*` (émises 2026-08-19) |
| Sortie | `<REPO>/sources/plans/electrique/E*_Rev0.pdf`, `<REPO>/sources/plans/architecture/A*_Rev0.pdf`, `<REPO>/provenance/source-hashes.json`, `<REPO>/codex-export/source-hashes.csv` |
| Script | `<REPO>/codex-export/prepare.ps1` (rend les feuilles et calcule les empreintes) ; l'empreinte du dépôt entier vient de `<REPO>/tools/make_index.py` |
| Commande | `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File codex-export\prepare.ps1` |

`provenance/source-hashes.json` contient, pour chaque PDF, `filename` / `sha256` / `bytes`, et l'empreinte du
QPL original (`a82dcee5bb37ac3180457c8ed4a54508c058a83f14469c848811cd62637b1867`, `included: false`).
**Toute quantité devra pouvoir être rattachée à un de ces PDF empreintés.**

### Étape 2 — Extraction du texte des feuilles

| | |
|---|---|
| Entrée | `sources/plans/electrique/E*_Rev0.pdf` |
| Sortie | `<REPO>/sources/text/E*_Rev0.txt` (un fichier par feuille) |
| Script | pymupdf `page.get_text()` ; variantes conservées dans `<REPO>/lots/telecom/text/` (`E1xx.txt`, `E1xx-utf8.txt`, `E1xx-bbox.html`) |
| Commande | `uv run --with pymupdf python -c "import pymupdf;..."` (extraction directe, cf. `REPRODUCTION.md` §1) |

Ce texte est la **matière première de tout le reste** : les étiquettes (`DS1`, `Do`, `K`, `CC`, `LV`, `SM`…) sont
lues comme mots avec leurs coordonnées, ce qui donne à la fois le compte et la position.

### Étape 3 — Projet Plan Expert nu et rasters

| | |
|---|---|
| Entrée | les 21 PDF électriques |
| Sortie | `planexpert/00-original-codex/maison st-michel test (8-Septembre-2026).qpl` + `<REPO>/rasters/E*_Rev0.png` (21 PNG **5694 × 4022**) |
| Script | aucun : **import PDF fait par Plan Expert lui-même** (Plan Expert 3.0.17 dans la VM) |
| Commande | UI Plan Expert : nouveau projet → importer les PDF |

Ce fichier est **l'original, jamais modifié** (règle de Francis, `HANDOFF` §1). Les rasters lui appartiennent :
tout `.qpl` du dépôt les référence en **relatif** (`FileName="E4xx_Rev0.png"`), donc pour ouvrir n'importe
quelle version il faut **copier le `.qpl` à côté des 21 PNG** (`REPRODUCTION.md` §2).

### Étape 4 — Relevé par lot (le vrai travail de lecture)

| | |
|---|---|
| Entrée | PDF + texte extrait + légendes (`E102`, `E103`, `E104`) |
| Sortie | un dossier par lot sous `<REPO>/lots/` : `<lot>-result.md`, CSV d'occurrences, rendus PNG de preuve, réserves |
| Script | scripts propres à chaque lot, p. ex. `<REPO>/lots/receptacles/prepare_receptacles.py` puis `export_reviewed.py` |
| Commande | `uv run lots/receptacles/prepare_receptacles.py` puis `uv run lots/receptacles/export_reviewed.py` |

Lots réellement traités (`<REPO>/lots/`) : `lighting` (éclairage E400–E404), `controls` (commandes + secours),
`telecom`, `receptacles` (prises), `fire` (alarme incendie), `power`, `distribution-occurrences` (E200/E600),
`calibration`, `edge` (consolidation). Chiffres par lot dans `HANDOFF` §2 : luminaires 509 (506 typés),
commandes 207, secours 85, prises 329, alarme 123, télécom 63, distribution E200 38, tableaux E600 182.

Méthode d'un lot, telle qu'écrite dans `<REPO>/lots/receptacles/README.md` :
1. **extraction de candidats géométriques** depuis les vrais chemins vectoriels du PDF (`prepare_receptacles.py`
   suit les contours orange fermés) — cette extraction *ne valide pas* un objet ;
2. **inspection visuelle** de chaque candidat dans des rendus de détail à 6 px/pt (`E405-detail-*.png`) et un
   pavage de tuiles à 1,6 px/pt avec 50 pt de recouvrement (`E405-tile-11.png` … `E409-tile-33.png`, 45 tuiles),
   la couverture étant consignée dans `coverage-reviewed.csv` ;
3. **décisions manuelles** enregistrées dans `review-decisions.json` ;
4. **export CSV stable** par `export_reviewed.py` → `receptacles-reviewed.csv`, avec un champ `evidence`
   (fichier de détail + case de contact + index du chemin vectoriel source).

Format de sortie commun à tous les lots — c'est **le contrat du pipeline** :
`sheet, label, x_pt, y_pt, occurrence_id, status`, coordonnées en **points PDF, origine haut-gauche**
(en-tête de `<REPO>/tools/import/planexpert_counter_import.py`).

### Étape 5 — Consolidation des lots

| | |
|---|---|
| Entrée | les CSV de tous les lots |
| Sortie | `<REPO>/lots/edge/combined-v2-occurrences.csv` → `<REPO>/data/occurrences.csv` (1 536 lignes + en-tête, 120 groupes) et `<REPO>/data/counts-by-label.csv` |
| Preuve | `<REPO>/lots/edge/v2-consolidation-audit.json`, `<REPO>/provenance/consolidation-summary.json` (chaque source avec son sha256 et son nombre de lignes) |
| Commande | consolidation faite lot par lot ; le résultat est **validé** par `uv run scripts/validate_takeoff.py manifest.json` |

`provenance/consolidation-summary.json` liste par exemple `combined-current-occurrences.csv` (902 lignes,
rôle « base902 »), `planexpert-emergency.csv` (85, « secours »), `receptacles-reviewed.csv` (329, « prises »),
`import-e200.csv` — chacun avec son sha256. **C'est ce fichier qui prouve d'où viennent les 1 536.**

### Étape 6 — Import CSV → compteurs dans le `.qpl` (v2)

| | |
|---|---|
| Entrée | `project/…qpl` source (les 21 PNG **doivent** être à côté), `data/occurrences.csv`, `data/plan-mapping.json` |
| Sortie | un **nouveau** `.qpl` frère + son `<sortie>.qpl.audit.json` |
| Script | `<REPO>/tools/import/planexpert_counter_import.py` (PEP 723 : pydantic, typer, pillow) |
| Tests | `<REPO>/tools/import/test_planexpert_counter_import.py` |

```
uv run tools/import/planexpert_counter_import.py SOURCE.qpl data/occurrences.csv \
    data/plan-mapping.json SORTIE.qpl --share-groups-by-label
```

`data/plan-mapping.json` associe chaque feuille à son plan et donne les dimensions de page :
`{"sheets":[{"sheet":"E400","plan_name":"E400_Rev0","layer_index":"0","page_width_pt":2383.92,"page_height_pt":1683.72}, …]}`.

Garde-fous réellement codés dans le script (lus dans le source) — **c'est ce qui rend l'import sûr** :
- la sortie doit être **un frère nouveau** de la source (sinon les rasters relatifs ne sont plus trouvés) ; refus
  si la sortie ou l'audit existe déjà (`open(..., "xb")`) ;
- refus si le XML contient `<!DOCTYPE` ou `<!ENTITY` ; racine obligatoire `QuoterPlanSession` ;
- refus si une occurrence sort de la page (`x_pt > page_width_pt`) ;
- refus si les `occurrence_id` ne sont pas uniques, si une feuille du CSV n'est pas dans le mapping, si un
  `GroupID` est dupliqué dans sa portée ou si deux nœuds partagent un `GroupID` avec un nom/style différent
  (`validate_group_ids`) ;
- les dimensions du raster sont **lues dans le PNG** (`PIL.Image.open(...).size` + `image.verify()`), jamais
  supposées ;
- **le XML d'origine est préservé octet pour octet** hors insertions : le script repère les bornes d'octets des
  balises `Layer` avec `xml.parsers.expat` (`element_spans`) et n'insère que des fragments.

L'audit JSON écrit : `source_sha256`, `output_sha256`, `occurrences`, `count_by_sheet_label`,
`new_group_ids`, `raster_dimensions`, `coordinate_origin: top-left`,
`coordinate_units: "PDF points to raster pixels, nearest integer"`, et la liste complète des points
(`x_pt, y_pt, x_px, y_px`). Exemple réel : `planexpert/00-original-codex/Saint-Michel-Codex-Releve-v2-20260908.qpl.audit.json`.

Puis : **ouvrir le résultat dans Plan Expert, sauvegarder, comparer le sha256 du fichier natif**
(`HANDOFF` §4 point 6). Reçus : `<REPO>/evidence/native-validation.json` (1 536 marques, 120 GroupID, 21 plans,
`native_points_match_sent_v2: true`) et `<REPO>/evidence/guest-hash-confirmation.json`.

### Étape 7 — Calibration et échelle (v3)

| | |
|---|---|
| Entrée | feuilles électriques + **une cote d'architecte** lue sur `A101_Rev0.pdf` |
| Sortie | `<REPO>/lots/calibration/calibration-points.csv`, `<REPO>/evidence/calibration-v3-applied.md`, `<REPO>/evidence/calibration-v3-validation.json`, `project/saint-michel-releve-v3-scaled.qpl` |
| Script | mesure par pymupdf ; **l'échelle elle-même est saisie à la main dans Plan Expert** (UI) |
| Commande | UI Plan Expert : sélectionner le plan → échelle métrique, dénominateur `100` |

Méthode (colonnes réelles de `calibration-points.csv`) : pour chaque feuille, deux mesures — horizontale entre
les **axes 1 et 2** et verticale entre les **axes B et A** — avec `x1_pt,y1_pt,x2_pt,y2_pt`, la cote de référence
(`reference_mm` 7200 H et 6440 V), la distance PDF mesurée, `mm_per_pdf_pt` et le `scale_denominator` obtenu.
Chaque ligne cite le PDF cible **et** le PDF d'architecture avec leurs sha256, plus les rendus de preuve
(`renders/E400-H.png`, `renders/A101-cal615.png`).

Résultats : **mm/pt = 35,27336945 (H) et 35,283800739 (V)**, dénominateurs 99,9875 et 100,0171. `E403` est
décalé (origine 466,68 / 295,56 au lieu de 381,0 / 210,0) — d'où la table `FRAME` par feuille (§ artères).

Contrôle d'intégrité (`evidence/calibration-v3-validation.json`) : un objet `CTRL-ECHELLE-BA-E400` tracé sur
E400 sur les axes B–A ; documenté 6,44 m, **mesuré 6,45 m par Plan Expert**, écart 10 mm = 0,16 %. Le fichier
note aussi `measurements_certified: false` et « aucun métré de conduit n'est déclaré à ce stade ».
Échelle appliquée aux 10 feuilles `E400_Rev0`…`E409_Rev0` ; 11 feuilles laissées sans échelle
(`E000, E100, E101, E102, E103, E104, E150, E200, E201, E500, E600`).

### Étape 8 — Artères : mesure puis injection (v4)

| | |
|---|---|
| Entrée | positions d'équipement lues au texte PDF, niveaux `A300/A301`, notes `E100` §27/§28/§29, tableau `E200` |
| Sortie | `<REPO>/arteres/arteres-metres.csv`, `arteres-summary.json`, `arteres-result.md` |
| Script | `<REPO>/arteres/compute_arteres.py` |
| Commande | `uv run arteres/compute_arteres.py` |

Tout ce que le script suppose est **explicitement paramétré** dans le dict `PARAMS` (lu dans le source) :
hauteur d'appareil 1 500 mm, sortie en toiture 1 000 mm, raccord local CC→moteur 3,0 m, flexible 450 mm
(E100 §28), pas de supports 1,5 m (E100 §29), réserve de tirage 5 % (« paramètre estimateur, non prescrit »),
point du puits technique = cage `ASC 111` (E100 §27, « position exacte du puits non cotée »).
Niveaux `LEVEL` (mm) : SS 36 155, RDC 39 200, N1 42 500, N2 45 800, TOIT 49 680.

Chaque départ est un `Feeder(id, src, dst, protection, spec, note, route, local_m)` avec `route` ∈
`direct | puits | local | reserve`. Les trajets sont **orthogonaux** (`segments_same_sheet` : A → coude → B) et
la longueur horizontale est une distance de Manhattan ; un départ inter-niveaux passe par le puits
(`manhattan(S,R) + manhattan(R,D)`) et la montée vaut `|ΔLEVEL| + end_rise(source) + end_rise(destination)`.
Un départ dont la destination n'est pas localisée est marqué `reserve` et **sort avec une longueur nulle et un
statut explicite**, jamais une valeur inventée (F22, F23, F25, F26).

Injection des tracés :

| | |
|---|---|
| Entrée | QPL v3 + `arteres/arteres-summary.json` |
| Sortie | `<REPO>/arteres/Saint-Michel-Codex-Releve-v4-20260909.qpl` + `.audit.json` |
| Script | `<REPO>/arteres/inject_lines.py` |
| Commande | `uv run arteres/inject_lines.py` |

Le script écrit des `<Line …><Element X1 Y1 X2 Y2/></Line>` avec `Color="-29696"` et `PenWidth="6"`, insérés
juste avant le `</Layer>` du plan visé, en conservant le reste du texte XML intact. Il passe aussi la
`Precision` de l'échelle de `0` à `2` sur les dix feuilles E400–E409 (affichage au centimètre).
Son audit contient `source_sha256`, `output_sha256`, `lines_before/after`, `counters_after`, `mm_per_px` et,
pour chaque artère, la longueur attendue en mètres — **à comparer ensuite à ce que Plan Expert affiche**.

`MM_PER_PX = 2383.92 / 5694 * 35.27336945` = mm par pixel raster, soit environ 14,768 mm/px.

### Étape 9 — Contre-vérification indépendante et ajouts (v5)

| Script | Entrée | Sortie | Commande |
|---|---|---|---|
| `verification/crosscheck_text.py` | PDF E400–E409 + QPL v4 natif | `verification/crosscheck-text.md/.json` | `uv run verification/crosscheck_text.py` |
| `verification/crosscheck_geo.py` | idem | `verification/crosscheck-geo.md/.json` | `uv run verification/crosscheck_geo.py` |
| `verification/cc_scan.py` | PDF E405–E409, E600 | `verification/cc-plans-etage.csv` | `uv run verification/cc_scan.py` |
| `verification/additions.py` | `cc-plans-etage.csv` + texte PDF | `verification/additions-import.csv` (39 ajouts) | `uv run verification/additions.py` |
| `tools/import/planexpert_counter_import.py` | v4 + `additions-import.csv` + `additions-mapping.json` | `verification/Saint-Michel-Codex-Releve-v5-20260909.qpl` | idem étape 6 |

- **`crosscheck_text.py`** compte les mots exacts du PDF (hors cartouche, filtre `w[0] < 2050`) et les compare
  au nombre de marques du QPL, feuille par feuille et type par type. Le rapport dit lui-même qu'« un écart de
  quelques unités n'est pas une erreur en soi, il désigne où regarder ».
- **`crosscheck_geo.py`** apparie chaque étiquette texte à la marque la plus proche, **rayon 30 pt (≈ 1,06 m à
  1:100)**, avec `PT_PER_PX = 2383.92/5694`, et sort deux listes : étiquettes sans marque, marques sans
  étiquette. C'est l'outil qui montre *où* il manque quelque chose.
- **`cc_scan.py`** recense les sectionneurs « CC » dessinés sur les plans d'étage et leur associe l'étiquette
  d'équipement la plus proche (< 45 pt, sinon `?`), puis compte les mentions correspondantes sur E600.
- **`additions.py`** transforme ces trouvailles en CSV d'import, avec une zone utile explicite
  `AREA = (330, 600, 1600, 1520)` en points, une liste d'équipements déjà comptés sur E200 à exclure, et le
  filtrage du symbole de légende en bas à gauche. Familles ajoutées : CC de plans d'étage, `SM`, `Ts`, `LV`,
  `Ht`, `V`, `EN`.

Résultat (`HANDOFF` §2) : 1 536 + 39 = **1 575 marques**, sur 218 compteurs / 127 libellés.
Rapport de synthèse : `<REPO>/verification/rapport-contre-verification.md`.

### Étape 10 — Comparaison avec un relevé concurrent, puis mise en forme (v6)

| Script | Rôle | Commande |
|---|---|---|
| `tools/cloud/dupuis_pages.py` | rend les 20 pages du PDF concurrent, découpe **la légende** (quantités par feuille) et le cartouche | `python3 tools/cloud/dupuis_pages.py sources/dupuis/S1857-27Aout2026.pdf build/dupuis` |
| `tools/cloud/dupuis_match.py` | une famille : segmentation couleur des marques adverses + appariement glouton | appelé par le suivant |
| `tools/cloud/dupuis_run_jobs.py` | rejoue les familles décisives | `python3 tools/cloud/dupuis_run_jobs.py sources/dupuis/S1857-27Aout2026.pdf verification/…-v6-….qpl verification/dupuis-match` |
| `verification/make_v6.py` + `rules_dupuis.py` | applique forme + couleur par famille et déplace la légende | `uv run verification/make_v6.py` |
| `verification/diff_vert.py` | PDF des différences en vert fluo (11 p.) | `uv run verification/diff_vert.py` |
| `tools/cloud/overlay_dupuis_claude.py` | superposition « adverse rouge / nous vert » (11 p.) | `python3 tools/cloud/overlay_dupuis_claude.py` |

Points de méthode vérifiés dans `<REPO>/tools/cloud/README.md` :
- **les quantités officielles du concurrent viennent de ses légendes**, pas de la segmentation d'image ; la
  segmentation ne sert qu'à *localiser* les écarts ;
- table de pages **explicite** parce que le PDF adverse n'a pas les mêmes feuilles : E400=9, E401=10, E402=11,
  E403=12, E405=13, E406=14, E407=15, E408=16, E409=17 (**E404 absente**) ;
- page adverse 2997 × 2116 pt ⇒ `pt = px × 2997 / 5694` ;
- opacité du calque Plan Expert sur sa page ≈ **0,74** (mesurée : pastille (238,182,53) → sur plan (255,202,105)) ;
- paramètres d'appariement retenus : échelle de rendu **2**, rayon **40 pt**, `amin` 60, `tol` 60.

`make_v6.py` fait quatre choses, et son audit (`planexpert/05-v6/….qpl.audit.json`) les prouve :
`n_counters: 218`, `n_lines: 28`, `n_elements: 1575`, `unmatched: []` (**aucun libellé sans règle**),
`renamed` (1 : « Chauffage électrique 3R » → « Borne de recharge VE (BRVE)… »),
`dropped_lines` (4 segments des artères F22/F23), `legend` (12 plans repositionnés en 4250/1350),
`out_sha256: 765f0e08bb82829c1c113b7ed5f5d606f43a73af2ddc332c6a988e0a6595a080`, `out_bytes: 177559`.
Il retire aussi les `<Price>` des groupes supprimés.

### Étape 11 — Aller-retour avec Plan Expert (à chaque version)

| | |
|---|---|
| Hôte → VM | `uv run tools/transfer/serve_qpl2.py QPL RUN_DIR HOST_IP PEER_IP` puis, dans la VM, `Invoke-WebRequest -OutFile` + `Get-FileHash` |
| VM → hôte | `uv run tools/transfer/receive_qpl3.py RUN_DIR HOST_IP PEER_IP` puis, dans la VM, `Compress-Archive` + `Invoke-WebRequest -Method Post -InFile -Headers @{'X-SHA256'=…}` ; dézippage `tools/host/_unz5.py` |

Les deux serveurs sont **à usage unique et vérifiés** (lu dans les sources) : lien secret
`secrets.token_urlsafe(24)` comparé en temps constant, **contrôle de l'IP appelante**, en-tête `X-SHA256`
vérifié à la réception (sinon 422), écriture en `xb` (jamais d'écrasement), reçu JSON
(`download-receipt.json`, `transfer-receipt.json`), `bind` sur **port 0** et fenêtre de 900 s.
`receive_qpl3.py` monte le timeout socket à **180 s** et la taille max à **256 Mo** (voir §6).

Dans Plan Expert (procédure éprouvée, `HANDOFF` §4 point 2) :
1. Fichier → Ouvrir…, cliquer le champ « File name », **taper le chemin complet du QPL**, Entrée.
2. Changer de feuille par **la liste déroulante du panneau Groupes** (pas par « Plans récents »).
3. Vérifier visuellement les feuilles critiques, puis **icône disquette** (statut « Sauvegardé » en bas).
4. Rapports → Exporter vers **XML / HTML / PDF / Excel** (chaque export ouvre IE/Edge : fermer ; l'Excel
   affiche « How do you want to open » : Échap, le `.xls` est quand même écrit dans `Mes rapports`).
5. Plans → Exporter vers PDF → **Sélectionner tout** → Confirmer →
   `Mes plans PDF\Fichiers exportés\<projet>\<projet>.pdf`.

Sorties natives attendues (ce que contiennent réellement `planexpert/03-v4-native/` et `04-v5-native/`) :
le `.qpl` resauvegardé, `…-Métré-[Classé_par_plans].xml`, `…-Rapport-de-métré-(par-plans).html/.pdf/.xls`,
`…-Plans-annotes.pdf`, plus les images d'accompagnement du rapport HTML (`2737922945.png`, `356868256.png`,
`4133685977.gif`).

### Étape 12 — Réserves et méthode des dérivations

| | |
|---|---|
| Sortie | `<REPO>/reserves/registre-reserves.md` + `.csv` (**63 réserves**, 22 questions d'addenda) ; `<REPO>/derivations/methode-derivations.md`, `parametres-derivations.csv`, `derivations-quantites-base.csv` |

Le registre est ventilé par lot (éclairage 10, commandes 6, prises 9, alarme 4, télécom 6, sécurité 2,
distribution 19, artères 2, général 5) et par nature (fourniture 27, calibre 12, coordination 9, longueur 9,
compte 6). Il déclare explicitement : « aucune valeur inventée, aucune résolution tacite ».

`methode-derivations.md` est **une méthode paramétrée, pas un métré** : « Statut : MÉTHODE PARAMÉTRÉE. Aucune
longueur de dérivation n'est mesurée ni calculée ici », parce que les plans ne dessinent pas les parcours.
`parametres-derivations.csv` (séparateur `;`) a une ligne par paramètre avec
`nom;unite;valeur_par_defaut;source;commentaire`, et la **valeur par défaut est laissée vide quand aucune
source ne la fonde**. Le document liste aussi ce qui est explicitement hors méthode.

### Étape 13 — Dossier PDF et livraison

| | |
|---|---|
| Entrée | les `.md` de résultats + les PDF natifs de Plan Expert + les PDF visuels |
| Sortie | `<REPO>/dossier/Saint-Michel-S-1857-Dossier-releve-PlanExpert-2026-09-09.pdf` (94 p. en v5) |
| Script | `<REPO>/arteres/build_dossier.py` (PEP 723 : markdown, pypdf) |
| Commande | `uv run arteres/build_dossier.py v6` (ou `v5`) |

Chaîne réelle : Markdown → HTML (avec un CSS inline dans le script) → PDF par
`msedge.exe --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=…`, puis fusion `pypdf` avec un
signet par pièce. **Le script refuse de construire si un fichier attendu manque** (`sys.exit('FICHIERS
MANQUANTS (dossier non construit)')`) — pas de repli silencieux sur une autre version.

Livraison : `tools/host/_git6.ps1` … `_git15.ps1` (copie vers `LIVRAISON-…`, copie Drive, `git add -A`, commit,
push **GitLab `origin` et GitHub `github` au même commit**). Attention : `.gitignore` du dépôt exclut
`*.zip` et les caches ; à l'époque il excluait aussi `*.qpl/*.pdf/*.png`, d'où `git add -f` (`HANDOFF` §3).

---

## 2. Spécification du format QPL — **observée dans les fichiers réels**

Vérifiée en lisant `planexpert/00-original-codex/maison st-michel test (8-Septembre-2026).qpl` (projet nu
sauvegardé par Plan Expert) et `planexpert/05-v6/Saint-Michel-Codex-Releve-v6-20260909.qpl` (218 compteurs,
28 lignes, 1 575 éléments), et en recomptant les balises.

### 2.1 Enveloppe

XML, encodage **UTF-8 avec BOM** dans les fichiers écrits par Plan Expert (les scripts lisent en
`utf-8-sig`), prologue `<?xml version="1.0"?>` **sans déclaration d'encodage**, indentation par tabulations,
fins de ligne CRLF. Racine `<QuoterPlanSession>`. Ordre des sections tel qu'observé :

```xml
<QuoterPlanSession>
  <Project Name="…">
    <Description/><ContactName/><ContactInfo/><JobNumber/><Comment/>
    <CreationDate>2026/9/8</CreationDate><LastModified>2026/9/8</LastModified>
    <DisplayResultsForAllPlans>True</DisplayResultsForAllPlans>
  </Project>
  <Workspace>
    <ActivePlan Name="E406_Rev0"/>
    <RecentPlans><Plan Name="E409_Rev0"/> … </RecentPlans>   <!-- 10 entrées -->
  </Workspace>
  <Plans> … 21 <Plan> … </Plans>
  <Prices> … 155 <Price> … </Prices>
  <Reports><Report Name="Default" Order="1" ScaleType="1" Precision="0"> 16 <Property/> </Report></Reports>
</QuoterPlanSession>
```

Dates au format `AAAA/M/J` sans zéro de tête. `<Workspace>` est vide dans le projet nu et rempli après usage.

### 2.2 `<Plan>` — une feuille

```xml
<Plan Name="E409_Rev0" FileName="E409_Rev0.png">
  <Thumbnail FileName="bedc3551-3f9a-4c6a-aaa4-46783dd5c132"/>
  <Scale Value="100" Type="0" Precision="2" SetManually="False" Engineering="False"/>
  <Bookmarks><Bookmark Name="Default" LayerIndex="0" Zoom="10" X="0" Y="0"/></Bookmarks>
  <Comment/>
  <Layers> … </Layers>
</Plan>
```

- `FileName` : **nom du PNG, en relatif** → le `.qpl` doit être ouvert à côté des rasters.
- `Thumbnail FileName` : un GUID sans extension (vignette interne de Plan Expert) ; **à conserver tel quel**.
- `Bookmark Zoom` vaut `-1` dans le projet nu et `10` après usage.

### 2.3 `<Scale>` — l'échelle

`<Scale Value Type Precision SetManually Engineering/>`. Deux états seulement dans la v6 (recomptés) :

| État | Attributs | Nombre de feuilles |
|---|---|---|
| **non calibrée** | `Value="0" Type="1" Precision="0" SetManually="False" Engineering="False"` | 11 |
| **1:100 métrique** | `Value="100" Type="0" Precision="2" SetManually="False" Engineering="False"` | 10 (E400…E409) |

⇒ **`Type="0"` = métrique, `Type="1"` = non défini / impérial** ; `Value` = dénominateur de l'échelle ;
`Precision` = décimales affichées pour les mesures (mise à `2` par `inject_lines.py` pour lire au centimètre).
`<Report … ScaleType="1">` dans la v6 alors que le projet nu a `ScaleType="0"` : c'est le réglage du rapport,
distinct de l'échelle des plans — c'est ce qui a produit un rapport en pieds-pouces (réserve R-057, §6).

### 2.4 `<Layer>` et `<Legend>`

```xml
<Layer Index="0" Name="Releve autonome" Opacity="150" Visible="True" Active="True">
  <Legend Name="Légende" X="4250" Y="1350" FontSize="45" MaxRows="25"
          Color="-657931" PenWidth="6" PenType="Generic" FillColor="-657931"
          ShowMeasure="True" Visible="True"/>
  … Counter … Line …
</Layer>
```

- Un seul calque par plan dans tout le dépôt (`Index="0"`). Nom du calque créé par l'import :
  `Releve autonome` ; celui du projet nu : `Calque par défaut`. `Opacity="150"` (sur 255).
- **`<Legend>` est le premier enfant du calque**, avant les compteurs.
- `X`/`Y` de la légende sont **en pixels du raster**, pas en points : `4250 / 1350` place la légende à droite du
  dessin sur une image large de 5 694 px. Positions réellement présentes en v6 : `4250/1350` sur les 12 feuilles
  utiles (E200, E400–E409, E600), `0/0` sur 8 feuilles sans marque, `100/100` sur E000.
- `Color="-657931"` = `0xFFF5F5F5` (blanc cassé) : c'est le **fond** du cartouche de légende.

### 2.5 `<Counter>` — un compteur (une famille d'objets)

```xml
<Counter Name="Alarme avertisseur combine K" GroupID="77" Shape="0" DefaultSize="26"
         Text="1" Color="-2200779" PenWidth="2" PenType="Generic" FillColor="-2200779"
         ShowMeasure="True" Visible="True">
  <Element X="1901" Y="2238" Width="26" Height="26"/>
</Counter>
```

| Attribut | Observé | Sens |
|---|---|---|
| `Name` | 127 libellés distincts | libellé affiché en légende et dans les rapports ; **échappé XML** (`&gt;` dans les noms d'artères) |
| `GroupID` | entiers 1…157, **127 valeurs distinctes pour 218 nœuds `Counter`** | identité logique de la famille |
| `Shape` | v6 : `0` ×98, `1` ×115, `3` ×4, `4` ×1 | forme (§2.7) |
| `DefaultSize` | `20, 22, 24, 26, 28, 30` | taille du symbole en **pixels raster** |
| `Text` | toujours `1` | valeur unitaire comptée par marque |
| `Color`, `FillColor` | **toujours égaux** (218/218), 59 valeurs distinctes | ARGB signé (§2.7) |
| `PenWidth` | toujours `2` | épaisseur du contour |
| `PenType` | toujours `Generic` | — |
| `ShowMeasure`, `Visible` | `True` | — |

**Un même `GroupID` est partagé par plusieurs plans** : 41 des 127 groupes apparaissent sur 2 à 4 feuilles
(p. ex. `GroupID="37"` « Luminaire DR2 » sur E400, E401, E402, E403). C'est exactement ce que fait l'option
`--share-groups-by-label` de l'import ; le validateur exige alors que nom, type et style soient identiques
partout (`validate_group_ids` dans `tools/import/planexpert_counter_import.py`), et **interdit deux nœuds du
même groupe dans le même plan**.

### 2.6 `<Element>` — une marque, et `<Line>` — un tracé mesuré

Marque de compteur : `<Element X="1901" Y="2238" Width="26" Height="26"/>` — **coordonnées et dimensions en
pixels du raster**, origine haut-gauche. Recompte sur la v6 : 1 575 éléments, dont
`26×26` ×973, `24×24` ×388, `20×20` ×199, `28×28` ×8, `30×30` ×4, `22×22` ×3.

```xml
<Line Name="ART F10 P-P1&gt;VRT-1 [puits-&gt;TOIT]" GroupID="138" Color="-29696"
      PenWidth="6" PenType="Generic" ShowMeasure="True" Visible="True">
  <Element X1="2193" Y1="1720" X2="1822" Y2="1720"/>
  <Element X1="1822" Y1="1720" X2="1822" Y2="3055"/>
</Line>
```

Une `<Line>` porte **plusieurs segments** (28 lignes / 55 segments en v6) ; sa longueur est calculée par Plan
Expert à partir de l'échelle du plan, d'où l'obligation d'avoir fait l'étape 7 avant. `GroupID` des lignes :
123…150, dans le **même espace de numérotation** que les compteurs. Couleurs observées : `-29696` (27 artères)
et `-16776961` (1 : l'objet de contrôle d'échelle `CTRL-ECHELLE-BA-E400`).

### 2.7 Formes et couleurs

**Formes** — énumération lue par réflexion dans `PlanExpert.exe`
(`QuoterPlan.DrawCounter+CounterShapeTypeEnum`, script `<REPO>/tools/host/planexpert-enum/enum.ps1`) :

| Valeur | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Forme | Circle | Square | Diamond | Triangle | TriangleReversed | Trapeze | TrapezeReversed | CustomImage |

**Couleurs = ARGB 32 bits signé** (entier décimal, négatif dès que alpha = 255). Conversion, telle que codée
dans `verification/make_v6.py` :

```python
def argb(r, g, b):
    v = 0xFF000000 | (r << 16) | (g << 8) | b
    return str(v - (1 << 32))     # entier signé 32 bits
```

Vérifié sur les valeurs réelles du fichier v6 :

| Compteur | `Shape` | `Color` | hex | (A,R,G,B) |
|---|---|---|---|---|
| Luminaire DS1 | 1 (carré) | `-1133003` | `0xFFEEB635` | 255, 238, 182, 53 |
| Luminaire DS0 | 0 (cercle) | `-9659458` | `0xFF6C9BBE` | 255, 108, 155, 190 |
| DATA_MURAL | 3 (triangle) | `-13290082` | `0xFF35359E` | 255, 53, 53, 158 |
| Borne de recharge VE | 4 (triangle inversé) | `-3884235` | `0xFFC4BB35` | 255, 196, 187, 53 |
| Alarme panneau PAI | 1 | `-13290187` | `0xFF353535` | 255, 53, 53, 53 |
| artère (Line) | — | `-29696` | `0xFFFF8800` | 255, 255, 136, 0 |
| contrôle d'échelle (Line) | — | `-16776961` | `0xFF0000FF` | 255, 0, 0, 255 |
| fond de légende | — | `-657931` | `0xFFF5F5F5` | 255, 245, 245, 245 |

### 2.8 Écarts constatés entre la documentation du projet et les fichiers réels

Trois points où la doc du dépôt ne correspond pas exactement à ce que contient le `.qpl` — à corriger dans le
socle :

1. **`HANDOFF` §3b affirme que « les `Element` acceptent `Width` ≠ `Height` (rectangles, comme Dupuis pour les
   luminaires) ».** Recompte sur `planexpert/05-v6/…-v6-….qpl` : **0 élément sur 1 575 n'a `Width` ≠ `Height`**.
   La capacité est peut-être réelle côté logiciel, mais elle **n'est pas exercée** dans le livrable ; ne pas s'y
   fier sans essai.
2. **`arteres/inject_lines.py` commente `COLOR = '-29696'  # orange ARGB FFFF8C00`** ; la valeur vaut en réalité
   `0xFFFF8800`. Le commentaire est faux d'un chiffre, la couleur est bonne.
3. **`HANDOFF` §3b annonce « 7 formes »** ; l'énumération lue dans l'exécutable en compte **8** (0…7, avec
   `CustomImage`). La v6 n'en utilise que 4 (0, 1, 3, 4) — les valeurs 2, 5, 6, 7 sont disponibles et non testées.

### 2.9 `<Prices>` et `<Reports>`

`<Price Key="48;;Counter;" CostEach="0" MarkupEach="0" SystemType="2"/>` — la clé est
`<GroupID>;;<Counter|Line>;`. Il y a 155 `Price` en v6 pour 127 groupes de compteurs + 28 lignes.
`make_v6.py` supprime les `Price` des groupes qu'il retire ; **si on supprime un objet, il faut supprimer son
prix**. `<Reports>` porte 16 `<Property Name Value/>` (`ShowProjectInfo`, `ApplyFilter`, `ReportSortBy`…).

---

## 3. Conversion PDF → raster et correspondance px ↔ pt

### 3.1 Chiffres mesurés

| Grandeur | Valeur | Comment elle a été vérifiée |
|---|---|---|
| Page PDF électrique | **2383,919921875 × 1683,719970703125 pt** | `pymupdf` `page.rect` sur `sources/plans/electrique/E405_Rev0.pdf` et `E000_Rev0.pdf` |
| Raster Plan Expert | **5694 × 4022 px** | `PIL.Image.open` sur les 21 PNG de `<REPO>/rasters/` (tous identiques, mode `P` palettisé) |
| **DPI du PNG** | **171,9834** | métadonnée `dpi` des PNG = `72 × 5694 / 2383,92` |
| Page du PDF concurrent | **2997 × 2116 pt** | `pymupdf` sur `sources/dupuis/S1857-27Aout2026.pdf` (20 pages) |

Le raster **n'est pas produit par nos scripts** : c'est Plan Expert qui importe les PDF (étape 3). Le DPI de
171,98 est donc une conséquence, pas un réglage — mais c'est la valeur à retrouver pour qu'un nouveau projet
soit compatible avec ces formules.

### 3.2 La formule, telle qu'elle est réellement codée

`tools/import/planexpert_counter_import.py` utilise **un rapport par axe**, calculé à partir des dimensions
lues dans le PNG et des dimensions de page du mapping :

```python
x_px = round(x_pt * raster_width  / page_width_pt)    # 5694 / 2383.92 = 2.388502970
y_px = round(y_pt * raster_height / page_height_pt)   # 4022 / 1683.72 = 2.388758226
```

**Contrôle refait pour ce document** : les 1 536 occurrences de `<REPO>/data/occurrences.csv` reprojetées avec
ces deux facteurs retombent **exactement, au pixel près, sur les 1 536 `<Element X Y>` de
`project/saint-michel-releve.qpl`** (1 536 retrouvées, 0 manquante). La formule est donc confirmée.

**Attention — incohérence à corriger en généralisant.** `REPRODUCTION.md` et `HANDOFF` §4.6 énoncent une
formule à **un seul facteur** : « px = pt × 5694/2383,92 ». Deux scripts l'appliquent aux deux axes :
`arteres/compute_arteres.py` (`PX_PER_PT = 5694 / 2383.92`) et `verification/crosscheck_geo.py`
(`PT_PER_PX = 2383.92 / 5694`). L'écart entre les deux facteurs est de **0,0107 %** — soit ≈ 0,4 px sur toute la
hauteur de la page. C'est négligeable ici (rayon d'appariement 30 pt) mais **ce n'est pas exact** : le socle doit
retenir la version à deux facteurs de l'import.

Sens inverse : `pt = px × page/raster`. Vers le PDF du concurrent : `pt = px × 2997 / 5694`
(`tools/cloud/README.md`).

### 3.3 De la mesure au terrain (échelle 1:100)

`lots/calibration/calibration-points.csv` donne les facteurs mesurés sur les axes du cadre :
**mm/pt = 35,27336945 (H)** et **35,283800739 (V)**, soit des dénominateurs 99,9875 et 100,0171 pour une
échelle nominale 1:100. En pixels : `MM_PER_PX = 2383.92/5694 × 35.27336945 ≈ 14,768 mm/px`
(`arteres/inject_lines.py`).

### 3.4 Comment le `.qpl` référence les images

`<Plan Name="E409_Rev0" FileName="E409_Rev0.png">` : **nom de fichier nu, résolu relativement au dossier du
`.qpl`**. Le script d'import le confirme en ouvrant le PNG par `source.parent / FileName`
(fonction `raster_path`, qui gère aussi un chemin Windows absolu). Conséquences pratiques :

- un `.qpl` sans ses PNG à côté **ne s'ouvre pas correctement** dans Plan Expert ;
- l'import **exige que la sortie soit un frère de la source** (« Output must be a different sibling QPL to
  preserve background references ») ;
- `<Thumbnail FileName="<GUID>"/>` pointe une vignette interne : à recopier telle quelle, ne jamais la générer.

---

## 4. Les scripts : réutilisables, à généraliser, jetables

### 4.1 Réutilisables tels quels (aucun chemin en dur, arguments complets)

| Script | Rôle | Pourquoi il est portable |
|---|---|---|
| `tools/import/planexpert_counter_import.py` | **cœur du socle** : CSV → compteurs `.qpl` | 4 arguments + 2 options, PEP 723, aucun chemin en dur, audit JSON, tests fournis |
| `tools/import/test_planexpert_counter_import.py` | tests de l'import | — |
| `tools/make_index.py` | `INDEX.md` + `SHA256SUMS.txt`, et `--check` | racine déduite du fichier, sans dépendance externe |
| `scripts/validate_takeoff.py` | validation CI CSV ↔ QPL contre `manifest.json` | tout vient du manifeste |
| `tools/transfer/serve_qpl2.py` | hôte → VM, lien à usage unique | IP en arguments |
| `tools/transfer/receive_qpl3.py` | VM → hôte, gros fichiers | IP en arguments |
| `tools/cloud/dupuis_pages.py` | rendu des pages + découpe des légendes d'un relevé concurrent | `argparse`, PDF et dossier en arguments |
| `tools/cloud/dupuis_match.py` / `dupuis_run_jobs.py` | appariement par famille | PDF, QPL, dossier et fichier de jobs en arguments |
| `tools/host/planexpert-enum/enum.ps1` | lit l'énumération des formes dans `PlanExpert.exe` | à réexécuter à chaque changement de version de Plan Expert |

### 4.2 À généraliser — la logique est bonne, les données sont dans le code

| Script | Ce qui est en dur | À paramétrer |
|---|---|---|
| `arteres/compute_arteres.py` | `FRAME` (origine des axes par feuille), `LEVEL`/`STOREY`/`SHEET_LEVEL`, `EQ` (positions d'équipement), `RISER`, la liste `FEEDERS`, `MM_PER_PT_H/V` | sortir `PARAMS`, `FRAME`, `LEVEL`, `EQ` et `FEEDERS` dans un **JSON/CSV par soumission** ; garder dans le code seulement la géométrie (Manhattan, `end_rise`, `segments_same_sheet`) |
| `arteres/inject_lines.py` | chemins `SRC`/`DST`, couleur `-29696`, `PenWidth 6`, liste des 10 feuilles à passer en `Precision=2` | source/sortie en arguments ; couleur, épaisseur et liste de feuilles en options |
| `verification/make_v6.py` | `SRC`/`OUT` absolus, `RENAME`, `DROP_LINE_PREFIX`, `LEGEND_XY` | source/sortie en arguments ; renommages, suppressions et position de légende dans un JSON de config |
| `verification/rules_dupuis.py` | table de 70 règles `(regex, forme, RGB, taille)` | **c'est la charte graphique** : un fichier de règles par soumission (ou une charte maison réutilisable) |
| `verification/crosscheck_text.py` | `BASE`, `QPL` absolus, listes `LUM`/`CMD`/`FA`, filtre `w[0] < 2050`, feuilles E400–E409 | chemins en arguments ; **table des familles et de leurs étiquettes** en JSON ; largeur du cartouche par gabarit |
| `verification/crosscheck_geo.py` | mêmes chemins, dict `TYPES` par feuille, `RADIUS = 30.0`, exclusion des bulles d'axes `300 < x < 1900` | idem + rayon et zones d'exclusion en options |
| `verification/cc_scan.py` | `BASE`, feuilles, seuil 45 pt, regex d'étiquette | chemins, feuilles et seuils en arguments |
| `verification/additions.py` | `BASE`, `AREA = (330,600,1600,1520)`, `E200_CC`, dict `LABELS`, exceptions codées par coordonnées (`abs(x-1264) < 3`) | zone utile et table de libellés en config ; **supprimer les exceptions par coordonnées** (voir §6) |
| `arteres/build_dossier.py` | `WS`, `EDGE`, `STEM`, `DESCR`, liste `docs`, CSS | racine et version en arguments ; **table de matières déclarative** (liste de pièces) |
| `tools/cloud/overlay_dupuis_claude.py` | déjà pilotable par variables d'environnement (`DUPUIS_PDF`, `SRC_DIR`, `QPL`, `OUT_DIR`, `FINAL_PDF`) | passer en `argparse` |
| `verification/diff_vert.py` | catégories A/B/C/D et positions | table des différences en entrée JSON |
| `codex-export/prepare.ps1` / `build-qpl.ps1` / `validate*.ps1` | chemins de sources | `build-qpl.ps1` prend déjà `-DataPath` / `-OutputDirectory` et **refuse un dossier existant** : bonne base pour un export portable |

Paramètres à isoler dans un **fichier de projet** unique (proposition de socle) : identifiant de soumission,
dossier des plans, liste des feuilles et leur niveau, dimensions de page, dimensions du raster, feuilles à
mettre à l'échelle et dénominateur, position de la légende, charte graphique (règles forme/couleur/taille),
paramètres de métré (hauteurs, flexible, supports, réserve), et la table des pages du relevé concurrent.

### 4.3 Jetables — utiles une fois, à ne pas reprendre

Tout `<REPO>/tools/host/_*.ps1` et `_*.py` (≈ 70 fichiers) : ce sont les **scripts d'exploitation d'une session**,
avec chemins absolus, numérotés au fil de l'eau (`_git.ps1` … `_git15.ps1`, `_qpl.py` … `_qpl5.py`,
`_dig.py` … `_dig8.py`, `_recv*.ps1`, `_serve*.ps1`, `_pdf1..4.py`). Exemples typiques :
- `tools/host/_upd7.py` : applique un `str.replace` à `compute_arteres.py` pour corriger F22/F23 — **correctif
  ponctuel**, l'équivalent d'un patch ;
- `tools/host/_marks.py`, `_perplan.py`, `_qpl4.py` : extractions ad hoc vers `C:\Users\fvegi\.agents\_*.txt` ;
- `tools/host/_git6.ps1` … `_git15.ps1` : copie + commit + push d'un livrable donné.

À conserver comme **modèles** (la logique vaut, pas le fichier) : `_vm_export.ps1` (export Hyper-V par WMI),
`_unz5.py` (dézippage des exports reçus), `_serve_pdf.py` (serveur PDF local pour relecture).
`verification/inject_f22_f23.py` et `tools/cloud/overlay_v1_fond_eclairci.py` sont explicitement des impasses
conservées pour l'historique (la v1 de la superposition a été refusée par Francis).

---

## 5. Contrôle qualité : preuves, hachages, vérifications qui ont attrapé des erreurs

### 5.1 Les fichiers qui servent de preuve

| Preuve | Fichier | Ce qu'elle établit |
|---|---|---|
| Empreinte des plans reçus | `provenance/source-hashes.json`, `codex-export/source-hashes.csv` | on a relevé **ces** PDF-là |
| Origine des occurrences | `provenance/consolidation-summary.json`, `lots/edge/v2-consolidation-audit.json` | chaque source de lot avec son sha256 et son nombre de lignes |
| Audit d'import | `<sortie>.qpl.audit.json` (à côté de chaque QPL généré) | sha256 avant/après, comptes par feuille et libellé, tous les points en pt **et** en px, dimensions des rasters |
| Reçu Plan Expert | `evidence/native-validation.json`, `evidence/guest-hash-confirmation.json` | Plan Expert a bien relu et resauvegardé : 1 536 marques, 120 groupes, 21 plans, `native_points_match_sent_v2: true` |
| Contrôle d'échelle | `evidence/calibration-v3-validation.json`, `evidence/calibration-v3-applied.md` | 6,44 m documentés vs **6,45 m mesurés**, écart 0,16 % |
| Calibration détaillée | `lots/calibration/calibration-points.csv` (+ `renders/`) | chaque mesure avec son PDF cible, son PDF d'architecture, leurs sha256 et l'image de preuve |
| Contre-vérification | `verification/crosscheck-text.md/.json`, `crosscheck-geo.md/.json`, `overlays/*.png` | écarts étiquettes ↔ marques, localisés |
| Comparaison concurrent | `verification/comparaison-dupuis.md/.csv`, `dupuis-match/*.json`, `dupuis-legends/` | famille par famille, quantités officielles tirées de ses légendes |
| Captures d'écart | `verification/captures/E401-DS1-oublie-Dupuis.png`, `E402-DS0-oublie-Dupuis.png`, `E401-toilette105-Do.png` | l'oubli est visible au pixel |
| Preuves de lot | `lots/receptacles/*-detail-*.png`, `*-tile-*.png`, `coverage-reviewed.csv`, `review-decisions.json` | chaque objet a été regardé, la couverture est tracée |
| Rapports natifs | `planexpert/0*-native/…-Métré-[Classé_par_plans].xml`, `…-Rapport-de-métré-(par-plans).html/.pdf/.xls` | les quantités **telles que Plan Expert les calcule** |
| Catalogue du dépôt | `INDEX.md` + `SHA256SUMS.txt` | taille et sha256 de chaque fichier suivi |

### 5.2 Les hachages, et pourquoi ils sont stables

Tout est en **SHA-256**. Trois usages distincts :

1. **Empreintes de sources** (PDF, QPL original) : figées dans `provenance/`.
2. **Chaîne de transformation** : chaque script écrit `source_sha256` et `output_sha256` dans son audit
   (`planexpert_counter_import.py`, `inject_lines.py`, `make_v6.py`). On peut donc **remonter la chaîne**
   d'un livrable jusqu'aux PDF d'origine.
3. **Catalogue du dépôt** : `tools/make_index.py` hache **le contenu tel que git le stocke**
   (`git cat-file --batch` sur l'index), donc les fins de ligne sont normalisées par `.gitattributes`
   (`* text=auto eol=lf`, `*.qpl binary`) et **l'empreinte est identique sur Windows et Linux**.
   Vérification : `python tools/make_index.py --check` (sort en code 1 s'il y a une différence ou un absent).

Hachages de référence cités dans `HANDOFF` §2 et §3b : v5 natif
`c898425a608b37dace7fb9f4b4c766678acaf2df981bcc19daba5e28897e9118` (176 272 o) ; v6
`765f0e08bb82829c1c113b7ed5f5d606f43a73af2ddc332c6a988e0a6595a080` (177 559 o) ; original **intact**
`a82dcee5bb37ac3180457c8ed4a54508c058a83f14469c848811cd62637b1867` (9 174 o).
Le transfert VM ↔ hôte vérifie aussi le sha256 des deux côtés (`X-SHA256`, `Get-FileHash`).

### 5.3 Les vérifications qui ont réellement attrapé quelque chose

| Vérification | Erreur trouvée | Trace |
|---|---|---|
| **Contrôle d'échelle dans Plan Expert** (objet `CTRL-ECHELLE-BA-E400`) | confirme l'échelle à 0,16 % — sans lui, rien ne prouvait que la saisie UI avait pris | `evidence/calibration-v3-validation.json` |
| **`crosscheck_text.py` + `crosscheck_geo.py`** | 7 familles entières manquaient au relevé Codex (CC de plans d'étage, LV, SM, Ht, Ts, V, EN) → **39 ajouts** en v5 | `verification/crosscheck-*.md`, `additions-import.csv`, `rapport-contre-verification.md` |
| **Comparaison avec le relevé du concurrent** (`dupuis_run_jobs.py`) | **3 oublis du concurrent localisés au pixel** : DS1 E401 (1058, 3356) salle 124 ; DS0 E402 (3540, 2430) ; Do E401 (1614, 1685) toilette 105 | `verification/dupuis-match/*.json`, `tools/cloud/README.md`, captures |
| **Lecture de la légende E104 lors de cette comparaison** | **erreur d'interprétation de notre côté** : les 2 symboles « 3R » du débarcadère 107 étaient lus comme du chauffage ; ce sont des **bornes de recharge VE** → artères F22/F23 retirées, compteur renommé BRVE, réserve R-042 rétablie et **R-063 ajoutée** | `HANDOFF` §3b, `make_v6.py` (`RENAME`, `DROP_LINE_PREFIX`), audit v6 |
| **`unmatched: []` dans l'audit de `make_v6.py`** | garantit qu'**aucun des 127 libellés n'est resté sans règle** de forme/couleur | `planexpert/05-v6/….qpl.audit.json` |
| **Comptage des blobs vs légendes du concurrent** | a montré que la segmentation couleur attrape des familles voisines (DS4 jaune, Di bleu) → les quantités officielles doivent venir des **légendes**, pas de l'image | `tools/cloud/README.md`, note `*` du tableau |
| **`validate_group_ids` de l'import** | refuse un `GroupID` dupliqué dans sa portée ou un groupe partagé avec un nom/style différent | `tools/import/planexpert_counter_import.py` |
| **`build_dossier.py` refuse si un fichier manque** | empêche de livrer un dossier construit sur une version périmée | `arteres/build_dossier.py` |
| **CI GitLab** | `pytest tests` + `validate_takeoff.py manifest.json` + `ruff check` et `ruff format --check` à chaque push | `.gitlab-ci.yml` |
| **`tools/make_index.py --check`** | détecte toute dérive de contenu du dépôt | `SHA256SUMS.txt` |

Deux règles de fond, vérifiées à l'usage :
- **la vérification doit être indépendante de la lecture initiale** (Claude a contre-vérifié Codex avec une
  méthode différente : texte + géométrie, et non une relecture des mêmes rendus) ;
- **un écart n'est pas une erreur** : les rapports de contre-vérification le disent explicitement, l'écart
  désigne un endroit à regarder.

---

## 6. Pièges documentés — « erreurs à ne pas refaire »

Repris de `<REPO>/HANDOFF-SAINT-MICHEL.md` §5 (tableau complet), complété par §3b, §4 et §6.

### 6.1 Outils et shell

| Symptôme | Cause | Correction |
|---|---|---|
| `$var` vide dans un `-Command` PowerShell | le wrapper pwsh7 de Desktop Commander interpole les `$var` | écrire un `.ps1` et l'exécuter avec Windows PowerShell 5.1 `-File` |
| `Get-VM` échoue (« Value cannot be null. Parameter name: name ») | bug CIM de pwsh7 (et cassé même en 5.1 sur ce poste) | passer par WMI `root\virtualization\v2 Msvm_ComputerSystem` |
| `http.server` : `WinError 10013` sur 8765/47311 | plages de ports exclues par Windows | **binder le port 0** et lire le port attribué |
| `Bind WinError 10049` | l'IP du Default Switch Hyper-V a changé | lire `ipconfig` dans la VM et passer HOST/PEER en arguments (les scripts Codex avaient 172.19.224.x en dur) |
| Upload 17 Mo « connection closed on send » | timeout socket de 10 s | `receive_qpl3.py` : 180 s, lecture par blocs, 256 Mo |
| `.qpl` / `.pdf` absents du commit | `.gitignore` | `git add -f` |

### 6.2 Pilotage de Plan Expert dans la VM

| Symptôme | Cause | Correction |
|---|---|---|
| `ctrl+a` **tape un « a »** dans un champ Plan Expert | raccourci non transmis par noVNC | **Fin + Retour arrière ×N** pour vider un champ |
| Champ d'échelle qui affiche « 0100 » | la valeur « 0 » était préremplie | **vider le champ avant** de taper `100` |
| Un double-clic dans « Plans récents » ouvre le renommage | comportement de la liste | Échap, et **changer de feuille par la liste déroulante du panneau Groupes** |
| Capture noVNC 508×50, rendu minuscule ou figé | zoom / renderer Chrome ; le cadre change (1354×896, 1512×812, 1566×784) | `resize_window(1400, 950)` puis recharger l'URL ; **toujours faire une capture avant de cliquer** |
| Rapport natif sorti en pieds-pouces | option du rapport Plan Expert, distincte de l'échelle des plans | documenté en réserve R-057 ; vérifier `ScaleType` du `<Report>` |
| Une seule personne à la fois | **un seul exécuteur UI dans Plan Expert** ; la VM a été bloquée une après-midi par une session Antigravity/Gemini | ne pas toucher l'écran si quelqu'un l'utilise |
| Exports qui ouvrent un navigateur / une boîte Excel | comportement normal de Plan Expert | fermer IE/Edge ; Échap sur « How do you want to open » — **le `.xls` est quand même écrit** dans `Mes rapports` |

### 6.3 Lecture des plans et métré

| Symptôme | Cause | Correction |
|---|---|---|
| **« 3R » lu comme un appareil de chauffage** (artères F22/F23 à 0 m) | interprétation d'un symbole **sans vérifier la légende** (E104) | E104 = borne de recharge VE ; F22/F23 retirées, compteur BRVE, R-063. **Toujours remonter à la feuille de légende avant de nommer une famille** |
| Longueurs 0 m pour F22/F23 | destination non nommée sur les plans | ne pas inventer : `route='reserve'`, longueur nulle, statut explicite, réserve au registre |
| v5 : **tous les compteurs en carrés rouges, légende posée sur le dessin** | `Shape`, `Color` et `Legend` jamais paramétrés à l'import (valeurs par défaut `Shape=1`, `Color=-65536`, légende en 0/0) | `make_v6.py` + `rules_dupuis.py` : une règle forme/couleur/taille par famille, légende en 4250/1350 |
| Superposition : la feuille E406 rendait la page E407 du concurrent | **index de page décalé d'un** parce que E404 est absente de son PDF | table `PAGES` explicite (E400=9 … E409=17), confirmée par le texte du cartouche |
| Segmentation couleur trouvant trop peu d'objets | rendu à l'échelle 1, seuils trop serrés, rayon 14 pt | échelle 2, couleurs **échantillonnées sur les pastilles de légende**, appariement glouton 40 pt |
| Étiquettes vert fluo qui se chevauchent | placement fixe | candidats de position + test d'intersection + lignes de rappel (`diff_vert.py`) |
| Filtre `-notlike '*Plans*'` qui exclut « par-plans » | comparaison PowerShell **insensible à la casse** | commit de rattrapage `f1e9295` |
| Le 7z « Plans de blocage préliminaires » ne correspond à rien | fichier d'une autre soumission (S-1854 Sollio St-Hubert) | signalé, non comparé — **vérifier l'identité de chaque fichier reçu** |
| La visionneuse PDF de Chrome ne défile pas par CDP | plugin PDF | recadrages `pymupdf` ; rendu local Playwright pour vérifier une page de livraison |

### 6.4 Pièges de méthode (déduits des sources, à éviter dans le socle)

- **Exceptions codées par coordonnées** : `verification/additions.py` contient des tests du type
  `if r['sheet']=='E406' and abs(x-1264) < 3` pour étiqueter deux objets. Ça marche une fois, ce n'est pas
  reconductible — ces cas doivent devenir des lignes de données, pas des `if`.
- **Chemins absolus dans les scripts d'analyse** : `crosscheck_*.py`, `cc_scan.py`, `additions.py` et
  `make_v6.py` pointent `C:\Users\fvegi\Documents\Codex\2026-09-08\ouv\work\saint-michel\sources\…`, un dossier
  **extérieur au dépôt**. Le dépôt est auto-suffisant (`sources/plans/electrique/`), mais les scripts ne le
  savent pas : les rejouer tels quels échouera sur une autre machine.
- **`inject_lines.py` lit sa source dans `v3-roundtrip/incoming-project.zip`** — un fichier de transfert qui est
  en réalité le QPL XML, et que `.gitignore` exclut (`incoming-project.zip`). À remplacer par un argument.
- **Le connecteur Google Drive ne met pas à jour le contenu d'un fichier existant** : créer un nouveau fichier
  puis mettre l'ancien à la corbeille (`HANDOFF` §3b).
- **Ne jamais écrire un secret dans un fichier** : jeton GitHub dans les variables d'environnement utilisateur
  (`GH_TOKEN`/`GITHUB_TOKEN`), clé Tailscale dans `credentials.local.env` ; `.gitignore` exclut `*.private.json`
  (les fichiers de session des transferts).

---

## 7. Ce qu'il faut préparer pour une nouvelle soumission

Liste minimale, déduite de tout ce qui précède :

1. **Les PDF**, hachés en SHA-256 avant toute chose.
2. **Un projet Plan Expert nu** créé par import des PDF dans Plan Expert, jamais modifié ensuite, et le
   dossier de rasters qui l'accompagne. Relever les dimensions de page (pt) et du raster (px) : elles
   fondent toutes les conversions.
3. **Un fichier de projet** (JSON) portant : liste des feuilles avec `plan_name`, `layer_index`,
   `page_width_pt`, `page_height_pt` (= `plan-mapping.json`) ; feuilles à mettre à l'échelle et
   dénominateur ; niveaux du bâtiment ; position de légende ; paramètres de métré.
4. **Les points de calibration** : deux axes cotés par feuille, avec la cote d'architecte source et son
   sha256 (= `calibration-points.csv`), plus un objet de contrôle à mesurer dans Plan Expert.
5. **Une charte graphique** forme/couleur/taille par famille (l'équivalent de `rules_dupuis.py`), à défaut
   la légende du client ou du concurrent, échantillonnée sur ses pastilles.
6. **La table des familles et de leurs étiquettes texte** par feuille — c'est ce qui permet la
   contre-vérification automatique (`crosscheck_text.py` / `crosscheck_geo.py`).
7. **Un dépôt git** avec `.gitattributes` (`* text=auto eol=lf`, `*.qpl binary`), `tools/make_index.py`,
   `manifest.json` et la CI de validation.

Ordre d'exécution, en une ligne : `sources hachées → texte extrait → lots → consolidation → import v2 →
échelle v3 → artères v4 → contre-vérification v5 → charte + comparaison v6 → exports natifs → dossier →
livraison`, avec **un aller-retour Plan Expert (ouvrir / vérifier / sauvegarder / comparer le sha256) après
chaque version**.

---

## 8. État du relevé S-1857 au moment de la rédaction

Pour mémoire, l'étape restante côté S-1857 (`REPRODUCTION.md` §6.5, `HANDOFF` §3b/§3c) : ouvrir la v6 dans
Plan Expert, vérifier E406/E405/E401, sauvegarder, exporter rapports + plans PDF vers
`planexpert/06-v6-native/`, puis `uv run arteres/build_dossier.py v6`, LIVRAISON / Drive / GitLab+GitHub,
page de livraison et captures de preuve. 63 réserves et 22 questions d'addenda restent ouvertes.

---

*Document rédigé le 2026-09-10 à partir de la seule lecture du dépôt S-1857, sans modifier aucun de ses
fichiers. Toute valeur citée ici est vérifiable au chemin indiqué. Porté dans `dr-estimation-ia` le
2026-09-22 (voir consolidation.md).*
