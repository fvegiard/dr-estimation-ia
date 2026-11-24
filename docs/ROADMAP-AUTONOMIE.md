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
| G8 | Soumission autonome sur un dossier neuf | comparaisons sourcées, longueurs, chiffrage complet et décision de Francis | **OUVERTE** — les deux pilotes restent non conformes ; aucun dossier neuf accepté ni prix de soumission émis |

### Mise à jour mesurée — pilotes stricts du 24 novembre 2026

Voir [la preuve de rejeu et les données disponibles](preuves/autonomie-pilote/README.md),
[S-1844](../dossiers/S-1844/ACCEPTATION.md) et [S-1715](../dossiers/S-1715/ACCEPTATION.md).
Les états ci-dessous sont les plus récents ; le diagnostic plus bas documente le point de départ.

| Chantier | Livré au pilote | Encore ouvert |
|---|---|---|
| P1 / G0 | 455 tests ; benchmark historique rejoué 2× ; HR26-14 reconfirmé | Le benchmark historique des cinq QPL complets ne valide pas les 11 dossiers par poste. |
| P2 | S-1715 plans AO + ELE-001 et ELE-002 récupérés, 12 feuilles actives sur 21 | Avis textuels et autres plans manquants ; accès Drive à rétablir. |
| P3 | Règles locales S-1844 pour prises et projecteurs ; 199 repères contre 1 au départ ; bibliothèque inchangée | Reconnaître et vérifier les autres familles, dont la dépose. Ne pas transformer 724 signatures en quantités. |
| P4 / G4 | Quantités par portée ; facteurs à source obligatoire et quantités de note `source_qte` testés | Extraire et justifier ces règles sur les dossiers réels, comparer les sous-types et sécuriser les reports entre révisions. |
| P5 / G5 | 17 axes E400, 93,41 m horizontaux attestés dans QPL, rapport et BOM | Câbles, descentes, autres parcours, validation native et même périmètre que la référence. |
| P6 / G6 | Export interne sourcé par poste, sans 0 h de repli ; un poste tarifé, six réservés et un conservé sur S-1844 | Couverture exhaustive, lots et taux confirmés, gabarit client soumis au verdict. |
| P7 / G7 | 19 sorties D/E identiques ; comparaison séparée après gel, 2 dossiers pilotes examinés | Recalage fiable pour les pages humaines, preuves individuelles, révision et recontrôle ; pas de vote pour la route agent. |
| P8 / G8 | Rotation MCP locale vérifiée ; ancien bearer refusé | Reconfigurer les clients distants sans journaliser la clé. Terminer les mesures, puis prouver le parcours sur dossier neuf avant décision de Francis. |

**Rattachement après gel (P7).** La [comparaison stricte des fonds](boucle-acceptation.md#recaler-les-fonds-en-plans-seuls)
ne redirige plus une page vers une feuille qui a seulement des marques voisines. Sans les rasters humains,
les deux pilotes donnent **VÉRIFICATION INCOMPLÈTE** ; les nombres historiques restent des diagnostics.
Les 242 marques S-1715 associées par nom à des éditions présumées remplacées ne sont pas reportées vers ELE-002.
Les avis écrits, la validation des longueurs, le chiffrage et le dossier neuf restent des conditions de G8.

**Reconnaissance S-1844 (P3/P4).** La [passe F](preuves/autonomie-pilote/recalage-et-d4.md) ajoute un
seul D4-N confirmé sur E300 (200 repères, les 199 précédents conservés). Les têtes non typées et la
dépose restent à relever. Les métrés E400 ne changent pas.

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
- **Rapatriés le 2026-11-24 depuis GitHub** (branche `data-hr26-14-plans` du dépôt, intégrité
  vérifiée) : `INBOX/HR26-14/` (plans-entree 28 p. + addenda-01 complet), `INBOX/S-1844/plans.pdf`
  (12 p., SAQ Varennes), `INBOX/S-1715/Addenda-ELE-002-Plans.pdf`, corpus Dupuis
  (`apprentissage/qpl-manifest.json`), et **le gold complet `apprentissage/hr26-14-exemplaire/EXEMPLE.pdf`
  (87 p., sha256 0861bc3a…eb84b correspondant à SOURCE.txt — la porte `verify_exemple` du rendu octet-près
  devient jouable hors du poste de Francis)**.
- G8 : la boucle `python -m src.validation.boucle_acceptation <S> --workdir W --dossier D` +
  référence de l'estimateur.

### Diagnostic initial — bibliothèque de blocs, bureau de S-1844 (SAQ Varennes)

Premier relevé à l'aveugle de S-1844 par la route blocs (2026-11-24, route déterministe) :
pipeline rendu jusqu'à Plans-annotes, mais identification incomplète — 836 signatures indexées, **724
signatures fréquentes à étiqueter** (`OUTBOX/S-1844/travail/blocs-a-etiqueter.md`), seulement 3
auto-étiquetées depuis la bibliothèque S-1902 (HF Experts-Conseils) → 1 occurrence, état
« TERMINÉ — À VÉRIFIER » honnête, pas de quantités livrées. L'étiquetage se fait UNE fois
(vignettes ×8 + légende E100, jamais deviné : dans le doute on laisse inconnue) et reste appris
dans `releve/bibliotheque-blocs.csv` pour ce bureau comme pour tous. Suite exacte : étiqueter par
vagues (découper sous 20 images/tour), rejouer `run.py S-1844`, classer les désaccords vs la
référence Dupuis (`dossiers/S-1844/reference/`), justifier sur le plan, ACCEPTATION.md.

## Règles qui ne bougent pas avec l'autonomie

1. Jamais en dessous de l'estimateur (boucle d'acceptation) ; « vérification incomplète » vaut
   mieux qu'une certification sans preuve.
2. Un rapport d'agent n'est pas une preuve : lire le fichier produit, rejouer la commande soi-même.
3. Rien n'est inventé : chaque quantité vient d'un symbole étiquette, d'une cédule, d'une note ; le
   doute va en réserve.
4. Le gold HR26-14 ne se corrige pas ; on corrige la spec.
5. Le verdict final de soumission reste à Francis.

## Plan complet (P1-P8) — tout ce qu'il y a à faire, ce qui manque pour y arriver

État mesuré au 2026-11-24 (preuves du jour : démarrage 26,6-34,4 ms / 46,8-86,2 ms conteneur,
421 tests, jeu_reference rejoué identique octet-par-octet deux passages, gold 0861bc3a vérifié,
relevé S-1844 à l'aveugle : 724 sigs à étiqueter, occurrences ≈ 0, « À VÉRIFIER » honnête).

### P1 — Socle (FAIT, 2026-11-24)
Démarrage MCP < 0,2 s dans les deux environnements, suite verte, socle rejoué identique. Preuve :
`.venv/bin/python outils/mesurer_demarrage_mcp.py --essais 5 --limite 0.2 --rapport mcp-demarrage-rapport.json`,
`python -m pytest tests -q`, `python -m src.validation.jeu_reference` exit 0.

### P2 — Données (rapatriement des plans par dossier)
À faire : pour chacun des dossiers, le(s) PDF de plans + addendas d'origine dans `INBOX/<S>/` —
jamais le relevé humain dans l'INBOX. Déjà rapatrié : **S-1844 ✓ (12 p.), HR26-14 ✓ (28 p. +
addenda-01), S-1715 ✓ partiel (addenda ELE-002 seul, plans d'AO à suivre)** ; à rapatrier de
Drive/SharePoint/Legion : plans AO de S-1715 complets, S-1714, S-1769 (AO + addenda), S-1811, et
pour la re-route complète des 11 : S-1857, S-1689, S-1693, S-1695, S-1797, S-1808. Vérifier aussi
la branche `releve/S-1902-georgette-lepage` pour les plans de S-1902. Preuve par passe :
`sha256sum INBOX/<S>/*.pdf` au journal + inventaire.json du runner.

### P3 — Bibliothèque de signatures multi-bureaux
À faire : une campagne d'étiquetage **une fois par bureau d'ingénieurs** (vignettes ×8 + légende
lue — jamais deviné, dans le doute on laisse inconnue). Ne publier une règle dans
`releve/bibliotheque-blocs.csv` qu'après validation sur les collisions, variantes et portées.
Les 724 signatures fréquentes de S-1844 restent à comprendre : nombre d'entre elles sont du fond
de plan. Le pilote local ci-dessus n'entraîne pas la bibliothèque partagée.

### P4 — Précision de comptage fine
À faire, mesuré vs le jeu de référence à chaque pas : multiplicateur des unités/chambres types
branché dans la route blocs (le fichier existe sur la chaîne MCP) ; détection vectorielle des
symboles sans étiquette (la forme, pas le texte) ; « une ligne de légende = un compteur »
(variantes fusionnées, interrupteurs S-1689) ; notes de plan (« prévoir N par logement », S-1714 :
140 prises d'échangeur) → N objets ; sous-types (tension, pôles, calibre ; S-1808) ; stabilité de
la route agent (double passe + vote). Preuve : seuil G2/G3 mesuré (écarts par poste ≤ 10 %, 0
manquant non signalé) sur la passe rejouée des 11 dossiers ; test par item dans `tests/`.

### P5 — Métré des longueurs (câbles et conduits — l'essentiel des heures d'une soumission)
À faire : compléter les 17 tracés vérifiés E400 par des parcours sourcés de câbles et conduits.
`src/cablage/compute_arteres.py` et `inject_lines.py` restent disponibles pour les artères
configurées ; ne pas utiliser la distance de Manhattan comme substitut à un parcours réel non établi.
Comparer les longueurs par portée à la référence et vérifier le QPL dans Plan Expert.

### P6 — Chiffrage complet sourcé
À faire : couverture du catalogue Dupuis mesurée (quels postes ont prix/heures, lesquels pas) ;
soumission générée automatiquement au gabarit DR (ReportLab) — la première existe (S-1902, 194 000 $).
Manque : mesure de couverture + les postes non chiffrables listés explicitement (jamais 0 h par
défaut, jamais inventés — le livrable marque « poste non chiffrable » avec réserve).

### P7 — Boucle d'acceptation rejouée sur les 11 dossiers, chacun jusqu'au verdict
À faire : par dossier, la boucle complète (aveugle → gel → comparaison → classement → justification
sur le plan → corriger/revérifier → `ACCEPTATION.md`). Manque mesuré : ACCEPTATION.md présent pour
2 dossiers seulement (S-1844, S-1902) ; à produire par dossier : S-1857 (prises E407-E408 + addenda
ADME-01 complet), S-1689 (interrupteurs fusionnés, 14 luminaires B→D), S-1769 (4 corrections),
S-1715 (mécanique +20 %, portes : référence en erreur), S-1844 (doublons + 12 têtes — en cours
dans P3), S-1808 (TYPE D→C, 4 objets), S-1811 (corrections légères), S-1695 (chambres types −64 %),
S-1693 (salle électrique, interrupteurs, fausses gâches), S-1797 (alarme, chauffage, distribution),
S-1714 (enseignes, prises d'échangeur, allocations logements, 20 conduits).

### P8 — Soumission autonome sur un dossier NEUF + opération
À faire : un dossier jamais relevé (prochain appel d'offres), de bout en bout sous la boucle
complète, verdict final à Francis (jamais à l'IA) ; puis opération journalière : le service MCP
déjà déployé (`expert-estimateur-svc`, 8765, rollback taggé), doc d'usage pour l'équipe,
surveillance des erreurs, le mécanisme d'apprentissage des bureaux maintenu. Manque : rien
d'opérationnel à coder — le service roule ; il faut la formation + le pilotage.

### Ordre et dépendances

P1 ✓ → P2 (données) → P3 (bibliothèques par bureau, nécessaire à toute identification) → P4
(précision, nécessaire à G2/G3) ∥ P5 (longueurs, nécessaire aux heures) → P6 (chiffrage,
dépend de P4+P5) → P7 (acceptation, dépend de P3+P4) → P8 (soumission autonome, dépend de tout).
P3 ∥ P2 : on étiquette le bureau d'un dossier dès que ses plans sont là.

### Risques récurrents (rappel)

Le gold ne se corrige pas (on corrige la spec) ; la voie par agent ne se vérifie que par la route
déterministe + la double passe quand elle existe ; la VM Plan Expert (vérification native, la plus
forte) reste un outil Windows/Legion — inutilisable ici, seule la comparaison déterministe est
possible sur cette machine ; un poste sans heure sourcée reste réservé, jamais 0 h.

