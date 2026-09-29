# E103 — relevé à l'aveugle (SAQ Varennes, contrôle d'éclairage nLight)

Entrées : `../E103-page6.pdf`, `../SKILL.md` uniquement. Porte de prévention : `../porte/` (VALIDÉE par le superviseur).

## Décompte (23 marques, 1 par étiquette #nn, ancrée au centre du carré vectoriel)
| Famille | Qté | Étiquettes |
|---|---|---|
| DP1 - NPP16 D EFP 347 | 8 | #27 #28 #29 #30 #31 #32 #33 #35 |
| DP2 - NPP PCD EFP | 4 | #16 #21 #22 #23 |
| PP1 - NPP20 PL BP | 2 | #19 #20 |
| SO3 - WSXA MWO PDT D WH | 2 | #17 #24 |
| SO4 - WSXA MWO PDT WH | 4 | #18 #25 #26 #37 |
| SW1 - NPODMA WH | 2 | #34 #36 |
| SW6 - NPOD TOUCH WH | 1 | #13 |
Réserves sans quantité : PS 150, CAT5e (à métrer), RJ45 (par règle), SN (à classer). 12 réserves au total : reserves.md (R-001 à R-012 ; liées aux lignes du bordereau par la colonne prescription).

## Fichiers
- `nomenclature.csv` — 7 familles comptées + 4 compteurs en réserve (colonnes code/materiel/portee/modele ajoutées, valeurs lues par le relevé, rien d'ajouté).
- `occurrences-visuel.csv` — 23 lignes (x_pt, y_pt en points PDF, page 3456 × 2592).
- `S-1844-E103-releve-HQ.pdf` — 2 pages produites par la chaîne (`python -m src.estimer.render.from_releve`, bordereau « materiel »): page 1 plan annoté + encadré + 8 calques; page 2 « BORDEREAU MATERIEL - E103 » (8 colonnes, 23 repères) + « RESERVES ET COMPLEMENTS ».
- `S-1844-E103-releve-HQ.png`, `S-1844-E103-bordereau.png` — rendus de vérification. `bordereau.csv` — sortie de la chaîne.
- `tableau-ia-vs-dupuis.md`, `cmp103.py`, `appariement.txt` — comparaison (commit d20dccc).
- Le premier rendu (75cc5b8) venait d'un script à part (non commité, supprimé de la liste); remplacé par la chaîne. Réserve R-013 (rendu) retirée: obsolète.
