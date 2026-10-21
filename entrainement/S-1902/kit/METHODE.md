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
   Lots confirmés pour S-1902 (entrées, prix confirmés par Francis le 2026-10-20) : lot éclairage 11 893 $ (A1 ×11 à 185 $, Axis SL1 4′ ×12 à 290 $, 3′ ×15 à 230 $, 1′ ×6 à 110 $, trousses 1 500 $, E ×3 à 475 $,
   Z6 ×3 à 161,60 $), lot distribution 6 200 $ (NF 225 A 42 cct 3 400 $ + EDB 1P 95 $ ×20 + EJB 3P 300 $ ×3), JCI 7 400 $ + 2 détecteurs 600 $,
   GPR 1 250 $ — **prix confirmés par Francis le 2026-10-20**.
3. **Heures** = Σ quantité × *temps unitaire* Dupuis (prise 1,175 h ; USB 1,125 h ; DDFT 1,3 h ; tel/data 0,63–0,89 h ; luminaire 0,75 h ;
   enseigne 1 h ; tête 0,5 h ; détecteur 0,5 h ; panneau 8 h ; disjoncteur 1P 0,2 h / 3P 1 h ; percement 1 h ; luminaire enlevé 0,5 h ;
   prise enlevée 0,35 h ; relocalisation de prise 1,5 h ; conduit 3/4 03c12 0,113 h/pi ; conduit vide 3/4 0,056 h/pi ; moteur 0,75 h ; UTA 1 h ;
   annonciateur relocalisé 8 h ; nacelle 1 250 $ / 16 h). **Toujours la colonne « À UTILISER » (dernier Dupuis), jamais la médiane**. Formule ACCEO pour les conduits : QTE × TEMPUNI + sections de 10 pi × TEMPSEC.
4. **Heures chargées** = heures relevées arrondies **vers le haut** au multiple de 10 (S-1881 : 4 128,6 → 4 150 ; S-1854 : 5 872,6 → 5 880).
5. **Main-d'œuvre** = heures chargées × **taux** : 85 $/h sur ses dossiers d'août–octobre 2026 (S-1797, S-1835, S-1854, S-1881 ; 99 $/h sur
   S-1857 ; 110 $/h Canderel centre-ville ; 78–82 $/h en hiver-printemps). Règle de choix à confirmer avec Jo.
6. **Total sommaire ACCEO** = matériel + main-d'œuvre. Contrôle : part MO 30–69 % (médiane ≈ 45 %), 450–520 h par 100 k$ de prix.
7. **Prix de vente** = total ACCEO × **1,244** — unique couple observé : S-1844, sommaire 191 909,19 $ → prix remis 238 744 $
   (courriel Dupuis 2026-08-26 ; versions Jo 253 600 / 259 000 $ = ×1,32–1,35). Arrondi au millier. Facteur modifiable dans le classeur.


