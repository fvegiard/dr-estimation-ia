# chunk-26.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited page rendered (pymupdf, 110 dpi full page) and read visually.
`ne_page` = 1-based PDF page (printed folio = PDF-1); `neca_page` = printed folio (= PDF page, 1-based; footer checked on every page opened).
Pages opened: NE PDF p.18 (printed 17), p.94 (93), p.249 (248), p.372 (371), p.380 (379); NECA p.150, 202, 276, 318, 410.
Rows with confidence none (FIXT TYPE L3B, FIXTURE TYPE C, FIXT TYPE R3) and low (MOTEUR 120V) were not re-opened as a verdict,
but MOTEUR 120V cites p.380 / p.276 which were opened for UTA: "Fractional HP L1@0.50 Ea 5.22 23.30 28.52" and
"20 Amp Circuits #12 & #10 0.25 0.30 0.36 E" are both present exactly as cited.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| UTA | medium | p.380 / 379 — Equipment Hookup, "Hook up mechanical equipment": Air handlers | L1@1.50 Ea 49.20 69.90 119.10 | p.276 Section 8 Div 26 — Power Connections to Equipment Installed By Others - Copper 600 Volt Conduit: 20 Amp Circuits #12 & #10 | 0.25 / 0.30 / 0.36, Unit E | OK — both books exact |
| 1 EMT 7#10 (conduit) | medium | p.18 / 17 — Electrical Metallic Tubing, "EMT conduit in concealed areas, walls and closed ceilings": 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 — Electrical Metallic Tubing (EMT): 1-inch | 5.50 / 6.80 / 8.20, Unit C | OK — exact |
| 1 EMT 7#10 (wire) | high | p.94 / 93 — Copper Building Wire, "Type THHN 600 volt solid copper building wire": # 10 | L2@8.00 KLF 264.00 373.00 637.00 | p.150 — 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #10 | 7.00 / 8.75 / 10.50, Unit M | OK — exact |
| DETECTEUR THERMIQUE (head) | medium | p.372 / 371 — Detectors, "Temperature detectors": Fixed temp, 135 degree | L1@0.50 Ea 20.00 23.30 43.30 | p.410 Section 10 Div 28 — Fire Alarm Initiating Devices: Detector Head | 0.20 / 0.25 / 0.31, Unit E | OK — exact |
| DETECTEUR THERMIQUE (base) | medium | — | — | p.410 — Fire Alarm Initiating Devices: Detector Base | 0.65 / 0.81 / 1.02, Unit E | OK — exact |
| 2 EMT 33#12 (conduit) | medium | p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 — EMT: 2-inch | 8.00 / 10.00 / 12.00, Unit C | OK — exact |
| 2 EMT 33#12 (wire) | high | p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 — THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 2 EMT 42#12 (conduit) | medium | p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 — EMT: 2-inch | 8.00 / 10.00 / 12.00, Unit C | OK — exact |
| 2 EMT 42#12 (wire) | high | p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 — THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 1 EMT 12#12 (conduit) | medium | p.18 / 17 — EMT concealed: 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 — EMT: 1-inch | 5.50 / 6.80 / 8.20, Unit C | OK — exact |
| 1 EMT 12#12 (wire) | high | p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 — THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 2 EMT 31#12 (conduit) | medium | p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 — EMT: 2-inch | 8.00 / 10.00 / 12.00, Unit C | OK — exact |
| 2 EMT 31#12 (wire) | high | p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 — THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| PRISE 30A 250V | medium | p.249 / 248 — Power Cord Receptacles, "2 pole, 3-wire single, grounding": 30A, 250V, NEMA 6-30R | L1@0.25 Ea 13.00 11.60 24.60 | p.318 — Single Receptacle - Straight Blade or Twist Lock: 30 Amp 3 Wire | 40.00 / 50.00 / 60.00, Unit C | OK — exact (NE page title is "Power Cord Receptacles", CSV says "Single Receptacles" — section heading is right, line is exact) |

Result: 14 rows checked, 0 rejected. No change to chunk-26.csv.
