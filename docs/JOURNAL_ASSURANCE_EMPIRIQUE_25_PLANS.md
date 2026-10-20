# JOURNAL D'ASSURANCE EMPIRIQUE - CAMPAGNE 25 PLANS (DR ÉLECTRIQUE INC.)

**Responsable de l'audit** : Léna AI / Francis Végiard  
**Dernière mise à jour** : 2026-10-20T05:18:00-04:00  
**Taux MO de référence** : 124,00 $/h  
**Validation globale de non-régression** : 375 tests pytest exécutés et passés (100% SUCCÈS, 0 échec).  
**Objectif** : Validation empirique de bout en bout sur 25 planches électriques réelles isolées, contrôle visuel des pastilles, encadré bordereau dans l'espace libre et synchronisation BOM/QPL.

---

## 1. Tableau de Suivi en Temps Réel

| ID Cas | Projet | Feuille / Discipline | Repères Détectés | Score Visuel | Encadré Espace Libre | Statut MCP | Preuves & Livrables |
|---|---|---|:---:|:---:|:---:|:---:|---|
| **P01** | BOURASSA | E-002 (Légende & Normes) | 0 (texte/cartouche) | Conforme | Conforme | **SUCCÈS (0 err)** | preuves/P01-BOURASSA-E-002.json (110s) |
| **P02** | BOURASSA | E-101 (Éclairage RDC) | 5 repères | 4/5 | Conforme (ox_in_free_space: true) | **SUCCÈS (0 err)** | preuves/P02-BOURASSA-E-101.json (195s) |
| **P03** | BOURASSA | E-102 (Éclairage Étage) | 4 repères | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (217s) |
| **P04** | BOURASSA | E-103 (Éclairage Toit) | 2 repères | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (225s) |
| **P05** | BOURASSA | E-104 (Détails Éclairage) | 2 repères (1 EU, 1 PC) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (144s) |
| **P06** | BOURASSA | E-105 (Tableaux Éclairage) | 6 repères (2 DF, 4 SM) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (139s) |
| **P07** | BOURASSA | E-151 (Alarme Incendie RDC) | 6 repères (2 SM, 3 EU, 1 PC) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (126s) |
| **P08** | BOURASSA | E-152 (Alarme Incendie Étage) | 3 repères (2 SM, 1 L4) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (128s) |
| **P09** | BOURASSA | E-153 (Réseau Incendie) | 1 repère | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (225s) |
| **P10** | BOURASSA | E-201 (Distribution RDC) | Signatures brutes (368) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures générées (127s) |
| **P11** | BOURASSA | E-202 (Distribution Étage) | 5 repères (1 L4, 4 G) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (213s) |
| **P12** | BOURASSA | E-203 (Distribution Toit) | Signatures brutes (330) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | 13 planches signatures-01..13.png prêtes (71s) |
| **P13** | BOURASSA | E-204 (Schéma Unifilaire) | 1 repère (1 LL) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (122s) |
| **P14** | BOURASSA | E-205 (Détails Distribution) | 34 repères (34 L4) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (126s) |
| **P15** | BOURASSA | E-206 (Horodépot / Bornes) | Signatures brutes (92) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures-01..04.png prêtes (123s) |
| **P16** | BOURASSA | E-207 (Raccordements Équip.) | 9 repères (8 BJ, 1 Gâche) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (223s) |
| **P17** | BOURASSA | E-251 (Télécom & Sécurité) | Signatures brutes (300) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures générées (119s) |
| **P18** | BOURASSA | E-252 (Contrôle d'accès) | 1 repère (1 L4) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (124s) |
| **P19** | BOURASSA | E-253 (Caméras CCTV) | Signatures brutes (260) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | 10 planches signatures prêtes (67s) |
| **P20** | BOURASSA | E-301 (Plan de Masse Ext.) | Signatures brutes (155) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | 6 planches signatures prêtes (66s) |
| **P21** | BOURASSA | E-302 (Éclairage Extérieur) | Signatures brutes (71) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures prêtes (123s) |
| **P22** | CAMPUS MIL | page-1 (Tracé MT 25kV) | 0 (tracé raster) | Conforme | Conforme | **SUCCÈS (0 err)** | Analyse raster MT complétée (124s) |
| **P23** | CAMPUS MIL | page-2 (Profils Tranchées MT) | 0 (tracé raster) | Conforme | Conforme | **SUCCÈS (0 err)** | Analyse profils MT complétée (126s) |
| **P24** | CAMPUS MIL | E-100B (Jonctions 25kV Pav. C/D) | 5 signatures isolées | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Raccordements 25kV Pavillons C/D (116s) |
| **P25** | SUN LIFE | E003 (Opérateurs Portes 9-10) | À traiter | - | - | EN ATTENTE | Vague 4 |

---

## 2. Audit Visuel et Qualité par Cas

### Cas P01 - P01-BOURASSA-E-002
- **Type** : Légendes, symboles et notes générales.
- **Rendu MCP** : Succès (110s). Intégrité préservée (zéro pastille erronée sur les cartouches de texte).

### Cas P02 - P02-BOURASSA-E-101
- **Type** : Plan électrique d'éclairage RDC (41 310 tracés vectoriels).
- **Rendu MCP** : 5 repères vectoriels extraits et reconnus.
- **Contrôle visuel** : ox_in_free_space: true.

### Cas P03 - P03-BOURASSA-E-102
- **Type** : Plan électrique d'éclairage étage.
- **Rendu MCP** : 4 repères, 2 familles. produit: true.
- **Contrôle visuel** : Pastilles parfaitement centrées, bordereau matériel incrusté dans l'espace libre (ox_in_free_space: true), zéro troncature. BOM Excel et CSV synchronisés.

### Cas P04 - P04-BOURASSA-E-103
- **Type** : Plan électrique d'éclairage toit.
- **Rendu MCP** : 2 repères (Stations manuelles SM), 1 famille. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2430, 1410, 2665, 1617]), zéro troncature, calques conformes. Planche de contrôle E103-planche-01.png validée. BOM Excel/CSV synchronisés.

### Cas P05 - P05-BOURASSA-E-104
- **Type** : Plan de détails et montages d'éclairage.
- **Rendu MCP** : 2 repères reconnus (1 encastré d'urgence EU, 1 prise double 15A PC), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([1175, 1770, 1410, 2009.1]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P06 - P06-BOURASSA-E-105
- **Type** : Tableaux et agencements d'éclairage.
- **Rendu MCP** : 6 repères reconnus (2 détecteurs de fumée DF, 4 stations manuelles SM), 2 familles alarme. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([260, 1260, 495, 1499.1]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P07 - P07-BOURASSA-E-151
- **Type** : Plan d'alarme incendie RDC.
- **Rendu MCP** : 6 repères reconnus (2 stations manuelles SM, 3 encastrés d'urgence EU, 1 prise double 15A PC), 3 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([280, 1660, 515, 1931.1]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P08 - P08-BOURASSA-E-152
- **Type** : Plan d'alarme incendie étage.
- **Rendu MCP** : 3 repères reconnus (2 stations manuelles SM, 1 luminaire LED 4PI L4), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2500, 1410, 2735, 1649.1]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P09 - P09-BOURASSA-E-153
- **Type** : Plan d'alarme incendie réseau.
- **Rendu MCP** : 1 repère, 1 famille. produit: true.
- **Contrôle visuel** : ox_in_free_space: true. BOM Excel et CSV synchronisés.

### Cas P11 - P11-BOURASSA-E-202
- **Type** : Plan de distribution électrique étage.
- **Rendu MCP** : 5 repères identifiés (1 luminaire LED 4PI L4, 4 gâches G), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2515, 1445, 2750, 1684]), zéro troncature, calques conformes. Planche de contrôle E202-planche-01.png validée. BOM Excel/CSV synchronisés.

### Cas P13 - P13-BOURASSA-E-204
- **Type** : Schéma unifilaire électrique.
- **Rendu MCP** : 1 repère reconnu (1 luminaire linéaire LL), 1 famille. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2430, 1375, 2665, 1582]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P14 - P14-BOURASSA-E-205
- **Type** : Plan de détails et distribution électrique.
- **Rendu MCP** : 34 repères reconnus (34 luminaires LED 4PI L4), 1 famille éclairage. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2310, 835, 2545, 1042]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.

### Cas P16 - P16-BOURASSA-E-207
- **Type** : Plan d'équipement et raccordements.
- **Rendu MCP** : 9 repères identifiés (8 boîtes de jonction BJ, 1 gâche G), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2290, 205, 2525, 444]), zéro troncature, calques conformes. Planche de contrôle E207-planche-01.png validée. BOM Excel/CSV synchronisés.

### Cas P18 - P18-BOURASSA-E-252
- **Type** : Plan de contrôle d'accès.
- **Rendu MCP** : 1 repère reconnu (1 luminaire LED 4PI L4), 1 famille. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2560, 1385, 2795, 1592]), zéro troncature, calques conformes. BOM Excel/CSV synchronisés au taux officiel de 124,00 $/h.
