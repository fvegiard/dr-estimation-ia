# FORMAT-EXEMPLE — target visual spec (EXEMPLE.pdf, HR26-14)

Source: 87-page EXEMPLE.pdf. Only pages 1 (DSI01), 30 (bordereau DSI06) and 70 (E11) were locally viewable.
STANDARD-RELEVE.md / bordereau-materiel.csv were NOT found (branch origin/hr26-14-entrainement absent; no file under /home/claude/data/apprentissage) — this spec derives from the photos only.

## Document structure
For each plan sheet, in order:
1. Annotated plan page (original sheet, same size/orientation, landscape).
2. One or more `BORDEREAU MATERIEL - <sheet>` table pages (e.g. page 30 = DSI06).

## 1. Annotated plan page
- Original drawing kept intact: title block (consultant, sceau, client, emission/revision, projet, dessin, feuille), "NE PAS UTILISER POUR CONSTRUCTION" stamp, notes — never overwritten or moved.
- **Markers**: small filled circle (~radius 5-7 pt at sheet scale) with a darker outline of the same hue, pastel fill, placed on each counted device symbol. One colour per family (see palette).
- **Repere labels**: tiny text next to each marker, format `<family>-<nn>` (e.g. `I01-03`); source repere shown in bordereau as `<sheet>-<nnn>` (e.g. `DSI06-037`).
- **In-sheet box** `RELEVE <sheet> - MATERIEL`: thin grey-bordered white rectangle placed in free drawing space (DSI01: full width between plan rows; E11: under the unit plans), never on the title block.
  - Header line: bold title `RELEVE DSI01 - MATERIEL`, then `N repères / F familles / RES n` (e.g. `122 repères / 8 familles / RES 122`; `172 / 20 / RES 64`), then right text `Calques activables; modèles, prescriptions et réserves complètes page 2`.
  - Subline in dark red, small: `RES = réserve source, modèle, position, portée ou réconciliation; * = identification à revalider`.
  - Family rows laid out in 4 columns (column-major): coloured circle, bold code (`I01`, or trade codes `AF`, `BJ`, `CP`, `PL`…), uppercase label (e.g. `AVERTISSEUR DE FUMEE AUTONOME 120V MURAL`), right-aligned `qty / Rn` (e.g. `36 / R36`, `4 / R4`, or just `12` when no reserve). Linear items (PL plinthe) may use a rectangle swatch.
  - Optional footer: `Quantités source et renvois, voir bordereau détaillé` / `PL = dimensions graphiques du plan; …`.
- Palette observed (fill order): I01 yellow #FFE9A8, I02 light blue #A9D3F5, I03 mint green #A8E6C4, I04 lavender #D9C2EE, I05 grey #C8CCD2, I06 salmon/pink #F6C2BD, I07 orange-yellow, I08 blue; E-sheets reuse the same pastel cycle (green, blue, pink, cyan, lilac, red, orange…).

## 2. Bordereau page `BORDEREAU MATERIEL - <sheet>`
- Landscape, same page size, white, sans-serif (Helvetica).
- Bold title top-left `BORDEREAU MATERIEL - DSI06`, then 2 small lines:
  `Quantités représentées avec multiplicateurs; portées et composants de chaque ensemble conservés.` /
  `Les renvois et composants de panneaux ne constituent pas des ensembles supplémentaires à additionner.`
- Header row with light blue-grey fill (#E3ECF5), bold small text; columns (approx. width share):
  `Repère / source` (7%) | `Matériel` (15%) | `Désignation` (6%) | `Qté` (3.5%) | `Portée` (9%) | `Modèle` (15%) | `Prescription / réserve` (38%) | `Parent` (rest).
- One row per repère, tall rows (~2 text lines) separated by thin light-grey rules, no vertical lines. Repère cell 2 lines: `I01-01` / `DSI06-037`.
- Values: Matériel uppercase label, Désignation = legend symbol (K, F, DF…), Qté integer, Portée e.g. `RENVOI_DSI05`, Modèle `MODELE NON PRECISE` when unknown, Prescription/réserve free text, Parent empty unless component of an assembly.
- ~21 rows per page; continue on further pages with same header.
