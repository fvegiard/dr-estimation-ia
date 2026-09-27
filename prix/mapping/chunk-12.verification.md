# chunk-12.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited page rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted and grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1);
`neca_page` = printed folio (= PDF page, 1-based; checked on the footer of every page opened).
Rows with confidence low/none (HDMI, BORNE DE RECHARGE, DETECTEUR COMBUSTION x2, B PRISE, FIXT TYPE X1/X/C3/F1, S)
were not re-opened (HDMI and DETECTEUR COMBUSTION cite p.383 / p.410, which were opened for other rows: "RCA Module
0.50 0.65 0.75 E", "Detector Base 0.65 0.81 1.02 E", "Detector Head 0.20 0.25 0.31 E" all present as cited).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| MODULE ADRESSABLE | medium | — | — | p.410 Section 10 Division 28 — 28 46 00 Fire Detection and Alarm, Fire Alarm Initiating Devices: Addressable Point ID Module | 0.60 / 0.75 / 0.94, Unit E | OK — item, unit, 0.60 E exact |
| 1/2 EMT 3#12 (conduit) | high | p.448 / 447 — 1/2" EMT Conduit Assemblies, "100' 1/2" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps": 3 #12THHN, solid | L1@6.17 CLF 95.20 287.00 382.20 | p.202 Section 8 Division 26 — Electrical Metallic Tubing (EMT): 1/2-inch | 4.50 / 5.60 / 6.70, Unit C | OK — both books exact (material 95.20, 6.17 h, CLF; NECA 4.50 C) |
| 1/2 EMT 3#12 (wire) | high | — | — | p.150 Section 8 Division 26 — 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| SORTIE TV | medium | — | — | p.383 Section 9 Division 27 — 27 15 00 Communications Horizontal Cabling, Work Area Terminations: Type F Modular Jack | 0.20 / 0.25 / 0.30, Unit E | OK — exact |

Result: 4 rows checked, 0 rejected. No change to chunk-12.csv.
