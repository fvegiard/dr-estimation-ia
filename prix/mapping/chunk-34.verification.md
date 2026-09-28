# chunk-34.csv adversarial verification (2026-09-27)

Method: every row with confidence high/medium had its cited book pages rendered (pymupdf, 130 dpi) and read visually; item, unit and numbers compared against the page. Low/none rows (1, 2, 7, 8, 19, 20) were not in scope. Row numbers are 1-based data rows.

| row | family | book/page | page says | verdict |
|---|---|---|---|---|
| 3, 5 | 1 EMT conduit | NE p18 (printed 17) / NECA p202 | EMT concealed 1" L1@4.25 CLF 125.00 198.00 323.00 ; EMT 1-inch 5.50 6.80 8.20 C | OK |
| 4, 6 | #10 THHN | NE p94 (printed 93) / NECA p150 | THHN solid #10 L2@8.00 KLF 264.00 373.00 637.00 ; #10 7.00 8.75 10.50 M | OK |
| 9, 21, 23 | 1 1/4 EMT conduit | NE p18 / NECA p202 | EMT concealed 1-1/4" L1@5.00 CLF 189.00 233.00 422.00 ; EMT 1 1/4-inch 6.20 7.80 9.30 C | OK |
| 10, 24 | #8 THHN | NE p95 (printed 94) / NECA p150 | THHN stranded #8 L2@9.00 KLF 408.00 419.00 827.00 ; #8 9.00 11.25 13.50 M | OK |
| 11 | 3 EMT conduit | NE p18 / NECA p202 | EMT concealed 3" L1@12.0 CLF 571.00 559.00 1,130.00 ; EMT 3-inch 11.00 13.70 16.50 C | OK |
| 12 | 300 kcmil THHN | NE p95 / NECA p150 | THHN stranded #300 KCMIL L4@23.0 KLF 7,400.00 1,070.00 8,470.00 ; 300 kcmil 35.00 44.00 52.00 M | OK |
| 13 | 2 1/2 EMT conduit | NE p18 / NECA p202 | EMT concealed 2-1/2" L1@10.0 CLF 465.00 466.00 931.00 ; EMT 2 1/2-inch 9.50 11.80 14.20 C | OK |
| 14 | 250 kcmil THHN | NE p95 / NECA p150 | THHN stranded #250 KCMIL L4@20.0 KLF 6,220.00 932.00 7,152.00 ; 250 kcmil 32.00 40.00 48.00 M | OK |
| 15, 17 | 2 EMT conduit | NE p18 / NECA p202 | EMT concealed 2" L1@8.00 CLF 285.00 373.00 658.00 ; EMT 2-inch 8.00 10.00 12.00 C | OK |
| 16, 18, 22 | #12 THHN | NE p94 / NECA p150 | THHN solid #12 L2@7.00 KLF 173.00 326.00 499.00 ; #12 6.00 7.50 9.00 M | OK |

Checked: 18 rows (all high/medium). Rejected: 0.

Remarks (no data change): NE p94 THHN solid stops at #10, so #8 and kcmil rows correctly cite the stranded table on p95. The kcmil crews (L4) and the NECA note "reduce labor 10% when using factory lubricated wire" are as printed. Low rows spot-checked in passing: p95 "# 2 L3@13.0 KLF 1,780.00 606.00 2,386.00" and "# 1 L3@14.0 KLF 2,250.00 652.00 2,902.00", NECA p150 "#2 17.00 21.25 25.50 M" and "#1 19.00 23.75 28.50 M" also match the page.
