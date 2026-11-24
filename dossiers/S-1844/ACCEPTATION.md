# Acceptation — S-1844, SAQ Varennes (pilote contextuel)

**Verdict : JUSTIFICATIONS REQUISES** — relevé partiel et non soumissible. G8 reste ouvert.

## Passe figée avant comparaison

Le premier relevé sur les 12 pages d'origine avait donné 1 occurrence et 724 signatures fréquentes
inconnues. La première passe contextuelle a donné 65 repères, mais les vignettes ont révélé des
associations D3/D4 de part et d'autre du rail. Les deux rejeux corrigés D et E, sans accès à la
référence pendant l'exécution, donnent **199 repères** : 14 duplex ordinaires proposés, 17 conservés
et 168 projecteurs typés. Le gain de 198 repères n'est **pas** une mesure du gain d'exactitude.
Le relevé historique déjà présent dans le dépôt n'est remplacé ni par le pilote ni par sa comparaison.

- [Manifestes et preuves](../../docs/preuves/autonomie-pilote/README.md) : SHA-256 de 33 artefacts
  vérifiés avant et après comparaison pour D ; 19 sorties D/E identiques octet pour octet.
- [Décisions par candidat](autonomie-pilote/contexte-candidats.csv) : 273 candidats, dont 199 comptés,
  15 reports E200/E200D dédupliqués (existants conservés) et 59 autres candidats non comptés.
  Les 724 inconnues de l'index des blocs subsistent ; ce sont des signatures, **pas des appareils**.
- `qualite.json` : 27 erreurs ouvertes (3 Q1, 24 Q15). Une partie des Q15 concerne des reports ou des
  variantes ; aucune n'est blanchie sur la seule ressemblance du cercle. Les huit planches de
  contrôle ont été ouvertes. L'ancrage visuel ne vaut pas certification d'exhaustivité ni de portée.

## Quantités et portées — lecture indépendante du recalage

La référence ci-dessous est la [transcription ACCEO](reference-quantites.csv), sans ventilation par
feuille. Les quatre types de projecteur se recoupent par code avec E101 p.4 ; `D4-NTI` est rapproché
de `D4-NT1`. Les écarts arithmétiques n'établissent pas à eux seuls qui a raison.

| Poste | IA gelée | Dupuis | Écart IA − réf. | Interprétation |
|---|---:|---:|---:|---|
| D3-N, E300 | 101 | 122 | −21 | Écart de comptage ou de typage ; le rail bas sans étiquette reste en réserve. |
| D3-NT1, E300 | 21 | 6 | +15 | La colonne ouest porte `D3-NT1` écrit sur le plan ; appariement individuel à reprendre. |
| D4-N, E300 | 26 | 27 | −1 | Un D4-N visible mais non associé à (1909.14, 680.94) est une omission du pilote. |
| D4-NT1, E300 | 20 | 19 | +1 | La différence n'est pas tranchée sans recalage. |
| **Total des quatre types** | **168** | **174** | **−6** | −3,4 % au total masque des écarts supérieurs à 10 % par type. |
| Duplex proposés, E200 | 14 | 47 (15/20 A groupés) | non comparable | Le pilote ne prend que le duplex ordinaire 15 A ; le poste humain est plus large. |
| Duplex conservés, E200D | 17 | non isolés | — | `E.C.` ; pas une pose neuve. |
| Prises à enlever / luminaires à enlever | non relevés | 65 / 204 | — | Dépose non couverte : réserves E200D/E300D, pas un zéro vérifié. |
| Têtes de secours / panneaux P2 | non relevés | 9 doubles + 5 simples / 29 | — | Autres familles hors profil ; ne pas les confondre avec les projecteurs sur rail. |

### Témoins sur les plans originaux (points PDF)

| Source | Preuve et décision |
|---|---|
| E300 p.11 (1319.70, 687.72) | [Zoom D3/D4](autonomie-pilote/D3-D4.png) : `D3-N` à droite et sous le rail ; `D4-N` au-dessus est un autre objet. Corrigé entre les passes de 65 et de 199. |
| E300 p.11 (1909.14, 680.94) | [Zoom du coude](autonomie-pilote/E300-D4-texte-au-dessus.png) : triangle vert et `D4-N` au-dessus, non associé par la règle du couloir. Omission constatée après le gel ; la passe n'est pas modifiée. |
| E300 p.11, x 1212–1698, y 2019–2026 | [Douze têtes visibles sur rail](autonomie-pilote/E300-tetes-non-typees.png) sans repère individuel D3/D4. Elles sont signalées dans le CSV, pas chiffrées au hasard. |
| E200 p.8 (411.66, 987.90) et E200D p.7 au même point | Surimpression cyan/gris avec `E.C.`. Une seule marque de conservation sur E200D, aucune commande neuve sur E200. |
| E200 p.8 (900.2, 1370.1) | [Variante sous le duplex ordinaire](autonomie-pilote/variante.png) : le remplissage et l'annotation l'excluent du poste ordinaire. Le sous-type reste à confirmer avant prix. |
| E300 p.11 (2000.2, 622.9) | [Carré bleu barré](autonomie-pilote/boite.png) compatible avec une boîte de jonction selon E100 ; `96″` ne donne pas les dimensions de la boîte ni la portée. |

## Comparaison QPL — diagnostic, pas un verdict par appareil

Le [classement brut](autonomie-pilote/ecarts-classes.csv) donne 151 appariements, 343 omissions
automatiques, 41 « en trop », 7 « doublons » et 15 « mauvaise famille ». La somme de 406 désaccords
**n'est pas** 406 erreurs vérifiées : [pages.csv](autonomie-pilote/pages.csv) montre six pages
humaines recalées sur E300, dont des libellés de démolition ou de prises. Les 31 marques de
prises se retrouvent sans page humaine appariée. La page humaine du schéma E103 n'a pas de dimensions
raster attestées. Corriger le rattachement à partir des cartouches/fonds de la référence, pas en
ajustant le seuil pour améliorer artificiellement le score. Les autres positions restent à arbitrer.

## Longueurs et chiffrage

[E400 p.12](autonomie-pilote/E400-leg.png) indique 1/4″ = 1′ et deux calibres. Le [métré](autonomie-pilote/metre-longueurs.csv)
donne 17 tracés dans le QPL, dont **52,88 m en EMT 3/4 po** et **40,52 m en EMT 1-1/4 po**
(93,41 m avant arrondi des groupes). Ni descentes, ni traversées, ni câble ne sont déduits.
L'ACCEO présente 650 pi et 150 pi de conduit vide de ces diamètres (198,12 m et 45,72 m),
mais sans ventilation E400 ni preuve d'un périmètre équivalent ; aucune validation G5.
Le chiffrage interne couvre un seul poste par barème historique (14 duplex à poser) ; un poste est
hors achat et six sont non chiffrables. Les familles non relevées ne font pas partie du dénominateur.
Pas de forfait, d'émission client ni d'approbation de Francis.