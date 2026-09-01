# 07 · Market Microstructure & Execution

Study the limit order book, build order-imbalance / micro-price signals, and schedule large orders with Almgren-Chriss optimal execution.

> Part of the **Quant Lab** — section 07 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Limit order book / matching engine
- Transaction-cost / slippage modeling
- Order flow / order imbalance
- Market impact modeling
- VWAP / execution benchmarks
- Tick-level / odd-lot microstructure factors
- Optimal execution (Almgren-Chriss)
- Micro-price / OBI analytics
- Closing-auction dynamics
- ETF rebalancing / mechanics
- Optimal execution as a Markov Decision Process
- Regime-switching / stochastic liquidity
- Information-based microstructure (Kyle, Glosten-Milgrom)

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs
- Time-series analysis
- Regression
- Numerical methods / integration
- Convex optimization
- Dynamic programming / Bellman / HJB (stochastic control)
- Markov models (chains, MDPs)
- Linear algebra / spectral-gap analysis

## Table C — Technical & computational (referenced)
- Python
- C++ (matching engine)
- Low-latency / lock-free / SIMD
- Big-data / tick-data engineering
- Concurrency / multithreading
- Backtesting-engine design

## Upstox data sources
| Source | What it gives you |
|---|---|
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `intraday_candles` | Current-day intraday OHLCV candles for near-tick studies. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`07-01-almgren-chriss-optimal-execution`](07-01-almgren-chriss-optimal-execution) | **Almgren-Chriss optimal execution** | Schedule a large NIFTY order to minimize impact + timing risk; compare vs TWAP/VWAP. |
| [`07-02-order-book-imbalance-micro-price`](07-02-order-book-imbalance-micro-price) | **Order-book imbalance & micro-price signal** | From the depth feed, build OBI/micro-price features to predict short-horizon returns. |
| [`07-03-impact-slippage-model`](07-03-impact-slippage-model) | **Impact / slippage model** | Fit a market-impact curve from your own executions and tick data. |
| [`07-04-liquidity-regimes-markov-chain-optimal`](07-04-liquidity-regimes-markov-chain-optimal) | **Liquidity regimes (Markov chain) + optimal execution as an MDP** | Classify NIFTY/BANKNIFTY intraday liquidity into Deep/Normal/Shallow/Crisis states from the depth feed, fit the transition matrix, and solve execution as an MDP (value iteration; prove the Bellman contraction). Report the transition matrix's spectral gap and derive spectral-gap-based liquidity-fragility and crisis-absorption measures, then benchmark cost against Almgren-Chriss / TWAP / VWAP; sketch the continuous-time HJB extension. |

## Research-paper bot
arXiv categories: `q-fin.TR`, `q-fin.CP`, `q-fin.MF`

Seed queries:
  - "optimal execution Almgren Chriss"
  - "order book imbalance price impact"
  - "limit order book microstructure"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Statistical Arbitrage & Relative Value](../05-statistical-arbitrage), [Market Making](../06-market-making), [Market Simulation & Agent-Based / Behavioral Finance](../14-market-simulation-abm)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
