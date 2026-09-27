# chunk-28.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually.
`ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.18 shows footer "17", p.94 "93", p.95 "94", p.276 "275", p.279 "278");
`neca_page` = printed folio (= PDF index; footers "150", "202", "322" checked on the pages opened).
Rows with confidence low (PLINTHE 1500W, DEMARREUR MANUEL, OUVRE PORTE, INTERCOM) and none (VA, TYPE F) were not re-opened — out of scope (high/medium only).

| # | family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|---|
| 3 | 60A NF | medium | PDF p.276 / 275 — 240 Volt General Duty Safety Switches: NEMA 1 general duty non-fused 240 volt, 3P 60A | L1@0.70 Ea 145.00 32.60 177.60 | p.322 Disconnect Safety Switches - Nonfused 3-Pole (NEMA 1; 3R +10%; stainless +20%): 60 Amp | 3.00 / 3.75 / 4.50 E | OK — exact in both books |
| 4 | 3/4 EMT 3#8 | medium | PDF p.18 / 17 — EMT conduit in concealed areas, walls and closed ceilings: 3/4" | L1@3.75 CLF 74.30 175.00 249.30 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch | 5.00 / 6.20 / 7.50 C | OK — exact |
| 5 | 3/4 EMT 3#8 | high | PDF p.95 / 94 — Type THHN 600 volt stranded copper building wire: # 8 | L2@9.00 KLF 408.00 419.00 827.00 | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #8 | 9.00 / 11.25 / 13.50 M | OK — exact |
| 6 | 2 EMT 37#12 | medium | PDF p.18 / 17 — EMT concealed: 2" | L1@8.00 CLF 285.00 373.00 658.00 | p.202 EMT: 2-inch | 8.00 / 10.00 / 12.00 C | OK — exact |
| 7 | 2 EMT 37#12 | high | PDF p.94 / 93 — Type THHN 600 volt solid copper building wire: # 12 | L2@7.00 KLF 173.00 326.00 499.00 | p.150 THHN & THWN: #12 | 6.00 / 7.50 / 9.00 M | OK — exact |
| 8 | 1 EMT 4#6 | medium | PDF p.18 / 17 — EMT concealed: 1" | L1@4.25 CLF 125.00 198.00 323.00 | p.202 EMT: 1-inch | 5.50 / 6.80 / 8.20 C | OK — exact |
| 9 | 1 EMT 4#6 | high | PDF p.95 / 94 — THHN stranded: # 6 | L2@10.0 KLF 607.00 466.00 1,073.00 | p.150 THHN & THWN: #6 | 11.00 / 13.75 / 16.50 M | OK — exact |
| 10 | 1 1/4 EMT 13#10 | medium | PDF p.18 / 17 — EMT concealed: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 EMT: 1 1/4-inch | 6.20 / 7.80 / 9.30 C | OK — exact |
| 11 | 1 1/4 EMT 13#10 | high | PDF p.94 / 93 — THHN solid: # 10 | L2@8.00 KLF 264.00 373.00 637.00 | p.150 THHN & THWN: #10 | 7.00 / 8.75 / 10.50 M | OK — exact |
| 12 | DISCONN 30A 600V NF | medium | PDF p.279 / 278 — 600 Volt Heavy Duty Safety Switches: NEMA 1 heavy duty non-fused 600 volt, 3P 30A | L1@0.50 Ea 261.00 23.30 284.30 | p.322 Nonfused 3-Pole: 30 Amp | 2.00 / 2.50 / 3.00 E | OK — exact |

Adversarial notes (siblings seen, not the cited lines): NE p.18 has three EMT tables (floor slab / concealed / exposed) — the cited numbers are from the "concealed" table as stated, not the exposed one (3/4" L1@4.00 there). NE p.276 also lists NEMA 3R 3P 60A 323.00 and fusible 3P 60A 233.00 — not cited. NECA p.322 also has Nonfused 2-Pole (60 Amp 2.50, 30 Amp 1.70) — the 3-Pole block is the one cited.

Result: 10 rows checked, 0 rejected. No change to chunk-28.csv.
