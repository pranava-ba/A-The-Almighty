# 12 · Asset Classes & Data Infrastructure

The foundational data layer: ingest instruments and candles across all Upstox segments into a local lake, record the websocket feed for replay, and normalize symbology.

> Part of the **Quant Lab** — section 12 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Equities (single-stock & index)
- FX / currencies
- Commodities
- Crypto / digital assets (via external feeds)
- Prediction markets (external)
- Real estate (external)
- Point-in-time / survivorship-bias-free data
- Corporate-action adjustment (splits, bonus, dividends)

## Table B — Math & statistics (referenced)
- Time-series analysis
- Probability & statistics (core)
- Dimensionality reduction
- Data reconciliation / cross-source validation

## Table C — Technical & computational (referenced)
- Python (Pandas)
- SQL / databases (DuckDB/Postgres)
- Big-data / tick-data engineering
- API integration / web scraping
- Data pipelines / ETL
- Docker / FastAPI
- kdb+/q
- Version control / dev tooling

## Upstox data sources
| Source | What it gives you |
|---|---|
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `intraday_candles` | Current-day intraday OHLCV candles for near-tick studies. |
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`12-01-unified-data-lake`](12-01-unified-data-lake) | **Unified data lake** | Ingest instruments + candles across NSE_EQ/NSE_FO/MCX_FO/NSE_CD/BSE_EQ into Parquet/DuckDB with incremental updates. |
| [`12-02-websocket-tape-recorder`](12-02-websocket-tape-recorder) | **Websocket tape recorder** | Capture depth/LTP to disk for deterministic strategy replay. |
| [`12-03-symbology-normalizer`](12-03-symbology-normalizer) | **Symbology normalizer** | Map instrument keys/tickers consistently across segments and corporate actions. |
| [`12-04-point-in-time-universe-corporate`](12-04-point-in-time-universe-corporate) | **Point-in-time universe & corporate-action engine** | Build survivorship-bias-free, point-in-time index membership plus a split/bonus/dividend adjustment layer so every backtest sees only what was knowable at the time. |
| [`12-05-cross-source-reconciliation-gap-fill`](12-05-cross-source-reconciliation-gap-fill) | **Cross-source reconciliation & gap-fill** | reconcile() candles across Upstox / NSE / yfinance to flag bad prints and fill gaps, emitting a per-instrument data-quality scorecard. |

## Research-paper bot
arXiv categories: `q-fin.CP`, `q-fin.TR`, `q-fin.GN`

Seed queries:
  - "market data infrastructure high frequency"
  - "financial time series database"
  - "tick data storage compression"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** _none_
- **Feeds:** [Derivatives & Options Pricing](../01-derivatives-options-pricing), [Volatility Modeling & Trading](../02-volatility-modeling), [Systematic Trading Strategies](../04-systematic-trading), [Statistical Arbitrage & Relative Value](../05-statistical-arbitrage), [Market Making](../06-market-making), [Market Microstructure & Execution](../07-microstructure-execution), [Portfolio Construction & Optimization](../08-portfolio-optimization), [Factor / Alpha Research](../09-factor-alpha-research), [Fixed Income & Credit](../10-fixed-income-credit), [Market Simulation & Agent-Based / Behavioral Finance](../14-market-simulation-abm)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
