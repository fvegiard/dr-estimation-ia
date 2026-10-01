# Plan d'entraînement — 10 projets à l'aveugle, puis comparaison au .qpl humain

Demande de Francis (session Copilot « Create a branch protect main… ») : protéger `main`, préparer une branche
d'entraînement où le LLM relève 10 projets **sans toucher au .qpl de l'estimateur**; une fois un projet relevé,
il ouvre le .qpl humain, identifie les écarts avec son propre relevé, et on en tire des corrections.

## 0. Garde-fous (avant tout)
- **Protéger `main`** (réglage GitHub, à faire par Francis : Settings → Branches → règle sur `main` :
  PR obligatoire, pas de push direct, pas de force-push). Aucun outil de l'agent ne pose cette règle.
- Travail uniquement sur `test-comparaison` (ou une branche par lot) ; fusion dans `main` par PR relue.
- La PR #10 a déjà été fusionnée dans `main` (01:38) : décider si on la garde ou si on la revert.

## 1. Constat de départ (lu en entier)
- Le **critère d'acceptation** de la branche `agent/openhands/repeatable-pdf` (PR #9, pas encore dans `main`) décrit déjà la
  procédure voulue : identifier à l'aveugle → geler (commit) → comparer (`compare_qpl`) → classer chaque désaccord
  (omission, doublon, mauvaise famille, portée, feuille) → justifier sur le plan → corriger → revérifier.
  Le plan ci-dessous l'applique à 10 projets ; il ne la remplace pas.
- Seuls 5 dossiers du dépôt ont le .qpl humain dans `reference/` : S-1714, S-1715, S-1769, S-1811, S-1844.
- `apprentissage/qpl-2021-2026/recensement-complet/appariement-plans-qpl.csv` : 41 numéros S ont plans (Drive) + .qpl
  de M. Dupuis avec marques > 0. Les plus riches : S-1741 (5758 marques), S-1767 (4334), S-1692 (3656), S-1775 (3231),
  S-1706 (2722), S-1740, S-1783, S-1766 (hors les 5 déjà au dépôt).
- Les plans bruts sont à prendre dans Drive « original » (`docs/sources-cloud-plans-originaux.md` sur la PR #9) ;
  exclure le sous-dossier `Prix` et tout .qpl/PNG marqué de l'estimateur.
- Limite : le dossier S-1714 (8503 marques) est très lourd ; commencer par des projets de taille moyenne.

## 2. Choix des 10 projets
- Les 5 déjà au dépôt + 5 pris dans la liste ci-dessus (S-1692, S-1740, S-1766, S-1775, S-1706 : tailles moyennes, types variés
  — écoles, clinique, caserne, logements).
- Un projet à la fois ; pas de .qpl humain téléchargé avant que le relevé IA soit gelé.

## 3. Boucle par projet (répétée 10 fois)
1. **Aveugle** : `releve/prepare.py` puis agent `releveur`. Le .qpl humain reste hors de portée
   (`reference/` jamais lue pendant cette étape ; l'agent n'a pas Read sur ce dossier).
2. `extract_occurrences.py` → `build_qpl.py` → `render_pdf.py` (`run.py --reprendre <S>`).
3. **Déverrouillage** : seulement après le .qpl IA, ouvrir le .qpl humain.
4. **Écarts** : `compare_qpl` → manquants (humain oui / IA non), en trop, mauvaise famille, mauvaise position.
   L'agent `verificateur` prouve chaque écart sur le plan (zoom) : vraie erreur IA, erreur humaine, ou plan ambigu.
5. **Fiche d'apprentissage** `dossiers/<S>/ecart.md` : cause de chaque écart (symbole mal lu, cédule oubliée, réserve manquante…).

## 4. Apprentissage entre projets
- Les causes qui reviennent ≥ 2 fois deviennent des règles dans `.claude/skills/releve-planexpert/SKILL.md`.
- Chaque modification de la compétence → jeu de référence sans régression (règle du projet).
- Tableau de suivi : rappel / précision par projet, pour voir si la courbe monte du projet 1 au 10.

## 5. Critères de succès
- Rappel et précision par projet, et moyenne mobile qui progresse.
- Aucune régression sur les projets déjà relevés.
- Rapport final : écarts classés par cause, règles ajoutées, gain mesuré.

## 6. Points à trancher par Francis
1. PR #10 : garder ou revert ? (elle n'a fusionné que le 1er des 7 commits de la PR #9)
2. Valider les 5 projets proposés (S-1692, S-1740, S-1766, S-1775, S-1706)
3. Le .qpl humain peut-il rester public dans le dépôt (décision du 22/09 : oui) ?
