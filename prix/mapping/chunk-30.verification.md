# chunk-30.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually.
`ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.95 "94", p.281 "280", p.448 "447", p.449 "448");
`neca_page` = printed folio (= PDF index; footers "150", "202", "323" checked on the pages opened).
Rows with confidence low (2 EMT 4#3 x2, CONTACTEUR, GSM) and none (FIXT TYPE S5) were not re-opened — out of scope (high/medium only).

| # | family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|---|
| 0 | 3/4 EMT 6#12 | high | PDF p.449 / 448 — 3/4" EMT Conduit Assemblies (100' 3/4" EMT, 2 set screw connectors, 9 set screw couplings, 9 one-hole straps): 6 #12THHN, solid | L1@8.72 CLF 184.00 406.00 590.00 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50 C | OK — exact in both books |
| 1 | 3/4 EMT 6#12 | high | none (bundled in row 0) | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |
| 2 | 2 EMT 27#10 | medium | PDF p.18 / 17 — EMT conduit in concealed areas, walls and closed ceilings: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 EMT: 2-inch | 8.00 / 10.00 / 12.00 C | OK — exact |
| 3 | 2 EMT 27#10 | high | PDF p.94 / 93 — Type THHN 600 volt solid copper building wire: # 10 | L2@8.00 KLF 264.00 373.00 637.00 | p.150 THHN & THWN: #10 | 7.00 / 8.75 / 10.50 M | OK — exact |
| 7 | 2 EMT 39#12 | medium | PDF p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 EMT: 2-inch | 8.00 / 10.00 / 12.00 C | OK — exact |
| 8 | 2 EMT 39#12 | high | PDF p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |
| 9 | 30A 600V F | medium | PDF p.281 / 280 — 600 Volt Heavy Duty Safety Switches: NEMA 1 heavy duty fusible 600 volt, 3P 30A | L1@0.50 Ea 492.00 23.30 515.30 | p.323 Disconnect Safety Switches - Fused 3-Pole (NEMA 1; 3R +10%; stainless +20%): 30 Amp | 2.20 / 2.75 / 3.30 E | OK — exact |
| 12 | 1 1/4 EMT 3#4 | medium | PDF p.18 / 17 — EMT concealed: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 EMT: 1 1/4-inch | 6.20 / 7.80 / 9.30 C | OK — exact |
| 13 | 1 1/4 EMT 3#4 | high | PDF p.95 / 94 — Type THHN 600 volt stranded copper building wire: # 4 | L2@12.0 KLF 1,130.00 559.00 1,689.00 | p.150 THHN & THWN: #4 | 13.00 / 16.25 / 19.50 M | OK — exact |
| 14 | 1/2 EMT 6#12 | high | PDF p.448 / 447 — 1/2" EMT Conduit Assemblies (100' 1/2" EMT, 2 connectors, 9 couplings, 9 straps): 6 #12THHN, solid | L1@8.27 CLF 147.00 385.00 532.00 | p.202 EMT: 1/2-inch | 4.50 / 5.60 / 6.70 C | OK — exact |
| 15 | 1/2 EMT 6#12 | high | none (bundled in row 14) | — | p.150 THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |
| 16 | 1 1/4 EMT 4#4 | medium | PDF p.18 / 17 — EMT concealed: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 EMT: 1 1/4-inch | 6.20 / 7.80 / 9.30 C | OK — exact |
| 17 | 1 1/4 EMT 4#4 | high | PDF p.95 / 94 — THHN stranded: # 4 | L2@12.0 KLF 1,130.00 559.00 1,689.00 | p.150 THHN & THWN: #4 | 13.00 / 16.25 / 19.50 M | OK — exact |
| 18 | 1 1/4 EMT 22#12 | medium | PDF p.18 / 17 — EMT concealed: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 EMT: 1 1/4-inch | 6.20 / 7.80 / 9.30 C | OK — exact |
| 19 | 1 1/4 EMT 22#12 | high | PDF p.94 / 93 — THHN solid: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |

Adversarial notes (siblings seen, not the cited lines):
- NE p.449 and p.448: the "stranded" alternates (3/4": 6 #12THHN, stranded L1@8.72 CLF 164.00 406.00 570.00; 1/2": 6 #12THHN, stranded L1@8.27 CLF 127.00 385.00 512.00) exist on the same pages with the same manhours and lower material — the CSV cites the "solid" lines as stated. The notes on both pages say one electrician, costs include the assembly (conduit + fittings + wire).
- NE p.18 has three EMT tables (floor slab / concealed / exposed) — the cited numbers are from the "concealed" table (2" exposed would be L1@10.0, 1-1/4" exposed L1@6.00; slab 2" L1@7.00, 1-1/4" L1@4.50). Not cited.
- NE p.94: #12 also exists as THW solid (250.00) and THW stranded (290.00) — the cited 173.00 is the THHN solid line, third table, as stated.
- NE p.95: #4 XHHW stranded is 1,670.00 on the same page — the cited 1,130.00 is THHN stranded, as stated.
- NE p.281: NEMA 3R 3P 30A fusible 600V is 836.00 (same manhours 0.50) — the cited 492.00 is NEMA 1, as stated.
- NECA p.323 also has Fused 2-Pole 30 Amp 2.00 and Fused 4-Pole 30 Amp 2.70 — the 3-Pole block (2.20) is the one cited. NECA p.322 (not opened) holds the Nonfused blocks.
- NECA p.150 notes: reduce labor 10% with factory-lubricated wire (already mentioned in the CSV notes). NECA p.202 note: add 10% for colored conduit (already mentioned).

Result: 15 rows checked, 0 rejected. No change to chunk-30.csv.
