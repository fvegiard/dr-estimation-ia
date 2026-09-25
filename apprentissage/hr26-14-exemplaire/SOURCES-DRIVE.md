# Sources HR26-14 dans Google Drive — état et reste à faire

Localisations confirmées (Legion, `G:\My Drive`, 2026-09-25) pour compléter l'entraînement.

## Dossier source du relevé
`G:\My Drive\AI\Soumission 2026\HR26-14 - OMH Haut-Richelieu\`
- `HR26-14-projet-vide-Plans.pdf` (25 Mo) — plans source
- `HR26-14-OMH-Haut-Richelieu (15-Septembre-2026).qpl` (11 738 o) — **projet Plan Expert (QPL) de référence**
- `HR26-14-ANALYSE.md` / `.pdf` — analyse du dossier
- `01-projet-vide\`, `Analyse Claude 2026-09-15\`

## Corpus QPL (apprentissage symboles/libellés)
`G:\My Drive\AI\Releves-auto\` (INBOX/OUTBOX) + corpus historique 2021-2026 (déjà traité dans
`apprentissage/qpl-2021-2026/`). QPL de référence par dossier dans chaque `Soumission 2026\S-xxxx\`.

## Prix (SQL / références)
- Références de prix trouvées : `G:\My Drive\code electrique\OneDrive_2026-06-11\Estimation\`
  → `national estimator 2025(.pdf/OCR)`, `Neca 2022(.pdf/OCR)` (bases main-d'œuvre/matériel, format PDF).
- Base **SQL ACCEO EEWin** : non localisée comme fichier `.sql/.bak/.mdf` dans Drive lors de ce
  balayage (Drive stream). À confirmer par Francis (chemin exact du dump SQL dans Drive).

## Reste à faire (dépend d'un accès fichier stable au Drive)
1. **Hydrater** puis rapatrier le QPL HR26-14 (fichiers « en ligne seulement » du Drive : clic droit →
   « Disponible hors connexion » avant copie ; le stream a masdqué les fichiers par intermittence ce jour).
2. Parser le QPL (`src/releve/qplschema.py` / `apprentissage/qpl-2021-2026/outils/parse.py`) et
   **recouper marque par marque** au bordereau extrait ici → `ecart.md` (jeu de référence HR26-14).
3. Brancher la base **SQL prix** pour remplir les grilles `$` (E03/E04/E05/E08) — jamais de prix inventé.
