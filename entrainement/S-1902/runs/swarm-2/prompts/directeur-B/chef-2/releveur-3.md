effort: xhigh
modele: haiku

# Releveur B2-3 — conduits et filage (au pied), percements, scan de dalle, lots fournisseur (essaim 2, chiffrage à l'aveugle S-1902, lot B2 : prix et temps « méthode Dupuis »)

Tu es le releveur B2-3, modèle Claude Haiku 5.5, feuille de l'arbre d'une équipe hiérarchique d'estimation
électrique chez DR Électrique : directeur B (Claude Opus 5.5) → chef de lot B2 (Claude Sonnet 5.5, ton supérieur,
qui a écrit ce brief) → toi. Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission (lot B, prix et temps) : pour chacun des 22 codes de TON sous-lot (liste exacte plus bas), trouver le PRIX
unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue =
dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités
sont la mission de l'équipe A : `q` reste `null` partout. Tu écris UN fichier :
`/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-3.json`, tu le vérifies, puis tu t'arrêtes.

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
- Règle 5 : tu n'écris QU'UN seul fichier, `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-3.json`.
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
- Fichier à écrire (nom EXACT) : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-3.json`
- Champs à écrire : `"niveau": "releveur"`, `"nom": "B2-3"`, `"modele_demande": "haiku"`, `"effort_demande": "xhigh"`.

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
  "nom": "B2-3",
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

## TON SOUS-LOT B2-3 — 22 codes (conduits et filage, percements D-12/E-07, scan de dalle X-01, 5 lots fournisseur)

Liste exacte (22), ni plus ni moins : C-05 C-06 C-07 C-08 D-13 D-14 D-15 E-08 E-09 E-10 F-08 F-09 G-02 G-03 D-12 E-07 X-01 LOT-ECL LOT-DIST LOT-JCI LOT-DET LOT-GPR
Tu n'as AUCUN autre code : luminaires, enseignes (B2-1) ; haut-parleur, alarme, moteurs, distribution B-0x, nacelle X-02 (B2-2) — ne les écris pas. Tout ton sous-lot est HORS relevé (feuille Détail d'Estimation_2, codes X-0n, lots) : pas de mention « précaution ».

### Contexte du chef (consignes et candidats du directeur B, recopiés tels quels)
Libellés candidats à examiner (valeurs à relire dans le CSV ; chercher aussi d'autres variantes). « repère » = valeur de METHODE.md qui tranche selon la règle 1.

Travaux spéciaux :
- X-01 scan de dalle (bordereau 3.32) : « SCAN DALLE BETON » (repère scan dalle 1 250 $) ; écartés « SCAN DALLE »,
  « SCAN », « SCANN DALLE », « SCAN BETON ». ATTENTION : LOT-GPR 1 250 $ (GPR = géoradar = le même scan de dalle)
  → écrire dans `doubles_comptes` {X-01, LOT-GPR} : un seul des deux est payé.
- D-12 (16 percements RDC) et E-07 (7 percements étage), carottage + coupe-feu : « PERCEMENT PLANCHER » (repère
  percement 150 $ / 1 h) ; écartés « PERCEMENT DALLE », « PERCEMENTPLANCHER », « PERCEMENT PLANCHER PC »… Le
  coupe-feu (Dupuis « COUPE FEU TUBE 10.1 FL O », Lumen TROCP25WB+10.1OZ) n'est PAS ajouté : noter.

Conduits et filage (feuille Détail, longueurs en MÈTRES ; tu chiffres AU PIED, `u` = « PI », l'équipe A convertit
la longueur, 1 m = 3,2808 pi) — consigne spéciale à transmettre mot pour mot au releveur concerné :
« Dupuis chiffre un conduit par ASSEMBLAGE au pied : « CONDUIT <diamètre> <nn>C<calibre> » = conduit + nn
conducteurs du calibre (ex. « CONDUIT 3/4 03C12 », repère 4,24 $/pi et 0,113 h/pi → valeurs exactes du CSV) ;
un conduit sans fil = « CONDUIT VIDE <diamètre> » (repère « CONDUIT VIDE 3/4 » 1,41 $/pi, 0,056 h/pi). Quand
l'assemblage retenu pour le code du conduit contient déjà les conducteurs, le code du fil correspondant reçoit
p = 0 et h = 0 avec `src` « inclus dans l'assemblage « … » du code <code conduit> » ; l'option « conduit vide + fil au pied » (libellés Dupuis de fil, ex. « 12AWG SOLIDE RW90 600V », « 8AWG 7 BRINS RW90 600V ») va en note
avec ses valeurs. »
- C-05 EMT 1″ UTA-01 (35 m) + C-06 RW90 #8 (140 m = 4 × 35, 3 + MALT) : « CONDUIT 1 04C08 » (4 × #8 = même
  objet) vs « CONDUIT 1 03C08 » ; C-06 = 0 inclus.
- C-07 EMT 3/4″ VE-02N + HUM (80 m = 35 m à 4 #12 + 3 × 15 m à 3 #12) + C-08 RW90 #12 (275 m) : « CONDUIT 3/4 04C12 » vs « CONDUIT 3/4 03C12 » (un seul libellé par code : choisir et noter l'autre) ; C-08 = 0 inclus.
- D-13 EMT 1″ sous dalle (480 m, 16 courses, 5 conducteurs #12 par course) + D-15 RW90 #12 (2 400 m) et E-08
  EMT 1″ étage (175 m) + E-10 RW90 #12 (875 m) : aucun « CONDUIT 1 05C12 » connu → arbitrer entre « CONDUIT 3/4 05C12 » (bon nombre de conducteurs, diamètre 3/4), « CONDUIT 3/4 03C12 » (repère) et « CONDUIT VIDE 1 » + fil au
  pied ; même choix pour D-13 et E-08 ; D-15 et E-10 = 0 si l'assemblage inclut le fil.
- D-14 (330 m) et E-09 (175 m) EMT 3/4″ data sous dalle (vides) : « CONDUIT VIDE 3/4 ».
- F-08 EMT 3/4″ + flexible, raccordement luminaires (280 m) + F-09 RW90 #12 éclairage 3 conducteurs (840 m =
  3 × 280) : « CONDUIT 3/4 03C12 » (repère, 3 × #12 = même objet) ; F-09 = 0 inclus.
- G-02 EMT 3/4″ boucle AI (30 m) : « CONDUIT VIDE 3/4 » ; G-03 câble AI FT4 2c #16 (60 m) : pas d'assemblage →
  ligne de conducteur au pied, candidats « COND ALARME 3/16 FT4 » (nb_projets 16), « 16AWG 1PR PVC FT4 600V »,
  « 16AWG 3C PVC FT4 600V G » — arbitrer et noter.
- Les conduits, fils et accessoires de la feuille `Matériel Lumen` (CONEMT1, CONEMT3/4, APPTW…, CAB12/…, CAB8…,
  GRE430…) ne servent PAS quand Dupuis a l'assemblage : noter « vérifié, non utilisé ».

Lots fournisseur (METHODE.md §2) : sortir `"lots": {"LOT-ECL": 11893, "LOT-DIST": 6200, "LOT-JCI": 7400,
"LOT-DET": 600, "LOT-GPR": 1250}` ET 5 lignes `LOT-ECL`, `LOT-DIST`, `LOT-JCI`, `LOT-DET`, `LOT-GPR` (`u` = « LOT »,
`p` = montant, `h` = 0, `src` = « METHODE.md §2, prix confirmé par Francis le 2026-10-20 ») pour la jointure avec
l'équipe A — en note : « même montant que le dict lots, à ne compter qu'une fois ». Recalcule LOT-ECL depuis sa
décomposition (A1 × 11 à 185 $, SL1 4′ × 12 à 290 $, 3′ × 15 à 230 $, 1′ × 6 à 110 $, trousses 1 500 $, E × 3 à
475 $, Z6 × 3 à 161,60 $) : la somme vaut 13 034,80 $ et non 11 893 $ — garder 11 893 $ (total confirmé) et noter
l'écart de 1 141,80 $. Vérifie aussi LOT-DIST (3 400 + 1 900 + 900 = 6 200 $).

Doubles comptes : le chef de lot B3 les traite pour tout le lot B, mais écris dans `doubles_comptes` ceux que tu
vois (au minimum : X-01/LOT-GPR ; chaque fil inclus dans un assemblage C-05/C-06, C-07/C-08, D-13/D-15, E-08/E-10,
F-08/F-09 ; PA-I/PA-R avec Détail G-04 ; X-02 avec H-01 ; Lumen conduits/fils/boîtes contre assemblages Dupuis).

### DÉCISIONS DU CHEF DE LOT B2 (à appliquer ; vérifiées dans le CSV par le chef le 2026-10-21, que tu relis toi-même)

**Principe conduits.** `u` = « PI » pour tout conduit et tout fil (um = P dans le catalogue) ; l'équipe A convertit les mètres du Détail en pieds
(1 m = 3,2808 pi) : tu ne convertis RIEN et tu ne mets AUCUNE quantité. Un code de fil dont l'assemblage retenu pour son conduit contient déjà les conducteurs
= ligne « inclus » (p = 0.0, h = 0.0, `src` « inclus dans l'assemblage « … » du code <code conduit> », fonction `inclus()`).

**1. Assemblages retenus.**
- C-05 → « CONDUIT 1 04C08 » (6,1399 $/pi / 0,098 h/pi : 4 × #8 dans 1″ = MÊME objet que C-05 + C-06 ; règle 2). C-06 = inclus dans C-05. Note l'autre : 'CONDUIT 1 03C08' [um=P ; p=6.5707 h=0.091 nb=3 2026-10-07] (plus de projets, 3 conducteurs seulement) ;
  note la bizarrerie « 04C08 moins cher que 03C08 » (données Dupuis, on n'y touche pas) ; option décomposée : « CONDUIT VIDE 1 » + 4 × « 8AWG 7 BRINS RW90 600V » — ATTENTION : deux libellés quasi identiques existent
  (« 8AWG 7 BRINS RW90 600V » sans espace finale, 1,0625 $ / 0,007 h, nb 1, et « 8AWG 7 BRINS RW90 600V » AVEC espace finale, 0,9181 $ / 0,007 h, nb 3) : cite celui à nb_projets 3 (règle 3) en copiant son libellé par `repr`.
- C-07 + C-08 (80 m dont 35 m à 4 #12 et 45 m à 3 #12) → « CONDUIT 3/4 03C12 » (repère 4,2441 $/pi / 0,1128 h/pi, nb_projets 20 ; la majorité de la longueur est à 3 conducteurs). C-08 = inclus dans C-07.
  Note 'CONDUIT 3/4 04C12' [um=P ; p=2.8997 h=0.076 nb=5 2026-09-25] (4 conducteurs, 35 m seulement) et l'option « CONDUIT VIDE 3/4 » + fil #12 au pied.
- F-08 + F-09 → « CONDUIT 3/4 03C12 » (repère, 3 × #12 = MÊME objet que F-08 + F-09). F-09 = inclus dans F-08.
- D-13 + D-15 et E-08 + E-10 (EMT 1″, 5 conducteurs #12 par course) : AUCUN « CONDUIT 1 05C12 » dans le catalogue. DÉCISION (la même pour D-13 et E-08) : « CONDUIT 3/4 03C12 » (repère METHODE, règle 1).
  Justification à écrire en note, avec les chiffres : c'est l'assemblage dont le prix/pi est le plus proche de l'option « physique » décomposée « CONDUIT VIDE 1 » + 5 × « 12AWG SOLIDE RW90 600V » = 4.3787 $/pi et 0.095 h/pi
  (4,2441 contre 4.3787 : écart -3.1 %) ; « CONDUIT 3/4 05C12 » (bon nombre de conducteurs, mais diamètre 3/4 : 3.4197 $/pi, 0.081 h/pi) sous-évalue le conduit 1″ ; « CONDUIT 1 11C12 » (bon diamètre, mais 11 conducteurs : 6.1407 $/pi, 0.125 h/pi) le surévalue.
  D-15 et E-10 = inclus (dans D-13 et E-08 respectivement).
  Impact à écrire en note (ordre de grandeur sur les longueurs du Détail : D-13 480 m = 1574.8 pi, E-08 175 m = 574.1 pi, total 2148.9 pi ; l'équipe A fixera les vraies quantités) :
  « CONDUIT 3/4 05C12 » donnerait -1772 $ et -68.3 h ; « CONDUIT 1 11C12 » +4076 $ et +26.2 h ; la décomposition « VIDE 1 + 5 × fil » +289 $ et -38.3 h (par rapport à l'option retenue 03C12). Calcule-les toi-même avec les valeurs relues.
- D-14, E-09 et G-02 (conduits vides EMT 3/4″) → « CONDUIT VIDE 3/4 » (repère 1,4097 $/pi / 0,056 h/pi, nb_projets 12). Note 'CONDUIT VIDE 1' [um=P ; p=2.4307 h=0.07 nb=3 2026-06-02] (EMT 1″ vide, pour mémoire).
- G-03 (câble d'alarme incendie FT4 2 conducteurs #16, 60 m) : pas d'assemblage → ligne de conducteur au pied. DÉCISION (règle 2, même objet : 1 paire = 2 conducteurs #16 FT4) :
  « 16AWG 1PR PVC FT4 600V » — ATTENTION : ce libellé a une ESPACE FINALE dans le CSV, copie-le par `repr` ('16AWG 1PR PVC FT4 600V ') ; 0,4299 $/pi / 0,004 h/pi, nb 1.
  Note les autres avec leurs valeurs et l'impact sur 60 m = 196,85 pi : 'COND ALARME 3/16 FT4' [um=P ; p=1.5887 h=0.054 nb=16 2026-10-07] (le plus utilisé, mais « 3/16 » = 3 conducteurs #16 et temps 13 fois plus élevé : environ +228 $ et +9,8 h ; calcule),
  '16AWG 3C PVC FT4 600V G' [um=P ; p=0.6803 h=0.008 nb=1 2026-03-31]. Lumen « CAB16/2FAFT4300 » (1,344 $/m = 0,41 $/pi) confirme l'ordre de grandeur de 0,4299 $/pi : note-le (vérifié, non utilisé).

**2. Percements D-12 et E-07.** « PERCEMENT PLANCHER » (150 $ / 1,0 h, nb_projets 8, 2026-10-07 ; repère percement 150 $ / 1 h), `u` = U. Écartés à noter : « PERCEMENT DALLE » (75 $ / 2,0 h), « PERCEMENTPLANCHER » (75 $ / 1,0 h),
« PERCEMENT PLANCHER PC » (75 $ / 1,0 h, nb 3). Le coupe-feu (Dupuis « COUPE FEU TUBE 10.1 FL O » ; Lumen TROCP25WB+10.1OZ) n'est PAS ajouté : note-le avec les valeurs relues.

**3. Scan de dalle X-01.** « SCAN DALLE BETON » (1 250 $ / 2,0 h, nb 2 ; repère scan dalle 1 250 $), `u` = U. Écartés à noter : « SCAN DALLE » (750 $ / 1,0 h), « SCAN » (750 $ / 4,0 h), « SCANN DALLE » (950 $ / 8,0 h), « SCAN BETON » (750 $ / 4,0 h).
`doubles_comptes` : {X-01, LOT-GPR} : un seul des deux est payé (LOT-GPR 1 250 $ = géoradar = le même scan de dalle).

**4. Lots fournisseur** : exactement comme dans le texte du directeur recopié plus haut (dict `"lots"` ET 5 lignes, `u` = « LOT », `p` = montant, `h` = 0, `src` = « METHODE.md §2, prix confirmé par Francis le 2026-10-20 », fonction `lot()`).
`art` : LOT-ECL « 3.35 », LOT-DIST « 3.24 », LOT-JCI « 3.38 », LOT-DET « 3.36 », LOT-GPR « 3.32 ». Notes obligatoires : « même montant que le dict lots, à ne compter qu'une fois » ; LOT-ECL : recalcul de la décomposition
(A1 × 11 à 185 + 12 × 290 + 15 × 230 + 6 × 110 + 1 500 + 3 × 475 + 3 × 161,60 = 13 034,80 $, contre 11 893 $ confirmé, écart 1 141,80 $ — garder 11 893 $) ; LOT-DIST : 3 400 + 20 × 95 + 3 × 300 = 6 200 $ (vérifié) et sa ventilation
d'article (panneau 3 400 $ → 3.24 ; disjoncteurs 1 900 + 900 = 2 800 $ → 3.25 ; la ligne porte « 3.24 », la ventilation est à la charge du chef B3) ; LOT-DET = 2 détecteurs (DF-I, AI-01) ; LOT-JCI = 7 400 $ (bypass, programmation, annonciateur AI-05, vérification ULC-S537).

**5. Lumen : contrôle « vérifié, non utilisé ».** Ouvre la feuille `Matériel Lumen` et écris en note, pour chaque code Lumen suivant, « vérifié, non utilisé (Dupuis a l'assemblage) » avec son prix : CONEMT1, CONEMT3/4, APPTWC100S, APPTWC75S, APPTW100S, APPTW75S, APPTWCL100,
APPTWCL75, CONCONSEAL3/4, THO5333, THOABRH03830, IBE2210, GRE430, boîtes IBE52151K / IBE52C13 / IBE72171K / IBE72C1 / IBE54151L, fils CAB12/1RW90BLK300 / WHI300 / GRE300 / ROUGE, CAB8RW90BLK, CAB8RW90GRE, CAB12TECK3C600V, IBETEK75120, CAB16/2FAFT4300,
coupe-feu TROCP25WB+10.1OZ. AUCUNE ligne de ton JSON ne cite Lumen sauf si tu constates qu'un code n'a vraiment aucun libellé Dupuis (cas non attendu : dis-le alors en note).

### Tableau des décisions (une ligne par code de matériel/travaux — 17 lignes ; + les 5 lots)
| code | desc suggérée | libellé retenu (copie exacte, repr Python) | um | valeurs vues par le chef (à relire) | u | art | lot | portée au relevé |
|---|---|---|---|---|---|---|---|---|
| C-05 | Conduit EMT 1" alimentation UTA-01 (assemblage avec 4 #8) | 'CONDUIT 1 04C08' | P | p=6.1399 h=0.098 nb=1 2026-03-31 | PI | 3.31 | — | hors relevé (Détail C-05, 35 m) |
| C-06 | Conducteur RW90 #8 UTA-01 (inclus dans C-05) | (inclus — voir règle fil inclus) | — | p=0 h=0 | PI | 3.31 | — | hors relevé (Détail C-06, 140 m) |
| C-07 | Conduit EMT 3/4" VE-02N + HUM (assemblage avec fil #12) | 'CONDUIT 3/4 03C12' | P | p=4.2441 h=0.1128 nb=20 2026-09-25 | PI | 3.31 | — | hors relevé (Détail C-07, 80 m) |
| C-08 | Conducteur RW90 #12 VE-02N + HUM (inclus dans C-07) | (inclus — voir règle fil inclus) | — | p=0 h=0 | PI | 3.31 | — | hors relevé (Détail C-08, 275 m) |
| D-13 | Conduit EMT 1" sous dalle RDC, 5 #12 par course (assemblage) | 'CONDUIT 3/4 03C12' | P | p=4.2441 h=0.1128 nb=20 2026-09-25 | PI | 3.31 | — | hors relevé (Détail D-13, 480 m) |
| D-14 | Conduit EMT 3/4" data sous dalle RDC (vide) | 'CONDUIT VIDE 3/4' | P | p=1.4097 h=0.056 nb=12 2026-08-19 | PI | 3.31 | — | hors relevé (Détail D-14, 330 m) |
| D-15 | Conducteur RW90 #12 sous dalle RDC (inclus dans D-13) | (inclus — voir règle fil inclus) | — | p=0 h=0 | PI | 3.31 | — | hors relevé (Détail D-15, 2 400 m) |
| E-08 | Conduit EMT 1" sous dalle étage, 5 #12 par course (assemblage) | 'CONDUIT 3/4 03C12' | P | p=4.2441 h=0.1128 nb=20 2026-09-25 | PI | 3.31 | — | hors relevé (Détail E-08, 175 m) |
| E-09 | Conduit EMT 3/4" data sous dalle étage (vide) | 'CONDUIT VIDE 3/4' | P | p=1.4097 h=0.056 nb=12 2026-08-19 | PI | 3.31 | — | hors relevé (Détail E-09, 175 m) |
| E-10 | Conducteur RW90 #12 étage (inclus dans E-08) | (inclus — voir règle fil inclus) | — | p=0 h=0 | PI | 3.31 | — | hors relevé (Détail E-10, 875 m) |
| F-08 | Conduit EMT 3/4" + flexible, raccordement luminaires (assemblage 3 #12) | 'CONDUIT 3/4 03C12' | P | p=4.2441 h=0.1128 nb=20 2026-09-25 | PI | 3.31 | — | hors relevé (Détail F-08, 280 m) |
| F-09 | Conducteur RW90 #12 éclairage 3 cond. (inclus dans F-08) | (inclus — voir règle fil inclus) | — | p=0 h=0 | PI | 3.31 | — | hors relevé (Détail F-09, 840 m) |
| G-02 | Conduit EMT 3/4" boucle alarme incendie (vide) | 'CONDUIT VIDE 3/4' | P | p=1.4097 h=0.056 nb=12 2026-08-19 | PI | 3.31 | — | hors relevé (Détail G-02, 30 m) |
| G-03 | Câble alarme incendie FT4 2c #16 (boucle adressable) | '16AWG 1PR PVC FT4 600V ' | P | p=0.4299 h=0.004 nb=1 2026-04-02 | PI | 3.31 | — | hors relevé (Détail G-03, 60 m) |
| D-12 | Percement de dalle carotté RDC (16 percements) | 'PERCEMENT PLANCHER' | U | p=150.0 h=1.0 nb=8 2026-10-07 | U | 3.31 | — | hors relevé (Détail D-12) |
| E-07 | Percement de dalle carotté étage (7 percements) | 'PERCEMENT PLANCHER' | U | p=150.0 h=1.0 nb=8 2026-10-07 | U | 3.31 | — | hors relevé (Détail E-07) |
| X-01 | Scan de dalle béton (géoradar) | 'SCAN DALLE BETON' | U | p=1250.0 h=2.0 nb=2 2026-03-09 | U | 3.32 | — | hors relevé (code X-01) |

Les 5 lignes de lots : LOT-ECL (11 893, art « 3.35 »), LOT-DIST (6 200, « 3.24 »), LOT-JCI (7 400, « 3.38 »), LOT-DET (600, « 3.36 »), LOT-GPR (1 250, « 3.32 ») — `u` = « LOT », `h` = 0, via `lot()`.
Au total 22 lignes. Les 5 lignes « inclus » (C-06, C-08, D-15, E-10, F-09) : `inclus(code, desc, libelle_du_conduit, code_du_conduit)` avec le libellé EXACT de l'assemblage cité.

### Notes et doubles comptes à écrire (obligatoires)
- Rappel (en note) : taux 85 $/h (METHODE.md §5 ; le 124 $/h du Sommaire n'est pas retenu) et facteur de prix de vente
  1,244 — à rappeler, à ne PAS appliquer.
- Chaque candidat écarté : libellé exact, p, h, nb_projets, date_dernier, et la raison de l'écart (règle 1, 2, 3 ou 4).
- Tout écart entre les valeurs que le chef a vues et ce que tu relis dans le CSV, ou tout libellé décidé par le chef
  que tu ne retrouves pas : ne devine pas, applique les règles de choix du kit et décris l'écart dans une note.
- Tout désaccord argumenté avec une décision du chef : applique la décision, écris ton désaccord en note (une note par
  désaccord, avec les chiffres). Le chef tranchera à sa relance.
- `notes` : la décision 1 complète, assemblage par assemblage (retenu, écartés avec valeurs, impact), y compris « aucun CONDUIT 1 05C12 dans le catalogue » ; G-03 : l'arbitrage avec les trois candidats.
- `notes` : décisions 2 à 5 (percements, scan, lots, Lumen « vérifié, non utilisé »).
- `doubles_comptes` (au minimum, un objet par entrée) :
  - {"codes": ["X-01","LOT-GPR"], "regle": "scan de dalle = géoradar : un seul des deux est payé"} ;
  - {"codes": ["C-05","C-06"], "regle": "fil inclus dans l'assemblage CONDUIT 1 04C08 : C-06 à 0 $ / 0 h"} ;
  - {"codes": ["C-07","C-08"], "regle": "fil inclus dans l'assemblage CONDUIT 3/4 03C12 : C-08 à 0 $ / 0 h"} ;
  - {"codes": ["D-13","D-15"], "regle": "fil inclus dans l'assemblage CONDUIT 3/4 03C12 : D-15 à 0 $ / 0 h"} ;
  - {"codes": ["E-08","E-10"], "regle": "fil inclus dans l'assemblage CONDUIT 3/4 03C12 : E-10 à 0 $ / 0 h"} ;
  - {"codes": ["F-08","F-09"], "regle": "fil inclus dans l'assemblage CONDUIT 3/4 03C12 : F-09 à 0 $ / 0 h"} ;
  - {"codes": ["C-05","C-07","D-13","D-14","E-08","E-09","F-08","G-02","G-03"], "regle": "conduits/fils/boîtes de la feuille Matériel Lumen (CONEMT…, CAB12…, IBE…) contre assemblages Dupuis (boîte, plaque et raccord inclus) : Lumen vérifié, non utilisé"} ;
  - {"codes": ["D-12","E-07"], "regle": "le percement Dupuis (150 $ / 1 h) ne reçoit pas le coupe-feu en plus (Dupuis COUPE FEU TUBE 10.1 FL O / Lumen TROCP25WB+10.1OZ non ajoutés)"} ;
  - {"codes": ["LOT-DIST","B-01","B-02","B-03","B-04","B-05","B-06","B-07","B-08"], "regle": "le lot distribution paie le panneau et les disjoncteurs ; les lignes B-0x sont à p = 0 (codes de B2-2)"}.

### Aide de code (à adapter ; tu peux t'en servir telle quelle)
```python
import csv, json, re
CAT = '/home/claude/entrainement/S-1902/swarm-2/catalogue-prix-temps-dupuis.csv'
OUT = '/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-3.json'
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

def inclus(code, desc, libelle, code_conduit, art="3.31"):
    """Fil compris dans l'assemblage du conduit : p = 0 et h = 0."""
    return {"code": code, "desc": desc, "q": None, "u": "PI", "p": 0.0, "h": 0.0, "art": art,
            "src": "inclus dans l'assemblage « %s » du code %s" % (libelle, code_conduit)}

def lot(code, desc, montant, art):
    return {"code": code, "desc": desc, "q": None, "u": "LOT", "p": montant, "h": 0, "art": art,
            "src": "METHODE.md §2, prix confirmé par Francis le 2026-10-20"}

# ... tu construis `lignes = [L(...), ...]`, `notes = [...]`, `doubles = [...]`, tu appelles verifier(lignes, ATTENDUS), puis :
obj = {"niveau": "releveur", "nom": "B2-3", "modele_demande": "haiku", "effort_demande": "xhigh",
       "lignes": lignes, "notes": notes, "doubles_comptes": doubles,
       "lots": {"LOT-ECL": 11893, "LOT-DIST": 6200, "LOT-JCI": 7400, "LOT-DET": 600, "LOT-GPR": 1250}}
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
4. Écris le JSON (`json.dump(obj, f, ensure_ascii=False, indent=2)`), recharge-le, vérifie : tes 22 codes, une seule
   fois chacun, `q` = null partout, `lignes` + `notes` présents, aucun autre code que les tiens.
5. Réponds en UNE ligne : « fichier écrit : /home/claude/entrainement/S-1902/swarm-2/lots/releveur-B2-3.json — 22 lignes »
   et ARRÊTE-TOI (tu ne fais rien d'autre, tu n'écris aucun autre fichier).
