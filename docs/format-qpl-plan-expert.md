# Format `.qpl` Plan Expert — projets de référence de M. Dupuis (mesuré 2026-09-27)

> Ancien nom : `dupuis-target-format.md` (renommé le 2026-10-05). Décrit le fichier XML `.qpl` de Plan Expert,
> **pas** le PDF de relevé annoté : celui-ci est décrit uniquement dans `docs/FORMAT-EXEMPLE.md`.

Source: data/dossiers/S-{1714,1715,1769,1811,1844}/reference/*Dupuis*.qpl (S-1857 has NO Dupuis reference file).
Reproduce: `cd data/dossiers && python3 <repo>/tools/dupuis_profile.py`.

## Envelope
UTF-8 BOM, CRLF, `<?xml version="1.0"?>`, root `QuoterPlanSession` > Project, Workspace, Plans(Group*, Plan*), Prices, Reports(1 Report, 16 Property).

## Per sheet (Plan)
`<Plan Name="<pdf stem> - N" FileName="<pdf stem> - N.png">` > Thumbnail, Scale, Bookmarks/Bookmark, Comment, Layers/Layer x4 (Index 0-3, "Calque par défaut", "Nouveau calque 1..3"), Legend on layer 0 (X=100 Y=100 FontSize=45 MaxRows=25 Color=-657931).
Only a minority of sheets carry objects: 37/52, 8/29, 2/7, 11/67, 9/42.

## Scale
`<Scale Value Type Precision=2 SetManually=False Engineering=False>`; Type=1 imperial, Value = inch-per-foot fraction with French comma ("0,09375"=3/32, "0,125"=1/8, "0,0625", "0,15625", "0,25"); Type=0 metric 1:Value (200, 250); Value=0 = unscaled (majority of sheets).

## Objects (pixel coords on the PNG raster)
- Counter: Name, GroupID, Shape (0 Circle,1 Square,2 Diamond,3 Triangle), DefaultSize (~20-38), Text="1", Color, FillColor; children `<Element X Y Width Height>` one per symbol.
- Line: Name (circuit/conduit spec e.g. "3/16 KS", "PVC 3/12", "conduit 3/4 03c12", or "Distance N"), GroupID; children `<Element X1 Y1 X2 Y2>` segments.
- Area (polygon Points), Rectangle (markers): rare.
- One GroupID per Name (0 names split across groups); every GroupID has a `Price Key="<GroupID>;;Counter|Line|Area;" CostEach=0`.

## EE link
`<Plans><Group GroupID=g><EEExchangeData ItemType="A" ItemID="ENS<16 hex>" Name Key PersonalKey Description/>` — only S-1714 (1) and S-1844 (2), all conduits (Key "19PE0.75 #12", "19PE2 #12"). Dupuis links almost nothing; mapping to EE ensembles must be done downstream.

## Counts
| Job | plans | counters | symbols | distinct labels | lines | segments | EE |
|---|---|---|---|---|---|---|---|
| S-1714 | 52 | 462 | 8503 | 93 | 54 | 1825 | 1 |
| S-1715 | 29 | 79 | 401 | 78 | 34 | 360 | 0 |
| S-1769 | 7 | 35 | 116 | 35 | 8 | 37 | 0 |
| S-1811 | 67 | 101 | 1411 | 101 | 46 | 722 | 0 |
| S-1844 | 42 | 53 | 716 | 52 | 15 | 206 | 2 |

Labels are free text, fixture-type driven ("FIXTURE TYPE A1", "LO PRISE", "KS", "TH"), with renovation prefixes ("ADD ", "ENLEVER", "DEPLACER").
Corpus census (apprentissage/qpl-2021-2026/recensement-complet/summary.json): 511 unique/510 parsed, 386005 marks, 11807 distinct labels, 16905 sheets, 8955 lines, 132 EE ensembles, 30 projects with EE link, 0 nonzero prices.
