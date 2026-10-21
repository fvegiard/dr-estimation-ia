effort: xhigh
modele: sonnet

# Chef de lot B2 — ÉCLAIRAGE, URGENCE, ALARME, MÉCANIQUE, DISTRIBUTION, CONDUITS/FILAGE, LOTS : prix et temps « méthode Dupuis » (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le chef de lot B2, modèle Claude Sonnet 5.5, d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton supérieur est le directeur B (Claude Opus 5.5), lui-même sous le chef de l'essaim (Claude
Fable 5.1). Tu as sous tes ordres EXACTEMENT 3 releveurs, modèle « haiku » (releveurs B2-1, B2-2, B2-3).
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la
médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités sont la mission de l'équipe A :
`q` reste `null` partout.

Ton lot B2 (76 codes, liste exacte plus bas) : luminaires existants à enlever/relocaliser (ENC, ENCU, L14, L22,
L4, LLIN), haut-parleur HP, luminaires neufs du tableau E-008 (LA1, LC1, LC11, LC13, LE — 0 $ + temps), enseigne
Z6, alarme incendie DF/SM/PA, moteurs MM/MT, distribution B-01…B-09 (panneau PP-3 et disjoncteurs), nacelle X-02,
scan dalle X-01, percements D-12/E-07, conduits et filage (C-05…C-08, D-13…D-15, E-08…E-10, F-08, F-09, G-02,
G-03, conversion au pied), les 5 lots fournisseur confirmés, et le repli Lumen pour toute famille introuvable.

Effort `xhigh` choisi pour toi par le directeur B : c'est le lot le plus lourd et le plus piégé — assemblages de
conduits au pied (fil inclus ou non), choix « 0 $ + lot » contre prix en ligne, panneau et disjoncteurs couverts
ou non par LOT-DIST, repères METHODE introuvables (luminaire enlevé 0,5 h), annonciateur à 550 $ ou 0 $ — chacune
de ces décisions déplace tout le total ACCEO.

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
   briefer EXACTEMENT 3 subalternes, modèle haiku : les releveurs B2-1, B2-2 et B2-3.
2. PHASE 1 (maintenant) : tu lis le kit, tu découpes ton lot en 3 sous-lots DISJOINTS (aucun code dans deux
   sous-lots) et COUVRANTS (chacun des 76 codes attribué), puis tu écris les 3 prompts de tes releveurs dans le
   dossier `prompts/directeur-B/chef-2/` (à créer) : `prompts/directeur-B/chef-2/releveur-1.md`,
   `prompts/directeur-B/chef-2/releveur-2.md`, `prompts/directeur-B/chef-2/releveur-3.md`. Chaque fichier
   commence EXACTEMENT par deux lignes — `effort: <low|medium|high|xhigh|max>` puis `modele: haiku` — suivies du
   prompt complet et autonome. Le releveur B2-m écrit `lots/releveur-B2-m.json` (m = 1, 2, 3).
3. Chaque prompt de releveur DOIT contenir, MOT POUR MOT : les RÈGLES D'AVEUGLE ci-dessus ET le bloc « MÉCANIQUE DE RELAIS » ci-dessous (tu recopies ces mêmes règles et cette même mécanique). Il DOIT aussi contenir : son rôle
   et son nom (« releveur B2-3 »…), le dossier de travail, la liste exacte de SES codes avec, pour chacun, la portée
   relevée et les libellés candidats, les sections « Le kit », « Règles de prix et de temps », « Nomenclature »,
   « Format de src, u et art », « Format JSON » et « Vérifications » ci-dessous (recopiées ou adaptées sans rien
   perdre), les consignes spéciales de son sous-lot (conduits, lots…), le nom EXACT du fichier à écrire, et l'ordre
   de s'arrêter après l'avoir écrit et vérifié. Les releveurs ne voient ni ce prompt ni ton contexte : chaque brief
   doit se suffire à lui-même.
4. Après avoir écrit tes 3 prompts et vérifié leurs deux premières lignes (`head -2`), tu T'ARRÊTES : tu ne fais
   pas le travail des releveurs et tu n'écris pas `lots/chef-B2.json`. Tu réponds seulement « prompts prêts », avec
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
§6 vérification, §7 prompts/effort — la loi de l'essaim), `rapport-releve.md`, `reserves.md` (R-002, R-003,
R-005). Puis ouvre le catalogue (code ci-dessous), la feuille `Détail` d'Estimation_2 (sections A, B, C, D-12…D-15,
E-07…E-10, F, G), la feuille `Matériel Lumen` (toute), `entree/reference-Releve_Eclairage_Urgence.xlsx` et
`entree/reference-Releve_Alarme_Incendie.xlsx` (contexte des lots), et `releve.xlsx` (feuille `Par libellé`).
Interroge toi-même le catalogue pour chaque famille AVANT d'écrire les prompts : tu dois connaître les candidats
pour briefer juste.

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

## Ton lot B2 — les 76 codes à couvrir (portées relevées = tableau de rapport-releve.md)
Libellés candidats à examiner (valeurs à relire dans le CSV ; liste non exhaustive : chercher aussi d'autres
variantes). « repère » = valeur de METHODE.md qui tranche selon la règle 1.

Luminaires existants (ENCASTRE : CONSERVER 49, ENLEVER 26, RELOCALISER 4 ; ENCASTRE URGENCE : CONSERVER 10 ;
LED 1X4 : CONSERVER 27, ENLEVER 6 ; LED 2X2 : CONSERVER 86, ENLEVER 8 ; LED 4PI : CONSERVER 2 ; LUMINAIRE
LINEAIRE : CONSERVER 4) — codes ENC, ENCU, L14, L22, L4, LLIN en -I, -E, -R :
- -E : « ENLEVER FIXTURE ENCAST » (ENC, ENCU), « ENLEVER FIXTURE 1X4 » (L14), « ENLEVER FIXTURE 2X2 » (L22),
  « ENLEVER FIXTURE 2X4 », « ENLEVER FIXTURE MURAL », « FIXTURE ENCASTRE ENLEV », « APPAREIL D'ECLAIRAGE A DEMANTELER », « STRIP STRIP ENLEVER ». Repère METHODE « luminaire enlevé 0,5 h » : chercher un libellé
  d'enlèvement de luminaire à 0,5 h ; s'il n'existe pas, l'écrire en note et appliquer les règles 2 à 4 (même
  objet + même action d'abord). Harmoniser : un même raisonnement pour les 6 familles.
- -R : « RELO ENCASTRE », « RELO FIXTURE 30X30 », « RELO FIXT TYPE E2 », « RELO FIXTURE TYPE S7 ».
- -I (portée absente, précaution) : « FIXTURE ENCASTRE », « FIXTURE TYPE 2X2 », etc. — pas dans un lot, p du
  catalogue.
- HP (HP ENCASTRE PLAFOND : ENLEVER 1) : HP-E aucun libellé « ENLEVER HAUT PARLEUR » connu → analogue Dupuis ou
  jugement, en note ; HP-R : « RELO HAUT PARLEUR PL », « RELO HAUPARLEUR MURAL » (le libellé « RELO HAUT PARLEUR »
  a un temps 0 : à écarter, noter) ; HP-I : « HAUT PARLEUR ».

Luminaires neufs du tableau E-008 (LUMINAIRE A1 : INSTALLER 11 ; C1 : 12 ; C1_1 : 6 ; C1_3 : 15 ; E : 3) — codes
LA1-I, LC1-I, LC11-I, LC13-I, LE-I, et enseigne Z6 (ENSEIGNE SORTIE Z6 : INSTALLER 3) — codes Z6-I, Z6-E, Z6-R :
- p = 0 en ligne (couverts par LOT-ECL), temps seulement. Repère luminaire 0,75 h : « FIXTURE TYPE A1 »
  (nb_projets 7), « FIXTURE TYPE C1 », « FIXTURE TYPE E », « FIXTURE TYPE A »… ; écartés à noter : « LUMINAIRE A1 »
  et « LUMINAIRE C1 » (autre projet ; lettres de type propres à chaque dossier). Dire en note si les modules 1′ et
  3′ (C1_1, C1_3) méritent un autre temps et pourquoi tu gardes ou non 0,75 h.
- Z6-I : « ENSEIGNE SORTIE » (nb_projets 10) ou « ENSEIGNE SORTIE Z6 » (repère enseigne 1 h), p = 0 (LOT-ECL) ;
  Z6-E : « ENLEVER ENSEIGNE SORTI » ; Z6-R : « RELO ENSEIGNE SORTIE », « ENSEIGNE RELO ». (reserves.md R-005 :
  tracé pointillé, « confirmer neuf » — d'où la précaution E/R.)

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

Travaux spéciaux :
- X-01 scan de dalle (bordereau 3.32) : « SCAN DALLE BETON » (repère scan dalle 1 250 $) ; écartés « SCAN DALLE »,
  « SCAN », « SCANN DALLE », « SCAN BETON ». ATTENTION : LOT-GPR 1 250 $ (GPR = géoradar = le même scan de dalle)
  → écrire dans `doubles_comptes` {X-01, LOT-GPR} : un seul des deux est payé.
- X-02 nacelle : « NACELLE » (repère 1 250 $ / 16 h). Noter le recouvrement possible avec Détail H-01
  (« plateforme/échafaudage roulant », chiffré par le chef B3).
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

Liste exacte (76) : ENC-I ENC-E ENC-R ENCU-I ENCU-E ENCU-R L14-I L14-E L14-R L22-I L22-E L22-R L4-I L4-E L4-R
LLIN-I LLIN-E LLIN-R HP-I HP-E HP-R LA1-I LC1-I LC11-I LC13-I LE-I Z6-I Z6-E Z6-R DF-I DF-E DF-R SM-I SM-E SM-R
PA-I PA-E PA-R MM-I MM-E MM-R MT-I MT-E MT-R B-01 B-02 B-03 B-04 B-05 B-06 B-07 B-08 B-09 X-01 X-02 D-12 E-07
C-05 C-06 C-07 C-08 D-13 D-14 D-15 E-08 E-09 E-10 F-08 F-09 G-02 G-03 LOT-ECL LOT-DIST LOT-JCI LOT-DET LOT-GPR.

Doubles comptes : le chef de lot B3 les traite pour tout le lot B, mais écris dans `doubles_comptes` ceux que tu
vois (au minimum : X-01/LOT-GPR ; chaque fil inclus dans un assemblage C-05/C-06, C-07/C-08, D-13/D-15, E-08/E-10,
F-08/F-09 ; PA-I/PA-R avec Détail G-04 ; X-02 avec H-01 ; Lumen conduits/fils/boîtes contre assemblages Dupuis).

## Découpage et effort de tes releveurs
Tu découpes toi-même. Suggestion (que tu peux changer en restant disjoint et couvrant) : B2-1 = luminaires
existants ENC, ENCU, L14, L22, L4, LLIN + luminaires neufs LA1-I, LC1-I, LC11-I, LC13-I, LE-I + Z6 (26 codes) ;
B2-2 = HP, DF, SM, PA, MM, MT + B-01…B-09 + X-02 (28 codes) ; B2-3 = conduits et filage (14 codes) + X-01, D-12,
E-07 + les 5 lots (22 codes). Tu choisis l'effort de chaque releveur selon la grille d'ARCHITECTURE.md §7 (`low`
recopie mécanique d'un petit tableau ; `medium` recherche simple ; `high` arbitrage entre libellés approximatifs,
portées, doublons ; `xhigh` quand une erreur se propage à tout le chiffrage ; `max` réservé à la consolidation
finale). Nos moyens ne sont pas comptés : choisis ce qui maximise la justesse. Justifie chaque choix d'une ligne.

## À ta relance (PHASE 2 — « tes releveurs ont fini »)
1. Ouvre `lots/releveur-B2-1.json`, `lots/releveur-B2-2.json`, `lots/releveur-B2-3.json` ; vérifie qu'ils se
   chargent et que chacun des 76 codes apparaît exactement une fois au total (un manque = tu le chiffres
   toi-même ; un doublon = tu tranches).
2. Pour AU MOINS 5 lignes de chaque releveur (au hasard, dont au moins un conduit pour B2-3 et une ligne à p = 0
   forcé), rouvre le catalogue avec `ligne(desc, um)` et vérifie `p == prix_a_utiliser` et `h == temps_a_utiliser`
   du libellé cité (ou la cellule Lumen / Détail citée). Note le score x/5 de chaque releveur dans `notes`. Une
   erreur trouvée = TOUT le lot de ce releveur est revu ligne par ligne par toi, corrections notées.
3. Contrôle les choix : repère METHODE respecté quand il existe ; p = 0 pour tout ce qui est dans un lot
   (luminaires neufs, Z6, DF-I, B-01…B-05 et ce que tu décides pour B-06…B-08) ; conduits en `u` = « PI » ;
   fil inclus = 0 sans double paiement ; aucun h = 0 pour un vrai travail ; candidats écartés et replis notés ;
   `lots` contient exactement les 5 lots confirmés.
4. Écris `lots/chef-B2.json` : `"niveau": "chef"`, `"nom": "B2"`, `"modele_demande": "sonnet"`,
   `"effort_demande": "xhigh"`, `"lignes"` (76 lignes, q = null), `"lots"` (les 5 montants), `"notes"` (découpage
   en 3 sous-lots avec la liste des codes de chacun, effort de chaque releveur + justification d'une ligne, scores
   x/5, arbitrages, candidats écartés, replis Lumen/jugement, écart LOT-ECL, rappel taux 85 $/h et facteur 1,244 non
   appliqués), `"doubles_comptes"`. Vérifie qu'il se charge (`python3 -c "import json;json.load(open('...'))"`),
   qu'aucun code n'y figure deux fois et que `q` est null partout.
5. Réponds seulement : nombre de codes couverts, codes sans correspondance Dupuis directe (et leur repli), tes
   arbitrages en 5 lignes maximum.

Maintenant (PHASE 1) : lis, interroge le catalogue, découpe, écris les 3 prompts, vérifie leurs en-têtes, et
arrête-toi en répondant « prompts prêts » avec l'effort choisi pour chaque releveur et sa justification d'une ligne.
