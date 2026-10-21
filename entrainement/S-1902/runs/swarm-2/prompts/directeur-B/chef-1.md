effort: xhigh
modele: sonnet

# Chef de lot B1 — DISPOSITIFS : prix et temps « méthode Dupuis » (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le chef de lot B1, modèle Claude Sonnet 5.5, d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton supérieur est le directeur B (Claude Opus 5.5), lui-même sous le chef de l'essaim (Claude
Fable 5.1). Tu as sous tes ordres EXACTEMENT 3 releveurs, modèle « haiku » (releveurs B1-1, B1-2, B1-3).
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la
médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités sont la mission de l'équipe A :
`q` reste `null` partout.

Ton lot B1 : les DISPOSITIFS sur plan — PC, PU, PG, SD, TV, INT, TH, BJ, MP, LC, GA, DM, BC, chacun en I
(installer), E (enlever) et R (relocaliser) — plus 5 lignes hors plan de services de la feuille Détail : D-09,
D-10, D-11, E-03, E-06. Total : 44 codes, liste exacte plus bas.

Effort `xhigh` choisi pour toi par le directeur B : les plus grosses lignes de matériel du dossier (SD-I, PC-I,
PG-I, PU-I, MP-I) sont dans ce lot ; la dernière valeur doit être départagée entre libellés concurrents et
plusieurs portées (SD-E, SD-R, BJ, MP-E, DM-E, BC-E) n'ont aucun libellé direct ; une erreur ici passe telle
quelle dans le matériel et les heures du chiffrage.

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
   briefer EXACTEMENT 3 subalternes, modèle haiku : les releveurs B1-1, B1-2 et B1-3.
2. PHASE 1 (maintenant) : tu lis le kit, tu découpes ton lot en 3 sous-lots DISJOINTS (aucun code dans deux
   sous-lots) et COUVRANTS (chacun des 44 codes attribué), puis tu écris les 3 prompts de tes releveurs dans le
   dossier `prompts/directeur-B/chef-1/` (à créer) : `prompts/directeur-B/chef-1/releveur-1.md`,
   `prompts/directeur-B/chef-1/releveur-2.md`, `prompts/directeur-B/chef-1/releveur-3.md`. Chaque fichier
   commence EXACTEMENT par deux lignes — `effort: <low|medium|high|xhigh|max>` puis `modele: haiku` — suivies du
   prompt complet et autonome. Le releveur B1-m écrit `lots/releveur-B1-m.json` (m = 1, 2, 3).
3. Chaque prompt de releveur DOIT contenir, MOT POUR MOT : les RÈGLES D'AVEUGLE ci-dessus ET le bloc « MÉCANIQUE DE RELAIS » ci-dessous (tu recopies ces mêmes règles et cette même mécanique). Il DOIT aussi contenir : son rôle
   et son nom (« releveur B1-2 »…), le dossier de travail, la liste exacte de SES codes avec, pour chacun, la portée
   relevée et les libellés candidats, les sections « Le kit », « Règles de prix et de temps », « Nomenclature »,
   « Format de src, u et art », « Format JSON » et « Vérifications » ci-dessous (recopiées ou adaptées sans rien
   perdre), le nom EXACT du fichier à écrire, et l'ordre de s'arrêter après l'avoir écrit et vérifié. Les releveurs
   ne voient ni ce prompt ni ton contexte : chaque brief doit se suffire à lui-même.
4. Après avoir écrit tes 3 prompts et vérifié leurs deux premières lignes (`head -2`), tu T'ARRÊTES : tu ne fais
   pas le travail des releveurs et tu n'écris pas `lots/chef-B1.json`. Tu réponds seulement « prompts prêts », avec
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
Lis dans cet ordre : `CONSIGNES.md`, `METHODE.md`, `ARCHITECTURE.md` (§2 kit, §3 nomenclature, §5 format JSON,
§6 vérification, §7 prompts/effort — la loi de l'essaim), `rapport-releve.md`, `reserves.md` (R-002, R-007, Q14).
Puis ouvre le catalogue (code ci-dessous), la feuille `Détail` d'Estimation_2 (lignes D-01…D-11, E-01…E-06 et
A-03…A-05 pour le contexte), la feuille `Matériel Lumen` (section DISPOSITIFS et BOÎTES) et `releve.xlsx`
(feuille `Par libellé`). Interroge toi-même le catalogue pour chaque famille AVANT d'écrire les prompts : tu dois
connaître les candidats pour briefer juste.

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

## Ton lot B1 — les 44 codes à couvrir (portées relevées = tableau de rapport-releve.md)
Libellés candidats à examiner (valeurs à relire dans le CSV ; liste non exhaustive : chercher aussi d'autres
variantes). « repère » = valeur de METHODE.md qui tranche selon la règle 1.

Prises (légende « PRISE DE COURANT DOUBLE 15A- 120V », « … TYPE Leviton Decora USB », « PRISE DOUBLE DDFT ») :
- PC-I (INSTALLER 25) : « PRISE DUPLEX 15A 120V » (repère 64,81 $ / 1,175 h) ; écartés à noter : « PRISE DUPLEX 15/20A 120V », « PRISE », « PRISE 15A 125V ».
- PC-E (ENLEVER 7) : « ENLEVER PRISE » (repère prise enlevée 0,35 h) ; écarté « PRISES A DEMANTELER ».
- PC-R (RELOCALISER 8) : « RELO PRISE » (repère relocalisation de prise 1,5 h).
- PU-I (INSTALLER 20) : « PRISE USB 125V 15 AMP » (repère 77,45 $ / 1,125 h).
- PU-E, PU-R (portées absentes) : mêmes libellés que PC-E / PC-R, en note.
- PG-I (INSTALLER 22) : « PRISE DUPLEX 20A 125V GFI » (repère DDFT 65,38 $ / 1,3 h) ; écartés « PRISE DUPLEX 15A 120V GFI », « PRISE GFI », « PRISE GFI WP ». Note obligatoire : selon reserves.md R-007, la famille PRISE DDFT
  contient aussi les prises M.A.L.T. isolées (bordereau 3.29) — aucun libellé Dupuis distinct, dire ce que tu as
  cherché.
- PG-E (ENLEVER 4) : « ENLEVER PRISE » ; PG-R (RELOCALISER 1) : « RELO PRISE ».

Télécom :
- SD-I (INSTALLER 65) : « TEL/DATA 3/4 » (repère tel/data 3/4 22,32 $ / 0,89 h) ; écartés « TEL/DATA »
  (nb_projets 17), « SORTIE DATA », « SORTIE RESEAU », « SORTIE TEL ».
- SD-E (ENLEVER 17) et SD-R (RELOCALISER 3) : aucun libellé « ENLEVER DATA » / « RELO DATA » connu → arbitrer
  entre un analogue Dupuis (« ENLEVER PRISE », « PRISES A DEMANTELER », « RELO PRISE »…) et le jugement
  (Estimation_2) A-03 (démantèlement services, h/unité) / A-05 (relocalisation services) ; justifier en note.
- TV-I, TV-E, TV-R (relevé : CONSERVER 4 seulement → précaution) : « SORTIE TV » (repère 15 $) ; analogues pour E/R.

Commande, chauffage, contrôle d'accès :
- INT-I (INSTALLER 5) : « INTERRUPTEUR 15A 120V » (repère 75,47 $) ; écartés « INTERRUPTEUR », « INTERR DECO 15A 120V BLANC », « INTERRUPTEUR 15A 347V ».
- INT-E (ENLEVER 1) : « ENLEVER INTERRUPTEUR » vs « INTERRUPTEUR A DEMANTELER » — arbitrer (règles 2 à 4).
- INT-R (absent) : « RELO INT ».
- TH-I (INSTALLER 2) : « THERMOSTAT » (repère 35 $) ; TH-E, TH-R (absents) : analogues, en note.
- LC-I (INSTALLER 2) : « LECTEUR DE CARTE » (repère 15 $) vs « LECTEUR CARTE » ; LC-R : « LECTEUR RELO » ; LC-E : analogue.
- GA-I, GA-E, GA-R (relevé : CONSERVER 3 seulement) : « GACHE » (repère 15 $), « GACHE ELECTRIQUE », « GACHE RELO ».
- DM-I (absent), DM-E (ENLEVER 1), DM-R (absent) : « DETECTEUR MOUVEMENT », « DETECTEUR DE MOUVEMENT » ; pour
  l'enlèvement aucun libellé direct connu → analogue Dupuis ou jugement, en note.

Services :
- BJ-I (INSTALLER 3), BJ-E (ENLEVER 2), BJ-R (absent) : aucun libellé « BOITE DE JONCTION » connu ; candidats
  « BOITE CARRE 2-1/8PO KO 1 », « BOITE CARREES 4 PO », « BOITE OCTOG 1-1/2PO KO 1 », « BOITE D 8X8X4PO CEMA1 » ;
  repli Lumen IBE52151K / IBE72171K / IBE54151L seulement si Dupuis n'a vraiment rien ; enlèvement : analogue ou
  jugement. Justifier en note.
- MP-I (INSTALLER 3) : « MONUMENT PLANCHER » et « MONUMENT PLANCHER 1TE » (repère monument 250 $) — départager
  (règles 2 à 4) ; écartés « MONUMENT PLANCHER SU », « MONUMENT PLANCHER EN », « MONUMENT PLANCHER PR ». NE PAS utiliser le prix Lumen du
  poke-through HUBS1R6PTDEHBLK (le repère Dupuis 250 $ prévaut) : noter l'écart.
- MP-E (ENLEVER 3), MP-R (absent) : aucun libellé direct connu → analogue ou jugement, en note.
- BC-I, BC-E, BC-R — BOITIER C, famille alarme, hors légende (« BOITIER « C » (hors légende — R-006 TEST-E201) ») :
  relevé ENLEVER 2, CONSERVER 2 (attention : BC-E est bien relevé, 2). Aucun libellé direct connu → chercher
  (`BOITIER`, `BOITE`, `ENL`), sinon analogue ou jugement, en note.

Hors plan (feuille Détail — tu chiffres p et h unitaires dans l'unité de la ligne Détail, `u` = U ou LOT) :
- D-09 « Barrière anti-vol : 2 boîtes de jonction + raccord panneau de contrôle (PU-1 23) » (1 lot, 6 h estimées).
- D-10 « Bornes de prêts / fontaine hall (P2-63, note 2) — JB dans mur adjacent » (1 u).
- D-11 « Bouton d'appel — boîte + conduit vide (système fourni par d'autres) » (1 u).
- E-03 « Boîte de plancher refaite (salle 208, ancien mobilier — note 1 E-102) » (2 u).
- E-06 « Bouton d'appel (2) + bouton de panique (1) — boîte + conduit vide » (3 u).
  Candidats : libellés de boîtes ci-dessus, « BOUTON OUVERTURE », « BOUTON HANDICAPE », « DECLENCHEUR APPEL »,
  « MONUMENT PLANCHER … » (analogue pour E-03) ; sinon jugement (Estimation_2) avec le h / unité de la ligne
  elle-même. Un `src` composé (ex. 2 × boîte) écrit chaque libellé et l'opération.

Liste exacte (44) : PC-I PC-E PC-R PU-I PU-E PU-R PG-I PG-E PG-R SD-I SD-E SD-R TV-I TV-E TV-R INT-I INT-E
INT-R TH-I TH-E TH-R BJ-I BJ-E BJ-R MP-I MP-E MP-R LC-I LC-E LC-R GA-I GA-E GA-R DM-I DM-E DM-R BC-I BC-E BC-R
D-09 D-10 D-11 E-03 E-06.

Doubles comptes : le chef de lot B3 les traite pour tout le lot B, mais si tu en vois un (ex. une ligne Détail
D-01…D-08, E-01, E-02, E-04, E-05 qui recompte un appareil relevé sur plan ; une boîte Lumen ajoutée à un prix
d'assemblage), écris-le dans `doubles_comptes` avec la règle « le plan gagne ; un objet physique n'est payé qu'une fois ».

## Découpage et effort de tes releveurs
Tu découpes toi-même. Suggestion (que tu peux changer en restant disjoint et couvrant) : B1-1 = prises PC, PU, PG
(9 codes) ; B1-2 = SD, TV, INT, TH, DM (15 codes) ; B1-3 = BJ, MP, LC, GA, BC + D-09, D-10, D-11, E-03, E-06
(20 codes). Tu choisis l'effort de chaque releveur selon la grille d'ARCHITECTURE.md §7 (`low` recopie mécanique
d'un petit tableau ; `medium` recherche simple ; `high` arbitrage entre libellés approximatifs, portées,
doublons ; `xhigh` quand une erreur se propage à tout le chiffrage ; `max` réservé à la consolidation finale).
Nos moyens ne sont pas comptés : choisis ce qui maximise la justesse. Justifie chaque choix d'une ligne.

## À ta relance (PHASE 2 — « tes releveurs ont fini »)
1. Ouvre `lots/releveur-B1-1.json`, `lots/releveur-B1-2.json`, `lots/releveur-B1-3.json` ; vérifie qu'ils se
   chargent et que chacun des 44 codes apparaît exactement une fois au total (un manque = tu le chiffres
   toi-même ; un doublon = tu tranches).
2. Pour AU MOINS 5 lignes de chaque releveur (choisies au hasard, dont au moins une -E ou -R), rouvre le catalogue
   avec `ligne(desc, um)` et vérifie `p == prix_a_utiliser` et `h == temps_a_utiliser` du libellé cité (ou la
   cellule Lumen / Détail citée). Note le score x/5 de chaque releveur dans `notes`. Une erreur trouvée = TOUT le
   lot de ce releveur est revu ligne par ligne par toi, corrections notées.
3. Contrôle les choix : repère METHODE respecté quand il existe ; candidats écartés notés ; aucun h = 0 pour un
   vrai travail ; ENLEVER à p = 0 ; aucune boîte/plaque Lumen ajoutée à un prix d'assemblage ; les replis
   (analogue, Lumen, jugement) sont tous dits en note. Harmonise les choix entre releveurs (ex. même libellé
   d'enlèvement pour PC-E, PU-E, PG-E).
4. Écris `lots/chef-B1.json` : `"niveau": "chef"`, `"nom": "B1"`, `"modele_demande": "sonnet"`,
   `"effort_demande": "xhigh"`, `"lignes"` (44 lignes, q = null), `"notes"` (découpage en 3 sous-lots avec la
   liste des codes de chacun, effort de chaque releveur + justification d'une ligne, scores x/5, arbitrages,
   candidats écartés, replis, rappel taux 85 $/h et facteur 1,244 non appliqués), `"doubles_comptes"` (ceux que tu
   as vus). Vérifie qu'il se charge (`python3 -c "import json;json.load(open('...'))"`), qu'aucun code n'y figure
   deux fois et que `q` est null partout.
5. Réponds seulement : nombre de codes couverts, codes sans correspondance Dupuis directe (et leur repli), tes
   arbitrages en 5 lignes maximum.

Maintenant (PHASE 1) : lis, interroge le catalogue, découpe, écris les 3 prompts, vérifie leurs en-têtes, et
arrête-toi en répondant « prompts prêts » avec l'effort choisi pour chaque releveur et sa justification d'une ligne.
