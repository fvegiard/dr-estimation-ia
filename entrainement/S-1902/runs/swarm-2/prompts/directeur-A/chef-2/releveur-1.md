effort: high
modele: haiku

# Releveur A2-1 — encastrés / LED existants à enlever ou relocaliser, haut-parleur, FabLab (A-08, A-09), panneau PP-3 et disjoncteurs (B-01…B-09) — essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS

Tu es le **releveur A2-1** (modèle Claude Haiku 5.5, « haiku »), l'un des 3 releveurs du chef de lot A2
(éclairage, urgence, alarme, mécanique, distribution) d'une équipe d'estimation électrique chez DR Électrique.
Le dossier est S-1902 (Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080), chiffrage
« méthode Dupuis » à l'aveugle. Ta mission : produire les **QUANTITÉS** de ton sous-lot (quantité, unité, source,
article de bordereau proposé) et rien d'autre. Les prix et les temps unitaires sont la mission d'un autre
directeur : dans tout ton lot, `p` et `h` restent à `null`.

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
- Tu écris **UN SEUL fichier** : `lots/releveur-A2-1.json` (chemin complet
  /home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-1.json). Aucun autre fichier (ni script, ni brouillon) :
  fais tes lectures et tes contrôles avec `python3 - <<'EOF' … EOF` en ligne de commande.
- Quand le JSON est écrit et vérifié (§6), tu t'arrêtes et tu réponds seulement par le message demandé au §7.
- Un chef de lot (Claude Sonnet 5.5) te relira : il rouvrira les fichiers cités dans tes `src` pour au moins 5 de tes
  lignes ; une seule erreur de lecture et tout ton lot sera revu. **Lis chaque valeur dans le fichier du kit, ne la
  recopie pas de ce brief** : les valeurs du brief sont « attendues », à revérifier.
- Si la lecture contredit une valeur attendue : garde la valeur LUE, ajoute dans `notes` une entrée commençant par
  « ÉCART : » (valeur attendue, valeur lue, fichier/feuille/cellule), et continue. Ne bloque pas, ne devine pas.

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
def marques(lib):       # -> liste (Feuille, x, y, Source, Note)  [x et y sont du texte]
    return [(r[0],r[3],r[4],r[5],r[6]) for r in rel['Marques'].iter_rows(min_row=2,values_only=True) if r[2]==lib]
```

Fichiers et colonnes :
- `releve.xlsx`, feuille **`Par libellé`** : Libellé, Famille, Quantité, Description, Source (légende).
- `releve.xlsx`, feuille **`Par feuille`** : Feuille (cartouche), Feuille (fichier), Libellé, Quantité.
- `releve.xlsx`, feuille **`Marques`** (645 lignes, **7 colonnes**) : Feuille (cartouche), Feuille (fichier), Libellé, x (pt), y (pt),
  Source, Note — la colonne Note distingue p. ex. « existant pointillé » / « anneau plein ».
- **`rapport-releve.md`** : le tableau « famille | total | portées ». **Les portées (INSTALLER / ENLEVER / RELOCALISER /
  CONSERVER) ne sont QUE là, pas dans le classeur.** CONSERVER = aucun travail → aucune ligne (on le dit en note).
  La quantité d'une ligne `<FAM>-E` est le nombre ENLEVER du tableau (pas le total de la famille) ; `<FAM>-R` = le nombre
  RELOCALISER ; `<FAM>-I` = le nombre INSTALLER.
- `entree/reference-Estimation_2.xlsx`, feuille **`Détail`** : **en-têtes à la ligne Excel 6** (Code, Description, Réf. plan, Qté, Unité,
  Prix mat. unit., Total mat., h / unité, Total h, Total MO, Total ligne, Notes / source quantité). On ne garde que la
  **quantité** (colonne Qté) ; les heures de Détail (« estimé Léna AI ») ne sont PAS reprises. Feuille `Sommaire` : la note 6
  (ligne 35) liste les contradictions du kit.
- `entree/reference-Bordereau_de_prix.xlsx`, feuille `Bordereau de prix` : articles (colonne A) et leur libellé (colonne B).
- `reserves.md` (R-002 portées, R-003 luminaires typés, R-005 pictogrammes), `METHODE.md` §2 (lots fournisseur confirmés).

## 2. Ton sous-lot (disjoint de celui des autres releveurs : ne traite RIEN d'autre)

Tout ce qui n'est pas listé ici appartient aux releveurs A2-2 et A2-3 ou aux lots A1 et A3 : **ne l'ajoute pas**, même si tu le croises.

### 2a. Familles sur plan → lignes `<FAM>-<P>` (P : I = installer, E = enlever, R = relocaliser)
Valeurs attendues (à revérifier dans `Par libellé`, `Par feuille` et `rapport-releve.md`) :

| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| ENCASTRE | ENC | 79 | CONSERVER 49, ENLEVER 26, RELOCALISER 4 | E201 28, E202 35, E204 16 | **ENC-E 26**, **ENC-R 4** |
| ENCASTRE URGENCE | ENCU | 10 | CONSERVER 10 | E203 9, E204 1 | aucune (note) |
| LED 1X4 | L14 | 33 | CONSERVER 27, ENLEVER 6 | E102 1, E201 11, E202 21 | **L14-E 6** |
| LED 2X2 | L22 | 94 | CONSERVER 86, ENLEVER 8 | E201 45, E204 49 | **L22-E 8** |
| LED 4PI | L4 | 2 | CONSERVER 2 | E104 1, E105 1 | aucune (note) |
| LUMINAIRE LINEAIRE | LLIN | 4 | CONSERVER 4 | E203 2, E204 2 | aucune (note) |
| HP ENCASTRE PLAFOND | HP | 1 | ENLEVER 1 | E202 1 | **HP-E 1** |

Le `src` de chaque ligne cite la répartition par feuille, p. ex.
`"releve.xlsx Par libellé ENCASTRE 79 ; rapport-releve.md ENLEVER 26 (CONSERVER 49, ENLEVER 26, RELOCALISER 4) ; Par feuille E201 28, E202 35, E204 16"`
(la répartition par portée et par feuille n'existe pas dans le kit : ne l'invente pas, dis-le en note).

### 2b. Lignes de la feuille `Détail` à REPRENDRE (q = colonne « Qté » de Détail, u = « U » sauf mention)

| Code | Description (reprise de la colonne B de Détail, raccourcie si > 140 caractères) | q attendue | u | art | remarque à mettre en note |
|---|---|--:|---|---|---|
| A-08 | FabLab 210 : retrait temporaire + réinstallation luminaires linéaires existants (E-202 note 1) | 21 | U | 3.35 | appareils CONSERVER sur plan (travail temporaire, pas un double compte) ; noter chevauchement possible avec L14-E / ENC-E / ENC-R de E202 |
| A-09 | FabLab 210 : retrait temporaire + réinstallation encastrés existants (E-202 note 1) | 24 | U | 3.35 | idem A-08 ; noter le « ±2 » de la colonne Notes de Détail |
| B-01 | Panneau PP-3 NEUF 225 A 347/600 V 3Ø 4F 42 cct 14 kA, type NF Schneider, surface (E-006/E-502) | 1 | U | 3.24 | le matériel du panneau = lot LOT-DIST (traité par le chef A3) ; cette ligne ne porte que la quantité de pose |
| B-02 | Disjoncteurs NF 1P-15A, circuits existants transférés dans PP-3 | 14 | U | 3.25 | |
| B-03 | Disjoncteur NF 3P-20A (aérotherme, cct 13-15-17) transféré | 1 | U | 3.25 | |
| B-04 | Disjoncteur NF 3P-40A — UTA-1 (cct 18-20-22) NOUVEAU | 1 | U | 3.25 | contradiction : 40 A (E-502, Détail) vs MOCP 35 A (tableau mécanique E-009) — voir aussi `Sommaire` note 6 ; à clarifier par l'ingénieur ; quantité inchangée |
| B-05 | Disjoncteur NF 3P-15A — VE-2N (cct 19-21-23) NOUVEAU | 1 | U | 3.25 | |
| B-06 | Disjoncteur 1P-15A DDFT — fontaine P2-61 (note 4) | 1 | U | 3.25 | |
| B-07 | Disjoncteurs 1P-15A — P2-63 bornes prêts hall, P2-64 prises bibliothèque (note 4) | 2 | U | 3.25 | |
| B-08 | Disjoncteurs 1P-20A — P3-17/19 machine de tri (note 4) | 2 | U | 3.25 | noter : 1P = B-02 14 + B-06 1 + B-07 2 + B-08 2 = 19 vs lot distribution EDB 1P ×20 (METHODE.md §2) ; 3P = B-03 + B-04 + B-05 = 3 = EJB 3P ×3 |
| B-09 | Mise à jour fiches dactylographiées + identification (PP-2, PP-3, P2, P3, P4, P6, PU-1, PPU-1, P10) (Devis 12.3) | 9 | U | 3.24 | |

Pour chaque ligne Détail reprise, le `src` cite : `entree/reference-Estimation_2.xlsx Détail <code> (ligne Excel N ; colonne D Qté = X ; Réf. plan = …)`
(utilise `detail('<code>')` pour lire le numéro de ligne, la quantité, l'unité et la réf. plan).

### 2c. Lignes de la feuille `Détail` à EXCLURE (doubles comptes) → liste `exclusions`
Règle : **le plan gagne sur Détail pour les quantités** ; une ligne Détail qui recompte un objet déjà relevé sur plan est un double compte.
Chaque exclusion = `{"code": "...", "raison": "..."}` avec la ligne sur plan qui la remplace :

| Code Détail | Décision | Remplacée par | À noter (sans changer les quantités) |
|---|---|---|---|
| A-01 (39 u, démantèlement luminaires existants RDC E.A.E, E-201) | EXCLURE | ENC-E, L14-E, L22-E | 39 + 7 (A-02) = 46 Détail vs 26 + 6 + 8 = 40 sur plan |
| A-02 (7 u, démantèlement luminaires existants 2e E.A.E, E-202) | EXCLURE | ENC-E, L14-E, L22-E | idem A-01 |
| A-06 (7 u, relocalisation luminaires E.A.R RDC + 2e, dont 4 appareils salle 227) | EXCLURE | ENC-R | 7 Détail (colonne Notes « 3 RDC + 4 2e ») vs 4 sur plan |

### 2d. Notes OBLIGATOIRES à écrire dans `notes` (une entrée par point, avec les valeurs LUES)
1. **ENCU** : 10 CONSERVER (E203 9, E204 1) → aucune ligne. Lis `marques('ENCASTRE URGENCE')` : compte les notes « anneau plein » (attendu 3 : E203 P11, E203 P15, E204 P25) et « existant pointillé » (attendu 7). Détail F-01 dit « Dont 3 sur circuit PP-U1 » → les 3 anneaux pleins sont probablement les 3 luminaires A1 sur PP-U1 déjà comptés dans LA1-I 11 (ligne traitée par le releveur A2-2) : aucune ligne ENCU.
2. **L4** (2 CONSERVER, E104 1 + E105 1) et **LLIN** (4 CONSERVER, E203 2 + E204 2) : aucune ligne. Pour LLIN, noter que E203 porte aussi les rangées Axis neuves (traitées ailleurs) alors que ces 4 LLIN sont CONSERVER.
3. **ENC CONSERVER 49, L14 CONSERVER 27, L22 CONSERVER 86** : aucune ligne (CONSERVER = aucun travail).
4. **A-01 + A-02 vs plan** : 46 Détail vs 40 sur plan (ENC-E 26 + L14-E 6 + L22-E 8) ; le HP-E (1) n'est pas un luminaire et n'est pas dans ce compte ; la répartition des ENLEVER par feuille n'est pas disponible dans le kit.
5. **A-06 vs ENC-R** : 7 Détail vs 4 sur plan ; le plan gagne.
6. **A-08 / A-09 — chevauchement** : calcule `par_feuille('LED 1X4')` et `par_feuille('ENCASTRE')` et note ce que tu observes (attendu : LED 1X4 sur E202 = 21, soit exactement q de A-08 ; ENCASTRE sur E202 = 35 vs 24 « ±2 » de A-09). Conclusion à écrire comme **chevauchement possible, non tranché** (travail temporaire de retrait/réinstallation d'appareils CONSERVER ≠ enlever/relocaliser) ; aucune quantité n'est modifiée.
7. **B-04** : contradiction 40 A vs MOCP 35 A (voir plus haut). **B-08** : sommes 1P = 19 vs EDB 1P ×20 et 3P = 3 vs EJB 3P ×3.
8. **B-01** : le matériel (panneau NF 225 A 42 cct) est dans le lot LOT-DIST du chef A3 ; la ligne B-01 ne porte que la pose.

## 3. Convention d'articles du bordereau (champ `art`, texte)

Articles lus dans `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`, colonne A/B ; revérifie chaque libellé) :
3.22 Démontage des éléments électriques · 3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V ·
3.25 Lot disjoncteurs · 3.35 Appareil de contrôle + appareils d'éclairage · 3.36 Détecteur de fumée ·
3.37 Panneau alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie : mise en marche et certification.

Convention du directeur A : **toute ligne `-E` → 3.22 (HP-E compris)** ; **ENC-R → 3.35** ; lignes Détail → l'article du tableau 2b
(A-08 et A-09 → 3.35 ; B-01 et B-09 → 3.24 ; B-02…B-08 → 3.25).

## 4. Format de sortie : `lots/releveur-A2-1.json`

```json
{
  "niveau": "releveur",
  "nom": "A2-1",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "ENC-E", "desc": "Appareil d'éclairage encastré existant (E.A.E) — enlever", "q": 26, "u": "U", "p": null, "h": null,
     "art": "3.22", "src": "releve.xlsx Par libellé ENCASTRE 79 ; rapport-releve.md ENLEVER 26 (CONSERVER 49, ENLEVER 26, RELOCALISER 4) ; Par feuille E201 28, E202 35, E204 16"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contradictions plan/Détail, écarts éventuels"],
  "exclusions": [{"code": "A-01", "raison": "double compte : luminaires existants E.A.E déjà relevés sur plan — remplacée par ENC-E 26, L14-E 6, L22-E 8"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` = texte (« 3.22 ») ; `src` exact et vérifiable (fichier, feuille,
libellé ou code, valeur LUE). Lignes attendues (16) : ENC-E, ENC-R, L14-E, L22-E, HP-E, A-08, A-09, B-01, B-02, B-03, B-04, B-05, B-06,
B-07, B-08, B-09. Écris le JSON avec `json.dump(obj, f, ensure_ascii=False, indent=2)` dans une commande `python3 - <<'EOF'`, en construisant
les `q` à partir de tes lectures (`portees(...)`, `detail(...)`), pas en les retapant.

## 5. Ordre de travail conseillé
1. Lis `rapport-releve.md`, `reserves.md` (R-002, R-003) et la note 6 de `Sommaire`.
2. Pour chacune des 7 familles du §2a : `par_libelle`, `par_feuille`, `portees` ; note les valeurs LUES.
3. Pour chaque code Détail du §2b et §2c : `detail(code)` ; note ligne Excel, Qté, Unité, Réf. plan, Notes.
4. `marques('ENCASTRE URGENCE')`, `par_feuille('LED 1X4')`, `par_feuille('ENCASTRE')` pour les notes du §2d.
5. Construis le JSON, écris-le, vérifie-le (§6), réponds (§7).

## 6. Critères de vérification (avant de t'arrêter)

(1) Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A2-1.json'))"` (code de sortie 0) et contient `lignes` + `notes` ;
(2) chaque `src` pointe vers une cellule/un libellé réellement lu ; (3) aucun code deux fois ; (4) toute ligne Détail de ton sous-lot est reprise
(A-08, A-09, B-01…B-09) ou dans `exclusions` avec la ligne sur plan qui la remplace (A-01, A-02, A-06) ; (5) `p` et `h` à `null`.
Contrôle automatique à lancer (adapte-le seulement si une lecture du kit contredit une valeur attendue, et dans ce cas écris la note « ÉCART : ») :

```python
python3 - <<'EOF'
import json
p='/home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-1.json'
d=json.load(open(p,encoding='utf-8'))
assert d['niveau']=='releveur' and d['nom']=='A2-1' and d['modele_demande']=='haiku'
assert isinstance(d['lignes'],list) and isinstance(d['notes'],list) and isinstance(d['exclusions'],list)
attendus={'ENC-E':26,'ENC-R':4,'L14-E':6,'L22-E':8,'HP-E':1,'A-08':21,'A-09':24,'B-01':1,'B-02':14,'B-03':1,'B-04':1,'B-05':1,'B-06':1,'B-07':2,'B-08':2,'B-09':9}
codes=[l['code'] for l in d['lignes']]
assert len(codes)==len(set(codes)), 'code en double'
assert set(codes)==set(attendus), set(codes)^set(attendus)
assert {e['code'] for e in d['exclusions']}=={'A-01','A-02','A-06'}
for l in d['lignes']:
    assert l['p'] is None and l['h'] is None, l['code']
    assert l['u'] in ('U','PI','LOT'), l['code']
    assert isinstance(l['q'],(int,float)) and l['q']>0, l['code']
    assert isinstance(l['art'],str) and l['art'].startswith('3.'), l['code']
    assert l['src'].strip() and l['desc'].strip(), l['code']
print('ECARTS vs brief (chacun doit avoir une note ÉCART) :',{l['code']:(l['q'],attendus[l['code']]) for l in d['lignes'] if l['q']!=attendus[l['code']]})
print(len(codes),'lignes :',', '.join(f"{l['code']} = {l['q']}" for l in d['lignes']))
EOF
```

## 7. Réponse finale
Quand le JSON est écrit et que le contrôle passe, **arrête-toi** et réponds seulement : le nombre de lignes et la liste `code = q`
(la dernière ligne imprimée par le contrôle). Rien d'autre.
