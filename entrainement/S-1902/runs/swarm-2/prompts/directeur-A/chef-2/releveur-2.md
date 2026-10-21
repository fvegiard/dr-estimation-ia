effort: high
modele: haiku

# Releveur A2-2 — luminaires neufs E-008 (A1, C1, C1_1, C1_3, E), enseignes de sortie Z6, rangées Axis (F-05), lot JB éclairage (F-10) — essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS

Tu es le **releveur A2-2** (modèle Claude Haiku 5.5, « haiku »), l'un des 3 releveurs du chef de lot A2
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
- Tu écris **UN SEUL fichier** : `lots/releveur-A2-2.json` (chemin complet
  /home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-2.json). Aucun autre fichier (ni script, ni brouillon) :
  fais tes lectures et tes contrôles avec `python3 - <<'EOF' … EOF` en ligne de commande.
- Quand le JSON est écrit et vérifié (§6), tu t'arrêtes et tu réponds seulement par le message demandé au §7.
- Un chef de lot (Claude Sonnet 5.5) te relira : il rouvrira les fichiers cités dans tes `src` pour au moins 5 de tes
  lignes ; une seule erreur de lecture et tout ton lot sera revu. **Lis chaque valeur dans le fichier du kit, ne la
  recopie pas de ce brief** : les valeurs du brief sont « attendues », à revérifier.
- Si la lecture contredit une valeur attendue : garde la valeur LUE, ajoute dans `notes` une entrée commençant par
  « ÉCART : » (valeur attendue, valeur lue, fichier/feuille/cellule), et continue. Ne bloque pas, ne devine pas.
  (Exception : les arbitrages ci-dessous marqués « décision du directeur » — p. ex. LE-I = 3 — se suivent tels quels et se notent.)

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
  Source, Note — pour les luminaires typés la Note dit « étiquette A1 sur bloc S035 », « étiquette C1 (2 modules sur la rangée…) », etc.
- **`rapport-releve.md`** : le tableau « famille | total | portées ». **Les portées (INSTALLER / ENLEVER / RELOCALISER /
  CONSERVER) ne sont QUE là, pas dans le classeur.** La quantité d'une ligne `<FAM>-I` est le nombre INSTALLER du tableau.
- `entree/reference-Estimation_2.xlsx`, feuille **`Détail`** : **en-têtes à la ligne Excel 6** (Code, Description, Réf. plan, Qté, Unité,
  Prix mat. unit., Total mat., h / unité, Total h, Total MO, Total ligne, Notes / source quantité). On ne garde que la
  **quantité** (colonne Qté) ; les heures de Détail (« estimé Léna AI ») ne sont PAS reprises.
- `entree/reference-Releve_Eclairage_Urgence.xlsx`, feuille `Relevé` (en-têtes ligne 7 : Type, Fabricant / modèle (E-008), Qté, Unité,
  Tension / charge, Notes, Prix unit., Total) : contrôle croisé — A1 11 (ligne 9), C1 12 (10), C1_1 6 (11), C1_3 15 (12), C-SUSP 20 rangées (13),
  E 4 (14), Z6 3 (16) ; la ligne 4 dit « Aucun appareil neuf à l'étage (E-204) ».
- `entree/reference-Bordereau_de_prix.xlsx`, feuille `Bordereau de prix` : articles (colonne A) et leur libellé (colonne B).
- `reserves.md` : R-003 (luminaires typés : **l'unité est l'ÉTIQUETTE** ; LUMINAIRE E 3 vs 4), R-004 (étiquettes écartées), R-005 (Z6) ;
  `METHODE.md` §2 (lots fournisseur confirmés : lot éclairage A1 ×11, SL1 4′ ×12, 3′ ×15, 1′ ×6, trousses, E ×3, Z6 ×3).

## 2. Ton sous-lot (disjoint de celui des autres releveurs : ne traite RIEN d'autre)

Tout ce qui n'est pas listé ici appartient aux releveurs A2-1 et A2-3 ou aux lots A1 et A3 : **ne l'ajoute pas**, même si tu le croises.

### 2a. Familles sur plan → lignes `<FAM>-I`
Valeurs attendues (à revérifier dans `Par libellé`, `Par feuille` et `rapport-releve.md`) :

| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | ligne attendue |
|---|---|--:|---|---|---|
| LUMINAIRE A1 | LA1 | 11 | INSTALLER 11 | E203 11 | **LA1-I 11** |
| LUMINAIRE C1 | LC1 | 12 | INSTALLER 12 | E203 12 | **LC1-I 12** |
| LUMINAIRE C1_1 | LC11 | 6 | INSTALLER 6 | E203 6 | **LC11-I 6** |
| LUMINAIRE C1_3 | LC13 | 15 | INSTALLER 15 | E203 15 | **LC13-I 15** |
| LUMINAIRE E | LE | 3 | INSTALLER 3 | E203 3 | **LE-I 3** |
| ENSEIGNE SORTIE Z6 | Z6 | 3 | INSTALLER 3 | E203 2, E204 1 | **Z6-I 3** |

Descriptions suggérées (u = « U », art = 3.35 pour les 6 lignes) :
- LA1-I : « Luminaire A1 Cooper 24CGTS-NUV-MEDIUM-3500K 2'x4' encastré 347 V 50 W — neuf » (modèle lu dans Détail F-01 et dans le relevé éclairage ligne 9)
- LC1-I : « Luminaire C1 Axis AXIS-SL1-4 (module 4') 120-277 V — neuf » (Détail F-02)
- LC11-I : « Luminaire C1_1 Axis AXIS-SL1-1 (module 1') — neuf » (Détail F-03)
- LC13-I : « Luminaire C1_3 Axis AXIS-SL1-3 (module 3') — neuf » (Détail F-04)
- LE-I : « Luminaire E GreenCreative PXCYL-8-PM-LE05-90-35 cylindre suspendu — neuf » (Détail F-06)
- Z6-I : « Enseigne de sortie Z6 Stanpro RMSOWH-UDC pictogramme LED — neuve » (Détail F-07)

Le `src` de chaque ligne cite la répartition par feuille et le contrôle croisé, p. ex.
`"releve.xlsx Par libellé LUMINAIRE A1 11 ; rapport-releve.md INSTALLER 11 ; Par feuille E203 11 ; relevé éclairage A1 11"`
(pour les luminaires, ajoute le fichier du relevé éclairage : `entree/reference-Releve_Eclairage_Urgence.xlsx Relevé ligne 9`).

**Décision du directeur (LE-I = 3)** : le relevé sur plan compte **3 étiquettes E sur bloc** (R-003 ; le lot éclairage confirmé de METHODE.md compte E ×3) ;
Détail F-06 et le relevé éclairage (ligne 14) en comptent 4. **Retiens 3** et note l'écart 4 vs 3.

### 2b. Lignes de la feuille `Détail` à REPRENDRE

| Code | Description (colonne B de Détail, raccourcie si > 140 caractères) | q attendue | u | art | remarque à mettre en note |
|---|---|--:|---|---|---|
| F-05 | Rangées linéaires Axis : suspension aux tiges/câbles fixés à la dalle (devis 16.5), alimentation de rangée | 20 | U (rangée : écris « rangée » dans `desc`) | 3.35 | travail de rangée, distinct des modules LC1/LC11/LC13 (ceux-ci comptent des étiquettes) ; recoupe C-SUSP 20 rangées du relevé éclairage (ligne 13 : « ≈20 rangées (combinaisons 3', 4'+1', 3'+4') — agent à confirmer config. ») ; noter « ≈20 » de Détail (colonne Notes : « ≈20 rangées continues ») |
| F-10 | Boîtes de jonction éclairage, chaînes de retenue à la dalle (devis 16.5), quincaillerie | 1 | LOT | 3.35 | Réf. plan E-005 |

Pour chaque ligne Détail reprise, le `src` cite : `entree/reference-Estimation_2.xlsx Détail <code> (ligne Excel N ; colonne D Qté = X ; Unité = …)`
(utilise `detail('<code>')`).

### 2c. Lignes de la feuille `Détail` à EXCLURE (doubles comptes) → liste `exclusions`
Règle : **le plan gagne sur Détail pour les quantités** ; une ligne Détail qui recompte un objet déjà relevé sur plan est un double compte.
Chaque exclusion = `{"code": "...", "raison": "..."}` avec la ligne sur plan qui la remplace :

| Code Détail | Décision | Remplacée par | À noter |
|---|---|---|---|
| F-01 (11 luminaires A1) | EXCLURE | LA1-I | dit « Dont 3 sur circuit PP-U1 » |
| F-02 (12 C1) | EXCLURE | LC1-I | |
| F-03 (6 C1_1) | EXCLURE | LC11-I | |
| F-04 (15 C1_3) | EXCLURE | LC13-I | |
| F-06 (4 luminaires E) | EXCLURE | **LE-I 3** (3 étiquettes sur plan, lot éclairage E ×3 ; R-003) | 4 Détail / relevé éclairage vs 3 retenus |
| F-07 (3 enseignes Z6) | EXCLURE | Z6-I | Détail note « Symboles noirs (neufs) » |

### 2d. Notes OBLIGATOIRES à écrire dans `notes` (une entrée par point, avec les valeurs LUES)
1. **LUMINAIRE E : 3 vs 4** (voir §2a) : plan 3 étiquettes (`marques('LUMINAIRE E')`, attendu 3 sur E203, « étiquette E sur bloc S014 »), Détail F-06 = 4, relevé éclairage ligne 14 = 4, lot éclairage METHODE.md = E ×3 ; R-004 écarte une étiquette « E » à (1717, 967), listée deux fois (cartouche/notes probables). Retenu : **3**.
2. **L'unité des luminaires neufs est l'ÉTIQUETTE** (R-003) : une rangée linéaire « C1 + C1_1 » = 2 modules. Compte `marques('LUMINAIRE A1')` (attendu 7 sur bloc S035 + 4 sur bloc S343 = 11), `marques('LUMINAIRE C1')`, `marques('LUMINAIRE C1_1')`, `marques('LUMINAIRE C1_3')` et note si le total de chaque famille retrouve bien 11 / 12 / 6 / 15.
3. **Z6** : total 3 = E203 2 + E204 1 (`par_feuille('ENSEIGNE SORTIE Z6')`) ; R-005 : « tracé pointillé : confirmer neuf — E-008 en liste 3 » (voir la Note du marqueur E203 P13) ; Détail F-07 : « Symboles noirs (neufs) » ; **le relevé éclairage (ligne 4) dit « Aucun appareil neuf à l'étage (E-204) » alors qu'un Z6 est relevé sur E204** → contradiction à noter ; retenu Z6-I 3 (rapport-releve.md : INSTALLER 3 ; lot éclairage Z6 ×3).
4. **F-05 vs C-SUSP** : F-05 = 20 rangées (« ≈20 ») recoupe C-SUSP 20 du relevé éclairage ; la ligne chiffre le travail de suspension/alimentation par rangée ; les trousses de suspension fournies sont dans le lot fournisseur éclairage (« trousses 1 500 $ », METHODE.md §2), donc le matériel n'est pas repris ici.
5. **Circuit PP-U1** : Détail F-01 précise « Dont 3 sur circuit PP-U1 » ; ces 3 luminaires A1 sont compris dans LA1-I 11 (et recoupent probablement les 3 « anneaux pleins » de la famille ENCASTRE URGENCE, qui n'a aucune ligne, traitée par le releveur A2-1) — aucune quantité modifiée.
6. **Exclusions F-01…F-04, F-06, F-07** : rappelle en une entrée que les quantités de ces six lignes Détail (11, 12, 6, 15, 4, 3) sont remplacées par les lignes sur plan (LA1-I 11, LC1-I 12, LC11-I 6, LC13-I 15, LE-I 3, Z6-I 3).

## 3. Convention d'articles du bordereau (champ `art`, texte)

Articles lus dans `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`, colonne A/B ; revérifie le libellé de 3.35) :
3.22 Démontage des éléments électriques · 3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V ·
3.25 Lot disjoncteurs · 3.35 Appareil de contrôle + appareils d'éclairage · 3.36 Détecteur de fumée ·
3.37 Panneau alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie : mise en marche et certification.

Convention du directeur A : **luminaires neufs (LA1, LC1, LC11, LC13, LE) et Z6 → 3.35** ; lignes Détail → l'article du tableau 2b (F-05 et F-10 → 3.35).
Pour ton sous-lot, les 8 lignes sont donc toutes en **3.35**.

## 4. Format de sortie : `lots/releveur-A2-2.json`

```json
{
  "niveau": "releveur",
  "nom": "A2-2",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "LA1-I", "desc": "Luminaire A1 Cooper 24CGTS-NUV-MEDIUM-3500K 2'x4' encastré 347 V 50 W — neuf", "q": 11, "u": "U", "p": null, "h": null,
     "art": "3.35", "src": "releve.xlsx Par libellé LUMINAIRE A1 11 ; rapport-releve.md INSTALLER 11 ; Par feuille E203 11 ; relevé éclairage A1 11"}
  ],
  "notes": ["hésitations, contradictions plan/Détail, écarts éventuels"],
  "exclusions": [{"code": "F-01", "raison": "double compte : 11 luminaires A1 déjà relevés sur plan — remplacée par LA1-I"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` = texte (« 3.35 ») ; `src` exact et vérifiable (fichier, feuille,
libellé ou code, valeur LUE). Lignes attendues (8) : LA1-I, LC1-I, LC11-I, LC13-I, LE-I, Z6-I, F-05, F-10. Écris le JSON avec
`json.dump(obj, f, ensure_ascii=False, indent=2)` dans une commande `python3 - <<'EOF'`, en construisant les `q` à partir de tes lectures
(`portees(...)`, `detail(...)`), pas en les retapant.

## 5. Ordre de travail conseillé
1. Lis `rapport-releve.md`, `reserves.md` (R-003, R-004, R-005) et le relevé éclairage (`entree/reference-Releve_Eclairage_Urgence.xlsx`).
2. Pour chacune des 6 familles du §2a : `par_libelle`, `par_feuille`, `portees`, `marques` ; note les valeurs LUES.
3. Pour F-01…F-07 et F-10 : `detail(code)` ; note ligne Excel, Qté, Unité, Réf. plan, Notes.
4. Construis le JSON, écris-le, vérifie-le (§6), réponds (§7).

## 6. Critères de vérification (avant de t'arrêter)

(1) Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A2-2.json'))"` (code de sortie 0) et contient `lignes` + `notes` ;
(2) chaque `src` pointe vers une cellule/un libellé réellement lu ; (3) aucun code deux fois ; (4) toute ligne Détail de ton sous-lot est reprise
(F-05, F-10) ou dans `exclusions` avec la ligne sur plan qui la remplace (F-01, F-02, F-03, F-04, F-06, F-07) ; (5) `p` et `h` à `null`.
Contrôle automatique à lancer (adapte-le seulement si une lecture du kit contredit une valeur attendue, et dans ce cas écris la note « ÉCART : ») :

```python
python3 - <<'EOF'
import json
p='/home/claude/entrainement/S-1902/swarm-2/lots/releveur-A2-2.json'
d=json.load(open(p,encoding='utf-8'))
assert d['niveau']=='releveur' and d['nom']=='A2-2' and d['modele_demande']=='haiku'
assert isinstance(d['lignes'],list) and isinstance(d['notes'],list) and isinstance(d['exclusions'],list)
attendus={'LA1-I':11,'LC1-I':12,'LC11-I':6,'LC13-I':15,'LE-I':3,'Z6-I':3,'F-05':20,'F-10':1}
codes=[l['code'] for l in d['lignes']]
assert len(codes)==len(set(codes)), 'code en double'
assert set(codes)==set(attendus), set(codes)^set(attendus)
assert {e['code'] for e in d['exclusions']}=={'F-01','F-02','F-03','F-04','F-06','F-07'}
for l in d['lignes']:
    assert l['p'] is None and l['h'] is None, l['code']
    assert l['u'] in ('U','PI','LOT'), l['code']
    assert isinstance(l['q'],(int,float)) and l['q']>0, l['code']
    assert l['art']=='3.35', l['code']
    assert l['src'].strip() and l['desc'].strip(), l['code']
assert [l for l in d['lignes'] if l['code']=='LE-I'][0]['q']==3, 'LE-I doit valoir 3 (décision du directeur)'
print('ECARTS vs brief (chacun doit avoir une note ÉCART) :',{l['code']:(l['q'],attendus[l['code']]) for l in d['lignes'] if l['q']!=attendus[l['code']]})
print(len(codes),'lignes :',', '.join(f"{l['code']} = {l['q']}" for l in d['lignes']))
EOF
```

## 7. Réponse finale
Quand le JSON est écrit et que le contrôle passe, **arrête-toi** et réponds seulement : le nombre de lignes et la liste `code = q`
(la dernière ligne imprimée par le contrôle). Rien d'autre.
