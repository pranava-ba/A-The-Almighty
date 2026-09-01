# 08 · Portfolio Construction & Optimization

Construct MVO, risk-parity, minimum-variance and regime/cluster portfolios with shrinkage and real-world constraints, and stress-test them.

> Part of the **Quant Lab** — section 08 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Mean-variance / Markowitz optimization
- Efficient frontier
- Portfolio constraints (sector caps, no-short, neutrality)
- Dynamic rebalancing
- Position / bet sizing
- Stress testing / scenario analysis
- Convex optimization for portfolios (cvxpy/MOSEK)
- Regime / clustering-based construction
- Beta-neutral / minimum-risk portfolio
- Covariance / correlation shrinkage
- Black-Litterman (views + equilibrium)
- Hierarchical Risk Parity (HRP)
- Mean-CVaR / tail-risk optimization

## Table B — Math & statistics (referenced)
- Convex optimization
- Linear algebra / matrix decompositions
- Dimensionality reduction (PCA)
- Clustering (K-Means, Davies-Bouldin)
- Regression
- Monte Carlo simulation
- Random matrix theory (eigenvalue clipping)
- Robust / CVaR optimization (Rockafellar-Uryasev)

## Table C — Technical & computational (referenced)
- Python (cvxpy)
- Machine learning
- Deep learning (autoencoder clustering)
- Data pipelines / ETL

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `portfolio_holdings` | Long-term holdings (delivery). |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`08-01-nifty-50-mvo-with-shrinkage`](08-01-nifty-50-mvo-with-shrinkage) | **Nifty-50 MVO with shrinkage + constraints** | cvxpy MVO with Ledoit-Wolf shrinkage, sector caps and no-short; trace the efficient frontier. |
| [`08-02-regime-cluster-portfolio`](08-02-regime-cluster-portfolio) | **Regime / cluster portfolio** | K-Means or autoencoder low-correlation clusters for dynamic allocation (net of costs). |
| [`08-03-risk-parity-vs-min-variance`](08-03-risk-parity-vs-min-variance) | **Risk-parity vs min-variance vs beta-neutral** | Compare construction schemes on an NSE universe with walk-forward rebalancing. |
| [`08-04-black-litterman-with-explicit-views`](08-04-black-litterman-with-explicit-views) | **Black-Litterman with explicit views** | Combine market-implied equilibrium returns with a few explicit views and their confidences; compare allocations and out-of-sample stability against plain MVO. |
| [`08-05-hrp-vs-mvo-under-estimation`](08-05-hrp-vs-mvo-under-estimation) | **HRP vs MVO under estimation error** | Hierarchical Risk Parity vs MVO on an NSE universe, stressing the covariance with random-matrix-theory eigenvalue clipping; compare turnover and out-of-sample risk. |
| [`08-06-mean-cvar-tail-optimizer`](08-06-mean-cvar-tail-optimizer) | **Mean-CVaR tail optimizer** | Optimize mean-CVaR via the Rockafellar-Uryasev LP and compare tail behaviour and drawdowns against mean-variance. |

## Research-paper bot
arXiv categories: `q-fin.PM`, `q-fin.RM`, `q-fin.CP`

Seed queries:
  - "mean variance portfolio optimization shrinkage"
  - "risk parity portfolio construction"
  - "clustering based portfolio selection"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Factor / Alpha Research](../09-factor-alpha-research), [Risk Management & Performance Metrics](../11-risk-performance)
- **Feeds:** _none_

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
