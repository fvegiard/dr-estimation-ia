# chunk-11.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited page rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `neca_page` = printed folio (= PDF index).
Rows with confidence low/none (HP RELO, FIXT TYPE D3/L14/S3/L11/K/M, DD, DV) were not re-opened
(HP RELO: p.390 text layer spot-checked — "Speaker - Ceiling - Note: Includes Cutting Hole" line present as cited).

No row in this chunk cites the National Estimator 2025 (all `ne_item = none`).

| family | conf | NECA (p) | seen on page | verdict |
|---|---|---|---|---|
| INT DECT | medium | p.281 Section 8 Division 26 — Occupancy Sensors: Automatic Wall Switch | 0.35 / 0.44 / 0.53, Unit E | OK — item, unit, 0.35 E exact |
| DETECTEUR PRESENCE | medium | p.281 Occupancy Sensors: Ceiling Mounted Sensor | 0.50 / 0.63 / 0.75, Unit E | OK — exact (Passive Infrared Occupancy Sensor same page 0.50 / 0.63 / 0.75 E, Intelligent Power Pack 0.75 / 0.94 / 1.13 E as noted) |
| DETECTEUR MOUV | medium | p.281 Occupancy Sensors: Ceiling Mounted Sensor | 0.50 / 0.63 / 0.75, Unit E | OK — exact |

Result: 3 rows checked, 0 rejected. No change to chunk-11.csv.
