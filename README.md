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

## Structure pour Claude (Code, Cowork, action GitHub)

- `CLAUDE.md` — règles du projet, carte du dépôt, commandes (lu à chaque session).
- `.claude/skills/releve-planexpert/` — la méthode de relevé (conventions de l'estimateur incluses) ;
  `.claude/skills/comparer-estimateur/` — rejouer le jeu de référence.
- `.claude/agents/` — `releveur` (Opus), `verificateur` (Opus), `inventaire` (Haiku).
- `releve/` — la chaîne de relevé (rapatriée de `planexpert-s1857-saint-michel`, branche `releve-auto-v2`, e781203).
- `dossiers/_jeu-reference/` — rappel/précision de l'IA contre les projets Plan Expert de M. Dupuis (5 dossiers) ;
  la ligne de base est vérifiée à chaque PR par `.github/workflows/ci.yml`.
- `.github/workflows/claude.yml` — `@claude` dans une issue ou une PR ; nécessite le secret `CLAUDE_CODE_OAUTH_TOKEN`
  (`claude setup-token`) et l'app GitHub Claude installée sur le dépôt.

## Pipeline

1. **Entrée** — `dossiers/<no>/entree/` : plans PDF, devis, addendas
2. **Relevé** — `dossiers/<no>/releve.xlsx` : quantités par item, référence de page/plan pour chaque ligne
3. **Validation** — `dossiers/<no>/ecart.md` : comparaison ligne par ligne vs estimation de référence
4. **Saisie Plan Expert** — VM Windows sur `mxlinux`, pilotée par Claude Code (mxlinux) + Windows-MCP
5. **Chemins de câblage** — `dossiers/<no>/cablage.pdf` : tracé sur les plans

## Outillage livré (voir `SPEC.md` et `docs/consolidation.md`)

- `src/releve/` — chaîne `python -m src.releve` : `inventaire`, `index`, `raster`, `qpl`, `verifier`,
  `xlsx` (export `releve.xlsx` au gabarit DR)
- `src/pipeline/` — préparation d'un dossier de soumission (feuilles, tuiles, occurrences, `.qpl`, PDF)
- `src/validation/ecart.py` — comparateur déterministe référence vs décompte IA → `ecart.md`
  (verdict PASS/FAIL **calculé** ; le verdict FINAL reste à Francis)
- `src/cablage/` — métré des artères (`compute_arteres`) et injection de lignes dans le `.qpl`
  (`inject_lines`, assertion d'unicité des GroupID corrigée)
- `src/qpl/` — import de compteurs dans un `.qpl` existant (`import_counters`) + charte graphique (`charte`)
- `docs/` — format QPL et pipeline complet (`pipeline-qpl.md`), gabarits de livrables
  (`format-livrable.md`), table de consolidation (`consolidation.md`)
- `infra/` — VM Plan Expert sur mxlinux (`infra/mxlinux/`) et traitement en série (`infra/pe-batch.ps1`)
- `tests/` — pytest, fixtures **synthétiques uniquement** (aucune donnée client)

```bash
pip install -r requirements.txt
python -m compileall src        # propre
python -m pytest tests -q       # vert
```

## État réel au 22 septembre 2026, 5 h (heure de l'Est)

**11 dossiers refaits à l'aveugle** par la chaîne automatique (`releve/`, branche `releve-auto-v2` de
`fvegiard/saint-michel-planexpert-s1857`) dans le cloud, sans Plan Expert ni VM, puis **chacun comparé par un
vérificateur indépendant** (agent Opus distinct, qui lit le relevé humain scanné, transcrit chaque ligne, et va voir
chaque écart sur le plan). Tout est dans `dossiers/<S>/` : `releve.xlsx`, `ecart.md` (preuves), `Plans-annotes.pdf`,
`Rapport-de-metre.pdf`, projet Plan Expert (`planexpert/*.qpl`), réserves, nomenclature.

| S- | Projet | Référence humaine | Objets comparés | Écart net | Postes > 10 % | Manquants non signalés | 10 marques au hasard | Verdict du vérificateur |
|---|---|---|--:|--:|---|--:|---|---|
| S-1857 | Maison communautaire Saint-Michel | M. Dupuis (Plan Expert) | 1 343 | −0,5 % | prises spéciales (3/5) | ~10 (colonnette, 3 prises + 1 data bureau 315, ~5 prises près des klaxons) | 10/10 | pas tel quel : prises E407-E408 à reprendre ; addenda ADME-01 complet jamais reçu |
| S-1689 | Pultrusion St-Bruno | take-off (éclairage seul, 105 obj.) | 105 | +8,6 % imputable IA | commandes | 2 réglettes E | 10/10 | pas tel quel : interrupteurs fusionnés, 14 luminaires B au lieu de D |
| S-1769 | CPE Soleil Souriant | relevé complet (ACCEO) | 122 | −1,6 % | télécom (−50 %, 2 obj.) | 2 (1 klaxon, 1 GFI) | 10/10 | proche : 4 corrections |
| S-1715 | Sportive Parc Lionel-Groulx | RELEVÉ ESTIMATION | 302 | +1,7 % | mécanique +20 % (3 obj.), portes (référence en erreur) | 0 objet (1 poteau mal qualifié « par autres ») | 10/10 | utilisable comme base après 3 corrections |
| S-1844 | SAQ Varennes | take off | 410 | −0,5 % | commandes nLight +87 % (doublons), prises −32 %, data −45 % | 12 projecteurs sans étiquette, 14 doublons, 7 monuments | 10/10 | pas tel quel : doublons + 12 têtes |
| S-1808 | CPE Les Copains d'abord | relevé final Daniel | 777 | +1,2 % | chauffage +10,6 %, distribution −12,5 % | 4 (3 détecteurs-gradateurs, 1 thermique) | 10/10 | base de travail : TYPE D→C, 4 objets, sous-types |
| S-1811 | CDC 6 bâtiments (1 bât. + site) | relevé final Daniel | 787 | +2,7 % | distribution +10,5 % (2 obj.) | 1 (3 interrupteurs mal typés) | 10/10 | oui après corrections légères ; plus à jour que Daniel sur l'addenda |
| S-1695 | Hôtel Playground Kahnawake | relevé de Daniel | 853 (aires communes) | −0,5 % | sèche-mains, raccords, prises 30 A | 78 sectionneurs, N4B, 11 raccords | 10/10 | **non** : chambres types non multipliées (−64 % luminaires) |
| S-1693 | École primaire Beloeil | Relevé de Daniel | 1 794 | −3,8 % (−11,8 % toutes familles) | distribution −37 %, caméras −13 %, interrupteurs/intercom non relevés | salle électrique, 17 grillages, 5 prises… | 10/10 | pas tel quel : salle électrique, interrupteurs, fausses gâches |
| S-1797 | École Chambly | Relevé de Daniel + alarme | 788 | +5,3 % (+2,3 % sans sectionneurs TP) | alarme (référence faite sur AO, l'IA a raison), chauffage, distribution | 5 relais RE253C, remplacement panneau alarme | 10/10 | éclairage/urgence/nLight utilisables ; distribution et chauffage non |
| S-1714 | Riviera Carignan 140 logements | relevé de Daniel | 7 352 | −0,75 % | enseignes −54 % | 39 enseignes, 140 prises d'échangeur, allocations logements, 20 conduits | 10/10 | proche : 4 corrections |

Lecture honnête :
- **Ce qui marche** : le repérage. Sur 110 marques tirées au hasard (10 par dossier), **110 sont sur un vrai objet du plan**.
  Sur 7 dossiers sur 11, l'écart net est sous 3 %. Dans 4 dossiers (S-1811, S-1797, S-1715, S-1844), l'IA est **plus juste ou
  plus à jour que la référence** sur au moins un poste (addendas appliqués, oublis de l'estimateur retrouvés).
- **Ce qui ne marche pas encore** : le critère « aucun item manquant non signalé » n'est atteint dans **aucun** dossier ; les
  écarts par poste dépassent 10 % dans 10 dossiers sur 11 (souvent sur 2-3 objets, parfois sur une famille entière). Causes
  répétées : symboles sans étiquette, variantes fusionnées, unités types non multipliées (S-1695), notes de plan non chiffrées,
  démolition sans type, neuf/existant, et une part de hasard d'une exécution à l'autre (v1 ↔ v2).
- **Aucune longueur** (câble, conduit) n'est métrée : c'est l'essentiel des heures d'une soumission et ce n'est pas couvert.
- **Verdict** : pas « 100 % prêt » au sens du critère ci-dessus. Prêt à être **montré** : un estimateur peut ouvrir n'importe
  quel `ecart.md` et voir, ligne par ligne, où l'IA a raison, où elle se trompe, et pourquoi.

## Exports natifs Plan Expert (22 septembre, 8 h 45 – 11 h, VM `mxlinux`)

Les 11 projets `.qpl` produits par la chaîne ont été **importés dans le vrai Plan Expert** (VM Windows sur mxlinux, pilotée
à la souris par VNC, captures d'écran à l'appui) : ouverture du projet, sauvegarde native, rapport de métré « classé par
plans » exporté en PDF/Excel/XML, plans annotés exportés en PDF. Résultat dans `dossiers/<S>/export-natif/` :
`<S>.qpl` (sauvé par Plan Expert), `<S>-Rapport-de-métré-(par-plans).pdf/.xls`, `<S>-Métré-[Classé_par_plans].xml`.
Les plans annotés natifs (`<S>.pdf`, 12 à 120 Mo chacun) ne sont pas dans le dépôt : ils sont sur le Legion dans
`D:\claude\releve-auto\OUTBOX\<S>\export-natif-planexpert\` et sur mxlinux dans `/srv/planexpert/shared/sorties/<S>/`.

Contrôle : le nombre d'objets compté par Plan Expert (XML natif) est **identique** au `releve.xlsx` de la chaîne
pour les 11 dossiers (S-1689 256, S-1693 1 765, S-1695 1 719, S-1714 7 385, S-1715 359, S-1769 141, S-1797 1 218,
S-1808 826, S-1811 811, S-1844 773, S-1857 1 421) — les marques survivent à l'import sans perte ni doublon.
Ce que Plan Expert ne fait pas ici : aucune ligne d'estimation (prix/heures) n'est rattachée aux compteurs, et les
longueurs ne sont toujours pas métrées.

## Ce qui a été corrigé cette nuit dans la chaîne (v1 → v2)

1. Pages tournées (Rotate 90/270 : S-1714, S-1769, S-1797, S-1811) — coordonnées texte fausses, marques mal placées. Corrigé.
2. Pages sans numéro de feuille lisible ignorées (S-1714 : 34 pages sur 44 ; S-1769 : 5 sur 7). Corrigé : plus aucune page perdue.
3. Noms de feuilles faux dans les livrables (E401 publiée « E004 »). Corrigé : numéro lu dans le cartouche.
4. Mots superposés comptés en double (S-1844). Corrigé dans `extract_occurrences.py`.
5. Nouvel outil `traits.py` (neuf vs existant par épaisseur/couleur de trait) ; règles ajoutées à la compétence de l'agent
   (étiquettes dans un autre texte, qualificatifs MO/DDFT, doublons inter-feuilles, cédules et unifilaire → raccordements,
   symboles hors légende, démolition, linéaires).
6. Outils de l'agent refusés (chemins absolus, commandes chaînées) → autorisés + règle « une commande par appel ».

Reste à corriger (constaté par les vérificateurs, non encore codé) : multiplicateur des unités/chambres types ; détection des
symboles sans étiquette par la forme vectorielle ; une ligne de légende = un compteur (variantes) ; notes « prévoir N par
logement » → N objets ; sous-types (tension, pôles, calibre) ; stabilité d'une exécution à l'autre (double passe + vote).

## Repos existants (à consolider ici)

planexpert-core, planexpert-atelier, planexpert-s1857-saint-michel, planexpert-hr26-14,
planexpert-s1787-bioscript, planexpert-infra-mxlinux, dr-releves-2026,
dashboard-soumissions-dr, electrical-estimation-mcp (tous privés)

## Ce qui ne va jamais dans ce repo

Image de la VM, installateurs ou licences Windows/Plan Expert, clés/tokens. Décision de Francis (22 sept. 2026) : les plans,
les prix et tous les fichiers produits ici sont publics — les relevés humains de référence (`dossiers/<S>/entree/reference-*.pdf`)
et les projets Plan Expert de M. Dupuis (`dossiers/<S>/reference/<S>-Dupuis-PlanExpert.qpl`, le jeu de référence de
`compare_qpl`) sont dans le dépôt. Les tests n'utilisent que des fixtures synthétiques.
