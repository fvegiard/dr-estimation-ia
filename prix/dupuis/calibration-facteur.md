# Calibration du facteur « sommaire ACCEO → prix remis » (Daniel Dupuis)

Généré par `entrainement/calibrer_facteur.py` depuis `prix/dupuis/couples-sommaire-prix-remis.csv`. Le facteur en vigueur reste
celui de `parametres.json` (1.244) tant que Jo n'en décide pas autrement.

| Dossier | Date | Sommaire ACCEO ($) | Prix remis ($) | Ratio | Plus bas ($) | Dupuis vs plus bas | Gagnant | Source | À vérifier |
|---|---|---|---|---|---|---|---|---|---|
| S-1844 | 2026-08-26 | 191 909.19 | 238 744 | 1.244 | — | — | — | sommaire : dossiers/S-1844/reference-quantites.csv (p.1 du take-off scanné) ; prix remis : eewin/soumissions-dr/S-1844/Soumission_S-1844_LC2000_SAQ_.pdf.txt (PDF DR du 25 août 2026, courriel Dupuis 2026-08-26) |  |
| S-1753 | 2026-05-05 | 180 638.85 | — | — | — | — | — | sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à lire dans Drive « Soumission_S-1753_Norgereq.pdf » (inventaire Drive 2026-09-23) | oui |
| S-1763 | 2026-05-18 | 59 887.15 | — | — | — | — | — | sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à lire dans Drive « Soumission_S-1763_QMD.pdf » / « _r1.pdf » (inventaire Drive 2026-09-23) | oui |
| S-1693 | 2026-03-31 | 1 231 798.52 | — | — | — | — | — | sommaire : dossiers/S-1693/reference-quantites.csv ; prix remis à lire dans Drive « BORDEREAU SOUMISSION ELECTRICITÉ.pdf » / « formule de soumission du bsdq.pdf » (inventaire Drive 2026-09-23) | oui |
| S-1775 | 2026-06-03 | 428 310.26 | — | — | — | — | — | sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à vérifier dans Drive « Electricité_Soumission_2026 04 03.pdf » (auteur à confirmer) | oui |
| S-1835 | 2026-08-26 | 88 315.00 | — | — | — | — | — | sommaire v2 : dossiers/S-1835/reference-quantites.csv ; manuscrits 70 000 / 75 000 / 80 000 / 89 777 $ « prix CL 50 » sur le sommaire, prix remis non confirmé | oui |

## Facteur

Un seul couple exploitable (ratio 1.244) : écart-type indéfini, le facteur n'est pas calibré, il est posé. Il faut au moins 5 dossiers remis par Daniel avec leur sommaire ACCEO pour parler de calibration.

Sensibilité sur un sommaire de 155 899 $ :

| Facteur | Prix de vente ($) | vs facteur actuel |
|---|---|---|
| 1.200 | 187 000 | -3.5 % |
| 1.244 | 194 000 | +0.0 % |
| 1.300 | 203 000 | +4.5 % |
| 1.350 | 210 000 | +8.5 % |

## Prix remis à retrouver (un sommaire ACCEO existe, le prix remis manque)

- S-1753 (sommaire 180 638.85 $) : sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à lire dans Drive « Soumission_S-1753_Norgereq.pdf » (inventaire Drive 2026-09-23)
- S-1763 (sommaire 59 887.15 $) : sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à lire dans Drive « Soumission_S-1763_QMD.pdf » / « _r1.pdf » (inventaire Drive 2026-09-23)
- S-1693 (sommaire 1 231 798.52 $) : sommaire : dossiers/S-1693/reference-quantites.csv ; prix remis à lire dans Drive « BORDEREAU SOUMISSION ELECTRICITÉ.pdf » / « formule de soumission du bsdq.pdf » (inventaire Drive 2026-09-23)
- S-1775 (sommaire 428 310.26 $) : sommaire : catalogue Dupuis, onglet Paramètres Jo ; prix remis à vérifier dans Drive « Electricité_Soumission_2026 04 03.pdf » (auteur à confirmer)
- S-1835 (sommaire 88 315.00 $) : sommaire v2 : dossiers/S-1835/reference-quantites.csv ; manuscrits 70 000 / 75 000 / 80 000 / 89 777 $ « prix CL 50 » sur le sommaire, prix remis non confirmé

Avec ces 5 prix, le facteur reposerait sur 6 couples au lieu de 1.

## Position par rapport au plus bas soumissionnaire

Aucun résultat d'ouverture avec le prix du plus bas soumissionnaire dans le fichier.
