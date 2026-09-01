# 11 · Risk Management & Performance Metrics

The shared evaluation backbone: walk-forward backtesting, Sharpe / Deflated-Sharpe / drawdown / VaR, P&L attribution, and a live risk dashboard used by every strategy section.

> Part of the **Quant Lab** — section 11 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Systematic strategy backtesting
- Sharpe ratio
- Maximum drawdown
- P&L attribution
- Walk-forward / out-of-sample validation
- Risk-adjusted return / alpha vs benchmark
- Value at Risk (VaR)
- Deflated Sharpe ratio
- Fill ratio / spread capture
- Hit rate / win rate
- Protection rate (defensive)
- Extreme-value-theory VaR/ES (POT/GPD)
- Expected-shortfall backtesting (Acerbi-Szekely)
- Copula tail-dependence

## Table B — Math & statistics (referenced)
- Hypothesis testing (bootstrap, Deflated Sharpe)
- Time-series analysis
- Monte Carlo simulation
- Extreme-value theory / tail modeling
- Regression
- Extreme-value theory (POT, GPD, Hill estimator)
- Copulas (t / Clayton, tail dependence)

## Table C — Technical & computational (referenced)
- Python
- Backtesting-engine design
- Walk-forward / purged CV
- Real-time dashboards / attribution analytics
- Data pipelines / ETL

## Upstox data sources
| Source | What it gives you |
|---|---|
| `portfolio_positions` | Intraday/derivative open positions and live P&L. |
| `portfolio_holdings` | Long-term holdings (delivery). |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `orders_trades` | Order placement, modification, and trade book (execution). |
| `funds_margin` | Available funds, used margin, exposure. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`11-01-backtest-validation-harness-shared-lib`](11-01-backtest-validation-harness-shared-lib) | **Backtest / validation harness (shared lib)** | Walk-forward, purged CV, Deflated Sharpe and bootstrap CIs — importable by all strategy sections. |
| [`11-02-var-expected-shortfall-engine`](11-02-var-expected-shortfall-engine) | **VaR / Expected-Shortfall engine** | Historical + Monte-Carlo VaR/ES on a live book. |
| [`11-03-live-p-l-risk-dashboard`](11-03-live-p-l-risk-dashboard) | **Live P&L & risk dashboard** | Stream positions and render exposures, drawdown and attribution in real time. |
| [`11-04-evt-tail-risk-engine`](11-04-evt-tail-risk-engine) | **EVT tail-risk engine** | Peaks-over-threshold GPD fits for VaR/ES in the tail; compare against historical and Gaussian VaR and backtest Expected Shortfall with the Acerbi-Szekely test. |
| [`11-05-copula-portfolio-tail-dependence`](11-05-copula-portfolio-tail-dependence) | **Copula portfolio tail-dependence** | Fit t and Clayton copulas to capture joint tail moves across an NSE book and stress joint drawdowns against a Gaussian-correlation baseline. |

## Research-paper bot
arXiv categories: `q-fin.RM`, `q-fin.ST`, `q-fin.PM`

Seed queries:
  - "deflated Sharpe ratio backtest overfitting"
  - "value at risk expected shortfall"
  - "probabilistic Sharpe ratio"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** _none_
- **Feeds:** [Portfolio Construction & Optimization](../08-portfolio-optimization)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
