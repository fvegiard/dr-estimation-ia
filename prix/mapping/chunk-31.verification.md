# chunk-31.csv adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited book pages rendered (pymupdf, 110 dpi) and read visually; item, unit and numbers compared against the page.

| row | family | book/page | page says | verdict |
|---|---|---|---|---|
| 0 | PANN ALARME | NECA p410 | Addressable Control Panel - Main Board (Rev X) 4.00 5.00 6.00 E | OK |
| 3 | 3/4 HP | NE p380 (printed 379) / NECA p276 | Fractional HP L1@0.50 Ea 5.22 ; 20 Amp Circuits #12 & #10 0.25 0.30 0.36 E | OK |
| 5 | VE-1 | NE p380 / NECA p276 | Exhaust fans, small L1@1.50 Ea 49.20 ; 20 Amp Circuits #12 & #10 0.25 E | OK |
| 7, 9, 11, 13 | 1 1/4 EMT conduit | NE p18 (printed 17) / NECA p202 | EMT concealed 1-1/4" L1@5.00 CLF 189.00 ; EMT 1 1/4-inch 6.20 7.80 9.30 C | OK |
| 8, 10, 12, 16 | #10 THHN | NE p94 (printed 93) / NECA p150 | THHN solid #10 L2@8.00 KLF 264.00 ; #10 7.00 8.75 10.50 M | OK |
| 14 | #12 THHN | NE p94 / NECA p150 | THHN solid #12 L2@7.00 KLF 173.00 ; #12 6.00 7.50 9.00 M | OK |
| 15 | 2 EMT conduit | NE p18 / NECA p202 | EMT concealed 2" L1@8.00 CLF 285.00 ; EMT 2-inch 8.00 10.00 12.00 C | OK |

Checked: 13 rows (all high/medium). Rejected: 0.

Minor note-only remark (no data change): row 0 note lists "Integrated Digital Communicator 1.00 1.25 1.50 E" as part of the Addressable Control Panels table; on p410 that line sits under "Fire Alarm Control Panels Hardwired". Hours quoted are correct.
