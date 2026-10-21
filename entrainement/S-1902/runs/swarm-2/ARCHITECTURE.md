# ARCHITECTURE — essaim 2, chiffrage à l'aveugle S-1902 (méthode Dupuis)

Réécriture structurée de l'idée de Francis (IDEE-FRANCIS.md) par le chef (Claude Fable 5.1, réflexion élevée).
Ce document gouverne tout l'essaim : qui fait quoi, dans quel ordre, avec quels fichiers, et comment chaque
niveau choisit les prompts et l'effort de ses subalternes.

## 0. L'idée de Francis, reformulée

Une équipe hiérarchique à trois niveaux de délégation sous un chef :

| Niveau | Rôle | Modèle | Nombre | Qui écrit son prompt et choisit son effort |
|---|---|---|---|---|
| 0 | Chef | Claude Fable 5.1 (réflexion élevée) | 1 | Francis (IDEE-FRANCIS.md) → réécrit ici |
| 1 | Directeur | Claude Opus 5.5 (« opus ») | 2 | le chef |
| 2 | Chef de lot | Claude Sonnet 5.5 (« sonnet ») | 3 par directeur = 6 | son directeur |
| 3 | Releveur | Claude Haiku 5.5 (« haiku ») | 3 par chef de lot = 18 | son chef de lot |

Total : 2 + 6 + 18 = 26 agents subalternes. Chaque niveau décide lui-même (a) du découpage de son lot en trois
sous-lots, (b) du texte complet du prompt de chacun de ses subalternes, (c) de l'effort demandé à chacun
(`low` / `medium` / `high` / `xhigh` / `max`), en le justifiant d'une ligne. La profondeur de délégation est fixée
à 3 (releveur = feuille de l'arbre : il ne délègue à personne).

### Mécanique de relais (contrainte vérifiée : aucun niveau ne possède l'outil Agent)
Aucun agent de l'essaim ne peut en lancer un autre. Le pouvoir de décision reste à chaque niveau ; c'est la
**session principale** qui dispatche, niveau par niveau, les prompts écrits tels quels :
1. Le chef écrit `prompts/directeur-A.md` et `prompts/directeur-B.md` → la session principale lance les 2 Opus.
2. Chaque directeur écrit `prompts/<directeur>/chef-1.md`, `chef-2.md`, `chef-3.md` puis s'arrête → la session
   principale lance les 3 Sonnet de chaque directeur (6 en parallèle).
3. Chaque chef de lot écrit `prompts/<directeur>/chef-<n>/releveur-1.md`, `-2.md`, `-3.md` puis s'arrête → la
   session principale lance les 3 Haiku de chaque chef (18 en parallèle).
4. Les releveurs travaillent et écrivent `lots/releveur-<X><n>-<m>.json`.
5. Chaque chef de lot est **relancé** (même prompt + mention « tes releveurs ont fini ») : il vérifie et
   consolide en `lots/chef-<X><n>.json`.
6. Chaque directeur est **relancé** : il tranche entre ses chefs et consolide en `lots/directeur-<X>.json`.
7. Le chef consolide (ÉTAPE 2) : `chiffrage.py` → `chiffrage.json`, puis `NOTES.md` avec l'organigramme réel.

Format d'en-tête obligatoire de **tout** fichier de prompt (deux premières lignes, exactement) :
```
effort: <low|medium|high|xhigh|max>
modele: <opus|sonnet|haiku>
```
puis le prompt complet et autonome. Les niveaux inférieurs ne voient jamais cette conversation ni ce document
(sauf s'ils le lisent eux-mêmes dans le dossier) : **chaque brief doit se suffire à lui-même**.

## 1. Règles d'aveugle (à recopier mot pour mot dans chaque prompt, à tous les niveaux)

```
RÈGLES D'AVEUGLE (obligatoires, à recopier mot pour mot dans chaque prompt que tu écris) :
1. Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/ — tu travailles UNIQUEMENT dedans.
2. Interdit de lire quoi que ce soit hors de ce dossier : ni /home/claude/dr-estimation-ia, ni le web,
   ni d'autres dossiers d'entraînement, ni une mémoire ou un dépôt quelconque.
3. Tu n'as pas accès à la réponse de référence ; tu ne cherches ni à la retrouver ni à la deviner.
4. Rien n'est inventé : chaque ligne cite sa source (libellé EXACT du catalogue Dupuis, code Lumen de la
   feuille « Matériel Lumen », code de ligne de la feuille « Détail » (A-01…H-04), libellé de releve.xlsx,
   ou « jugement (Estimation_2) »). Ce qui est incertain va dans les notes, jamais dans une quantité muette.
5. Ne modifie rien dans le kit (releve.xlsx, entree/, catalogue-prix-temps-dupuis.csv, CONSIGNES.md,
   METHODE.md, rapport-releve.md, reserves.md). Tu n'écris que dans lots/ et prompts/.
6. Tu ne peux pas lancer d'agent toi-même : tu écris les prompts de tes subalternes dans prompts/… avec
   l'en-tête « effort: … » / « modele: … », tu t'arrêtes, et la session principale les lance tels quels.
   (Un releveur ne délègue à personne : il fait le travail et écrit son JSON.)
```

## 2. Le kit (ce que chaque niveau doit savoir pour lire les fichiers)

- `releve.xlsx` (openpyxl, `data_only=True`) : feuilles `Résumé`, `Par famille`, `Par libellé` (Libellé, Famille,
  Quantité, Description, Source), `Par feuille` (feuille × libellé × quantité), `Marques` (645 lignes :
  feuille, libellé, x, y, source, note), `Feuilles`, `Réserves`. **Les portées (INSTALLER / ENLEVER /
  RELOCALISER / CONSERVER) ne sont PAS dans le classeur** : elles sont dans le tableau « famille | total |
  portées » de `rapport-releve.md`. CONSERVER = aucun travail (0 qté, 0 h), sauf cas justifié en note.
- `entree/reference-Estimation_2.xlsx` : feuille `Détail` (colonnes Code, Description, Réf. plan, Qté, Unité,
  Prix mat. unit., Total mat., h/unité, Total h, Total MO, Total ligne, Notes) — codes A-01…H-04 + OPT-1…4
  (hors total) ; ses heures sont un « estimé Léna AI à valider » : on garde ses **quantités** hors plan, pas
  ses heures (sauf « jugement (Estimation_2) » quand le catalogue n'a rien). Feuille `Matériel Lumen`
  (Code Lumen, Description, Qté, Unité, Prix unit., Total, Base) : prix réguliers Lumen 2026-10-07, pour les
  familles absentes du catalogue Dupuis. Feuille `Sommaire` : taux 124 $/h « référence Jo » — **non retenu**,
  le taux Dupuis de METHODE.md prévaut (85 $/h, dossiers août–octobre 2026).
- `entree/reference-Bordereau_de_prix.xlsx` : articles électriques 3.22 à 3.38 (+ 5.11 percement du plancher,
  5.19 démolition des systèmes électriques, 6.1/6.2 frais) — chaque ligne du chiffrage reçoit un article.
- `entree/reference-Releve_Alarme_Incendie.xlsx` (AI-01…AI-09) et `reference-Releve_Eclairage_Urgence.xlsx`
  (A1 11, C1 12, C1_1 6, C1_3 15, C-SUSP 20 rangées, E 4, Z6 3) : relevés de demande de prix.
- `catalogue-prix-temps-dupuis.csv` : 2 068 lignes, `;` comme séparateur, encodage utf-8-sig. Colonnes à
  utiliser : `description`, `um` (U = unité, P = pied), `prix_a_utiliser`, `temps_a_utiliser` (= « PRIX À
  UTILISER » / « TEMPS À UTILISER », dernière valeur de Dupuis). **Jamais** `prix_unit_median` /
  `temps_unit_median`. Il n'y a PAS de colonne TEMPSEC : les conduits se chiffrent en temps/pi × longueur en
  pieds (1 m = 3,2808 pi). Les libellés sont tronqués/approximatifs (ex. « DETECTEUR A FUME », « RELO PANNEAU
  ANNONCIA ») : chercher par sous-chaînes et retenir le libellé exact dans `src`.
- `METHODE.md` : lots confirmés (éclairage 11 893 $, distribution 6 200 $, JCI 7 400 $ + 2 détecteurs 600 $,
  GPR 1 250 $), taux 85 $/h, facteur 1,244, arrondi des heures au multiple de 10 vers le haut.

## 3. Nomenclature commune (le pivot qui permet de joindre quantités et prix)

Les deux directeurs produisent des lignes portant le **même `code`** ; le chef joint sur ce code.
- Sur plan : `<FAM>-<P>` où P ∈ {I = installer, E = enlever, R = relocaliser}. FAM :
  `PC` prise double 15 A · `PU` prise USB · `PG` prise DDFT · `SD` sortie data · `TV` sortie TV ·
  `INT` interrupteur simple · `TH` thermostat · `BJ` boîte de jonction · `MP` monument plancher ·
  `LC` lecteur de carte · `GA` gâche · `DM` détecteur de mouvement · `ENC` encastré · `ENCU` encastré urgence ·
  `L14` LED 1x4 · `L22` LED 2x2 · `L4` LED 4 pi · `LLIN` luminaire linéaire · `LA1` `LC1` `LC11` `LC13` `LE`
  luminaires neufs E-008 · `Z6` enseigne · `DF` détecteur de fumée · `SM` station manuelle · `HP` haut-parleur ·
  `PA` panneau annonciateur · `MM` moteur monophasé · `MT` moteur triphasé · `BC` boîtier C.
  Exemples : `PC-I` (25), `PC-E` (7), `PC-R` (8), `SD-I` (65), `ENC-E` (26), `LA1-I` (11), `MM-R` (6).
- Hors plan : le code de la feuille Détail tel quel (`A-07`, `B-01`, `C-05`, `D-12`, `H-01`…), ou un code
  `X-nn` pour une ligne que le kit justifie mais que Détail n'a pas (ex. `X-01 SCAN DALLE`, `X-02 NACELLE`).
- Lots fournisseur : `LOT-ECL`, `LOT-DIST`, `LOT-JCI`, `LOT-DET`, `LOT-GPR` (montants de METHODE.md).

Portées : INSTALLER → prix + temps d'installation ; ENLEVER → 0 $ + temps d'enlèvement ; RELOCALISER → prix
selon catalogue (souvent 0 $) + temps de relocalisation ; CONSERVER → rien.

## 4. Découpage du travail

### Directeur A — QUANTITÉS (Opus, effort **high**)
Produit `lots/directeur-A.json` : toutes les lignes avec `q` et `u`, `p` et `h` à `null`, `art` proposé.
- Chef de lot A1 (Sonnet) — services sur plan : prises PC/PU/PG, data SD, TV, INT, TH, BJ, MP, LC, GA, DM,
  BC, portées depuis rapport-releve.md, répartition par feuille (E101/E102 existant, E104/E105 neuf).
- Chef de lot A2 (Sonnet) — éclairage, urgence, alarme, mécanique, distribution sur plan : ENC/ENCU/L14/L22/
  L4/LLIN/HP (enlever, relocaliser), luminaires neufs LA1/LC1/LC11/LC13/LE, Z6, DF/SM/PA, MM/MT, + lignes
  Détail B-01…B-09 (panneau et disjoncteurs, hors relevé), A-07…A-10.
- Chef de lot A3 (Sonnet) — hors plan depuis Détail : conduits et filage (en pi), percements D-12/E-07,
  scan dalle (bordereau 3.32), raccordements C-01…C-04, D-09…D-11, D-16, E-03, E-06, E-11, F-05, F-08…F-10,
  G-02…G-07, H-01…H-04, lots fournisseur ; et la **liste des lignes Détail à exclure** parce qu'elles
  doublent le relevé sur plan (A-01…A-06, D-01…D-08, E-01, E-02, E-04, E-05, F-01…F-04, F-06, F-07, G-01).
Pourquoi `high` : comptage et portées déjà faits par la machine ; la difficulté est l'arbitrage des doubles
comptes plan/Détail et la conversion d'unités, pas la lecture — `xhigh` n'apporterait rien, `medium`
risquerait de laisser passer un double compte.

### Directeur B — PRIX ET TEMPS (Opus, effort **xhigh**)
Produit `lots/directeur-B.json` : pour chaque code de la nomenclature (§3) et chaque code Détail retenu,
`p` et `h` unitaires, `q` à `null`, `art` final, `src` = libellé exact ; plus `lots` et les vérifications.
- Chef de lot B1 (Sonnet) — dispositifs : correspondance catalogue pour PC/PU/PG/SD/TV/INT/TH/BJ/MP/LC/GA/DM
  et leurs variantes enlever/relocaliser (ENLEVER PRISE, RELO PRISE…), avec la dernière valeur.
- Chef de lot B2 (Sonnet) — éclairage/urgence/alarme/mécanique/distribution : luminaires (0 $ + temps),
  enseignes, têtes, détecteurs, panneaux, disjoncteurs, moteurs/UTA, annonciateur relocalisé, nacelle, et
  lots confirmés ; conduits/filage (CONDUIT 3/4 03C12, CONDUIT VIDE 3/4, CONDUIT 1 …, conversion m → pi) ;
  familles absentes → Lumen (feuille Matériel Lumen) + temps par jugement (Estimation_2), chaque fois en note.
- Chef de lot B3 (Sonnet) — ventilation par article du bordereau (3.22…3.38, 5.11, 5.19) pour chaque code,
  percements/scan, et **vérification des doubles comptes** (un même objet physique ne peut pas être payé par
  une ligne sur plan ET par une ligne Détail ; prix d'assemblage Dupuis = boîte + plaque + raccord inclus,
  donc pas de boîtes Lumen en plus pour les mêmes prises).
Pourquoi `xhigh` : 2 068 libellés approximatifs, règle « dernière valeur jamais la médiane », trois sources de
prix concurrentes (Dupuis, Lumen, jugement) et la détection des doubles comptes — c'est là que se décide
l'écart au référentiel. `max` est réservé au chef pour la consolidation finale.

Le chef (ÉTAPE 2) : joint A et B sur `code`, tranche les désaccords (règle : le plan gagne sur Détail pour les
quantités ; Dupuis dernier gagne sur Lumen pour les prix ; Lumen gagne sur le jugement), écrit `chiffrage.py`
(déterministe, stdlib + openpyxl, lit `lots/*.json` et le kit), exécute, vérifie
`materiel + heures_chargees × taux == total_acceo` et `prix_vente == arrondi millier(total_acceo × 1,244)`,
puis `NOTES.md`.

## 5. Format des sorties intermédiaires (`lots/<niveau>-<nom>.json`)

```json
{
  "niveau": "releveur|chef|directeur",
  "nom": "A1-2",
  "modele_demande": "haiku",
  "effort_demande": "medium",
  "lignes": [
    {"code": "PC-I", "desc": "Prise double 15 A 120 V neuve", "q": 25, "u": "U", "p": null, "h": null,
     "art": "3.28", "src": "releve.xlsx Par libellé PRISE DOUBLE 15A 95 ; rapport-releve.md INSTALLER 25"}
  ],
  "notes": ["hésitations, familles introuvables, choix faits, lignes exclues et pourquoi"]
}
```
- `code` : §3. `u` : `U` (unité), `PI` (pied), `LOT`. `p` : prix unitaire $ (`null` si pas ce lot). `h` : temps
  unitaire en heures (`null` si pas ce lot). `art` : article du bordereau (texte, ex. `"3.31"`). `src` : source
  exacte et vérifiable.
- Un directeur peut ajouter `"lots": {"LOT-ECL": 11893, ...}` et `"exclusions": [ {code, raison} ]`.
- Les releveurs écrivent `lots/releveur-<X><n>-<m>.json` (ex. `releveur-A1-2.json`), les chefs de lot
  `lots/chef-<X><n>.json`, les directeurs `lots/directeur-<X>.json`.

## 6. Critères de vérification à chaque niveau (avant d'écrire son JSON)

1. Le JSON se charge (`python3 -c "import json;json.load(open(...))"`) et contient `lignes` + `notes`.
2. Chaque ligne a un `src` qui pointe vers une cellule/un libellé réellement lu — un chef de lot ou un
   directeur **rouvre** le fichier pour au moins 5 lignes de chaque subalterne (contrôle au hasard) et note
   le score x/5 dans ses notes ; une erreur trouvée = tout le lot du subalterne est revu.
3. Pas de médiane : pour le lot B, `p == prix_a_utiliser` et `h == temps_a_utiliser` de la ligne citée.
4. Pas de double compte : un code n'apparaît qu'une fois par fichier consolidé ; une ligne Détail exclue est
   listée dans `exclusions` avec la ligne sur plan qui la remplace.
5. Sommes de contrôle attendues (ordre de grandeur, pas une cible) : part main-d'œuvre 30–69 % du total
   ACCEO, 450–520 h par 100 k$ de prix de vente (METHODE.md §6). Hors plage → expliquer en note, ne pas forcer.
6. Un rapport d'agent n'est pas une preuve : le niveau supérieur juge sur le fichier `lots/*.json`, pas sur
   le récit.

## 7. Comment chaque niveau choisit prompts et effort de ses subalternes

- Le prompt d'un subalterne contient, dans cet ordre : son rôle et son nom (ex. « releveur A1-2 »), les
  RÈGLES D'AVEUGLE du §1 mot pour mot, le dossier de travail, le lot précis (familles ou codes, fichiers et
  feuilles à lire, colonnes à utiliser), la nomenclature des codes (§3) pour son lot, le format JSON (§5) et le
  nom exact du fichier de sortie, les critères de vérification (§6), et pour un niveau 1 ou 2 : le nombre EXACT
  de subalternes qu'il doit briefer (3), le dossier `prompts/…` où écrire, l'obligation de recopier les règles
  d'aveugle et de transmettre ce même mode d'emploi, et l'ordre de s'arrêter après avoir écrit ses prompts.
- Effort : `low` pour une recopie mécanique d'un petit tableau ; `medium` pour un comptage/une recherche
  simple dans un fichier ; `high` quand il faut arbitrer (portées, doublons, libellés approximatifs) ;
  `xhigh` quand une erreur se propage à tout le chiffrage (prix/temps, doubles comptes) ; `max` seulement pour
  une consolidation finale. Chaque choix est justifié en une ligne dans les notes du JSON du niveau qui l'a fait.
- Le découpage en trois doit être **disjoint** (aucune famille dans deux sous-lots) et **couvrant** (toute
  famille ou tout code du lot est attribué) ; le niveau qui découpe écrit la liste dans ses notes.
