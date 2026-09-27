# chunk-2.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 120 dpi) and read visually,
plus the text layer grepped for the raw line. `ne_page` = 1-based PDF page (printed = PDF-1); `neca_page` = printed folio (= PDF index).

| # | family (ee_code) | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|
| 0 | STATION MANUEL | NECA p410, "Fire Alarm Initiating Devices" | `Manual Station Non-Coded 0.50 0.63 0.78 E` | 0.50 E | OK (medium) |
| 2 | BOITE (LQE008445) | NE PDF p128 (printed 127), "4" x 4" x 2-1/8" deep square boxes" | `4-S 1/2 & 3/4 KO L1@0.27 Ea 8.63 12.60 21.23` | 8.63 / 0.27 / Ea | OK |
| 2 | BOITE (LQE008445) | NECA p200, "Knockout Type Steel Boxes" | `4-inch Square Boxes 30.00 35.00 40.00 C` | 30.00 C | OK |
| 3 | BOITE (LQE011995) | NE PDF p128 (printed 127), "4" x 4" x 1-1/2" deep square boxes" | `4-S 1/2 & 3/4 KO L1@0.25 Ea 5.41 11.60 17.01` | 5.41 / 0.25 / Ea | OK |
| 3 | BOITE (LQE011995) | NECA p200 | `4-inch Square Boxes 30.00 35.00 40.00 C` | 30.00 C | OK |
| 4 | BOITE (LQE008444) | NE PDF p147 (printed 146), "NEMA 1 surface or flush mounted screw cover pull boxes" | `12 x 12 x 4 L1@0.55 Ea 73.60 25.60 99.20` | 73.60 / 0.55 / Ea | OK |
| 4 | BOITE (LQE008444) | NECA p218, "NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts" | `12-inch x 12-inch x 4-inch 1.25 1.60 2.15 E` | 1.25 E | OK |
| 5 | BOITE (LQE011273) | NE PDF p147 (printed 146) | `12 x 12 x 6 L1@0.60 Ea 86.40 28.00 114.40` | 86.40 / 0.60 / Ea | OK |
| 5 | BOITE (LQE011273) | NECA p218 | `12-inch x 12-inch x 6-inch 1.35 1.75 2.20 E` | 1.35 E | OK |
| 6 | BOITE (LQE010549) | NE PDF p148 (printed 147), "NEMA 1 surface or flush mounted screw cover pull boxes" | `24 x 24 x 6 L1@1.00 Ea 298.00 46.60 344.60` | 298.00 / 1.00 / Ea | OK |
| 6 | BOITE (LQE010549) | NECA p218 | `24-inch x 24-inch x 6-inch 2.75 3.50 4.00 E` | 2.75 E | OK |
| 7 | BOITE (LQE004733) | NE PDF p147 (printed 146) | `6 x 6 x 4 L1@0.35 Ea 31.80 16.30 48.10` | 31.80 / 0.35 / Ea | OK |
| 7 | BOITE (LQE004733) | NECA p218 | `6-inch x 6-inch x 4-inch 1.00 1.25 1.50 E` | 1.00 E | OK |
| 8 | BOITE (no code) | NE PDF p128 / NECA p200 | same lines as row 3 | 5.41 / 0.25 / Ea ; 30.00 C | OK (medium) |
| 9 | BOITE (no code) | NE PDF p147 / NECA p218 | same lines as row 4 | 73.60 / 0.55 / Ea ; 1.25 E | OK (medium) |
| 12 | GRADATEUR | NE PDF p230 (printed 229), "Dimmer switches, incandescent with decorative wallplate, 120 volt" | `600W, slide on/off, ivory L1@0.25 Ea 12.90 11.60 24.50` | 12.90 / 0.25 / Ea | OK (medium) |
| 12 | GRADATEUR | NECA p320, "Dimmer Switch" | `1-Pole 600 Watt 0.40 0.50 0.60 E` | 0.40 E | OK (medium) |
| 15 | PRISE DUPLEX 15/20A 120V (ENSE03A359013913CDE1) | NE PDF p242 (printed 241), "20 amp, 125 volt, back & side wired, self grounding, commercial-grade, NEMA 5-20R" | `Ivory L1@0.20 Ea 10.20 9.32 19.52` | 10.20 / 0.20 / Ea | OK |
| 15 | PRISE DUPLEX 15/20A 120V | NECA p318, "Duplex Receptacle - Straight Blade" | `20 Amp 3 Wire 30.00 37.50 45.00 C` | 30.00 C | OK |

Also read on the same rendered pages (low rows, not in scope but checked in passing): NECA p410 `Detector Base 0.65 0.81 1.02 E`
(row 10) — exact. NE p128 alternates quoted in notes (`4-S 1/2 KO L1@0.27 Ea 8.08`, `4-S 3/4 KO L1@0.27 Ea 9.15`) — exact.

Result: 11 rows checked (8 high, 3 medium), 0 rejected. chunk-2.csv unchanged.
