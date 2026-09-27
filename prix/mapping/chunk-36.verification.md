# chunk-36.csv adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited book pages rendered (pymupdf, 110 dpi) and read visually; item, unit and numbers compared against the page. Low/none rows (1, 2, 3, 4) were not in scope. Row numbers are 1-based data rows.

| row | family | book/page | page says | verdict |
|---|---|---|---|---|
| 5 | 2 EMT conduit (2 EMT 30#10) | NE p18 (printed 17) / NECA p202 | EMT concealed 2" L1@8.00 CLF 285.00 373.00 658.00 ; EMT 2-inch 8.00 10.00 12.00 C | OK |
| 6 | #10 THHN (2 EMT 30#10) | NE p94 (printed 93) / NECA p150 | THHN solid # 10 L2@8.00 KLF 264.00 373.00 637.00 ; #10 7.00 8.75 10.50 M | OK |

Checked: 2 rows (all high/medium). Rejected: 0.

Remarks (no data change): low rows spot-checked in passing on NECA p150: "#3 15.00 18.75 22.50 M" (row 2) and "#2 17.00 21.25 25.50 M" (row 4) also match the page. Rows 1 and 3 ("4/1" conduit size, not a trade size) correctly remain none.
