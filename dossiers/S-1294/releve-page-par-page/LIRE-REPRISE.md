# S-1294 — reprise locale hors E201

Livraison de travail pour revue, au 2 octobre 2026. **22 feuilles : 14 conservées et 8 nouvelles. E201 est expressément exclue.** E200 v2, E202 v3 et E205 v3 sont corrigées et remises pour revue delta. E203 v2, E204 v3, E206 v2 et E300/E301 v3 ont reçu un PASS borné aux corrections examinées. Aucun montant ni total d'achat ne doit être déduit de l'addition des feuilles.

## Contenu et utilisation

- Les JPG `S-1294-…-releve.jpg` contiennent le plan entier et une légende intégrée. Les huit nouveaux plans conservent la largeur source de 10 799 pixels et les 7 199 lignes de l'image originale, avec la légende ajoutée dessous. Les pastilles colorées correspondent aux familles; un astérisque signale une réserve.
- Les CSV par feuille conservent les identifiants, quantités, portées, références, réserves et coordonnées source. `S-1294-reprise-detail.csv` regroupe les 1 812 lignes des huit feuilles. Ce nombre inclut les renvois et références documentaires; il n'est pas un nombre d'appareils à acheter.
- `S-1294-reprise-par-panneau.xlsx` contient 29 onglets : les cinq historiques conservés, neuf panneaux P-…, sept schémas CM-…, les types PL non multipliés, les inventaires, réserves et sources. Les 197 lignes de départs et 86 références de schémas sont gardées distinctes. Les schémas et implantations ne s'additionnent pas.
- `audit/` contient le relevé structuré figé, un aperçu, la légende et toutes les vignettes de repères. `sources/` contient 22 PNG de plans et 12 fichiers scans; les scans représentent 11 empreintes distinctes. Aucun QPL ni source E201 n'est inclus.
- `S-1294-classement-scans.csv` distingue les doublons binaires et les contenus répétés. Ces scans ne servent pas de source aux quantités nouvelles.
- `S-1294-reserves-reprise.csv` rassemble les réserves majeures. Les réserves détaillées figurent dans les CSV et le classeur. Les conflits sont étayés par les extraits de `evidence/`.
- `S-1294-deltas-revue-E203-E206.csv` trace 1 008 changements de champs après revue, sans changement de quantités, identifiants ou coordonnées.
- `S-1294-deltas-revue-E200-E202.csv` trace 92 retouches de coordonnées/rayons et le retrait explicite de la prise E202-0269, non justifiée sur le symbole source. Les autres IDs sont conservés. `S-1294-delta-E205-v3.csv` corrige seulement la lettre de commande b → f du repère 0108.
- Le manifeste courant est `MANIFEST-REPRISE.json`. Les anciens README, manifest et checkpoint restent dans `historique/` dans l'archive : ils décrivent l'état initial, pas cette reprise.

## État par feuille nouvelle

| Feuille | Repères | Version figée | État réel |
|---|---:|---|---|
| E200 | 681 | v2 | Ancrages D3–D6 et lisibilité corrigés; revue delta attendue. |
| E202 | 356 | v3 | H recentré; prise 0269 retirée, 19 → 18 prises doubles; revue delta attendue. |
| E203 | 201 | v2 | PASS borné D1–D4, sans certification exhaustive. |
| E204 | 204 | v3 | PASS borné D1–D4. Commande S/T réservée. |
| E205 | 169 | v3 | Lettre f du repère 0108 corrigée; revue delta attendue. 16 spots E / 18 F inchangés, erratum du reviewer reçu. |
| E206 | 167 | v2 | PASS borné D1–D4. Symbole P réservé. |
| E300 | 25 | E300-E301 v3 | PASS borné du delta v3 et corrections D1–D4. Réserves de dimensions et d'interfaces maintenues. |
| E301 | 9 | E300-E301 v3 | Références documentaires, pas neuf installations. Identique à la v2 revue sur D1–D4. |

Les 14 feuilles historiques sont E001, E002 pages 02/03, E100, E101, E102, E103, E104, E105 pages 09/10, E107, E108 et E400 pages 22/23. Leurs plans et CSV sont inchangés, vérifiés contre leurs empreintes historiques. Ils ne font pas l'objet d'une nouvelle certification exhaustive.

## Réserves déterminantes

PL206/PL208 sont répétés sur E104 à deux niveaux : aucun renommage n'a été déduit. PS1 est décrit 120/208 V, 225 A, Icc 10 kA sur E102, contre 347/600 V, barres 100 A, Icc 14 kA sur E105. PP1 porte Icc 35 kA sur E102 contre 14 kA sur E105. Ces divergences ne sont pas arbitrées.

Le massif de 6 conduits de 100 mm est coté 550 × 405 sur E300 et 625 × 455 dans le tableau E301. Des modèles et prescriptions se contredisent également dans les sources, notamment batterie 320/144 W, flux du spot logement et modèles CO. Les alternatives sont conservées.

Les symboles C isolés sur E200, symboles non identifiés et renvois des types restent explicitement distingués. Aucun multiplicateur de logements ni métrage de câbles/conduits n'est inventé. Les longueurs approximatives E300 proviennent des mentions du dessin.

## Protocole et preuves

Aucun QPL ouvert, aucune lecture ou modification de E201, aucune récupération de main. Le classement initial des scans a exposé des annotations humaines avant le gel : **le protocole ne peut pas être qualifié d'intégralement aveugle**. L'exposition est décrite dans `evidence/PROTOCOL-EXPOSURE.md`; aucune quantité n'est reprise de ces totaux humains et aucune comparaison avec l'estimateur n'est revendiquée.

Le ZIP Granby de référence a été intégralement inventorié et lu : tables et cellules, plus pixels des 14 plans d'exemple. Ses 26 empreintes sont conservées dans `evidence/granby-full-read.json`. La reprise emploie la méthode existante de rendu et d'export, avec légendes par type et quantités de conduits précisées.

Les contrôles techniques vérifient les CSV/JSON, coordonnées, dimensions, empreintes, conservation des fichiers historiques et relecture du classeur enregistré. Ils **ne prouvent pas l'exhaustivité ni l'exactitude métier**. Les comptes des nouvelles feuilles doivent rester soumis à la revue indiquée ci-dessus.

Checkout isolé basé sur `829445d2c5dd07b83e79a265342a15cdf3846620`. Aucun push, merge, publication, modification de sécurité ou de secret. La seule modification de fichier suivi concerne `methode/render_sheet.py`, dans S-1294; le diff est inclus pour revue. Les anciennes worktrees n'ont pas été utilisées.
