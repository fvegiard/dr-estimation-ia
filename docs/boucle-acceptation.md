# Boucle d'acceptation — aveugle → gel → comparaison → classement → justifications

La boucle d'acceptation automatise les étapes 1 à 8 du
[critère d'acceptation de CLAUDE.md](../CLAUDE.md) : le relevé IA « ne doit jamais être
accepté s'il est pire » que le relevé de référence de l'estimateur. Chaque étape est
**calculée** par un script déterministe, jamais rapportée sur foi d'un agent : un verdict
s'appuie sur les fichiers produits, jamais sur le journal d'une exécution. Les étapes
1 à 4 sont prouvées par des artefacts sur disque (voir plus bas).

Chaîne (s'arrête au premier refus — la comparaison n'appelle jamais `compare_qpl` si le
relevé n'est pas aveugle ou si le gel est violé) :

```
controle aveugle (étape 1) → gel sha256 (étape 2) → comparaison marque par marque (étape 3)
→ classification des désaccords (étape 4) → dossier de justifications à remplir (étapes 5 à 7)
→ ACCEPTATION.md (verdict ; décision finale = Francis)
```

Un relevé sans référence estimateur disponible donne **VÉRIFICATION INCOMPLÈTE**, jamais un
« pas pire que l'estimateur » tacite (étape 8 : l'absence de preuve n'est pas une preuve
d'absence de régression).

## Modules (tous dans `src/validation/`)

| Module | Rôle | Étapes du critère |
|---|---|---|
| `aveugle.py` | Scan récursif du workdir du relevé IA : `.qpl` « dupuis », dossier `reference/`, noms `dupuis/estimateur/reference/humain`, `releve.xlsx`, signatures de contenu. | 1 |
| `gel.py` | Gel sha256 de chaque artefact du relevé IA (`nomenclature.csv`, `occurrences-*.csv`, `feuilles-classement.csv`, `reserves.md`, tout `.qpl`) dans `gel.json`, revérifié à chaque relance. | 2 |
| `compare_qpl.py` | Comparaison déterministe marque par marque, page par page (préexistante, partagée avec le jeu de référence). | 3 |
| `classer_ecarts.py` | Classe chaque désaccord du comparateur — jamais un compte global seul. | 4 |
| `justifier.py` | Génère puis contrôle `justifications.md` : preuve + verdict par désaccord, tranché sur la source originale. | 5–7 |
| `boucle_acceptation.py` | Orchestrateur : enchaîne le tout et écrit `ACCEPTATION.md`. | 1–8 |

Le rendu visuel des plans annotés n'est pas touché par la boucle ; il reste régi par la
spec unique [`docs/FORMAT-EXEMPLE.md`](FORMAT-EXEMPLE.md).

## CLI

```bash
python -m src.validation.boucle_acceptation <S> --workdir W --dossier D
```

- `<S>` — nom de la soumission (ex. `S-1844`) ;
- `--workdir W` — dossier de travail du relevé IA (`OUTBOX/<S>/travail` : nomenclature,
  occurrences, feuilles-classement, réserves, `.qpl` IA) ;
- `--dossier D` — dossier de la soumission dans le dépôt (`dossiers/<S>` : `reference/`
  et sorties).

La dernière ligne de la sortie est `VERDICT : …` (machine-lisible). Codes de sortie :

| Code | Signification |
|---|---|
| 0 | `PRÊT POUR DÉCISION FRANCIS` ou `VÉRIFICATION INCOMPLÈTE` — rien à corriger dans le relevé |
| 1 | `INVALIDE` ou `JUSTIFICATIONS REQUISES` — boucle bloquée avant la décision |
| 2 | Erreur d'entrée (workdir/dossier introuvable, gel illisible) |

## Artefacts (preuve sur disque)

| Artefact | Emplacement | Écrit par | Prouve |
|---|---|---|---|
| `controle-aveugle.json` | workdir | `aveugle.controler` | étape 1 (aucune référence estimateur dans le relevé IA) |
| `gel.json` | workdir | `gel.geler` / `verifier_gel` | étape 2 (empreinte de chaque artefact, revérifiée à chaque relance) |
| `comparaison-dupuis-qpl/ecarts-classes.csv` | dossier | `classer_ecarts.ecrire_sorties` | étapes 3–4 (contrat gelé : en-tête exact, une ligne par désaccord) |
| `comparaison-dupuis-qpl/ecarts-classes.md` | dossier | `classer_ecarts.ecrire_sorties` | étapes 3–4 (compte par classe + liste individuelle) |
| `justifications.md` | dossier | `justifier.generer_dossier` | étapes 5–7 (une ligne à trancher par désaccord ; jamais écrasé s'il existe) |
| `ACCEPTATION.md` | dossier | `ecrire_acceptation` | synthèse : étapes, compteurs par classe, verdict |

## Verdicts

| Verdict | Sens | Code |
|---|---|---|
| `INVALIDE` | Relevé non aveugle (étape 1) ou **gel violé** (étape 2) : les désaccords mesurés ne sont plus ceux du relevé d'aveugle. | 1 |
| `VÉRIFICATION INCOMPLÈTE` | Référence de l'estimateur absente, incomplète, illisible — ou comparaison en échec : rien n'est prouvé dans un sens ni dans l'autre (étape 8). | 0 |
| `JUSTIFICATIONS REQUISES` | Comparaison faite, désaccords classés, dossier de justification non entièrement tranché : preuve sur le plan exigée pour chaque ligne. | 1 |
| `PRÊT POUR DÉCISION FRANCIS` | Vérification complète : aveugle, gel intact, comparaison faite, aucun désaccord non tranché. La décision **finale** reste à Francis — ce verdict ouvre la décision, il ne la remplace pas. | 0 |

Le gel couvre aussi le `.qpl` IA quand il vit hors du workdir (dossier assemblé
`dossiers/<S>/planexpert/<S>.qpl`) : son empreinte sha256 rejoint `gel.json` avant la
comparaison. Modifier ou supprimer n'importe quel artefact gélé après le gel invalide la
boucle à la relance (verdict `INVALIDE`, motif « gel violé ») et la comparaison n'est
pas relancée.

Six classes de désaccords (étape 4), une ligne du CSV par désaccord : `omission`,
`en_trop`, `doublon`, `mauvaise_famille`, `mauvaise_portee`,
`mauvais_rattachement_feuille`. Chaque verdict de justification exige une **preuve non
vide** sur la source originale (« estimateur correct » compris) : `IA correcte`,
`estimateur correct` ou `ambigu → réserve`.

## Exemple minimal

```bash
# Relevé IA dans OUTBOX/S-1844/travail, référence dans dossiers/S-1844/reference/
python -m src.validation.boucle_acceptation S-1844 \
    --workdir OUTBOX/S-1844/travail --dossier dossiers/S-1844
# → - controle_aveugle : ok — 57 fichier(s) scanné(s)…
# → - gel : gelé (6 artefact(s))
# → - comparaison : ok ; - classement : 12 désaccord(s)…
# → VERDICT : JUSTIFICATIONS REQUISES            # exit 1
```

Une fois `justifications.md` rempli (preuve + verdict pour chaque ligne), relancer la même
commande : le dossier rempli n'est jamais écrasé, et une vérification entièrement tranchée
donne `VERDICT : PRÊT POUR DÉCISION FRANCIS` (exit 0).

## Intégrations et tests

- `releve/run.py` lance la boucle à la fin du parcours canonique (verdict consigné dans
  `STATUT.md`, jamais bloquant — `VÉRIFICATION INCOMPLÈTE` si la référence manque).
- `python -m src.validation.jeu_reference` affiche le verdict de chaque `ACCEPTATION.md`
  en section informative (lecture seule, jamais pass/fail).
- `tests/test_boucle_acceptation_e2e.py` rejoue la boucle **par son CLI** (subprocess,
  fixtures synthétiques) et vérifie sur disque chaque artefact, y compris la propriété
  clé : modifier le `.qpl` IA après le gel puis relancer → `INVALIDE « gel violé »`,
  comparaison non relancée.
- `tests/test_boucle_acceptation.py` — tests de niveau API des mêmes règles.