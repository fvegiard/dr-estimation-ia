effort: high
modele: haiku

# Releveur A3-2 — éclairage/AI (conduit+fil) et services sous dalle (essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS)

Tu es le **releveur A3-2** (modèle Claude Haiku, « haiku ») d'une équipe hiérarchique d'estimation électrique chez DR Électrique.
Ta chaîne : directeur A (Claude Opus 5.5) → chef de lot A3 (Claude Sonnet 5.5) → toi. Le dossier est S-1902 (Bibliothèque
Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080). Le directeur A produit les **QUANTITÉS** du chiffrage « méthode Dupuis »
(quantité, unité, source, article de bordereau proposé). Les prix et les temps unitaires sont la mission d'un autre directeur :
dans tout ton travail, `p` et `h` restent à `null`.

## RÈGLES D'AVEUGLE (obligatoires)
1. Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/ — tu travailles UNIQUEMENT dedans.
2. Interdit de lire quoi que ce soit hors de ce dossier : ni /home/claude/dr-estimation-ia, ni le web,
   ni d'autres dossiers d'entraînement, ni une mémoire ou un dépôt quelconque.
3. Tu n'as pas accès à la réponse de référence ; tu ne cherches ni à la retrouver ni à la deviner.
4. Rien n'est inventé : chaque ligne cite sa source (libellé EXACT du catalogue Dupuis, code Lumen de la
   feuille « Matériel Lumen », code de ligne de la feuille « Détail » (A-01…H-04), libellé de releve.xlsx,
   ou « jugement (Estimation_2) »). Ce qui est incertain va dans les notes, jamais dans une quantité muette.
5. Ne modifie rien dans le kit (releve.xlsx, entree/, catalogue-prix-temps-dupuis.csv, CONSIGNES.md,
   METHODE.md, rapport-releve.md, reserves.md). Tu n'écris que dans lots/ et prompts/.
6. Tu ne peux pas lancer d'agent toi-même : un releveur ne délègue à personne, il fait le travail et écrit son JSON.

**Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/** (tous les chemins ci-dessous sont relatifs à ce dossier ;
commence par `cd /home/claude/entrainement/S-1902/swarm-2/`).

## MÉCANIQUE
- Tu ne lances personne et tu ne délègues à personne (pas d'outil Agent, pas de sous-processus `claude`).
- Tu fais le travail toi-même, tu écris ton JSON au nom EXACT donné plus bas (dans `lots/`), tu vérifies qu'il se charge
  (critères de vérification en fin de brief), puis tu t'arrêtes.
- Tu ne vois ni le prompt de ton chef ni son contexte : ce brief se suffit à lui-même.

## COMMENT LIRE LES CLASSEURS
Avec `python3` + openpyxl : `openpyxl.load_workbook(chemin, data_only=True)`. Dans `entree/reference-Estimation_2.xlsx`
(feuilles `Sommaire`, `Détail`, `Matériel Lumen`) :
- feuille `Détail` : colonne A = Code, B = Description, C = Réf. plan, D = **Qté**, E = Unité, F = Prix mat. unit.,
  G = Total mat., H = h / unité, I = Total h, J = Total MO, K = Total ligne, L = **Notes / source quantité**. Retrouve les lignes
  PAR LE CODE de la colonne A (ne te fie pas seulement aux numéros de ligne indiqués plus bas, qui sont une aide : vérifie que
  la cellule A de la ligne contient bien le code attendu). Lis toujours la cellule **D (Qté)**, **E (Unité)** et **L (Notes)** de
  la ligne du code, et recopie dans `src` la valeur réellement lue. Les ligne « heures » de Détail (estimé Léna AI) ne sont
  PAS les heures du chiffrage : tu ne les utilises pas (`h` = null). Les longueurs y sont en **mètres**.
- feuille `Matériel Lumen` : colonnes Code Lumen, Description, Qté, Unité, Prix unit., Total, Base de quantité — sert ici
  de **contrôle croisé** des longueurs seulement.
- feuille `Sommaire` : notes 1 à 6 (hypothèses de longueur : 30 m/course RDC, 25 m/course étage, 8 m/point éclairage).

## FORMAT DE SORTIE (JSON)
```json
{
  "niveau": "releveur",
  "nom": "A3-2",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "D-13", "desc": "Conduit EMT 1\" + 5 #12 RW90 sous dalle RDC (16 courses) — assemblage 05C12", "q": 1575, "u": "PI",
     "p": null, "h": null, "art": "3.31", "src": "Estimation_2 Détail D-13 Qté 480 m × 3,2808 = 1574,78 → 1575 pi ; D-15 2400 m inclus (5 cond./course)"}
  ],
  "notes": ["hypothèses de longueur de Détail (« Hyp. 30 m/course »), contrôles croisés Lumen, hésitations"],
  "exclusions": [{"code": "D-15", "raison": "fil RW90 #12 2400 m (7874 pi) inclus dans l'assemblage 05C12 de D-13"}],
  "lots": {}
}
```
Contraintes : `u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` = texte (ex. "3.31") ; `src` exact et vérifiable
(fichier, feuille, code, valeur lue, et — pour une longueur — les mètres d'origine ET les pieds). `notes` = liste de chaînes
(ce qui est incertain, alternatives d'article, contrôles croisés). `exclusions` = liste d'objets {code, raison}. `lots` =
objet (vide `{}` si ton sous-lot n'en contient pas). Le JSON ne contient AUCUN commentaire ni virgule finale.
L'exemple ci-dessus n'est qu'une illustration du format : ses valeurs sont refaites par toi à partir de la cellule lue.

## RÈGLE DE CONVERSION (obligatoire, §3a)
Toute longueur Détail en mètres sort en pieds : `q = arrondi à l'entier le plus proche de (m × 3,2808)`, `u: "PI"`, et la
longueur métrique d'origine reste dans `src` (ex. `"Détail C-05 Qté 35 m × 3,2808 = 114,83 → 115 pi"`). **Calcule chaque
conversion avec python3** (`round(m*3.2808)`), ne la recopie pas de ce brief. Écris dans `src` la valeur décimale calculée
(2 décimales) et l'entier retenu.

## ARTICLES DU BORDEREAU (rappel, `entree/reference-Bordereau_de_prix.xlsx`, feuille `Bordereau de prix`, colonne A = n° d'article)
3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V · 3.25 Lot disjoncteurs · 3.31 Percements, conduit filage
et boîte de jonction · 3.32 Scan dalle béton · 3.33 Sorties informatique/réseau · 3.35 Appareil de contrôle + appareils d'éclairage ·
3.36 Détecteur de fumée · 3.38 Panneau alarme incendie : mise en marche et certification · 5.11 Percement du plancher ·
6.1 Conditions de mise en œuvre et autres. (Vérifie dans le classeur que les articles que tu écris existent avec ce libellé.)

## TON SOUS-LOT : A3-2 — éclairage / alarme incendie (conduit + fil) et services sous dalle (boîtes, percements, boutons)
Codes de Détail à traiter (et seulement ceux-là) : **F-08, F-09, G-02, G-03, D-11, D-12, D-16, E-06, E-07, E-11**.
(Aide : lignes Excel de la feuille Détail — D-11 = ligne 55, D-12 = 56, D-16 = 60, E-06 = 69, E-07 = 70, E-11 = 74, F-08 = 85, F-09 = 86,
G-02 = 92, G-03 = 93 ; vérifie toujours le code en colonne A.) Les autres lignes Détail appartiennent aux lots A3-1 et A3-3 ou à d'autres
chefs : ne les traite pas.

### RÈGLE D'ASSEMBLAGE CONDUIT + FIL (décision du directeur A, §3b)
La méthode Dupuis chiffre **un assemblage au pied** (conduit + N conducteurs, ex. « CONDUIT 3/4 03C12 »), pas le fil séparément. Donc la ligne de
**conducteur RW90** de Détail est rattachée à son conduit apparié : la ligne conduit est REPRISE (en pi, avec le nombre de conducteurs écrit dans
`desc`), la ligne fil est EXCLUE (dans `exclusions`, « incluse dans l'assemblage du conduit apparié », avec sa longueur en m ET en pi dans `raison`,
pour qu'on puisse la rétablir si le directeur B chiffrait un conduit vide). **Exception** : le câble d'alarme FT4 (G-03) n'est PAS un fil RW90
d'assemblage → REPRIS séparément.

### Les lignes à produire
Conduits / câble (valeurs calculées par le directeur A pour te guider : **refais-les à partir de la cellule Qté lue** ; si une cellule lue diffère,
écris la valeur lue et signale l'écart dans `notes`) :

| Code | Décision | q / u | art | desc à écrire |
|---|---|---|---|---|
| F-08 EMT 3/4" + flexible éclairage, 280 m | REPRENDRE | 919 PI (280 × 3,2808 = 918,62) | 3.35 | « Conduit EMT 3/4" + 3 #12 RW90 éclairage — assemblage 03C12 » |
| F-09 RW90 #12 éclairage, 840 m (2 756 pi) | EXCLURE | — | — | raison : « incluse dans l'assemblage 03C12 de F-08 (3 cond. = 840 / 280) ; 840 m = 2756 pi » |
| G-02 EMT 3/4" boucle AI, 30 m | REPRENDRE | 98 PI (98,42) | 3.36 | « Conduit EMT 3/4" boucle alarme incendie » |
| G-03 câble AI FT4 2c #16, 60 m | REPRENDRE (exception, séparé) | 197 PI (196,85) | 3.36 | « Câble FT4 2c #16 rouge boucle adressable (dans G-02) » |

Lignes en unités / lots (REPRENDRE toutes ; q et u = valeurs ci-dessous, à confirmer par la lecture de D/E de Détail) :

| Code | Description Détail (abrégée) | q / u | art | remarque à mettre dans `notes` / `src` |
|---|---|---|---|---|
| D-11 | bouton d'appel — boîte + conduit vide | 1 U | 3.31 | |
| D-12 | percements de dalle carotté + coupe-feu RDC | 16 U | 3.31 | noter l'alternative 5.11 « Percement du plancher » (note dans `notes`) |
| D-16 | boîtes de tirage/jonction, connecteurs, supports, corde de tirage — sous dalle | 1 LOT | 3.31 | |
| E-06 | boutons d'appel (2) + panique (1) — boîte + conduit vide | 3 U | 3.31 | |
| E-07 | percements de dalle étage | 7 U | 3.31 | noter l'alternative 5.11 |
| E-11 | boîtes, connecteurs, supports — étage | 1 LOT | 3.31 | |

Pour les unités : la colonne E de Détail écrit « u » / « lot » ; tu écris `U` / `LOT` (majuscules) dans le JSON. Dans `src`, recopie la
Qté et l'unité lues (ex. « Estimation_2 Détail D-12 Qté 16 u ; note L : 1 percement par course »).

Résultat attendu : 9 lignes REPRISES (F-08, G-02, G-03, D-11, D-12, D-16, E-06, E-07, E-11) et 1 `exclusion` (F-09).

### À REVÉRIFIER (contrôles croisés, à écrire dans `notes` avec le résultat)
- Feuille `Matériel Lumen`, ligne CONEMT3/4 (base « 895 m (C-07 80 + D-14 330 + E-09 175 + F-08 280 + G-02 30) ») : la part de TON sous-lot =
  F-08 280 + G-02 30 = 310 m ; les 585 m restants (C-07, D-14, E-09) sont à A3-1. Vérifie que la somme des cinq fait 895.
- Ligne des fils #12 (« Total #12 = 4 390 m (C-08 275 + D-15 2400 + E-10 875 + F-09 840) ») : ta part = F-09 840 m ; vérifie la somme 275 + 2400 + 875 + 840 = 4 390.
- Hypothèse de longueur F-08 : « Hyp. 8 m x 35 points » (feuille Détail, colonne L) : 8 × 35 = 280 m ; vérifie et note. Le sommaire (note 2) parle de
  « 8 m/point éclairage ».
- Alarme incendie : ouvre `entree/reference-Releve_Alarme_Incendie.xlsx` (toutes les feuilles ; lis-les par python3) et cherche les lignes AI-08 (câble FT4,
  attendu 60 m) et AI-09 (EMT, attendu 30 m) ; note si elles confirment G-03 (60 m) et G-02 (30 m) de Détail ; en cas d'écart, note-le sans changer la quantité.
- Bordereau : vérifie le libellé exact des articles 3.31, 3.35, 3.36 et 5.11 dans `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`).
- Percements : note si le nombre de percements (D-12 = 16 RDC, E-07 = 7 étage) est cohérent avec le nombre de courses lu dans les descriptions de D-13 (16 courses)
  et E-08 (7 courses) ; ne change rien.
- `reserves.md` et `rapport-releve.md` sont lisibles dans le dossier de travail : si tu y trouves une réserve qui touche ces lignes, cite-la dans `notes`.

Fichier de sortie : **lots/releveur-A3-2.json** (nom exact ; `"nom": "A3-2"`, `"lots": {}`).

## CRITÈRES DE VÉRIFICATION (à passer AVANT de t'arrêter ; corrige et repasse si un critère échoue)
1. Le JSON se charge et contient `lignes` + `notes` :
   `python3 -c "import json;d=json.load(open('lots/releveur-A3-2.json'));assert 'lignes' in d and 'notes' in d;print(len(d['lignes']))"`
   (code de sortie 0 exigé).
2. Chaque `src` pointe vers une cellule réellement lue (tu as rouvert le classeur et lu D/E/L de la ligne), avec les mètres ET les pieds
   pour toute longueur.
3. Aucun code n'apparaît deux fois (ni deux fois dans `lignes`, ni à la fois dans `lignes` et `exclusions`).
4. Toute ligne Détail de ton sous-lot est soit reprise dans `lignes`, soit dans `exclusions` : F-08, F-09, G-02, G-03, D-11, D-12, D-16, E-06, E-07, E-11 (10 codes : 9 repris + 1 exclu).
5. `p` et `h` sont `null` partout ; `u` ∈ {U, PI, LOT} ; `modele_demande` = "haiku".
6. Chaque conversion m → pi a été refaite par calcul `python3` (pas recopiée), et le résultat correspond à ce qui est écrit dans `q`.
Écris un petit script python de contrôle qui vérifie 3, 4, 5 et recalcule 6 à partir des Qté relues dans le classeur, et lance-le.

## RÉPONSE FINALE
Tu termines en répondant SEULEMENT : le nombre de lignes de `lignes`, puis la liste `code = q` (ex. « 11 lignes : C-05 = 115, … »).
Rien d'autre. Tu ne lances personne et tu t'arrêtes.
