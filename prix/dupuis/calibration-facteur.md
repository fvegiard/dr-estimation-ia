# Calibration du facteur « sommaire ACCEO → prix remis » (Daniel Dupuis)

Généré par `entrainement/calibrer_facteur.py` depuis `prix/dupuis/couples-sommaire-prix-remis.csv`. Le facteur en vigueur reste
celui de `parametres.json` (1.244) tant que Jo n'en décide pas autrement.

| Dossier | Date | Sommaire ACCEO ($) | Prix remis ($) | Ratio | Plus bas ($) | Dupuis vs plus bas | Gagnant | Source | À vérifier |
|---|---|---|---|---|---|---|---|---|---|
| S-1844 | 2026-08-26 | 191 909.19 | 238 744 | 1.244 | — | — | — | sommaire : dossiers/S-1844/reference-quantites.csv (p.1 du take-off scanné) ; prix remis : eewin/soumissions-dr/S-1844/Soumission_S-1844_LC2000_SAQ_.pdf.txt (PDF DR du 25 août 2026, courriel Dupuis 2026-08-26) |  |
| S-1753 | 2026-05-08 | 180 638.85 | 198 000 | 1.096 | — | — | — | sommaire Dupuis 2026-05-05 (catalogue, onglet Paramètres Jo) ; prix remis 198 000 $ : Drive « Soumission_S-1753_Norgereq.pdf » (lettre DR du 8 mai 2026 signée Jonathan Parent, École Assomption, plans E-000…E-104 + addenda ME-01) ; même portée que le sommaire à confirmer | oui |
| S-1693 | 2026-03-27 | 1 231 798.52 | 1 522 070 | 1.236 | — | — | — | sommaire : dossiers/S-1693/reference-quantites.csv ; prix = montant APPROXIMATIF de la demande de cautionnement (Drive « demande cautionnement beloeil.pdf » : 1 750 000 $ taxes incluses, ouverture 2026-03-27) ramené hors taxes ÷ 1,14975 ; le prix réellement remis reste à lire sur la formule BSDQ | oui |
| S-1763 | 2026-05-12 | 59 887.15 | — | — | — | — | — | sommaire Dupuis 2026-05-18 (catalogue, Paramètres Jo) ; lettres DR : 39 250 $ (partie 1, 8 mai, « Soumission_S-1763_QMD.pdf ») et 85 800 $ (parties 1+2 avec conteneur 600 A, 12 mai, « _r1.pdf ») ; portée du sommaire inconnue, inutilisable tel quel | oui |
| S-1775 | 2026-06-03 | 428 310.26 | — | — | — | — | — | sommaire Dupuis 2026-06-03 (catalogue, Paramètres Jo) ; Drive « FORMULE DE SOUMISSION BSDQ.pdf » (dossier s-1775 clinique mieux etre, 2026-06-03) est un scan sans texte : montant à lire à l'écran | oui |
| S-1835 | 2026-08-26 | 88 315.00 | — | — | — | — | — | sommaire v2 : dossiers/S-1835/reference-quantites.csv ; manuscrits 70 000 / 75 000 / 80 000 / 89 777 $ « prix CL 50 » sur le sommaire, prix remis non confirmé | oui |

## Facteur

Un seul couple confirmé (ratio 1.244) : écart-type indéfini, le facteur n'est pas calibré, il est posé. Il faut au moins 5 dossiers remis par Daniel avec leur sommaire ACCEO pour parler de calibration.

En comptant les 2 couples « à vérifier » (3 au total) : ratio moyen 1.192, écart-type 0.083, min 1.096, max 1.244. Lecture : le facteur n'est pas une constante de Dupuis ; il varie d'un dossier à l'autre de 7 % (±12 954 $ sur 155 899 $). Ces couples doivent être confirmés (même portée, auteur du prix) avant de changer parametres.json.

Sensibilité sur un sommaire de 155 899 $ :

| Facteur | Prix de vente ($) | vs facteur actuel |
|---|---|---|
| 1.192 | 186 000 | -4.2 % |
| 1.200 | 187 000 | -3.5 % |
| 1.244 | 194 000 | +0.0 % |
| 1.300 | 203 000 | +4.5 % |
| 1.350 | 210 000 | +8.5 % |

## Prix remis à retrouver (un sommaire ACCEO existe, le prix remis manque)

- S-1763 (sommaire 59 887.15 $) : sommaire Dupuis 2026-05-18 (catalogue, Paramètres Jo) ; lettres DR : 39 250 $ (partie 1, 8 mai, « Soumission_S-1763_QMD.pdf ») et 85 800 $ (parties 1+2 avec conteneur 600 A, 12 mai, « _r1.pdf ») ; portée du sommaire inconnue, inutilisable tel quel
- S-1775 (sommaire 428 310.26 $) : sommaire Dupuis 2026-06-03 (catalogue, Paramètres Jo) ; Drive « FORMULE DE SOUMISSION BSDQ.pdf » (dossier s-1775 clinique mieux etre, 2026-06-03) est un scan sans texte : montant à lire à l'écran
- S-1835 (sommaire 88 315.00 $) : sommaire v2 : dossiers/S-1835/reference-quantites.csv ; manuscrits 70 000 / 75 000 / 80 000 / 89 777 $ « prix CL 50 » sur le sommaire, prix remis non confirmé

Avec ces 3 prix, le facteur reposerait sur 4 couples au lieu de 1.

## Position par rapport au plus bas soumissionnaire

Aucun résultat d'ouverture avec le prix du plus bas soumissionnaire dans le fichier.
