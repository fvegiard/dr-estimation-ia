# chunk-14.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `neca_page` = printed folio (= PDF page, 1-based; footer "410" checked on the page opened).
Rows with confidence low (WF1500W, SORTIE TEL/DATA, VENTILATEUR) and none (FIXT TYPE R/L15/S6/L4A, VC, PULL BOX, K) were not re-opened — out of scope (high/medium only).
chunk-14 has no row with confidence high and no medium row citing the National Estimator 2025.

| family | conf | National Estimator | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|
| TEL POMPIER | medium | none | p.410 Section 10 / 28 46 00 Fire Detection and Alarm — Fire Alarm - Signaling: Fire Fighters Phone | 1.25 / 1.60 / 2.00, Unit E | OK — item, unit and all three columns exact (sibling seen: Fire Fighters Jack 0.50 / 0.75 / 1.00 E) |
| RELAIS ADRESSABLE | medium | none | p.410 Section 10 / 28 46 00 Fire Detection and Alarm — Fire Alarm - Miscellaneous Devices: Addressable Control Relay | 0.75 / 1.00 / 1.25, Unit E | OK — exact (siblings seen: Semi-Flush Control Relay 0.75 / 1.00 / 1.25 E; Relay Module under Addressable Control Panels 0.90 / 1.15 / 1.35 E — not the cited line) |

Result: 2 rows checked, 0 rejected. No change to chunk-14.csv.
