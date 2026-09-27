# chunk-21.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.242 "241");
`neca_page` = printed folio (= PDF index; footers "202", "150", "318", "409" checked on the pages opened).
Rows with confidence low (SECHOIRE A MAIN, D/M, TH INTEGRE, VOLET MOTORIZER, OPERATEUR DE PORTE, PORTE GARAGE) and none (FIXT TYPE C4, TEE) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 1 1/4 EMT 25#12 (raceway row) | medium | PDF p.18 / printed 17 — Electrical Metallic Tubing: EMT conduit in concealed areas, walls and closed ceilings, 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 Electrical Metallic Tubing (EMT): 1 1/4-inch | 6.20 / 7.80 / 9.30, Unit C | OK — exact |
| 1 1/4 EMT 25#12 (wire companion) | high | PDF p.94 / printed 93 — Copper Building Wire: Type THHN 600 volt solid copper building wire, # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| PRISE 20A 125V | high | PDF p.242 / printed 241 — Duplex Receptacles: 20 amp, 125 volt, side wired, corrosion resistant, commercial-grade, NEMA 5-20R, Ivory | L1@0.20 Ea 1.32 9.32 10.64 | p.318 Duplex Receptacle - Straight Blade: 20 Amp 3 Wire | 30.00 / 37.50 / 45.00, Unit C | OK — exact |
| CLAVIER | medium | none (not cited) | — | p.409 (28 31 00 Intrusion Detection) Security Systems - Peripherals: Digital Keypad | 1.00 / 1.25 / 1.50, Unit E | OK — exact |
| 1 EMT 15#12 (raceway row) | medium | PDF p.18 / printed 17 — EMT conduit in concealed areas, walls and closed ceilings, 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 Electrical Metallic Tubing (EMT): 1-inch | 5.50 / 6.80 / 8.20, Unit C | OK — exact |
| 1 EMT 15#12 (wire companion) | high | PDF p.94 / printed 93 — Type THHN 600 volt solid copper building wire, # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |

Result: 6 rows checked, 0 rejected. No change to chunk-21.csv.
