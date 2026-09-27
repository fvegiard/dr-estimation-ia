# chunk-16.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page + 200-220 dpi crops of the cited block) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.147 shows footer "146", p.449 "448", p.18 "17", p.94 "93");
`neca_page` = printed folio (= PDF index; footers "218", "202", "150" checked on the pages opened).
Rows with confidence low (1750W, A/C UNIT, CHAUFFE-EAU, BOITE VOLUME) and none (LAMPADAIRE, FIXT TYPE D7/A3/S, RM) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| BOITE D 8X8X4PO CEMA1 | high | PDF p.147 / printed 146 — Sheet Metal Pull Boxes: NEMA 1 surface or flush mounted screw cover pull boxes, 8 x 8 x 4 | L1@0.45 Ea 43.20 21.00 64.20 | p.218 NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts: 8-inch x 8-inch x 4-inch | 1.10 / 1.35 / 1.80, Unit E | OK — item, unit and all numbers exact in both books (neighbours seen NE: 8 x 6 x 4 L1@0.40 38.40; NECA: 6x6x4 1.00, 10x8x4 1.10 — not the cited line) |
| 3/4 EMT 3#10 (assembly row) | high | PDF p.449 / printed 448 — 3/4" EMT Conduit Assemblies: 100' 3/4" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps, 3 #10THHN, solid | L1@6.92 CLF 159.00 322.00 481.00 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch (note "Add 10% for colored conduit") | 5.00 / 6.20 / 7.50, Unit C | OK — exact (stranded sibling 3 #10THHN, stranded L1@6.92 CLF 143.00 322.00 465.00 seen, not cited) |
| 3/4 EMT 3#10 (wire companion) | high | none | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #10 (note "Reduce labor units 10% when using factory lubricated wire") | 7.00 / 8.75 / 10.50, Unit M | OK — exact |
| 3/4 EMT 7#12 (raceway row) | medium | PDF p.18 / printed 17 — Electrical Metallic Tubing: EMT conduit in concealed areas, walls and closed ceilings, 3/4" | L1@3.75 CLF 74.30 175.00 249.30 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50, Unit C | OK — exact (siblings seen: slab/trapeze 3/4" L1@3.50 74.30 163.00 237.30; exposed 3/4" L1@4.00 74.30 186.00 260.30 — match the note's alts) |
| 3/4 EMT 7#12 (wire companion) | high | PDF p.94 / printed 93 — Copper Building Wire: Type THHN 600 volt solid copper building wire, # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact (crew L2 = two electricians, as the page footnote says for sizes up to #4; THW solid # 12 on the same page is 250.00 / 7.00 — not the cited line) |

Result: 5 rows checked, 0 rejected. No change to chunk-16.csv.
