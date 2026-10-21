effort: xhigh
modele: sonnet

# Chef de lot B3 — BORDEREAU, DOUBLES COMPTES et TRAVAUX HORS PLAN DIVERS : prix, temps et articles « méthode Dupuis » (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le chef de lot B3, modèle Claude Sonnet 5.5, d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton supérieur est le directeur B (Claude Opus 5.5), lui-même sous le chef de l'essaim (Claude
Fable 5.1). Tu as sous tes ordres EXACTEMENT 3 releveurs, modèle « haiku » (releveurs B3-1, B3-2, B3-3).
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la
médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités sont la mission de l'équipe A :
`q` reste `null` partout.

Ton lot B3 a trois livrables :
1. ARTICLES DU BORDEREAU — l'article définitif (3.22 … 3.38, 5.11, 5.19, 6.1) de CHACUN des 141 codes du lot B
   (liste exacte plus bas), avec des règles d'affectation écrites. Les chefs B1 et B2 posent un article provisoire ;
   c'est ta table qui fait foi pour le directeur B.
2. DOUBLES COMPTES — la liste complète des doubles comptes possibles entre le relevé sur plan, la feuille Détail,
   la feuille Matériel Lumen, les assemblages Dupuis et les lots fournisseur, chacun avec la règle à appliquer
   (« le plan gagne ; un objet physique n'est payé qu'une fois »).
3. PRIX ET TEMPS des 21 codes hors plan « divers » qui ne sont ni dans B1 ni dans B2 : A-07, A-08, A-09, A-10,
   A-11, C-01, C-02, C-03, C-04, D-16, E-11, F-05, F-10, G-04, G-05, G-06, G-07, H-01, H-02, H-03, H-04.

Effort `xhigh` choisi pour toi par le directeur B : un double compte non vu (ou un objet payé deux fois entre une
ligne Détail, une ligne sur plan, un assemblage Dupuis et un lot fournisseur) déplace tout le total, et ces
21 lignes hors plan sont presque toutes des « jugements » à arbitrer contre le catalogue ; la ventilation par
article (`par_article`) du chiffrage final dépend entièrement de ta table.

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

## Dossier de travail
`/home/claude/entrainement/S-1902/swarm-2/` — tu y travailles uniquement (chemins absolus conseillés). Tu n'écris
que dans `lots/` et `prompts/`. Tu n'as pas besoin des fichiers de l'équipe A.

## Mécanique de relais (tu ne lances personne)
1. Tu n'as pas l'outil Agent et tu ne lances aucun agent (ni outil, ni `claude -p`, ni script). Tu as le droit de
   briefer EXACTEMENT 3 subalternes, modèle haiku : les releveurs B3-1, B3-2 et B3-3.
2. PHASE 1 (maintenant) : tu lis le kit, tu découpes ton lot en 3 sous-lots DISJOINTS (aucune tâche ni aucun code
   dans deux sous-lots) et COUVRANTS (les 3 livrables et tous les codes attribués), puis tu écris les 3 prompts de
   tes releveurs dans le dossier `prompts/directeur-B/chef-3/` (à créer) : `prompts/directeur-B/chef-3/releveur-1.md`,
   `prompts/directeur-B/chef-3/releveur-2.md`, `prompts/directeur-B/chef-3/releveur-3.md`. Chaque fichier commence
   EXACTEMENT par deux lignes — `effort: <low|medium|high|xhigh|max>` puis `modele: haiku` — suivies du prompt
   complet et autonome. Le releveur B3-m écrit `lots/releveur-B3-m.json` (m = 1, 2, 3).
3. Chaque prompt de releveur DOIT contenir, MOT POUR MOT : les RÈGLES D'AVEUGLE ci-dessus ET le bloc « MÉCANIQUE DE RELAIS » ci-dessous (tu recopies ces mêmes règles et cette même mécanique). Il DOIT aussi contenir : son rôle
   et son nom (« releveur B3-1 »…), le dossier de travail, sa tâche exacte (codes, articles, doubles comptes) avec
   les données utiles ci-dessous, les sections « Le kit », « Règles de prix et de temps », « Nomenclature »,
   « Format de src, u et art », « Format JSON » et « Vérifications » ci-dessous (recopiées ou adaptées sans rien
   perdre), les clés JSON supplémentaires de son sous-lot (`articles`, `regles_articles`, `doubles_comptes`), le nom
   EXACT du fichier à écrire, et l'ordre de s'arrêter après l'avoir écrit et vérifié. Les releveurs ne voient ni
   ce prompt ni ton contexte : chaque brief doit se suffire à lui-même.
4. Après avoir écrit tes 3 prompts et vérifié leurs deux premières lignes (`head -2`), tu T'ARRÊTES : tu ne fais
   pas le travail des releveurs et tu n'écris pas `lots/chef-B3.json`. Tu réponds seulement « prompts prêts », avec
   l'effort choisi pour chaque releveur et sa justification d'une ligne.
5. La session principale lance tes 3 releveurs tels quels. PHASE 2 : tu es relancé avec ce même prompt et la
   mention « tes releveurs ont fini » → section « À ta relance » plus bas.

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

## Première chose à faire
Lis dans cet ordre : `CONSIGNES.md`, `METHODE.md`, `ARCHITECTURE.md` (§2 kit, §3 nomenclature, §4 découpage et
liste des lignes Détail à exclure, §5 format JSON, §6 vérification, §7 prompts/effort — la loi de l'essaim),
`rapport-releve.md`, `reserves.md`. Puis ouvre `entree/reference-Bordereau_de_prix.xlsx` (articles 3.22 à 3.38,
5.11, 5.19, 6.1, 6.2), TOUTE la feuille `Détail` et TOUTE la feuille `Matériel Lumen` d'Estimation_2, les deux
relevés `entree/reference-Releve_Alarme_Incendie.xlsx` et `entree/reference-Releve_Eclairage_Urgence.xlsx`,
`releve.xlsx` (feuille `Par libellé`) et le catalogue (code ci-dessous).

## Le kit — comment lire chaque fichier (à transmettre tel quel à tes releveurs)
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
   Lecture type (à recopier dans chaque prompt de releveur) :
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

## Règles de prix et de temps (à transmettre tel quel)
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

## Format JSON (ARCHITECTURE.md §5) — releveurs et chefs de lot (exemple : adapter niveau, nom, effort)
```json
{
  "niveau": "releveur",
  "nom": "B1-2",
  "modele_demande": "haiku",
  "effort_demande": "high",
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

## Livrable 1 — articles du bordereau (les 141 codes du lot B)
Articles électriques du bordereau (libellés exacts du fichier) : 3.22 Démontage des éléments électriques ·
3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V · 3.25 Lot disjoncteurs · 3.26 MCC ·
3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles 15A-120V MALT isolées ·
3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction · 3.32 Scan dalle béton ·
3.33 Sorties informatique/réseau · 3.34 Moinument plancher · 3.35 Appareil de contrôle + appareils d'éclairage ·
3.36 Détecteur de fumée · 3.37 Panneau alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie :
mise en marche et certification ; ailleurs : 5.11 Percement du plancher · 5.19 Démolition des systèmes
électriques · 6.1 Conditions de mise en œuvre et autres · 6.2 Frais généraux, administration et profit.

Codes du chef B1 (44) : PC-I PC-E PC-R PU-I PU-E PU-R PG-I PG-E PG-R SD-I SD-E SD-R TV-I TV-E TV-R INT-I INT-E
INT-R TH-I TH-E TH-R BJ-I BJ-E BJ-R MP-I MP-E MP-R LC-I LC-E LC-R GA-I GA-E GA-R DM-I DM-E DM-R BC-I BC-E BC-R
D-09 D-10 D-11 E-03 E-06.
Codes du chef B2 (76) : ENC-I ENC-E ENC-R ENCU-I ENCU-E ENCU-R L14-I L14-E L14-R L22-I L22-E L22-R L4-I L4-E L4-R
LLIN-I LLIN-E LLIN-R HP-I HP-E HP-R LA1-I LC1-I LC11-I LC13-I LE-I Z6-I Z6-E Z6-R DF-I DF-E DF-R SM-I SM-E SM-R
PA-I PA-E PA-R MM-I MM-E MM-R MT-I MT-E MT-R B-01 B-02 B-03 B-04 B-05 B-06 B-07 B-08 B-09 X-01 X-02 D-12 E-07
C-05 C-06 C-07 C-08 D-13 D-14 D-15 E-08 E-09 E-10 F-08 F-09 G-02 G-03 LOT-ECL LOT-DIST LOT-JCI LOT-DET LOT-GPR.
Tes codes (21) : A-07 A-08 A-09 A-10 A-11 C-01 C-02 C-03 C-04 D-16 E-11 F-05 F-10 G-04 G-05 G-06 G-07 H-01 H-02
H-03 H-04.
(Familles : voir « Nomenclature » ; descriptions des codes Détail : feuille `Détail` ; X-01 = scan de dalle,
X-02 = nacelle ; LOT-ECL = luminaires neufs + Z6 + trousses, LOT-DIST = panneau NF 3 400 $ + disjoncteurs EDB/EJB
2 800 $, LOT-JCI = services JCI/Simplex (bypass, programmation, vérification S537, certificat), LOT-DET = 2
détecteurs de fumée, LOT-GPR = scan de dalle par géoradar.)

Décisions à trancher et à écrire en règles (`regles_articles`), en partant de la règle provisoire de la section
« Format de src, u et art » :
- ENLEVER : 3.22 ou 5.19 (les deux parlent de démolition électrique ; 3.22 est dans la section Électricité, 5.19
  dans « Démantèlement d'élément de bâtiment ») — une seule règle, et dire ce que reçoit l'autre article.
- RELOCALISER : 3.22 (dépose) ou l'article de la famille (repose) — une seule règle, avec ses exceptions
  (PA → 3.37 « déplacement annonciateur » ; moteurs/équipements au toit → 3.23).
- Percements D-12/E-07 : 3.31 ou 5.11 « Percement du plancher ».
- Conduits/filage des raccordements mécaniques (C-05…C-08) : 3.23 ou 3.31 ; C-03 (tiroirs CCM-1 des chaudières) :
  3.23 ou 3.26 « MCC ».
- LOT-DIST : un seul `art` par code, mais écrire la règle de ventilation (3 400 $ → 3.24, 2 800 $ → 3.25).
- Familles sans article évident : TV, LC, GA, TH, BC, DM, INT, HP ; la famille PG contient aussi des prises M.A.L.T.
  isolées (reserves.md R-007, article 3.29) — dire comment on les ventile ou pourquoi on ne le peut pas.
- 6.1 (frais de chantier : H-01…H-04, X-02, A-11 ?) ; 6.2 reçoit 0 $ (administration et profit = 0 % chez Dupuis,
  la marge est dans le prix vendant — METHODE.md §2, point 1).
- 3.38 (LOT-JCI, G-06, G-07) ; 3.36 (DF, SM, LOT-DET, G-02, G-03, G-05 ?) ; 3.37 (PA, G-04).

## Livrable 2 — doubles comptes (liste de départ, à VÉRIFIER sur les fichiers et à COMPLÉTER)
Pour chacun : les codes en cause, les quantités de part et d'autre quand elles sont lisibles (relevé : tableau de
rapport-releve.md ; Détail : colonne Qté), et la règle (« le plan gagne », « payé une fois par … », « 0 $ en ligne + lot », « inclus dans l'assemblage »). Les lignes Détail exclues ne reçoivent ni p ni h : elles sont remplacées
par le code sur plan, tu les listes ici.
- Lignes Détail qui recomptent le plan (ARCHITECTURE.md §4) : A-01, A-02 (démantèlement luminaires E.A.E 39 + 7)
  ↔ ENC-E, L14-E, L22-E ; A-03, A-04 (démantèlement services E.A.E 34 + 10) ↔ PC-E, PG-E, SD-E, INT-E, BJ-E, MP-E,
  DM-E, BC-E, DF-E, HP-E ; A-05 (relocalisation services E.A.R 13) ↔ PC-R, PG-R, SD-R, DF-R ; A-06 (relocalisation
  luminaires 7) ↔ ENC-R ; D-01…D-08, E-01, E-02, E-04, E-05 ↔ PC-I, PU-I, PG-I, SD-I, MP-I, BJ-I ; F-01…F-04, F-06,
  F-07 ↔ LA1-I, LC1-I, LC11-I, LC13-I, LE-I, Z6-I (LE : relevé 3, F-06 = 4, lot = 3) ; G-01 ↔ DF-I.
- Même objet, deux lignes chiffrées : G-04 ↔ PA-I/PA-R (relocalisation de l'annonciateur) ; G-07 ↔ LOT-JCI ;
  X-01 « SCAN DALLE BETON » 1 250 $ ↔ LOT-GPR 1 250 $ (GPR = géoradar = scan de dalle) ; H-01 (plateforme /
  échafaudage roulant) ↔ X-02 nacelle ; C-01, C-02, C-03, C-04 (raccordements UTA-01, VE-02N, chaudières, HUM) ↔
  MT-I (4), MM-I (3) ; A-10 (toit, 6 E.A.R) ↔ MM-R (6) ; A-07 ↔ INT-R/INT-E ; A-08, A-09 (FabLab, retrait +
  réinstallation 21 linéaires + 24 encastrés) ↔ LLIN, ENC-R, ENC-E ; D-11, E-06 (boutons, boîte + conduit vide) ↔
  BJ-I.
- Assemblages Dupuis qui incluent déjà le fil : C-05/C-06, C-07/C-08, D-13/D-15, E-08/E-10, F-08/F-09 (fil à 0 si
  l'assemblage « CONDUIT … nnCcc » est retenu) ; C-01, C-02, C-04 décrivent aussi leur conduit et leur fil, déjà
  comptés en C-05…C-08 : le temps de ces lignes ne doit pas repayer le tirage.
- Prix d'assemblage Dupuis (boîte + plaque + raccord inclus) ↔ feuille Matériel Lumen : boîtes IBE52151K,
  IBE52C13, IBE72171K, IBE72C1, IBE54151L ; dispositifs LEV16252W, LEV16352W, LEVT5633W, LEVGFNT1W, LEV80401NW ;
  poke-through HUBS1R6PTDEHBLK (2 × 1 461,22 $) ↔ MP-I (MONUMENT PLANCHER 250 $) ; conduits, accessoires et fils
  CONEMT…, APPTW…, CAB… ↔ assemblages « CONDUIT … » ; coupe-feu TROCP25WB+ ↔ « PERCEMENT PLANCHER » ; tige filetée
  VISTF3/8 et ancrages ↔ LOT-ECL trousses (1 500 $) et F-05 ; HUBHBL1372 (sectionneurs HUM) ↔ C-04.
- Lots fournisseur ↔ lignes : LOT-ECL ↔ LA1-I…LE-I, Z6-I, F-05 (trousses de suspension) ; LOT-DIST ↔ B-01…B-05
  (et B-06…B-08 ?) ; LOT-DET ↔ DF-I ; LOT-JCI ↔ G-07, AI-03…AI-06 ; LOT-GPR ↔ X-01 — les lignes couvertes par un lot
  sont à 0 $ (temps seulement).
- Autres recouvrements de temps à juger : F-05 et F-10 ↔ temps unitaire des luminaires neufs (0,75 h) ; D-16, E-11
  (boîtes, connecteurs, supports) ↔ assemblages de conduits au pied ; A-11 ↔ B-09 ; H-03 ↔ G-06.
- Hors total : OPT-1…OPT-4 (Détail) — à noter, jamais chiffrés.

## Livrable 3 — p et h de tes 21 codes hors plan (feuille Détail : Qté, Unité, h / unité ; `u` = U ou LOT)
Le catalogue d'abord (règles 1 à 4), sinon Lumen, sinon « jugement (Estimation_2) » avec le h / unité de la ligne
elle-même ; chaque double compte identifié au livrable 2 est rappelé en note de la ligne (la ligne garde son p/h,
c'est le directeur B qui tranche). Candidats connus (non exhaustifs, valeurs à relire dans le CSV) :
- A-07 relocalisation des interrupteurs maîtres du hall (1 lot) : « RELO INT », « INTERRUPTEUR MAITRE » ; jugement A-07.
- A-08 FabLab 210, retrait temporaire + réinstallation de 21 linéaires ; A-09 idem 24 encastrés : « RELO ENCASTRE »,
  « RELO FIXTURE 30X30 », « RELO FIXTURE TYPE S7 », « ENLEVER FIXTURE … » ; jugement A-08 / A-09.
- A-10 toit, 6 équipements E.A.R : « DEBRANCHEMENT APPAREILAGE MECANIQUE », « SECTIONNEUR ENL », « SECTIONNEUR 30A 600V 3P », « MOTEUR » ; jugement A-10.
- A-11 continuité de service, traçage des circuits (1 lot) : « IDENTIFIER LES CIRCUITS EXISTANTS A », « NOTE 5 RETRACER DERIVA », « NOTE 6 RETRACER FILAGE », « DEMOLITION ALIMENTATION TEMPORAIRE CONSOMATEURS EXISTANTS » ;
  jugement A-11.
- C-01 UTA-01 : « MOTEUR UAF-1 » (repère UTA 1 h), « DEMARREUR MOTEUR UAF » ; C-02 VE-02N : « MOTEUR VE-2 120V »,
  « MOTEUR » (repère moteur 0,75 h) ; C-03 chaudières (2) : « CHAUDIERE », « CHAUDIERE ELECTRQUE 1 » ; C-04
  humidificateurs (3) avec sectionneur 30 A : « HUMIDIFICATEUR », « MOTEUR HUM », sectionneur « INTERR 30A 2P 600V CEMA1 » (même prix que Lumen HUBHBL1372), « SECTIONNEUR 30A 240V 1P » (`src` composé permis, opération écrite).
- D-16 (RDC) et E-11 (étage) boîtes de tirage/jonction, connecteurs, supports, corde de tirage (1 lot chacun) :
  libellés de boîtes Dupuis (« BOITE CARRE 2-1/8PO KO 1 », « BOITE D 8X8X4PO CEMA1 »…), Lumen IBE72171K, GRE430 ;
  jugement D-16 / E-11. Dire si le lot recouvre les assemblages au pied.
- F-05 rangées linéaires Axis, suspension + alimentation de rangée (20 rangées) et F-10 boîtes de jonction
  éclairage, chaînes de retenue, quincaillerie (1 lot) : jugement F-05 / F-10, « TIGE FILETE 3/8PO », « BOITE OCTOG 1-1/2PO KO 1 » ; matériel des trousses déjà dans LOT-ECL.
- G-04 relocalisation de l'annonciateur : mêmes candidats que PA (« RELO PANNEAU ANNONCIA » 550 $ / 8 h,
  « RELO PANN ANNOCIATEUR » 0 $ / 8 h, « PANNEAU ANNONCIATEUR ») — repère annonciateur relocalisé 8 h.
- G-05 démontage/protection/réinstallation des dispositifs AI existants (1 lot) : « RELO DETECTEUR A FUME »,
  « RELO STATION MANUEL » ; jugement G-05. G-06 assistance programmation / vérification ULC-S537 (1 lot) :
  « ALARME INCENDIE VERIFIC » (temps 0 → à écarter, noter) ; jugement G-06.
- G-07 sous-traitance JCI/Simplex : p = 0, h = 0, `src` « couvert par LOT-JCI 7 400 $ (METHODE.md §2) ».
- H-01 mobilisation, outillage, plateforme/échafaudage roulant ; H-02 coordination, dessins d'atelier, plans TQC ;
  H-03 essais, mise en service, vérification des prises existantes, étiquetage ; H-04 nettoyage, déchets (1 lot
  chacun) : jugement H-01…H-04 ; options catalogue à noter si pertinentes (« CONTENEUR 20PI », « ETUDE COORDINATION » — à juger : objet différent ?).

## Découpage et effort de tes releveurs
Tu découpes toi-même. Suggestion (que tu peux changer en restant disjoint et couvrant) : B3-1 = articles des
83 codes sur plan (39 de B1 + 44 de B2) avec la règle écrite pour chaque famille et portée ; B3-2 = p, h et `art`
des 21 codes hors plan de B3 + articles des 37 autres codes hors plan ou lots (D-09, D-10, D-11, E-03, E-06,
B-01…B-09, X-01, X-02, D-12, E-07, les 14 conduits/fils, les 5 LOT-*) ; B3-3 = les doubles comptes (livrable 2
complet). Tu choisis l'effort de chaque releveur selon la grille d'ARCHITECTURE.md §7 (`low` recopie mécanique
d'un petit tableau ; `medium` recherche simple ; `high` arbitrage entre libellés approximatifs, portées, doublons ;
`xhigh` quand une erreur se propage à tout le chiffrage, ce qui est le cas des doubles comptes ; `max` réservé à la
consolidation finale). Nos moyens ne sont pas comptés : choisis ce qui maximise la justesse. Justifie chaque choix
d'une ligne.

Clés JSON supplémentaires de ton lot (en plus de `lignes` et `notes`) :
- `"articles"` : `{"PC-I": "3.28", "PC-E": "3.22", …}` — les 141 codes, chacun une fois.
- `"regles_articles"` : `["tout code -E → 3.22 parce que …", …]`.
- `"doubles_comptes"` : `[{"codes": ["A-01", "A-02", "ENC-E", "L14-E", "L22-E"], "regle": "…", "quantites": "…"}]`.
Un releveur sans ligne chiffrée met `"lignes": []`.

## À ta relance (PHASE 2 — « tes releveurs ont fini »)
1. Ouvre `lots/releveur-B3-1.json`, `lots/releveur-B3-2.json`, `lots/releveur-B3-3.json` ; vérifie qu'ils se
   chargent ; `articles` couvre les 141 codes exactement une fois ; `lignes` couvre tes 21 codes exactement une
   fois ; tout manque = tu le fais toi-même.
2. Pour AU MOINS 5 lignes chiffrées de B3-2, rouvre le catalogue avec `ligne(desc, um)` (ou la cellule Lumen /
   Détail citée) et vérifie `p` et `h` ; pour AU MOINS 5 articles de B3-1 et B3-2, rouvre le bordereau ; pour AU
   MOINS 5 doubles comptes de B3-3, rouvre la feuille Détail / Matériel Lumen / rapport-releve.md et vérifie codes et
   quantités. Note un score x/5 par releveur dans `notes`. Une erreur trouvée = TOUT le lot de ce releveur est revu
   ligne par ligne par toi, corrections notées.
3. Contrôle de cohérence : chaque règle d'article s'applique sans exception non écrite ; aucun code sans article ;
   aucune ligne Détail exclue à la fois remplacée et chiffrée ; les doubles comptes « lot ↔ ligne » mettent bien la
   ligne à 0 $ ; les 21 lignes ont p/h justifiés et leurs doubles comptes rappelés.
4. Écris `lots/chef-B3.json` : `"niveau": "chef"`, `"nom": "B3"`, `"modele_demande": "sonnet"`,
   `"effort_demande": "xhigh"`, `"lignes"` (21 lignes, q = null), `"articles"` (141 codes), `"regles_articles"`,
   `"doubles_comptes"`, `"notes"` (découpage en 3 sous-lots avec la tâche de chacun, effort de chaque releveur +
   justification d'une ligne, scores x/5, arbitrages, rappel taux 85 $/h et facteur 1,244 non appliqués). Vérifie
   qu'il se charge (`python3 -c "import json;json.load(open('...'))"`), qu'aucun code n'y figure deux fois et que `q`
   est null partout.
5. Réponds seulement : nombre de codes chiffrés et d'articles posés, codes sans correspondance Dupuis directe (et
   leur repli), le nombre de doubles comptes et tes arbitrages en 5 lignes maximum.

Maintenant (PHASE 1) : lis, interroge le kit, découpe, écris les 3 prompts, vérifie leurs en-têtes, et
arrête-toi en répondant « prompts prêts » avec l'effort choisi pour chaque releveur et sa justification d'une ligne.
