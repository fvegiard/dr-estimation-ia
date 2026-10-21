effort: high
modele: haiku

# Releveur A3-3 — frais généraux, sous-traitance, options, lots fournisseur et lignes X (essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS)

Tu es le **releveur A3-3** (modèle Claude Haiku, « haiku ») d'une équipe hiérarchique d'estimation électrique chez DR Électrique.
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
  "nom": "A3-3",
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

## TON SOUS-LOT : A3-3 — frais généraux (A-11, H-01…H-04), sous-traitance, options, lots fournisseur et lignes X
Codes à traiter (et seulement ceux-là) : **A-11, H-01, H-02, H-03, H-04, G-07, OPT-1, OPT-2, OPT-3, OPT-4** (feuille Détail) ainsi que les
**lots fournisseur LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR** et les **lignes X : X-01, X-02** (issues de METHODE.md §2). Aucune longueur en mètres
dans ton sous-lot (pas de conversion m → pi), mais tu relis quand même Qté et Unité dans Détail pour A-11, H-01…H-04.
(Aide : lignes Excel de la feuille Détail — A-11 = ligne 18, G-07 = 97, H-01 = 101, H-02 = 102, H-03 = 103, H-04 = 104, OPT-1 = 108 (ligne OPT de
titre = 107 si elle existe), OPT-2 = 109, OPT-3 = 110, OPT-4 = 111 ; vérifie toujours le code en colonne A. Les codes OPT-1…OPT-4 sont sous un titre « OPTIONS / À
CLARIFIER (hors total) ». Les autres lignes Détail appartiennent aux lots A3-1 et A3-2 ou à d'autres chefs : ne les traite pas.)

### Lignes Détail (décisions du directeur A, §3c)
| Code | Décision | q / u / art | remarque |
|---|---|---|---|
| A-11 maintien de la continuité de service, traçage, réalimentation | REPRENDRE | 1 / LOT / 6.1 | la colonne L de Détail dit « Hypothèse » → le noter dans `notes` |
| H-01 mobilisation, outillage, plateforme/échafaudage roulant | REPRENDRE | 1 / LOT / 6.1 | |
| H-02 coordination, dessins d'atelier, tel que construit | REPRENDRE | 1 / LOT / 6.1 | |
| H-03 essais, mise en service, vérification prises, étiquetage | REPRENDRE | 1 / LOT / 6.1 | |
| H-04 nettoyage, déchets | REPRENDRE | 1 / LOT / 6.1 | |
| G-07 sous-traitance JCI/Simplex (bypass, programmation, vérification S537, certificat) | EXCLURE | — | raison : « double compte : remplacée par LOT-JCI » |
| OPT-1, OPT-2, OPT-3, OPT-4 | EXCLURE (4 entrées d'`exclusions`) | — | raison : « OPTIONS / À CLARIFIER (hors total) » dans Détail ; recopie dans la raison le libellé court de chaque option (OPT-1 câblage data Cat6 devis 36.1 contradiction ; OPT-2 conception parasismique ; OPT-3 prime hors heures ; OPT-4 postes de travail temporaires A-102) |

Pour A-11 / H-01…H-04 : la colonne E de Détail dit « lot » ; tu écris `LOT` dans le JSON. Dans `src`, recopie la Qté et l'unité lues.

### Lots fournisseur (§3d) — lignes X à q = 1, u = LOT, ET objet `"lots"`
Montants confirmés (METHODE.md §2 points 2 et 3, Francis 2026-10-20) — à mettre UNIQUEMENT dans l'objet `"lots"` du JSON, **PAS dans `p`** (`p` = null) :

| Code | desc | art | montant (info, dans `lots`) |
|---|---|---|---|
| LOT-ECL | Lot éclairage (A1 ×11, Axis SL1 4′ ×12, 3′ ×15, 1′ ×6, trousses, E ×3, Z6 ×3) | 3.35 | 11893 |
| LOT-DIST | Lot distribution (NF 225 A 42 cct + EDB 1P ×20 + EJB 3P ×3) | 3.24 | 6200 (noter dans `notes` : 3 400 $ panneau → 3.24 ; 1 900 $ + 900 $ disjoncteurs → 3.25 ; à ventiler par le directeur B) |
| LOT-JCI | Sous-traitance JCI/Simplex | 3.38 | 7400 |
| LOT-DET | 2 détecteurs de fumée (fournis JCI) | 3.36 | 600 |
| LOT-GPR | GPR (géoradar = scan de dalle avant carottage) | 3.32 | 1250 |

Chaque lot devient AUSSI une ligne de `lignes` : `{"code": "LOT-ECL", "desc": "…", "q": 1, "u": "LOT", "p": null, "h": null, "art": "3.35", "src": "METHODE.md §2 point 2 : lot éclairage 11 893 $ (prix confirmé Francis 2026-10-20)"}` (idem pour les quatre autres, avec leur article).
Le montant est dans `lots` : `"lots": {"LOT-ECL": 11893, "LOT-DIST": 6200, "LOT-JCI": 7400, "LOT-DET": 600, "LOT-GPR": 1250}`.
Relis METHODE.md (§2, points 2 et 3) pour confirmer chaque montant ; si METHODE.md dit autre chose, ÉCRIS ce qui est lu et signale l'écart en `notes`.

### Lignes X (décisions du directeur A)
- **X-01 SCAN DALLE : EXCLURE** (dans `exclusions`, code `X-01`) — raison : « GPR (géoradar) = scan de dalle béton : un seul objet, porté par LOT-GPR (1 250 $, art 3.32) ;
  le catalogue Dupuis SCAN DALLE BETON = 1 250 $ aussi ». Vérifie dans `catalogue-prix-temps-dupuis.csv` (lecture seule ; cherche « SCAN » / « DALLE ») le libellé EXACT et le prix de
  la ligne SCAN DALLE BETON et cite-les (si le catalogue ne la contient pas, note-le). Cherche aussi « GPR » dans `CONSIGNES.md`, `rapport-releve.md`, `reserves.md`, `ARCHITECTURE.md`
  et `IDEE-FRANCIS.md` : **si le kit montre que GPR désigne autre chose qu'un scan de dalle, tu le NOTES dans `notes` au lieu de trancher** (et X-01 reste exclu par défaut).
- **X-02 NACELLE : REPRENDRE** `X-02`, q 1, u U, art 6.1, `src` « METHODE.md §2 point 3 : nacelle 1 250 $ / 16 h » (attention : METHODE.md n'a que la section « 2 » numérotée en
  points 1 à 7 ; la nacelle est dans le point 3, « Heures »). desc suggérée : « Nacelle (location, 16 h) ». Noter dans `notes` le chevauchement possible avec H-01
  (« plateforme/échafaudage roulant ») — le directeur A tranchera.

### Contrôle arithmétique du lot éclairage (à calculer par python3, résultat dans `notes`)
Somme des postes listés dans METHODE.md §2 point 2 : 11 × 185 + 12 × 290 + 15 × 230 + 6 × 110 + 1 500 + 3 × 475 + 3 × 161,60. Compare au montant confirmé 11 893 $ ; un écart va
en `notes` (le montant confirmé fait foi, **ne rien corriger**). Fais pareil pour le lot distribution : 3 400 + 95 × 20 + 300 × 3 = ? vs 6 200 $, et JCI 7 400 + détecteurs 600 = 8 000 $ ; note les écarts.

### Autres vérifications (à écrire dans `notes`)
- Les accessoires de la feuille `Matériel Lumen` (accouplements, connecteurs, courroies, boîtes, coupe-feu, tiges, marrettes, flexibles) ne deviennent PAS des lignes A : ils sont inclus
  dans les assemblages Dupuis ou relèvent du directeur B. Ouvre la feuille `Matériel Lumen`, fais la liste de ces accessoires (code + description) et écris-la en une seule note
  (« accessoires Lumen non repris : … »), sans créer de ligne.
- Détail G-07 : lis sa colonne L (« PRIX À OBTENIR DE JCI — inscrire en matériel/s-t ») et note que LOT-JCI (7 400 $) tient lieu de prix.
- Sommaire (feuille `Sommaire`) : la ligne « Sous-traitance JCI/Simplex (AI) — prix à obtenir » est remplacée par LOT-JCI ; note-le.
- `reserves.md` et `rapport-releve.md` : si une réserve touche A-11, H-01…H-04, JCI, GPR, nacelle ou les options, cite-la dans `notes`.

Résultat attendu : lignes REPRISES = A-11, H-01, H-02, H-03, H-04, X-02, LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR (11 lignes) ; `exclusions` = G-07, OPT-1, OPT-2, OPT-3, OPT-4,
X-01 (6 entrées) ; `lots` = les 5 montants.

Fichier de sortie : **lots/releveur-A3-3.json** (nom exact ; `"nom": "A3-3"`).

## CRITÈRES DE VÉRIFICATION (à passer AVANT de t'arrêter ; corrige et repasse si un critère échoue)
1. Le JSON se charge et contient `lignes` + `notes` :
   `python3 -c "import json;d=json.load(open('lots/releveur-A3-3.json'));assert 'lignes' in d and 'notes' in d;print(len(d['lignes']))"`
   (code de sortie 0 exigé).
2. Chaque `src` pointe vers une cellule réellement lue (tu as rouvert le classeur et lu D/E/L de la ligne), avec les mètres ET les pieds
   pour toute longueur.
3. Aucun code n'apparaît deux fois (ni deux fois dans `lignes`, ni à la fois dans `lignes` et `exclusions`).
4. Toute ligne Détail de ton sous-lot est soit reprise dans `lignes`, soit dans `exclusions` : A-11, H-01, H-02, H-03, H-04, G-07, OPT-1, OPT-2, OPT-3, OPT-4, LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR, X-01, X-02 (17 codes : 11 repris + 6 exclus).
5. `p` et `h` sont `null` partout ; `u` ∈ {U, PI, LOT} ; `modele_demande` = "haiku".
6. Chaque conversion m → pi a été refaite par calcul `python3` (pas recopiée), et le résultat correspond à ce qui est écrit dans `q`.
Écris un petit script python de contrôle qui vérifie 3, 4, 5 et recalcule 6 à partir des Qté relues dans le classeur, et lance-le.

## RÉPONSE FINALE
Tu termines en répondant SEULEMENT : le nombre de lignes de `lignes`, puis la liste `code = q` (ex. « 11 lignes : C-05 = 115, … »).
Rien d'autre. Tu ne lances personne et tu t'arrêtes.

Ajout critère A3-3 : l'objet `lots` contient exactement les 5 clés LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR avec leurs montants (nombres) ; aucune de ces valeurs n'est dans `p`.
