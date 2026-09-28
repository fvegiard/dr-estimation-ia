# STATUT — relevé automatique « S-1808 »

Date : 2026-09-22 03:43 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 25-64_CPE Copains d'Abord_SOUM_REV01.pdf | 4928078 | 5abb4e6869f02671a16b88096e030d7aa62cd90f9964229b03d7ce50c5fc7a2a |
| 25-64_M_ADD.ME-01_20260629_S 1.pdf | 1691814 | 16fe1666e5048a010aa273ef359a7a22b0306ce65e7e4dd98ae2675cb902ae1f |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1808-Dossier-complet.pdf | 9675262 | ee529f166547ef1a11ff8dd24fb6a397cd81a5c80b31d7a48492304174f105a9 |
| S-1808-Plans-annotes.pdf | 9515121 | cb1484d62e8496378fd1ecf0ddc285996ca370391ef25a29c113c893f2cf19d9 |
| S-1808-Rapport-de-metre.md | 33362 | 7cf0b2c8a3f0da175407e3eb44f88aa5a735f698fc7fb905412cd271408c3876 |
| S-1808-Rapport-de-metre.pdf | 160461 | 91665a545b6229b01ae3831e79752fb607c5a3d44e5e435151b7528431593317 |
| journal-etapes.log | 8266 | aa83dd7871ebfa92c8d09efd9f85bdd8d7e24a0b04a40dadc25980f6b4b85172 |
| S-1808-planexpert/S-1808.qpl | 104993 | 2241d758075e346417f1950ec11ac5156b6dae009749d846d4c0d0cb493a853c |

Le projet Plan Expert `S-1808.qpl` est dans `S-1808-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| prepare | 0.0 min | déjà à jour |
| agent Claude | 18.4 min | success / code 0 |
| build_qpl | 0.0 min | ok |
| render_pdf | 0.1 min | ok |
| total | 18.6 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : 135 · sous-type : success
- coût estimé (client, `total_cost_usd`) : 19.639943499999998 $ US
- jetons : entrée 196, cache créé 446178, cache lu 24893817, sortie 109211
- session : `ee0971be-0747-5d2f-962e-a9f568c158d0` · dossier de travail : `/home/claude/releve-auto/runs/S-1808/OUTBOX/S-1808/travail`

### Résumé de l'agent

Le relevé S-1808 est terminé : les six fichiers attendus sont dans `travail/`. `comparaison-estimateur.md` n'a pas été produit parce que le dossier `estimateur/` est vide.

- **Feuilles** : les 22 pages sont classées. J'ai relevé 8 plans (E100/E101 éclairage et alarme, E200/E201/E202 services, élévations E051/E052, implantation E050), plus des éléments des schémas E010/E020, des cédules E004 et des détails E040/E041. L'addenda reçu (M-606) ne touche que la plomberie : aucune incidence électrique.
- **Total** : 826 marques, 534 lues sur les étiquettes texte et 292 relevées à l'œil. Par feuille : E100 216, E101 241, E200 161, E201 133, les autres ≤ 30 chacune. Les 94 libellés utilisés existent tous dans `nomenclature.csv`.
- **Luminaires** : les étiquettes « TYPE A » sont en deux mots et le script ne lit qu'un mot à la fois. J'ai donc ajouté ces luminaires à la main à partir des coordonnées des mots, avec le même contrôle pour les détecteurs « D » et les « F ».
- **Réserves** : 33 dans `reserves.md`. Les principales :
  - Distinction à valider entre les interrupteurs B.V. avec et sans gradation, et prises 15 A / 20 A non séparées.
  - Une unité AC dessinée sans étiquette sur E200, alors que la cédule AC-01 à 11 est déjà complète.
  - Les appliques extérieures EX2 et EX3 ne figurent que sur les élévations ; un doublon aux coins n'est pas vérifié.
  - 13 modules isolateurs dessinés contre le panneau d'alarme ; ce sont peut-être des cartes internes.
  - La numérotation de l'index E-001 ne correspond pas aux cartouches (E-100/E-101 y sont appelés E-200/E-201).
- **Manque** :
  - Les éléments linéaires ne sont pas métrés (artères, câble chauffant, conduits).
  - E004 et E032 sont des images sans texte, lues sur l'aperçu à basse résolution.
  - L'addenda ME-01 est peut-être incomplet.
  - J'ai demandé un contrôle final avec `comm`, mais la commande a été refusée par les permissions de la session. Je l'ai remplacé par une comparaison manuelle des deux listes de libellés.

## reserves.md

# Réserves — S-1808 CPE Les Copains d'Abord (HF Experts-Conseils, dossier 25-64)

Relevé du 2026-09-22. Chaque réserve donne la feuille, l'objet, puis la question ou la décision prise.

- **R-001 — (tous) — Export estimateur.** Le dossier `estimateur/` est vide. Aucune comparaison n'a été faite et `comparaison-estimateur.md` n'est pas produit.
- **R-002 — E001 / E100 / E101 — Numérotation.** L'index E-001 liste « E-200 éclairage et alarme RDC » et « E-201 … étage », mais les cartouches portent **E-100** et **E-101**. On a gardé les numéros des cartouches.
- **R-003 — M606 — Addenda ME-01.** Une seule feuille reçue : M-606 Équipements sanitaires (suite), rév. 3 « émis pour addenda ME-01 » du 2026-06-29. Elle ne touche que la plomberie (mitigeur thermostatique 12-ZW1070XL-PF, non électrique) : aucune incidence électrique. Si l'addenda ME-01 comprend d'autres feuilles (mécanique ou électrique), elles n'ont pas été reçues ni relevées.
- **R-004 — E100 / E101 — Interrupteurs B.V.** On a distingué visuellement « barre en bout de $ » (label **Interrupteur BV 2 scènes grad.**, 30) et « sans barre » (**Interrupteur BV 2 scènes**, 10). Cette distinction est à valider.
- **R-005 — E101 — Gradateur (8).** Symbole $ avec barre mais sans mention B.V. Il est classé « Gradateur » selon la légende. Ce pourrait être des interrupteurs nLight non étiquetés : à confirmer.
- **R-006 — E100 — Interrupteur simple (2).** Dépôt 106 (1108,1112) et salle électrique 104 (1010,1390) : $ sans barre ni B.V. À confirmer.
- **R-007 — E100 — Détecteurs D sans B.V.** Les deux détecteurs en (700.9,657) et (1107,661) sont comptés comme « Détecteur mouvement BV ».
- **R-008 — E200 / E201 — Prises 15 A / 20 A.** Le crochet 20 A est illisible à l'échelle : un seul label « Prise double ». Les calibres sont à tirer des cédules E-004.
- **R-009 — E200 — Unité AC sans étiquette** (905,1357), bureau DA, avec thermostat FPD. La cédule RDC AC-01 à AC-11 est déjà complète (11 étiquettes relevées). Elle est relevée en « Raccordement AC — à confirmer ».
- **R-010 — E200 / E201 — Ascenseur.** Le moteur gris PS-32/34/36 du puits RDC E200 (695,970) est **écarté**. L'ascenseur est compté une fois sur E201 (pompe hydraulique, contrôleur, sectionneur lumière), qui est son niveau (salle méc.). Le trait gris laisse penser que c'est fourni par l'ascensoriste.
- **R-011 — E051 / E052 — Appliques extérieures.** Les EX2 (18) et EX3 (2) ne figurent que sur les élévations, pas sur les plans d'étage. On les a relevés sur les élévations. Les doublons possibles aux coins entre deux élévations ne sont pas vérifiés.
- **R-012 — E200 / E201 — Thermostat AC fourni par autres (20).** T gris + FPD : contrôleur mural fourni par autres, libellé séparé non chiffré DR. La boîte et le conduit sont à prévoir selon le devis.
- **R-013 — E200 / E201 — Relais triac RT (33).** Le symbole est tracé en gris, mais il est à la légende électrique : relevé comme neuf. Le nombre de RT (33) ne correspond pas au nombre de SCR + OFM (39) : certains appareils ont un TI au lieu d'un RT.
- **R-014 — E200 / E201 — TI (8).** Les thermostats intégrés sont comptés à part (ligne de légende distincte). À retirer s'ils sont inclus au prix de l'appareil.
- **R-015 — E101 — Volets coupe-feu.** La note dit « prévoir 4 raccordements au total pour l'étage ». Il n'y a que 2 bulles : 4 marques posées aux bulles. Pour le RDC, aucune indication : rien n'est relevé.
- **R-016 — E020 — MI (18).** Les 13 MI dessinés contre le PAI sont comptés comme modules isolateurs ; ce peut être des cartes internes du panneau. La boîte « I » (2) et le sablier du puits (1) sont hors légende : « à classer ».
- **R-017 — E020 — Autres appareils du schéma.** Les détecteurs de fumée de gaine (3), l'ANN, le GSM, le MTA et les RFL ne figurent qu'au schéma : ils sont comptés sur E020. Les appareils des boucles d'étage du schéma (K, F, détecteurs) ne sont **pas** recomptés, car ils sont déjà relevés en plan.
- **R-018 — E100 / E020 / E041 — Hotte H-1.** Le raccordement alarme est compté une fois sur E100 (note 1), la note 1 de E020 est écartée. E041 : l'essentiel est fourni ou installé par la ventilation. On a relevé seulement le SF VA-01 (fourni et installé DR) et le démarreur hotte (fourni par autres). Le filage de contrôle hotte / PAI est à métrer.
- **R-019 — E004 — Cuisinière et boîtes VRF.** La cuisinière PCUI-14/16 et les boîtes de dérivation VRF (PSS1-37/39, PSS2-47/49) n'apparaissent qu'aux cédules, sans symbole en plan : posées sur E004. E004 est une image raster, lue sur l'aperçu : les circuits sont à revérifier.
- **R-020 — E200 — PCUI-9 deux fois** (cuisine et garde-manger), alors que la cédule prévoit PCUI-9 et PCUI-11 pour deux congélateurs : étiquette probablement erronée. 2 prises comptées.
- **R-021 — E200 — Îlot de cuisine (PCUI-15).** Aucune prise n'est dessinée. Seule la « colonne électrique » (note 1) est comptée : le nombre de prises de l'îlot est inconnu.
- **R-022 — E200 / E201 — Contrôle d'accès.** 4 bulles au RDC (note 2) et 4 à l'étage (note 1), soit 8 portes. Équipements fournis par autres ; part DR : conduits vides, relais au PAI, alimentation 120 V.
- **R-023 — E202 — Bulle note 1 sans prise** en (1002,710). Relevée « Prise service toiture — à confirmer » (règle des 7,5 m autour des équipements CVCA).
- **R-024 — (tous) — Linéaires non métrés.** Artère 2×(4#250 NUAL RWU90) PVC 2½ po (E-005 : 19,5 pi), artères PS→TX1→PSS2→PSS1/PCUI, câble chauffant OWC-M (2 zones, longueur absente), conduits télécom 2 po : **à métrer**.
- **R-025 — E101 — TYPE D.** Dessiné comme un rond encastré dans les toilettes, alors que E-032 décrit un CLX L48 surface linéaire. À confirmer.
- **R-026 — E032 — Nature exacte de Z2 / Z4 / Z5 / Z6.** Selon les modèles Stanpro, sur un tableau raster : Z2 et Z4 sont dessinés en combiné batterie + tête / enseigne.
- **R-027 — E100 — Klaxon extérieur E.I** (540,378). Compté dans « Klaxon », avec mention dans `note`.
- **R-028 — E010 — Unifilaire non recompté.** PS, PSS2, TX1 (E201), PSS1, PCUI, C2, HQ, boîte de tirage et 400 A (E200) sont comptés en plan. Seuls C1, la minuterie, le sélecteur, la MALT et le contreplaqué / conduits télécom sont posés sur E010.
- **R-029 — E031 — Appariement cédules ↔ plan.** AC-01 à 11 (E200), AC-12 à 20 (E201), VE-01 (E202), VE-02/03/04 (E200), VE-05 (E201), EVP-01, VA-01, SE-01, P-01 (E200), SE-02/03/04, HUM-01/02, ECH-01/02, CE-01, P-02 (E201), COND-1/2/3 (E202 ; la cédule dit COND-01/02/03). Aucun équipement de cédule n'est resté sans symbole en plan.
- **R-030 — (tous) — Existant et démolition.** Aucun élément électrique existant ou à démolir n'a été vu (bâtiment neuf de remplacement). Les traits gris sont de l'architecture.
- **R-031 — E200 / E201 — SCR et OFM.** Toutes les puissances (450 à 1 500 W) sont regroupées sous un label par type ; la puissance est lisible au plan.
- **R-032 — E040 — Interrupteur lumière de fosse d'ascenseur.** Compté 1 sur le détail, faute de symbole en plan.
- **R-033 — E002 / E003 / E005 / E030 / E042 — Non relevés.** Devis, calculs, extraits du Code et schémas types de contrôle : non relevés, rien à compter.

