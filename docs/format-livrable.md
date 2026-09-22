# Format du livrable attendu — gabarits DR Électrique (lecture directe, EP2026-074)

> Porté tel quel depuis `dr-releves-2026/_socle/FORMAT-LIVRABLE.md`
> (voir `consolidation.md`).

## 1. Inventaire des gabarits

**`Décompte des sorties - Gabarit.xlsx`** (résidentiel léger) — feuilles par étage
(`Grenier`, `Étage 2`, `Étage 1`, `Rez-de-chaussée`, `Sous-sol`, `Garage + Extérieur`,
`Pool house`) + `Chauffage`, `Entrée Électrique`, `Liste des prix`, `Matériel`, `Total`,
`Prix soumission`. Sur chaque étage : blocs par pièce (`Chambre #01`, `SDB des maîtres`…),
colonne label (ex. `Prise 15A 125V`, `Prise 15A 125V USB`, `Interrupteur`, `Interrupteur
3 voies`, `Gradateur`, `Encastrée`, `Fixture`, `Détecteur de fumée`, `Câblodistribution TV`,
`Raccordement ventilation`) et colonne quantité (humain saisit `0`→N à côté). Feuille
`Total` : `=SUMIF($B:$B,K3,$C:$C)+...` sur toutes les feuilles d'étage → un compte par
type d'appareil pour toute la maison. `Entrée Électrique` : Matériel/Coût unitaire/Unité/
Quantité/Total par calibre (100A/200A/320A). `Matériel` : `Description | Prix unitaire |
Unité | Quantité | Total` (divers). `Liste des prix` : catalogue boîtes avec prix/marge
(30%/20%).

**`Take-off et demande de prix - Gabarit.xlsx`** (projet, feuille `Complet`) — colonnes
exactes : `Description | Type / Identification | Quantité | Emplacement | Fabricant |
Modèle | Notes | Total`. Regroupé par lot en-tête (`Éclairage et commande`, `Éclairage
d'urgence`, `Services`, `Distribution`, `Chauffage`) puis par bloc `HORS LOGEMENT` /
`LOGEMENT` (ce dernier avec tableau `NB LOGEMENTS × Niveau` par Type A-F). `Total` = somme
across étages/types pour ce repère. Feuille `Demande de prix` : mêmes colonnes, format
d'envoi aux fournisseurs.

**`Take-off et suivi de soumission - Gabarit.xlsx`** — feuille `Take-Off` : `Description
du matériel | Fabricant | Modèle | Quantité | Commentaire` (par article numéroté,
ex. automatisation). Feuille `Suivi soumission` : `Article | (desc) | SPEC/ÉQUIVALENT |
Envoyé | Refu | En attente | Prix | # Soum | Commentaire | PJ` — suivi de fournisseurs,
**pas** un relevé de quantités.

**`E2026-XX - Soumission projet (DR).xlsm`** : `Sommaire` (`Article | Description | Unité
| Prix | Quantité | Sous-total | Total partiel`) + onglets numérotés (1.1, 1.2… 2.6) =
sections de devis, chacun lié au Sommaire par formule.

**`E2026-XX - Soumission résidentiel léger.xlsx`** : texte de soumission (portée des
travaux), pas de tableau de quantités — remplit à partir des totaux du Décompte.

**`E2026-XX - Fermeture soumission (SIP).xlsx`** : `Résumé` + `Compil.1..13` — coûts
main-d'œuvre/matériel post-attribution, hors relevé.

## 2. Quel gabarit pour EP2026-075/076/077 (légers, résidentiel/petit commercial)

**`Décompte des sorties - Gabarit.xlsx`** est le gabarit résidentiel léger (pièce par
pièce, unifamilial/duplex simple) — usage direct si ce sont des maisons/petits logements
individuels. Le gabarit **projet** (`Take-off et demande de prix - Gabarit.xlsx` /
`Soumission projet (DR).xlsm`) sert aux immeubles à logements multiples ou commercial
(structure par lot + par niveau + par Type de logement A-F, fournisseur/modèle en colonnes
propres). Différence clé : Décompte = comptage brut par pièce sans fabricant/modèle ;
Take-off Complet = comptage **avec** identification (repère), fabricant, modèle, notes,
prêt pour demande de prix. Si EP2026-075/076/077 sont des maisons unifamiliales →
Décompte ; si petits commerciaux ou multilogements → Take-off Complet.

## 3. Livrable cible d'un relevé (Plan Expert → gabarit)

1. **Rapport de métré Plan Expert** (par plans, natif `.xls`/export) : `Groupe | Nom du
   compteur | Quantité | Feuille/Plan` — c'est la source de vérité, jamais modifiée.
2. **`data/counts-by-label.csv`** (ou équivalent) : `label, occurrence_count` — agrégat par
   étiquette Plan Expert, toutes feuilles confondues → alimente directement la colonne
   **Quantité** du gabarit (Take-off Complet ou Décompte, additionnée par `Emplacement`/
   étage si le rapport distingue les feuilles).
3. **`arteres/arteres-metres.csv`** (artères/câbles) : `id, de, vers, protection,
   conducteurs, L_total_m…` → alimente une section Distribution/filerie séparée (métrage
   linéaire, pas une "Quantité" d'appareil).
4. **`reserves/registre-reserves.csv`** (points non résolus) → ne va **pas** dans le
   gabarit final tant qu'ouvert ; sert de checklist de validation avant livraison.
5. Ordre de production : Plan Expert (sauvegarde + export rapports) → CSV agrégés par
   label/étage → collage dans `Complet`/`Décompte` (colonnes Description/Type-Repère,
   Quantité, Emplacement remplies par le relevé) → colonnes Fabricant/Modèle/Notes
   remplies par l'estimateur → `Total` (formule) → `Demande de prix` (export) →
   `Sommaire` de soumission.

## 4. Ce qu'un relevé de plans NE peut PAS remplir

`Fabricant`, `Modèle` (sauf mention explicite au devis), `Notes` (équivalences, accords
chantier du type "Vu avec Benoit Philippe"), toute la feuille `Suivi soumission`
(Envoyé/Refu/Prix/# Soum/PJ fournisseurs), `Coût unitaire`/`Prix`/marges (`Liste des
prix`, `Sommaire`), `Compil.*` (main-d'œuvre, taux horaire), dates/validité de
soumission, et les repères "à confirmer"/"?" que Plan Expert ne peut lever seul — ceux-là
restent des réserves ouvertes pour Francis ou le fournisseur.

Gabarits lus dans :
`C:\Users\fvegi\.codex\workspaces\2026-09-10-releves\_lot4\EP2026-074 - 138 Ch de la
Baie-Robinson, Lac-Brome\` (Feuille de calcul et quantités\, Soumission électrique\).
Comparaison lue en lecture seule dans
`C:\Users\fvegi\.codex\workspaces\2026-09-08-install-planexpert\gitlab\saint-michel-takeoff\`
(`git status --porcelain` vide, confirmé après lecture).
