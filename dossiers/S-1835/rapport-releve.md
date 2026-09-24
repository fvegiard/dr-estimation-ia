# Rapport de relevé — S-1835 (ESBG, réhabilitation, démolition phase 1)

## Méthode
1. J'ai classé les 31 feuilles (`feuilles-classement.csv`) et lu le texte de l'addenda E-01 (D210_ADD_2). Les 8 feuilles d'addenda remplacent E-002 et E-D210 à E-D222.
2. J'ai lu la légende E-001 (abréviations EC / EAR / EE…) et les notes générales et spécifiques des feuilles d'addenda et de T-D4xx.
3. Relevé des symboles par lecture des calques CAO du PDF d'addenda : masque WIPEOUT + calque E-D-* ou E-E-*. Le type d'appareil est donné par la taille du masque. Des zooms de contrôle ont été faits sur D210_ADD. Les haut-parleurs télécom ont été relevés par leur signature vectorielle (disque noir).
4. Les étiquettes EAC ont été relevées par `extract_occurrences.py`.

## Totaux
- Occurrences texte : 54 (Repère EAC).
- Occurrences visuelles : 3254.

| libellé | qté |
|---|--:|
| Dém. luminaire 1x4 / segment linéaire | 1888 |
| Dém. luminaire 2x4 | 554 |
| Luminaire 24h existant — dépose/repose temp. | 218 |
| Détecteur fumée existant — dépose/repose temp. | 192 |
| Haut-parleur existant — dépose/entreposage | 152 |
| Dém. luminaire rond encastré | 85 |
| Éclairage existant carré — à classer | 55 |
| Station manuelle existante (F) — à confirmer | 32 |
| Dém. éclairage — à classer | 27 |
| Détecteur sécurité (M) — par autres | 13 |
| Dém. prise plafond projecteur | 13 |
| Dém. luminaire 2x2 | 6 |
| autres à classer / par autres | 19 |

Détail par feuille : les coordonnées de marques livrées sont dans `releve.xlsx`, onglet `Marques`. D221_ADD est la feuille la plus chargée (1x4 : 459).

## Limites
- Il n'y a pas de parcours visuel exhaustif : le relevé dépend des calques CAO. Voir R-003 et R-013.
- Les notes 2, 4 et 7 ne sont pas ventilées. Voir R-005 et R-008.
- Le sous-sol télécom (D400-D403) compte 0 haut-parleur, à vérifier.
- J'ai utilisé des scripts pymupdf ad hoc (`uv run python`, lecture seule du PDF de l'INBOX) en plus des outils `releve/`.
