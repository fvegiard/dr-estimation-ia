# Gabarit de dossier de soumission

Copier ce gabarit pour chaque nouvelle soumission :

```
dossiers/<no>-<nom>/
├── entree/          # plans PDF, devis, addendas — déposés par Francis, jamais modifiés
├── releve.xlsx      # produit par `python -m src.releve xlsx` (gabarit DR)
├── ecart.md         # produit par `python -m src.validation.ecart` (verdict calculé ; FINAL = Francis)
├── projet.qpl       # projet Plan Expert (rasters à côté)
└── cablage.pdf      # plans annotés des chemins de câblage
```

Règles :

- `entree/` est en **lecture seule** : chaque PDF reçu est empreinté en SHA-256
  (`python -m src.releve inventaire dossiers/<no>/entree --out inventaire.json`).
- Chaque ligne de `releve.xlsx` garde sa référence de feuille et de page.
- `ecart.md` est **calculé** : ses chiffres viennent des fichiers comparés, jamais d'un texte rédigé.
- **Aucun dossier client n'est commité** : `.gitignore` exclut tout `dossiers/` sauf ce gabarit.
  Seul ce gabarit vit dans le dépôt.
