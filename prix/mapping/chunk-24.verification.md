# chunk-24.csv — adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited pages rendered (pymupdf, 120 dpi full page) and read visually;
the text layer was also grepped for the raw line. `ne_page` = 1-based PDF page (printed folio = PDF-1: PDF p.448 shows footer "447",
p.18 "17", p.94 "93", p.279 "278"); `neca_page` = printed folio (= PDF index; footers "202", "150", "281", "322" checked on the pages opened).
Rows with confidence low (A 1000W, EXIT RELO, MOTEUR) and none (CP, CR10, FIXT TYPE P3, FIXT TYPE P2) were not re-opened — out of scope (high/medium only).

| family | conf | National Estimator (PDF p / printed) | seen on page | NECA (p) | seen on page | verdict |
|---|---|---|---|---|---|---|
| 1/2 EMT 4#12 (assembly row) | high | PDF p.448 / printed 447 — 1/2" EMT Conduit Assemblies: 100' 1/2" EMT conduit, 2 set screw connectors, 9 set screw couplings and 9 one-hole straps, 4 #12THHN, solid | L1@6.87 CLF 113.00 320.00 433.00 | p.202 Electrical Metallic Tubing (EMT): 1/2-inch (note "Add 10% for colored conduit") | 4.50 / 5.60 / 6.70, Unit C | OK — exact. Fittings quoted in the note also exact (Set Screw Box Connectors 1/2-inch 0.08/0.10/0.12 E; Set Screw Couplings 1/2-inch 0.04/0.05/0.06 E) |
| 1/2 EMT 4#12 (wire companion) | high | none (not cited) | — | p.150 600 Volt Bldg Wire-1/C-Copper Type THHN & THWN: #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| 1 1/4 EMT 19#12 (conduit row) | medium | PDF p.18 / printed 17 — EMT conduit in concealed areas, walls and closed ceilings: 1-1/4" | L1@5.00 CLF 189.00 233.00 422.00 | p.202 Electrical Metallic Tubing (EMT): 1 1/4-inch | 6.20 / 7.80 / 9.30, Unit C | OK — exact. Caveat (not a book error, row kept): 19 x #12 THHN in 1-1/4" EMT looks above the NEC Chapter 9 / Annex C fill for that size — worth checking on the plan whether the label really means one 1-1/4" raceway |
| 1 1/4 EMT 19#12 (wire companion) | medium | PDF p.94 / printed 93 — Type THHN 600 volt solid copper building wire: # 12 | L2@7.00 KLF 173.00 326.00 499.00 (crew of 2, per 1,000 ft, one conductor) | p.150 #12 | 6.00 / 7.50 / 9.00, Unit M | OK — exact |
| INT MOUV | medium | none (not cited) | — | p.281 Occupancy Sensors: Automatic Wall Switch | 0.35 / 0.44 / 0.53, Unit E | OK — exact. On the page "Automatic Wall Switch" is a stand-alone line under the Occupancy Sensors block (after "Ceiling Mounted Sensor 0.50" and "Passive Infrared Occupancy Sensor 0.50") |
| 30A 600V NF WP | medium | PDF p.279 / printed 278 — 600 Volt Heavy Duty Safety Switches: NEMA 3R heavy duty non-fused 600 volt safety switches, 3P 30A | L1@0.50 Ea 455.00 23.30 478.30 | p.322 (26 28 00) Disconnect Safety Switches - Nonfused 3-Pole, 30 Amp; note "These labor units apply to NEMA 1 enclosures only - For NEMA 3R add 10%" | 2.00 / 2.50 / 3.00, Unit E | OK — exact, NEMA 3R note correctly carried |
| 1/2 EMT 4#14 (assembly row) | high | PDF p.448 / printed 447 — same 1/2" EMT Conduit Assemblies block, 4 #14THHN, solid | L1@6.47 CLF 91.30 301.00 392.30 | p.202 EMT 1/2-inch | 4.50 / 5.60 / 6.70, Unit C | OK — exact |
| 1/2 EMT 4#14 (wire companion) | high | none (not cited) | — | p.150 #14 | 5.00 / 6.20 / 7.50, Unit M | OK — exact |

Result: 8 rows checked (3 high, 5 medium), 0 rejected. No change to chunk-24.csv.
