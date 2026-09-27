# chunk-18.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.308 "307");
`neca_page` = printed folio (= PDF index; footers "202", "150", "293" checked on the pages opened).
Rows with confidence low (BOUTON RELACHE, WF 2000W, CHAUFFE EAU) and none (FIXT TYPE K2, TR, FIXT TYPE D6, H, B 1500W, F) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 1 EMT 13#12 (raceway row) | medium | PDF p.18 / printed 17 — Electrical Metallic Tubing: EMT conduit in concealed areas, walls and closed ceilings, 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 Electrical Metallic Tubing (EMT): 1-inch | 5.50 / 6.80 / 8.20, Unit C | OK — exact |
| 1 EMT 13#12 (wire companion) | high | PDF p.94 / printed 93 — Copper Building Wire: Type THHN 600 volt solid copper building wire, # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 3/4 EMT 9#12 (raceway row) | medium | PDF p.18 / printed 17 — EMT conduit in concealed areas, walls and closed ceilings, 3/4" | L1@3.75 CLF 74.30 175.00 249.30 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50, Unit C | OK — exact |
| 3/4 EMT 9#12 (wire companion) | high | PDF p.94 / printed 93 — Type THHN 600 volt solid copper building wire, # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 20A 1P | medium | PDF p.308 / printed 307 — Circuit Breakers: 120/240 volt bolt-on circuit breakers, 10,000 A.I.C., 1 pole 20A | L1@0.15 Ea 29.80 6.99 36.79 | p.293 Panelboard Terminations: Single Pole Circuit Breaker (copper conductor termination including neutral): 20 Amp | 0.34 / 0.43 / 0.51, Unit E | OK — exact |

Result: 5 rows checked, 0 rejected. No change to chunk-18.csv.
