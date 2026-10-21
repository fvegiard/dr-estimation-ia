effort: xhigh
modele: haiku

# Releveur B3-1 — ARTICLES DU BORDEREAU (120 codes) + DOUBLES COMPTES « MATÉRIEL LUMEN » (essaim 2, chiffrage à l'aveugle S-1902)

Tu es le releveur B3-1, modèle Claude Haiku 5.5, feuille de l'arbre d'une équipe hiérarchique d'estimation électrique chez DR Électrique. Ton supérieur est le chef de lot B3 (Claude Sonnet 5.5), lui-même sous le directeur B (Claude Opus 5.5), sous le chef de l'essaim (Claude Fable 5.1). Effort demandé pour ton travail : xhigh (une erreur ici se propage au chiffrage : un article faux fausse la ventilation par article, et un objet payé deux fois — matériel Lumen en plus d'un assemblage Dupuis — déplace tout le total).
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` / `temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les quantités sont la mission de l'équipe A : `q` reste `null` partout. Le chef de lot B3 est responsable de la ventilation par article du bordereau, des doubles comptes et des 21 codes hors plan « divers ».

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
`/home/claude/entrainement/S-1902/swarm-2/` — tu y travailles uniquement (chemins absolus conseillés, `python3`). Tu n'écris que `lots/releveur-B3-1.json`. Tu n'ouvres JAMAIS un autre fichier de `lots/` ni de `prompts/` (aucun fichier de collègue ni de supérieur : ça fausserait la mesure à l'aveugle).

## Première chose à faire
Lis dans cet ordre : `CONSIGNES.md`, `METHODE.md`, `rapport-releve.md`, `reserves.md` ; puis ouvre `entree/reference-Bordereau_de_prix.xlsx` (articles 3.22 à 3.38, 5.11, 5.19, 6.1, 6.2), TOUTE la feuille `Détail` et TOUTE la feuille `Matériel Lumen` d'`entree/reference-Estimation_2.xlsx`, `releve.xlsx` (feuille `Par libellé`) et le catalogue. (`ARCHITECTURE.md` §3 nomenclature et §5 format JSON : facultatif.)

## TA TÂCHE EXACTE — releveur B3-1
Seul fichier à écrire : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-1.json`.

Découpage du lot B3 (3 sous-lots DISJOINTS et COUVRANTS ; tu es B3-1) :
- B3-1 (toi) : (A) l'article définitif des 120 codes listés ci-dessous + les règles d'articles écrites ; (B) les doubles comptes liés à la feuille « Matériel Lumen » (38 lignes de matériel Lumen).
- B3-2 : p, h, `art` et `src` des 21 codes hors plan « divers » (A-07 … H-04, listés ci-dessous comme « PAS À TOI ») + leurs 21 articles.
- B3-3 : TOUS les autres doubles comptes (relevé sur plan ↔ feuille Détail ↔ lots fournisseur ↔ assemblages Dupuis) ; toute entrée dont AUCUN objet n'est une ligne de la feuille « Matériel Lumen ».
Tu ne fais ni le travail de B3-2 ni celui de B3-3 ; tu n'as AUCUNE ligne chiffrée (`"lignes": []`).

### Livrable A — l'article du bordereau de CHACUN des 120 codes (clé `articles`) + les règles écrites (clé `regles_articles`)
Les 120 codes (chacun UNE fois dans `articles`, forme {"PC-I": "3.28", …} ; les valeurs ci-dessous ne sont PAS données : tu les DÉRIVES des règles R0 à R12 plus bas) :
1. Codes sur plan (83 = 26 familles × {-I, -E, -R} + 5 luminaires neufs -I) :
   PC-I PC-E PC-R
   PU-I PU-E PU-R
   PG-I PG-E PG-R
   SD-I SD-E SD-R
   TV-I TV-E TV-R
   INT-I INT-E INT-R
   TH-I TH-E TH-R
   BJ-I BJ-E BJ-R
   MP-I MP-E MP-R
   LC-I LC-E LC-R
   GA-I GA-E GA-R
   DM-I DM-E DM-R
   BC-I BC-E BC-R
   ENC-I ENC-E ENC-R
   ENCU-I ENCU-E ENCU-R
   L14-I L14-E L14-R
   L22-I L22-E L22-R
   L4-I L4-E L4-R
   LLIN-I LLIN-E LLIN-R
   HP-I HP-E HP-R
   Z6-I Z6-E Z6-R
   DF-I DF-E DF-R
   SM-I SM-E SM-R
   PA-I PA-E PA-R
   MM-I MM-E MM-R
   MT-I MT-E MT-R
   LA1-I LC1-I LC11-I LC13-I LE-I
2. Codes hors plan du chef B1 (5) : D-09 D-10 D-11 E-03 E-06
3. Codes hors plan et lots du chef B2 (32) : B-01 B-02 B-03 B-04 B-05 B-06 B-07 B-08 B-09 X-01 X-02 D-12 E-07 C-05 C-06 C-07 C-08 D-13 D-14 D-15 E-08 E-09 E-10 F-08 F-09 G-02 G-03 LOT-ECL LOT-DIST LOT-JCI LOT-DET LOT-GPR
PAS À TOI (releveur B3-2, 21 codes) : A-07 A-08 A-09 A-10 A-11 C-01 C-02 C-03 C-04 D-16 E-11 F-05 F-10 G-04 G-05 G-06 G-07 H-01 H-02 H-03 H-04
(Ces 21 codes ne figurent PAS dans ton `articles`.)

Marche à suivre :
 a. Ouvre le bordereau et relis les libellés des articles 3.22 … 3.38, 5.11, 5.19, 6.1, 6.2 ; compare-les à ceux de la section « RÈGLES D'ARTICLES DÉFINITIVES » ci-dessous. Écris dans `notes` : « LIBELLÉS BORDEREAU VÉRIFIÉS : » suivi des numéros relus (au moins 3.22, 3.23, 3.24, 3.25, 3.26, 3.31, 3.32, 3.33, 3.34, 3.35, 3.36, 3.37, 3.38, 5.11, 5.19, 6.1, 6.2) et de tout écart de libellé.
 b. Pour les 37 codes hors plan : relis la ligne de la feuille Détail correspondante (Description, Réf. plan, Notes) ; les lots LOT-* : relis METHODE.md §2. Pour les codes sur plan : relis la famille dans `releve.xlsx` (feuille `Par libellé`) et ses portées dans `rapport-releve.md` (tableau « famille | total | portées »).
 c. Applique les règles R0 à R12 code par code. Dans ton script, écris un dictionnaire {code: (article, numéro de règle)} construit par code — jamais un article « de mémoire ».
 d. Contrôle de cohérence interne : si tu as bien appliqué les règles, le nombre de codes par article est EXACTEMENT : 3.22 → 48 ; 3.23 → 5 ; 3.24 → 3 ; 3.25 → 7 ; 3.27 → 1 ; 3.28 → 1 ; 3.30 → 1 ; 3.31 → 19 ; 3.32 → 2 ; 3.33 → 6 ; 3.34 → 2 ; 3.35 → 15 ; 3.36 → 5 ; 3.37 → 3 ; 3.38 → 1 ; 6.1 → 1 ; et AUCUN code en 3.26, 3.29, 5.11, 5.19, 6.2 (total 120). Un écart = tu relis la règle du code fautif (ne force pas les chiffres : corrige l'application de la règle).
 e. `regles_articles` : une entrée par règle (P0, R1 … R12) au format « <énoncé> — parce que <motif tiré du libellé EXACT du bordereau ou de la ligne Détail> — exceptions : <liste> — ce que reçoit l'autre article : <…> ». Tu peux reprendre le texte des règles en l'adaptant, sans en perdre.
 f. `notes` : (i) « CONTRADICTION POSSIBLE : … » (voir plus bas) ; (ii) la liste « PORTÉE ABSENTE DU RELEVÉ — correspondance de précaution » : pour chacune des 26 familles sur plan, les portées présentes dans rapport-releve.md (ex. « PC : INSTALLER 25, ENLEVER 7, RELOCALISER 8, CONSERVER 55 ») puis les codes -I/-E/-R de la famille sans portée correspondante ; (iii) le contrôle d'e) ci-dessus (comptes par article obtenus).

### Livrable B — doubles comptes liés à la feuille « Matériel Lumen » (clé `doubles_comptes`)
Contexte : la feuille « Matériel Lumen » (38 lignes de matériel, Total 23 159,6714 $, prix RÉGULIERS Lumen du 2026-10-07) est faite pour les familles ABSENTES du catalogue Dupuis. Or les prix d'assemblage Dupuis incluent boîte, plaque, raccord (prise duplex 15 A 64,81 $, USB 77,45 $, DDFT 65,38 $, tel/data 3/4 22,32 $, interrupteur 75,47 $, percement 150 $, monument 250 $, conduit 3/4 03C12 4,24 $/pi…), et le catalogue contient aussi des lignes « composants » (ex. « COND TME 1PO » um=P 1,8378 = CONEMT1 Lumen 1,8378 ; « TIGE FILETE 3/8PO » um=P 0,6435 = VISTF3/8 Lumen 0,6435 ; « INTERR 30A 2P 600V CEMA1 » 117,84 = HUBHBL1372 Lumen 117,84). Règle : « le plan gagne ; un objet physique n'est payé qu'une fois » — un objet déjà payé par un assemblage Dupuis ou par un lot fournisseur ne doit JAMAIS être payé une 2e fois par Lumen.
Pour CHACUNE des 38 lignes Lumen (chaque code Lumen de la colonne « Code Lumen »), classe et JUSTIFIE :
  (1) INCLUS — l'objet est déjà dans un prix d'assemblage ou une ligne composant Dupuis : cite le libellé exact (`ligne(desc, um)`), son um, son prix et son temps, et dis quelle ligne de chiffrage le porte ; la ligne Lumen n'est PAS ajoutée ;
  (2) À CHIFFRER — aucune ligne Dupuis ne décrit cette famille après AU MOINS 3 recherches différentes (écris les motifs essayés) : Lumen est alors permis (prix régulier). Aucun code de nomenclature ne porte ces lignes : écris « aucun code de nomenclature — à signaler au directeur B » ;
  (3) DOUBLE AVEC UNE LIGNE OU UN LOT — ex. un monument Lumen vs le code MP-I à 250 $ ; un sectionneur Lumen vs la ligne C-04 ; un coupe-feu Lumen vs « PERCEMENT PLANCHER » ; des tiges filetées Lumen vs les trousses de LOT-ECL : dis quelle ligne reste payée et laquelle tombe.
Niveau de confiance de chaque classement : CERTAIN (libellé ou prix identiques) / PROBABLE (même objet, prix différent : cite l'écart) / INCERTAIN (à trancher par le directeur B : donne les deux options chiffrées).
Procédure de recherche (obligatoire) : (i) pour chaque prix Lumen, cherche dans le catalogue les lignes dont `prix_a_utiliser` est égal au prix Lumen à ±0,011 près (une égalité exacte est une PREUVE d'équivalence ; hors égalité, regarde aussi ±3 %) ; (ii) 3 recherches par regex au minimum par famille (motifs courts et variantes : `CONDUIT`, `COND TME`, `CONN TME`, `COURR`, `COUV CARRE`, `BOITE CARRE`, `BOITE OCTOG`, `PRISE DUPLEX`, `PRISE USB`, `DDFT`, `PLAQUE`, `MONUMENT`, `INTERR 30A`, `SECTIONNEUR`, `PERCEMENT`, `COUPE`, `TIGE`, `ANCRAGE`, `AWG`, `RW90`, `TECK`, `FLEX`, `CONSEAL`, `MARRETTE`, `CORDE`) ; (iii) lis les `classe` (information seulement) et `date_dernier` / `projet_dernier` des candidats.
Pistes du chef B3 (chiffres lus par le chef — à RE-VÉRIFIER dans les fichiers, jamais à recopier sans relire ; ce sont des pistes, pas des conclusions) :
 - CONEMT1 / CONEMT3/4 et raccords APPTWC100S, APPTWC75S, APPTW100S, APPTW75S, APPTWCL100, APPTWCL75 ↔ assemblages « CONDUIT 1 nnC12 » / « CONDUIT 3/4 03C12 » (um=P, conduit + raccords + fils) et lignes C-05, C-07, D-13, D-14, E-08, E-09, F-08, G-02 (colonne « Base de quantité » : 690 m = C-05 35 + D-13 480 + E-08 175 ; 895 m = C-07 80 + D-14 330 + E-09 175 + F-08 280 + G-02 30 : vérifie ces additions sur le Détail).
 - Fils CAB12/1RW90BLK300, CAB12/1RW90WHI300, CAB12/1RW90GRE300, « CAB12/1RW90 ROUGE » (4 390 m = C-08 275 + D-15 2 400 + E-10 875 + F-09 840), CAB8RW90BLK / CAB8RW90GRE (UTA-01 : C-06 140 m), CAB16/2FAFT4300 (G-03 60 m = AI-08 du relevé Alarme incendie) ↔ assemblages « nnCcc » ou lignes fil.
 - Boîtes IBE52151K / IBE52C13 (66 : prises, data, JB postes, boutons, barrières) ↔ prix d'assemblage prise / data / interrupteur Dupuis (boîte + plaque + raccord inclus) et D-09, D-10, D-11, E-06 ; IBE72171K / IBE72C1 (46 = « 23 courses sous dalle x 2 ») ↔ D-16, E-11 ; IBE54151L (35 « JB éclairage ») ↔ F-10 et assemblage luminaire.
 - Dispositifs LEV16252W, LEV16352W, LEVT5633W, LEVGFNT1W, LEV80401NW ↔ PC-I, PU-I, PG-I et leurs assemblages (compare les quantités Lumen aux quantités du relevé : ex. LEVT5633W 10 vs PU-I 20 du relevé ; dis lequel gagne : le plan).
 - HUBS1R6PTDEHBLK (2 × 1 461,22 $ = 2 922,44 $, poke-through) ↔ MP-I (« MONUMENT PLANCHER » 250 $, repère METHODE) et les lignes Détail E-02, E-03.
 - HUBHBL1372 (3 sectionneurs HUM) ↔ C-04 et « INTERR 30A 2P 600V CEMA1 ».
 - TROCP25WB+10.1OZ (coupe-feu, 25) ↔ « PERCEMENT PLANCHER » (150 $ / 1 h) et D-12 (16), E-07 (7) (« coupe-feu » dans leur description).
 - VISTF3/8, VISDIA3/816BX50 (suspension des luminaires à la dalle) ↔ LOT-ECL (trousses 1 500 $), F-05, F-10 (« TIGE FILETE 3/8PO » existe au catalogue en um=P).
 - CONCONSEAL3/4 (14 m : UTA, VE-02N, HUM ×3, CH ×2), THO5333 (20), IBETEK75120 (4), CAB12TECK3C600V (10 m) ↔ C-01…C-04 (raccord LFMC ; C-03 dit « câbles existants » réutilisés : un câble TECK neuf pour les chaudières le contredit-il ?).
 - THOABRH03830 (63 m = 35 points × 1,8 m), IBE2210 (70) ↔ F-08 (« conduit EMT 3/4" + flexible ») et assemblage luminaire.
 - GRE430 (corde de tirage, 1) ↔ D-16, E-11 (« corde de tirage » dans leur description) ; IDE30452 (marrettes) ↔ tout assemblage de prise ou de conduit avec fil.
Sortie : (a) dans `doubles_comptes`, une entrée par groupe de lignes Lumen qui partagent le même partenaire : {"codes": [codes Lumen concernés + codes de nomenclature / Détail partenaires], "regle": "…", "quantites": "…"} — `regle` dit ce qui reste payé et ce qui tombe (« le plan gagne » ; « payé une fois par … » ; « inclus dans l'assemblage Dupuis <libellé exact> : pas de ligne Lumen » ; « 0 $ en ligne + lot ») ; `quantites` donne les quantités de part et d'autre avec leur source (cellule ou ligne lue) ; (b) dans `notes`, la TABLE COMPLÈTE des 38 lignes sous la forme « LUMEN <code> → <classe 1/2/3> → <libellé Dupuis exact + um + prix + temps | motifs de recherche> → <confiance> → entrée doubles_comptes n° k » ; (c) dans `notes`, trois sommes calculées par script depuis la colonne « Total » de la feuille : Σ INCLUS, Σ À CHIFFRER, Σ DOUBLE LOT/LIGNE, et leur total qui doit retomber sur 23 159,6714 $.

## RÈGLES D'ARTICLES DÉFINITIVES (décisions du chef de lot B3 — à APPLIQUER telles quelles ; elles REMPLACENT la règle PROVISOIRE de la section « Format de `src`, `u` et `art` »)

Libellés exacts du bordereau (feuille « Bordereau de prix » de `entree/reference-Bordereau_de_prix.xlsx` — à RELIRE dans le fichier, pas de mémoire) :
Section Électricité : 3.22 Démontage des éléments électriques (sous-titre « Démolition ») · 3.23 Raccordement des équipements mécaniques (sous-titre « Mécanique ») · 3.24 Nouveau panneau 600V · 3.25 Lot disjoncteurs · 3.26 MCC · 3.27 Prises doubles 15A-120V - usb · 3.28 Prises doubles 15A-120V · 3.29 Prises doubles 15A-120V MALT isolées · 3.30 Prises doubles 15A-120V GFI · 3.31 Percements, conduit filage et boîte de jonction · 3.32 Scan dalle béton · 3.33 Sorties informatique/réseau · 3.34 Moinument plancher [sic] (3.24 à 3.34 sous le sous-titre « Distribution ») · 3.35 Appareil de contrôle + appareils d'éclairage (sous-titre « Éclairage, éclairage d'urgence et contrôle ») · 3.36 Détecteur de fumée · 3.37 Panneau alarme incendie : déplacement annonciateur · 3.38 Panneau alarme incendie : mise en marche et certification (3.36 à 3.38 sous le sous-titre « Alarme incendie »).
Hors section Électricité : 5.11 Percement du plancher · 5.19 Démolition des systèmes électriques (section 5.0 « Construction spéciale et démolition », sous-titre « DÉMANTÈLEMENT D'ÉLÉMENT DE BÂTIMENT ») · 6.1 Conditions de mise en œuvre et autres · 6.2 Frais généraux, administration et profit (section 6.0 « Frais de chantier et Administration et profits »).

P0 — PRINCIPE. Un code va à l'article dont le libellé nomme son objet. TOUT le prix électrique de DR (matériel + main-d'œuvre) est ventilé dans la section Électricité (3.22 à 3.38) et, pour les frais de chantier, en 6.1. Les articles 5.11, 5.19 et 6.2 ne reçoivent AUCUN code (0 $ dans cette ventilation) : 5.11 et 5.19 sont dans la section 5.0 du général (« Démantèlement d'élément de bâtiment ») alors que 3.31 (« Percements, conduit filage et boîte de jonction ») et 3.22 (« Démontage des éléments électriques ») nomment déjà les mêmes objets DANS la section Électricité (en cas d'égalité de libellé, l'article de la section Électricité l'emporte) ; 6.2 = 0 parce que administration et profit = 0 % chez Dupuis (METHODE.md §2 point 1 : la marge est dans le prix vendant).
R1 — ENLEVER. Tout code -E → 3.22 (dépose d'un élément électrique existant). Exception unique : PA-E → 3.37 (l'annonciateur est un seul objet DÉPLACÉ : on ne scinde pas sa dépose et sa repose en deux articles). Ce que reçoit 5.19 : 0 $ (renvoi à 3.22).
R2 — RELOCALISER. Tout code -R → 3.22 : la ligne catalogue « RELO … » prix la dépose ET la repose en un seul temps (p = 0 le plus souvent) ; ce n'est pas un appareil NEUF, il n'entre donc pas dans l'article de sa famille (3.27, 3.28, 3.30, 3.33, 3.34, 3.35, 3.36), réservé aux appareils neufs. Exceptions : PA-R → 3.37 (« déplacement annonciateur ») ; MM-R et MT-R → 3.23 (débranchement/rebranchement d'équipements mécaniques au toit = « Raccordement des équipements mécaniques »). Hors plan, même logique : A-07, A-08, A-09, G-05 (RELO ou retrait temporaire + réinstallation d'interrupteurs, de luminaires, de dispositifs AI existants) → 3.22 ; A-10 (débrancher/rebrancher équipements de ventilation au toit) → 3.23 ; G-04 (relocalisation de l'annonciateur) → 3.37.
R3 — INSTALLER un appareil NEUF (-I et lignes équivalentes), selon la famille :
   PC-I → 3.28 · PU-I → 3.27 · PG-I → 3.30 (voir R11 pour les M.A.L.T.) ·
   SD-I, TV-I, LC-I, GA-I, D-11, E-06 → 3.33 (seul article de « sorties » ; ce sont des sorties de courant faible — câblodistribution, contrôle d'accès, boutons d'appel — dont le système est fourni par d'autres : boîte + plaque + conduit vide ; 3.35 est écarté parce que son « contrôle » est rattaché au titre « Éclairage, éclairage d'urgence et contrôle », donc au contrôle d'éclairage) ·
   MP-I, E-03 → 3.34 (monument / boîte de plancher) ·
   INT-I, DM-I → 3.35 (appareils de contrôle d'éclairage : interrupteurs, détecteurs de mouvement) ·
   luminaires neufs et appareils d'éclairage : LA1-I, LC1-I, LC11-I, LC13-I, LE-I, ENC-I, ENCU-I, L14-I, L22-I, L4-I, LLIN-I, et l'enseigne Z6-I (éclairage d'urgence, même sous-titre) → 3.35 ·
   TH-I, MM-I, MT-I → 3.23 (commande ou raccordement d'un équipement mécanique par l'électricien) ·
   BJ-I → 3.31 (voir R4) · D-09, D-10 → 3.31 (boîtes de jonction + raccord) ·
   BC-I, HP-I, DF-I, SM-I → 3.36 (famille alarme ; 3.36 est le seul article d'appareils d'alarme incendie) · PA-I → 3.37.
R4 — CHEMINS DE CÂBLES, FILAGE, BOÎTES, PERCEMENTS → 3.31, quel que soit le système desservi. Sont concernés : tout conduit, tout fil ou câble, toute boîte de jonction ou de tirage, connecteurs, supports, corde de tirage, et tout percement de dalle (carottage + coupe-feu) : BJ-I, D-09, D-10, D-12, E-07, C-05, C-06, C-07, C-08, D-13, D-14, D-15, D-16, E-08, E-09, E-10, E-11, F-08, F-09, G-02, G-03. Motif : le libellé de 3.31 les nomme tous (« Percements, conduit filage et boîte de jonction ») sans restreindre le système ; les articles par système ne reçoivent que les APPAREILS, leur pose et leur raccordement. Ce que reçoit 5.11 « Percement du plancher » : 0 $ (D-12 et E-07, carottages de dalle pour conduits, restent à 3.31 : même objet, article de la section Électricité). Ce que reçoit 3.23 des conduits/fils C-05…C-08 : rien (3.23 ne reçoit que les raccordements finaux, voir R5).
R5 — RACCORDEMENTS FINAUX D'ÉQUIPEMENTS MÉCANIQUES : C-01 (UTA-01), C-02 (VE-02N), C-04 (humidificateurs) → 3.23 ; C-03 (chaudières CH-01/CH-02 : vérifier et réutiliser les tiroirs CCM-1 F15A) → 3.26 « MCC » (seule ligne du Détail qui touche un centre de commande de moteurs ; sinon 3.26 resterait vide ; alternative écartée : 3.23).
R6 — DISTRIBUTION : B-01 (panneau PP-3 neuf) et B-09 (fiches dactylographiées + identification des panneaux) → 3.24 ; B-02 à B-08 (disjoncteurs) → 3.25 ; LOT-DIST → 3.24 comme `art` du code (un seul `art` par code) avec la règle de VENTILATION DU MONTANT : 3 400 $ (panneau NF 225 A 42 cct) → 3.24 et 2 800 $ (EDB 1P 95 $ × 20 + EJB 3P 300 $ × 3) → 3.25. 3.26 ne reçoit que C-03.
R7 — ÉCLAIRAGE : LOT-ECL (luminaires neufs + Z6 + trousses), F-05 (rangées Axis : suspension et alimentation de rangée) et F-10 (boîtes de jonction d'éclairage, chaînes de retenue, quincaillerie : même geste de suspension/retenue des luminaires, devis 16.5 ; alternative écartée : 3.31) → 3.35, en plus des -I de R3.
R8 — ALARME INCENDIE : LOT-DET (2 détecteurs) → 3.36 ; LOT-JCI (services JCI/Simplex), G-06 (assistance programmation / vérification ULC-S537) et G-07 (sous-traitance JCI/Simplex) → 3.38 « mise en marche et certification » ; G-04 et PA-* → 3.37 ; G-05 → 3.22 (R2) ; G-02, G-03 → 3.31 (R4).
R9 — SCAN DE DALLE : X-01 (« SCAN DALLE BETON ») et LOT-GPR (géoradar) → 3.32 (même article, même objet : un seul des deux sera payé, c'est une affaire de double compte, pas d'article).
R10 — FRAIS DE CHANTIER : H-01, H-02, H-03, H-04, X-02 (nacelle : moyen d'accès de chantier) et A-11 (maintien de la continuité de service, devis 1.16 : condition de mise en œuvre ; alternative écartée : 3.22) → 6.1 « Conditions de mise en œuvre et autres ». 6.2 reçoit 0 $ (P0).
R11 — PRISES M.A.L.T. ISOLÉES (3.29). La famille PG (PRISE DDFT) contient aussi des prises M.A.L.T. isolées (reserves.md R-007 : « les deux variantes tombent ici dans PRISE DDFT, à départager au zoom »). Le relevé ne les sépare pas et la nomenclature n'a pas de code pour elles : on NE PEUT PAS ventiler. Tout PG-I → 3.30 ; 3.29 reçoit 0 $ tant que l'équipe A ne sépare pas les M.A.L.T. (à écrire tel quel dans `regles_articles` ET dans `notes`).
R12 — PORTÉE ABSENTE DU RELEVÉ. Un code dont la portée n'existe pas dans rapport-releve.md (ex. BC-I, TV-R, ENC-I…) reçoit quand même l'article de sa règle (correspondance de précaution).
Tu APPLIQUES ces règles. Si, en lisant le Détail ou le bordereau, une règle te semble contredire un libellé, tu l'appliques QUAND MÊME et tu écris dans `notes` : « CONTRADICTION POSSIBLE : <code> règle <Rn> vs <raison> » — c'est le chef qui tranche.

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

(Pour toi, B3-1 : tu n'écris aucune ligne `lignes`, mais ces conventions de `src`, `u` et `art` valent pour tout texte de `doubles_comptes` qui cite un libellé du catalogue — copie toujours le libellé EXACT depuis le CSV avec `repr(r['description'])`, jamais de mémoire.)

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

## Squelette EXACT de ton fichier (releveur B3-1)
```json
{
  "niveau": "releveur",
  "nom": "B3-1",
  "modele_demande": "haiku",
  "effort_demande": "xhigh",
  "lignes": [],
  "articles": {"<code>": "<article>", "...": "... (120 codes, chacun une fois)"},
  "regles_articles": ["P0 — <énoncé> — parce que … — exceptions : … — ce que reçoit l'autre article : …", "R1 — …"],
  "doubles_comptes": [
    {"codes": ["<code Lumen>", "<code nomenclature ou Détail>"], "regle": "…", "quantites": "…"}
  ],
  "notes": ["LIBELLÉS BORDEREAU VÉRIFIÉS : …", "CONTRADICTION POSSIBLE : …", "PORTÉE ABSENTE DU RELEVÉ — correspondance de précaution : …", "LUMEN <code> → …"]
}
```
Écris avec `json.dump(obj, f, ensure_ascii=False, indent=2)`. `lignes` est une liste VIDE. Chaque code n'apparaît qu'UNE fois dans `articles`.

## Vérifications avant d'écrire un JSON (ARCHITECTURE.md §6, tous niveaux)
1. Le JSON se charge (`python3 -c "import json;json.load(open('...'))"`) et contient `lignes` + `notes`.
2. Chaque ligne a un `src` qui pointe vers un libellé/une cellule réellement lu ; tout code du sous-lot est présent
   une et une seule fois ; `q` est `null` partout.
3. Pas de médiane : pour chaque ligne Dupuis, relire la ligne avec `ligne(desc, um)` et vérifier
   `p == float(prix_a_utiliser)` et `h == float(temps_a_utiliser)` (sauf p = 0 forcé par un lot, écrit dans `src`).
4. Un rapport d'agent n'est pas une preuve : le niveau supérieur juge sur le fichier `lots/*.json`, pas sur le récit.

Vérifications propres à B3-1 (à exécuter par script, avec les codes de sortie vérifiés) :
 5. `articles` contient EXACTEMENT les 120 codes de ta liste (ni un de plus, ni un de moins, aucun des 21 codes de B3-2), chacun une fois ; chaque valeur est l'un de 3.22 … 3.38 (sauf 3.26 et 3.29 qui restent vides pour tes 120 codes), 6.1 ; AUCUNE valeur 5.11, 5.19 ou 6.2 ; les comptes par article égalent ceux du contrôle d).
 6. `regles_articles` contient P0 et R1 à R12 (13 entrées au moins), chacune avec son motif.
 7. `doubles_comptes` : chaque entrée a exactement les clés `codes` (liste de 2 codes ou plus), `regle`, `quantites` ; chaque entrée contient AU MOINS un code Lumen (sinon elle est à B3-3) ; chaque code Lumen cité existe dans la colonne « Code Lumen » de la feuille ; chaque autre code cité existe dans la nomenclature, dans la feuille Détail (A-01 … H-04), parmi les lots (LOT-*), X-01/X-02, ou parmi les entrées AI-01 … AI-09 du relevé Alarme incendie et C-SUSP du relevé d'éclairage ; les 38 codes Lumen apparaissent TOUS, au moins une fois, dans `notes` (table) ; les trois sommes retombent sur 23 159,6714 $.
 8. Rouvre au hasard au moins 5 libellés du catalogue cités (`ligne(desc, um)`) et 5 cellules Lumen/Détail citées : p, h, quantités doivent correspondre à ce que tu as écrit.

## Quand tu as fini
Écris UNIQUEMENT `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-1.json`, vérifie qu'il se charge en JSON (`python3 -c "import json;json.load(open('/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B3-1.json'))"`), puis réponds en UNE ligne : nom du fichier écrit + nombre d'articles (120 attendus) + nombre d'entrées `doubles_comptes`. Tu t'arrêtes ensuite. Tu ne délègues à personne et tu ne lances aucun agent.
