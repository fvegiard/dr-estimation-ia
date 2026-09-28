# STATUT — relevé automatique « S-1695 »

Date : 2026-09-22 03:48 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| 2024-023_Playground Hotel électrique_Soumission REV1.pdf | 21138470 | 4fe8eee5b3e2ca7f1b52b70b1d6ebc58ad1a10434f2e9950dcd27d7ff0a58b31 |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1695-Dossier-complet.pdf | 12865792 | 75f7a825afe1d5f7c2781f4de54ca6ebc7ffa27ad5e935b048f894f8f806b62b |
| S-1695-Plans-annotes.pdf | 12712510 | 76f118e67fcdf9a3b5da9f07d127aa128763602d128b5f8cf39b22b390ef0f0b |
| S-1695-Rapport-de-metre.md | 29538 | 826769152fe4be132fd57245a222728a128da07674ac25f487f9db0834880c72 |
| S-1695-Rapport-de-metre.pdf | 153569 | 182263e8ec5ec0be427e1eb0cc26d9a18ca9de8252b4940057602cbc2d303038 |
| journal-etapes.log | 9402 | 004518d5d7cb1be85018ee44d8bee34676ba541a3ce50ba88497512014f16a4a |
| S-1695-planexpert/S-1695.qpl | 159777 | fcf5a0f7a6d0073f2c4d00711afa53dfeb054e3ce19117826ca1f0a388c735fc |

Le projet Plan Expert `S-1695.qpl` est dans `S-1695-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| prepare | 0.0 min | déjà à jour |
| agent Claude | 18.5 min | success / code 0 |
| build_qpl | 0.0 min | ok |
| render_pdf | 0.2 min | ok |
| total | 18.7 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : 220 · sous-type : success
- coût estimé (client, `total_cost_usd`) : 27.291062500000006 $ US
- jetons : entrée 268, cache créé 1100434, cache lu 27752765, sortie 96360
- session : `ee0971be-0747-5d2f-962e-a9f568c158d0` · dossier de travail : `/home/claude/releve-auto/runs/S-1695/OUTBOX/S-1695/travail`

### Résumé de l'agent

Relevé S-1695 (Playground Hotel) terminé : tous les fichiers de sortie sont écrits.

- **Feuilles :** les 23 pages sont classées (17 plans, 1 légende, 2 schémas, 2 tableaux, 1 page titre), avec le vrai numéro de cartouche. Plans relevés : E200 à E203, E210 à E213, E217 à E219, E400, E401, E800 à E803.
- **Marques :** 1 719 au total, dont 1 306 lues sur des étiquettes texte et 413 relevées visuellement. Les faux positifs ont été retirés : adresses d'alarme posées sur des modules MRA/MAT, et doublons de CD-IT-01, des volets VM et d'une caméra.
- **Réserves :** 25 (R-001 à R-025).
- **Le plus important :** les chambres typiques (E400/E401) ne sont dessinées qu'une fois. Leurs quantités sont donc par chambre type ; il faut encore les multiplier par le nombre de chambres de chaque type aux niveaux 4 à 6.
- **Pas relevé dans les chambres types :** interrupteurs, détecteurs de fumée à base vibrante, télécom.
- **Autres manques :**
  - la longueur des luminaires linéaires reste à métrer ;
  - les contrôles Lutron ne sont pas comptés ;
  - l'éclairage d'urgence n'est pas relevé, sauf les enseignes de sortie ;
  - les feuilles E300, E301/E302 (sans texte lisible) et E804 ne sont pas chiffrées ;
  - pour l'alarme, le type exact de chaque appareil n'est pas distingué (détecteur ou poste, haut-parleur ou haut-parleur + stroboscope).
- **Pas de comparaison :** aucun export de M. Dupuis n'était fourni (`estimateur/` vide), donc pas de `comparaison-estimateur.md`.
- **Commandes refusées :** mes scripts Python d'aide (lecture des mots par zone, filtrage automatique) ont été bloqués faute d'approbation. J'ai fait ces corrections à la main dans les CSV. La vérification que chaque libellé existe dans `nomenclature.csv` a donc été faite à la main, pas par la commande `cut … | sort -u`.

## reserves.md

# Réserves — S-1695 Playground Hotel (2024-023, soumission REV1)

R-001 · toutes feuilles · Aucun export Plan Expert de l'estimateur (`estimateur/` vide) : pas de `comparaison-estimateur.md`.

R-002 · E400 / E401 · **Chambres typiques dessinées une seule fois** (11 types : universelle 1-3, luxe, luxe XL, première double, prestige, signature, présidentielle…). Sur E200-E202 / E210-E212 les chambres sont grisées ou réduites à un cadre de boîtes de jonction. Les quantités E400/E401 sont **par chambre type** : il faut les multiplier par le nombre de chambres de chaque type aux niveaux 4, 5 et 6 (plans clés E400/E401). Ce multiplicateur n'a PAS été appliqué.

R-003 · E400 · Seuls les luminaires (étiquettes A1…D2) et les HP/stroboscopes 177cd (mention E.I.) sont relevés. **Non relevés** : interrupteurs ($ avec lettres a…h, 3a/3b, 4a/4b), détecteurs de fumée à base vibrante, sorties TV/data, prises USB de chevet dessinées sur E400. À relever visuellement chambre type par chambre type.

R-004 · E401 · Prises relevées par étiquette de circuit (CCT-PRISES / CCT-DDFT / CCT-FRIGO / CCT-CAFÉ). Les CCT-PRISES « (DÉT. FUITE) » (détecteur de fuite sous nuage) sont comptées comme prises chambre ; les prises sans étiquette CCT et les sorties TV/data/WiFi des chambres types ne sont pas relevées.

R-005 · E200-E202 · Un luminaire = une étiquette. Les étiquettes qui désignent une rangée ou un profilé linéaire (B7, B9, C3, C4, D1, D3, D5) sont comptées comme 1 segment : **longueurs à métrer** (échelle 1/8 po = 1 pi). D1 : longueur « à confirmer » selon E001.

R-006 · E200-E202 · Note générale : contrôles des corridors / jardin par système Lutron (contrôle local, « prévoir une zone par type d'appareil »). Les modules/panneaux Lutron ne sont pas dessinés : non comptés.

R-007 · E200-E202 · Phares d'urgence et accumulateurs (Lumacell MQM / RG24S) : non identifiés sur les tuiles ; seules les enseignes de sortie ont été relevées. Vérifier si l'éclairage d'urgence est dessiné ailleurs.

R-008 · E200 · Groupes d'interrupteurs du spa (a-b-c, e-j-k, f-g-h, m-n-p, q-r-s, t-u-v) comptés comme 3 interrupteurs simples chacun ; type exact (gradateur 0-10V ?) à confirmer.

R-009 · E202 · Six carrés à croix avec bulle note spécifique 1 (« alimentation des appareils d'éclairage extérieurs », circuits N6A-43, N6B-43/45, N6C-43, N6D-35/37) relevés en « Boîte de jonction ». Les appareils extérieurs eux-mêmes ne sont pas dessinés.

R-010 · E210-E212 · Chambres : cadre de 5 carrés à croix = 1 marque « Boîtes de jonction chambre ×5 » (5 boîtes). Carré plein (chambres universelles) = « Raccord direct ».

R-011 · E210-E212 · Plinthes : 1 marque par étiquette de puissance (500W…2500W, hexagone A). Thermostats de ligne non vus sur ces feuilles ; bulle « CHAUFFAGE RADIANT (SI REQUIS) » en haut de E211/E212 (nuage) non chiffrée — à confirmer.

R-012 · E210-E212 · Symbole « carré H » (4 sur E210) hors lecture de légende → « Élément H — à classer » (hygrostat/humidistat probable).

R-013 · E210-E212 · Prises / sorties télécom relevées visuellement hors chambres ; relevé dense aux locaux serveurs et élec. — précision ± 1 appareil par local. Les « x2 » près des triangles télécom sont comptés 1 marque (quantité 2 dans `note`) : **à doubler au chiffrage**.

R-014 · E217 / E218 / E219 / E213 · CD-IT-01 (208V 40A, UNH-5-A-7/9) apparaît sur E213 et en rappel sur E217-E219 : compté **une fois** sur E213.

R-015 · E219 · Étiquette « CAM » (2495, 600) = rappel de la caméra de E212 : écartée.

R-016 · E803 · Volets VM-T-A…E dessinés sur E213 (services) et E803 (alarme, « 120V via relais D6-034/042 ») : comptés **une fois** sur E213 ; les relais sont les MRA de E802.

R-017 · E800-E802 · Dispositifs AI comptés par étiquette d'adresse : « AI dispositif adressé D » (détecteurs/stations — type non discriminé) et « AI signal adressé S » (HP ou HP+strobe — type non discriminé). Les adresses qui étiquettent un MRA/MAT ou un détecteur de conduit (D4-025…028, D5-024…030, D6-033/034/037…044) sont exclues pour ne pas doubler les modules.

R-018 · E800-E802 · Détecteurs de chambres (base vibrante) sans étiquette d'adresse : non relevés (voir R-003).

R-019 · E218 · Unités mécaniques en gris (FUM-1, FUM-2, UAF-2, UAF-3, AC-2, AC-3, UC-2) sans symbole électrique : non relevées ; raccordement probablement à l'existant ou par autres — à confirmer.

R-020 · E300 · Unifilaire « distribution existante modifiée » : panneaux N4A…N6D, UN3H, transformateurs non comptés en marques (pas de plan d'étage) — à relever à la main sur E300 (neuf en noir, existant en gris).

R-021 · E301 / E302 · Cédules de panneaux sans texte vectoriel (98 mots, cartouche seulement) : raccordements de cédule non recoupés.

R-022 · E804 · Matrice de programmation désenfumage : non chiffrée en marques.

R-023 · E213 · Cartouche mentionne l'addenda ME-01 (24-09-25) déjà intégré à la révision 1 ; aucun fichier d'addenda séparé reçu.

R-024 · QC138 · Liste des plans : E-214/E-215/E-216 (contrôle d'accès) non émises — contrôle d'accès non relevé.

R-025 · E201 / E202 · Parcours visuel moins dense qu'E200 (pas de spa) ; interrupteurs de locaux techniques relevés, prises des corridors relevées sur E211/E212.

