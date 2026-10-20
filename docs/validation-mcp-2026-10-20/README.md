# Validation du serveur Expert estimateur — 20 octobre 2026

## Verdict et périmètre

La mission complète **n'est pas acceptée** : le fichier E05 fourni est un relevé déjà
annoté, et le démarrage MCP mesuré dépasse le seuil de 0,2 seconde. Les correctifs
et les tests du serveur ne constituent pas une validation électrique d'E05.

Les résultats reproductibles sont conservés dans ce dossier :

- `audit-e05.json` : identité des fichiers, préparation et extraction effectivement rejouées;
- `pytest-execution.json`, `pytest.log`, `pytest.xml` : commande, code de sortie et résultats de la suite;
- `demarrage-mcp.json` : temps jusqu'à la réponse réelle `initialize`, puis contrôle des catalogues;
- `qualite-code.json` : contrôles Ruff et Pyright LSP des nouveaux modules.
- `sources-verifiees.json` : empreintes des douze fichiers Python modifiés ou ajoutés.

Validation exécutée dans `.venv` :

| Contrôle | Résultat |
|---|---|
| Suite complète `pytest tests -q` avec répertoire temporaire dédié | 361 réussites, 1 test POSIX ignoré; code 0; 776,41 s |
| Dernier correctif de classement, après la collecte de la suite complète | 24 réussites; code 0; 23,92 s |
| Jeu de référence, après la dernière modification de `releve/` | 5 dossiers, aucune régression; code 0 |
| Livrables réels du parcours synthétique | 5 repères, 5 unités, MO non chiffrable sans heures sourcées; contrôle visuel 5/5 |
| Démarrage MCP, 5 essais | Fonctionnel, mais seuil de 0,2 s dépassé; benchmark code 1 |

Les contrôles Ruff et LSP sont propres sur huit fichiers vérifiés. Le module
historique `blocs_vers_releve.py` conserve 19 diagnostics Ruff et 5 diagnostics LSP antérieurs, comparés
au HEAD et détaillés dans le reçu; les outils renvoient code 1 pour ces diagnostics.
Ce rapport ne prétend pas que le dépôt entier est exempt d'erreurs statiques.

## Source E05 et signatures

`travail-mcp/TEST-PLAN-RAW/entree/E05-Electricite.pdf` et
`dossiers/HR26-14-essai/E05/HR26-14-E05-releve-1page.pdf` ont la même empreinte :
`24e22753712a84ff3522e898586824eba08afd4df1447af28c2c45dace4efcb8`.
L'inspection visuelle confirme l'encadré de relevé et les pastilles préexistantes.

Le replay diagnostique initial a produit un raster de 5694 × 3796 pixels,
12 tuiles, **249 signatures distinctes et 4 824 blocs candidats**.
Les **106** signatures mentionnées dans la mission correspondent au sous-ensemble
présent au moins trois fois. Ce nombre ne prouve ni 106 familles d'appareils ni
106 symboles électriques. La première planche contient notamment des lettres
vectorisées et des annotations. Aucun appareil n'a été reconnu par la bibliothèque;
le pipeline initial a renvoyé `produit: false`, sans livrable E05.

Le contrôle corrigé refuse désormais cette source avant extraction, y compris en
reprise. Aucun apprentissage de signatures n'a été effectué à partir de ce relevé.
Les signatures rares d'un plan admis sont maintenant signalées dès une occurrence.
Le test d'intégration suit une signature unique jusqu'à sa décision explicite,
puis vérifie la reprise et la réutilisation de la bibliothèque.

Le candidat trouvé sur le Drive, dans
`AI/Soumission 2026/HR26-14 - OMH Haut-Richelieu/01-projet-vide/`,
est un PDF raster de 28 pages sans couche texte ni blocs CAD extractibles.
Ce constat ne prouve pas l'absence d'un original vectoriel ailleurs.
Une source E05 originale adéquate reste nécessaire pour valider les quantités.

## Correctifs livrés

- Refus des références explicitement nommées ou portant l'encadré et le décompte
  caractéristiques d'un relevé, même après les trois premières pages.
- Export Excel alimenté par les occurrences texte **et** visuelles, avec multiplicateurs.
- Maintien du CSV historique par repère; ajout d'un CSV de quantités agrégées.
- Erreurs d'export remontées; aucun succès annoncé après un échec Excel.
- Planches de contrôle générées avec les livrables MCP et incluses dans l'archive.
- Exclusions `1`, `oui`, `x`, `true` cohérentes entre contrôle, comptage et rendu.
- MO calculée à 124 $ CAD/h uniquement avec `heures_unitaires` et `source_heures`
  dans la nomenclature. Sans heures sourcées, le total est non chiffrable, jamais
  présenté comme zéro. La réserve de ventilation INSTALLER / CONSERVER / ENLEVER /
  RELOCALISER est affichée dans le JSON, le rapport et le classeur.
- Provenance des rapports tirée des fichiers, pages, feuilles et occurrences du dossier
  courant; retrait des références et résultats historiques présentés à tort comme preuves.
- Classement des feuilles sans restriction à un ancien format de numéro : une feuille de
  plan générique doit contribuer aux quantités, et pas seulement porter des repères au PDF.

## Mesure du démarrage

```text
.venv/Scripts/python.exe outils/mesurer_demarrage_mcp.py --essais 5 --rapport docs/validation-mcp-2026-10-20/demarrage-mcp.json
```

La mesure commence à la création du processus et finit à la réception complète
de `initialize`. Elle vérifie ensuite outils, ressources, prompts et fermeture
avec code zéro. Les caches du système ne sont pas vidés. Le benchmark retourne
**1** lorsque la limite stricte est dépassée, même si le serveur fonctionne.
Le succès d'un simple import ou d'un processus lancé n'est pas assimilé à un serveur prêt.

Dernière série, sans autre test ni agent de cette mission en parallèle :
**0,930 à 1,290 s, médiane 1,002 s**. Les cinq processus serveur ferment avec code 0,
sans stderr; chacun expose 19 outils, 4 ressources et 1 prompt.
Le programme de mesure termine avec **code 1** parce que le seuil demandé est dépassé.

Le profil initial attribue environ 0,893 s à l'import du SDK MCP 2.3.0.
Le SDK et le protocole n'ont pas été remplacés pour produire un faux signal de disponibilité.
`uv pip check --python .venv/Scripts/python.exe` a confirmé la compatibilité des
60 paquets installés; les dépendances du pipeline sont aussi importées réellement
par les tests, sans ignorer celles qui seraient manquantes.

## Preuve de livraison sur plan synthétique

Le dossier `parcours-auto-synthetique/` conserve la sortie réelle du deuxième
dossier du test d'apprentissage : PDF annoté, `.qpl` et son fond de plan, BOM,
quantités, estimation MO, rapport de rendu et planche de contrôle.
Il s'agit d'un plan synthétique de test, **pas d'E05**.

Inspection directe de la planche : **5/5 repères correctement centrés**, sans
case fausse. Le plan d'ensemble montre les cinq boîtiers marqués, les quatre
losanges et la forme unique explicitement ignorés, et l'encadré hors des symboles.
Les étiquettes BJ-01 à BJ-05 sont visibles sur le PDF. Le nombre de repères
correspond aux occurrences, au BOM, aux quantités agrégées et au projet exporté.
Le bordereau cite `plans.pdf, page 1, feuille plans-p01 ; bloc S001`.
Les vignettes de contrôle coupent une partie du texte des étiquettes; celles-ci
sont entièrement lisibles sur le plan. `preuve.json` conserve le score et les empreintes.

## Conditions de test et limites

La première exécution complète a terminé avec code 1 : 252 réussites, deux échecs,
57 erreurs et un test ignoré. Son répertoire temporaire partagé a disparu pendant
les sessions pytest parallèles; un test a aussi rencontré le contrat BOM intermédiaire.
La suite finale utilise un `--basetemp` dédié sous `travail-mcp/` et conserve ses résultats.
Ce changement isole les artefacts d'essai; il ne retire aucun test.

La première suite isolée a passé 342 tests, avec un test POSIX ignoré, en 941,01 s.
L'inspection ultérieure des livrables a détecté une incohérence non couverte :
cinq repères rendus, mais zéro quantité agrégée pour une feuille `plans-p01`
classée à tort comme détail. Des assertions de quantités et de coût non chiffrable
ont été ajoutées au parcours complet après correction de ce classement.
Le dernier ajustement, qui exclut les feuilles spécialisées dès l'extraction,
a été vérifié par les 24 tests ciblés après leur ajout : ces tests ne sont pas tous
inclus dans le nombre 361, puisque la suite complète les avait déjà collectés.

Le test POSIX préexistant est ignoré sous Windows. L'acceptation native du `.qpl`
par Plan Expert et la comparaison d'E05 à l'estimateur ne sont pas certifiées ici.
La revue indépendante approuve les correctifs du serveur; elle ne lève pas ces
limites ni les deux conditions de mission encore insatisfaites.
