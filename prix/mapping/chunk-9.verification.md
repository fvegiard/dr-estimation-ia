# chunk-9.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF index).
Rows with confidence low/none (MIA, B750W, CONDENSEUR, FIXT TYPE E3, MRA, FIXT TYPE L, B500W) were not re-opened.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 30A NF WP | medium | p.276 / 275 "240 Volt General Duty Safety Switches" — NEMA 3R general duty non-fused 240 volt safety switches — 3P 30A | L1@0.50 Ea 207.00 23.30 230.30 | p.322 Disconnect Safety Switches - Nonfused 3-Pole: 30 Amp, note "These labor units apply to NEMA 1 enclosures only - For NEMA 3R add 10%" | 2.00 / 2.50 / 3.00, Unit E | OK — item, unit, 207.00, 0.50 h, 2.00 E and the +10% NEMA 3R note all exact |
| 12X12X4 | high | p.147 / 146 "Sheet Metal Pull Boxes" — NEMA 1 surface or flush mounted screw cover pull boxes — 12 x 12 x 4 | L1@0.55 Ea 73.60 25.60 99.20 | p.218 NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts: 12-inch x 12-inch x 4-inch | 1.25 / 1.60 / 2.15, Unit E | OK — exact |
| STATION | medium | none cited | — | p.410 Fire Alarm Initiating Devices: Manual Station Non-Coded | 0.50 / 0.63 / 0.78, Unit E | OK — exact |
| 2#12 CONN | medium | none cited | — | p.277 Standard Wire Conductor Terminations: #12 | 0.15 / 0.19 / 0.23, Unit E | OK — exact |
| GFI WP | medium | p.247 / 246 "Ground Fault Circuit Interrupter (GFCI) Duplex Receptacles" — 15 amp, 120 volt AC, commercial specification-grade, duplex less indicating light, with wall plate — Ivory | L1@0.20 Ea 11.70 9.32 21.02 | p.318 Duplex Receptacle - Straight Blade: 15 Amp GFCI or AFCI | 30.00 / 37.50 / 45.00, Unit C | OK — exact |

Result: 5 rows checked, 0 rejected. No change to chunk-9.csv.
