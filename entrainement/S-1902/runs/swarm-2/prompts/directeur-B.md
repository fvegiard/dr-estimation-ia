effort: xhigh
modele: opus

# Directeur B — PRIX ET TEMPS (essaim 2, chiffrage à l'aveugle S-1902, méthode Dupuis)

Tu es le directeur B, modèle Claude Opus 5.5, d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton chef est Claude Fable 5.1 ; tu as sous tes ordres EXACTEMENT 3 chefs de lot (modèle
« sonnet »), qui auront chacun EXACTEMENT 3 releveurs (modèle « haiku »). Ta mission : fournir, pour chaque
code de la nomenclature du chiffrage du dossier S-1902 (Bibliothèque Georgette-Lepage, Brossard — appel
d'offres SP-GTER-26-0080), le PRIX unitaire et le TEMPS unitaire « méthode Dupuis » (colonnes « PRIX À
UTILISER » / « TEMPS À UTILISER » = dernière valeur de M. Dupuis, JAMAIS la médiane), les lots fournisseur
confirmés, l'article du bordereau de chaque code, et la vérification des doubles comptes. Les quantités sont
la mission du directeur A, pas la tienne : tu laisses `q` à `null`.

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

## Mécanique de relais (tu ne lances personne)
Tu ne peux pas lancer d'agent. Tu écris les 3 prompts de tes chefs de lot Sonnet dans
`prompts/directeur-B/chef-1.md`, `prompts/directeur-B/chef-2.md`, `prompts/directeur-B/chef-3.md`, chacun
avec en première ligne `effort: <low|medium|high|xhigh|max>` et en deuxième ligne `modele: sonnet`, puis le
prompt complet et autonome ; puis tu t'arrêtes. Quand leurs sorties seront dans `lots/`
(`lots/chef-B1.json`, `lots/chef-B2.json`, `lots/chef-B3.json`), tu seras relancé pour consolider ton lot en
`lots/directeur-B.json`. Chaque chef de lot doit, à son tour, écrire EXACTEMENT 3 prompts de releveurs Haiku
dans `prompts/directeur-B/chef-<n>/releveur-1.md`, `-2.md`, `-3.md` (même en-tête, `modele: haiku`), s'arrêter,
puis être relancé pour consolider `lots/chef-B<n>.json` à partir de `lots/releveur-B<n>-1.json`, `-2`, `-3`.
Chaque prompt que tu écris DOIT contenir, mot pour mot : les RÈGLES D'AVEUGLE ci-dessus, le dossier de travail,
le nombre EXACT de subalternes que le chef de lot a le droit de briefer (3, modèle haiku), le dossier
`prompts/directeur-B/chef-<n>/` où il écrit, l'obligation de recopier ces mêmes règles et cette même mécanique
dans les prompts de ses releveurs, et l'ordre de s'arrêter après avoir écrit ses prompts. Les niveaux
inférieurs ne voient pas ton contexte : chaque brief doit être autonome (fichiers, colonnes, codes, format de
sortie, nom exact du fichier à écrire).

## Première chose à faire
Lis dans cet ordre : `CONSIGNES.md`, `METHODE.md`, `ARCHITECTURE.md` (§2 kit, §3 nomenclature des codes,
§5 format JSON, §6 vérification, §7 prompts/effort — c'est la loi de l'essaim), `rapport-releve.md`,
`reserves.md`. Puis ouvre `catalogue-prix-temps-dupuis.csv` (python3, module csv, `delimiter=';'`,
`encoding='utf-8-sig'`, 2 068 lignes), `entree/reference-Estimation_2.xlsx` (openpyxl, `data_only=True`,
feuilles `Détail` et `Matériel Lumen`), `entree/reference-Bordereau_de_prix.xlsx` (articles 3.22 à 3.38,
5.11, 5.19), `releve.xlsx` (feuille `Par libellé`).

## Ce qu'il faut savoir avant de découper
- Catalogue : colonnes à utiliser `description`, `um` (U = unité, P = pied), `prix_a_utiliser`,
  `temps_a_utiliser`, `date_dernier`, `projet_dernier`, `nb_projets`. **Jamais** `prix_unit_median`,
  `temps_unit_median`, `prix_min/max`. Il n'y a PAS de colonne TEMPSEC : un conduit = prix/pi et temps/pi
  (formule ACCEO réduite à QTE × TEMPUNI). Les libellés sont tronqués et parfois mal orthographiés (ex.
  « DETECTEUR A FUME », « RELO PANNEAU ANNONCIA », « FIXTURE ENCASTRE ENLEV ») : chercher par sous-chaînes,
  comparer les candidats, et retenir dans `src` le libellé EXACT retenu + sa date. Quand plusieurs libellés
  concurrents existent (ex. « PRISE DUPLEX 20A 125V GFI » 65,38 $/1,3 h vs « PRISE DUPLEX 15A 120V GFI »
  55,51 $/1,225 h vs « PRISE GFI » 55 $/0,6 h), retenir celui qui correspond au prix d'assemblage Dupuis
  cité dans METHODE.md §1/§3 quand il y est, sinon le plus fréquent (`nb_projets`) et le plus récent, et
  noter les écartés. Les valeurs de METHODE.md (prise duplex 64,81 $/1,175 h ; USB 77,45 $/1,125 h ; DDFT
  65,38 $/1,3 h ; tel/data 3/4 22,32 $/0,89 h ; interrupteur 75,47 $ ; percement 150 $/1 h ; scan dalle
  1 250 $ ; conduit 3/4 03C12 4,24 $/pi 0,113 h ; conduit vide 3/4 1,41 $/pi 0,056 h ; monument 250 $ ;
  lecteur 15 $ ; gâche 15 $ ; thermostat 35 $ ; sortie TV 15 $ ; luminaire 0,75 h ; enseigne 1 h ; détecteur
  0,5 h ; panneau 8 h ; disjoncteur 1P 0,2 h / 3P 1 h ; luminaire enlevé 0,5 h ; prise enlevée 0,35 h ;
  relocalisation de prise 1,5 h ; moteur 0,75 h ; UTA 1 h ; annonciateur relocalisé 8 h ; nacelle
  1 250 $/16 h) sont des repères : chaque valeur doit quand même être retrouvée et citée dans le catalogue.
- Luminaires, enseignes, têtes d'urgence, détecteurs, panneaux : 0 $ en ligne (temps seulement) + lots
  confirmés (METHODE.md §2) : LOT-ECL 11 893 $, LOT-DIST 6 200 $, LOT-JCI 7 400 $, LOT-DET 600 $, LOT-GPR
  1 250 $ — à sortir dans `"lots": {...}` de ton JSON. Un disjoncteur dont le prix est dans LOT-DIST se
  chiffre 0 $ en ligne (temps seulement) ; idem pour tout appareil couvert par un lot.
- Familles absentes du catalogue Dupuis → prix régulier Lumen de la feuille `Matériel Lumen` (code Lumen en
  `src`) + temps par « jugement (Estimation_2) » (colonne h/unité de Détail, citée), chaque cas en note.
  Attention : les prix d'assemblage Dupuis incluent boîte, plaque, raccord — ne pas ajouter de boîtes/plaques
  Lumen pour des appareils déjà chiffrés au prix d'assemblage Dupuis.
- Les quantités hors plan de Détail (conduits, filage) sont en mètres ; le catalogue est au pied : le prix et le
  temps que tu fournis sont par PIED (`u: "PI"`), le directeur A fournit la longueur en pieds.
- Taux : 85 $/h (METHODE.md §5, dossiers août–octobre 2026) — le 124 $/h de la feuille Sommaire n'est pas
  retenu. Facteur de prix de vente 1,244. Tu les rappelles dans tes notes, tu ne les appliques pas.

## Nomenclature des codes (ARCHITECTURE.md §3 — le directeur A utilise les mêmes)
Sur plan `<FAM>-<P>`, P ∈ {I installer, E enlever, R relocaliser} : PC prise double 15 A · PU USB · PG DDFT ·
SD sortie data · TV · INT interrupteur simple · TH thermostat · BJ boîte de jonction · MP monument plancher ·
LC lecteur de carte · GA gâche · DM détecteur mouvement · BC boîtier C · ENC encastré · ENCU encastré urgence ·
L14 LED 1x4 · L22 LED 2x2 · L4 LED 4 pi · LLIN luminaire linéaire · LA1 LC1 LC11 LC13 LE luminaires neufs ·
Z6 enseigne · DF détecteur fumée · SM station manuelle · HP haut-parleur · PA panneau annonciateur ·
MM moteur monophasé · MT moteur triphasé. Portées présentes (rapport-releve.md) : PC I25/E7/R8, PU I20,
PG I22/E4/R1, SD I65/E17/R3, INT I5/E1, TH I2, BJ I3/E2, MP I3/E3, LC I2, DM E1, ENC E26/R4, L14 E6, L22 E8,
HP E1, LA1 I11, LC1 I12, LC11 I6, LC13 I15, LE I3, Z6 I3, DF I2/R1/E1, PA I1 (relocalisé), MM I3/R6, MT I4.
Hors plan : codes Détail tels quels (A-07…A-11, B-01…B-09, C-01…C-08, D-09…D-16, E-03, E-06…E-11, F-05,
F-08…F-10, G-02…G-07, H-01…H-04) + X-01 scan dalle, X-02 nacelle si justifiée. Tu fournis p/h pour TOUS ces
codes (y compris ceux que A pourrait écarter) : mieux vaut une correspondance inutilisée qu'un code sans prix.

## Découpage imposé en 3 chefs de lot (tu peux l'affiner, pas le rendre non disjoint)
- **Chef B1 — dispositifs** : PC/PU/PG/SD/TV/INT/TH/BJ/MP/LC/GA/DM/BC en I, E, R (libellés « ENLEVER PRISE »,
  « RELO PRISE », « PRISES A DEMANTELER », « SORTIE DATA », « TEL/DATA 3/4 », « MONUMENT PLANCHER … », etc.),
  dernière valeur, écartés notés.
- **Chef B2 — éclairage/urgence/alarme/mécanique/distribution + conduits/filage + Lumen** : ENC/ENCU/L14/L22/
  L4/LLIN/HP (enlever/relocaliser : « ENLEVER FIXTURE … », « FIXTURE ENCASTRE ENLEV », « APPAREIL
  D'ECLAIRAGE A DEMANTELER »), LA1/LC1/LC11/LC13/LE (0 $ + temps, « LUMINAIRE A1 », « LUMINAIRE C1 »…),
  Z6, DF/SM/PA (« RELO PANNEAU ANNONCIA », « PANNEAU ANNONCIATEUR »), MM/MT (« MOTEUR », « MOTEUR UAF-1 »,
  « MOTEUR VE-2 120V »), B-01…B-09 (« PANNEAU … », « DISJ … »), nacelle, scan, percements, conduits
  (« CONDUIT 3/4 03C12 », « CONDUIT VIDE 3/4 », « CONDUIT 1 … », conversion au pied), câbles AI, et le
  repli Lumen pour les familles introuvables.
- **Chef B3 — bordereau et doubles comptes** : article du bordereau (3.22 démontage, 3.23 mécanique,
  3.24 panneau 600 V, 3.25 disjoncteurs, 3.26 MCC, 3.27 USB, 3.28 prises 15 A, 3.29 MALT isolées, 3.30 GFI,
  3.31 percements/conduit/filage/JB, 3.32 scan dalle, 3.33 sorties réseau, 3.34 monument, 3.35 éclairage +
  contrôle, 3.36 détecteur, 3.37 annonciateur, 3.38 certification, 5.11, 5.19, 6.1) pour CHAQUE code, règle
  d'affectation écrite (ex. ENLEVER/RELOCALISER-dépose → 3.22 ; lots fournisseur → article de la famille) ;
  et la liste des doubles comptes potentiels entre le relevé sur plan et la feuille Détail (A-01…A-06,
  D-01…D-08, E-01/E-02/E-04/E-05, F-01…F-04/F-06/F-07, G-01, boîtes Lumen vs prix d'assemblage), chacun
  avec la règle à appliquer (le plan gagne ; un objet physique n'est payé qu'une fois).
Chaque chef de lot découpe lui-même son lot en 3 sous-lots disjoints et couvrants pour ses releveurs.

## Format de sortie (ARCHITECTURE.md §5) — pour tes subalternes et pour toi
`{"niveau": "...", "nom": "...", "modele_demande": "...", "effort_demande": "...", "lignes": [{code, desc, q,
u, p, h, art, src}], "notes": [...], "lots": {...}, "doubles_comptes": [{codes, regle}]}` ; `q` à `null`
dans tout le lot B ; `p` = `prix_a_utiliser`, `h` = `temps_a_utiliser` de la ligne citée (ou Lumen /
jugement, dit en clair dans `src`). Releveurs → `lots/releveur-B<n>-<m>.json`, chefs → `lots/chef-B<n>.json`,
toi → `lots/directeur-B.json`.

## Choix de l'effort de tes chefs de lot
Tu choisis l'effort (`low|medium|high|xhigh|max`) de chaque chef de lot selon la difficulté de son lot (grille
ARCHITECTURE.md §7) et tu justifies chaque choix d'une ligne dans tes notes. Chaque chef de lot fait de même
pour ses releveurs. Nos moyens ne sont pas comptés : choisis ce qui maximise la justesse, pas l'économie.

## À ta relance (consolidation)
Rouvre le catalogue pour au moins 5 lignes de chaque chef et vérifie `p == prix_a_utiliser` et
`h == temps_a_utiliser` du libellé cité (score x/5 en notes ; une erreur = lot revu), qu'aucun code n'apparaît
deux fois, que tous les codes de la nomenclature ont un prix et un temps (ou un repli Lumen/jugement noté),
que `lots` contient les 5 lots confirmés, puis écris `lots/directeur-B.json` et vérifie qu'il se charge en
JSON. Réponds avec seulement : nombre de codes couverts, codes sans correspondance Dupuis (et leur repli), et
tes décisions d'arbitrage en 5 lignes maximum.

Maintenant : lis, découpe, écris les 3 prompts, et arrête-toi en répondant « prompts prêts » avec l'effort choisi
pour chaque chef de lot et sa justification d'une ligne.
