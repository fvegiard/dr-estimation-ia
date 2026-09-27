# chunk-3.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi) and read visually,
plus the text layer grepped for the raw line. `ne_page` = 1-based PDF page (printed = PDF-1); `neca_page` = printed folio (= PDF index).
Rows with confidence low/none (HOTTE, FIXT TYPE A1/L6/L3, INT ENL) were not checked (out of scope).

| # | family | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|
| 1 | SWITCH | NE PDF p225 (printed 224), "Commercial specification-grade, side wired with ground screw, 15 amp, 120/277 volt, AC quiet" | `Single pole, ivory L1@0.20 Ea 2.12 9.32 11.44` | 2.12 / 0.20 / Ea | OK |
| 1 | SWITCH | NECA p320, table titled "Switches - General Use Toggle Switches - Keyed Switches" | `1-Pole 15 Amp 20.00 25.00 30.00 C` | 20.00 C | OK, title AMENDED (CSV had dropped "- Keyed Switches") |
| 2 | DETECTEUR MOUVEMENT | NECA p281, "Occupancy Sensors" | `Ceiling Mounted Sensor 0.50 0.63 0.75 E` | 0.50 E | OK |
| 3 | DETECTEUR MOUVEMENT | NECA p281 (standalone line under Occupancy Sensors block) | `Automatic Wall Switch 0.35 0.44 0.53 E` | 0.35 E | OK |
| 4 | HP | NECA p390, "Sound Systems - Sound Generating Equipment" | `Speaker - Ceiling - Note: Includes Cutting Hole 0.75 0.95 1.15 E` | 0.75 E | OK |
| 5 | CAMERA | NECA p407, "Television Systems - Camera and Enclosure" | `Camera Indoor on Exterior Mount 0.50 0.65 0.75 E` | 0.50 E | OK |
| 8 | PRISE 15A 125V | NE PDF p240 (printed 239), "15 amp, 125 volt, back & side wired, corrosion resistant, commercial grade, NEMA 5-15R" | `Ivory L1@0.20 Ea 1.05 9.32 10.37` | 1.05 / 0.20 / Ea | OK (high) |
| 8 | PRISE 15A 125V | NECA p318, "Duplex Receptacle - Straight Blade" | `15 Amp 3 Wire 25.00 31.25 37.50 C` | 25.00 C | OK (high) |
| 10 | STROB | NECA p410, "Fire Alarm - Signaling" | `Strobe Light 0.75 1.00 1.25 E` | 0.75 E | OK (high) |
| 12 | INTERRUPTEUR (1-pole) | NE PDF p225 | `Single pole, ivory L1@0.20 Ea 2.12 9.32 11.44` | 2.12 / 0.20 / Ea | OK |
| 12 | INTERRUPTEUR (1-pole) | NECA p320 "…Toggle Switches - Keyed Switches" | `1-Pole 15 Amp 20.00 25.00 30.00 C` | 20.00 C | OK, title AMENDED |
| 13 | INTERRUPTEUR (3-way) | NE PDF p225 | `Three-way, ivory L1@0.25 Ea 3.85 11.60 15.45` | 3.85 / 0.25 / Ea | OK |
| 13 | INTERRUPTEUR (3-way) | NECA p320 "…Toggle Switches - Keyed Switches" | `3-Way 15 Amp 35.00 43.75 52.50 C` | 35.00 C | OK, title AMENDED |

## Findings

- 9 rows checked (2 high, 7 medium), 0 rejected. Every number and unit matches the rendered page.
- 3 rows (SWITCH, INTERRUPTEUR x2) cited the NECA p320 table as "Switches - General Use Toggle Switches"; the
  printed title is "Switches - General Use Toggle Switches - Keyed Switches". Checked p317-321 and the full
  neca-2022.csv: NECA 2022 has no other general-use toggle-switch table (p318 only has "Plugtail Wired Switches",
  15 Amp 1 Pole 10.00 C), so the line cited is the only candidate. `neca_item` was completed to the exact title and
  the note flags it; chunk-0 (family INT) already uses the full title for the same line. Confidence unchanged (medium).
- Caveat carried from the mapping: the p320 title bundles keyed switches with general-use toggle switches; whether the
  labor unit differs for a plain (non-keyed) toggle switch is not stated by the book.
