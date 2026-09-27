# chunk-29.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 130 dpi full page) and read visually.
`ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.95 "94", p.371 "370", p.380 "379");
`neca_page` = printed folio (= PDF index; footers "150", "202", "276", "383" checked on the pages opened).
Rows with confidence low (HUM, CABLE CHAUFFANT) and none (TA, PANN CONTROL) were not re-opened — out of scope (high/medium only).

| # | family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 1 1/4 EMT 4#3 | medium | PDF p.18 / 17 — EMT conduit in concealed areas, walls and closed ceilings: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 Electrical Metallic Tubing (EMT): 1 1/4-inch | 6.20 / 7.80 / 9.30 C | OK — exact in both books |
| 2 | 1 1/4 EMT 4#3 | medium | none (NE p.94 THW and p.95 THHN/XHHW tables go # 4 -> # 2, no # 3 line — confirmed) | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #3 | 15.00 / 18.75 / 22.50 M | OK — exact; "none" on NE side is correct |
| 3 | MOTEUR VE | medium | PDF p.380 / 379 — Equipment Hookup: Hook up mechanical equipment: Exhaust fans, small | L1@1.50 Ea 49.20 69.90 119.10 | p.276 Power Connections to Equipment Installed By Others - Copper 600 Volt Conduit: 20 Amp Circuits #12 & #10 | 0.25 / 0.30 / 0.36 E | OK — exact |
| 4 | BOUTON SONNETTE | medium | PDF p.371 / 370 — Signal Systems: Surface mounted push buttons: Round, plain | L1@0.20 Ea 3.59 9.32 12.91 | none | — | OK — exact |
| 7 | 2 EMT 35#12 | medium | PDF p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 EMT: 2-inch | 8.00 / 10.00 / 12.00 C | OK — exact |
| 8 | 2 EMT 35#12 | high | PDF p.94 / 93 — Type THHN 600 volt solid copper building wire: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |
| 9 | 1 EMT 3#6 | medium | PDF p.18 / 17 — EMT concealed: 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 EMT: 1-inch | 5.50 / 6.80 / 8.20 C | OK — exact |
| 10 | 1 EMT 3#6 | high | PDF p.95 / 94 — Type THHN 600 volt stranded copper building wire: # 6 | L2@10.0 KLF 607.00 466.00 1,073.00 | p.150 THHN & THWN: #6 | 11.00 / 13.75 / 16.50 M | OK — exact |
| 11 | B TV | medium | none | — | p.383 Work Area Terminations: Type F Modular Jack | 0.20 / 0.25 / 0.30 E | OK — exact (1 Gang Face Plate 0.10/0.13/0.15 E cited in note also on page) |
| 12 | 1 EMT 3#8 | medium | PDF p.18 / 17 — EMT concealed: 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 EMT: 1-inch | 5.50 / 6.80 / 8.20 C | OK — exact |
| 13 | 1 EMT 3#8 | high | PDF p.95 / 94 — THHN stranded: # 8 | L2@9.00 KLF 408.00 419.00 827.00 | p.150 THHN & THWN: #8 | 9.00 / 11.25 / 13.50 M | OK — exact |
| 14 | 2 EMT 31#10 | medium | PDF p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 EMT: 2-inch | 8.00 / 10.00 / 12.00 C | OK — exact |
| 15 | 2 EMT 31#10 | high | PDF p.94 / 93 — THHN solid: # 10 | L2@8.00 KLF 264.00 373.00 637.00 | p.150 THHN & THWN: #10 | 7.00 / 8.75 / 10.50 M | OK — exact |

Adversarial notes (siblings seen, not the cited lines): NE p.18 has three EMT tables (floor slab / concealed / exposed) — every cited line is from the "concealed" table as stated (floor-slab 1-1/4" is L1@4.50, exposed 2" is L1@10.0; the alternates quoted in the notes match the page). NE p.94 THHN solid stops at # 10; #6/#8 exist only in stranded tables (p.94 THW stranded, p.95 THHN/XHHW stranded) — rows 10/13 correctly cite THHN stranded p.95. NECA p.276 has a second "Aluminum 600 Volt Conduit" block whose first line is "20 Amp Circuits #10 0.40" — row 3 cites the copper block (0.25), as stated. NECA p.202 fittings quoted in notes (2-inch box connector 0.25/0.31/0.37, coupling 0.12/0.14/0.16; 1-inch 0.12/0.15/0.18 and 0.06/0.07/0.08) match the page. NE p.371 flush-mounted alternates (5/8" chrome L1@0.25 2.57 11.60 14.17) match; row 4 cites the surface-mounted table as stated.

Result: 13 rows checked, 0 rejected. No change to chunk-29.csv.
