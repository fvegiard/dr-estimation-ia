effort: xhigh
modele: haiku

# Releveur B1-1 — PRISES, INTERRUPTEURS, THERMOSTATS : prix et temps « méthode Dupuis » (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le releveur B1-1, modèle Claude Haiku, feuille de l'arbre d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton supérieur est le chef de lot B1 (Claude Sonnet 5.5), sous le directeur B (Claude Opus 5.5), sous le chef de l'essaim
(Claude Fable 5.1). Tu ne délègues à personne : tu fais tout toi-même, tu écris UN fichier JSON, tu le vérifies et tu t'arrêtes.
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` /
`temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les
quantités sont la mission d'une autre équipe : `q` reste `null` partout.

Ton sous-lot (B1-1) : 15 codes, ni plus ni moins : PC-I PC-E PC-R PU-I PU-E PU-R PG-I PG-E PG-R INT-I INT-E INT-R TH-I TH-E TH-R.
Pourquoi tu es sur ce sous-lot avec le plus grand soin : Les plus grosses lignes de matériel du dossier pour les prises (PC-I 25, PU-I 20, PG-I 22) sont dans ton sous-lot : une erreur de libellé ou une médiane glissée ici passe telle quelle dans le matériel et les heures.

```
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
```

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

## Dossier de travail
`/home/claude/entrainement/S-1902/swarm-2/` — tu y travailles uniquement (chemins absolus conseillés, `python3`). Tu n'écris QUE ton fichier
`lots/releveur-B1-1.json`. Tu n'as pas besoin des fichiers de l'équipe A (quantités).

## Première chose à faire
Lis `CONSIGNES.md` et `METHODE.md` (courts), `rapport-releve.md` (tableau « famille | total | portées »), `reserves.md` (R-002, R-006, R-007, Q14), puis ouvre
le catalogue (code ci-dessous), la feuille `Détail` d'Estimation_2 (lignes D-01…D-11, E-01…E-06 et A-03…A-05 pour le contexte), la feuille `Matériel Lumen`
et `releve.xlsx` (feuilles `Par libellé` et `Marques`). Pour CHAQUE code, interroge toi-même le catalogue (`cherche`, `ligne`) : relis les candidats cités
plus bas ET cherche d'autres variantes par sous-chaînes courtes — ne conclus jamais « absent » après une seule recherche. Le chef de lot a déjà arbitré
chaque code (bloc « RETENU ») : tu dois le CONFIRMER ou le CONTREDIRE par la lecture du fichier, jamais le recopier sans relire.

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

## Format JSON (ARCHITECTURE.md §5) — releveur (l'exemple ci-dessous est illustratif : ton fichier ne contient QUE tes codes)
```json
{
  "niveau": "releveur",
  "nom": "B1-1",
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

## POLITIQUE D'ANALOGUES (harmonisée entre les 3 releveurs B1 — à appliquer telle quelle)
Quand le catalogue n'a aucun libellé direct pour une portée (enlever / relocaliser), les trois releveurs B1 utilisent LE MÊME analogue
Dupuis (les valeurs ci-dessous sont lues dans le CSV par le chef de lot — RELIS-LES toi-même avec `ligne()`) :
- Démontage (-E) d'un dispositif mural/boîte (prise, USB, DDFT, data, TV, thermostat, boîte de jonction, monument, détecteur de mouvement) :
  « ENLEVER PRISE » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)   ← repère METHODE « prise enlevée 0,35 h »
- Relocalisation (-R) du même type de dispositif : « RELO PRISE » um=U p=0.0 h=1.5 nb_projets=3 dernier 2026-05-05 (s-1753 ecole asomption)   ← repère METHODE « relocalisation de prise 1,5 h »
- Démontage (-E) d'un dispositif de contrôle d'accès (lecteur de carte, gâche, boîtier C) : « CONTACT DE PORTE ENL » um=U p=0.0 h=0.5 nb_projets=1 dernier 2026-02-09 (s1659 ecole arc en ciel ste julie)
  (famille « ENL » du projet S-1659, la même qui contient « LECTEUR RELO », « GACHE RELO » ; valeurs identiques pour
  « OPERATEUR PORTE ENL » um=U p=0.0 h=0.5 nb_projets=1 dernier 2026-02-09 (s1659 ecole arc en ciel ste julie) ; « IC ENL » um=U p=0.0 h=0.5 nb_projets=1 dernier 2026-02-09 (s1659 ecole arc en ciel ste julie) ; « STATION ENL » um=U p=0.0 h=0.5 nb_projets=1 dernier 2026-02-09 (s1659 ecole arc en ciel ste julie))
- Relocalisation (-R) d'un détecteur de mouvement : « RELO DETECTEUR A FUME » um=U p=0.0 h=0.75 nb_projets=3 dernier 2026-10-07 (s-1881 hotel candlewood st-hyacinthe)
- Libellé direct pour INT-R : « RELO INT » um=U p=0.0 h=1.5 nb_projets=1 dernier 2026-05-05 (s-1753 ecole asomption)
Alternatives à NOMMER en notes quand tu les écartes : « PRISES A DEMANTELER » um=U p=0.0 h=0.2 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable) ; « EQUIPEMENT A ENLEVER » um=U p=0.0 h=0.5 nb_projets=1 dernier 2026-05-05 (s-1753 ecole asomption) ;
jugement (Estimation_2) Détail A-03 (démantèlement services RDC, h/unité), A-04 (2e), A-05 (relocalisation services) — relis ces h/unité dans la feuille Détail.
Ordre de repli (rappel) : analogue Dupuis > prix régulier Lumen (matériel) + jugement (Estimation_2) (temps). Aucun code de ton lot ne devrait exiger Lumen
ou le jugement ; si tu en utilises un, dis pourquoi en note.

## Tes 15 codes — portée relevée, libellés candidats et arbitrage du chef de lot
Les valeurs `p`, `h`, `nb_projets`, date et projet ci-dessous ont été lues dans le CSV par le chef de lot ; relis-les toi-même (`ligne(desc, um)`) avant d'écrire. Les portées viennent du tableau de `rapport-releve.md` ; « absente du relevé » = correspondance de précaution (la phrase « portée absente du relevé — correspondance de précaution » va dans `src`).

### PC-I — Prise double 15 A 120 V neuve
- portée relevée : INSTALLER 25 — u = `U` — art = `3.28`
- libellé du relevé / de la feuille Détail : « PRISE DE COURANT DOUBLE 15A- 120V » (famille PRISE DOUBLE 15A, légende E-001)
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « prise duplex 15 A 64,81 $ / 1,175 h » (p ET h égalent le repère).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « PRISE DUPLEX 15A 120V » um=U p=64.81 h=1.175 nb_projets=20 dernier 2026-09-25 (S-1857 - Maison St-Michel)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISE DUPLEX 15/20A 120V » um=U p=60.19 h=1.225 nb_projets=17 dernier 2026-10-07 (s-1881 hotel candlewood st-hyacinthe)
  - « PRISE » um=U p=45.0 h=0.6 nb_projets=2 dernier 2026-10-07 (s-1881 hotel candlewood st-hyacinthe)
  - « PRISE 15A 125V » um=U p=45.0 h=0.6 nb_projets=1 dernier 2026-03-27 (S-1714 PARTAGE DE RIVIERA)
  - « DROP DE PRISE » um=U p=35.43 h=0.9 nb_projets=4 dernier 2026-06-02 (s-1783 anjinnov mcgill 1981 accenture)
- NOTE : R-007 : le relevé ne distingue pas les prises 15 A et 20 A ; le repère METHODE (15 A, 64,81 $) prévaut — à dire en note.
- NOTE : Ne JAMAIS ajouter les prises/plaques Lumen LEV16252W / LEV16352W / LEV80401NW (feuille « Matériel Lumen ») : le prix d'assemblage Dupuis inclut déjà boîte, plaque et raccord.

### PC-E — Prise double 15 A enlevée
- portée relevée : ENLEVER 7 — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : famille PRISE DOUBLE 15A, portée ENLEVER
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « prise enlevée 0,35 h » → « ENLEVER PRISE » (h = 0,35, p = 0).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « ENLEVER PRISE » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISES A DEMANTELER » um=U p=0.0 h=0.2 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)
- NOTE : « PRISES A DEMANTELER » est plus récent (2026-09-23) mais h = 0,2 : écarté par la règle 1 (repère 0,35 h). ENLEVER → p = 0 (temps seulement).

### PC-R — Prise double 15 A relocalisée
- portée relevée : RELOCALISER 8 — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : famille PRISE DOUBLE 15A, portée RELOCALISER
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « relocalisation de prise 1,5 h » → « RELO PRISE » (p = 0, h = 1,5).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « RELO PRISE » um=U p=0.0 h=1.5 nb_projets=3 dernier 2026-05-05 (s-1753 ecole asomption)
- NOTE : RELOCALISER → prix selon le catalogue (ici 0 $) + temps de relocalisation.

### PU-I — Prise double 15 A USB neuve (Leviton Decora USB)
- portée relevée : INSTALLER 20 — u = `U` — art = `3.27`
- libellé du relevé / de la feuille Détail : « PRISE DE COURANT DOUBLE 15A- 120V TYPE Leviton Decora USB » (famille PRISE USB ; Q14 : code PU conservé)
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « USB 77,45 $ / 1,125 h ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « PRISE USB 125V 15 AMP » um=U p=77.45 h=1.125 nb_projets=6 dernier 2026-09-10 (s-1854 sollio st hubert lanthier)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISE DUPLEX 15A 120V » um=U p=64.81 h=1.175 nb_projets=20 dernier 2026-09-25 (S-1857 - Maison St-Michel)
- NOTE : Ne PAS utiliser le prix Lumen LEVT5633W (48,66 $) ni LEV80401NW : Dupuis a le libellé et le prix d'assemblage inclut boîte, plaque, raccord.
- NOTE : « PRISE DUPLEX 15A 120V » est la prise ordinaire (PC-I), pas la USB : à noter comme écarté.

### PU-E — Prise USB enlevée
- portée relevée : absente du relevé — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : aucune (portée absente)
- règle appliquée par le chef de lot : Même libellé que PC-E (harmonisation obligatoire).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « ENLEVER PRISE » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)
- à dire dans `src` : « ; analogue : une prise USB enlevée se démonte comme une prise ordinaire (repère METHODE prise enlevée 0,35 h) »
- à dire dans `src` : « ; portée absente du relevé — correspondance de précaution »
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISES A DEMANTELER » um=U p=0.0 h=0.2 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)

### PU-R — Prise USB relocalisée
- portée relevée : absente du relevé — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : aucune (portée absente)
- règle appliquée par le chef de lot : Même libellé que PC-R (harmonisation obligatoire).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « RELO PRISE » um=U p=0.0 h=1.5 nb_projets=3 dernier 2026-05-05 (s-1753 ecole asomption)
- à dire dans `src` : « ; analogue : une prise USB relocalisée se déplace comme une prise ordinaire (repère METHODE relocalisation de prise 1,5 h) »
- à dire dans `src` : « ; portée absente du relevé — correspondance de précaution »

### PG-I — Prise double 15 A DDFT (GFI) neuve
- portée relevée : INSTALLER 22 — u = `U` — art = `3.30`
- libellé du relevé / de la feuille Détail : « PRISE DOUBLE DDFT (moitié pleine) » (famille PRISE DDFT, légende E-001)
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « DDFT 65,38 $ / 1,3 h ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « PRISE DUPLEX 20A 125V GFI » um=U p=65.38 h=1.3 nb_projets=16 dernier 2026-10-07 (s-1881 hotel candlewood st-hyacinthe)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISE DUPLEX 15A 120V GFI » um=U p=55.51 h=1.225 nb_projets=2 dernier 2026-03-11 (S-1695_Hotel Playground Kahnawake)
  - « PRISE GFI » um=U p=55.0 h=0.6 nb_projets=2 dernier 2026-10-07 (s-1881 hotel candlewood st-hyacinthe)
  - « PRISE GFI WP » um=U p=65.5 h=1.25 nb_projets=2 dernier 2026-03-31 (S-1693_Ecole Primaire Beloeil)
  - « RECEPT DDFT AUTO TEST 20 A125V INVIOL BLANC » um=U p=22.54 h=0.25 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)
- NOTE : OBLIGATOIRE (reserves.md R-007) : la famille PRISE DDFT du relevé contient aussi les prises M.A.L.T. isolées (barre pleine ; bordereau 3.29 « Prises doubles 15A-120V MALT isolées »), non départagées au relevé. Cherche dans le catalogue (motifs MALT, ISOL, ORANGE, \bIG\b, DDFT, GFI, GFCI) un libellé distinct et DIS dans les notes ce que tu as cherché et trouvé. Le chef de lot n'a trouvé aucun libellé « prise M.A.L.T. isolée » (les libellés « TIGE MALT », « BARRE … ISOL », « ISOLATEUR », « BOITE TIGE MALT » sont d'autres objets) : sans libellé distinct, PG-I porte les deux variantes au prix DDFT.
- NOTE : « RECEPT DDFT AUTO TEST 20 A125V INVIOL BLANC » (22,54 $ / 0,25 h) est un récepteur seul (sans boîte ni plaque), pas un prix d'assemblage : écarté.
- NOTE : Ne PAS ajouter LEVGFNT1W (Lumen) : prix d'assemblage Dupuis.

### PG-E — Prise DDFT enlevée
- portée relevée : ENLEVER 4 — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : famille PRISE DDFT, portée ENLEVER
- règle appliquée par le chef de lot : Même libellé que PC-E (harmonisation obligatoire ; règle 1, repère 0,35 h).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « ENLEVER PRISE » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « PRISES A DEMANTELER » um=U p=0.0 h=0.2 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)

### PG-R — Prise DDFT relocalisée
- portée relevée : RELOCALISER 1 — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : famille PRISE DDFT, portée RELOCALISER
- règle appliquée par le chef de lot : Même libellé que PC-R (harmonisation obligatoire ; règle 1, repère 1,5 h).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « RELO PRISE » um=U p=0.0 h=1.5 nb_projets=3 dernier 2026-05-05 (s-1753 ecole asomption)

### INT-I — Interrupteur simple 15 A 120 V neuf
- portée relevée : INSTALLER 5 — u = `U` — art = `3.35`
- libellé du relevé / de la feuille Détail : « INTERRUPTEUR SIMPLE » (famille INT SIMPLE, légende E-001)
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « interrupteur 75,47 $ ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « INTERRUPTEUR 15A 120V » um=U p=75.47 h=1.075 nb_projets=13 dernier 2026-09-25 (S-1857 - Maison St-Michel)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « INTERRUPTEUR » um=U p=0.0 h=0.25 nb_projets=1 dernier 2026-02-02 (S-1645 ANNEXE-BOURASSA)
  - « INTERR DECO 15A 120V BLANC » um=U p=7.85 h=0.2 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)
  - « INTERRUPTEUR 15A 347V » um=U p=57.24 h=1.325 nb_projets=1 dernier 2026-06-02 (s-1783 anjinnov mcgill 1981 accenture)
- NOTE : Le bâtiment a des luminaires en 347 V : « INTERRUPTEUR 15A 347V » (57,24 $ / 1,325 h) est écarté parce que le repère METHODE (75,47 $) désigne « INTERRUPTEUR 15A 120V » ; le dire en note.

### INT-E — Interrupteur enlevé
- portée relevée : ENLEVER 1 — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : famille INT SIMPLE, portée ENLEVER
- règle appliquée par le chef de lot : Règles 2 à 4 (pas de repère) : « ENLEVER INTERRUPTEUR » et « INTERRUPTEUR A DEMANTELER » décrivent le MÊME objet et la MÊME action (règle 2 : égalité) ; nb_projets = 1 pour les deux (règle 3 : égalité) ; règle 4 : date_dernier le plus récent → « INTERRUPTEUR A DEMANTELER ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « INTERRUPTEUR A DEMANTELER » um=U p=0.0 h=0.1 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « ENLEVER INTERRUPTEUR » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)
- NOTE : Arbitrage mécanique par la règle 4 (date). Écrire dans les notes l'alternative « ENLEVER INTERRUPTEUR » (0,35 h, même famille S-1835 que ENLEVER PRISE) : le chef de lot / le directeur pourra la préférer pour la cohérence.

### INT-R — Interrupteur relocalisé
- portée relevée : absente du relevé — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : aucune (portée absente)
- règle appliquée par le chef de lot : Libellé direct : « RELO INT » (règle 2 : même objet, même action).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « RELO INT » um=U p=0.0 h=1.5 nb_projets=1 dernier 2026-05-05 (s-1753 ecole asomption)
- à dire dans `src` : « ; portée absente du relevé — correspondance de précaution »

### TH-I — Thermostat neuf
- portée relevée : INSTALLER 2 — u = `U` — art = `3.23`
- libellé du relevé / de la feuille Détail : « THERMOSTAT » (famille THERMOSTAT, chauffage)
- règle appliquée par le chef de lot : Règle 1 : repère METHODE « thermostat 35 $ ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « THERMOSTAT » um=U p=35.0 h=0.4 nb_projets=4 dernier 2026-06-03 (s-1775 clinique mieux etre)
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « THERMOSTAT B/V » um=U p=68.0 h=0.35 nb_projets=1 dernier 2026-03-11 (s-1689 pultrusion st-bruno)
  - « THERMOSTAT TS » um=U p=81.88 h=0.35 nb_projets=1 dernier 2026-09-25 (S-1857 - Maison St-Michel)
  - « THERMOSTAT ELECTRONIQUE INTEGRE » um=U p=66.0 h=0.0 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)
  - « THERMOSTAT FDP » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-07-13 (s-1808 cpe les copain d'ABORD)
- NOTE : « THERMOSTAT ELECTRONIQUE INTEGRE » (h = 0) est écarté (temps nul pour un vrai travail).

### TH-E — Thermostat enlevé
- portée relevée : absente du relevé — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : aucune (portée absente)
- règle appliquée par le chef de lot : Aucun libellé direct → analogue Dupuis (même action, objet voisin : dispositif mural) : « ENLEVER PRISE ».
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « ENLEVER PRISE » um=U p=0.0 h=0.35 nb_projets=1 dernier 2026-08-26 (s-1835 esbg  rehabilitation inbterieur)
- à dire dans `src` : « ; analogue : aucun libellé « ENLEVER THERMOSTAT » ; dispositif mural ≈ prise enlevée (repère METHODE 0,35 h) »
- à dire dans `src` : « ; portée absente du relevé — correspondance de précaution »
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « INTERRUPTEUR A DEMANTELER » um=U p=0.0 h=0.1 nb_projets=1 dernier 2026-09-23 (s-1866 gar mun st amable)

### TH-R — Thermostat relocalisé
- portée relevée : absente du relevé — u = `U` — art = `3.22`
- libellé du relevé / de la feuille Détail : aucune (portée absente)
- règle appliquée par le chef de lot : Aucun libellé direct → analogue Dupuis : « RELO PRISE » (même valeur que « RELO INT »).
- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :
  - « RELO PRISE » um=U p=0.0 h=1.5 nb_projets=3 dernier 2026-05-05 (s-1753 ecole asomption)
- à dire dans `src` : « ; analogue : aucun libellé « RELO THERMOSTAT » ; dispositif mural ≈ prise relocalisée (repère METHODE 1,5 h) »
- à dire dans `src` : « ; portée absente du relevé — correspondance de précaution »
- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :
  - « RELO INT » um=U p=0.0 h=1.5 nb_projets=1 dernier 2026-05-05 (s-1753 ecole asomption)

## Doubles comptes à examiner (à écrire dans `doubles_comptes`, règle « le plan gagne ; un objet physique n'est payé qu'une fois »)
Tu ne tranches pas les quantités (équipe A) : tu SIGNALES, avec `codes` et `regle`, ceux de ces couples que tu juges réels après lecture de la feuille Détail et de `releve.xlsx` (et tu écris ceux que tu vois en plus). Un couple jugé non réel va en note avec la raison.
- [D-06, PC-I] : Détail D-06 « Prise double murale/colonne NEUVE » (8 u) recompte des prises doubles neuves relevées sur plan
- [D-02, PU-I] : Détail D-02 « Table c/a boîte d'électrification : 2 prises doubles + 2 prises USB » (5 u) recompte des USB relevées
- [D-07, PG-I] : Détail D-07 « Prise DDFT 15A fontaine (P2-61) » (1 u) recompte une DDFT relevée
- [D-01, PC-I] : Détail D-01 « Poste de travail intégré mobilier : … 1 prise double 15A + 1 prise double 20A Decora… » (18 postes)
- [LEV16252W/LEV80401NW (Lumen), PC-I] : les prises et plaques Lumen ne s'ajoutent pas au prix d'assemblage Dupuis

## Squelette Python conseillé (tu peux l'adapter ; il élimine les fautes de frappe dans `p`, `h` et `src`)
```python
import csv, json, re
CAT = '/home/claude/entrainement/S-1902/swarm-2/catalogue-prix-temps-dupuis.csv'
rows = list(csv.DictReader(open(CAT, encoding='utf-8-sig'), delimiter=';'))
assert len(rows) == 2068, len(rows)
def ligne(desc, um=None):
    t = [r for r in rows if r['description'] == desc and (um is None or r['um'] == um)]
    assert len(t) == 1, (desc, len(t))
    return t[0]
def src_d(r):          # src Dupuis EXACT, construit depuis la ligne (aucune frappe à la main)
    return (f"catalogue Dupuis « {r['description']} » um={r['um']} (dernier {r['date_dernier']}, "
            f"{r['projet_dernier']}, nb_projets {r['nb_projets']})")
def note_ecarte(desc, um='U'):   # note d'un candidat écarté : libellé exact, p, h, nb_projets, date
    r = ligne(desc, um)
    return (f"écarté « {r['description']} » um={r['um']} p={r['prix_a_utiliser']} h={r['temps_a_utiliser']} "
            f"nb_projets={r['nb_projets']} dernier {r['date_dernier']}")
def mk(code, desc, u, art, lib, um='U', suite=''):   # ligne simple (un seul libellé Dupuis)
    r = ligne(lib, um)
    return {"code": code, "desc": desc, "q": None, "u": u,
            "p": float(r['prix_a_utiliser']), "h": float(r['temps_a_utiliser']),
            "art": art, "src": src_d(r) + suite}
# ligne composée (ex. D-09) : p = round(2*p1 + p2, 4), h idem ; src = « 2 × <src_d(r1)> + 1 × <src_d(r2)> »
```

## Ce que tu produis (et rien d'autre)
- Un SEUL fichier : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B1-1.json` (format « Format JSON » ci-dessus ; `"niveau": "releveur"`,
  `"nom": "B1-1"`, `"modele_demande": "haiku"`, `"effort_demande": "xhigh"`), avec EXACTEMENT les 15 lignes de tes codes (une par code, dans l'ordre
  de ta liste), `q` = `null` partout, `p` et `h` en nombres, `notes` (liste de textes) et `doubles_comptes` (liste ; vide si rien). `desc` = l'intitulé qui suit
  le code dans le titre « ### CODE — intitulé » de chaque bloc ci-dessus ; `u` et `art` = ceux écrits dans le bloc du code.
- N'écris AUCUN autre fichier (ni script, ni brouillon) : exécute ton code Python en ligne (`python3 - <<'EOF' … EOF`). Ne lis pas les autres
  fichiers de `lots/` ni de `prompts/` : tu n'en as pas besoin et ils ne t'aident pas à relire le catalogue.
- Contenu minimal de `notes` : (1) une entrée par code de ton lot disant le libellé retenu, la règle appliquée (1, 2, 3 ou 4 ; ou « analogue »)
  et les candidats écartés avec libellé exact, p, h, nb_projets, date (utilise `note_ecarte`) ; (2) tes désaccords éventuels avec l'arbitrage du chef de
  lot (choix + raison) ; (3) ce que tu as cherché sans trouver (motifs de recherche) ; (4) le rappel « taux 85 $/h et facteur de prix de vente 1,244 :
  non appliqués (METHODE.md §5/§7) » ; (5) le nom du modèle que tu es (« Claude Haiku », tel que ton contexte le dit).
- Avant d'écrire : relis CHAQUE ligne Dupuis avec `ligne(desc, um)` et vérifie `p == float(prix_a_utiliser)` et `h == float(temps_a_utiliser)` (somme
  pondérée pour une ligne composée) ; vérifie que `src` reproduit le libellé exact ; vérifie 0 doublon de code, `q is None` partout, ENLEVER → p = 0.
- Après avoir écrit le fichier : `python3 -c "import json;d=json.load(open('/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B1-1.json'));print(len(d['lignes']), sorted(l['code'] for l in d['lignes']))"`
  doit afficher 15 et exactement tes codes. Puis réponds en UNE ligne (nom du fichier écrit + nombre de lignes) et ARRÊTE-TOI : tu ne lances
  personne, tu n'écris pas de prompt, tu ne consolides rien.
