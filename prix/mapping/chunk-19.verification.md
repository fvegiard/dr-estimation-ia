# chunk-19.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.448 shows footer "447");
`neca_page` = printed folio (= PDF index; footers "281", "202", "150" checked on the pages opened).
Rows with confidence low (MOTEUR 600V, HORN WP, HORLOGE) and none (FIXT TYPE D5/B/BB/N2/S2, RS, R) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| OS | medium | none | — | p.281 Occupancy Sensors: Ceiling Mounted Sensor | 0.50 / 0.63 / 0.75, Unit E | OK — exact. Siblings quoted in the note also exact: Passive Infrared Occupancy Sensor 0.50/0.63/0.75 E, Automatic Wall Switch 0.35/0.44/0.53 E, Intelligent Power Pack 0.75/0.94/1.13 E |
| 1/2 EMT 5#12 | high | PDF p.448 / printed 447 — 1/2" EMT Conduit Assemblies, 100' 1/2" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps: 5 #12THHN, solid | L1@7.57 CLF 130.00 353.00 483.00 | p.202 Electrical Metallic Tubing (EMT): 1/2-inch | 4.50 / 5.60 / 6.70, Unit C | OK — item, unit and all numbers exact in both books (stranded alt on same page 5 #12THHN, stranded L1@7.57 CLF 113.00 353.00 466.00 also exact) |
| 1/2 EMT 5#12 (companion) | high | none | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact; the "reduce labor 10% when using factory lubricated wire" note is on the page as quoted |

Result: 3 rows checked, 0 rejected. No change to chunk-19.csv.
