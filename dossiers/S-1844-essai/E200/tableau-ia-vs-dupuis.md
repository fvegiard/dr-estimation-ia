# S-1844 E200 — IA vs Dupuis (comparé APRÈS le commit 1ab6c02)

Source Dupuis : `S-1844 (17-Août-2026).qpl` (Drive, SHA256 0273D1DF57716680E9D0B71242D937A16EDFC3FA32EFB0DD72CCA7DEF0C2A4D4, identique à dossiers/S-1844/reference/S-1844-Dupuis-PlanExpert.qpl).

**Constat : le qpl de M. Dupuis ne contient AUCUN repère sur la feuille E200 (page 8 du PDF « 26-0108-02_ELECTRICITE_POUR SOUMISSION », 0 marque).** Seule la page 6 de ce PDF (E103, contrôle d'éclairage) porte des marques (23). Les prises de M. Dupuis sont relevées sur le jeu d'architecte « 23347_SELECTION_GLOBAL_SOUM » page 5 (plan 26-347-07A « Plan électrique et mécanique », 57 marques), autre dessin, autre raster : la comparaison est par famille seulement, pas par position.

| Famille | IA (E200, 62) | Dupuis (GLOBAL_SOUM p.5, 57) | Note |
|---|---|---|---|
| Prises courant (PD 17 + PH 15 + TL 1) | 33 | 23 « prise » + 14 « prise contrôlée » = 37 | écart −4 ; Dupuis sépare les prises contrôlées |
| Data / télécom (BX 4 + TRI 7 + BC 1) | 12 | 10 « INFORMATIQUE » | écart +2 |
| Mobilier / monument plancher | non relevé (BX 24" = raccordement mobilier, compté en télécom) | 7 « MONUMENT PLANCHER D » | à rapprocher des BX 24" |
| Séchoirs | 0 | 2 | non identifiés par l'IA |
| Chauffage / mécanique (T 5, R 4, SE 2, SM 1, MOT 2, HQ 1, BH 1, VAV 1) | 17 | 1 « SN » | Dupuis ne compte pas ces raccordements sur ce plan |
| Conduits | non comptés | PVC 1po 21 segments, conduit 3/4 6, conduit 2 3 | l'IA n'a pas relevé de longueurs |

Total repères : IA 62 / Dupuis 57 (jeux de plans différents ; ne pas conclure à une précision).
