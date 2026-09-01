# 02 · Volatility Modeling & Trading

Estimate realized vol, fit implied-vol surfaces and stochastic-vol models, detect regimes, and trade the vol-risk premium.

> Part of the **Quant Lab** — section 02 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Volatility forecasting
- Realized-vol estimators
- Regime-switching volatility (DS3M / hybrid rough-regime)
- Volatility surface / regime analysis
- Heston stochastic-vol model
- Rough volatility (rough Bergomi, Hurst, fBM)
- SABR model
- SVI surface
- Jump-diffusion model
- Implied-tail / higher-moment trading
- Volatility / roughness risk premium
- Short-volatility arbitrage

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs
- Time-series analysis (EWMA, Kalman, ARIMA)
- Fractional Brownian motion / rough paths
- Realized-volatility estimators (Parkinson, Yang-Zhang)
- Hurst exponent / long memory
- Monte Carlo simulation

## Table C — Technical & computational (referenced)
- Python (NumPy/Pandas/SciPy)
- PyTorch (vol-forecasting nets)
- Big-data / tick-data engineering
- Backtesting-engine design
- Deep learning (surrogate vol-surface calibration)

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `option_chain` | Option chain by underlying+expiry with per-strike IV, greeks (Δ Γ Θ ν ρ), OI, LTP. |
| `india_vix` | India VIX index level (via index quote) for volatility regime work. |
| `intraday_candles` | Current-day intraday OHLCV candles for near-tick studies. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`02-01-india-vix-vs-realized-vol`](02-01-india-vix-vs-realized-vol) | **India VIX vs realized-vol premium** | Compute Parkinson/Yang-Zhang realized vol from candles vs the India VIX level; trade the implied-realized premium. |
| [`02-02-sabr-svi-surface-fitter`](02-02-sabr-svi-surface-fitter) | **SABR / SVI surface fitter** | Fit SABR and SVI to the NIFTY chain; classify low/high-vol regimes by VIX bands and study surface dynamics. |
| [`02-03-rough-vol-hurst-estimator`](02-03-rough-vol-hurst-estimator) | **Rough-vol Hurst estimator** | Estimate the Hurst exponent on intraday NIFTY to test roughness across regimes; compare to rough-Bergomi simulation. |
| [`02-04-neural-network-vol-surface-calibration`](02-04-neural-network-vol-surface-calibration) | **Neural-network vol-surface calibration** | Deep-calibrate the NIFTY IV surface with a small neural network (Horvath-style deep-learning surrogate) and benchmark speed/accuracy against SABR/SVI least-squares fits. |

## Research-paper bot
arXiv categories: `q-fin.ST`, `q-fin.PR`, `q-fin.CP`

Seed queries:
  - "rough volatility Hurst exponent"
  - "volatility forecasting regime switching"
  - "SABR SVI implied volatility surface"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra), [Machine Learning & Alternative Data](../15-ml-alt-data)
- **Feeds:** [Derivatives & Options Pricing](../01-derivatives-options-pricing), [Hedging & Greeks](../03-hedging-greeks), [Systematic Trading Strategies](../04-systematic-trading), [Statistical Arbitrage & Relative Value](../05-statistical-arbitrage), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
