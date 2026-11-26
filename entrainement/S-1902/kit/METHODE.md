# Méthode de chiffrage « Dupuis » (extrait de la référence officielle, sans le résultat)

## 2. La méthode de chiffrage de M. Dupuis (reproduite, chiffres à l'appui)

Reconstituée à partir de 27 de ses sommaires ACCEO/Expert Estimateur 2026 (`prix/dupuis/Catalogue-prix-temps-Dupuis.xlsx`, 4 629 lignes
transcrites, onglets LISEZ-MOI / Catalogue / Paramètres Jo / Backtest / Lignes sources) et de `eewin/docs/CALCUL-SOUMISSION.md`.

1. **Matériel** = Σ quantité × *prix vendant d'assemblage* du catalogue — **dernière valeur** de Dupuis, pas la médiane (règle du LISEZ-MOI :
   « sa valeur la plus récente ; médiane/min/max = contrôle seulement »). Les prix d'assemblage incluent boîte/plaque/raccord
   (prise duplex 15 A 64,81 $, USB 77,45 $, DDFT 65,38 $, tel/data 3/4 22,32 $, interrupteur 75,47 $, percement 150 $, scan dalle 1 250 $,
   conduit 3/4 03c12 4,24 $/pi, conduit vide 3/4 1,41 $/pi, monument 250 $, lecteur de carte 15 $, gâche 15 $, thermostat 35 $, sortie TV 15 $).
   Administration et profit = **0 %** dans son sommaire (la marge est dans le prix vendant).
2. **Luminaires, enseignes, têtes d'urgence, détecteurs, panneaux** : 0 $ en ligne (temps seulement) + un **PRIX DE LOT** fournisseur.
   Lots pour S-1902 (entrées, montants confirmés par Francis le 2026-10-20, sans soumission fournisseur) : lot éclairage = somme de son
   détail (A1 ×11 à 185 $, Axis SL1 4′ ×12 à 290 $, 3′ ×15 à 230 $, 1′ ×6 à 110 $, trousses 1 500 $, E ×3 à 475 $, Z6 ×3 à 161,60 $) =
   **13 034,80 $** (règle en vigueur ; le 11 893 $ est l'allocation notée le 2026-10-20 à midi, voir §8, décision `lot_eclairage`) ;
   lot distribution 6 200 $ (NF 225 A 42 cct 3 400 $ + EDB 1P 95 $ ×20 + EJB 3P 300 $ ×3) ; JCI 7 400 $ + 2 détecteurs 600 $ ; GPR 1 250 $.
3. **Heures** = Σ quantité × *temps unitaire* Dupuis (prise 1,175 h ; USB 1,125 h ; DDFT 1,3 h ; tel/data 0,63–0,89 h ; luminaire 0,75 h ;
   enseigne 1 h ; tête 0,5 h ; détecteur 0,5 h ; panneau 8 h ; disjoncteur 1P 0,2 h / 3P 1 h ; percement 1 h ; luminaire enlevé 0,5 h ;
   prise enlevée 0,35 h ; relocalisation de prise 1,5 h ; conduit 3/4 03c12 0,113 h/pi ; conduit vide 3/4 0,056 h/pi ; moteur 0,75 h ; UTA 1 h ;
   annonciateur relocalisé 8 h ; nacelle 1 250 $ / 16 h). **Toujours la colonne « À UTILISER » (dernier Dupuis), jamais la médiane**. Formule ACCEO pour les conduits : QTE × TEMPUNI + sections de 10 pi × TEMPSEC.
4. **Heures chargées** = heures relevées arrondies **vers le haut** au multiple de 10 (S-1881 : 4 128,6 → 4 150 ; S-1854 : 5 872,6 → 5 880).
5. **Main-d'œuvre** = heures chargées × **taux** : 85 $/h sur ses dossiers d'août–octobre 2026 (S-1797, S-1835, S-1854, S-1881 ; 99 $/h sur
   S-1857 ; 110 $/h Canderel centre-ville ; 78–82 $/h en hiver-printemps). Règle de choix à confirmer avec Jo.
6. **Total sommaire ACCEO** = matériel + main-d'œuvre. Contrôle : part MO 30–69 % (médiane ≈ 45 %), 450–520 h par 100 k$ de prix.
7. **Prix de vente** = total ACCEO × **1,244** — unique couple observé : S-1844, sommaire 191 909,19 $ → prix remis 238 744 $
   (courriel Dupuis 2026-08-26 ; versions Jo 253 600 / 259 000 $ = ×1,32–1,35). Arrondi au millier. Facteur modifiable dans `parametres.json`.
   Un seul couple : le facteur est posé, pas calibré (`entrainement/calibrer_facteur.py` le mesure dès qu'il y a d'autres dossiers remis).

## 8. Décisions de portée (règles écrites, 2026-10-23)

Le banc v1 (10 runs) a montré que l'écart tenait à cinq décisions que la méthode ne disait pas. Les voici écrites comme règles
**en vigueur depuis le 2026-10-23, à confirmer par Jo**. Un run les applique dans `decisions.json` (valeur + justification) ; s'il
s'en écarte, il le justifie. Dans tous les cas il fournit les lignes des deux options, étiquetées, pour que le comparateur mesure le
coût exact de toute déviation.

| Clé | Valeurs permises | Règle en vigueur |
|---|---|---|
| `postes_composites` | `en_plus`, `couverts` | **`en_plus`** : les postes de travail de la feuille Détail (D-01, D-02, D-03…D-06, E-01, E-04, E-05) sont comptés en plus du relevé ; les dispositifs du relevé déjà inclus dans ces postes sont retranchés des lignes du relevé (ex. D-08 : sorties data du relevé moins celles des postes, écrans et kiosque). `couverts` : le relevé fait foi au compte complet, aucune ligne composite. |
| `monuments` | `lumen`, `dupuis` | **`lumen`** : monuments poke-through E-02 au prix fournisseur Lumen (feuille Matériel Lumen), temps Dupuis 1 h ; les boîtes de plancher E-03 restent au prix Dupuis « MONUMENT PLANCHER ». |
| `lot_eclairage` | `detail_13034_80`, `readme_11893` | **`detail_13034_80`** : le lot vaut la somme de son détail (§2). |
| `eae_hors_plan` | `comptes`, `releve`, `sautes` | **`comptes`** : démantèlement et relocalisation E.A.E/E.A.R (A-01…A-06) comptés depuis la feuille Détail (hors plan), temps Dupuis (luminaire enlevé 0,5 h, prise enlevée 0,35 h, relocalisation de prise 1,5 h, luminaire relocalisé 1 h). `releve` : mêmes familles mais aux quantités ENLEVER/RELOCALISER du relevé. `sautes` : rien. |
| `conduits` | `temps_pi`, `acceo_tempsec` | **`temps_pi`** : pas de colonne TEMPSEC au catalogue → temps/pi × longueur en pieds (m × 3,28084) ; équivalences : 1″ 05c12 → « CONDUIT 3/4 07C12 », 1″ #8 → « CONDUIT 1 13C12 », 3/4″ → « CONDUIT 3/4 03C12 », data vide → « CONDUIT VIDE 3/4 ». `acceo_tempsec` : refusé par le moteur tant que le catalogue n'a pas TEMPSEC. |

Les quantités ne se tranchent pas ici : elles viennent du relevé et de la feuille Détail, ligne par ligne, avec leur source.
L'effet mesuré de chaque décision est dans `entrainement/README.md` et `SYNTHESE-auto.md`, hors du kit.

