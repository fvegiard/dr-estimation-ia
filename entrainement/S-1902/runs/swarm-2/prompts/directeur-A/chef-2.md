effort: xhigh
modele: sonnet

# Chef de lot A2 — ÉCLAIRAGE, URGENCE, ALARME, MÉCANIQUE, DISTRIBUTION (essaim 2, chiffrage à l'aveugle S-1902, directeur A = QUANTITÉS)

Tu es le **chef de lot A2** (modèle Claude Sonnet 5.5, « sonnet ») d'une équipe hiérarchique d'estimation
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

- Tu as le droit de briefer **EXACTEMENT 3 subalternes, des releveurs de modèle « haiku »** : `A2-1`, `A2-2`,
  `A2-3`. Ni plus, ni moins.
- Tu écris leurs prompts dans le dossier **`prompts/directeur-A/chef-2/`** : `prompts/directeur-A/chef-2/releveur-1.md`,
  `prompts/directeur-A/chef-2/releveur-2.md`, `prompts/directeur-A/chef-2/releveur-3.md`. Chaque fichier commence
  EXACTEMENT par deux lignes : `effort: <low|medium|high|xhigh|max>` puis `modele: haiku`, puis le prompt complet.
- Chaque releveur écrit `lots/releveur-A2-1.json`, `lots/releveur-A2-2.json`, `lots/releveur-A2-3.json`.
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
- `reserves.md` : R-002 (portées), R-003 (luminaires typés : l'unité est l'ÉTIQUETTE ; LUMINAIRE E 3 vs 4),
  R-005 (pictogrammes Z6, détecteurs, encastrés d'urgence), Q12.
- `METHODE.md` §2 : lots fournisseur confirmés (éclairage A1 ×11, SL1 4′ ×12, 3′ ×15, 1′ ×6, trousses, E ×3, Z6 ×3 ;
  distribution NF 225 A 42 cct + EDB 1P ×20 + EJB 3P ×3 ; JCI + 2 détecteurs).
- `releve.xlsx` : feuilles `Par libellé` (Libellé, Famille, Quantité, Description, Source (légende)), `Par feuille`
  (Feuille (cartouche), Feuille (fichier), Libellé, Quantité), `Marques` (645 lignes : Feuille, Libellé, x, y,
  Source, Note — la colonne Note distingue p. ex. « existant pointillé » / « neuf (tracé plein) » / « anneau plein »).
- `entree/reference-Estimation_2.xlsx`, feuille `Détail` (en-têtes ligne 5 : Code, Description, Réf. plan, Qté,
  Unité, Prix mat. unit., Total mat., h / unité, Total h, Total MO, Total ligne, Notes / source quantité) et feuille
  `Sommaire` (note 6 : contradictions UTA-1 40 A vs MOCP 35 A ; détecteurs RDC vs étage). On ne garde que les
  **quantités** hors plan de Détail ; ses heures (« estimé Léna AI ») ne sont pas les heures du chiffrage.
- `entree/reference-Releve_Eclairage_Urgence.xlsx` (A1 11, C1 12, C1_1 6, C1_3 15, C-SUSP 20 rangées, E 4, Z6 3) et
  `entree/reference-Releve_Alarme_Incendie.xlsx` (AI-01…AI-09) : contrôles croisés.
- `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`) : articles 3.22 à 3.38.
- Le catalogue Dupuis n'est PAS nécessaire au lot A (pas de prix ni de temps).

## 3. Ton lot (disjoint des lots A1 et A3)

### 3a. Familles sur plan → codes `<FAM>-<P>` (P : I = installer, E = enlever, R = relocaliser)
Valeurs lues par le directeur — **à revérifier dans les fichiers**, pas à recopier de ce brief :

| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| ENCASTRE | ENC | 79 | CONSERVER 49, ENLEVER 26, RELOCALISER 4 | E201 28, E202 35, E204 16 | ENC-E 26, ENC-R 4 |
| ENCASTRE URGENCE | ENCU | 10 | CONSERVER 10 | E203 9, E204 1 | aucune (note, voir 3c) |
| LED 1X4 | L14 | 33 | CONSERVER 27, ENLEVER 6 | E102 1, E201 11, E202 21 | L14-E 6 |
| LED 2X2 | L22 | 94 | CONSERVER 86, ENLEVER 8 | E201 45, E204 49 | L22-E 8 |
| LED 4PI | L4 | 2 | CONSERVER 2 | E104 1, E105 1 | aucune (note) |
| LUMINAIRE LINEAIRE | LLIN | 4 | CONSERVER 4 | E203 2, E204 2 | aucune (note, voir 3c) |
| HP ENCASTRE PLAFOND | HP | 1 | ENLEVER 1 | E202 1 | HP-E 1 |
| LUMINAIRE A1 | LA1 | 11 | INSTALLER 11 | E203 11 | LA1-I 11 |
| LUMINAIRE C1 | LC1 | 12 | INSTALLER 12 | E203 12 | LC1-I 12 |
| LUMINAIRE C1_1 | LC11 | 6 | INSTALLER 6 | E203 6 | LC11-I 6 |
| LUMINAIRE C1_3 | LC13 | 15 | INSTALLER 15 | E203 15 | LC13-I 15 |
| LUMINAIRE E | LE | 3 | INSTALLER 3 | E203 3 | LE-I 3 |
| ENSEIGNE SORTIE Z6 | Z6 | 3 | INSTALLER 3 | E203 2, E204 1 | Z6-I 3 |
| DETECTEUR FUMEE | DF | 10 | CONSERVER 6, INSTALLER 2, RELOCALISER 1, ENLEVER 1 | E201 5, E203 5 | DF-I 2, DF-R 1, DF-E 1 |
| STATION MANUELLE | SM | 4 | CONSERVER 4 | E201 4 | aucune (note) |
| PANNEAU ANNONCIATEUR | PA | 1 | INSTALLER 1 | E203 1 | **PA-R 1** (arbitrage 3b) |
| MOTEUR MONOPHASE | MM | 9 | RELOCALISER 6, INSTALLER 3 | E103 6, E105 3 | MM-R 6, MM-I 3 |
| MOTEUR TRIPHASE | MT | 9 | CONSERVER 5, INSTALLER 4 | E102 5, E105 2, E106 2 | MT-I 4 |

Le `src` de chaque ligne donne la répartition par feuille, p. ex.
`"releve.xlsx Par libellé LUMINAIRE A1 11 ; rapport-releve.md INSTALLER 11 ; Par feuille E203 11 ; relevé éclairage A1 11"`.

### 3b. Lignes de la feuille `Détail` attribuées à A2 (chacune : reprise OU exclue, jamais oubliée)
Arbitrages tranchés par le directeur (règle : **le plan gagne sur Détail pour les quantités** ; une ligne Détail
qui recompte un objet déjà relevé sur plan est un DOUBLE COMPTE → `exclusions` avec la ligne sur plan qui la
remplace ; la contradiction de quantité va en note). Si la lecture des fichiers contredit une hypothèse marquée
« vérifier », le releveur/le chef reprend la ligne et explique en note au lieu de l'exclure.

| Code Détail | Décision | Remplacée par / remarque |
|---|---|---|
| A-01 (39 u, démantèlement luminaires RDC E.A.E) | EXCLURE | ENC-E, L14-E, L22-E — noter 39 + 7 (A-02) = 46 Détail vs 26 + 6 + 8 = 40 sur plan |
| A-02 (7 u, démantèlement luminaires 2e) | EXCLURE | idem A-01 |
| A-06 (7 u, relocalisation luminaires E.A.R, dont 4 salle 227) | EXCLURE | ENC-R — noter 7 Détail vs 4 sur plan |
| F-01 (11 luminaires A1) | EXCLURE | LA1-I |
| F-02 (12 C1) | EXCLURE | LC1-I |
| F-03 (6 C1_1) | EXCLURE | LC11-I |
| F-04 (15 C1_3) | EXCLURE | LC13-I |
| F-06 (4 luminaires E) | EXCLURE | LE-I **3** (3 étiquettes sur plan, lot éclairage E ×3 ; R-003) — noter 4 Détail / relevé éclairage vs 3 retenus |
| F-07 (3 enseignes Z6) | EXCLURE | Z6-I |
| G-01 (2 détecteurs de fumée adressables) | EXCLURE | DF-I 2 (fourniture des 2 détecteurs = lot LOT-DET, traité par A3) |
| G-04 (1 u relocalisation panneau annonciateur Simplex, note 1 E-007) | EXCLURE | **PA-R 1** : le PANNEAU ANNONCIATEUR « INSTALLER 1 » de E203 est le nouvel emplacement de l'annonciateur existant relocalisé (G-04, relevé AI AI-05 « Relocalisation annonciateur Simplex existant », bordereau 3.37 « déplacement annonciateur ») → un seul objet physique ; code PA-R (pas PA-I), q 1, art 3.37, src citant rapport-releve.md INSTALLER 1 + Détail G-04 + AI-05 |
| A-10 (6 u toit : débrancher, entreposer sectionneurs, rebrancher équipements de ventilation E.A.R, E-103/E-106) | EXCLURE | **MM-R 6** (6 MOTEUR MONOPHASE RELOCALISER sur E103 = les « 6 E.A.R sur E-103 » de A-10) — reporter la description de A-10 dans le `desc`/`src` de MM-R |
| C-01 (UTA-01 au toit, E-106) | EXCLURE | **MT-I** (vérifier : 2 MOTEUR TRIPHASE INSTALLER sur E106 = UTA-01 + VE-02N) |
| C-02 (VE-02N au toit, E-106) | EXCLURE | **MT-I** (idem) |
| C-03 (2 chaudières CH-01/CH-02, E-105) | EXCLURE | **MT-I** (vérifier : 2 MOTEUR TRIPHASE sur E105) — MT-I 4 = C-01 + C-02 + C-03 ×2 |
| C-04 (3 humidificateurs HUM-1/2/3 120 V/1Ø, E-105) | EXCLURE | **MM-I 3** (vérifier : 3 MOTEUR MONOPHASE INSTALLER sur E105) ; le sectionneur sans fusible 30 A de C-04 n'est pas un symbole relevé → ligne **X-03** ci-dessous |
| X-03 (nouvelle, hors Détail) | REPRENDRE `X-03`, q 3, u U, art 3.23 | « Sectionneur sans fusible 30 A — HUM-1/2/3 » ; src « Détail C-04 (sectionneur sans fusible 30A 1Ø ×3) ; Matériel Lumen HUBHBL1372 qté 3 » |
| A-08 (21 u FabLab 210 : retrait temporaire + réinstallation luminaires linéaires existants) | REPRENDRE `A-08`, q 21, u U, art 3.35 | appareils CONSERVER sur plan (travail temporaire, pas un double) ; noter chevauchement possible avec L14-E/ENC-E/ENC-R de E202 |
| A-09 (24 u FabLab 210 : retrait temporaire + réinstallation encastrés existants, « ±2 ») | REPRENDRE `A-09`, q 24, u U, art 3.35 | idem, noter « ±2 » de Détail |
| B-01 (1 u panneau PP-3 neuf 225 A 42 cct) | REPRENDRE `B-01`, q 1, u U, art 3.24 | matériel = LOT-DIST (A3) ; cette ligne porte la quantité de pose |
| B-02 (14 disj. 1P-15A transférés) | REPRENDRE, u U, art 3.25 | |
| B-03 (1 disj. 3P-20A) | REPRENDRE, art 3.25 | |
| B-04 (1 disj. 3P-40A UTA-1) | REPRENDRE, art 3.25 | noter contradiction 40 A (E-502) vs MOCP 35 A (E-009) |
| B-05 (1 disj. 3P-15A VE-2N) | REPRENDRE, art 3.25 | |
| B-06 (1 disj. 1P-15A DDFT fontaine) | REPRENDRE, art 3.25 | |
| B-07 (2 disj. 1P-15A) | REPRENDRE, art 3.25 | |
| B-08 (2 disj. 1P-20A) | REPRENDRE, art 3.25 | noter : 1P B-02 + B-06 + B-07 + B-08 = 19 vs lot distribution EDB 1P ×20 ; 3P B-03 + B-04 + B-05 = 3 = EJB 3P ×3 |
| B-09 (9 u mise à jour fiches dactylographiées + identification) | REPRENDRE, u U, art 3.24 | |
| F-05 (20 rangées linéaires Axis : suspension + alimentation de rangée) | REPRENDRE `F-05`, q 20, u U (rangée), art 3.35 | travail de rangée, distinct des modules LC1/LC11/LC13 ; recoupe C-SUSP 20 du relevé éclairage ; noter « ≈20 » |
| F-10 (1 lot JB éclairage, chaînes de retenue, quincaillerie) | REPRENDRE `F-10`, q 1, u LOT, art 3.35 | |
| G-05 (1 lot démontage/protection/réinstallation dispositifs AI existants) | REPRENDRE `G-05`, q 1, u LOT, art 3.36 | noter chevauchement possible avec DF-R 1 / DF-E 1 |
| G-06 (1 lot assistance électricien programmation/vérification ULC-S537) | REPRENDRE `G-06`, q 1, u LOT, art 3.38 | |

Les autres lignes Détail (A-03…A-05, A-07, A-11, C-05…C-08, D-, E-, F-08, F-09, G-02, G-03, G-07, H-, OPT-)
appartiennent aux lots A1 et A3 : ne les traite pas.

### 3c. Points à noter (sans changer les quantités)
- ENCU : 10 CONSERVER, mais `Marques` montre 3 « anneau plein » (neufs ?) et 7 « existant pointillé » ; F-01 dit
  « dont 3 [A1] sur circuit PP-U1 » → les 3 anneaux pleins sont probablement les 3 A1 sur PP-U1 déjà comptés dans
  LA1-I 11 : aucune ligne ENCU, note seulement.
- LLIN : 4 CONSERVER (E203 2, E204 2) alors que E203 porte les rangées Axis neuves → note (aucune ligne).
- DF : `Marques` distingue « existant (tracé pointillé) » ×3, « neuf (tracé plein) » ×1, bloc S146 ×6 ; rapport :
  I2 R1 E1 C6 → le rapport fait foi ; noter l'écart éventuel. Relevé AI : 2 détecteurs neufs au RDC (plans prévalent
  sur le schéma E-007).

## 4. Articles du bordereau à proposer (`art`, texte)
3.22 Démontage des éléments électriques · 3.23 Raccordement des équipements mécaniques · 3.24 Nouveau panneau 600V ·
3.25 Lot disjoncteurs · 3.35 Appareil de contrôle + appareils d'éclairage · 3.36 Détecteur de fumée · 3.37 Panneau
alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie : mise en marche et certification.
Convention du directeur A : toute ligne `-E` → **3.22** (HP-E et DF-E compris) ; ENC-R → 3.35 ; luminaires neufs et
Z6 → 3.35 ; DF-I, DF-R → 3.36 ; PA-R → 3.37 ; MM-*, MT-*, X-03 → 3.23 ; lignes Détail → l'article du tableau 3b.

## 5. Format de sortie (pour tes releveurs et pour toi)
```json
{
  "niveau": "releveur",
  "nom": "A2-1",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "LA1-I", "desc": "Luminaire A1 Cooper 24CGTS 2'x4' encastré 347 V — neuf", "q": 11, "u": "U", "p": null, "h": null,
     "art": "3.35", "src": "releve.xlsx Par libellé LUMINAIRE A1 11 ; rapport-releve.md INSTALLER 11 ; Par feuille E203 11"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contradictions plan/Détail"],
  "exclusions": [{"code": "F-01", "raison": "double compte : 11 luminaires A1 déjà relevés sur plan — remplacée par LA1-I"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte ; `src` exact et vérifiable (fichier, feuille,
libellé ou code, valeur lue). Releveurs → `lots/releveur-A2-<m>.json` ; toi → `lots/chef-A2.json`
(`"niveau": "chef"`, `"nom": "A2"`, `"modele_demande": "sonnet"`, `"effort_demande": "xhigh"`).

## 6. Découpage et choix d'effort (phase 1)
- Découpe ton lot (§3a + §3b, + X-03) en **3 sous-lots disjoints** (aucune famille ni aucun code dans deux sous-lots)
  **et couvrants** (tout est attribué). Garde ensemble ce qui s'arbitre ensemble (MM/MT avec A-10, C-01…C-04, X-03 ;
  PA avec G-04 ; DF avec G-01, G-05, G-06 ; luminaires neufs avec F-01…F-07). Suggestion non imposée :
  A2-1 = ENC, ENCU, L14, L22, L4, LLIN, HP + A-01, A-02, A-06, A-08, A-09 ;
  A2-2 = LA1, LC1, LC11, LC13, LE, Z6 + F-01…F-07, F-10 ;
  A2-3 = DF, SM, PA, MM, MT + G-01, G-04, G-05, G-06, A-10, C-01…C-04, X-03, B-01…B-09.
  Écris la liste du découpage dans ta réponse de phase 1 et dans les notes de `lots/chef-A2.json`.
- Choisis l'effort de chaque releveur (`low` recopie mécanique d'un petit tableau ; `medium` comptage/recherche
  simple ; `high` arbitrage de portées, doublons, libellés approximatifs ; `xhigh` quand une erreur se propage à tout
  le chiffrage ; `max` réservé aux consolidations finales). Nos moyens ne sont pas comptés : choisis ce qui maximise
  la justesse. Justifie chaque choix d'une ligne (réponse de phase 1 + notes de phase 2).
- Chaque prompt de releveur contient, dans cet ordre : son rôle et son nom (« releveur A2-3 »), les RÈGLES
  D'AVEUGLE mot pour mot, le dossier de travail, la mécanique (il ne délègue à personne, écrit son JSON, s'arrête),
  son sous-lot précis (familles et codes, fichiers/feuilles/colonnes à lire, valeurs attendues à revérifier, les
  décisions d'arbitrage du §3b/§3c qui le concernent, recopiées en entier), la convention d'articles du §4, le
  format JSON du §5 avec le nom exact de son fichier, et les critères de vérification : (1) le JSON se charge
  (`python3 -c "import json;json.load(open('lots/releveur-A2-<m>.json'))"`) et contient `lignes` + `notes` ;
  (2) chaque `src` pointe vers une cellule/un libellé réellement lu ; (3) aucun code deux fois ; (4) toute ligne
  Détail du sous-lot est reprise ou dans `exclusions` (avec la ligne sur plan qui la remplace) ; (5) `p` et `h` à
  `null`. Le releveur termine en répondant seulement : nombre de lignes et liste code = q.

## 7. Phase 2 — consolidation (quand tu es relancé : « tes releveurs ont fini »)
1. Lis `lots/releveur-A2-1.json`, `-2.json`, `-3.json`. Pour **au moins 5 lignes de chaque releveur**, rouvre toi-même
   le fichier du kit cité dans `src` et vérifie la valeur ; note le score « A2-m : x/5 » dans tes notes. **Une erreur
   trouvée = tout le lot de ce releveur est revu** par toi, ligne par ligne, et corrigé.
2. Vérifie : aucun code deux fois ; chaque famille du §3a à portée I/E/R a sa ligne (PA par PA-R) ; chaque code
   Détail du §3b est repris ou dans `exclusions` ; les familles 100 % CONSERVER (ENCU, L4, LLIN, SM) sont en note ;
   LE-I = 3 ; `p`/`h` à `null`.
3. Écris `lots/chef-A2.json` (format §5, avec `exclusions`), puis vérifie qu'il se charge en JSON (code de sortie 0).
   Dans les notes : découpage, efforts choisis et leur justification, scores x/5, contradictions plan/Détail.
4. Réponds seulement : nombre de lignes, liste code = q, et tes arbitrages en 5 lignes maximum.

**Maintenant (phase 1)** : lis, découpe, écris les 3 prompts dans `prompts/directeur-A/chef-2/`, et arrête-toi en
répondant « prompts prêts » avec l'effort de chaque releveur et sa justification d'une ligne.
