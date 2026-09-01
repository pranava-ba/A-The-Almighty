# 15 · Machine Learning & Alternative Data

The ML + research hub. Hosts the arXiv/SSRN research-paper bot and the NLP/alt-data sentiment pipeline; trains sequence models on Upstox candles and feeds signals to the pricing, factor, and simulation sections.

> Part of the **Quant Lab** — section 15 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Sentiment factor (news NLP)
- Alpha signal generation
- Return-direction prediction
- Nowcasting (mixed-frequency)
- Cross-asset / regime-switching allocation (ML regime)
- Stress testing / scenario analysis (ML)

## Table B — Math & statistics (referenced)
- Regression
- Dimensionality reduction (PCA / t-SNE / UMAP)
- Clustering (K-Means)
- Hypothesis testing
- Time-series analysis
- Bayesian & frequentist inference

## Table C — Technical & computational (referenced)
- Python
- Machine learning (tree ensembles / boosting)
- Deep learning (CNN / RNN / LSTM / Transformer)
- NLP / LLMs (BERT / FinBERT / GPT)
- PyTorch / TensorFlow
- Hyperparameter optimization
- Generative models (GANs for risk / synthetic data)
- Reinforcement learning (deep hedging, execution)
- scikit-learn
- API integration / web scraping

## Upstox data sources
| Source | What it gives you |
|---|---|
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `option_chain` | Option chain by underlying+expiry with per-strike IV, greeks (Δ Γ Θ ν ρ), OI, LTP. |
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `intraday_candles` | Current-day intraday OHLCV candles for near-tick studies. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`15-01-research-paper-bot`](15-01-research-paper-bot) | **Research-paper bot** | Fetch arXiv q-fin (and SSRN) papers per section, dedup, tag, and emit a weekly digest — productionizes common/paper_fetcher.py. |
| [`15-02-sequence-models-for-return-vol`](15-02-sequence-models-for-return-vol) | **Sequence models for return/vol forecasting** | LSTM / Transformer on candles with walk-forward evaluation; export signals downstream. |
| [`15-03-news-alt-data-sentiment-pipeline`](15-03-news-alt-data-sentiment-pipeline) | **News / alt-data sentiment pipeline** | FinBERT sentiment on news feeds → sentiment factor consumed by Factor/Alpha (09). |
| [`15-04-generative-scenarios-for-risk-gan`](15-04-generative-scenarios-for-risk-gan) | **Generative scenarios for risk (GAN / diffusion)** | Train a GAN/diffusion model on index-return histories to generate synthetic stress scenarios for VaR/ES and portfolio stress-testing (11), validated against historical crises. |

## Research-paper bot
arXiv categories: `q-fin.CP`, `q-fin.ST`, `q-fin.TR`

Seed queries:
  - "machine learning stock return prediction"
  - "deep learning limit order book"
  - "large language models finance"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Derivatives & Options Pricing](../01-derivatives-options-pricing), [Volatility Modeling & Trading](../02-volatility-modeling), [Systematic Trading Strategies](../04-systematic-trading), [Factor / Alpha Research](../09-factor-alpha-research), [Corporate Finance & Valuation (IB/PE)](../13-corporate-finance-valuation), [Market Simulation & Agent-Based / Behavioral Finance](../14-market-simulation-abm)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
