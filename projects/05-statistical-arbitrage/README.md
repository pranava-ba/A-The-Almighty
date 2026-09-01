# 05 · Statistical Arbitrage & Relative Value

Screen cointegrated pairs, trade Z-score spreads with borrow/slippage, and exploit index-futures basis and calendar spreads.

> Part of the **Quant Lab** — section 05 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Statistical arbitrage / pairs trading
- Cointegration trading (Engle-Granger, ADF)
- Relative-value trading
- Commodity spread trading
- Risk-free / triangular arbitrage
- Ornstein-Uhlenbeck spread trading (optimal bands)
- Kalman dynamic hedge ratio

## Table B — Math & statistics (referenced)
- Cointegration / stationarity tests (Engle-Granger, ADF)
- Time-series analysis
- Linear algebra / matrix decompositions
- Hypothesis testing
- Convex optimization
- Ornstein-Uhlenbeck / mean-reversion (half-life, first-passage)
- Kalman filtering / state-space cointegration

## Table C — Technical & computational (referenced)
- Python (Pandas/statsmodels)
- Backtesting-engine design
- Walk-forward / purged CV
- SQL / databases

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`05-01-cointegration-pairs-engine-nse`](05-01-cointegration-pairs-engine-nse) | **Cointegration pairs engine (NSE)** | ADF/Engle-Granger screen across a sector; Z-score state machine with borrow costs and slippage; per-pair & portfolio reporting. |
| [`05-02-index-futures-basis-calendar-spread`](05-02-index-futures-basis-calendar-spread) | **Index-futures basis & calendar spread** | Trade NIFTY future-vs-spot basis and near/far calendar spreads. |
| [`05-03-etf-vs-constituent-basket-arbitrage`](05-03-etf-vs-constituent-basket-arbitrage) | **ETF vs constituent-basket arbitrage** | Track a Nifty ETF against its synthetic basket for dislocations. |
| [`05-04-ou-calibrated-pairs-with-optimal`](05-04-ou-calibrated-pairs-with-optimal) | **OU-calibrated pairs with optimal bands** | Model each spread as an Ornstein-Uhlenbeck process; estimate the half-life and derive entry/exit thresholds that maximise expected return per unit time (first-passage), then walk-forward with borrow and slippage costs. |
| [`05-05-kalman-dynamic-hedge-ratio-pairs`](05-05-kalman-dynamic-hedge-ratio-pairs) | **Kalman dynamic hedge-ratio pairs** | Estimate a time-varying hedge ratio with a Kalman filter (state-space cointegration) and compare stability and P&L against a static-OLS hedge ratio. |

## Research-paper bot
arXiv categories: `q-fin.TR`, `q-fin.ST`, `q-fin.PM`

Seed queries:
  - "statistical arbitrage pairs trading cointegration"
  - "Ornstein Uhlenbeck mean reversion trading"
  - "index arbitrage futures basis"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Market Microstructure & Execution](../07-microstructure-execution), [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Portfolio Construction & Optimization](../08-portfolio-optimization), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
