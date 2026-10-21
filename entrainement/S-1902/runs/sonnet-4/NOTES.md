# NOTES — chiffrage « méthode Dupuis » à l'aveugle, S-1902

**Modèle ayant produit ce travail : Claude Sonnet 5.5** (claude-sonnet-5-5), sans sous-agent, kit seul (aucune lecture hors du dossier).

## Résultat (chiffrage.py → chiffrage.json, code de sortie 0, déterministe)
- 85 lignes; matériel 58 473,25 $ (dont lots 27 343 $); heures relevées 978,19 h → chargées 980 h; MO 980 × 85 = 83 300 $
- Total ACCEO 141 773,25 $; × 1,244 = 176 358 → prix de vente **176 000 $**
- Contrôles : matériel + chargées × taux = total ACCEO; prix = arrondi au millier; part MO 58,8 % (plage 30–69 %); ≈ 556 h / 100 k$ de prix (un peu au-dessus de 450–520).
- Dans `lignes`, `p` = prix unitaire, `h` = heures **unitaires** (total ligne = q × p, q × h). Conduits/fils en pi (m × 3,28084, arrondi au pi supérieur).

## Méthode appliquée
1. Quantités sur plan : `rapport-releve.md` (portées par famille; recoupé avec `releve.xlsx` « Par libellé ») — INSTALLER → pose, ENLEVER → démantèlement, RELOCALISER → relocalisation, CONSERVER → rien. Hors plan et heures de jugement : feuille Détail (Estimation_2), lue par code.
2. Prix/temps : colonnes PRIX À UTILISER / TEMPS À UTILISER du catalogue (jamais la médiane), libellé exact cité dans `src`. Les descriptions du catalogue sont comparées après suppression des espaces de fin.
3. Lots, taux 85 $/h, facteur 1,244 : METHODE.md. Luminaires, enseignes, détecteurs, panneau, disjoncteurs : 0 $ en ligne + lots.
4. `par_article` : `heures` = heures relevées (non arrondies) de l'article; `total` = matériel + heures × taux. La somme des totaux est donc inférieure de (980 − 978,19) × 85 ≈ 154 $ au total ACCEO (arrondi vers le haut des heures chargées non réparti). Lots répartis : éclairage → 3.35; distribution → 3.24 (panneau 3 400 $) + 3.25 (EDB/EJB 2 800 $); JCI → 3.38; détecteurs JCI → 3.36; GPR → 3.32.
- Correspondance Détail → bordereau retenue : 5.19 = démolition (luminaires, prises, équipements enlevés); 3.22 = démontage/relocalisations/retraits temporaires; 3.23 = raccordements mécaniques (+ thermostats); 3.26 = MCC (chaudières sur tiroirs CCM-1); 3.27/3.28/3.30 = prises USB / 15 A / DDFT; 3.31 = percements, conduits, filage, boîtes; 3.32 = scan dalle; 3.33 = sorties data et conduits data; 3.34 = monuments; 3.35 = luminaires, enseignes, interrupteurs; 3.36–3.38 = alarme incendie; 6.1 = frais de chantier. Ce mapping est un jugement (le kit ne le donne pas).

## Hypothèses et décisions principales
- **Taux 85 $/h** (METHODE §5, dossiers août–octobre 2026), malgré le 124 $/h du Sommaire d'Estimation_2 (référence Jo) : METHODE.md prime; « règle de choix à confirmer avec Jo ».
- **Postes/prises : un seul comptage.** Les prises, DDFT, USB et sorties data viennent du relevé (INSTALLER); les lignes composites du Détail (D-01 à D-07, E-01 à E-05) ne sont pas rechargées en plus. Seules les boîtes de jonction/raccords de mobilier hors plan restent (D-01, D-03, E-01, E-04 = « DROP DE PRISE », 25 u) et les boutons d'appel (D-11, E-06).
- Relevé INSTALLER de boîtes de jonction (3) = D-09 (2) + D-10 (1) du Détail.
- Moteurs INSTALLER (4 triphasés + 3 monophasés = 7) = UTA + VE-02N + 2 chaudières + 3 humidificateurs (C-01 à C-04) : UTA 1 h, moteur 0,75 h (METHODE §3). Sectionneurs 30 A des humidificateurs (C-04b) : prix Lumen 117,84 $ (prix catalogue = 0 $) + temps catalogue 2 h.
- Conduits : assemblages du catalogue (« CONDUIT VIDE 1 », « CONDUIT VIDE 3/4 », « CONDUIT 3/4 03C12 » = 4,2441 $/pi, 0,1128 h/pi) avec longueurs d'hypothèse du Détail; fils #12/#8 séparés. Le catalogue n'a pas de colonnes TEMPSEC/sections de 10 pi : temps au pi seulement. F-09 (3 #12) est inclus dans F-08 (assemblage 03C12).
- Scan dalle : ligne « SCAN DALLE BETON » à 0 $ (2 h) car le prix 1 250 $ est déjà le lot GPR (METHODE §2) — pour ne pas le compter deux fois.
- Panneau PP-3 : 8 h (METHODE §3) sur « PANNEAU 100A 347/600V 3F » (0 $, 8 h); le Détail comptait 24 h (inclut démontage de l'ancien et transfert des charges) — non retenu.
- Disjoncteurs : 1P 0,2 h, 3P 1 h (METHODE §3), prix 0 $ (dans le lot distribution). Quantités du Détail : 19 × 1P (le lot en prévoit 20) et 3 × 3P.
- Frais de chantier : H-01 remplacé par « NACELLE » 1 250 $ / 16 h (METHODE §3); H-02, H-03, H-04 gardés en jugement (Détail).
- Jugements d'heures repris du Détail sans changement : A-07, A-10 (4 h × 6 moteurs relocalisés), A-11, B-09, D-09, D-10, D-11b/E-06, D-16, E-11, F-05, G-05, G-06, H-02 à H-04.

## Lignes où j'ai hésité
- **Luminaire enlevé (A-01, 40 u)** : METHODE §3 dit 0,5 h mais aucun libellé du catalogue n'a 0,5 h (« ENLEVER FIXTURE ENCAST/2X2/1X4 » = 0,35 h, « FIXTURE ENCASTRE ENLEV » 0,25 h, Détail A-01 0,35 h). J'ai retenu 0,5 h (METHODE); écart si 0,35 h : −6 h. Quantité 40 = ENCASTRE 26 + LED 1X4 6 + LED 2X2 8 (le Détail compte 39 + 7 = 46; A-02 fusionné dans A-01, de même A-04 dans A-03).
- **Luminaire E** : 3 (relevé, lot ×3) contre 4 (Détail/relevé d'éclairage); retenu 3.
- **C1_1 et C1_3** : pas de libellé catalogue; « FIXTURE TYPE C1 » (0,75 h) comme « luminaire 0,75 h » de METHODE (le Détail jugeait 0,5 h / 0,6 h).
- **Lot éclairage** : METHODE donne 11 893 $, mais la somme de ses composantes (11×185 + 12×290 + 15×230 + 6×110 + 1 500 + 3×475 + 3×161,60) fait 13 034,80 $. J'ai retenu le total confirmé 11 893 $.
- **Sorties data** : 10 avec conduit 3/4" (D-08, « TEL/DATA 3/4 » 22,32 $ / 0,89 h) et 55 simples (« TEL/DATA » 13,96 $ / 0,63 h) = 65 INSTALLER; le partage 10/55 est un jugement.
- **PRISE DOUBLE 15A** : le relevé ne distingue pas 15 A et 20 A; tout en « PRISE DUPLEX 15A 120V ». DDFT et MALT isolée non départagées : tout en « PRISE DUPLEX 20A 125V GFI » (65,38 $ / 1,3 h); aucune ligne 3.29.
- **Relocalisation d'annonciateur** : « RELO PANN ANNOCIATEUR » (0 $, 8 h) plutôt que « RELO PANNEAU ANNONCIATEUR » (550 $, 8 h, plus récent) — panneaux à 0 $ en ligne.
- **A-08 / A-09 (FabLab, retrait + réinstallation)** : libellé voisin « RELO ENCASTRE » (1 h) au lieu des 0,5–0,6 h du Détail.
- **Percements** : 150 $ / 1 h (PERCEMENT PLANCHER) sans ligne coupe-feu en plus (supposé inclus), 23 percements = D-12 (16) + E-07 (7).
- **Boîtes de tirage 4-11/16"**, couvercles et corde de tirage : prix Lumen, temps par jugement (compris dans D-16/E-11 du Détail), quantités 2 par course (32 + 14).

## Introuvable dans le catalogue (ou prix 0 $)
- « LUMINAIRE ENLEVE » (0,5 h), « FIXTURE TYPE C1_1 / C1_3 », sectionneur 30 A (prix 0 $) → voir ci-dessus; boîte de tirage 4-11/16", couvercle plat 4-11/16", corde de tirage → Lumen.
- Non chiffrés volontairement : coupe-feu en tube, tiges filetées/ancrages de suspension et marrettes (Lumen; supposés dans les trousses du lot éclairage et les assemblages), câble TECK et connecteurs TECK des chaudières (câbles existants réutilisés), flexibles étanches des moteurs (compris dans le prix 25 $ du libellé MOTEUR), câblage data Cat6 (OPT-1), parasismique (OPT-2), hors-heures (OPT-3), postes temporaires (OPT-4).
- Éléments CONSERVER du relevé (gâches, lecteurs existants, sorties TV, stations manuelles, thermostats existants, luminaires existants, encastrés d'urgence) : aucun coût. Si le relevé automatique (« à VÉRIFIER ») change des portées, les quantités suivent en relançant chiffrage.py.
