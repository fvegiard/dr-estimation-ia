# Écart relevé automatique (v2) vs relevé estimateur — S-1689 (Pultrusion)

Vérificateur indépendant, 2026-09-22.

**Sources**
- **IA (v2)** : `S-1689-Rapport-de-metre.md` et `travail/occurrences-{texte,visuel}.csv`, soit 256 marques retenues.
- **Référence** : `reference/TAKE OFF ECL.pdf`. C'est un scan d'une page, pivoté de 180° (version redressée : `travail/ecart-preuves/00-reference-scan-redresse.png`). La transcription complète est dans `reference-quantites.csv` : 16 lignes, toutes lisibles.
- **Plans vectoriels** : `INBOX/S-1689/Pultrusion Plan Électrique.pdf`. La légende E001_2 est à la page 3, E002_2 à la page 4 et E005 à la page 5.

**Conventions**
- Les coordonnées sont en points PDF.
- Chaque preuve dans `travail/ecart-preuves/` montre deux vues côte à côte : à gauche le plan brut (rendu depuis le PDF vectoriel), à droite le même plan avec les marques de l'IA (en rouge) et mes constats (en bleu).

## 0. La référence est PARTIELLE

La référence est un « Relevé matériel – demande de prix » ACCEO de 16 lignes, sans feuille, sans zone et sans prix. Elle ne couvre que trois domaines :
- les **luminaires** ;
- les **contrôles d'éclairage** : BlueEcosystem et Wattstopper ;
- l'**éclairage d'urgence**.

Elle ne compte pas l'alarme incendie, les prises, la télécom, le CVC, la distribution ni les interrupteurs ordinaires. **Le verdict se limite à ces trois postes.**

## 1. Correspondance des nomenclatures

| Ligne de la référence | Réf. | Libellé(s) IA | IA | Justification |
|---|--:|---|--:|---|
| FIXTURE TYPE A | 2 | Luminaire A 2x4 24W | 2 | Même lettre dans la légende E001_2 (tableau des appareils d'éclairage) |
| FIXTURE TYPE B | 4 | Luminaire B 2x4 30W | 18 | Même lettre. Mais **14 des 18 marques (E005) sont en réalité des D**, voir §3.1 |
| FIXTURE TYPE C | 7 | Luminaire C 2x4 38W | 7 | Même lettre |
| FIXTURE TYPE D | 0 | *(aucun libellé)* | 0 | **L'IA n'a créé aucun libellé D**, alors que la légende a une ligne « ⊕D rond haut plafond Technilight TLHBUS150A80 150 W suspendu » (`02b-…png`) |
| FIXTURE TYPE E | 6 | Luminaire E réglette 26W | 4 | Même lettre |
| FIXTURE TYPE F | 4 | Luminaire F 2x4 surface 30W | 4 | Même lettre |
| FIXTURE TYPE D1 | 35 | Luminaire D1 2x2 30W | 35 | Même lettre |
| BBR-HV BLUEECOSYTEM | 10 | Contrôleur BBR-HV (Z1) | 10 | Légende BlueEcosystem, ligne 1 |
| ROOM-PIR BLUEECOSYTEM | 11 | Détecteur RooM-PIR (DP) | 13 | Légende BlueEcosystem, ligne 2 |
| SBWS-4B BLUEECOSYTEM | 7 | Interrupteur — type à confirmer | 18 | L'IA ne distingue pas le SBWS-4B (« $ » barré) du « $ » simple ni du « ¥$ » (R-005). Ce libellé fourre-tout est rapproché de la ligne SBWS faute de mieux, voir §3.4 |
| DETECTEUR WATTSTOPER WT-2255 | 2 | Interrupteur détecteur présence | 1 | Aucun symbole ⊙C (WT-2255) n'est dessiné. Les objets équivalents sont les « ¥$ » (PW-200) : c'est un choix de modèle de l'estimateur, rapproché par fonction |
| RUNNING MAN RMXL-UDC | 3 | Indicateur sortie mural + plafond | 2+1 | Légende d'urgence, lignes 1 et 2 |
| TETE URG SIMPLE N1 | 2 | Phare simple LED | 3 | Légende N1 |
| TETE DOUBLE URG N2 | 7 | Phare double LED | 7 | Légende N2 |
| BATTERIE UNIT SLC 2TETE | 1 | Batterie 2 phares 144W — à confirmer | 1 | Batterie 2 têtes sans pictogramme de sortie |
| COMBO RMSLC 2TETE | 4 | Batterie 2 phares c/a sortie 144W | 4 | RMSLC avec indicateur |

**Hors périmètre de la référence** : ce que l'IA relève et que la référence ne compte pas.
- Alarme : 13.
- Prises : 46.
- Télécom : 10, dont 1 conduit à métrer.
- Chauffage : 29.
- Mécanique : 9.
- Distribution et divers : 14.
- Schéma de contrôle extérieur d'E006 : 5 (minuterie, cellule PE, sélecteur, contacteur, programmation).

Soit **126 marques non comparables**. À l'inverse, la référence ne contient ni câblage, ni longueurs, ni main-d'œuvre : rien de ce qu'elle compte n'échappe au périmètre de l'IA.

## 2. Tableau d'écart par famille

| Famille | Réf. | IA | Écart | Écart % | Explication |
|---|--:|--:|--:|--:|---|
| Luminaires | 58 | 70 | +12 | +20,7 % | B : +14. Ce sont les 14 luminaires de l'abri E005, qui sont des **D** au plan ; la référence porte D = 0. E : −2, deux réglettes manquées par l'IA |
| Commandes / interrupteurs / détecteurs | 30 | 42 | +12 | +40,0 % | Libellé « interrupteur » fourre-tout : +11 face aux SBWS. RooM-PIR : +2, l'IA a raison. ¥$ : −1, un détecteur mal typé en interrupteur |
| Secours | 17 | 18 | +1 | +5,9 % | Phare « U » sur PS(4) compté à tort (+1). Les batteries SLC/RMSLC sont justes |
| Alarme incendie | — | 13 | n/c | n/c | Absente de la référence |
| Prises | — | 46 | n/c | n/c | Absente de la référence |
| Télécom / data | — | 10 | n/c | n/c | Absente de la référence |
| Distribution / panneaux / sectionneurs | — | 14 | n/c | n/c | Absente de la référence |
| Mécanique / chauffage | — | 38 | n/c | n/c | Absente de la référence |
| Autres (commandes E006) | — | 5 | n/c | n/c | Absente de la référence |
| **Total comparable** | **105** | **130** | **+25** | **+23,8 %** | Somme des \|écarts\| par ligne : 31, soit 29,5 % |

### Ventilation par feuille (familles dont l'écart n'est pas nul)

La référence ne donne pas de feuille. La colonne « vérité plan » est mon propre recomptage.

| Famille | IA E002_2 | IA E005 | Vérité plan E002_2 | Vérité plan E005 | Réf. |
|---|--:|--:|--:|--:|--:|
| Luminaires | 56 | 14 (étiquetés B) | 58 (A2 B4 C7 D1 35 E6 F4) | 14 (D) | 58 |
| Commandes | 42 | 0 | 42 (Z1 10, DP 13, symboles $/$ barré/¥$ 19) — même total que l'IA, types différents | 0 | 30 |
| Secours | 18 | 0 | 17 | 0 | 17 |

La référence a exactement la valeur du plan pour E002_2 en luminaires (58) et en secours (17). **Elle exclut l'abri E005** (D = 0).

## 3. Chaque écart : qui a raison, et la preuve

| # | Ligne | Réf. | IA | Verdict | Preuve |
|---|---|--:|--:|---|---|
| 3.1 | B / D (E005) | B 4, D 0 | B 18, D 0 | **Plan : 14 D. L'IA a le bon nombre mais le mauvais type. La référence exclut l'abri, pour une raison indécidable** (autre lot ? prix séparé ?). | Sur E005, 14 symboles ⊕ avec la lettre dessinée **D** et « PP(12) MH: 21 », en x = 1794 et 1974, y = 440 à 1040. Le « B » que l'IA a lu est un minuscule texte vectoriel caché sous le cercle (police d'environ 4,7 pt). La légende donne D = rond haut plafond de 150 W, suspendu, et B = 2'x4' encastré de 30 W, ce qui fait **un écart de prix majeur**. L'IA a signalé la contradiction (R-004) mais a gardé B, et n'a pas de libellé D. Fichiers : `02a-E005-type-D-dessine-vs-B-IA.png` et `02b-legende-type-D-rond-haut-plafond.png` |
| 3.2 | Luminaire E | 6 | 4 | **La référence a raison.** L'IA a manqué 2 réglettes. | Chaque escalier de la mezzanine a 2 barres « E » : h à (1216,309) et (≈1302,308), k à (1216,792) et (≈1302,793). L'IA ne marque que la première barre de chaque escalier. Les escaliers du RDC n'ont qu'une barre chacun, à (1984,308) et (1990,792), toutes deux marquées. Total au plan : 2 + 2 + 1 + 1 = 6. Fichiers : `01a…01d-*.png`. **Aucune réserve ne couvre ces oublis.** |
| 3.3 | RooM-PIR | 11 | 13 | **L'IA a raison, selon le plan.** | 13 mots texte « DP » sur E002_2 (`feuilles.csv` : DP×13), chacun avec son cercle. Les 2 « en trop » sont au RDC, à (2001,297) dans l'escalier h et à (2037,808) dans l'escalier k, chacun à côté d'un Z1. La référence compte pourtant les 10 Z1, y compris ces 2 du RDC. Fichiers : `03a-DP-RDC-escalier-h.png` et `03b-DP-RDC-escalier-k.png` |
| 3.4 | SBWS-4B / interrupteurs | 7 | 18 | **La référence a raison pour les SBWS. L'IA est inutilisable pour cette ligne.** | Les 19 symboles de type interrupteur (18 génériques et 1 PW) se répartissent ainsi : **7 portent une lettre de zone a–g** : a (1144,301), g (1129,375), f (1175,419), c (1130,554), e (1177,556), d (1103,701), b (1144,789). C'est exactement 7, le nombre de SBWS de la référence, et la barre du SBWS est visible sur c et d. Viennent ensuite **4 $ simples d'escalier** : (1175,303), (1174,816), (1971,289) et (2036,817). Enfin, **7 « ¥$ »** (flèches en Y, tournées) : (1128,303), (1196,639), (1129,737), (1129,786), (1853,383), (1873,347) et (1896,383). S'y ajoute 1 « $ » en salle des serveurs, (1176,696), de type indécidable. L'IA met tout sous un seul libellé. Fichiers : `04-interrupteurs-zoom.png`, `04b-legende-SBWS-4B.png` et `04c-legende-interrupteurs.png` |
| 3.5 | WT-2255 / ¥$ | 2 | 1 | **L'IA a tort sur le type** : le « $ » de la salle des serveurs (1196,639) est un ¥$ (PW-200) et elle l'a compté en interrupteur. Pour le compte de la référence (2 contre 7 ¥$ lisibles), l'écart est **indécidable** : l'estimateur n'a peut-être codé que les 2 ¥$ droits, et les 5 ¥$ tournés sont à confirmer. | `05-interrupteur-detecteur-salle-serveurs.png` et `04-interrupteurs-zoom.png`. La v1 avait 2 ¥$ droits : c'est une régression. |
| 3.6 | Phare simple N1 | 2 | 3 | **La référence a raison (probable).** | Le symbole « carré U + cône » à (1175,580) est sur le circuit **PS(4)**, qui est l'éclairage normal. Or tous les phares sont sur un circuit CC X# (légende d'urgence), et le symbole n'est pas dans la légende. Les 2 autres, (1118,803) et (1132,715), sont de vrais N1 sur X1. L'IA l'a signalé (R-027) mais l'a compté. Fichier : `06-phare-simple-U-PS4.png` |
| 3.7 | Batteries SLC / RMSLC | 1 / 4 | 1 / 4 | **Exact.** | La batterie « 144W X1 » de la salle technique (1059,326) a 2 têtes sans pictogramme, et l'IA l'a séparée des 4 RMSLC. Fichiers : `07a-batterie-SLC-sans-indicateur.png` et `07b-legende-batteries.png` |

**Exact à l'unité** : A, C, D1, F, BBR-HV, indicateurs de sortie, phares doubles et batteries.

### Contrôle aléatoire : 10 marques IA

**Méthode.** Population : les 256 marques non exclues, prises dans l'ordre texte puis visuel. Tirage : `random.seed(1689)` puis `random.sample`.

| # | Indice | Feuille | Libellé IA | x,y | Constat sur le rendu | OK ? |
|--:|--:|---|---|---|---|---|
| 1 | 92 | E002_2 | Prise double | 569,454 | Prise double PS(23) présente | oui |
| 2 | 107 | E002_2 | Plinthe 1500W | 613,557 | Plinthe « 1500W » présente | oui |
| 3 | 128 | E002_2 | Luminaire D1 | 999,300 | D1 PS(2), salle technique | oui |
| 4 | 136 | E002_2 | Luminaire D1 | 1062,405 | D1 PS(2)g | oui |
| 5 | 166 | E002_2 | Luminaire C | 1216,522 | C PS(2)e | oui |
| 6 | 181 | E002_2 | Luminaire B | 1240,642 | 2x4 B, salle des serveurs | oui |
| 7 | 184 | E002_2 | Luminaire D1 | 1001,685 | D1 PS(4)c | oui |
| 8 | 201 | E002_2 | Phare simple | 1132,715 | Phare simple X1, toilettes | oui |
| 9 | 216 | E002_2 | Interrupteur (à confirmer) | 1971,289 | $ simple, escalier h du RDC. L'objet existe, le type est non tranché | oui (type vague) |
| 10 | 238 | E002_2 | Prise double | 1851,361 | Prise double PS(40) | oui |

**Résultat : 10 sur 10.** Aucune marque tirée n'est un faux positif, à 5 pt près. Fichier : `10-echantillon-10-marques-seed1689.png`.

Le tirage ne touche aucune marque d'E005. Les erreurs de v2 sont des erreurs de **type** et d'**omission**, pas de faux positifs.

## 4. Verdict

### 4.1 Écart net sur les objets communs

- **Contre la référence telle quelle** : +25 sur 105, soit **+23,8 %**. La somme des écarts absolus est de 31.
- **Écart imputable à l'IA**, après arbitrage par le plan (les 14 D d'E005 et les 13 DP comptent comme vérité plan) :
  - interrupteurs non typés : +11 ;
  - ¥$ mal typé : −1 ;
  - phare « U » : +1 ;
  - réglettes E manquées : −2.

  Le net est de **+9 sur 105, soit +8,6 %** (somme absolue : 15). S'y ajoutent **14 luminaires dont le type est faux** (B au lieu de D) : le compte est juste, mais le prix est faux.

### 4.2 Par poste majeur (critère Francis : ≤ 10 % par poste, ≤ 5 % au total)

| Poste | Contre la référence | Imputable à l'IA | Critère |
|---|--:|--:|---|
| Luminaires | +20,7 % | −3,4 % en quantité, mais 14 luminaires sur 70 mal typés (20 %) | ✗ brut ; ✗ en type |
| Commandes | +40,0 % | +33,3 % | ✗ |
| Secours | +5,9 % | +5,9 % | ✓ |
| **Total** | **+23,8 %** | **+8,6 %** | ✗ (> 5 %) |

### 4.3 Items manquants NON signalés en réserve (critère : aucun)

**2 items** : les 2 réglettes E de la mezzanine, à E002_2 (≈1302,308) dans l'escalier h et (≈1302,793) dans l'escalier k. **Le critère n'est pas respecté.**

Les autres écarts sont couverts par une réserve (R-004 pour B/D, R-005 pour les interrupteurs, R-027 pour le phare). Mais dans chaque cas, la décision prise est la mauvaise.

### 4.4 Utilisable tel quel ?

**Non.** Pour la demande de prix « éclairage », le relevé devient utilisable après 4 corrections, qui prennent environ 15 minutes :
1. Retyper les 14 luminaires d'E005 en **D** (150 W haut plafond) et créer le libellé D.
2. Ajouter 2 réglettes E, ce qui en porte le total à 6.
3. Scinder les interrupteurs en 7 SBWS-4B (zones a–g), 4 $ simples, les ¥$ (dont celui de la salle des serveurs) et 1 à confirmer.
4. Retirer le phare « U » sur PS(4), ce qui ramène les N1 à 2.

L'estimateur doit, de son côté, confirmer :
- l'exclusion de l'abri (D = 0) ;
- les 2 RooM-PIR du RDC ;
- le nombre de détecteurs WT/PW (2 contre 7 ¥$ lisibles).

## 5. Erreurs systématiques de l'IA : règles à corriger

1. **Elle fait confiance à la couche texte plutôt qu'au glyphe dessiné** (E005 : texte caché « B » contre lettre dessinée D). Règle : si le texte extrait contredit la lettre dessinée ou la forme du symbole de la légende, **le dessin gagne**. Tout texte de moins d'environ 5 pt placé sous un symbole est un attribut de bloc, pas une étiquette.
2. **Sa nomenclature est incomplète** : pas de D, pas de ¥$ distinct du $, pas de SBWS distinct. Règle : **une ligne de légende donne un libellé**, sans exception, même si ce type semble absent. Contrôle : nombre de lignes de légende = nombre de libellés.
3. **Elle fusionne les variantes de symboles tournés** ($, $ barré, ¥$). Règle : garder des compteurs séparés, et utiliser la lettre de zone de séquence comme clé du SBWS (un SBWS par zone). Si c'est indécidable, donner une borne (« SBWS 7 à 18 ») plutôt que d'agréger.
4. **Elle manque les luminaires répétés ou appariés** (réglettes). Règle : contrôler la symétrie entre les pièces et les escaliers répétés, et rapprocher le nombre de lettres de type dessinées du nombre de marques.
5. **Elle ne suit pas ses propres réserves.** Un objet hors légende, ou sur un circuit incohérent (un phare sur PS au lieu de X#), ne se compte pas dans la classe voisine : il se met en « à confirmer », hors total.

## 6. v1 → v2

La v1 est dans `archives/S-1689-v1/`. Je l'ai lue et mes jugements ci-dessous ont été vérifiés sur le plan.

- **Comparable** : v1 = 131, v2 = 130, référence = 105.
- **Écart imputable** : v1 +10 (9,5 %, |Σ| 12) ; v2 +9 (8,6 %, |Σ| 15), plus 14 luminaires mal typés.
- **Corrigé** : la batterie SLC est séparée des RMSLC (1/4, exact).
- **Non corrigé** : interrupteurs toujours fusionnés (17 → 18) ; phare « U » toujours compté (3).
- **Régressions** :
  - E005 retypé de D (juste en v1) en B, parce que le texte caché l'a emporté sur le dessin, et le libellé D a disparu ;
  - réglettes E : 5 → 4 (−2 au lieu de −1) ;
  - ¥$ de la salle des serveurs : 2 → 1, parce qu'il est maintenant noyé dans les interrupteurs.
- **Net** : la chaîne corrigée n'est pas meilleure sur l'éclairage. Elle a gagné en réserves et en périmètre (E006, notes), mais elle a perdu en fidélité au dessin.
