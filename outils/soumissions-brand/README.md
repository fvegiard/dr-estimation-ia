# soumissions-brand

Un seul gabarit de soumission / lettre, brandé automatiquement selon la compagnie (DR, SIP, BR, ou toute autre).
La palette est dérivée de la couleur du logo ; les logos viennent de `dr-sip-br-electritek.netlify.app/assets/images/`.

```bash
pip install reportlab num2words pillow

# Soumission sur gabarit SIP
python generate.py --brand sip --data examples/soumission_EP2026-079.json --out out/EP2026-079_sip.pdf

# Lettre sur gabarit DR
python generate.py --brand dr --data examples/lettre_E2026-XX.json

# Une PDF par marque
python generate.py --all --data examples/soumission_EP2026-079.json
```

## Ajouter une compagnie
1. Déposer le logo : `assets/logo_xxx.png` (fond transparent). Si le logo est en texte blanc (version web fond foncé) :
   `python extract_brand.py logo_web.png --print-safe assets/logo_xxx.png --dark 2B2B2B`
2. Mesurer la couleur : `python extract_brand.py assets/logo_xxx.png` → `primary` / `secondary`
3. Ajouter l'entrée dans `brands.json` (name, short, logo, primary, secondary, address, rbq).

## Palette dérivée (brands.json → generate.py)
| rôle | formule | DR | SIP | BR |
|---|---|---|---|---|
| primaire (bandes, titres, lignes) | couleur du logo | #B82048 | #D84820 | #E01010 |
| teinte (bloc CLIENT/DÉTAILS, ligne TOTAL) | primaire + 90 % blanc | #F8E9ED | #FBEDE9 | #FCE7E7 |
| gris (en-tête tableau) | fixe | #F2F2F2 | #F2F2F2 | #F2F2F2 |

## Format JSON
- `type`: `soumission` | `lettre`
- soumission : `no, date, client[], projet[], items[[desc, prix]], exclusions[], signer, salutation?` — total et montant en lettres calculés.
- lettre : `lieu_date, attention[], projet, objet, montant, documents[], inclusions[], exclusions[], signer, validite, salutation?`.
- `signer` : **dict par marque** `{"br": ["Nom", "courriel", "Titre"], "dr": [...]}` — la forme à utiliser avec `--all`. Une liste simple `["Nom", "courriel", "Titre"]` n'est valide que pour une génération mono-marque (`--brand`) ; avec `--all`, elle est remplacée par un placeholder sur toutes les marques (avertissement affiché). Marque sans entrée → « Nom du signataire / <compagnie> ».
- `salutation` : défaut « Madame, Monsieur » (lettre : appel ; soumission : formule de politesse).

Les 10 conditions standards + clause de volatilité des matériaux + encadré APPROBATION / BON DE COMMANDE sont intégrés.

`preview.html` = aperçu interactif (switch marque / type) publié comme artefact Claude.
