# The data foundation

Everything downstream — every price, every backtest — flows through one small library,
`datalake`. It gives the whole portfolio a single, normalized, reproducible view of the
market so no strategy ever has to care where a candle came from.

## Use it

Pull candles from any source into a DuckDB store, then read them back:

```python
from datalake import DuckDBStore, backfill
from datalake.sources import YFinanceSource

store = DuckDBStore("lake.duckdb")                      # or ":memory:"
backfill(store, YFinanceSource(), "^NSEI", "1day",
         start="2026-01-01", end="2026-08-28")          # Nifty 50, keyless
df = store.read_candles("^NSEI", "1day")                # tz-aware IST, canonical columns
```

Every source returns the **same schema** — `instrument_key, interval, ts, open, high, low,
close, volume, oi, source` — so they are interchangeable and mixable.

| Source | Auth | What it's for |
|---|---|---|
| `YFinanceSource` | none | index/ETF/stock EOD + shallow intraday |
| `NSEBhavcopySource` | none | official EOD equity (and F&O with OI) |
| `UpstoxSource` | token | intraday candles, option chain, quotes *(private)* |
| `BullseyeSeedSource` | none | a large local 1-minute history seed *(private)* |

**Trust the data.** Reconcile the same instrument across sources to catch bad prints and
fill gaps, and get a quality scorecard:

```python
from datalake import reconcile
merged, scorecard = reconcile({"yfinance": a, "nse_bhavcopy": b}, primary="nse_bhavcopy")
scorecard["cross_source_mismatches"], scorecard["coverage"]
```

**Avoid the classic traps** (see {doc}`foundations/01_what_is_a_backtest`):

```python
from datalake import PointInTimeUniverse, adjust_candles, Symbology
universe.members_asof("NIFTY50", "2019-06-01")   # survivorship-safe membership
adjust_candles(df, corporate_actions)            # back-adjust splits/bonuses/dividends
Symbology.yahoo("RELIANCE")                       # 'RELIANCE.NS' — one key across sources
```

## Understand it

- **Why DuckDB, not files.** A single embedded columnar database is the store of record —
  idempotent upserts (re-pulling an overlapping window never duplicates a bar), SQL for ad-hoc
  slicing, and no scattered CSVs to drift. Nothing but the code and tiny samples is committed;
  the raw data is rebuilt locally from the free sources.
- **One protocol, many sources.** Each adapter implements a single `candles()` method and
  registers itself; a strategy asks the lake for `("NSE_INDEX|Nifty 50", "1minute")` and never
  learns which feed answered.
- **Honesty built in.** Point-in-time membership and corporate-action adjustment are not
  optional extras bolted on later — they're in the data layer so a backtest *cannot* see the
  future or a survivor-only universe by accident.

:::{admonition} Limitations — be candid
:class: warning
The free sources are unofficial and rate-limited; NSE occasionally blocks automated pulls.
Upstox's 1-minute history caps at ~6 months, so long intraday history is built by
accumulating going forward and cross-referencing the local seed. Live option-chain Greeks are
snapshot-only; IV/Greek *history* must be recomputed offline.
:::

*Reproduce the SENSEX tearsheet in {doc}`evaluation` with the `BullseyeSeedSource` + `evalkit`.*
