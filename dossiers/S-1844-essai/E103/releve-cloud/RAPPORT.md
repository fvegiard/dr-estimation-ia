# TEST-E103 — relevé cloud (voie B)

- **Source** : `dossiers/S-1844-essai/E103/E103-page6.pdf` (1 page, 3456 × 2592 pt, feuille E103 « DÉTAILS — CONTRÔLE D'ÉCLAIRAGE », SAQ Varennes, Direktion 360).
- **Voie** : B — session cloud, fonctions Python `serveur_mcp.serveur` avec `ESTIMATEUR_BASE=$PWD/travail-mcp` :
  `relever_automatique` → `etiqueter_signatures(apprendre=True)` → `relever_automatique(reprendre=True)` (une seule reprise).
- **Modèle** : `claude-opus-5-5` (configuré pour la session, observé dans le contexte système ; le modèle servant un tour peut différer).
- **Date** : 2026-10-19.

## Résultat

| Famille | Code | Repères | Détail lu à l'étiquette du plan | Statut |
|---|---|--:|---|---|
| BOITIER NLIGHT (commande) | NL | 20 | DP1 ×8 (NPP16 D EFP 347), DP2 ×4 (NPP PCD EFP), PP1 ×2 (NPP20 PL BP), SO3 ×2 (WSXA MWO PDT D WH), SO4 ×4 (WSXA MWO PDT WH) | CONFIRMÉ |
| INTERRUPTEUR NLIGHT (commande) | NS | 3 | SW1 ×2 (NPODMA WH), SW6 ×1 (NPOD TOUCH WH) | CONFIRMÉ |
| **Total** | | **23** | ID #13, #16 à #37 (#14 et #15 absents de cette feuille) | |

Contre-vérification indépendante : comptage des mots DP1/DP2/PP1/SO3/SO4/SW1/SW6 du PDF = 8+4+2+2+4+2+1 = 23, chacun au centre d'un bloc relevé.

## Signatures (étape 2)

31 signatures inconnues (≥ 3 instances) + 2 rares sur le plan. Seuls les blocs du **plan d'étage** sont des appareils ;
les autres sont dans les schémas types de câblage nLight (détails 1 à 10), l'instruction code-barres, le détail CAT5 et le cartouche.

| Signature | Instances | Étiquette | Apprise (bibliothèque) |
|---|--:|---|---|
| S004 | 20 | BOITIER NLIGHT / commande / carré / NL | oui |
| S059 | 2 | INTERRUPTEUR NLIGHT / commande / carré / NS | oui |
| S139 | 1 | INTERRUPTEUR NLIGHT / commande / carré / NS | oui |
| S006 S007 S009–S015 S017 S020–S028 S030–S035 S037–S041 (30) | 3 à 16 | IGNORER (schémas types, CAT5, cartouche) | oui |

33 lignes ajoutées à `releve/bibliotheque-blocs.csv` (source `TEST-E103 Sxxx (LLM client MCP)`).
Non réétiquetées : S001 (IGNORER) et S002 (SORTIE DATA, ø 0–6,5 pt → aucune instance à 16 pt) déjà dans la bibliothèque ;
ce sont des doublons superposés des mêmes 23 boîtiers — aucun double compte (23 positions uniques).

## Contrôle visuel (étape 4) — fait par la session, sans sous-agent

Images vues : `E103_annote.png` (ZIP), recadrage du plan, planche ×4 des 23 repères (`controle-23-reperes.png`, rendue depuis `TEST-E103-RELEVE.pdf`), `E103_bordereau_01.png`.

- Pastille sur le bon symbole : **23/23**
- 1 symbole = 1 repère : **23/23** (aucun doublon, aucun symbole de schéma type compté)
- Étiquette lisible (NL-01…NL-20, NS-01…NS-03) : **23/23**
- **Score : 23/23** — cases fausses : aucune.
- Encadré RELEVE E103 - MATERIEL dans un espace libre (`box_in_free_space: true`), bordereau 1 p., 0 troncature.
- Symboles de légende comptés par erreur : aucun (la feuille n'a pas de légende de symboles ; les schémas types sont ignorés).

## Étape 3 — multiplicateurs
Aucun logement ni chambre TYPE sur E103 : sans objet.

## Étape 5 — référence estimateur
Aucune référence `.qpl` de l'estimateur pour TEST-E103 : **vérification incomplète**, aucune comparaison faite, rien n'est certifié « pas pire que l'estimateur ».

## Réserves

1. **À VALIDER — un seul bloc pour 5 types.** DP1, DP2, PP1, SO3 et SO4 partagent le même bloc CAO (S004) : le bordereau sort une ligne NL = 20. La ventilation par type ci-dessus vient du texte de l'étiquette (CONFIRMÉ), pas du bloc — à reporter à la main si le chiffrage exige une ligne par modèle.
2. **À VALIDER — portée CONSERVER.** La feuille n'est ni « NOUVEAU » ni « EXISTANT/DÉMOLITION » : la route par blocs met les 23 repères en CONSERVER. Le contenu (numéros d'appareils, instructions code-barres nLight, « every nLight enabled device… is furnished with… ») indique des appareils neufs à installer — HYPOTHÈSE, à trancher avant chiffrage.
3. **HYPOTHÈSE — luminaires non relevés.** Les zones colorées et les luminaires du plan d'étage (U1, U2, U3, J1, P1, P2, K3, G3, G4…) ne sont pas des blocs reconnus sur cette feuille de détails ; ils relèvent des plans d'éclairage. Rien n'est compté pour eux ici.
4. **À VALIDER — codes NL / NS.** Codes courts choisis par la session (aucune légende de symboles sur E103) ; la colonne « Source » du bordereau affiche « E-001 légende » par défaut du script — il n'y a pas de légende E-001 dans ce dossier.
5. **À VALIDER — appareils #14 et #15** : numéros absents de cette feuille (probablement sur une autre feuille du projet) ; non comptés.
6. Tous les repères sont en RES (règle du format : réserve tant qu'une source ne la lève pas).

## Fichiers
`TEST-E103-RELEVE.pdf`, `TEST-E103-LIVRABLES-PNG.zip` (E103_annote.png, calque, bordereau, BOM csv/xlsx), `TEST-E103.qpl`,
`TEST-E103-Rapport-de-metre.pdf/.md`, `TEST-E103-rendu-rapport.json`, `reserves-auto.md` (réserves du script), `controle-23-reperes.png`.

Non-régression : `python -m src.validation.jeu_reference` → « Régressions (> 1.0 point) : aucune » (Δ 0,0 sur S-1714, S-1715, S-1769, S-1811, S-1844).
