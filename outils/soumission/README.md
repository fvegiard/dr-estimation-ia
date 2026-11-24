# `outils/soumission/` — chiffrage « méthode Dupuis » et soumission DR (référence officielle)

Gelé le 2026-10-20 par Francis (décision : « ceci = référence officielle »). Première application : `dossiers/S-1902/soumission/`
(Bibliothèque Georgette-Lepage, 194 000 $ avant taxes le 2026-10-20 ; rév. 1 du 2026-10-26 avec l'addenda E-01 : 233 000 $). Tout est reproductible depuis ce dépôt ; aucune valeur n'est inventée :
chaque ligne du chiffrage cite sa source (catalogue de M. Dupuis, liste Lumen, prix confirmé par Francis).

## 1. Le processus complet (du courriel d'invitation à la soumission remise)

| # | Étape | Entrée | Outil / fichier | Sortie | Preuve exigée |
|---|---|---|---|---|---|
| 1 | Réception de l'invitation (EG, SEAO/BSDQ) | courriel RDJ transféré par André Lamothe | — | `INBOX/<S>/` : plans PDF + addendas | courriel archivé |
| 2 | Relevé de quantités à l'aveugle | plans électriques (E-1xx/E-2xx) | `uv run releve/run.py <S>` (route `blocs`, zéro agent) | `dossiers/<S>/` : `releve.xlsx`, `Plans-annotes.pdf` (pastilles + légende « RELEVÉ Exxx – MATÉRIEL » par feuille, calques), `Rapport-de-metre.pdf`, `STATUT.md` | planches `controle/*.png` ouvertes et notées (CLAUDE.md §Autonomie) |
| 3 | Quantités hors plan (longueurs, panneaux, raccordements) | notes des plans, devis, tableaux E-00x | estimation de l'estimateur (hypothèses écrites : m/course, m/point) | `entree/reference-Estimation_*.xlsx` (feuille Détail) | chaque hypothèse notée dans la colonne Notes |
| 4 | Prix matériel courant | compte Lumen PRO 4417250 (prix **réguliers**, jamais promo) | lumen.ca connecté | feuille « Matériel Lumen » | date du relevé de prix inscrite |
| 5 | **Chiffrage méthode Dupuis** (ce dossier) | quantités (2, 3) + catalogue Dupuis (`prix/dupuis/`) + prix Lumen (4) + lots fournisseur | `chiffrage_dupuis.py --ventiler` du dossier | `chiffrage_dupuis.json` (lignes, heures, matériel, lots, historique, par article) + ventilation réécrite dans `soumission.json` | sortie console : matériel, heures relevées/chargées, total ACCEO, par article, prix soumis = Σ ventilation |
| 6 | Classeur imprimable | `chiffrage_dupuis.json` + `soumission.json` | `build_xlsx.py` | `<S>_Chiffrage_methode_Dupuis.xlsx` (Sommaire, Détail, Par article) | recalcul LibreOffice : 0 erreur ; aperçu PNG des pages regardé |
| 7 | Soumission client | `soumission.json` (ventilation = somme des articles) | `gen_soumission.py` | `Soumission_<S>_<projet>.pdf` (gabarit DR) | PNG de chaque page regardé ; montant en chiffres = en lettres = somme des articles |
| 8 | Regroupement : `pypdf` fusionne soumission + chiffrage (lettre) en `<S>_Dossier_complet.pdf` ; les plans (format D) restent à part | PDF (7) + PDF du classeur (6) | `pypdf` | `<S>_Dossier_complet.pdf` | nombre de pages = 3 + 6 |
| 9 | Dépôt dans le dépôt Git | les fichiers ci-dessus | `git commit` sur `main` | `dossiers/<S>/soumission/` | commit poussé |

Ordre imposé : **toujours un aperçu PNG regardé avant d'émettre un PDF** (demande de Francis, 2026-10-20).

## 2. La méthode de chiffrage de M. Dupuis (reproduite, chiffres à l'appui)

Reconstituée à partir de 27 de ses sommaires ACCEO/Expert Estimateur 2026 (`prix/dupuis/Catalogue-prix-temps-Dupuis.xlsx`, 4 629 lignes
transcrites, onglets LISEZ-MOI / Catalogue / Paramètres Jo / Backtest / Lignes sources) et de `eewin/docs/CALCUL-SOUMISSION.md`.

1. **Matériel** = Σ quantité × *prix vendant d'assemblage* du catalogue — **dernière valeur** de Dupuis, pas la médiane (règle du LISEZ-MOI :
   « sa valeur la plus récente ; médiane/min/max = contrôle seulement »). Les prix d'assemblage incluent boîte/plaque/raccord
   (prise duplex 15 A 64,81 $, USB 77,45 $, DDFT 65,38 $, tel/data 3/4 22,32 $, interrupteur 75,47 $, percement 150 $, scan dalle 1 250 $,
   conduit 3/4 03c12 4,24 $/pi, conduit vide 3/4 1,41 $/pi, monument 250 $, lecteur de carte 15 $, gâche 15 $, thermostat 35 $, sortie TV 15 $).
   Administration et profit = **0 %** dans son sommaire (la marge est dans le prix vendant).
2. **Luminaires, enseignes, têtes d'urgence, détecteurs, panneaux** : 0 $ en ligne (temps seulement) + un **PRIX DE LOT** fournisseur.
   Ici (rév. 1) : lot éclairage ADD E-01 **42 820,79 $ = soumission fournisseur Éclairage Hi-Tech S100946-R1** (seule vraie soumission reçue),
   E/Z6 1 909,80 $ (allocation Gerrie), lot distribution 6 200 $ (allocation ≈ NF 3 400 $ + EDB ×20 + EJB ×3), JCI 7 400 $ + 2 détecteurs 600 $
   (allocation, prix demandé par Jo le 2026-10-08), GPR 1 250 $ (Dupuis). **Règle : un lot est « ferme » seulement avec une soumission fournisseur
   datée en main ; sinon il est marqué ALLOCATION dans la colonne source (jaune dans le classeur), même si Francis a retenu le montant.**
   Une soumission fournisseur transmise par courriel (ex. Daniel Dupuis → Francis) est une source légitime : citer no, date, validité et ce qu'elle exclut.
3. **Heures** = Σ quantité × *temps unitaire* Dupuis (prise 1,175 h ; USB 1,125 h ; DDFT 1,3 h ; tel/data 0,63–0,89 h ; luminaire 0,75 h ;
   enseigne 1 h ; tête 0,5 h ; détecteur 0,5 h ; panneau 8 h ; disjoncteur 1P 0,2 h / 3P 1 h ; percement 1 h ; luminaire enlevé 0,5 h ;
   prise enlevée 0,35 h ; relocalisation de prise 1,5 h ; conduit 3/4 03c12 0,113 h/pi ; conduit vide 3/4 0,056 h/pi ; moteur 0,75 h ; UTA 1 h ;
   annonciateur relocalisé 8 h ; nacelle 1 250 $ / 16 h). **Toujours la colonne « À UTILISER » (dernier Dupuis), jamais la médiane** — l'écart sur les seuls conduits de S-1902 fait 11 000 $ de prix de vente. Formule ACCEO pour les conduits : QTE × TEMPUNI + sections de 10 pi × TEMPSEC.
4. **Heures chargées** = heures relevées arrondies **vers le haut** au multiple de 10 (S-1881 : 4 128,6 → 4 150 ; S-1854 : 5 872,6 → 5 880).
5. **Main-d'œuvre** = heures chargées × **taux** : 85 $/h sur ses dossiers d'août–octobre 2026 (S-1797, S-1835, S-1854, S-1881 ; 99 $/h sur
   S-1857 ; 110 $/h Canderel centre-ville ; 78–82 $/h en hiver-printemps). Règle de choix à confirmer avec Jo.
6. **Total sommaire ACCEO** = matériel + main-d'œuvre. Contrôle : part MO 30–69 % (médiane ≈ 45 %), 450–520 h par 100 k$ de prix.
7. **Prix de vente** = total ACCEO × **1,244** — unique couple observé : S-1844, sommaire 191 909,19 $ → prix remis 238 744 $
   (courriel Dupuis 2026-08-26 ; versions Jo 253 600 / 259 000 $ = ×1,32–1,35). Arrondi au millier. Facteur modifiable dans le classeur.

Résultat S-1902 v4 (2026-10-20) : matériel 66 649,11 $ + 1 050 h × 85 $ = 155 899,11 $ → × 1,244 = 193 938 → **194 000 $** ; **rév. 1 / v5 (2026-10-26,
addenda E-01, lot éclairage Hi-Tech R1) : matériel 98 376,90 $ + 1 050 h × 85 $ = 187 626,90 $ → × 1,244 = 233 408 → 233 000 $** (comparatifs : Estimation_2 Léna
112 381 $ sans marge ; v2 du midi 158 296 $ ; v3 avec médianes de conduits 183 000 $ ; Dupuis sort historiquement +18–20 % au-dessus du plus bas soumissionnaire — tableau de suivi 2026).

## 3. Le gabarit de soumission DR (`gen_soumission.py`)

Reproduit la sortie réelle de DR (S-1913, S-1914 du 2026-10-20) : bandeau bordeaux `#6B1A1A` avec le **logo officiel** (`logo_dr.png`, copie de
`soumissions-brand/assets/logo_dr.png`), « SOUMISSION S-xxxx » + « Varennes, le … », bloc **CLIENT / DÉTAILS** sur fond rose `#F5E6E6`,
prix forfaitaire en chiffres **et en lettres** « — taxes en sus », note de prix, **VENTILATION selon le bordereau** (tableau), **FOURNIR ET
INSTALLER**, **PRIX SÉPARÉS**, **EXCLUSIONS**, **CONDITIONS 1) à 10)** (texte fixe DR), clause de volatilité des matériaux, remerciement,
signature, encadré **APPROBATION / BON DE COMMANDE**, pied « DR Électrique inc. | Merci de votre confiance | Soumission S-xxxx Page N ».
Le prix forfaitaire n'est jamais saisi : c'est la somme des articles de `ventilation` (Decimal, arrondi demi-cent) ; le montant en lettres
vient de `num2words` (fr). Police Helvetica (comme les sorties DR).

## 4. Reproduire (commandes)

```bash
python -m venv .venv-soumission && .venv-soumission/bin/pip install -r outils/soumission/requirements.txt   # reportlab, num2words, openpyxl, pillow
PY=.venv-soumission/bin/python
$PY dossiers/S-1902/soumission/chiffrage_dupuis.py --ventiler           # -> chiffrage_dupuis.json + ventilation de soumission.json + sommaire console
$PY outils/soumission/build_xlsx.py dossiers/S-1902/soumission/chiffrage_dupuis.json dossiers/S-1902/soumission/soumission.json \
    dossiers/S-1902/soumission/S-1902_Chiffrage_methode_Dupuis.xlsx
$PY outils/soumission/gen_soumission.py dossiers/S-1902/soumission/soumission.json \
    dossiers/S-1902/soumission/Soumission_S-1902_Georgette-Lepage.pdf
# aperçus PNG (obligatoires avant d'émettre) :
soffice --headless --convert-to pdf --outdir /tmp dossiers/S-1902/soumission/S-1902_Chiffrage_methode_Dupuis.xlsx
pdftoppm -r 80 -png /tmp/S-1902_Chiffrage_methode_Dupuis.pdf /tmp/xl ; pdftoppm -r 60 -png dossiers/S-1902/soumission/Soumission_S-1902_Georgette-Lepage.pdf /tmp/soum
```
Sur Windows (poste yogafv) : `pwsh`, même venv (`py -m venv`), LibreOffice remplacé par Excel → Fichier → Imprimer → PDF (mise en page déjà réglée).

Vérifié le 2026-10-20 (bac à sable cloud, Python 3.13) : chiffrage → 155 899,11 $ / 1 045,85 h → 1 050 h ; classeur 177 formules, 0 erreur
(recalcul LibreOffice) ; PDF 3 pages, « 194 000,00 $ » = « Cent quatre-vingt-quatorze mille dollars » = Σ articles ; dossier regroupé 9 pages.

## 5. Nouveau dossier — marche à suivre

1. Copier `dossiers/S-1902/soumission/chiffrage_dupuis.py` dans `dossiers/<S>/soumission/`, remplacer les lignes `add(...)` par les quantités
   du nouveau relevé (`releve.xlsx` + feuille Détail de l'estimation) ; pour chaque ligne, chercher le libellé dans
   `prix/dupuis/catalogue-prix-temps-dupuis.csv` et prendre **PRIX À UTILISER / TEMPS À UTILISER** (dernier Dupuis) ; famille absente →
   Lumen (prix régulier) + temps NECA « Normal » ou jugement, **toujours écrit dans la colonne source**.
2. Mettre le taux (`TAUX`) selon la période/le type de projet (voir onglet « Paramètres Jo »).
3. Copier `soumission.json`, remplir client/détails/travaux/prix séparés/exclusions avec les mêmes codes d'article que le chiffrage ; lancer
   `chiffrage_dupuis.py --ventiler` : il écrit la `ventilation` (total article × facteur, arrondi au dollar ; prix soumis arrondi au millier ; 3.31 absorbe l'écart).
4. Générer, regarder les PNG, corriger, puis seulement produire les PDF ; commit sur `main`.

## 6. Ce qui reste ouvert (pas inventé, donc dit)

- La règle de choix du taux horaire (85 / 99 / 110 $) et la règle exacte de l'arrondi des heures sont « à confirmer avec Jo ».
- Un seul couple sommaire → prix remis (S-1844) fonde le facteur 1,244 ; un deuxième couple affinerait.
- S-1902 rév. 1 : l'addenda E-01 lui-même n'a pas été lu (salle de plans RDJ `lecatalogue.ca` en erreur 503 le 2026-10-26 ; addendas 2 et 3 non reçus) —
  les quantités d'éclairage viennent de la soumission Hi-Tech ; E/Z6, panneau NF et JCI restent des allocations sans soumission fournisseur.
- Le relevé S-1902 est « EN VALIDATION » (pas de `.qpl` Dupuis pour comparer marque par marque) ; le relevé IA compte 65 sorties data et
  20 prises USB (pris) ; les 22 prises MALT isolées sont classées avec les DDFT par le relevé (gardées en IG, 1 DDFT fontaine).
