# Rapport de relevé — S-1695 Playground Hotel (2024-023, soumission REV1)

## Méthode
1. Classement des 23 pages d'après les cartouches (`feuilles-classement.csv`) : 17 plans, 1 légende (E001), 2 schémas (E300, E804), 2 tableaux (E301, E302), 1 page titre (QC138).
2. Légende E001 lue par zooms → `nomenclature.csv` (luminaires A1…E2, urgence, services, chauffage, télécom, alarme, raccordements mécaniques EV/VT/SE/BC/VE/CD/VM/UAF, adresses AI D/S).
3. `extract_occurrences.py` puis contrôle des faux positifs (MRA/MAT, doublons CD-IT-01, VM, CAM — voir réserves R-014 à R-017).
4. Relevé visuel par zooms sur E200-E202, E210-E212, E213, E400 → `occurrences-visuel.csv`.
5. Pas d'export estimateur : pas de comparaison.

## Totaux
| feuille | texte | visuel | total |
|---|--:|--:|--:|
| E200 éclairage 4e | 221 | 41 | 262 |
| E201 éclairage 5e | 109 | 16 | 125 |
| E202 éclairage 6e | 107 | 22 | 129 |
| E203 éclairage toit atrium | 44 | 0 | 44 |
| E210 services 4e | 76 | 138 | 214 |
| E211 services 5e | 76 | 88 | 164 |
| E212 services 6e | 81 | 82 | 163 |
| E213 services toit | 19 | 15 | 34 |
| E217 électro-méc. 4e | 13 | 0 | 13 |
| E218 électro-méc. 5e | 7 | 0 | 7 |
| E219 électro-méc. 6e | 8 | 0 | 8 |
| E400 chambres types éclairage | 251 | 11 | 262 |
| E401 chambres types services | 118 | 0 | 118 |
| E800 alarme 4e | 68 | 0 | 68 |
| E801 alarme 5e | 51 | 0 | 51 |
| E802 alarme 6e | 57 | 0 | 57 |
| E803 alarme toit | 0 | 0 | 0 (doublons E213) |
| **Total** | **1306** | **413** | **1719** |

## Non relevé / limites
- Multiplicateur des chambres typiques (E400/E401 × nombre de chambres par type) non appliqué (R-002).
- Interrupteurs, détecteurs et télécom des chambres types (R-003, R-004, R-018).
- Longueurs des luminaires linéaires à métrer (R-005) ; contrôles Lutron (R-006) ; éclairage d'urgence hors enseignes (R-007).
- Unifilaire E300, cédules E301/E302 (non vectorielles), matrice E804 (R-020 à R-022).
- Type des dispositifs AI non discriminé (D = entrée, S = signal) (R-017).
- Contrôle d'accès E-214/215/216 non émis (R-024).
- Toutes les étiquettes des deux fichiers d'occurrences existent dans `nomenclature.csv` (vérifié à la main, liste des 20 libellés visuels).
