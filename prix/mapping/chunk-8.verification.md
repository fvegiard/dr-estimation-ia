# chunk-8.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF index).
Rows with confidence none (FIXT TYPE D2 and the 9 other `none` rows) were not re-opened — they cite no page.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| BOITE RACCORD | medium | p.147 / 146 "Sheet Metal Pull Boxes" — NEMA 1 surface or flush mounted screw cover pull boxes — 6 x 6 x 4 | L1@0.35 Ea 31.80 16.30 48.10 | p.218 NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts: 6-inch x 6-inch x 4-inch | 1.00 / 1.25 / 1.50, Unit E | OK — item, unit, 31.80, 0.35 h, 1.00 E all exact. Note's alternates also checked on p.218: NEMA 3R 6x6x4 = 1.00 E (note cites NE p149 for 3R, not NECA); NEMA 12 hinged 6x6x4 = 0.70 E |
| WIFI | medium | none (no NE line cited) | — | p.385 Section 9 Div 27 — 27 21 00 Data Communications Network Equipment — Computer Equipment - Network Devices: Wireless Access Point | 1.00 / 1.25 / 1.50, Unit E | OK — exact (sibling line "Modem - Router - Switch - Hub 1.00 1.25 1.56 E") |

Result: 2 rows checked, 0 rejected. No change to chunk-8.csv.
