# Méthode de relevé page par page (format Granby)

Ce document décrit le livrable produit pour le projet Granby (branche
`agent/codex/granby-page-by-page`) de façon reproductible. Ce dossier est le
format de relevé approuvé par Francis : **une feuille de plan = un JPEG annoté
+ un CSV de la feuille**, sans agrégation implicite entre feuilles.

Source de vérité : les 28 fichiers du dossier Granby (en lecture seule) et le
`READ-ME.txt` qui les accompagne.

## Entrées

- Les plans PDF du projet. Pour Granby : 19 pages, dont les pages 1 à 5 sont
  la couverture, le devis et la légende — **non relevées**. Les feuilles
  relevées sont E201 à E901 (pages PDF 6 à 19).
- La feuille E401 déjà approuvée est conservée sans changement dans
  `Granby-approved-reference-20260930` et sert de référence de style.

## Règle d'or

**Une feuille = un JPEG annoté haute résolution + un CSV propre à la feuille.**

Nommage observé :

- `Granby-<FEUILLE>-page<NN>-releve.jpg` quand le numéro de page PDF est utile
  (E201→page06, E202→page07, E301→page08, E302→page09) ;
- `Granby-<FEUILLE>-releve.jpg` sinon (E303, E401, E402, E403, E501, E502,
  E503, E601, E801, E901) ;
- `Granby-<FEUILLE>-<type>.csv` pour le relevé tabulaire de la feuille.

## Sorties

### 1. JPEG annotés (14 fichiers, E201→E901)

- Plan original conservé, **annotations couleur par-dessus le plan** avec
  **légende intégrée** au JPEG.
- Haute résolution (2,5 à 7,4 Mo par JPEG) pour permettre le zoom repère par
  repère.
- Familles non surlignées : **non réputées comptées**.

### 2. CSV par feuille (colonnes réelles observées)

| Fichier | Colonnes | Contenu |
|---|---|---|
| `Granby-E401-equipment.csv` | `Type,Description,Quantité,Source` | Luminaires, avec ligne `TOTAL` et colonne `Source` (`E401 / E104`) |
| `Granby-E402-equipment.csv` | `Type,Description,Niveau 2,Niveau 3,Total` | Quantités ventilées par niveau |
| `Granby-E403-equipment.csv` | `Type,Description,Niveau 4,Toit,Total` | Quantités ventilées par zone |
| `Granby-E501-equipment.csv` | `Type,Repère,Description,X points,Y points` | Appareils localisés (coordonnées en points PDF) |
| `Granby-E502-equipment.csv` | idem E501 | idem |
| `Granby-E503-equipment.csv` | idem E501 | idem |
| `Granby-E303-breakers.csv` | `Panel,Ampere,Poles,Quantity` | Disjoncteurs par panneau (cédule E303) |
| `Granby-E601-symbols.csv` | `Type,Description,Symboles dessinés - pas quantité finale` | Symboles du schéma d'alarme — **pas une commande globale** |
| `Granby-E801-by-room-type.csv` | `Type de chambre - un extrait,PC,MF,PTAC,LC,LA,AP,CH,TH,DF,SF,RCFF,TV,CUI` | Quantités pour **un** dessin de chaque type de chambre, **sans multiplication hôtel** |
| `Granby-E901-details.csv` | `Détail,Sujet,Portée / réserve` | Détails A→M avec portée et réserves explicites |

### 3. Fichiers transverses

- `Granby-breakers-detailed.csv` : `panel,circuits,ampere,poles,quantity,description,protection_source,sheet`
  — détail circuit par circuit, avec `protection_source` (« Non indiquée » si
  absent du plan) et la feuille d'origine.
- `Granby-breakers-by-panel.xlsx` : classeur avec onglets `Purchase list`,
  `All breakers`, un onglet par panneau (A1…D4, PDU, PS-1, PS-2, PPU),
  `Service breakers`, `Before ordering`. L'en-tête consigne les réserves :
  tableau PS-G absent, disjoncteurs principaux non renseignés non ajoutés,
  marque/série/protections/pouvoir de coupure **à confirmer avant commande**.
- `manifest.json` : liste des fichiers avec taille et **sha256** — preuve
  d'intégrité du livrable.
- `READ-ME.txt` : état du travail, portée, réserves et contradictions.

## Règles de rigueur (rien d'inventé)

1. **Pas d'addition entre schémas, plans d'étage et chambres types sans
   contrôle des doublons.** Chaque CSV reste attaché à sa feuille ;
   l'agrégation est une étape séparée et explicite.
2. **Contradictions consignées, jamais tranchées arbitrairement.** Exemples
   relevés dans le READ-ME : ascenseurs 20 kVA (E901) / 30 kVA (E501) ;
   sectionneurs 30 A au dessin / 60 A et fusibles 40 A aux notes (E901) ;
   prise de toiture 20 A au détail E901 / symbole 15 A en E104. Aucun calibre
   choisi arbitrairement.
3. **Portée déclarée par feuille.** E501 : DATA, téléphone, TV non comptés ;
   8 puissances source ancrées aux notes plutôt qu'aux appareils physiques.
   E801 : interrupteurs, DATA et téléphone à compléter. E601 : multiplicateurs
   et réserves du plan conservés.
4. **Câbles et conduits non métrés** dans ce livrable.
5. **L'incertain va en réserve** (colonne `Portée / réserve`, onglet
   `Before ordering`, section du READ-ME), jamais dans une quantité.

## Étapes reproductibles

1. **Inventorier** le PDF : identifier les feuilles à relever (exclure
   couverture, devis, légende) et leur numéro de page.
2. **Rasteriser** chaque feuille en haute résolution.
3. **Relever feuille par feuille** : annoter le plan en couleur avec légende
   intégrée ; compter uniquement ce qui est vu (symbole, étiquette, cédule,
   note) ; une famille non surlignée n'est pas comptée.
4. **Produire le CSV de la feuille** avec les colonnes adaptées au contenu
   (équipement par zone, appareils localisés, cédule de panneaux, symboles de
   schéma, détails).
5. **Consigner** réserves et contradictions dans le CSV (`Portée / réserve`)
   et dans le `READ-ME.txt`.
6. **Agréger séparément** ce qui a du sens transverse (ex. disjoncteurs →
   `Granby-breakers-detailed.csv` + `Granby-breakers-by-panel.xlsx`), avec
   contrôle des doublons.
7. **Sceller** le livrable : `manifest.json` (fichier, taille, sha256) et
   `READ-ME.txt` (état, portée, réserves).

## État du livrable Granby

Relevé supervisé encore partiel — le dossier n'est **pas** une soumission
exhaustive (voir `READ-ME.txt` pour la liste exacte des réserves).
