effort: high
modele: sonnet

# Chef de lot A1 — SERVICES SUR PLAN (essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS)

Tu es le **chef de lot A1** (modèle Claude Sonnet 5.5, « sonnet ») d'une équipe hiérarchique d'estimation
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

- Tu as le droit de briefer **EXACTEMENT 3 subalternes, des releveurs de modèle « haiku »** : `A1-1`, `A1-2`,
  `A1-3`. Ni plus, ni moins.
- Tu écris leurs prompts dans le dossier **`prompts/directeur-A/chef-1/`** : `prompts/directeur-A/chef-1/releveur-1.md`,
  `prompts/directeur-A/chef-1/releveur-2.md`, `prompts/directeur-A/chef-1/releveur-3.md`. Chaque fichier commence
  EXACTEMENT par deux lignes : `effort: <low|medium|high|xhigh|max>` puis `modele: haiku`, puis le prompt complet.
- Chaque releveur écrit `lots/releveur-A1-1.json`, `lots/releveur-A1-2.json`, `lots/releveur-A1-3.json`.
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
- `rapport-releve.md` : tableau « famille | total | portées ». **Les portées (INSTALLER / ENLEVER / RELOCALISER /
  CONSERVER) ne sont QUE là**, pas dans le classeur. CONSERVER = aucun travail → aucune ligne (le noter).
- `reserves.md` : R-002 (règle des portées), R-007 (prises : DDFT et M.A.L.T. isolée confondues ; 15 A et 20 A non
  distingués), Q14 (code PU pour la prise USB).
- `releve.xlsx` : feuille `Par libellé` (colonnes Libellé, Famille, Quantité, Description, Source (légende)),
  feuille `Par feuille` (colonnes Feuille (cartouche), Feuille (fichier), Libellé, Quantité), feuille `Marques`
  (645 lignes : Feuille, Libellé, x, y, Source, Note).
- `entree/reference-Estimation_2.xlsx`, feuille `Détail` (en-têtes en ligne 5 : Code, Description, Réf. plan, Qté,
  Unité, Prix mat. unit., Total mat., h / unité, Total h, Total MO, Total ligne, Notes / source quantité). On ne
  garde que ses **quantités** hors plan ; ses heures (« estimé Léna AI ») ne sont pas les heures du chiffrage.
- `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`) : articles 3.22 à 3.38, 5.11, 5.19, 6.1.
- Le catalogue Dupuis (`catalogue-prix-temps-dupuis.csv`) n'est PAS nécessaire au lot A (pas de prix ni de temps).

## 3. Ton lot (disjoint des lots A2 et A3)

### 3a. Familles sur plan → codes `<FAM>-<P>` (P : I = installer, E = enlever, R = relocaliser)
Valeurs lues par le directeur dans `rapport-releve.md` et `releve.xlsx` — **à revérifier dans les fichiers**, pas à
recopier de ce brief :

| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| PRISE DOUBLE 15A | PC | 95 | CONSERVER 55, INSTALLER 25, RELOCALISER 8, ENLEVER 7 | E101 48, E102 22, E104 23, E105 2 | PC-I 25, PC-R 8, PC-E 7 |
| PRISE USB | PU | 20 | INSTALLER 20 | E104 20 | PU-I 20 |
| PRISE DDFT | PG | 49 | CONSERVER 22, INSTALLER 22, ENLEVER 4, RELOCALISER 1 | E101 23, E102 4, E104 20, E105 2 | PG-I 22, PG-E 4, PG-R 1 |
| SORTIE DATA | SD | 120 | INSTALLER 65, CONSERVER 35, ENLEVER 17, RELOCALISER 3 | E101 36, E102 19, E104 45, E105 20 | SD-I 65, SD-E 17, SD-R 3 |
| SORTIE TV | TV | 4 | CONSERVER 4 | E101 1, E102 3 | aucune (note) |
| INT SIMPLE | INT | 10 | INSTALLER 5, CONSERVER 4, ENLEVER 1 | E201 5, E203 5 | INT-I 5, INT-E 1 |
| THERMOSTAT | TH | 9 | CONSERVER 7, INSTALLER 2 | E101 7, E104 2 | TH-I 2 |
| BOITE JONCTION | BJ | 10 | CONSERVER 5, INSTALLER 3, ENLEVER 2 | E101 4, E102 1, E104 3, E201 2 | BJ-I 3, BJ-E 2 |
| MONUMENT PLANCHER | MP | 7 | ENLEVER 3, INSTALLER 3, CONSERVER 1 | E101 1, E102 3, E105 3 | MP-I 3, MP-E 3 |
| LECTEUR CARTE | LC | 5 | CONSERVER 3, INSTALLER 2 | E101 3, E104 2 | LC-I 2 |
| GACHE | GA | 3 | CONSERVER 3 | E101 3 | aucune (note) |
| DETECTEUR MOUVEMENT | DM | 3 | CONSERVER 2, ENLEVER 1 | E201 3 | DM-E 1 |
| BOITIER C | BC | 4 | ENLEVER 2, CONSERVER 2 | E101 1, E201 3 | BC-E 2 |

**Contrôle de cohérence par feuille (à faire écrire par les releveurs)** : d'après R-002, une marque sans étiquette
est CONSERVER sur une feuille existant/démolition et INSTALLER sur une feuille nouveau. Pour les familles de ton lot,
on doit retrouver : C + E + R = somme des feuilles E101 + E102 + E103 + E201 + E202 (existant), et I = somme des
feuilles E104 + E105 + E106 + E203 + E204 (nouveau). Ex. PC : 48 + 22 = 70 = 55 + 7 + 8 ; 23 + 2 = 25 = I.
Un écart à ce contrôle va en note (il ne modifie pas la quantité : le rapport fait foi pour la portée).
Le `src` de chaque ligne donne la répartition par feuille, p. ex.
`"releve.xlsx Par libellé PRISE DOUBLE 15A 95 ; rapport-releve.md INSTALLER 25 ; Par feuille E104 23 + E105 2 (feuilles nouveau)"`.

### 3b. Lignes de la feuille `Détail` attribuées à A1 (chacune : reprise OU exclue, jamais oubliée)
Arbitrages déjà tranchés par le directeur (règle : **le plan gagne sur Détail pour les quantités** ; une ligne
Détail qui recompte un objet déjà relevé sur plan est un DOUBLE COMPTE → `exclusions` avec la ligne sur plan qui la
remplace ; la contradiction de quantité va en note) :

| Code Détail | Décision | Remplacée par / remarque |
|---|---|---|
| A-03 (34 u, démantèlement services RDC E.A.E) | EXCLURE | PC-E, PG-E, SD-E, BJ-E, MP-E, BC-E — noter 34 + 10 (A-04) = 44 E.A.E Détail vs total des lignes -E sur plan |
| A-04 (10 u, démantèlement services 2e) | EXCLURE | idem A-03 |
| A-05 (13 u, relocalisation services E.A.R) | EXCLURE | PC-R, PG-R, SD-R — noter 13 Détail vs 8 + 1 + 3 = 12 sur plan |
| D-01 (18 postes mobilier : JB + prise 15 A + prise 20 A + data) | EXCLURE | PC-I, SD-I — noter que les JB de poste et les prises 20 A ne sont pas distinguées sur plan (R-007) |
| D-02 (5 tables : 2 prises + 2 USB) | EXCLURE | PC-I, PU-I — noter 5 × 2 = 10 USB Détail vs PU-I 20 sur plan |
| D-03 (2 cabines : prise + JB) | EXCLURE | PC-I |
| D-04 (2 écrans : courant + données) | EXCLURE | PC-I, SD-I |
| D-05 (1 kiosque TV : prise + data) | EXCLURE | PC-I, SD-I |
| D-06 (8 prises murales/colonnes neuves) | EXCLURE | PC-I |
| D-07 (1 DDFT fontaine) | EXCLURE | PG-I |
| D-08 (10 sorties data murales/colonnes) | EXCLURE | SD-I |
| E-01 (2 postes aide au lecteur 227) | EXCLURE | PC-I, SD-I |
| E-02 (2 monuments de plancher) | EXCLURE | MP-I (3 sur plan ; noter 2 vs 3) |
| E-04 (3 cabines/salles : JB + prise) | EXCLURE | PC-I |
| E-05 (1 écran sur colonne) | EXCLURE | PC-I, SD-I |
| D-09 (1 lot barrière anti-vol : 2 JB + raccord panneau de contrôle PU-1 23) | REPRENDRE `D-09`, q 1, u LOT, art 3.31 | desc « raccord panneau de contrôle barrière anti-vol — les 2 JB sont comptées dans BJ-I » ; hypothèse : BJ-I 3 (E104) = 2 JB de D-09 + 1 JB de D-10 (vérifier : 3 BJ INSTALLER, toutes sur E104) |
| D-10 (1 u bornes de prêts / fontaine hall — JB dans mur) | EXCLURE | BJ-I (si le contrôle ci-dessus tient ; sinon reprendre D-10 q 1 et expliquer en note) |
| A-07 (1 lot relocalisation interrupteurs maîtres du hall, note spécifique 1 E-201) | REPRENDRE `A-07`, q 1, u LOT, art 3.35 | note : chevauchement possible avec INT-E 1 (E201) / INT-I 5 (E203) — non tranchable sans le plan |
| E-03 (2 u boîte de plancher refaite salle 208, note 1 E-102) | REPRENDRE `E-03`, q 2, u U, art 3.34 | note : chevauchement possible avec MP-E 3 (E102) / MP-I 3 (E105) — « à confirmer » dans Détail |

Les autres lignes Détail (A-01, A-02, A-06, A-08…A-11, B-, C-, D-11…D-16, E-06…E-11, F-, G-, H-, OPT-) appartiennent
aux lots A2 et A3 : ne les traite pas.

## 4. Articles du bordereau à proposer (`art`, texte)
Bordereau `entree/reference-Bordereau_de_prix.xlsx` : 3.22 Démontage des éléments électriques · 3.23 Raccordement
des équipements mécaniques · 3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles
15A-120V MALT isolées · 3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction ·
3.33 Sorties informatique/réseau · 3.34 Moinument plancher · 3.35 Appareil de contrôle + appareils d'éclairage ·
5.19 Démolition des systèmes électriques.
Convention du directeur A : toute ligne `-E` (enlever) → **3.22** ; une ligne `-R` (relocaliser) → l'article de sa
famille ; PC → 3.28 ; PU → 3.27 ; PG → 3.30 (noter que R-007 confond DDFT et M.A.L.T. isolée = 3.29) ; SD → 3.33 ;
MP → 3.34 ; INT → 3.35 ; TH → 3.23 ; BJ → 3.31 ; LC → 3.31 (aucun article « intrusion » au bordereau : le noter).

## 5. Format de sortie (pour tes releveurs et pour toi)
```json
{
  "niveau": "releveur",
  "nom": "A1-2",
  "modele_demande": "haiku",
  "effort_demande": "medium",
  "lignes": [
    {"code": "PC-I", "desc": "Prise double 15 A 120 V neuve", "q": 25, "u": "U", "p": null, "h": null,
     "art": "3.28", "src": "releve.xlsx Par libellé PRISE DOUBLE 15A 95 ; rapport-releve.md INSTALLER 25 ; Par feuille E104 23 + E105 2"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contrôles par feuille, contradictions plan/Détail"],
  "exclusions": [{"code": "D-06", "raison": "double compte : 8 prises murales neuves déjà dans PC-I (plan) — remplacée par PC-I"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte (« 3.28 ») ; `src` exact et vérifiable (fichier,
feuille, libellé ou code, valeur lue). Releveurs → `lots/releveur-A1-<m>.json` ; toi → `lots/chef-A1.json`
(`"niveau": "chef"`, `"nom": "A1"`, `"modele_demande": "sonnet"`, `"effort_demande": "high"`).

## 6. Découpage et choix d'effort (phase 1)
- Découpe ton lot (§3a + §3b) en **3 sous-lots disjoints** (aucune famille ni aucun code Détail dans deux sous-lots)
  **et couvrants** (tout est attribué). Suggestion non imposée : A1-1 = PC, PU, PG + D-01…D-08, A-05 ;
  A1-2 = SD, TV, MP, BJ + E-01, E-02, E-03, E-04, E-05, D-09, D-10, A-03, A-04 ; A1-3 = INT, TH, LC, GA, DM, BC + A-07.
  Écris la liste du découpage dans les notes de `lots/chef-A1.json` (phase 2) et dans ta réponse de phase 1.
- Choisis l'effort de chaque releveur (`low` recopie mécanique d'un petit tableau ; `medium` comptage/recherche
  simple dans un fichier ; `high` arbitrage de portées, doublons, libellés approximatifs ; `xhigh` quand une erreur
  se propage à tout le chiffrage ; `max` réservé aux consolidations finales). Nos moyens ne sont pas comptés :
  choisis ce qui maximise la justesse. Justifie chaque choix d'une ligne (réponse de phase 1 + notes de phase 2).
- Chaque prompt de releveur contient, dans cet ordre : son rôle et son nom (« releveur A1-2 »), les RÈGLES
  D'AVEUGLE mot pour mot, le dossier de travail, la mécanique (il ne délègue à personne, écrit son JSON, s'arrête),
  son sous-lot précis (familles et codes, fichiers/feuilles/colonnes à lire, valeurs attendues à revérifier,
  décisions d'arbitrage du §3b qui le concernent), la convention d'articles du §4, le format JSON du §5 avec le nom
  exact de son fichier, et les critères de vérification : (1) le JSON se charge
  (`python3 -c "import json;json.load(open('lots/releveur-A1-<m>.json'))"`) et contient `lignes` + `notes` ;
  (2) chaque `src` pointe vers une cellule/un libellé réellement lu ; (3) aucun code deux fois ; (4) toute ligne
  Détail du sous-lot est reprise ou dans `exclusions` ; (5) `p` et `h` à `null` ; (6) contrôle par feuille du §3a
  écrit en note. Le releveur termine en répondant seulement : nombre de lignes et liste code = q.

## 7. Phase 2 — consolidation (quand tu es relancé : « tes releveurs ont fini »)
1. Lis `lots/releveur-A1-1.json`, `-2.json`, `-3.json`. Pour **au moins 5 lignes de chaque releveur**, rouvre toi-même
   le fichier du kit cité dans `src` et vérifie la valeur ; note le score « A1-m : x/5 » dans tes notes. **Une erreur
   trouvée = tout le lot de ce releveur est revu** par toi, ligne par ligne, et corrigé.
2. Vérifie : aucun code deux fois ; chaque famille du §3a à portée I/E/R a sa ligne ; chaque code Détail du §3b est
   repris ou dans `exclusions` ; les familles 100 % CONSERVER (TV, GA) sont en note ; `p`/`h` à `null`.
3. Écris `lots/chef-A1.json` (format §5, avec `exclusions`), puis vérifie qu'il se charge en JSON (code de sortie 0).
   Dans les notes : découpage, efforts choisis et leur justification, scores x/5, contradictions plan/Détail.
4. Réponds seulement : nombre de lignes, liste code = q, et tes arbitrages en 5 lignes maximum.

**Maintenant (phase 1)** : lis, découpe, écris les 3 prompts dans `prompts/directeur-A/chef-1/`, et arrête-toi en
répondant « prompts prêts » avec l'effort de chaque releveur et sa justification d'une ligne.
