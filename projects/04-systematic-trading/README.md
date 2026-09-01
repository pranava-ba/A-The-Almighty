# 04 · Systematic Trading Strategies

Build momentum, mean-reversion, breakout, macro-event and regime-switching strategies on Indian equities with rigorous walk-forward validation.

> Part of the **Quant Lab** — section 04 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Momentum / trend-following
- Mean-reversion
- Technical indicators (SMA, Bollinger, rolling averages)
- Cross-asset / regime-switching allocation
- Long/short equity (market-neutral)
- Breakout strategy
- Macro / event-driven trading
- Post-earnings drift
- Financial contagion / cross-market transmission

## Table B — Math & statistics (referenced)
- Time-series analysis
- Regression (OLS, Ridge, Lasso)
- Hypothesis testing
- Markov models (regime)
- Econometrics / panel data
- Markov regime-switching (Hamilton filter)
- VAR / Granger causality / impulse response
- Endogeneity / instrumental variables / 2SLS
- Jump detection / jump processes

## Table C — Technical & computational (referenced)
- Python (Pandas)
- Backtesting-engine design
- Walk-forward / purged CV / leakage control
- Machine learning (tree ensembles)
- Data pipelines / ETL

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `intraday_candles` | Current-day intraday OHLCV candles for near-tick studies. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `market_quote_ltp` | Last traded price for many instruments in one call. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`04-01-cross-sectional-momentum-on-nifty`](04-01-cross-sectional-momentum-on-nifty) | **Cross-sectional momentum on Nifty-500** | Rank the universe on trailing return, rebalance monthly, validate walk-forward with transaction costs. |
| [`04-02-regime-switched-trend-mean-reversion`](04-02-regime-switched-trend-mean-reversion) | **Regime-switched trend / mean-reversion** | Use an SMA/vol regime filter to flip between continuation and reversal books. |
| [`04-03-event-study-rbi-policy-budget`](04-03-event-study-rbi-policy-budget) | **Event study: RBI policy / budget / earnings** | Measure post-event drift and build an event-driven overlay. |
| [`04-04-cross-market-jump-contagion-us`](04-04-cross-market-jump-contagion-us) | **Cross-market jump contagion (US/SGX → Nifty)** | Test overnight transmission from US/SGX moves into the next-day Nifty open using a predetermined-regressor design off the time-zone gap; White-robust OLS + full diagnostics, 2SLS endogeneity check, bivariate VAR/Granger, jump detection, and crisis-interaction regressions separating contagion from interdependence (Forbes-Rigobon). |
| [`04-05-two-state-markov-regime-switching`](04-05-two-state-markov-regime-switching) | **Two-state Markov regime-switching risk monitor** | Estimate a Hamilton regime-switching model on index returns (calm vs crisis volatility) and drive a risk-on/off overlay off the smoothed crisis-regime probability; validate against out-of-sample stress episodes. |

## Research-paper bot
arXiv categories: `q-fin.TR`, `q-fin.PM`, `q-fin.ST`

Seed queries:
  - "cross-sectional momentum equity returns"
  - "regime switching trading strategy"
  - "post earnings announcement drift"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Factor / Alpha Research](../09-factor-alpha-research), [Machine Learning & Alternative Data](../15-ml-alt-data), [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Portfolio Construction & Optimization](../08-portfolio-optimization), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
