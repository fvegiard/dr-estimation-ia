# Feuille de route — autonomie totale de l'estimation

But déclaré (Francis, 2026-11-24) : la chaîne produit une soumission complète sans humain dans la
mécanique (repérage, livrables, chiffrage sourcé), avec la porte d'acceptation mesurée obligatoire —
**jamais en dessous de l'estimateur** (CLAUDE.md § Critère d'acceptation : identifie à l'aveugle →
gel sha256 → comparaison → classement → justification sur le plan → corriger/revérifier → verdict).
Le verdict final reste à Francis, jamais à l'IA.

## Définition mesurable de « autonome » (par porte, avec preuve et seuil)

Une porte est FERMÉE seulement par une preuve sur disque (fichier, journal, compte, exit code) —
jamais par le récit d'un agent. Les écarts se lisent contre `dossiers/`, pas contre la mémoire.

| # | Porte | Seuil mesurable | État prouvé (2026-11-24) |
|---|---|---|---|
| G0 | Plateforme + rejouabilité du socle | démarrage stdio < 0,2 s ; suite pytest exit 0 ; jeu_reference rejoué à l'identique | **PASS** — 26,6-34,4 ms (.venv), 46,8-86,2 ms (conteneur collègue), `mcp-demarrage-rapport.json` conforme true ; 421 tests passés ; comparaison jouée 2×, sorties octet-à-octet identiques (preuve rejouabilité vague 1, journal 2026-11-24-autonomie-totale) |
| G1 | Repérage des symboles | 110 marques échantillonnées sur un vrai objet ; écart net < 3 % | **PASS partiel** — 110/110 ; 7 dossiers sur 11 sous 3 % |
| G2 | Écarts par poste majeur | luminaires/distribution/filage/conduits ≤ 10 % sur les 11 dossiers | **NON** — 10 dossiers sur 11 dépassent 10 % sur ≥ 1 poste |
| G3 | Aucun manquant non signalé | 0 objet omis sans réserve, 11 dossiers | **NON** — 0/11 atteint |
| G4 | Précision de comptage fine | multiplicateurs unités types (S-1695 : −64 % luminaires) ; variantes = compteurs ; symboles sans étiquette vectoriellement détectés ; sous-types (tension/pôles/calibre) ; notes « prévoir N » → N objets | **NON** — multiplicateurs.csv existe dans la chaîne MCP mais pas branché dans la route blocs ; détection vectorielle sans étiquette absente |
| G5 | Métré des longueurs | câbles et conduits métrés dans le .qpl et le rapport de métré, comparé à la référence | **NON** — `src/cablage/compute_arteres.py` + `inject_lines.py` existent mais aucune longueur n'est dans les livrables ; c'est l'essentiel des heures |
| G6 | Chiffrage complet sourcé | prix + heures par poste (prix/dupuis), jamais inventé | **PARTIEL** — soumission S-1902 194 000 $ produite (méthode Dupuis) ; poste sans heure sourcée = non chiffrable, réservé |
| G7 | Stabilité d'exécution | même entrée → même sortie (double passe + vote pour la route par agent) | **PARTIEL** — route blocs déterministe prouvée par rejouabilité du socle ; route agent : vote/double passe non implémenté |

## Ordre de dépendances et prochains chantiers

G0 (socle) → G3+G4 (précision de comptage, conditions de G2/G3) → G5 (longueurs, conditions des
heures) → G6 étendu → G7 complet (vote pour la route agent) → **G8 — soumission autonome sur un
dossier neuf, prouvée par la boucle d'acceptation complète** (étapes 1 à 8, verdict tranché sur le
plan, `ACCEPTATION.md` écrit par la chaîne).

Chaque chantier : lire le code d'abord (jamais depuis les souvenirs), le contrat de fin = la
commande de preuve qui passe, aucune révision du gold (docs/FORMAT-EXEMPLE.md), chaque désaccord
classé et justifié sur le plan.

## Données requises par chantier

- G3/G4/G5 : plans d'origine (Drive « plan expert qpl » → sous-dossier `original`, ou SharePoint
  « Mes projets » de Daniel — `docs/sources-cloud-plans-originaux.md` ; sur le poste : INBOX/<S>/
  avec plans + addendas seulement). Sur cette machine : aucun plan complet local — les portes
  plan-dépendantes attendent le rapatriement cloud/Legion.
- G8 : la boucle `python -m src.validation.boucle_acceptation <S> --workdir W --dossier D` +
  référence de l'estimateur.

## Règles qui ne bougent pas avec l'autonomie

1. Jamais en dessous de l'estimateur (boucle d'acceptation) ; « vérification incomplète » vaut
   mieux qu'une certification sans preuve.
2. Un rapport d'agent n'est pas une preuve : lire le fichier produit, rejouer la commande soi-même.
3. Rien n'est inventé : chaque quantité vient d'un symbole étiquette, d'une cédule, d'une note ; le
   doute va en réserve.
4. Le gold HR26-14 ne se corrige pas ; on corrige la spec.
5. Le verdict final de soumission reste à Francis.
