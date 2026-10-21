effort: xhigh
modele: haiku

# Releveur A1-2 — chef de lot A1 (services sur plan), essaim 2, S-1902

Tu es le **releveur A1-2** (modèle haiku, effort xhigh) du chef de lot A1. Ta mission : produire `lots/releveur-A1-2.json`
pour les familles **SD (SORTIE DATA), TV (SORTIE TV), MP (MONUMENT PLANCHER), BJ (BOITE JONCTION)** et trancher les lignes Détail
**A-03, A-04, D-09, D-10, E-01, E-02, E-03, E-04 et E-05**.

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

## Ton sous-lot (disjoint de A1-1 et A1-3)
### Familles sur plan (valeurs lues par le chef — À REVÉRIFIER dans les fichiers, pas à recopier d'ici)
| Libellé releve.xlsx | FAM | total | portées (rapport-releve.md) | Par feuille | lignes attendues |
|---|---|--:|---|---|---|
| SORTIE DATA | SD | 120 | INSTALLER 65, CONSERVER 35, ENLEVER 17, RELOCALISER 3 | E101 36, E102 19, E104 45, E105 20 | SD-I 65, SD-E 17, SD-R 3 |
| SORTIE TV | TV | 4 | CONSERVER 4 | E101 1, E102 3 | aucune ligne (100 % CONSERVER : à noter) |
| BOITE JONCTION | BJ | 10 | CONSERVER 5, INSTALLER 3, ENLEVER 2 | E101 4, E102 1, E104 3, E201 2 | BJ-I 3, BJ-E 2 |
| MONUMENT PLANCHER | MP | 7 | ENLEVER 3, INSTALLER 3, CONSERVER 1 | E101 1, E102 3, E105 3 | MP-I 3, MP-E 3 |
CONSERVER = aucune ligne (écris-le en note : SD 35, BJ 5, MP 1, TV 4). TV et GA sont 100 % CONSERVER : TV n'a aucune ligne, c'est une note.
Exemple de `src` : `"releve.xlsx Par libellé SORTIE DATA 120 ; rapport-releve.md INSTALLER 65 ; Par feuille E104 45 + E105 20 (feuilles nouveau)"`.
Note R-006 : sorties data = triangle plein ≤ 6,5 pt seulement (les grandes flèches sont des renvois de circuit).

### Lignes de la feuille `Détail` (chacune : reprise OU exclue, jamais oubliée). Règle : LE PLAN GAGNE sur Détail pour les quantités ;
une ligne Détail qui recompte un objet déjà relevé sur plan est un DOUBLE COMPTE → la mettre dans `exclusions` avec la ligne sur plan
qui la remplace ; la contradiction de quantité va en note. Arbitrages déjà tranchés par le directeur :
| Code Détail | Décision | Remplacée par / remarque à mettre en note |
|---|---|---|
| A-03 (34 u, démantèlement services RDC E.A.E, note « Compte E.A.E E-101 ») | EXCLURE | PC-E, PG-E, SD-E, BJ-E, MP-E, BC-E — noter 34 + 10 (A-04) = 44 E.A.E Détail vs total des lignes -E sur plan (PC-E 7 + PG-E 4 + SD-E 17 + BJ-E 2 + MP-E 3 + BC-E 2 = 35 ; les lignes PC-E, PG-E, BC-E sont dans les lots d'autres releveurs : lis leurs valeurs ENLEVER dans rapport-releve.md ; DM-E 1 et INT-E 1 existent aussi : cite l'écart, pas de reprise) |
| A-04 (10 u, démantèlement services 2e E.A.E, note « Compte E.A.E E-102 ») | EXCLURE | idem A-03 |
| E-01 (2 postes aide au lecteur 227 : JB, 2 prises, data 2 RJ45) | EXCLURE | PC-I, SD-I |
| E-02 (2 monuments de plancher, prise 20A + 2 RJ45) | EXCLURE | MP-I (3 sur plan ; noter 2 vs 3) |
| E-04 (3 cabines/salles : JB + prise) | EXCLURE | PC-I (et BJ-I si pertinent) |
| E-05 (1 écran sur colonne : courant + données) | EXCLURE | PC-I, SD-I |
| D-09 (1 lot barrière anti-vol : 2 JB + raccord panneau de contrôle PU-1 23) | REPRENDRE `D-09`, q 1, u LOT, art 3.31 | desc « raccord panneau de contrôle barrière anti-vol — les 2 JB sont comptées dans BJ-I » ; hypothèse : BJ-I 3 (E104) = 2 JB de D-09 + 1 JB de D-10 — VÉRIFIER : 3 BJ INSTALLER, toutes sur E104 (Par feuille BOITE JONCTION E104 = 3) |
| D-10 (1 u bornes de prêts / fontaine hall — JB dans mur adjacent) | EXCLURE si le contrôle ci-dessus tient (BJ-I 3 = 2 + 1, toutes sur E104) ; sinon REPRENDRE D-10 q 1, u U, art 3.31 et expliquer en note | BJ-I |
| E-03 (2 u boîte de plancher refaite salle 208, note « P-6 25 / P-6 38 — à confirmer » ; Réf. plan E-102/E-105) | REPRENDRE `E-03`, q 2, u U, art 3.34 | note : chevauchement possible avec MP-E 3 (E102) / MP-I 3 (E105) — « à confirmer » dans Détail ; non tranchable sans le plan |
Pour chacune, relis dans `Détail` sa description, sa quantité (colonne Qté), son unité et sa note (« Notes / source quantité ») et écris dans la `raison`
de l'exclusion (ou dans le `src` de la ligne reprise) le code Détail, sa quantité lue et la ligne plan qui la remplace. Ne traite AUCUN autre code Détail
(A-05, A-07, D-01 à D-08 sont à d'autres releveurs).
Lignes de reprise attendues : D-09 (LOT 1), E-03 (U 2). `src` de ces lignes : `"entree/reference-Estimation_2.xlsx Détail D-09 Qté 1 lot ; arbitrage chef A1"`.

## Articles du bordereau à proposer (`art`, texte)
Bordereau `entree/reference-Bordereau_de_prix.xlsx` : 3.22 Démontage des éléments électriques · 3.23 Raccordement
des équipements mécaniques · 3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles
15A-120V MALT isolées · 3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction ·
3.33 Sorties informatique/réseau · 3.34 Moinument plancher · 3.35 Appareil de contrôle + appareils d'éclairage ·
5.19 Démolition des systèmes électriques.
Convention du directeur A : toute ligne `-E` (enlever) → **3.22** ; une ligne `-R` (relocaliser) → l'article de sa
famille ; PC → 3.28 ; PU → 3.27 ; PG → 3.30 (noter que R-007 confond DDFT et M.A.L.T. isolée = 3.29) ; SD → 3.33 ;
MP → 3.34 ; INT → 3.35 ; TH → 3.23 ; BJ → 3.31 ; LC → 3.31 (aucun article « intrusion » au bordereau : le noter).

## Format de sortie : `lots/releveur-A1-2.json`
```json
{
  "niveau": "releveur",
  "nom": "A1-2",
  "modele_demande": "haiku",
  "effort_demande": "xhigh",
  "lignes": [
    {"code": "SD-I", "desc": "Sortie informatique/réseau neuve", "q": 65, "u": "U", "p": null, "h": null,
     "art": "3.33", "src": "releve.xlsx Par libellé SORTIE DATA 120 ; rapport-releve.md INSTALLER 65 ; Par feuille E104 45 + E105 20"}
  ],
  "notes": ["hésitations, familles sans ligne (CONSERVER), contrôles par feuille, contradictions plan/Détail"],
  "exclusions": [{"code": "E-01", "raison": "double compte : 2 postes aide au lecteur (Détail E-01 Qté 2) déjà dans PC-I et SD-I (plan) — remplacée par PC-I, SD-I"}]
}
```
`u` ∈ {`U`, `PI`, `LOT`} ; `p` et `h` toujours `null` ; `art` texte (« 3.28 ») ; `src` exact et vérifiable
(fichier, feuille, libellé ou code, valeur lue). Une ligne par code `<FAM>-<P>` (P : I = installer, E = enlever,
R = relocaliser) quand la portée existe dans rapport-releve.md ; la quantité `q` est celle du rapport pour cette portée
(ne pas additionner les portées entre elles). `desc` : description courte en français.
Lignes attendues pour ce sous-lot (à reconfirmer) : SD-I, SD-E, SD-R, BJ-I, BJ-E, MP-I, MP-E, D-09, E-03 (9 lignes ; TV aucune ligne).
Exclusions attendues : A-03, A-04, E-01, E-02, E-04, E-05, D-10 (7 codes, D-10 sous réserve du contrôle BJ).
Les unités : `U` sauf D-09 en `LOT`.

## Contrôle de cohérence par feuille (à écrire en note, un par famille de ton lot)
D'après R-002, une marque sans étiquette est CONSERVER sur une feuille existant/démolition et INSTALLER sur une feuille
nouveau. Pour chaque famille de ton lot, calcule depuis `releve.xlsx` feuille `Par feuille` :
- EXISTANT = somme des feuilles E101 + E102 + E103 + E201 + E202 ; doit être égal à C + E + R (CONSERVER + ENLEVER + RELOCALISER du rapport) ;
- NOUVEAU = somme des feuilles E104 + E105 + E106 + E203 + E204 ; doit être égal à I (INSTALLER du rapport).
Exemple (PC) : 48 + 22 = 70 = 55 + 7 + 8 ; 23 + 2 = 25 = I. Écris en note, pour chaque famille, le calcul avec les
valeurs lues (« PC : existant 48+22=70 vs C+E+R 55+7+8=70 OK ; nouveau 23+2=25 vs I 25 OK »). Un écart va en note :
il ne modifie PAS la quantité (le rapport-releve.md fait foi pour la portée).
Familles de ton lot : SD (attendu 36+19=55 vs 35+17+3=55 ; 45+20=65 vs 65), TV (4 = 4 ; nouveau 0), BJ (E101 4 + E102 1 + E201 2 = 7 vs 5+2=7 ; E104 3 vs 3), MP (1+3=4 vs 1+3=4 ; E105 3 vs 3).

## Vérifications avant de t'arrêter (toutes obligatoires)
1. Le JSON se charge : `python3 -c "import json;json.load(open('lots/releveur-A1-2.json'))"` (code de sortie 0)
   et contient les clés `lignes`, `notes` et `exclusions`.
2. Chaque `src` pointe vers une cellule/un libellé/un code RÉELLEMENT lu : rouvre le fichier et recompare les valeurs
   chiffrées (rapport-releve.md, Par libellé, Par feuille, Détail) avant de terminer ; corrige toute divergence.
3. Aucun `code` n'apparaît deux fois dans `lignes`.
4. Toute ligne Détail de ton sous-lot est reprise dans `lignes` OU listée dans `exclusions` avec sa raison.
5. `p` et `h` valent `null` partout ; `u` ∈ {U, PI, LOT} ; `art` est du texte.
6. Le contrôle par feuille de chaque famille est écrit en note.
Puis arrête-toi. Ne lance personne. Réponds seulement : le nombre de lignes et la liste « code = q » (une ligne par code), rien d'autre.
