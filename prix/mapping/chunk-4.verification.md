# chunk-4.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi) and read visually,
plus the text layer extracted for the raw line. `ne_page` = 1-based PDF page (printed = PDF-1); `neca_page` = printed folio (= PDF index).
Rows with confidence low/none (STRIP, RELAIS, B300W, TV, FIXT TYPE L2, FIXT TYPE F, MA, COND, HORN, P) were not checked (out of scope).

| # | family | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|
| 8 | PRISE SECHEUSE | NE PDF p249 (printed 248), "Power Cord Receptacles", table "3 pole, 4-wire single, grounding, Dryer" | `30A, 125/250V, NEMA 14-30R L1@0.25 Ea 21.50 11.60 33.10` | 21.50 / 0.25 / Ea | OK (medium) |
| 8 | PRISE SECHEUSE | NECA p318, "Single Receptacle - Straight Blade or Twist Lock" | `30 Amp 4 Wire 45.00 56.25 67.50 C` | 45.00 C | OK (medium) |
| 9 | DETECTEUR GAINE | NECA p410, "28 46 00: Fire Detection and Alarm", table "Fire Alarm - Initiating Devices" | `Duct Smoke Detector 2.00 2.50 3.00 E` | 2.00 E | OK (high) |

## Findings

- 2 rows checked (1 high, 1 medium), 0 rejected. Every item, unit and number matches the rendered page.
- Row 8 alternates quoted in the note (surface-mounted 14-30R `L1@0.35 Ea 14.70 16.30 31.00`; 3-wire 10-30R
  `L1@0.25 Ea 3.32 11.60 14.92`; NECA `30 Amp 3 Wire 40.00 50.00 60.00 C`) are also on the cited pages as quoted.
- Row 9 accessories quoted in the note (`Duct Smoke Detector Test Station 0.80 1.00 1.20 E`,
  `Duct Smoke Detector Remote Light 0.40 0.50 0.63 E`) are on p410 as quoted.
- No change made to chunk-4.csv.
