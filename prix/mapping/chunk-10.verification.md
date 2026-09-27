# chunk-10.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF page, 1-based; checked on the footer of every page opened).
Rows with confidence low (GACHE, DETECTEUR A FUMER x2, EVAPORATEUR, VE, FIXT TYPE 2X2) and none (PORTE, FIXT TYPE L12/S1/B3)
were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| BATTERIE UNIT 2T | medium | none (no NE line cited) | — | p.360 26 52 00 Safety Lighting — Egress/Emergency Fixtures: Self Contained Dual Head | 1.20 / 1.50 / 1.88, Unit E | OK — exact (siblings: Remote Single Head 0.60, Remote Double Head 0.70, Recessed Emergency Fixtures 1.50, Emergency Ballasts - Field Installed 0.75) |
| 8X8X4 | high | p.147 / 146 "Sheet Metal Pull Boxes" — NEMA 1 surface or flush mounted screw cover pull boxes — 8 x 8 x 4 | L1@0.45 Ea 43.20 21.00 64.20 | p.218 NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts: 8-inch x 8-inch x 4-inch | 1.10 / 1.35 / 1.80, Unit E | OK — item, unit, 43.20, 0.45 h, 1.10 E all exact (NEMA 3R 8x8x4 on same page = 1.10 E; NEMA 12 hinged 8x6x4 = 1.00 E) |
| CLOCHE | medium | p.368 / 367 "Bells, Buzzers and Sirens" — Bells — 6" 24 VAC | L1@0.35 Ea 94.80 16.30 111.10 | p.410 28 46 00 Fire Detection and Alarm — Fire Alarm - Signaling: Bell | 0.75 / 1.00 / 1.25, Unit E | OK — exact (sibling lines: Bell/Strobe 0.75 E, Chime 0.75 E, Strobe Light 0.75 E) |

Result: 3 rows checked, 0 rejected. No change to chunk-10.csv.
