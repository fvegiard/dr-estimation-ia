# FORMAT-EXEMPLE — target look of the relevé PDF (EXEMPLE.pdf, HR26-14)

Sources (all in this repo, read directly — no estimate from photos):
- `origin/data-hr26-14-plans:hr26-14/exemple-sortie-cible.pdf` = EXEMPLE.pdf (87 pages, 2594 x 1729 pt, PyMuPDF overlay).
- `origin/hr26-14-entrainement:apprentissage/hr26-14-exemplaire/` = `STANDARD-RELEVE.md`, `bordereau-materiel.csv`
  (886 rows, DSI01-08 + E02/E07/E10/E13), `feuilles.csv`, `reserves.md`.

The first version of this spec (commit aed7dfc) was written from 3 photos only and stated that these files did not
exist; they do. Values below are read from the EXEMPLE content streams and replace the photo estimates.

Implementation: `src/estimer/render/` — constants in `style.py`.

## Document order
Per sheet: the annotated plan page, then its `BORDEREAU MATERIEL - <sheet>` pages (same page size, landscape).
PDF bookmarks: `<sheet> - plan`, `Bordereau materiel <sheet>`.

## Annotated plan page
- The original vector page is kept as is (drawing, title block, stamp, seal widget, its own layers); the overlay is
  added as vector content in optional-content layers: one per family `RELEVE <code> - <materiel>` plus
  `RELEVE - Legende et avertissements` ("Calques activables").
- **Marker** per repère, at the symbol anchor: circle r = 4.186 pt around the symbol (or the symbol bbox as a
  rectangle for panels/boxes, diamond for some E families); stroke 0.7 pt; fill = stroke colour at 28 % opacity,
  stroke at 90 % (-> pastel look).
- **Colour cycle** per family (in family order on the sheet): orange (1, .690, 0), blue (0, .447, .808),
  green (0, .651, .318), purple (.557, .267, .678), slate (.173, .243, .314), red (.906, .298, .235), then repeat.
- **Repère label** (`I01-03`): Helvetica 4.8 pt, colour .1 grey, in a white box (88 % opacity, 8 pt high, text
  width + 2 pt) joined to the marker centre by a 0.35 pt leader of the family colour. Default position right of
  the marker, 2 pt past its edge; the renderer moves it left / above / below / further out to avoid other labels,
  markers and inked plan text (tags like `[K2.2]` stay readable).
- **`RELEVE <sheet> - MATERIEL` box**: white, 0.7 pt border (.25 .30 .35), placed in empty drawing space, never
  on or right of the title-block frame.
  - Wide box (DSI01: 4 columns x 505 pt, x0+10 pad): one header line at +16 pt — title Helvetica-Bold 12,
    `N reperes / F familles / RES n` Helvetica 8.2, `Calques activables; modeles, prescriptions et reserves
    completes page <p>` Helvetica 8.2 — then at +29 the dark-red (.55 .1 .1) 7.2 pt line
    `RES = reserve source, modele, position, portee ou reconciliation; * = identification a revalider`.
  - Narrow box (E02: 1 x 390 pt; E07: 1 x 250 pt): same lines stacked and wrapped.
  - Family rows from +49 pt, 27 pt pitch (22.33 on E02, ~14 on E07), filled column by column: 10 pt swatch
    (same style as the markers), code Helvetica-Bold 8.2 at +15, label Helvetica 6.6 at +50 (upper case,
    wrapped to 2 lines in narrow columns), quantity Helvetica 7.1 at column width - 74 (`36 / R36`, count alone
    when no reserve).
  - Footer 7 pt at bottom - 4.5: `Quantites source et renvois; voir bordereau detaille.`
  - Legend quantity = number of repères of the family (not the Qte multipliers: E02 M07 = 8 repères, Qte sum 23).
  - RES: every repère row is in reserve unless the input clears it (12/12 EXEMPLE sheets: RES = reperes).
- All EXEMPLE text is unaccented ASCII (`reperes`, `Quantites representees`); the renderer reproduces it verbatim.

## Bordereau page
- Title Helvetica-Bold 26 at baseline 60 (x = 55); Helvetica 12 at 86:
  `Quantites representees avec multiplicateurs; portees et composants de chaque ensemble conserves.`;
  Helvetica 11 at 106: `Les renvois et composants de panneaux ne constituent pas des ensembles supplementaires a additionner.`
- Header band y 135-162, fill (.90 .94 .97), labels Helvetica-Bold 10 at +18.
- Columns (text x on a 2484 pt table starting at 55 + 4): Repere / source 0 · Materiel 173.88 · Designation 546.48 ·
  Qte 695.52 · Portee 782.46 · Modele 1006.02 · Prescription / reserve 1378.62 · Parent 2334.96 (scaled to page width).
- Rows 65 pt, Helvetica 9, first line at +13.675, repère column second line (source id) at +10.6425;
  0.4 pt separator (.75 .79 .82) under each row, no vertical lines. 21 rows per page, header repeated.
- Rows sorted by repère (I01-01, I01-02, ... I02-01).
- `RESERVES ET COMPLEMENTS` block (Helvetica 10, not bold) 25.75 pt under the last separator, lines every 12.3625 pt,
  text from `reserves.md`.

## Renderer
```
python -m src.estimer.render <estimer-output-dir> <plans.pdf> <out.pdf> [--report report.json]
```
Input dir: `estimate.json` (estimer format; elements may carry `repere`, `source`, `bbox`, `shape`, `reserve`),
optional `bordereau.csv` (gold `bordereau-materiel.csv` schema, joined on feuille + repere, optional `reserve`
column) and `reserves.md`. Without bordereau.csv, codes F01.. per estimator family, `MODELE NON PRECISE`,
portee `A PRECISER`. Positions are raster px of `width_px`/`height_px`, mapped onto the PDF page.

Gold proof on HR26-14:
```
python -m src.estimer.render.from_exemple EXEMPLE.pdf bordereau-materiel.csv feuilles.csv OUT --reserves reserves.md
python -m src.estimer.render OUT OUT/plans.pdf HR26-14-rendu.pdf --report HR26-14-rendu.report.json
python -m src.estimer.render.verify_exemple HR26-14-rendu.pdf HR26-14-rendu.report.json EXEMPLE.pdf OUT
```
`from_exemple` reads each gold marker (centre, bbox, shape, repère) from the EXEMPLE overlay (886/886 matched to
the CSV rows, 1:1) and writes `plans.pdf` = the 12 plan pages with the RELEVE overlay streams and layers removed
(the original ARI vector drawing). Result (2026-09-27): 12 sheets, 59 pages; 886/886 markers within 0.001 pt of the
EXEMPLE; 12/12 box headers and legends identical; 7797/7797 bordereau text spans identical (text + position at
0.1 pt); bordereau page count identical for every sheet.

Not covered: the aggregated (E01, E03-E06, E08, E09, E11, E12, E14) and EU travaux/achats bordereau formats —
their gold data is not in `bordereau-materiel.csv`.
