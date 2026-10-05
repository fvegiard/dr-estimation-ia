# S-1897 BR Sorel — A-801 — preuves (2026-10-05)

Pipeline officiel, sans annotate.py : `prepare.py` → relevé par la session (compétence releve-planexpert, route
« session tient lieu d'agent », aucun agent imbriqué) → `extract_occurrences.py` → `controle_qualite.py` →
`build_qpl.py` → `render_vectoriel.py` → `render_pdf.py` → `outils/assembler_dossier.py`.
Modèle de la session : claude-opus-5-5 (identifiant configuré de la session Cowork).

| Contrôle | Résultat |
|---|---|
| controle_qualite (Q1-Q10) | conforme=True, 0 erreur, 66 occurrences, 0/66 coordonnée sur grille 5 pt |
| build_qpl | 1 plan, 14 compteurs, 66 marques — sha256 bc6adb1b…741f |
| render_vectoriel | v6 format agrege (comme E03/E04/E05 de l'EXEMPLE) : 2 pages (plan + bordereau 1 p.), codes AF/C3/CI/CT/CU/EV/LD/LE/LM/LS/PC/PL/RA/TH, 66 repères / 14 familles / RES 66, encadré dans l'espace libre |
| pytest (WSL Ubuntu-26.04, POSIX) | 163 passed |
| pytest (Windows pwsh) | 162 passed, 1 failed : test_tool_guard_refuses_disguised_windows_traversal_on_posix (test POSIX, échoue seulement sous Windows ; aucun code modifié) |
| jeu_reference | aucune régression (S-1714/1715/1769/1811/1844 Δ 0,0) |
| verify_exemple (gold EXEMPLE.pdf sha256 0861bc3a…) | 87/87 pages, 2177 repères (max 0,001 pt), 8196/8196 cellules → OK |
| Contrôle visuel JPEG (controle/) | passage 1 : 64/66 (M10-01 prise comptoir 8 pt sous le symbole ; encastré escalier haut 13 pt) → corrigés → passage 2 : 66/66 |

Limites :
- Pas de relevé d'estimateur pour S-1897 : vérification « pas pire que l'estimateur » incomplète.
- `from_releve` lit la colonne `reserve` comme booléen et n'offre pas de drapeau `*` pour une marque visuelle :
  les 3 identifications à revalider (R-002/R-003/R-004) sont dans `note`, `reserves.md` et le bordereau, pas en `*` sur l'étiquette.
- Nom de feuille rendu « A801 » (le moteur retire le tiret du cartouche A-801).
- Porte de prévention (SKILL §5e) : légende, familles et zooms ambigus publiés dans le rapport au lieu d'attendre « VALIDÉ » (consigne de Francis : livrer).

- v6 (2026-10-05) : comparaison aux images de Francis (E03/E04/E05/E11/E14 = logements types en format agrege) -> feuille reclassée bordereau=agrege ; contrôle visuel 66/66.

