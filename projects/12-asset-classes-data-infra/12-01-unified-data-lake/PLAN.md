# 12-01 Unified data lake — build plan

The shared **DuckDB** store of record for every candle we pull (Upstox / NSE bhavcopy /
yfinance), normalized to one schema and keyed by `(instrument_key, interval, ts)`. Draws
on the old `p01-market-data-foundation/PROJECT_SPEC.md` (which spans all of section 12),
reconciled to the portfolio conventions.

## Built (token-free, runs offline; live yfinance verified)
- `src/datalake/schema.py` — canonical schema (`instrument_key, interval, ts, o/h/l/c,
  volume, oi, source`), DuckDB DDL, and `normalize()` (tz-aware IST, naive→IST).
- `src/datalake/store.py` — `DuckDBStore`: idempotent `upsert_candles` (INSERT … ON
  CONFLICT so a re-pull never duplicates), `read_candles`, `count`.
- `src/datalake/sources/` — `MarketData` protocol + registry; **four adapters**:
  `YFinanceSource` + `NSEBhavcopySource` (keyless), `UpstoxSource` + `BullseyeSeedSource`
  (**private/gitignored** — token / local DB). `ingest.backfill()` ties source → store;
  `schema.canonical()` handles many-instrument frames (full bhavcopy).
- `tests/` — **15 green offline** (store, yfinance, NSE, Upstox, Bullseye-seed; no
  network/token). Live verified: yfinance `^NSEI` → DuckDB; NSE bhavcopy `2026-08-27` →
  3,624 rows; **Bullseye seed → 375 real 1-min SENSEX bars** into the lake. Upstox: opt-in
  smoke with `UPSTOX_ACCESS_TOKEN`.

## Architecture decision
- The reusable core lives **here in `src/datalake/` for now**; once a 2nd subproject needs
  it, promote it to `quant_lab/common/marketdata/` (and un-ignore the public parts).
- **Adapters split by trust:** yfinance + NSE bhavcopy are **keyless/public**; the Upstox
  adapter is **private** (needs a token, gitignored, never shipped).
- **No data is committed** — DuckDB file is gitignored; reproduce via the free sources.

## Next
1. F&O bhavcopy (OI/settlement) as an extension of the NSE adapter.
2. `reconcile()` — cross-check candles across sources, flag bad prints, per-instrument
   data-quality scorecard (subproject `12-05`).
3. Symbology normalizer (`12-03`) — map Yahoo tickers ↔ NSE symbols ↔ Upstox
   instrument_keys so one canonical key spans all three sources.
4. Option chain + India VIX (Upstox) for the volatility/derivatives sections.

## Resolved (2026-08-28)
Upstox token confirmed working; yfinance + NSE confirmed as the free keyless sources.
