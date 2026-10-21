effort: xhigh
modele: haiku

# Releveur B3-3 — DOUBLES COMPTES (relevé sur plan ↔ feuille Détail ↔ lots fournisseur ↔ assemblages Dupuis) (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le releveur B3-3, modèle Claude Haiku 5.5, feuille de l'arbre d'une équipe hiérarchique d'estimation électrique chez DR Électrique. Ton supérieur est le chef de lot B3 (Claude Sonnet 5.5), lui-même sous le directeur B (Claude Opus 5.5), sous le chef de l'essaim (Claude Fable 5.1). Effort demandé pour ton travail : xhigh — un double compte non vu (ou un objet payé deux fois entre une ligne Détail, une ligne sur plan, un assemblage Dupuis et un lot fournisseur) déplace tout le total, et la liste que tu écris sert de garde-fou au directeur B.
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités sont la mission de l'équipe A : `q` reste `null` partout. Le chef de lot B3 est responsable de la ventilation par article du bordereau, des doubles comptes et des 21 codes hors plan « divers ». Ta part : les doubles comptes.

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
`/home/claude/entrainement/S-1902/swarm-2/` — tu y travailles uniquement (chemins absolus conseillés, `python3`). Tu n'écris que `lots/releveur-B3-3.json`. Tu n'ouvres JAMAIS un autre fichier de `lots/` ni de `prompts/` (aucun fichier de collègue ni de supérieur : ça fausserait la mesure à l'aveugle).

## Première chose à faire
Lis dans cet ordre : `CONSIGNES.md`, `METHODE.md`, `rapport-releve.md`, `reserves.md` ; puis ouvre `entree/reference-Bordereau_de_prix.xlsx` (articles 3.22 à 3.38, 5.11, 5.19, 6.1, 6.2), TOUTE la feuille `Détail` et TOUTE la feuille `Matériel Lumen` d'`entree/reference-Estimation_2.xlsx`, les deux relevés `entree/reference-Releve_Alarme_Incendie.xlsx` et `entree/reference-Releve_Eclairage_Urgence.xlsx`, `releve.xlsx` (feuilles `Par libellé` et `Par feuille`) et le catalogue. (`ARCHITECTURE.md` §3 nomenclature, §4 découpage et lignes Détail à exclure, §5 format JSON : à lire.)
Lecture de `releve.xlsx` feuille `Par feuille` (feuille × libellé × quantité, SANS portée) :
```python
import openpyxl
from collections import defaultdict
wb = openpyxl.load_workbook('/home/claude/entrainement/S-1902/swarm-2/releve.xlsx', data_only=True)
tab = defaultdict(lambda: defaultdict(int))
for r in list(wb['Par feuille'].iter_rows(values_only=True))[1:]:
    tab[r[0]][r[2]] += (r[3] or 0)      # r = (feuille cartouche, feuille fichier, libellé, quantité)
for f in sorted(tab):
    print(f, dict(tab[f]))
```
Les portées (INSTALLER / ENLEVER / RELOCALISER / CONSERVER) ne sont QUE dans le tableau « famille | total | portées » de `rapport-releve.md` (pas par feuille).

## TA TÂCHE EXACTE — releveur B3-3
Seul fichier à écrire : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-3.json`. Tu n'as AUCUNE ligne chiffrée (`"lignes": []`), AUCUN article (`"articles": {}` et `"regles_articles": []`).

Découpage du lot B3 (3 sous-lots DISJOINTS et COUVRANTS ; tu es B3-3) :
- B3-1 : les articles des 120 codes + les doubles comptes dont UN des objets est une ligne de la feuille « Matériel Lumen » (38 lignes, codes Lumen : CONEMT1, IBE52151K, LEV16252W, HUBS1R6PTDEHBLK, TROCP25WB+10.1OZ, VISTF3/8…). Tu N'écris PAS ces entrées-là (même si la liste de départ ci-dessous les mentionne).
- B3-2 : p, h, art, src des 21 codes hors plan « divers » (A-07, A-08, A-09, A-10, A-11, C-01, C-02, C-03, C-04, D-16, E-11, F-05, F-10, G-04, G-05, G-06, G-07, H-01, H-02, H-03, H-04).
- B3-3 (toi) : TOUS les autres doubles comptes : toute entrée dont AUCUN objet n'est une ligne Lumen. Les 21 lignes de B3-2 sont dans ton périmètre COMME PARTENAIRES de doubles comptes (tu ne les chiffres pas).

Règle de fond (METHODE + ARCHITECTURE) : « le plan gagne ; un objet physique n'est payé qu'une fois » ; « Dupuis dernier gagne sur Lumen ; Lumen gagne sur le jugement » ; les lignes couvertes par un lot fournisseur sont à 0 $ en ligne (temps seulement) ; une ligne Détail exclue ne reçoit NI p NI h (elle est remplacée par le code sur plan). Les lignes Détail dont les quantités recomptent le plan sont, d'après ARCHITECTURE.md §4 : A-01 à A-06, D-01 à D-08, E-01, E-02, E-04, E-05, F-01 à F-04, F-06, F-07, G-01 (25 lignes).

### Ce que tu dois produire
(1) `doubles_comptes` : TOUTES les entrées (au moins 20) {"codes": […], "regle": "…", "quantites": "…"} sauf celles qui impliquent Lumen.
(2) `exclusions` : une entrée par ligne Détail exclue (les 25 ci-dessus) : {"code": "A-01", "remplace_par": ["ENC-E", "L14-E", "L22-E"], "raison": "… avec les quantités de part et d'autre"}.
(3) `notes` : la TABLE D'EXHAUSTIVITÉ de la feuille Détail : pour CHACUN des 76 codes A-01 … H-04, une ligne « DÉTAIL <code> → EXCLUE (remplacée par …) | DOUBLE (entrée n° k) | INDÉPENDANTE (raison en une phrase : pourquoi aucun recouvrement) » ; puis la ligne « OPT-1…OPT-4 : hors total, jamais chiffrés » ; puis les contrôles de lots (ci-dessous) ; puis tes doutes.

### LISTE DE DÉPART du directeur B (recopiée mot pour mot ; à VÉRIFIER sur les fichiers et à COMPLÉTER ; la puce « Prix d'assemblage Dupuis ↔ feuille Matériel Lumen » est à B3-1, pas à toi)
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

### PISTES DU CHEF B3 (chiffres lus par le chef — à RE-VÉRIFIER dans les fichiers, jamais à recopier sans relire ; ce sont des pistes, pas des conclusions)
Attention : `Par feuille` ne donne PAS la portée ; toute attribution d'une portée à une feuille ci-dessous (ex. « tous sur E103 ») est une DÉDUCTION du chef à confirmer ou infirmer, pas une lecture.
 P1. A-05 = 13 (6 RDC + 7 étage) ; relevé RELOCALISER : PRISE DOUBLE 15A 8 + PRISE DDFT 1 + SORTIE DATA 3 + DETECTEUR FUMEE 1 = 13 → égalité exacte : mêmes objets.
 P2. A-01 + A-02 = 39 + 7 = 46 luminaires E.A.E ; relevé ENLEVER : ENCASTRE 26 + LED 1X4 6 + LED 2X2 8 = 40 → écart 6 à signaler.
 P3. A-03 + A-04 = 34 + 10 = 44 services E.A.E ; relevé ENLEVER hors luminaires : PRISE DOUBLE 15A 7 + PRISE DDFT 4 + SORTIE DATA 17 + INT SIMPLE 1 + BOITE JONCTION 2 + MONUMENT PLANCHER 3 + DETECTEUR MOUVEMENT 1 + BOITIER C 2 + DETECTEUR FUMEE 1 + HP ENCASTRE PLAFOND 1 = 39 → écart 5 à signaler.
 P4. A-06 = 7 (3 RDC + 4 étage, « incl. 4 appareils salle 227 ») vs relevé ENCASTRE RELOCALISER 4.
 P5. F-01…F-04 = 11 / 12 / 6 / 15 = relevé LUMINAIRE A1 11, C1 12, C1_1 6, C1_3 15 = relevé d'éclairage A1 11, C1 12, C1_1 6, C1_3 15 (égalité exacte) ; F-06 = 4 vs relevé plan LUMINAIRE E 3 vs relevé d'éclairage « E » 4 vs METHODE « E ×3 à 475 $ » (reserves.md R-003 : « l'estimation en compte 4 — à trancher au zoom ») ; F-07 = 3 = Z6 3 ; F-05 = 20 rangées = C-SUSP 20 du relevé d'éclairage.
 P6. G-01 = 2 = DF-I 2 (DETECTEUR FUMEE INSTALLER 2) = AI-01 2 = LOT-DET (2 détecteurs, 600 $).
 P7. C-01, C-02, C-03, C-04 (UTA-01 1, VE-02N 1, chaudières 2, humidificateurs 3) ↔ MT-I 4 et MM-I 3 : `Par feuille` donne MOTEUR TRIPHASE E105 2 + E106 2 et MOTEUR MONOPHASE E105 3 ; vérifie que 1 + 1 + 2 = 4 et 3 = 3 (même objets, deux lignes) et dis ce que chaque ligne (code plan 0,75 h / ligne Détail 16, 10, 12, 12 h) couvre.
 P8. A-10 = 6 u = MM-R 6 (MOTEUR MONOPHASE RELOCALISER 6, tous sur E103 d'après `Par feuille`).
 P9. Disjoncteurs : 1P B-02 14 + B-06 1 + B-07 2 + B-08 2 = 19 vs LOT-DIST « EDB 1P 95 $ × 20 » ; 3P B-03 1 + B-04 1 + B-05 1 = 3 vs « EJB 3P 300 $ × 3 » ; B-01 ↔ « NF 225 A 42 cct 3 400 $ » ; B-09 non couvert par le lot.
 P10. BJ-I 3 (BOITE JONCTION INSTALLER 3, relevé) = D-09 (2 boîtes de jonction) + D-10 (1 JB dans le mur adjacent) ; D-11 et E-06 : « boîte + conduit vide » d'un bouton d'appel (déjà dans SD-I ? à examiner).
 P11. Monuments : relevé MONUMENT PLANCHER INSTALLER 3 (E105 3), ENLEVER 3 (E102 3), CONSERVER 1 (E101 1) ↔ E-02 (2 monuments Hubbell neufs, étage) et E-03 (2 boîtes de plancher « refaites », salle 208, note 1 E-102).
 P12. FabLab (E-202 note 1) : A-08 = 21 ↔ « LED 1X4 » sur E202 = 21 (`Par feuille`) ; A-09 = 24 ↔ « ENCASTRE » sur E202 = 35 ; A-07 : le relevé n'a aucune relocalisation d'interrupteur (INT SIMPLE : INSTALLER 5, CONSERVER 4, ENLEVER 1).
 P13. Services neufs : compare D-01 … D-08, E-01, E-02, E-04, E-05 (Qté Détail, avec le contenu par poste/table décrit dans leur description) aux familles du relevé PC-I 25, PU-I 20, PG-I 22, SD-I 65, MP-I 3, BJ-I 3 (ex. D-02 : 5 tables × 2 prises + 2 USB ; D-01 : 18 postes × (1 prise 15 A + 1 prise 20 A + boîte data 2 RJ45) ; reserves.md R-007 : 15 A et 20 A non distinguées au relevé) ; donne l'écart de part et d'autre, dis que le plan gagne.
 P14. Lots : METHODE.md §2 donne LOT-ECL « 11 893 $ » alors que la somme de ses composantes énumérées (A1 ×11 à 185 + Axis 4' ×12 à 290 + 3' ×15 à 230 + 1' ×6 à 110 + trousses 1 500 + E ×3 à 475 + Z6 ×3 à 161,60) = 13 034,80 $ (écart 1 141,80 $) ; LOT-DIST : 3 400 + 20 × 95 + 3 × 300 = 6 200 $. Ne modifie AUCUN montant de lot (prix confirmés par Francis le 2026-10-20) : recalcule chaque lot par script et SIGNALE tout écart dans `notes`.
 P15. Assemblages Dupuis « CONDUIT … nnCcc » (um=P) qui incluent le fil : établis par recherche (`^CONDUIT`) quels assemblages existent pour EMT 1" et 3/4" avec 3, 4 et 5 conducteurs #12 / #8 (C-06 : 1" 4 #8 ; C-08 : 3/4" 4 #12 ; D-15 : 5 conducteurs #12 par course ; E-10 : 5 conducteurs ; F-09 : 3 conducteurs ; G-03 : câble AI 2c #16) et dis, pour chaque paire conduit/fil (C-05/C-06, C-07/C-08, D-13/D-15, E-08/E-10, F-08/F-09), si l'assemblage retenu couvre déjà le NOMBRE de conducteurs du Détail (alors le fil séparé est à 0) ou non (alors seulement les conducteurs excédentaires sont à chiffrer) ; cite les libellés exacts avec um, prix, temps.

### MÉTHODE
 1. Lis la feuille Détail LIGNE PAR LIGNE (76 codes A-01 à H-04 : A 11, B 9, C 8, D 16, E 11, F 10, G 7, H 4) ; pour chacune, cherche ce qui la recouvre : une famille du relevé (`rapport-releve.md`, `Par libellé`, `Par feuille`), une autre ligne Détail, un lot fournisseur (METHODE.md §2), une entrée des relevés Alarme incendie / Éclairage (AI-01…AI-09 ; A1, C1, C1_1, C1_3, C-SUSP, E, Z6), un assemblage Dupuis.
 2. Vérifie CHAQUE élément de la liste de départ et des pistes (codes en cause, quantités de part et d'autre, cellule ou ligne lue) ; corrige ce qui est faux ; ajoute ce qui manque.
 3. Cherche activement d'AUTRES doubles comptes que la liste n'annonce pas (compare aussi les Notes de chaque ligne Détail, les « Réf. plan » et les descriptions : ex. « incl. démantèlement ancien PP-3 » en B-01, « Incl. … » ; ce qui est dit « fourni par JCI/Simplex » ; ce qui est dit « fourni par d'autres »). Note aussi, dans `notes`, les ambiguïtés INTERNES au relevé qui touchent aux prix (PU/PC : reserves.md Q14 ; PG et M.A.L.T. : R-007 ; 15 A / 20 A et comptoir / standard non distingués : R-007 ; LE 3 vs 4 : R-003) — ce ne sont pas des doubles comptes mais ils expliquent des écarts de quantités.
 4. Pour chaque entrée, écris la RÈGLE à appliquer avec ce vocabulaire (un seul sens par phrase) :
    - « le plan gagne : la ligne Détail <X> est EXCLUE (ni p ni h) ; seuls <codes plan> sont chiffrés » ;
    - « payé une fois par <ligne A> : <ligne B> tombe (ou est à 0 $ en ligne, temps seulement) » ;
    - « 0 $ en ligne + lot : <ligne> a p = 0 car couverte par <LOT-xxx> » ;
    - « inclus dans l'assemblage Dupuis <libellé exact> : pas de fil / boîte / plaque séparés » ;
    - « À TRANCHER PAR LE DIRECTEUR B : option 1 … ; option 2 … ; valeur par défaut recommandée : … » quand le plan ne tranche pas (même objet, deux lignes chiffrées : C-01…C-04 ↔ MT-I/MM-I ; A-10 ↔ MM-R ; G-04 ↔ PA ; H-01 ↔ X-02 ; X-01 ↔ LOT-GPR…) — donne alors l'écart chiffré en HEURES (qté × h) ou en $ quand il se calcule SANS inventer de valeur, et ta recommandation par défaut avec son motif.
 5. `quantites` : texte avec les quantités de part et d'autre ET leur source (ex. « Détail A-01 Qté 39 (cellule D8) + A-02 Qté 7 ; rapport-releve.md ENCASTRE ENLEVER 26, LED 1X4 ENLEVER 6, LED 2X2 ENLEVER 8 = 40 ; écart 6 »). Quand une quantité n'est pas lisible : « non lisible — <pourquoi> », jamais une valeur inventée.
 6. Regroupe intelligemment : une entrée par PAIRE ou GROUPE d'objets physiques (ex. une entrée « A-05 ↔ PC-R, PG-R, SD-R, DF-R », une pour « D-01 … D-08 ↔ PC-I, PU-I, PG-I, SD-I, BJ-I », etc.), mais JAMAIS en mélangeant des objets sans rapport pour faire court.
 7. Contrôles de lots à écrire dans `notes` (calculés par script, avec les valeurs lues) : composition de LOT-ECL (METHODE.md §2 vs relevé d'éclairage et relevé plan : quantités A1 11, C1 12, C1_1 6, C1_3 15, C-SUSP 20, E 4 (relevé d'éclairage) vs 3 (plan, lot), Z6 3), LOT-DIST (Détail B-01…B-08), LOT-DET (AI-01 : 2), LOT-JCI (AI-03 à AI-06), LOT-GPR (X-01 ou aucune ligne Détail) ; pour chacun : quels codes de ligne sont couverts (donc p = 0), lesquels ne le sont pas.

### Univers de codes autorisés dans `codes` (à vérifier par script)
Codes de nomenclature sur plan (`<FAM>-<I|E|R>` pour les 26 familles PC PU PG SD TV INT TH BJ MP LC GA DM BC ENC ENCU L14 L22 L4 LLIN HP Z6 DF SM PA MM MT, plus LA1-I LC1-I LC11-I LC13-I LE-I) ; les 76 codes de la feuille Détail (A-01 … H-04) ; OPT-1 … OPT-4 ; X-01, X-02 ; LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR ; AI-01 … AI-09 (relevé Alarme incendie) ; C-SUSP (relevé d'éclairage). AUCUN code Lumen dans tes entrées. Un code inconnu = tu le retires.

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

(Pour toi, B3-3 : tu n'écris aucune ligne chiffrée ; ces conventions valent pour tout libellé du catalogue que tu cites dans `regle` ou `quantites` : copie-le EXACT depuis le CSV avec `repr(r['description'])`, jamais de mémoire.)

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

## Squelette EXACT de ton fichier (releveur B3-3)
```json
{
  "niveau": "releveur",
  "nom": "B3-3",
  "modele_demande": "haiku",
  "effort_demande": "xhigh",
  "lignes": [],
  "articles": {},
  "regles_articles": [],
  "doubles_comptes": [
    {"codes": ["A-01", "A-02", "ENC-E", "L14-E", "L22-E"], "regle": "le plan gagne : …", "quantites": "…"}
  ],
  "exclusions": [
    {"code": "A-01", "remplace_par": ["ENC-E", "L14-E", "L22-E"], "raison": "…"}
  ],
  "notes": ["DÉTAIL A-01 → EXCLUE (remplacée par ENC-E, L14-E, L22-E)", "…", "CONTRÔLE LOT-ECL : …"]
}
```
(L'exemple ci-dessus montre seulement la FORME ; les valeurs sont à établir par toi sur les fichiers.) Écris avec `json.dump(obj, f, ensure_ascii=False, indent=2)`. `lignes` est VIDE, `articles` est `{}`, `regles_articles` est `[]`.

## Vérifications avant d'écrire un JSON (ARCHITECTURE.md §6, tous niveaux)
1. Le JSON se charge (`python3 -c "import json;json.load(open('...'))"`) et contient `lignes` + `notes`.
2. Chaque ligne a un `src` qui pointe vers un libellé/une cellule réellement lu ; tout code du sous-lot est présent
   une et une seule fois ; `q` est `null` partout.
3. Pas de médiane : pour chaque ligne Dupuis, relire la ligne avec `ligne(desc, um)` et vérifier
   `p == float(prix_a_utiliser)` et `h == float(temps_a_utiliser)` (sauf p = 0 forcé par un lot, écrit dans `src`).
4. Un rapport d'agent n'est pas une preuve : le niveau supérieur juge sur le fichier `lots/*.json`, pas sur le récit.

Vérifications propres à B3-3 (à exécuter par script, avec les codes de sortie vérifiés) :
 5. `doubles_comptes` : au moins 20 entrées ; chacune a EXACTEMENT les clés `codes` (liste de 2 codes ou plus, tous dans l'univers autorisé, aucun code Lumen), `regle` (texte non vide), `quantites` (texte non vide).
 6. `exclusions` : EXACTEMENT les 25 lignes Détail exclues (A-01 à A-06, D-01 à D-08, E-01, E-02, E-04, E-05, F-01 à F-04, F-06, F-07, G-01), une fois chacune, avec `remplace_par` (liste de codes de nomenclature sur plan, non vide) ; si une preuve te montre qu'une de ces lignes ne double PAS le plan (ou qu'une 26e le double), écris « CONTRADICTION POSSIBLE : <code> … » dans `notes` mais GARDE les 25 dans `exclusions`.
 7. TABLE D'EXHAUSTIVITÉ : les 76 codes A-01 … H-04 apparaissent TOUS dans `notes` (une ligne chacun) ; tout code classé « DOUBLE (entrée n° k) » figure bien dans l'entrée k de `doubles_comptes` ; tout code classé « EXCLUE » figure dans `exclusions`.
 8. Rouvre au hasard au moins 5 cellules de la feuille Détail citées dans tes `quantites` et 5 lignes du tableau de `rapport-releve.md` : les nombres écrits doivent correspondre ; recalcule par script chaque somme citée (46 = 39 + 7, 40 = 26 + 6 + 8, 13 = 8 + 1 + 3 + 1…).
 9. Chaque lot (LOT-ECL, LOT-DIST, LOT-JCI, LOT-DET, LOT-GPR) : montant METHODE.md recopié tel quel, composantes recalculées par script, écart éventuel écrit dans `notes` ; aucun montant de lot modifié.

## Quand tu as fini
Écris UNIQUEMENT `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-3.json`, vérifie qu'il se charge en JSON (`python3 -c "import json;json.load(open('/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-3.json'))"`), puis réponds en UNE ligne : nom du fichier écrit + nombre d'entrées `doubles_comptes` + nombre d'exclusions (25 attendues). Tu t'arrêtes ensuite. Tu ne délègues à personne et tu ne lances aucun agent.
