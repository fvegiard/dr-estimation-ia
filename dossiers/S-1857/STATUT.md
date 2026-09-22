# STATUT — relevé automatique « S-1857 »

Date : 2026-09-22 04:06 · État : **TERMINÉ**

## Entrées

| fichier | octets | sha256 |
|---|--:|---|
| Addenda02-ADME-01-plans-electrique-E600.pdf | 1208763 | c5076cb555858c9eb4882a06b6ab653115700f555af013b353a0dc913d40f1c6 |
| plans-electriques/E000_Rev0.pdf | 369102 | d0f3f414999c47434a17e56a7a14122ce4a67a330d39760fa9739157f6e7597c |
| plans-electriques/E100_Rev0.pdf | 1794636 | 93b3e225fbfde0d9f94f9fb9f63184c52e1090eb4f58c80306172239077fb361 |
| plans-electriques/E101_Rev0.pdf | 1555199 | 8a490459526a44109b479a24fa0515522cdb9968f4d385d7a8a2ab73f6ecbf6a |
| plans-electriques/E102_Rev0.pdf | 321490 | 1265774c70a5ba64eeae08e010c2b6358582adf6b0d3dac2a35cf90e5b7ec3d5 |
| plans-electriques/E103_Rev0.pdf | 373306 | 21dc791866215b9ecc2bfa1bf5fadb352efe4c858f84bcd89e17662efbfe0d2e |
| plans-electriques/E104_Rev0.pdf | 347932 | e5318ce6ed1d38292ae02cf8a70b08a3f4e7e029534af2a4636ff33346499cc7 |
| plans-electriques/E150_Rev0.pdf | 661011 | c328c77d4067beb33081bcfd1ba9b296a36d166f57a6e77d26aef135decdfe4f |
| plans-electriques/E200_Rev0.pdf | 315646 | 5834a9d1544fcf191963d65b464fbb66c08d51899ff74919ee2e869598a5c1e2 |
| plans-electriques/E201_Rev0.pdf | 502855 | e9717efe9effa1d68dff17d2e23656f9c2d48bf8e096c3c3fc71a8493728eb9e |
| plans-electriques/E400_Rev0.pdf | 432678 | 3206a6650ce3664679451c9d751def9d64d336f67e86aa4a5eb3fe77bff79a9a |
| plans-electriques/E401_Rev0.pdf | 853974 | c3d6ee467463dbb706d83214064acc67bbcb0362fd3a7f8adba2ddc92f093e5b |
| plans-electriques/E402_Rev0.pdf | 678123 | bf7807eb7e15a80d5eb6ad58ba361c1800f2f6e53bbc8f3505932416f81a390e |
| plans-electriques/E403_Rev0.pdf | 766823 | 20120659537cf04e23cdc86c89015f6463666e09919917feae88c7c55ba2db50 |
| plans-electriques/E404_Rev0.pdf | 346749 | 5577c85f5233553eb72b1ce0669e55fa908263a91ce7f85890f905c9b3f3d41c |
| plans-electriques/E405_Rev0.pdf | 498070 | 2b4445455e11af25e64395d760642ced2adc737832578df1864372ca5b99416d |
| plans-electriques/E406_Rev0.pdf | 820017 | a95b7b77b44d0f2b35b5a659fdf38fb378dba6da2a6051191085af67294ab191 |
| plans-electriques/E407_Rev0.pdf | 632240 | 84a93d28628fdf2f0c47ab6488bc882fc5338603d3bc17a8c142bf6c4e41c6bf |
| plans-electriques/E408_Rev0.pdf | 740552 | c6e997b45036bef95b77c537a1f4a67a1f4eeca8ada563b7e53baba9f3e6a789 |
| plans-electriques/E409_Rev0.pdf | 371422 | f26ba98f07436995dc143bafab4dbd8216ccc1282026fb2302c7af79ad122626 |
| plans-electriques/E500_Rev0.pdf | 269322 | e7b02b7fcbcede394fe94e94d8425f05700412b9b1238e5828c4d11591b67707 |
| plans-electriques/E600_Rev0.pdf | 333881 | 450fcc5688ef97924799391fd450005d6f36f5ca29367109393af771cf51c891 |

## Sorties

| fichier | octets | sha256 |
|---|--:|---|
| S-1857-Dossier-complet.pdf | 6850915 | 8f857c79c9b4c95441706cefa93db3a2486f546304131358b576da25b4497891 |
| S-1857-Plans-annotes.pdf | 6701090 | 3dc30add54387abf25e55d72cea28c6bfbb5f7a26d90aa8cd31e4792eade9be4 |
| S-1857-Rapport-de-metre.md | 27168 | fbcda3f39330dfb3c8576455e153278f539c1d6a0ab64437c1a621f479489b0b |
| S-1857-Rapport-de-metre.pdf | 150162 | c38e0f07cb95c60c6bde591e3513dd2d722217ea0255d6686e7bdf6fae4247f4 |
| journal-etapes.log | 7422 | d30bddc7a555c4b39a6507c8ba03b9cf277d9bd543e9fabd21fc3ba548389122 |
| S-1857-planexpert/S-1857.qpl | 143408 | 9178afe4b14c98dd0b8ab3c8ae2d9067b2c5735623b31e464e44a0013166904b |

Le projet Plan Expert `S-1857.qpl` est dans `S-1857-planexpert/` avec ses rasters PNG : copier le dossier entier, puis Fichier → Ouvrir dans Plan Expert. Le PDF « Plans annotés » et le rapport de métré ci-dessus sont rendus par `releve/render_pdf.py` à partir du même .qpl.

**Export natif Plan Expert : non** (étape non exécutée)

## Étapes

| étape | durée | résultat |
|---|--:|---|
| prepare | 0.0 min | déjà à jour |
| agent Claude | 18.0 min | success / code 0 |
| build_qpl | 0.0 min | ok |
| render_pdf | 0.1 min | ok |
| total | 18.2 min |  |

## Agent de relevé — claude -p (headless)

- modèle : `opus` · tours : 216 · sous-type : success
- coût estimé (client, `total_cost_usd`) : 35.134022499999986 $ US
- jetons : entrée 346, cache créé 974899, cache lu 46610255, sortie 83127
- session : `ee0971be-0747-5d2f-962e-a9f568c158d0` · dossier de travail : `/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/travail`

### Résumé de l'agent

Le relevé S-1857 est écrit : 1 421 marques sur 11 feuilles et 25 réserves, mais une partie reste à vérifier (voir la fin du résumé).

- **Feuilles** : les 22 pages sont classées, dont 9 plans relevés (E400 à E409 ; E404 n'a aucun appareil) et les cédules de l'addenda E600_ADD. L'addenda 02 est une E600 complète, donc il remplace E600 rév. 1. `prepare.py` avait appelé « E600 » le fichier E000 (page titre) et « E600_2 » la vraie E600.
- **Marques** : 909 viennent des étiquettes texte, après suppression des faux positifs (bulles d'axes, « ESC. B », LV d'architecture, doublons). Les 512 autres sont visuelles, dont 37 raccordements tirés des cédules et de l'unifilaire E200. Tous les libellés existent dans `nomenclature.csv` (63 libellés).
- **Ajouts de l'addenda** : 2 bornes VE (BRVE-01 et BRVE-02) et toute la cédule P-P1 (pompes, chauffage, UAT). Les bornes VE n'ont aucun symbole au plan, leur emplacement est à confirmer.
- **Ce qui manque** :
  - pas de `comparaison-estimateur.md`, parce qu'aucun export de M. Dupuis n'était fourni ;
  - E500 (détails communs) est une feuille vide ;
  - les modules Mi/Cx, batteries et résistances de fin de ligne ne sont pas comptés ;
  - quelques symboles hors légende sont relevés « à classer » ;
  - des doublons sont possibles (carrés pleins DDFT contre évier électrique, SPP-1 contre SPS-1) ;
  - les cédules PS-2 à PS-4 n'ont été relues que pour les départs vers des équipements.
- **Outils** : deux commandes ont été refusées par la politique d'outils (un script Python et un `sed`). Je les ai refaites autrement, sans perte de relevé, et c'est noté en R-024.

STATUT : À VÉRIFIER

Fichiers dans `/home/claude/releve-auto/runs/S-1857/OUTBOX/S-1857/travail/` :
- feuilles-classement.csv
- nomenclature.csv
- occurrences-texte.csv
- occurrences-visuel.csv
- reserves.md
- rapport-releve.md

## reserves.md

# Réserves — S-1857 Maison communautaire Saint-Michel (relevé du 2026-09-22)

R-001 · E600 / E600_2 / E600_ADD · Arbitrage des feuilles E600 — `prepare.py` a nommé « E600 » le fichier E000_Rev0.pdf (page titre, rien à relever) et « E600_2 » la vraie E600 rév. 1 (SOUMISSION 2026-08-17). L'addenda 02 (ADME-01, 2026-09-11, scan) est une E600 **complète** (PS-1 à PS-5 + P-P1). Décision : l'addenda prime ; E600_2 classée `remplacee`.

R-002 · E500 · La feuille « DÉTAILS COMMUNS » ne contient aucun détail dessiné (cartouche seulement). Aucun article relevé. Faut-il des détails d'un autre lot ?

R-003 · E150 · Les 5 étiquettes DMW1 d'IMPLANTATION (1:100) sont les mêmes luminaires muraux que ceux des plans d'étage. Relevés sur E401/E403 seulement, E150 écartée pour éviter le double comptage.

R-004 · E600_ADD vs E600_2 · Comparaison des deux versions : la rév. 1 n'avait **pas** de cédule P-P1, et les charges changent partout (ex. PS-1 = 171 408 W dans l'addenda). Ajouts de l'addenda relevés comme raccordements : **BRVE-01 et BRVE-02 (bornes VE 50 A, PS-5)**, P-P1 au complet (PC-1 à PC-6, PREF-1 à PREF-4, SPS-1, SE-2, UAT-1, chauffage ESC.A / S-07 / ESC.B / SAS00 / S-03). Le scan est lisible, mais l'ABV et la description de chaque circuit de PS-2 à PS-4 n'ont pas été relus un à un. Seuls les départs « Q » sans symbole au plan ont été relevés (VC, évier électrique, sécheuse, UAT-2). Les bornes VE n'ont **aucun symbole au plan** : leur emplacement est à confirmer.

R-005 · E401 · Deux anneaux orange suspendus sans étiquette (ACCUEIL, ~557,813 et ~715,813), hors du tableau des luminaires. Relevés sous « Luminaire ovale — à classer ». Quel est le type ?

R-006 · E401 · Cercle pointé mural « VERS CME-01 » (~587,1473) sans étiquette. Relevé sous « Luminaire extérieur — à classer ». Trois autres symboles muraux identiques (370,756 / 370,872 / 1170,731) ont été relevés comme DMW1, parce qu'E150 montre 5 DMW1 sur ce niveau. Ce type est à confirmer.

R-007 · E402 · Phare simple sans étiquette PH1 (~1020,1229) : relevé sous « Phare simple — sans étiquette ».

R-008 · E400-E403 · Les enseignes de sortie ne portent ni la face ni le montage. Toutes sont relevées sous « Enseigne de sortie ». Les bulles « X1 » (renvoi de note) ne sont pas comptées comme des appareils.

R-009 · E400-E403 · Les accumulateurs 36W/18W montrés avec une enseigne intégrée (carré + ⊗ + phares) sont relevés sous « Accumulateur … + enseigne ». L'étiquette « 36W » est lue sur le plan, mais le fait que l'enseigne soit intégrée est une interprétation du symbole (légende E104).

R-010 · E403 · Trois cercles bleus barrés avec flèche (620,927 ; 1071,937 ; 1046,1214 ; lettres « 3 », « g ») sont absents de la légende. Relevés sous « Cercle barré fléché — à classer ». Ce sont peut-être des interrupteurs de commande ou des détecteurs.

R-011 · E406 · Au SAS 00 : un cercle vert « TS » et un carré vert pointillé avec ⊗ sont absents de la légende. Relevés sous « … — à classer ». « PMI » est interprété comme poste maître d'intercom (E104).

R-012 · E406/E407/E408 · « SM » (2 par niveau) interprété comme **sèche-main** d'après les cédules « SÈCHE-MAIN (108/208/302) ». Relevé sous « Raccord sèche-main ».

R-013 · E405-E408 · Les prises « carré plein » près des lavabos et des éviers sont relevées comme DDFT. Les cédules ont des circuits « ÉVIER ÉLECTRIQUE » (valve électrique), qui peuvent correspondre à certains de ces symboles. Risque de double comptage avec « Raccord évier électrique » (6 relevés sur cédule).

R-014 · E406 · Les cercles « C » en cuisine (1341,1019 ; 1369,1019) et en Joujouthèque 110 (434,1208) sont relevés comme « Prise cuisinière C ». Ils correspondent aux cédules CUISINIÈRE 4 FEU / 6 FEU (140) et CUISINIÈRE (110). Les 2 « CUISINIÈRE (150) » et le « FOUR COMBINÉ (140) » 250 A de PS-5 n'ont pas de symbole au plan : relevés sur la cédule.

R-015 · E405 · SPP-1 est étiqueté deux fois sur E405 (salle mécanique ~535,1289 et local ~1008,677), alors que la cédule P-P1 n'en compte qu'un. Deux marques sont relevées : l'une des deux est peut-être SPS-1 mal étiquetée. SPS-1 est aussi relevée sur la cédule, d'où un risque de +1.

R-016 · E405/E406 · Un « CC » isolé sans nom d'équipement, hors du bâtiment (~404,1494), apparaît sur les deux feuilles. Compté une fois sur E406 et écarté sur E405. Quel équipement ?

R-017 · E405-E409 · Les klaxons avec ⊗ et candela (15/30) sont relevés comme Klaxon + « Avertisseur visuel ». Le repérage « Ei » n'a été vérifié que sur E408/E409 (3 klaxons Ei). Sur les autres feuilles, un klaxon Ei a pu rester dans « Klaxon ».

R-018 · E201 · L'unifilaire d'alarme (K×103, M, F, Mi) n'a **pas** été recompté : il reprend les appareils des plans. Les modules isolateurs Mi (7 étiquettes sur E201) et les modules Cx n'ont pas de symbole au plan et **ne sont pas comptés**. À ajouter si l'estimateur les chiffre.

R-019 · E102 · Les accessoires du tableau des spécifications sans symbole au plan ne sont pas comptés : batteries 12 VCC (2/panneau), résistances de fin de ligne, clavier GSM, capteur de courant 400 A (E-46, lié aux BRVE), routeur, points d'accès. À chiffrer au forfait ou à confirmer.

R-020 · E400-E403 · Les interrupteurs « $ » ne sont relevés que là où ils sont dessinés (5). L'éclairage est surtout commandé par détecteurs et boutons-poussoirs B.

R-021 · E404 · ACCÈS TOITURE - ÉCLAIRAGE : aucun appareil dessiné. Seules les bulles d'axes « B », « F », etc. ont été lues et elles ont été supprimées.

R-022 · Toutes feuilles · Faux positifs supprimés d'`occurrences-texte.csv` :
- 40 bulles d'axes (B/F en marge) ;
- 2 « B » de « ESC. B » (E402, E407) ;
- 6 « LV » (lave-vaisselle d'architecture) sur les plans d'éclairage E401-E403 ;
- 6 doublons « LV » ou étiquettes « LV » voisines (E406, E407, E408) ;
- 1 « CC » en double (E405).

R-023 · E401/E402/E403 · « DR51/DR52 » et « DR5 » sont relevés séparément, même quand un seul luminaire porte deux étiquettes superposées. Chaque marque a été vérifiée en zoom : une étiquette = un luminaire.

R-024 · Outils · Deux commandes d'édition, une commande Python (commentaire dans le script) et un `sed`, ont été refusées par la politique d'outils. Elles ont été refaites autrement (script sans commentaire, outil Edit). Aucune perte de relevé.

R-025 · Chemins de câbles / linéaires · Aucun profilé ni chemin de câbles n'est dessiné. Rien à métrer.

