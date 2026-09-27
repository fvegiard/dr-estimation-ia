# chunk-15.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 130 dpi full page) and read visually;
the text layer was also extracted to locate the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.449 shows footer "448",
PDF p.225 shows "224", PDF p.437 shows "436"); `neca_page` = printed folio (= PDF index; footers "202", "150", "320", "226" checked on the pages opened).
Rows with confidence low (MAT, PROJECTEUR) and none (RT, FIXT TYPE P, M, E, MONUMENT, C) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 3/4 EMT 3#12 (assembly row) | high | PDF p.449 / printed 448 — 3/4" EMT Conduit Assemblies, 100' 3/4" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps: 3 #12THHN, solid | L1@6.62 CLF 132.00 308.00 440.00 | p.202 Electrical Metallic Tubing (EMT): 3/4-inch (note "Add 10% for colored conduit") | 5.00 / 6.20 / 7.50, Unit C | OK — exact in both books. Alts quoted in note also exact: NE "3 #12THHN, stranded L1@6.62 CLF 122.00 308.00 430.00"; NECA set screw box connector 3/4-inch 0.10/0.12/0.15 E, set screw coupling 3/4-inch 0.05/0.06/0.07 E |
| 3/4 EMT 3#12 (companion wire row) | high | none | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 (note "Reduce labor units 10% when using factory lubricated wire") | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 1 VOIE | medium | PDF p.225 / printed 224 — Switches: Commercial specification-grade, side wired with ground screw, 15 amp, 120/277 volt, AC quiet: Single pole, ivory | L1@0.20 Ea 2.12 9.32 11.44 | p.320 Switches - General Use Toggle Switches - Keyed Switches: 1-Pole 15 Amp | 20.00 / 25.00 / 30.00, Unit C | OK — exact in both books (alts in note exact: NE side-wired w/o ground screw "Single pole ivory L1@0.20 Ea 2.70 9.32 12.02"; NECA 1-Pole 20 Amp 25.00/31.25/37.50 C) |
| 3 VOIE | medium | PDF p.225 / printed 224 — same block: Three-way, ivory | L1@0.25 Ea 3.85 11.60 15.45 | p.320 same block: 3-Way 15 Amp | 35.00 / 43.75 / 52.50, Unit C | OK — exact (alts exact: NE "Three-way ivory L1@0.25 Ea 4.84 11.60 16.44"; NECA 3-Way 20 Amp 40.00/50.00/60.00 C) |
| COLONNETTE | medium | PDF p.437 / printed 436 — Telephone-Power Poles: Telephone-power pole assemblies, 2-1/8" x 2-1/8", 4 power outlets: 10'-5" pole, flush boot | L1@1.30 Ea 155.00 60.60 215.60 | p.226 Wiremold Product - Tele-Power Poles: ALTP-4 Tele-Power Pole | 1.25 / 1.56 / 1.88, Unit E | OK — exact in both books (alts in note exact: NE 12'-5" L1@1.35 202.00, 15'-5" L1@1.40 257.00, isol gr. L1@1.35 181.00, 2x2 adj foot L1@1.30 347.00, 1-1/4x1-3/4 10' L1@1.25 187.00, Tel entrance fitting L1@0.30 12.10 14.00 26.10; NECA 30TP-3 1.25, 25TP4D 1.25, 25TC4 1.00 E) |

Result: 5 rows checked, 0 rejected. chunk-15.csv unchanged (no wrong item, unit or number found).
