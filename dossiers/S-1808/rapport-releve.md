# Rapport de relevé — S-1808 CPE Les Copains d'Abord (projet de remplacement)

Il s'agit de l'électricité, dossier HF 25-64, émission « Pour soumission REV01 » du 2026-06-23, plus l'addenda ME-01 (M-606).
Relevé par l'agent le 2026-09-22. Aucun export d'estimateur n'a été fourni, donc il n'y a pas de comparaison (R-001).

## Méthode
1. Les 22 pages ont été classées d'après l'aperçu et le cartouche (`feuilles-classement.csv`).
   - Pages `plan` : E050, E051, E052, E100, E101, E200, E201 et E202.
   - Les numéros réels sont notés dans la colonne `note`. L'index E-001 numérote E-100/E-101 comme E-200/E-201 (R-002).
2. La nomenclature (`nomenclature.csv`, 94 labels) vient de :
   - la légende E-001 (alarme, services, éclairage, interrupteurs, chauffage) ;
   - les tableaux E-032 (types A–F, EX1–EX3, Z1–Z6, SCR / OWC-M / OAC / OFM) et E-031 (équipements mécaniques) ;
   - les notes des plans et les schémas E-010 / E-020.
3. Occurrences par étiquette : `extract_occurrences.py` a donné 257 lignes. On a retiré 1 faux positif, le mot « TIRAGE » d'une note sur E050.
   - On a ensuite ajouté à la main des lignes lues dans `texte/<F>-mots.csv` :
     - les paires `TYPE` + lettre des luminaires (la regex ne lit qu'un mot) ;
     - les `D` de détecteurs, en excluant les bulles d'axes et `TYPE D` ;
     - les `F`, classés station ou piézo-strobe après zoom ;
     - les `T` avec ou sans FPD, les noms de panneaux, TX1, 400A et C2.
   - Contrôles faits : les bulles d'axes A…F / B / C / D / E sont exclues ; `(a)`, `(b)`, `E.I` et les circuits PSx sont traités comme des qualificatifs, pas comme des appareils.
4. Relevé visuel (`occurrences-visuel.csv`) :
   - 12 zooms d'environ 420 × 360 pt sur chaque plan d'étage E100, E101, E200 et E201, plus E202 et des zooms ciblés ;
   - interrupteurs, détecteurs, prises, sorties informatiques, bulles de notes et sectionneurs ;
   - schémas E010 / E020, cédule E004 et détails E040 / E041 pour ce qui n'a pas de symbole en plan.
5. Addenda : M-606 (plomberie), sans incidence électrique (R-003).
6. Le recoupement plan ↔ cédules ↔ schémas est détaillé en R-018, R-019, R-028 et R-029. Les doublons écartés sont l'ascenseur sur E200 et la hotte sur E020.

## Totaux par feuille (826 marques)
| feuille | marques | détail principal |
|---|--:|---|
| E100 RDC écl. + alarme | 216 | A 55 · B 4 · C 15 · D 2 · E 6 · F 1 · EX1 8 · Z 25 · RE 15 · dét. BV 21 · interrupteurs BV 18 (13 grad. + 5) · int. simple 2 · dét.-grad. 4 · K 7 · F 5 (3 strobes + 2 stations) · thermiques 17 · fumée 4 · CO 1 · RA 4 · PAI 1 · hotte 1 |
| E101 étage écl. + alarme | 241 | A 74 · C 18 · D 14 · E 6 · F 1 · Z 22 · RE 18 · dét. BV 22 · interrupteurs BV 22 (17 grad. + 5) · gradateurs 8 · dét.-grad. 4 · K 9 · F 3 · thermiques 12 · fumée 3 · CO 1 · volets 4 |
| E200 RDC services | 161 | prises : double 47, comptoir 4, comptoir DDFT 6, DDFT 3, ext. E.I 8, spéciales 2 · info 5 · SCR 12 · OFM 6 · OAC 2 · OWC-M 2 · RT 17 · TI 3 · T plancher 2 · T FPD 11 · AC 11 (+1 à confirmer) · VE 3 · EVP · VA-01 · SE-01 · P-01 · four combi · PSS1 · PCUI · C2 · 400 A · HQ · tirage · contrôle d'accès 4 · colonne îlot |
| E201 étage services | 133 | prises : double 40, comptoir DDFT 9, comptoir 2 · info 1 · SCR 18 · OFM 3 · RT 16 · TI 5 · T FPD 9 · AC 9 · HUM 2 · ECH 2 · SE 3 · CE-01 · P-02 · VE-05 + démarreur combiné · PS · PSS2 · TX1 · ascenseur (pompe, contrôleur, sectionneur lum.) · contrôle d'accès 4 |
| E202 toit | 9 | COND 3 · VE-01 · sectionneurs E.I 3 · prise service 1 (+1 à confirmer) |
| E051 / E052 élévations | 12 / 8 | EX2 11 + EX3 1 / EX2 7 + EX3 1 |
| E020 schéma alarme | 30 | MI 18 · RFL 3 · détecteurs de gaine 3 · MTA · ANN · GSM · « I » 2 et symbole de puits 1 à classer |
| E010 unifilaire | 9 | C1, minuterie, sélecteur, barre MALT, 2 liaisons MALT, contreplaqué, 2 conduits vides |
| E004 cédules | 3 | cuisinière, 2 boîtes de dérivation VRF |
| E041 / E040 / E050 | 2 / 1 / 1 | SF VA-01, démarreur hotte (fourni par autres) / interrupteur lumière de puits / point de raccordement HQ |

Totaux projet par famille : luminaires 224 · secours 47 · commandes (RE, détecteurs, interrupteurs, etc.) 137 · alarme 102 · prises 123 · télécom 17 · chauffage 86 · mécanique (raccordements et FPD) 69 · distribution 21. Somme : 826.

## Non relevé, limites
- **Linéaires non métrés** : artères, câble chauffant, conduits (R-024).
- **Pages sans quantité** : E002, E003, E005, E030 et E042. E004 et E032 sont des rasters lus à basse résolution (R-019, R-026).
- **Distinctions incertaines** : prises 15 A / 20 A (R-008), variantes d'interrupteurs B.V. (R-004, R-005), MI au panneau (R-016).
- **Addenda ME-01** peut-être incomplet (R-003).
- **Vérification finale** : les 94 labels des deux fichiers d'occurrences existent tous dans `nomenclature.csv` (contrôle `cut -f2 | sort -u`).
- **Réserves** : 33 (R-001 à R-033).
