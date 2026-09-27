# chunk-6.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi) and read visually,
plus the text layer extracted for the raw line. `neca_page` = printed folio (= PDF index).
Rows with confidence low/none (FIXT TYPE L4/E2/I/H/B1/L10/D1, TYPE A, KLAXON STROB, B1250W, PRISE WP x2) were not checked (out of scope).

| # | family | book / page | line read on the page | CSV values | verdict |
|---|---|---|---|---|---|
| 4 | LECTEUR CARTE | NECA p404, "28 15 00: Integrated Access Control Hardware Devices", table "Access Control" | `Card Reader - Wall Mounted X 1.50 1.88 2.25 E` (X = Rev column marker) | 1.50 E | OK (medium) |

## Findings

- 1 row checked (0 high, 1 medium), 0 rejected. Item, unit and number match the rendered page.
- Alternates quoted in the note are on the cited pages as quoted: p404 `Card Reader - Post Mounted X 1.50 1.88 2.25 E`;
  p403 `Two Door Controller 2.00 2.50 3.00 E`; p409 `Digital Keypad 1.00 1.25 1.50 E`;
  p401 "Power Supply for Access Control Door Hardware" section exists.
- No change made to chunk-6.csv.
