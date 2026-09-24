# S-1835 — Écart relevé IA / relevé humain (Daniel, v2)

Vérificateur indépendant, 2026-09-23. Référence : scans `reference/releve daniel 2e version-*.png` (transcrits dans
`reference-quantites.csv`). Pas de .qpl humain, donc la comparaison se fait sur les totaux par famille, pas marque par marque.
Relevé IA : `runs/S-1835/OUTBOX/S-1835/travail/occurrences-visuel.csv` (3244 marques, addenda T-01 intégré).

## v1 → v2
Les quantités sont identiques. Seuls les temps unitaires changent : plastic/ballast/entreposage passent de 0,100 h à 0 h (1809,1 h → 1039 h,
154 700 $ → 88 315 $). En v2, la page 2 est une variante manuscrite (700 h, « TEMPORAIRE », démolition au pi² 193 315 × 0,50 = 96 657,50 $).

## Résumé chiffré
Indicateur `min(H, IA) / H` : **accord des totaux par famille** (pas un rappel marque à marque).
| Famille | Humain | IA | Accord des totaux (min/H) | Précision apparente |
|---|---|---|---|---|
| Luminaires à enlever (1x4+2x4+2x2+encastré+mural) | 2567 | 2560 (1888+554+6+85+27 à classer) | 99,7 % | 10/10 au tirage |
| 1x4 | 1927 | 1888 | 98,0 % | — |
| 2x4 | 579 | 554 | 95,7 % | — |
| 2x2 | 6 | 6 | 100 % | — |
| Encastré (rond) | 41 | 85 | 100 % | 48 % si l'humain a raison (voir #3) |
| Mural | 14 | 0 | 0 % | — |
| Interrupteurs | 176 | 0 | **0 %** | — |
| Prises | 7 | 17 (13 projecteur + 4 existantes) | 100 % | 41 % |
| Haut-parleurs (dépose + réinstallation) | 153 | 142 (+3 « classe — par autres ») | 92,8 % | — |
| Plastique/ballast/entreposage | 2567 ×3 | 0 | n/a | compté par règle = somme des luminaires |

Luminaires : total presque égal (−7). Le vrai trou est **les interrupteurs (−176)**.
Tirage de 10 marques IA au hasard (`shuf`, graine « 1835 ») : **10/10 sur un vrai objet**.

## Tableau des écarts classés (10 plus gros)
| # | Objet | Humain | IA | Écart | Cause | Preuve (feuille, x, y en pt) |
|---|---|---|---|---|---|---|
| 1 | Luminaire 24 h dépose/repose temporaire | 0 | 218 | +218 | Convention différente : l'humain n'a pas de ligne unitaire. Le temporaire est traité en forfait (« TEMPORAIRE = », v2 p2), et le devis 1.19.4, surligné, met l'éclairage temporaire aux frais de l'entrepreneur général | D210_ADD 760,588 et 843,470 : tête hachurée d'une rangée pointillée, bulle ① (zoom `preuves/D210_ADD_720_440_990_620.png`) |
| 2 | Détecteur de fumée dépose/repose | 0 | 192 | +192 | Hors périmètre / convention : note 3, suspendre temporairement ; alarme non chiffrée par l'humain (bordereau : « détection incendie » est une ligne distincte) | nomenclature, calque E-E-600-ALA-EQP |
| 3 | Interrupteurs | 176 | 0 | −176 | **Oubli IA** : aucun label d'interrupteur dans la nomenclature, alors que le symbole « $ » est dans la légende E001 (ligne 115) | D220_ADD ≈1860,1430 : 4 « $ » en pointillé non marqués (zoom `preuves/D220_ADD_1780_1420_1920_1540.png`) |
| 4 | Plastique/ballast/entreposage | 2567×3 | 0 | −7701 | Compté par règle (= somme des luminaires 1927+579+41+14+6) | reference-quantites.csv |
| 5 | Encastré rond | 41 | 85 | +44 | Probable oubli humain : les ronds IA vérifiés sont de vrais luminaires ronds pointillés | D210_ADD 1214,1294 (sans marques) ; D212_ADD 1551,1221 |
| 6 | Luminaire 1x4 | 1927 | 1888 | −39 | Convention : l'IA compte des segments de 35 pt (R-004), l'humain compte des luminaires ; une partie des 24 h hachurés et des « à classer » est probablement dans son 1x4 | D220_ADD 1815,1512 / 1884,1454 : rangée de 4 segments |
| 7 | Station F à confirmer | 0 | 32 | +32 | Hors périmètre (alarme existante, non chiffrée) | nomenclature |
| 8 | Éclairage « à classer » (55 carrés + 27 + 5) | — | 87 | ±87 | Libellé plus grossier : une partie devrait aller dans mural/1x4/2x4 | D210_ADD 1203,302 : carré mi-noir existant (unité d'urgence ?) |
| 9 | 2x4 | 579 | 554 | −25 | Convention / à classer : 17x33 classé « à classer » au lieu de 2x4 | D211_ADD 352,1972 masque 17x33 |
| 10 | Mural | 14 | 0 | −14 | Oubli IA (libellé absent) : rectangle pointillé à 2 points contre un mur, classé en 1x4 | D212_ADD 1490,1210 (PLAUSIBLE) |
| — | Prises | 7 | 17 | +10 | IA : 13 prises plafond de projecteur (note 6) réelles | D220_ADD 1225,1003 / 1369,1003 : cercles pointillés, classe B-114 |
| — | Détecteur M / HP classe (par autres) | 0 | 16 | +16 | Hors périmètre (CSSST, note générale 01), déjà étiqueté par autres | D210_ADD 1061,304 |

Répartition des 10 : oubli IA 2 (interrupteurs, mural), oubli humain 1 (encastré), convention 5 (24 h, plastique/ballast, 1x4, à classer, 2x4),
hors périmètre 2 (détecteurs, station F).

## Tirage de 10 marques
| Feuille | Label | x,y | Verdict |
|---|---|---|---|
| D220_ADD | 1x4 segment | 1815,1512 | OK |
| D220_ADD | 1x4 segment | 1884,1454 | OK |
| D220_ADD | prise plafond projecteur | 1369,1003 | OK (cercle pointillé) |
| D220_ADD | prise plafond projecteur | 1225,1003 | OK |
| D211_ADD | 1x4 segment | 857,2072 | OK |
| D211_ADD | 1x4 segment | 524,1889 | OK |
| D210_ADD | 1x4 segment | 897,718 | OK (1x4 isolé) |
| D210_ADD | détecteur M par autres | 1061,304 | OK |
| D210_ADD | éclairage carré à classer | 1203,302 | OK (objet réel, mal classé) |
| D212_ADD | rond encastré | 1551,1221 | OK (vérifié sans marques) |
Résultat : 10/10.

## Règles à ajouter à `releve-planexpert`
- Relever les interrupteurs en pointillé (symbole « $ » de la légende E001) sur les plans de démolition d'éclairage. Preuve : S-1835, 176 chez l'humain, 0 chez l'IA (D220_ADD 1860,1430).
- Ajouter un label « Dém. luminaire mural » pour le rectangle pointillé à points collé à un mur ; ne pas le fondre dans le 1x4. Preuve : S-1835, humain 14 (D212_ADD 1490,1210).
- Produire les lignes par règle plastique/ballast/entreposage = somme des luminaires enlevés. Preuve : S-1835, 2567 = 1927+579+41+14+6.
- Pour une démolition, sortir aussi le total de luminaires en unités 4 pi à côté des segments, et dire si les 24 h hachurés sont inclus. Preuve : S-1835, 1x4 humain 1927 contre IA 1888 + 218 en 24 h.
- Mettre dépose/repose temporaire (24 h, détecteurs) dans une section séparée « temporaire (forfait) », sans la mêler au démantèlement. Preuve : S-1835, devis 1.19.4 surligné et « TEMPORAIRE = » manuscrit.
- Classer les masques 17x33 comme 2x4 (tolérance ±2 pt), plutôt que « à classer ». Preuve : S-1835, D211_ADD 352,1972, 2x4 −25.
- Haut-parleurs télécom : sortir dépose et réinstallation en 2 lignes de même quantité. Preuve : S-1835, 153/153 chez l'humain.
