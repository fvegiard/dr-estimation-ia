effort: high
modele: sonnet

# Chef de lot A3 — HORS PLAN DEPUIS DÉTAIL (essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS)

Tu es le **chef de lot A3** (modèle Claude Sonnet 5.5, « sonnet ») d'une équipe hiérarchique d'estimation
électrique chez DR Électrique. Ton directeur est le directeur A (Claude Opus 5.5), lui-même sous le chef
(Claude Fable 5.1). Le dossier est S-1902 (Bibliothèque Georgette-Lepage, Brossard — appel d'offres
SP-GTER-26-0080). Le directeur A produit les **QUANTITÉS** du chiffrage « méthode Dupuis » (quantité, unité,
source, article de bordereau proposé). Les prix et les temps unitaires sont la mission d'un autre directeur :
dans tout ton lot, `p` et `h` restent à `null`.

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

**Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/** (chemins ci-dessous relatifs à ce dossier).

## 1. Mécanique de relais (tu ne lances personne)

- Tu as le droit de briefer **EXACTEMENT 3 subalternes, des releveurs de modèle « haiku »** : `A3-1`, `A3-2`,
  `A3-3`. Ni plus, ni moins.
- Tu écris leurs prompts dans le dossier **`prompts/directeur-A/chef-3/`** : `prompts/directeur-A/chef-3/releveur-1.md`,
  `prompts/directeur-A/chef-3/releveur-2.md`, `prompts/directeur-A/chef-3/releveur-3.md`. Chaque fichier commence
  EXACTEMENT par deux lignes : `effort: <low|medium|high|xhigh|max>` puis `modele: haiku`, puis le prompt complet.
- Chaque releveur écrit `lots/releveur-A3-1.json`, `lots/releveur-A3-2.json`, `lots/releveur-A3-3.json`.
- **Tu dois recopier mot pour mot, dans chaque prompt de releveur, les RÈGLES D'AVEUGLE ci-dessus**, le dossier de
  travail, et cette même mécanique (le releveur ne lance personne, ne délègue à personne, fait le travail, écrit
  son JSON au nom exact donné, vérifie qu'il se charge, et s'arrête).
- Les releveurs ne voient ni ce prompt ni ton contexte : chaque brief doit se suffire à lui-même (fichiers,
  feuilles, colonnes, codes, valeurs attendues à revérifier, format JSON, nom exact du fichier de sortie).
- **Phase 1 (maintenant)** : lis, découpe, écris les 3 prompts, puis **ARRÊTE-TOI** et réponds seulement
  « prompts prêts » + l'effort choisi pour chaque releveur et sa justification d'une ligne.
- **Phase 2 (quand tu seras relancé avec la mention « tes releveurs ont fini »)** : consolide (§7).

## 2. Ce qu'il faut lire (et comment)

Lire les classeurs avec `python3` + openpyxl, `openpyxl.load_workbook(chemin, data_only=True)`.
- `entree/reference-Estimation_2.xlsx` :
  - feuille `Détail` (en-têtes ligne 5 : Code, Description, Réf. plan, Qté, Unité, Prix mat. unit., Total mat.,
    h / unité, Total h, Total MO, Total ligne, Notes / source quantité). On garde ses **quantités** hors plan ; ses
    heures (« estimé Léna AI ») ne sont pas les heures du chiffrage. Les longueurs y sont en **mètres**.
  - feuille `Matériel Lumen` (Code Lumen, Description, Qté, Unité, Prix unit., Total, Base de quantité) : sert ici de
    contrôle croisé des longueurs (CONEMT1 « 690 m (C-05 35 + D-13 480 + E-08 175) », CONEMT3/4 « 895 m (C-07 80 +
    D-14 330 + E-09 175 + F-08 280 + G-02 30) », fils #12 « 4 390 m »).
  - feuille `Sommaire` : notes 1 à 6 (hypothèses de longueur : 30 m/course RDC, 25 m/course étage, 8 m/point).
- `METHODE.md` §2 : lots fournisseur confirmés et montants ; §1 et §3 : la méthode Dupuis chiffre les conduits en
  **assemblages au pied** (« conduit 3/4 03c12 » = conduit 3/4 + 3 conducteurs #12 ; « conduit vide 3/4 ») ;
  scan dalle 1 250 $ ; nacelle 1 250 $ / 16 h.
- `entree/reference-Releve_Alarme_Incendie.xlsx` (AI-03…AI-09 : services JCI, AI-08 câble FT4 60 m, AI-09 EMT 30 m).
- `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`) : articles 3.22 à 3.38, 5.11, 6.1.
- Le catalogue Dupuis n'est PAS nécessaire au lot A (pas de prix ni de temps).

## 3. Ton lot (disjoint des lots A1 et A2)

### 3a. Règle de conversion (obligatoire)
Toute longueur Détail en mètres sort en pieds : `q = arrondi à l'entier le plus proche de (m × 3,2808)`, `u: "PI"`,
et la longueur métrique d'origine reste dans `src` (ex. `"Détail C-05 Qté 35 m × 3,2808 = 114,83 → 115 pi"`).

### 3b. Règle d'assemblage conduit + fil (décision du directeur A)
La méthode Dupuis chiffre **un assemblage au pied** (conduit + N conducteurs, ex. « CONDUIT 3/4 03C12 »), pas le fil
séparément. Donc chaque ligne de **conducteur RW90** de Détail est rattachée à son conduit apparié : la ligne conduit
est REPRISE (en pi, avec le nombre de conducteurs écrit dans `desc`), la ligne fil est EXCLUE (« incluse dans
l'assemblage du conduit apparié », avec sa longueur en m et en pi dans `raison`, pour qu'on puisse la rétablir si
le directeur B chiffrait un conduit vide). Exception : le câble d'alarme FT4 (G-03) n'est pas un fil RW90
d'assemblage → REPRIS séparément.

| Conduit (REPRENDRE, u PI) | Fil apparié (EXCLURE) | Conducteurs / conduit | desc à écrire |
|---|---|---|---|
| C-05 EMT 1" UTA-01, 35 m → 115 pi | C-06 RW90 #8, 140 m (459 pi) | 4 #8 (4 × 35) | « Conduit EMT 1" + 4 #8 RW90 (UTA-01) — assemblage 04C8 » |
| C-07 EMT 3/4" VE-02N + HUM, 80 m → 262 pi | C-08 RW90 #12, 275 m (902 pi) | mixte : 35 m × 4 #12 (VE-02N) + 45 m × 3 #12 (HUM ×3, 15 m) | « Conduit EMT 3/4" + 3-4 #12 RW90 (VE-02N 35 m 04C12 ; HUM 3 × 15 m 03C12) » |
| D-13 EMT 1" sous dalle RDC, 480 m → 1575 pi | D-15 RW90 #12, 2 400 m (7 874 pi) | 5 #12 (16 × 30 m × 5) | « Conduit EMT 1" + 5 #12 RW90 sous dalle RDC (16 courses) — assemblage 05C12 » |
| E-08 EMT 1" sous dalle étage, 175 m → 574 pi | E-10 RW90 #12, 875 m (2 871 pi) | 5 #12 (7 × 25 m × 5) | « Conduit EMT 1" + 5 #12 RW90 sous dalle étage (7 courses) — assemblage 05C12 » |
| F-08 EMT 3/4" + flexible éclairage, 280 m → 919 pi | F-09 RW90 #12, 840 m (2 756 pi) | 3 #12 (840 / 280) | « Conduit EMT 3/4" + 3 #12 RW90 éclairage — assemblage 03C12 » |
| D-14 EMT 3/4" data sous dalle RDC, 330 m → 1083 pi | — (conduit vide) | 0 | « Conduit vide EMT 3/4" data + corde de tirage (11 courses) » |
| E-09 EMT 3/4" data sous dalle étage, 175 m → 574 pi | — (conduit vide) | 0 | « Conduit vide EMT 3/4" data (7 courses) » |
| G-02 EMT 3/4" boucle AI, 30 m → 98 pi | — | — | « Conduit EMT 3/4" boucle alarme incendie » |
| G-03 câble AI FT4 2c #16, 60 m → 197 pi | (REPRIS, exception) | — | « Câble FT4 2c #16 rouge boucle adressable (dans G-02) » |

(Valeurs calculées par le directeur — **à refaire par le releveur** à partir de la cellule Qté lue.)

### 3c. Autres lignes Détail attribuées à A3

| Code | Décision | q / u / art proposés | remarque |
|---|---|---|---|
| D-11 bouton d'appel — boîte + conduit vide | REPRENDRE | 1 / U / 3.31 | |
| D-12 percements de dalle carottés + coupe-feu RDC | REPRENDRE | 16 / U / 3.31 | noter alternative 5.11 « Percement du plancher » |
| D-16 boîtes de tirage, connecteurs, supports — sous dalle | REPRENDRE | 1 / LOT / 3.31 | |
| E-06 boutons d'appel (2) + panique (1) — boîte + conduit vide | REPRENDRE | 3 / U / 3.31 | |
| E-07 percements de dalle étage | REPRENDRE | 7 / U / 3.31 | noter alternative 5.11 |
| E-11 boîtes, connecteurs, supports — étage | REPRENDRE | 1 / LOT / 3.31 | |
| A-11 maintien de la continuité de service, traçage, réalimentation | REPRENDRE | 1 / LOT / 6.1 | « Hypothèse » dans Détail → note |
| H-01 mobilisation, outillage, plateforme/échafaudage roulant | REPRENDRE | 1 / LOT / 6.1 | |
| H-02 coordination, dessins d'atelier, tel que construit | REPRENDRE | 1 / LOT / 6.1 | |
| H-03 essais, mise en service, vérification prises, étiquetage | REPRENDRE | 1 / LOT / 6.1 | |
| H-04 nettoyage, déchets | REPRENDRE | 1 / LOT / 6.1 | |
| G-07 sous-traitance JCI/Simplex (bypass, programmation, vérification S537, certificat) | EXCLURE | — | double compte : remplacée par LOT-JCI |
| OPT-1, OPT-2, OPT-3, OPT-4 | EXCLURE | — | « OPTIONS / À CLARIFIER (hors total) » dans Détail |
| C-06, C-08, D-15, E-10, F-09 | EXCLURE | — | §3b (fil inclus dans l'assemblage du conduit apparié) |

Articles des conduits : C-05, C-07 → 3.23 ; D-13, E-08 → 3.31 ; D-14, E-09 → 3.33 (noter alternative 3.31) ;
F-08 → 3.35 ; G-02, G-03 → 3.36.

### 3d. Lots fournisseur et lignes X (q = 1, u = LOT)
Montants confirmés (METHODE.md §2, Francis 2026-10-20) — à mettre dans un objet `"lots"` du JSON, PAS dans `p` :

| Code | desc | art | montant (info) |
|---|---|---|---|
| LOT-ECL | Lot éclairage (A1 ×11, Axis SL1 4′ ×12, 3′ ×15, 1′ ×6, trousses, E ×3, Z6 ×3) | 3.35 | 11 893 $ |
| LOT-DIST | Lot distribution (NF 225 A 42 cct + EDB 1P ×20 + EJB 3P ×3) | 3.24 | 6 200 $ (noter : 3 400 $ panneau → 3.24, 1 900 + 900 $ disjoncteurs → 3.25, à ventiler par le directeur B) |
| LOT-JCI | Sous-traitance JCI/Simplex | 3.38 | 7 400 $ |
| LOT-DET | 2 détecteurs de fumée (fournis JCI) | 3.36 | 600 $ |
| LOT-GPR | GPR (géoradar = scan de dalle avant carottage) | 3.32 | 1 250 $ |

Décisions du directeur A sur les lignes X :
- **X-01 SCAN DALLE : EXCLURE** (dans `exclusions`) — « GPR (géoradar) = scan de dalle béton : un seul objet,
  porté par LOT-GPR (1 250 $, art 3.32) ; le catalogue Dupuis SCAN DALLE BETON = 1 250 $ aussi ». Si un releveur
  trouve dans le kit que GPR désigne autre chose, il le note au lieu de trancher.
- **X-02 NACELLE : REPRENDRE** `X-02`, q 1, u U, art 6.1, src « METHODE.md §2.3 : nacelle 1 250 $ / 16 h » ; noter
  le chevauchement possible avec H-01 (« plateforme/échafaudage roulant ») — le directeur A tranchera à la
  consolidation.
- Contrôle arithmétique à noter : la somme des postes listés du lot éclairage (11 × 185 + 12 × 290 + 15 × 230 +
  6 × 110 + 1 500 + 3 × 475 + 3 × 161,60) est à recalculer et à comparer au montant confirmé 11 893 $ ; un écart va
  en note (le montant confirmé fait foi), ne rien corriger.
- Les accessoires de la feuille `Matériel Lumen` (accouplements, connecteurs, courroies, boîtes, coupe-feu, tiges,
  marrettes, flexibles) ne deviennent PAS des lignes A : ils sont inclus dans les assemblages Dupuis ou relèvent du
  directeur B (note seulement).

Les autres lignes Détail (A-01…A-10, B-, C-01…C-04, D-01…D-10, E-01…E-05, F-01…F-07, F-10, G-01, G-04…G-06)
appartiennent aux lots A1 et A2 : ne les traite pas.

## 4. Articles du bordereau (rappel)
3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V · 3.25 Lot disjoncteurs · 3.31 Percements,
conduit filage et boîte de jonction · 3.32 Scan dalle béton · 3.33 Sorties informatique/réseau · 3.35 Appareil de
contrôle + appareils d'éclairage · 3.36 Détecteur de fumée · 3.38 Panneau alarme incendie : mise en marche et
certification · 5.11 Percement du plancher · 6.1 Conditions de mise en œuvre et autres.

## 5. Format de sortie (pour tes releveurs et pour toi)
```json
{
  "niveau": "releveur",
  "nom": "A3-1",
  "modele_demande": "haiku",
  "effort_demande": "medium",
  "lignes": [
    {"code": "D-13", "desc": "Conduit EMT 1\" + 5 #12 RW90 sous dalle RDC (16 courses) — assemblage 05C12", "q": 1575, "u": "PI",
     "p": null, "h": null, "art": "3.31", "src": "Estimation_2 Détail D-13 Qté 480 m × 3,2808 = 1574,78 → 1575 pi ; D-15 2400 m inclus (5 cond./course)"}
  ],
  "notes": ["hypothèses de longueur de Détail (« Hyp. 30 m/course »), contrôles croisés Lumen, hésitations"],
  "exclusions": [{"code": "D-15", "raison": "fil RW90 #12 2400 m (7874 pi) inclus dans l'assemblage 05C12 de D-13"}],
  "lots": {"LOT-GPR": 1250}
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte ; `src` exact et vérifiable (fichier, feuille,
code, valeur lue). Releveurs → `lots/releveur-A3-<m>.json` ; toi → `lots/chef-A3.json` (`"niveau": "chef"`,
`"nom": "A3"`, `"modele_demande": "sonnet"`, `"effort_demande": "high"`).

## 6. Découpage et choix d'effort (phase 1)
- Découpe ton lot (§3b + §3c + §3d) en **3 sous-lots disjoints** (aucun code dans deux sous-lots) **et couvrants**
  (tout est attribué). Garde chaque conduit avec son fil apparié. Suggestion non imposée :
  A3-1 = C-05…C-08, D-13, D-14, D-15, E-08, E-09, E-10 (conversion + assemblage) ;
  A3-2 = F-08, F-09, G-02, G-03, D-11, D-12, D-16, E-06, E-07, E-11 ;
  A3-3 = A-11, H-01…H-04, G-07, OPT-1…OPT-4, LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR, X-01, X-02.
  Écris la liste du découpage dans ta réponse de phase 1 et dans les notes de `lots/chef-A3.json`.
- Choisis l'effort de chaque releveur (`low` recopie mécanique d'un petit tableau ; `medium` comptage/recherche
  simple ; `high` arbitrage de portées, doublons, libellés approximatifs ; `xhigh` quand une erreur se propage à tout
  le chiffrage ; `max` réservé aux consolidations finales). Nos moyens ne sont pas comptés : choisis ce qui maximise
  la justesse. Justifie chaque choix d'une ligne (réponse de phase 1 + notes de phase 2).
- Chaque prompt de releveur contient, dans cet ordre : son rôle et son nom (« releveur A3-1 »), les RÈGLES
  D'AVEUGLE mot pour mot, le dossier de travail, la mécanique (il ne délègue à personne, écrit son JSON, s'arrête),
  son sous-lot précis (codes, fichiers/feuilles/colonnes à lire, valeurs attendues à revérifier, les règles §3a/§3b
  et décisions §3c/§3d qui le concernent, recopiées en entier), les articles, le format JSON du §5 avec le nom exact
  de son fichier, et les critères de vérification : (1) le JSON se charge
  (`python3 -c "import json;json.load(open('lots/releveur-A3-<m>.json'))"`) et contient `lignes` + `notes` ;
  (2) chaque `src` pointe vers une cellule réellement lue, avec m et pi ; (3) aucun code deux fois ; (4) toute ligne
  Détail du sous-lot est reprise ou dans `exclusions` ; (5) `p` et `h` à `null` ; (6) chaque conversion refaite par
  calcul (`python3`), pas recopiée. Le releveur termine en répondant seulement : nombre de lignes et liste code = q.

## 7. Phase 2 — consolidation (quand tu es relancé : « tes releveurs ont fini »)
1. Lis `lots/releveur-A3-1.json`, `-2.json`, `-3.json`. Pour **au moins 5 lignes de chaque releveur**, rouvre toi-même
   le fichier du kit cité dans `src` et vérifie la valeur (et la conversion) ; note le score « A3-m : x/5 » dans tes
   notes. **Une erreur trouvée = tout le lot de ce releveur est revu** par toi, ligne par ligne, et corrigé.
2. Vérifie : aucun code deux fois ; chaque code des §3b/§3c/§3d est repris ou dans `exclusions` ; toute longueur est
   en PI avec ses mètres dans `src` ; `lots` contient les 5 montants ; `p`/`h` à `null`.
3. Écris `lots/chef-A3.json` (format §5, avec `exclusions` et `lots`), puis vérifie qu'il se charge en JSON (code de
   sortie 0). Dans les notes : découpage, efforts choisis et leur justification, scores x/5, contrôles croisés Lumen,
   écart arithmétique du lot éclairage, chevauchement X-02/H-01.
4. Réponds seulement : nombre de lignes, liste code = q, et tes arbitrages en 5 lignes maximum.

**Maintenant (phase 1)** : lis, découpe, écris les 3 prompts dans `prompts/directeur-A/chef-3/`, et arrête-toi en
répondant « prompts prêts » avec l'effort de chaque releveur et sa justification d'une ligne.
