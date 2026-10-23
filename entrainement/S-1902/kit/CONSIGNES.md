# Consignes — chiffrage à l'aveugle, dossier S-1902 (Bibliothèque Georgette-Lepage, Brossard) — protocole v2

Tu es estimateur électrique chez DR Électrique. Tu dois produire les quantités et les décisions de portée du chiffrage
« méthode Dupuis » de ce dossier à partir des seules entrées de ce kit. Tu n'as pas accès à la réponse ; ne cherche pas
à la retrouver. Interdit : lire quoi que ce soit en dehors de ton dossier de travail (ni le dépôt dr-estimation-ia, ni
le web, ni d'autres dossiers).

**Tu ne calcules aucun prix.** Le prix sort d'un moteur commun à tous les runs, `chiffrage_commun.py`, à partir de tes
deux fichiers. Ton travail, c'est le relevé et les décisions ; le moteur fait le reste, de la même façon pour tout le monde.

## Entrées
- `releve.xlsx` : relevé de quantités à l'aveugle (feuilles Marques, Par libellé, Par famille, Réserves).
- `entree/reference-Estimation_2.xlsx` : feuille **Détail** (quantités hors plan, codes A-, B-, C-… et heures estimées à valider),
  feuille **Matériel Lumen** (prix réguliers Lumen 2026-10-07, pour les familles absentes du catalogue Dupuis).
- `entree/reference-Bordereau_de_prix.xlsx` : articles du bordereau client (3.22, 3.23, 3.24, 3.25, 3.26, 3.31, 5.19, …).
- `entree/reference-Releve_*.xlsx` : relevés alarme incendie et éclairage d'urgence.
- `catalogue-prix-temps-dupuis.csv` : catalogue de M. Dupuis. Le moteur lit **les colonnes « PRIX À UTILISER » / « TEMPS À
  UTILISER » (dernière valeur), jamais la médiane** ; toi, tu cites le libellé exact.
- `METHODE.md` : la méthode, les lots fournisseur, le taux, le facteur et les **décisions de portée** (§8).
- `NOMENCLATURE.md` : les codes de ligne imposés (code, libellé court, unité, article du bordereau).
- `parametres.json` : taux, facteur, arrondis, seuils du comparateur. Tu ne le modifies pas.
- `chiffrage_commun.py` : le moteur. Tu ne le modifies pas.
- `rapport-releve.md`, `reserves.md` : contexte du relevé.

Bibliothèques disponibles : la bibliothèque standard de Python 3 et `openpyxl`. Rien d'autre.

## Règles
1. Rien n'est inventé : chaque ligne cite sa source dans `src` (libellé exact du catalogue Dupuis, ligne Lumen, ou « jugement (Estimation_2) »).
2. Une ligne = un code de `NOMENCLATURE.md`. Si une quantité relevée n'a pas de code, crée un code `X-nn` avec un libellé clair ;
   ne réutilise jamais un code imposé pour autre chose que son libellé.
3. Prix et temps : `prix = {"type": "catalogue", "entrees": [{"desc": "<libellé exact>", "mult": n}, …]}` quand le catalogue Dupuis
   a l'entrée (assemblage composite = plusieurs entrées ; supplément hors catalogue = `supplement_p` / `supplement_h` avec sa source) ;
   `prix = {"type": "fixe", "p": $, "h": heures}` pour un prix Lumen ou un jugement. Luminaires, enseignes, têtes, détecteurs,
   panneaux : 0 $ en ligne (temps seulement) + une ligne de lot (`"lot": true`) par PRIX DE LOT de `METHODE.md` §2.
4. Conduits : longueurs en pieds (m × 3,28084), temps/pi du catalogue (pas de colonne TEMPSEC) ; indique dans `src` la famille
   retenue et l'équivalence utilisée quand l'assemblage exact n'existe pas.
5. Décisions de portée (`METHODE.md` §8) : pour chacune, **fournis les lignes des deux options**, étiquetées
   (`"decision": {"cle", "actif_si"}` pour une ligne qui n'existe que dans une option ; `"variantes"` pour une ligne dont le
   prix ou la quantité change), et **tranche dans `decisions.json`** avec une justification. Le comparateur mesure ainsi
   l'effet exact de chaque décision, quelle que soit la tienne.
6. Ventile chaque ligne sur un article du bordereau (`art`). Les frais de chantier et heures de jugement vont dans l'article que
   `NOMENCLATURE.md` indique, jamais dans un article que le bordereau ne contient pas.

## Sortie attendue (dans ton dossier de travail)
- `quantites.json` : `{"dossier": "S-1902", "lignes": [{"code", "desc", "q", "u", "art", "src", "prix", "decision"?, "variantes"?, "lot"?}, …]}`
  (contrat complet en tête de `chiffrage_commun.py`).
- `decisions.json` : `{"postes_composites": …, "monuments": …, "lot_eclairage": …, "eae_hors_plan": …, "conduits": …,
  "justifications": {clé: "pourquoi, avec la source"}}` — valeurs permises dans `METHODE.md` §8.
- `chiffrage.json` : produit par `python3 chiffrage_commun.py . --kit .` (code de sortie 0). Si le moteur refuse une ligne, corrige
  la ligne, pas le moteur.
- `NOTES.md` : tes hypothèses, les lignes où tu as hésité, ce que tu n'as pas trouvé dans le catalogue, et le modèle et l'effort
  que tu déclares être (une déclaration, pas une preuve).
- Ne modifie rien dans le kit. Ne produis pas de `chiffrage.py`.
