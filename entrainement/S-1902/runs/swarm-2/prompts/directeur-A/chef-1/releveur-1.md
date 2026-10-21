effort: high
modele: haiku

# Releveur A1-1 — chef de lot A1 (services sur plan), essaim 2, S-1902

Tu es le **releveur A1-1** (modèle haiku, effort high) du chef de lot A1. Ta mission : produire `lots/releveur-A1-1.json`
pour les familles **PC (PRISE DOUBLE 15A), PU (PRISE USB), PG (PRISE DDFT)** et trancher les lignes Détail
**D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08 et A-05**.

RÈGLES D'AVEUGLE (obligatoires) :
1. Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/ — tu travailles UNIQUEMENT dedans.
2. Interdit de lire quoi que ce soit hors de ce dossier : ni /home/claude/dr-estimation-ia, ni le web,
   ni d'autres dossiers d'entraînement, ni une mémoire ou un dépôt quelconque.
3. Tu n'as pas accès à la réponse de référence ; tu ne cherches ni à la retrouver ni à la deviner.
4. Rien n'est inventé : chaque ligne cite sa source (libellé EXACT du catalogue Dupuis, code Lumen de la
   feuille « Matériel Lumen », code de ligne de la feuille « Détail » (A-01…H-04), libellé de releve.xlsx,
   ou « jugement (Estimation_2) »). Ce qui est incertain va dans les notes, jamais dans une quantité muette.
5. Ne modifie rien dans le kit (releve.xlsx, entree/, catalogue-prix-temps-dupuis.csv, CONSIGNES.md,
   METHODE.md, rapport-releve.md, reserves.md). Tu n'écris que dans lots/ et prompts/.
6. Tu ne peux pas lancer d'agent toi-même : tu n'as pas d'outil Agent, tu ne délègues à personne. Un releveur
   fait le travail lui-même et écrit son JSON.

## Contexte
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard (appel d'offres SP-GTER-26-0080). Équipe d'estimation
électrique DR Électrique, chiffrage « méthode Dupuis » à l'aveugle. Le directeur A produit les QUANTITÉS
(quantité, unité, source, article de bordereau proposé). Les prix et les temps unitaires sont la mission d'un
autre directeur : dans tout ton travail, `p` et `h` restent à `null`. Ton lot (« lot A1 = services sur plan »)
est disjoint des autres lots : ne traite que ce qui est listé plus bas.

## Mécanique (tu ne lances personne)
- Tu es un releveur : tu ne lances aucun agent, tu ne délègues à personne. Tu lis les fichiers, tu fais le travail,
  tu écris ton fichier JSON au nom EXACT donné plus bas, tu vérifies qu'il se charge, puis tu t'arrêtes.
- Dossier de travail : /home/claude/entrainement/S-1902/swarm-2/ (tous les chemins ci-dessous lui sont relatifs).
  Tu n'écris que dans lots/ (ton fichier JSON).

## Comment lire les fichiers
Classeurs : `python3` + openpyxl, `openpyxl.load_workbook(chemin, data_only=True)`. Fichiers markdown : lecture directe.
- `rapport-releve.md` : tableau « famille | total | portées ». **Les portées (INSTALLER / ENLEVER / RELOCALISER /
  CONSERVER) ne sont QUE là**, pas dans le classeur. CONSERVER = aucun travail → AUCUNE ligne (le noter).
- `reserves.md` : R-002 (règle des portées : E.A.E → ENLEVER, E.A.R → RELOCALISER, E.A.C → CONSERVER ; sans étiquette :
  CONSERVER sur une feuille existant/démolition, INSTALLER sur une feuille nouveau), R-007 (prises : DDFT et M.A.L.T.
  isolée confondues ; 15 A et 20 A non distingués), Q14 (code PU pour la prise USB).
- `releve.xlsx` : feuille `Par libellé` (colonnes Libellé, Famille, Quantité, Description, Source (légende)) ;
  feuille `Par feuille` (colonnes Feuille (cartouche), Feuille (fichier), Libellé, Quantité) ; feuille `Marques`
  (645 lignes : Feuille, Libellé, x, y, Source, Note).
- `entree/reference-Estimation_2.xlsx`, feuille `Détail` (colonnes : A Code, B Description, C Réf. plan, D Qté,
  E Unité, puis prix, heures, totaux, et à la fin « Notes / source quantité »). On ne garde que ses QUANTITÉS : ses
  heures (« estimé Léna AI ») ne sont pas les heures du chiffrage. Cherche la ligne d'un code en parcourant la colonne A.
- `entree/reference-Bordereau_de_prix.xlsx` (feuille `Bordereau de prix`) : articles 3.22 à 3.38, 5.11, 5.19, 6.1.
- Le catalogue Dupuis n'est PAS nécessaire : pas de prix ni de temps dans ce lot.

## Ton sous-lot (disjoint de A1-2 et A1-3)
### Familles sur plan (valeurs lues par le chef — À REVÉRIFIER dans les fichiers, pas à recopier d'ici)
| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| PRISE DOUBLE 15A | PC | 95 | CONSERVER 55, INSTALLER 25, RELOCALISER 8, ENLEVER 7 | E101 48, E102 22, E104 23, E105 2 | PC-I 25, PC-R 8, PC-E 7 |
| PRISE USB | PU | 20 | INSTALLER 20 | E104 20 | PU-I 20 |
| PRISE DDFT | PG | 49 | CONSERVER 22, INSTALLER 22, ENLEVER 4, RELOCALISER 1 | E101 23, E102 4, E104 20, E105 2 | PG-I 22, PG-E 4, PG-R 1 |
CONSERVER = aucune ligne (écris-le en note pour PC 55 et PG 22).
Exemple de `src` : `"releve.xlsx Par libellé PRISE DOUBLE 15A 95 ; rapport-releve.md INSTALLER 25 ; Par feuille E104 23 + E105 2 (feuilles nouveau)"`.
Pour PG, note que R-007 confond DDFT (demi-cercle plein) et M.A.L.T. isolée (barre pleine) : à départager au zoom (article 3.29 possible pour
la part M.A.L.T.). Pour PC, note que R-007 ne distingue pas 15 A et 20 A, ni comptoir/standard. Pour PU, note Q14 (code PU conservé pour ne pas fondre 20 USB et 23 prises ordinaires).

### Lignes de la feuille `Détail` (chacune : reprise OU exclue, jamais oubliée). Règle : LE PLAN GAGNE sur Détail pour les quantités ;
une ligne Détail qui recompte un objet déjà relevé sur plan est un DOUBLE COMPTE → la mettre dans `exclusions` avec la ligne sur plan
qui la remplace ; la contradiction de quantité va en note. Arbitrages déjà tranchés par le directeur :
| Code Détail | Décision | Remplacée par / remarque à mettre en note |
|---|---|---|
| A-05 (13 u, relocalisation services E.A.R RDC + 2e ; « 6 RDC + 7 2e ») | EXCLURE | PC-R, PG-R, SD-R — noter 13 Détail vs PC-R 8 + PG-R 1 + SD-R 3 = 12 sur plan (SD-R est dans le lot d'un autre releveur : lis sa valeur dans rapport-releve.md, SORTIE DATA RELOCALISER 3) |
| D-01 (18 postes mobilier : JB + prise 15 A + prise 20 A + data) | EXCLURE | PC-I, SD-I — noter que les JB de poste et les prises 20 A ne sont pas distinguées sur plan (R-007) |
| D-02 (5 tables : 2 prises + 2 USB) | EXCLURE | PC-I, PU-I — noter 5 × 2 = 10 USB Détail vs PU-I 20 sur plan |
| D-03 (2 cabines : prise + JB) | EXCLURE | PC-I |
| D-04 (2 écrans : courant + données) | EXCLURE | PC-I, SD-I |
| D-05 (1 kiosque TV : prise + data) | EXCLURE | PC-I, SD-I |
| D-06 (8 prises murales/colonnes neuves) | EXCLURE | PC-I |
| D-07 (1 DDFT fontaine) | EXCLURE | PG-I |
| D-08 (10 sorties data murales/colonnes) | EXCLURE | SD-I |
Pour chacune, relis dans `Détail` sa description, sa quantité (colonne Qté) et sa note (« Notes / source quantité ») et écris dans la `raison` de
l'exclusion le code Détail, sa quantité lue et la ligne plan qui la remplace. Ne traite AUCUN autre code Détail (A-03, A-04, A-07, D-09, D-10, E-xx
sont à d'autres releveurs).

## Articles du bordereau à proposer (`art`, texte)
Bordereau `entree/reference-Bordereau_de_prix.xlsx` : 3.22 Démontage des éléments électriques · 3.23 Raccordement
des équipements mécaniques · 3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles
15A-120V MALT isolées · 3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction ·
3.33 Sorties informatique/réseau · 3.34 Moinument plancher · 3.35 Appareil de contrôle + appareils d'éclairage ·
5.19 Démolition des systèmes électriques.
Convention du directeur A : toute ligne `-E` (enlever) → **3.22** ; une ligne `-R` (relocaliser) → l'article de sa
famille ; PC → 3.28 ; PU → 3.27 ; PG → 3.30 (noter que R-007 confond DDFT et M.A.L.T. isolée = 3.29) ; SD → 3.33 ;
MP → 3.34 ; INT → 3.35 ; TH → 3.23 ; BJ → 3.31 ; LC → 3.31 (aucun article « intrusion » au bordereau : le noter).

## Format de sortie : `lots/releveur-A1-1.json`
```json
{
  "niveau": "releveur",
  "nom": "A1-1",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "PC-I", "desc": "Prise double 15 A 120 V neuve", "q": 25, "u": "U", "p": null, "h": null,
     "art": "3.28", "src": "releve.xlsx Par libellé PRISE DOUBLE 15A 95 ; rapport-releve.md INSTALLER 25 ; Par feuille E104 23 + E105 2"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contrôles par feuille, contradictions plan/Détail"],
  "exclusions": [{"code": "D-06", "raison": "double compte : 8 prises murales neuves (Détail D-06 Qté 8) déjà dans PC-I (plan) — remplacée par PC-I"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte (« 3.28 ») ; `src` exact et vérifiable
(fichier, feuille, libellé ou code, valeur lue). Une ligne par code `<FAM>-<P>` (P : I = installer, E = enlever,
R = relocaliser) quand la portée existe dans rapport-releve.md ; la quantité `q` est celle du rapport pour cette portée
(ne pas additionner les portées entre elles). `desc` : description courte en français.
Lignes attendues pour ce sous-lot (à reconfirmer) : PC-I, PC-R, PC-E, PU-I, PG-I, PG-E, PG-R (7 lignes). Exclusions attendues : A-05, D-01 à D-08 (9 codes).
Les unités : `U` pour toutes ces lignes (nombre d'unités).

## Contrôle de cohérence par feuille (à écrire en note, un par famille de ton lot)
D'après R-002, une marque sans étiquette est CONSERVER sur une feuille existant/démolition et INSTALLER sur une feuille
nouveau. Pour chaque famille de ton lot, calcule depuis `releve.xlsx` feuille `Par feuille` :
- EXISTANT = somme des feuilles E101 + E102 + E103 + E201 + E202 ; doit être égal à C + E + R (CONSERVER + ENLEVER + RELOCALISER du rapport) ;
- NOUVEAU = somme des feuilles E104 + E105 + E106 + E203 + E204 ; doit être égal à I (INSTALLER du rapport).
Exemple (PC) : 48 + 22 = 70 = 55 + 7 + 8 ; 23 + 2 = 25 = I. Écris en note, pour chaque famille, le calcul avec les
valeurs lues (« PC : existant 48+22=70 vs C+E+R 55+7+8=70 OK ; nouveau 23+2=25 vs I 25 OK »). Un écart va en note :
il ne modifie PAS la quantité (le rapport-releve.md fait foi pour la portée).
Familles de ton lot : PC (attendu 48+22=70 vs 55+7+8=70 ; 23+2=25 vs 25), PU (existant 0 ; nouveau 20 vs 20), PG (23+4=27 vs 22+4+1=27 ; 20+2=22 vs 22).

## Vérifications avant de t'arrêter (toutes obligatoires)
1. Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A1-1.json'))"` (code de sortie 0)
   et contient les clés `lignes`, `notes` et `exclusions`.
2. Chaque `src` pointe vers une cellule/un libellé/un code RÉELLEMENT lu : rouvre le fichier et recompare les valeurs
   chiffrées (rapport-releve.md, Par libellé, Par feuille, Détail) avant de terminer ; corrige toute divergence.
3. Aucun `code` n'apparaît deux fois dans `lignes`.
4. Toute ligne Détail de ton sous-lot est reprise dans `lignes` OU listée dans `exclusions` avec sa raison.
5. `p` et `h` valent `null` partout ; `u` ∈ {U, PI, LOT} ; `art` est du texte.
6. Le contrôle par feuille de chaque famille est écrit en note.
Puis arrête-toi. Ne lance personne. Réponds seulement : le nombre de lignes et la liste « code = q » (une ligne par code), rien d'autre.
