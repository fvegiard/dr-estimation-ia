effort: xhigh
modele: haiku

# Releveur A2-3 — alarme incendie (DF, SM, PA, G-01, G-04, G-05, G-06) et mécanique (MM, MT, A-10, C-01…C-04, X-03) — essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS

Tu es le **releveur A2-3** (modèle Claude Haiku 5.5, « haiku »), l'un des 3 releveurs du chef de lot A2
(éclairage, urgence, alarme, mécanique, distribution) d'une équipe d'estimation électrique chez DR Électrique.
Le dossier est S-1902 (Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080), chiffrage
« méthode Dupuis » à l'aveugle. Ta mission : produire les **QUANTITÉS** de ton sous-lot (quantité, unité, source,
article de bordereau proposé) et rien d'autre. Les prix et les temps unitaires sont la mission d'un autre
directeur : dans tout ton lot, `p` et `h` restent à `null`. Ton sous-lot est le plus délicat du chef de lot A2
(arbitrages plan/Détail, portées, un même objet physique vu par deux sources) : une erreur ici se propage à tout
le chiffrage, donc lis chaque valeur dans les fichiers et prends le temps de recouper.

RÈGLES D'AVEUGLE (obligatoires) :
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

## 0. Mécanique (tu es un releveur : la feuille de l'arbre)

- **Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/** (tous les chemins ci-dessous sont relatifs à ce dossier).
- Tu ne lances personne et tu ne délègues à personne (aucun outil Agent, aucun `claude -p`, aucun sous-agent). Tu n'as
  aucun subalterne et tu n'écris aucun prompt : tu fais le travail toi-même.
- Tu écris **UN SEUL fichier** : `lots/releveur-A2-3.json` (chemin complet
  /home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-3.json). Aucun autre fichier (ni script, ni brouillon) :
  fais tes lectures et tes contrôles avec `python3 - <<'EOF' … EOF` en ligne de commande.
- Quand le JSON est écrit et vérifié (§6), tu t'arrêtes et tu réponds seulement par le message demandé au §7.
- Un chef de lot (Claude Sonnet 5.5) te relira : il rouvrira les fichiers cités dans tes `src` pour au moins 5 de tes
  lignes ; une seule erreur de lecture et tout ton lot sera revu. **Lis chaque valeur dans le fichier du kit, ne la
  recopie pas de ce brief** : les valeurs du brief sont « attendues », à revérifier.
- Si la lecture contredit une valeur attendue : garde la valeur LUE, ajoute dans `notes` une entrée commençant par
  « ÉCART : » (valeur attendue, valeur lue, fichier/feuille/cellule), et continue. Ne bloque pas, ne devine pas.
- Les hypothèses marquées **« vérifier »** ci-dessous (correspondance MM/MT ↔ lignes C-0x/A-10) : si ta lecture les contredit, **reprends la
  ligne Détail concernée** (elle n'est alors plus exclue) et explique en note, au lieu de l'exclure.

## 1. Comment lire le kit

Lecture avec `python3` + openpyxl, `data_only=True`. Boîte à outils à coller en tête de chaque commande `python3 - <<'EOF'` :

```python
import openpyxl, json
D='/home/claude/entrainement/S-1902/swarm-2/'
rel=openpyxl.load_workbook(D+'releve.xlsx',data_only=True)
est=openpyxl.load_workbook(D+'entree/reference-Estimation_2.xlsx',data_only=True)
def par_libelle(lib):   # -> (Famille, Quantité, Description, Source (légende))
    for r in rel['Par libellé'].iter_rows(min_row=2,values_only=True):
        if r[0]==lib: return r[1],r[2],r[3],r[4]
def par_feuille(lib):   # -> {feuille: quantité}
    return {r[0]:r[3] for r in rel['Par feuille'].iter_rows(min_row=2,values_only=True) if r[2]==lib}
def portees(lib):       # -> ligne du tableau « famille | total | portées » de rapport-releve.md
    for l in open(D+'rapport-releve.md',encoding='utf-8'):
        if l.startswith('| '+lib+' |'): return l.strip()
def detail(code):       # -> (ligne Excel, Description, Réf. plan, Qté, Unité, Notes / source quantité)
    for row in est['Détail'].iter_rows(min_row=7):
        if row[0].value==code: return row[0].row,row[1].value,row[2].value,row[3].value,row[4].value,row[11].value
def marques(lib):       # -> liste (Feuille, x, y, Source, Note)  [x et y sont du TEXTE : utilise float(...)]
    return [(r[0],r[3],r[4],r[5],r[6]) for r in rel['Marques'].iter_rows(min_row=2,values_only=True) if r[2]==lib]
```

Fichiers et colonnes :
- `releve.xlsx`, feuille **`Par libellé`** : Libellé, Famille, Quantité, Description, Source (légende).
- `releve.xlsx`, feuille **`Par feuille`** : Feuille (cartouche), Feuille (fichier), Libellé, Quantité.
- `releve.xlsx`, feuille **`Marques`** (645 lignes, **7 colonnes**) : Feuille (cartouche), Feuille (fichier), Libellé, x (pt), y (pt),
  Source, Note — la colonne Note distingue p. ex. « existant (tracé pointillé) » / « neuf (tracé plein) » / « bloc S146 ».
- **`rapport-releve.md`** : le tableau « famille | total | portées ». **Les portées (INSTALLER / ENLEVER / RELOCALISER /
  CONSERVER) ne sont QUE là, pas dans le classeur.** CONSERVER = aucun travail → aucune ligne (on le dit en note).
  La quantité d'une ligne `<FAM>-I` est le nombre INSTALLER du tableau, `<FAM>-E` le nombre ENLEVER, `<FAM>-R` le nombre RELOCALISER
  (jamais le total de la famille). **La portée par marque ou par feuille n'existe pas dans le kit** : ne l'invente pas.
- `entree/reference-Estimation_2.xlsx`, feuille **`Détail`** : **en-têtes à la ligne Excel 6** (Code, Description, Réf. plan, Qté, Unité,
  Prix mat. unit., Total mat., h / unité, Total h, Total MO, Total ligne, Notes / source quantité). On ne garde que la
  **quantité** (colonne Qté) ; les heures de Détail (« estimé Léna AI ») ne sont PAS reprises. Feuille `Sommaire` : la note 6 (ligne 35) liste les
  contradictions du kit (UTA-1 40 A vs MOCP 35 A ; détecteurs RDC vs étage). Feuille `Matériel Lumen` (en-têtes ligne 5 : Code Lumen, Description,
  Qté, Unité, Prix unit., Total, Base de quantité) : la ligne 43 est HUBHBL1372.
- `entree/reference-Releve_Alarme_Incendie.xlsx`, feuille `Relevé` (en-têtes ligne 7 : Item, Description, Qté, Unité, Réf. plan, Notes, Prix unit., Total) :
  AI-01 (ligne 9, 2 détecteurs neufs E-203), AI-03 (12), AI-04 (13), AI-05 (14, « Relocalisation annonciateur Simplex existant »), AI-06 (15),
  AI-07 (16, option vérification des dispositifs existants retirés/réinstallés), ligne 21 (la quantité aux plans prévaut sur le schéma E-007).
- `entree/reference-Bordereau_de_prix.xlsx`, feuille `Bordereau de prix` : articles (colonne A) et leur libellé (colonne B).
- `reserves.md` (R-002 portées, R-005 pictogrammes dont les détecteurs de fumée), `METHODE.md` §2 (lots confirmés : JCI 7 400 $ + 2 détecteurs 600 $).

## 2. Ton sous-lot (disjoint de celui des autres releveurs : ne traite RIEN d'autre)

Tout ce qui n'est pas listé ici appartient aux releveurs A2-1 et A2-2 ou aux lots A1 et A3 : **ne l'ajoute pas**, même si tu le croises
(p. ex. B-01…B-09, A-08, A-09, F-0x, G-02, G-03, G-07, C-05…C-08 ne sont PAS à toi).

### 2a. Familles sur plan → lignes `<FAM>-<P>` (P : I = installer, E = enlever, R = relocaliser)
Valeurs attendues (à revérifier dans `Par libellé`, `Par feuille` et `rapport-releve.md`) :

| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| DETECTEUR FUMEE | DF | 10 | CONSERVER 6, INSTALLER 2, RELOCALISER 1, ENLEVER 1 | E201 5, E203 5 | **DF-I 2**, **DF-R 1**, **DF-E 1** |
| STATION MANUELLE | SM | 4 | CONSERVER 4 | E201 4 | aucune (note) |
| PANNEAU ANNONCIATEUR | PA | 1 | INSTALLER 1 | E203 1 | **PA-R 1** (arbitrage ci-dessous : PA-R, pas PA-I) |
| MOTEUR MONOPHASE | MM | 9 | RELOCALISER 6, INSTALLER 3 | E103 6, E105 3 | **MM-R 6**, **MM-I 3** |
| MOTEUR TRIPHASE | MT | 9 | CONSERVER 5, INSTALLER 4 | E102 5, E105 2, E106 2 | **MT-I 4** (CONSERVER 5 = note) |

Le `src` de chaque ligne cite la répartition par feuille, p. ex.
`"releve.xlsx Par libellé MOTEUR MONOPHASE 9 ; rapport-releve.md RELOCALISER 6 (INSTALLER 3) ; Par feuille E103 6, E105 3"`.

**Arbitrage PA (décision du directeur)** : le PANNEAU ANNONCIATEUR « INSTALLER 1 » de E203 est le nouvel emplacement de l'annonciateur Simplex existant
relocalisé (Détail G-04 « Relocalisation panneau annonciateur Simplex — réutiliser câbles… », note 1 E-007 ; relevé alarme AI-05 « Relocalisation annonciateur
Simplex existant » ; bordereau 3.37 « déplacement annonciateur ») → **un seul objet physique**. Code **PA-R** (pas PA-I), q 1, art **3.37**, `src` qui cite
rapport-releve.md INSTALLER 1 + Détail G-04 + AI-05.

**Arbitrage MM / MT / A-10 / C-01…C-04 (« vérifier » à chaque ligne)** :
- MM-R 6 = les « 6 E.A.R sur E-103 » de Détail A-10 (`par_feuille('MOTEUR MONOPHASE')` : E103 = 6 ; Détail A-10, colonne Notes) → **reporte la description
  de A-10** (« Toit : débrancher, entreposer sectionneurs, isoler/couvrir câbles, rebrancher équipements de ventilation (E.A.R) ») dans le `desc` et le `src` de MM-R.
- MT-I 4 = C-01 (UTA-01, E-106) 1 + C-02 (VE-02N, E-106) 1 + C-03 (2 chaudières CH-01/CH-02, E-105) 2. Vérifie : MOTEUR TRIPHASE sur E106 = 2 (UTA-01 + VE-02N)
  et sur E105 = 2 (chaudières) ; les 5 MOTEUR TRIPHASE de E102 sont les CONSERVER 5 (la portée par feuille n'est pas dans le kit : c'est une **inférence** cohérente
  avec les totaux — E105 + E106 = 4 = INSTALLER 4 — à écrire comme inférence).
- MM-I 3 = C-04 (3 humidificateurs HUM-1/2/3 Carel 120 V/1Ø, E-105). Vérifie : MOTEUR MONOPHASE sur E105 = 3.

### 2b. Lignes de la feuille `Détail` à REPRENDRE (q = colonne « Qté » de Détail)

| Code | Description | q attendue | u | art | remarque à mettre en note |
|---|---|--:|---|---|---|
| **X-03** (nouvelle, hors Détail) | « Sectionneur sans fusible 30 A — HUM-1/2/3 » | 3 | U | 3.23 | `src` : « Détail C-04 (sectionneur sans fusible 30A 1Ø ×3) ; Matériel Lumen HUBHBL1372 qté 3 » (lis la ligne 43 de `Matériel Lumen` : code, description, qté 3 ; sa colonne « Base de quantité » dit « Devis 20 : service intensif — à valider ») ; le sectionneur de C-04 n'est pas un symbole relevé sur plan, d'où cette ligne |
| G-05 | Démontage/protection/réinstallation dispositifs AI existants dans zones touchées (Réf. plan E-201/E-203) | 1 | LOT | 3.36 | noter chevauchement possible avec DF-R 1 / DF-E 1 ; voir aussi AI-07 du relevé alarme (option, prix séparé) ; Détail Notes : « Allocation — à valider » |
| G-06 | Assistance électricien lors de la programmation / vérification ULC-S537 (E-007 note 3) | 1 | LOT | 3.38 | JCI fait la programmation/vérification/certificat (lot LOT-JCI du chef A3) ; cette ligne est l'assistance de l'électricien (AI-06 du relevé alarme) |

Pour chaque ligne Détail reprise, le `src` cite : `entree/reference-Estimation_2.xlsx Détail <code> (ligne Excel N ; colonne D Qté = X ; Unité = …)`
(utilise `detail('<code>')`).

### 2c. Lignes de la feuille `Détail` à EXCLURE (doubles comptes) → liste `exclusions`
Règle : **le plan gagne sur Détail pour les quantités** ; une ligne Détail qui recompte un objet déjà relevé sur plan est un double compte.
Chaque exclusion = `{"code": "...", "raison": "..."}` avec la ligne sur plan qui la remplace :

| Code Détail | Décision | Remplacée par | À noter |
|---|---|---|---|
| G-01 (2 détecteurs de fumée adressables, E-203) | EXCLURE | **DF-I 2** | la fourniture des 2 détecteurs = lot LOT-DET (METHODE.md : « 2 détecteurs 600 $ »), traité par le chef A3 ; la pose est dans DF-I |
| G-04 (1 u relocalisation panneau annonciateur Simplex, note 1 E-007) | EXCLURE | **PA-R 1** | même objet physique que le PANNEAU ANNONCIATEUR de E203 (voir arbitrage PA) |
| A-10 (6 u toit : débrancher, entreposer sectionneurs, rebrancher équipements de ventilation E.A.R, E-103/E-106) | EXCLURE | **MM-R 6** | Détail Notes : « 6 E.A.R sur E-103 » |
| C-01 (UTA-01 York KE036 575 V/3Ø au toit, E-106) | EXCLURE | **MT-I** | vérifier (voir arbitrage MM/MT) |
| C-02 (VE-02N Plymovent FUA-2700 1,5 HP 575 V/3Ø au toit, E-106) | EXCLURE | **MT-I** | vérifier |
| C-03 (2 chaudières CH-01/CH-02, E-105) | EXCLURE | **MT-I** | vérifier ; MT-I 4 = C-01 + C-02 + C-03 ×2 ; Détail Notes : « Réutilisation selon état — à vérifier » |
| C-04 (3 humidificateurs HUM-1/2/3 120 V/1Ø, E-105) | EXCLURE | **MM-I 3** | vérifier ; son sectionneur sans fusible 30 A = ligne **X-03** |

### 2d. Notes OBLIGATOIRES à écrire dans `notes` (une entrée par point, avec les valeurs LUES)
1. **SM** : 4 CONSERVER (E201 4 ; `marques('STATION MANUELLE')` : blocs S319 ×2 et S320 ×2) → aucune ligne. **MT** : CONSERVER 5 (E102 5) → aucune ligne.
2. **DF — recoupement des sources** : `marques('DETECTEUR FUMEE')` donne 10 marques : E201 5 « bloc S146 » ; E203 1 « bloc S146 » + 3 « instance manuelle : existant (tracé pointillé) » (P07, P08, P12)
   + 1 « instance manuelle : neuf (tracé plein) — P23 ; relevé alarme AI-01 ». Le rapport donne CONSERVER 6, INSTALLER 2, RELOCALISER 1, ENLEVER 1 : **le rapport fait foi** (DF-I 2, DF-R 1, DF-E 1).
   Écarts à noter : `Marques` ne montre qu'**un seul** détecteur « neuf (tracé plein) » alors que le rapport dit INSTALLER 2, le relevé alarme AI-01 = 2 et Détail G-01 = 2 (salle de tri 110 + secteur commis 110.8) ;
   la portée ENLEVER/RELOCALISER n'est pas lisible par marque.
3. **DF — mêmes coordonnées sur deux feuilles** : calcule la distance entre chaque détecteur E203 « existant pointillé » (P07, P08, P12) et les détecteurs de E201 (x, y en pt, `float(...)`) ; attendu : ≈ 1 pt, soit les
   mêmes emplacements que 3 des 5 détecteurs de E201 (462,414 ≈ 462,413 ; 541,378 ≈ 541,377 ; 1034,390 ≈ 1033,389). Note : ce sont probablement les mêmes objets physiques dessinés sur la feuille d'existant (E201) et
   sur la feuille de travaux (E203) → le total 10 pourrait surcompter 3 ; sans effet sur DF-I/DF-R/DF-E si ces 3 sont CONSERVER (portée par marque absente du kit) ; **aucune quantité modifiée**, le rapport fait foi.
4. **Contradiction détecteurs RDC vs étage** : Sommaire note 6 et relevé alarme (ligne 21) — le schéma E-007 montre 2 détecteurs neufs à l'étage, les plans E-203/E-204 en montrent 2 neufs au RDC et aucun à l'étage → **les plans prévalent** : DF-I 2 au RDC.
5. **PA-R** : explique l'arbitrage (même objet que G-04 et AI-05 ; un seul objet physique ; PA-R et non PA-I ; art 3.37 ; `marques('PANNEAU ANNONCIATEUR')` : 1 marque E203 « bloc S328 »). Note aussi Détail G-04 : « Nouvel emplacement à confirmer ».
6. **MM / MT** : écris la vérification « vérifier » faite pour chaque ligne (A-10 ↔ MM-R 6 sur E103 ; C-01 + C-02 ↔ MT E106 2 ; C-03 ×2 ↔ MT E105 2 ; C-04 ×3 ↔ MM E105 3 ; somme MT-I = 1 + 1 + 2 = 4 ; somme MM = 6 + 3 = 9 ; MT = 4 + 5 CONSERVER = 9) et signale toute inférence (portée par feuille).
7. **B-04** (hors de ton sous-lot, traité par A2-1) : le moteur UTA-1 est lié à la contradiction « disjoncteur 40 A (E-502) vs MOCP 35 A (E-009) » de Sommaire note 6 — mentionne-la en une ligne comme renvoi, sans créer de ligne.
8. **G-05 / G-06 / X-03** : écris les chevauchements possibles et le rôle de chaque ligne (voir tableau 2b) ; X-03 ne double aucun symbole relevé (le sectionneur n'est pas un symbole de `Marques`).

## 3. Convention d'articles du bordereau (champ `art`, texte)

Articles lus dans `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`, colonne A/B ; revérifie chaque libellé) :
3.22 Démontage des éléments électriques · 3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V ·
3.25 Lot disjoncteurs · 3.35 Appareil de contrôle + appareils d'éclairage · 3.36 Détecteur de fumée ·
3.37 Panneau alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie : mise en marche et certification.

Convention du directeur A : **toute ligne `-E` → 3.22 (DF-E compris)** ; **DF-I et DF-R → 3.36** ; **PA-R → 3.37** ; **MM-*, MT-*, X-03 → 3.23** ;
lignes Détail → l'article du tableau 2b (G-05 → 3.36 ; G-06 → 3.38 ; X-03 → 3.23).

## 4. Format de sortie : `lots/releveur-A2-3.json`

```json
{
  "niveau": "releveur",
  "nom": "A2-3",
  "modele_demande": "haiku",
  "effort_demande": "xhigh",
  "lignes": [
    {"code": "MM-R", "desc": "Moteur monophasé existant de ventilation au toit (E.A.R, E-103) — débrancher, entreposer les sectionneurs, isoler/couvrir les câbles, rebrancher (Détail A-10)", "q": 6, "u": "U", "p": null, "h": null,
     "art": "3.23", "src": "releve.xlsx Par libellé MOTEUR MONOPHASE 9 ; rapport-releve.md RELOCALISER 6 (INSTALLER 3) ; Par feuille E103 6, E105 3 ; Détail A-10 (6 E.A.R sur E-103)"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contradictions plan/Détail, écarts éventuels, inférences"],
  "exclusions": [{"code": "A-10", "raison": "double compte : 6 moteurs monophasés E.A.R sur E-103 déjà relevés sur plan — remplacée par MM-R 6"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` = texte (« 3.23 ») ; `src` exact et vérifiable (fichier, feuille,
libellé ou code, valeur LUE). Lignes attendues (10) : DF-I, DF-R, DF-E, PA-R, MM-R, MM-I, MT-I, X-03, G-05, G-06.
Descriptions suggérées : DF-I « Détecteur de fumée adressable neuf (RDC E-203 : salle de tri 110 + secteur commis 110.8) — pose ; fourniture = LOT-DET » ;
DF-R « Détecteur de fumée existant — relocaliser » ; DF-E « Détecteur de fumée existant — enlever » ; PA-R « Panneau annonciateur Simplex existant — relocaliser au nouvel emplacement (E203) » ;
MM-I « Moteur monophasé neuf à raccorder — humidificateurs HUM-1/2/3 Carel 120 V/1Ø (E-105) » ; MT-I « Moteurs triphasés neufs à raccorder — UTA-01 York KE036 et VE-02N Plymovent FUA-2700 (toit E-106) + chaudières CH-01/CH-02 (E-105) ».
Écris le JSON avec `json.dump(obj, f, ensure_ascii=False, indent=2)` dans une commande `python3 - <<'EOF'`, en construisant les `q` à partir de tes lectures
(`portees(...)`, `detail(...)`), pas en les retapant.

## 5. Ordre de travail conseillé
1. Lis `rapport-releve.md`, `reserves.md` (R-002, R-005), la note 6 de `Sommaire`, le relevé alarme incendie (AI-01…AI-09) et `METHODE.md` §2.
2. Pour chacune des 5 familles du §2a : `par_libelle`, `par_feuille`, `portees`, `marques` ; note les valeurs LUES. Fais le calcul de distance du §2d point 3.
3. Pour G-01, G-04, G-05, G-06, A-10, C-01, C-02, C-03, C-04 : `detail(code)` ; note ligne Excel, Qté, Unité, Réf. plan, Notes. Lis la ligne 43 de `Matériel Lumen`.
4. Fais les vérifications « vérifier » du §2a (E106 = 2, E105 = 2, E105 MM = 3, E103 MM = 6).
5. Construis le JSON, écris-le, vérifie-le (§6), réponds (§7).

## 6. Critères de vérification (avant de t'arrêter)

(1) Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A2-3.json'))"` (code de sortie 0) et contient `lignes` + `notes` ;
(2) chaque `src` pointe vers une cellule/un libellé réellement lu ; (3) aucun code deux fois ; (4) toute ligne Détail de ton sous-lot est reprise
(G-05, G-06, X-03) ou dans `exclusions` avec la ligne sur plan qui la remplace (G-01, G-04, A-10, C-01, C-02, C-03, C-04) ; (5) `p` et `h` à `null`.
Contrôle automatique à lancer (adapte-le seulement si une lecture du kit contredit une valeur attendue — dans ce cas la ligne Détail correspondante est reprise,
pas exclue, et tu écris la note « ÉCART : ») :

```python
python3 - <<'EOF'
import json
p='/home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-3.json'
d=json.load(open(p,encoding='utf-8'))
assert d['niveau']=='releveur' and d['nom']=='A2-3' and d['modele_demande']=='haiku'
assert isinstance(d['lignes'],list) and isinstance(d['notes'],list) and isinstance(d['exclusions'],list)
attendus={'DF-I':2,'DF-R':1,'DF-E':1,'PA-R':1,'MM-R':6,'MM-I':3,'MT-I':4,'X-03':3,'G-05':1,'G-06':1}
arts={'DF-I':'3.36','DF-R':'3.36','DF-E':'3.22','PA-R':'3.37','MM-R':'3.23','MM-I':'3.23','MT-I':'3.23','X-03':'3.23','G-05':'3.36','G-06':'3.38'}
codes=[l['code'] for l in d['lignes']]
assert len(codes)==len(set(codes)), 'code en double'
assert set(codes)==set(attendus), set(codes)^set(attendus)
assert {e['code'] for e in d['exclusions']}=={'G-01','G-04','A-10','C-01','C-02','C-03','C-04'}
for l in d['lignes']:
    assert l['p'] is None and l['h'] is None, l['code']
    assert l['u'] in ('U','PI','LOT'), l['code']
    assert isinstance(l['q'],(int,float)) and l['q']>0, l['code']
    assert l['art']==arts[l['code']], (l['code'],l['art'])
    assert l['src'].strip() and l['desc'].strip(), l['code']
print('ECARTS vs brief (chacun doit avoir une note ÉCART) :',{l['code']:(l['q'],attendus[l['code']]) for l in d['lignes'] if l['q']!=attendus[l['code']]})
print(len(codes),'lignes :',', '.join(f"{l['code']} = {l['q']}" for l in d['lignes']))
EOF
```

## 7. Réponse finale
Quand le JSON est écrit et que le contrôle passe, **arrête-toi** et réponds seulement : le nombre de lignes et la liste `code = q`
(la dernière ligne imprimée par le contrôle). Rien d'autre.
