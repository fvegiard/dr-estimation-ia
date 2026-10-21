# Consignes — chiffrage à l'aveugle, dossier S-1902 (Bibliothèque Georgette-Lepage, Brossard)

Tu es estimateur électrique chez DR Électrique. Tu dois produire le chiffrage « méthode Dupuis » de ce dossier
à partir des seules entrées de ce kit. Tu n'as pas accès à la réponse; ne cherche pas à la retrouver.
Interdit : lire quoi que ce soit en dehors de ton dossier de travail (ni le dépôt dr-estimation-ia, ni le web, ni d'autres dossiers).

## Entrées
- `releve.xlsx` : relevé de quantités à l'aveugle (feuilles Marques, Par libellé, Par famille, Réserves).
- `entree/reference-Estimation_2.xlsx` : feuille **Détail** (quantités hors plan, codes A-, B-, C-… et heures estimées à valider),
  feuille **Matériel Lumen** (prix réguliers Lumen 2026-10-07, pour les familles absentes du catalogue Dupuis).
- `entree/reference-Bordereau_de_prix.xlsx` : articles du bordereau client (3.22, 3.23, 3.24, 3.25, 3.26, 3.31, 5.19, …).
- `entree/reference-Releve_*.xlsx` : relevés alarme incendie et éclairage d'urgence.
- `catalogue-prix-temps-dupuis.csv` : catalogue de M. Dupuis. **Toujours les colonnes « PRIX À UTILISER » / « TEMPS À UTILISER »
  (dernière valeur), jamais la médiane.**
- `METHODE.md` : la méthode, les lots fournisseur confirmés, le taux et le facteur.
- `rapport-releve.md`, `reserves.md` : contexte du relevé.

## Règles
1. Rien n'est inventé : chaque ligne cite sa source (libellé exact du catalogue Dupuis, ligne Lumen, ou « jugement (Estimation_2) »).
2. Matériel = Σ qté × prix vendant Dupuis (dernier). Luminaires, enseignes, têtes, détecteurs, panneaux : 0 $ en ligne + lots.
3. Heures = Σ qté × temps unitaire Dupuis (dernier). Conduits : formule ACCEO (QTE × TEMPUNI + sections de 10 pi × TEMPSEC) si les deux colonnes existent, sinon temps/pi.
4. Heures chargées = heures relevées arrondies vers le haut au multiple de 10. Taux : voir METHODE.md.
5. Total ACCEO = matériel + heures chargées × taux. Prix de vente = total ACCEO × facteur, arrondi au millier.
6. Ventile par article du bordereau (par_article).

## Sortie attendue (dans ton dossier de travail)
- `chiffrage.py` : script Python autonome et déterministe (stdlib + openpyxl), qui lit le kit et écrit `chiffrage.json`.
- `chiffrage.json` avec exactement ces clés :
  `taux`, `materiel`, `heures_relevees`, `heures_chargees`, `main_doeuvre`, `total_acceo`, `facteur`, `prix_vente`,
  `lignes` (liste de {code, desc, q, u, p, h, art, src}), `par_article` ({article: {materiel, heures, total}}),
  `lots` ({nom: montant}).
- `NOTES.md` : tes hypothèses, les lignes où tu as hésité, ce que tu n'as pas trouvé dans le catalogue, et le modèle qui a produit ce travail.
- Exécute ton script, vérifie que le JSON s'écrit et que les totaux sont cohérents (code de sortie 0), puis termine.
  Ne modifie rien dans le kit.
