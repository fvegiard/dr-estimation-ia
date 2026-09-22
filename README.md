# DR Estimation IA

Estimations électriques de DR Électrique produites par IA, prêtes pour soumission.
Les dossiers (plans, devis, addendas) sont publics — appels d'offres publiés.

## Définition de « 100 % prêt » (mesurable)

- 10 dossiers déjà soumissionnés refaits par l'IA de bout en bout
- Écart sur le total ≤ 5 % vs l'estimation de référence de Francis (seuil proposé, à confirmer par Francis)
- Écart par poste majeur (luminaires, distribution, filage, conduits) ≤ 10 %
- Aucun item manquant non signalé
- Verdict final : Francis, pas l'IA

Tant que ces chiffres ne sont pas atteints et prouvés dans `dossiers/`, le projet n'est PAS prêt.

## Pipeline

1. **Entrée** — `dossiers/<no>/entree/` : plans PDF, devis, addendas
2. **Relevé** — `dossiers/<no>/releve.xlsx` : quantités par item, référence de page/plan pour chaque ligne
3. **Validation** — `dossiers/<no>/ecart.md` : comparaison ligne par ligne vs estimation de référence
4. **Saisie Plan Expert** — VM Windows sur `mxlinux`, pilotée par Claude Code (mxlinux) + Windows-MCP
5. **Chemins de câblage** — `dossiers/<no>/cablage.pdf` : tracé sur les plans

## État réel

| Étape | État |
|---|---|
| Estimations produites | **0** |
| 1. Entrée | non commencé |
| 2. Relevé | non commencé |
| 3. Validation | non commencé |
| 4. Saisie Plan Expert | non prouvé (S-1857 rejeté) |
| 5. Chemins de câblage | jamais essayé |

## Repos existants (à consolider ici)

planexpert-core, planexpert-atelier, planexpert-s1857-saint-michel, planexpert-hr26-14,
planexpert-s1787-bioscript, planexpert-infra-mxlinux, dr-releves-2026,
dashboard-soumissions-dr, electrical-estimation-mcp (tous privés)

## Ce qui ne va jamais dans ce repo

Image de la VM, installateurs ou licences Windows/Plan Expert, clés/tokens.
