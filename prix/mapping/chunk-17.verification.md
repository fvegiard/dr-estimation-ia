# chunk-17.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also extracted for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.279 shows footer "278");
`neca_page` = printed folio (= PDF index; footers "360", "322", "318" checked on the pages opened).
Rows with confidence low (2#12 MOTOR, OPERATEUR PORTE) and none (FIXT TYPE B2/R2/L13/H1, BORNE, BA, J) were not re-opened — out of scope (high/medium only).
chunk-17 has no row with confidence high.

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| EXIT COMBO | medium | none | — | p.360 26 52 00 Safety Lighting: Combination Exit & Emergency Lights (Rev X) | 1.00 / 1.25 / 1.56, Unit E | OK — numbers and unit exact. Label fix: the line is its own bold heading, NOT under "Power Pack with Dual Heads" (that block ends at "Mounting Shelf 1.00 / 1.25 / 1.56 E"); `neca_item` heading corrected, no number changed |
| 30A 600V NF | medium | PDF p.279 / printed 278 — 600 Volt Heavy Duty Safety Switches: NEMA 1 heavy duty non-fused 600 volt safety switches, 3P 30A | L1@0.50 Ea 261.00 23.30 284.30 | p.322 26 28 00: Disconnect Safety Switches - Nonfused 3-Pole (NEMA 1 only; NEMA 3R add 10%; stainless add 20%): 30 Amp | 2.00 / 2.50 / 3.00, Unit E | OK — item, unit and all numbers exact in both books (sibling seen NE: 2P 30A same 261.00 / 0.50; NEMA 3R 3P 30A 455.00 / 0.50 — not the cited line) |
| USB | medium | none | — | p.318 Duplex Receptacle - Straight Blade: 15 Amp 3 Wire with USB Ports | 25.00 / 31.25 / 37.50, Unit C | OK — exact (sibling seen: 20 Amp 3 Wire with USB Ports 30.00 / 37.50 / 45.00 C) |

Result: 3 rows checked, 0 rejected. One label correction in chunk-17.csv (EXIT COMBO `neca_item` parent heading), numbers untouched.
