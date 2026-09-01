# 13 · Corporate Finance & Valuation (IB/PE)

DCF/LBO/comps valuation with Monte-Carlo scenarios and NLP-extracted financials. Upstox supplies market-implied inputs (price, market cap/EV); fundamentals come from filings/screeners.

> Part of the **Quant Lab** — section 13 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- DCF valuation
- Due diligence / investment screening
- Financial-statement / P&L analysis
- Trading comparables (comps)
- M&A analysis
- LBO modeling
- IRR / equity multiple / cash-on-cash
- Real-estate underwriting
- Market sizing / demand forecasting
- Reverse-DCF / market-implied expectations
- Real-options valuation (binomial/BSM on projects)

## Table B — Math & statistics (referenced)
- Regression
- Probability & statistics (core)
- Monte Carlo simulation (scenario)
- Numerical methods (IRR root-finding)
- Global sensitivity analysis (Sobol indices)

## Table C — Technical & computational (referenced)
- Python
- Excel / VBA / financial-modeling tools
- NLP / LLMs (filings extraction)
- Machine learning (comps / KNN)
- Data pipelines / ETL

## Upstox data sources
| Source | What it gives you |
|---|---|
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`13-01-automated-comps-engine-nse-sector`](13-01-automated-comps-engine-nse-sector) | **Automated comps engine (NSE sector)** | KNN comps with sector/size distance metrics; pull market cap/EV from live quotes. |
| [`13-02-dcf-monte-carlo-scenario-valuation`](13-02-dcf-monte-carlo-scenario-valuation) | **DCF + Monte-Carlo scenario valuation** | Probabilistic DCF with sensitivity/tornado analysis and IRR. |
| [`13-03-filings-nlp-extractor`](13-03-filings-nlp-extractor) | **Filings NLP extractor** | LLM-parse annual reports into a structured financial-statement dataset. |
| [`13-04-reverse-dcf-implied-expectations-screen`](13-04-reverse-dcf-implied-expectations-screen) | **Reverse-DCF implied-expectations screen** | Invert the DCF to solve for the growth/margin the current price implies, and rank an NSE sector to flag rich vs cheap embedded expectations. |
| [`13-05-real-options-project-valuation`](13-05-real-options-project-valuation) | **Real-options project valuation** | Value a capex/expansion option with a binomial/BSM real-options model over Monte-Carlo scenario trees, with Sobol sensitivity on the key value drivers. |

## Research-paper bot
arXiv categories: `q-fin.GN`, `q-fin.EC`, `q-fin.PM`

Seed queries:
  - "discounted cash flow valuation uncertainty"
  - "comparable company valuation machine learning"
  - "financial statement analysis NLP"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Machine Learning & Alternative Data](../15-ml-alt-data)
- **Feeds:** [Portfolio Construction & Optimization](../08-portfolio-optimization)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
