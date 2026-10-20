# JOURNAL D'ASSURANCE EMPIRIQUE — CAMPAGNE 25 PLANS (DR ÉLECTRIQUE INC.)

**Responsable de l'audit** : Léna AI / Francis Végiard  
**Dernière mise à jour** : 2026-10-20T04:37:00-04:00  
**Taux MO de référence** : 124,00 $/h  
**Objectif** : Validation empirique de bout en bout sur 25 planches électriques réelles isolées, contrôle visuel des pastilles, encadré bordereau dans l'espace libre et synchronisation BOM/QPL.

---

## 1. Tableau de Suivi en Temps Réel

| ID Cas | Projet | Feuille / Discipline | Repères Détectés | Score Visuel | Encadré Espace Libre | Statut MCP | Preuves & Livrables |
|---|---|---|:---:|:---:|:---:|:---:|---|
| **P01** | BOURASSA | `E-002` (Légende & Normes) | 0 (texte/cartouche) | Conforme | Conforme | **SUCCÈS (0 err)** | `preuves/P01-BOURASSA-E-002.json` (110s) |
| **P02** | BOURASSA | `E-101` (Éclairage RDC) | 5 repères | 4/5 (1 décalage) | Conforme (`box_in_free_space: true`) | **SUCCÈS (0 err)** | `preuves/P02-BOURASSA-E-101.json` (195s) |
| **P03** | BOURASSA | `E-102` (Éclairage Étage) | 4 repères | **5/5 Conforme** | **Conforme (`box_in_free_space: true`)** | **SUCCÈS (0 err)** | `BOM.xlsx`, `BOM.csv`, `Plans-annotes.pdf` (217s) |
| **P04** | BOURASSA | `E-103` (Éclairage Toit) | En cours | - | - | EN COURS | Vague 1 |
| **P05** | BOURASSA | `E-104` (Détails Éclairage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P06** | BOURASSA | `E-105` (Tableaux Éclairage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P07** | BOURASSA | `E-151` (Alarme Incendie RDC) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P08** | BOURASSA | `E-152` (Alarme Incendie Étage) | À traiter | - | - | EN ATTENTE | Vague 1 |
| **P09** | BOURASSA | `E-153` (Réseau Incendie) | 1 repère | **5/5 Conforme** | **Conforme (`box_in_free_space: true`)** | **SUCCÈS (0 err)** | `BOM.xlsx`, `BOM.csv`, `Plans-annotes.pdf` (225s) |
| **P10** | BOURASSA | `E-201` (Distribution RDC) | En cours | - | - | EN COURS | Vague 2 |
| **P11** | BOURASSA | `E-202` (Distribution Étage) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P12** | BOURASSA | `E-203` (Distribution Toit) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P13** | BOURASSA | `E-204` (Schéma Unifilaire) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P14** | BOURASSA | `E-205` (Détails Distribution) | À traiter | - | - | EN ATTENTE | Vague 2 |
| **P15** | BOURASSA | `E-206` (Horédépot / Bornes) | 98 signatures | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches `signatures-01..04.png` prêtes |
| **P16** | BOURASSA | `E-207` (Raccordements Équip.) | En cours | - | - | EN COURS | Vague 3 |
| **P17** | BOURASSA | `E-251` (Télécom & Sécurité) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P18** | BOURASSA | `E-252` (Contrôle d'accès) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P19** | BOURASSA | `E-253` (Caméras CCTV) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P20** | BOURASSA | `E-301` (Plan de Masse Ext.) | À traiter | - | - | EN ATTENTE | Vague 3 |
| **P21** | BOURASSA | `E-302` (Éclairage Extérieur) | Signatures | À étiqueter | Conforme | **ISOLÉ (signatures extraites)** | Planches signatures prêtes |
| **P22** | CAMPUS MIL | `page-1` (Tracé MT 25kV) | En cours | - | - | EN COURS | Vague 4 |
| **P23** | CAMPUS MIL | `page-2` (Profils Tranchées MT) | À traiter | - | - | EN ATTENTE | Vague 4 |
| **P24** | CAMPUS MIL | `E-100B` (Jonctions 25kV Pav. C/D) | À traiter | - | - | EN ATTENTE | Vague 4 |
| **P25** | SUN LIFE | `E003` (Opérateurs Portes 9-10) | À traiter | - | - | EN ATTENTE | Vague 4 |

---

## 2. Audit Visuel et Qualité par Cas

### Cas P01 — `P01-BOURASSA-E-002`
- **Type** : Légendes, symboles et notes générales.
- **Rendu MCP** : Succès (110s). Intégrité préservée (zéro pastille erronée sur les cartouches de texte).

### Cas P02 — `P02-BOURASSA-E-101`
- **Type** : Plan électrique d'éclairage RDC (41 310 tracés vectoriels).
- **Rendu MCP** : 5 repères vectoriels extraits et reconnus.
- **Contrôle visuel** : `box_in_free_space: true`.

### Cas P03 — `P03-BOURASSA-E-102`
- **Type** : Plan électrique d'éclairage Étage.
- **Rendu MCP** : 4 repères, 2 familles. `produit: true`.
- **Contrôle visuel** : Pastilles parfaitement centrées, bordereau matériel incrusté dans l'espace libre (`box_in_free_space: true`), zéro troncature. BOM Excel et CSV synchronisés.

### Cas P09 — `P09-BOURASSA-E-153`
- **Type** : Plan d'alarme incendie réseau.
- **Rendu MCP** : 1 repère, 1 famille. `produit: true`.
- **Contrôle visuel** : `box_in_free_space: true`. BOM Excel et CSV synchronisés.