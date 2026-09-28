# chunk-13.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF page, 1-based; checked on the footer of every page opened).
Rows with confidence low (MINI KLAXON, TRIAC) and none (FIXT TYPE N/E5/C2/P1/N1, B, PANN, PP) were not re-opened — out of scope (high/medium only).
chunk-13 has no row with confidence high.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| PRISE IG (20A) | medium | p.243 / 242 "Duplex Receptacles" — 20 amp, 125 volt, back & side wired, isolated ground, NEMA 5-20R — Ivory | L1@0.20 Ea 11.70 9.32 21.02 | p.318 Duplex Receptacle - Straight Blade: 20 Amp 3 Wire | 30.00 / 37.50 / 45.00, Unit C | OK — item, unit, 11.70, 0.20 h, 30.00 C all exact (Brown/White same 11.70; Orange 18.10) |
| PRISE IG (15A) | medium | p.238 / 237 "Single Receptacles" — 15 amp, 125 volt, isolated ground, NEMA 5-15R — Orange | L1@0.20 Ea 26.50 9.32 35.82 | p.318 Duplex Receptacle - Straight Blade: 15 Amp 3 Wire | 25.00 / 31.25 / 37.50, Unit C | OK — exact. Note: NE line is under the Single Receptacles heading (already stated in the row note) while the NECA line is the Duplex heading; NECA "Single Receptacle - Straight Blade or Twist Lock: 15 Amp 3 Wire" on the same page is also 25.00 C, so the hours are identical either way |
| CONTACT PORTE | medium | p.372 / 371 "Detectors" — Intrusion detectors — Door switch | L1@0.25 Ea 10.60 11.60 22.20 | p.409 28 31 00 Intrusion Detection — Security Systems - Detection Devices: Magnetic Switch - Note: Includes drilling, mounting and termination | 0.75 / 0.95 / 1.15, Unit E | OK — exact (siblings seen: Door switch, closed cir. L1@0.40 10.80; Overhead Door Contact 1.00 E; Wireless Door Contact 0.50 E) |

Result: 3 rows checked, 0 rejected. No change to chunk-13.csv.
