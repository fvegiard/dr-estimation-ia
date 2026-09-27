# chunk-0.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi) and read visually.
`ne_page` = 1-based PDF page (printed folio = PDF-1); `neca_page` = printed folio (= PDF index). Text layers of both
books do not carry the numbers inline, so all numbers below were read from the rendered page image.

| row | family | conf | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|---|
| 0 | PRISE | medium | NE PDF p240 (printed 239), "15 amp, 125 volt, back & side wired, corrosion resistant, commercial grade, NEMA 5-15R" | `Ivory L1@0.20 Ea 1.05 9.32 10.37` | 1.05 / 0.20 / Ea | OK |
| 0 | PRISE | medium | NECA p318, "Duplex Receptacle - Straight Blade" | `15 Amp 3 Wire 25.00 31.25 37.50 C` | 25.00 C | OK |
| 1 | PRISE LQE005029 | high | NE PDF p255 (printed 254), "4 pole, 5 wire, 3 phase Y grounding locking receptacles" | `30A, 120/208V, NEMA L21-30R L1@0.30 Ea 36.50 14.00 50.50` | 36.50 / 0.30 / Ea | OK |
| 1 | PRISE LQE005029 | high | NECA p318, "Single Receptacle - Straight Blade or Twist Lock" | `30 Amp 5 Wire 50.00 62.50 75.00 C` | 50.00 C | OK |
| 4 | INT (3-way) | high | NE PDF p225 (printed 224), "Commercial specification-grade, side wired with ground screw, 15 amp, 120/277 volt, AC quiet" | `Three-way, ivory L1@0.25 Ea 3.85 11.60 15.45` | 3.85 / 0.25 / Ea | OK |
| 4 | INT (3-way) | high | NECA p320, "Switches - General Use Toggle Switches - Keyed Switches" | `3-Way 15 Amp 35.00 43.75 52.50 C` | 35.00 C | OK |
| 6 | INT (1-pole) | medium | NE PDF p225 (printed 224), same table | `Single pole, ivory L1@0.20 Ea 2.12 9.32 11.44` | 2.12 / 0.20 / Ea | OK |
| 6 | INT (1-pole) | medium | NECA p320, same table | `1-Pole 15 Amp 20.00 25.00 30.00 C` | 20.00 C | OK |
| 7 | HAUT PARLEUR | medium | NECA p390, "Sound Systems - Sound Generating Equipment" | `Speaker - Ceiling - Note: Includes Cutting Hole 0.75 0.95 1.15 E` | 0.75 E | OK |
| 8 | TH | medium | NECA p74, "Thermostats" | `Line Voltage 1-Circuit Thermostats 0.60 0.84 1.18 E` | 0.60 E | OK |
| 12 | PRISE 15A | high | NE PDF p240 / NECA p318 | identical to row 0 | 1.05 / 0.20 / Ea ; 25.00 C | OK |
| 14 | GFI | medium | NE PDF p247 (printed 246), "15 amp, 120 volt AC, commercial specification-grade, duplex less indicating light, with wall plate" | `Ivory L1@0.20 Ea 11.70 9.32 21.02` | 11.70 / 0.20 / Ea | OK |
| 14 | GFI | medium | NECA p318, "Duplex Receptacle - Straight Blade" | `15 Amp GFCI or AFCI 30.00 37.50 45.00 C` | 30.00 C | OK |
| 18 | ENSEIGNE SORTIE | medium | NECA p360 | `Combination Exit & Emergency Lights X 1.00 1.25 1.56 E` | 1.00 E | OK (numbers/unit exact) |

Correction applied (no rejection): row 18 `neca_item` breadcrumb said "Power Pack with Dual Heads > ..." but on p360
"Combination Exit & Emergency Lights" is its own standalone header row (Rev X), not under the Power Pack table. Breadcrumb fixed.

Not checked (confidence low/none, out of scope): rows 2, 3, 5, 9, 10, 11, 13, 15, 16, 17.

Result: 9 rows checked (3 high, 6 medium), 0 rejected.
