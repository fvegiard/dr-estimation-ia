# chunk-7.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 130 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF index).
Rows with confidence low/none (FIXT TYPE J2, C1, L5, T1, A2, 2X4, DM, MONUMENT PLANCHER, RACCORD PARTITION) were not re-opened.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| POELE | medium | p.249 / 248 "Power Cord Receptacles" — 3 pole, 4-wire single, grounding, Range — 50A, 125/250V, NEMA 14-50R | L1@0.35 Ea 20.90 16.30 37.20 | p.318 Single Receptacle - Straight Blade or Twist Lock: 50 Amp 4 Wire | 55.00 / 68.75 / 82.50, Unit C | OK — item, unit, 20.90, 0.35 h, 55.00 C all exact |
| PRISE 20A | high | p.242 / 241 "Duplex Receptacles" — 20 amp, 125 volt, side wired, corrosion resistant, commercial-grade, NEMA 5-20R — Ivory | L1@0.20 Ea 1.32 9.32 10.64 | p.318 Duplex Receptacle - Straight Blade: 20 Amp 3 Wire | 30.00 / 37.50 / 45.00, Unit C | OK — exact |
| 52171 | medium | p.128 / 127 "Square Boxes" — 4" x 4" x 2-1/8" deep square boxes — 4-S 1/2 & 3/4 KO | L1@0.27 Ea 8.63 12.60 21.23 | p.200 Knockout Type Steel Boxes: 4-inch Square Boxes | 30.00 / 35.00 / 40.00, Unit C | OK — exact |

Result: 3 rows checked, 0 rejected. No change to chunk-7.csv.
