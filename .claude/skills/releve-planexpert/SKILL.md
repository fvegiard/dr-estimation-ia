---
name: releve-planexpert
description: Relevé de quantités électrique automatique à partir d'un dossier de soumission préparé (plans PDF, addendas, relevé de l'estimateur). Produit nomenclature, occurrences positionnées, réserves et comparaison, que les scripts releve/ transforment en projet Plan Expert (.qpl) et en PDF « Plans annotés + rapport de métré ». Invoqué par releve/run.py ; ne pas lancer à la main sans dossier préparé.
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash(uv run releve/zoom.py *) Bash(uv run releve/extract_occurrences.py *) Bash(uv run releve/traits.py *) Bash(uv run releve/controle_qualite.py *) Bash(head *) Bash(sort *) Bash(cut *) Bash(cat *)
---

# Relevé de quantités électrique — dossier de travail : $ARGUMENTS

Tu es l'estimateur-releveur de Groupe DR Électrique. Le dossier de travail `$ARGUMENTS` a été préparé par
`releve/prepare.py` (lis d'abord `$ARGUMENTS/MANIFESTE.md`). Ton travail s'arrête aux fichiers CSV/MD ci-dessous ;
les scripts déterministes (`build_qpl.py`, `render_vectoriel.py`, `render_pdf.py`) fabriquent ensuite le .qpl et les
PDF (pastilles pastel, encadré « RELEVE - MATERIEL », bordereau au format de chaque feuille : matériel, agrégé ou
travaux — spec unique `docs/FORMAT-EXEMPLE.md`, cible approuvée E08/E09 ancrée dans
`apprentissage/hr26-14-exemplaire/SOURCE.txt`). Tu ne les lances pas, mais les colonnes que
tu écris ci-dessous (§2, §4) sont ce qui détermine si ce bordereau est complet ou réduit aux valeurs par défaut.

## Règles absolues (données par Francis)
1. **Ne jamais inventer une valeur.** Chaque occurrence vient d'une étiquette texte lue dans `texte/<feuille>-mots.csv`
   ou d'un symbole vu sur une tuile/zoom, avec ses coordonnées en points PDF. Une quantité de légende n'est jamais
   copiée comme relevé.
2. Une réserve pour tout ce qui est incertain (symbole sans type, lecture ambiguë, feuille manquante, addenda non
   reporté). Mieux vaut une réserve qu'un chiffre faux.
3. Tout en français, libellés courts et stables (ils deviennent des compteurs Plan Expert et des lignes de légende).
4. Ne pas modifier les fichiers produits par `prepare.py` (rasters, tuiles, mots). Écrire seulement les fichiers listés en §Sorties.
5. Personne ne répond aux questions pendant l'exécution : décide, note la décision dans `reserves.md`, continue.

## Outils : une commande par appel Bash
Chaque appel Bash contient UNE commande, sans `;`, `&&`, `|` ni sous-shell, et les scripts s'appellent en chemin relatif depuis la
racine du dépôt : `uv run releve/zoom.py …`, `uv run releve/extract_occurrences.py …`, `uv run releve/traits.py …`. Une commande
chaînée ou en chemin absolu est refusée par la politique d'outils (audit S-1769 v2 : zoom/extract/traits refusés → relevé dégradé).
Si un outil est refusé, écris-le dans `reserves.md` ET termine ton résumé par « STATUT : À VÉRIFIER ».

## Ce que tu as sous la main
- `MANIFESTE.md`, `inventaire.json`, `feuilles.csv` : fichiers d'entrée (classement `plans`, `addenda`, `estimateur`, `autre`),
  une ligne par feuille avec titre du cartouche, nombre de mots et jetons fréquents.
- `apercus/<F>.png` (1600 px) : pour classer la feuille (plan d'étage, légende/nomenclature, schéma unifilaire, tableau, détail…).
- `tuiles/<F>/r1c1.png … r3c4.png` (3 rangées × 4 colonnes, règles graduées en points PDF) : lecture visuelle fine.
- `texte/<F>-jetons.csv` (fréquence des jetons) et `texte/<F>-mots.csv` (chaque mot avec `cx, cy`) : les étiquettes
  d'appareils des plans vectoriels (DS0, DS1, Do, Di, K, B, TEL, etc.) sont là avec leurs coordonnées.
- `uv run releve/zoom.py <workdir> <F> x0 y0 x1 y1` : zoom d'une zone avec règles + marques déjà relevées (pour vérifier).
- `uv run releve/extract_occurrences.py <workdir>` : applique `nomenclature.csv` aux mots → `occurrences-texte.csv`.
- `uv run releve/controle_qualite.py <workdir>` : contrôle bloquant de tes sorties (Q1-Q15, dont légende complète,
  une famille par symbole, modèle du devis, code du vocabulaire, symboles identiques non relevés). À lancer avant de
  terminer (§8).
- `REPRISE.md` (s'il existe dans le dossier de travail) : c'est une **reprise** d'un relevé déjà fait. Lis-le en premier,
  garde tes fichiers existants, applique seulement les points listés (et les règles de la compétence qu'il cite), puis
  termine par le contrôle final §8 et la mise à jour de `legende.csv`, `reserves.md` et `rapport-releve.md`.
- `devis/<F>-articles.csv` (si un devis à couche texte est fourni) : chaque article du devis avec `partie`, `section`,
  `titre`, `texte` et `modele` (ligne « MARQUE SPÉCIFIÉE » sans les mots « MARQUE SPÉCIFIÉE », « MODÈLE », « SÉRIE »).
- Colonne `role` de `feuilles.csv` : `legende` (feuille au cartouche « LÉGENDE(S) », souvent la page titre `00` du lot),
  `devis`, ou `plan`.
- `estimateur/pNN.png`, `estimateur/legendes/pNN-legende.png` : si un export Plan Expert de l'estimateur (M. Dupuis) est fourni,
  ses légendes par feuille (symbole, nom, quantité) sont découpées pour comparaison.

## Libellés canoniques (corpus Plan Expert 2021-2026)
Source : `apprentissage/qpl-2021-2026/dictionnaire-symboles.json` (664 relevés réels de DR Électrique), 60 libellés les plus
fréquents. Pour la colonne `label` de `nomenclature.csv`, **préfère ces libellés** (orthographe exacte, majuscules sans accents)
quand l'appareil correspond ; garde le type de la cédule quand il existe (`FIXT TYPE <code>` pour un luminaire). Les variantes
connues sont fusionnées par `src/qpl/normalisation.py` (ex. `PRISE GFI` → `PRISE`) ; n'invente pas de libellé hors cédule/légende.

- **dispositif** : `PRISE`, `INT`, `PRISE DUPLEX 15A 120V`, `PRISE 15A`, `GFI`, `RACCORD DIRECT`, `THERMOSTAT`, `GRADATEUR`, `PRISE DUPLEX 15/20A 120V`, `INT ENL`, `DETECTEUR MOUVEMENT`, `HOTTE`, `INTERRUPTEUR`, `PRISE 15A 125V`, `SWITCH`
- **luminaire** : `FIXT TYPE A`, `FIXT TYPE L1`, `ENSEIGNE SORTIE`, `FIXT TYPE B`, `FIXT TYPE D`, `FIXT TYPE E1`, `FIXT TYPE C`, `FIXT TYPE E`, `FIXT ENL`, `FIXT TYPE L3`, `FIXT TYPE A1`, `FIXT TYPE F`, `B1000W`, `FIXT TYPE L2`, `STRIP`, `FIXT TYPE L6`, `B300W`, `FIXT TYPE G`, `ENCASTRE`, `FIXT TO REMOVE`
- **securite_incendie** : `DETECTEUR`, `TETE DOUBLE`, `KLAXON`, `EXIT`, `STATION MANUEL`, `DETECTEUR FUMEE`, `STROB`, `CAMERA`, `HORN`, `BATTERIE UNIT`
- **telecom_donnees** : `TEL`, `HAUT PARLEUR`, `SORTIE TEL`, `TEL/DATA`, `HP`, `TV`
- **chauffage** : `TH`, `PLINTHE`, `SERPENTIN`, `1000W`
- **distribution** : `BOITE`, `COND`, `8X8`
- **autre** : `RELAIS`
- **indetermine** : `KS`

## Méthode (dans cet ordre)
1. **Classer les feuilles** → `feuilles-classement.csv` (`feuille,type,echelle,note,bordereau`). `type` ∈ `plan` (plan d'étage/toiture
   avec appareils à compter), `legende`, `schema` (unifilaire, distribution), `tableau` (cédules de panneaux), `detail`, `autre`.
   `echelle` = dénominateur métrique lu dans le cartouche (ex. `100` pour 1:100), vide si non lu. Ouvre chaque aperçu.
   `bordereau` (optionnel — voir `apprentissage/hr26-14-exemplaire/STANDARD-RELEVE.md` §4) choisit le format du bordereau
   produit ; vide = déduit automatiquement (`materiel` si `type=schema` ou discipline incendie, `travaux` si toute la
   feuille est en secours/urgence, sinon `agrege`). **Laisse `bordereau` vide** : cette déduction est celle de
   l'exemplaire approuvé (spec unique `docs/FORMAT-EXEMPLE.md` §1 — plans d'étage et de logements en agrégé, y compris
   quand ils mélangent `INSTALLER`, `REMPLACER` et `CONSERVER` ; unifilaires, cédules et incendie en matériel). Une
   portée mixte ne justifie pas `materiel` : la portée de chaque famille reste dans `nomenclature.csv` et au rapport.
   Ne renseigne `bordereau` que si la feuille est d'un type que la déduction classe mal, et dis pourquoi dans `note`.
   (Révisé le 2026-10-05 : l'ancienne consigne « portée mixte → materiel » contredisait l'exemplaire et remplaçait les
   codes de famille de la légende par des numéros M01, M02… dans l'encadré et le bordereau.)
   Le nom de feuille donné par `prepare.py` est provisoire (lu par regex, parfois pris dans une bulle de détail ou absent :
   `<fichier>-pNN`) : lis le VRAI numéro et le titre dans le cartouche de l'aperçu et écris-les dans la colonne `note`
   (`cartouche=E401 · REZ-DE-CHAUSSÉE ÉCLAIRAGE`). AUCUNE page ne doit rester non classée. Distingue aussi le neuf de l'existant
   (trait gris/fin, mention « EXISTANT », « EX. », « À DÉMOLIR ») : ne relève que le neuf, ou un label « existant » séparé.
1b. **Légende d'abord → `legende.csv`** (correctif du 2026-10-05 : sans légende lue, un agent invente ses codes, fond
   des appareils voisins dans une même famille et oublie des symboles). Avant d'écrire une seule famille :
   - Trouve la légende qui s'applique à chaque feuille `plan` : d'abord l'encadré « LÉGENDE » de la feuille elle-même,
     sinon la **légende générale du lot** (feuille au `role=legende` de `feuilles.csv`, souvent la page titre `00`
     « PAGE TITRE, LÉGENDES ET LISTE DES DESSINS »). Les descriptions y sont souvent vectorisées (pas dans
     `texte/*-mots.csv`) : lis-les au zoom (`zoom.py`, colonne par colonne, assez gros pour lire chaque mot).
   - Transcris **chaque ligne** des sections de légende utiles au plan (ÉLECTRICITÉ, et DÉTECTION ET SIGNALISATION
     INCENDIE pour les avertisseurs posés sur un plan d'électricité) dans `legende.csv` :
     `feuille,section,no,symbole,description,code,statut,qte,preuve`
     - `no` : numéro de ligne stable (`L01`, `L02`…) ; `symbole` : le dessin en quelques mots (« cercle + 2 traits »,
       « carré plein ») ; `description` : le texte de la légende recopié **tel quel** ; `code` : le code du
       vocabulaire ci-dessous ;
     - `statut` ∈ `compte` (au moins une occurrence relevée), `absent` (cherché sur tout le plan, pas trouvé),
       `hors_portee` (ex. phare d'urgence sur une feuille de logements) ; `qte` = quantité relevée (0 si absent) ;
       `preuve` = où tu as cherché ou relevé (feuille, zone, zoom).
   - **Aucun symbole de légende présent sur le plan n'est oublié** : parcours la légende ligne par ligne et cherche
     chaque symbole sur toutes les tuiles. Les identifications de luminaires (« Aa » : lettre de type + contrôle) se
     relèvent par type : **cherche sur le plan chaque lettre de type** listée au devis ou à la cédule des luminaires,
     y compris les appareils linéaires ou encastrés dessinés autrement qu'en cercle (rectangle étroit + lettre) ; un
     type du devis introuvable au plan va en réserve avec les zones vérifiées.
   - Un symbole vu au plan mais absent de la légende reçoit sa famille avec `legende=HORS LEGENDE` dans
     `nomenclature.csv`, `materiel` suffixé `(hors legende - R-0xx)` et une réserve.
   **Vocabulaire des codes** (vient de la description de légende, jamais inventé ; contrôle `Q14` via
   `releve/legende.py::code_attendu`) :
   | Description de légende (motif) | Code |
   |---|---|
   | prise de courant au-dessus d'un comptoir, avec mention DDFT/GFI au plan | `CG` |
   | prise de courant au-dessus d'un comptoir | `CT` |
   | prise de courant avec disjoncteur différentiel de fuite à la terre (DDFT/GFI) | `GF` |
   | prise de courant pour cuisinière | `CP` |
   | prise de courant simple 30 A (sécheuse) | `SE` |
   | prise de courant double 15 A | `PC` |
   | raccord direct d'un appareil (hotte…) | `RA` |
   | boîte de jonction | `BJ` |
   | évacuateur (de toilette) | `EV` |
   | commutateur unipolaire | `CU` |
   | sortie téléphonique | `TE` |
   | sortie câblodistribution (TV) | `TV` |
   | intercom (contrôle de porte) | `IC` |
   | avertisseur de fumée (mural 120 V) | `AF` |
   | luminaire / appareil d'éclairage TYPE X | `LX` (`LA`, `LB`, `LC`…) |
   | thermostat | `TH` |
   | plinthe de chauffage | `PL` |
   | panneau de logement | `PN` |
   Hors de ce tableau : un code court de 2 lettres tiré de la description, justifié dans `source`.
2. **Lire la légende / nomenclature du projet** (feuilles `legende`, tableaux de luminaires) et écrire `nomenclature.csv` :
   `label,famille,forme,rgb,jeton_regex,description,source,code,materiel,portee,modele,prescription,discipline,legende`.
   - **Une famille = une ligne de `legende.csv`** (colonne `legende` = son `no`, ou `HORS LEGENDE`). Jamais deux familles
     pour un même symbole qui ne diffèrent que par la puissance, le circuit ou la pièce : la variante va dans la colonne
     `designation` de chaque occurrence (ex. `750 W C4,6`, `1/2 SUR INTERRUPTEUR C9`). Seules exceptions (contrôle
     `Q12`) : le même symbole de comptoir avec ou sans mention DDFT/GFI au plan (`CT` / `CG` : appareils différents au
     devis) et une lettre de type de luminaire différente (`LA`, `LF`… : appareils différents).
   - **Prises (R4)** : c'est le SYMBOLE et la légende qui tranchent. Symbole de comptoir sans mention → `CT` ; symbole de
     comptoir + « gfi »/« DDFT » au-dessus d'un comptoir de CUISINE → `CG` ; symbole DDFT de la légende → `GF` ; prise
     double ordinaire → `PC` (une moitié commandée = `designation`, pas une famille). Seule exception de pièce : une prise
     marquée gfi/DDFT dans une **salle de bain** (près d'un lavabo ou d'une baignoire) est une prise DDFT `GF`, même
     dessinée avec le symbole de comptoir — le « comptoir » d'une légende électrique est le comptoir de cuisine (exigence
     propre aux prises de comptoir de cuisine), la prise de salle de bain relève de l'exigence DDFT ; note la règle dans
     `note`. Les prises
     cachées sous une hachure d'armoire se lisent avec `traits.py` (et le contrôle `Q15` les signale).
   - `famille` ∈ luminaire, commande, secours, prise, alarme, telecom, distribution, mecanique, chauffage, autre.
   - `forme` : cercle | carre | losange | triangle | triangle_inverse | trapeze | trapeze_inverse (vide = défaut de la famille).
     Convention Dupuis/Plan Expert : luminaires DS0 cercle, DS1 carré, commandes cercle, alarme cercle, télécom triangle,
     prises cercle, poste manuel carré, distribution carré. `rgb` vide = palette automatique par famille.
   - `jeton_regex` : expression régulière (fullmatch, sensible à la casse) qui reconnaît l'étiquette texte de l'appareil sur
     le plan (ex. `DS0`, `Do`, `Di`, `K`, `B`, `PH1`). Vide pour les appareils sans étiquette (prises, enseignes…), qui se relèvent visuellement.
   - `source` : feuille et zone où la définition a été lue (ex. `E103 légende, colonne 2`).
   - **Colonnes du rendu final** (lues par `releve/render_vectoriel.py` pour produire le bordereau de chaque feuille
     dans son format — matériel, agrégé ou travaux, voir `docs/FORMAT-EXEMPLE.md` §4 et
     `apprentissage/hr26-14-exemplaire/STANDARD-RELEVE.md` §4, §5, §6 ; toutes optionnelles
     mais **à remplir chaque fois que l'information est lisible sur le plan/la légende/la cédule** — un bordereau qui reste
     aux valeurs par défaut sur tout un dossier est un signe que ces colonnes n'ont pas été lues, pas qu'elles étaient absentes) :
     - `code` : le code de la ligne de `legende.csv` (vocabulaire du §1b) — jamais un code inventé (`Q14` refuse un code
       qui contredit le vocabulaire pour la description donnée).
     - `materiel` : la **description de la ligne de légende recopiée telle quelle** (majuscules sans accents), complétée
       seulement de la variante qui fait la famille, après un tiret (ex. légende « APPAREIL D'ÉCLAIRAGE ENCASTRÉ » +
       lettre D2 au plan → `APPAREIL D'ECLAIRAGE ENCASTRE TYPE D2` ; légende « PRISE DOUBLE 20A » + mention GFI →
       `PRISE DOUBLE 20A - DDFT`) ; hors légende : la désignation du plan/devis + `(hors legende - R-0xx)`. Jamais une
       reformulation de la légende avec tes propres mots.
     - `portee` : vocabulaire `STANDARD-RELEVE.md` §5 — `INSTALLER`, `ENLEVER`, `REMPLACER`, `CONVERTIR`, `CONSERVER`,
       `TEMPORAIRE`, `A PRECISER` (réserve de portée), ou un `RENVOI_*` si l'appareil est compté ailleurs (ne pas laisser
       vide quand la portée est lisible : note de plan, légende « existant à remplacer », etc.).
     - `modele` : **quand un devis est fourni (`devis/*-articles.csv`), cherche l'article de chaque famille** (section
       « PRISES ÉLECTRIQUES », « INTERRUPTEUR », « PLINTHE », « THERMOSTATS », « APPAREILS D'ÉCLAIRAGE » + `TYPE X`…) et
       recopie la colonne `modele` de l'article littéralement (ex. fictif : `HUBBELL HBL5262`) — choisis l'article par sa
       description (ampérage, GFCI ou non, conducteur cuivre / aluminium, type de luminaire) ; quand le devis admet deux
       variantes selon une condition, écris les deux modèles séparés par `;` avec leur condition. Article sans « MARQUE
       SPÉCIFIÉE » : la désignation technique courte de l'article (type d'appareil, dimension, puissance, tension).
       Existant conservé : `EXISTANT CONSERVE - MODELE NON INDIQUE`.
       Devis lu sans article pour cet appareil : `MODELE NON INDIQUE DANS LA SOURCE ELECTRIQUE`. Ne jamais écrire
       `MODELE NON PRECISE` (valeur par défaut du rendu = devis pas lu ; `Q13` bloque une colonne vide quand un devis existe).
     - `prescription` : extrait littéral court de l'article du devis (caractéristiques qui distinguent l'appareil :
       ampérage, NEMA, GFCI, inviolable, couleur ; ≤ 160 caractères, préfixé `Devis:`), sinon le texte de légende/note
       recopié tel quel ; vide plutôt qu'inventé.
     - `source` : où la famille et son modèle ont été lus — ligne de légende ET article du devis, ex. fictif :
       `E00 legende L03 ; E20 section 5 PRISES (devis/E20-articles.csv art. 5.2)`.
     - `discipline` : `incendie` | `electricite` | `urgence` — détermine le préfixe I/M du repère sur les feuilles au
       format `materiel` ; vide = déduit de `famille` (alarme/securite_incendie → incendie, secours → urgence, sinon
       electricite). **`incendie` = appareils du réseau d'alarme incendie** (détecteurs, modules, klaxons, postes
       manuels reliés au panneau, feuilles DSI). Un avertisseur de fumée **autonome 120 V** branché sur un circuit de
       logement et dessiné sur un plan d'électricité est `electricite` — écris-le explicitement, car une colonne vide
       avec la famille `alarme` serait déduite `incendie` :
       une seule ligne `incendie` suffit à faire passer toute la feuille au format `materiel` (déduction automatique),
       ce qui remplace les codes de légende par des numéros I01/M01 dans l'encadré et le bordereau.
   Ces mêmes champs (`designation,portee,modele,prescription,parent,qte,reserve`) peuvent aussi être ajoutés par
   occurrence dans `occurrences-texte.csv`/`occurrences-visuel.csv` (§4) quand la valeur varie d'un repère à l'autre
   dans une même famille (ex. deux plinthes de puissance différente, R1 de `STANDARD-RELEVE.md` §9) — la colonne de
   l'occurrence prime alors sur celle de `nomenclature.csv`. **`designation` porte la 2e ligne de l'étiquette** : puissance
   et circuit lus au plan (`750 W C4,6`), circuit seul (`C5`), variante (`1/2 SUR INTERRUPTEUR C9`).
3. **Occurrences par étiquettes** : `uv run releve/extract_occurrences.py <workdir>`. Puis contrôle des faux positifs
   feuille par feuille avec les tuiles/zooms : bulles d'axes (`B`, `K`… dans un cercle de grille), numéros de circuits,
   texte de notes. Édite `occurrences-texte.csv` (supprime les lignes fausses, ou ajoute une colonne `exclure=1`).
   Erreurs systématiques constatées lors de l'audit S-1857 (2026-09-22), à éliminer explicitement :
   - une lettre-étiquette (`B`, `K`, `M`, `T`, `F`…) qui fait partie d'un autre texte (« ESC. B », « CORR. B », nom de local,
     bulle d'axe, numéro de porte) n'est PAS un appareil : vérifie les mots voisins dans `texte/<F>-mots.csv` (même ligne, ±30 pt) ;
   - un qualificatif écrit SOUS ou À CÔTÉ d'un appareil déjà relevé (« MO » micro-onde, « DDFT », « GFI », « WP », « LV », « SM »,
     « 1070 », « HT », « USB », « 30A »…) qualifie CETTE prise/appareil : une seule marque, avec le bon label (ex. « Prise micro-onde »),
     jamais une marque de plus ;
   - un appareil dessiné sur deux feuilles (raccord extérieur, sectionneur en limite de zone, équipement de toiture repris en
     plan et en détail) se compte UNE fois, sur la feuille de son niveau ; note la feuille écartée dans `reserves.md` ;
   - un symbole visible mais absent de la légende (« TS », « CME », équipement mécanique, borne de recharge…) se relève quand même
     sous un label « à confirmer » ET s'inscrit dans `reserves.md` — un objet vu et non relevé sans réserve est une faute.
3b. **Un libellé que tu as écrit et que tu ne relèves jamais est presque toujours une confusion, pas une absence.**
   Avant de terminer, compare `nomenclature.csv` aux libellés réellement employés dans les `occurrences-*.csv`. Pour chaque
   libellé jamais employé : soit l'appareil est réellement absent du projet — alors écris-le dans `reserves.md` avec la
   feuille et la zone vérifiées — soit tu l'as compté sous le libellé d'un appareil voisin, et le relevé est faux.
   Le contrôle `Q8` bloque ce cas ; ne le contourne pas en effaçant la ligne de la nomenclature.
   Constaté sur DSI01 (kimi-k3, 2026-09-29) : `AVERTISSEUR FUMEE AUTONOME` lu dans la légende, écrit dans la nomenclature,
   jamais relevé — ses 36 appareils comptés en `DETECTEUR FUMEE` (13 attendus, 40 relevés). Une seule confusion coûtait
   36 marques sur 122, soit le tiers de la feuille.
   Les paires qui se confondent le plus (même forme, même famille, étiquette voisine ou absente) :
   - **avertisseur de fumée autonome 120V** (alimenté, souvent mural, dans les logements) ≠ **détecteur de fumée** du réseau
     d'alarme (relié au panneau, souvent au plafond des corridors et locaux communs) ;
   - **détecteur thermique 135°F** ≠ **200°F** : si la température n'est pas lisible, relève un seul libellé générique
     ET mets la distinction en réserve — n'invente pas la répartition ;
   - **klaxon** (avertisseur sonore d'alarme) ≠ **avertisseur piezo** ≠ **strobe** ;
   - **module adressable** simple ≠ double ≠ **relais adressable**.
   Quand deux appareils partagent la forme et la famille, c'est la position qui tranche (logement privé vs aire commune,
   mur vs plafond) : dis dans `note` ce qui a tranché.
4. **Occurrences visuelles** → `occurrences-visuel.csv` (`feuille,label,x_pt,y_pt,source,note` + au besoin
   `designation,portee,modele,prescription,parent,qte,reserve` par repère, voir §2, quand une valeur diffère de
   celle de `nomenclature.csv` pour ce repère précis), `source=visuel` : parcours
   **toutes** les tuiles de chaque feuille `plan` et relève les symboles sans étiquette (prises duplex, DDFT, enseignes de sortie,
   phares, postes manuels, klaxons non étiquetés, sectionneurs, raccordements d'équipements…). Coordonnées lues sur les règles,
   **au centre du symbole, sans arrondir** : interpole entre deux graduations au lieu de prendre la graduation la plus proche.
   Une pastille ne fait que 4 à 6 pt de rayon (rayons par format : `docs/FORMAT-EXEMPLE.md` §2.2) — arrondir à 5 pt la
   déplace d'autant que sa propre taille et la fait rater le symbole.
   Repère mesuré : sur les 319 marques relevées à la main dans le dépôt, 3,1 % seulement tombent sur un multiple de 5 pt dans
   les deux axes. Si presque toutes tes coordonnées sont rondes, tu ne lis pas le plan — tu poses une grille mentale, et le
   contrôle Q10 le bloque (gemma-4-31b : 53/53 sur 10 pt ; kimi-k3 : 104/104 sur 5 pt, familles correctes mais positions fausses).
   Utilise `zoom.py` pour les zones denses. Chaque label utilisé doit exister dans `nomenclature.csv`.
5. **Addendas** : si un fichier `addenda` existe, lis-le (aperçus/texte) et applique ce qui touche l'électricité : feuilles
   remplacées (la version d'addenda prime), ajouts/retraits d'appareils. Note chaque application dans `reserves.md`.
   Si une feuille d'addenda remplace une feuille de base, relève l'addenda et retire la feuille de base du classement (`type=remplacee`) ;
   n'écris jamais « aucun appareil ajouté ni retiré » sans avoir comparé les deux versions tuile par tuile. Si l'addenda est
   incomplet (une seule feuille reçue alors qu'il en annonce plusieurs), dis-le en réserve : les feuilles non reçues ne sont pas relevées.
5b. **Ce qui n'a pas de symbole au plan mais que l'estimateur chiffre** (audits S-1715, S-1811, S-1844, S-1769 du 2026-09-22) :
   - lis les **cédules de panneaux** et l'**unifilaire** (feuilles `tableau`/`schema`) : chaque départ vers un équipement
     (réfrigération, chauffe-eau, aérotherme, plancher chauffant, moteur, ascenseur, borne VE, sectionneur, compteur HQ)
     devient une ligne « Raccordement <équipement> » posée sur la feuille du schéma (coordonnée de la ligne de cédule), avec la
     famille `mecanique`/`distribution` ; recoupe ensuite avec les symboles du plan (un raccordement déjà relevé en plan ne se
     compte pas deux fois — note l'appariement) ;
   - les **notes du plan** qui disent « fournir et installer… », « deux zones », « boîtier de protection », « prise pour… »
     deviennent des articles comptés (avec la note comme `source`), pas seulement une réserve ;
   - les **schémas de contrôle** (nLight, WaveLinx, DALI, alarme adressable) : relais, modules, capteurs, postes — compte-les sur
     le schéma s'ils n'ont pas de symbole en plan ;
   - un symbole **hors légende** reçoit son propre libellé « <forme/texte> — à classer » (jamais fondu dans le libellé le plus proche) ;
   - un libellé par **composante chiffrée séparément** (sonde, thermostat maître/esclave, batterie sans/avec enseigne, variante
     de symbole = ligne de légende distincte) : une ligne de légende du plan = un compteur ;
   - **démolition** (« E.D. », « À ENLEVER », feuilles `…D`) : compte par type d'appareil, dans une famille `demolition`, en
     excluant ce qui est « par le bailleur / par autres / par HQ » (libellé séparé « fourni par autres », non chiffré par DR) ;
   - éléments **linéaires** (profilés d'éclairage T, chemins de câbles, rails) : quantité = nombre de segments ET longueur estimée
     dans `note` si l'échelle est connue ; sinon réserve explicite « à métrer ».
5c. **Neuf vs existant** : en cas de doute, `uv run releve/traits.py <workdir> <F> x y` donne la nature vectorielle de la zone
   (texte/tracé, épaisseur, gris/noir, pointillé). Existant = gris, fin, pointillé, hachuré, mention « EX. » ; ne le relève que
   sous un libellé « existant » séparé, jamais dans le neuf.
5d. **Conventions de l'estimateur** (comparaison marque par marque avec les projets Plan Expert de M. Dupuis, 2026-09-22 ;
   jeu de référence `dossiers/_jeu-reference/`) :
   - **la marque va sur le symbole, pas sur l'étiquette** : quand l'étiquette texte est écrite à côté du symbole (> 8 pt du centre),
     déplace la coordonnée au centre du symbole (vérifie au zoom). S-1844 : 20 % des marques IA tombaient sur le texte du repère ;
   - **un compteur par numéro de modèle** quand la légende ou le schéma donne des modèles (WST-C-1, WST-C-3, WST-C-3D, WST-C-5D…) :
     le libellé porte le modèle ; jamais un compteur générique « interrupteur BT » qui les regroupe (S-1715) ;
   - **plan d'abord, schéma en contrôle** : un appareil visible au plan se marque au plan ; le schéma de contrôle ne sert qu'à
     typer (modèle) et à trouver ce qui n'a pas de symbole. Jamais les deux (S-1715 : capteurs OSC comptés au schéma par l'estimateur,
     au plan par l'IA — même quantité) ;
   - **pièces éclairées sans commande dessinée** : si une pièce a des luminaires mais aucun interrupteur/détecteur au plan, ajoute
     une marque « Interrupteur — par pièce (à confirmer) » à la porte de la pièce et une réserve. L'estimateur les compte (S-1714 :
     227 interrupteurs marqués aux portes des logements sans aucun symbole au plan) ;
   - **supports et accessoires comptés par règle** (J-hook télécom, boîtes de tirage, plafonds suspendus) : ne les invente pas,
     mais crée le compteur avec une réserve « quantité par règle à fixer » dès qu'une note ou la légende les mentionne (S-1715 :
     45 J-hook chez l'estimateur, 1 chez l'IA).
5e. **Règles apprises de M. Dupuis** (S-1769 E401, S-1844 E200 ; rédigées par le superviseur, appliquées telles quelles) :
   - **R1** (révisée le 2026-10-05) Une famille = une ligne de légende (§1b, §2) ; la caractéristique de CHAQUE appareil (puissance, calibre, circuit — lire le kW dans l'hexagone/étiquette) va dans la colonne `designation` de son occurrence, jamais dans une famille de plus. La distinction de M. Dupuis reste visible repère par repère (S-1769 : 7 × 1500 W + 2 × 900 W = 9 occurrences d'une seule famille PL, avec 1500 W ou 900 W en `designation`), et le bordereau garde une ligne par symbole de légende (`Q12`).
   - **R2** Ne jamais fusionner un appareil de contrôle/protection avec l'appareil qu'il sert : sectionneur 30A/SF, WP, etc. = sa propre famille (Dupuis : « 30A NF WP »).
   - **R3** Thermostats : séparer thermostat de plinthe et thermostat de plancher chauffant (sonde/note plancher chauffant à côté = famille « thermostat plancher chauffant »).
   - **R4** Prises : une famille par symbole de légende (régulière 15 A, 15/20 A, 20 A, comptoir, DDFT, cuisinière, sécheuse…) ; le même symbole de comptoir avec mention « GFI »/« DDFT » est une famille à part (`CG`, voir §2). Une prise GFI n'est jamais comptée comme prise ordinaire, et une prise de comptoir n'est jamais comptée comme prise DDFT ordinaire.
   - **R5** Un symbole dont l'identification dépend de la légende (lettre dans un cercle, cercle mi-noir) : vérifier la légende AVANT de nommer ; si le même symbole existe comme luminaire ET comme détecteur, trancher par la légende, sinon réserve *. (Erreur S-1769 : « luminaire type F » compté 7 fois, Dupuis a 5 détecteurs de fumée + 1 F + 1 F1.)
   - **R6** Les notes « RELO / relocaliser / déplacer » sont des appareils à compter (famille « RELO <appareil> »), même si l'appareil est existant.
   - **R7** Nommer les familles comme la légende du plan (FIXTURE TYPE A, A1, B…) — colonne `materiel` = texte de la légende ; le code 2 lettres (vocabulaire §1b) reste pour l'étiquette.
   - **R8** Choix de la feuille d'essai : c'est le SUPERVISEUR qui choisit une feuille que la référence a réellement relevée (tu ne regardes pas la référence). S-1844 E200 était invalide : Dupuis n'a aucune marque sur E200 (il a relevé les prises sur le plan d'architecte).
   - **R9** Panneau de logement : un rectangle mural étiqueté `PA`, `PB`… (« P » + type de logement) EST le panneau de distribution du logement, même quand sa cédule est imprimée en tableau ailleurs sur la feuille : 1 repère par rectangle, famille `PN` (vocabulaire `apprentissage/hr26-14-exemplaire/STANDARD-RELEVE.md` §6). Ne pas écrire « panneau non dessiné » sans avoir cherché ces étiquettes (gold HR26-14 E08 p.62 : PN-01 et PN-02 sur `PA` / `PB`).
   - **R10** Réglette sous armoire / le long d'un comptoir : un rectangle étroit (≈ 3-4 pt de large, ≥ 30 pt de long) tracé **plus épais** que le mobilier autour (≈ 1 pt contre 0,5 pt) est un luminaire, avec une lettre de type (`C`, `F`…) posée contre lui. Ne pas conclure « absent » faute de texte : sur les plans AutoCAD, ces lettres et les circuits sont souvent **dessinés en traits** (police SHX) et ne sont PAS dans la couche texte (`texte/*-mots.csv`). Chercher le rectangle avec `traits.py` (épaisseur, dimensions), puis lire la lettre au zoom. Une lettre seule = type de luminaire du devis ; lettre + chiffres (`C2`, `C14`) = circuit (gold HR26-14 E08 p.62 : LC-01 / LC-02, rectangle 3,5 × 43,2 pt trait 0,99 pt au-dessus de l'évier, « C » tracé en traits).
   - **R11** Feuille de vues en plan d'ensemble (les logements y renvoient aux feuilles de types : « VOIR LOGEMENT TYPE A/B/C… ») : les appareils dessinés sont des **existants**, qu'ils soient à REMPLACER ou à CONSERVER (notes générales). Le gold les relève avec le vocabulaire existant de `STANDARD-RELEVE.md` §6 : `CH` « APPAREIL DE CHAUFFAGE ELECTRIQUE EXISTANT » (plinthes ET convecteurs : une seule famille), `I` « COMMUTATEUR UNIPOLAIRE EXISTANT », `PC` « PRISE DE COURANT DOUBLE EXISTANTE », `T` « THERMOSTAT EXISTANT » ; tout autre existant prend un numéro de la série `M` (`M03` « PRISE DDFT EXISTANTE », `M05` « PRISE SPECIALE EXISTANTE » pour cuisinière et sécheuse ensemble). Écris EXISTANT dans `materiel` et la portée dans `portee` : `Q14` admet alors ces codes. Sur une feuille de logements types (E08), garder les codes de la légende (`PL`, `TH`…), même pour un existant (gold HR26-14 : E09 p.64 CH 36, I 14, PC 20, T 28, M03 2, M05 3 ; E08 p.62 PL 14, TH 12).
   - **Porte de prévention** : pour chaque feuille, AVANT de placer les marques et AVANT tout commit, publier (a) capture zoom de la légende, (b) la liste des familles avec le symbole/étiquette qui les distingue et la règle R1-R7 appliquée, (c) 3 zooms des symboles ambigus, puis attendre « VALIDÉ » du superviseur.
6. **Comparaison avec l'estimateur** (si `estimateur/` existe) → `comparaison-estimateur.md` : pour chaque feuille, tableau
   `famille/objet | estimateur | nous | écart | commentaire`, en lisant ses légendes (`estimateur/legendes/*-legende.png`, où
   chaque ligne porte symbole, nom et quantité). Explique les écarts (périmètre différent, oubli probable de l'un ou l'autre).
7. **`reserves.md`** : liste numérotée R-001… (feuille, objet, question), et **`rapport-releve.md`** : méthode suivie, feuilles
   traitées, totaux par feuille, ce qui n'a pas pu être relevé, temps/limites. Termine en vérifiant que chaque `label` des
   deux fichiers d'occurrences existe dans `nomenclature.csv` (`cut -d, -f2 … | sort -u`).
8. **Contrôle final obligatoire** : `uv run releve/controle_qualite.py <workdir>`. Corrige CHAQUE erreur listée
   (`qualite.json`) — en particulier Q8 (famille jamais relevée), Q11 (ligne de légende ni comptée ni prouvée absente),
   Q12 (symbole éclaté en plusieurs familles), Q13 (modèle vide malgré le devis), Q14 (code hors vocabulaire), Q15
   (cercle vectoriel identique à un symbole relevé, sans occurrence : zoome dessus, relève-le avec la bonne famille, ou
   écris dans `reserves.md` la ligne « Q15 (x, y) : <pourquoi ce n'est pas un appareil> ») — puis relance le contrôle
   jusqu'à `conforme=True`. Une erreur que tu juges fausse se justifie dans `reserves.md` (règle,
   preuve au zoom), jamais en effaçant la ligne fautive. Mets à jour `qte` et `statut` de `legende.csv` avec les comptes
   finaux.

## Sorties attendues (toutes dans `$ARGUMENTS/`)
`feuilles-classement.csv`, `legende.csv`, `nomenclature.csv`, `occurrences-texte.csv`, `occurrences-visuel.csv`, `reserves.md`,
`rapport-releve.md`, et `comparaison-estimateur.md` si un export d'estimateur était fourni.
Quand tout est écrit, réponds par un résumé de 10 lignes maximum : feuilles traitées, total de marques, nombre de réserves,
ce qui manque.
