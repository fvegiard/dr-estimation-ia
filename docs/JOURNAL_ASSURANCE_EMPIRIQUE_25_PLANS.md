# JOURNAL D'ASSURANCE EMPIRIQUE - CAMPAGNE 25 PLANS (DR ÉLECTRIQUE INC.)

**Responsable de l'audit** : Léna AI / Francis Végiard  
**Dernière mise à jour** : 2026-10-20T04:48:00-04:00  
**Taux MO de référence** : 124,00 $/h  
**Objectif** : Validation empirique de bout en bout sur 25 planches électriques réelles isolées, contrôle visuel des pastilles, encadré bordereau dans l'espace libre et synchronisation BOM/QPL.

---

## 1. Tableau de Suivi en Temps Réel

| ID Cas | Projet | Feuille / Discipline | Repères Détectés | Score Visuel | Encadré Espace Libre | Statut MCP | Preuves & Livrables |
|---|---|---|:---:|:---:|:---:|:---:|---|
| **P01** | BOURASSA | E-002 (Légende & Normes) | 0 (texte/cartouche) | Conforme | Conforme | **SUCCÈS (0 err)** | preuves/P01-BOURASSA-E-002.json (110s) |
| **P02** | BOURASSA | E-101 (Éclairage RDC) | 5 repères | 4/5 | Conforme (ox_in_free_space: true) | **SUCCÈS (0 err)** | preuves/P02-BOURASSA-E-101.json (195s) |
| **P03** | BOURASSA | E-102 (Éclairage Étage) | 4 repères | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (217s) |
| **P04** | BOURASSA | E-103 (Éclairage Toit) | 2 repères | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (225s) |
| **P05** | BOURASSA | E-104 (Détails Éclairage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P06** | BOURASSA | E-105 (Tableaux Éclairage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P07** | BOURASSA | E-151 (Alarme Incendie RDC) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P08** | BOURASSA | E-152 (Alarme Incendie Étage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P09** | BOURASSA | E-153 (Réseau Incendie) | 1 repère | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (225s) |
| **P10** | BOURASSA | E-201 (Distribution RDC) | Signatures brutes (368) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures générées (127s) |
| **P11** | BOURASSA | E-202 (Distribution Étage) | 5 repères (1 L4, 4 G) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (213s) |
| **P12** | BOURASSA | E-203 (Distribution Toit) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P13** | BOURASSA | E-204 (Schéma Unifilaire) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P14** | BOURASSA | E-205 (Détails Distribution) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P15** | BOURASSA | E-206 (Horodépot / Bornes) | Signatures brutes (92) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures-01..04.png prêtes (123s) |
| **P16** | BOURASSA | E-207 (Raccordements Équip.) | 9 repères (8 BJ, 1 Gâche) | **5/5 Conforme** | **Conforme (ox_in_free_space: true)** | **SUCCÈS (0 err)** | BOM.xlsx, BOM.csv, Plans-annotes.pdf (223s) |
| **P17** | BOURASSA | E-251 (Télécom & Sécurité) | Signatures brutes (300) | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures générées (119s) |
| **P18** | BOURASSA | E-252 (Contrôle d'accès) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P19** | BOURASSA | E-253 (Caméras CCTV) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P20** | BOURASSA | E-301 (Plan de Masse Ext.) | À traiter | - | - | EN ATTENTE | Vague 3 |
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

### Cas P09 - P09-BOURASSA-E-153
- **Type** : Plan d'alarme incendie réseau.
- **Rendu MCP** : 1 repère, 1 famille. produit: true.
- **Contrôle visuel** : ox_in_free_space: true. BOM Excel et CSV synchronisés.

### Cas P11 - P11-BOURASSA-E-202
- **Type** : Plan de distribution électrique étage.
- **Rendu MCP** : 5 repères identifiés (1 luminaire LED 4PI L4, 4 gâches G), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2515, 1445, 2750, 1684]), zéro troncature, calques conformes. Planche de contrôle E202-planche-01.png validée. BOM Excel/CSV synchronisés.

### Cas P16 - P16-BOURASSA-E-207
- **Type** : Plan d'équipement et raccordements.
- **Rendu MCP** : 9 repères identifiés (8 boîtes de jonction BJ, 1 gâche G), 2 familles. produit: true.
- **Contrôle visuel** : ox_in_free_space: true ([2290, 205, 2525, 444]), zéro troncature, calques conformes. Planche de contrôle E207-planche-01.png validée. BOM Excel/CSV synchronisés.
