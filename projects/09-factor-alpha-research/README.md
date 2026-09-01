# 09 · Factor / Alpha Research

Build a multi-factor library (value/momentum/low-vol/quality + microstructure + sentiment), evaluate by IC/RankIC, and neutralize style exposures.

> Part of the **Quant Lab** — section 09 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Alpha signal generation
- Multi-factor models
- Sentiment factor (news NLP)
- Information Coefficient (IC / RankIC)
- Return-direction prediction
- Factor neutralization / style exposure
- Barra risk model (CNE6)
- Turnover / self-correlation control
- Nowcasting (mixed-frequency)
- Fama-MacBeth priced-factor testing
- Backtest-overfitting control (deflated Sharpe, PBO)

## Table B — Math & statistics (referenced)
- Regression
- Dimensionality reduction (PCA)
- Information Coefficient / rank statistics
- Time-series analysis (Kalman nowcasting)
- Hypothesis testing
- Fama-MacBeth / Newey-West standard errors
- Multiple-testing / combinatorial-purged CV

## Table C — Technical & computational (referenced)
- Python (Pandas)
- Machine learning (tree ensembles)
- NLP / LLMs (FinBERT)
- Data pipelines / ETL
- PyTorch

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `option_chain` | Option chain by underlying+expiry with per-strike IV, greeks (Δ Γ Θ ν ρ), OI, LTP. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`09-01-multi-factor-library-on-nse`](09-01-multi-factor-library-on-nse) | **Multi-factor library on NSE** | Value/momentum/low-vol/quality factors with IC/RankIC evaluation and cross-sectional neutralization. |
| [`09-02-news-sentiment-factor-finbert`](09-02-news-sentiment-factor-finbert) | **News-sentiment factor (FinBERT)** | Score headlines with FinBERT and test the sentiment factor's RankIC and turnover. |
| [`09-03-option-oi-positioning-factor`](09-03-option-oi-positioning-factor) | **Option-OI positioning factor** | Derive a positioning/flow factor from the option chain OI and test it. |
| [`09-04-fama-macbeth-priced-factor-test`](09-04-fama-macbeth-priced-factor-test) | **Fama-MacBeth priced-factor test** | Estimate cross-sectional factor risk premia with Fama-MacBeth and Newey-West standard errors on the NSE cross-section; test which factors are actually priced. |
| [`09-05-backtest-overfit-aware-factor-search`](09-05-backtest-overfit-aware-factor-search) | **Backtest-overfit-aware factor search** | Search a factor zoo under combinatorial-purged cross-validation with the deflated Sharpe and probability-of-backtest-overfitting to control false discoveries. |

## Research-paper bot
arXiv categories: `q-fin.PM`, `q-fin.ST`, `q-fin.TR`

Seed queries:
  - "equity factor investing cross section of returns"
  - "alpha signal information coefficient"
  - "news sentiment stock returns FinBERT"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Machine Learning & Alternative Data](../15-ml-alt-data), [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Systematic Trading Strategies](../04-systematic-trading), [Portfolio Construction & Optimization](../08-portfolio-optimization)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
