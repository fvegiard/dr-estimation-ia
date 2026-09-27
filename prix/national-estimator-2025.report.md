# National Electrical Estimator 2025 — parse report

- source: `/home/claude/data/livres/national estimator 2025.pdf` (553 pages)
- output: `national-estimator-2025.csv` — 13370 rows
- pages with a `Craft@Hrs` header: 470
- header pages yielding 0 rows: 0
- crew codes: {'L1': 11959, 'L2': 888, 'L3': 157, 'L4': 355, 'L5': 11}
- units: {'Ea': 11534, 'CLF': 1010, 'KLF': 735, 'LF': 36, 'Pr': 30, '100': 14, '500': 6, '1000': 3, '50': 1, 'MLF': 1}
- rows whose item is still a bare size (no heading found above on the page): 0

## Labor check (labor_usd vs manhours x 46.59)

- strict |diff| <= 0.02 USD: 6525/13370 = 48.80%
- publisher rounding (3 significant digits, book p.5 printed) or |diff| <= 0.02: 13277/13370 = 99.30%
- within one unit of the 3rd significant digit (book sometimes truncates, e.g. 0.39 x 46.59 = 18.17 printed 18.10): 13330/13370 = 99.70%
- rows failing all three (book errata candidates, kept as printed): 40

  - p.342 `#1 horz. elbows, 30 L1@0.20 Ea 241.00 11.60 252.60` -> expected 9.3180 (3 s.f. 9.32)
  - p.445 `5/8" dia x 8' long L1@1.70 Ea 23.30 73.30 96.60` -> expected 79.2030 (3 s.f. 79.20)
  - p.509 `Single 15 amp brown L1@0.41 Ea 22.40 19.00 41.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.509 `Single 15 amp ivory L1@0.41 Ea 22.40 19.00 41.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.509 `Single 15 amp white L1@0.41 Ea 22.40 19.00 41.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.510 `Single 15 amp brown L1@0.41 Ea 26.40 19.00 45.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.510 `Single 15 amp ivory L1@0.41 Ea 26.40 19.00 45.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.510 `Single 15 amp white L1@0.41 Ea 26.40 19.00 45.40` -> expected 19.1019 (3 s.f. 19.10)
  - p.511 `Single 15 amp brown L1@0.78 Ea 49.60 36.20 85.80` -> expected 36.3402 (3 s.f. 36.30)
  - p.511 `Single 15 amp ivory L1@0.78 Ea 49.60 36.20 85.80` -> expected 36.3402 (3 s.f. 36.30)
  - p.511 `Single 15 amp white L1@0.78 Ea 49.60 36.20 85.80` -> expected 36.3402 (3 s.f. 36.30)
  - p.512 `Single 15 amp brown L1@0.41 Ea 23.80 19.00 42.80` -> expected 19.1019 (3 s.f. 19.10)
  - p.512 `Single 15 amp ivory L1@0.41 Ea 23.80 19.00 42.80` -> expected 19.1019 (3 s.f. 19.10)
  - p.512 `Single 15 amp white L1@0.41 Ea 23.80 19.00 42.80` -> expected 19.1019 (3 s.f. 19.10)
  - p.512 `Single 15 amp brown L1@0.82 Ea 47.70 38.00 85.70` -> expected 38.2038 (3 s.f. 38.20)
  - p.512 `Single 15 amp ivory L1@0.82 Ea 47.70 38.00 85.70` -> expected 38.2038 (3 s.f. 38.20)
  - p.512 `Single 15 amp white L1@0.82 Ea 47.70 38.00 85.70` -> expected 38.2038 (3 s.f. 38.20)
  - p.513 `Single 15 amp brown L1@0.88 Ea 51.10 40.80 91.90` -> expected 40.9992 (3 s.f. 41.00)
  - p.513 `Single 15 amp ivory L1@0.88 Ea 51.10 40.80 91.90` -> expected 40.9992 (3 s.f. 41.00)
  - p.513 `Single 15 amp white L1@0.88 Ea 51.10 40.80 91.90` -> expected 40.9992 (3 s.f. 41.00)
  - p.514 `Single 15 amp brown L1@0.98 Ea 51.70 45.50 97.20` -> expected 45.6582 (3 s.f. 45.70)
  - p.514 `Single 15 amp ivory L1@0.98 Ea 51.70 45.50 97.20` -> expected 45.6582 (3 s.f. 45.70)
  - p.514 `Single 15 amp white L1@0.98 Ea 51.70 45.50 97.20` -> expected 45.6582 (3 s.f. 45.70)
  - p.515 `4-S-tile ring 1-1/4" L1@0.55 Ea 27.30 25.50 52.80` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 1-1/2" L1@0.55 Ea 30.20 25.50 55.70` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 2" L1@0.55 Ea 30.50 25.50 56.00` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 1-1/4" L1@0.55 Ea 27.30 25.50 52.80` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 1-1/2" L1@0.55 Ea 30.20 25.50 55.70` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 2" L1@0.55 Ea 30.50 25.50 56.00` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 1-1/4" L1@0.55 Ea 27.30 25.50 52.80` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 1-1/2" L1@0.55 Ea 30.20 25.50 55.70` -> expected 25.6245 (3 s.f. 25.60)
  - p.515 `4-S-tile ring 2" L1@0.55 Ea 30.50 25.50 56.00` -> expected 25.6245 (3 s.f. 25.60)
  - p.519 `48" 4 lamp L1@1.26 Ea 330.00 58.60 388.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp energy saver L1@1.26 Ea 353.00 58.60 411.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp L1@1.26 Ea 344.00 58.60 402.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp energy saver L1@1.26 Ea 367.00 58.60 425.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp L1@1.26 Ea 350.00 58.60 408.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp energy saver L1@1.26 Ea 387.00 58.60 445.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp L1@1.26 Ea 356.00 58.60 414.60` -> expected 58.7034 (3 s.f. 58.70)
  - p.519 `48" 4 lamp energy saver L1@1.26 Ea 392.00 58.60 450.60` -> expected 58.7034 (3 s.f. 58.70)

## Notes

- `page` = 1-based PDF page; printed page number = PDF page - 1 (checked on every table page; PDF 540 and 542 carry no printed number).
- PDF p.342 `#1 horz. elbows, 30 L1@0.20 ... 11.60`: 11.60 USD is 0.25 h x 46.59, not 0.20 h — printed inconsistency in the book, kept as printed.
- PDF p.445 `5/8" dia x 8' long L1@1.70 ... 73.30`: 73.30 USD is 1.57 h x 46.59 — printed inconsistency, kept as printed.
- Rows repeated verbatim in the book (same heading printed twice on PDF p.217 and p.251) are kept: 5 duplicate rows.
- Units `100`, `500`, `1000`, `50` are per-package quantities printed in the Unit column (wire connectors, PDF p.116-118).
- PDF p.423 has an Equipment cost column; its value is in `raw` only.

## Parser issues

- none
