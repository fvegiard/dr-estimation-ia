# S-1902 — Soumission (référence officielle, révision 1 du 2026-10-26 — addenda E-01)

Bibliothèque Georgette-Lepage, 2001 boul. Rome, Brossard — Technologie RFID, aménagement RDC et étage — AO SP-GTER-26-0080 —
invitation Constructions R.D.J. (E-26-75-GE, SEAO 20173885 / BSDQ M-1026-26) transférée par André Lamothe (Groupe SIP) le 2026-10-07.
Dossier d'évaluation : la soumission produite avec Claude est comparée à celles de Jo (Jonathan Parent) et de Daniel Dupuis.

| Fichier | Rôle |
|---|---|
| `chiffrage_dupuis.py` → `chiffrage_dupuis.json` | modèle de chiffrage ligne par ligne (quantités, prix d'assemblage et temps Dupuis, lots) ; `--ventiler` réécrit la ventilation de `soumission.json` |
| `soumission.json` | contenu de la soumission (client, détails, ventilation par article, travaux, prix séparés, exclusions, signataire) |
| `S-1902_Chiffrage_methode_Dupuis.xlsx` | classeur imprimable (Sommaire 1 page / Détail / Par article), 181 formules |
| `Soumission_S-1902_Georgette-Lepage.pdf` | soumission au gabarit DR, 3 pages |
| `S-1902_Dossier_complet.pdf` | soumission + chiffrage imprimable en un seul PDF lettre (9 p.), sans les plans |
| `S-1902_Chiffrage_p*.png` | aperçus regardés avant émission |

**Prix soumis (rév. 1) : 233 000 $ avant taxes** (TPS 11 650 $, TVQ 23 241,75 $, 267 891,75 $ taxes incluses) — 1 050 h chargées × 85 $/h +
98 376,90 $ matériel/lots = 187 626,90 $ (sommaire ACCEO) × 1,244 = 233 408 → 233 000 $. Prix séparé PS-1 parasismique 8 058 $. Validité 30 jours.

## D'où vient chaque montant (réponse à la question des patrons, 2026-10-26)

| Poste | Montant | Source | Statut |
|---|---|---|---|
| Prix et temps unitaires (prises, data, conduits, percements, GPR, interrupteurs, détecteurs, annonciateur, nacelle…) | — | `prix/dupuis/catalogue-prix-temps-dupuis.csv`, colonne « À UTILISER » (dernier relevé ACCEO de Daniel Dupuis) | **vérifié** ligne par ligne |
| Taux horaire 85 $/h | — | Dupuis S-1797, S-1835, S-1854, S-1881 (août–oct. 2026) | vérifié ; règle de choix du taux à confirmer avec Jo |
| Lot luminaires ADD E-01 (A1 Cooper ×10, Axis Slate ×32, Pinnacle M/M1 ×5) | **42 820,79 $** | **soumission Éclairage Hi-Tech S100946-R1 du 2026-10-23** (Tiziana Rollo, prix d'achat via distributeur Guillevin, 30 jours, transport Axis prépayé) — courriel Daniel Dupuis → Francis du 2026-10-22 11 h 53 ; PDF vu page par page le 2026-10-27 : génération unique DevExpress 21.1.5 le 2026-10-21 13:41 (3 p., items ADD E-01, sous-total 42 820,79 $) puis mise à jour incrémentale (2 `%%EOF`) de la page 1 seulement (« 100946 → 100946-R1 », « 15 → 23 oct ») ; l'en-tête « 15 oct / 100946 » de la p. 2 est l'original non retouché, pas un mélange de versions | **ferme** ; en sus non chiffrés : transport Pinnacle, courtage/dédouanement et tarifs USA (mis en exclusion) ; note Cooper « 347 V discontinué » à valider ; à confirmer avec Tiziana : que 42 820,79 $ couvre toute la liste ADD E-01 et que les 30 jours courent du 23 oct (→ 22 nov 2026) |
| Luminaires E ×3 (475 $) et Z6 ×3 (161,60 $) | 1 909,80 $ | allocation Gerrie prix réguliers / agents (2026-10-20) | **allocation** — absents de la soumission Hi-Tech R1 ; l'ADD E-01 n'a pas pu être lu (salle de plans RDJ en erreur 503 le 2026-10-26) |
| Panneau NF 225 A 42 cct + disjoncteurs | 6 200 $ | ≈ Schneider NF 3 400 $ + EDB 1P 95 $ ×20 + EJB 3P 300 $ ×3 — montant retenu par Francis le 2026-10-20 | **allocation** — aucune soumission Guillevin/Electrimat reçue |
| Services JCI/Simplex (bypass, 4007ES, annonciateur, ULC-S537) | 7 400 $ | montant retenu par Francis le 2026-10-20 ; prix demandé à JCI par Jo le 2026-10-08 | **allocation** — aucune soumission JCI reçue |
| 2 détecteurs Simplex 4098-9714 | 600 $ | idem | **allocation** |
| ~90 h de jugement (continuité de service 16 h, toit 24 h, coordination 20 h, essais 12 h, nettoyage 8 h, AI 20 h…) | — | reprises de `../entree/reference-Estimation_2.xlsx` | jaune dans le classeur |
| Facteur 1,244 | — | un seul couple observé : S-1844 (sommaire 191 909,19 $ → prix remis 238 744 $) | à affiner avec un 2ᵉ dossier |

Ces statuts sont repris tels quels dans la colonne « source » du classeur (jaune = allocation ou jugement). Rien d'autre n'est inventé.

## Ce que l'addenda E-01 change (d'après la soumission Hi-Tech, l'addenda lui-même n'ayant pas été lu)
- A1 : 11 → 10 (Cooper 24CGTS-L3C3 + clips sismiques CGTEQ) ; C1 : 33 → 32 modules Axis Slate (7′ ×11, 5′ ×5, 4′ ×2, 3′ ×14) ; **type M/M1 Pinnacle ajouté** (8′ ×4, 2′ ×1).
- Lot luminaires : 11 893 $ (allocation) → 42 820,79 $ (ferme) = **+30 928 $ de matériel → +38 500 $ de prix de vente** (194 000 → 233 000 $).
- Heures : 1 045,8 → 1 049,1 h relevées (toujours 1 050 h chargées).
- Addendas no 2 (2026-10-22) et no 3 (2026-10-24) : existent dans la salle de plans RDJ, non reçus ni lus → exclusion explicite dans la soumission.

Sources du chiffrage : `../releve.xlsx` et `../Plans-annotes.pdf` (relevé 2026-10-17, 645 repères), `../entree/reference-Estimation_2.xlsx`
(quantités hors plan et liste Lumen du 2026-10-07), `../../../prix/dupuis/` (catalogue Dupuis), `../../../outils/soumission/README.md` (méthode).
Historique des prix : Estimation_2 Léna 2026-10-08 = 112 381,39 $ (sans marge) ; v2 2026-10-20 midi = 158 296 $ ; v3 méthode Dupuis avec
médianes de conduits = 183 000 $ ; v4 2026-10-20 = dernières valeurs du catalogue = 194 000 $ ; **v5 2026-10-26 = ADD E-01, lot éclairage Hi-Tech R1 = 233 000 $**.

Contrôle de la rév. 1 (bac à sable cloud, 2026-10-26) : chiffrage 187 626,90 $ / 1 049,10 h → 1 050 h ; classeur 181 formules, 0 erreur au
recalcul LibreOffice (Sommaire B10:B17 = 98 376,90 / 1 049,10 / 1 050 / 89 250 / 187 626,90 / 1,244 / 233 408 / 233 000) ; PDF 3 pages,
« 233 000,00 $ » = « Deux cent trente-trois mille dollars » = Σ 18 articles ; dossier regroupé 9 pages, les 9 pages regardées après fusion (planche). Formats de nombres forcés en français (Canada) `[$-C0C]` pour que
« 98 376,90 $ » s'affiche pareil dans Excel fr-CA et dans un LibreOffice anglais.
