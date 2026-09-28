# chunk-1.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi) and read visually,
plus the text layer grepped for the raw line. `ne_page` = 1-based PDF page (printed = PDF-1); `neca_page` = printed folio (= PDF index).

| family | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|
| THERMOSTAT | NECA p74 (printed 74), table "Thermostats" | `Line Voltage 1-Circuit Thermostats 0.60 0.84 1.18 E` | 0.60 E | OK |
| PRISE DUPLEX 15A 120V | NE PDF p240 (printed 239), "15 amp, 125 volt, back & side wired, specification-grade, NEMA 5-15R" | `Ivory L1@0.20 Ea 2.83 9.32 12.15` | 2.83 / 0.20 / Ea | OK |
| PRISE DUPLEX 15A 120V | NECA p318, "Duplex Receptacle - Straight Blade" | `15 Amp 3 Wire 25.00 31.25 37.50 C` | 25.00 C | OK |
| PRISE DUPLEX 15A 120V (GFI) | NE PDF p247 (printed 246), "15 amp, 120 volt AC, commercial specification-grade, duplex less indicating light, with wall plate" | `Ivory L1@0.20 Ea 11.70 9.32 21.02` | 11.70 / 0.20 / Ea | OK |
| PRISE DUPLEX 15A 120V (GFI) | NECA p318, "Duplex Receptacle - Straight Blade" | `15 Amp GFCI or AFCI 30.00 37.50 45.00 C` | 30.00 C | OK |
| EXIT | NE PDF p173 (printed 172), "Double face exit fixtures, 20-watt T6 1/2 lamps" | `Ceiling mounted, red L1@0.55 Ea 46.20 25.60 71.80` | 46.20 / 0.55 / Ea | OK |
| EXIT | NECA p360, "Exit Fixtures" | `Surface Mount - Standard or LED 1.00 1.25 1.56 E` | 1.00 E | OK |
| TETE DOUBLE | NECA p360, "Egress/Emergency Fixtures" | `Remote Double Head 0.70 0.88 1.09 E` | 0.70 E | OK |

Also spot-checked (text layer) the alternates quoted in notes of low rows: NECA p72 `Connect Thermostat 0.75 1.25 1.50 E`,
NECA p78 `60-inch 1.00 1.25 1.50 E`, NE PDF p369 `24 VAC, grille L1@0.40 Ea 73.00 18.60 91.60` and
`24 VAC, weatherproof L1@0.40 Ea 97.50 18.60 116.10` — all exact.

Result: 5 rows checked (2 high, 3 medium), 0 rejected. chunk-1.csv unchanged.
