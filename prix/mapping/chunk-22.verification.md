# chunk-22.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.247 shows footer "246", p.449 "448");
`neca_page` = printed folio (= PDF index; footers "360", "318", "202", "150" checked on the pages opened).
Rows with confidence low (BOUTON POUSSOIRE, BRASSEUR AIR) and none (FIXT TYPE G2/E7/M1/Q, LC) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| COMBO | medium | none (not cited) | — | p.360 (26 52 00 Safety Lighting) Combination Exit & Emergency Lights | Rev X, 1.00 / 1.25 / 1.56, Unit E | OK — numbers exact. Cosmetic: the CSV prefixes the item with "Power Pack with Dual Heads:"; on the page "Combination Exit & Emergency Lights" is its own bold heading row, not a sub-line of Power Pack. Not a numeric error, row kept |
| GFI 20A | medium | PDF p.247 / printed 246 — GFCI Duplex Receptacles: 20 amp, 120 volt AC, commercial specification-grade, duplex with indicating light and wall plate, feed through, Ivory | L1@0.20 Ea 14.10 9.32 23.42 | p.318 Duplex Receptacle - Straight Blade: 20 Amp GFCI or AFCI | 35.00 / 43.75 / 52.50, Unit C | OK — exact |
| 3/4 EMT 5#12 (assembly row) | high | PDF p.449 / printed 448 — 3/4" EMT Conduit Assemblies: 100' 3/4" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps, 5 #12THHN, solid | L1@8.02 CLF 166.00 374.00 540.00 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50, Unit C | OK — exact |
| 3/4 EMT 5#12 (wire companion) | high | none (not cited) | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| PRISE 15/20A GFI | medium | PDF p.247 / printed 246 — same 20 amp GFCI line as GFI 20A, Ivory | L1@0.20 Ea 14.10 9.32 23.42 | p.318 20 Amp GFCI or AFCI | 35.00 / 43.75 / 52.50, Unit C | OK — exact |
| PRISE 15A GFI | high | PDF p.247 / printed 246 — 15 amp, 120 volt AC, commercial specification-grade, duplex less indicating light, with wall plate, Ivory | L1@0.20 Ea 11.70 9.32 21.02 | p.318 15 Amp GFCI or AFCI | 30.00 / 37.50 / 45.00, Unit C | OK — exact |

Result: 6 rows checked, 0 rejected. No change to chunk-22.csv.
