# S-0922 — pilote E-3 v2 : étoile de réserve E-3-188

Correction locale prête pour revue indépendante. L'étoile E-3-188 a été déplacée dans le blanc au-dessus de son symbole, libérant le libellé source `3(P1)`. Son cercle et ses coordonnées métier restent inchangés. Aucune généralisation aux autres feuilles. **QPL global : BLOCKED; aucune validation de chantier.**

## Pièces à ouvrir

- [Source / pilote v1 / pilote v2](preuves/E3-188-source-v1-v2.jpg) : même fenêtre source `(5484, 5610, 5835, 5926)` et même agrandissement pour les trois témoins. Cette capture a été réellement ouverte et inspectée après le rendu.
- [JPEG E-3 exact](paquet/S-0922-E-3-releve.jpg) : feuille entière, 12623 × 9467 pixels.
- [Diff minimal du renderer](delta-renderer-v1-v2.diff).
- [Localisation des pixels modifiés](preuves/delta-pixels-E3-188.json), [conservation et empreintes](preuves/conservation-v1-v2.json).
- [59 tests après rendu](tests-apres-rendu-v2.txt), [vérification du paquet sous Python -O](verification-paquet-v2.txt).

## Correction et preuves

La revue indépendante `task-6/independent-pilot-E3-v1/REVUE-INDEPENDANTE-PILOTE-E3.md` et son témoin `visual/E3-188-circuit-reserve.jpg` ont été lus. Leurs empreintes figurent dans `preuves/conservation-v1-v2.json`. La revue avait accepté la légende et les 14 contours G, tout en signalant l'étoile sur `3(`, défaut déjà présent en v3. Le numéro n'était ni effacé ni absent.

Dans le renderer existant, le décalage d'affichage de cette seule étoile passe de `(4, -6)` à `(-1, -13)` dans le référentiel de travail de largeur 1800. La condition exige à la fois le mode pilote et l'identifiant `E-3-188`. Les autres étoiles et le rendu hors pilote conservent leur comportement.

Le centre métier reste `(804.4, 826.2)`, famille `IS`, parent `EM#1`, modèle `STANPRO RMEA0WHUDC`, portée `INSTALLER`. La réserve reste : « * Faces et flèches de sortie à confirmer selon orientation du dessin. » Le CSV généré conserve les 223 lignes E-3, identiques octet par octet à v3.

La nouvelle boîte typographique de l'étoile `(5634, 5713, 5653, 5748)` ne contient aucun pixel source de luminance inférieure à 200. L'inspection confirme son emplacement dans le blanc, sous l'arc de porte et au-dessus du symbole. Le contrôle de luminance documente cette zone; il ne définit aucun seuil graphique universel.

La différence entre les JPEG v1 et v2 est contenue dans `(5632, 5712, 5688, 5784)`. **Aucun pixel ne diffère hors de la fenêtre locale `(5618, 5697, 5704, 5813)`.** Celle-ci couvre les deux positions de l'étoile et leur voisinage JPEG. Le cercle, la légende, les 14 G et le reste de la feuille sont donc identiques en pixels au pilote v1.

Le rectangle de l'ancien emplacement contient des franges colorées du texte source. Le premier test les avait prises à tort pour un reste d'étoile : 58 tests réussis et un échec, journal conservé dans `tests-premier-passage-v2.txt`. Le contrôle corrigé compare exactement la fenêtre `(5664, 5760, 5696, 5808)`, alignée sur les blocs JPEG 8 × 8, au raster source réencodé en qualité 96 sans sous-échantillonnage. Les pixels sont identiques. Aucun changement du renderer ni nouveau rendu n'a été nécessaire pour corriger ce test.

## Contrôles après le rendu final

- Rendu réel : `python -B travail/methode/render_sheet.py E-3 --pilot-granby`, code 0; journal `rendu-v2.txt`.
- **59 tests réussis en 79,30 s** : les 56 tests du pilote précédent, dont les mutations adverses du vérificateur, et trois contrôles de gel v1, localisation du delta et suppression du chevauchement.
- Vérificateur réel : `python -B -O paquet/methode/verify_delivery.py paquet`, code 0; **27 fichiers physiques et 26/26 empreintes conformes**.
- Le paquet v2 diffère du paquet v1 dans exactement trois fichiers : `S-0922-E-3-releve.jpg`, `methode/render_sheet.py`, `manifest.json`. Les 24 autres fichiers sont identiques.
- Les 16 fichiers métier historiques v3 sont intacts. Dans le paquet v2, 15/16 fichiers métier restent identiques à v3; seul le JPEG E-3 diffère. Aucun CSV, classeur, modèle, quantité, portée, centre ou réserve n'a changé.
- Les **59/59 fichiers gelés du pilote v1 et son ZIP sont intacts**. SHA-256 du ZIP v1 : `a02dcffb26f8693795f030d12165d5ba43e8aebaceae5c43464c86f1e11ab901`.
- E-5 reste inchangée : 72 repères réservés, dont E-5-072, portée `À PRÉCISER` et mention **DO NOT USE FOR CONSTRUCTION** conservées.

## Reproduction et portée

Le sous-dossier `paquet/` est le paquet complet de 27 fichiers. `travail/` contient le PNG source E-3, les scripts existants, le CSV réellement généré et les vues d'inspection. Le JPEG de travail, identique au JPEG livré, n'est pas dupliqué dans l'archive.

Depuis ce dossier, le rendu se rejoue avec la commande ci-dessus; la vérification de livraison est autonome. La suite complète se lance avec `python -B -m pytest tests -q --basetemp=<nouveau-dossier-temporaire>`. Ses tests de conservation exigent les témoins adjacents `../releve-page-par-page/` (v3) et `../pilote-graphique-E3-v1/`, dont son checkpoint et le ZIP au chemin consigné. Ces témoins historiques ne sont pas dupliqués dans l'archive v2. Le rendu exact utilise l'environnement Windows et Arial existants.

Le verdict de ce delta est laissé à la revue indépendante. Ce travail ne rouvre ni le QPL ni les autres dossiers, ne certifie aucune exhaustivité métier ni aucun taux de 95 %, et ne généralise pas le pilote. Aucun push, merge, publication ou changement d'UI n'a été effectué.

Checkout : `C:\Users\fvegi\Documents\codex\2026-10-02\task-2\S-0922-review`.
Branche : `local/S-0922-repair-20261002`, base `0085374ee0eb971b2700b91a986f4935c89f8887`.
