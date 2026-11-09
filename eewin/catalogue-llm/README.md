# DRE Électrique – LLM estimating catalog

Lets Claude (or another LLM) build priced estimates from the ACCEO Estimation (EEWin) data:
material prices (Lumen), labor times, assemblies and 3,698 past quotes.
**The LLM only picks items and quantities; all prices, unit conversions and totals are computed by code.**

## Two copies, same results
| | Local | Cloud (Supabase `dre-estimation`, ca-central-1) |
|---|---|---|
| Data | `data/dre.sqlite` (built from EEWin) | tables `products`, `assemblies`, … (RLS on, no direct access) |
| Tools | MCP server `dre-estimation` (Claude Code + Claude Desktop) | SQL functions `search_products`, `search_assemblies`, `get_item`, `price_estimate`, `labor_rates_list` (service role only) |
| Use | "Estimate 12 duplex receptacles and 40 ft of EMT 3/4" in Claude | Claude via the Supabase connector: `select price_estimate('[{"code":"…","qty":12}]')` |

Local and cloud were checked against each other: 300 random lines identical, totals identical to the cent.

## Refresh after a price update in ACCEO
```powershell
.\scripts\refresh.ps1            # VM export -> dre.sqlite -> tests -> cloud
.\scripts\refresh.ps1 -SkipCloud # local only
```
The cloud step needs the service_role key in `.env` (`SUPABASE_SERVICE_ROLE_KEY=...`, from Supabase >
Project Settings > API keys). `.env` is git-ignored. The cloud swap is atomic and refuses incomplete data.

## Estimate rules (validated)
- Recomputing 777 past quotes (2015+) with their saved prices: **material matches EEWin on 99.5%**.
- Assemblies use their stored labor time (as EEWin does); final quote hours are often rounded up by the estimator.
- Quantity default unit: each for items priced per 100/1000, feet for per 100/1000 ft, metres for per km.
- Products with no catalog labor time get the median from past quotes (flagged "labor estimated").
- Every missing price / labor time / unknown code is returned as a warning and highlighted in the Excel quote.
- Totals are the sum of rounded lines, rounded half-up (same in Python and Postgres).

## Layout
- `scripts/extract_from_eewin.ps1` – export EEWin tables from the Hyper-V VM (`EEWin2_zip`) to `data/raw`
- `scripts/build_db.py` – build `data/dre.sqlite` (search text, usage counts, labor fallback)
- `scripts/validate_quotes.py` – recompute past quotes and compare with EEWin totals
- `scripts/sync_cloud.py` – push to Supabase
- `src/dre_estimation/` – `engine.py` (math), `search.py` (FR/EN matching), `store.py`, `xlsx.py`, `server.py` (MCP)
- `out/` – generated Excel quotes
