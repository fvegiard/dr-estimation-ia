# chunk-23.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page, 200 dpi zoom on the NECA EMT block) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.370 "369");
`neca_page` = printed folio (= PDF index; footers "202", "150", "404" checked on the pages opened).
Rows with confidence low (PRISE TOIT, VOLET MOTORISER, SECHOIRE, SECHOIR, BOUTON) and none (FIXT TYPE L3A, V, T) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 1 1/4 EMT 17#12 (conduit row) | medium | PDF p.18 / printed 17 — EMT conduit in concealed areas, walls and closed ceilings: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 Electrical Metallic Tubing (EMT): 1 1/4-inch | 6.20 / 7.80 / 9.30, Unit C | OK — exact (alts quoted in note also exact: slab/trapeze L1@4.50 189.00 210.00 399.00; exposed L1@6.00 189.00 280.00 469.00) |
| 1 1/4 EMT 17#12 (wire companion) | high | PDF p.94 / printed 93 — Type THHN 600 volt solid copper building wire: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| CARILLON | medium | PDF p.370 / printed 369 — Chimes: One entrance, white | L1@0.40 Ea 17.40 18.60 36.00 | none (not cited) | — | OK — exact |
| 3/4 EMT 4#10 (conduit row) | medium | PDF p.18 / printed 17 — EMT conduit in concealed areas, walls and closed ceilings: 3/4" | L1@3.75 CLF 74.30 175.00 249.30 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50, Unit C | OK — exact |
| 3/4 EMT 4#10 (wire companion) | high | PDF p.94 / printed 93 — Type THHN 600 volt solid copper building wire: # 10 | L2@8.00 KLF 264.00 373.00 637.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #10 | 7.00 / 8.75 / 10.50, Unit M | OK — exact |
| LECTEUR DE CARTE | medium | none (not cited) | — | p.404 (28 15 00 Access Control) Card Reader - Wall Mounted | Rev X, 1.50 / 1.88 / 2.25, Unit E | OK — exact |

Result: 6 rows checked, 0 rejected. No change to chunk-23.csv.
