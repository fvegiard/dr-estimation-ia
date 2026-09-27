# chunk-20.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 110 dpi full page) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.247 shows footer "246", p.308 "307", p.276 "275", p.225 "224", p.230 "229", p.448 "447");
`neca_page` = printed folio (= PDF index; footers "318", "293", "322", "320", "202", "150" checked on the pages opened).
Rows with confidence low (1 row) and none (5 rows: FIXT TYPE G1 and others) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| GFI 15/20 | medium | PDF p.247 / printed 246 — GFCI Duplex Receptacles: 20 amp, 120 volt AC, commercial specification-grade, duplex with indicating light and wall plate, feed through, Ivory | L1@0.20 Ea 14.10 9.32 23.42 (alts quoted in note also on page: 15 A Ivory 11.70 / heavy duty 20 A Ivory 60.40) | p.318 Duplex Receptacle - Straight Blade: 20 Amp GFCI or AFCI | 35.00 / 43.75 / 52.50, Unit C | OK — exact |
| 15A 1P | medium | PDF p.308 / printed 307 — Circuit Breakers: 120/240 volt bolt-on circuit breakers, 10,000 A.I.C., 1 pole 15A | L1@0.15 Ea 29.80 6.99 36.79 | p.293 Panelboard Terminations: Single Pole Circuit Breaker (copper conductor termination including neutral): 15 Amp | 0.32 / 0.40 / 0.48, Unit E | OK — exact |
| NF 30A | medium | PDF p.276 / printed 275 — 240 Volt General Duty Safety Switches: NEMA 1 general duty non-fused, 3P 30A | L1@0.50 Ea 115.00 23.30 138.30 | p.322 Disconnect Safety Switches - Nonfused 3-Pole (NEMA 1; NEMA 3R add 10%): 30 Amp | 2.00 / 2.50 / 3.00, Unit E | OK — exact |
| A INT | medium | PDF p.225 / printed 224 — Switches: Commercial specification-grade, side wired with ground screw, 15 amp, 120/277 volt, AC quiet, Single pole, ivory | L1@0.20 Ea 2.12 9.32 11.44 | p.320 Switches - General Use Toggle Switches - Keyed Switches: 1-Pole 15 Amp | 20.00 / 25.00 / 30.00, Unit C | OK — exact (heading on page reads exactly "Switches - General Use Toggle Switches - Keyed Switches") |
| GRADATEUR 3 VOIE | medium | PDF p.230 / printed 229 — Switches: Dimmer switches, incandescent with decorative wallplate, 120 volt, three-way, 600W, touch on/off, ivory | L1@0.25 Ea 35.60 11.60 47.20 | p.320 Dimmer Switch: 3-Way 600 Watt | 0.70 / 0.88 / 1.05, Unit E | OK — exact |
| 1/2 EMT 3#10 (assembly row) | high | PDF p.448 / printed 447 — 1/2" EMT Conduit Assemblies: 100' 1/2" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps, 3 #10THHN, solid | L1@6.47 CLF 122.00 301.00 423.00 | p.202 Electrical Metallic Tubing (EMT): 1/2-inch | 4.50 / 5.60 / 6.70, Unit C | OK — exact |
| 1/2 EMT 3#10 (wire companion) | high | none (NECA only) | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #10 | 7.00 / 8.75 / 10.50, Unit M | OK — exact |

Result: 7 rows checked, 0 rejected. No change to chunk-20.csv.
