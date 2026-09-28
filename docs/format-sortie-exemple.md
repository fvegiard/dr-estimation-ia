# Format de sortie cible — dossier de relevé annoté

> Source : `EXEMPLE.pdf` reçu de Francis le 2026-09-25 (87 pages, 29 Mo, PDF 1.7,
> créé 2026-09-16 avec PDF-XChange Editor, non chiffré).
> Statut : **spécification du livrable final du pipeline** — ce que doivent produire
> les `.qpl` + la base SQL (Drive) à la fin de la chaîne.

## 1. Structure du document (faits extraits du PDF)

- 87 pages = **26 pages de plans annotés** + **61 pages de bordereau matériel**.
- 3 disciplines, 26 plans :
  - `DSI01`–`DSI08` — détection/signalisation incendie (8 plans) ;
  - `E01`–`E14` — électricité (14 plans) ;
  - `EU01`–`EU04` — éclairage d'urgence (4 plans).
- Pour **chaque plan** : 1 page plan annoté, suivie de N pages `BORDEREAU MATERIEL - <PLAN>`.

### Page plan annoté (ex. page 1, DS01)

- Le **plan d'origine vectoriel** est conservé tel quel, avec **tous ses calques CAD**
  (ex. `EN-ALARME INCENDIE`, `A-N-GEN-TXT`, `CARTOUCHE`, `PLOMBERIE-EXISTANTE`, …).
- Le pipeline **ajoute des calques OCG** dédiés au relevé (1 670 calques au total dans
  l'exemple, dont par plan) :
  - `RELEVE <CODE> - <DESCRIPTION>` — un calque par famille d'équipement
    (ex. `RELEVE I01 - AVERTISSEUR DE FUMEE AUTONOME 120V MURAL`) ;
  - `RELEVE - Legende et avertissements` — calque de l'encadré sommaire ;
  - `réperage AI` — calque des étiquettes de repère.
- Marques matérielles + **étiquettes de repère numérotées** positionnées sur le plan
  (ex. `I01-01`, `I01-02`, …), une par occurrence.
- Encadré intégré au plan :

  ```
  RELEVE DS01 - MATERIEL     122 reperes      8 familles     RES 122
  (plan reprise le 2026-07-28 - comparaison 2026-09-04 - zones NON CONFORMES marquees O)
  Calques activables; modeles, prescriptions et reserves completes page 2
  ```
  suivi du tableau des familles (code, pastille couleur, description, quantité).

### Pages bordereau (ex. pages 2–7, DS01)

- Titre : `BORDEREAU MATERIEL - <PLAN>` (paysage, tableau sur toute la largeur).
- Sous-titre : *« Quantités representees avec multiplicateurs; portees et composants de
  chaque ensemble conserves. Les retraits et composants de peaufinage ne constituent pas
  des quantités supplémentaires; à déduire. »*
- Colonnes exactes :

  | Repere / source | Materiel | Designation | Qte | Portee | Modele | Prescription / reserve | Parent |
  |---|---|---|---|---|---|---|---|

  - `Repere / source` : ex. `I01-01` + ref. source (`DS01-046`) ;
  - `Materiel` : description FR en majuscules (ex. `AVERTISSEUR DE FUMEE AUTONOME 120V MURAL`) ;
  - `Designation` : lettre de classe (observé : `A`, `K`) ;
  - `Qte` : entier ;
  - `Portee` : valeurs observées — `INSTALLER` (505×), `EXISTANT` (342×),
    `RENVOI_LOGEMENTS` (109×), `REMPLACER` (40×), `CONSERVER` (8×) ;
  - `Modele` : ex. `MODELE NON PRECISE`, `EMERGY LITE EA_WU` ;
  - `Prescription / reserve` : texte libre par repère ;
  - `Parent` : lien vers repère parent (ex. `DS01-044`).
- Fin de chaque discipline : bloc `Notes de reserve source`.

## 2. D'où viennent les données (`.qpl` + base SQL)

| Élément du livrable | Source | État |
|---|---|---|
| Plan d'origine + calques CAD | PDF plans (Drive) | CONFIRMÉ (pipeline actuel) |
| Marques + positions + repères numérotés | `occurrences` (extract_occurrences) + `nomenclature` | CONFIRMÉ |
| Codes familles + descriptions | `nomenclature` (label → famille → description) | CONFIRMÉ |
| Encadré `RELEVE <PLAN> - MATERIEL` | agrégat occurrences par plan/famille + compte `RES` | CONFIRMÉ |
| Calques OCG par famille | renderer vectoriel (pikepdf/pymupdf) | À FAIRE |
| `Portee`, `Parent`, `Prescription / reserve` | `.qpl` Plan Expert + schéma SQL (V0→V45) | **À VALIDER** — champs exacts du schéma non encore croisés avec un `.qpl` réel (BLOQUÉ : `.bak` SQL + `.qpl` Dupuis restants) |
| `Modele`, `Designation`, `Qte` (multiplicateurs) | base Plan Expert (catalogue/modèles) via `.qpl` | **À VALIDER** — même blocage |

## 3. Écart vs `src/pipeline/render_pdf.py` actuel

| Aspect | Actuel | Cible EXEMPLE.pdf |
|---|---|---|
| Support du plan | raster JPEG ré-échantillonné (fond gris) | **vectoriel d'origine conservé** |
| Calques | aucun (aplat) | **OCG par famille + légende + réperage** |
| Étiquettes | aucune | **repère numéroté par occurrence** |
| Encadré sommaire | légende à droite, style export Plan Expert | **strip `RELEVE <PLAN> - MATERIEL` intégré** |
| Bordereau | `Rapport-de-metre.pdf` global par label | **bordereau par plan, 8 colonnes** |
| Colonnes métier | label + compte | **Repère/Portee/Modele/Prescription/Parent** |
| Multi-disciplines | mono | **26 plans, 3 disciplines, dossier unique** |

## 4. Plan d'adaptation (ordre recommandé)

1. **Bordereau par plan** (nouveau module `render_bordereau.py`) : table 8 colonnes à
   partir d'`occurrences`+`nomenclature` ; `Portee/Modele/Prescription/Parent` en
   `[PLACEHOLDER]` tant que les `.qpl` Dupuis/`.bak` ne sont pas là.
2. **Repères numérotés + encadré RELEVE** sur la page plan (extension de `render_pdf.py`).
3. **Passage au vectoriel avec calques OCG** (pikepdf/pymupdf) : marques + étiquettes
   + légende chacune sur son calque `RELEVE <famille>`.
4. **Remplissage métier** (Portee/Modele/Prescription/Parent) depuis `.qpl` + base SQL —
   **BLOQUÉ** sur `.qpl` Dupuis 6 derniers mois + S-1857 + `.bak` SQL 1 an.

## 5. Ce qui reste BLOQUÉ (à obtenir, pas à inventer)

- `.qpl` Dupuis — 6 derniers mois (5 reçus : S-1714, 1715, 1769, 1811, 1844) ;
- sauvegarde `.bak` SQL Server 1 an d'estimation Plan Expert ;
- S-1857 de Dupuis (v3 reçue 2026-09-22, mais la version Dupuis fait foi pour la comparaison).

Sans ces données, les étapes 1–3 produisent le gabarit complet avec placeholders ;
l'étape 4 (le cœur métier du bordereau) ne peut pas être validée marque par marque.
