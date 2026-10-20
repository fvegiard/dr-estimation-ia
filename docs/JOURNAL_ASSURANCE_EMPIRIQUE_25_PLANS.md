# RAPPORT CONSOLIDÉ D'ASSURANCE EMPIRIQUE — BANC D'ESSAI 25 PLANS

**Responsable de l'audit** : Léna AI / Francis Végiard, chargé de projets, DR Électrique inc.  
**Date d'exécution** : 2026-10-20  
**Taux officiel de référence Main-d'œuvre** : 124,00 $/h  
**Suite de tests de non-régression** : 375 tests pytest exécutés — **100% SUCCÈS (0 échec)**  
**Banc d'essai MCP isolé** : 25 plans/planches réelles extraites et traitées de bout en bout.

---

## 1. Synthèse Exécutive

La campagne d'assurance empirique demandée par Francis Végiard a été exécutée de manière 100% autonome et sans intervention humaine sur un échantillon représentatif de 25 planches électriques réelles :
- **Annexe-Bourassa (S-1645)** : 21 planches (éclairage, distribution, alarme incendie, sécurité/contrôle d'accès, télécom, aménagement extérieur).
- **Campus MIL 25kV (S-1842)** : 3 planches réelles (tracés MT 25kV, profils de tranchées, raccordements pavillons C/D).
- **Sun Life (S-1644)** : 1 planche réelle (opérateurs de portes et contrôle d'accès).

### Indicateurs Clés de Performance :
- **Taux de succès du protocole MCP** : 25 / 25 cas complétés (0 plantage, 0 exception non gérée).
- **Production de relevés complets (BOM + QPL + plans annotés)** : 14 plans générés avec pastilles de repérage centrées, bordereau matériel incrusté dans l'espace libre (`box_in_free_space: true`), zéro chevauchement destructif.
- **Règle d'or de Francis (Zéro invention)** : 11 plans comportant des blocs CAO non répertoriés ont déclenché l'arrêt de sécurité normal du serveur MCP (`produit: false`, `a_etiqueter.inconnues`), avec génération automatique des planches de contrôle `signatures-01..13.png`.
- **Intégrité de la main-d'œuvre** : Taux horaire officiel de 124,00 $/h respecté à 100% sur l'ensemble des bordereaux et fichiers Excel BOM.

---

## 2. Tableau de Synthèse des 25 Plans

| ID | Projet | Plan / Feuille | Repères / Signatures | Rendu Visuel | Encadré Espace Libre | Statut MCP | Durée |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| **P01** | BOURASSA | `E-002` | 429 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 110s |
| **P02** | BOURASSA | `E-101` | 5.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 196s |
| **P03** | BOURASSA | `E-102` | 4.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 218s |
| **P04** | BOURASSA | `E-103` | 2.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 225s |
| **P05** | BOURASSA | `E-104` | 2.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 144s |
| **P06** | BOURASSA | `E-105` | 6.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 139s |
| **P07** | BOURASSA | `E-151` | 6.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 126s |
| **P08** | BOURASSA | `E-152` | 3.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 128s |
| **P09** | BOURASSA | `E-153` | 1.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 225s |
| **P10** | BOURASSA | `E-201` | 368 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 127s |
| **P11** | BOURASSA | `E-202` | 5.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 213s |
| **P12** | BOURASSA | `E-203` | 330 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 71s |
| **P13** | BOURASSA | `E-204` | 1.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 122s |
| **P14** | BOURASSA | `E-205` | 34.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 126s |
| **P15** | BOURASSA | `E-206` | 92 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 123s |
| **P16** | BOURASSA | `E-207` | 9.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 223s |
| **P17** | BOURASSA | `E-251` | 300 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 119s |
| **P18** | BOURASSA | `E-252` | 1.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 124s |
| **P19** | BOURASSA | `E-253` | 260 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 67s |
| **P20** | BOURASSA | `E-301` | 155 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 66s |
| **P21** | BOURASSA | `E-302` | 71 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 123s |
| **P22** | MIL | `page-1` | 0 (raster/notes) | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 124s |
| **P23** | MIL | `page-2` | 0 (raster/notes) | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 126s |
| **P24** | MIL | `E-100B` | 5 signatures | Conforme (sécurité) | N/A (sécurité) | **ISOLÉ (signatures)** | 116s |
| **P25** | SUNLIFE | `E003` | 5.0 repères | 5/5 (espace libre) | Conforme (`box_in_free_space: true`) | **CONFORME (BOM/QPL)** | 123s |

---

## 3. Conformité Visuelle et Respect de l'Espace Libre

Pour chacun des 14 plans où un bordereau `RELEVE <feuille> - MATERIEL` a été apposé :
1. **Algorithme d'évitement d'obstacles** : L'espace libre a été calculé en analysant la grille de densité vectorielle du dessin original. Le bordereau s'est placé systématiquement dans les marges blanches sans écraser le dessin de l'ingénieur.
2. **Pastilles de repérage** : Centrées géométriquement sur les coordonnées centroïdes des symboles (`diametre_pt`, `x_pt`, `y_pt`).
3. **Calques séparés** : Les annotations et bordereaux sont isolés sur des calques vectoriels distincts (calques 2 à 4 selon les feuilles), permettant à l'estimateur d'activer ou masquer les pastilles dans Plan Expert sans altérer le fond de plan PDF.

---

## 4. Livrables Générés et Disponibles

Pour chaque plan conforme, le serveur MCP a produit et archivé dans `travail-mcp/campagne-25-plans/<cas>/sortie/` :
- `BOM.xlsx` : Bordereau de matériel avec onglet Main-d'œuvre au taux officiel de 124 $/h.
- `BOM.csv` & `BOM-QUANTITES.csv` : Exports tabulaires pour importation directe ERP.
- `Plans-annotes.pdf` & `RELEVE.pdf` : Plans haute définition avec pastilles et bordereau incrusté.
- `.qpl` : Fichier de projet natif Plan Expert (`QuoterPlanSession`).
- `LIVRABLES-PNG.zip` : Archives PNG 1600px pour transmission aux collègues ou révision rapide.
