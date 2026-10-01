# Plan d'entraînement — 10 projets à l'aveugle, puis comparaison au .qpl humain

Demande de Francis (session Copilot « Create a branch protect main… ») : protéger `main`, préparer une branche
d'entraînement où le LLM relève 10 projets **sans toucher au .qpl de l'estimateur**; une fois un projet relevé,
il ouvre le .qpl humain, identifie les écarts avec son propre relevé, et on en tire des corrections.

## 0. Garde-fous (avant tout)
- **Protéger `main`** (réglage GitHub, à faire par Francis : Settings → Branches → règle sur `main` :
  PR obligatoire, pas de push direct, pas de force-push). Aucun outil de l'agent ne pose cette règle.
- Travail uniquement sur `test-comparaison` (ou une branche par lot) ; fusion dans `main` par PR relue.
- La PR #10 a déjà été fusionnée dans `main` (01:38) : décider si on la garde ou si on la revert.

## 1. Constat de départ
- 5 dossiers ont un .qpl humain exploitable (`dossiers/<S>/reference/<S>-Dupuis-PlanExpert.qpl`) ; il en faut 10.
- Le jeu de référence (`python -m src.validation.jeu_reference`) rejoue déjà la comparaison marque par marque.
- Dépendance manquante dans ce conteneur : `numpy` (`pip install -r requirements.txt`).

## 2. Choix des 10 projets
- Lister les dossiers S-* ayant plans + .qpl humain ; compléter à 10 avec les projets où l'estimateur fournit son .qpl.
- Mélanger types (bureaux, industriel, résidentiel…) pour ne pas entraîner sur un seul style.

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
1. Garder ou revert la PR #10 ?
2. Quels sont les 5 projets supplémentaires avec .qpl humain ?
3. Le .qpl humain peut-il rester public dans le dépôt (décision du 22/09 : oui) ?
