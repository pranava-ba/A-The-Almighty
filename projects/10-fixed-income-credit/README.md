# 10 · Fixed Income & Credit

Construct yield curves from bond ETFs + public data, price fixed-income derivatives, and model credit default and stress. Note: Upstox is market data (equity/F&O/commodity/currency) — proxy rates via bond/GILT ETFs and combine with RBI/CCIL public yields.

> Part of the **Quant Lab** — section 10 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Fixed income / bond analytics
- Credit risk / default modeling
- Credit stress testing
- Option-Adjusted Spread (OAS)
- Yield-curve / yield-data covariance
- Insurance / loss modeling
- Rating-transition credit model (Jarrow-Lando-Turnbull)
- Risk-neutral survival / default probabilities
- Defaultable-bond pricing & credit spreads
- Options on defaultable bonds
- Credit hedging (rate vs credit separation)
- Short-rate / interest-rate models

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs (short-rate models)
- Numerical methods / integration
- Regression
- Time-series analysis
- Convex optimization
- Markov models (rating chain, absorbing default)
- Change of measure (Girsanov) & Feynman-Kac
- Martingales / optional stopping
- Measure theory / risk-neutral valuation

## Table C — Technical & computational (referenced)
- Python
- Machine learning (boosting for default)
- Data pipelines / ETL
- Excel / financial-modeling

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`10-01-yield-curve-from-gilt-bharat`](10-01-yield-curve-from-gilt-bharat) | **Yield curve from GILT/Bharat-Bond ETFs** | Fit a Nelson-Siegel curve from GILT/Bharat-Bond ETF prices + public RBI/CCIL yields. |
| [`10-02-ml-credit-default-model`](10-02-ml-credit-default-model) | **ML credit-default model** | Gradient-boosting default prediction on public financials; report AUC and stress-adjusted scores. |
| [`10-03-bond-etf-duration-carry-strategy`](10-03-bond-etf-duration-carry-strategy) | **Bond-ETF duration / carry strategy** | Duration-timed carry using liquid debt ETFs. |
| [`10-04-jarrow-lando-turnbull-defaultable-bond`](10-04-jarrow-lando-turnbull-defaultable-bond) | **Jarrow-Lando-Turnbull defaultable-bond engine (Indian credit)** | Reconstruct JLT from first principles: estimate a real-world rating-transition matrix from CRISIL/ICRA migration data, build the risk-neutral TPM Q̃=I+Π[Q−I], and price defaultable bonds, credit spreads and puts-on-risky-bonds; construct the exact rate-vs-credit hedge and verify monotonicity across rating grades. |
| [`10-05-risk-neutral-vs-real-world`](10-05-risk-neutral-vs-real-world) | **Risk-neutral vs real-world survival curves** | Compare risk-neutral survival probabilities (from the JLT engine) against real-world estimates from rating-transition data across grades and horizons; decompose the risky forward rate into risk-free + credit terms. |

## Research-paper bot
arXiv categories: `q-fin.PR`, `q-fin.RM`, `q-fin.MF`

Seed queries:
  - "term structure interest rate model"
  - "credit default prediction machine learning"
  - "Nelson Siegel yield curve"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Portfolio Construction & Optimization](../08-portfolio-optimization), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
