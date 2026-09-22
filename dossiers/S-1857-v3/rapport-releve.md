# Rapport de relevé — S-1857 Maison communautaire Saint-Michel (v3, à l'aveugle, 2026-09-22)

Agent releveur, skill `releve-planexpert`, dossier `S-1857-v3/travail`. Aucun relevé humain ni export d'estimateur n'a été fourni : pas de comparaison.

## Méthode suivie
1. **Classement** des 22 pages (21 feuilles de base et 1 feuille d'addenda). Chaque aperçu a été ouvert et le numéro du cartouche lu (voir `feuilles-classement.csv`). J'ai corrigé deux noms provisoires de `prepare.py` : « E600 » est en réalité E000 (page titre) et « E600_2 » est la vraie E600.
2. **Nomenclature** (102 libellés) lue dans les légendes E103 et E104 et dans le tableau des luminaires E102. J'ai ajouté les départs de cédule (E600 addenda) et les symboles hors légende sous « à classer ».
3. **Occurrences texte** : j'ai lancé `uv run releve/extract_occurrences.py`, puis contrôlé chaque mot par sa couleur vectorielle et sa position. Les bulles d'axes et le texte gris d'architecture sont exclus, de même que le cartouche et le doublon E150. Certains libellés ont été précisés d'après le symbole : Do/Di mural ou plafond, luminaire en service continu, K combiné visuel (⊗) ou intempéries (Ei).
4. **Occurrences visuelles** : j'ai détecté tous les symboles rouges et magenta (prises, sorties data) des feuilles E405 à E409 par leur géométrie vectorielle, puis classé chacun selon la légende E103 (∥ = 15A, ⊣ = 20A, capuchon = DDFT, barre = 1070mm, carré = mobilier, cadre = plancher, MO, Ei, C, S). L'éclairage d'urgence, les commandes et les raccords ▲CC ont été classés un par un sur des planches de zooms. Le résultat a été vérifié par `zoom.py` avec les marques (E401, E402, E403, E406, E408).
5. **Addenda ADME-01** : E600 rév. 2 remplace E600 rév. 1. J'ai comparé les 5 cédules plus P-P1 et relevé les départs sans symbole au plan. Détails dans `reserves.md` R-002 et R-003.
6. **Cédules et unifilaire** (étape 5b) : j'ai relevé les départs d'équipement sans symbole au plan et apparié ceux déjà relevés en plan (R-008).

## Feuilles traitées (22 pages) — par type
| type | nb | feuilles |
|---|--:|---|
| plan | 11 | E150, E400, E401, E402, E403, E404, E405, E406, E407, E408, E409 |
| legende | 3 | E102, E103, E104 |
| schema | 2 | E200, E201 |
| tableau | 1 | E600_ADD (E600 rév. 2 ADME-01) |
| detail | 1 | E500 (vide) |
| autre | 3 | E600 (= E000 page titre), E100, E101 (devis) |
| remplacee | 1 | E600_2 (E600 rév. 1) |

## Preuve par feuille (occurrences ajoutées par feuille — comptes consolidés en fin de relevé, le rapport ayant été rédigé en une fois)
- **E400 SOUS-SOL ÉCLAIRAGE** : 77 occurrences (65 texte + 12 visuel). Principaux : DR5 29, Do mural 12, DR51 8, DR52 service continu 4, PH1 4, DW4 3, accumulateurs 6, enseignes 4.
- **E401 RDC ÉCLAIRAGE** : 249 (217 + 32). DS1 74 et DS1 service continu 4, DS0 50, Do 29, B 17, Di 14, DR5 11, DMW1 5, urgence 26, ovales à classer 2, CME-01 1.
- **E402 NIVEAU 1 ÉCLAIRAGE** : 317 (292 + 25). DS0 100, DS1 58 et DS1 service continu 2, Do 42, B 31, DR51 31, Di 16, urgence 25.
- **E403 NIVEAU 2 ÉCLAIRAGE** : 161 (141 + 20). DS1 63, DS0 26, Do 13, Di 10, B 9, DR5 7, DMW1 5, urgence 15, gradateurs 3.
- **E404 TOITURE ÉCLAIRAGE** : 0 (aucun appareil ; 6 mots exclus = bulles d'axes et cartouche).
- **E150 IMPLANTATION** : 0 retenu (5 DMW1 exclus comme doublons d'E401, R-006).
- **E405 SOUS-SOL ALARME / PRISES** : 90 (42 + 48). Prises 20A 25, K 12 et combiné 1, ▲CC 10, Sx/Ls/ID 17 (entrée d'eau), DDFT 5, pompes à classer 3, M 2, Xfo 2, sectionneurs 2, MHQ 1, panneaux 2.
- **E406 RDC ALARME / PRISES** : 218 (49 + 169). Prises 20A 73, 15A 21, DDFT 9 et DDFT Ei 1, mobilier 9, 1070mm 8, MO 5, C 3, S 1, plancher 3 ; data 25 ; K 31, M 4 ; LV 4, Ht 1, ▲CC 6, BRVE 2, CC 3R 2, PAI, TRA, PMI, Ts et ACP.
- **E407 NIVEAU 1 ALARME / PRISES** : 170 (47 + 123). Prises 20A 96, 15A 3, DDFT 5, MO 4, mobilier 2 ; data 13 ; K 38, M 3 ; SM 2, LV 2.
- **E408 NIVEAU 2 ALARME / PRISES** : 93 (30 + 63). Prises 20A 34 et 1070mm 1, DDFT 4 et DDFT Ei 3, MO 2, 15A 2, mobilier 5 ; data 10 ; K 14, combinés 4 et combinés Ei 2, F 3, T 1, M 2 ; SM 2, LV 1 ; à classer 3.
- **E409 TOITURE ALARME / PRISES** : 3 (1 + 2). Combiné Ei 1, raccords THP-1 et VRT-1.
- **E200 (schéma)** : 4 départs sans symbole (SPS-1 ×2, ascenseur, SE-1).
- **E600_ADD (cédules addenda)** : 37 départs sans symbole (VC 8, éviers 7, PC 6, PREF 4, chauffage P-P1 4, UAT 2, LV 2, PECD-1, VE-SECH, SE-2, four combiné).

## Totaux
- `occurrences-texte.csv` : 965 lignes, dont **884 retenues** et 81 exclues (`exclure=1` avec motif).
- `occurrences-visuel.csv` : **535** occurrences.
- **Total : 1 419 marques.**
- 10 libellés les plus nombreux : Prise duplex 20A 228 · Luminaire DS1 195 · Luminaire DS0 176 · Klaxon alarme (K) 95 · Détecteur inoccupation plafond (Do) 73 · Bouton-poussoir (B) 58 · Luminaire DR5 50 · Luminaire DR51 43 · Sortie data 41 · Détecteur infrarouge plafond (Di) 40.
- Contrôle final : chaque `label` des deux fichiers d'occurrences existe dans `nomenclature.csv` (0 libellé manquant).

## Ce qui n'a pas pu être relevé / limites
- Addenda 02 incomplet : seule E600 a été reçue, sans le texte de l'addenda (R-003). Les plans restent en rév. 1.
- Les symboles à classer (R-009 à R-014) sont à confirmer par l'estimateur.
- Conduits, câblage et chemins de câbles ne sont pas métrés (R-023).
- Le classement automatique 15A/20A, mural/plafond et les directions d'enseignes repose sur la géométrie vectorielle. Il a été vérifié par échantillon (zooms), pas symbole par symbole sur toutes les feuilles (R-016 à R-021).
- `build_qpl.py` et `render_pdf.py` n'ont pas été exécutés (réservés à l'orchestrateur).

STATUT : TERMINÉ (aucun outil refusé ; 28 réserves, dont 7 symboles ou équipements « à classer / à confirmer » et un addenda incomplet à faire vérifier)
