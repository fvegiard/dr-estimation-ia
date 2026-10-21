effort: xhigh
modele: haiku

# Releveur B2-2 — haut-parleur, alarme incendie, moteurs, distribution (PP-3 et disjoncteurs), nacelle (essaim 2, chiffrage à l'aveugle S-1902, lot B2 : prix et temps « méthode Dupuis »)

Tu es le releveur B2-2, modèle Claude Haiku 5.5, feuille de l'arbre d'une équipe hiérarchique d'estimation
électrique chez DR Électrique : directeur B (Claude Opus 5.5) → chef de lot B2 (Claude Sonnet 5.5, ton supérieur,
qui a écrit ce brief) → toi. Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission (lot B, prix et temps) : pour chacun des 28 codes de TON sous-lot (liste exacte plus bas), trouver le PRIX
unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue =
dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités
sont la mission de l'équipe A : `q` reste `null` partout. Tu écris UN fichier :
`/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-2.json`, tu le vérifies, puis tu t'arrêtes.

Ce brief se suffit à lui-même : tu ne vois ni le prompt de ton chef ni ses échanges. Les chiffres que le chef a
relevés dans le catalogue (colonnes « valeurs vues par le chef ») sont des CONTRÔLES : tu relis toi-même chaque
ligne dans le CSV avec `ligne()` et ce sont TES valeurs relues qui vont dans le JSON, pas les siennes.

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

Précisions pour toi, releveur (elles complètent les règles ci-dessus sans les changer) :
- Règle 5 : tu n'écris QU'UN seul fichier, `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-2.json`.
  Aucun autre fichier (pas de script sur disque : exécute ton Python avec `python3 - <<'EOF' … EOF`), aucun prompt.
- Règle 6 : tu es la feuille de l'arbre. Tu n'écris de prompt pour personne et tu ne lances personne.
- Règle 2 : dans le dossier de travail, tu peux lire tout le kit (CONSIGNES.md, METHODE.md, ARCHITECTURE.md,
  rapport-releve.md, reserves.md, releve.xlsx, le catalogue CSV et les fichiers de `entree/`). Tu n'ouvres PAS les
  autres fichiers de `lots/` ni de `prompts/` (ceux des autres équipes et des autres releveurs) : ils fausseraient
  ton travail à l'aveugle.

Mécanique de relais (obligatoire, mot pour mot) :
```
MÉCANIQUE DE RELAIS (à recopier mot pour mot dans chaque prompt de releveur) :
- Aucun agent de l'essaim ne peut en lancer un autre (personne n'a l'outil Agent ; ni `claude -p`, ni script
  de lancement). La session principale lance, tels quels, les prompts écrits dans prompts/…, dont les deux
  premières lignes sont obligatoirement « effort: <low|medium|high|xhigh|max> » puis « modele: <opus|sonnet|haiku> ».
- Organigramme du lot B (prix et temps) : directeur B (opus) → 3 chefs de lot (sonnet) B1, B2, B3 → chacun
  EXACTEMENT 3 releveurs (haiku). Le chef de lot B<n> a le droit de briefer EXACTEMENT 3 releveurs, modèle haiku ;
  il écrit leurs prompts dans prompts/directeur-B/chef-<n>/releveur-1.md, releveur-2.md, releveur-3.md, puis
  il s'arrête. Il est relancé quand ses 3 releveurs ont écrit lots/releveur-B<n>-1.json, lots/releveur-B<n>-2.json
  et lots/releveur-B<n>-3.json, et il consolide alors lots/chef-B<n>.json ; le directeur B consolide ensuite
  lots/directeur-B.json.
- Un releveur est la feuille de l'arbre : il ne délègue à personne, n'écrit aucun prompt, ne lance aucun agent.
  Il fait lui-même tout son travail, écrit UNIQUEMENT son fichier lots/releveur-B<n>-<m>.json, vérifie qu'il se
  charge en JSON, répond en une ligne (nom du fichier écrit + nombre de lignes) et s'arrête.
```

## Dossier de travail et fichier à écrire
- Dossier de travail (absolu) : `/home/claude/entrainement/S-1902/swarm-2/` ; langage : `python3` (stdlib + openpyxl).
- Fichier à écrire (nom EXACT) : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-2.json`
- Champs à écrire : `"niveau": "releveur"`, `"nom": "B2-2"`, `"modele_demande": "haiku"`, `"effort_demande": "xhigh"`.

## Le kit — comment lire chaque fichier
Tous les chemins sont sous `/home/claude/entrainement/S-1902/swarm-2/` (chemins absolus conseillés, `python3`).

1. `catalogue-prix-temps-dupuis.csv` — catalogue de M. Dupuis, 2 068 lignes, séparateur `;`, encodage `utf-8-sig`.
   Colonnes PERMISES : `description` (libellé, souvent tronqué ou mal orthographié), `um` (U = unité, P = pied ;
   2 lignes seulement en M = mètre), `classe`, `prix_a_utiliser`, `temps_a_utiliser` (= « PRIX À UTILISER » /
   « TEMPS À UTILISER », dernière valeur de Dupuis), `nb_projets`, `nb_lignes`, `dernier_prix` (identique à
   `prix_a_utiliser`), `date_dernier`, `projet_dernier`, `projets`.
   Colonnes INTERDITES pour p et h : `prix_unit_median`, `temps_unit_median`, `prix_min`, `prix_max`,
   `temps_min`, `temps_max`, `var_prix_pct`, `var_temps_pct`. JAMAIS la médiane.
   Il n'y a PAS de colonne TEMPSEC : un conduit se chiffre en prix/pi et temps/pi (QTE × TEMPUNI).
   Deux libellés existent en double (P et M) : « 16AWG 3C ALARME ARME 3 » et « COND FLEX 1PO ALUM BOB » — préciser l'um.
   Lecture type :
   ```python
   import csv, re
   CAT = '/home/claude/entrainement/S-1902/swarm-2/catalogue-prix-temps-dupuis.csv'
   rows = list(csv.DictReader(open(CAT, encoding='utf-8-sig'), delimiter=';'))
   assert len(rows) == 2068, len(rows)
   def cherche(motif):
       """Toutes les lignes dont la description contient le motif (regex, sans casse)."""
       for r in rows:
           if re.search(motif, r['description'], re.I):
               print(repr(r['description']), 'um=' + r['um'], 'p=' + r['prix_a_utiliser'],
                     'h=' + r['temps_a_utiliser'], 'nb_projets=' + r['nb_projets'],
                     r['date_dernier'], r['projet_dernier'])
   def ligne(desc, um=None):
       """La ligne dont la description est EXACTEMENT desc (et l'um si donnée)."""
       t = [r for r in rows if r['description'] == desc and (um is None or r['um'] == um)]
       assert len(t) == 1, (desc, len(t))
       return t[0]
   cherche(r'ENLEVER PRISE')
   ```
   Chercher par sous-chaînes courtes et par variantes (ex. `RELO`, `ENLEV`, `ENL$`, `DEMANTEL`, `FUM`,
   `ANNO`), comparer TOUS les candidats, et ne jamais conclure « absent » après une seule recherche.
2. `entree/reference-Estimation_2.xlsx` (openpyxl, `data_only=True`) :
   - feuille `Détail` : colonnes Code, Description, Réf. plan, Qté, Unité, Prix mat. unit., Total mat., h / unité,
     Total h, Total MO, Total ligne, Notes — lignes A-01…H-04 (+ OPT-1…4 hors total). Ses heures sont un « estimé Léna AI à valider » : on ne les prend QUE comme « jugement (Estimation_2) » quand le catalogue Dupuis n'a rien.
     Ses longueurs (conduits, fils) sont en MÈTRES.
   - feuille `Matériel Lumen` : colonnes Code Lumen, Description, Qté, Unité, Prix unit., Total, Base de quantité —
     prix réguliers Lumen du 2026-10-07, seulement pour une famille ABSENTE du catalogue Dupuis.
   - feuille `Sommaire` : taux 124 $/h « référence Jo » — NON retenu.
   ```python
   import openpyxl, re
   wb = openpyxl.load_workbook('/home/claude/entrainement/S-1902/swarm-2/entree/reference-Estimation_2.xlsx', data_only=True)
   for row in wb['Détail'].iter_rows(values_only=True):
       if row[0] and re.match(r'^[A-H]-\d\d$', str(row[0])):
           print(row)
   for row in wb['Matériel Lumen'].iter_rows(values_only=True):
       if any(c is not None for c in row):
           print(row)
   ```
3. `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`) : articles électriques 3.22 à 3.38,
   plus 5.11 « Percement du plancher », 5.19 « Démolition des systèmes électriques », 6.1 « Conditions de mise en œuvre et autres », 6.2 « Frais généraux, administration et profit ».
4. `releve.xlsx` (feuille `Par libellé` : Libellé, Famille, Quantité, Description, Source) et `rapport-releve.md`
   (tableau « famille | total | portées » : les portées INSTALLER / ENLEVER / RELOCALISER / CONSERVER ne sont QUE
   là ; CONSERVER = aucun travail, donc aucun code). `reserves.md` : réserves du relevé (R-002 portées, R-007 prises).
5. `METHODE.md` : la méthode Dupuis, les lots fournisseur confirmés, le taux et le facteur.

## Règles de prix et de temps
- `p` = `prix_a_utiliser` et `h` = `temps_a_utiliser` de la ligne citée, recopiés EXACTEMENT comme nombres
  (ex. 4.2441 et 0.1128, pas l'arrondi 4,24 / 0,113 de METHODE.md).
- Choix entre libellés concurrents, dans cet ordre :
  1. le libellé dont `prix_a_utiliser` et/ou `temps_a_utiliser` égale le repère de METHODE.md (liste ci-dessous) ;
  2. sinon le libellé qui décrit le MÊME objet ET la MÊME action (installer ; enlever = « ENLEVER », « ENL »,
     « A DEMANTELER » ; relocaliser = « RELO ») ;
  3. sinon le plus grand `nb_projets` ;
  4. sinon le `date_dernier` le plus récent.
  Écarter un libellé dont `temps_a_utiliser` = 0 pour un travail réel quand une autre ligne a un temps non nul.
  Chaque candidat écarté va dans `notes` avec son libellé exact, p, h, nb_projets et date.
- Les lettres de type de luminaire (A1, C1, E…) sont propres à chaque projet : « LUMINAIRE A1 » d'un autre
  dossier n'est PAS le luminaire A1 de S-1902 ; c'est le repère METHODE (luminaire 0,75 h) qui tranche.
- Un libellé Dupuis analogue (même action, objet voisin) vaut mieux que Lumen ou le jugement, à condition de le
  dire en note. Ordre de repli quand Dupuis n'a vraiment rien : prix régulier Lumen (feuille `Matériel Lumen`,
  code Lumen dans `src`) pour le matériel + temps par « jugement (Estimation_2) » (h / unité de la ligne Détail
  la plus proche, citée) — chaque cas en note.
- Les prix d'assemblage Dupuis incluent boîte, plaque, raccord : ne JAMAIS ajouter de boîte/plaque/prise Lumen
  pour un appareil déjà chiffré au prix d'assemblage Dupuis.
- ENLEVER → p = 0 (temps seulement). RELOCALISER → prix selon le catalogue (souvent 0 $) + temps de relocalisation.
- Luminaires, enseignes, têtes d'urgence, détecteurs, panneaux et disjoncteurs couverts par un lot fournisseur :
  p = 0 en ligne (temps seulement). Si le libellé retenu a un `prix_a_utiliser` non nul, mettre p = 0 et l'écrire
  dans `src` : « p = 0 forcé : couvert par LOT-xxx (catalogue p = …) ».
- Lots fournisseur confirmés (METHODE.md §2, prix confirmés par Francis le 2026-10-20) : LOT-ECL 11 893 $,
  LOT-DIST 6 200 $, LOT-JCI 7 400 $, LOT-DET 600 $ (2 détecteurs), LOT-GPR 1 250 $.
- Taux 85 $/h (METHODE.md §5, dossiers août–octobre 2026 ; le 124 $/h du Sommaire n'est pas retenu), facteur de
  prix de vente 1,244 : à rappeler dans les notes, à ne PAS appliquer.

Repères de METHODE.md (à retrouver et citer dans le catalogue, valeur exacte du CSV) : prise duplex 15 A
64,81 $ / 1,175 h ; USB 77,45 $ / 1,125 h ; DDFT 65,38 $ / 1,3 h ; tel/data 3/4 22,32 $ / 0,89 h (tel/data
0,63–0,89 h) ; interrupteur 75,47 $ ; percement 150 $ / 1 h ; scan dalle 1 250 $ ; conduit 3/4 03C12
4,24 $/pi 0,113 h/pi ; conduit vide 3/4 1,41 $/pi 0,056 h/pi ; monument 250 $ ; lecteur de carte 15 $ ; gâche
15 $ ; thermostat 35 $ ; sortie TV 15 $ ; luminaire 0,75 h ; enseigne 1 h ; tête 0,5 h ; détecteur 0,5 h ;
panneau 8 h ; disjoncteur 1P 0,2 h / 3P 1 h ; luminaire enlevé 0,5 h ; prise enlevée 0,35 h ; relocalisation
de prise 1,5 h ; moteur 0,75 h ; UTA 1 h ; annonciateur relocalisé 8 h ; nacelle 1 250 $ / 16 h.

## Nomenclature des codes (commune aux équipes A et B — le chef joint quantités et prix sur `code`)
- Sur plan : `<FAM>-<P>`, P ∈ {I installer, E enlever, R relocaliser}. FAM : PC prise double 15 A · PU USB ·
  PG DDFT · SD sortie data · TV · INT interrupteur simple · TH thermostat · BJ boîte de jonction · MP monument
  plancher · LC lecteur de carte · GA gâche · DM détecteur de mouvement · BC boîtier C · ENC encastré · ENCU
  encastré urgence · L14 LED 1x4 · L22 LED 2x2 · L4 LED 4 pi · LLIN luminaire linéaire · LA1 LC1 LC11 LC13 LE
  luminaires neufs (tableau E-008 : A1, C1, C1_1, C1_3, E) · Z6 enseigne · DF détecteur de fumée · SM station
  manuelle · HP haut-parleur · PA panneau annonciateur · MM moteur monophasé · MT moteur triphasé.
- Hors plan : le code de la feuille Détail tel quel (A-07, B-01, C-05, D-12, H-01…), ou X-01 scan dalle,
  X-02 nacelle. Lots : LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR.
- Un code qui n'a pas de portée dans le relevé est quand même chiffré (« portée absente du relevé — correspondance de précaution » dans `src`) : mieux vaut une correspondance inutilisée qu'un code sans prix.

## Format de `src`, `u` et `art`
- `src` Dupuis : `catalogue Dupuis « <description exacte> » um=<U|P> (dernier <date_dernier>, <projet_dernier>, nb_projets <n>)`.
  `src` Lumen : `Matériel Lumen <Code Lumen> « <Description> » <Prix unit.> $/<Unité>`.
  `src` jugement : `jugement (Estimation_2) Détail <code> h/unité <valeur>`. Un `src` composé (ex. deux libellés
  additionnés) écrit chaque libellé et l'opération.
- `u` : `U` (unité ; catalogue um U, Détail « u », « poste », « rangée »), `PI` (pied ; catalogue um P — tout
  conduit et tout fil est chiffré AU PIED, l'équipe A fournit la longueur en pieds, 1 m = 3,2808 pi), `LOT`
  (Détail « lot » et lots fournisseur).
- `art` : article du bordereau, texte (« 3.28 »). Règle PROVISOIRE (le chef de lot B3 fixe la règle définitive) :
  tout code -E → « 3.22 » ; tout code -R → « 3.22 » sauf PA-R → « 3.37 » et MM-R/MT-R → « 3.23 » ; PC-I 3.28 ;
  PU-I 3.27 ; PG-I 3.30 ; SD-I 3.33 ; TV-I 3.33 ; MP-I 3.34 ; BJ-I 3.31 ; INT-I 3.35 ; DM-I 3.35 ; TH-I 3.23 ;
  LC-I et GA-I 3.33 ; BC-I 3.36 ; luminaires (LA1, LC1, LC11, LC13, LE, ENC, ENCU, L14, L22, L4, LLIN) -I et Z6-I
  3.35 ; DF-I, SM-I, HP-I 3.36 ; PA-I 3.37 ; MM-I, MT-I 3.23 ; B-01 3.24 ; B-02…B-08 3.25 ; B-09 3.24 ;
  conduits, filage, percements, boîtes 3.31 ; X-01 3.32 ; X-02 6.1 ; D-09, D-10 3.31 ; D-11, E-06 3.33 ;
  E-03 3.34 ; LOT-ECL 3.35 ; LOT-DIST 3.24 (+ 3.25) ; LOT-JCI 3.38 ; LOT-DET 3.36 ; LOT-GPR 3.32.

## Format JSON (ARCHITECTURE.md §5) — exemple adapté à ton niveau (releveur)
```json
{
  "niveau": "releveur",
  "nom": "B2-2",
  "modele_demande": "haiku",
  "effort_demande": "xhigh",
  "lignes": [
    {"code": "PC-I", "desc": "Prise double 15 A 120 V neuve", "q": null, "u": "U", "p": 64.81, "h": 1.175,
     "art": "3.28", "src": "catalogue Dupuis « PRISE DUPLEX 15A 120V » um=U (dernier 2026-09-25, S-1857 - Maison St-Michel, nb_projets 20)"}
  ],
  "notes": ["candidats écartés, hésitations, replis Lumen/jugement, portées absentes"],
  "doubles_comptes": [{"codes": ["D-06", "PC-I"], "regle": "le plan gagne ; un objet physique n'est payé qu'une fois"}]
}
```
`q` est TOUJOURS `null` dans le lot B. `p` et `h` sont des nombres (jamais du texte). Écrire le fichier avec
`json.dump(obj, f, ensure_ascii=False, indent=2)`. Chaque code n'apparaît qu'UNE fois par fichier.

## Vérifications avant d'écrire un JSON (ARCHITECTURE.md §6, tous niveaux)
1. Le JSON se charge (`python3 -c "import json;json.load(open('...'))"`) et contient `lignes` + `notes`.
2. Chaque ligne a un `src` qui pointe vers un libellé/une cellule réellement lu ; tout code du sous-lot est présent
   une et une seule fois ; `q` est `null` partout.
3. Pas de médiane : pour chaque ligne Dupuis, relire la ligne avec `ligne(desc, um)` et vérifier
   `p == float(prix_a_utiliser)` et `h == float(temps_a_utiliser)` (sauf p = 0 forcé par un lot, écrit dans `src`).
4. Un rapport d'agent n'est pas une preuve : le niveau supérieur juge sur le fichier `lots/*.json`, pas sur le récit.

## TON SOUS-LOT B2-2 — 28 codes (haut-parleur, alarme incendie, mécanique, distribution B-01…B-09, nacelle X-02)

Liste exacte (28), ni plus ni moins : HP-I HP-E HP-R DF-I DF-E DF-R SM-I SM-E SM-R PA-I PA-E PA-R MM-I MM-E MM-R MT-I MT-E MT-R B-01 B-02 B-03 B-04 B-05 B-06 B-07 B-08 B-09 X-02
Tu n'as AUCUN autre code : luminaires, enseignes Z6 (B2-1) ; conduits, filage, percements, scan de dalle et lots fournisseur (B2-3) — ne les écris pas.

### Contexte du chef (libellés candidats du directeur B, recopiés tels quels — liste non exhaustive)
Libellés candidats à examiner (valeurs à relire dans le CSV ; chercher aussi d'autres variantes). « repère » = valeur de METHODE.md qui tranche selon la règle 1.

- HP (HP ENCASTRE PLAFOND : ENLEVER 1) : HP-E aucun libellé « ENLEVER HAUT PARLEUR » connu → analogue Dupuis ou
  jugement, en note ; HP-R : « RELO HAUT PARLEUR PL », « RELO HAUPARLEUR MURAL » (le libellé « RELO HAUT PARLEUR »
  a un temps 0 : à écarter, noter) ; HP-I : « HAUT PARLEUR ».

Alarme incendie :
- DF (DETECTEUR FUMEE : CONSERVER 6, INSTALLER 2, RELOCALISER 1, ENLEVER 1) : DF-I « DETECTEUR A FUMEE »
  (nb_projets 9) vs « DETECTEUR FUMEE », « DETECTEUR A FUME » (repère détecteur 0,5 h), p = 0 (LOT-DET 600 $ =
  2 détecteurs) ; DF-R « RELO DETECTEUR A FUME » vs « RELO DETECTEUR FUME » ; DF-E aucun libellé direct connu →
  analogue (« STATION ENL », « IC ENL »…) ou jugement, en note.
- SM (STATION MANUELLE : CONSERVER 4 → précaution) : SM-I « STATION MANUEL » ; SM-E « STATION ENL » ; SM-R
  « RELO STATION MANUEL ».
- PA (PANNEAU ANNONCIATEUR : INSTALLER 1 au relevé, mais Détail G-04, bordereau 3.37 et relevé alarme AI-05 disent
  RELOCALISATION de l'annonciateur Simplex existant) : chiffrer PA-I ET PA-R comme une relocalisation (repère
  annonciateur relocalisé 8 h). Candidats : « RELO PANNEAU ANNONCIA » (550 $ / 8 h, nb_projets 1, 2026-06-26),
  « RELO PANN ANNOCIATEUR » (0 $ / 8 h, nb_projets 2), « PANNEAU ANNONCIATEUR » (0 $ / 8 h), « REINSTALLER PANN ANNO » (24 h). Le repère ne fixe que le temps : arbitrer le prix (règles 2 à 4) et noter l'autre option avec son
  montant. PA-E : analogue, en note. La reprogrammation JCI (AI-05) est dans LOT-JCI, pas dans ces lignes.

Mécanique (MOTEUR MONOPHASE : RELOCALISER 6, INSTALLER 3 ; MOTEUR TRIPHASE : CONSERVER 5, INSTALLER 4) — MM-I,
MM-E, MM-R, MT-I, MT-E, MT-R. Contexte Détail : C-01 UTA-01 575 V 3Ø, C-02 VE-02N 575 V 3Ø, C-03 chaudières
CH-01/CH-02 600 V 3Ø, C-04 humidificateurs HUM-1/2/3 120 V 1Ø, A-10 toit « débrancher, entreposer, rebrancher »
6 équipements E.A.R. Candidats : « MOTEUR » (repère moteur 0,75 h), « MOTEUR UAF-1 » (repère UTA 1 h), « MOTEUR VE-2 120V », « MOTEUR HUM », « HUMIDIFICATEUR », « CHAUDIERE », « DEBRANCHEMENT APPAREILAGE MECANIQUE », « ENLEVER MOTEUR 1/2 HP 6 ». Aucun « RELO MOTEUR » connu pour MM-R → analogue ou jugement (Estimation_2) A-10, en note.

Distribution (hors relevé, feuille Détail ; LOT-DIST 6 200 $ = panneau NF 225 A 42 cct 3 400 $ + EDB 1P 95 $ × 20
+ EJB 3P 300 $ × 3) :
- B-01 panneau PP-3 neuf 225 A 347/600 V 42 cct NF, remplacement de l'existant : p = 0 (LOT-DIST), repère panneau
  8 h. Candidats à 8 h et 347/600 V : « PANN 400A 347/600V 3PH 4 », « PANNEAU 100A 347/600V 3F », « PANN PD 400A 347/600V 42CCT 35KA C/A », « PANN UE 200A 347/600V 3PI », « PANN S 347/600V 3PH 4F 60 » ; « PANNEAU 225A 347/600V 3 » a un temps 0 (à écarter, noter) ; « PANNEAU A CHANGER » (16 h) et « ENL PANN 42CCT 120/208V »
  (4 h) à noter comme options pour le démantèlement de l'ancien PP-3 inclus dans B-01.
- B-02 (14 × 1P-15A transférés dans PP-3), B-03 (3P-20A transféré), B-04 (3P-40A UTA-1 neuf), B-05 (3P-15A VE-2N
  neuf) : p = 0 (LOT-DIST), repères disjoncteur 1P 0,2 h / 3P 1 h : « DISJ15A1P », « DISJ 20A 1P 120V 10KA »,
  « DISJ 15A 1P 120V 10KA » ; 3P : « DISJ 100A 3P 120/240V 22 K » (p = 0 forcé, l'écrire).
- B-06 (1P-15A DDFT fontaine P2-61), B-07 (2 × 1P-15A P2-63/P2-64), B-08 (2 × 1P-20A P3-17/19) : panneaux P2/P3,
  pas PP-3. Le lot compte 20 EDB 1P ; B-02 + B-06 + B-07 + B-08 = 19 → dire en note si tu les considères couverts
  (p = 0) ou non, et donner l'autre option chiffrée (libellé Dupuis 1P avec son prix).
- B-09 mise à jour des fiches dactylographiées + identification (9 panneaux) : « IDENTIFIER LES CIRCUITS EXISTANTS A » vs jugement (Estimation_2) B-09.

- X-02 nacelle : « NACELLE » (repère 1 250 $ / 16 h). Noter le recouvrement possible avec Détail H-01
  (« plateforme/échafaudage roulant », chiffré par le chef B3).

### Portées relevées (rapport-releve.md ; CONSERVER = aucun travail)
- HP ENCASTRE PLAFOND (1) : ENLEVER 1 → HP-E utilisé ; HP-I, HP-R absents (précaution).
- DETECTEUR FUMEE (10) : CONSERVER 6, INSTALLER 2, RELOCALISER 1, ENLEVER 1 → DF-I (2), DF-R (1), DF-E (1) utilisés.
- STATION MANUELLE (4) : CONSERVER 4 → SM-I, SM-E, SM-R : portée absente (précaution).
- PANNEAU ANNONCIATEUR (1) : INSTALLER 1 au relevé, mais Détail G-04, bordereau 3.37 et relevé alarme AI-05 (reference-Releve_Alarme_Incendie.xlsx)
  disent RELOCALISATION de l'annonciateur Simplex existant → PA-I et PA-R sont chiffrés tous deux comme une relocalisation ; PA-E = précaution.
- MOTEUR MONOPHASE (9) : RELOCALISER 6, INSTALLER 3 → MM-R (6) et MM-I (3) utilisés ; MM-E absent.
- MOTEUR TRIPHASE (9) : CONSERVER 5, INSTALLER 4 → MT-I (4) utilisé ; MT-E, MT-R absents (précaution).
- B-01…B-09 et X-02 : HORS relevé (feuille Détail d'Estimation_2, codes B-01…B-09 ; X-02 = nacelle) : pas de mention « précaution ».
Un code sans portée au relevé est quand même chiffré : `precaution=True` dans `L()` écrit « portée absente du relevé —
correspondance de précaution » dans `src` (uniquement pour les codes marqués « absente » dans le tableau plus bas).

### DÉCISIONS DU CHEF DE LOT B2 (à appliquer ; vérifiées dans le CSV par le chef le 2026-10-21, que tu relis toi-même)

**1. Haut-parleur.** HP-I → « HAUT PARLEUR » (nb_projets 10, 0,5 h) ; note « HAUT PARLEUR PL » et « HAUT PARLEUR MURAL » (1,0 h, nb 1).
HP-R → « RELO HAUT PARLEUR PL » (plafond = l'objet du plan, 1,0 h) ; note « RELO HAUPARLEUR MURAL » (1,0 h) et écarte « RELO HAUT PARLEUR »
(temps 0). HP-E (utilisé, 1 au relevé) : aucun libellé « ENLEVER HAUT PARLEUR » → ANALOGUE Dupuis « STATION ENL » (enlèvement d'un
dispositif d'alarme/sonorisation, 0,5 h) ; note les autres analogues (« IC ENL » 0,5 h, « ENLEVER FIXTURE ENCAST » 0,35 h : appareil
encastré au plafond, « EQUIPEMENT A ENLEVER » 0,5 h) et écarte « REINSTALLER HAUT PARLE » (temps 0). Ce n'est ni du Lumen ni du jugement :
un analogue Dupuis (même action, objet voisin) vaut mieux, à condition de le dire en note.

**2. Détecteurs et stations.** DF-I → « DETECTEUR A FUMEE » (nb_projets 9, repère détecteur 0,5 h), p = 0 forcé (`lot='LOT-DET'`, LOT-DET 600 $ = 2 détecteurs) ;
note « DETECTEUR FUMEE » et « DETECTEUR A FUME » (mêmes valeurs, moins de projets). DF-R → « RELO DETECTEUR A FUME » (0,75 h, nb 3, 2026-10-07) ; note
« RELO DETECTEUR FUME » (1,0 h, nb 2) et « RELO DETECTEUR A FUMEI » (0,75 h). DF-E : analogue « STATION ENL » (0,5 h) ; note « IC ENL ».
SM-I → « STATION MANUEL » (nb 16) ; SM-E → « STATION ENL » ; SM-R → « RELO STATION MANUEL » (0,75 h, nb 3). Les 3 SM = précaution.

**3. Annonciateur (PA).** PA-I ET PA-R : même ligne de relocalisation, repère « annonciateur relocalisé 8 h » : le repère ne fixe que le TEMPS ; le PRIX
s'arbitre par les règles 2 à 4 entre les libellés « RELO … ANNONCIATEUR » : « RELO PANN ANNOCIATEUR » (0 $ / 8 h, nb_projets 2) l'emporte sur « RELO PANNEAU ANNONCIA »
(550 $ / 8 h, nb_projets 1, 2026-06-26) à la règle 3. DÉCISION : 0 $ / 8 h. Note l'autre option avec son montant (+550 $) et les écartés : « PANNEAU ANNONCIATEUR »
(0 $ / 8 h, nb 4 : c'est l'installation, pas la relocalisation), « REINSTALLER PANN ANNO » (24 h ≠ repère 8 h), « RELO PANN ANNONCIATEU » (temps 0). PA-E (précaution) : analogue
« STATION ENL » (0,5 h) ; note que c'est bas pour un annonciateur et cite « ENL PANN 42CCT 120/208V » (4 h) comme option. La reprogrammation JCI (AI-05) est dans LOT-JCI : pas dans ces lignes.
Pas de `lot=` pour PA (pas couvert par LOT-DET) ; pour PA-R, mets `extra="relocalisation de l'annonciateur existant (Détail G-04, bordereau 3.37, relevé alarme AI-05)"`
et pour PA-I `extra="relevé INSTALLER 1 traité comme relocalisation (Détail G-04 / AI-05)"`.

**4. Moteurs.** MM-I et MT-I → « MOTEUR » (25 $ / 0,75 h, nb 2 ; repère moteur 0,75 h, règle 1). Note les écartés : « MOTEUR UAF-1 » et « MOTEUR VE-2 120V » (1,0 h : repère UTA 1 h, UTA-01
et VE-02N sont les lignes C-01/C-02 du Détail, hors de ton sous-lot), « MOTEUR HUM » et « HUMIDIFICATEUR » (15 $ / 0,35 h : les 3 humidificateurs sont du MM-I, mais le repère moteur prime), « CHAUDIERE » (15 $ / 0,5 h).
MM-E et MT-E (précaution) → « ENLEVER MOTEUR 1/2 HP 6 » (0,25 h, nb 2 ; même objet, même action).
MM-R (6 au relevé) et MT-R (précaution) : aucun « RELO MOTEUR » → ANALOGUE : même action « RELO » sur un équipement alimenté fixe : « RELO PLINTHE 2000W » (0 $ / 1,0 h, 2026-10-07).
Note les autres options AVEC LEUR IMPACT sur 6 unités : « DISCONNECTER ET RECON » (0 $ / 8,0 h, nb 2 → 48 h), jugement (Estimation_2) Détail A-10 (h/unité à relire dans la feuille Détail, 4 h → 24 h),
« DEBRANCHEMENT APPAREILAGE MECANIQUE » (0,4 h) + « MOTEUR » (0,75 h) (cumul à titre d'information). DÉCISION : 1,0 h ; le chef tranchera à sa relance au vu de ta note — écris-la avec soin.

**5. Distribution (hors relevé, lots : LOT-DIST 6 200 $ = panneau NF 225 A 42 cct 3 400 $ + EDB 1P 95 $ × 20 + EJB 3P 300 $ × 3).**
- B-01 : repère panneau 8 h, 347/600 V, 42 cct → « PANN PD 400A 347/600V 42CCT 35KA C/A » (8,0 h ; seul candidat à 8 h avec 42 cct ET 347/600 V), p = 0 forcé (`lot='LOT-DIST'`). Note les autres à 8 h :
  « PANN 400A 347/600V 3PH 4 » (nb 1, 2026-09-10), « PANNEAU 100A 347/600V 3F », « PANN UE 200A 347/600V 3PI », « PANN S 347/600V 3PH 4F 60 » ; écarte « PANNEAU 225A 347/600V 3 » (temps 0 pour un vrai travail).
  Options pour le démantèlement de l'ancien PP-3 (inclus dans le B-01 du Détail, 24 h Léna) : « PANNEAU A CHANGER » (16 h) et « ENL PANN 42CCT 120/208V » (4 h) : NON ajoutées, notées avec leurs valeurs (+4 h ou +16 h).
- B-02 → « DISJ15A1P » (repère disjoncteur 1P 0,2 h, nb 2), `lot='LOT-DIST'`. B-06 et B-07 → « DISJ15A1P » aussi. B-08 → « DISJ 20A 1P 120V 10KA » (catalogue 10,17 $ / 0,2 h → p = 0 forcé, à écrire dans `src`).
  Note les concurrents 1P : « DISJ 15A 1P 120V 10KA » (54,82 $ / 0,2 h), « DISJ 15A 1P 120V 10KA (AI) » (10,17 $ / 0,2 h).
- B-03, B-04, B-05 (3P) → « DISJ 100A 3P 120/240V 22 K » (719,6 $ / 1,0 h : seul 3P à 1 h, repère disjoncteur 3P 1 h) ; p = 0 forcé (`lot='LOT-DIST'`, 3 × EJB 3P). Note l'écart de calibre (100 A au lieu de 15–40 A) et « DISJ 125A 3P 600V 18KA » (4 h) écarté.
- COUVERTURE B-06/B-07/B-08 par LOT-DIST : le lot compte 20 EDB 1P ; B-02 (14) + B-06 (1) + B-07 (2) + B-08 (2) = 19 ≤ 20 → DÉCISION : tous couverts (p = 0). Écris en note l'autre option chiffrée : si NON couverts,
  B-06 et B-07 (3 disjoncteurs) à « DISJ 15A 1P 120V 10KA » 54,82 $ = 164,46 $ et B-08 (2) à « DISJ 20A 1P 120V 10KA » 10,17 $ = 20,34 $, soit 184,80 $ en tout ; et pour les 3P non couverts : 3 × 719,60 $ = 2 158,80 $.
  Écris aussi : « reference-Estimation_2.xlsx / Matériel Lumen exclut les disjoncteurs P2/P3 (marque à confirmer) : c'est la raison du doute, tranché par le décompte 19 ≤ 20 ».
  Vérifie la décomposition de LOT-DIST : 3 400 + 20 × 95 + 3 × 300 = 6 200 $.
- B-09 (9 panneaux) → « IDENTIFIER LES CIRCUITS EXISTANTS A » (0 $ / 3,0 h, nb 1, 2026-09-23, s-1866) : analogue Dupuis (même action) ; note le jugement (Estimation_2) Détail B-09 (h/unité à relire : 1 h) et l'impact sur 9 panneaux :
  27 h (Dupuis) contre 9 h (jugement) — à signaler au chef comme l'arbitrage le plus incertain de ton sous-lot.

**6. Nacelle X-02.** « NACELLE » (1 250 $ / 16,0 h, nb 2, 2026-07-14 ; repère nacelle 1 250 $ / 16 h). Note le recouvrement possible avec le Détail H-01 (« mobilisation / plateforme-échafaudage roulant », 16 h Léna, chiffré par un autre chef) :
doubles_comptes {X-02, H-01}.

### Tableau des décisions (une ligne par code — 28 lignes)
| code | desc suggérée | libellé retenu (copie exacte, repr Python) | um | valeurs vues par le chef (à relire) | u | art | lot | portée au relevé |
|---|---|---|---|---|---|---|---|---|
| HP-I | Haut-parleur encastré plafond à installer (précaution) | 'HAUT PARLEUR' | U | p=0.0 h=0.5 nb=10 2026-08-26 | U | 3.36 | — | absente |
| HP-E | Haut-parleur encastré plafond à enlever | 'STATION ENL' | U | p=0.0 h=0.5 nb=1 2026-02-09 | U | 3.22 | — | ENLEVER 1 |
| HP-R | Haut-parleur encastré plafond à relocaliser (précaution) | 'RELO HAUT PARLEUR PL' | U | p=0.0 h=1.0 nb=1 2026-06-02 | U | 3.22 | — | absente |
| DF-I | Détecteur de fumée neuf | 'DETECTEUR A FUMEE' | U | p=0.0 h=0.5 nb=9 2026-09-25 | U | 3.36 | LOT-DET | INSTALLER 2 |
| DF-E | Détecteur de fumée existant à enlever | 'STATION ENL' | U | p=0.0 h=0.5 nb=1 2026-02-09 | U | 3.22 | — | ENLEVER 1 |
| DF-R | Détecteur de fumée existant à relocaliser | 'RELO DETECTEUR A FUME' | U | p=0.0 h=0.75 nb=3 2026-10-07 | U | 3.22 | — | RELOCALISER 1 |
| SM-I | Station manuelle à installer (précaution) | 'STATION MANUEL' | U | p=0.0 h=0.5 nb=16 2026-10-07 | U | 3.36 | — | absente (CONSERVER 4) |
| SM-E | Station manuelle à enlever (précaution) | 'STATION ENL' | U | p=0.0 h=0.5 nb=1 2026-02-09 | U | 3.22 | — | absente |
| SM-R | Station manuelle à relocaliser (précaution) | 'RELO STATION MANUEL' | U | p=0.0 h=0.75 nb=3 2026-10-07 | U | 3.22 | — | absente |
| PA-I | Annonciateur Simplex : relocalisation (relevé : INSTALLER 1) | 'RELO PANN ANNOCIATEUR' | U | p=0.0 h=8.0 nb=2 2026-03-09 | U | 3.37 | — | INSTALLER 1 (= relocalisation) |
| PA-E | Panneau annonciateur à enlever (précaution) | 'STATION ENL' | U | p=0.0 h=0.5 nb=1 2026-02-09 | U | 3.22 | — | absente |
| PA-R | Annonciateur Simplex existant à relocaliser | 'RELO PANN ANNOCIATEUR' | U | p=0.0 h=8.0 nb=2 2026-03-09 | U | 3.37 | — | absente au relevé (voir PA-I) |
| MM-I | Moteur monophasé à raccorder (installer) | 'MOTEUR' | U | p=25.0 h=0.75 nb=2 2026-02-19 | U | 3.23 | — | INSTALLER 3 |
| MM-E | Moteur monophasé à enlever (précaution) | 'ENLEVER MOTEUR 1/2 HP 6' | U | p=0.0 h=0.25 nb=2 2026-03-09 | U | 3.22 | — | absente |
| MM-R | Moteur monophasé à relocaliser (débrancher, relocaliser, rebrancher) | 'RELO PLINTHE 2000W' | U | p=0.0 h=1.0 nb=1 2026-10-07 | U | 3.23 | — | RELOCALISER 6 |
| MT-I | Moteur triphasé à raccorder (installer) | 'MOTEUR' | U | p=25.0 h=0.75 nb=2 2026-02-19 | U | 3.23 | — | INSTALLER 4 |
| MT-E | Moteur triphasé à enlever (précaution) | 'ENLEVER MOTEUR 1/2 HP 6' | U | p=0.0 h=0.25 nb=2 2026-03-09 | U | 3.22 | — | absente |
| MT-R | Moteur triphasé à relocaliser (précaution) | 'RELO PLINTHE 2000W' | U | p=0.0 h=1.0 nb=1 2026-10-07 | U | 3.23 | — | absente (CONSERVER 5) |
| B-01 | Panneau PP-3 neuf 225 A 347/600 V 42 cct NF (remplacement de l'existant) | 'PANN PD 400A 347/600V 42CCT 35KA C/A' | U | p=0.0 h=8.0 nb=1 2026-02-02 | U | 3.24 | LOT-DIST | hors relevé (Détail B-01) |
| B-02 | Disjoncteurs 1P-15A transférés dans PP-3 (14) | 'DISJ15A1P' | U | p=0.0 h=0.2 nb=2 2026-03-09 | U | 3.25 | LOT-DIST | hors relevé (Détail B-02) |
| B-03 | Disjoncteur 3P-20A (aérotherme) transféré | 'DISJ 100A 3P 120/240V 22 K' | U | p=719.6 h=1.0 nb=1 2026-06-02 | U | 3.25 | LOT-DIST | hors relevé (Détail B-03) |
| B-04 | Disjoncteur 3P-40A UTA-1 neuf | 'DISJ 100A 3P 120/240V 22 K' | U | p=719.6 h=1.0 nb=1 2026-06-02 | U | 3.25 | LOT-DIST | hors relevé (Détail B-04) |
| B-05 | Disjoncteur 3P-15A VE-2N neuf | 'DISJ 100A 3P 120/240V 22 K' | U | p=719.6 h=1.0 nb=1 2026-06-02 | U | 3.25 | LOT-DIST | hors relevé (Détail B-05) |
| B-06 | Disjoncteur 1P-15A DDFT fontaine P2-61 | 'DISJ15A1P' | U | p=0.0 h=0.2 nb=2 2026-03-09 | U | 3.25 | LOT-DIST | hors relevé (Détail B-06) |
| B-07 | Disjoncteurs 1P-15A P2-63 / P2-64 (2) | 'DISJ15A1P' | U | p=0.0 h=0.2 nb=2 2026-03-09 | U | 3.25 | LOT-DIST | hors relevé (Détail B-07) |
| B-08 | Disjoncteurs 1P-20A P3-17 / P3-19 (2) | 'DISJ 20A 1P 120V 10KA' | U | p=10.17 h=0.2 nb=2 2026-06-26 | U | 3.25 | LOT-DIST | hors relevé (Détail B-08) |
| B-09 | Mise à jour des fiches dactylographiées + identification des circuits (9 panneaux) | 'IDENTIFIER LES CIRCUITS EXISTANTS A' | U | p=0.0 h=3.0 nb=1 2026-09-23 | U | 3.24 | — | hors relevé (Détail B-09) |
| X-02 | Nacelle | 'NACELLE' | U | p=1250.0 h=16.0 nb=2 2026-07-14 | U | 6.1 | — | hors relevé (code X-02) |

Une ligne avec « lot = LOT-DIST » ou « LOT-DET » : `p` = 0.0 forcé et `src` doit contenir « p = 0 forcé : couvert par LOT-xxx (catalogue p = … ) » (déjà fait par `L(..., lot=...)`).
Codes « absente » dans la colonne portée : `precaution=True` dans `L()`. B-01…B-09 et X-02 : pas de mention « précaution ».

### Notes et doubles comptes à écrire (obligatoires)
- Rappel (en note) : taux 85 $/h (METHODE.md §5 ; le 124 $/h du Sommaire n'est pas retenu) et facteur de prix de vente
  1,244 — à rappeler, à ne PAS appliquer.
- Chaque candidat écarté : libellé exact, p, h, nb_projets, date_dernier, et la raison de l'écart (règle 1, 2, 3 ou 4).
- Tout écart entre les valeurs que le chef a vues et ce que tu relis dans le CSV, ou tout libellé décidé par le chef
  que tu ne retrouves pas : ne devine pas, applique les règles de choix du kit et décris l'écart dans une note.
- Tout désaccord argumenté avec une décision du chef : applique la décision, écris ton désaccord en note (une note par
  désaccord, avec les chiffres). Le chef tranchera à sa relance.
- `notes` : chaque décision 1 à 6 avec ses candidats écartés et leurs valeurs ; la liste des codes « précaution ».
- `notes` : analogues utilisés (aucun libellé direct) : HP-E, DF-E, PA-E, MM-R, MT-R (et MM-E/MT-E : même objet « ENLEVER MOTEUR ») — dire pour chacun le libellé retenu, ses valeurs, et l'alternative.
- `notes` : la couverture de LOT-DIST (19 ≤ 20 EDB 1P, 3 EJB 3P) avec le calcul de l'option « non couverts ».
- `doubles_comptes` (au minimum) :
  - {"codes": ["B-01","B-02","B-03","B-04","B-05","B-06","B-07","B-08","LOT-DIST"], "regle": "panneau, disjoncteurs 1P et 3P payés UNE fois par LOT-DIST ; les lignes à p = 0 ne portent que le temps"} ;
  - {"codes": ["PA-I","PA-R","G-04"], "regle": "un seul annonciateur physique : relevé INSTALLER 1 = relocalisation Détail G-04 = bordereau 3.37 = AI-05 ; ne le payer qu'une fois"} ;
  - {"codes": ["X-02","H-01"], "regle": "nacelle et plateforme roulante de mobilisation peuvent se recouvrir : à trancher au chef B3"} ;
  - {"codes": ["DF-I","G-01","LOT-DET"], "regle": "les 2 détecteurs neufs du relevé = Détail G-01 = AI-01 ; matériel payé par LOT-DET, seul le temps de DF-I compte"} ;
  - {"codes": ["MM-I","MT-I","C-01","C-02","C-03","C-04"], "regle": "les raccordements mécaniques C-01…C-04 du Détail (UTA, VE-02N, chaudières, humidificateurs) recouvrent les moteurs MM-I/MT-I du relevé : à trancher"} ;
  - {"codes": ["MM-R","A-10"], "regle": "les 6 équipements E.A.R du toit (Détail A-10) sont les 6 MM-R du relevé : un seul des deux est payé"}.

### Aide de code (à adapter ; tu peux t'en servir telle quelle)
```python
import csv, json, re
CAT = '/home/claude/entrainement/S-1902/swarm-2/catalogue-prix-temps-dupuis.csv'
OUT = '/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-2.json'
rows = list(csv.DictReader(open(CAT, encoding='utf-8-sig'), delimiter=';'))
assert len(rows) == 2068, len(rows)

def ligne(desc, um=None):
    t = [r for r in rows if r['description'] == desc and (um is None or r['um'] == um)]
    assert len(t) == 1, (desc, len(t))
    return t[0]

def src_dupuis(r):
    return "catalogue Dupuis « %s » um=%s (dernier %s, %s, nb_projets %s)" % (
        r['description'], r['um'], r['date_dernier'], r['projet_dernier'], r['nb_projets'])

def L(code, desc, libelle, um, u, art, lot=None, precaution=False, extra=None):
    """Ligne Dupuis construite depuis le CSV : p et h = prix_a_utiliser / temps_a_utiliser (jamais retapés).
    lot='LOT-xxx' -> p = 0 forcé et écrit dans src ; precaution=True -> mention « portée absente du relevé »."""
    r = ligne(libelle, um)
    p = float(r['prix_a_utiliser']); h = float(r['temps_a_utiliser'])
    src = src_dupuis(r)
    if lot:
        src += " ; p = 0 forcé : couvert par %s (catalogue p = %s)" % (lot, r['prix_a_utiliser'])
        p = 0.0
    if precaution:
        src += " ; portée absente du relevé — correspondance de précaution"
    if extra:
        src += " ; " + extra
    return {"code": code, "desc": desc, "q": None, "u": u, "p": p, "h": h, "art": art, "src": src}

def verifier(lignes, attendus):
    codes = [l['code'] for l in lignes]
    assert len(codes) == len(set(codes)), 'code en double'
    assert sorted(codes) == sorted(attendus), (set(attendus) - set(codes), set(codes) - set(attendus))
    for l in lignes:
        assert l['q'] is None, l['code']
        assert isinstance(l['p'], (int, float)) and isinstance(l['h'], (int, float)), l['code']
        m = re.match(r"catalogue Dupuis « (.*) » um=(\w+) \(dernier", l['src'])
        if m:                                   # pas de médiane : on relit la ligne citée
            r = ligne(m.group(1), m.group(2))
            assert l['h'] == float(r['temps_a_utiliser']), ('h', l['code'])
            if 'p = 0 forcé' not in l['src']:
                assert l['p'] == float(r['prix_a_utiliser']), ('p', l['code'])
    print('OK', len(lignes), 'lignes')

# ... tu construis `lignes = [L(...), ...]`, `notes = [...]`, `doubles = [...]`, tu appelles verifier(lignes, ATTENDUS), puis :
obj = {"niveau": "releveur", "nom": "B2-2", "modele_demande": "haiku", "effort_demande": "xhigh",
       "lignes": lignes, "notes": notes, "doubles_comptes": doubles}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)
json.load(open(OUT, encoding='utf-8'))          # le fichier se recharge
```

## Ordre de travail (suis-le dans cet ordre)
1. Lis `METHODE.md` (§2 lots, §3 temps, §5 taux), `rapport-releve.md` (tableau des portées) et les parties utiles de
   `reserves.md`, puis, pour tes codes, les lignes concernées de la feuille `Détail` d'Estimation_2 (et `Matériel Lumen`
   seulement pour le contrôle demandé).
2. Pour CHAQUE code de ton sous-lot : lance `cherche(...)` sur le libellé retenu ET sur au moins un concurrent
   (sous-chaînes courtes, variantes), compare les candidats, vérifie que le libellé décidé par le chef existe tel quel
   (`ligne(libelle, um)` ; attention : certains libellés ont une espace finale — copie-les par `repr`, ne les retape
   jamais de mémoire), relis p, h, nb_projets, date_dernier, projet_dernier.
3. Construis les lignes avec l'aide de code ci-dessus (`L(...)`), écris les `notes` et les `doubles_comptes`
   (obligatoires, voir plus haut), puis `verifier(lignes, ATTENDUS)` avec la liste exacte de tes codes.
4. Écris le JSON (`json.dump(obj, f, ensure_ascii=False, indent=2)`), recharge-le, vérifie : tes 28 codes, une seule
   fois chacun, `q` = null partout, `lignes` + `notes` présents, aucun autre code que les tiens.
5. Réponds en UNE ligne : « fichier écrit : /home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-2.json — 28 lignes »
   et ARRÊTE-TOI (tu ne fais rien d'autre, tu n'écris aucun autre fichier).
