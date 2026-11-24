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
| `recalage_sources.py` | En plans seuls : rattache les fonds à un PDF/page et une révision, sans utiliser les marques pour choisir ou déplacer une feuille. | 3 |
| `classer_ecarts.py` | Classe chaque désaccord du comparateur — jamais un compte global seul. | 4 |
| `justifier.py` | Génère puis contrôle `justifications.md` : preuve + verdict par désaccord, tranché sur la source originale. | 5–7 |
| `boucle_acceptation.py` | Orchestrateur : enchaîne le tout et écrit `ACCEPTATION.md`. | 1–8 |

Le rendu visuel des plans annotés n'est pas touché par la boucle ; il reste régi par la
spec unique [`docs/FORMAT-EXEMPLE.md`](FORMAT-EXEMPLE.md).

## CLI

```bash
RELEVE_BASE=/chemin/passe-isolee uv run releve/run.py --aveugle /chemin/INBOX/<S>
python -m src.validation.boucle_acceptation <S> --workdir W --qpl-ia Q --dossier D --sortie A
```

- `<S>` — nom de la soumission (ex. `S-1844`) ;
- `--workdir W` — dossier de travail du relevé IA (`OUTBOX/<S>/travail` : nomenclature,
  occurrences, feuilles-classement, réserves, `.qpl` IA) ;
- `--dossier D` — dossier de la soumission (`reference/` pour la référence). Sans `--sortie`, les
  comparaisons historiques écrivent dans `D` ; **en plans seuls, une sortie distincte est obligatoire**.
- `--sortie A` — dossier séparé pour la comparaison et les justifications. Le lanceur standard enregistre
  ces résultats dans le sous-dossier `acceptation/` de la passe, sans modifier les comparaisons historiques.
  En plans seuls, rester hors de `D`, de l'INBOX et de `travail/`.
- `--qpl-ia Q` — chemin du projet produit par **la passe courante**. Avec `--gel-seul`,
  aucun dossier `D` n'est nécessaire et aucune référence n'est ouverte.
- Une reprise modifiant le relevé se fait dans un nouveau dossier : le lanceur refuse
  d'écraser un relevé déjà gelé. La comparaison revérifie le scan sans réécrire son rapport initial.

La dernière ligne de la sortie est `VERDICT : …` (machine-lisible). Codes de sortie :

| Code | Signification |
|---|---|
| 0 | `PRÊT POUR DÉCISION FRANCIS` ou `VÉRIFICATION INCOMPLÈTE` (code informatif ; lire le verdict) |
| 1 | `INVALIDE` ou `JUSTIFICATIONS REQUISES` — boucle bloquée avant la décision |
| 2 | Erreur d'entrée (workdir/dossier introuvable, gel illisible) |

## Artefacts (preuve sur disque)

| Artefact | Emplacement | Écrit par | Prouve |
|---|---|---|---|
| `controle-aveugle.json` | workdir | `aveugle.controler` | étape 1 (aucune référence estimateur dans le relevé IA) |
| `gel.json` | workdir | `gel.geler` / `verifier_gel` | étape 2 (empreinte de chaque artefact, revérifiée à chaque relance) |
| `comparaison-dupuis-qpl/ecarts-classes.csv` | dossier | `classer_ecarts.ecrire_sorties` | étapes 3–4 (contrat gelé : en-tête exact, une ligne par désaccord) |
| `comparaison-dupuis-qpl/ecarts-classes.md` | dossier | `classer_ecarts.ecrire_sorties` | étapes 3–4 (compte par classe + liste individuelle) |
| `comparaison-dupuis-qpl/recalage-pages.csv` | `--sortie` (plans seuls) | `recalage_sources.ecrire` | identité candidate, preuve, couverture, révision et nombre de lignes par page |
| `comparaison-dupuis-qpl/marques-hors-comparaison.csv` | `--sortie` (plans seuls) | `recalage_sources.ecrire` | une ligne par marque non évaluée, en coordonnées natives, y compris sur une version remplacée |
| `justifications.md` | dossier | `justifier.generer_dossier` | étapes 5–7 (une ligne à trancher par désaccord ; jamais écrasé s'il existe) |
| `ACCEPTATION.md` | dossier | `ecrire_acceptation` | synthèse : étapes, compteurs par classe, verdict |

## Verdicts

| Verdict | Sens | Code |
|---|---|---|
| `INVALIDE` | Relevé non aveugle (étape 1) ou **gel violé** (étape 2) : les désaccords mesurés ne sont plus ceux du relevé d'aveugle. | 1 |
| `VÉRIFICATION INCOMPLÈTE` | Référence de l'estimateur absente, incomplète, illisible — ou comparaison en échec : rien n'est prouvé dans un sens ni dans l'autre (étape 8). | 0 |
| `JUSTIFICATIONS REQUISES` | Comparaison faite, mais désaccords, corrections, ambiguïtés, contrôle qualité ou anomalies de recalage encore ouverts. | 1 |
| `PRÊT POUR DÉCISION FRANCIS` | Vérification complète de la **comparaison de repères**, pas une attestation de chiffrage ou une autorisation d'envoi. La décision finale reste à Francis. | 0 |

Le gel couvre aussi le `.qpl` IA quand il vit hors du workdir (dossier assemblé
`dossiers/<S>/planexpert/<S>.qpl`) : son empreinte sha256 rejoint `gel.json` avant la
comparaison. Modifier ou supprimer n'importe quel artefact gélé après le gel invalide la
boucle à la relance (verdict `INVALIDE`, motif « gel violé ») et la comparaison n'est
pas relancée.

Six classes de désaccords (étape 4), une ligne du CSV par désaccord : `omission`, `en_trop`, `doublon`, `mauvaise_famille`, `mauvaise_portee`,
`mauvais_rattachement_feuille`. Chaque verdict de justification exige une **preuve non
vide** sur la source originale (« estimateur correct » compris) : `IA correcte`,
`estimateur correct` ou `ambigu → réserve`.

## Limites connues du contrôle à l'aveugle

Le contrôle d'aveugle (étape 1) voit un export de l'estimateur fourni à tort dans
l'INBOX par la voie principale du pipeline : `prepare.py` le classe « estimateur » et
consigne ce classement dans `inventaire.json` (scanné, contenu → « contenu-estimateur »)
— le workdir est alors reconnu non aveugle, verdict `INVALIDE`. Si en plus le nom du
PDF d'entrée porte « dupuis »/« estimateur »/« releve »/« plan expert »,
`estimateur/pages.csv` est détecté lui aussi (« contenu-dupuis »…).

Tout fichier sous `estimateur/` ou `reference/` dans `travail/` est refusé, même
s'il est binaire et porte un nom neutre. Le pré-vol `--aveugle` refuse aussi avant
préparation le PDF explicitement marqué comme relevé. Il n'authentifie pas pour
autant l'origine d'un scan anonyme : conserver la provenance et les empreintes.
Le gel strict revérifie le jeu de PDF depuis `inventaire.json`, y compris un ajout,
un remplacement ou une suppression postérieurs au gel.

## Recaler les fonds en plans seuls

Après établissement du gel, prendre **les rasters effectivement référencés par le QPL humain** et
les placer dans `D/reference/rasters/` (hors INBOX, hors Git). Vérifier à l'œil sur les deux fonds le
cartouche complet (dossier, feuille, titre, dernière révision) et au moins trois repères fixes et bien
répartis (coins de dessin ou axes, pas les marques ni uniquement les bords du papier).

`D/reference/recalage-pages.json` décrit ce contrôle. Il contient `version: 1`, `qpl_sha256` (empreinte
du QPL humain), éventuellement `documents` (nom de document humain → empreinte d'un PDF gelé si le nom
d'entrée a changé), et `calages`, indexé par le `FileName` exact du plan dans le QPL :

| Champ de `calages[FileName]` | Valeur à relever |
|---|---|
| `pdf_sha256`, `page` | PDF **dans le gel**, et numéro physique de sa page à partir de 1. |
| `feuille`, `revision` | Identifiant de feuille et date ISO de sa révision courante, lues dans les cartouches des deux fonds. |
| `raster_sha256` | Empreinte du raster humain effectivement contrôlé. Ne pas utiliser un export du relevé IA à sa place. |
| `preuve`, `preuve_zero` | Désigner les témoins contrôlés. `preuve_zero` obligatoire sur une page humaine sans marques : prouver le périmètre examiné, pas simplement l'absence de compteurs dans le QPL. |
| `ancres` | Couples `[[x_raster, y_raster], [x_pdf, y_pdf]]`, chaque point normalisé dans les dimensions affichées de sa page, origine en haut à gauche. |

La boucle lit `feuilles.csv` du gel, refuse les correspondances contredisant l'inventaire, confirme le
cartouche du PDF et contrôle le recouvrement d'encre global et dans le cartouche à la transformation
donnée par les ancres. Ce dernier contrôle ne remplace pas la lecture de la date dans le cartouche
humain. Une rotation non vérifiée, un fond trop différent ou une feuille ambiguë restent en réserve.
Le recouvrement des marques ne prouve ni un doublon de page ni une révision. Un alias sans `calages`
sert uniquement au triage. Une version présumée remplacée n'est ni reportée ni déclarée résolue.

Le gel est revérifié après lecture de la référence, avant écriture des écarts. Si le périmètre n'est pas
entièrement attesté, la boucle rend **VÉRIFICATION INCOMPLÈTE** même si le CSV d'écarts est vide. Les
longueurs ne sont toujours pas comparées. Le benchmark `jeu_reference` garde son appariement historique :
il ne valide ni le nouveau recalage des fonds ni la couverture du devis.

## Exemple minimal (comparaison historique)

```bash
# Relevé IA dans OUTBOX/S-1844/travail, référence dans dossiers/S-1844/reference/
python -m src.validation.boucle_acceptation S-1844 \
    --workdir OUTBOX/S-1844/travail --dossier dossiers/S-1844
# → - controle_aveugle : ok — 57 fichier(s) scanné(s)…
# → - gel : gelé (6 artefact(s))
# → - comparaison : ok ; - classement : 12 désaccord(s)…
# → VERDICT : JUSTIFICATIONS REQUISES            # exit 1
```

Relancer la comparaison après avoir rempli `justifications.md` ; ce fichier n'est pas
écrasé. « estimateur correct » demande une correction réelle et un nouveau contrôle,
« ambigu → réserve » reste bloquant, même si toutes les cases sont remplies. Ne pas
présenter une révision faite après ouverture de la référence comme une nouvelle passe aveugle.

## Intégrations et tests

- `releve/run.py` lance la boucle à la fin du parcours canonique (verdict consigné dans
  `STATUT.md`, `VÉRIFICATION INCOMPLÈTE` si la référence manque). Le chiffrage de travail est
  écrit dans `chiffrage-interne/` et n'est pas copié sur le miroir Drive.
- `python -m src.validation.jeu_reference` affiche le verdict de chaque `ACCEPTATION.md`
  en section informative (lecture seule, jamais pass/fail).
- `tests/test_boucle_acceptation_e2e.py` rejoue la boucle **par son CLI** (subprocess,
  fixtures synthétiques) et vérifie sur disque chaque artefact, y compris la propriété
  clé : modifier le `.qpl` IA après le gel puis relancer → `INVALIDE « gel violé »`,
  comparaison non relancée.
- `tests/test_boucle_acceptation.py` — tests de niveau API des mêmes règles.