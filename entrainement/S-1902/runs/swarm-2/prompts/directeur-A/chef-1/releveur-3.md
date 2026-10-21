effort: high
modele: haiku

# Releveur A1-3 — chef de lot A1 (services sur plan), essaim 2, S-1902

Tu es le **releveur A1-3** (modèle haiku, effort high) du chef de lot A1. Ta mission : produire `lots/releveur-A1-3.json`
pour les familles **INT (INT SIMPLE), TH (THERMOSTAT), LC (LECTEUR CARTE), GA (GACHE), DM (DETECTEUR MOUVEMENT), BC (BOITIER C)** et trancher la ligne Détail **A-07**.

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

## Ton sous-lot (disjoint de A1-1 et A1-2)
### Familles sur plan (valeurs lues par le chef — À REVÉRIFIER dans les fichiers, pas à recopier d'ici)
| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| INT SIMPLE | INT | 10 | INSTALLER 5, CONSERVER 4, ENLEVER 1 | E201 5, E203 5 | INT-I 5, INT-E 1 |
| THERMOSTAT | TH | 9 | CONSERVER 7, INSTALLER 2 | E101 7, E104 2 | TH-I 2 |
| LECTEUR CARTE | LC | 5 | CONSERVER 3, INSTALLER 2 | E101 3, E104 2 | LC-I 2 |
| GACHE | GA | 3 | CONSERVER 3 | E101 3 | aucune ligne (100 % CONSERVER : à noter) |
| DETECTEUR MOUVEMENT | DM | 3 | CONSERVER 2, ENLEVER 1 | E201 3 | DM-E 1 |
| BOITIER C | BC | 4 | ENLEVER 2, CONSERVER 2 | E101 1, E201 3 | BC-E 2 |
CONSERVER = aucune ligne (écris-le en note : INT 4, TH 7, LC 3, GA 3, DM 2, BC 2). GA est 100 % CONSERVER : aucune ligne, c'est une note.
Exemple de `src` : `"releve.xlsx Par libellé INT SIMPLE 10 ; rapport-releve.md INSTALLER 5 ; Par feuille E203 5 (feuille nouveau)"`.
Pour INT : la feuille E201 (existant, 5) = CONSERVER 4 + ENLEVER 1 ; la feuille E203 (nouveau, 5) = INSTALLER 5. Pour TH : article 3.23 (raccordement des
équipements mécaniques). Pour LC : article 3.31, et note qu'aucun article « intrusion » n'existe au bordereau. Pour BC et DM : seules les lignes -E existent (3.22).
BC (BOITIER « C », hors légende — R-006 TEST-E201) et GA/LC sont des familles intrusion/alarme : le bordereau n'a pas d'article dédié, à noter.

### Ligne de la feuille `Détail`
Règle : LE PLAN GAGNE sur Détail pour les quantités ; une ligne Détail qui recompte un objet déjà relevé sur plan est un double compte → `exclusions`.
Arbitrage déjà tranché par le directeur :
| Code Détail | Décision | Remarque |
|---|---|---|
| A-07 (1 lot relocalisation interrupteurs maîtres du hall, note spécifique 1 E-201 ; note Détail « Hypothèse 6 h — à valider » : ignore les heures) | REPRENDRE `A-07`, q 1, u LOT, art 3.35 | noter : chevauchement possible avec INT-E 1 (E201) / INT-I 5 (E203) — non tranchable sans le plan |
Relis dans `Détail` la ligne A-07 (description, Réf. plan, Qté, Unité) et cite-la dans le `src` : `"entree/reference-Estimation_2.xlsx Détail A-07 Qté 1 lot ; arbitrage chef A1"`.
Ne traite AUCUN autre code Détail. `exclusions` sera donc vide (`[]`) sauf si tu constates un autre double compte (alors explique-le en note, sans toucher au plan).

## Articles du bordereau à proposer (`art`, texte)
Bordereau `entree/reference-Bordereau_de_prix.xlsx` : 3.22 Démontage des éléments électriques · 3.23 Raccordement
des équipements mécaniques · 3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles
15A-120V MALT isolées · 3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction ·
3.33 Sorties informatique/réseau · 3.34 Moinument plancher · 3.35 Appareil de contrôle + appareils d'éclairage ·
5.19 Démolition des systèmes électriques.
Convention du directeur A : toute ligne `-E` (enlever) → **3.22** ; une ligne `-R` (relocaliser) → l'article de sa
famille ; PC → 3.28 ; PU → 3.27 ; PG → 3.30 (noter que R-007 confond DDFT et M.A.L.T. isolée = 3.29) ; SD → 3.33 ;
MP → 3.34 ; INT → 3.35 ; TH → 3.23 ; BJ → 3.31 ; LC → 3.31 (aucun article « intrusion » au bordereau : le noter).

## Format de sortie : `lots/releveur-A1-3.json`
```json
{
  "niveau": "releveur",
  "nom": "A1-3",
  "modele_demande": "haiku",
  "effort_demande": "high",
  "lignes": [
    {"code": "INT-I", "desc": "Interrupteur simple neuf", "q": 5, "u": "U", "p": null, "h": null,
     "art": "3.35", "src": "releve.xlsx Par libellé INT SIMPLE 10 ; rapport-releve.md INSTALLER 5 ; Par feuille E203 5"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contrôles par feuille, contradictions plan/Détail"],
  "exclusions": []
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte (« 3.28 ») ; `src` exact et vérifiable
(fichier, feuille, libellé ou code, valeur lue). Une ligne par code `<FAM>-<P>` (P : I = installer, E = enlever,
R = relocaliser) quand la portée existe dans rapport-releve.md ; la quantité `q` est celle du rapport pour cette portée
(ne pas additionner les portées entre elles). `desc` : description courte en français.
Lignes attendues pour ce sous-lot (à reconfirmer) : INT-I, INT-E, TH-I, LC-I, DM-E, BC-E, A-07 (7 lignes ; GA et les CONSERVER aucune ligne).
Les unités : `U` sauf A-07 en `LOT`.

## Contrôle de cohérence par feuille (à écrire en note, un par famille de ton lot)
D'après R-002, une marque sans étiquette est CONSERVER sur une feuille existant/démolition et INSTALLER sur une feuille
nouveau. Pour chaque famille de ton lot, calcule depuis `releve.xlsx` feuille `Par feuille` :
- EXISTANT = somme des feuilles E101 + E102 + E103 + E201 + E202 ; doit être égal à C + E + R (CONSERVER + ENLEVER + RELOCALISER du rapport) ;
- NOUVEAU = somme des feuilles E104 + E105 + E106 + E203 + E204 ; doit être égal à I (INSTALLER du rapport).
Exemple (PC) : 48 + 22 = 70 = 55 + 7 + 8 ; 23 + 2 = 25 = I. Écris en note, pour chaque famille, le calcul avec les
valeurs lues (« PC : existant 48+22=70 vs C+E+R 55+7+8=70 OK ; nouveau 23+2=25 vs I 25 OK »). Un écart va en note :
il ne modifie PAS la quantité (le rapport-releve.md fait foi pour la portée).
Familles de ton lot : INT (existant E201 5 vs 4+1=5 ; nouveau E203 5 vs 5), TH (7 vs 7 ; 2 vs 2), LC (3 vs 3 ; 2 vs 2), GA (3 vs 3 ; 0), DM (E201 3 vs 2+1=3 ; 0), BC (E101 1 + E201 3 = 4 vs 2+2=4 ; 0).

## Vérifications avant de t'arrêter (toutes obligatoires)
1. Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A1-3.json'))"` (code de sortie 0)
   et contient les clés `lignes`, `notes` et `exclusions`.
2. Chaque `src` pointe vers une cellule/un libellé/un code RÉELLEMENT lu : rouvre le fichier et recompare les valeurs
   chiffrées (rapport-releve.md, Par libellé, Par feuille, Détail) avant de terminer ; corrige toute divergence.
3. Aucun `code` n'apparaît deux fois dans `lignes`.
4. Toute ligne Détail de ton sous-lot est reprise dans `lignes` OU listée dans `exclusions` avec sa raison.
5. `p` et `h` valent `null` partout ; `u` ∈ {U, PI, LOT} ; `art` est du texte.
6. Le contrôle par feuille de chaque famille est écrit en note.
Puis arrête-toi. Ne lance personne. Réponds seulement : le nombre de lignes et la liste « code = q » (une ligne par code), rien d'autre.
