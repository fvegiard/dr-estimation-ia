# chunk-32.csv adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited book pages rendered (pymupdf, 110 dpi) and read visually; item, unit and numbers compared against the page. Low-confidence rows (0, 1, 5, 6) were not in scope.

| row | family | book/page | page says | verdict |
|---|---|---|---|---|
| 2 | A POELE | NE p249 (printed 248) / NECA p318 | Power Cord Receptacles, "3 pole, 4-wire single, grounding, Range": 50A, 125/250V, NEMA 14-50R L1@0.35 Ea 20.90 16.30 37.20 ; Single Receptacle - Straight Blade or Twist Lock: 50 Amp 4 Wire 55.00 68.75 82.50 C | OK |
| 3, 7 | 1 EMT conduit | NE p18 (printed 17) / NECA p202 | EMT concealed 1" L1@4.25 CLF 125.00 198.00 323.00 ; EMT 1-inch 5.50 6.80 8.20 C | OK |
| 4, 12 | #12 THHN | NE p94 (printed 93) / NECA p150 | THHN solid #12 L2@7.00 KLF 173.00 326.00 499.00 ; #12 6.00 7.50 9.00 M | OK |
| 8, 14, 18 | #10 THHN | NE p94 / NECA p150 | THHN solid #10 L2@8.00 KLF 264.00 373.00 637.00 ; #10 7.00 8.75 10.50 M | OK |
| 9, 15 | 3/4 EMT conduit | NE p18 / NECA p202 | EMT concealed 3/4" L1@3.75 CLF 74.30 175.00 249.30 ; EMT 3/4-inch 5.00 6.20 7.50 C | OK |
| 10 | #8 THHN | NE p95 (printed 94) / NECA p150 | THHN stranded #8 L2@9.00 KLF 408.00 419.00 827.00 ; #8 9.00 11.25 13.50 M | OK |
| 11, 13, 17 | 2 EMT conduit | NE p18 / NECA p202 | EMT concealed 2" L1@8.00 CLF 285.00 373.00 658.00 ; EMT 2-inch 8.00 10.00 12.00 C | OK |
| 16, 20 | #6 THHN | NE p95 / NECA p150 | THHN stranded #6 L2@10.0 KLF 607.00 466.00 1,073.00 ; #6 11.00 13.75 16.50 M | OK |
| 19 | 1 1/4 EMT conduit | NE p18 / NECA p202 | EMT concealed 1-1/4" L1@5.00 CLF 189.00 233.00 422.00 ; EMT 1 1/4-inch 6.20 7.80 9.30 C | OK |

Checked: 18 rows (all high/medium). Rejected: 0.

Remark (no data change): NE solid THHN (p94) stops at #10, so #8/#6 correctly cite the stranded table on p95. Low rows 5/6 (2 EMT 3#1) were spot-checked in passing: p18 2" and p95 #1 L3@14.0 KLF 2,250.00 652.00 2,902.00 and NECA p150 #1 19.00 23.75 28.50 M also match the page.
