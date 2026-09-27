# chunk-5.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page + 220 dpi table crops)
and read visually; the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed = PDF-1);
`neca_page` = printed folio (= PDF index).
Rows with confidence low/none (300W, FIXT TYPE G, TYPE B, ENCASTRE, 1500W baseboard, FIXT TYPE L8, LAMPE TEMOIN, A, ECH)
were not checked (out of scope).

| # | family | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|
| 2 | 8X8 | NE PDF p147 (printed 146), "Sheet Metal Pull Boxes", table "NEMA 1 surface or flush mounted screw cover pull boxes" | `8 x 8 x 4 L1@0.45 Ea 43.20 21.00 64.20` | 43.2 / 0.45 / Ea | OK (medium) |
| 2 | 8X8 | NECA p218, table "NEMA 1 Screw Cover J-Boxes & Pull Boxes with Knockouts" | `8-inch x 8-inch x 4-inch 1.10 1.35 1.80 E` | 1.1 E | OK (medium) |
| 3 | BATTERIE UNIT | NECA p360, "26 52 00: Safety Lighting", table "Egress/Emergency Fixtures" | `Self Contained Dual Head 1.20 1.50 1.88 E` | 1.2 E | OK (medium) |
| 4 | BATTERIE UNIT | NECA p360, same table | `Remote Single Head 0.60 0.75 0.94 E` | 0.6 E | OK (medium) |
| 5 | DISCONN | NE PDF p276 (printed 275), "240 Volt General Duty Safety Switches", table "NEMA 1 general duty non-fused 240 volt safety switches" | `3P 30A L1@0.50 Ea 115.00 23.30 138.30` | 115.0 / 0.5 / Ea | OK (medium) |
| 5 | DISCONN | NECA p322, table "Disconnect Safety Switches - Nonfused 3-Pole" (note: NEMA 1 only, NEMA 3R add 10%) | `30 Amp 2.00 2.50 3.00 E` | 2.0 E | OK (medium) |
| 9 | 1500W | NECA p352, table "Recessed Heating Fixtures" | `1500 Watt Ceiling Heater with Fan 1.50 1.88 2.25 E` | 1.5 E | OK (medium) |

## Findings

- 5 rows checked (0 high, 5 medium), 0 rejected. Every item, unit and number matches the rendered page.
- Alternates quoted in the notes were also confirmed on the cited pages: NE p147 `8 x 8 x 6 L1@0.50 Ea 53.30`;
  NE p276 fusible `2P 30A L1@0.50 Ea 91.20`, NEMA 3R non-fused `3P 30A L1@0.50 Ea 207.00`;
  NECA p322 2-pole nonfused `30 Amp 1.70 2.13 2.55 E`; NECA p360 `Remote Double Head 0.70 0.88 1.09 E`,
  `Recessed Emergency Fixtures 1.50 1.88 2.34 E`, `Power Pack with Dual Heads 36 Watt 1.10`, `54 Watt 1.30`.
- Note for row 5 says "2-pole nonfused 30 Amp = 1.70 h p322" — confirmed.
- No change made to chunk-5.csv.
